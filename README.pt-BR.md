<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

Seis ferramentas. Uma missão: tornar os testes de acessibilidade verificáveis, automatizados e difíceis de ignorar.

---

## Visão Geral

A maioria das ferramentas de acessibilidade para com a informação "você tem 12 violações". O Accessibility Suite vai além: ele registra evidências verificáveis do que foi testado, integra-se ao seu pipeline de CI para detectar regressões e fornece orientações para correções, adaptadas para usuários com baixa visão, leitores de tela, dislexia e para aqueles com dificuldades de processamento cognitivo.

O conjunto de ferramentas abrange todo o ciclo de vida: analisa a saída da linha de comando em busca de padrões de acessibilidade, verifica o HTML em busca de violações das diretrizes WCAG, aplica controles de qualidade no CI e disponibiliza tudo através do MCP para que assistentes de IA possam participar do processo de correção.

**Princípios chave:**

- **Evidências em vez de afirmações:** cada resultado é respaldado por um registro de rastreabilidade com digests de integridade SHA-256.
- **Foco em usuários com baixa visão:** todas as ferramentas de linha de comando usam o contrato `[OK]/[WARN]/[FAIL] + O que/Por quê/Como corrigir`.
- **Determinístico:** a mesma entrada sempre produz a mesma saída; não há chamadas de rede, não há aleatoriedade.
- **Nativo para CI:** códigos de saída, JSON de scorecard e comentários de pull request projetados para pipelines automatizados.

---

## Projetos

| Projeto | Descrição | Stack | Pacote |
| --------- | ------------- | ------- | --------- |
| [a11y-lint](src/a11y-lint/) | Analisador de acessibilidade para a saída da linha de comando: valida se as mensagens de erro seguem padrões de acessibilidade. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | Controle de qualidade para scorecards de acessibilidade no CI, com detecção de regressões e listas de permissões. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | Assistente de linha de comando focado em usuários com baixa visão, com cinco perfis de acessibilidade. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Scanner HTML sem interface gráfica com registros de rastreabilidade. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Servidor MCP para captura e diagnóstico de evidências de acessibilidade. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | Site de demonstração com violações intencionais para testes de ponta a ponta. | HTML | -- |

---

## Como Começar

### Analise a saída da linha de comando em busca de padrões de acessibilidade

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Integre o controle de qualidade no seu pipeline de CI para detectar regressões de acessibilidade

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Verifique o HTML e capture a rastreabilidade

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### Obtenha orientações para corrigir uma falha na linha de comando

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Capture evidências e diagnostique através do MCP

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### Execute o site de demonstração de ponta a ponta

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## Arquitetura

As seis ferramentas formam um pipeline que vai desde a detecção até a correção:

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

**Fluxo de dados:**

1. **a11y-lint** analisa o texto da linha de comando em busca de padrões de mensagens de erro acessíveis e gera um scorecard.
2. **a11y-evidence-engine** analisa arquivos HTML e gera resultados com registros de rastreabilidade.
3. **a11y-ci** consome scorecards, aplica limites, detecta regressões e gera comentários de pull request.
4. **a11y-mcp-tools** encapsula a captura de evidências e o diagnóstico como ferramentas MCP para integração com assistentes de IA.
5. **a11y-assist** recebe resultados (JSON estruturados ou texto bruto) e gera orientações para correção em cinco perfis de acessibilidade.
6. **a11y-demo-site** integra tudo em um exemplo executável com violações intencionais.

**Contratos comuns:**

- `cli.error.schema.v0.1.json` -- formato de erro estruturado para todas as ferramentas Python.
- `evidence.bundle.schema.v0.1.json` -- pacotes de evidências com cadeias de rastreabilidade.
- `.a11y_artifacts/` -- diretório unificado de artefatos para pipelines de CI.
- IDs de método de rastreabilidade -- identificadores estáveis e versionados para cada etapa de rastreabilidade.

---

## Configuração do Cliente MCP

Para conectar a11y-mcp-tools ao seu cliente MCP (Claude Desktop, Cursor, VS Code, etc.):

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

Ou, se instalado globalmente:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

O servidor expõe duas ferramentas:

| Tool | Descrição |
| ------ | ------------- |
| `a11y.evidence` | Capture de evidências com proteção contra adulteração, provenientes de HTML, logs de linha de comando ou outras fontes. |
| `a11y.diagnose` | Execução de verificações de conformidade com as diretrizes WCAG em relação às evidências, com verificação de origem. |

---

## Integração com CI (GitHub Actions)

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

Consulte o arquivo [GETTING_STARTED.md](GETTING_STARTED.md) para exemplos do Azure DevOps e informações sobre solução de problemas.

---

## Documentação

| Documento. | Descrição. |
| ---------- | ------------- |
| [HANDBOOK.md](HANDBOOK.md) | Análise aprofundada da arquitetura, padrões de integração e guia de desenvolvimento. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuração local com três comandos, modelos de CI e solução de problemas. |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de lançamentos no formato "Keep a Changelog". |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Estratégia unificada para diretórios de artefatos. |
| [docs/prov-spec/](docs/prov-spec/) | Especificação de rastreabilidade (proveniência). |

---

## Licença

[MIT](LICENSE)
