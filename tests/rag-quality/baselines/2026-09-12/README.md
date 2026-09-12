# Recorded RAG baseline — September 12, 2026

This is the original 20-question synthetic pilot, preserved without another model run. All 20 answers
passed all 59 rubric criteria and the agent grounding review; citation integrity was 90/90. The same
agent authored the cases and reviewed the answers. These are development results, not a production
accuracy estimate or a measurement of wiki lift.

Read the [full scorecard and answers](report.md), the [machine-readable scores](scores.json), or the
[pilot summary](../../pilot-2026-09-12.md).

## Evidence map

| Artifact | Retained evidence |
|---|---|
| [manifest.json](manifest.json) | Model and reasoning settings, CLI version, run timestamp, document IDs/paths/hashes, dataset and runner hashes. |
| [dataset-at-execution.json](dataset-at-execution.json) | Exact questions, original-source mappings, and answer criteria used for this run. |
| [reviews.json](reviews.json) | Reviewer identity, every criterion verdict, grounding decisions, rationales, and original answer hashes. |
| Each case's `response.json` | Exact original answer bytes and quoted citations. For example, [FQ01](FQ01/response.json). |
| Each case's `result.json` | Run status, answer, ordered reads/searches, observed source IDs, objective checks, timing, and token usage. For example, [FQ01](FQ01/result.json). |
| [scores.json](scores.json) | Aggregate and per-case scores, including the reviewed answer and retrieval records. |
| [verification.json](verification.json) | Test outcomes and the recorded revalidation verdicts for all 20 raw traces. |
| [source-integrity.json](source-integrity.json) | Original-source preservation outcome. |
| [runner-at-execution.py](runner-at-execution.py) | Exact runner code before final trace-validator hardening; an audit snapshot, not a standalone installation. |

All retained material is synthetic. No answer was regenerated, reworded, or regraded during archival.
Answer hashes still match the original reviews. Rebuilding the scorecard uses the archived dataset,
so later edits to the development question set do not change the historical rubric.

## Provenance and verification

The source fixtures, dataset, and final validator are available in repository revision `6a03a0a`.
That is an archive lookup reference established after the run, not a claim about the run's Git HEAD.
The manifest preserves the exact source and execution-version hashes; the historical runner snapshot
matches its recorded hash.

From the repository root, regenerate the report without a model call:

```bash
python3 tests/rag-quality/report.py tests/rag-quality/baselines/2026-09-12
```

Raw CLI traces, exact prompts containing temporary paths, and stderr remain local under the Git-ignored
`tests/rag-quality/results/2026-09-12-pilot/` directory. The baseline retains processed retrieval records
and validation verdicts. Repeating the original command-level validation requires those raw traces;
the archived records alone do not prove provider ACLs, sandbox enforcement, or full lifecycle behavior.

Keep this baseline as the historical observation. Use a new directory for a new run or explicitly
record any later grading correction; do not silently replace these answers with a fresh execution.
