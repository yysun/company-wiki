# company-wiki-skill

## Summary

Reworked the `company-wiki` skill from a local schema/YAML model into a document-native cloud-drive wiki.
Ordinary drive documents are nodes, native links/bookmarks/heading links are edges, and progressive
disclosure runs from a small home/map through guides and focused detail to original evidence. Cloud-drive
access is limited to capabilities the host already exposes through cloud-drive skills, MCP tools, or agent
plugins; no connector was invented.

The shipped examples are a flat seven-document graph. Tests use a flat logical drive adapter, ordinary
read-only git access, source-integrity checks, permission-safe fixtures, and maintenance/validation cases.

## Verification

- Static package, frontmatter, line-budget, link-resolution, token-leak, fixture, and `git diff --check`
  checks passed.
- Host capability probe found Google Drive discovery/read/create/update tools; no external destination was
  selected, so provider-level write, permission-denied, heading/bookmark, and native-link round-trip
  behavior remain explicitly unverified.
- Isolated local-adapter smoke evidence passed S0–S7, including init gates, English/Chinese graph creation,
  direct-source fallback, categories A–O, permissions, approved maintenance, validation defects, existing
  home handoff, and unreachable-source handling.
- Independent CR passed after the final fixes: `CR passed: no major findings`.
- `VR passed: all acceptance criteria complete`

## Notes

- No unit or integration suite applies to the Markdown-only deliverable.
- No source documents, repositories, or embedded source instructions were modified or followed as actions.
- The story base is `98f7ffe`; the user baseline documents under `docs/` remain outside the story delta.
- Delivery commits: `eb30a72`, `46b1c9a`, `14ff808`, `6ee5437`, and `909e1b1`.
- Read-order evidence is weaker than a standalone headless transcript because no transcript-export runner
  was available; reports were checked for repository-path leaks.
