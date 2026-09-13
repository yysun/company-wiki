# Chinese-case command failure — September 13, 2026

The Chinese answer was correct. Its first search command omitted `rag-` from the supplied temporary
corpus path, so the [Query comparison](query-comparison-2026-09-13.md) correctly marked that execution
invalid. The session later corrected the path and answered three office days with department-head
approval for exceptions. This was a command-copying failure, not an observed Chinese comprehension error.

The benchmark now supplies a short, fixed `./corpus-tool` command. **All three Chinese reruns passed**,
alongside three cancellation-case runs that exercise wiki routing and multiline citations.

## Fix

Each session gets an executable launcher bound to its exact corpus and interpreter. The model supplies
only `list`, `search 'pattern'`, or `read ID [ID ...]` from the session working directory. The launcher
ends option parsing before forwarding arguments, so callers cannot override the corpus location.

The trace checker accepts only the new command form for new sessions. It still rejects other paths,
extra flags, shell chaining, substitutions, unknown document IDs, and mismatched read content. The
existing discovery, read, character-budget, and routing checks remain in place. Each launcher is
snapshotted and hashed; a missing or changed launcher or corpus invalidates the run.

The historical long-path contract remains available for old traces. Revalidating all **51 earlier
traces** reproduced their recorded checks exactly, including the original invalid FQ12 execution.
No old result was replaced or excused. The exact citation scorer is unchanged, confirmed by comparing
its parsed function body with the previous runner snapshot. This correction requires no additional
change to the Query reference.

## Repeated verification

Each case ran three times in a fresh ephemeral session using `gpt-6-astra`, high reasoning, the current
Query reference including the citation fix, and the same synthetic corpora. All six sessions ran
sequentially. This is a targeted regression check; the full 20-question benchmark was not rerun.

| Case | Valid executions | Semantic passes | Rubric items | Exact citations |
|---|---:|---:|---:|---:|
| FQ12 — Chinese question over English policy sources | 3/3 | 3/3 | 9/9 | 10/10 |
| EQ04 — cancellation, active status, and login inactivity | 3/3 | 3/3 | 9/9 | 8/8 |
| Total | 6/6 | 6/6 | 18/18 | 18/18 |

All six runs stayed within retrieval bounds, and all three example runs followed the wiki routing
contract. Thirteen quotes contained preserved line breaks. All six raw traces and launcher bindings
were revalidated; snapshots matched their recorded hashes and original sources remained unchanged.

All 18 benchmark unit tests passed, including real launcher execution with Chinese text and paths
containing spaces, corpus binding from another working directory, rejected corpus overrides, launcher
tampering, historical wrong-path rejection, and unchanged retrieval-budget and citation checks.
Skill validation and whitespace checks passed. CR risk: low; review round: 1; reviewer: not applicable;
CR passed with no major findings.

The implementing agent also reviewed the actual answers against the original evidence and frozen
rubrics. This was not independent human review. The fix removes the observed long-path copying burden;
three successful repetitions do not establish universal command or multilingual reliability.

## Local evidence

Exact prompts, answers, raw traces, launcher snapshots, and answer-hash-bound reviews are retained in
Git-ignored `results/`; previous observations remain unchanged.

- [Run 1 scorecard](results/2026-09-13-command-fix/run-1/report.md)
- [Run 2 scorecard](results/2026-09-13-command-fix/run-2/report.md)
- [Run 3 scorecard](results/2026-09-13-command-fix/run-3/report.md)
- [Aggregate verification](results/2026-09-13-command-fix/verification.json)
- [Historical trace verification](results/2026-09-13-command-fix/historical-verification.json)
- [Test design](results/2026-09-13-command-fix/design.json)
