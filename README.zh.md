<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

六个工具，一个目标：使可访问性测试具有可验证性、自动化，并且难以被忽视。

> **从源代码运行。** 此套件中的任何内容尚未发布到 npm 或 PyPI。下面的每个命令都将从此仓库安装。每个工具的 `package.json` 和 `pyproject.toml` 中的软件包名称是预期的发布名称，而不是您可以今天安装的链接。

---

## 一览

大多数可访问性工具都停留在“您有 12 处违规”。可访问性套件更进一步：它捕获可篡改的证据，记录了测试的内容，将您的 CI 流水线与回归问题关联，并提供针对弱视、屏幕阅读器、阅读障碍和认知负荷配置文件的修复指导。

该套件涵盖了整个生命周期——对 CLI 输出进行 lint 检查，以查找可访问的模式，使用密码学来源扫描 HTML 以查找 WCAG 违规，在 CI 中强制执行质量控制，并通过 MCP 公开所有内容，以便 AI 助手可以参与修复循环。

**关键原则：**

- **证据胜于断言**——每个发现都由具有 SHA-256 完整性摘要的 prov-spec 来源记录支持。
- **首先考虑弱视用户的输出**——所有 CLI 工具都使用 `[OK]/[WARN]/[FAIL] + What/Why/Fix` 协议。
- **确定性**——相同的输入始终产生相同的输出；没有网络调用，没有随机性。
- **与 CI 原生兼容**——退出代码、评分卡 JSON 和 PR 注释，专为自动化流水线而设计。

---

## 项目

| 项目 | 描述 | 技术栈 | 分发方式 |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | 用于 CLI 输出的可访问性 lint 工具——验证错误消息是否遵循可访问的模式。 | Python 3.10+ | 仅源代码 |
| [a11y-ci](src/a11y-ci/) | 具有回归检测和允许列表的可访问性评分卡 CI 门控。 | Python 3.10+ | 仅源代码 |
| [a11y-assist](src/a11y-assist/) | 具有五种可访问性配置文件的、首先考虑弱视用户的 CLI 助手。 | Python 3.10+ | 仅源代码 |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | 具有 prov-spec 来源记录的无头 HTML 扫描器。 | Node.js 18+ | 仅源代码 |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | 用于可访问性证据捕获和诊断的 MCP 服务器。 | Node.js 18+ | 仅源代码 |
| [a11y-demo-site](examples/a11y-demo-site/) | 具有有意违规的演示站点，用于端到端测试。 | HTML | -- |

---

## 快速入门

### 对 CLI 输出进行 lint 检查，以查找可访问的模式

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### 将您的 CI 与可访问性回归关联

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### 扫描 HTML 并捕获来源

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### 获取 CLI 错误的修复指导

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### 通过 MCP 捕获证据并进行诊断

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### 运行演示站点的端到端测试

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### 在本地运行所有测试

```bash
npm test
# or
./scripts/verify.sh
```

这将为三个 Python 项目运行 pytest，为两个 Node.js 项目运行 npm test，并验证手册。

---

## 架构

这六个工具构成了一个从检测到修复的流水线：

```
                        CLI output                HTML files
                            |                         |
                    +-------v-------+        +--------v---------+
                    |   a11y-lint   |        | a11y-evidence-   |
                    | (scan & score)|        | engine (scan +   |
                    +-------+-------+        | provenance)      |
                            |                +--------+---------+
                  scorecard.json                      |
                            |               evidence bundle
                    +-------v-------+                 |
                    |    a11y-ci    |        +---------v---------+
                    |  (CI gate +  |        |  a11y-mcp-tools   |
                    |  PR comment) |        | (MCP evidence +   |
                    +-------+-------+        |  diagnosis)      |
                            |                +---------+---------+
                    pass / fail                        |
                            |                  findings + fixes
                    +-------v-------+                 |
                    |  a11y-assist  |<----------------+
                    | (fix guidance |
                    |  5 profiles)  |
                    +---------------+
```

**数据流：**

1. **a11y-lint** 扫描 CLI 文本，以查找可访问的错误消息模式，并生成评分卡。
2. **a11y-evidence-engine** 扫描 HTML 文件，并使用 prov-spec 来源记录生成发现结果。
3. **a11y-ci** 使用评分卡，强制执行阈值，检测回归，并生成 PR 注释。
4. **a11y-mcp-tools** 将证据捕获和诊断封装为 MCP 工具，以便与 AI 助手集成。
5. **a11y-assist** 接收发现结果（结构化 JSON 或原始文本），并生成五种可访问性配置文件的修复指导。
6. **a11y-demo-site** 将所有内容整合到一个可运行的示例中，其中包含有意违规。

**共享协议：**

- `cli.error.schema.v0.1.json`——所有 Python 工具中使用的结构化错误格式。
- `evidence.bundle.schema.v0.1.json`——带有来源链的证据包。
- `.a11y_artifacts/`——用于 CI 流水线的统一工件目录。
- prov-spec 方法 ID——每个来源步骤的稳定、版本化的标识符。

---

## MCP 客户端配置

要将 a11y-mcp-tools 连接到您的 MCP 客户端（Claude Desktop、Cursor、VS Code 等）：

```json
{
  "mcpServers": {
    "a11y": {
      "command": "node",
      "args": ["/absolute/path/to/accessibility-suite/src/a11y-mcp-tools/bin/server.js"]
    }
  }
}
```

或者，在 `npm --prefix src/a11y-mcp-tools link` 之后：

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

服务器公开两个工具：

| 工具 | 描述 |
|------|-------------|
| `a11y.evidence` | 从 HTML、CLI 日志或其他输入中捕获可篡改的证据包。 |
| `a11y.diagnose` | 使用来源验证，对证据包运行 WCAG 规则检查。 |

---

## CI 集成（GitHub Actions）

```yaml
jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Scan code
        run: |
          pip install a11y-lint
          mkdir .a11y_artifacts
          a11y-lint scan . --artifact-dir .a11y_artifacts

      - uses: mcp-tool-shop-org/accessibility-suite/.github/actions/a11y-ci@main
        with:
          artifact-dir: .a11y_artifacts
          fail-on: serious
```

有关 Azure DevOps 示例和故障排除，请参阅 [GETTING_STARTED.md](GETTING_STARTED.md)。

---

## 文档

| 文档 | 描述 |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | 架构深入分析、集成模式和开发指南。 |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 三个命令的本地设置、CI 模板和故障排除。 |
| [CHANGELOG.md](CHANGELOG.md) | 以 Keep a Changelog 格式记录的发布历史。 |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | 统一工件目录策略。 |
| [docs/prov-spec/](docs/prov-spec/) | 来源规范。 |

---

## 安全性和数据范围

- **访问的数据：** 读取 HTML 文件、CLI 输出和评分卡 JSON，以进行可访问性分析。捕获 DOM 快照并生成证据包。
- **未访问的数据：** 无网络请求。无遥测。无用户数据存储。无凭据或令牌。
- **所需的权限：** 对目标文件具有读取权限。对证据/工件输出目录具有写入权限。

## 评分卡

| 门控 | 状态 |
|------|--------|
| A. 安全基线 | 通过 |
| B. 错误处理 | 通过 |
| C. 操作员文档 | 通过 |
| D. 发布规范 | 通过 |
| E. 身份验证 | 通过 |

## 许可证

[MIT](LICENSE)

---

由 <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> 构建。
