# Query learning handoff — September 13, 2026

Query now uses approved investigation patterns as fallible routing context and can offer one useful lesson for
optional Curate after answering. Curate reconciles the candidate with existing knowledge and proposes concrete
edits under the existing approval protocol. Users improve wiki knowledge through normal use; they do not edit the
skill. Query remains read-only and retains the same routing phase, evidence requirements, and retrieval bounds.

The revised guidance passed all six targeted learning scenarios, compared with five for the previous guidance.
The difference was the useful-lesson handoff: both versions answered the synthetic customer-service question
correctly, but only the revised version suggested retaining the customer-specific authority route.

Both versions passed all 20 questions in the existing RAG benchmark, with no execution or citation failures.
The revised run used 8.2% fewer source reads and 6.0% fewer source characters, but 4.6% more input tokens. Elapsed
time was essentially unchanged. These are single-run observations, not evidence of accumulated cross-query gains.

## Controlled comparison

- Before: the Query reference at `48fb719`, frozen before this change.
- After: the same reference plus approved-pattern routing and optional learning-handoff guidance.
- Model: `gpt-6-astra`; reasoning: `high`; CLI: `0.154.0`.
- Identical 20 questions, synthetic corpora, tools, budgets, answer schema, and exact-citation scorer.
- One fresh ephemeral session per question and condition; no answer or lesson carries between sessions.
- Two concurrent condition processes, sequential questions within each. The stage-probe process also ran
  concurrently for part of the experiment. Timing includes startup, service latency, and shared resource effects.
- All 40 paired prompts differ only inside their frozen Query-reference block. No main-benchmark reruns replaced
  observations. The runner and dataset were unchanged from the existing benchmark.

The changes to the skill entry point and Curate reference were reviewed as contracts; the full RAG runner embeds
only the Query reference. It does not execute registration, provider access, curation writes, or skill discovery.

## First-attempt answer quality

| Measurement | Before | After |
|---|---:|---:|
| Valid executions | 20/20 | 20/20 |
| Semantic answer passes | 20/20 | 20/20 |
| Atomic answer criteria | 59/59 | 59/59 |
| Required-source-open recall | 100% | 100% |
| Exact citation integrity | 55/55 quotes | 56/56 quotes |
| Within retrieval bounds | 20/20 | 20/20 |
| Example navigation contract | 8/8 | 8/8 |
| Chinese question | Pass | Pass |

Citation integrity verifies exact quotes, observed original reads, and inline references; semantic support was
reviewed separately. The implementing agent reviewed all answers against the fixed criteria and original evidence
with condition labels visible. This is not independent or human grading. No answer-accuracy improvement was measured.

## Effort on all 20 matched questions

| Measurement | Before | After | Change |
|---|---:|---:|---:|
| Total original-document reads | 49 | 45 | −8.2% |
| Mean original-document reads | 2.45 | 2.25 | −8.2% |
| Mean source characters returned | 1,454.4 | 1,367.3 | −6.0% |
| Mean listing/search calls | 1.40 | 1.50 | +7.1% |
| Mean wiki reads | 0.85 | 0.85 | Unchanged |
| Mean answer characters | 368.35 | 377.70 | +2.5% |
| Mean elapsed seconds | 28.20 | 28.17 | −0.1% |
| Total input tokens | 1,838,209 | 1,922,799 | +4.6% |
| Cached input tokens, included above | 1,466,240 | 1,582,720 | +7.9% |
| Uncached input tokens | 371,969 | 340,079 | −8.6% |
| Total output tokens | 8,419 | 8,775 | +4.2% |

The read reduction came entirely from EQ01 (leave entitlement) and EQ03 (leave approval): each used one original
instead of three. The other 18 questions used the same number of originals. All required evidence and answer
qualifications were retained. The revised answers did not add routine Curate pitches to this question set.

Do not attribute these differences to learned wiki content: this experiment saved no lessons and evaluated each
question independently. The extra prompt content, model variability, and cache behavior prevent a general speed
or cost claim. The relevant observed feature improvement is the targeted handoff below.

## Learning scenarios

The [probe specification](query-learning-probes.md) covers six synthetic stage-level scenarios. Each condition
received the same supplied routing context and original excerpts in a fresh session. Expected outcomes were hidden
from the evaluated agent. L01–L05 start after retrieval; L06 tests the initial routing decision. No tool use was
needed or authorized. Neither stage executes a durable write or proves an end-to-end learning lifecycle.

| Scenario | Before | After |
|---|---|---|
| L01 — New customer-specific authority distinction | Correct answer; no Curate suggestion | Correct answer plus one supported, conditional suggestion |
| L02 — Explicit do-not-curate preference | Pass | Pass |
| L03 — Routine lookup with an existing route | Pass; no duplicate suggestion | Pass; no duplicate suggestion |
| L04 — Failed search does not prove absence | Pass | Pass |
| L05 — Current originals supersede a stale pattern note | Pass | Pass |
| L06 — Approved pattern guides routing without overriding bounds | Pass | Pass |
| All scenario criteria satisfied | 5/6 scenarios; 13/14 criteria | 6/6 scenarios; 14/14 criteria |

In L01, the originals establish an eight-hour general response commitment and a signed two-hour Helios exception.
The revised answer proposes a customer-schedule route and checking applicable signed overrides before applying
general policy, citing both originals. It does not claim to have saved the suggestion or generalized it into an
unconditional precedence rule. Both versions retain correct factual answers across these stage probes.

### Probe-checker correction

The initial stage checker classified every `error` event as an unauthorized action. All 12 probe traces contained
the same CLI startup notice about shortened skill descriptions, so their original `result.json` files show invalid.
Inspection established that this was a non-action host notice, also present in the main benchmark; it was not a
tool call or failed model execution. The main benchmark's existing checker already handles that event type.

The probe revalidator accepts only that exact notice alongside reasoning and answer events. Other errors and all
tool actions still fail; rejection checks cover a shell write, an MCP call, another error, and a modified notice.
It revalidated all 12 traces with no tool actions. Original results, prompts, traces, and answer bytes remain
unchanged; corrected validation is stored separately. The scenario scores above use that corrected classification,
not replacement model runs or edited answers.

## Verification and review

- All 40 main traces revalidated against recorded checks; frozen prompts, Query references, dataset, runner,
  launcher bindings, and source hashes matched. Original sources remained unchanged.
- The current Query reference matches the frozen After reference byte for byte. Citation guidance and the scorer
  are unchanged. There were 37 multiline quotes before and 35 after, all exact.
- All semantic reviews bind to the exact answer bytes. All 12 stage-probe traces and paired prompts were checked.
- 18 RAG runner/report tests and 23 adapter/lifecycle tests passed: 41 distinct existing tests. The nine lifecycle
  contract tests passed again after the entry-point and README updates.
- `git diff --check` passed.

CR risk: low — localized, reversible guidance changes preserve retrieval, approval, source, and write boundaries.

CR review round: 1; reviewer: not applicable — reviewed locally under the low-risk workflow.

CR passed: no major findings.

## Evidence and limits

The tracked report preserves the comparison and review conclusions. Exact execution artifacts remain in the
Git-ignored local results directory; they are synthetic, and no real company corpus or user registry was accessed.

- [Before scorecard and reviewed answers](results/2026-09-13-query-learning/before/report.md)
- [After scorecard and reviewed answers](results/2026-09-13-query-learning/after/report.md)
- [Paired measurements](results/2026-09-13-query-learning/paired-comparison.json)
- [Frozen comparison design](results/2026-09-13-query-learning/comparison-design.json)
- [Main verification](results/2026-09-13-query-learning/verification.json)
- [Exact learning cases and criteria](results/2026-09-13-query-learning/learning-cases.json)
- [Learning-probe summary](results/2026-09-13-query-learning/learning-probes/summary.json)
- [Probe execution script](results/2026-09-13-query-learning/run-learning-probes.py)
- [Probe correction and review script](results/2026-09-13-query-learning/review-learning-probes.py)
- [Main revalidation script](results/2026-09-13-query-learning/verify-comparison.py)

These are familiar short synthetic development questions and one run per condition. The six handoff probes were
authored for this change. Results do not establish production reliability, provider enforcement, natural skill
triggering, or improved retrieval after repeated curation. A future multi-query experiment would need an actually
approved curated route and held-out subsequent questions over the same original corpus.
