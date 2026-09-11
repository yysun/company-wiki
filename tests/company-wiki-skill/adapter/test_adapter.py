"""Unit coverage for the deterministic lifecycle test adapter and trace guard."""

from __future__ import annotations

import hashlib
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
        self.registry = self.root / "registry"
        self.harness = self.root / "harness"
        for directory in (self.source, self.wiki, self.registry, self.harness):
            directory.mkdir()
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
            "registry_root": str(self.registry),
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

    def run_adapter_soft(self, operation: str, target: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ADAPTER),
                "--config",
                str(self.config),
                "--soft-errors",
                operation,
                target,
            ],
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

        soft_denied = self.run_adapter_soft("read", "source:drive/denied.md")
        self.assertEqual(0, soft_denied.returncode)
        self.assertEqual({"error": "permission denied", "ok": False}, json.loads(soft_denied.stdout))
        self.assertNotIn("secret content", soft_denied.stdout + soft_denied.stderr)

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

    def test_event_log_cannot_live_in_registry_or_reach_wiki_through_symlink(self) -> None:
        self.write_config(event_log=str(self.registry / "events.jsonl"))
        self.assertEqual(13, self.run_adapter("read", "source:drive/allowed.md").returncode)

        linked_log = self.harness / "linked-events.jsonl"
        linked_log.symlink_to(self.wiki / "events.jsonl")
        self.write_config(event_log=str(linked_log))
        self.assertEqual(13, self.run_adapter("read", "source:drive/allowed.md").returncode)
        self.assertFalse((self.wiki / "events.jsonl").exists())


class TraceGuardTest(unittest.TestCase):
    def run_guard(
        self,
        events: list[dict[str, object]],
        adapter_events: list[dict[str, object]] | None = None,
        use_alternate_config: bool = False,
        mutate_expected_config: bool = False,
        use_alternate_interpreter: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary:
            expected_config = Path(temporary) / "config.json"
            expected_config.write_text('{"scope":"expected"}\n', encoding="utf-8")
            expected_checksum = hashlib.sha256(expected_config.read_bytes()).hexdigest()
            alternate_config = Path(temporary) / "alternate.json"
            alternate_config.write_text('{"scope":"alternate"}\n', encoding="utf-8")
            replacements = {
                "__CONFIG__": str(alternate_config if use_alternate_config else expected_config),
                "__PYTHON__": "/bin/echo" if use_alternate_interpreter else sys.executable,
            }
            rendered = json.dumps(events)
            for marker, value in replacements.items():
                rendered = rendered.replace(marker, value)
            rendered_events = json.loads(rendered)
            trace = Path(temporary) / "trace.jsonl"
            trace.write_text(
                "".join(json.dumps(event) + "\n" for event in rendered_events), encoding="utf-8"
            )
            if mutate_expected_config:
                expected_config.write_text('{"scope":"changed"}\n', encoding="utf-8")
            command = [
                sys.executable,
                str(GUARD),
                "--jsonl",
                str(trace),
                "--adapter",
                str(ADAPTER),
                "--interpreter",
                sys.executable,
                "--config",
                str(expected_config),
                "--config-sha256",
                expected_checksum,
                "--adapter-sha256",
                hashlib.sha256(ADAPTER.read_bytes()).hexdigest(),
                "--require-soft-errors",
                "--protected-token",
                "/private/source-root",
                "--protected-token",
                "drive-source",
                "--protected-token",
                "wiki-documents",
                "--protected-token",
                str(expected_config),
            ]
            if adapter_events is not None:
                event_log = Path(temporary) / "adapter-events.jsonl"
                event_log.write_text(
                    "".join(json.dumps(event) + "\n" for event in adapter_events), encoding="utf-8"
                )
                command.extend(("--adapter-events", str(event_log)))
            return subprocess.run(
                command,
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
                "command": f"__PYTHON__ {ADAPTER} --config __CONFIG__ --soft-errors read source:drive/policy.md",
                "aggregated_output": "The wiki records drive-source and wiki-documents locators.",
            },
        }
        adapter_events = [{"seq": 1, "operation": "read", "target": "source:drive/policy.md", "result": "ok"}]
        result = self.run_guard([event], adapter_events)
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

    def test_rejects_adapter_event_missing_from_trace(self) -> None:
        adapter_events = [
            {"seq": 1, "operation": "read", "target": "source:drive/denied.md", "result": "permission_denied"}
        ]
        result = self.run_guard([], adapter_events)
        self.assertEqual(1, result.returncode)

    def test_rejects_alternate_adapter_config(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "alternate-config",
                "type": "command_execution",
                "command": f"__PYTHON__ {ADAPTER} --config __CONFIG__ --soft-errors read source:drive/policy.md",
            },
        }
        result = self.run_guard([event], use_alternate_config=True)
        self.assertEqual(1, result.returncode)

    def test_rejects_substitute_interpreter(self) -> None:
        event = {
            "type": "item.completed",
            "item": {
                "id": "alternate-interpreter",
                "type": "command_execution",
                "command": f"__PYTHON__ {ADAPTER} --config __CONFIG__ --soft-errors read source:drive/policy.md",
            },
        }
        result = self.run_guard([event], use_alternate_interpreter=True)
        self.assertEqual(1, result.returncode)

    def test_rejects_changed_expected_config(self) -> None:
        result = self.run_guard([], mutate_expected_config=True)
        self.assertEqual(1, result.returncode)

    def test_rejects_transient_config_mutation_and_restore_trace(self) -> None:
        events = [
            {
                "type": "item.completed",
                "item": {
                    "id": "mutate",
                    "type": "command_execution",
                    "command": "python3 -c 'open(\"__CONFIG__\", \"w\").write(\"changed\")'",
                },
            },
            {
                "type": "item.completed",
                "item": {
                    "id": "invoke",
                    "type": "command_execution",
                    "command": f"__PYTHON__ {ADAPTER} --config __CONFIG__ --soft-errors read source:drive/policy.md",
                },
            },
            {
                "type": "item.completed",
                "item": {
                    "id": "restore",
                    "type": "command_execution",
                    "command": "cp /tmp/config.backup __CONFIG__",
                },
            },
        ]
        adapter_events = [{"seq": 1, "operation": "read", "target": "source:drive/policy.md", "result": "ok"}]
        result = self.run_guard(events, adapter_events)
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
