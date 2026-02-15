# a11y-ci Handbook

The policy gate. It turns findings into a pass/fail decision, detects regressions, supports waivers, and produces evidence + PR comments.

## Quickstart

**Install**
```bash
pip install -e src/a11y-ci
```

**Run**
```bash
a11y-ci gate --artifact-dir .a11y_artifacts
```

**Output**
* `.a11y_artifacts/gate-result.json`
* `.a11y_artifacts/report.txt`
* `.a11y_artifacts/evidence.json`

**Common Failures**
* `A11Y.CI.Schema.Invalid` (Exit 2): Scorecard JSON is mangled
* `A11Y.CI.Gate.Failed` (Exit 3): Open violations found

## Options

### Set the severity threshold

```bash
a11y-ci gate --artifact-dir .a11y_artifacts --fail-on serious
```

### Use a baseline
If `.a11y_artifacts/baseline.scorecard.json` exists, it is automatically used (unless overridden).

### Use an allowlist (waivers)
If `.a11y_artifacts/allowlist.json` exists, it is automatically used.

**Allowlist supports:**
* `owner` (required)
* `expires` (required)
* `ticket` (optional)
* suppression identity via `id` or `fingerprint` (best)

## Output formats

### Human report
`.a11y_artifacts/report.txt` is optimized for quick reading and low-vision clarity.

### Machine report
`.a11y_artifacts/gate-result.json` is stable and parseable.

### Evidence bundle (MCP)
`.a11y_artifacts/evidence.json` includes traceability metadata + hashes.

### PR comments
Generate from evidence (recommended):

```bash
a11y-ci comment --mcp .a11y_artifacts/evidence.json --platform github --top 10 > .a11y_artifacts/comment.md
```

## Error IDs and exit codes

* `0`: PASS
* `2`: Input error (schema, missing required file, etc.)
* `3`: Gate failed (policy violation / regression / expired waiver)
* `1`: Internal tool error

Error IDs are standardized (grep-friendly). If you see an error, copy the ID into issues/PR discussions.
