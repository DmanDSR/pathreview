## Part 1 — Understanding the Issue

**Can I explain what this issue is asking for in my own words?**

Paraphrase the issue without looking at it. If you can't, you don't understand it well enough yet. Read the full issue body, look at any linked PRs or comments, and try again.

[*] I can explain the problem and the expected behavior in 2–3 sentences without reading the issue.

**Do I understand which part of the app is affected?**

Check the labels on the issue — they often indicate the area (api, rag, ingestion, frontend, etc.). Look at the referenced files if any are mentioned. Find those files in the repo.

[*] I've located the relevant files and confirmed they exist in the codebase.

**Do I understand what "done" looks like?**
[*] Yes

**Can you describe what the app should do (or not do) once the issue is fixed?** 

If the issue has acceptance criteria, read them carefully. If it doesn't, try writing your own — that forces you to understand the scope.

[*] I can describe a concrete before-and-after: what the user sees before the fix and what they see after.

## Part 2 — Tier Fit
Issues in the tracker are tagged with a tier level. Here's what each one means:

T**ier	Description	Typical scope**
**Tier 1**	Self-contained, localized fix. The change lives in one or two files and doesn't require understanding how the whole system fits together.	Bug fix, missing validation, broken test, documentation update
**Tier 2**	Requires understanding how two or more modules interact. May involve a service layer, database model, or API endpoint.	Feature addition, refactor, data flow bug
**Tier 3**	Requires understanding the full system — multiple modules, possibly infrastructure or AI pipeline changes.	Architecture change, cross-cutting behavior, RAG or agent modification

**Is the tier a realistic match for where I am right now?** 

[*] If this is my first open source contribution: I'm choosing Tier 1.

This tier works best for me with my time constraints and skill level. This summer schedule allows me to handle a problem of this level.

## Part 3 — Codebase Readiness

**Can I find the relevant code?**

Before claiming the issue, locate the specific function, route, or module it describes. Don't rely on grep alone — open the file, read the surrounding context, and confirm you're in the right place.

[*] I've found and read the specific code the issue references (not just the file — the function or section).

**Do I understand the surrounding code well enough to change it safely?**

You don't need to understand the whole codebase. But you need to understand the file you're about to edit well enough to predict what a change will break. Read the function signatures, docstrings, and any callers.

[*] I've read enough surrounding context that I can write a rough plan for the fix without looking anything up.

**Have I read the relevant test file?**

Find the test file for the module your issue touches (tests/unit/ is the right place to start). Look at how existing tests are structured — fixtures, assertions, mock patterns. You'll need to write at least one new test.

[*] I've found the test file for my module and read at least one test end-to-end.

## Part 4 — Scope and Time

**How many others are already working on this issue?**

Claims are non-exclusive — more than one student may work on the same issue, and your grade comes from your own artifacts, never from being first. Still, check the issue comments and the Claims column in the Issue Catalog tab of the cohort ledger: a less-crowded issue of the same tier can mean smoother coaching and peer review.

[*] I've checked the issue comments and the ledger's Claims count, and I'm fine with how many others are on this issue.

**Is the scope realistic for Weeks 8–9?**

You have roughly two weeks to implement, test, and submit a PR. Tier 1 issues should take 3–6 hours of focused work. Tier 2 issues may take 8–12 hours. Tier 3 issues can take significantly longer.

Think about your week — other classes, work, other commitments. Is this achievable?

[*] I've estimated the time this will take and I'm confident I can complete it before the Week 9 deadline.

**Are there any blockers or dependencies?**

Some issues say "blocked by #X" or reference another issue that needs to be resolved first. Check the issue for any such dependencies.

[*] This issue has no open blockers or dependencies on other unresolved issues.


## Week 7 — Issue selection

**Issue link:** [(https://github.com/ascherj/pathreview/issues/50)]

**Issue title:** [Add a has_tests boolean to the repo analysis output #50]

**Tier:** [*] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
This issue it adding detection logic to the project. This means adding logic to see if a repository has a tests/ or test/ directory, a pytest.ini, or test files matching test_*.py, and shows a boolean field in the analysis output. I am thinking for the core structural approach to either use Declarative rules or modular components and anf for the lifecycle pipeline approach using version control with git

**Branch name:** [50-dev-environment-setup]

**Setup confirmation:** [*] App runs locally at localhost:5173

**Cohort ledger:** [*] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/DmanDSR/pathreview/commit/ec77790306b1ba4ce36c124700b74a72c13e4b07

**Reproduction summary:**
Added a failing unit test (`tests/unit/test_github_tool.py`) that mocks the GitHub API and drives `GitHubTool._fetch_repo_metadata()` — the agent-side repo analysis tool named in issue #50. The test asserts the analysis output contains a `has_tests` boolean; it fails today because the output dict (github_tool.py:86-97) reports `has_readme` but has no `has_tests` key, confirming the gap and pinning it to that exact dict. (A separate path, `ingestion/parsers/repo_analyzer.py`, already has `has_tests` — that is out of scope; the issue targets the agent tool.)

**PLAN.md link:** https://github.com/DmanDSR/pathreview/blob/chore/50-dev-environment-setup/PLAN.md

**Walkthrough video (recommended):** [link to your Loom video, ≤2 min — recommended, not graded]

**Blockers or open questions:**
The manifest lists `agent/tools/repo_analyzer.py` as a target file, but it does not exist in the current tree — the agent's repo analysis lives entirely in `github_tool.py`, so that is where the fix will go. Open question for Week 9: detecting tests needs the repo file tree (an extra GitHub API call, like `_has_readme`); confirm the Git Trees API is the right approach and how to handle truncated trees on large repos.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
Before writing any code I recorded a baseline of the existing failures (see the
pre-existing failures note below), so I could prove later that my changes added
none. PLAN.md steps 1–3 are done, in commit `616b1df`
(`feat(agent): add has_tests detection to repo analysis output`):

- **Step 1 — detection helper.** Added `GitHubTool._has_tests()`, which reads the
  repo file tree from the GitHub Git Trees API
  (`GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1`) and reports whether
  any path is a test marker. It reuses the auth-header pattern from `_has_readme`.
- **Step 2 — wired into the output.** `_fetch_repo_metadata()` now includes
  `"has_tests"`. I pass the `default_branch` already present in the repo JSON
  instead of re-fetching it, so the feature costs exactly one extra API call.
- **Step 3 — graceful failure.** The tree request is wrapped in try/except and
  defaults to `False`, the same defensive shape as `_has_readme`, so a missing
  branch, a rate limit, or a network error can never break repo analysis.

One design change from PLAN.md: I split the path matching into a separate pure
`_path_indicates_tests(path)` classmethod. The plan's edge cases called out that
`contest/` and `latest/` must not match, so the matcher splits a path on `/` and
compares whole segments rather than doing a substring test. Pulling it out of the
network code means those false-positive traps can be tested directly with no HTTP
mocking at all.

The Week 8 reproduction test now passes.

**Next steps:**
PLAN.md steps 4–5: widen `tests/unit/test_github_tool.py` past the single
reproduction case to cover each detection marker, the false-positive traps, and
the API-failure paths; then re-run the full checks and diff them against my
baseline to confirm no new failures.

**Blockers:**
None. Both Week 8 open questions are resolved: the Git Trees API with
`recursive=1` is the right call, and for truncated trees I return `False` rather
than paginating — under-reporting is acceptable for Tier 1 and is commented in
the code. I also confirmed the third open question from PLAN.md ("should a
downstream consumer use `has_tests`?") is a no: `agent/orchestrator.py` caches
`ToolResult.data` as an untyped dict with no schema, so adding a key is purely
additive and the issue only asks to surface the field.

---

### Check-in 2 (end of week)

**PR link:** (https://github.com/ascherj/pathreview/pull/299)

**Branch:** `chore/50-dev-environment-setup`

**What you built:**
The agent-side repo analysis in `agent/tools/github_tool.py` reported
`has_readme` but had no test signal. It now also reports `has_tests`: a new
`_has_tests()` helper reads the repository file tree via the GitHub Git Trees API
and returns `True` when any path is a test marker — a `tests/` or `test/`
directory, a `pytest.ini`, or a `test_*.py` file. Matching happens on whole path
segments via `_path_indicates_tests()`, so `contest/` and `latest/` are not false
positives, and any failure reading the tree degrades to `False` so analysis never
crashes.

**Tests added or updated:**
`tests/unit/test_github_tool.py` — grew from the 1 Week 8 reproduction test to 26
passing tests. Through `execute()`: each marker type detected (`tests/` dir,
scattered `test_*.py`, `pytest.ini`), a repo with no markers reporting `False`, a
tree request error and a non-200 tree response both degrading to `False`, a
truncated tree still reporting markers it did see, the tree being requested
recursively from the repo's default branch, and a regression check that all ten
pre-existing metadata fields are untouched. Directly against
`_path_indicates_tests`: parametrized marker paths plus the false-positive traps
(`contest/entry.py`, `latest/build.py`, `src/protest.py`, `docs/testing.md`,
`attestation.py`) that a naive substring match would wrongly flag. The original
reproduction test is kept as the regression guard that the field exists and is a
bool.

**Self-review confirmation:** [*] make check passes  [*] make test-unit passes

Checked per the pre-existing-failures rule below — this codebase has documented
pre-existing failures in both commands, so "passes" here means **my changes
introduce no new failures**, verified by diffing against the baseline I took
before starting:

- `make test-unit`: **54 failed / 375 passed** before → **53 failed / 401 passed**
  after. Diffing the two failure lists, new failures: **none**. The one that
  flipped to passing is my own Week 8 reproduction test; the other 25 tests I
  added all pass.
- `make check`: fails at its first step (`lint`) both before and after, on **181
  pre-existing ruff errors** across files I never touched — so it never reaches
  `format` or `typecheck`. The repo-wide count is **exactly 181 before and after**,
  so I added none. Scoped to my two changed files, `ruff`, `black --check`, and
  `mypy` are all clean, and the repo's own pre-commit hooks (ruff, black, mypy)
  passed on both commits.
- `make typecheck` independently: **5 pre-existing errors** before and after —
  missing library stubs (`PyPDF2`, `jose`, `passlib`, `rank_bm25`) plus a numpy
  stub that needs Python 3.12+ syntax. All are in files I did not touch, and mypy
  reports "errors prevented further checking", so it bails before reaching
  `agent/`. That is why I ran mypy directly on `agent/tools/github_tool.py`
  (clean) rather than relying on `make typecheck`.

**Pre-existing failures observed (documented for the PR description):** the 181
ruff errors, the 5 mypy errors, and 53 failing unit tests listed above all predate
this branch and are unrelated to issue #50. My changes do not affect them.

**Draft PR feedback received from:** [name or Slack handle, or "none"]