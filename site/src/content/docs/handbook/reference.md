---
title: Reference
description: Full command reference, exit codes, error IDs, schemas, and shared conventions.
sidebar:
  order: 6
---

This page is the complete reference for all commands, options, exit codes, error identifiers, and schemas in the Accessibility Suite.

## Commands

### a11y-lint

| Command | Description |
|---------|-------------|
| `a11y-lint scan <path>` | Scan a file or directory for accessible error message patterns |
| `a11y-lint scan <path> --artifact-dir <dir>` | Scan and write outputs to the specified artifact directory |

### a11y-ci

| Command | Description |
|---------|-------------|
| `a11y-ci gate --artifact-dir <dir>` | Run the policy gate against scorecards in the artifact directory |
| `a11y-ci gate --artifact-dir <dir> --fail-on <level>` | Set the severity threshold (`minor`, `moderate`, `serious`) |
| `a11y-ci comment --mcp <evidence.json> --platform <platform>` | Generate a PR comment from an evidence bundle |
| `a11y-ci comment --mcp <evidence.json> --platform <platform> --top <n>` | Limit the comment to the top N findings |

### a11y-assist

| Command | Description |
|---------|-------------|
| `a11y-assist help --rule <rule-id>` | Get remediation guidance for a specific rule |
| `a11y-assist explain --json <file> --profile <profile>` | Explain a failure with profile-specific guidance |

**Profiles:** `standard`, `low-vision`, `screen-reader`, `dyslexia`, `cognitive-load`

### a11y-evidence-engine

| Command | Description |
|---------|-------------|
| `a11y-engine scan <path> --out <dir>` | Scan HTML files and emit evidence with provenance records |

### a11y-mcp-tools

| Command | Description |
|---------|-------------|
| `a11y-mcp` | Start the MCP server (default, for use with MCP clients) |
| `mcp-server-a11y --evidence-dir <dir>` | Start with a pre-existing evidence directory |

### MCP tools

| Tool | Description |
|------|-------------|
| `a11y.evidence` | Capture tamper-evident evidence bundles from HTML, CLI logs, or other inputs |
| `a11y.diagnose` | Run WCAG rule checks over evidence bundles with provenance verification |

## Exit codes

All CLI tools in the suite follow this exit code convention:

| Code | Meaning | When it happens |
|------|---------|----------------|
| `0` | Success / PASS | The operation completed successfully or the gate passed |
| `1` | Internal error | An unexpected error in the tool itself |
| `2` | Input error | Invalid scorecard schema, missing required file, unwritable directory |
| `3` | Gate failed | Policy violation, regression detected, or expired waiver (a11y-ci only) |

## Error IDs

Error IDs are standardized across the suite. They are grep-friendly and stable across versions. When reporting issues, include the error ID.

### a11y-lint errors

| Error ID | Meaning |
|----------|---------|
| `A11Y.SCAN.IO` | Input path does not exist or is not readable |
| `A11Y.SCAN.SCHEMA` | Output directory does not exist or is not writable |

### a11y-ci errors

| Error ID | Meaning |
|----------|---------|
| `A11Y.CI.Schema.Invalid` | Scorecard JSON is malformed or missing required fields |
| `A11Y.CI.Gate.Failed` | Open violations exceed the severity threshold |

## Schemas

### Scorecard schema (`current.scorecard.json`)

The scorecard is the primary data exchange format between a11y-lint and a11y-ci. It follows `cli.error.schema.v0.1.json`:

```json
{
  "meta": {
    "tool": "a11y-lint",
    "version": "1.0.0"
  },
  "findings": [
    {
      "id": "color-contrast",
      "severity": "serious",
      "message": "Element has insufficient color contrast ratio",
      "location": "src/components/Button.tsx:42"
    }
  ]
}
```

**Required fields:**

- `meta.tool` -- name of the tool that produced the scorecard
- `meta.version` -- version of the tool
- `findings[].id` -- unique identifier for the rule
- `findings[].severity` -- severity level (minor, moderate, serious, critical)
- `findings[].message` -- human-readable description

**Optional fields:**

- `findings[].location` -- file path and line number

### Evidence bundle schema (`evidence.json`)

The evidence bundle follows `evidence.bundle.schema.v0.1.json`. It extends the scorecard with provenance chains and integrity digests:

- Traceability metadata linking findings back to source artifacts
- SHA-256 hashes for each artifact (scorecard, screenshots, DOM snapshots)
- prov-spec method IDs identifying the provenance steps

### Allowlist schema (`allowlist.json`)

```json
[
  {
    "id": "color-contrast",
    "owner": "team-frontend",
    "expires": "2026-06-01",
    "ticket": "JIRA-1234"
  }
]
```

**Required fields:**

- `id` or `fingerprint` -- which finding to suppress
- `owner` -- who approved the waiver
- `expires` -- ISO date when the waiver expires

**Optional fields:**

- `ticket` -- reference to a tracking issue

## The artifact directory

All tools read from and write to `.a11y_artifacts/` by default. Here is the complete listing:

| File | Produced by | Description |
|------|-------------|-------------|
| `current.scorecard.json` | a11y-lint | Current scan results |
| `baseline.scorecard.json` | CI baseline workflow | Previous known-good state for regression detection |
| `allowlist.json` | Human-authored | Expiring suppressions (waivers) |
| `gate-result.json` | a11y-ci | Structured pass/fail result |
| `report.txt` | a11y-ci | Human-readable report |
| `evidence.json` | a11y-ci | Evidence bundle with provenance |
| `comment.md` | a11y-ci | PR comment markdown |
| `result.json` | a11y-lint | Detailed scanner results |
| `evidence-manifest.json` | a11y-evidence-engine | Manifest linking screenshots and DOM snapshots |

## Provenance

Every finding produced by the evidence engine carries a prov-spec provenance record. Provenance records use stable, versioned method IDs so you can verify them across tool versions. The SHA-256 integrity digests ensure that findings have not been tampered with after generation.

For the full provenance specification, see `docs/prov-spec/` in the repository.
