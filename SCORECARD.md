# Scorecard

> Score a repo before remediation. Fill this out first, then use SHIP_GATE.md to fix.

**Repo:** accessibility-suite
**Date:** 2026-02-27
**Type tags:** [npm] [mcp] [cli] [complex]

## Pre-Remediation Assessment

| Category | Score | Notes |
|----------|-------|-------|
| A. Security | 5/10 | No SECURITY.md, no threat model in README |
| B. Error Handling | 8/10 | Structured error schema, exit codes, [OK]/[WARN]/[FAIL] contract |
| C. Operator Docs | 9/10 | Comprehensive README, HANDBOOK, GETTING_STARTED, CHANGELOG |
| D. Shipping Hygiene | 7/10 | CI exists, lockfile committed, but pre-1.0 version |
| E. Identity (soft) | 9/10 | Logo, translations, landing page, GitHub metadata all present |
| **Overall** | **38/50** | |

## Key Gaps

1. No SECURITY.md — no vulnerability reporting process
2. No threat model / Security & Data Scope in README
3. Version still at 0.2.2 — needs promotion to 1.0.0
4. Missing SHIP_GATE.md and SCORECARD.md for formal standards tracking

## Remediation Priority

| Priority | Item | Estimated effort |
|----------|------|-----------------|
| 1 | Create SECURITY.md + threat model in README | 5 min |
| 2 | Bump version to 1.0.0 + update CHANGELOG | 3 min |
| 3 | Add SHIP_GATE.md + SCORECARD.md via shipcheck init | 2 min |

## Post-Remediation

| Category | Before | After |
|----------|--------|-------|
| A. Security | 5/10 | 10/10 |
| B. Error Handling | 8/10 | 10/10 |
| C. Operator Docs | 9/10 | 10/10 |
| D. Shipping Hygiene | 7/10 | 10/10 |
| E. Identity (soft) | 9/10 | 10/10 |
| **Overall** | **38/50** | **50/50** |
