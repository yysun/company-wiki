# Changelog

## Unreleased

## 1.2.0 — 2026-09-14

### Fixed

- Separate distinct-source and evidence-read budgets from a finite update-verification allowance; preserve all
  returned-content and explicit legacy/total-read caps across rechecks and recovery. Existing aggregate allowances
  replace unspecified component defaults, and every discovery result page consumes its own request.
- Resolve specific unambiguous source descriptions and explicitly requested finite batches to exact targets
  without redundant selection; keep ambiguity, completeness, access, and scope checks.
- Allow one bounded wiki routing follow-up for a concrete evidence gap while preserving compact initial routing,
  traversal/source limits, and read-only Query/Explore behavior.
- Let explicit Add Source/Ingest, Curate, and Maintain requests authorize bounded updates to an existing wiki,
  including after candidate selection. Preserve review-first approval, publication checks, protected writes,
  and setup/registration approval; replan within task scope without redundant confirmation.
- Separate read-and-answer, transient-draft, and publication capabilities for existing plugins, MCP tools,
  CLIs, and APIs. Source connectivity no longer implies support for publishing wiki changes.
- Keep ordinary authorized answers independent of destination write tools, ACL enumeration, and optional source
  revisions. Preserve requester access checks, including for broader service accounts.
- Route missing publication capabilities to an authorized transient result without wiki or registry writes;
  distinguish source freshness from destination concurrency protection and preserve disclosure boundaries.
- Run bounded benchmark commands synchronously and record execution overrides; retain invalid-output evidence
  and distinguish execution reliability from answer quality in comparison reports.

### Validation and known limitations

- All 42 adapter/contract and benchmark/report unit tests passed; skill, Markdown-link, and whitespace checks passed.
- All 18 independent retrieval decision scenarios and variants passed, covering budget accounting, legacy limits,
  source selection, and routing boundaries. See the [verification record](.docs/tests/test-bounded-wiki-retrieval.md).
- These checks validate the instruction package and its interpretation. Live-provider execution/enforcement and
  retrieval-quality improvements under the new defaults remain untested. Historical benchmark results and their
  stricter read/routing limits remain unchanged.

## 1.1.0 — 2026-09-13

### Added

- Query can use approved investigation patterns during initial routing and offer one useful lesson for
  optional Curate after answering. Curation preserves evidence, applicability, and uncertainty; the skill
  stays stable during use and Query remains read-only.
- Bounded Add Source discovery by title, keywords, or filename pattern, followed by exact user selection
  before reconciliation reads.
- Visible `Updated` and `Evidence checked` timestamps on generated wiki pages, with explicit handling of
  partial checks, unknown history, and unchanged content.
- Six synthetic learning-handoff scenarios and a fresh before/after Query benchmark.

### Changed

- Publication guidance distinguishes provider-managed wiki permissions and current audience checks from
  explicitly required continuing source-permission inheritance. Source and destination boundaries remain separate.

### Validation and known limitations

- All 41 existing benchmark, adapter, and lifecycle tests passed.
- The [Query learning comparison](tests/rag-quality/query-learning-2026-09-13.md) passed all 20 answers in
  both conditions, with exact citations at 55/55 before and 56/56 after. Learning scenarios improved from
  5/6 to 6/6; the difference was a useful optional Curate suggestion, not factual answer accuracy.
- In that single run, source reads fell 8.2% and source characters fell 6.0%, while input tokens rose 4.6%.
  Elapsed time was essentially unchanged. These synthetic, agent-reviewed results do not establish
  production reliability or accumulated cross-query learning gains.

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
