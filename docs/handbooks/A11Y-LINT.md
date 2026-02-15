# a11y-lint Handbook

The scanner/linter that produces accessibility findings and writes the canonical scorecard used by `a11y-ci`.

## Quickstart

**Install**
```bash
pip install -e src/a11y-lint
```

**Run**
```bash
a11y-lint scan docs --artifact-dir .a11y_artifacts
```

**Output**
* `.a11y_artifacts/current.scorecard.json`
* `.a11y_artifacts/result.json`

**Common Failures**
* `A11Y.SCAN.IO`: Input path does not exist
* `A11Y.SCAN.SCHEMA`: Output directory not writable

## Install

**Source-of-truth:** Lives in `accessibility-suite` (standalone `a11y-lint` repo may be deprecated).
**Recommended dev install:** Editable install from monorepo (e.g., `pip install -e src/a11y-lint`).

## Usage

### Standard mode (recommended)

Writes outputs to `.a11y_artifacts/`:

```bash
a11y-lint scan --artifact-dir .a11y_artifacts
```

**Expected outputs:**
* `.a11y_artifacts/current.scorecard.json`
* `.a11y_artifacts/result.json`

### Using a custom output directory

```bash
a11y-lint scan --artifact-dir path/to/output
```

## Output: scorecard schema

`current.scorecard.json` follows the locked schema:

* required `meta` object (tool, version)
* required `findings[]`
  * each finding: `id`, `severity`, `message` (+ optional `location`)

## Troubleshooting

If `a11y-ci` rejects your scorecard, validate that you’re writing:
* `meta.tool`, `meta.version`
* `findings[].id`, `findings[].severity`, `findings[].message`
