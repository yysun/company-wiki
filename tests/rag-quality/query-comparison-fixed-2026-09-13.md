# Query comparison after citation and command fixes — September 13, 2026

The refreshed comparison supports keeping the strengthened retrieval guidance. On the 19 questions
valid in both conditions, it used **19.0% fewer source reads** and **17.0% fewer source characters**
with unchanged semantic answer quality. All **118 citation checks** passed across valid executions,
including 70 multiline quotes. The Chinese case passed in both conditions.

One new trace-integrity failure remains visible: an After/FQ04 listing command recorded empty output.
The full run therefore has 20/20 valid executions before and 19/20 after. The earlier comparison and
its failures are preserved; this report records a new experiment.

## Controlled comparison

- **Before:** original retrieval guidance from `3af9b6954050f5dafe3afbbc9185513ad2b85fa2`, with the
  same exact-quote preservation paragraph added as in the current Query reference.
- **After:** current Query reference, including strengthened search, reading, and stopping guidance.
- Both use the fixed `./corpus-tool` launcher, identical benchmark citation instructions, the same
  exact-match scorer, and the same 20 questions and synthetic sources.
- Model: `gpt-6-astra`; reasoning: `high`; CLI: `0.154.0`. The question evaluation date remains
  September 12, 2026. The two conditions ran concurrently, with sequential fresh sessions within
  each condition. Two separate diagnostic sessions ran after both main conditions completed.

Both references receive the citation fix so this experiment isolates retrieval guidance. Verification
confirmed that each paired prompt differs only inside its Query-reference block. Registry, provider
permissions, publication, and long-document passage retrieval remain outside this component test.

## First-attempt quality

| Measurement | Before | After |
|---|---:|---:|
| Attempted questions | 20 | 20 |
| Valid executions | 100% (20/20 cases) | 95% (19/20 cases) |
| Semantic answer passes among valid executions | 20/20 | 19/19 |
| Atomic answer criteria passed | 59/59 | 56/56 |
| Required-source-open recall among valid executions | 100% | 100% |
| Exact citation integrity | 100% (69/69 quotes) | 100% (49/49 quotes) |
| Valid executions within retrieval bounds | 20/20 | 19/19 |
| Example navigation checks | 8/8 | 8/8 |
| Chinese case FQ12 | Pass | Pass |

Execution rates count cases; citation rates count quotations from valid executions only. Citation
integrity stayed at 100% in both conditions. The matched 19 cases produced 66 quotes before and 49
after; the other three Before quotes belong to FQ04, whose After execution was invalid. Fewer quotes
are not a reduction in citation accuracy or required-source coverage.

The previous citation failures in EQ01, EQ04, and EQ05 did not recur in either condition. Quotes were
checked as decoded strings against the original text, with no whitespace normalization or repairs.

**Remaining execution issue:** After/FQ04 recorded `./corpus-tool list` as completed with exit code 0
but an empty output payload. The strict JSON check correctly invalidated the attempt. Its final answer
gave the correct six-hour and next-business-day on-site commitments, but it receives no quality score.
The empty payload's cause is unconfirmed; the retained trace does not establish a Query-logic defect.

Both separate FQ04 diagnostics passed execution, all three semantic criteria, and citation checks.
The Before diagnostic exercised `list` successfully; the After diagnostic used only `search` and
`read`. Those successes do not resolve the empty-list observation or replace its failed first attempt.

## Effort on the same 19 valid questions

FQ04 is excluded from both conditions below. FQ12 is included in both.

| Measurement | Before | After | Change |
|---|---:|---:|---:|
| Mean source documents read | 3.05 | 2.47 | −19.0% |
| Mean source characters returned | 1,746.7 | 1,448.9 | −17.0% |
| Mean listing/search calls | 1.63 | 1.42 | −12.9% |
| Mean wiki documents read | 0.84 | 0.79 | −6.25% |
| Mean elapsed time, including CLI startup | 29.11 s | 25.89 s | −11.0% |
| Total input tokens | 1,786,176 | 1,721,753 | −3.6% |
| Cached input tokens, included above | 1,605,120 | 1,402,368 | −12.6% |
| Uncached input tokens | 181,056 | 319,385 | +76.4% |
| Total output tokens | 8,874 | 7,744 | −12.7% |

Source reads fell from 58 to 47: seven questions used fewer reads, twelve were unchanged, and none
used more. The larger reductions were Q2/Kestrel diagnosis (five to three), leave approval (three to
one), the churn formula (four to two), and missing sick-leave entitlement (three to one). Each retained
the required evidence and answer qualifications.

Elapsed time includes startup, service latency, and concurrent execution. Cache behavior differed
substantially: uncached input increased despite lower total input. These observations establish
neither pure retrieval latency nor monetary savings.

## Judgment and relationship to the earlier run

Keep the strengthened retrieval guidance. This repeat supports the earlier observation of fewer
unnecessary reads while preserving answers, authority distinctions, and explicit uncertainty. The
citation and Chinese-command fixes also held across the full comparison's relevant cases.

The [original comparison](query-comparison-2026-09-13.md) measured 12.2% fewer reads and 6.0% fewer
source characters. This follow-up shows the same direction, but uses shared fixes and a different
matched set: the original excluded FQ12, while this one excludes FQ04. Each percentage is a comparison
within its own experiment; differences between them do not isolate the effect of the fixes.

This remains one execution per question and condition on short, familiar synthetic documents. The
implementing agent reviewed the answers against the frozen criteria and originals with condition
labels visible. There is no independent human grading, demonstrated accuracy gain, or production
reliability estimate. The empty-output issue needs separate investigation before treating the harness
as consistently reliable.

## Evidence and verification

All 40 main traces and both diagnostic traces were revalidated against their recorded checks. Query,
runner, dataset, launcher, corpus-binding, and original-source hashes matched. The citation scorer
matches the pre-fix implementation, and original sources remained unchanged. All 39 valid main answers
and both diagnostic answers have semantic reviews bound to their exact response bytes.

The exact prompts, answers, traces, reviews, and snapshots remain in Git-ignored `results/`. The
tracked summaries preserve the conclusions; raw local artifacts are not part of the versioned baseline.

- [Before scorecard](results/2026-09-13-query-comparison-fixed/before/report.md)
- [After scorecard](results/2026-09-13-query-comparison-fixed/after/report.md)
- [Paired metrics and per-question measurements](results/2026-09-13-query-comparison-fixed/paired-comparison.json)
- [Comparison design](results/2026-09-13-query-comparison-fixed/comparison-design.json)
- [Aggregate verification](results/2026-09-13-query-comparison-fixed/verification.json)
- [Revalidation and comparison script](results/2026-09-13-query-comparison-fixed/verify-comparison.py)
- [Before FQ04 diagnostic](results/2026-09-13-query-comparison-fixed/diagnostic-before/report.md)
- [After FQ04 diagnostic](results/2026-09-13-query-comparison-fixed/diagnostic-after/report.md)
- [Diagnostic design](results/2026-09-13-query-comparison-fixed/diagnostic-design.json)
- [Empty-output observation](results/2026-09-13-query-comparison-fixed/execution-observations.json)

## Subsequent execution follow-up

The [September 14 synchronous follow-up](query-execution-2026-09-14.md) documents a backend
mitigation and a new 20/20 versus 20/20 execution result. The historical observations, exclusions,
and measurements above are unchanged. The original empty-output mechanism remains unconfirmed;
the new run reports its own answer-quality qualification separately.
