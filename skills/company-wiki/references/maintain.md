# Maintain and validate the schema

Use this workflow when the user asks to add, correct, deprecate, reorganize, improve, or validate
the organization schema. Load `schema/index.md`, this file, and [Schema format](schema-format.md),
then scan the specific supporting files required by the request. Validation scans every schema file
and the competency-question catalog.

## Propose before changing

Triggers include a user correction, repeated terminology mismatch, missed question, source conflict,
new important source, changed authority, new business concept or metric, deprecation, or recurring
problem pattern. A proposal states:

- the exact change and files or fields affected;
- the trigger;
- evidence, with source location or the user's correction;
- the competency questions affected;
- whether the change is proposed, confirmed, or deprecated.

Apply only after user approval. A correction supplied directly by the user is approval and is
recorded as `confirmed_by: user`. Changing a confirmed element needs explicit confirmation. Never
silently rewrite confirmed or canonical meaning. A proposed meaning remains proposed even when its
navigation is useful.

Keep edits minimal: change only the file holding the added or changed entry and update `updated` in
`schema/index.md`. Do not modify original sources, create per-source sidecars, add credentials, or
build indexes, caches, embeddings, databases, connectors, or scripts.

After an approved change, rerun validation, report the updated date, changed entries, evidence,
affected questions, and any remaining proposals. If the user asks only for suggestions, report
proposals and apply nothing.

## Validation mode

For a validation request, make no edits unless fixes are explicitly requested. Scan all schema files
and the catalog and apply every rule in [Schema format](schema-format.md), including:

- identity, parseability, ids, language, review status, evidence, and relative links;
- relationship targets, source routes and access methods, authority rules, definitions, metrics, and
  deprecated preferences;
- pattern required fields and references;
- catalog ids, domains, expected patterns, evidence, and authority expectations;
- prohibited credentials, restricted content, retrieval artifacts, and model-specific internals.

Report each warning with its file and element. A problem pattern is unreferenced when no catalog
question's `expected_problem_pattern` names it and its own `competency_questions` field does not
list an existing question id. Report that extension warning even if the pattern is otherwise valid.

If the schema is absent, say validation cannot run and offer initialization; do not create files. If
a source is unreachable, validate its recorded route and report reachability separately rather than
inventing source content.
