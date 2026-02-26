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

Sei strumenti. Un'unica missione: rendere i test di accessibilità verificabili, automatizzati e difficili da ignorare.

---

## Panoramica

La maggior parte degli strumenti di accessibilità si limita a indicare "hai 12 violazioni". Accessibility Suite va oltre: registra prove verificabili di ciò che è stato testato, integra i test di accessibilità nel tuo flusso di lavoro CI (Continuous Integration) e fornisce suggerimenti per la correzione, ottimizzati per utenti con problemi di vista, lettori di schermo, dislessia e per ridurre il carico cognitivo.

Questa suite copre l'intero ciclo di vita: analizza l'output della riga di comando per individuare modelli di accessibilità, esamina il codice HTML per rilevare violazioni delle linee guida WCAG, applica controlli di qualità nel flusso di lavoro CI e rende tutto disponibile tramite MCP (Metadata Center Protocol) in modo che gli assistenti AI possano partecipare al processo di correzione.

**Principi chiave:**

- **Prove, non semplici asserzioni:** ogni riscontro è supportato da un record di provenienza con checksum SHA-256 per garantirne l'integrità.
- **Priorità agli utenti con problemi di vista:** tutti gli strumenti della riga di comando utilizzano la convenzione `[OK]/[WARN]/[FAIL] + Cosa/Perché/Come risolvere`.
- **Determinismo:** lo stesso input produce sempre lo stesso output; non ci sono chiamate di rete né elementi casuali.
- **Integrazione nativa con CI:** codici di uscita, file JSON per i report e commenti per le richieste di pull (PR) progettati per i flussi di lavoro automatizzati.

---

## Progetti

| Progetto | Descrizione | Stack | Pacchetto |
| --------- | ------------- | ------- | --------- |
| [a11y-lint](src/a11y-lint/) | Analizzatore della riga di comando per individuare modelli di accessibilità nell'output -- verifica che i messaggi di errore seguano schemi accessibili. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | Controllo di accessibilità per i report CI con rilevamento di regressioni e liste di consentiti. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | Assistente per la riga di comando ottimizzato per utenti con problemi di vista, con cinque profili di accessibilità. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Scanner HTML senza interfaccia grafica con record di provenienza. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Server MCP per la raccolta di prove e la diagnosi di problemi di accessibilità. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | Sito dimostrativo con violazioni intenzionali per test end-to-end. | HTML | -- |

---

## Guida rapida

### Analizza l'output della riga di comando per individuare modelli di accessibilità

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Integra i test di accessibilità nel tuo flusso di lavoro CI per rilevare regressioni

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Scansiona il codice HTML e registra la provenienza dei dati

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### Ottieni suggerimenti per risolvere un errore della riga di comando

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Raccogli prove e diagnostica i problemi tramite MCP

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### Esegui il sito dimostrativo per test end-to-end

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## Architettura

I sei strumenti formano una pipeline che va dalla rilevazione alla correzione:

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

1. **a11y-lint** analizza il testo della riga di comando per individuare modelli di messaggi di errore accessibili e genera un report.
2. **a11y-evidence-engine** analizza i file HTML e segnala i problemi, registrando la provenienza dei dati.
3. **a11y-ci** elabora i report, applica le soglie, rileva le regressioni e genera commenti per le richieste di pull.
4. **a11y-mcp-tools** integra la raccolta di prove e la diagnosi come strumenti MCP per l'integrazione con gli assistenti AI.
5. **a11y-assist** riceve i risultati (in formato JSON strutturato o testo semplice) e genera suggerimenti per la correzione, basati su cinque profili di accessibilità.
6. **a11y-demo-site** mette insieme tutti gli elementi in un esempio funzionante con violazioni intenzionali.

**Interfacce standard:**

- `cli.error.schema.v0.1.json` -- formato standardizzato per i messaggi di errore in tutti gli strumenti Python.
- `evidence.bundle.schema.v0.1.json` -- pacchetti di prove con catene di provenienza.
- `.a11y_artifacts/` -- directory unificata per gli artefatti utilizzati nei flussi di lavoro CI.
- ID dei metodi di provenienza -- identificatori stabili e versionati per ogni passaggio di provenienza.

---

## Configurazione del client MCP

Per collegare a11y-mcp-tools al tuo client MCP (Claude Desktop, Cursor, VS Code, ecc.):

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

Oppure, se installato globalmente:

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

| Tool | Descrizione |
| ------ | ------------- |
| `a11y.evidence` | Acquisizione di pacchetti di prove con protezione anti-manomissione da HTML, log della riga di comando o altre fonti. |
| `a11y.diagnose` | Esecuzione di controlli delle regole WCAG sui pacchetti di prove con verifica della provenienza. |

---

## Integrazione con CI (GitHub Actions)

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

Consultare il file [GETTING_STARTED.md](GETTING_STARTED.md) per esempi di Azure DevOps e per la risoluzione dei problemi.

---

## Documentazione

| Documento. | Descrizione. |
| ---------- | ------------- |
| [HANDBOOK.md](HANDBOOK.md) | Analisi approfondita dell'architettura, modelli di integrazione e guida per gli sviluppatori. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configurazione locale con tre comandi, modelli CI e risoluzione dei problemi. |
| [CHANGELOG.md](CHANGELOG.md) | Cronologia delle release in formato "Keep a Changelog". |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Strategia unificata per la directory degli artefatti. |
| [docs/prov-spec/](docs/prov-spec/) | Specifiche della provenienza. |

---

## Licenza

[MIT](LICENSE)
