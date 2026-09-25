# accessibility-suite: how it works

Mapped at 2026-09-25 from commit cfd4730.

## What this is

15 parts, mostly Python (74 files), JavaScript (32) and TypeScript (2). Work enters through 7 doors; the busiest is CI, which reaches 3 parts. It publishes to npm. People run a11y-assist, a11y-ci, a11y-lint and assist-run.

## What changed since the last map

This is the first map.

## What comes in

1. **CI.** On a pull request to main touching 13 paths; on a push to main touching 13 paths; or by hand. Runs scripts/verify_handbooks.py, src/a11y-ci/a11y_ci/cli.py and src/a11y-lint/a11y_lint/cli.py.
2. **Deploy site to GitHub Pages.** On a push to main touching 2 paths; or by hand. Runs site/astro.config.mjs and site/src/.
3. **Publish to npm.** By hand. Runs scripts/verify.sh and scripts/verify_handbooks.py.
4. **a11y-assist** (a command people run). Runs src/a11y-assist/a11y_assist/cli.py.
5. **a11y-ci** (a command people run). Runs src/a11y-ci/a11y_ci/cli.py.
6. **a11y-lint** (a command people run). Runs src/a11y-lint/a11y_lint/cli.py.
7. **assist-run** (a command people run). Runs src/a11y-assist/a11y_assist/cli.py.

## What happens through CI

1. The workflow runs src/a11y-ci/a11y_ci/cli.py in a11y-ci, src/a11y-lint/a11y_lint/cli.py in a11y-lint and scripts/verify_handbooks.py in scripts.
2. It writes to docs/baselines/a11y.scorecard.json.
3. It also writes to src/a11y-ci/report.json, which is not tracked.
4. It commits docs/baselines/a11y.scorecard.json and pushes when run by hand.

## Who reads the results

- **docs/baselines/a11y.scorecard.json** has no reader in this repository.

## The other doors

**Deploy site to GitHub Pages** runs site/astro.config.mjs and site/src/, and deploys the site.

**Publish to npm** runs scripts/verify.sh and scripts/verify_handbooks.py, and publishes to npm.

**a11y-assist** (a command people run) runs src/a11y-assist/a11y_assist/cli.py.

**a11y-ci** (a command people run) runs src/a11y-ci/a11y_ci/cli.py.

**a11y-lint** (a command people run) runs src/a11y-lint/a11y_lint/cli.py.

**assist-run** (a command people run) runs src/a11y-assist/a11y_assist/cli.py.

## What breaks what

- **a11y-assist** is imported by no other part and sits on the path of 2 doors.
- **a11y-ci** is imported by no other part and sits on the path of 2 doors.
- **a11y-lint** is imported by no other part and sits on the path of 2 doors.
- **scripts** is imported by no other part and sits on the path of 2 doors.

## What tends to change together

No two source files changed together often enough to name.

Window: 180 days; a pair counts from 3 shared commits, since the window holds fewer than 30 qualifying commits.

## What no test touches

- **scripts** is imported by no test.

36 test files run in no workflow: src/a11y-assist/tests/test_cognitive_load.py, src/a11y-assist/tests/test_dyslexia.py, src/a11y-assist/tests/test_explain.py and 33 mores.

## Written but never read

- **docs/baselines/a11y.scorecard.json** is written by .github/workflows/ci.yml and read by nothing else in this repository.

## Helpers that look duplicated

These are candidates from names and call order, not a judgement.

- **main** is exported by 3 parts (a11y-assist, a11y-ci and a11y-lint); with the same name in this many parts it is most likely a shared contract, not a copy.
- **render** is exported by src/a11y-ci/a11y_ci/render.py (a11y-ci) and src/a11y-lint/a11y_lint/render.py (a11y-lint); the two look alike.

## Generated, never hand-edited

- **docs/baselines/a11y.scorecard.json** is written by .github/workflows/ci.yml.

## Hand-authored

People write .a11y_artifacts_test/, .github/, assets/, examples/, pipelines/, the repository root and site/; 6 writes with paths built at run time may land here.

## Where to start

.github/workflows/ci.yml → src/a11y-ci/a11y_ci/cli.py → src/a11y-ci/a11y_ci/__init__.py → src/a11y-ci/a11y_ci/allowlist.py → src/a11y-ci/a11y_ci/gate.py → src/a11y-ci/a11y_ci/render.py → src/a11y-ci/a11y_ci/scorecard.py → src/a11y-ci/a11y_ci/mcp_payload.py

Read those in order to follow one pull request end to end.

## What this map cannot see

- 6 writes and 22 reads use paths built at run time and are not named here.
- 1 write goes to places this repository does not track, so it is not listed as generated.
- 8 writes and 10 reads go to a path their caller passes, not to this repository.
- 1 write and 1 read go to the home directory (.a11y-assist/), not to this repository.
- 1 read goes to the directory the command is run in (spec/), not to this repository.
- Statistics confidence is low: fewer than 30 qualifying commits in the window, and fewer than 20 source files reach 10 revisions.

Regenerate with `npx --yes @dogfood-lab/atlas map`.
