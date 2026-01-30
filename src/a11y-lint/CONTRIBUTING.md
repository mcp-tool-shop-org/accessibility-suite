# Contributing to a11y-lint

Thank you for helping improve accessibility tooling.

Before contributing, please understand the core rule:

> **Accessibility behavior is a public API.**

---

## Non-Negotiables

- Do not change the CLI output contract without discussion
- Do not weaken accessibility rules for convenience
- All new rules must include:
  - a clear problem statement
  - why it affects accessibility
  - a concrete fix

---

## Adding a Rule

Rules must be deterministic and testable.

Each rule must:
- operate on plain text
- produce actionable output
- include tests with good and bad fixtures

---

## Rule Categories

When adding a rule, classify it correctly:

- **WCAG**: Mapped to a specific WCAG success criterion (e.g., SC 1.4.1)
- **Policy**: Best practice for cognitive accessibility, not a WCAG violation

Policy rules are intentional and valuable — but should not be conflated with WCAG requirements.

---

## Tests

All contributions must include tests.
Behavior without tests will not be merged.

Run tests with:

```bash
pytest tests/ -v
```

---

## Tone

This project is strict, not judgmental.

Output should explain *what*, *why*, and *how to fix* — never shame.

---

## Pull Requests

- Keep PRs focused on a single change
- Include test coverage for new behavior
- Update documentation if behavior changes
- Ensure all tests pass before submitting
