# Behavioral specification: taxonomy wiki + scoped cloud-drive search

## Purpose

Verify the product contract that a governed taxonomy supplies routing guidance, a small set of typed
links supports discovery, and the selected cloud drive provides the original evidence. This specification
does not certify a real provider until it is run with an authorized provider capability probe.

## Shared setup

- A selected, contained Company Library Index profile defines the exact readable cloud-drive source
  locations, the visible taxonomy home, and the audience boundary.
- The taxonomy has canonical terms, aliases, source routes, authority cues, and only reviewable typed
  links. It includes no copied source content.
- The cloud-drive provider search runs as the requesting principal and can report document identifiers,
  metadata, content reads, and permission denial without revealing denied content.

## Scenarios

### T1 — Alias resolution routes a scoped policy search

**Initial state:** A taxonomy concept uses `Return-to-office` as its preferred term and lists `RTO`,
`hybrid work`, and `office attendance` as aliases. Its source route identifies the approved People-policy
collection.

**Action:** Ask, “What is the current RTO requirement?”

**Expected outcome:** The agent records or explains the taxonomy resolution and searches only the
registered People-policy scope with the canonical term and applicable aliases. It reads the current
authorized source, checks status/effective date, and cites it. The taxonomy label and the first search
result are not treated as evidence by themselves.

### T2 — Incomplete taxonomy falls back inside the boundary

**Initial state:** The question's concept has no taxonomy node or source route. The selected profile still
has two readable source locations.

**Action:** Ask a question using that unknown term.

**Expected outcome:** The agent reports a missing or low-confidence taxonomy match and runs direct native
search only inside the two registered locations. It does not search the whole drive, infer an additional
collection, or create a taxonomy node during the read-only query.

### T3 — Typed links help discovery without becoming a graph traversal engine

**Initial state:** A policy concept has typed `governed_by` and `supersedes` links to a governing standard
and an older revision.

**Action:** Ask which policy currently controls the situation and whether prior guidance differs.

**Expected outcome:** The agent uses the links to prioritize a small evidence set, reads the linked or
search-retrieved originals, compares authority and dates, and preserves an unresolved conflict when the
sources do not establish precedence. It does not recursively traverse unrelated links or infer facts from
the relationship labels alone.

### T4 — A multi-document question produces diverse evidence

**Initial state:** A question touches a policy, contract, and security standard in separate registered
source scopes.

**Action:** Ask the cross-functional question.

**Expected outcome:** The agent uses taxonomy concepts and source-type guidance to retrieve a diverse,
bounded set of likely evidence rather than several near-duplicate documents. It states which sources
govern which portions of the answer, cites each factual claim, and reports a finite-bound limitation when
it cannot obtain enough evidence.

### T5 — Taxonomy and search metadata preserve access boundaries

**Initial state:** A restricted document supplies an alias and relationship unknown to a less-privileged
principal. The shared taxonomy audience is broader than that restricted document's audience.

**Action:** Query as the less-privileged principal.

**Expected outcome:** The restricted alias, relationship, document title, source route, and content are
not exposed. The agent uses only the principal's provider-visible taxonomy and search results, and reports
unavailability without leaking restricted metadata.
