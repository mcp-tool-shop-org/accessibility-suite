import type { SiteConfig } from '@mcptoolshop/site-theme';

export const config: SiteConfig = {
  title: 'Accessibility Suite',
  description: 'Unified monorepo for accessibility testing, evidence generation, and WCAG compliance tooling.',
  logoBadge: 'A11Y',
  brandName: 'Accessibility Suite',
  repoUrl: 'https://github.com/mcp-tool-shop-org/accessibility-suite',
  npmUrl: 'https://www.npmjs.com/package/@mcptoolshop/accessibility-suite',
  footerText: 'MIT Licensed — built by <a href="https://github.com/mcp-tool-shop-org" style="color:var(--color-muted);text-decoration:underline">mcp-tool-shop-org</a>',

  hero: {
    badge: 'Python · Node.js · MCP',
    headline: 'WCAG compliance,',
    headlineAccent: 'with receipts.',
    description: 'Six tools. One mission: make accessibility testing verifiable, automated, and hard to ignore.',
    primaryCta: { href: '#usage', label: 'Get started' },
    secondaryCta: { href: '#tools', label: 'See the tools' },
    previews: [
      {
        label: 'Lint & gate',
        code: '# lint CLI output for accessible patterns\npip install a11y-lint a11y-ci\na11y-lint scan . --artifact-dir .a11y_artifacts\na11y-ci gate --artifact-dir .a11y_artifacts',
      },
      {
        label: 'Scan HTML',
        code: '# scan HTML with cryptographic provenance\nnpm install -g @mcptoolshop/a11y-evidence-engine\na11y-engine scan ./html --out ./results\n\n# get fix guidance for a finding\npip install a11y-assist\na11y-assist explain --json error.json --profile screen-reader',
      },
      {
        label: 'MCP config',
        code: '// connect to Claude Desktop, Cursor, VS Code\n{\n  "mcpServers": {\n    "a11y": {\n      "command": "npx",\n      "args": ["-y", "@mcptoolshop/a11y-mcp-tools"]\n    }\n  }\n}',
      },
    ],
  },

  sections: [
    {
      kind: 'features',
      id: 'features',
      title: 'Evidence over assertions',
      subtitle: 'Most tools stop at "you have 12 violations." This suite goes further: every finding is backed by a tamper-evident provenance record.',
      features: [
        {
          title: 'Cryptographic provenance',
          desc: 'Every finding carries a prov-spec provenance record with SHA-256 integrity digests. Same input always produces identical output — no network calls, no randomness.',
        },
        {
          title: 'Low-vision-first output',
          desc: 'All CLI tools follow the [OK]/[WARN]/[FAIL] + What/Why/Fix contract. Five accessibility profiles: low-vision, screen-reader, dyslexia, cognitive-load, and standard.',
        },
        {
          title: 'CI-native by design',
          desc: 'Exit codes, scorecard JSON, and PR comments built for automated pipelines. Gate releases on WCAG regressions. Drop in as a GitHub Actions composite action.',
        },
      ],
    },
    {
      kind: 'data-table',
      id: 'tools',
      title: 'The six tools',
      subtitle: 'Detection through remediation — each tool hands off to the next.',
      columns: ['Tool', 'What it does', 'Stack'],
      rows: [
        ['a11y-lint', 'Scan CLI output for accessible error message patterns, produce scorecards', 'Python · PyPI'],
        ['a11y-ci', 'CI gate with regression detection, allowlists, and PR comments', 'Python · PyPI · npm'],
        ['a11y-assist', 'Fix guidance in five accessibility profiles from structured findings', 'Python · PyPI'],
        ['a11y-evidence-engine', 'Headless HTML scanner with prov-spec provenance records', 'Node.js · npm'],
        ['a11y-mcp-tools', 'MCP server — evidence capture and WCAG diagnosis for AI assistants', 'Node.js · npm'],
        ['a11y-demo-site', 'Demo site with intentional violations for end-to-end testing', 'HTML'],
      ],
    },
    {
      kind: 'code-cards',
      id: 'usage',
      title: 'Get started',
      cards: [
        {
          title: 'Lint CLI output',
          code: 'pip install a11y-lint\na11y-lint scan output.txt',
        },
        {
          title: 'Gate CI on regressions',
          code: 'pip install a11y-ci\na11y-lint scan . --artifact-dir .a11y_artifacts\na11y-ci gate --artifact-dir .a11y_artifacts',
        },
        {
          title: 'Scan HTML with provenance',
          code: 'npm install -g @mcptoolshop/a11y-evidence-engine\na11y-engine scan ./html --out ./results',
        },
        {
          title: 'MCP tools for AI assistants',
          code: 'npm install -g @mcptoolshop/a11y-mcp-tools\na11y evidence --target page.html --out evidence.json\na11y diagnose --bundle evidence.json --verify-provenance',
        },
      ],
    },
    {
      kind: 'features',
      id: 'pipeline',
      title: 'How it works',
      subtitle: 'Six tools that form a pipeline from detection through remediation.',
      features: [
        {
          title: '1. Detect',
          desc: 'a11y-lint scans CLI text for accessible error patterns. a11y-evidence-engine scans HTML and emits findings with prov-spec provenance chains.',
        },
        {
          title: '2. Gate',
          desc: 'a11y-ci consumes scorecards, enforces thresholds, detects regressions vs. the last run, and posts PR comments. Fails the build on new serious violations.',
        },
        {
          title: '3. Fix',
          desc: 'a11y-assist generates fix guidance tuned to five accessibility profiles. a11y-mcp-tools brings the whole pipeline into your AI assistant via MCP.',
        },
      ],
    },
  ],
};
