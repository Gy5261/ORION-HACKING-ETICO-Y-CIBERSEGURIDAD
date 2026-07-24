# Skills y plugins ORION

La carpeta `skills/` ya no contiene únicamente descripciones conceptuales. Ahora publica el contrato legible por máquinas del runtime funcional de ORION.

## Archivos

- `skills.json`: manifiesto generado desde los plugins ejecutables;
- `plugin.schema.json`: JSON Schema formal del manifiesto;
- `ai-entrypoint.md`: orden de carga para agentes, MCP y LLM;
- `agent-instructions.md`: reglas obligatorias de autorización y seguridad.

## Fuente de verdad

Las clases de `orion/plugins/builtin.py` son la fuente de verdad para los plugins oficiales. El manifiesto puede regenerarse con:

```bash
orion plugins export-manifest --output skills/skills.json
```

Esto evita que nombre, versión, permisos, schemas y capacidades queden desincronizados del código real.

## Plugins oficiales

| Plugin | Categoría | Riesgo | Red | Efectos externos | Uso principal |
|---|---|---:|---:|---:|---|
| `ioc_enricher` | OSINT Intelligence | Bajo | Sí | No | Clasificación, DNS y enriquecimiento opcional de IOCs |
| `tls_posture_audit` | Web / Network | Bajo | Sí | No | Inventario y auditoría defensiva de TLS |
| `findings_ticket_sync` | Automation / Reporting | Medio | Condicional | Sí | Planificación o creación aprobada de tickets |

## Flujo para agentes

1. Leer `agent-instructions.md`.
2. Cargar y validar `skills.json`.
3. Elegir un plugin por capacidad, riesgo y permisos.
4. Consultar su contrato con `orion plugins describe`.
5. Construir un objeto JSON conforme a `input_schema`.
6. Confirmar autorización, actor y permisos mínimos.
7. Ejecutar mediante CLI, Python o adaptador MCP.
8. Conservar el resultado completo para auditoría.

## Resultados

El runtime devuelve una envoltura uniforme con:

- `plugin_id`;
- `plugin_version`;
- `request_id`;
- `actor`;
- `ok`;
- `duration_ms`;
- `data` o `error`;
- `warnings`.

## Extensibilidad

Los paquetes externos pueden publicar plugins mediante:

```toml
[project.entry-points."orion.plugins"]
my_plugin = "my_package.plugin:MyPlugin"
```

ORION descubre estas extensiones automáticamente, rechaza identificadores duplicados y muestra fallos de carga mediante `orion plugins doctor`.

## Compatibilidad y seguridad

- Python 3.10 o superior;
- interfaces JSON estables;
- red y efectos externos deshabilitados por defecto;
- autorización obligatoria en plugins oficiales;
- uso exclusivamente defensivo, educativo o expresamente autorizado.

Consulta `docs/PLUGIN_SYSTEM.md`, `orion/SKILL.md` y `orion/PLAYBOOK_INDEX.md` para metodología y documentación técnica ampliada.
