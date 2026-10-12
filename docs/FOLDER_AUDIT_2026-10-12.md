# ORION — Auditoría integral por carpetas

**Fecha:** 12 de octubre de 2026  
**Revisión:** [PR #9](https://github.com/Gy5261/ORION-HACKING-ETICO-Y-CIBERSEGURIDAD/pull/9)  
**Estado:** cambios propuestos; consultar los resultados de GitHub Actions del SHA de la revisión antes de aprobar su integración.

## Criterios técnicos

Se inspeccionó el inventario del repositorio y los puntos de entrada del runtime. Los cambios priorizan pruebas reproducibles, límites de recursos, autorización explícita, entradas JSON tipadas y documentación sustentada. Un componente **implementado** no es necesariamente **operativo**. Las pruebas sintéticas no certifican las integraciones externas.

## Matriz de revisión por carpeta

| Carpeta | Cambios concretos | Verificación y límite |
| --- | --- | --- |
| `orion/controls.py` | El IOC local, incluidos dominios y URLs, no necesita DNS ni permiso de red | El perímetro de TLS sigue requiriendo aprobación exacta; una etiqueta de actor no es autenticación |
| `orion/plugins/` | Eliminada duplicación del clasificador IOC; SpiderFoot limitado a loopback, sin proxies ni redirecciones; igualdad JSON estricta; entorno de subprocesos protegido | Los demás adaptadores OSINT permanecen denegados online, incluso cuando están instalados |
| `orion/mcp/` | Rechazo de cabeceras HTTP de longitud incompatibles, Transfer-Encoding duplicado y cuerpos indebidos | No implementa OAuth remoto ni conformidad MCP 2026-07-28 |
| `orion/scripts/` | Auditorías HTTP offline/loopback, TLS sometido a `OrionRuntime`, tickets sólo como planes, inventario SHA-256 limitado, entradas IOC offline, validación de Markdown real, sitio HTML filtrado, instaladores plan-first y retirada del generador de texto sintético | Los scripts no constituyen un sandbox; hay que comprobar el HTML generado en navegador y no publicar secretos |
| `orion/resources.py` | Búsqueda literal con límite de bytes, parámetros estrictos y ranking determinista | No es búsqueda semántica ni indexación de producción |
| `orion/SKILL.md` y `orion/references/` | Guía activa abreviada y progresiva; material histórico íntegro archivado como no verificado | Las referencias siguen siendo metodológicas, no pruebas de implementación |
| `orion/playbooks/` | Inventariados y conservados; consumidos selectivamente a través de referencias del skill | Ejemplos y fases históricas no se consideran pruebas ejecutadas |
| `docs/` | Alcance efectivo y denegaciones de OSINT/tickets, guía del runtime actualizado y este informe | La documentación complementa, no sustituye, un test funcional |
| `skills/` | Instrucciones alineadas con el runtime, metadatos de descubrimiento, versión estática corregida | Contratos declarativos y manifest no equivalen a conectividad verificada |
| `schemas/` | JSON controlado en la validación del repositorio; esquema de aprobación conservado | La aprobación estructural no autentica personas ni propiedad de activos |
| `tests/` | Nuevos casos de regresión para IOC offline, TLS, JSON, HTML, recursos, procesos, HTTP, documentación y límites | Sólo se declaran aprobados cuando la CI del commit correspondiente finaliza correctamente |
| `tools/` | Verificación AST de scripts que antes se omitían, JSON sin duplicados ni valores no finitos, comparación de versiones | No garantiza cobertura total de todos los posibles estados |
| `samples/` | Aclarado el origen sintético y las aprobaciones intencionalmente inválidas | No utilizar direcciones y ejemplos como autorización real |
| `evals/` | Catálogo de prompts etiquetado como rúbrica cualitativa manual | No se ha ejecutado una evaluación automática de IA |
| `eval-results/` | Retiradas cifras históricas sin evidencia y señalizadas las salidas de ejemplo | No se presentan muestras como auditorías reales |
| `.github/workflows/` | CI Python 3.12/3.15 Linux y 3.15 Windows, lint de símbolos y pruebas de instaladores sin aplicar cambios | Consultar artefactos, suites y resultado final de la matriz antes del merge |
| Raíz (`README.md`, `pyproject.toml`, `requirements.txt`, `AGENTS.md`) | Ruta de entrada y contratos revisados; la compatibilidad de Python 3.15 se preparó previamente | El proyecto sigue anunciando compatibilidad con Python >=3.10; no se ha probado aquí cada plataforma/version declarada |

## Hallazgos técnicos concretos

1. La clasificación IOC directa podía consultar DNS al recibir dominios. La ruta actual sin red ya no consulta DNS.
2. El inventario TLS antiguo desactivaba la validación PKI y podía devolver datos vacíos sin aclarar su límite. Ahora informa una huella DER y no atribuye validez del certificado.
3. El código histórico para tickets remotos podía ejecutarse directamente fuera de la política. La CLI controlada ahora rechaza `--apply`.
4. El generador HTML incorporaba contenido local de múltiples tipos sin una lista explícita de exclusión. Se limitó publicación, tamaño y salida JSON segura.
5. El generador de documentación ampliaba texto con patrones repetitivos no verificados. Fue sustituido por un auditor de solo lectura.
6. El validador AST omitía scripts heredados. Ahora revisa su sintaxis y uso del shell; también comprueba archivos JSON.
7. La documentación de evaluaciones describía resultados sin enlazar a una ejecución reproducible. Se sustituyó por criterios y advertencias.

## Límites aún abiertos

- Los seis adaptadores OSINT requieren instalación, credenciales y revisión independiente antes de cualquier prueba real. En el perfil controlado permanecen deshabilitados online.
- La copia HTML `orion/ORION-HACKING-singlefile.html` ya versionada no se regenera automáticamente con cada cambio del generador. Debe verificarse y reconstruirse como artefacto explícito antes de anunciar una actualización de la interfaz publicada.
- El contenido de los 32 archivos de referencias y seis playbooks es amplio e ilustrativo. Esta revisión no certifica la exactitud de cada afirmación histórica; el material sintético está marcado para revisión.
- El stack de seguridad local no es aislamiento del sistema operativo, gestión de identidades corporativas ni almacén inmutable de evidencias.
- La ejecución de scripts de terceros no controlados y los objetivos externos quedan fuera de esta entrega.

## Reproducir verificaciones

```bash
python -m pip install -e ".[dev,mcp]"
python tools/validate_repository.py
python -m pytest -v
python -m build
python -m orion plugins doctor
python orion/scripts/run_skill_sanity.py
python orion/scripts/expand_markdown_docs.py
```

La fecha y el número de pruebas válidas son los que constan en las ejecuciones finales de GitHub Actions para el SHA exacto. Un pipeline verde no garantiza ausencia absoluta de defectos.
