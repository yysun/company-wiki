#!/usr/bin/env python3
"""Render objective measurements and separately recorded semantic reviews without inventing scores.

Reviews bind to the exact response bytes and dataset version. Missing reviews stay unscored; invalid
runs remain visible and never enter quality averages. All evidence in this pilot is synthetic.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from statistics import mean

from benchmark import HERE, REPOSITORY, dataset, digest, save


def report(root: Path) -> None:
    gold = dataset()
    manifest = json.loads((root / "manifest.json").read_text())
    if manifest["dataset_sha256"] != digest((HERE / "dataset.json").read_bytes()):
        raise ValueError("dataset changed since execution; use the recorded dataset version")
    reviews_path = root / "reviews.json"
    reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else {"reviewer": None, "cases": {}}
    cases = {c["id"]: c for c in gold["cases"]}
    rows = []
    for case_id in manifest["case_ids"]:
        case = cases[case_id]
        path = root / case_id / "result.json"
        if not path.exists():
            rows.append({"id": case_id, "corpus": case["corpus"], "status": "not_run"})
            continue
        result = json.loads(path.read_text())
        row = {"id": case_id, "corpus": case["corpus"], "status": result["status"],
               "rubric_passed": None, "rubric_total": len(case["criteria"]), "grounded": None,
               "strict_answer_pass": None, "result": result}
        review = reviews["cases"].get(case_id)
        if review and result["status"] == "completed":
            if not reviews.get("reviewer"):
                raise ValueError("semantic review has no reviewer identity/type")
            if review["response_sha256"] != digest((root / case_id / "response.json").read_bytes()):
                raise ValueError(f"{case_id}: review refers to a different answer")
            verdicts = review["criteria_passed"]
            if len(verdicts) != len(case["criteria"]) or any(type(v) is not bool for v in verdicts):
                raise ValueError(f"{case_id}: one boolean verdict per criterion is required")
            if type(review["grounded"]) is not bool or not review.get("reason"):
                raise ValueError(f"{case_id}: semantic grounding verdict and review rationale are required")
            row.update(rubric_passed=sum(verdicts), grounded=review["grounded"],
                       strict_answer_pass=all(verdicts) and review["grounded"], review=review)
        rows.append(row)
    completed = [r for r in rows if r["status"] == "completed"]
    reviewed = [r for r in completed if r["rubric_passed"] is not None]
    example_runs = [r for r in completed if r["corpus"] == "example"]
    summary = {
        "total_cases": len(rows), "completed_cases": len(completed), "reviewed_cases": len(reviewed),
        "invalid_or_not_run": len(rows) - len(completed), "reviewer": reviews.get("reviewer"),
        "strict_answer_pass_rate": mean(r["strict_answer_pass"] for r in reviewed) if reviewed else None,
        "answer_rubric_coverage": (sum(r["rubric_passed"] for r in reviewed) /
                                  sum(r["rubric_total"] for r in reviewed)) if reviewed else None,
        "grounded_answer_rate": mean(r["grounded"] for r in reviewed) if reviewed else None,
        "required_source_open_recall": mean(r["result"]["objective_scores"]["required_source_open_recall"] for r in completed) if completed else None,
        "citation_count": sum(r["result"]["objective_scores"]["citation_count"] for r in completed),
        "valid_citations": sum(r["result"]["objective_scores"]["valid_citations"] for r in completed),
        "query_bounds_passes": sum(r["result"]["trace_checks"]["query_bounds_ok"] for r in completed),
        "example_navigation_passes": sum(r["result"]["trace_checks"]["example_navigation_ok"] for r in example_runs),
        "example_navigation_cases": len(example_runs),
        "mean_source_reads": mean(len(r["result"]["trace_checks"]["source_reads"]) for r in completed) if completed else None,
        "mean_elapsed_seconds": mean(r["result"]["elapsed_seconds"] for r in completed) if completed else None,
        "total_input_tokens": sum(r["result"]["trace_checks"]["usage"].get("input_tokens", 0) for r in completed),
        "total_cached_input_tokens": sum(r["result"]["trace_checks"]["usage"].get("cached_input_tokens", 0) for r in completed),
        "total_output_tokens": sum(r["result"]["trace_checks"]["usage"].get("output_tokens", 0) for r in completed),
    }
    save(root / "scores.json", {"summary": summary, "cases": rows})
    def fraction(value: object) -> str:
        return "not scored" if value is None else f"{float(value):.1%}"
    lines = ["# Synthetic RAG quality pilot", "",
             f"Run: {manifest['created_at']}. Model: `{manifest['model']}`; reasoning: `{manifest['reasoning_effort']}`.", "",
             "This evaluates retrieval and answer behavior under the company-wiki Query contract. It does not execute",
             "registry selection, initialization, curation, provider permissions, or publication. Fixture cases use",
             "direct source discovery; example cases use the shipped example wiki and synthetic originals.", "",
             "These are different corpora, so their results do not establish the incremental benefit of wiki routing.", "",
             f"Completed: **{len(completed)}/{len(rows)}**. Semantically reviewed: **{len(reviewed)}/{len(rows)}**.", "",
             "| Measurement | Result |", "|---|---:|",
             f"| Strict answer pass (all rubric items + grounded) | {fraction(summary['strict_answer_pass_rate'])} |",
             f"| Answer rubric coverage | {fraction(summary['answer_rubric_coverage'])} |",
             f"| Answers grounded in original evidence (semantic review) | {fraction(summary['grounded_answer_rate'])} |",
             f"| Required-source-open recall, mean per question | {fraction(summary['required_source_open_recall'])} |",
             f"| Citation integrity (exact quote + original read + inline reference) | {summary['valid_citations']}/{summary['citation_count']} |",
             f"| Within Query retrieval bounds | {summary['query_bounds_passes']}/{len(completed)} |",
             f"| Example navigation contract | {summary['example_navigation_passes']}/{summary['example_navigation_cases']} |",
             f"| Mean original documents opened | {summary['mean_source_reads']} |",
             f"| Mean elapsed seconds | {round(summary['mean_elapsed_seconds'], 1) if completed else 'not recorded'} |", "",
             "Citation integrity does not prove that a quote entails its associated claim. Semantic reviews assess",
             "the full answer against the sources and the explicit rubric. A review by an agent is not human validation.", "",
             "| Case | Corpus / category | Rubric | Grounded | Source recall | Sources opened | Seconds |",
             "|---|---|---:|---|---:|---|---:|"]
    for row in rows:
        case = cases[row["id"]]
        if row["status"] != "completed":
            lines.append(f"| {row['id']} | {case['corpus']} / {case['category']} | {row['status']} | — | — | — | — |")
            continue
        result = row["result"]
        rubric = f"{row['rubric_passed']}/{row['rubric_total']}" if row["rubric_passed"] is not None else "not scored"
        grounded = "not scored" if row["grounded"] is None else ("yes" if row["grounded"] else "no")
        lines.append(f"| {row['id']} | {case['corpus']} / {case['category']} | {rubric} | {grounded} | "
                     f"{fraction(result['objective_scores']['required_source_open_recall'])} | "
                     f"{', '.join(result['trace_checks']['source_reads'])} | {result['elapsed_seconds']:.1f} |")
    lines += ["", "## Evidence and limitations", "",
              "- One execution per question; no estimate of run-to-run reliability or production accuracy.",
              "- Twenty short synthetic questions; no large-corpus retrieval, long documents, live provider, or ACL acceptance claim.",
              "- Questions and gold criteria were authored by an agent; human calibration is still needed.",
              "- Correct-source recall uses the predeclared required documents, not an exhaustive relevance judgment.",
              "- Raw CLI traces, exact answers, prompts, source hashes, timing, token usage, and rubric reviews are retained.",
              "- CLI token usage includes host prompt/skill overhead. No monetary cost or pure retrieval-latency claim is made.",
              "- Original-source checksums are in `source-integrity.json`; example navigation is recorded per case.", "",
              f"Reviewer: `{json.dumps(reviews.get('reviewer'), ensure_ascii=False)}`", ""]
    for row in rows:
        lines += [f"## {row['id']}", "", cases[row["id"]]["question"], ""]
        if "result" not in row:
            lines += ["Not run.", ""]
            continue
        lines += [row["result"]["response"]["answer"], ""]
        if "review" in row:
            lines += [f"Review: {row['review']['reason']}", ""]
            for criterion, passed in zip(cases[row["id"]]["criteria"], row["review"]["criteria_passed"]):
                lines.append(f"- {'PASS' if passed else 'FAIL'}: {criterion}")
            lines.append("")
    # Resolve source-ID citations to the versioned synthetic originals in the repository.
    for doc in gold["documents"]:
        relative = os.path.relpath(REPOSITORY / doc["path"], root)
        lines.append(f"[{doc['id']}]: <{relative}>")
    (root / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    report(parser.parse_args().results.resolve())
