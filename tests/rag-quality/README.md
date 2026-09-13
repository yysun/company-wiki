# Synthetic RAG quality benchmark

Twenty questions test retrieval and answer behavior with two bounded synthetic corpora:

- **12 fixture questions:** current/superseded/draft policy, ownership, vocabulary mismatch, a numeric
  approval boundary, conflicting definitions, multi-source diagnosis, missing evidence, a false premise,
  project intent versus delivery, and a Chinese query over English sources.
- **8 example questions:** the shipped example wiki routes to seven synthetic original documents.
  Cases cover aliases, policy versions, approvals, subscription definitions, metric exclusions,
  arithmetic across documents, causal uncertainty, and an unanswerable sick-leave question.

Browse the [questions and evaluator answer key](questions.md) and the
[tracked pilot summary](pilot-2026-09-12.md). The [versioned baseline](baselines/2026-09-12/README.md)
preserves the original answers, scores, retrieval records, and grading decisions. Disposable runs and
raw CLI logs stay in the Git-ignored `results/` directory.

The example wiki stays in `examples/sample-company/`; original evidence stays separately in
`examples/sample-company-sources/`. Existing source fixtures are unchanged. No cloud connection or
user registry is used, and no governed or confidential fixture is exposed to the evaluated process.

## What this measures

This is a **Query-contract component pilot**, not a full lifecycle acceptance test. An actual Codex
session retrieves documents through a bounded read-only tool and produces an answer. The tool offers
directory listing, regex search over originals, and full document reads. It is a deterministic fixture
adapter, not a claim about native provider search relevance or permissions.

The runner embeds the current `skills/company-wiki/references/query.md` in every evaluated prompt.
Use `--query-contract /path/to/query.md` to compare a different version under the same harness. The
reference is frozen once per run and retained with its hash. Benchmark-specific tools, routing, and
output rules take precedence; the reference does not activate registry or provider lifecycle steps.
The September 12 baseline predates this integration and used only the runner's hardcoded contract,
so it cannot by itself measure the effect of changes to `query.md`.

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

Exact-quote checks run on the decoded JSON string. A source line break must survive JSON serialization;
replacing it with a space or a literal backslash sequence fails. The Query reference and benchmark prompt
make this preservation requirement explicit. The scorer does not normalize whitespace or repair answers.

Reports show execution and citation pass percentages with their counts. Execution rates count cases;
citation rates count quotations from valid executions. For example, `100% (69/69 quotes)` and
`100% (49/49 quotes)` have the same integrity rate despite different quotation counts. Invalid
executions remain visible and receive no quality scores.

Trace checks reject commands outside the exact corpus-tool invocation and reject other observed tools.
They are evidence checks, not an operating-system security boundary. Source hashes verify the original
documents remain unchanged. Invalid runs stay visible and do not receive quality scores.

Each new session uses `./corpus-tool list`, `./corpus-tool search 'pattern'`, or
`./corpus-tool read ID [ID ...]` from its supplied working directory. A generated launcher binds that
command to the exact corpus; caller arguments cannot override the corpus path. This avoids asking the
model to reproduce a long temporary path. Launcher and corpus hashes are checked after execution.
Historical traces use their original long-path contract; new runs accept only the short launcher contract.

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
New cases also retain `corpus-tool-at-execution.sh` and `tool-binding.json`, recording the exact launcher,
corpus binding, and their hashes for trace revalidation. These are execution evidence, not reusable tools.

New runs also save `query-contract-at-execution.md`, `dataset-at-execution.json`, and
`runner-at-execution.py`. For a before/after comparison, use identical questions, corpora, model,
reasoning effort, and harness; vary only the Query reference. Record execution concurrency when
comparing timing. Full-document-only retrieval does not test passage expansion in long documents.

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

## Retain a baseline

Keep `results/` for scratch runs. Promote a reviewed run into a new `baselines/<run-id>/` directory;
keep failures and unscored cases visible, and never replace the observations with a rerun.

Preserve this explicit evidence set:

- `manifest.json`, `reviews.json`, `source-integrity.json`, and `verification.json` when present;
- `dataset-at-execution.json`, whose bytes must match the manifest's dataset hash;
- `runner-at-execution.py` when needed to preserve the exact evaluated code version;
- `query-contract-at-execution.md` when the run manifest records `query_contract_sha256`;
- each case's exact `response.json` and `result.json`, including citations, ordered retrieval operations,
  scores, timing, and token usage;
- regenerated `scores.json` and `report.md`, plus a short README explaining provenance and limits.

Copy the retained answer bytes unchanged so the grading hashes remain valid. Use an allowlist rather
than copying whole case directories: `prompt.txt`, `trace.jsonl`, stderr, and temporary local paths are
execution artifacts. Document omitted raw traces; processed retrieval records preserve the observations
but do not independently reproduce the original command-level validation. Real-data runs additionally
need an authorized storage destination for their content; this baseline contains synthetic material only.

Archived reports use their own dataset snapshot and check both its hash and the binding between the
scored answer and the retained response. They can be regenerated without running the model:

```bash
python3 tests/rag-quality/report.py tests/rag-quality/baselines/2026-09-12
```

Before committing a baseline, compare its scores with the reviewed run and verify that Git includes the
baseline evidence while continuing to ignore disposable results. Full raw traces needed for a separate
audit can be retained as controlled CI artifacts rather than mixed into the baseline.

These questions are development cases, not a hidden release benchmark. Expand with held-out questions,
larger corpora, repeated runs, and human-calibrated grading before making production-quality claims.
Provider ACL/publication acceptance remains in the existing lifecycle test specifications.

The [September 13 Query-reference comparison](query-comparison-2026-09-13.md) runs the previous and
strengthened instructions through the same harness and reports first-attempt failures separately
from semantic quality and matched-case retrieval effort.

The [citation line-break fix](citation-fix-2026-09-13.md) records three repeated runs of the affected
questions after explicit quote-preservation guidance, with the exact-match scorer unchanged.

The [Chinese-case command fix](command-fix-2026-09-13.md) replaces long temporary-path invocations
with a corpus-bound launcher. It records three Chinese and three cancellation-case reruns, plus
revalidation of all 51 earlier traces without changing their outcomes.

The [comparison after citation and command fixes](query-comparison-fixed-2026-09-13.md) is the latest
full comparison: both references share the fixes, so only retrieval guidance differs. It preserves
all 40 first attempts and reports a new empty-output failure separately from two diagnostic retries.
