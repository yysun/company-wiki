# Bounded wiki retrieval

Routine updates and investigations stop because required verification consumes a five-call retrieval budget,
resolved source names require another selection turn, and an initial routing mistake cannot be corrected after
reading evidence. Remove these three restrictions while keeping bounded, requester-authorized work.

## Acceptance criteria

- [ ] Distinct sources, evidence read calls, retrieved characters, and update verification have explicit finite
  limits. Three selected short documents can be reconciled and rechecked without expanding default read-call
  limits. Several sections of one source do not count as several distinct sources.
- [ ] Explicit existing hard limits keep their meaning. Rechecks, overlapping passages, failed/retried reads,
  selection, replanning, and recovery cannot reset or bypass the applicable counters; reserve required verification
  before consuming its capacity. Character limits cover all returned source content.
- [ ] A specific unambiguous source description can resolve to an exact target without a second selection turn.
  An explicit finite batch can select a complete enumerated snapshot. Ambiguity, incomplete membership, truncation,
  out-of-scope matches, or exhausted bounds cannot silently expand selection or start an unauthorized batch.
- [ ] Query/Explore may perform one targeted wiki follow-up when original evidence reveals a concrete missing
  authority, alias, or exception. Keep compact initial routing, bounded traversal, the selected profile and named
  index edge, source access checks, and all retrieval limits; no unrestricted rerouting loop is permitted.
- [ ] Setup/registration approval, review-first behavior, source immutability, publication/governance checks,
  protected writes, unknown-outcome stops, and read-only Query/Explore/Validate behavior remain unchanged.
- [ ] Live skill instructions, guides, current product descriptions, examples, and affected scenarios agree.
  Package checks and independent synthetic decision evaluation pass. Historical benchmark results and explicit
  benchmark limits remain identifiable and unchanged; no live-provider execution is claimed.

## Scope

Only the first three findings from the user's restriction review are authorized. No setup/registration approval
relaxation, standalone Personal Wiki feature, real registry/wiki changes, connector implementation, release, or push.
