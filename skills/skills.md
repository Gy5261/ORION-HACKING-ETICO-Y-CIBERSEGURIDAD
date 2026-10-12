# Sistema de capacidades ORION

Esta carpeta describe contratos de ejecución defensiva; **un contrato publicado no implica que una integración pueda utilizarse**. La fuente ejecutable es `PluginRegistry` en `orion/plugins/core.py`, y la política vigente se encuentra en `orion/controls.py`.

## Archivos y fuente de verdad

- `skills.json`: inventario estático para descubrimiento. El campo `python_runtime` de un inventario estático no representa el intérprete actualmente instalado.
- `plugin.schema.json`: estructura del inventario, no validación de autorización.
- `ai-entrypoint.md`: instrucciones para agentes confiables.
- `agent-instructions.md`: controles y límites de alcance.
- `orion/SKILL.md`: guía de carga progresiva, limitada a instrucciones actuales.

Para consultar contratos efectivos, usar `python -m orion plugins list --json --health` y `python -m orion plugins describe ID --health`. El `doctor` revisa disponibilidad local y no prueba conectividad externa ni cumplimiento legal.

## Matriz real del perfil controlado

| Plugin | Funcionamiento admitido |
| --- | --- |
| `ioc_enricher` | Clasificación offline de IP, hash, dominio y URL sin DNS |
| `tls_posture_audit` | Sólo laboratorio con aprobación exacta, red permitida y auditoría |
| `findings_ticket_sync` | Planificación local; no envía tickets |
| `spiderfoot` | Adaptador instalado si existe dependencia; ejecución online denegada |
| `theharvester`, `sherlock`, `osint_spy`, `phoneinfoga`, `photon` | Contratos visibles; ejecución online denegada |

El protocolo MCP local expone herramientas y recursos sólo para el operador confiable. No dispone de OAuth remoto ni conformidad con revisiones del protocolo que no hayan sido implementadas y probadas.

## Integraciones de terceros

Los entry points del grupo `orion.plugins` no se cargan por defecto. Sólo se habilitan mediante `PluginRegistry(load_external=True)` cuando el operador controla el código y sus dependencias. No otorgar a un agente acceso para activar este modo automáticamente.

## Ejecución y comprobación

```bash
python -m pip install -e ".[dev,mcp]"
python -m orion plugins doctor
python -m orion plugins run ioc_enricher --input samples/controlled/offline-iocs.json --authorization LOCAL-CLASSIFICATION-001
python tools/validate_repository.py
python -m pytest
```

Conservar `request_id`, versión, entrada autorizada, salida, errores, tiempos y limitaciones. No registrar datos sensibles innecesarios. Consultar [operación controlada](../docs/CONTROLLED_OPERATION.md) y [matriz de capacidades](../docs/VERIFIED_CAPABILITIES.md).
