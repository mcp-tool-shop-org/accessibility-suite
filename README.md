<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.npmjs.com/package/@mcptoolshop/accessibility-suite"><img src="https://img.shields.io/npm/v/@mcptoolshop/accessibility-suite" alt="npm"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

Six tools. One mission: make accessibility testing verifiable, automated, and hard to ignore.

---

## At a Glance

Most accessibility tools stop at "you have 12 violations." The Accessibility Suite goes further: it captures tamper-evident evidence of what was tested, gates your CI pipeline on regressions, and surfaces fix guidance tuned for low-vision, screen-reader, dyslexia, and cognitive-load profiles.

The suite spans the full lifecycle -- lint CLI output for accessible patterns, scan HTML for WCAG violations with cryptographic provenance, enforce quality gates in CI, and expose everything through MCP so AI assistants can participate in the remediation loop.

**Key principles:**

- **Evidence over assertions** -- every finding is backed by a prov-spec provenance record with SHA-256 integrity digests
- **Low-vision-first output** -- all CLI tools use the `[OK]/[WARN]/[FAIL] + What/Why/Fix` contract
- **Deterministic** -- same input always produces identical output; no network calls, no randomness
- **CI-native** -- exit codes, scorecard JSON, and PR comments designed for automated pipelines

---

## Projects

| Project | Description | Stack | Package |
|---------|-------------|-------|---------|
| [a11y-lint](src/a11y-lint/) | Accessibility linter for CLI output -- validates error messages follow accessible patterns | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | CI gate for accessibility scorecards with regression detection and allowlists | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | Low-vision-first CLI assistant with five accessibility profiles | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Headless HTML scanner with prov-spec provenance records | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | MCP server for accessibility evidence capture and diagnosis | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | Demo site with intentional violations for end-to-end testing | HTML | -- |

---

## Quick Start

### Lint CLI output for accessible patterns

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Gate your CI on accessibility regressions

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Scan HTML and capture provenance

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### Get fix guidance for a CLI failure

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Capture evidence and diagnose via MCP

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### Run the demo site end-to-end

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## Architecture

The six tools form a pipeline from detection through remediation:

```
                        CLI output                HTML files
                            |                         |
                    +-------v-------+        +--------v---------+
                    |   a11y-lint   |        | a11y-evidence-   |
                    | (scan & score)|        | engine (scan +   |
                    +-------+-------+        | provenance)      |
                            |                +--------+---------+
                  scorecard.json                      |
                            |               evidence bundle
                    +-------v-------+                 |
                    |    a11y-ci    |        +---------v---------+
                    |  (CI gate +  |        |  a11y-mcp-tools   |
                    |  PR comment) |        | (MCP evidence +   |
                    +-------+-------+        |  diagnosis)      |
                            |                +---------+---------+
                    pass / fail                        |
                            |                  findings + fixes
                    +-------v-------+                 |
                    |  a11y-assist  |<----------------+
                    | (fix guidance |
                    |  5 profiles)  |
                    +---------------+
```

**Data flow:**

1. **a11y-lint** scans CLI text for accessible error message patterns and produces a scorecard
2. **a11y-evidence-engine** scans HTML files and emits findings with prov-spec provenance records
3. **a11y-ci** consumes scorecards, enforces thresholds, detects regressions, and generates PR comments
4. **a11y-mcp-tools** wraps evidence capture and diagnosis as MCP tools for AI assistant integration
5. **a11y-assist** takes findings (structured JSON or raw text) and generates fix guidance in five accessibility profiles
6. **a11y-demo-site** ties it all together as a runnable example with intentional violations

**Shared contracts:**

- `cli.error.schema.v0.1.json` -- structured error format across all Python tools
- `evidence.bundle.schema.v0.1.json` -- evidence bundles with provenance chains
- `.a11y_artifacts/` -- unified artifact directory for CI pipelines
- prov-spec method IDs -- stable, versioned identifiers for every provenance step

---

## MCP Client Configuration

To connect a11y-mcp-tools to your MCP client (Claude Desktop, Cursor, VS Code, etc.):

```json
{
  "mcpServers": {
    "a11y": {
      "command": "npx",
      "args": ["-y", "@mcptoolshop/a11y-mcp-tools"]
    }
  }
}
```

Or if installed globally:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

The server exposes two tools:

| Tool | Description |
|------|-------------|
| `a11y.evidence` | Capture tamper-evident evidence bundles from HTML, CLI logs, or other inputs |
| `a11y.diagnose` | Run WCAG rule checks over evidence bundles with provenance verification |

---

## CI Integration (GitHub Actions)

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan code
        run: |
          pip install a11y-lint
          mkdir .a11y_artifacts
          a11y-lint scan . --artifact-dir .a11y_artifacts

      - uses: mcp-tool-shop-org/accessibility-suite/.github/actions/a11y-ci@main
        with:
          artifact-dir: .a11y_artifacts
          fail-on: serious
```

See [GETTING_STARTED.md](GETTING_STARTED.md) for Azure DevOps examples and troubleshooting.

---

## Documentation

| Document | Description |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Architecture deep dive, integration patterns, and development guide |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Three-command local setup, CI templates, and troubleshooting |
| [CHANGELOG.md](CHANGELOG.md) | Release history in Keep a Changelog format |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Unified artifact directory strategy |
| [docs/prov-spec/](docs/prov-spec/) | Provenance specification |

---

## Security & Data Scope

- **Data accessed:** Reads HTML files, CLI output, and scorecard JSON for accessibility analysis. Captures DOM snapshots and generates evidence bundles.
- **Data NOT accessed:** No network requests. No telemetry. No user data storage. No credentials or tokens.
- **Permissions required:** Read access to target files. Write access for evidence/artifact output directories.

## Scorecard

| Gate | Status |
|------|--------|
| A. Security Baseline | PASS |
| B. Error Handling | PASS |
| C. Operator Docs | PASS |
| D. Shipping Hygiene | PASS |
| E. Identity | PASS |

## License

[MIT](LICENSE)

---

Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
