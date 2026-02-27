<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

## Resumen

La mayoría de las herramientas de accesibilidad se limitan a indicar "tiene 12 infracciones". El conjunto de herramientas de accesibilidad va más allá: captura evidencia verificable de lo que se ha probado, integra las pruebas en su canal de integración continua (CI) para detectar regresiones y proporciona sugerencias de corrección adaptadas a perfiles de baja visión, lectores de pantalla, dislexia y carga cognitiva.

Este conjunto de herramientas abarca todo el ciclo de vida: analiza la salida de la línea de comandos (CLI) en busca de patrones accesibles, escanea el código HTML en busca de infracciones de las WCAG con información de procedencia criptográfica, aplica controles de calidad en el CI y expone todo a través de MCP para que los asistentes de IA puedan participar en el proceso de corrección.

**Principios clave:**

- **Evidencia sobre afirmaciones:** cada resultado está respaldado por un registro de procedencia con sumas de verificación SHA-256.
- **Salida optimizada para baja visión:** todas las herramientas de la línea de comandos utilizan el contrato `[OK]/[WARN]/[FAIL] + ¿Qué/Por qué/Cómo solucionar?`.
- **Determinista:** la misma entrada siempre produce la misma salida; no hay llamadas a la red, ni aleatoriedad.
- **Nativo de CI:** códigos de salida, archivos JSON de puntuación y comentarios de solicitudes de extracción (PR) diseñados para canales de automatización.

---

## Proyectos

| Proyecto | Descripción | Entorno | Paquete |
|---------|-------------|-------|---------|
| [a11y-lint](src/a11y-lint/) | Analizador de accesibilidad para la salida de la línea de comandos: valida que los mensajes de error sigan patrones accesibles. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-lint/) |
| [a11y-ci](src/a11y-ci/) | Control de calidad para puntuaciones de accesibilidad en el CI, con detección de regresiones y listas de permisos. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-ci/) / [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-ci) |
| [a11y-assist](src/a11y-assist/) | Asistente de línea de comandos optimizado para baja visión, con cinco perfiles de accesibilidad. | Python 3.10+ | [PyPI](https://pypi.org/project/a11y-assist/) |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Escáner HTML sin interfaz gráfica con registros de procedencia. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-evidence-engine) |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Servidor MCP para la captura y el diagnóstico de evidencia de accesibilidad. | Node.js 18+ | [npm](https://www.npmjs.com/package/@mcptoolshop/a11y-mcp-tools) |
| [a11y-demo-site](examples/a11y-demo-site/) | Sitio de demostración con infracciones intencionales para pruebas de extremo a extremo. | HTML | -- |

---

## Cómo empezar

### Analiza la salida de la línea de comandos en busca de patrones accesibles

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

### Escanea el código HTML y captura la información de procedencia

```bash
npm install -g @mcptoolshop/a11y-evidence-engine
a11y-engine scan ./html --out ./results
```

### Obtén sugerencias de corrección para un error de la línea de comandos

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

1. **a11y-lint** analiza el texto de la línea de comandos en busca de patrones de mensajes de error accesibles y genera un informe de puntuación.
2. **a11y-evidence-engine** analiza archivos HTML y genera resultados con registros de procedencia.
3. **a11y-ci** consume los informes de puntuación, aplica umbrales, detecta regresiones y genera comentarios para solicitudes de extracción (PR).
4. **a11y-mcp-tools** encapsula la captura de evidencia y el diagnóstico como herramientas MCP para la integración con asistentes de IA.
5. **a11y-assist** toma los resultados (JSON estructurado o texto sin formato) y genera sugerencias de corrección en cinco perfiles de accesibilidad.
6. **a11y-demo-site** integra todo como un ejemplo funcional con infracciones intencionales.

**Contratos comunes:**

- `cli.error.schema.v0.1.json`: formato de error estructurado para todas las herramientas de Python.
- `evidence.bundle.schema.v0.1.json`: paquetes de evidencia con cadenas de procedencia.
- `.a11y_artifacts/`: directorio unificado de artefactos para canales de integración continua (CI).
- ID de métodos de procedencia: identificadores estables y versionados para cada paso de la procedencia.

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

O, si está instalado globalmente:

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

| Herramienta | Descripción |
|------|-------------|
| `a11y.evidence` | Captura paquetes de evidencia verificable desde HTML, registros de la línea de comandos u otras fuentes. |
| `a11y.diagnose` | Ejecuta comprobaciones de reglas WCAG sobre paquetes de evidencia con verificación de procedencia. |

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

Consulte [GETTING_STARTED.md](GETTING_STARTED.md) para ver ejemplos de Azure DevOps y solucionar problemas.

---

## Documentación

| Documento | Descripción |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Análisis profundo de la arquitectura, patrones de integración y guía de desarrollo. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuración local con tres comandos, plantillas de CI y solución de problemas. |
| [CHANGELOG.md](CHANGELOG.md) | Historial de versiones en formato Keep a Changelog. |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Estrategia unificada de directorio de artefactos. |
| [docs/prov-spec/](docs/prov-spec/) | Especificación de trazabilidad. |

---

## Seguridad y alcance de los datos

- **Datos accedidos:** Lee archivos HTML, la salida de la línea de comandos y archivos JSON de la evaluación de accesibilidad. Captura instantáneas del DOM y genera paquetes de evidencia.
- **Datos NO accedidos:** No hay solicitudes de red. No hay telemetría. No se almacenan datos de usuario. No hay credenciales ni tokens.
- **Permisos requeridos:** Acceso de lectura a los archivos de destino. Acceso de escritura para los directorios de salida de evidencia/artefactos.

## Evaluación

| Puerta de control | Estado |
|------|--------|
| A. Línea base de seguridad | PASADO |
| B. Manejo de errores | PASADO |
| C. Documentación del operador | PASADO |
| D. Higiene de la entrega | PASADO |
| E. Identidad | PASADO |

## Licencia

[MIT](LICENSE)

---

Creado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
