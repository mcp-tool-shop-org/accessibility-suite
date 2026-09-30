# accessibility-suite: how it works

Mapped at 2026-09-30 from commit f18e246 by Atlas 1.24.0.

## What this is

15 parts, mostly Python (74 files), JavaScript (32), HTML (7), CSS (2), TypeScript (2), shell (2), Astro (1) and PowerShell (1). Work enters through 10 doors; the busiest is CI, which reaches 6 parts. It deploys a site to GitHub Pages. People run a11y, a11y-assist, a11y-ci, a11y-engine, a11y-lint, a11y-mcp and assist-run.

## What changed since 2026-09-25 (cfd4730)

- CI now also runs src/a11y-assist/tests/, src/a11y-ci/tests/, src/a11y-evidence-engine/test/ and 5 more.
- a11y-engine (src/a11y-evidence-engine/package.json) is a new command. It runs src/a11y-evidence-engine/bin/a11y-engine.js.
- a11y (src/a11y-mcp-tools/package.json) is a new command. It runs src/a11y-mcp-tools/bin/cli.js.
- And 1 more change to a door.
- docs/baselines/a11y.scorecard.json is now read by .github/workflows/ci.yml.
- 1 file changed content, across 1 part.

## What comes in

1. **CI.** On a pull request to main touching 13 paths; on a push to main touching 13 paths; or by hand. Runs scripts/verify_handbooks.py, src/a11y-ci/a11y_ci/cli.py, src/a11y-lint/a11y_lint/cli.py and 39 more.
2. **Deploy site to GitHub Pages.** On a push to main touching 2 paths; or by hand. Runs site/astro.config.mjs and site/src/.
3. **Publish to npm.** By hand. Runs scripts/verify.sh and scripts/verify_handbooks.py.
4. **a11y** (a command people run). Runs src/a11y-mcp-tools/bin/cli.js.
5. **a11y-assist** (a command people run). Runs src/a11y-assist/a11y_assist/cli.py.
6. **a11y-ci** (a command people run). Runs src/a11y-ci/a11y_ci/cli.py.
7. **a11y-engine** (a command people run). Runs src/a11y-evidence-engine/bin/a11y-engine.js.
8. **a11y-lint** (a command people run). Runs src/a11y-lint/a11y_lint/cli.py.
9. **a11y-mcp** (a command people run). Runs src/a11y-mcp-tools/bin/server.js.
10. **assist-run** (a command people run). Runs src/a11y-assist/a11y_assist/cli.py.

## What happens through CI

1. The workflow runs src/a11y-assist/tests/ in a11y-assist, src/a11y-ci/a11y_ci/cli.py and src/a11y-ci/tests/ in a11y-ci, src/a11y-evidence-engine/test/ in a11y-evidence-engine, src/a11y-lint/a11y_lint/cli.py and src/a11y-lint/tests/ in a11y-lint, 4 files in a11y-mcp-tools, and scripts/verify_handbooks.py in scripts.
2. When run by hand, it writes to docs/baselines/a11y.scorecard.json.
3. It writes to src/a11y-ci/report.json, which is not tracked.
4. It commits docs/baselines/a11y.scorecard.json and pushes when run by hand.

## Who reads the results

Only CI itself reads what it writes.

## The other doors

**Deploy site to GitHub Pages** runs site/astro.config.mjs and site/src/, and deploys the site.

**Publish to npm** runs scripts/verify.sh and scripts/verify_handbooks.py.

**a11y** (a command people run) runs src/a11y-mcp-tools/bin/cli.js.

**a11y-assist** (a command people run) runs src/a11y-assist/a11y_assist/cli.py.

**a11y-ci** (a command people run) runs src/a11y-ci/a11y_ci/cli.py.

**a11y-engine** (a command people run) runs src/a11y-evidence-engine/bin/a11y-engine.js.

**a11y-lint** (a command people run) runs src/a11y-lint/a11y_lint/cli.py.

**a11y-mcp** (a command people run) runs src/a11y-mcp-tools/bin/server.js.

**assist-run** (a command people run) runs src/a11y-assist/a11y_assist/cli.py.

## What breaks what

- **a11y-assist** is imported by no other part and sits on the path of 3 doors.
- **a11y-mcp-tools** is imported by no other part and sits on the path of 3 doors.
- **a11y-ci** is imported by no other part and sits on the path of 2 doors.
- **a11y-evidence-engine** is imported by no other part and sits on the path of 2 doors.
- **a11y-lint** is imported by no other part and sits on the path of 2 doors.
- **scripts** is imported by no other part and sits on the path of 2 doors.

tools holds only PowerShell files, which this map does not read, so what uses it cannot be seen.

## What tends to change together

No two source files changed together often enough to name.

Window: 180 days; a pair counts from 3 shared commits, since the window holds fewer than 30 qualifying commits.

## What no test touches

- **scripts** is imported by no test.

tools holds only PowerShell files, which this map does not read, so whether a test touches it cannot be seen.

## Written but never read

- **docs/baselines/a11y.scorecard.json** is written by .github/workflows/ci.yml and read by nothing else in this repository.

## Helpers that look duplicated

These are candidates from names and call order, not a judgement.

- **main** is exported by 3 parts (a11y-assist, a11y-ci and a11y-lint); with the same name in this many parts it is most likely a shared contract, not a copy.
- **render** is exported by src/a11y-ci/a11y_ci/render.py (a11y-ci) and src/a11y-lint/a11y_lint/render.py (a11y-lint); the two look alike.

## Generated, never hand-edited

- **docs/baselines/a11y.scorecard.json** is written by .github/workflows/ci.yml.

## Hand-authored

People write .a11y_artifacts_test/, .github/, assets/, examples/, pipelines/, the repository root and site/. Nothing in this repository writes to them.

## Where to start

.github/workflows/ci.yml → src/a11y-ci/a11y_ci/cli.py → src/a11y-ci/a11y_ci/gate.py → src/a11y-ci/a11y_ci/scorecard.py → src/a11y-ci/a11y_ci/severity.py

Read those in order to follow one pull request end to end.

## What this map cannot see

- 5 reads use paths built at run time and are not named here.
- 1 write goes to places this repository does not track, so it is not listed as generated.
- 19 writes and 27 reads go to a path their caller passes, not to this repository.
- 1 write and 1 read go to the home directory (.a11y-assist/), not to this repository.
- 1 read goes to the directory the command is run in (spec/) or a path its caller passes, not to this repository.
- 1 read goes to the directory the command is run in (spec/), not to this repository.
- Statistics confidence is low: fewer than 30 qualifying commits in the window, and fewer than 25 source files reach 10 revisions.

Regenerate with `npx --yes @dogfood-lab/atlas map`.
