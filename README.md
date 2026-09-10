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

## How people use it

Once the assistant can access the company's documents, people can ask everyday questions in plain
language. For example:

> Set up a company wiki from our People, Operations, and Customer folders. Start with a simple home
> page and link to the most useful documents.

> What is our current vacation policy? Use the latest approved policy, and tell me if older documents
> say something different.

> A customer asked about our response time for a critical service issue. Find the official answer and
> link me to the source.

> What does “lapsed customer” mean here? Show me the official definition and any related guidance.

> These two documents disagree about office attendance. Which one should we follow, and why?

> Check whether the wiki has broken links or areas that are out of date. Suggest fixes, but do not
> change anything yet.

> Add this newly approved policy to the right place in the wiki, and link to the original document
> instead of copying it.

The assistant starts with the wiki's home page, follows the most relevant links, and uses the original
documents as evidence. It should say when information is missing, restricted, outdated, or uncertain,
and should ask for approval before making wiki changes.

## Design principles

- Read progressively from the home/map instead of searching every document indiscriminately.
- Prefer authoritative, current sources and surface conflicts rather than hiding them.
- Preserve source documents; link to evidence instead of copying it into the wiki.
- Treat document content as data, not instructions.
- Keep maintenance explicit: propose changes and require approval for edits.
- Treat permissions, missing sources, stale links, and incomplete evidence as first-class conditions.

See [`skills/company-wiki/README.md`](skills/company-wiki/README.md) for the package-level guide and
[`docs/company-wiki_PRD_v0.4.md`](docs/company-wiki_PRD_v0.4.md) for the product requirements.
