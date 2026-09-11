#!/usr/bin/env python3
"""Reject Codex lifecycle-test traces that bypass the configured document adapter.

The guard checks model-issued command and file-change events, not prose. It is evidence validation for the
test harness rather than a production security boundary or an operating-system sandbox.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


TOOL_ITEM_TYPES = {"command_execution", "file_change", "mcp_tool_call", "tool_call"}


def strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from strings(nested)


def tool_payload(event: dict[str, Any]) -> dict[str, Any] | None:
    item = event.get("item")
    if isinstance(item, dict) and item.get("type") in TOOL_ITEM_TYPES:
        return item
    if event.get("type") in TOOL_ITEM_TYPES:
        return event
    return None


def check_trace(trace: Path, adapter: str, protected_tokens: list[str]) -> list[str]:
    failures: list[str] = []
    seen_items: set[str] = set()
    with trace.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            event = json.loads(line)
            payload = tool_payload(event)
            if payload is None:
                continue
            item_id = str(payload.get("id", f"line-{line_number}"))
            signature = json.dumps(payload, sort_keys=True)
            identity = f"{item_id}:{signature}"
            if identity in seen_items:
                continue
            seen_items.add(identity)
            combined = "\n".join(strings(payload))
            hits = sorted(token for token in protected_tokens if token and token in combined)
            if hits:
                failures.append(
                    f"line {line_number}: protected source/wiki access outside adapter ({', '.join(hits)})"
                )
            elif ("source:" in combined or "wiki:" in combined) and adapter not in combined:
                failures.append(f"line {line_number}: logical document target used outside adapter")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl", required=True, type=Path)
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--protected-token", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        failures = check_trace(args.jsonl, args.adapter, args.protected_token)
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
