# Instrucciones obligatorias para agentes ORION

Estas reglas aplican a cualquier IA, agente, adaptador MCP, operador humano o automatización que utilice ORION.

## Principios no negociables

1. **Autorización explícita:** no ejecutar un plugin contra activos reales sin permiso válido y alcance definido.
2. **Mínimo privilegio:** red y efectos externos permanecen deshabilitados salvo necesidad demostrada.
3. **Seguridad por defecto:** preferir análisis local, `plan`, simulación o *dry-run*.
4. **Reversibilidad:** todo cambio externo debe tener aprobación, responsable y procedimiento de rollback.
5. **Trazabilidad:** conservar `request_id`, actor, autorización, versión del plugin, entrada, resultado y evidencia.
6. **Minimización de datos:** no incluir secretos, credenciales, PII innecesaria ni evidencia sensible en logs.
7. **Control de alcance:** detenerse ante objetivos, ventanas o acciones no incluidas en el permiso.

## Permitido

- análisis defensivo y validación de controles;
- hardening, AppSec, detección, DFIR y threat modeling;
- OSINT ético y enriquecimiento de indicadores;
- auditorías y laboratorios expresamente autorizados;
- normalización de hallazgos, generación de reportes y planes de remediación;
- creación de tickets aprobada mediante permisos explícitos;
- desarrollo de plugins defensivos, pequeños, auditables y reversibles.

## Prohibido

- acceso o explotación no autorizada;
- malware, ransomware, persistencia, evasión o destrucción;
- phishing real, robo de credenciales o suplantación;
- abuso de APIs, tokens o claves sin autorización;
- interrupción de servicios o cambios fuera de ventana;
- recolección masiva o innecesaria de datos personales;
- modificar plugins para eliminar guardrails o facilitar abuso.

## Protocolo de ejecución

Antes de ejecutar:

1. cargar `skills/skills.json`;
2. inspeccionar el plugin con `orion plugins describe`;
3. validar la entrada contra `input_schema`;
4. confirmar autorización y actor;
5. habilitar solo los permisos requeridos;
6. establecer límites de tamaño, concurrencia y timeout;
7. ejecutar y validar `output_schema`;
8. revisar errores y advertencias;
9. archivar evidencia de forma segura.

## Acciones con efectos externos

Una acción real requiere simultáneamente:

- intención explícita en el payload, por ejemplo `apply=true`;
- `allow_side_effects=true`;
- acceso de red cuando corresponda;
- credenciales autorizadas fuera del código;
- plan de rollback y responsable identificado.

La ausencia de cualquiera de estas condiciones obliga a permanecer en modo de planificación.

## Respuesta ante ambigüedad

Si el alcance, autorización o impacto no son claros, el agente debe detener la ejecución real y limitarse a documentación, análisis seguro o simulación. ORION no convierte una petición del usuario en autorización legal.
