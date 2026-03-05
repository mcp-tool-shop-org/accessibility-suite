---
title: MCP Integration
description: Connect the Accessibility Suite to Claude Desktop, Cursor, VS Code, and other MCP clients.
sidebar:
  order: 4
---

The Accessibility Suite includes an MCP server (`a11y-mcp-tools`) that exposes accessibility evidence capture and WCAG diagnosis as tools for AI assistants. This page explains how to configure your MCP client to use it.

## What MCP provides

Once connected, your AI assistant gains two capabilities:

| Tool | What it does |
|------|-------------|
| `a11y.evidence` | Capture tamper-evident evidence bundles from HTML files, CLI logs, or other inputs. Each bundle includes DOM snapshots, screenshots, and SHA-256 integrity digests. |
| `a11y.diagnose` | Run WCAG rule checks over an evidence bundle with provenance verification. Returns findings with severity, rule IDs, and fix guidance. |

This means you can ask your AI assistant to scan a page, verify provenance, and suggest fixes -- all within a single conversation.

## Configuration

### Using npx (recommended)

Add this to your MCP client configuration file. This works with Claude Desktop, Cursor, VS Code, and any other MCP-compatible client:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "npx",
      "args": ["-y", "@accessibility-suite/mcp-tools"]
    }
  }
}
```

The `npx -y` flag ensures the package is installed automatically if it is not already present.

### Using a global install

If you have already installed the package globally:

```bash
npm install -g @accessibility-suite/mcp-tools
```

Then configure your MCP client with:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

### Pointing to an evidence directory

If you want the MCP server to start with a pre-existing evidence directory:

```bash
mcp-server-a11y --evidence-dir .a11y_artifacts
```

## Where to put the configuration

The configuration file location depends on your MCP client:

| Client | Config file |
|--------|------------|
| Claude Desktop | `claude_desktop_config.json` (Settings > Developer > Edit Config) |
| Cursor | `.cursor/mcp.json` in your project root |
| VS Code | `.vscode/mcp.json` in your project root |
| Claude Code | `.claude/mcp.json` in your project root |

## Typical workflow

1. Open a conversation with your AI assistant
2. Ask it to scan a page or evidence bundle: "Scan `index.html` for accessibility issues"
3. The assistant calls `a11y.evidence` to capture a tamper-evident bundle
4. Ask for diagnosis: "Diagnose the evidence bundle and verify provenance"
5. The assistant calls `a11y.diagnose`, checks integrity, and returns findings with fix guidance
6. Iterate on fixes within the conversation

## Integration with CI

Most teams combine MCP with CI:

1. CI runs `a11y-lint` and `a11y-ci gate` on every pull request
2. The gate uploads `.a11y_artifacts/` as CI artifacts
3. Developers forward `evidence.json` to MCP tools for interactive diagnosis and remediation
4. The AI assistant helps fix issues, and the next CI run verifies the fixes

This creates a feedback loop: automated detection in CI, interactive remediation via MCP, and automated verification on the next push.
