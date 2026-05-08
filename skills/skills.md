# 📋 Skills ORION - Sistema Estandarizado para IA

Este directorio proporciona un manifiesto legible por IA para todos los skills del proyecto.

## Estructura
- `skills.json`: Manifiesto principal (JSON estructurado).
- `ai-entrypoint.md`: Guía rápida de integración para agentes.
- `agent-instructions.md`: Reglas de seguridad estrictas.

**Skills principales** (extraídos de `orion/`):
- Ver `orion/SKILL.md` y `orion/PLAYBOOK_INDEX.md` para lista completa.
- Scripts en `orion/scripts/` son ejecutables y JSON-first.

**Uso por IA**:
1. Carga `skills/skills.json`.
2. Selecciona skill por categoría/riesgo.
3. Ejecuta conceptualmente o llama scripts vía MCP.
4. Siempre valida contra límites éticos.

Mantén compatibilidad: outputs JSON, inputs estandarizados, solo defensive.
