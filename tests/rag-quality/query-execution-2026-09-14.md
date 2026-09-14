# Synchronous execution follow-up — September 14, 2026

The new paired run completed **20/20 valid executions in both conditions**, with all **130 command
payloads** present and all **135 citation checks** passing. Strict answer passes were **20/20 Before
and 19/20 After**: After/EQ05 omitted an explicit calendar-month qualifier from its answer, although
its citation included it. Source reads fell from 55 to 48 (12.7%). This is a new observation under a
hardened command backend; it does not replace the historical 20/20 versus 19/20 execution result.

## Failure boundary and mitigation

The [September 13 corrected comparison](query-comparison-fixed-2026-09-13.md) retains an After/FQ04
`./corpus-tool list` event with exit code zero and empty `aggregated_output`. The strict JSON check
correctly rejected it. The trace does not establish whether output emission or CLI capture failed.

The bound launcher returned the exact expected listing in 100/100 direct shell checks. A fresh
forced-listing diagnostic on the original backend also passed, so the historical failure was not
reproduced. The runner now passes `--disable unified_exec` to select synchronous shell execution
for its short, bounded corpus commands, and records the override in its manifest. This is an
execution-backend mitigation, not a confirmed explanation or repair of the historical mechanism.
The launcher, Query references, trace validator, and exact-quote scorer are unchanged. Empty or
truncated output still invalidates an attempt even when a later read and the answer succeed.

## Focused verification

- All 19 benchmark/report unit tests passed, including rejection of missing or truncated listing
  output followed by a successful read, and preservation of the read-only sandbox and recorded override.
- Six fresh FQ04 diagnostics forced `list` as the first operation: three with each frozen retrieval
  guide. All six returned the exact 2,096-byte listing, passed all 18 answer criteria, and passed
  all 22 citation checks. They finished before the full comparison began.
- All 42 historical comparison and diagnostic traces revalidated to their original outcomes.
  The historical After/FQ04 remains invalid and unscored. AST checks confirm that the trace validator
  and citation scorer are unchanged.
- One preliminary launch was blocked by the outer host sandbox before a model session started.
  It remains in the investigation directory and is excluded from the separately designed paired run.
  The subsequent authorized original-backend diagnostic passed; it is not part of the six mitigated cases.

## Fresh paired comparison

The same frozen Before and After Query references from the corrected comparison were reused byte
for byte. Both conditions used the new runner, identical questions, synthetic originals, budgets,
answer schema, `gpt-6-astra`, high reasoning effort, and Codex CLI `0.154.0`. The evaluation date
remained September 12, 2026. Two conditions ran concurrently, with sequential fresh ephemeral
sessions within each condition. Main-run prompts did not force listing and differ only in their
Query-reference blocks. All first attempts are retained; no diagnostic result is substituted.

| Measurement | Original retrieval | Strengthened retrieval |
|---|---:|---:|
| Valid executions | 100% (20/20) | 100% (20/20) |
| Strict answer passes | 20/20 | 19/20 |
| Atomic answer criteria satisfied | 59/59 | 58/59 |
| Grounded answers | 20/20 | 20/20 |
| Required-source-open recall | 100% | 100% |
| Exact citation integrity | 100% (68/68 quotes) | 100% (67/67 quotes) |
| Within retrieval bounds | 20/20 | 20/20 |
| Example navigation checks | 8/8 | 8/8 |
| Chinese question FQ12 | Pass | Pass |
| Total source reads | 55 | 48 |
| Mean source reads, all 20 cases | 2.75 | 2.40 |
| Mean source characters, all 20 cases | 1,615.75 | 1,435.35 |
| Mean discovery calls | 1.70 | 1.50 |
| Mean elapsed time | 29.42 s | 26.64 s |
| Total input tokens | 1,917,245 | 1,857,122 |
| Uncached input tokens | 372,029 | 392,418 |

All 20 cases, including FQ04 and EQ05, enter both effort averages. Source characters fell 11.2%,
total input tokens fell 3.1%, and uncached input rose 5.5%. Timing includes startup and service
latency; it establishes neither pure retrieval speed nor monetary savings. The changed backend
also prevents attributing differences between this experiment and the earlier run to guidance alone.

**Answer-quality qualification:** After/EQ05 states a monthly formula and uses the population at the
start of the month, but does not explicitly say calendar month in its answer text. Its exact citation
does contain that qualifier. Under conservative answer-text grading, the period criterion is marked
incomplete; the other three criteria pass and the answer contains no unsupported assertion. Before/EQ05
states calendar month explicitly. The observed reduction in reads therefore does not establish
unchanged strict answer quality. The implementing agent reviewed all 40 answers against frozen criteria
and originals with condition labels visible; this is not independent or human-calibrated grading.

## Evidence and limits

The current code change removes the interactive execution path from this benchmark. The successful
repeat supports using that mitigation, but a small synthetic run cannot establish a failure-rate
reduction, prove the original cause, or guarantee future capture reliability. There is no provider ACL,
lifecycle, long-document, or production-quality claim. The Query references predate later learning,
source-access, and capability changes; this repeat does not evaluate those additions.

| Artifact | SHA-256 |
|---|---|
| Follow-up runner | `701acca3a7fbab36e8bf23953902f89ca44f4b763ad1e8a0140c7df1062e0215` |
| Dataset | `f1d34da1b835ea51cde3a5049c3c3cd5108ab91214b209b768785735187ae54a` |
| Frozen Before Query | `09dbcdb8301f81c2025a837756e85f84d631bb3ae0377f68c49985f8f6f573e9` |
| Frozen After Query | `530da0a1c54c2aa4c7797f82c7275fb09b044f6fd8f2e01d08e846f73ea51d98` |

All 40 main traces, 130 command payloads, source hashes, launcher bindings, answer hashes, and
objective scores were rechecked. All originals remained unchanged. Raw execution artifacts stay
in Git-ignored local results; this tracked report does not provide an independently reproducible
command-level archive.

- [Comparison design](results/2026-09-14-query-comparison-synchronous/comparison-design.json)
- [Before scorecard and reviewed answers](results/2026-09-14-query-comparison-synchronous/before/report.md)
- [After scorecard and reviewed answers](results/2026-09-14-query-comparison-synchronous/after/report.md)
- [Paired measurements](results/2026-09-14-query-comparison-synchronous/paired-comparison.json)
- [Main-run verification](results/2026-09-14-query-comparison-synchronous/verification.json)
- [Historical revalidation](results/2026-09-14-query-comparison-synchronous/historical-revalidation.json)
- [Direct listing checks](results/2026-09-14-empty-output-investigation/direct-list-checks.json)
- [Six forced-listing diagnostics](results/2026-09-14-empty-output-investigation/synchronous-diagnostics.json)
