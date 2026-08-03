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