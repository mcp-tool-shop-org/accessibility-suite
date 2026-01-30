# Release Notes

## v0.1.0 (2026-01-26)

First stable release of **a11y-lint**, a low-vision-first accessibility linter for command-line tools.

### Highlights

- **Stable CLI output contract**: `[OK] / [WARN] / [ERROR]` + `What / Why / Fix` structure
- **Ground-truth JSON schema**: `cli.error.schema.v0.1.json`
- **Low-vision-first rule set** covering:
  - Line length and spacing
  - Color-only meaning detection (WCAG SC 1.4.1)
  - Emoji-only signaling
  - Technical jargon
  - Ambiguous pronouns
  - Error message structure
- **Deterministic rendering** suitable for CI and diffing
- **Reports and scorecards** in Markdown format
- **176+ tests** with comprehensive coverage

### CLI Commands

- `a11y-lint scan` — Check CLI output for accessibility issues
- `a11y-lint validate` — Validate JSON messages against schema
- `a11y-lint scorecard` — Generate accessibility scorecard
- `a11y-lint report` — Generate Markdown report
- `a11y-lint list-rules` — Show available rules
- `a11y-lint schema` — Print JSON schema

### Rule Categories

Rules are classified as:
- **WCAG**: Mapped to WCAG success criteria (e.g., `no-color-only` → SC 1.4.1)
- **Policy**: Best practices for cognitive accessibility

### Stability Guarantees

- CLI output structure is **stable**
- JSON schema `cli.error.v0.1` is **frozen**
- Rule coverage may expand, but guarantees will not be weakened
- Breaking changes require a major version bump

### Environment Variables

- `NO_COLOR` — Disable colored output
- `FORCE_COLOR` — Force colored output

### Known Limitations

- Focused on CLI text output only
- Single accessibility profile (low vision)
- No AI-assisted suggestions in v0.1

---

This release establishes the foundation for accessible CLI tooling.
