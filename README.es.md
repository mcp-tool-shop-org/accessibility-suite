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

Seis herramientas. Una misión: hacer que las pruebas de accesibilidad sean verificables, automatizadas y difíciles de ignorar.

---

## En resumen

La mayoría de las herramientas de accesibilidad se limitan a indicar "tiene 12 infracciones". El conjunto de herramientas de accesibilidad va más allá: captura evidencia verificable de lo que se ha probado, integra las pruebas en su canal de integración continua (CI) para detectar regresiones y proporciona sugerencias de corrección adaptadas a perfiles de baja visión, lectores de pantalla, dislexia y carga cognitiva.

Este conjunto de herramientas abarca todo el ciclo de vida: analiza la salida de la línea de comandos (CLI) en busca de patrones accesibles, analiza el código HTML en busca de infracciones de las WCAG con información de origen verificable, aplica controles de calidad en el CI y expone todo a través de MCP para que los asistentes de IA puedan participar en el proceso de corrección.

**Principios clave:**

- **Evidencia sobre afirmaciones:** cada resultado está respaldado por un registro de origen verificable con sumas de comprobación de integridad SHA-256.
- **Salida prioritaria para personas con baja visión:** todas las herramientas de la línea de comandos utilizan el contrato `[OK]/[WARN]/[FAIL] + ¿Qué/Por qué/Cómo solucionar?`.
- **Determinista:** la misma entrada siempre produce la misma salida; no hay llamadas a la red, ni aleatoriedad.
- **Nativo de CI:** códigos de salida, archivos JSON de puntuación y comentarios de solicitudes de extracción (PR) diseñados para canales de automatización.

---

## Proyectos

| Proyecto | Descripción | Stack | Paquete |
| --------- | ------------- | ------- | --------- |
| [a11y-lint](src/a11y-lint/) | Analizador de la línea de comandos (CLI) para detectar patrones accesibles en la salida: valida que los mensajes de error sigan patrones accesibles. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | Control de calidad (gate) para las puntuaciones de accesibilidad en el CI, con detección de regresiones y listas de permisos. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | Asistente de la línea de comandos (CLI) priorizado para personas con baja visión, con cinco perfiles de accesibilidad. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Analizador de código HTML sin interfaz gráfica con registros de origen verificable. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Servidor MCP para la captura y el diagnóstico de evidencia de accesibilidad. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | Sitio de demostración con infracciones intencionales para pruebas de extremo a extremo. | HTML | -- |

---

## Cómo empezar

### Analiza la salida de la línea de comandos (CLI) en busca de patrones accesibles

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Integra las pruebas de accesibilidad en tu canal de integración continua (CI) para detectar regresiones

```bash
pip install a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Analiza el código HTML y captura la información de origen

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### Obtén sugerencias de corrección para un error en la línea de comandos

```bash
pip install a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Captura evidencia y realiza diagnósticos a través de MCP

```bash
npm install -g @mcptoolshop/a11y-mcp-tools
a11y evidence --target page.html --dom-snapshot --out evidence.json
a11y diagnose --bundle evidence.json --verify-provenance --fix
```

### Ejecuta el sitio de demostración de extremo a extremo

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

---

## Arquitectura

Las seis herramientas forman una cadena de procesamiento desde la detección hasta la corrección:

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

**Flujo de datos:**

1. **a11y-lint** analiza el texto de la línea de comandos (CLI) en busca de patrones de mensajes de error accesibles y genera un informe de puntuación.
2. **a11y-evidence-engine** analiza archivos HTML y genera resultados con registros de origen verificable.
3. **a11y-ci** consume los informes de puntuación, aplica umbrales, detecta regresiones y genera comentarios para solicitudes de extracción (PR).
4. **a11y-mcp-tools** integra la captura de evidencia y el diagnóstico como herramientas MCP para la integración con asistentes de IA.
5. **a11y-assist** toma los resultados (JSON estructurado o texto sin formato) y genera sugerencias de corrección en cinco perfiles de accesibilidad.
6. **a11y-demo-site** integra todo como un ejemplo funcional con infracciones intencionales.

**Contratos comunes:**

- `cli.error.schema.v0.1.json` -- formato de error estructurado para todas las herramientas de Python.
- `evidence.bundle.schema.v0.1.json` -- paquetes de evidencia con cadenas de origen.
- `.a11y_artifacts/` -- directorio unificado de artefactos para canales de CI.
- ID de métodos prov-spec -- identificadores estables y versionados para cada paso de origen.

---

## Configuración del cliente MCP

Para conectar a11y-mcp-tools a tu cliente MCP (Claude Desktop, Cursor, VS Code, etc.):

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

O si está instalado globalmente:

```json
{
  "mcpServers": {
    "a11y": {
      "command": "a11y-mcp"
    }
  }
}
```

El servidor expone dos herramientas:

| Tool | Descripción |
| ------ | ------------- |
| `a11y.evidence` | Captura paquetes de evidencia con protección contra manipulación desde HTML, registros de la línea de comandos u otras fuentes. |
| `a11y.diagnose` | Realiza comprobaciones de las normas WCAG sobre los paquetes de evidencia, con verificación de su origen. |

---

## Integración con CI (GitHub Actions)

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

Consulte [GETTING_STARTED.md](GETTING_STARTED.md) para obtener ejemplos de Azure DevOps y para solucionar problemas.

---

## Documentación

| Documento. | Descripción. |
| ---------- | ------------- |
| [HANDBOOK.md](HANDBOOK.md) | Análisis profundo de la arquitectura, patrones de integración y guía de desarrollo. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuración local con tres comandos, plantillas de CI y solución de problemas. |
| [CHANGELOG.md](CHANGELOG.md) | Historial de versiones en formato "Keep a Changelog". |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Estrategia unificada para el directorio de artefactos. |
| [docs/prov-spec/](docs/prov-spec/) | Especificación de origen. |

---

## Licencia

[MIT](LICENSE)
