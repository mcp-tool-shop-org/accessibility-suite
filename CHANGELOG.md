# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-09-07

### Fixed

- **The README advertised seven packages that do not exist.** Install commands for
  `@accessibility-suite/{core,ci,evidence-engine,mcp-tools}` and PyPI
  `a11y-{lint,ci,assist}` all 404, and the npm version badge pointed at a package
  with no versions. Anyone following the Quick Start got seven failures. Every
  command now installs from this repository, the Distribution column reads
  `source only`, and the MCP client snippet points at
  `src/a11y-mcp-tools/bin/server.js` instead of telling clients to `npx` a package
  that was never published. Translations regenerated to match.

### Changed

- **Root package is `private: true`.** It is a monorepo umbrella with no `main`,
  `bin`, `exports` or `files`; publishing it would have shipped the entire working
  tree -- `site/`, `docs/`, `examples/`, `pipelines/`, `tools/` and
  `.a11y_artifacts_test/` -- as the first artifact ever to appear under the
  `@accessibility-suite` scope.
- **`publish.yml` no longer fires on `release: published`.** With a live `NPM_TOKEN`
  on the repo since 2026-03-03, creating a GitHub Release ran `npm publish`. Since
  tag `v1.0.0` had no Release, the obvious housekeeping fix was also the trigger.
  Manual dispatch only until the suite genuinely ships.

## [1.0.1] - 2026-03-25

### Added

- Root `scripts/verify.sh` to run all sub-project tests locally
- `npm test` / `npm run verify` commands in package.json
- Local testing section in README

## [1.0.0] - 2026-02-27

### Added

- SECURITY.md with threat model and vulnerability reporting
- SHIP_GATE.md and SCORECARD.md for product standards
- Security & Data Scope section in README
- Scorecard and standard footer in README

### Changed

- Bumped version from 0.2.2 to 1.0.0

## [0.2.0] - 2026-02-17

### Added

- Product-focused README.md replacing the migration notice with suite value proposition, architecture overview, project table, quick start guides, MCP client configuration, and documentation links.
- HANDBOOK.md with comprehensive documentation covering the accessibility testing problem space, architecture deep dives for all six sub-projects, evidence-based testing with prov-spec provenance, CI integration patterns (GitHub Actions and Azure DevOps), MCP integration guide, development setup for the multi-language monorepo, and FAQ.
- CHANGELOG.md in Keep a Changelog format.
- MIT license badge in README.md.

## [0.1.0] - 2026-02-12

### Added

- Initial monorepo structure consolidating six accessibility tools.
- a11y-lint: accessibility linter for CLI output with WCAG and policy rules.
- a11y-ci: CI gate for accessibility scorecards with regression detection and allowlists.
- a11y-assist: low-vision-first CLI assistant with five accessibility profiles (lowvision, cognitive-load, screen-reader, dyslexia, plain-language).
- a11y-evidence-engine: headless HTML scanner with prov-spec provenance records.
- a11y-mcp-tools: MCP server exposing evidence capture and diagnosis tools.
- a11y-demo-site: demo site with intentional violations for end-to-end testing.
- Unified artifact strategy with `.a11y_artifacts/` directory convention.
- GETTING_STARTED.md with three-command local setup and CI templates.
- prov-spec documentation in `docs/prov-spec/`.

[0.2.0]: https://github.com/mcp-tool-shop-org/accessibility-suite/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/mcp-tool-shop-org/accessibility-suite/releases/tag/v0.1.0
