# Sistema de Plugins ORION 1.0

## Propósito

ORION deja de tratar las *skills* como simples documentos descriptivos. La versión 1.0 incorpora un runtime real que convierte cada capacidad en un plugin instalable, descubrible, validable y ejecutable mediante Python, CLI, agentes de IA o adaptadores MCP.

El diseño conserva una regla no negociable: todas las operaciones deben ejecutarse dentro de un alcance autorizado, con trazabilidad y con permisos explícitos para red o efectos externos.

## Componentes

```text
orion/
├── cli.py                    # Interfaz `orion plugins ...`
├── plugins/
│   ├── core.py               # Contratos, schema, policy, registry y runtime
│   └── builtin.py            # Plugins oficiales
└── scripts/                  # Motores reutilizados por los plugins
skills/
├── skills.json               # Manifiesto exportado por el runtime
└── plugin.schema.json        # Contrato del manifiesto
```

## Contrato de plugin

Todo plugin hereda de `BasePlugin`, publica `PluginMetadata` inmutable e implementa `run`:

```python
from orion.plugins import BasePlugin, PluginContext, PluginMetadata


class MyPlugin(BasePlugin):
    metadata = PluginMetadata(
        plugin_id="my_plugin",
        name="My Plugin",
        version="1.0.0",
        category="defensive",
        description="Ejemplo de plugin defensivo y auditable.",
        risk_level="low",
        capabilities=("example",),
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )

    def run(self, payload: dict, context: PluginContext) -> dict:
        return {"ok": True}
```

### Metadatos obligatorios

Cada plugin declara:

- identificador estable y único;
- versión semántica;
- categoría y descripción;
- nivel de riesgo;
- capacidades;
- schema JSON de entrada y salida;
- necesidad de autorización;
- acceso a red;
- posibles efectos externos;
- timeout lógico por defecto y máximo;
- etiquetas de descubrimiento.

## Registro y descubrimiento

Los plugins oficiales se registran de forma determinista. Los plugins de terceros se descubren mediante el grupo estándar de entry points `orion.plugins`:

```toml
[project.entry-points."orion.plugins"]
my_plugin = "my_package.plugin:MyPlugin"
```

Al instalar el paquete externo, ORION lo detecta automáticamente. Un identificador duplicado nunca reemplaza silenciosamente a un plugin oficial. Los errores de descubrimiento quedan expuestos por `orion plugins doctor` sin ocultar los plugins sanos.

## Seguridad por diseño

### Autorización obligatoria

Los plugins oficiales exigen una referencia explícita de autorización: ticket, Rules of Engagement, Terms of Reference, orden de trabajo o documento equivalente. Una cadena vacía o genérica es rechazada antes de ejecutar lógica técnica.

La referencia mejora trazabilidad, pero no sustituye un permiso legal válido.

### Permisos separados

ORION diferencia:

- `allow_network`: permite conexiones de salida necesarias para consultas o auditorías autorizadas;
- `allow_side_effects`: permite crear o modificar recursos externos;
- `apply`: vive dentro del payload y activa el cambio concreto.

Para crear tickets se necesitan simultáneamente `apply=true`, `allow_side_effects=true` y `allow_network=true`. El modo predeterminado sigue siendo *dry-run*.

### Validación de entrada y salida

Cada plugin declara JSON Schema para su entrada y salida. El runtime rechaza:

- campos desconocidos cuando `additionalProperties=false`;
- campos obligatorios ausentes;
- tipos incorrectos;
- listas vacías, demasiado grandes o duplicadas;
- valores fuera de rangos, patrones o enumeraciones;
- salidas que incumplen el contrato publicado.

### Trazabilidad

Cada ejecución recibe:

- `request_id` UUID;
- identidad del actor;
- identificador y versión del plugin;
- duración;
- estado;
- advertencias;
- error normalizado;
- resultado JSON.

### Límites de tiempo

El runtime valida un límite lógico máximo. Los motores siguen siendo responsables de configurar timeouts internos por operación de red. Si una ejecución excede el límite lógico, el resultado incluye una advertencia auditable.

## CLI

### Instalar en desarrollo

```bash
python -m pip install -e ".[dev]"
```

### Ver plugins

```bash
orion plugins list
orion plugins list --json
orion plugins describe ioc_enricher
```

### Ejecutar

```bash
orion plugins run ioc_enricher \
  --input samples/ioc-plugin-request.json \
  --authorization "TOR-2026-ORION-001" \
  --actor "security-team" \
  --allow-network
```

La entrada también puede venir de stdin:

```bash
cat request.json | orion plugins run tls_posture_audit \
  --input - \
  --authorization "CHANGE-SEC-2048" \
  --allow-network
```

Puede proporcionarse un UUID externo para correlación:

```bash
orion plugins run findings_ticket_sync \
  --input samples/ticket-plugin-request.json \
  --authorization "SECURITY-REVIEW-7781" \
  --request-id "6e36ad9f-4d58-4f8a-9ab1-e5612b25bb79"
```

### Diagnóstico

```bash
orion plugins doctor
```

El diagnóstico valida descubrimiento, metadatos y contratos básicos.

### Regenerar el manifiesto

```bash
orion plugins export-manifest --output skills/skills.json
```

El manifiesto se genera desde las clases ejecutables. Así, el código es la fuente de verdad y no una descripción manual susceptible de quedar obsoleta.

## Plugins oficiales

### `ioc_enricher`

Capacidades:

- clasificación de IPv4, IPv6, dominio, URL y hashes comunes;
- resolución DNS defensiva;
- enriquecimiento opcional mediante integraciones existentes;
- procesamiento concurrente conservando el orden;
- deduplicación y límites de volumen.

Entrada mínima:

```json
{"iocs": ["8.8.8.8"]}
```

Por seguridad, `external_sources` es `false` de manera predeterminada en el plugin.

### `tls_posture_audit`

Capacidades:

- auditoría de múltiples endpoints;
- inventario de negociación TLS y certificado;
- timeout por destino;
- concurrencia limitada a 32 workers;
- errores aislados por objetivo.

Entrada mínima:

```json
{"targets": ["example.org:443"]}
```

### `findings_ticket_sync`

Capacidades:

- normalización de hallazgos;
- planificación de Jira o ServiceNow;
- modo seguro `plan` por defecto;
- creación real solo con triple consentimiento explícito;
- máximo de 1.000 hallazgos por ejecución.

Entrada de planificación:

```json
{
  "mode": "plan",
  "findings": [
    {
      "title": "Certificado próximo a vencer",
      "severity": "medium",
      "asset": "portal.example.org"
    }
  ]
}
```

## Desarrollo de plugins

1. Definir un identificador estable y semántico.
2. Mantener el plugin pequeño y delegar lógica pesada a módulos de dominio.
3. Declarar con precisión red, riesgo y efectos externos.
4. Diseñar el modo seguro o simulación como comportamiento predeterminado.
5. Limitar tamaño de entradas, concurrencia y timeouts.
6. Nunca incluir secretos en resultados, logs o excepciones.
7. Probar autorización, errores, contratos y comportamiento sin red.
8. Publicar el plugin mediante `orion.plugins`.
9. Ejecutar `orion plugins doctor` y la suite de pruebas antes de publicar.

## Compatibilidad

- Python 3.10 o superior;
- sin dependencias obligatorias del runtime;
- JSON como interfaz estable;
- entry points estándar de Python;
- compatible con ejecución local, CI, contenedores y adaptadores MCP.

## Límites éticos y operativos

ORION no autoriza por sí mismo un assessment. El operador sigue siendo responsable de respetar alcance, ventanas, restricciones, privacidad, tratamiento de evidencia y legislación aplicable. El runtime no incorpora malware, persistencia, evasión, explotación automática ni acceso no autorizado.
