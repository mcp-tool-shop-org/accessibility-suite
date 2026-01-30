# Introducing a11y-lint
## Accessibility as a Contract for CLI Tools

Today we're releasing **a11y-lint**, an accessibility linter built specifically for command-line tools.

Most accessibility tooling focuses on web interfaces. But developers, operators, and data professionals spend much of their time in terminals — and terminal output is often inaccessible by default.

a11y-lint treats accessibility as a **hard interface**, not a suggestion.

---

## What a11y-lint Does

a11y-lint scans CLI output and enforces a strict, low-vision-first accessibility contract:

- Clear textual status indicators: `[OK]`, `[WARN]`, `[ERROR]`
- Deterministic error structure:
  - What happened
  - Why it happened
  - How to fix it
- No reliance on color, emojis, or visual tricks
- Machine-parseable output suitable for CI
- Human-readable output under stress

If output fails checks, a11y-lint explains **what's wrong and how to fix it**.

---

## Philosophy

Accessibility should not rely on memory, heroics, or good intentions.

It should be:
- explicit
- testable
- enforceable
- boring

That's what a11y-lint is for.

---

## Get Started

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

a11y-lint is open source and welcomes contributors who care about building tools that respect real humans.
