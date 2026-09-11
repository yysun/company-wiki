# confirm-wiki-initialization-inputs

## Summary

Company-wiki initialization now has a strict four-input gate: wiki name, explicit original-material
location and scope, explicit writable wiki destination, and prose language. Natural-language analysis keeps
unambiguous values already supplied by the user and asks only for what remains unknown. A request such as
“创建一个财务文库” therefore supplies the name, finance subject, and Chinese language—but never a source
location or destination.

Mutable user configuration is separated from the installed skill and provider data. The versioned skill
remains in this repository and is discovered through `~/.agents/skills/company-wiki`. The single registry
entry is `~/company-wiki/index.md`; it links to contained Markdown profiles under `wikis/`. Agents read the
entry first, follow only the selected profile, and never scan the registry directory.

## Implementation

- Root `AGENTS.md` independently requires the original-material read boundary and wiki destination write
  boundary; neither may be inferred and read access never implies write authority.
- Init asks for all missing required inputs together and offers exactly four optional inputs: key domains,
  owners, core/source-of-truth documents, and an initial navigation outline.
- Registry routes reject URLs, absolute paths, traversal, missing targets, symlink escapes, duplicate names,
  collisions, and ambiguous matches.
- Registration is idempotent, preserves unrelated content, stores no source copies or credentials, and
  reports partial provider success without deleting created provider documents when final persistence fails.
- The user registry was created with only `index.md` and an empty `wikis/` directory. No real wiki profile
  was invented.

## Verification

- Corrected-scope AR passed in round 3 after tightening containment, rollback, partial-failure, and symlink
  behavior.
- Independent CR round 1 found premature registry creation, exclusion of C7 from the suite pass gate, and an
  unreproducible fixture-hash claim. All three were fixed; round 2 passed with no major findings.
- Final TT passed 29 scoped Markdown links, 29 contract assertions, formatting, clean-tree,
  protected-`docs/**`, skill-budget, registry-file-count, symlink-target, installed/fixture byte-identity,
  and credential-pattern checks.
- The installed entry and versioned fixture match at SHA-1
  `0709218281236c164371e72c389dd23d7f148f68`.
- ET was not executed because the repository has no standalone headless agent/provider runner or transcript
  exporter. Prose scenarios and static checks are not claimed as provider-runtime proof.

## Final VR result

`VR passed: all acceptance criteria complete`

### Initialization contract

1. Missing required inputs are requested together; no registry or provider write occurs first. Init performs
   only a read-only index lookup before the four-input gate, and I1 covers a missing registry.
2. The four required inputs are wiki name, explicit original-material location and scope, explicit writable
   destination, and prose language.
3. Natural-language analysis reuses unambiguous name, subject, and language values.
4. Fully supplied requests are not asked to reconfirm those values.
5. Source discovery and reads remain inside user-specified original-material locations; semantic topics never
   authorize whole-drive discovery.
6. Source location, destination, permissions, inaccessible sources, and broader scope are never inferred.
7. `AGENTS.md` independently defines the source-read and destination-write boundaries and states that read
   access does not imply write authority.
8. Exactly four optional inputs are offered: key domains, owners, core/source-of-truth documents, and initial
   navigation outline.
9. Missing optional inputs do not block initialization.
10. The initial outline is explicitly reader navigation, not a storage-folder tree.
11. Created home/map guidance requires the confirmed wiki name and records source boundary, destination route,
    and language.
12. Root/package English and Chinese documentation and I1–I4/S0–S1b scenarios consistently cover the
    contract.

### Shared Markdown registry correction

13. `/Users/esun/company-wiki/index.md` exists as the sole registry entry;
    `/Users/esun/company-wiki/wikis/` exists for profiles.
14. The registry contains no skill code. Versioned skill source remains under
    `/Users/esun/Documents/Projects/company-wiki/skills/company-wiki/`.
15. `/Users/esun/.agents/skills/company-wiki` is a symlink resolving exactly to that repository skill
    directory.
16. `SKILL.md` and `registry.md` require entry-first loading, one selected profile, and no registry-directory
    scan.
17. Profile routes must be relative Markdown links whose normalized resolved targets remain under
    `~/company-wiki/wikis/`; URLs, absolute paths, traversal, missing targets, symlink escapes, duplicates,
    and ambiguous matches are rejected.
18. The profile contract records wiki name, source locations/scope/read boundary, destination/write boundary,
    language, optional inputs, and native home/map link.
19. Successful registration writes one profile and one index link while preserving unrelated registry text.
20. Registration is collision-safe and idempotent; conflicting identities, labels, filenames, or targets are
    preserved and rejected rather than overwritten.
21. Missing/unavailable behavior is defined separately for setup, query, maintenance, and validation; no
    workflow invents configuration or claims unavailable persistence.
22. Registry feasibility is checked before provider creation. A later registration failure reports partial
    completion and the native home link, preserves previous registry bytes, and does not delete provider
    documents.
23. Registry content is restricted to locators and navigation metadata and treated as untrusted data, not
    instructions or evidence. The installed empty registry contains no profile, source copy, credential,
    evidence cache, YAML, or sidecar.
24. Root/package documentation clearly separates versioned skill, user registry, discovery symlink,
    provider-native wiki, and original evidence.
25. R1–R6, including R2b and R3b, cover discovery, entry-first loading, containment, unsafe routes,
    ambiguity, registration, preservation, idempotency, collisions, missing/unavailable configuration, and
    provider-success/registration-failure behavior.

### Limitations and residual risk

- The actual registry is intentionally empty because no real wiki was initialized. Profile creation,
  collision, and provider-failure behavior are contract/spec verified, not runtime exercised.
- Availability is local to agents that can access this user home; cross-machine and cloud-agent
  synchronization remain out of scope.
- Risk remains non-low because the design persists user-home configuration and exposes skill discovery
  across same-user local agents.

## Notes

- Story base: `ee6c766`.
- Implementation milestones: `4f07f0c`, `197db45`, `7f6fd3b`, `37b8708`, `00e3cac`.
- External state created: `/Users/esun/company-wiki/index.md` and
  `/Users/esun/company-wiki/wikis/`. The pre-existing correct skill symlink was preserved.
- No original source, provider wiki, cloud-drive collection, or baseline `docs/**` file was modified.
- The `!!` run stopped after DD and before GC. GC was resumed only after the user's explicit follow-up
  authorization to commit this change.
