<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

Six outils. Une mission : rendre les tests d'accessibilité vérifiables, automatisés et difficiles à ignorer.

---

## Aperçu

La plupart des outils d'accessibilité se limitent à indiquer "vous avez 12 violations". La suite d'outils pour l'accessibilité va plus loin : elle enregistre des preuves infalsifiables de ce qui a été testé, elle intègre les tests d'accessibilité dans votre pipeline CI pour détecter les régressions, et elle fournit des conseils de correction adaptés aux profils de personnes ayant une faible vision, utilisant des lecteurs d'écran, atteintes de dyslexie ou ayant des difficultés cognitives.

Cette suite couvre l'ensemble du cycle de vie : analyse de la sortie de la ligne de commande pour détecter les modèles d'accessibilité, analyse du code HTML pour détecter les violations des directives WCAG avec une provenance cryptographique, application de règles de qualité dans le pipeline CI, et exposition de toutes ces informations via MCP afin que les assistants IA puissent participer au processus de correction.

**Principes clés :**

- **Preuves plutôt que simples affirmations** : chaque constatation est étayée par un enregistrement de provenance avec des sommes de contrôle SHA-256 garantissant l'intégrité.
- **Conception axée sur les personnes ayant une faible vision** : tous les outils de ligne de commande utilisent le format `[OK]/[WARN]/[FAIL] + Quoi/Pourquoi/Comment corriger`.
- **Déterminisme** : la même entrée produit toujours la même sortie ; pas d'appels réseau, pas de hasard.
- **Intégration native avec les systèmes CI** : codes de sortie, fichiers JSON de score, et commentaires pour les demandes de tirage, conçus pour les pipelines automatisés.

---

## Projets

| Projet | Description | Environnement | Package |
|---------|-------------|-------|---------|
| [a11y-lint](src/a11y-lint/) | Analyseur d'accessibilité pour la sortie de la ligne de commande : valide que les messages d'erreur suivent les modèles d'accessibilité. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | Vérificateur d'accessibilité pour les pipelines CI, avec détection de régressions et listes blanches. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | Assistant de ligne de commande axé sur les personnes ayant une faible vision, avec cinq profils d'accessibilité. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Analyseur HTML sans interface graphique, avec enregistrements de provenance. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Serveur MCP pour la capture et le diagnostic des problèmes d'accessibilité. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | Site de démonstration avec des violations intentionnelles pour les tests de bout en bout. | HTML | -- |

---

## Démarrage rapide

### Analyse de la sortie de la ligne de commande pour détecter les modèles d'accessibilité

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Intégration des tests d'accessibilité dans votre pipeline CI pour détecter les régressions

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Analyse du code HTML et capture de la provenance

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### Obtention de conseils de correction pour une erreur de la ligne de commande

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Capture de preuves et diagnostic via MCP

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### Exécution du site de démonstration de bout en bout

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## Architecture

Les six outils forment une chaîne de traitement, de la détection à la correction :

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

**Flux de données :**

1. **a11y-lint** analyse le texte de la ligne de commande pour détecter les modèles d'erreur d'accessibilité et génère un rapport.
2. **a11y-evidence-engine** analyse les fichiers HTML et génère des rapports avec des enregistrements de provenance.
3. **a11y-ci** utilise les rapports, applique des seuils, détecte les régressions et génère des commentaires pour les demandes de tirage.
4. **a11y-mcp-tools** encapsule la capture de preuves et le diagnostic en tant qu'outils MCP pour l'intégration avec les assistants IA.
5. **a11y-assist** prend les rapports (JSON structuré ou texte brut) et génère des conseils de correction en fonction de cinq profils d'accessibilité.
6. **a11y-demo-site** regroupe tout cela dans un exemple exécutable avec des violations intentionnelles.

**Interfaces standardisées :**

- `cli.error.schema.v0.1.json` : format d'erreur structuré utilisé par tous les outils Python.
- `evidence.bundle.schema.v0.1.json` : format des ensembles de preuves avec chaînes de provenance.
- `.a11y_artifacts/` : répertoire unifié pour les artefacts utilisés dans les pipelines CI.
- Identifiants de méthode de provenance : identifiants stables et versionnés pour chaque étape de la provenance.

---

## Configuration du client MCP

Pour connecter a11y-mcp-tools à votre client MCP (Claude Desktop, Cursor, VS Code, etc.) :

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

Ou si installé globalement :

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

Le serveur expose deux outils :

| Outil | Description |
|------|-------------|
| `a11y.evidence` | Capture des ensembles de preuves infalsifiables à partir de HTML, de journaux de la ligne de commande ou d'autres sources. |
| `a11y.diagnose` | Exécution de vérifications des règles WCAG sur les ensembles de preuves avec vérification de la provenance. |

---

## Intégration CI (GitHub Actions)

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

Consultez [GETTING_STARTED.md](GETTING_STARTED.md) pour des exemples Azure DevOps et des conseils de dépannage.

---

## Documentation

| Document | Description |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Analyse approfondie de l'architecture, modèles d'intégration et guide de développement. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuration locale en trois étapes, modèles CI et conseils de dépannage. |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions au format Keep a Changelog. |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Stratégie de répertoire unifié pour les artefacts. |
| [docs/prov-spec/](docs/prov-spec/) | Spécification de la provenance. |

---

## Sécurité et portée des données

- **Données accessibles :** Lecture de fichiers HTML, de la sortie de l'interface en ligne de commande (CLI) et de fichiers JSON de score pour l'analyse de l'accessibilité. Capture d'instantanés du DOM et génération de paquets de preuves.
- **Données non accessibles :** Aucune requête réseau. Aucune télémétrie. Aucun stockage de données utilisateur. Aucun identifiant ou jeton.
- **Autorisations requises :** Accès en lecture aux fichiers cibles. Accès en écriture pour les répertoires de sortie des preuves/artefacts.

## Score

| Portail | Statut |
|------|--------|
| A. Base de sécurité | PASSÉ |
| B. Gestion des erreurs | PASSÉ |
| C. Documentation de l'opérateur | PASSÉ |
| D. Qualité du code | PASSÉ |
| E. Identité | PASSÉ |

## Licence

[MIT](LICENSE)

---

Créé par <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
