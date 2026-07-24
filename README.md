# ORION — Hacking Ético y Ciberseguridad Profesional

[![ORION](https://img.shields.io/badge/ORION-PLUGIN%20RUNTIME-111827?style=for-the-badge)](docs/PLUGIN_SYSTEM.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](pyproject.toml)
[![Security](https://img.shields.io/badge/SECURITY-AUTHORIZED%20ONLY-B91C1C?style=for-the-badge)](#uso-ético-y-autorizado)

**ORION** es un framework extensible para ciberseguridad defensiva, auditoría autorizada, gestión de hallazgos y automatización segura con agentes de IA.

La versión 1.0 transforma las antiguas *skills* descriptivas en **plugins funcionales completos**: instalables, descubribles, tipados, validados, ejecutables desde CLI y preparados para integraciones con agentes o servidores MCP.

## Qué cambia en ORION 1.0

Antes, `skills/skills.json` describía scripts de manera manual. Ahora el repositorio incorpora:

- runtime real de plugins;
- contratos de entrada y salida mediante JSON Schema;
- autorización obligatoria antes de ejecutar;
- permisos separados para red y efectos externos;
- descubrimiento automático de plugins de terceros;
- CLI unificada `orion plugins`;
- resultados JSON auditables con `request_id`, actor, versión y duración;
- procesamiento concurrente con límites seguros;
- pruebas unitarias, type checking, lint y build de paquete en CI;
- manifiesto generado desde el código ejecutable para evitar desincronización.

## Uso ético y autorizado

Este proyecto se proporciona exclusivamente para:

- defensa, hardening y validación de controles;
- auditorías con permiso explícito y por escrito;
- laboratorios controlados;
- OSINT ético y análisis de indicadores;
- AppSec, DFIR, detección y gestión responsable de vulnerabilidades;
- automatización de reportes y remediación aprobada.

No debe utilizarse para acceso no autorizado, malware, phishing real, persistencia, evasión, robo de credenciales, interrupción de servicios ni acciones fuera del alcance aprobado.

Una referencia introducida con `--authorization` mejora la trazabilidad, pero **no sustituye** un permiso legal válido, un Rules of Engagement o unos Terms of Reference.

## Arquitectura

```text
ORION
├── orion/
│   ├── SKILL.md                  # Sistema de conocimiento y guardrails
│   ├── playbooks/                # Metodologías operativas
│   ├── references/               # Referencias técnicas por dominio
│   ├── scripts/                  # Motores de automatización existentes
│   ├── plugins/
│   │   ├── core.py               # Contratos, policy, registry y runtime
│   │   └── builtin.py            # Plugins oficiales
│   └── cli.py                    # CLI unificada
├── skills/
│   ├── skills.json               # Manifiesto generado desde el runtime
│   └── plugin.schema.json        # Schema del manifiesto
├── samples/                      # Entradas reproducibles
├── tests/                        # Pruebas del runtime y guardrails
└── .github/workflows/plugin-ci.yml
```

El flujo general es:

```text
AUTORIZACIÓN
    ↓
SELECCIÓN DEL PLUGIN
    ↓
VALIDACIÓN JSON SCHEMA
    ↓
POLÍTICA DE RED / SIDE EFFECTS
    ↓
EJECUCIÓN DEL MOTOR
    ↓
VALIDACIÓN DE SALIDA
    ↓
RESULTADO JSON AUDITABLE
```

## Instalación

```bash
python -m pip install -e ".[dev]"
```

El paquete requiere Python 3.10 o superior porque el proyecto utiliza sintaxis moderna de tipos y entry points estándar.

## CLI

### Listar plugins

```bash
orion plugins list
orion plugins list --json
```

### Inspeccionar un contrato

```bash
orion plugins describe ioc_enricher
```

### Diagnosticar el runtime

```bash
orion plugins doctor
```

### Regenerar el manifiesto

```bash
orion plugins export-manifest --output skills/skills.json
```

## Plugins oficiales

### IOC Enricher

Clasifica IOCs, ejecuta resolución DNS y permite enriquecimiento externo opcional mediante las integraciones ya soportadas.

```bash
orion plugins run ioc_enricher \
  --input samples/ioc-plugin-request.json \
  --authorization "TOR-2026-ORION-001" \
  --actor "security-team" \
  --allow-network
```

Características:

- IPv4, IPv6, dominios, URL y hashes comunes;
- deduplicación estable;
- límites de hasta 500 indicadores;
- concurrencia configurable y limitada;
- fuentes externas desactivadas por defecto;
- salida JSON normalizada.

### TLS Posture Audit

Inspecciona endpoints TLS autorizados y aísla errores por objetivo.

```bash
orion plugins run tls_posture_audit \
  --input samples/tls-plugin-request.json \
  --authorization "CHANGE-SEC-2048" \
  --allow-network
```

Características:

- lotes de hasta 500 destinos;
- timeout por operación;
- máximo de 32 workers;
- inventario de versión, cipher, certificado y peer;
- un fallo no interrumpe el resto del lote.

### Findings Ticket Sync

Convierte hallazgos en planes de trabajo o tickets Jira/ServiceNow. El modo predeterminado no modifica sistemas externos.

```bash
orion plugins run findings_ticket_sync \
  --input samples/ticket-plugin-request.json \
  --authorization "SECURITY-REVIEW-7781"
```

Para aplicar cambios reales deben coincidir tres decisiones explícitas:

1. `"apply": true` en la entrada;
2. `--allow-side-effects` en la CLI;
3. `--allow-network` para comunicarse con Jira o ServiceNow.

## Crear plugins externos

Un paquete externo implementa `BasePlugin` y publica un entry point:

```toml
[project.entry-points."orion.plugins"]
cloud_posture = "my_orion_extension.plugin:CloudPosturePlugin"
```

Después de instalarlo, aparecerá automáticamente:

```bash
orion plugins list
```

ORION rechaza identificadores duplicados, registra errores de descubrimiento y valida tanto la entrada como la salida de cada extensión.

Consulta [docs/PLUGIN_SYSTEM.md](docs/PLUGIN_SYSTEM.md) para el contrato completo, ejemplos y reglas de desarrollo.

## Calidad y CI

El workflow `Plugin Runtime CI` ejecuta en Python 3.10, 3.11, 3.12 y 3.13:

- Ruff sobre la capa de runtime;
- comprobación de formato;
- mypy;
- pytest;
- `orion plugins doctor`;
- validación del manifiesto generado;
- construcción de wheel;
- instalación limpia y smoke test del paquete construido.

## Diseño de seguridad

ORION aplica defensa en profundidad:

- autorización antes de ejecutar;
- red deshabilitada salvo consentimiento explícito;
- efectos externos deshabilitados salvo consentimiento explícito;
- *dry-run* por defecto para ticketing;
- límites de tamaño, tiempo y concurrencia;
- errores normalizados;
- contratos inmutables por plugin;
- resultados aptos para auditoría, MCP y automatización.

## Documentación principal

- [Sistema de plugins](docs/PLUGIN_SYSTEM.md)
- [Skill principal](orion/SKILL.md)
- [Arquitectura general](orion/ARCHITECTURE.md)
- [Entrada para agentes](skills/ai-entrypoint.md)
- [Instrucciones seguras](skills/agent-instructions.md)

## Licencia

MIT. Las contribuciones deben mantener el enfoque defensivo, autorizado, reversible y auditable del proyecto.

**Powered by ORION IA**
