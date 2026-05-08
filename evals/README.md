# evals/

## Propósito

Esta carpeta contiene el conjunto de **evaluaciones (prompts de prueba)** diseñadas para validar el comportamiento del skill ORION bajo diferentes escenarios de ciberseguridad ética.

## Objetivos de las Evals

- Verificar cobertura de dominios (web, cloud, network, secure engineering, etc.)
- Validar enrutamiento correcto entre módulos y playbooks
- Comprobar que el skill mantenga límites éticos estrictos (rechazo de solicitudes maliciosas)
- Evaluar calidad, claridad y utilidad de las respuestas generadas
- Probar compatibilidad con agentes IA/MCP

## Archivos

- **`evals.json`** — Catálogo principal de prompts de prueba con expected_output.
- **`README.md`** — Esta documentación.

## Uso Recomendado

1. Revisar o extender `evals.json`
2. Ejecutar `orion/scripts/run_skill_sanity.py`
3. Analizar resultados en `eval-results/`
4. Iterar mejoras en `orion/references/`, `orion/playbooks/` y `SKILL.md`

Todo el contenido está diseñado exclusivamente para **hacking ético, auditoría autorizada y mejora continua de capacidades defensivas**.

---

*Parte del sistema de evaluación continua de ORION - Powered by ORION IA*