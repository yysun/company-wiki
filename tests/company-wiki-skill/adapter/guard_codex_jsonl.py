#!/usr/bin/env python3
"""Reject Codex lifecycle-test traces that bypass the configured document adapter.

The guard checks model-issued command and file-change events, not prose. It is evidence validation for the
test harness rather than a production security boundary or an operating-system sandbox.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import shutil
import sys
from pathlib import Path
from typing import Any


TOOL_ITEM_TYPES = {"command_execution", "file_change", "mcp_tool_call", "tool_call"}


def tool_payload(event: dict[str, Any]) -> dict[str, Any] | None:
    item = event.get("item")
    if isinstance(item, dict) and item.get("type") in TOOL_ITEM_TYPES:
        return item
    if event.get("type") in TOOL_ITEM_TYPES:
        return event
    return None


def shell_tokens(command: str) -> list[str] | None:
    try:
        outer = shlex.split(command)
        if len(outer) == 3 and Path(outer[0]).name in {"sh", "bash", "zsh"} and outer[1] in {"-c", "-lc"}:
            command = outer[2]
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>()")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return None
    if any(token and all(character in "; & | < > ( )" for character in token) for token in tokens):
        return None
    return tokens


def resolved_executable(value: str) -> Path:
    located = shutil.which(value) if "/" not in value else value
    return Path(located or value).resolve(strict=False)


def adapter_operation(
    command: str,
    adapter: str,
    interpreter: str,
    config: str,
    require_soft_errors: bool,
) -> tuple[str, str] | None:
    tokens = shell_tokens(command)
    if tokens is None or len(tokens) not in {6, 7}:
        return None
    python, adapter_token, config_flag, config_token, *remainder = tokens
    if resolved_executable(python) != resolved_executable(interpreter):
        return None
    if Path(adapter_token).resolve(strict=False) != Path(adapter).resolve(strict=False):
        return None
    if config_flag != "--config" or Path(config_token).resolve(strict=False) != Path(config).resolve(strict=False):
        return None
    soft_errors = remainder[:1] == ["--soft-errors"]
    if soft_errors:
        remainder = remainder[1:]
    if require_soft_errors != soft_errors or len(remainder) != 2:
        return None
    operation, target = remainder
    if operation not in {"list", "read", "preflight", "write"}:
        return None
    return operation, target


def is_adapter_help(command: str, adapter: str, interpreter: str, config: str) -> bool:
    tokens = shell_tokens(command)
    if tokens is None or len(tokens) != 5:
        return False
    if resolved_executable(tokens[0]) != resolved_executable(interpreter):
        return False
    if Path(tokens[1]).resolve(strict=False) != Path(adapter).resolve(strict=False):
        return False
    return (
        tokens[2] == "--config"
        and Path(tokens[3]).resolve(strict=False) == Path(config).resolve(strict=False)
        and tokens[4] == "--help"
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_change_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload.get("changes", payload), sort_keys=True)


def check_trace(
    trace: Path,
    adapter: str,
    interpreter: str,
    config: str,
    config_sha256: str,
    adapter_sha256: str,
    require_soft_errors: bool,
    protected_tokens: list[str],
    adapter_events: Path | None = None,
) -> list[str]:
    failures: list[str] = []
    if sha256(Path(config)) != config_sha256:
        failures.append("adapter configuration checksum mismatch")
    if sha256(Path(adapter)) != adapter_sha256:
        failures.append("adapter executable checksum mismatch")
    seen_commands: set[tuple[str, str]] = set()
    recorded_operations: list[tuple[str, str]] = []
    with trace.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            payload = tool_payload(event)
            if payload is None:
                continue
            if payload.get("type") == "command_execution":
                command = payload.get("command")
                if not isinstance(command, str):
                    failures.append(f"line {line_number}: command event has no command string")
                    continue
                item_id = str(payload.get("id", f"line-{line_number}"))
                identity = (item_id, command)
                if identity in seen_commands:
                    continue
                seen_commands.add(identity)
                operation = adapter_operation(
                    command, adapter, interpreter, config, require_soft_errors
                )
                hits = sorted(token for token in protected_tokens if token and token in command)
                if operation is not None:
                    recorded_operations.append(operation)
                elif is_adapter_help(command, adapter, interpreter, config):
                    continue
                elif hits or "source:" in command or "wiki:" in command or adapter in command:
                    detail = ", ".join(hits) if hits else "non-exact adapter command"
                    failures.append(f"line {line_number}: document access bypass ({detail})")
            elif payload.get("type") == "file_change":
                changed = file_change_text(payload)
                hits = sorted(token for token in protected_tokens if token and token in changed)
                if not hits:
                    continue
                failures.append(
                    f"line {line_number}: protected source/wiki file change ({', '.join(hits)})"
                )

    if adapter_events is not None:
        expected: list[tuple[str, str]] = []
        with adapter_events.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    event = json.loads(line)
                    expected.append((str(event["operation"]), str(event["target"])))
        if recorded_operations != expected:
            failures.append(
                "adapter event mismatch: "
                f"commands={recorded_operations!r}; events={expected!r}"
            )
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", required=True, type=Path)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--interpreter", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--config-sha256", required=True)
    parser.add_argument("--adapter-sha256", required=True)
    parser.add_argument("--require-soft-errors", action="store_true")
    parser.add_argument("--protected-token", action="append", default=[])
    parser.add_argument("--adapter-events", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        failures = check_trace(
            args.jsonl,
            args.adapter,
            args.interpreter,
            args.config,
            args.config_sha256,
            args.adapter_sha256,
            args.require_soft_errors,
            args.protected_token,
            args.adapter_events,
        )
    except (OSError, json.JSONDecodeError) as error:
        print(f"trace guard error: {error}", file=sys.stderr)
        return 2
    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print("trace guard passed: no direct source/wiki access")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
