<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

六つのツール。一つの目標：アクセシビリティテストを検証可能にし、自動化し、無視できないものにする。

---

## 概要

多くのアクセシビリティツールは「12件の違反があります」というメッセージで終わります。しかし、Accessibility Suiteはさらに進んでおり、テスト内容の改ざん防止機能付きの証拠を収集し、CIパイプラインでのリグレッションを検出し、視覚障碍者、スクリーンリーダー、読字障害、認知負荷の特性に合わせた修正方法を提示します。

このスイートは、アクセシブルなパターンをCLI出力で検証し、暗号学的プロビナンス情報付きでHTMLのWCAG違反をスキャンし、CI環境での品質ゲートを適用し、すべての情報をMCPを通じて公開することで、AIアシスタントが修正プロセスに参加できるようにします。

**主な原則：**

- **主張ではなく証拠:** すべての検出結果は、SHA-256整合性チェックサムを含むプロビナンスレコードによって裏付けられています。
- **視覚障碍者向けの出力:** すべてのCLIツールは、`[OK]/[WARN]/[FAIL] + 何が/なぜ/修正方法`という形式を使用します。
- **決定性:** 同じ入力は常に同じ出力を生成します。ネットワーク接続やランダム性は使用しません。
- **CIネイティブ:** 自動化パイプライン向けに、終了コード、スコアカードJSON、およびプルリクエストコメントが設計されています。

---

## プロジェクト

| プロジェクト | 説明 | 技術スタック | パッケージ |
|---------|-------------|-------|---------|
| [a11y-lint](src/a11y-lint/) | CLI出力のアクセシビリティリンター：エラーメッセージがアクセシブルなパターンに従っているか検証します。 | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | アクセシビリティスコアカードのCIゲート：リグレッション検出と許可リスト機能付き。 | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | 5つのアクセシビリティプロファイルに対応した、視覚障碍者向けのCLIアシスタント。 | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | プロビナンス情報付きのヘッドレスHTMLスキャナ。 | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | アクセシビリティの証拠収集と診断を行うMCPサーバー。 | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | 意図的に違反を含んだデモサイト：エンドツーエンドテスト用。 | HTML | -- |

---

## クイックスタート

### CLI出力のアクセシブルなパターンを検証します

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### アクセシビリティのリグレッションを検出し、CIパイプラインを制御します

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### HTMLをスキャンし、プロビナンス情報を収集します

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### CLIエラーに対する修正方法を取得します

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### MCPを通じて証拠を収集し、診断を行います

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### デモサイトをエンドツーエンドで実行します

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## アーキテクチャ

これらの6つのツールは、検出から修正までのパイプラインを構成します。

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

**データフロー：**

1. **a11y-lint:** CLIテキストをスキャンし、アクセシブルなエラーメッセージパターンを検出し、スコアカードを生成します。
2. **a11y-evidence-engine:** HTMLファイルをスキャンし、プロビナンス情報付きの検出結果を生成します。
3. **a11y-ci:** スコアカードを消費し、閾値を適用し、リグレッションを検出し、プルリクエストコメントを生成します。
4. **a11y-mcp-tools:** 証拠の収集と診断をMCPツールとしてラップし、AIアシスタントとの連携を可能にします。
5. **a11y-assist:** 検出結果（構造化されたJSONまたは生のテキスト）を受け取り、5つのアクセシビリティプロファイルで修正方法を生成します。
6. **a11y-demo-site:** これらすべてを統合し、意図的に違反を含んだ実行可能な例として提供します。

**共通のインターフェース：**

- `cli.error.schema.v0.1.json`: すべてのPythonツールで使用される構造化されたエラー形式。
- `evidence.bundle.schema.v0.1.json`: プロビナンスチェーンを含む証拠バンドル。
- `.a11y_artifacts/`: CIパイプライン用の統一されたアーティファクトディレクトリ。
- prov-specメソッドID：すべてのプロビナンスステップに、安定したバージョン管理された識別子を使用。

---

## MCPクライアントの設定

a11y-mcp-toolsをMCPクライアント（Claude Desktop、Cursor、VS Codeなど）に接続するには：

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

または、グローバルにインストールされている場合は：

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

サーバーは以下の2つのツールを提供します。

| ツール | 説明 |
|------|-------------|
| `a11y.evidence` | HTML、CLIログ、またはその他の入力から、改ざん防止機能付きの証拠バンドルを収集します。 |
| `a11y.diagnose` | プロビナンス検証付きで、証拠バンドルに対してWCAGルールチェックを実行します。 |

---

## CI統合（GitHub Actions）

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

[GETTING_STARTED.md](GETTING_STARTED.md) を参照して、Azure DevOps の例やトラブルシューティングについて確認してください。

---

## ドキュメント

| ドキュメント | 説明 |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | アーキテクチャの詳細、統合パターン、および開発ガイド |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 3つのコマンドでローカル環境を構築する方法、CI テンプレート、およびトラブルシューティング |
| [CHANGELOG.md](CHANGELOG.md) | Keep a Changelog 形式でのリリース履歴 |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | 統合された成果物ディレクトリ戦略 |
| [docs/prov-spec/](docs/prov-spec/) | プロヴェナンス仕様 |

---

## セキュリティとデータ範囲

- **アクセスするデータ:** アクセシビリティ分析のために、HTML ファイル、CLI の出力、およびスコアカードの JSON データを読み込みます。 DOM のスナップショットをキャプチャし、証拠バンドルを生成します。
- **アクセスしないデータ:** ネットワークリクエストは行いません。テレメトリーも行いません。ユーザーデータの保存も行いません。認証情報やトークンも使用しません。
- **必要な権限:** ターゲットファイルへの読み取りアクセス権。証拠/成果物出力ディレクトリへの書き込みアクセス権。

## スコアカード

| ゲート | ステータス |
|------|--------|
| A. セキュリティ基準 | 合格 |
| B. エラー処理 | 合格 |
| C. オペレーターのドキュメント | 合格 |
| D. リリースの品質 | 合格 |
| E. 認証 | 合格 |

## ライセンス

[MIT](LICENSE)

---

<a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> が作成しました。
