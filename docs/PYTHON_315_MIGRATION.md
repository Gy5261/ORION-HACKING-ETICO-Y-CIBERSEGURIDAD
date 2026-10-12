# ORION: adopción comprobable de Python 3.15.0 estable

**Versión recomendada:** Python 3.15.0, publicada el 9 de octubre de 2026. La versión 3.15.0rc1 (4 de agosto de 2026) es preliminar y ya fue reemplazada por la versión estable. No instalar RC1 para despliegues nuevos.

**Compatibilidad:** ORION conserva la sintaxis y el contrato de instalación de Python 3.10 o superior. Las pruebas automáticas nuevas incluyen Python 3.12 y 3.15 en Linux, y 3.15 en Windows. Esto evita romper equipos existentes sin una migración de versión mayor. La matriz no equivale a pruebas sobre todos los sistemas operativos e intérpretes soportados.

## Capacidades reales de 3.15

- **PEP 810 — importaciones diferidas:** la CLI usa la declaración compatible `__lazy_modules__`. Python 3.15 difiere la importación configurada; versiones anteriores la ignoran. Esto reduce trabajo innecesario para comandos de diagnóstico, pero no garantiza un tiempo de arranque específico. La carga diferida no se aplica globalmente a plugins, validadores ni permisos.
- **PEP 686 — UTF-8 por defecto:** conservar siempre `encoding="utf-8"` en entradas y salidas persistentes. No confiar en codificaciones implícitas del sistema.
- **PEP 814 — `frozendict`:** disponible en Python 3.15; no se utiliza automáticamente para JSON de plugins porque el contrato público necesita objetos mutables serializables y compatibilidad anterior.
- **PEP 799 — perfilado:** Python 3.15 incluye herramientas más modernas, entre ellas Tachyon; son herramientas de diagnóstico opcionales, no un acelerador automático.
- **JIT experimental:** disponibilidad y activación dependen de la compilación y la configuración del intérprete. ORION no lo habilita ni presupone velocidades superiores.
- **Free threading / GIL:** los hilos no pasan a ejecutar CPU en paralelo sólo por usar Python 3.15; depende de la build. La paralelización existente se utiliza para operaciones limitadas de I/O.
- **ABI y observabilidad:** `orion runtime-info --json` muestra versión, modo GIL, JIT, soporte de objetos incorporados y ABI cuando el intérprete publica esos atributos. Los campos desconocidos aparecen como `null`.

## Instalación en Windows con PowerShell

```powershell
py -3.15 --version
py -3.15 -m venv .venv315
.\.venv315\Scripts\python.exe -m pip install --upgrade pip
.\.venv315\Scripts\python.exe -m pip install -e ".[dev,mcp]"
.\.venv315\Scripts\python.exe -m orion runtime-info --json
.\.venv315\Scripts\python.exe -m pytest
```

Si el lanzador no encuentra Python 3.15, instalar la versión estable de Python.org y verificar el comando con la configuración real del equipo antes de continuar. No reemplazar instalaciones antiguas sin inventariar dependencias.

## Verificación offline

```bash
python tools/validate_repository.py
python -m pytest
python -m build
python -m orion plugins doctor
python orion/scripts/run_skill_sanity.py
python tools/benchmark_runtime.py --iterations 500 --samples 5
```

El comprobador de sanidad no consulta objetivos. El benchmark mide serialización canónica, validación de esquemas, huellas de solicitudes y generación de manifiestos. Informa mediana en nanosegundos y dispersión; para comparar versiones hay que usar el mismo equipo, carga, configuración, tamaño de entrada y metodología. **No interpretar operaciones por segundo como seguridad o rendimiento de redes.**

## Cambios de ingeniería

La CLI limita su entrada JSON a 1 MiB y rechaza claves duplicadas y valores no finitos. Los adaptadores ejecutan procesos sin intérprete de shell, capturan hasta 2 MiB por flujo, controlan la duración y detienen procesos agotados. En POSIX se detiene el grupo; en Windows sólo se garantiza la detención del proceso directo. Esto no constituye un sandbox ni un aislamiento de procesos descendientes de Windows.

El triaje de eventos normaliza instantes a UTC para seleccionar los límites temporales. Identifica fechas imposibles y entradas malformadas en vez de inventar una cronología. Las entradas sin zona horaria se interpretan como UTC por compatibilidad y se declara esta convención.

## Compatibilidad MCP y alcance

El proyecto mantiene por ahora el SDK MCP 1.x con `mcp>=1.27,<2`. El SDK 2.x introduce cambios incompatibles y requiere una migración de transporte y contratos independiente. Python 3.15 **no** concede automáticamente compatibilidad con MCP 2026-07-28, OAuth remoto ni clientes comerciales.

La suite no ejecuta OSINT de terceros ni audita objetivos reales. Son funciones bloqueadas o no evaluadas de acuerdo con `docs/CONTROLLED_OPERATION.md`. Consulte `docs/VERIFIED_CAPABILITIES.md` para diferenciar implementado, probado, operativo y denegado.

## Referencias oficiales

- Python 3.15.0: https://www.python.org/downloads/release/python-3150/
- Cambios de Python 3.15: https://docs.python.org/3.15/whatsnew/3.15.html
- Soporte del SDK MCP: https://github.com/modelcontextprotocol/python-sdk
