"""Protect the evaluation from invented scores, unseen citations, and bypassed retrieval."""

import argparse
import contextlib
import io
import json
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import benchmark as bench


class ScoringTest(unittest.TestCase):
    def setUp(self):
        self.docs = [{"id": "E01", "role": "source", "text": "Approved: 18 days."},
                     {"id": "W01", "role": "wiki", "text": "Follow the policy."}]
        self.case = {"required_sources": ["E01"]}
        self.trace = {"source_reads": ["E01"]}

    def test_missing_citations_and_semantic_review_are_not_perfect_scores(self):
        score = bench.objective_scores(self.case, {"answer": "18 days", "citations": []}, self.trace, self.docs)
        self.assertIsNone(score["citation_integrity"])
        self.assertIsNone(score["answer_correctness"])
        self.assertIsNone(score["answer_grounding"])

    def test_citation_must_be_opened_exact_original_and_inline(self):
        response = {"answer": "18 days [E01]", "citations": [{"source_id": "E01", "quote": "18 days"}]}
        self.assertEqual(1, bench.objective_scores(self.case, response, self.trace, self.docs)["valid_citations"])
        self.assertEqual(0, bench.objective_scores(self.case, response, {"source_reads": []}, self.docs)["valid_citations"])
        response["citations"][0]["quote"] = "22 days"
        self.assertEqual(0, bench.objective_scores(self.case, response, self.trace, self.docs)["valid_citations"])

    def test_wiki_cannot_prove_company_fact(self):
        response = {"answer": "Policy [W01]", "citations": [{"source_id": "W01", "quote": "Follow the policy."}]}
        self.assertEqual(0, bench.objective_scores(self.case, response, {"source_reads": ["W01"]}, self.docs)["valid_citations"])

    def test_exact_quote_preserves_source_line_break_through_json(self):
        source = "A request is not approval\nuntil the owner signs."
        documents = [{"id": "E01", "role": "source", "text": source}]
        for quote, expected in ((source, 1), (source.replace("\n", " "), 0),
                                (source.replace("\n", r"\n"), 0)):
            with self.subTest(quote=quote):
                response = json.loads(json.dumps({
                    "answer": "The owner must sign [E01].",
                    "citations": [{"source_id": "E01", "quote": quote}],
                }))
                score = bench.objective_scores(self.case, response, self.trace, documents)
                self.assertEqual(expected, score["valid_citations"])

    def test_direct_file_read_is_rejected(self):
        event = {"type": "item.completed", "item": {"type": "command_execution", "command": "cat /tmp/gold.json"}}
        self.assertTrue(bench.inspect_trace(json.dumps(event), Path("/tmp/corpus"), self.docs)["integrity_failures"])

    def test_unrecognized_tool_event_is_rejected(self):
        event = {"type": "item.completed", "item": {"type": "collab_agent_tool_call"}}
        self.assertTrue(bench.inspect_trace(json.dumps(event), Path("/tmp/corpus"), self.docs)["integrity_failures"])

    def test_exact_tool_read_is_counted_and_content_verified(self):
        corpus = Path("/tmp/corpus")
        command = shlex.join([sys.executable, str(Path(bench.__file__).resolve()), "tool", "--corpus", str(corpus), "read", "E01"])
        item = {"type": "command_execution", "command": command, "exit_code": 0,
                "aggregated_output": json.dumps({"operation": "read", "documents": [self.docs[0]]})}
        checks = bench.inspect_trace(json.dumps({"type": "item.completed", "item": item}), corpus, self.docs)
        self.assertEqual(["E01"], checks["source_reads"])
        self.assertFalse(checks["integrity_failures"])
        item["aggregated_output"] = item["aggregated_output"].replace("18 days", "22 days")
        self.assertTrue(bench.inspect_trace(json.dumps({"type": "item.completed", "item": item}), corpus, self.docs)["integrity_failures"])

    def test_command_substitution_is_rejected(self):
        command = shlex.join([sys.executable, str(Path(bench.__file__).resolve()), "tool", "--corpus",
                              "/tmp/corpus", "search", "$(cat /tmp/gold.json)"])
        event = {"type": "item.completed", "item": {"type": "command_execution", "command": command}}
        self.assertTrue(bench.inspect_trace(json.dumps(event), Path("/tmp/corpus"), self.docs)["integrity_failures"])


class QueryReferenceRunTest(unittest.TestCase):
    def test_reference_is_frozen_in_every_prompt_and_recorded_by_hash(self):
        self.check_run(tamper_launcher=False)

    def test_changed_launcher_invalidates_run(self):
        self.check_run(tamper_launcher=True)

    def check_run(self, *, tamper_launcher):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reference = root / "query.md"
            original = b"Use a distinctive retrieval strategy.\n"
            reference.write_bytes(original)
            gold = {"as_of": "2026-09-13", "documents": [], "cases": [
                {"id": case_id, "corpus": "fixture", "question": "A synthetic question?",
                 "category": "test", "required_sources": []}
                for case_id in ("T01", "T02")
            ]}
            bench.save(root / "dataset.json", gold)
            prompts = []
            commands = []

            class Process:
                returncode = 0

                def __init__(self, command, **kwargs):
                    commands.append(command)
                    response_path = Path(command[command.index("--output-last-message") + 1])
                    bench.save(response_path, {"answer": "Unknown.", "citations": []})
                    self.workspace = Path(command[command.index("--cd") + 1])

                def communicate(self, prompt, timeout):
                    prompts.append(prompt)
                    reference.write_text("Changed during execution.\n")
                    if tamper_launcher:
                        launcher = self.workspace / "corpus-tool"
                        launcher.chmod(0o700)
                        launcher.write_text("#!/bin/sh\nexit 0\n")
                    return "", ""

            args = argparse.Namespace(only=None, timeout=180, output=root / "run", model="test-model",
                                      effort="high", query_contract=reference)
            with patch.object(bench, "dataset", return_value=gold), patch.object(bench, "HERE", root), \
                    patch.object(bench.subprocess, "check_output", return_value="test-cli"), \
                    patch.object(bench.subprocess, "Popen", Process), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(int(tamper_launcher), bench.run(args))
            self.assertEqual(2, len(prompts))
            for command in commands:
                self.assertEqual("unified_exec", command[command.index("--disable") + 1])
                self.assertEqual("read-only", command[command.index("--sandbox") + 1])
            for prompt in prompts:
                self.assertIn(original.decode(), prompt)
                self.assertNotIn("Changed during execution.", prompt)
                self.assertNotIn("required_sources", prompt)
                self.assertIn("./corpus-tool search", prompt)
                self.assertNotIn("benchmark.py tool --corpus", prompt)
            manifest = json.loads((args.output / "manifest.json").read_text())
            self.assertEqual({"unified_exec": False}, manifest["cli_feature_overrides"])
            self.assertEqual(bench.digest(original), manifest["query_contract_sha256"])
            self.assertEqual(original, (args.output / "query-contract-at-execution.md").read_bytes())
            for snapshot, field in (("dataset-at-execution.json", "dataset_sha256"),
                                    ("runner-at-execution.py", "runner_sha256")):
                self.assertEqual(manifest[field], bench.digest((args.output / snapshot).read_bytes()))
            for case_id in ("T01", "T02"):
                destination = args.output / case_id
                binding = json.loads((destination / "tool-binding.json").read_text())
                launcher_bytes = (destination / "corpus-tool-at-execution.sh").read_bytes()
                self.assertEqual(bench.digest(launcher_bytes), binding["launcher_sha256"])
                self.assertEqual(bench.digest(b"[]\n"), binding["corpus_sha256"])
                self.assertIn(binding["corpus_path"], launcher_bytes.decode())
                result = json.loads((destination / "result.json").read_text())
                self.assertEqual(["corpus launcher missing or changed"] if tamper_launcher else [],
                                 result["trace_checks"]["integrity_failures"])


class LauncherTest(unittest.TestCase):
    def setUp(self):
        self.docs = [{"id": "E01", "role": "source", "path": "source.md", "title": "Hybrid 混合办公",
                      "text": "Hybrid 混合办公\n每周三天。\nDepartment head approves exceptions."},
                     {"id": "W01", "role": "wiki", "path": "home.md", "title": "Home", "text": "Read E01."}]
        self.corpus = Path("/private/tmp/company-wiki-rag-test/corpus.json")
        self.launcher = self.corpus.parent / "corpus-tool"

    def event(self, command, action="read", documents=None):
        return json.dumps({"type": "item.completed", "item": {
            "type": "command_execution", "command": command, "exit_code": 0,
            "aggregated_output": json.dumps({"operation": action,
                                              "documents": self.docs[:1] if documents is None else documents}),
        }})

    def check(self, trace):
        return bench.inspect_trace(trace, self.corpus, self.docs, launcher=self.launcher)

    def test_launcher_executes_unicode_search_and_read_against_bound_corpus(self):
        with tempfile.TemporaryDirectory(prefix="company-wiki-rag-") as temporary:
            root = Path(temporary)
            workspace = root / "含 空格"
            workspace.mkdir()
            corpus = workspace / "corpus.json"
            bench.save(corpus, self.docs)
            launcher = bench.create_launcher(corpus)
            # Running elsewhere must not select that directory's corpus.
            decoy = root / "corpus.json"
            bench.save(decoy, [{**self.docs[0], "text": "Wrong corpus."}])
            for action, values, expected_ids in (("list", [], ["E01", "W01"]),
                                                 ("search", ["hybrid|混合|办公"], ["E01"]),
                                                 ("read", ["E01"], ["E01"])):
                with self.subTest(action=action):
                    process = subprocess.run([str(launcher), action, *values], cwd=root,
                                             capture_output=True, text=True, check=True)
                    output = json.loads(process.stdout)
                    self.assertEqual(action, output["operation"])
                    self.assertEqual(expected_ids, [d["id"] for d in output["documents"]])
                    if action == "read":
                        self.assertEqual(self.docs[0]["text"], output["documents"][0]["text"])
                    if action == "search":
                        self.assertEqual(["Hybrid 混合办公"], output["documents"][0]["snippets"])
            for values in (("--corpus", str(decoy), "read", "E01"),
                           ("read", "E01", "--corpus", str(decoy))):
                process = subprocess.run([str(launcher), *values], cwd=root, capture_output=True, text=True)
                self.assertNotEqual(0, process.returncode)
                self.assertNotIn("Wrong corpus.", process.stdout)

    def test_exact_launcher_read_is_counted_and_content_verified(self):
        command = "/bin/zsh -lc './corpus-tool read E01'"
        checks = self.check(self.event(command))
        self.assertFalse(checks["integrity_failures"])
        self.assertEqual(["E01"], checks["source_reads"])
        self.assertEqual(len(self.docs[0]["text"]), checks["source_characters"])
        altered = [{**self.docs[0], "text": "Changed."}]
        self.assertTrue(self.check(self.event(command, documents=altered))["integrity_failures"])

    def test_missing_listing_output_stays_invalid_after_a_successful_read(self):
        for output in ("", " ", '{"operation":"list","documents":['):
            with self.subTest(output=output):
                event = json.loads(self.event("./corpus-tool list", action="list", documents=[]))
                event["item"]["aggregated_output"] = output
                checks = self.check(json.dumps(event) + "\n" + self.event("./corpus-tool read E01"))
                self.assertEqual(["tool output is not JSON"], checks["integrity_failures"])
                self.assertEqual(["E01"], checks["source_reads"])

    def test_launcher_contract_rejects_other_paths_flags_and_shell_operations(self):
        legacy = shlex.join([sys.executable, str(Path(bench.__file__).resolve()), "tool", "--corpus",
                             str(self.corpus), "read", "E01"])
        for command in ("./corpus-too read E01", "/tmp/corpus-tool read E01", "corpus-tool read E01",
                        "./corpus-tool read E01 --corpus /tmp/other.json", "./corpus-tool list E01",
                        "./corpus-tool search", "./corpus-tool read missing",
                        "./corpus-tool read E01; cat /tmp/gold", "./corpus-tool read E01 > /tmp/out",
                        "./corpus-tool search $(cat /tmp/gold)", "./corpus-tool search `cat /tmp/gold`",
                        "cd /tmp && ./corpus-tool read E01", legacy):
            with self.subTest(command=command):
                self.assertTrue(self.check(self.event(command))["integrity_failures"])

    def test_historical_wrong_corpus_path_stays_invalid(self):
        wrong = str(self.corpus).replace("company-wiki-rag-", "company-wiki-")
        command = shlex.join([sys.executable, str(Path(bench.__file__).resolve()), "tool", "--corpus",
                             wrong, "read", "E01"])
        checks = bench.inspect_trace(self.event(command), self.corpus, self.docs)
        self.assertTrue(checks["integrity_failures"])

    def test_launcher_preserves_routing_and_budget_checks(self):
        source = self.event("./corpus-tool read E01")
        wiki = self.event("./corpus-tool read W01", documents=self.docs[1:])
        search = self.event("./corpus-tool search 'hybrid|混合'", "search", documents=[])
        self.assertTrue(self.check(wiki + "\n" + source)["example_navigation_ok"])
        self.assertFalse(self.check(source + "\n" + wiki)["routing_order_ok"])
        self.assertFalse(self.check("\n".join([source] * 6))["query_bounds_ok"])
        self.assertFalse(self.check("\n".join([search] * 3))["query_bounds_ok"])
        large_search = self.event("./corpus-tool search 'hybrid'", "search",
                                  documents=[{"id": "E01", "snippets": ["x" * 40001]}])
        self.assertFalse(self.check(large_search)["query_bounds_ok"])


if __name__ == "__main__":
    unittest.main()
