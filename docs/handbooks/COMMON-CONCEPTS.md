# Common Concepts

## The Golden Folder: `.a11y_artifacts/`

All tools agree on a shared artifact directory:

```plaintext
.a11y_artifacts/
  current.scorecard.json     # produced by a11y-lint (or scanners)
  baseline.scorecard.json    # optional, stored/managed by CI baseline workflow
  allowlist.json             # optional, expiring suppressions (waivers)
  gate-result.json           # produced by a11y-ci (structured report)
  report.txt                 # produced by a11y-ci (human report)
  evidence.json              # produced by a11y-ci (MCP evidence bundle)
  comment.md                 # produced by a11y-ci (PR comment markdown)
  result.json                # produced by a11y-lint (scanner result details)
```

## Typical pipeline flow

1. **Scan** → `a11y-lint` writes `current.scorecard.json`
2. **Gate** → `a11y-ci` gate reads it, compares baseline/allowlist, emits reports
3. **Evidence** → `evidence.json` is produced for traceability/MCP
4. **Comment** → `comment.md` generated for PR systems (GitHub/ADO)
