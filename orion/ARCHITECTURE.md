# Arquitectura ORION-HACKING 1.0

## Visión general

ORION-HACKING es una plataforma documental y operativa para ciberseguridad ética, defensiva y expresamente autorizada. La versión 1.0 incorpora un runtime de plugins que conecta conocimiento, metodología y automatización mediante contratos ejecutables y auditables.

## Principios arquitectónicos

1. Separación estricta de responsabilidades.
2. Autorización y mínimo privilegio por defecto.
3. Desacoplamiento entre conocimiento, metodología y motores.
4. Plugins pequeños, componibles y reemplazables.
5. Interfaces JSON estables para CLI, agentes y MCP.
6. Validación de entrada y salida mediante contratos.
7. Trazabilidad completa de actor, solicitud, versión y resultado.
8. Reversibilidad de acciones externas.
9. Portabilidad sin dependencia obligatoria de proveedores.
10. Fallos explícitos y diagnosticables.

## Capas principales

### Nivel 1: Gobernanza y orquestación

`SKILL.md`, `skills/agent-instructions.md` y los playbooks definen autorización, alcance, restricciones, evidencia y criterios de decisión.

### Nivel 2: Conocimiento técnico

`references/` contiene módulos por dominio para AppSec, red, nube, identidad, contenedores, DFIR, detección y hardening.

### Nivel 3: Metodología

`playbooks/` organiza procedimientos reproducibles, criterios de entrada y salida, validaciones y reporte.

### Nivel 4: Motores de automatización

`orion/scripts/` conserva scripts JSON-first reutilizables. Estos motores no son reemplazados por el runtime: los plugins los encapsulan y controlan.

### Nivel 5: Runtime de plugins

`orion/plugins/core.py` implementa:

- `PluginMetadata`;
- `PluginContext`;
- `PluginResult`;
- `ExecutionPolicy`;
- `PluginRegistry`;
- `OrionRuntime`;
- validación JSON Schema;
- descubrimiento mediante entry points.

`orion/plugins/builtin.py` adapta los motores oficiales al contrato común.

### Nivel 6: Interfaces

`orion/cli.py` expone una CLI unificada. La misma API puede ser consumida por Python, contenedores, pipelines y adaptadores MCP.

### Nivel 7: Metadatos y navegación

`skills/skills.json`, `skills/plugin.schema.json`, `docs/PLUGIN_SYSTEM.md`, `MODULE_MAP.md` y `PLAYBOOK_INDEX.md` permiten descubrimiento humano y automático.

## Flujo end-to-end

```text
AUTORIZACIÓN / ALCANCE
        ↓
SELECCIÓN DE PLAYBOOK Y PLUGIN
        ↓
VALIDACIÓN DE INPUT_SCHEMA
        ↓
POLÍTICA DE RED Y EFECTOS EXTERNOS
        ↓
EJECUCIÓN DEL MOTOR EXISTENTE
        ↓
VALIDACIÓN DE OUTPUT_SCHEMA
        ↓
PLUGIN_RESULT AUDITABLE
        ↓
EVIDENCIA, REPORTE Y REMEDIACIÓN
```

## Extensibilidad

Los plugins externos se registran mediante el grupo de entry points `orion.plugins`. El registro mantiene identificadores únicos, conserva los plugins oficiales y reporta extensiones defectuosas mediante `orion plugins doctor`.

## Modelo de seguridad

- Los plugins oficiales requieren una referencia de autorización.
- La red está deshabilitada salvo habilitación explícita.
- Los efectos externos requieren consentimiento independiente.
- Ticketing opera en `plan` por defecto.
- Las entradas tienen límites de tamaño y concurrencia.
- Los errores se normalizan sin ocultar fallos.
- Los secretos permanecen fuera de código, manifiestos y resultados.

## Flujo para agentes

```text
agent-instructions.md
        ↓
skills.json + plugin.schema.json
        ↓
orion plugins describe
        ↓
construcción y validación del payload
        ↓
orion plugins run / OrionRuntime
        ↓
archivo del resultado y evidencia
```

Todo el sistema está orientado exclusivamente a defensa, aprendizaje, laboratorios controlados y auditorías con permiso explícito. ORION no convierte una solicitud en autorización legal ni incorpora capacidades diseñadas para malware, persistencia, evasión o acceso no autorizado.
