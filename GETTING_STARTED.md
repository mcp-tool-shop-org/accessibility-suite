# Getting Started with the Accessibility Suite

Welcome! The Accessibility Suite is a collection of tools designed to make accessibility testing, gating, and remediation seamless in your development workflow.

## 🚀 Run locally in 3 commands

1.  **Install the tools** (from the monorepo root)
    ```bash
    pip install -e src/a11y-lint
    pip install -e src/a11y-ci
    ```

2.  **Scan your project**
    ```bash
    # Scans your code and outputs to .a11y_artifacts/current.scorecard.json
    a11y-lint scan . --artifact-dir .a11y_artifacts
    ```

3.  **Run the gate**
    ```bash
    # Checks compliance against the scorecard
    a11y-ci gate --artifact-dir .a11y_artifacts
    ```

## 📦 Run in GitHub Actions

Use our pre-built action to add a gate to your PRs.

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # 1. Generate artifacts (Scan)
      - name: Scan Code
        run: |
            pip install a11y-lint
            mkdir .a11y_artifacts
            a11y-lint scan . --artifact-dir .a11y_artifacts

      # 2. Run Gate
      - uses: mcp-tool-shop-org/accessibility-suite/.github/actions/a11y-ci@main
        with:
          artifact-dir: .a11y_artifacts
          fail-on: serious
```

## 🔧 Run in Azure DevOps

Use the PowerShell wrapper in your pipeline.

```yaml
steps:
  - script: |
      pip install a11y-lint a11y-ci
      a11y-lint scan . --artifact-dir .a11y_artifacts
    displayName: 'Scan Accessibility'

  - task: PowerShell@2
    inputs:
      targetType: 'filePath'
      filePath: 'tools/ado/a11y-ci.ps1'
      arguments: '-ArtifactDir .a11y_artifacts -FailOn serious'
    displayName: 'Accessibility Gate'
```

## 🆘 Troubleshooting

**Where to look when it fails:**

*   **Console Output:** First check the logs for error IDs (e.g., `A11Y.CI.Schema.Invalid`).
*   **Artifacts:** Look in `.a11y_artifacts/` for `gate-result.json` (machine readable) and `report.txt` (human readable).

**Common Errors:**

| Error ID | Meaning | Fix |
| :--- | :--- | :--- |
| `A11Y.SCAN.IO` | Scanner input invalid | Check your file paths. |
| `A11Y.CI.Schema.Invalid` | Bad scorecard JSON | Ensure `a11y-lint` produced valid JSON. |
| `A11Y.CI.Gate.Failed` | Accessibility violations | Remediate verify or add waivers. |

## 📚 Learn More

*   [Accessibiltiy Suite Handbook](docs/handbooks/README.md)
*   [Unified Artifacts](docs/unified-artifacts.md)
