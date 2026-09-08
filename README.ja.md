<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

6つのツール。たった一つの目標：アクセシビリティテストを検証可能で、自動化され、無視できないものにする。

> **ソースから実行。** このスイートのいずれも、まだ npm や PyPI に公開されていません。以下のすべてのコマンドは、このリポジトリからインストールされます。各ツールの `package.json` および `pyproject.toml` にあるパッケージ名は、現在インストールできるリンクではなく、公開される予定の名前です。

---

## 概要

ほとんどのアクセシビリティツールは、「12件の違反があります」というところで止まります。アクセシビリティスイートはさらに進んで、テストされた内容の改ざん防止機能付きの証拠を記録し、CIパイプラインで回帰を検出し、視覚障害、スクリーンリーダー、失読症、認知負荷のプロファイルに合わせて調整された修正ガイダンスを提供します。

このスイートは、アクセシブルなパターンに対する CLI 出力のリンティングから、暗号学的証拠による WCAG 違反の HTML スキャン、CI での品質ゲートの強制、そして MCP を介してすべてを公開し、AI アシスタントが修正ループに参加できるようにすることまで、完全なライフサイクルを網羅します。

**主な原則：**

- **アサーションよりも証拠** - すべての検出結果は、SHA-256 整合性ダイジェストを持つ prov-spec 形式の証拠記録によって裏付けられます。
- **視覚障碍者向けの出力** - すべての CLI ツールは、`[OK]/[WARN]/[FAIL] + What/Why/Fix` 契約を使用します。
- **決定性** - 同じ入力は常に同じ出力を生成します。ネットワーク呼び出しやランダム性は一切ありません。
- **CI ネイティブ** - 自動化されたパイプライン用に設計された終了コード、スコアカード JSON、および PR コメント。

---

## プロジェクト

| プロジェクト | 説明 | スタック | 配布 |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | CLI 出力用のアクセシビリティリンター - エラーメッセージがアクセシブルなパターンに従っていることを検証します。 | Python 3.10+ | ソースのみ |
| [a11y-ci](src/a11y-ci/) | 回帰検出と許可リストを備えた、アクセシビリティスコアカードの CI ゲート | Python 3.10+ | ソースのみ |
| [a11y-assist](src/a11y-assist/) | 5つのアクセシビリティプロファイルを備えた、視覚障碍者向けの CLI アシスタント | Python 3.10+ | ソースのみ |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | prov-spec 形式の証拠記録を備えた、ヘッドレス HTML スキャナー | Node.js 18+ | ソースのみ |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | アクセシビリティの証拠キャプチャと診断のための MCP サーバー | Node.js 18+ | ソースのみ |
| [a11y-demo-site](examples/a11y-demo-site/) | エンドツーエンドテスト用の、意図的な違反を含むデモサイト | HTML | -- |

---

## クイックスタート

### アクセシブルなパターンに対する CLI 出力のリンティング

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### アクセシビリティの回帰に基づいて CI をゲート

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### HTML をスキャンし、証拠をキャプチャ

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### CLI エラーに対する修正ガイダンスを取得

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### 証拠をキャプチャし、MCP を介して診断

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### デモサイトをエンドツーエンドで実行

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### すべてのテストをローカルで実行

```bash
npm test
# or
./scripts/verify.sh
```

これは、3つの Python プロジェクトに対して pytest を、2つの Node.js プロジェクトに対して npm test を実行し、ハンドブックを検証します。

---

## アーキテクチャ

6つのツールは、検出から修正までのパイプラインを形成します。

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

1. **a11y-lint** は、アクセシブルなエラーメッセージパターンについて CLI テキストをスキャンし、スコアカードを生成します。
2. **a11y-evidence-engine** は、HTML ファイルをスキャンし、prov-spec 形式の証拠記録とともに検出結果を出力します。
3. **a11y-ci** は、スコアカードを消費し、しきい値を強制し、回帰を検出し、PR コメントを生成します。
4. **a11y-mcp-tools** は、証拠キャプチャと診断を、AI アシスタント統合のための MCP ツールとしてラップします。
5. **a11y-assist** は、検出結果（構造化 JSON または生のテキスト）を受け取り、5つのアクセシビリティプロファイルで修正ガイダンスを生成します。
6. **a11y-demo-site** は、意図的な違反を含む実行可能な例として、すべてをまとめます。

**共有契約：**

- `cli.error.schema.v0.1.json` - すべての Python ツール間で共有される、構造化されたエラー形式
- `evidence.bundle.schema.v0.1.json` - 証拠チェーンを備えた証拠バンドル
- `.a11y_artifacts/` - CI パイプライン用の統一されたアーティファクトディレクトリ
- prov-spec メソッド ID - すべての証拠ステップの安定したバージョン管理された識別子

---

## MCP クライアントの構成

a11y-mcp-tools を MCP クライアント（Claude Desktop、Cursor、VS Code など）に接続するには：

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

または、`npm --prefix src/a11y-mcp-tools link` の後：

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

サーバーは、次の2つのツールを公開します。

| ツール | 説明 |
|------|-------------|
| `a11y.evidence` | HTML、CLI ログ、またはその他の入力から、改ざん防止機能付きの証拠バンドルをキャプチャします。 |
| `a11y.diagnose` | 証拠検証付きで、証拠バンドルに対して WCAG ルールチェックを実行します。 |

---

## CI 統合（GitHub Actions）

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

Azure DevOps の例とトラブルシューティングについては、[GETTING_STARTED.md](GETTING_STARTED.md) を参照してください。

---

## ドキュメント

| ドキュメント | 説明 |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | アーキテクチャの詳細、統合パターン、および開発ガイド |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 3つのコマンドによるローカルセットアップ、CI テンプレート、およびトラブルシューティング |
| [CHANGELOG.md](CHANGELOG.md) | Keep a Changelog 形式でのリリース履歴 |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | 統一されたアーティファクトディレクトリ戦略 |
| [docs/prov-spec/](docs/prov-spec/) | 証拠仕様 |

---

## セキュリティとデータ範囲

- **アクセスされるデータ：** アクセシビリティ分析のために、HTML ファイル、CLI 出力、およびスコアカード JSON を読み取ります。DOM スナップショットをキャプチャし、証拠バンドルを生成します。
- **アクセスされないデータ：** ネットワークリクエストは行いません。テレメトリは送信しません。ユーザーデータは保存しません。資格情報やトークンは使用しません。
- **必要な権限：** ターゲットファイルへの読み取りアクセス。証拠/アーティファクト出力ディレクトリへの書き込みアクセス。

## スコアカード

| ゲート | ステータス |
|------|--------|
| A. セキュリティベースライン | PASS |
| B. エラー処理 | PASS |
| C. オペレーター向けドキュメント | PASS |
| D. リリース時の衛生管理 | PASS |
| E. 識別 | PASS |

## ライセンス

[MIT](LICENSE)

---

MCP Tool Shop によって構築
