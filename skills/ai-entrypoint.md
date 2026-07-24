# AI Entry Point — ORION Plugin Runtime

Esta es la ruta de entrada obligatoria para agentes IA, MCP y automatizaciones que consuman ORION.

## Orden de carga

1. Leer `skills/agent-instructions.md` para aplicar límites éticos y operativos.
2. Cargar `skills/skills.json` como manifiesto ejecutable y fuente de descubrimiento.
3. Validar el manifiesto contra `skills/plugin.schema.json`.
4. Consultar `orion/SKILL.md` para metodología, gobernanza y conocimiento de dominio.
5. Usar `orion plugins describe <plugin_id>` antes de construir una solicitud.
6. Ejecutar mediante `orion plugins run` o invocar `OrionRuntime` desde Python.
7. Conservar el `request_id`, actor, versión, duración y resultado para auditoría.

## Reglas de ejecución

- Nunca inferir autorización a partir de la intención del usuario.
- Requerir una referencia explícita de alcance, ticket, ToR o RoE.
- No habilitar red salvo que el contrato del plugin y el alcance lo requieran.
- No habilitar efectos externos salvo aprobación explícita y reversible.
- Preferir `plan`, `dry-run` o análisis local antes de cualquier cambio.
- Validar entrada y salida usando los schemas publicados.
- No exponer secretos, tokens, credenciales ni evidencia sensible en logs.

## Descubrimiento

```bash
orion plugins list --json
orion plugins describe ioc_enricher
orion plugins doctor
```

## Ejecución

```bash
orion plugins run ioc_enricher \
  --input samples/ioc-plugin-request.json \
  --authorization "TOR-2026-ORION-001" \
  --actor "authorized-agent" \
  --allow-network
```

## Integración Python o MCP

La API pública está en `orion.plugins`. Los plugins externos se publican mediante el grupo de entry points `orion.plugins`. El runtime rechaza entradas inválidas, identifica errores de descubrimiento y devuelve resultados JSON auditables.

Consulta `docs/PLUGIN_SYSTEM.md` para el contrato completo y `skills/skills.md` para la guía funcional de capacidades.
