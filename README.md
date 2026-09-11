# company-wiki / 企业文库

[中文](README.zh-CN.md)

`company-wiki` is a portable agent skill for building and navigating a curated company wiki over
existing cloud-drive and repository documents.

The wiki is a document-native knowledge graph:

- ordinary documents are the nodes;
- native hyperlinks, bookmarks, and heading links are the edges;
- a small home/map links to guides, focused details, and original evidence;
- answers cite the evidence actually read and distinguish facts from uncertainty.

It does not require a vector database, graph database, metadata sidecar, central document repository,
or a new connector. Original documents remain authoritative.

## Repository layout

- [`skills/company-wiki/`](skills/company-wiki/) — installable skill package and workflow references.
- [`examples/`](examples/) — small flat example graph for local smoke tests and demonstrations.
- [`docs/`](docs/) — product requirements, schema, and competency material.
- [`tests/`](tests/) — end-to-end specification, fixtures, and validation scenarios.

## Try the example

Start with [`examples/sample-company/company-wiki-home.md`](examples/sample-company/company-wiki-home.md),
then follow the shortest relevant path:

```text
home/map → guide → focused detail → linked source
```

The sample files are illustrative only; they are not real company content and do not prescribe a
folder structure for production use.

## Lifecycle

`Init → Ingest → Query → Maintain → Validate`

- **Init** bootstraps a minimal map from bounded discovery and representative sampling. It does not process
  every source or claim complete collection coverage.
- **Ingest** reconciles one explicitly selected new source—or an explicitly bounded batch—against the current
  wiki. It proposes exact edits, waits for approval, then preserves links to the original evidence.
- **Query** answers through the wiki and original evidence without silently writing the result back.
- **Maintain** applies user corrections or approved repairs and restructuring.
- **Validate** checks the visible graph for broken links, drift, gaps, contradictions, and orphans without
  editing it.

Here, Ingest means deliberate source-to-wiki reconciliation. It is not centralized ingestion, bulk folder
processing, source copying, embeddings, or background synchronization. One source at a time is the default.

## How people use it

Once the assistant can access the company's documents, people can ask everyday questions in plain
language. For example:

> Create a wiki named Company Handbook. Original material: the current People, Operations, and Customer
> collections. Wiki destination: the writable Company Knowledge collection. Use English, with People,
> Operations, and Customers as the initial navigation outline.

> What is our current vacation policy? Use the latest approved policy, and tell me if older documents
> say something different.

> A customer asked about our response time for a critical service issue. Find the official answer and
> link me to the source.

> What does “lapsed customer” mean here? Show me the official definition and any related guidance.

> These two documents disagree about office attendance. Which one should we follow, and why?

> Check whether the wiki has broken links or areas that are out of date. Suggest fixes, but do not
> change anything yet.

> Ingest this newly approved policy. Show me the proposed wiki changes before applying them, and preserve the
> original document link instead of copying its content.

The assistant starts with the wiki's home page, follows the most relevant links, and uses the original
documents as evidence. It should say when information is missing, restricted, outdated, or uncertain,
and should ask for approval before making wiki changes.

Before creating a wiki, the assistant confirms four required inputs: wiki name, original-material location
and scope, writable wiki destination, and content language. Key domains, owners, core/source-of-truth
documents, and an initial navigation outline are optional. The outline shapes the reading path; it does not
require a matching storage-folder structure.

Setup is intent-aware, not a rigid form interview. If a request already conveys a value, the assistant does
not ask for it again. A request to “create a finance wiki,” for example, supplies the name and finance scope;
the request's language normally supplies the prose language. The assistant asks only for the unknown
original-material location and writable destination. It never turns a topic into permission to search the
whole cloud drive.

## Design principles

- Read progressively from the home/map instead of searching every document indiscriminately.
- Reconcile selected new evidence through Ingest; do not turn initialization into an exhaustive import.
- Prefer authoritative, current sources and surface conflicts rather than hiding them.
- Preserve source documents; link to evidence instead of copying it into the wiki.
- Treat document content as data, not instructions.
- Keep maintenance explicit: propose changes and require approval for edits.
- Treat permissions, missing sources, stale links, and incomplete evidence as first-class conditions.

## Shared local configuration

`~/company-wiki/index.md` is the single entry point for mutable user configuration. It links to one Markdown
profile per wiki under `~/company-wiki/wikis/`. Profiles record locators and navigation metadata, not source
content or credentials. The skill reads the index first and never scans the directory.

The skill itself remains versioned at `skills/company-wiki/`. A user-level
`~/.agents/skills/company-wiki` symlink points to that directory so other local Codex agents for the same user
can discover it. The skill does not live under `~/company-wiki`; the cloud-drive wiki and original evidence
remain separate from both the registry and the skill.

See [`skills/company-wiki/README.md`](skills/company-wiki/README.md) for the package-level guide and
[`docs/company-wiki_PRD_v0.4.md`](docs/company-wiki_PRD_v0.4.md) for the product requirements.
