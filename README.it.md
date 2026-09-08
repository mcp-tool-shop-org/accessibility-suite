<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.md">English</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

Sei strumenti. Una missione: rendere i test di accessibilità verificabili, automatizzati e difficili da ignorare.

> **Esegui dal codice sorgente.** Al momento, nulla di questa suite è pubblicato su npm o PyPI. Ogni comando
> riportato di seguito viene installato da questo repository. I nomi dei pacchetti in `package.json` e
> `pyproject.toml` di ciascuno strumento sono i nomi previsti per la pubblicazione, non i link che è possibile installare oggi.

---

## In sintesi

La maggior parte degli strumenti di accessibilità si ferma a "hai 12 violazioni". La Suite di accessibilità va oltre: registra prove inconfutabili di ciò che è stato testato, imposta dei controlli nella pipeline CI per rilevare regressioni e fornisce indicazioni per la correzione, adattate a profili di utenti con problemi di vista, lettori di schermo, dislessia e sovraccarico cognitivo.

La suite copre l'intero ciclo di vita: analizza l'output CLI per individuare modelli accessibili, esegue la scansione di HTML alla ricerca di violazioni WCAG con una provenienza crittografica, applica controlli di qualità nella CI ed espone tutto tramite MCP in modo che gli assistenti AI possano partecipare al processo di correzione.

**Principi chiave:**

- **Prove anziché asserzioni:** ogni risultato è supportato da una registrazione della provenienza conforme alle specifiche, con digest di integrità SHA-256.
- **Output ottimizzato per utenti con problemi di vista:** tutti gli strumenti CLI utilizzano il contratto `[OK]/[WARN]/[FAIL] + What/Why/Fix`.
- **Deterministico:** lo stesso input produce sempre lo stesso output; non vengono effettuate chiamate di rete, non c'è casualità.
- **Nativo per la CI:** codici di uscita, scorecard JSON e commenti PR progettati per pipeline automatizzate.

---

## Progetti

| Progetto | Descrizione | Stack | Distribuzione |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | Linter di accessibilità per l'output CLI: verifica che i messaggi di errore seguano modelli accessibili. | Python 3.10+ | solo codice sorgente |
| [a11y-ci](src/a11y-ci/) | Controllo CI per scorecard di accessibilità con rilevamento di regressioni e liste di elementi consentiti. | Python 3.10+ | solo codice sorgente |
| [a11y-assist](src/a11y-assist/) | Assistente CLI ottimizzato per utenti con problemi di vista, con cinque profili di accessibilità. | Python 3.10+ | solo codice sorgente |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Scanner HTML senza interfaccia utente con registrazioni della provenienza conformi alle specifiche. | Node.js 18+ | solo codice sorgente |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Server MCP per la cattura e la diagnosi di prove di accessibilità. | Node.js 18+ | solo codice sorgente |
| [a11y-demo-site](examples/a11y-demo-site/) | Sito di esempio con violazioni intenzionali per test end-to-end. | HTML | -- |

---

## Avvio rapido

### Analizza l'output CLI per individuare modelli accessibili

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Imposta dei controlli nella CI per le regressioni di accessibilità

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Esegue la scansione di HTML e registra la provenienza

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### Ottieni indicazioni per la correzione di un errore CLI

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Cattura prove ed esegui la diagnosi tramite MCP

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### Esegui il sito di esempio end-to-end

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### Esegui tutti i test localmente

```bash
npm test
# or
./scripts/verify.sh
```

Questo esegue pytest per i tre progetti Python, npm test per i due progetti Node.js e verifica i manuali.

---

## Architettura

I sei strumenti formano una pipeline che va dal rilevamento alla correzione:

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

**Flusso dei dati:**

1. **a11y-lint** esegue la scansione del testo CLI alla ricerca di modelli di messaggi di errore accessibili e produce una scorecard.
2. **a11y-evidence-engine** esegue la scansione dei file HTML ed emette risultati con registrazioni della provenienza conformi alle specifiche.
3. **a11y-ci** utilizza le scorecard, applica le soglie, rileva le regressioni e genera commenti PR.
4. **a11y-mcp-tools** racchiude la cattura delle prove e la diagnosi come strumenti MCP per l'integrazione con l'assistente AI.
5. **a11y-assist** utilizza i risultati (JSON strutturato o testo non elaborato) e genera indicazioni per la correzione in cinque profili di accessibilità.
6. **a11y-demo-site** collega tutto in un esempio eseguibile con violazioni intenzionali.

**Contratti condivisi:**

- `cli.error.schema.v0.1.json`: formato di errore strutturato utilizzato in tutti gli strumenti Python.
- `evidence.bundle.schema.v0.1.json`: pacchetti di prove con catene di provenienza.
- `.a11y_artifacts/`: directory di artefatti unificata per le pipeline CI.
- ID del metodo prov-spec: identificatori stabili e con controllo delle versioni per ogni passaggio della provenienza.

---

## Configurazione del client MCP

Per connettere a11y-mcp-tools al client MCP (Claude Desktop, Cursor, VS Code, ecc.):

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

Oppure, dopo `npm --prefix src/a11y-mcp-tools link`:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

Il server espone due strumenti:

| Strumento | Descrizione |
|------|-------------|
| `a11y.evidence` | Cattura pacchetti di prove inconfutabili da HTML, log CLI o altri input. |
| `a11y.diagnose` | Esegue controlli delle regole WCAG sui pacchetti di prove con verifica della provenienza. |

---

## Integrazione CI (GitHub Actions)

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

Consulta [GETTING_STARTED.md](GETTING_STARTED.md) per esempi e risoluzione dei problemi di Azure DevOps.

---

## Documentazione

| Documento | Descrizione |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Analisi approfondita dell'architettura, modelli di integrazione e guida allo sviluppo. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configurazione locale in tre passaggi, modelli CI e risoluzione dei problemi. |
| [CHANGELOG.md](CHANGELOG.md) | Cronologia delle versioni in formato Keep a Changelog. |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Strategia di directory di artefatti unificata. |
| [docs/prov-spec/](docs/prov-spec/) | Specifiche della provenienza. |

---

## Sicurezza e ambito dei dati

- **Dati a cui si accede:** legge i file HTML, l'output CLI e il JSON della scorecard per l'analisi dell'accessibilità. Cattura gli snapshot del DOM e genera pacchetti di prove.
- **Dati a cui NON si accede:** non vengono effettuate richieste di rete. Non viene raccolto alcun dato di telemetria. Non vengono archiviati dati utente. Non vengono archiviati credenziali o token.
- **Autorizzazioni richieste:** accesso in lettura ai file di destinazione. Accesso in scrittura per le directory di output delle prove/artefatti.

## Scorecard

| Controllo | Stato |
|------|--------|
| A. Baseline di sicurezza | PASSATO |
| B. Gestione degli errori | PASSATO |
| C. Documentazione per l'operatore | PASSATO |
| D. Pratiche di rilascio | PASSATO |
| E. Identità | PASSATO |

## Licenza

[MIT](LICENSE)

---

Realizzato da <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
