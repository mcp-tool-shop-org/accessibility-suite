---
title: Getting Started
description: Install the Accessibility Suite and run your first scan in under a minute.
sidebar:
  order: 1
---

This guide walks you through installing the Accessibility Suite tools and running your first accessibility scan. By the end, you will have a scorecard, a CI gate result, and fix guidance -- all in under a minute.

## Prerequisites

- **Python 3.10+** for a11y-lint, a11y-ci, and a11y-assist
- **Node.js 18+** for a11y-evidence-engine and a11y-mcp-tools
- **pip** and **npm** available on your PATH

## Option A: Install from package registries

Install whichever tools you need. You do not have to install the entire suite.

### Lint CLI output for accessible patterns

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

This scans a file (or directory) for accessible error message patterns and produces a scorecard at `.a11y_artifacts/current.scorecard.json`.

### Gate your CI on regressions

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

The gate command reads the scorecard, compares against any baseline or allowlist, and returns a pass/fail exit code.

### Scan HTML with cryptographic provenance

```bash
npm install -g @accessibility-suite/evidence-engine
a11y-engine scan ./html --out ./results
```

The evidence engine scans HTML files and emits findings with prov-spec provenance records -- each finding carries a SHA-256 integrity digest.

### Get fix guidance for a finding

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

The assist tool generates remediation guidance tuned to one of five accessibility profiles: low-vision, screen-reader, dyslexia, cognitive-load, or standard.

### Capture evidence and diagnose via MCP

```bash
npm install -g @accessibility-suite/mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

## Option B: Install from source (developer mode)

If you want to contribute or modify the tools, clone the monorepo and use editable installs:

```bash
git clone https://github.com/mcp-tool-shop-org/accessibility-suite.git
cd accessibility-suite

# Install Python tools as editable
pip install -e src/a11y-lint
pip install -e src/a11y-ci
pip install -e src/a11y-assist

# Install Node tools
cd src/a11y-evidence-engine && npm install && cd ../..
cd src/a11y-mcp-tools && npm install && cd ../..
```

## Your first end-to-end run

The demo site provides a ready-made example with intentional accessibility violations. This is the fastest way to see all the tools working together:

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

This script runs the full pipeline: scan, gate, evidence capture, and comment generation. Inspect the `.a11y_artifacts/` directory afterward to see all the outputs.

## What to read next

- [Architecture](/accessibility-suite/handbook/architecture/) explains how the tools connect and how data flows between them
- [Tools](/accessibility-suite/handbook/tools/) provides a detailed guide to each tool
- [CI Integration](/accessibility-suite/handbook/ci-integration/) shows how to drop the gate into GitHub Actions
