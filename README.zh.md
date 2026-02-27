<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.npmjs.com/package/@mcptoolshop/accessibility-suite"><img src="https://img.shields.io/npm/v/@mcptoolshop/accessibility-suite" alt="npm"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

六个工具，一个目标：使辅助功能测试可验证、自动化，并且难以被忽视。

---

## 概述

大多数辅助功能工具只能指出“您有 12 个问题”。 辅助功能套件做得更多：它记录了经过篡改保护的测试结果，在持续集成（CI）流水线中检测回归，并提供针对低视力、屏幕阅读器、阅读障碍和认知负荷的修复建议。

该套件涵盖整个生命周期：检查命令行输出以查找符合辅助功能标准的模式，扫描 HTML 以查找 WCAG 违规情况并记录其来源，在 CI 中强制执行质量控制，并通过 MCP 将所有内容暴露出来，以便人工智能助手参与到修复过程中。

**核心原则：**

- **以证据为基础，而非断言**：每个发现都伴随一个包含 SHA-256 完整性摘要的、可追溯的记录。
- **以低视力为优先的输出**：所有命令行工具都使用 `[OK]/[WARN]/[FAIL] + 问题/原因/修复建议` 的格式。
- **确定性**：相同的输入始终产生相同的输出；没有网络调用，没有随机性。
- **原生 CI 支持**：提供退出码、 scorecard JSON 格式以及用于自动化流水线的拉取请求（PR）评论。

---

## 项目

| 项目 | 描述 | 技术栈 | 包 |
|---------|-------------|-------|---------|
| [a11y-lint](src/a11y-lint/) | 用于命令行输出的辅助功能检查器，验证错误消息是否符合辅助功能标准。 | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | 用于辅助功能 scorecard 的 CI 质量控制，具有回归检测和白名单功能。 | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | 具有五种辅助功能配置的命令行助手，专为低视力用户设计。 | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | 无头 HTML 扫描器，记录包含可追溯信息的报告。 | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | 用于捕获辅助功能证据和诊断的 MCP 服务器。 | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | 包含故意违规的演示站点，用于端到端测试。 | HTML | -- |

---

## 快速开始

### 检查命令行输出以查找符合辅助功能标准的模式

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### 在 CI 流水线中，根据辅助功能 scorecard 检测回归

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### 扫描 HTML 并记录其来源

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### 获取命令行错误修复建议

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### 通过 MCP 捕获证据并进行诊断

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### 运行演示站进行端到端测试

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## 架构

这六个工具形成一个从检测到修复的流水线：

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

1. **a11y-lint** 扫描命令行文本，查找符合辅助功能标准的错误消息，并生成 scorecard。
2. **a11y-evidence-engine** 扫描 HTML 文件，并生成包含可追溯信息的报告。
3. **a11y-ci** 消费 scorecard，执行阈值检查，检测回归，并生成拉取请求（PR）评论。
4. **a11y-mcp-tools** 将证据捕获和诊断包装为 MCP 工具，用于与人工智能助手集成。
5. **a11y-assist** 接收发现结果（结构化的 JSON 或原始文本），并生成针对五种辅助功能配置的修复建议。
6. **a11y-demo-site** 将所有内容整合到一个可运行的示例中，其中包含故意违规的内容。

**共享接口：**

- `cli.error.schema.v0.1.json`：所有 Python 工具使用的结构化错误格式。
- `evidence.bundle.schema.v0.1.json`：包含可追溯链的证据包。
- `.a11y_artifacts/`：用于 CI 流水线的统一工件目录。
- prov-spec 方法 ID：用于每个可追溯步骤的稳定、版本化的标识符。

---

## MCP 客户端配置

要将 a11y-mcp-tools 连接到您的 MCP 客户端（Claude Desktop、Cursor、VS Code 等）：

```json
{
  "mcpServers": {
    "a11y": {
      "command": "npx",
      "args": ["-y", "@mcptoolshop/a11y-mcp-tools"]
    }
  }
}
```

或者，如果已全局安装：

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

服务器暴露了两个工具：

| 工具 | 描述 |
|------|-------------|
| `a11y.evidence` | 从 HTML、命令行日志或其他输入捕获经过篡改保护的证据包。 |
| `a11y.diagnose` | 使用可追溯性验证，对证据包执行 WCAG 规则检查。 |

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

请参考 [GETTING_STARTED.md](GETTING_STARTED.md) 获取 Azure DevOps 的示例和故障排除方法。

---

## 文档

| 文档 | 描述 |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | 架构深入分析、集成模式和开发指南 |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 三步本地环境配置、CI 模板和故障排除 |
| [CHANGELOG.md](CHANGELOG.md) | 以 Keep a Changelog 格式记录的发布历史 |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | 统一的构建产物目录策略 |
| [docs/prov-spec/](docs/prov-spec/) | 溯源规范 |

---

## 安全与数据范围

- **访问的数据：** 读取 HTML 文件、CLI 输出以及用于可访问性分析的 scorecard JSON 文件。 捕获 DOM 快照并生成证据包。
- **未访问的数据：** 不进行任何网络请求。 不收集任何遥测数据。 不存储任何用户数据。 不存储任何凭证或令牌。
- **所需权限：** 访问目标文件的读取权限。 写入权限用于证据/构建产物输出目录。

## 评分

| 关卡 | 状态 |
|------|--------|
| A. 安全基线 | 通过 |
| B. 错误处理 | 通过 |
| C. 操作员文档 | 通过 |
| D. 发布流程规范 | 通过 |
| E. 身份验证 | 通过 |

## 许可证

[MIT](LICENSE)

---

由 <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> 构建。
