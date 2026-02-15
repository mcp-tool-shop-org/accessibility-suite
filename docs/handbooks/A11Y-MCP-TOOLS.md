# a11y-mcp-tools Handbook

An MCP server/tooling layer for capturing and transporting accessibility evidence bundles.

## Quickstart

**Install**
```bash
pip install -e src/a11y-mcp-tools
```

**Run**
```bash
mcp-server-a11y --evidence-dir .a11y_artifacts
```

**Input**
* `.a11y_artifacts/evidence.json`

**Output**
* MCP Resources (`a11y://evidence/...`)
* MCP Prompts

## Integration model

Treat `evidence.json` as the “source packet”:
* Store, index, or attach it to PR build artifacts
* **Prefer hash-verified artifacts** (`a11y-ci` includes SHA256 hashes)

## In practice

Most teams:
1. upload `.a11y_artifacts/` as CI artifacts
2. optionally forward `evidence.json` to MCP tools for aggregation
