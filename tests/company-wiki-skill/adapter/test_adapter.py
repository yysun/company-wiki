"""Unit coverage for the deterministic lifecycle test adapter and trace guard."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ADAPTER_DIR = Path(__file__).resolve().parent
ADAPTER = ADAPTER_DIR / "provider_adapter.py"
GUARD = ADAPTER_DIR / "guard_codex_jsonl.py"


class ProviderAdapterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.wiki = self.root / "wiki"
        self.harness = self.root / "harness"
        self.source.mkdir()
        self.wiki.mkdir()
        self.harness.mkdir()
        (self.source / "allowed.md").write_text("allowed content\n", encoding="utf-8")
        (self.source / "denied.md").write_text("secret content\n", encoding="utf-8")
        self.events = self.harness / "events.jsonl"
        self.config = self.harness / "config.json"
        self.write_config()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_config(self, **overrides: object) -> None:
        config: dict[str, object] = {
            "source_roots": {"drive": str(self.source)},
            "wiki_root": str(self.wiki),
            "event_log": str(self.events),
            "deny_reads": ["source:drive/denied.md"],
            "deny_preflight_writes": ["wiki:blocked.md"],
            "fail_write_number": 2,
        }
        config.update(overrides)
        self.config.write_text(json.dumps(config), encoding="utf-8")

    def run_adapter(self, operation: str, target: str, content: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ADAPTER), "--config", str(self.config), operation, target],
            input=content,
            text=True,
            capture_output=True,
            check=False,
        )

    def events_read(self) -> list[dict[str, object]]:
        return [json.loads(line) for line in self.events.read_text(encoding="utf-8").splitlines()]

    def test_read_and_boundary_controls(self) -> None:
        allowed = self.run_adapter("read", "source:drive/allowed.md")
        self.assertEqual(0, allowed.returncode)
        self.assertEqual("allowed content\n", allowed.stdout)

        denied = self.run_adapter("read", "source:drive/denied.md")
        self.assertEqual(13, denied.returncode)
        self.assertNotIn("secret content", denied.stdout + denied.stderr)

        escaped = self.run_adapter("read", "source:drive/../outside.md")
        self.assertEqual(13, escaped.returncode)

    def test_preflight_and_nth_write_failure(self) -> None:
        self.assertEqual(0, self.run_adapter("preflight", "wiki:first.md").returncode)
        self.assertEqual(13, self.run_adapter("preflight", "wiki:blocked.md").returncode)
        self.assertEqual(0, self.run_adapter("write", "wiki:first.md", "first\n").returncode)
        failed = self.run_adapter("write", "wiki:second.md", "second\n")
        self.assertEqual(13, failed.returncode)
        self.assertEqual("first\n", (self.wiki / "first.md").read_text(encoding="utf-8"))
        self.assertFalse((self.wiki / "second.md").exists())
        results = [(event["operation"], event["result"]) for event in self.events_read()]
        self.assertIn(("preflight", "permission_denied"), results)
        self.assertEqual(("write", "injected_failure"), results[-1])

    def test_event_log_cannot_live_in_protected_root(self) -> None:
        self.write_config(event_log=str(self.wiki / "events.jsonl"))
        result = self.run_adapter("read", "source:drive/allowed.md")
        self.assertEqual(13, result.returncode)
        self.assertFalse((self.wiki / "events.jsonl").exists())


class TraceGuardTest(unittest.TestCase):
    def run_guard(self, events: list[dict[str, object]]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary:
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
            return subprocess.run(
                [
                    sys.executable,
                    str(GUARD),
                    "--jsonl",
                    str(trace),
                    "--adapter",
                    str(ADAPTER),
                    "--protected-token",
                    "/private/source-root",
                    "--protected-token",
                    "drive-source",
                    "--protected-token",
                    "wiki-documents",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_allows_adapter_only_trace(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "1",
                "type": "command_execution",
                "command": f"python3 {ADAPTER} --config /tmp/config.json read source:drive/policy.md",
            },
        }
        result = self.run_guard([event])
        self.assertEqual(0, result.returncode, result.stderr)

    def test_rejects_shell_bypass(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "2",
                "type": "command_execution",
                "command": "sed -n 1,20p drive-source/policy.md",
            },
        }
        result = self.run_guard([event])
        self.assertEqual(1, result.returncode)

    def test_rejects_bypass_hidden_beside_adapter_invocation(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "mixed",
                "type": "command_execution",
                "command": f"cat drive-source/policy.md; python3 {ADAPTER} --help",
            },
        }
        result = self.run_guard([event])
        self.assertEqual(1, result.returncode)

    def test_rejects_logical_target_outside_adapter(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "logical",
                "type": "command_execution",
                "command": "other-provider read source:drive/policy.md",
            },
        }
        result = self.run_guard([event])
        self.assertEqual(1, result.returncode)

    def test_rejects_file_change_bypass(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "3",
                "type": "file_change",
                "changes": [{"path": "/private/source-root/policy.md", "kind": "read"}],
            },
        }
        result = self.run_guard([event])
        self.assertEqual(1, result.returncode)


if __name__ == "__main__":
    unittest.main()
