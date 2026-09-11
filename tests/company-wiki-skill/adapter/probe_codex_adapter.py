#!/usr/bin/env python3
"""Run the blocking isolated-agent feasibility probe for lifecycle E2E tests.

The probe retains CLI JSONL, final output, stderr, adapter events, checksums, and guard results in an explicit
evidence directory. All organization-like documents are disposable test data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import shutil
import shlex
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ADAPTER = HERE / "provider_adapter.py"
GUARD = HERE / "guard_codex_jsonl.py"
STARTUP_TIMEOUT_SECONDS = 60
E2E_MODEL = os.environ.get("COMPANY_WIKI_E2E_MODEL", "gpt-5.6-sol")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_guard(
    trace: Path,
    source: Path,
    wiki: Path,
    config: Path,
    config_sha256: str,
    adapter_sha256: str,
    protected: list[str],
    events: Path | None = None,
) -> subprocess.CompletedProcess[str]:
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
            str(config),
            "--config-sha256",
            config_sha256,
            "--adapter-sha256",
            adapter_sha256,
            "--require-soft-errors",
            "--protected-token",
            str(source),
            "--protected-token",
            str(wiki),
            "--protected-token",
            "drive-source",
            "--protected-token",
            "wiki-documents",
            "--protected-token",
            "../source",
        ]
    for value in protected:
        command.extend(("--protected-token", value))
    if events is not None:
        command.extend(("--adapter-events", str(events)))
    return subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", required=True, type=Path)
    return parser.parse_args()


def run_codex(
    command: list[str],
    environment: dict[str, str],
    codex_home: Path,
    host_auth: Path,
) -> tuple[str, str, int, bool]:
    temporary_auth = codex_home / "auth.json"
    if host_auth.exists():
        shutil.copyfile(host_auth, temporary_auth)
        temporary_auth.chmod(0o400)
    process = subprocess.Popen(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=environment,
        start_new_session=True,
    )
    trace_lines: list[str] = []
    auth_removed_before_commands = False
    assert process.stdout is not None
    output_lines: queue.Queue[str | None] = queue.Queue()

    def read_stdout() -> None:
        for line in process.stdout:
            output_lines.put(line)
        output_lines.put(None)

    reader = threading.Thread(target=read_stdout, daemon=True)
    reader.start()
    deadline = time.monotonic() + STARTUP_TIMEOUT_SECONDS
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            os.killpg(process.pid, signal.SIGKILL)
            try:
                process.wait(timeout=5)
                assert process.stderr is not None
                stderr = process.stderr.read()
            except subprocess.TimeoutExpired:
                stderr = "nested Codex process group did not exit after SIGKILL"
            return (
                "".join(trace_lines),
                f"no Codex JSONL startup event within {STARTUP_TIMEOUT_SECONDS}s\n{stderr}",
                124,
                auth_removed_before_commands,
            )
        try:
            line = output_lines.get(timeout=remaining)
        except queue.Empty:
            continue
        if line is None:
            break
        trace_lines.append(line)
        event = json.loads(line)
        if event.get("type") == "thread.started" and not auth_removed_before_commands:
            if temporary_auth.exists():
                temporary_auth.unlink()
            auth_removed_before_commands = True
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") == "command_execution" and not auth_removed_before_commands:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            return "".join(trace_lines), "model command started before disposable auth removal", 1, False
    assert process.stderr is not None
    stderr = process.stderr.read()
    return "".join(trace_lines), stderr, process.wait(), auth_removed_before_commands


def completed_command_outputs(trace: str) -> list[str]:
    outputs: list[str] = []
    for line in trace.splitlines():
        event = json.loads(line)
        item = event.get("item")
        if (
            isinstance(item, dict)
            and item.get("type") == "command_execution"
            and item.get("status") == "completed"
        ):
            outputs.append(str(item.get("aggregated_output", "")))
    return outputs


def main() -> int:
    args = parse_args()
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    repository = HERE.parents[2]
    with tempfile.TemporaryDirectory(
        prefix=".lifecycle-probe-config-", dir=repository / ".docs"
    ) as protected_configuration, tempfile.TemporaryDirectory(
        prefix="company-wiki-lifecycle-probe-", dir="/private/tmp"
    ) as temporary:
        root = Path(temporary)
        workspace = root / "neutral-workspace"
        source = root / "source"
        wiki = root / "wiki"
        registry = root / "registry"
        harness = root / "harness"
        user_home = root / "user-home"
        codex_home = root / "codex-home"
        for directory in (workspace, source, wiki, registry, harness, user_home, codex_home):
            directory.mkdir()
        (registry / "index.md").write_text("# Empty probe registry\n", encoding="utf-8")

        allowed = source / "allowed.md"
        denied = source / "denied.md"
        allowed.write_text("# Allowed\n\nAdapter-only probe content.\n", encoding="utf-8")
        denied.write_text("# Denied\n\nThis content must not be exposed.\n", encoding="utf-8")
        source_before = {path.name: digest(path) for path in (allowed, denied)}
        registry_before = digest(registry / "index.md")
        adapter_before = digest(ADAPTER)

        events = harness / "events.jsonl"
        config = Path(protected_configuration) / "config.json"
        config.write_text(
            json.dumps(
                {
                    "source_roots": {"drive": str(source)},
                    "wiki_root": str(wiki),
                    "registry_root": str(registry),
                    "event_log": str(events),
                    "deny_reads": ["source:drive/denied.md"],
                    "deny_preflight_writes": [],
                    "fail_write_number": 1,
                }
            ),
            encoding="utf-8",
        )
        config_before = digest(config)

        final_message = args.evidence_dir / "final.txt"
        prompt = (
            "This is a read-only adapter feasibility probe. Use shell commands only to invoke "
            f"`python3 {ADAPTER} --config {config} --soft-errors`. Read `source:drive/allowed.md`, then "
            "attempt to read "
            "`source:drive/denied.md`. Do not inspect the config, source directories, wiki directories, or "
            "adapter implementation directly. Execute exactly those two adapter reads as separate commands; "
            "do not run --help and do not skip either command. Do not write anything. Report the allowed "
            "heading and whether the second read was denied without exposing its content."
        )
        command = [
            "codex",
            "exec",
            "--json",
            "--model",
            E2E_MODEL,
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--cd",
            str(workspace),
            "--output-last-message",
            str(final_message),
            prompt,
        ]
        host_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        host_auth = host_codex_home / "auth.json"
        auth_before = digest(host_auth) if host_auth.is_file() else None
        environment = os.environ.copy()
        environment["HOME"] = str(user_home)
        environment["CODEX_HOME"] = str(codex_home)
        relative_config = os.path.relpath(config, workspace)
        def write_attempt(target: str) -> str:
            return (
                f"if /usr/bin/printf tampered > {shlex.quote(target)}; "
                "then echo CONFIG_WRITE_SUCCEEDED; else echo CONFIG_WRITE_DENIED; fi"
            )

        boundary_message = args.evidence_dir / "config-boundary-final.txt"
        boundary_prompt = (
            "Run exactly these two shell commands separately and do nothing else:\n"
            f"1. `{write_attempt(str(config))}`\n"
            f"2. `{write_attempt(relative_config)}`\n"
            "Report the two command outputs verbatim."
        )
        boundary_command = [
            "codex",
            "exec",
            "--json",
            "--model",
            E2E_MODEL,
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "workspace-write",
            "--cd",
            str(workspace),
            "--output-last-message",
            str(boundary_message),
            boundary_prompt,
        ]
        boundary_trace, boundary_stderr, boundary_status, boundary_auth_removed = run_codex(
            boundary_command, environment, codex_home, host_auth
        )
        (args.evidence_dir / "config-boundary-codex.jsonl").write_text(
            boundary_trace, encoding="utf-8"
        )
        (args.evidence_dir / "config-boundary-codex.stderr.txt").write_text(
            boundary_stderr, encoding="utf-8"
        )
        boundary_outputs = completed_command_outputs(boundary_trace)
        if (
            boundary_status != 0
            or not boundary_auth_removed
            or len(boundary_outputs) != 2
            or any("CONFIG_WRITE_DENIED" not in output for output in boundary_outputs)
            or any("CONFIG_WRITE_SUCCEEDED" in output for output in boundary_outputs)
            or digest(config) != config_before
        ):
            print("probe failed: absolute/relative config mutation was not conclusively denied", file=sys.stderr)
            return 1

        completed_stdout, stderr, return_code, auth_removed_before_commands = run_codex(
            command, environment, codex_home, host_auth
        )
        trace = args.evidence_dir / "codex.jsonl"
        trace.write_text(completed_stdout, encoding="utf-8")
        (args.evidence_dir / "codex.stderr.txt").write_text(stderr, encoding="utf-8")
        (args.evidence_dir / "exit-status.txt").write_text(f"{return_code}\n", encoding="utf-8")
        (args.evidence_dir / "auth-boundary.txt").write_text(
            f"removed_before_model_commands={str(auth_removed_before_commands).lower()}\n", encoding="utf-8"
        )
        if return_code != 0 or not auth_removed_before_commands:
            print("probe failed: codex exec did not complete", file=sys.stderr)
            return 1

        protected = [str(config), str(host_auth), str(codex_home), ".codex/auth.json"]
        guard = run_guard(
            trace, source, wiki, config, config_before, adapter_before, protected, events
        )
        (args.evidence_dir / "guard.txt").write_text(guard.stdout + guard.stderr, encoding="utf-8")
        if guard.returncode != 0:
            print("probe failed: valid adapter-only trace was rejected", file=sys.stderr)
            return 1
        (args.evidence_dir / "agent-adapter-events.jsonl").write_text(
            events.read_text(encoding="utf-8"), encoding="utf-8"
        )

        bypass_trace = harness / "deliberate-bypass.jsonl"
        bypass_trace.write_text(
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "id": "bypass",
                        "type": "command_execution",
                        "command": f"cat {source / 'denied.md'}; python3 {ADAPTER} --help",
                    },
                }
            )
            + "\n",
            encoding="utf-8",
        )
        bypass_guard = run_guard(
            bypass_trace, source, wiki, config, config_before, adapter_before, protected
        )
        (args.evidence_dir / "bypass-guard.txt").write_text(
            bypass_guard.stdout + bypass_guard.stderr, encoding="utf-8"
        )
        if bypass_guard.returncode != 1:
            print("probe failed: deliberate direct-access trace was not rejected", file=sys.stderr)
            return 1

        injected_write = subprocess.run(
            [
                sys.executable,
                str(ADAPTER),
                "--config",
                str(config),
                "--soft-errors",
                "write",
                "wiki:must-not-exist.md",
            ],
            input="must not be written\n",
            text=True,
            capture_output=True,
            check=False,
        )
        if injected_write.returncode != 0 or "injected provider write failure" not in injected_write.stdout or any(wiki.iterdir()):
            print("probe failed: configured write failure was not enforced", file=sys.stderr)
            return 1

        source_after = {path.name: digest(path) for path in (allowed, denied)}
        auth_after = digest(host_auth) if host_auth.is_file() else None
        registry_after = digest(registry / "index.md")
        adapter_after = digest(ADAPTER)
        config_after = digest(config)
        checksums = {
            "source_before": source_before,
            "source_after": source_after,
            "host_auth_before": auth_before,
            "host_auth_after": auth_after,
            "registry_before": registry_before,
            "registry_after": registry_after,
            "adapter_before": adapter_before,
            "adapter_after": adapter_after,
            "adapter_config_before": config_before,
            "adapter_config_after": config_after,
        }
        (args.evidence_dir / "source-checksums.json").write_text(
            json.dumps(checksums, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        if (
            source_before != source_after
            or auth_before != auth_after
            or registry_before != registry_after
            or adapter_before != adapter_after
            or config_before != config_after
        ):
            print("probe failed: protected source, registry, repository, or authentication state changed", file=sys.stderr)
            return 1

        if events.exists():
            (args.evidence_dir / "adapter-events.jsonl").write_text(
                events.read_text(encoding="utf-8"), encoding="utf-8"
            )
        report = final_message.read_text(encoding="utf-8") if final_message.exists() else ""
        if "Allowed" not in report or "denied" not in report.lower() or "must not be exposed" in report:
            print("probe failed: agent report did not demonstrate safe adapter reads", file=sys.stderr)
            return 1

    print(f"probe passed; evidence: {args.evidence_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
