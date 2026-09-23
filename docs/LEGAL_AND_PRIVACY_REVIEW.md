# Revisión de consentimiento, privacidad y reglas de compromiso

Este documento es una plantilla operativa. No es asesoría jurídica, certificación de cumplimiento ni permiso para acceder a sistemas. El responsable debe obtener revisión profesional para la jurisdicción, contratos y datos concretos. Los nombres de campos y controles de ORION no sustituyen esa revisión.

## Expediente previo al ejercicio

Complete el expediente antes de provisionar una aprobación. Los campos no resueltos significan que la actividad no debe comenzar.

| Área | Evidencia que debe revisar una persona responsable |
|---|---|
| Titularidad y autoridad | Propietario de cada activo y facultad de quien autoriza |
| Finalidad | Pregunta defensiva concreta, necesidad y beneficio esperado |
| Alcance positivo | Direcciones y puertos exactos, aplicación, entorno y periodo |
| Exclusiones | Producción, terceros, redes compartidas, cuentas reales y sistemas sensibles |
| Método | Solo la operación y parámetros revisados; sin ampliación automática |
| Marco aplicable | Jurisdicciones, contratos, permisos y condiciones del proveedor revisados por el responsable |
| Datos | Categorías necesarias, procedencia y preferencia por datos sintéticos |
| Responsables | Operador, revisor independiente, custodio de evidencia y contacto de emergencia |
| Impacto | Riesgo residual, límites de carga, presupuesto y criterio de parada |
| Conservación | Ubicación, acceso, periodo justificado y procedimiento de eliminación |

No incorpore documentos firmados, identificaciones, direcciones personales, números de teléfono o credenciales al repositorio para completar esta plantilla. Use referencias a un expediente separado con acceso restringido.

## Reglas de compromiso sugeridas

**Propósito:** describir qué configuración o hipótesis defensiva se revisa y cuál será el entregable. Evitar objetivos abiertos como investigar todo lo relacionado con una persona u organización.

**Activos:** enumerar los endpoints exactos. Un dominio de ejemplo, una IP privada o un nombre de usuario no constituye por sí solo autorización. Excluir infraestructura de proveedores que no esté comprendida en el permiso revisado.

**Acciones:** autorizar únicamente la inspección concreta. Este perfil no admite explotación, persistencia, evasión, robo de credenciales, phishing, destrucción ni modificaciones remotas. La documentación histórica tampoco concede autorización.

**Ventana y carga:** fijar comienzo, expiración, máximo de solicitudes y responsable que puede detener el proceso. La ventana del archivo ORION no debe exceder 24 horas; para ejercicios mayores se debe revisar y renovar la actividad, no ampliar informalmente el alcance.

**Cambio de alcance:** cualquier cambio de payload genera una nueva huella. Se suspende la ejecución hasta obtener otra revisión. No reutilizar aprobaciones para activos similares o para otro actor.

**Parada:** detener ante una dirección no reconocida, tráfico fuera del laboratorio, datos reales inesperados, degradación de servicio, alarma del propietario, credenciales expuestas o incertidumbre sobre consentimiento. No continuar para confirmar el impacto fuera del alcance.

## Roles y separación de funciones

El propietario confirma el alcance; el revisor comprueba documentación y parámetros; el operador ejecuta; el custodio conserva resultados mínimos. ORION solo exige que las etiquetas de actor y revisor difieran: no verifica que sean personas distintas. La separación efectiva debe imponerse mediante cuentas, permisos del sistema y procedimiento organizativo fuera del agente.

El agente puede proponer una solicitud y explicar resultados. No debe firmar, editar ni provisionar su aprobación, otorgarse flags, cambiar variables administrativas o escribir en la base de cuotas. No monte esos archivos en las herramientas de edición del agente.

## Privacidad durante el ejercicio

Use datos sintéticos cuando la finalidad pueda alcanzarse con ellos. No enriquezca IP o hashes mediante fuentes externas: esos envíos también comunican información a proveedores y están bloqueados en el perfil controlado. Los planes de tickets pueden contener detalles sensibles aunque todavía no se hayan enviado; revisarlos antes de exportarlos.

Minimice resultados y no conserve contenido innecesario. Separe el registro técnico de eventos del expediente de consentimiento y de los hallazgos. No copie evidencia completa en prompts, conversaciones, issues o pull requests. Revise los controles del cliente MCP y del proveedor del modelo antes de permitir que reciba información del ejercicio.

Defina quién puede leer cada categoría, cómo se protege en reposo y en tránsito, y cuándo debe eliminarse. No existe un plazo universal de conservación incorporado por este documento. El plazo debe justificarse y documentarse; los artefactos sintéticos de CI pueden tener un plazo distinto al de un expediente real.

## Evidencia y trazabilidad

Registre revisión del código, versiones instaladas, huella exacta de la solicitud, referencia de autorización, hora, UUID, decisión y resultado. Conserve los datos mínimos para reproducir una conclusión sin conservar secretos. Un hash demuestra correspondencia de bytes, no identidad del autorizante ni legalidad.

La SQLite local permite correlación y control de cupos, pero el administrador puede modificarla. Para requisitos de integridad más fuertes, el responsable debe definir un almacenamiento independiente, controles de acceso y un procedimiento de sellado/verificación. No describir el registro actual como inmutable o como cadena de custodia jurídicamente certificada.

## Cierre y comunicación

Separar observaciones reproducibles, interpretaciones y aspectos no probados. Comunicar hallazgos únicamente al destinatario autorizado y con la información necesaria. No publicar vulnerabilidades, datos personales o detalles de un tercero como resultado automático del ejercicio.

Al cerrar, retirar permisos del laboratorio, revocar las aprobaciones aún vigentes, registrar los usos consumidos, comprobar la restauración y ejecutar el plan de conservación o eliminación aprobado. Un resultado exitoso de CI no cierra estos requisitos administrativos.

## Criterio de aprobación final

La operación solo puede comenzar cuando el responsable pueda responder: quién autoriza; qué controla; qué se hará exactamente; dónde; cuándo; con qué límites; qué datos pueden salir; quién revisa; y cómo se detiene. Ante una respuesta desconocida, mantener el análisis offline.
