<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.md">English</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

Six outils. Une mission : rendre les tests d’accessibilité vérifiables, automatisés et impossibles à ignorer.

> **Exécution à partir du code source.** Aucun élément de cette suite n’est encore publié sur npm ou PyPI. Chaque commande ci-dessous s’installe à partir de ce dépôt. Les noms des paquets dans le `package.json` et le `pyproject.toml` de chaque outil sont les noms publiés prévus, et non des liens sur lesquels vous pouvez installer aujourd’hui.

---

## En bref

La plupart des outils d’accessibilité s’arrêtent à « vous avez 12 violations ». La suite d’accessibilité va plus loin : elle capture des preuves infalsifiables de ce qui a été testé, elle conditionne votre pipeline CI en fonction des régressions et elle propose des conseils de correction adaptés aux profils de basse vision, de lecteurs d’écran, de dyslexie et de charge cognitive.

La suite couvre l’ensemble du cycle de vie : analyse de la sortie CLI pour détecter les modèles accessibles, analyse du HTML pour détecter les violations WCAG avec une preuve cryptographique, application de règles de qualité dans le CI et exposition de tout via MCP afin que les assistants d’IA puissent participer à la boucle de correction.

**Principes clés :**

- **Preuves plutôt qu’affirmations** : chaque résultat est étayé par un enregistrement de provenance conforme à la spécification prov-spec, avec des hachages d’intégrité SHA-256.
- **Sortie optimisée pour la basse vision** : tous les outils CLI utilisent le contrat `[OK]/[WARN]/[FAIL] + What/Why/Fix`.
- **Déterministe** : la même entrée produit toujours la même sortie ; aucune requête réseau, aucun caractère aléatoire.
- **Intégré au CI** : codes de sortie, scorecard JSON et commentaires PR conçus pour les pipelines automatisés.

---

## Projets

| Projet | Description | Pile technologique | Distribution |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | Analyseur d’accessibilité pour la sortie CLI : valide que les messages d’erreur respectent les modèles accessibles. | Python 3.10+ | uniquement le code source |
| [a11y-ci](src/a11y-ci/) | Règle CI pour les scorecards d’accessibilité avec détection des régressions et listes d’autorisation. | Python 3.10+ | uniquement le code source |
| [a11y-assist](src/a11y-assist/) | Assistant CLI optimisé pour la basse vision avec cinq profils d’accessibilité. | Python 3.10+ | uniquement le code source |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Analyseur HTML sans interface graphique avec des enregistrements de provenance conformes à la spécification prov-spec. | Node.js 18+ | uniquement le code source |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Serveur MCP pour la capture et le diagnostic des preuves d’accessibilité. | Node.js 18+ | uniquement le code source |
| [a11y-demo-site](examples/a11y-demo-site/) | Site de démonstration avec des violations intentionnelles pour les tests de bout en bout. | HTML | -- |

---

## Démarrage rapide

### Analyse de la sortie CLI pour détecter les modèles accessibles

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Conditionnez votre CI en fonction des régressions d’accessibilité

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Analyse du HTML et capture de la provenance

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### Obtenez des conseils de correction pour une erreur CLI

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Capturez des preuves et effectuez un diagnostic via MCP

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### Exécutez le site de démonstration de bout en bout

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### Exécutez tous les tests localement

```bash
npm test
# or
./scripts/verify.sh
```

Cela exécute pytest pour les trois projets Python, npm test pour les deux projets Node.js et vérifie les manuels.

---

## Architecture

Les six outils forment un pipeline allant de la détection à la correction :

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

1. **a11y-lint** analyse le texte CLI pour détecter les modèles de messages d’erreur accessibles et produit un scorecard.
2. **a11y-evidence-engine** analyse les fichiers HTML et émet des résultats avec des enregistrements de provenance conformes à la spécification prov-spec.
3. **a11y-ci** consomme les scorecards, applique les seuils, détecte les régressions et génère des commentaires PR.
4. **a11y-mcp-tools** encapsule la capture des preuves et le diagnostic en tant qu’outils MCP pour l’intégration des assistants d’IA.
5. **a11y-assist** prend les résultats (JSON structuré ou texte brut) et génère des conseils de correction dans cinq profils d’accessibilité.
6. **a11y-demo-site** rassemble le tout dans un exemple exécutable avec des violations intentionnelles.

**Contrats partagés :**

- `cli.error.schema.v0.1.json` : format d’erreur structuré pour tous les outils Python.
- `evidence.bundle.schema.v0.1.json` : ensembles de preuves avec des chaînes de provenance.
- `.a11y_artifacts/` : répertoire d’artefacts unifié pour les pipelines CI.
- ID de méthode prov-spec : identifiants stables et versionnés pour chaque étape de la provenance.

---

## Configuration du client MCP

Pour connecter a11y-mcp-tools à votre client MCP (Claude Desktop, Cursor, VS Code, etc.) :

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

Ou, après `npm --prefix src/a11y-mcp-tools link` :

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
| `a11y.evidence` | Capturez des ensembles de preuves infalsifiables à partir du HTML, des journaux CLI ou d’autres entrées. |
| `a11y.diagnose` | Exécutez des vérifications des règles WCAG sur les ensembles de preuves avec une vérification de la provenance. |

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

Consultez [GETTING_STARTED.md](GETTING_STARTED.md) pour obtenir des exemples et des conseils de dépannage pour Azure DevOps.

---

## Documentation

| Document | Description |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Analyse approfondie de l’architecture, modèles d’intégration et guide de développement. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuration locale en trois étapes, modèles CI et dépannage. |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions au format Keep a Changelog. |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Stratégie de répertoire d’artefacts unifié. |
| [docs/prov-spec/](docs/prov-spec/) | Spécification de la provenance. |

---

## Sécurité et portée des données

- **Données consultées** : lit les fichiers HTML, la sortie CLI et le scorecard JSON pour l’analyse de l’accessibilité. Capture les instantanés du DOM et génère des ensembles de preuves.
- **Données NON consultées** : aucune requête réseau. Pas de télémétrie. Pas de stockage des données utilisateur. Pas d’informations d’identification ou de jetons.
- **Autorisations requises** : accès en lecture aux fichiers cibles. Accès en écriture pour les répertoires de sortie des preuves/artefacts.

## Scorecard

| Règle | Statut |
|------|--------|
| A. Base de sécurité | PASSÉ |
| B. Gestion des erreurs | PASSÉ |
| C. Documentation pour les opérateurs | PASSÉ |
| D. Bonnes pratiques de publication | PASSÉ |
| E. Identité | PASSÉ |

## Licence

[MIT](LICENSE)

---

Créé par <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
