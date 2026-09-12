# REQ: taxonomy wiki + scoped cloud-drive search

**Date:** 2026-09-11
**Updated:** 2026-09-12
**Deliverable:** a provider-neutral product contract and eventual implementation for taxonomy-assisted,
scoped cloud-drive retrieval using a lightweight, standards-informed taxonomy model.

## Problem

The current product can create a small Company Library Index and ask an agent to use it for navigation,
but that is not a credible retrieval mechanism for thousands of cloud-drive documents. A link tree cannot
reliably surface every relevant policy, contract, decision, report, or current revision required by a
multi-document question.

Raw cloud-drive search solves corpus coverage but does not reliably resolve company aliases, ambiguous
terms, source authority, supersession, or the relevant mix of source types. Treating either the wiki or
drive-search result rank as the answer would create a brittle, unauditable system.

## Outcome

Make the Company Library Index a small, human-governed **taxonomy and source-map layer** over an
authoritative cloud-drive evidence library. At question time, the taxonomy resolves language and produces
a bounded, permission-safe search plan; cloud-drive search retrieves accessible original documents; the
agent reads and compares the resulting evidence before answering.

```text
Taxonomy = the governed backbone
Typed links = the small useful graph on top
Cloud-drive search = evidence retrieval

User question → taxonomy and typed-link routing → scoped cloud-drive search
              → authority-aware, diverse source evidence → cited answer
```

The taxonomy is canonical for preferred terminology, aliases, durable relationships, source routes, and
authority guidance. It is not canonical for factual evidence and is never a copy of the drive corpus.

Typed links are a deliberately bounded discovery overlay: they express only high-value, reviewable
relationships that hierarchy cannot carry, such as ownership, governance, dependency, and supersession.
They do not turn the wiki into a generic graph database or make multi-hop graph inference the default
retrieval behavior.

Use SKOS-like semantics for the internal taxonomy—preferred and alternative labels, broader/narrower and
related concepts, scope notes, and mappings—without requiring RDF, a triple store, or a formal enterprise
ontology. External controlled vocabularies are optional reference inputs, never a replacement for the
company's terminology or source authority.

## Acceptance Criteria

### Taxonomy wiki

- [x] The shared Company Library Index can represent a small, human-readable taxonomy of durable concepts,
      systems, products, processes, policies, decisions, metrics, datasets, and source areas without
      requiring a node for every document.
- [x] A taxonomy node can record a canonical name, aliases/acronyms/legacy terms, a scoped definition,
      concise typed relationships, relevant knowledge type, authoritative source routes, and supported
      freshness or authority cues. Every substantive source-derived statement remains traceable to a
      native source target.
- [x] Domains are navigation aids rather than exclusive silos: a concept may participate in multiple
      domains, and relationships such as `related_to`, `governed_by`, and `supersedes` are distinct from
      tree placement.
- [x] The relationship vocabulary remains small and intelligible. The system does not present taxonomy
      placement as a logical fact or infer unrecorded relationships from it.
- [x] Taxonomy artifacts remain ordinary readable wiki documents and native links. The taxonomy does not
      require YAML records, a graph database, a document-side metadata store, or a new source copy.
- [x] Taxonomy changes follow the existing governance lifecycle: the agent may propose a new concept,
      alias, relationship, authority cue, or source route from explicitly selected evidence, but writes
      require the applicable destination authority and explicit approved change proposal.
- [x] Product and skill documentation state the three-layer model consistently: taxonomy is the governed
      backbone, typed links are the small useful graph on top, and cloud-drive search retrieves original
      evidence. Neither the taxonomy nor typed links are presented as a replacement for source search.
- [x] Typed links are limited to reviewable relationships that cannot be expressed by taxonomy placement
      alone. They support discovery and query expansion, but do not authorize source access, imply a
      formal fact, or trigger unconstrained graph traversal.

### Standards and vocabulary reuse

- [x] Internal taxonomy nodes use SKOS-like semantics: one preferred label per language, alternative and
      legacy labels for retrieval, concise scope notes, and distinct broader, narrower, and related
      relationships. These semantics are rendered as ordinary readable wiki content; RDF/SKOS serialization
      is not a V1 prerequisite.
- [x] A standard or domain controlled vocabulary may be mapped into the taxonomy only when an exact,
      authoritative version and terms are explicitly selected, its license and language are suitable, and
      it materially improves the supported company domain. Mappings retain the external stable identifier
      or URI when available and distinguish it from the internal canonical concept.
- [x] External vocabulary terms never silently replace company-preferred terminology, source authority,
      ownership, permissions, or relationship claims. A mapping is guidance for retrieval and navigation,
      not proof that the external taxonomy describes the company's internal meaning.
- [x] The system does not import a generic public subject-heading library merely to make the taxonomy look
      complete. External reuse is limited to targeted, evidenced mappings for demonstrated retrieval or
      governance needs.

### Query routing and scoped search

- [x] Every query selects one registered profile before taxonomy lookup or source search. The profile's
      exact original-material locations are the maximum source-search boundary; no query searches the
      whole drive, all connected drives, or an inferred collection.
- [x] The system resolves the question against visible taxonomy nodes and produces a readable search plan
      containing, when applicable: canonical concepts, aliases/query expansions, likely source scopes,
      source-type or authority preferences, time/status cues, and a fallback condition.
- [x] Taxonomy terms, source routes, and facets are soft retrieval signals by default: they expand and
      rank candidate searches but do not hide evidence merely because the taxonomy is incomplete or the
      match is uncertain. Provider permissions, the registered source boundary, and an explicit user-
      selected source are hard constraints.
- [x] When taxonomy coverage is absent, stale, unrelated, unavailable to the user, or low confidence, the
      system falls back to direct cloud-drive search within the registered permitted source locations and
      reports that it did so.
- [ ] Cloud-drive searches execute using the current authenticated principal and only provider-native,
      host-exposed search capabilities. Candidate results are rechecked for current access before content
      is read or a source link is exposed.
- [ ] The provider integration supports, or explicitly reports that it cannot support: bounded collection
      search, permission-trimmed discovery, stable native document identifiers/links, useful metadata
      such as title and modification time, and retrieval of the evidence required to answer. Unsupported
      capabilities are never simulated with guessed paths or an invented connector.
- [x] A question may retrieve multiple documents. The evidence-selection behavior avoids spending the
      entire bound on near-duplicates and considers distinct likely authority/source types when the query
      calls for them; it compares scope, status, effective date, version, and supersession before
      synthesizing an answer.
- [x] Factual answers are grounded in original source material read in the same operation, cite the
      sources used, distinguish established facts from interpretation, and preserve unresolved conflicts.
      A taxonomy page or search ranking alone is never evidence.
- [x] Search, reading, and evidence-context limits remain finite and visible. Exhausting a limit produces
      an explicit uncertainty/result limit and a proposed finite expansion; it never silently broadens
      the source boundary or search budget.

### Safety, freshness, and validation

- [ ] Source-system ACLs remain authoritative for search and reading. Taxonomy titles, aliases, source
      routes, summaries, search results, and relationships obey audience containment and must not reveal
      source-derived restricted metadata to a user who cannot access the underlying evidence.
- [ ] New or changed drive documents become searchable through the cloud drive without requiring wiki
      mirroring. Add Source updates the taxonomy only when selected evidence creates a material durable
      change such as a new reusable concept, alias, authority source, supersession, or source route.
- [x] Validate can report stale source routes, taxonomy aliases without usable routes, source access
      failures, broken links, stale authority/freshness claims, and high-value queries for which taxonomy
      routing did not improve retrieval. Validate remains read-only.

### Measurable value

- [ ] The product defines an evaluation set of real user questions with expected authoritative documents
      and, where feasible, supporting passages. It measures direct scoped cloud-drive search against
      taxonomy-assisted search for source recall, authority selection, multi-source completeness,
      citation faithfulness, latency, and permission safety.
- [ ] Taxonomy growth is justified by measured retrieval or navigation benefit. It is not justified by
      document count, a desire for complete classification, or an LLM-generated hierarchy alone.

## Verification Status

The documented skill contract, static coverage, and local permission-boundary adapter checks are complete as of
2026-09-12. The unchecked provider-execution and measurable-value criteria require an authorized cloud-drive
provider, exact source collections, a writable taxonomy destination, and a real-question evaluation set; none was
supplied for this story.

## Constraints

- Original cloud-drive documents remain the authority for content, ACLs, versions, retention, sharing,
  and auditability. The wiki and any answer do not replace them.
- Initial delivery reuses the selected cloud drive's native search and document-reading capabilities. Any
  derived lexical, semantic, or hybrid index is a separate later decision justified by failed evaluation;
  it must remain rebuildable, ACL-aware, and freshness-aware.
- The taxonomy wiki destination is separately specified and verified writable. Access to source documents
  does not grant permission to write taxonomy pages.
- Personal and shared taxonomy scopes follow the existing registry, audience, authority, and durable-change
  rules. A Personal Wiki may use the shared taxonomy as a retrieval prior but does not widen source access.
- The system remains provider-neutral and uses only already exposed provider/search/document capabilities.
- External controlled-vocabulary content is read or imported only from an exact user-selected authoritative
  source/version inside the approved work scope. It is not discovered through unbounded web or drive search.

## Non-goals

- Using the wiki as the sole retrieval corpus, an exhaustive document catalog, or a manually maintained
  duplicate of source content.
- A generic knowledge graph, graph database, automatic relationship extraction, or graph-first retrieval
  as the default architecture.
- Global or tenant-wide cloud-drive searches outside the selected profile's source boundary.
- Automatically classifying every document, creating one taxonomy node per file, or making every discovery
  durable.
- Treating taxonomy matches, graph links, or drive-search rank as proof of a factual answer.
- Requiring RDF, OWL, a triple store, or a complete public taxonomy library before the first taxonomy wiki
  can be useful.
- Importing generic subject headings or external vocabulary content as an unreviewed substitute for
  company-specific concepts, aliases, or source authority.
- A new vector database, GraphRAG system, custom ACL store, background crawler, mandatory indexing pipeline,
  or custom cloud-drive connector in the initial delivery.

## Blocking Questions

1. Which cloud-drive provider and exact source collections are in scope for the first implementation?
   The choice determines whether scoped, permission-trimmed full-text search and the required evidence
   reads can be verified.
2. Which authenticated principal and destination audience govern the first shared taxonomy wiki? Without
   those facts, a real taxonomy destination cannot be created or populated.
