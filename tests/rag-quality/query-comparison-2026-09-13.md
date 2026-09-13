# Query reference comparison — September 13, 2026

Follow-up: the [comparison after citation and command fixes](query-comparison-fixed-2026-09-13.md)
is the latest controlled run. This page preserves the original experiment and its first-attempt results.

The strengthened Query reference preserved semantic answer quality on the 19 questions valid in both
conditions while using 12.2% fewer source reads and 6.0% fewer retrieved source characters. Mean elapsed
time fell 3.1%. These are modest efficiency differences in one run per question, not proof of a general
performance improvement. The updated condition had one invalid first attempt, and both conditions had
exact-quote formatting failures.

## What was compared

The historical benchmark did not load `query.md`: its prompt contained only a hardcoded subset of the
Query contract. A plain rerun could not test the edit. The runner now embeds a selected Query reference,
freezes it once per run, and records the exact bytes and hash. Benchmark-specific tool, routing, and
output constraints remain in force; registry and provider lifecycle steps remain outside this test.

- **Before:** `query.md` from Git commit `3af9b6954050f5dafe3afbbc9185513ad2b85fa2`.
- **After:** the strengthened working-tree version of `query.md` at execution, before the citation fix.
- Same 20 questions, source documents, wiki documents, harness, CLI `0.154.0`, model `gpt-6-astra`,
  and `high` reasoning effort. The evaluation date remains September 12 for both sets of questions.
- The two conditions ran concurrently, with one sequential question at a time per condition. Each
  question used a fresh ephemeral session. Diagnostic retries ran only after both main runs finished.
- No gold criteria were supplied to the evaluated sessions. Semantic grading was performed against
  the original sources by the agent that edited the Query reference, with condition labels visible;
  this was not blind or independent human review.

## First-attempt quality and execution

| Measurement | Before | After |
|---|---:|---:|
| Attempted questions | 20 | 20 |
| Valid executions | 100% (20/20 cases) | 95% (19/20 cases) |
| Semantic answer pass among valid executions | 20/20 | 19/19 |
| Atomic answer criteria passed | 59/59 | 56/56 |
| Required-source-open recall among valid executions | 100% | 100% |
| Exact-quote citation integrity | 95.9% (71/74 quotes) | 97.1% (66/68 quotes) |
| Valid executions within retrieval bounds | 20/20 | 19/19 |
| Example navigation checks | 8/8 | 8/8 |

Semantic answer pass means every answer criterion passed and the full answer was judged grounded.
It does not imply perfect citation formatting or execution validity. Invalid runs are excluded from
quality averages, never silently converted to successes.

**Execution failure:** After/FQ12 initially omitted `rag-` from the supplied temporary corpus path.
That command failed with file-not-found; the session then corrected it and answered correctly in
Chinese. The trace checker rejected the initial non-allowlisted command, so the whole attempt remains
invalid. A separate FQ12 retry in each condition passed execution, all three semantic criteria, and
all citation checks. Those retries do not replace the first attempts or enter the main averages.
One successful retry does not establish reliability or explain why the original mistake occurred.

**Citation failures:** Before/EQ01, Before/EQ04, and Before/EQ05 each had one quote that collapsed a
source line break. After/EQ04 had two such quotes. All five match after whitespace normalization,
and their claims are supported, but they fail the benchmark's unchanged exact-quote requirement.
No answer or quote was edited to improve its score.

## Effort on the same 19 valid questions

FQ12 is excluded from both conditions in this table. Comparing 20 before cases with 19 after cases
would confound the efficiency calculation with case selection.

| Measurement | Before | After | Change |
|---|---:|---:|---:|
| Mean source documents read | 2.58 | 2.26 | −12.2% |
| Mean original-source characters returned | 1,434.5 | 1,348.9 | −6.0% |
| Mean listing/search calls | 1.47 | 1.42 | −3.6% |
| Mean wiki documents read | 0.79 | 0.68 | −13.3% |
| Mean elapsed time, including CLI startup | 28.70 s | 27.82 s | −3.1% |
| Total input tokens | 1,728,420 | 1,711,008 | −1.0% |
| Cached input tokens, included above | 1,367,552 | 1,370,112 | +0.2% |
| Uncached input tokens | 360,868 | 340,896 | −5.5% |
| Total output tokens | 9,309 | 9,038 | −2.9% |

Source reads fell from 49 to 43 across the matched cases. Five questions used fewer source reads,
one used more, and thirteen were unchanged. Timing and token observations include host context,
model variability, caching, and service latency; they do not establish pure retrieval latency or
monetary savings. Both conditions started concurrently, but their progress and cache hits differed.

## Observed behavior

- **Focused reads:** leave approval (EQ03) and missing sick-leave entitlement (EQ08) each fell from
  three source reads to one. Ownership (FQ03), conflicting definitions (FQ07), and missing policy
  (FQ09) each saved one source read while retaining required evidence.
- **Gap-directed follow-up:** After/FQ08 and After/FQ09 searched, read relevant originals, then used
  the remaining search to investigate causal or policy evidence. Their Before counterparts spent
  one discovery call listing the directory before searching.
- **Explicit uncertainty:** After/EQ08 distinguished an unknown sick-leave allowance from zero.
  Both conditions qualified the absence of an approved telemetry policy, so that behavior was not
  unique to the edit.
- **No uniform reduction:** After/EQ06 read four sources instead of three, added a discovery call,
  and read one more wiki page while calculating churn. The broader investigation found no change
  to the required answer.

The small corpus already produces near-ceiling semantic scores. This experiment supports keeping
the clearer retrieval guidance, but does not establish an accuracy gain. Long-document passage
expansion remains untested because the adapter only returns full documents. The next useful test
would use longer sources and held-out questions, with repeated runs and independent grading.

## Historical baseline

The September 12 pilot recorded 20/20 semantic passes, 90/90 exact-quote checks, 2.70 mean source reads,
and 29.0 seconds mean elapsed time. Its question and source hashes, model, reasoning effort, and CLI
match this experiment, but its hardcoded prompt and runner differ. It is a historical reference, not
the control used to estimate the effect of the Query edit. See the
[historical pilot](pilot-2026-09-12.md).

## Evidence and verification

The following run artifacts are retained locally under the Git-ignored `results/` directory. They
include exact answers, raw traces, prompts, reviews bound to answer hashes, and execution snapshots;
they are not part of the versioned September 12 baseline.

- [Before scorecard](results/2026-09-13-query-comparison/before/report.md)
- [After scorecard](results/2026-09-13-query-comparison/after/report.md)
- [Paired metrics and per-question measurements](results/2026-09-13-query-comparison/paired-comparison.json)
- [Comparison design](results/2026-09-13-query-comparison/comparison-design.json)
- [Before verification](results/2026-09-13-query-comparison/before/verification.json)
- [After verification](results/2026-09-13-query-comparison/after/verification.json)
- [Before FQ12 diagnostic](results/2026-09-13-query-comparison/diagnostic-before/report.md)
- [After FQ12 diagnostic](results/2026-09-13-query-comparison/diagnostic-after/report.md)

All 40 main-run traces were revalidated with unchanged recorded checks, including the invalid case.
Every main-run prompt included its frozen Query reference. Reference, runner, dataset, and source
hashes matched their manifests; original documents remained unchanged. All 11 benchmark unit tests
passed, including a new test that changes the reference during execution and verifies that all
questions still receive the original snapshot. Trace checks remain evaluation checks, not provider
access-control enforcement.
