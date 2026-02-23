# accessibility-suite

Six tools. One mission: make accessibility testing verifiable, automated, and hard to ignore.

---

## Key Features

- **Evidence over assertions** -- every finding is backed by a prov-spec provenance record with SHA-256 integrity digests
- **Low-vision-first output** -- all CLI tools use the `[OK]/[WARN]/[FAIL] + What/Why/Fix` contract
- **Deterministic** -- same input always produces identical output; no network calls, no randomness
- **CI-native** -- exit codes, scorecard JSON, and PR comments designed for automated pipelines
- **MCP integration** -- expose evidence capture and diagnosis as MCP tools for AI assistants
- **Full lifecycle** -- lint, scan, gate, diagnose, and fix across CLI output and HTML

---

## Install

### Python tools

```bash
pip install a11y-lint a11y-ci a11y-assist
```

### Node.js tools

```bash
npm install -g @mcptoolshop/a11y-evidence-engine @mcptoolshop/a11y-mcp-tools
```

---

## Quick Start

```bash
# Lint CLI output for accessible patterns
a11y-lint scan output.txt

# Gate your CI on accessibility regressions
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts

# Scan HTML and capture provenance
a11y-engine scan ./html --out ./results

# Get fix guidance for a CLI failure
a11y-assist explain --json error.json --profile screen-reader
```

---

## Links

- [GitHub Repository](https://github.com/mcp-tool-shop-org/accessibility-suite)
- [MCP Tool Shop](https://mcp-tool-shop.github.io/)
- [Getting Started Guide](https://github.com/mcp-tool-shop-org/accessibility-suite/blob/main/GETTING_STARTED.md)
- [Changelog](https://github.com/mcp-tool-shop-org/accessibility-suite/blob/main/CHANGELOG.md)
