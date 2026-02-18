# Accessibility Suite Handbook

A comprehensive guide to the Accessibility Suite: architecture, integration patterns, and development workflows.

---

## Table of Contents

- [The Problem](#the-problem)
- [Suite Architecture](#suite-architecture)
- [Project Deep Dives](#project-deep-dives)
  - [a11y-lint](#a11y-lint)
  - [a11y-ci](#a11y-ci)
  - [a11y-assist](#a11y-assist)
  - [a11y-evidence-engine](#a11y-evidence-engine)
  - [a11y-mcp-tools](#a11y-mcp-tools)
  - [a11y-demo-site](#a11y-demo-site)
- [Evidence-Based Testing](#evidence-based-testing)
- [CI Integration Patterns](#ci-integration-patterns)
- [MCP Integration Guide](#mcp-integration-guide)
- [Development Setup](#development-setup)
- [FAQ](#faq)

---

## The Problem

Accessibility testing today has three systemic gaps:

**1. Detection without proof.** Most scanners report violations but provide no verifiable evidence that a scan actually ran, what it tested, or whether the results were tampered with. When auditors or compliance teams ask "prove you tested this," teams have nothing but screenshots and trust.

**2. Remediation without context.** Violation reports list rule IDs and WCAG criteria, but rarely explain *why* a violation matters in terms a developer can act on. The gap between "WCAG 1.1.1 failure" and "add an alt attribute describing the chart's trend line" is where most remediation stalls.

**3. Output that fails its own test.** CLI tools that test for accessibility frequently produce inaccessible output themselves -- error messages with no structure, color-only status indicators, jargon-heavy text that screen readers cannot parse. The tools meant to improve accessibility create new barriers.

The Accessibility Suite addresses all three: findings carry cryptographic provenance, fix guidance is tuned per disability profile, and every tool's own output follows the low-vision-first contract.

---

## Suite Architecture

### The Six Tools

The suite is organized as a monorepo containing six projects that span the full accessibility testing lifecycle:

```
accessibility-suite/
  src/
    a11y-lint/              Python   Scan CLI text for accessible patterns
    a11y-ci/                Python   Gate CI pipelines on scorecards
    a11y-assist/            Python   Generate fix guidance (5 profiles)
    a11y-evidence-engine/   Node.js  Scan HTML with provenance
    a11y-mcp-tools/         Node.js  MCP server for AI integration
  examples/
    a11y-demo-site/         HTML     End-to-end demo
  docs/
    prov-spec/              Spec     Provenance specification
```

### How They Connect

The tools are designed to work independently or together. Here is the typical end-to-end flow:

**Path A: CLI text linting (Python tools)**

```
CLI output --> a11y-lint (scan) --> scorecard.json --> a11y-ci (gate) --> pass/fail
                                                                    --> PR comment
                                        |
                                        v
                                  a11y-assist (explain) --> fix guidance
```

1. Your tool produces CLI output (error messages, help text, logs).
2. `a11y-lint` scans the text against accessibility rules (line length, color-only, plain language, etc.) and produces a JSON scorecard.
3. `a11y-ci` consumes the scorecard, checks thresholds, detects regressions against a baseline, and either passes or fails the build.
4. `a11y-assist` takes structured findings (or raw text) and generates fix guidance in one of five accessibility profiles.

**Path B: HTML evidence scanning (Node.js tools)**

```
HTML files --> a11y-evidence-engine (scan) --> findings.json + provenance/
                                                    |
                                              a11y-mcp-tools
                                              (evidence + diagnose)
                                                    |
                                              a11y-assist (ingest)
                                                    |
                                              advisories.json
```

1. `a11y-evidence-engine` scans HTML files for WCAG violations (missing lang, missing alt, missing labels, missing accessible names).
2. Each finding is paired with a prov-spec provenance record containing SHA-256 digests over canonicalized evidence.
3. `a11y-mcp-tools` exposes evidence capture and diagnosis as MCP tools, allowing AI assistants to participate in the workflow.
4. `a11y-assist` can ingest the findings and produce fix-oriented advisories with provenance verification.

### Shared Contracts

All tools share a small set of contracts:

| Contract | Purpose |
|----------|---------|
| `cli.error.schema.v0.1.json` | Structured error format (`level`, `code`, `what`, `why`, `fix`) |
| `scorecard.schema.json` | Scorecard format for CI gating |
| `evidence.bundle.schema.v0.1.json` | Evidence bundles with artifact digests |
| `envelope.schema.v0.1.json` | MCP request/response envelope |
| `.a11y_artifacts/` directory | Unified artifact layout for CI |
| prov-spec method IDs | Stable versioned identifiers for provenance steps |

---

## Project Deep Dives

### a11y-lint

**Location:** `src/a11y-lint/`
**Language:** Python 3.10+
**Install:** `pip install a11y-lint`
**CLI entry point:** `a11y-lint`

The linter scans CLI text output for accessible error message patterns. It checks whether error messages follow the `[OK]/[WARN]/[ERROR] + What/Why/Fix` structure and flags issues like color-only information, excessive line length, all-caps text, jargon, and missing punctuation.

**Rule categories:**

- **WCAG rules** map to specific success criteria. Currently: `no-color-only` (WCAG SC 1.4.1).
- **Policy rules** enforce best practices for cognitive accessibility: `line-length`, `no-all-caps`, `plain-language`, `emoji-moderation`, `punctuation`, `error-structure`, `no-ambiguous-pronouns`.

**Key commands:**

| Command | Purpose |
|---------|---------|
| `a11y-lint scan <file>` | Scan a file for accessibility issues |
| `a11y-lint scan --stdin` | Scan from standard input |
| `a11y-lint scorecard <file>` | Generate a scorecard with grades |
| `a11y-lint report <file>` | Generate a markdown report |
| `a11y-lint validate <file>` | Validate JSON against the error schema |
| `a11y-lint list-rules` | Show available rules |

**Python API:**

```python
from a11y_lint import scan, Scanner, create_scorecard

messages = scan("ERROR: It failed")
scanner = Scanner()
scanner.disable_rule("line-length")
card = create_scorecard(messages)
```

**Design decisions:**

- Grades (A-F) are informational summaries, not CI gates. Gate on exit codes and rule failures.
- The `--strict` flag promotes warnings to errors for teams that want tighter enforcement.
- Respects `NO_COLOR` and `FORCE_COLOR` environment variables per the [no-color.org](https://no-color.org/) standard.

---

### a11y-ci

**Location:** `src/a11y-ci/`
**Language:** Python 3.10+
**Install:** `pip install a11y-ci` (Python) or `npm install @mcptoolshop/a11y-ci` (npm wrapper)
**CLI entry point:** `a11y-ci`

The CI gate consumes scorecards produced by `a11y-lint` and enforces quality thresholds. It supports baseline regression detection, severity-based gating, temporary allowlists with mandatory expiration dates, and PR comment generation for GitHub and Azure DevOps.

**Gate logic:**

1. Parse the current scorecard and (optionally) a baseline scorecard.
2. Fail if any finding meets or exceeds the `--fail-on` severity (default: `serious`).
3. Fail if serious/critical finding count increases from baseline.
4. Fail if new finding IDs appear (even if total count is stable).
5. Fail if any allowlist entry has expired.

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Gate passed |
| 2 | Input error (missing file, invalid schema) |
| 3 | Gate failed (threshold exceeded or regression) |

**MCP evidence emission:**

```bash
a11y-ci gate --current score.json --emit-mcp --mcp-out evidence.json
a11y-ci comment --mcp evidence.json --platform github > comment.md
```

This separates data generation from presentation, allowing the same evidence bundle to render as a GitHub PR comment, an Azure DevOps comment, or a machine-readable report.

**Allowlists:**

Temporary suppressions require a `finding_id`, an `expires` date (ISO 8601), and a `reason` (minimum 10 characters). Expired entries fail the gate -- there are no permanent exceptions.

---

### a11y-assist

**Location:** `src/a11y-assist/`
**Language:** Python 3.10+
**Install:** `pip install a11y-assist`
**CLI entry points:** `a11y-assist`, `assist-run`

The assistant takes structured errors or raw CLI text and generates fix guidance tailored to five accessibility profiles. It is non-interactive and deterministic: it never rewrites tool output, only adds an `ASSIST` block.

**Five profiles:**

| Profile | Audience | Key adaptations |
|---------|----------|-----------------|
| `lowvision` (default) | Low-vision users | Clear labels, numbered steps (max 5), SAFE commands |
| `cognitive-load` | ADHD, autism, anxiety | Max 3 steps, First/Next/Last labels, goal orientation |
| `screen-reader` | TTS/braille users | Spoken-friendly headers, expanded abbreviations, no visual references |
| `dyslexia` | Dyslexic users | Reduced reading friction, explicit labels, no symbolic emphasis |
| `plain-language` | Maximum clarity | One clause per sentence, simplified structure |

**Confidence levels:**

| Level | Trigger |
|-------|---------|
| High | Validated `cli.error.v0.1` JSON with error ID |
| Medium | Raw text with detectable `(ID: ...)` pattern |
| Low | Best-effort parse, no ID found |

**Safety contract:**

- Only SAFE commands are suggested (read-only, dry-run, diagnostic)
- Never invents error IDs
- No network calls
- Never rewrites original output

**Usage patterns:**

```bash
# From structured JSON (best)
a11y-assist explain --json error.json --profile screen-reader

# From raw CLI output (fallback)
some-tool do-thing 2>&1 | a11y-assist triage --stdin

# Wrapper mode
assist-run some-tool do-thing
a11y-assist last
```

---

### a11y-evidence-engine

**Location:** `src/a11y-evidence-engine/`
**Language:** Node.js 18+
**Install:** `npm install -g @mcptoolshop/a11y-evidence-engine`
**CLI entry point:** `a11y-engine`

The evidence engine scans HTML files for WCAG violations and produces findings with full prov-spec provenance chains. Unlike typical scanners, every finding includes cryptographically verifiable evidence: the exact content that was tested, a SHA-256 digest over the canonicalized evidence, and a provenance record documenting the extraction method.

**Rules (v0.1):**

| Rule ID | WCAG | Description |
|---------|------|-------------|
| `html.document.missing_lang` | 3.1.1 | Missing `lang` attribute on `<html>` |
| `html.img.missing_alt` | 1.1.1 | Missing `alt` attribute on `<img>` |
| `html.form_control.missing_label` | 1.3.1 | Form control missing associated label |
| `html.interactive.missing_name` | 4.1.2 | Interactive element missing accessible name |

**Output structure:**

```
results/
  findings.json
  provenance/
    finding-0001/
      record.json      # engine.extract.evidence.json_pointer
      digest.json       # integrity.digest.sha256
      envelope.json     # adapter.wrap.envelope_v0_1
```

**Key properties:**

- Pure static analysis -- no browser, no network, no headless Chrome
- Deterministic: identical input always produces identical output
- Uses htmlparser2 for parsing (lightweight, no native dependencies)
- Exit code 2 when findings exist at `error` severity

---

### a11y-mcp-tools

**Location:** `src/a11y-mcp-tools/`
**Language:** Node.js 18+
**Install:** `npm install -g @mcptoolshop/a11y-mcp-tools`
**CLI entry points:** `a11y` (CLI), `a11y-mcp` (MCP server)

MCP tools that expose accessibility evidence capture and diagnosis to AI assistants via the Model Context Protocol. This is the bridge between the suite's scanning capabilities and AI-powered remediation workflows.

**Two tools:**

| Tool | Purpose |
|------|---------|
| `a11y.evidence` | Capture tamper-evident evidence bundles (canonical HTML, DOM snapshots, SHA-256 digests, prov-spec records) |
| `a11y.diagnose` | Run WCAG 2.2 AA rule checks over evidence bundles with optional provenance verification |

**CLI usage:**

```bash
# Capture evidence
a11y evidence --target page.html --dom-snapshot --out evidence.json

# Diagnose with provenance verification
a11y diagnose --bundle evidence.json --verify-provenance --fix

# Pipe capture into diagnosis
a11y evidence --target page.html --dom-snapshot | a11y diagnose --fix
```

**MCP server:**

```bash
a11y-mcp
```

The server communicates over stdio using the MCP envelope format (v0.1). Configure your MCP client to point at the `a11y-mcp` binary.

**Provenance method IDs:**

Every operation is tracked with a stable, versioned method ID:

| Method | Description |
|--------|-------------|
| `engine.capture.html_canonicalize_v0_1` | HTML capture with attribute sorting and whitespace normalization |
| `engine.capture.dom_snapshot_v0_1` | DOM snapshot as flat node array |
| `engine.diagnose.wcag_rules_v0_1` | WCAG rule evaluation |
| `engine.extract.evidence.json_pointer_v0_1` | JSON Pointer evidence extraction (RFC 6901) |
| `adapter.integrity.sha256_v0_1` | SHA-256 integrity verification |
| `adapter.wrap.envelope_v0_1` | MCP envelope wrapping |
| `adapter.provenance.record_v0_1` | Provenance record creation |

See [PROV_METHODS_CATALOG.md](src/a11y-mcp-tools/PROV_METHODS_CATALOG.md) for the full catalog.

**Exit codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Findings exist |
| 3 | Capture/validation failure |
| 4 | Provenance verification failed (digest mismatch) |

---

### a11y-demo-site

**Location:** `examples/a11y-demo-site/`
**Language:** HTML + shell scripts

A minimal demo site with intentional accessibility violations. It demonstrates the end-to-end pipeline: scan with the evidence engine, ingest findings with a11y-assist, verify provenance, and fail CI with evidence.

**Intentional bugs in the demo HTML:**

- `<html>` missing `lang` attribute
- `<img>` missing `alt` attribute
- `<button>` missing accessible name
- `<a>` (empty link) missing accessible name
- `<input>` missing associated label

**Running the demo:**

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

The script runs the evidence engine, pipes findings into a11y-assist for advisory generation, and verifies provenance. When provenance verification passes, the output includes `Provenance: VERIFIED`.

---

## Evidence-Based Testing

### What Is prov-spec?

[prov-spec](https://github.com/mcp-tool-shop-org/prov-spec) is a provenance specification that defines how tools record what they did, what they consumed, and what they produced. The Accessibility Suite uses prov-spec to make every finding independently verifiable.

### Why Provenance Matters

Traditional scanners produce a list of violations. If someone asks "did you actually test that page?" or "has this report been modified?", there is no way to answer from the report alone.

With prov-spec provenance, each finding includes:

1. **An evidence record** (`engine.extract.evidence.json_pointer`) documenting exactly what content was extracted and from where.
2. **An integrity digest** (`integrity.digest.sha256`) -- a SHA-256 hash over the canonicalized evidence. Recomputing the hash and comparing it to the stored value proves the evidence has not been tampered with.
3. **An envelope** (`adapter.wrap.envelope_v0_1`) wrapping the finding in a standard format with metadata about the tool, version, and timestamp.

### Verification Flow

```bash
# Scan and capture evidence with provenance
a11y-engine scan ./html --out ./results

# Later: verify provenance is intact
a11y diagnose --bundle evidence.json --verify-provenance
```

Verification recomputes the SHA-256 digest from the canonicalized evidence and compares it to the stored digest. A match proves integrity. A mismatch (exit code 4) means the evidence was altered after capture.

**Important:** Provenance proves *integrity* (the evidence was not modified). It does not prove *trustworthiness* of the original scan environment. A compromised CI runner could produce fabricated evidence with valid digests. Provenance is one layer in a defense-in-depth strategy.

### Canonical Evidence

The evidence engine canonicalizes HTML before hashing: attributes are sorted alphabetically, whitespace is normalized, and the output is deterministic. This means the same HTML file always produces the same digest, regardless of attribute ordering or formatting differences.

---

## CI Integration Patterns

### Pattern 1: Basic Quality Gate (GitHub Actions)

Fail the build if serious or critical accessibility violations exist:

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan
        run: |
          pip install a11y-lint
          mkdir -p .a11y_artifacts
          a11y-lint scan . --artifact-dir .a11y_artifacts

      - uses: mcp-tool-shop-org/accessibility-suite/.github/actions/a11y-ci@main
        with:
          artifact-dir: .a11y_artifacts
          fail-on: serious
```

### Pattern 2: Regression Detection with Baseline

Fail only when accessibility gets worse, not when pre-existing issues exist:

```yaml
      - name: Gate with baseline
        run: |
          pip install a11y-ci
          a11y-ci gate \
            --current .a11y_artifacts/current.scorecard.json \
            --baseline baseline/a11y.scorecard.json
```

Commit your baseline scorecard to the repo. The gate fails if:
- The count of serious/critical findings increases
- New finding IDs appear (even if total count is stable)

### Pattern 3: Evidence + PR Comment

Generate a provenance-backed evidence bundle and render a PR comment:

```yaml
      - name: Gate with evidence
        run: |
          a11y-ci gate \
            --current .a11y_artifacts/current.scorecard.json \
            --emit-mcp --mcp-out .a11y_artifacts/evidence.json

      - name: PR comment
        if: github.event_name == 'pull_request'
        run: |
          a11y-ci comment \
            --mcp .a11y_artifacts/evidence.json \
            --platform github > comment.md
          gh pr comment ${{ github.event.number }} --body-file comment.md
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Pattern 4: HTML Scanning with Provenance

Scan HTML files and upload evidence as a build artifact:

```yaml
      - name: Scan HTML
        run: |
          npm install -g @mcptoolshop/a11y-evidence-engine
          a11y-engine scan ./html --out ./results

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: a11y-results
          path: results/
```

### Pattern 5: Azure DevOps

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

### Unified Artifact Directory

All tools default to `.a11y_artifacts/` as the output directory:

```
.a11y_artifacts/
  evidence/
    a11y-lint.json          # Structured findings (cli.error.v0.1)
    a11y-gate.json          # Gate decision
    provenance.json         # Build provenance
  reports/
    a11y-report.md          # Human-readable summary
    pr-comment.md           # PR comment content
  logs/
    a11y-lint.log
    a11y-ci.log
```

Publish the entire directory as a build artifact for audit trails and debugging.

---

## MCP Integration Guide

### What Is MCP?

The Model Context Protocol (MCP) is a standard for AI assistants to interact with external tools. The Accessibility Suite exposes its scanning and diagnosis capabilities as MCP tools, allowing AI assistants to capture evidence, run checks, and suggest fixes within the assistant's conversation.

### Server Setup

Install and start the MCP server:

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y-mcp
```

Or run without installing:

```bash
npx @mcptoolshop/a11y-mcp-tools
```

### Client Configuration

Add to your MCP client's configuration file:

**Claude Desktop / Cursor / VS Code:**

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

### Available Tools

**`a11y.evidence`** -- Capture an evidence bundle from an HTML file:

```json
{
  "input": {
    "targets": [{ "kind": "file", "path": "index.html" }],
    "capture": {
      "html": { "canonicalize": true },
      "dom": { "snapshot": true }
    }
  }
}
```

**`a11y.diagnose`** -- Run WCAG checks over an evidence bundle:

```json
{
  "input": {
    "bundle": { "...evidence bundle..." },
    "options": {
      "verify_provenance": true,
      "fix": true
    }
  }
}
```

### Envelope Format

All MCP communication uses the envelope format (v0.1):

```json
{
  "mcp": {
    "envelope": "mcp.envelope_v0_1",
    "request_id": "req_01HR9Y6GQ7V8WQ0K8N9K",
    "tool": "a11y.evidence",
    "ok": true
  },
  "result": { "..." }
}
```

Error responses include a `code`, `message`, and `fix` field following the same What/Why/Fix structure as the CLI tools.

---

## Development Setup

### Prerequisites

- **Python 3.10+** for a11y-lint, a11y-ci, and a11y-assist
- **Node.js 18+** for a11y-evidence-engine and a11y-mcp-tools
- **pip** and **npm** for package management

### Clone and Install

```bash
git clone https://github.com/mcp-tool-shop-org/accessibility-suite.git
cd accessibility-suite
```

**Python tools (editable install):**

```bash
pip install -e src/a11y-lint[dev]
pip install -e src/a11y-ci[dev]
pip install -e src/a11y-assist[dev]
```

**Node.js tools:**

```bash
cd src/a11y-evidence-engine && npm install && cd ../..
cd src/a11y-mcp-tools && npm install && cd ../..
```

### Running Tests

**Python tools:**

```bash
cd src/a11y-lint && pytest
cd src/a11y-ci && pytest
cd src/a11y-assist && pytest
```

**Node.js tools:**

```bash
cd src/a11y-evidence-engine && npm test
cd src/a11y-mcp-tools && npm test
```

### Linting

**Python:**

```bash
cd src/a11y-lint && ruff check .
cd src/a11y-ci && ruff check .
cd src/a11y-assist && ruff check .
```

### Project Structure Notes

This is a multi-language monorepo. Each sub-project manages its own dependencies:

- Python projects use `pyproject.toml` with setuptools
- Node.js projects use `package.json` with no bundler (plain Node.js)
- There is no top-level build system or workspace linkage -- each project is independently installable and publishable
- The root `package.json` is metadata only (name, version, keywords) and is not used for dependency management

### Schemas

JSON schemas are co-located with their tools:

| Schema | Location |
|--------|----------|
| CLI error format | `src/a11y-lint/a11y_lint/schemas/cli.error.schema.v0.1.json` |
| Scorecard | `src/a11y-ci/a11y_ci/schema/scorecard.schema.json` |
| Allowlist | `src/a11y-ci/a11y_ci/schemas/allowlist.schema.json` |
| MCP envelope | `src/a11y-mcp-tools/src/schemas/envelope.schema.v0.1.json` |
| Evidence bundle | `src/a11y-mcp-tools/src/schemas/evidence.bundle.schema.v0.1.json` |
| Diagnosis | `src/a11y-mcp-tools/src/schemas/diagnosis.schema.v0.1.json` |
| Tool requests/responses | `src/a11y-mcp-tools/src/schemas/tools/*.json` |

---

## FAQ

**Q: Do I need to install all six tools?**

No. Each tool is independently installable. Use `a11y-lint` alone for CLI text linting, `a11y-evidence-engine` alone for HTML scanning, or any combination that fits your workflow.

**Q: Does the evidence engine require a browser?**

No. It uses pure static HTML parsing via htmlparser2. No headless browser, no Puppeteer, no Playwright.

**Q: What WCAG version does the suite target?**

The evidence engine and MCP tools check against WCAG 2.2 AA criteria. The linter checks CLI-specific accessibility patterns (some map to WCAG, others are policy rules).

**Q: Can I use a11y-ci with tools other than a11y-lint?**

Yes. The CI gate consumes any JSON scorecard that conforms to the scorecard schema. You can produce scorecards from other tools as long as they include the required `meta` and `findings` fields.

**Q: What does "SAFE-only" mean in a11y-assist?**

SAFE commands are read-only, dry-run, or diagnostic operations that cannot modify state. a11y-assist will never suggest destructive commands. This is enforced at the profile rendering layer.

**Q: How do allowlists prevent permanent exceptions?**

Every allowlist entry requires an `expires` date. When the date passes, the entry becomes a gate failure instead of a suppression. There is no way to create a permanent allowlist entry.

**Q: Can AI assistants use the suite?**

Yes. Install `@mcptoolshop/a11y-mcp-tools` and configure your MCP client. The AI assistant can then capture evidence from HTML files, run WCAG checks, and receive fix guidance -- all within the conversation.

**Q: What is the relationship between a11y-evidence-engine and a11y-mcp-tools?**

The evidence engine is a standalone CLI scanner. The MCP tools package wraps similar scanning and diagnosis capabilities into MCP-compatible tools with envelope formatting, schema validation, and provenance method tracking. They share rule logic but serve different integration points (CLI vs. MCP).

**Q: How do I add a new rule?**

For **a11y-lint**: add a check function in `a11y_lint/scan_cli_text.py`, register it in the scanner, and add tests.

For **a11y-evidence-engine**: add a rule module in `src/rules/`, register it in `src/rules/index.js`, and add test fixtures in `fixtures/bad/`.

For **a11y-mcp-tools**: rules are shared with the evidence engine. Add the rule there and it becomes available through both the CLI and MCP interfaces.

**Q: Where should I file issues?**

All issues go to the monorepo: [github.com/mcp-tool-shop-org/accessibility-suite/issues](https://github.com/mcp-tool-shop-org/accessibility-suite/issues). The original standalone repositories have been archived.
