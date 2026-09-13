# Citation line-break regression — September 13, 2026

The three questions with observed citation-formatting failures passed three repetitions each after
the quote-preservation guidance was added: **29/29 exact citations**, including **20 multiline quotes**.
All nine executions passed the trace, retrieval-bound, navigation, and semantic checks.

## Cause and change

Five citations in the [Query comparison](query-comparison-2026-09-13.md) joined source lines with spaces.
Their claims were supported, but the decoded quote strings were not exact source substrings.

The Query reference now requires exact evidence quotes to retain source whitespace, line breaks,
punctuation, wording, conditions, and negation. It tells the agent to check the quote against text
already read and keep paraphrases in the answer. The benchmark prompt explains that JSON decoding
must recover the original passage, with source line breaks preserved through JSON newline escapes.

The citation scorer and trace checker are unchanged, verified by comparing their parsed function
bodies with the pre-fix runner snapshot. No whitespace normalization, automatic quote repair, source
editing, or historical-result replacement was introduced. This is an instruction-level fix, not a
new runtime enforcement mechanism.

## Targeted repeated verification

Cases EQ01, EQ04, and EQ05 cover all questions that had a whitespace citation failure in either
condition of the previous experiment. Each ran three times with `gpt-6-astra`, high reasoning, and
the existing bounded corpus tool. Three runs executed concurrently; cases within a run were sequential
and each question used a fresh ephemeral session. No timing comparison is claimed.

| Measurement | Run 1 | Run 2 | Run 3 | Total |
|---|---:|---:|---:|---:|
| Valid executions | 3/3 | 3/3 | 3/3 | 9/9 |
| Exact citation checks | 10/10 | 9/9 | 10/10 | 29/29 |
| Semantic answer passes | 3/3 | 3/3 | 3/3 | 9/9 |
| Atomic answer criteria | 9/9 | 9/9 | 9/9 | 27/27 |

The formerly failing cancellation passage retained its embedded line breaks in all three EQ04
responses. The successful checks therefore exercise multiline preservation rather than relying
only on quotations that avoid line breaks.

All 12 benchmark unit tests passed. The new regression test checks exact multiline text after JSON
serialization and decoding, and rejects both space substitution and a literal backslash sequence.
Skill validation and whitespace checks passed. All nine raw traces were revalidated against their
recorded checks, execution snapshots matched their manifests, and original-source hashes were unchanged.

The same agent authored the fix and graded answers against the original sources; this was not blind
or independent human review. These targeted repetitions address the observed failure, not universal
citation reliability. The full 20-question benchmark was not rerun for this narrow correction.

## Local evidence

Raw traces, prompts, exact answers, hash-bound semantic reviews, and execution snapshots are retained
under the Git-ignored `results/` directory. Previous benchmark outputs remain unchanged.

- [Run 1 scorecard](results/2026-09-13-citation-fix/run-1/report.md)
- [Run 2 scorecard](results/2026-09-13-citation-fix/run-2/report.md)
- [Run 3 scorecard](results/2026-09-13-citation-fix/run-3/report.md)
- [Aggregate verification](results/2026-09-13-citation-fix/verification.json)
- [Test design](results/2026-09-13-citation-fix/design.json)
