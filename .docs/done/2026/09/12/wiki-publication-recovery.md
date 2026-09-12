# Wiki publication and recovery

## Summary

Snapshot-only ACL checks previously permitted derived static pages whose native exposure could outlive source
access. The skill now requires provider-enforced continuing protection for governed publication, gates unsafe
legacy bytes before model ingestion, and isolates shared generation from excluded evidence. Private user-owned
local originals/tests retain their bounded path; synced/exported governed evidence never inherits that exception.

Setup and retries now distinguish failed from unknown outcomes, require conditional/exclusive writes and native
idempotent/conditional creates, and preserve successful and concurrent edits. Changed registrations create a fresh
profile and switch the index link last. Unrelated index edits can be merged under exact-entry approval with a fresh
version guard, while selected-registration drift requires revised approval. No automatic destructive rollback occurs.

PRD, personal requirements, repository boundaries, skill workflows, EN/CN/package guides, and acceptance scenarios
were reconciled. Independent review found and resolved profile overwrite and local-demo defects; independent
decision evaluation found and resolved registration approval ambiguity.

## Verification

- 23 existing Python adapter/contract tests passed on the corrected tree.
- Skill-creator validation passed; all 22 added Markdown links resolved; diff whitespace validation passed.
- Independent synthetic D1–D11 decision evaluation completed, including a rerun of corrected D5.
- AR passed; CR passed after corrections (round 3); final VR passed with all seven criteria complete.
- Implementation commits: `9652f51`, `549c7bc`; story base: `0ad9a9e`.

## Limits

This delivers the portable skill/requirements contract, not a production connector or ACL synchronization service.
Provider acceptance cases 1–6 are specified but unexecuted. The shipped local adapter does not implement enterprise
identity, continuing ACL protection, conditional writes, or crash-safe idempotency. No live provider, user registry,
or original source was accessed or changed. Existing disclosed/downloaded bytes cannot be recalled by these changes.

## Final VR result

VR risk: non-low — publication authorization, confidentiality, concurrency, and recovery contracts.

VR review round: 1; reviewer: reused

1. **Complete — Publication protection.** [publication.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/publication.md:13) requires current and continuing containment across native surfaces, including Personal copies and metadata. It blocks unsupported publication and preserves the narrow private-local exception. D1, D2, D8, and D10 cover these decisions.

2. **Complete — Separate authorization checks.** [publication.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/publication.md:8) distinguishes identity, exact-scope authority, audiences, and continuing protection, with verified/denied/unavailable outcomes. D3 confirms local access and registry roles cannot authorize shared publication.

3. **Complete — Generation and disclosure safety.** [publication.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/publication.md:40) and [query.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/query.md:3) require authorized generation context, pre-read protection, bounded fallback, and safe diagnostics/cleanup. D4, D8, and D9 cover these decisions.

4. **Complete — Setup and registration recovery.** [registry.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/registry.md:24) specifies preflight, exact-match profile reuse, fresh profiles for changed registrations, guarded index updates, and preservation on failure. [change-protocol.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/change-protocol.md:6) requires protected creates and dependency verification. Corrected D5 and added D11 passed.

5. **Complete — Conditional writes and partial outcomes.** [change-protocol.md](/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/references/change-protocol.md:17) requires conditional/exclusive updates, exact outcome reconciliation, drift invalidation, and remaining-work recovery without automatic rollback. D6 and D7 cover unknown outcomes and concurrent edits.

6. **Complete — Consistent documentation.** AGENTS.md, PRD, personal requirements, skill references, English/Chinese/package guides, and affected specifications agree on the final contracts. CR round 3 passed; original-source and registry boundaries remain intact.

7. **Complete — Scoped verification.** The [execution record](/Users/esun/Documents/Projects/company-wiki/.docs/tests/test-wiki-publication-recovery.md:62) records independent D1–D11 interpretation coverage. Final evidence records 23 passing Python tests, successful skill validation, 22 resolved added links, and a clean diff whitespace check. Provider acceptance cases 1–6 are explicitly unexecuted and are not claimed as production proof.

All plan tasks are complete. Reviewed commits `9652f51` and `549c7bc` against base `0ad9a9e`; reused existing verification without editing files or executing tests.

VR passed: all acceptance criteria complete
