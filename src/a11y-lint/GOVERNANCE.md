# Project Governance

a11y-lint is maintained with a bias toward stability.

---

## Decision Principles

1. Accessibility > aesthetics
2. Determinism > cleverness
3. Clarity > terseness
4. Humans under stress are the primary user

---

## What We Protect

The following are considered stable public interfaces:

- **CLI output contract**: `[OK]/[WARN]/[ERROR]` + `What/Why/Fix` structure
- **JSON schema**: `cli.error.schema.v0.1.json`
- **Exit codes**: 0 = clean, 1 = errors found

Changes to these require major version bumps and community discussion.

---

## What May Change

- New rules may be added
- Rule descriptions may be clarified
- Internal implementation details
- Performance optimizations

---

## Versioning

- **Patch** (0.1.x): Bug fixes, rule tuning
- **Minor** (0.x.0): New rules, new outputs
- **Major** (x.0.0): Contract or schema changes

---

## Accessibility Regressions

Accessibility regressions are treated as release blockers.

A change that makes output less accessible is a bug, not a feature.

---

## Maintainers

Final authority rests with the project maintainer(s).

Decisions prioritize the needs of users with disabilities over convenience of contributors.
