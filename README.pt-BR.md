<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

Seis ferramentas. Uma missão: tornar os testes de acessibilidade verificáveis, automatizados e difíceis de ignorar.

> **Executar a partir do código-fonte.** Nada neste conjunto é publicado no npm ou PyPI ainda. Cada comando abaixo instala a partir deste repositório. Os nomes dos pacotes em cada ferramenta `package.json` e `pyproject.toml` são os nomes pretendidos para publicação, e não links que você pode instalar hoje.

---

## Em resumo

A maioria das ferramentas de acessibilidade para no ponto em que informa: "você tem 12 violações". O Conjunto de Acessibilidade vai mais longe: ele captura evidências verificáveis do que foi testado, define limites para o seu pipeline de CI em caso de regressões e apresenta orientações de correção adaptadas para perfis de baixa visão, leitores de tela, dislexia e carga cognitiva.

O conjunto abrange todo o ciclo de vida: analisa a saída da CLI em busca de padrões acessíveis, examina o HTML em busca de violações da WCAG com rastreabilidade criptográfica, aplica limites de qualidade no CI e disponibiliza tudo por meio do MCP para que assistentes de IA possam participar do ciclo de correção.

**Princípios-chave:**

- **Evidência em vez de afirmações:** cada descoberta é apoiada por um registro de rastreabilidade prov-spec com resumos de integridade SHA-256.
- **Saída priorizando baixa visão:** todas as ferramentas de CLI usam o contrato `[OK]/[WARN]/[FAIL] + What/Why/Fix`.
- **Determinístico:** a mesma entrada sempre produz a mesma saída; sem chamadas de rede, sem aleatoriedade.
- **Nativo do CI:** códigos de saída, JSON de scorecard e comentários de PR projetados para pipelines automatizados.

---

## Projetos

| Projeto | Descrição | Tecnologia | Distribuição |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | Analisador de acessibilidade para saída da CLI: valida se as mensagens de erro seguem padrões acessíveis. | Python 3.10+ | apenas código-fonte |
| [a11y-ci](src/a11y-ci/) | Limite de CI para scorecards de acessibilidade com detecção de regressões e listas de permissões. | Python 3.10+ | apenas código-fonte |
| [a11y-assist](src/a11y-assist/) | Assistente de CLI priorizando baixa visão com cinco perfis de acessibilidade. | Python 3.10+ | apenas código-fonte |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Scanner HTML sem interface gráfica com registros de rastreabilidade prov-spec. | Node.js 18+ | apenas código-fonte |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Servidor MCP para captura e diagnóstico de evidências de acessibilidade. | Node.js 18+ | apenas código-fonte |
| [a11y-demo-site](examples/a11y-demo-site/) | Site de demonstração com violações intencionais para testes de ponta a ponta. | HTML | -- |

---

## Primeiros passos

### Analisar a saída da CLI em busca de padrões acessíveis

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Definir limites para o seu CI em caso de regressões de acessibilidade

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Analisar o HTML e capturar a rastreabilidade

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### Obter orientações de correção para uma falha na CLI

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Capturar evidências e diagnosticar por meio do MCP

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### Executar o site de demonstração de ponta a ponta

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### Executar todos os testes localmente

```bash
npm test
# or
./scripts/verify.sh
```

Isso executa o pytest para os três projetos Python, npm test para os dois projetos Node.js e verifica os manuais.

---

## Arquitetura

As seis ferramentas formam um pipeline desde a detecção até a correção:

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

1. **a11y-lint** analisa o texto da CLI em busca de padrões de mensagens de erro acessíveis e produz um scorecard.
2. **a11y-evidence-engine** analisa arquivos HTML e emite descobertas com registros de rastreabilidade prov-spec.
3. **a11y-ci** consome scorecards, aplica limites, detecta regressões e gera comentários de PR.
4. **a11y-mcp-tools** envolve a captura de evidências e o diagnóstico como ferramentas MCP para integração com assistentes de IA.
5. **a11y-assist** recebe as descobertas (JSON estruturado ou texto bruto) e gera orientações de correção em cinco perfis de acessibilidade.
6. **a11y-demo-site** une tudo em um exemplo executável com violações intencionais.

**Contratos compartilhados:**

- `cli.error.schema.v0.1.json`: formato de erro estruturado em todas as ferramentas Python.
- `evidence.bundle.schema.v0.1.json`: pacotes de evidências com cadeias de rastreabilidade.
- `.a11y_artifacts/`: diretório de artefatos unificado para pipelines de CI.
- IDs de método prov-spec: identificadores estáveis e versionados para cada etapa de rastreabilidade.

---

## Configuração do cliente MCP

Para conectar o a11y-mcp-tools ao seu cliente MCP (Claude Desktop, Cursor, VS Code, etc.):

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

Ou, após `npm --prefix src/a11y-mcp-tools link`:

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

| Ferramenta | Descrição |
|------|-------------|
| `a11y.evidence` | Capturar pacotes de evidências verificáveis de HTML, logs da CLI ou outras entradas. |
| `a11y.diagnose` | Executar verificações de regras da WCAG em pacotes de evidências com verificação de rastreabilidade. |

---

## Integração com o CI (GitHub Actions)

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

Consulte [GETTING_STARTED.md](GETTING_STARTED.md) para exemplos do Azure DevOps e solução de problemas.

---

## Documentação

| Documento | Descrição |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Análise aprofundada da arquitetura, padrões de integração e guia de desenvolvimento. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuração local de três comandos, modelos de CI e solução de problemas. |
| [CHANGELOG.md](CHANGELOG.md) | Histórico de lançamentos no formato Keep a Changelog. |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Estratégia de diretório de artefatos unificado. |
| [docs/prov-spec/](docs/prov-spec/) | Especificação de rastreabilidade. |

---

## Segurança e escopo de dados

- **Dados acessados:** Lê arquivos HTML, saída da CLI e JSON do scorecard para análise de acessibilidade. Captura instantâneos do DOM e gera pacotes de evidências.
- **Dados NÃO acessados:** Sem solicitações de rede. Sem telemetria. Sem armazenamento de dados do usuário. Sem credenciais ou tokens.
- **Permissões necessárias:** Acesso de leitura aos arquivos de destino. Acesso de gravação para diretórios de saída de evidências/artefatos.

## Scorecard

| Limite | Status |
|------|--------|
| A. Linha de base de segurança | APROVADO |
| B. Tratamento de erros | APROVADO |
| C. Documentação do operador | APROVADO |
| D. Higiene de envio | APROVADO |
| E. Identidade | APROVADO |

## Licença

[MIT](LICENSE)

---

Criado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
