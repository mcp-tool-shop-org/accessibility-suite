# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | Yes       |
| < 1.0   | No        |

## Reporting a Vulnerability

**Email:** 64996768+mcp-tool-shop@users.noreply.github.com

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact

**Response timeline:**
- Acknowledgment: within 48 hours
- Assessment: within 7 days
- Fix (if confirmed): within 30 days

## Scope

accessibility-suite is a **monorepo** containing six accessibility tools:
- **Data accessed:** Reads HTML files, CLI output, and scorecard JSON for accessibility analysis. Captures DOM snapshots and generates evidence bundles.
- **Data NOT accessed:** No network requests. No telemetry. No user data storage. No credentials or tokens.
- **Permissions required:** Read access to target files. Write access for evidence/artifact output directories.
