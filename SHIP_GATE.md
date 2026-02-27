# Ship Gate

> No repo is "done" until every applicable line is checked.
> Copy this into your repo root. Check items off per-release.

**Tags:** `[all]` every repo · `[npm]` `[pypi]` `[vsix]` `[desktop]` `[container]` published artifacts · `[mcp]` MCP servers · `[cli]` CLI tools

---

## A. Security Baseline

- [x] `[all]` SECURITY.md exists (report email, supported versions, response timeline) (2026-02-27)
- [x] `[all]` README includes threat model paragraph (data touched, data NOT touched, permissions required) (2026-02-27)
- [x] `[all]` No secrets, tokens, or credentials in source or diagnostics output (2026-02-27)
- [x] `[all]` No telemetry by default — state it explicitly even if obvious (2026-02-27)

### Default safety posture

- [x] `[cli|mcp|desktop]` Dangerous actions (kill, delete, restart) require explicit `--allow-*` flag (2026-02-27) — CLI tools are read-only analyzers; MCP tools write evidence bundles to user-specified dirs only
- [x] `[cli|mcp|desktop]` File operations constrained to known directories (2026-02-27) — artifacts scoped to .a11y_artifacts/ and user-specified output dirs
- [x] `[mcp]` Network egress off by default (2026-02-27) — deterministic, no network calls
- [x] `[mcp]` Stack traces never exposed — structured error results only (2026-02-27)

## B. Error Handling

- [x] `[all]` Errors follow the Structured Error Shape: `code`, `message`, `hint`, `cause?`, `retryable?` (2026-02-27) — cli.error.schema.v0.1.json
- [x] `[cli]` Exit codes: 0 ok · 1 user error · 2 runtime error · 3 partial success (2026-02-27)
- [x] `[cli]` No raw stack traces without `--debug` (2026-02-27) — [OK]/[WARN]/[FAIL] contract
- [x] `[mcp]` Tool errors return structured results — server never crashes on bad input (2026-02-27)
- [x] `[mcp]` State/config corruption degrades gracefully (stale data over crash) (2026-02-27) — evidence bundles are immutable
- [ ] `[desktop]` SKIP: not a desktop application
- [ ] `[vscode]` SKIP: not a VS Code extension

## C. Operator Docs

- [x] `[all]` README is current: what it does, install, usage, supported platforms + runtime versions (2026-02-27)
- [x] `[all]` CHANGELOG.md (Keep a Changelog format) (2026-02-27)
- [x] `[all]` LICENSE file present and repo states support status (2026-02-27)
- [x] `[cli]` `--help` output accurate for all commands and flags (2026-02-27)
- [x] `[cli|mcp|desktop]` Logging levels defined: silent / normal / verbose / debug — secrets redacted at all levels (2026-02-27)
- [x] `[mcp]` All tools documented with description + parameters (2026-02-27) — evidence and diagnose tools documented in README
- [x] `[complex]` HANDBOOK.md: daily ops, warn/critical response, recovery procedures (2026-02-27)

## D. Shipping Hygiene

- [x] `[all]` `verify` script exists (test + build + smoke in one command) (2026-02-27)
- [x] `[all]` Version in manifest matches git tag (2026-02-27)
- [x] `[all]` Dependency scanning runs in CI (ecosystem-appropriate) (2026-02-27)
- [x] `[all]` Automated dependency update mechanism exists (2026-02-27)
- [x] `[npm]` `npm pack --dry-run` includes: dist/, README.md, CHANGELOG.md, LICENSE (2026-02-27)
- [x] `[npm]` `engines.node` set · `[pypi]` `python_requires` set (2026-02-27)
- [x] `[npm]` Lockfile committed · `[pypi]` Clean wheel + sdist build (2026-02-27)
- [ ] `[vsix]` SKIP: not a VS Code extension
- [ ] `[desktop]` SKIP: not a desktop application

## E. Identity (soft gate — does not block ship)

- [x] `[all]` Logo in README header (2026-02-27)
- [x] `[all]` Translations (polyglot-mcp, 8 languages) (2026-02-27)
- [x] `[org]` Landing page (@mcptoolshop/site-theme) (2026-02-27)
- [x] `[all]` GitHub repo metadata: description, homepage, topics (2026-02-27)

---

## Gate Rules

**Hard gate (A–D):** Must pass before any version is tagged or published.
If a section doesn't apply, mark `SKIP:` with justification — don't leave it unchecked.

**Soft gate (E):** Should be done. Product ships without it, but isn't "whole."

**Checking off:**
```
- [x] `[all]` SECURITY.md exists (2026-02-27)
```

**Skipping:**
```
- [ ] `[pypi]` SKIP: not a Python project
```
