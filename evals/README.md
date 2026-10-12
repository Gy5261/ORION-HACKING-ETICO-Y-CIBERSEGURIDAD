# Casos de evaluación cualitativa

`evals.json` contiene **prompts y criterios esperados para revisión manual de comportamiento** de un agente IA que utilice ORION. No se ejecutan automáticamente, no incluyen respuestas de un modelo y no miden precisión, tasa de éxito ni seguridad de forma estadística.

Las pruebas automatizadas reproducibles se encuentran en `tests/`. Para ejecutarlas usar `python -m pytest`. Los experimentos con agentes deben conservar entradas, salida, modelo, configuración, versión, evaluador y rúbrica explícita, además de respetar los controles de autorización.

No usar el catálogo para afirmar que todos los escenarios se completaron satisfactoriamente.
