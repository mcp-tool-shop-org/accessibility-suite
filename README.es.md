<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/accessibility-suite/readme.png" alt="Accessibility Suite" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/accessibility-suite/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/accessibility-suite/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

Seis herramientas. Una misión: hacer que las pruebas de accesibilidad sean verificables, automatizadas y difíciles de ignorar.

> **Ejecutar desde el código fuente.** Nada de este conjunto se ha publicado todavía en npm o PyPI. Cada comando
> a continuación se instala desde este repositorio. Los nombres de los paquetes en el `package.json` y
> `pyproject.toml` de cada herramienta son los nombres previstos para su publicación, no enlaces que pueda instalar hoy.

---

## De un vistazo

La mayoría de las herramientas de accesibilidad se detienen en "tiene 12 infracciones". El conjunto de herramientas de accesibilidad va más allá: captura pruebas irrefutables de lo que se ha probado, establece límites en su canal de CI en caso de regresiones y proporciona orientación para la corrección, adaptada a perfiles de baja visión, lectores de pantalla, dislexia y carga cognitiva.

El conjunto de herramientas abarca todo el ciclo de vida: analiza la salida de la CLI en busca de patrones accesibles, examina el HTML en busca de infracciones de WCAG con pruebas criptográficas, aplica límites de calidad en CI y expone todo a través de MCP para que los asistentes de IA puedan participar en el ciclo de corrección.

**Principios clave:**

- **Evidencia sobre afirmaciones:** cada hallazgo está respaldado por un registro de procedencia prov-spec con resúmenes de integridad SHA-256.
- **Salida optimizada para personas con baja visión:** todas las herramientas de la CLI utilizan el contrato `[OK]/[WARN]/[FAIL] + What/Why/Fix`.
- **Determinista:** la misma entrada siempre produce la misma salida; no hay llamadas a la red, ni aleatoriedad.
- **Nativa de CI:** códigos de salida, JSON de puntuación y comentarios de PR diseñados para canalizaciones automatizadas.

---

## Proyectos

| Proyecto | Descripción | Pila tecnológica | Distribución |
|---------|-------------|-------|--------------|
| [a11y-lint](src/a11y-lint/) | Analizador de accesibilidad para la salida de la CLI: valida que los mensajes de error sigan patrones accesibles. | Python 3.10+ | solo código fuente |
| [a11y-ci](src/a11y-ci/) | Límite de CI para las puntuaciones de accesibilidad con detección de regresiones y listas de permitidos. | Python 3.10+ | solo código fuente |
| [a11y-assist](src/a11y-assist/) | Asistente de CLI optimizado para personas con baja visión con cinco perfiles de accesibilidad. | Python 3.10+ | solo código fuente |
| [a11y-evidence-engine](src/a11y-evidence-engine/) | Escáner HTML sin interfaz gráfica con registros de procedencia prov-spec. | Node.js 18+ | solo código fuente |
| [a11y-mcp-tools](src/a11y-mcp-tools/) | Servidor MCP para la captura y el diagnóstico de pruebas de accesibilidad. | Node.js 18+ | solo código fuente |
| [a11y-demo-site](examples/a11y-demo-site/) | Sitio de demostración con infracciones intencionales para pruebas de extremo a extremo. | HTML | -- |

---

## Primeros pasos

### Analizar la salida de la CLI en busca de patrones accesibles

```bash
pip install a11y-lint
a11y-lint scan output.txt
```

### Establecer límites en su CI en caso de regresiones de accesibilidad

```bash
pip install ./src/a11y-lint ./src/a11y-ci
a11y-lint scan . --artifact-dir .a11y_artifacts
a11y-ci gate --artifact-dir .a11y_artifacts
```

### Escanear HTML y capturar la procedencia

```bash
npm --prefix src/a11y-evidence-engine install
node src/a11y-evidence-engine/bin/a11y-engine.js scan ./html --out ./results
```

### Obtener orientación para la corrección de un error de la CLI

```bash
pip install ./src/a11y-assist
a11y-assist explain --json error.json --profile screen-reader
```

### Capturar pruebas y diagnosticar a través de MCP

```bash
npm --prefix src/a11y-mcp-tools install
node src/a11y-mcp-tools/bin/cli.js evidence --target page.html --dom-snapshot --out evidence.json
node src/a11y-mcp-tools/bin/cli.js diagnose --bundle evidence.json --verify-provenance --fix
```

### Ejecutar el sitio de demostración de extremo a extremo

```bash
cd examples/a11y-demo-site
./scripts/a11y.sh
```

### Ejecutar todas las pruebas localmente

```bash
npm test
# or
./scripts/verify.sh
```

Esto ejecuta pytest para los tres proyectos de Python, npm test para los dos proyectos de Node.js y verifica los manuales.

---

## Arquitectura

Las seis herramientas forman una canalización desde la detección hasta la corrección:

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

1. **a11y-lint** analiza el texto de la CLI en busca de patrones de mensajes de error accesibles y genera una puntuación.
2. **a11y-evidence-engine** analiza los archivos HTML y emite hallazgos con registros de procedencia prov-spec.
3. **a11y-ci** consume las puntuaciones, aplica los límites, detecta las regresiones y genera comentarios de PR.
4. **a11y-mcp-tools** encapsula la captura de pruebas y el diagnóstico como herramientas MCP para la integración con el asistente de IA.
5. **a11y-assist** toma los hallazgos (JSON estructurado o texto sin formato) y genera orientación para la corrección en cinco perfiles de accesibilidad.
6. **a11y-demo-site** lo une todo como un ejemplo ejecutable con infracciones intencionales.

**Contratos compartidos:**

- `cli.error.schema.v0.1.json`: formato de error estructurado en todas las herramientas de Python.
- `evidence.bundle.schema.v0.1.json`: paquetes de pruebas con cadenas de procedencia.
- `.a11y_artifacts/`: directorio de artefactos unificado para las canalizaciones de CI.
- ID de método prov-spec: identificadores estables y con versiones para cada paso de la procedencia.

---

## Configuración del cliente MCP

Para conectar a11y-mcp-tools a su cliente MCP (Claude Desktop, Cursor, VS Code, etc.):

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

O, después de `npm --prefix src/a11y-mcp-tools link`:

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
| `a11y.evidence` | Capturar paquetes de pruebas irrefutables de HTML, registros de la CLI u otras entradas. |
| `a11y.diagnose` | Ejecutar comprobaciones de las reglas de WCAG sobre los paquetes de pruebas con verificación de la procedencia. |

---

## Integración de CI (GitHub Actions)

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

Consulte [GETTING_STARTED.md](GETTING_STARTED.md) para obtener ejemplos de Azure DevOps y solución de problemas.

---

## Documentación

| Documento | Descripción |
|----------|-------------|
| [HANDBOOK.md](HANDBOOK.md) | Análisis detallado de la arquitectura, patrones de integración y guía de desarrollo. |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Configuración local de tres comandos, plantillas de CI y solución de problemas. |
| [CHANGELOG.md](CHANGELOG.md) | Historial de versiones en formato Keep a Changelog. |
| [docs/unified-artifacts.md](docs/unified-artifacts.md) | Estrategia de directorio de artefactos unificado. |
| [docs/prov-spec/](docs/prov-spec/) | Especificación de procedencia. |

---

## Seguridad y alcance de los datos

- **Datos a los que se accede:** Lee archivos HTML, la salida de la CLI y el JSON de la puntuación para el análisis de accesibilidad. Captura instantáneas del DOM y genera paquetes de pruebas.
- **Datos a los que NO se accede:** No hay solicitudes de red. No hay telemetría. No hay almacenamiento de datos de usuario. No hay credenciales ni tokens.
- **Permisos requeridos:** Acceso de lectura a los archivos de destino. Acceso de escritura para los directorios de salida de pruebas/artefactos.

## Puntuación

| Límite | Estado |
|------|--------|
| A. Línea de base de seguridad | APROBADO |
| B. Manejo de errores | APROBADO |
| C. Documentación del operador | APROBADO |
| D. Buenas prácticas de envío | APROBADO |
| E. Identidad | APROBADO |

## Licencia

[MIT](LICENSE)

---

Creado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
