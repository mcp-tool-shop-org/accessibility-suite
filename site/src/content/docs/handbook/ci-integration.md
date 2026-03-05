---
title: CI Integration
description: Gate your CI pipeline on accessibility regressions with GitHub Actions.
sidebar:
  order: 5
---

The Accessibility Suite is designed for automated pipelines. This page shows how to integrate it into GitHub Actions and other CI systems to gate releases on accessibility regressions.

## GitHub Actions

### Basic gate

The simplest integration scans your codebase and gates on accessibility violations:

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Scan code
        run: |
          pip install a11y-lint
          mkdir -p .a11y_artifacts
          a11y-lint scan . --artifact-dir .a11y_artifacts

      - uses: mcp-tool-shop-org/accessibility-suite/.github/actions/a11y-ci@main
        with:
          artifact-dir: .a11y_artifacts
          fail-on: serious
```

The composite action `a11y-ci` reads the scorecard, compares against any baseline, applies allowlists, and exits non-zero if the gate fails.

### With baseline regression detection

To detect regressions, store a baseline scorecard. The gate automatically compares against it:

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install tools
        run: pip install a11y-lint a11y-ci

      - name: Scan
        run: |
          mkdir -p .a11y_artifacts
          a11y-lint scan . --artifact-dir .a11y_artifacts

      - name: Gate with baseline
        run: a11y-ci gate --artifact-dir .a11y_artifacts
```

If `.a11y_artifacts/baseline.scorecard.json` exists in your repository, the gate uses it automatically. To update the baseline after fixing issues, use the baseline update workflow.

### With PR comments

Post a summary of findings directly on pull requests:

```yaml
      - name: Generate PR comment
        if: github.event_name == 'pull_request'
        run: |
          a11y-ci comment \
            --mcp .a11y_artifacts/evidence.json \
            --platform github \
            --top 10 \
            > .a11y_artifacts/comment.md

      - name: Post PR comment
        if: github.event_name == 'pull_request'
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: .a11y_artifacts/comment.md
```

### Upload artifacts

Always upload the artifact directory so developers can inspect detailed results:

```yaml
      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-artifacts
          path: .a11y_artifacts/
```

## Severity thresholds

The `--fail-on` flag controls which severity levels cause the gate to fail:

| Value | Fails on |
|-------|----------|
| `serious` | Only serious and critical violations |
| `moderate` | Moderate, serious, and critical |
| `minor` | All violations including minor |

Choose `serious` for most projects to avoid blocking on cosmetic issues while catching real barriers.

## Allowlists (waivers)

Sometimes you need to suppress a finding temporarily. Create `.a11y_artifacts/allowlist.json`:

```json
[
  {
    "id": "color-contrast",
    "owner": "team-frontend",
    "expires": "2026-06-01",
    "ticket": "JIRA-1234"
  }
]
```

Each waiver requires:

- **`owner`** -- who approved the waiver
- **`expires`** -- when the waiver expires (the gate fails on expired waivers)
- **`ticket`** (optional) -- link to the tracking issue
- **`id`** or **`fingerprint`** -- which finding to suppress

## Exit codes

Understanding exit codes helps you write conditional CI steps:

| Code | Meaning | Action |
|------|---------|--------|
| `0` | PASS | Pipeline continues |
| `1` | Internal error | Investigate the tool itself |
| `2` | Input error | Fix the scorecard or configuration |
| `3` | Gate failed | Fix the accessibility violations |

## CI workflows in the suite

The Accessibility Suite repository itself uses these workflows:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `a11y-gate.yml` | Push / PR | Runs the full scan-and-gate pipeline |
| `update-baseline.yml` | Manual | Updates the baseline scorecard after fixes |
| `test-a11y-action.yml` | Push / PR | Golden integration tests for the composite action |
