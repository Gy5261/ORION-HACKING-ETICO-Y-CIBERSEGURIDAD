# Registro de evaluación ORION — alcance verificable

## Estado de este documento

Este documento **no es una certificación de seguridad ni una evaluación automática de un modelo IA**. El antiguo informe contenía cifras y frases no respaldadas por un registro de ejecución reproducible. Se conserva el histórico en Git y esta versión lo sustituye por criterios de verificación.

## Evidencia técnica disponible

La rama principal anterior a esta revisión disponía de una ejecución GitHub Actions del 12 de octubre de 2026 con 136 pruebas aprobadas para Python 3.15. Esta evidencia corresponde exclusivamente a los escenarios programados en la suite. No acredita que las integraciones OSINT, Jira, ServiceNow o todos los clientes MCP hayan sido probados.

La revisión actual debe comprobarse en el PR y su commit específico. No reutilizar cifras de `main` para certificar cambios todavía no integrados.

## Reproducción y criterios

```bash
python tools/validate_repository.py
python -m pytest -v
python -m build
python -m orion plugins doctor
python orion/scripts/run_skill_sanity.py
python orion/scripts/expand_markdown_docs.py
```

Registrar versión exacta de Python, sistema operativo, SHA del commit, suite, número de pruebas, fallos y referencias a los registros originales.

## Criterios de aceptación

- Un control sólo está **probado** si existe entrada, aserción y resultado real.
- Un plugin opcional puede estar registrado aunque falte el ejecutable.
- Un script que imprime ayuda no demuestra que su funcionalidad real funcione.
- Una consulta HTTP o TLS no prueba una vulnerabilidad explotable.
- Los resultados de `evals/evals.json` son **criterios manuales de comportamiento**, no resultados automáticos de agentes IA.
- Los archivos JSON de esta carpeta son **muestras**, no evidencia de una evaluación de terceros.

## Limitaciones abiertas

No se ha efectuado pentest externo, auditoría jurídica, prueba de servicios de terceros ni verificación integral de todas las configuraciones. Las secciones generadas automáticamente en documentos históricos deben revisarse como ejemplos, no presentarse como implementaciones.
