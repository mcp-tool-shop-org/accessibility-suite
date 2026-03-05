---
title: Tools
description: Detailed guide to each of the six tools in the Accessibility Suite.
sidebar:
  order: 3
---

The Accessibility Suite contains six tools. This page provides a detailed guide to each one: what it does, how to install it, how to use it, and what output to expect.

## a11y-lint

**The scanner.** Scans CLI output, error messages, and user-facing strings for accessible error message patterns. Produces a scorecard that downstream tools consume.

| Detail | Value |
|--------|-------|
| Stack | Python 3.10+ |
| Package | [PyPI: a11y-lint](https://pypi.org/project/a11y-lint/) |
| Source | `src/a11y-lint/` |

### Install

```bash
pip install a11y-lint
# or editable from monorepo:
pip install -e src/a11y-lint
```

### Usage

Scan a file or directory and write outputs to the artifact directory:

```bash
a11y-lint scan docs --artifact-dir .a11y_artifacts
```

You can also scan a single file:

```bash
a11y-lint scan output.txt
```

### Output

- `.a11y_artifacts/current.scorecard.json` -- the scorecard (required `meta` object with tool/version, plus a `findings[]` array where each finding has `id`, `severity`, `message`, and optional `location`)
- `.a11y_artifacts/result.json` -- detailed scanner result data

### Common errors

| Error ID | Meaning |
|----------|---------|
| `A11Y.SCAN.IO` | Input path does not exist |
| `A11Y.SCAN.SCHEMA` | Output directory not writable |

### Troubleshooting

If `a11y-ci` rejects your scorecard, verify that it contains the required fields: `meta.tool`, `meta.version`, and each finding has `id`, `severity`, and `message`.

---

## a11y-ci

**The policy gate.** Turns findings into a pass/fail decision, detects regressions against a baseline, supports allowlist waivers, and produces evidence bundles and PR comments.

| Detail | Value |
|--------|-------|
| Stack | Python 3.10+ |
| Package | [PyPI: a11y-ci](https://pypi.org/project/a11y-ci/) / [npm: @accessibility-suite/ci](https://www.npmjs.com/package/@accessibility-suite/ci) |
| Source | `src/a11y-ci/` |

### Install

```bash
pip install a11y-ci
```

### Usage

Run the gate against the artifact directory:

```bash
a11y-ci gate --artifact-dir .a11y_artifacts
```

Set a severity threshold (only fail on violations at or above this level):

```bash
a11y-ci gate --artifact-dir .a11y_artifacts --fail-on serious
```

Generate a PR comment from evidence:

```bash
a11y-ci comment --mcp .a11y_artifacts/evidence.json --platform github --top 10 > .a11y_artifacts/comment.md
```

### Baselines and allowlists

- **Baseline:** If `.a11y_artifacts/baseline.scorecard.json` exists, a11y-ci automatically compares the current scorecard against it to detect regressions.
- **Allowlist (waivers):** If `.a11y_artifacts/allowlist.json` exists, findings matching an allowlist entry are suppressed. Each waiver requires an `owner`, `expires` date, and optionally a `ticket` reference. Findings are matched by `id` or `fingerprint`.

### Output

| File | Description |
|------|-------------|
| `gate-result.json` | Structured pass/fail result (machine-readable) |
| `report.txt` | Human-readable report optimized for quick reading and low-vision clarity |
| `evidence.json` | Evidence bundle with traceability metadata and SHA-256 hashes |
| `comment.md` | PR comment markdown for GitHub or Azure DevOps |

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | PASS |
| `1` | Internal tool error |
| `2` | Input error (schema invalid, missing required file) |
| `3` | Gate failed (policy violation, regression, or expired waiver) |

---

## a11y-assist

**Fix guidance engine.** Given a known failure signature, it suggests safe remediation steps. Output is tuned to one of five accessibility profiles.

| Detail | Value |
|--------|-------|
| Stack | Python 3.10+ |
| Package | [PyPI: a11y-assist](https://pypi.org/project/a11y-assist/) |
| Source | `src/a11y-assist/` |

### Install

```bash
pip install a11y-assist
```

### Usage

Get help for a specific rule:

```bash
a11y-assist help --rule "aria-required"
```

Explain a failure with profile-specific guidance:

```bash
a11y-assist explain --json error.json --profile screen-reader
```

### Profiles

| Profile | What it optimizes for |
|---------|----------------------|
| `standard` | General remediation guidance |
| `low-vision` | Large text, high contrast, magnification-friendly fixes |
| `screen-reader` | ARIA attributes, landmark roles, focus management |
| `dyslexia` | Font choices, spacing, reading flow |
| `cognitive-load` | Simplified language, progressive disclosure, reduced complexity |

### Recommended workflow

1. Run `a11y-ci gate` and inspect `report.txt`
2. Use the `help_url` or `help_hint` fields in findings to locate the rule
3. Run `a11y-assist` for structured, profile-specific guidance

---

## a11y-evidence-engine

**Provenance scanner.** A headless engine that generates traceable, structured accessibility evidence from HTML files -- not just a list of findings, but screenshots, DOM snapshots, and a manifest with cryptographic integrity.

| Detail | Value |
|--------|-------|
| Stack | Node.js 18+ |
| Package | [npm: @accessibility-suite/evidence-engine](https://www.npmjs.com/package/@accessibility-suite/evidence-engine) |
| Source | `src/a11y-evidence-engine/` |

### Install

```bash
npm install -g @accessibility-suite/evidence-engine
```

### Usage

```bash
a11y-engine scan ./html --out ./results
```

### Output

- Screenshots (`.png`)
- DOM snapshots (`.html`)
- `.a11y_artifacts/evidence-manifest.json` -- links all artifacts together with SHA-256 hashes

### Best practices

- Store evidence artifacts under `.a11y_artifacts/` (or a subfolder like `.a11y_artifacts/evidence/`)
- Reference them from `evidence.json` so everything is linked and verifiable

---

## a11y-mcp-tools

**MCP integration layer.** An MCP server that exposes accessibility evidence capture and diagnosis as tools for AI assistants.

| Detail | Value |
|--------|-------|
| Stack | Node.js 18+ |
| Package | [npm: @accessibility-suite/mcp-tools](https://www.npmjs.com/package/@accessibility-suite/mcp-tools) |
| Source | `src/a11y-mcp-tools/` |

### Install

```bash
npm install -g @accessibility-suite/mcp-tools
```

### Usage

Start the MCP server:

```bash
mcp-server-a11y --evidence-dir .a11y_artifacts
```

The server reads `evidence.json` from the artifact directory and exposes it as MCP resources and prompts.

### MCP tools exposed

| Tool | Description |
|------|-------------|
| `a11y.evidence` | Capture tamper-evident evidence bundles from HTML, CLI logs, or other inputs |
| `a11y.diagnose` | Run WCAG rule checks over evidence bundles with provenance verification |

For MCP client configuration, see [MCP Integration](/accessibility-suite/handbook/mcp-integration/).

---

## a11y-demo-site

**End-to-end demo.** A static site with intentional accessibility violations, designed for testing the full pipeline.

| Detail | Value |
|--------|-------|
| Stack | HTML |
| Source | `examples/a11y-demo-site/` |

### Usage

```bash
cd examples/a11y-demo-site
npm install
npm run dev
```

### What it demonstrates

- How evidence is generated from real HTML
- How the CI gate catches violations and produces reports
- How PR comments look with real findings
- How to validate new workflows or rules without touching production repos

Use the demo site as the "golden tutorial" -- it exercises every tool in the suite.
