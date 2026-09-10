# company-wiki / 企业文库

`company-wiki` is a portable Agent Skill for building a small, curated knowledge schema over an
organization's existing documents, repositories, and systems. It helps an agent resolve company
terminology, choose authoritative evidence, navigate relationships, investigate recurring question
types, and answer with explicit uncertainty. The original sources remain the system of record.

## Package layout

- `SKILL.md` — short routing and safety instructions loaded first.
- `references/` — progressive workflow and format instructions.
- `../../examples/` — an illustrative schema for learning the file format (kept outside the installed skill).

On initialization, the agent creates `<skill-dir>/schema/` and `<skill-dir>/competency-questions.md`.
The
schema contains the organization's identity, domains, concepts, vocabulary, relationships, sources,
authority rules, definitions, and problem patterns. The catalog contains the questions that define
what the schema must help answer.

`schema/` and `competency-questions.md` are organization data. Keep them when updating or replacing
the skill; do not treat them as disposable package files. The root example is format guidance only and
must never be copied as organizational content.

## Use it

1. Install or copy the complete skill into a writable skill directory.
2. Ask the agent to set up company-wiki, naming the sources and schema language. It will ask for
   whichever of those two answers is missing, inspect reachable sources, and create a minimal schema.
3. Ask company questions normally. The agent loads the schema progressively, queries original
   sources through tools already available on the host, and cites the evidence it actually read.
4. Ask it to suggest or apply a schema change, or to check the schema for problems. Changes require
   approval; validation is read-only by default.

The skill does not include connectors, databases, embeddings, indexes, caches, source copies,
per-document sidecars, workflow automation, or executable code. It reuses the host's access
capabilities and reports when a source or capability is unavailable. Derived retrieval infrastructure
is considered only after a demonstrated retrieval failure.
