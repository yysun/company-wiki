# Requirements: wiki publication and recovery

The skill currently checks access before publication but permits static derived pages to outlive source access,
and its recovery instructions do not distinguish a rejected write from a committed write with a lost response.
The package must make supported publication guarantees explicit and guide safe, bounded recovery.

## Acceptance criteria

- [x] Governed source-derived durable content, including Personal copies and metadata, requires current audience
      containment and provider-enforced continuing containment on every native exposure surface. Unavailable proof
      blocks publication; private local originals/test fixtures remain supported without enterprise guarantees.
- [x] Identity, exact-scope write/govern capability, audience, and continuing protection are separate checks with
      verified, denied, or unavailable outcomes. Synced files and registry roles cannot authorize shared writes.
- [x] All contributing evidence is authorized before shared generation. Restricted prior context cannot be
      sanitized by deleting tokens or citations. Query/Explore refuse unsafe legacy routing bytes before model
      ingestion and retain bounded direct-source fallback. Diagnostics and retirement stubs obey the same boundary.
- [x] Setup preflights registration, uses supported idempotent/conditional creates, verifies dependencies before
      links, and registers completed pages with the profile before an atomic, concurrency-protected index update.
      Failures preserve pre-existing registry bytes and successful pages; retry reconciles exact approved targets.
      Changed registrations use a fresh profile; exact existing profiles are reused without rewrite. Approval binds
      the selected entry delta, allowing guarded merges of unrelated entries while rejecting selected-entry drift.
- [x] Writes use provider-enforced version conditions or an equivalent exclusive-write mechanism. Unknown outcomes
      are reconciled before retry. Partial failure stops later writes without automatic rollback; changed bindings
      invalidate approval, and recovery proposes only remaining work without overwriting concurrent edits.
- [x] Repository AGENTS boundaries, the PRD, personal requirements, skill workflows, public guides, and affected behavioral specifications agree
      on these contracts, including unsupported-provider behavior and the limits of static exports and local tests.
- [x] Existing package/adapter unit tests and skill validation pass. Independent scenario-based evaluation covers
      authorization, metadata, revocation, setup failure, unknown outcomes, concurrency, and local compatibility.
      Provider acceptance scenarios are specified separately and never reported as production runtime proof.

## Constraints and non-goals

Keep registry-first selection, exact source/destination bounds, immutable originals, one routing phase, and existing
approval scope. No live wiki or registry is selected for this repository change. Do not add a connector, background
sync, ACL database, transaction coordinator, recovery ledger, or source cache. The product here is a portable skill
and its documentation: enforcement must come from exposed provider/tool capabilities, never fabricated responses.
Already disclosed/downloaded bytes cannot be recalled. Native searches, versions, previews, and exports must be
included in a provider's declared protection coverage before accepting its continuing-containment guarantee.
