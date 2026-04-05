# ORION-HACKING Evals

Este directorio contiene prompts de prueba para evaluar el skill.

## Objetivo

- comprobar cobertura de dominios
- comprobar que el skill enruta bien por modulos
- comprobar rechazo de solicitudes no autorizadas
- comprobar que la automatizacion por IA se mantiene en un carril seguro

## Archivos

- `evals.json`: set inicial de prompts realistas

## Uso sugerido

1. revisar `evals.json`
2. ejecutar `orion/scripts/run_skill_sanity.py`
3. revisar `eval-results/`
4. iterar sobre `SKILL.md`, `references/` y `playbooks/`
