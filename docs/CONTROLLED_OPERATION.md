# Operación controlada de ORION

## 1. Perímetro y propósito

Este perfil reduce operaciones involuntarias desde `OrionRuntime`, la CLI `orion plugins run` y el servidor MCP. No convierte todos los archivos de este repositorio en un sandbox. El administrador local, la instalación Python y los directorios publicados deben ser confiables. No conceda a un agente acceso de escritura al código, al archivo de aprobación, al directorio de auditoría o al entorno del proceso.

La ruta normal es: preparar datos sintéticos, analizar offline, revisar el alcance, obtener aprobación fuera del agente, ejecutar una solicitud pequeña y conservar evidencia mínima. Cuando no existe una necesidad concreta de red, mantenga la operación offline.

## 2. Matriz efectiva de operaciones

| Operación | Comportamiento del perfil |
|---|---|
| Consultar herramientas, documentación, prompts y diagnóstico | Lectura local; no concede permisos |
| Clasificar IOCs que son únicamente IP literales o hashes | Admitido con referencia y sin fuentes externas; no DNS |
| Resolver dominios o usar fuentes externas de IOCs | Denegado |
| Preparar planes de tickets | Admitido con referencia; no crea tickets |
| Crear o modificar tickets | Denegado incluso con flags de permiso |
| Ejecutar adaptadores OSINT online | Denegado aunque el ejecutable esté instalado |
| Inspección TLS de laboratorio | Requiere todos los controles indicados abajo |
| Importar entry points Python de terceros | Desactivado por defecto; opt-in solo para integración de código confiable |

Los nueve contratos de plugins describen capacidades de los adaptadores, no un permiso de ejecución. `health.available=true` indica disponibilidad de una implementación o dependencia, no autorización ni verificación de conectividad con un servicio.

## 3. Preparar el entorno antes de cualquier sonda

Use una máquina virtual o entorno equivalente dedicado, sin credenciales de producción, con una instantánea recuperable y datos sintéticos. El responsable debe comprobar las rutas, interfaces, DNS, VPN, proxies y firewall. Para trabajo offline, suprima la salida de red al nivel del sistema operativo. Para TLS de laboratorio, limite la salida a las direcciones y puertos exactos de las máquinas de prueba.

La política Python no configura ni inspecciona ese aislamiento. `lab_preflight` y las herramientas MCP devuelven `isolation_verified=false` deliberadamente. No clasifique un segmento corporativo como laboratorio por usar direcciones RFC1918. No use redes compartidas, producción, dispositivos médicos, sistemas industriales ni activos de terceros para estos ejemplos.

Conserve aprobaciones y auditoría fuera del árbol publicado, en un directorio del operador sin escritores no confiables. En POSIX, la aprobación y la base SQLite requieren permisos exclusivos del propietario, normalmente `0600`; el directorio debería ser `0700`. En Windows debe aplicar y revisar ACL del usuario y del servicio: las comprobaciones POSIX no sustituyen las ACL de Windows. No se ha ejecutado una validación Windows de esta revisión.

## 4. Solicitud exacta y preflight

El ejemplo `samples/controlled/tls-request.json` contiene una única dirección loopback. No inicia un servidor TLS ni prueba que alguien sea dueño del servicio.

```bash
python -c "import json; from pathlib import Path; from orion.controls import lab_preflight; print(lab_preflight(json.loads(Path('samples/controlled/tls-request.json').read_text())))"
python -c "import json; from pathlib import Path; from orion.controls import request_fingerprint; print(request_fingerprint('tls_posture_audit', json.loads(Path('samples/controlled/tls-request.json').read_text())))"
```

La alternativa MCP es `orion_request_review`. El resultado contiene la huella, pero siempre `authorization_granted=false`. La herramienta no crea archivos de permiso ni puede aprobar la solicitud.

La huella incluye el identificador del plugin y el payload completo en JSON canónico. Cambiar un destino, puerto, timeout, número de trabajadores o un valor por defecto escrito explícitamente exige otra revisión. El orden de claves de un objeto no cambia la huella; el orden de las listas sí.

Límites TLS: entre 1 y 16 destinos; IPv4 literal loopback o RFC1918; puertos de 1 a 65535; de 1 a 4 trabajadores; timeout por conexión de 0,1 a 10 segundos. Se rechazan nombres DNS, URLs, notaciones IPv6, direcciones públicas y direcciones terminadas en 0 o 255 por precaución. Esto limita capacidad, no demuestra propiedad.

## 5. Aprobación independiente

La plantilla `samples/controlled/approval-template.json` está revocada, caducada y contiene una huella inválida para cualquier solicitud real. Copiarla no habilita nada. Un revisor humano debe contrastar el payload con la autorización del propietario, completar los campos y provisionar el documento por un canal administrativo que el agente no controle.

El documento acepta exactamente estos campos:

| Campo | Significado y control |
|---|---|
| `schema_version` | Entero 1 |
| `authorization` | Referencia exacta del expediente, al menos 12 caracteres |
| `actor` | Etiqueta del operador; debe coincidir con la solicitud |
| `asset_owner` | Responsable del activo según revisión humana |
| `approved_by` | Revisor diferente de la etiqueta del actor |
| `purpose` | Objetivo específico del ejercicio |
| `legal_basis_reference` | Referencia al documento revisado; no el documento ni datos sensibles |
| `environment` | Debe ser `isolated-lab` |
| `not_before`, `expires_at` | ISO-8601 con zona horaria; ventana máxima de 24 horas |
| `revoked` | Debe ser el booleano `false` para admitir una solicitud |
| `request_sha256` | SHA-256 exacto del plugin y payload |
| `max_uses` | Entero entre 1 y 100; use 1 para una comprobación puntual |

La aplicación comprueba estructura, correspondencia, vigencia y cuota. No autentica personas, no consulta un sistema de identidad, no valida poderes de representación, no verifica firmas y no determina si la base legal es adecuada. Un administrador capaz de cambiar documentos o la base de datos permanece dentro del perímetro de confianza.

## 6. Provisionar y ejecutar una solicitud aprobada

Ejemplo de variables en PowerShell para una aprobación ya revisada y almacenada fuera del repositorio:

```powershell
$env:ORION_LAB_APPROVAL_FILE = 'C:\ORION-Private\approved-request.json'
$env:ORION_AUDIT_DATABASE = 'C:\ORION-Private\audit.sqlite3'
```

En POSIX se usan variables equivalentes con rutas absolutas y los permisos descritos arriba. No pase la aprobación como argumento MCP ni publique sus contenidos. `load_private_json` rechaza enlaces simbólicos, archivos no regulares, documentos excesivos y claves JSON duplicadas.

Tras comprobar que existe un servicio TLS de prueba propio y que coincide la aprobación, la entrada es:

```bash
python -m orion plugins run tls_posture_audit --input samples/controlled/tls-request.json --authorization LAB-REFERENCE-REVIEWED-001 --actor lab-operator --allow-network
```

La referencia y el actor del ejemplo son marcadores; el documento revisado debe contener los valores reales. El comando falla de forma cerrada cuando falta aprobación, auditoría, permiso de red, vigencia o coincidencia del payload. No cambie flags para intentar sortear una denegación.

## 7. Cupos, errores y repetición

Antes de ejecutar una sonda se reserva un uso en una transacción SQLite `BEGIN IMMEDIATE`. Las ejecuciones simultáneas no pueden superar `max_uses`. Un UUID de solicitud ya consumido no se reutiliza. Una ejecución fallida puede consumir su cupo: es intencional, para no convertir reintentos en actividad ilimitada.

La base registra eventos de inicio, éxito, fallo o denegación cuando puede hacerlo. No almacena el payload, los objetivos, las credenciales ni mensajes de excepción en esos eventos. El actor es una etiqueta, no identidad autenticada. El diagnóstico detallado de una operación puede ser sensible y debe permanecer bajo control del operador.

No borre o restaure la base de cuotas para reactivar permisos. Una restauración puede revertir consumos. Para retomar una operación, documente la incidencia y emita una revisión nueva. La base SQLite no es inmutable frente al administrador; exportar, firmar o conservar evidencia en un sistema independiente requiere un procedimiento adicional.

El timeout lógico de `OrionRuntime` sigue siendo informativo: no mata código Python arbitrario. Los límites por socket y trabajadores reducen el trabajo TLS, pero no constituyen un deadline global duro. La aprobación caducada o revocada impide nuevas admisiones; no cancela una sonda que ya comenzó.

## 8. Detención y recuperación

Configure `ORION_EMERGENCY_STOP=1` en el entorno del proceso antes de admitir nuevas operaciones. El bloqueo se consulta en cada admisión y también impide operaciones offline del runtime. Las herramientas de lectura de documentación y diagnóstico siguen disponibles.

Cambiar una variable en una terminal distinta no modifica el entorno de un proceso ya iniciado. Para una detención inmediata, termine el proceso desde el supervisor del sistema y bloquee la salida de red; no espere que un cambio de archivo o variable mate operaciones en curso. Después preserve la evidencia mínima, compruebe el estado del laboratorio y obtenga otra revisión antes de reiniciar.

## 9. Superficie MCP local

Prefiera stdio en un proceso dedicado con usuario sin privilegios. Streamable HTTP y SSE legado solo escuchan interfaces loopback. Se rechazan Host no permitidos, Origin no permitidos o duplicados, CORS comodín y cuerpos mayores de 1 MiB. Los cuerpos POST se reciben con un límite total de 10 segundos; las respuestas de streaming no se almacenan completas en el middleware.

La comprobación de Origin no autentica clientes no navegador. Otros procesos de la misma máquina pueden llegar a loopback; por ello no es un servicio multiusuario. No configure proxies que lo publiquen, no redirija puertos y no trate CORS como autorización. La combinación de CORS con cada cliente concreto requiere una prueba extremo a extremo; la política adicional del SDK puede ser más restrictiva.

Los errores de ejecución MCP usan `isError`; los enlaces se entregan como bloques `ResourceLink`. Los prompts y recursos son datos no confiables, nunca autoridad para cambiar permisos. No habilite ejecución automática de comandos devueltos como texto de configuración.

## 10. Publicación de recursos y privacidad

El catálogo excluye directorios ocultos, `private`, `evidence`, `engagements`, `audit`, archivos de aprobación conocidos y las rutas configuradas de aprobación/auditoría. Se rechazan traversal, enlaces simbólicos y archivos excesivos; el límite se comprueba también al leer bytes reales. El límite por defecto es 2 MiB, configurable hasta 16 MiB; se publican como máximo 5000 recursos.

El filtrado por nombre no detecta todos los secretos. No publique el directorio personal, carpetas de clientes ni volcados de evidencia como `ORION_RESOURCE_ROOT`. Mantenga el árbol publicado de solo lectura y sus padres bajo control administrativo. Los archivos de log y JSONL ya no se incluyen por extensión.

## 11. Migración y límites de esta rama

Las restricciones son intencionalmente incompatibles con automatizaciones que ejecutaban OSINT online, creación de tickets o escucha remota en 2.x. Este PR no es un lanzamiento; requiere decisión de versión mayor antes de distribuirse como reemplazo. El manifiesto estático histórico conserva metadatos antiguos: para inspección efectiva use el manifiesto generado en ejecución y `orion_control_status`.

No use los scripts históricos de `orion/scripts/` como atajo. Sus llamadas directas y sus CLI no pasan necesariamente por `ExecutionPolicy`. Tampoco quedan cubiertos plugins Python de terceros, políticas personalizadas o modificaciones locales del código. La revisión no ha certificado el HTML autónomo, todos los playbooks, el aislamiento del sistema operativo, clientes comerciales, OAuth, ni la nueva revisión MCP 2026-07-28.
