# ORION — Matriz de capacidades verificables

ORION es un runtime de seguridad defensiva autorizado. No es un sistema operativo ni un sandbox. Distinguir implementación, prueba y operación verificada.

| Componente | Estado real | Límite comprobable |
| --- | --- | --- |
| CLI y plugins | Implementados | Disponibilidad del contrato no garantiza eficacia externa |
| Clasificación IOC | Local y sin red | No confirma que un indicador sea malicioso |
| Normalización de hallazgos | Script local | No prueba existencia ni explotación de una vulnerabilidad |
| Triaje de eventos | Análisis heurístico | Una anomalía no demuestra incidente |
| Informe Markdown | Generador de plantilla | No incluye hallazgos inventados ni resultados certificados |
| TLS | Condicionado a aprobación exacta de laboratorio | No prueba autorización legal |
| OSINT externo | Adaptadores registrados, ejecución online denegada | Dependencias opcionales; sin prueba extrema a extrema |
| Tickets | Plan local permitido, escritura remota denegada | No afirmar integración operativa de Jira/ServiceNow |
| MCP local | SDK opcional; pruebas del protocolo antiguo | No proclamar conformidad MCP 2026-07-28 ni OAuth remoto |

## Nomenclatura rigurosa

- **Implementado:** existe código ejecutable para un contrato explícito.
- **Probado:** se ha ejecutado una prueba con resultado contrastado.
- **Operativo:** verificado extremo a extremo en un entorno declarado.
- **Denegado:** bloqueado por política aunque el código exista.
- **No evaluado:** falta evidencia. No equivale a aprobado.
- **Hipótesis:** posible vulnerabilidad sin confirmación.
- **Hallazgo:** observación comprobada con método, condiciones y evidencia.

## Pruebas locales reproducibles

Instalar en entorno aislado con: python -m pip install -e ".[dev,mcp]"

1. python tools/validate_repository.py
2. python -m pytest
3. python -m build
4. python -m orion plugins doctor
5. python orion/scripts/run_skill_sanity.py

Registrar versiones, sistema operativo, código de salida, número de casos, resultados y limitaciones. No transformar el porcentaje de comprobaciones en una puntuación de seguridad.

El chequeo de argumentos de http_surface_audit.py no realiza solicitudes HTTP y **no** verifica una auditoría de cabeceras. La generación del informe sólo valida que existe la plantilla y que no contiene resultados ficticios.

## Terminología y redacción por sección

Usar términos técnicos precisos en español, frases breves y párrafos explicativos con evidencia. Indicar objetivo, entrada, método, resultado verificable, limitaciones y criterio de aceptación. CVSS requiere versión y vector; CWE requiere una debilidad clasificada; ausencia de una cabecera no equivale automáticamente a una vulnerabilidad explotable. No asignar puntuaciones, hallazgos, porcentajes de cumplimiento o certificaciones por defecto.

## Perímetro de seguridad

La referencia de autorización y la etiqueta de actor no autentican la identidad. La aprobación local no es firma jurídica. Red y efectos externos permanecen denegados salvo el flujo controlado autorizado. Evitar ejecución directa de scripts históricos fuera de OrionRuntime. MCP en loopback no autentica procesos locales.

El generador de informe crea una plantilla sin conclusiones precargadas. No sobreescribe archivos salvo con --overwrite.

## Límites verificados documentalmente

Las pruebas de septiembre de 2026 cubren rutas locales, contratos, permisos y transportes específicos. No demuestran funcionamiento real de las herramientas OSINT de terceros, integración Jira/ServiceNow, aislamiento de sistema operativo, controles legales, compatibilidad de todos los clientes MCP ni conformidad con MCP 2026-07-28.

Consulte docs/CONTROLLED_OPERATION.md, docs/MCP_AUDIT_2026-09-23.md y AGENTS.md antes de ejecutar herramientas.