---
title: Handbook
description: Everything you need to know about Accessibility Suite.
sidebar:
  order: 0
---

Welcome to the Accessibility Suite handbook.

The Accessibility Suite is a monorepo containing six tools that form a pipeline from accessibility detection through remediation. Every finding is backed by a tamper-evident provenance record with SHA-256 integrity digests. All CLI tools use the `[OK]/[WARN]/[FAIL] + What/Why/Fix` contract for low-vision-first output. Same input always produces identical output -- no network calls, no randomness.

## What's inside

- **[Getting Started](/accessibility-suite/handbook/getting-started/)** -- Install the suite and run your first scan in under a minute
- **[Architecture](/accessibility-suite/handbook/architecture/)** -- How the monorepo is organized and how data flows between tools
- **[Tools](/accessibility-suite/handbook/tools/)** -- Detailed guide to each of the six tools
- **[MCP Integration](/accessibility-suite/handbook/mcp-integration/)** -- Connect the suite to Claude Desktop, Cursor, or VS Code
- **[CI Integration](/accessibility-suite/handbook/ci-integration/)** -- Gate your pipeline on accessibility regressions
- **[Reference](/accessibility-suite/handbook/reference/)** -- Full command reference, exit codes, error IDs, and schemas
- **[For Beginners](/accessibility-suite/handbook/beginners/)** -- New to accessibility testing? Start here

[Back to landing page](/accessibility-suite/)
