---
title: Architecture
description: How the Accessibility Suite monorepo is organized and how data flows between tools.
sidebar:
  order: 2
---

The Accessibility Suite is a monorepo containing six tools that form a pipeline from detection through remediation. This page explains the repo structure, the data flow between tools, and the shared contracts that keep everything consistent.

## Monorepo layout

```
accessibility-suite/
  src/
    a11y-lint/            # Python -- scanner/linter
    a11y-ci/              # Python -- CI gate
    a11y-assist/          # Python -- fix guidance
    a11y-evidence-engine/ # Node.js -- HTML scanner with provenance
    a11y-mcp-tools/       # Node.js -- MCP server
  examples/
    a11y-demo-site/       # HTML demo with intentional violations
  docs/
    handbooks/            # Source handbooks (you're reading the Starlight version)
    prov-spec/            # Provenance specification
    unified-artifacts.md  # Artifact directory strategy
  .github/
    workflows/            # CI pipelines
    actions/              # Composite actions (a11y-ci gate)
```

## Pipeline flow

The six tools form a pipeline. Each tool produces structured output that the next tool consumes:

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

### Step by step

1. **a11y-lint** scans CLI text (error messages, log output, user-facing strings) for accessible error message patterns. It produces a scorecard JSON file summarizing what it found.
2. **a11y-evidence-engine** scans HTML files and emits findings with prov-spec provenance records. Each finding carries a SHA-256 integrity digest so you can verify it was not tampered with.
3. **a11y-ci** consumes scorecards from a11y-lint, enforces severity thresholds, detects regressions against a stored baseline, applies allowlist waivers, and generates both human-readable reports and PR comment markdown.
4. **a11y-mcp-tools** wraps evidence capture and diagnosis as MCP tools so AI assistants (Claude Desktop, Cursor, VS Code) can participate in the remediation loop.
5. **a11y-assist** takes findings -- either structured JSON from the pipeline or raw text -- and generates fix guidance in five accessibility profiles (low-vision, screen-reader, dyslexia, cognitive-load, standard).
6. **a11y-demo-site** ties everything together as a runnable example with intentional violations for end-to-end testing.

## The golden folder: `.a11y_artifacts/`

All tools write their outputs to a shared artifact directory called `.a11y_artifacts/`. This convention ensures CI pipelines, MCP integrations, and human reviewers all look in the same place.

```
.a11y_artifacts/
  current.scorecard.json     # produced by a11y-lint
  baseline.scorecard.json    # optional -- stored by CI baseline workflow
  allowlist.json             # optional -- expiring suppressions (waivers)
  gate-result.json           # produced by a11y-ci (structured report)
  report.txt                 # produced by a11y-ci (human-readable report)
  evidence.json              # produced by a11y-ci (MCP evidence bundle)
  comment.md                 # produced by a11y-ci (PR comment markdown)
  result.json                # produced by a11y-lint (detailed scanner results)
```

## Shared contracts

The tools communicate through well-defined schemas and conventions:

- **`cli.error.schema.v0.1.json`** -- structured error format shared across all Python tools. Every error has a code, message, and hint.
- **`evidence.bundle.schema.v0.1.json`** -- the shape of evidence bundles with provenance chains, used by a11y-ci and a11y-mcp-tools.
- **prov-spec method IDs** -- stable, versioned identifiers for every provenance step. These ensure that provenance records can be verified across tool versions.

## Design principles

- **Evidence over assertions** -- every finding is backed by a provenance record with SHA-256 integrity digests. You can independently verify any claim.
- **Low-vision-first output** -- all CLI tools use the `[OK]/[WARN]/[FAIL] + What/Why/Fix` contract. Output is designed for humans first.
- **Deterministic** -- same input always produces identical output. No network calls, no randomness.
- **CI-native** -- exit codes, scorecard JSON, and PR comments are designed for automated pipelines from the start.
