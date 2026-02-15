# a11y-assist Handbook

Deterministic assistance for fixing accessibility failures. Think: “given a known failure signature, suggest safe remediation steps.”

## Quickstart

**Install**
```bash
pip install -e src/a11y-assist
```

**Run**
```bash
a11y-assist help --rule "aria-required"
```

**Output**
* Markdown remediation guide (stdout)

## How it fits

* `a11y-ci` tells you what failed and links to `docs/hints`
* `a11y-assist` can turn that into guided remediation (rules-based, deterministic)

## Recommended workflow

1. Run `a11y-ci gate` and inspect `report.txt`
2. Use `help_url` / `help_hint` fields to locate the rule
3. Use `a11y-assist` for structured guidance (when available)

**(More detail to be added once CLI is confirmed)**
