# Wiki update authorization

An explicit request to add evidence or correct an existing wiki currently stops for a second approval even
when the selected scope, destination, and requested outcome are clear. Carry the user's update intent through
source selection and bounded implementation without weakening publication or concurrency checks.

## Acceptance criteria

- [ ] An explicit Add Source/Ingest, Curate, or Maintain request authorizes necessary bounded changes in the
  selected existing wiki; later selection of exact discovered candidates retains that intent.
- [ ] Reading, source selection without update intent, factual corrections without an edit request, Query,
  Explore, Validate, and suggestions do not authorize writes. Explicit review-first requests wait for approval.
- [ ] Every write has concrete reviewable targets and changes, verified provider authority and audience,
  apply-time evidence/target rereads, protected operations, and result verification. Missing capabilities
  cannot be supplied by user confirmation. Original sources remain unchanged.
- [ ] Replanning stays within the authorized task and preserves concurrent work. A materially changed
  explicitly approved proposal needs fresh approval; task-authorized routine reconciliation may continue after
  a fresh plan and checks. Unresolved decisions or additional authority stop the affected action.
- [ ] No automatic source expansion, scope/destination changes, promotion, or unrelated restructuring is
  authorized. Init, Bootstrap, registration changes, failure/unknown-outcome stops, and read bounds are preserved.
- [ ] Live skill instructions, repository boundaries, current guides, and affected scenarios agree. Local
  package checks and independent decision evaluation pass, with provider execution limits stated accurately.

## Non-goals

No provider adapter implementation, live wiki update, registry mutation, new approval storage, release, or push.
No changes to source discovery selection requirements or publication access models. No blocking questions remain.
