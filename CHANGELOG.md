# Changelog

## 1.0.0 — 2026-09-13

Initial versioned release of the portable Company Library Index and Personal Wiki skill.

### Added

- Version and repository metadata in `SKILL.md`.
- Cloud-native and explicitly selected local workflows for Init, Bootstrap, Explore, Query, Curate,
  Add Source, Maintain, and Validate, with separate source and destination boundaries.
- A 20-question synthetic retrieval benchmark, a retained historical baseline, and reviewed comparisons
  that freeze the Query reference, dataset, runner, and source versions used in each run.

### Changed

- Query guidance now targets evidence gaps with search refinement, deduplicates hits while preserving
  distinct authorities, and uses bounded passage reads when supported. It distinguishes sufficient
  evidence from exhausted retrieval and keeps the existing scope, routing, and read limits.
- English, Chinese, and package READMEs identify the release and explain the latest evaluation.

### Fixed

- Exact-quote guidance requires source line breaks, whitespace, wording, and qualifications to survive
  JSON serialization. Paraphrases remain in the answer rather than exact-quote fields.
- A short, corpus-bound benchmark launcher removes the need to reproduce temporary paths, addressing
  the command-copying failure observed in the Chinese case. Launcher and corpus hashes detect changes.
- Reports show pass percentages alongside case or quotation counts, distinguishing fewer quotations
  from lower citation integrity. Scoring and historical failed attempts remain unchanged.

### Validation and known limitations

- All 18 benchmark unit tests and 9 lifecycle contract checks passed; skill validation passed.
- The [latest controlled comparison](tests/rag-quality/query-comparison-fixed-2026-09-13.md) retained
  semantic answer quality and 100% exact citation integrity among valid executions. On 19 matched
  questions, strengthened retrieval used 19.0% fewer source reads and 17.0% fewer source characters.
- One updated execution recorded an empty listing response and remains invalid. Its cause is unresolved;
  separate diagnostic successes do not replace it. Original and updated execution rates are 100% and 95%.
- The evaluation uses short synthetic sources and agent grading. It does not establish production
  accuracy, native provider access enforcement, publication guarantees, or long-document performance.
