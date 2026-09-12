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

Personal homes include readable sections for pinned, temporary, personally canonical, and do-not-curate topics.
Use `Retired` and `Merged into` stubs rather than deleting nodes only when their metadata remains audience-safe;
apply [Publication](publication.md) for legacy disclosure cleanup. Validate checks primary routes, outline/tree
consistency, provenance, links, aliases, freshness, conflicts, and audience-safe disclosure.
