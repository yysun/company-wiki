# Synthetic RAG quality benchmark

Twenty questions test retrieval and answer behavior with two bounded synthetic corpora:

- **12 fixture questions:** current/superseded/draft policy, ownership, vocabulary mismatch, a numeric
  approval boundary, conflicting definitions, multi-source diagnosis, missing evidence, a false premise,
  project intent versus delivery, and a Chinese query over English sources.
- **8 example questions:** the shipped example wiki routes to seven synthetic original documents.
  Cases cover aliases, policy versions, approvals, subscription definitions, metric exclusions,
  arithmetic across documents, causal uncertainty, and an unanswerable sick-leave question.

Browse the [questions and evaluator answer key](questions.md) and the
[tracked pilot summary](pilot-2026-09-12.md). Raw scorecards, answers, and traces remain local under
the Git-ignored `results/` directory.

The example wiki stays in `examples/sample-company/`; original evidence stays separately in
`examples/sample-company-sources/`. Existing source fixtures are unchanged. No cloud connection or
user registry is used, and no governed or confidential fixture is exposed to the evaluated process.

## What this measures

This is a **Query-contract component pilot**, not a full lifecycle acceptance test. An actual Codex
session retrieves documents through a bounded read-only tool and produces an answer. The tool offers
directory listing, regex search over originals, and full document reads. It is a deterministic fixture
adapter, not a claim about native provider search relevance or permissions.

The fixture cases use direct source discovery. The example cases start from the existing example home,
read at most three additional wiki pages before original evidence, and then answer from originals.
The corpora differ: comparing those two groups does **not** measure wiki lift. For that experiment,
the same example questions, original corpus, model, and budgets must also run without wiki routing.

`dataset.json` contains the document mappings, questions, required evidence IDs, and atomic answer
criteria. Gold criteria are never included in the evaluated agent's prompt or corpus. A fresh ephemeral
session receives one question at a time. Responses from other questions are not carried forward.

## Recorded metrics

| Measurement | Definition and limit |
|---|---|
| Required-source-open recall | Required original documents opened / required original documents, per case. Search snippets alone do not count as a full read. This is not exhaustive relevance recall. |
| Citation integrity | Citation quotes must occur exactly in an original read during the run, and the source ID must appear inline in the answer. This does not establish semantic entailment. |
| Answer rubric coverage | Passed atomic criteria / total criteria, entered in a separate semantic review. Missing reviews remain null. |
| Grounded answer | Reviewer checks the complete answer for unsupported factual assertions, including qualifications, inference, and attribution. This is a binary rubric assessment, not the Ragas faithfulness algorithm. |
| Strict answer pass | Every answer criterion passes and the answer is grounded. |
| Query bounds | At most two listing/search calls combined, five original document reads, and 40,000 source characters. Repeated reads count again. |
| Example navigation | Home first, no more than three additional wiki reads, and no wiki reads after original-source search/read begins. |
| Effort | Ordered reads, discovery calls, retrieved source characters, wall time, and CLI token usage. Tokens include host context; wall time includes CLI startup. |

Trace checks reject commands outside the exact corpus-tool invocation and reject other observed tools.
They are evidence checks, not an operating-system security boundary. Source hashes verify the original
documents remain unchanged. Invalid runs stay visible and do not receive quality scores.

## Run

Requirements: Python 3.10+ and an authenticated Codex CLI supporting `exec --json --ephemeral`,
`--ignore-user-config`, `--output-schema`, and a read-only sandbox. No additional Python package or
RAG evaluation service is required. Each question consumes a model call/session.

From the repository root:

```bash
python3 -m unittest discover -s tests/rag-quality -p 'test_*.py' -v
python3 tests/rag-quality/benchmark.py run \
  --output tests/rag-quality/results/my-run \
  --model gpt-6-astra --effort high
```

Use `--only FQ01,EQ06` for a small smoke run. Output directories must be new; previous observations
are never overwritten. The CLI may need host permission to initialize its own state and connect to
the model; the evaluated session itself still runs with `--sandbox read-only`.

Each case retains `prompt.txt`, `trace.jsonl`, `response.json`, `result.json`, and CLI stderr. The run
manifest records CLI/model settings, exact dataset/runner hashes, and source versions. Temporary
corpus snapshots contain synthetic text only and are removed after each session.

The first pilot also retains `runner-at-execution.py` and `dataset-at-execution.json` as audit snapshots.
`verification.json` records the final validator version and rechecks of the raw traces. Use the runner
above for new executions; the historical snapshot is not a standalone installation.

## Semantic review and report

Read each actual answer against the gold criteria and original evidence. Write `reviews.json` inside
the run directory, explicitly identifying the reviewer and binding each review to the answer bytes:

```json
{
  "reviewer": {"type": "human-or-agent", "name": "actual reviewer", "method": "source-backed rubric review"},
  "cases": {
    "FQ01": {
      "response_sha256": "SHA-256 of FQ01/response.json",
      "criteria_passed": [true, true, true],
      "grounded": true,
      "reason": "Explain the observed answer and evidence, including any failure."
    }
  }
}
```

Then render the scorecard:

```bash
python3 tests/rag-quality/report.py tests/rag-quality/results/my-run
```

This creates `scores.json` and `report.md`. A report without semantic reviews is valid, but answer
correctness and grounding remain **not scored**. Edited answers invalidate their old reviews; a
changed dataset requires the original dataset version for reporting.

These questions are development cases, not a hidden release benchmark. Expand with held-out questions,
larger corpora, repeated runs, and human-calibrated grading before making production-quality claims.
Provider ACL/publication acceptance remains in the existing lifecycle test specifications.
