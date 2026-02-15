# a11y-evidence-engine Handbook

A headless engine that generates traceable, structured accessibility evidence (often beyond “a list of findings”), suitable for audits and verification.

## Quickstart

**Install**
```bash
pip install -e src/a11y-evidence-engine
```

**Run**
```bash
(Pending CLI finalization)
```

**Output**
* Screenshots (`.png`)
* DOM snapshots (`.html`)
* `.a11y_artifacts/evidence-manifest.json`

## Where it fits

* `a11y-lint`: findings
* `a11y-ci`: policy + regression + waivers
* `a11y-evidence-engine`: traceable “proof artifacts” (screenshots, DOM snapshots), depending on what it supports

## Best practice

* Store evidence artifacts under `.a11y_artifacts/` (or a subfolder like `.a11y_artifacts/evidence/`)
* Reference them from `evidence.json` so everything is linked and hashable
