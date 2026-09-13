# Explore and Query

Both routes are read-only. Select one profile through [Registry](registry.md), then apply the pre-read gate in
[Publication](publication.md) before loading any wiki title, route, or content. If a legacy page's evidence safety
cannot be established without exposing its bytes, skip it and use the separately registered source-search scope.
Do not load a stale restricted alias and rely on a prompt to suppress it. Make one routing decision from
its compact context: Personal home as prior, named Company Index taxonomy home as router, and at most three declared
routing pages per scope. Resolve canonical concepts and aliases, choose the few relevant typed links, likely source
areas, and direct native searches together before evidence retrieval. Taxonomy and typed-link matches guide query
expansion and ranking; they never prove a fact, authorize access, or exclude evidence solely because the taxonomy is
incomplete. Never turn home → guide → detail into sequential routing hops or return to routing after the first
source read.

Retrieve inside registered accessible sources in bounded rounds. For cloud-drive sources, use the host's native
cloud-drive search as the evidence retrieval layer; for other sources, use the corresponding host-exposed native
search. Search remains available when taxonomy coverage is missing, stale, unrelated, unavailable, or low
confidence. Bypass both wikis for exact identifiers, recent/unrepresented documents, a more efficient direct search,
an unavailable wiki, or an explicit request.

Use the available source list/search rounds deliberately; a second search is not required when the evidence is
already sufficient:

1. Start with exact identifiers, distinctive phrases, canonical terms, and known aliases appropriate to the
   question. Use the provider's supported query syntax; do not assume literal or Boolean search support.
2. If evidence is missing and a round remains, target the specific gap. Broaden an unsuccessful phrase to its
   key terms, use synonyms or terms in the source language, or seek the missing authority or conflicting version.
   Refine native source queries within the registered scope and the initial routing decision; do not revisit
   wiki routing. Keep broader search available for evidence the taxonomy does not represent.

Listings consume the same discovery allowance as searches. Deduplicate repeated hits before opening sources,
but retain distinct versions or authority types needed to assess a conflict. Rank by relevance, applicable scope,
and authority; repeated matches do not establish correctness.

When a question plausibly spans policies, contracts, systems, decisions, or other distinct authority types, select a
small diverse evidence set rather than exhausting the bound on near-duplicate results. Compare each source's scope,
status, effective date, version, and supersession before synthesis; report a finite-bound limitation when the
available reads cannot establish a complete answer.

Check metadata/size before reads. For long documents, prefer native section or range reads around relevant hits
when the host supports them. Merge overlapping requested ranges where supported, and expand context enough to
include governing definitions, exceptions, table headers and units, effective dates, and supersession notices
needed for the claim. Use search snippets to locate evidence; verify their context in the original before citing
them. A short document may be cheaper and clearer to read in full. If bounded passage reads are unavailable,
read the full document only when it fits the remaining budget; otherwise report the limitation.

Account for every source read and all returned original-source characters, including repeated reads and
overlapping passages, against the existing operation bounds. Passage expansion grants no extra read allowance;
search refinement does not reset any bound. Count a full-document response in full even when only a passage is
used. Ask before expanding an exhausted bound.

After reading evidence, check which requested claims are supported, which material authority, exception, or
conflict remains unresolved, and what a further search or read could establish. Spend remaining retrieval on
those gaps. Stop as sufficiently supported when the evidence covers the requested answer and its material
qualifications. Otherwise return a partial or inconclusive answer when the bound is exhausted or accessible
retrieval cannot resolve the gap. State the unresolved point and the stopping reason; do not present budget
exhaustion or diminishing returns as proof of completeness. An unsuccessful search does not prove absence, and
an LLM relevance score does not establish factual confidence. Keep this assessment transient within the operation.

**Explore** reports transient routes and evidence and may offer Curate. **Query** retrieves the smallest useful
original evidence, cites every factual claim from evidence read in the same operation, labels interpretation and
conflicts, and writes nothing. A wiki statement without same-operation evidence is unverified navigation, not fact.

When supplying an exact evidence quote, copy a contiguous passage from the original text already read. Preserve
its line breaks, whitespace, punctuation, and wording; keep paraphrases in the answer, not in an exact-quote field.
Prefer a short passage that retains the claim's conditions and negation. If it crosses a source line break,
preserve that break rather than joining the lines. In structured output, escape characters as required so decoding
recovers the original passage. Before returning, check each quote against the source text in the current operation
and confirm that it supports the associated claim. Shorten a quote only if the remaining passage still supports
the claim; never rewrite the source or remove qualifications to make a quote match.

Recheck current source access/audience before exposing a derived route; fail closed on unavailable access.
Source search metadata, unavailable-route diagnostics, and response links obey the same disclosure boundary.
