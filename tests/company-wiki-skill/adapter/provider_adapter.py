#!/usr/bin/env python3
"""Deterministic local document adapter for company-wiki lifecycle tests.

The adapter exposes bounded source reads and wiki writes through logical targets. Scenario configuration and
events live outside source, wiki, and registry roots so product behavior cannot mistake harness state for
organization data. Fault controls model permission denial and non-atomic provider writes.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


class AdapterError(Exception):
    """A safe, content-free adapter failure."""


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)
    required = {"source_roots", "wiki_root", "event_log"}
    missing = sorted(required - config.keys())
    if missing:
        raise AdapterError(f"configuration missing: {', '.join(missing)}")
    return config


def is_contained(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_relative(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise AdapterError("target must be a non-empty relative path")
    resolved_root = root.resolve(strict=True)
    candidate = (resolved_root / relative).resolve(strict=False)
    if not is_contained(candidate, resolved_root):
        raise AdapterError("target escapes configured root")
    return candidate


def split_target(config: dict[str, Any], target: str) -> tuple[str, Path]:
    if target.startswith("wiki:"):
        return "wiki", resolve_relative(Path(config["wiki_root"]), target[5:])
    if target.startswith("source:"):
        remainder = target[7:]
        source_name, separator, relative = remainder.partition("/")
        if not separator or source_name not in config["source_roots"]:
            raise AdapterError("unknown source target")
        return "source", resolve_relative(Path(config["source_roots"][source_name]), relative)
    raise AdapterError("target must start with source:<name>/ or wiki:")


def normalized_target(config: dict[str, Any], target: str) -> str:
    kind, path = split_target(config, target)
    if kind == "wiki":
        relative = path.relative_to(Path(config["wiki_root"]).resolve(strict=True))
        return f"wiki:{relative.as_posix()}"
    source_name = target[7:].partition("/")[0]
    relative = path.relative_to(Path(config["source_roots"][source_name]).resolve(strict=True))
    return f"source:{source_name}/{relative.as_posix()}"


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                events.append(json.loads(line))
    return events


def append_event(config: dict[str, Any], operation: str, target: str, result: str) -> None:
    event_path = Path(config["event_log"])
    protected_roots = [Path(config["wiki_root"]).resolve(strict=True)]
    protected_roots.extend(Path(value).resolve(strict=True) for value in config["source_roots"].values())
    resolved_event_parent = event_path.parent.resolve(strict=True)
    if any(is_contained(resolved_event_parent, root) for root in protected_roots):
        raise AdapterError("event log must be outside source and wiki roots")
    events = read_events(event_path)
    event = {"seq": len(events) + 1, "operation": operation, "target": target, "result": result}
    with event_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def list_documents(config: dict[str, Any], target: str) -> int:
    if target == "wiki":
        root = Path(config["wiki_root"]).resolve(strict=True)
        logical_prefix = "wiki:"
    elif target.startswith("source:") and "/" not in target[7:]:
        source_name = target[7:]
        if source_name not in config["source_roots"]:
            raise AdapterError("unknown source root")
        root = Path(config["source_roots"][source_name]).resolve(strict=True)
        logical_prefix = f"source:{source_name}/"
    else:
        raise AdapterError("list target must be wiki or source:<name>")
    documents = sorted(path for path in root.rglob("*.md") if path.is_file())
    for document in documents:
        print(logical_prefix + document.relative_to(root).as_posix())
    append_event(config, "list", target, "ok")
    return 0


def read_document(config: dict[str, Any], target: str) -> int:
    normalized = normalized_target(config, target)
    if normalized in set(config.get("deny_reads", [])):
        append_event(config, "read", normalized, "permission_denied")
        raise AdapterError("permission denied")
    _, path = split_target(config, normalized)
    if not path.is_file():
        append_event(config, "read", normalized, "not_found")
        raise AdapterError("document not found")
    sys.stdout.write(path.read_text(encoding="utf-8"))
    append_event(config, "read", normalized, "ok")
    return 0


def preflight_write(config: dict[str, Any], target: str) -> int:
    normalized = normalized_target(config, target)
    kind, path = split_target(config, normalized)
    if kind != "wiki":
        raise AdapterError("writes are limited to the wiki root")
    if normalized in set(config.get("deny_preflight_writes", [])):
        append_event(config, "preflight", normalized, "permission_denied")
        raise AdapterError("permission denied")
    parent = path.parent
    if not parent.is_dir() or not os.access(parent, os.W_OK):
        append_event(config, "preflight", normalized, "unwritable")
        raise AdapterError("wiki target is not writable")
    if path.exists() and (not path.is_file() or not os.access(path, os.W_OK)):
        append_event(config, "preflight", normalized, "unwritable")
        raise AdapterError("wiki target is not writable")
    append_event(config, "preflight", normalized, "ok")
    return 0


def write_document(config: dict[str, Any], target: str) -> int:
    normalized = normalized_target(config, target)
    kind, path = split_target(config, normalized)
    if kind != "wiki":
        raise AdapterError("writes are limited to the wiki root")
    prior_writes = sum(1 for event in read_events(Path(config["event_log"])) if event["operation"] == "write")
    attempt = prior_writes + 1
    if attempt == config.get("fail_write_number"):
        append_event(config, "write", normalized, "injected_failure")
        raise AdapterError("injected provider write failure")
    content = sys.stdin.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)
    append_event(config, "write", normalized, "ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("operation", choices=("list", "read", "preflight", "write"))
    parser.add_argument("target")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config)
        if args.operation == "list":
            return list_documents(config, args.target)
        if args.operation == "read":
            return read_document(config, args.target)
        if args.operation == "preflight":
            return preflight_write(config, args.target)
        return write_document(config, args.target)
    except (AdapterError, json.JSONDecodeError, OSError) as error:
        print(f"adapter error: {error}", file=sys.stderr)
        return 13


if __name__ == "__main__":
    raise SystemExit(main())
