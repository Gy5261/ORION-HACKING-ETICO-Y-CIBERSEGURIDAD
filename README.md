# ORION — revisión de seguridad y operación controlada

Runtime defensivo con análisis local, controles de autorización para laboratorios y servidor MCP local. **Esta rama es una propuesta de revisión, no una nueva versión publicada ni una certificación legal.**

Antes de modificar el runtime se ejecutó la línea base: 24 pruebas aprobadas, compilación de distribuciones y diagnóstico. La primera revisión del código amplió la suite a **114 pruebas aprobadas**. Véase [evidencia y alcance de la auditoría](docs/MCP_AUDIT_2026-09-23.md).

## Empezar sin contactar objetivos

```bash
python -m pip install -e ".[dev,mcp]"
python -m orion plugins doctor
python -m orion plugins run ioc_enricher --input samples/controlled/offline-iocs.json --authorization LOCAL-CLASSIFICATION-001
python -m orion.mcp.server --transport stdio
```

El ejemplo clasifica una IP literal y un hash sin resolución DNS ni fuentes externas. Una referencia escrita por el usuario no demuestra consentimiento legal.

## Qué cambia

- Red denegada por defecto: el perfil solo admite sondas TLS acotadas de laboratorio con permiso independiente y solicitud exacta aprobada. Los adaptadores OSINT externos permanecen visibles, pero no pueden ejecutarse online desde este perfil.
- Cambios externos de plugins deshabilitados: los hallazgos se preparan como planes; la creación automática de tickets queda bloqueada.
- Aprobaciones con propietario, revisor, finalidad, referencia documental, fechas, huella SHA-256 y cupo de uso. Las cuotas se consumen mediante transacciones SQLite.
- Bloqueo de emergencia, rechazo de datos JSON no finitos o excesivos, importación de plugins externos desactivada por defecto y exclusión de archivos privados del catálogo MCP.
- MCP con 13 herramientas, 3 prompts, recursos tipados, enlaces MCP reales, errores `isError`, protección HTTP local de Host/Origin y tamaño del cuerpo.

## MCP: compatibilidad explícita

```bash
python -m orion.mcp.server --transport streamable-http --host 127.0.0.1 --port 8000
```

Se conservan stdio, Streamable HTTP y SSE legado del SDK 1.x. La revisión se probó con SDK 1.30.0, cuya revisión declarada es 2025-11-25. **No implementa todavía MCP 2026-07-28.** `orion_protocol_audit` describe esta diferencia en ejecución. No hay despliegue remoto OAuth implementado: `--allow-remote` no elimina la restricción local.

Configuración local de un cliente:

```json
{"mcpServers":{"orion":{"command":"orion-mcp","args":["--transport","stdio"]}}}
```

El soporte de la configuración de cada aplicación debe verificarse en esa aplicación; la suite no equivale a probar todos los productos comerciales.

## Documentación de esta revisión

- [Operación controlada, configuración, límites y recuperación](docs/CONTROLLED_OPERATION.md).
- [Revisión de consentimiento, privacidad y reglas de compromiso](docs/LEGAL_AND_PRIVACY_REVIEW.md).
- [Auditoría MCP, resultados reales y migración pendiente](docs/MCP_AUDIT_2026-09-23.md).
- [Contrato de ingeniería](AGENTS.md).

La guía de operación controlada prevalece sobre ejemplos de red de las guías históricas de [plugins](docs/PLUGIN_SYSTEM.md), [OSINT](docs/OSINT_INTEGRATIONS.md) y [MCP](docs/MCP_SERVER.md). Los playbooks, el HTML y los scripts históricos no se han reescrito ni certificado en esta revisión.

## Límites de confianza

El servidor requiere un operador local de confianza. Las etiquetas de actor no son identidad autenticada; la aprobación local no es firma electrónica ni verificación jurídica. Una IP privada no prueba propiedad ni aislamiento. SQLite no proporciona un registro inmutable frente al administrador. Los scripts de `orion/scripts/`, las llamadas directas a motores y las políticas Python personalizadas quedan fuera del perímetro de ejecución controlada: no deben exponerse a agentes ni usuarios no confiables.

No se debe desplegar en producción o como servicio multiusuario. Las restricciones de esta rama cambian comportamiento de 2.x; antes de publicar o fusionar como lanzamiento se necesita una decisión de versión mayor y revisar el manifiesto estático histórico. `main` no se modifica desde este PR de revisión.

## Reproducir verificaciones

```bash
python tools/validate_repository.py
python -m pytest
python -m build
python -m orion plugins doctor
```

Las pruebas emplean datos sintéticos, archivos temporales, ASGI en memoria y transportes loopback. La instalación de dependencias de CI sí requiere acceso a sus repositorios de paquetes; las pruebas no realizan evaluaciones de terceros.
