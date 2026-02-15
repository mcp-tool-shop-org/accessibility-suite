# Unified Artifact Strategy (Phase 5.3)

## Objective
Standardize artifact generation, storage, and consumption across all Accessibility Suite tools (`a11y-lint`, `a11y-assist`, `a11y-ci`).

## Directory Structure
All tools and CI pipelines must default to using `.a11y_artifacts/` as the root directory for outputs.

```
.a11y_artifacts/
├── evidence/                  # Signed/Verifiable Evidence
│   ├── a11y-lint.json        # Raw lint results (schema: cli.error.v0.1)
│   ├── a11y-gate.json        # Gate decision results
│   └── provenance.json       # Build/Environment provenance
├── reports/                   # Human-Readable Reports
│   ├── a11y-report.md        # Combined/Summary report
│   ├── a11y-report.html      # (Optional) HTML visualization
│   └── pr-comment.md         # Generated PR comment content
└── logs/                      # Debugging & Audit
    ├── a11y-lint.log
    ├── a11y-assist.log
    └── a11y-ci.log
```

## Tool Responsibilities

### 1. a11y-lint
- **Input**: Target text/file.
- **Output**: `evidence/a11y-lint.json` (Structured findings).
- **Format**: `cli.error.v0.1` schema.

### 2. a11y-ci
- **Input**: `evidence/a11y-lint.json`.
- **Output**: 
    - `evidence/a11y-gate.json` (Pass/Fail decision).
    - `reports/a11y-report.md` (Summary).
    - `reports/pr-comment.md` (Platform-specific comment).

### 3. a11y-assist
- **Input**: `evidence/a11y-lint.json` (or raw logs).
- **Output**: `logs/a11y-assist.log` (Recovery steps).

## CI Integration
CI Pipelines (GitHub Actions, Azure DevOps) must:
1. Create `.a11y_artifacts/` before execution.
2. Configure tools to output to this directory.
3. Publish the entire `.a11y_artifacts/` folder as a build artifact named `a11y-reports`.

## Implementation Plan
1. Update `a11y-ci` to accept an `--artifact-dir` flag (or default to `.a11y_artifacts`).
2. Update `a11y-lint` to support structured output to a specific path more easily.
3. Update CI templates to use this structure.
