# Accessibility Suite Handbook

This is the authoritative source for the entire suite. Most “standalone” repos are migrated here.

**Handbooks track main. For released versions, refer to tagged docs.**

**Also see:**
* [Universal Concepts](COMMON-CONCEPTS.md)
* [a11y-lint](A11Y-LINT.md)
* [a11y-ci](A11Y-CI.md)
* [a11y-mcp-tools](A11Y-MCP-TOOLS.md)
* [a11y-assist](A11Y-ASSIST.md)
* [a11y-evidence-engine](A11Y-EVIDENCE-ENGINE.md)
* [a11y-demo-site](A11Y-DEMO-SITE.md)
* [ally-demo-python](ALLY-DEMO-PYTHON.md)
* [CursorAssist](CURSORASSIST.md)

## Install (developer)

Typical dev loop:

1. Clone `mcp-tool-shop-org/accessibility-suite`
2. Install tool packages from `src/…` (editable installs are preferred)

If your tools are Python packages (likely for `a11y-ci`, `a11y-lint`):

```bash
# Install per-package from monorepo
pip install -e src/<tool>
```

## Run (suite convention)

From the repo root:

```bash
a11y-lint scan --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
a11y-ci comment --mcp .a11y_artifacts/evidence.json --platform github > .a11y_artifacts/comment.md
```

## CI

* **GitHub Actions:** `.github/workflows/a11y-gate.yml`
* **Baseline update:** `.github/workflows/update-baseline.yml`
* **Golden integration tests:** `.github/workflows/test-a11y-action.yml`

## Where to add docs

* **Suite-wide conventions:** `docs/unified-artifacts.md`
* **Rule remediation index:** `docs/rules.md`
