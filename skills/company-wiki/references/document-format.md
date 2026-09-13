# Human-readable document format

Wiki artifacts are ordinary human-readable documents with native links. In a cloud-drive destination, use the
provider's native document format and existing document tools. Preserve headings, lists, tables, and links as
readable document structure; Markdown syntax and `.md` files are not required. Markdown is the representation for
repository examples and explicitly selected local wiki storage. This contract defines content and relationships,
not a Git workflow, filename convention, or storage-folder layout.

No front matter, YAML, `.wiki/` state, sidecar, or hidden database is required. Each scope has a readable home/map
whose taxonomy is the governed backbone: canonical node title, aliases, one-line scope, source entry point, and
primary parent. At most three pages per scope may be marked
`Routing page`. Tree position is navigation only; it never implies a relationship. Aliases resolve to canonical
nodes. A small set of labeled, reviewable typed links—such as `related_to`, `governed_by`, `supersedes`, or
`depends_on`—forms a discovery overlay when taxonomy placement is insufficient; it is not a generic graph or a
replacement for native source search.

Near a substantive generated/curated claim retain, when available: original source URI/ID, section, source version,
checked date, relationship, verification/freshness state, and origin (`source text`, `agent-generated`,
`human-authored`, or `verified company definition`). Cite conflicts separately with authority, dates, supersession,
and an explicit unresolved state. Mark inference as `Proposed:`.

## Page timestamps

Every generated wiki page, including homes/maps, routing pages, and retained stubs, must display a compact
metadata line near its title with `Updated` and `Evidence checked` (labels may follow the page's language).
Use ISO 8601 timestamps with an explicit timezone, preferably UTC `Z`, in the page itself; no sidecar is needed.
For example: `Updated: 2026-09-13T14:30:00Z · Evidence checked: Not fully checked`.

- **Updated:** the actual time of page creation or the latest substantive content change, including changes to
  claims, source routes, relationships, or retirement/merge status. Preserve it for formatting-only edits,
  verification-only metadata changes, and reads. Do not substitute a source's modification time or the provider's
  generic page-modified time.
- **Evidence checked:** the time when all supporting original evidence for the page's current substantive claims
  was last checked for claim support and version changes. Set a timestamp only when that full check occurred;
  otherwise show `Not fully checked`, including for a reference-only Bootstrap home. Partial checks retain their
  timestamps beside the relevant claims and never advance the page-wide timestamp. Preserve a prior full-check
  timestamp only while it still describes the same claims and evidence; changed content without a full check
  must show `Not fully checked`. An unchanged synthesis may receive a new check timestamp through approved Maintain
  without changing `Updated`.

These fields record provenance, not a freshness verdict: a recent timestamp never makes a page `current` or resolves
a conflict. Full-page checking stays within the selected source scope and read bounds; do not expand retrieval just
to fill a timestamp. Query, Explore, Validate, and a no-op Add Source never persist timestamp updates.

For legacy pages, add missing metadata during the next approved edit, without inventing historical times. Use
`Updated: Unknown` when neither reliable history nor a substantive edit establishes it. Validate reports missing
or unsupported timestamps without backfilling them.

## Personal controls and graph health

Personal homes include readable sections for pinned, temporary, personally canonical, and do-not-curate topics.
Use `Retired` and `Merged into` stubs rather than deleting nodes only when their metadata remains audience-safe;
apply [Publication](publication.md) for legacy disclosure cleanup. Validate checks primary routes, outline/tree
consistency, provenance, links, aliases, freshness, conflicts, and audience-safe disclosure.
