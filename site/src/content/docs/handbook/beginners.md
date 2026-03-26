---
title: For Beginners
description: New to the Accessibility Suite? Start here for a gentle introduction.
sidebar:
  order: 99
---

## What is this tool?

The Accessibility Suite is a collection of six tools that work together to find accessibility problems in your code, prove the problems are real (with cryptographic evidence), block regressions in CI, and tell you exactly how to fix them.

Think of it as a pipeline: scan your code, gate your builds, get fix guidance — all with tamper-evident proof that the results haven't been altered.

## Who is this for?

- **Development teams** who want accessibility checks built into their CI pipeline
- **QA engineers** needing auditable evidence of accessibility compliance
- **Accessibility advocates** pushing for automated, verifiable standards enforcement
- **AI tool builders** who want to integrate accessibility checking through MCP (Model Context Protocol)

No deep accessibility expertise is required — the suite's output tells you what's wrong, why it matters, and how to fix it.

## Prerequisites

- **Python 3.10+** — for a11y-lint, a11y-ci, and a11y-assist (`python --version`)
- **Node.js 18+** — for a11y-evidence-engine and a11y-mcp-tools (`node --version`)
- **pip and npm** — Python and Node.js package managers
- **Basic terminal skills** — you'll run CLI commands and shell scripts

## Your First 5 Minutes

### 1. Install the two core tools

```bash
pip install a11y-lint a11y-ci
```

### 2. Scan some CLI output

Save this as `sample-output.txt`:

```
Error: file not found
```

```bash
a11y-lint scan sample-output.txt
```

a11y-lint checks whether your CLI output follows accessible patterns (structured errors, no color-only indicators, etc.).

### 3. Run the demo pipeline (optional but recommended)

Clone the full suite and run the demo:

```bash
git clone https://github.com/mcp-tool-shop-org/accessibility-suite
cd accessibility-suite/examples/a11y-demo-site
./scripts/a11y.sh
```

This scans intentionally broken HTML, captures provenance, verifies integrity, and produces fix advisories — the full pipeline in one command.

### 4. Inspect the results

After running the demo, look at:
- `.a11y_artifacts/` — the unified artifact directory containing scorecards, evidence, and gate results
- `results/a11y-assist/advisories.json` — fix recommendations for each finding

### 5. Try the CI gate

```bash
pip install a11y-ci
a11y-ci gate --artifact-dir .a11y_artifacts
```

This evaluates the findings against your policy and returns exit code 0 (pass) or 3 (fail).

## Common Mistakes

1. **Installing only one tool** — The suite tools are designed to work together. a11y-lint produces scorecards, a11y-ci gates on them, and a11y-assist explains fixes. Installing just one gives you part of the value.

2. **Confusing the two scanning tools** — `a11y-lint` scans CLI text output for accessible message patterns. `a11y-evidence-engine` scans HTML files for WCAG violations. They serve different purposes and produce different artifacts.

3. **Ignoring exit codes** — Exit code 2 means input error (bad JSON, missing files). Exit code 3 means the policy gate failed (actual findings). Don't treat all non-zero exits the same way in your CI scripts.

4. **Skipping the `--artifact-dir` flag** — Many suite commands expect a shared `.a11y_artifacts/` directory. If you skip it, tools can't find each other's output. Use `--artifact-dir .a11y_artifacts` consistently.

5. **Expecting browser-rendered analysis** — The evidence engine does static HTML parsing. It won't catch issues that require JavaScript execution or CSS rendering. For dynamic apps, capture the rendered HTML first.

## Next Steps

- **[Getting Started](../getting-started/)** — Full installation for all six tools
- **[Architecture](../architecture/)** — How the pipeline fits together
- **[Tools](../tools/)** — Deep dive into each individual tool
- **[CI Integration](../ci-integration/)** — Add accessibility gating to your GitHub Actions
- **[Reference](../reference/)** — Full command reference and schemas

## Glossary

| Term | Definition |
|------|-----------|
| **a11y** | Short for "accessibility" (a, 11 letters, y) |
| **WCAG** | Web Content Accessibility Guidelines — the international standard for web accessibility |
| **Scorecard** | A JSON file listing accessibility findings from a scan |
| **Finding** | A single detected accessibility issue (e.g., missing alt text) |
| **Provenance** | Cryptographic proof that evidence is authentic and unmodified |
| **Evidence bundle** | A collection of findings with provenance records and integrity digests |
| **Gate** | A pass/fail policy check that blocks or allows a CI build |
| **Allowlist** | Temporary suppressions for known findings, each with an owner and expiry date |
| **MCP** | Model Context Protocol — lets AI assistants call tools like the accessibility scanner |
| **Low-vision-first** | Output format with [OK]/[WARN]/[FAIL] status + What/Why/Fix sections for readability |
| **Artifact directory** | The `.a11y_artifacts/` folder where all tools read and write shared data |
