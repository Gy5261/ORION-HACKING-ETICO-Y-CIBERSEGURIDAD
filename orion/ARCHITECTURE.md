# ORION-HACKING Architecture

## Visión de Sistemas

ORION-HACKING está pensado como una **plataforma documental y operativa distribuida** para agentes de IA
capaces de leer, comprender, escribir y ejecutar código pequeño dentro de trabajos de ciberseguridad
autorizada. La idea central es **desacoplar completamente**:

- **Orquestación** (políticas, guardrails, decisiones)
- **Conocimiento** (referencias reutilizables por dominio)
- **Metodología** (playbooks operativos concretos)
- **Automatización** (scripts pequeños, auditable, reversibles)
- **Evidencia y Reporting** (normalización, trazabilidad, formatos reproducibles)

---

## Principios Arquitectónicos

### 1. Separación de Responsabilidades
Cada capa tiene responsabilidad clara, no debe mezclar políticas con técnica, ni conocimiento con procedimiento.

### 2. Desacoplamiento Vertical
- Las referencias no deben saber de playbooks
- Los playbooks no generan código directamente (usan scripts)
- Los scripts no contienen políticas (solo lógica técnica)
- La orquestación nunca hace trabajo técnico directo

### 3. Composabilidad
Un módulo (ej: Web AppSec) debe poder combinarse con otro (ej: Cloud) sin conflictos.
No es "o web o cloud"; es "queremos web + cloud + hardening para esto".

### 4. Portabilidad
El conocimiento debe ser agnóstico a:
- Stack tecnológico (Python vs Go, AWS vs Azure, etc.)
- Herramientas específicas (código que depende de Burp != código que depende de ZAP)
- Frameworks (sin favorecer Rails vs Django vs Laravel)

### 5. Auditabilidad Extrema
Cada decisión, acción, generación de código debe ser logueable y se pueda auditar después.

### 6. Reversibilidad
Lo automatizado debe poder rollback sin deuda técnica.

---

## Capas del Sistema (Arquitectura de 5 Niveles)

### Nivel 1: Orquestación (`SKILL.md`)

**Responsabilidad**:
- Activar/desactivar el sistema según contexto
- Imponer guardrails (hard stops)
- Seleccionar perfil operativo (rápido, completo, iterativo, continuo, urgente)
- Indicar qué módulos cargar
- Decidir flujo de trabajo
- Manejo de rechazo de solicitudes prohibidas

**Características**:
- Punto de entrada único
- No contiene referencia técnica (va a referencias/)
- No contiene procedimiento (va a playbooks/)
- Conocimiento: principios, guardrails, modos de operación, matriz de decisión

**Salidas**:
- Decisión de "activar / rechazar con motivo"
- Lista de módulos a cargar
- Perfil operativo (modo, timeline, alcance relativo)
- Flujo de trabajo recomendado

---

### Nivel 2: Biblioteca de Referencias (`references/`)

**Responsabilidad**:
- Proporcionar conocimiento reutilizable **por dominio**
- Mantener checklists, heurísticas, patrones, criterios de calidad
- Explicar conceptos **en profundidad** sin ser step-by-step
- Servir como fuente única de verdad técnica
- Minimizar improvisación del agente

**Característica**:
- 32 módulos independientes
- Cada uno cubre un dominio o tema específico
- No son guías paso a paso (eso va en playbooks)
- Pueden ser cargados de forma selectiva
- Actualizables independientemente

**Estructura de un módulo de referencia**:
```
# Título del dominio

## Resumen ejecutivo
[Qué es, por qué importa]

## Conceptos claveClaves
[Definiciones, TTPs, patrones]

## Checklists
[Lo que debe verificarse]

## Heurísticas de riesgo
[Cómo clasificar hallazgos]

## Criterios de calidad
[Cuándo es "suficientemente seguro"]

## Herramientas recomendadas
[Agnósticas si es posible]

## Referencias externas
[OWASP, NIST, CWE, mitre-attack, etc.]

## Ejemplos y patrones
[Código vulnerable vs seguro]

## Preguntas frecuentes
[Mitos, trampes comunes]
```

**32 Módulos actuales** (referencias/):
1. Authorization & Governance
2. Engagement Workflow
3. AI Code Execution
4. Network Security
5. OSINT & Asset Intelligence
6. Web / API / AppSec
7. Vulnerability Management
8. Cloud / Container / K8s
9. Identity / Endpoint / AD
10. Wireless / Remote Access
11. DFIR / Threat Hunting
12. Detection Engineering
13. Secure Engineering / SDLC
14. Reporting & Remediation
15. Labs & Learning
16. Architecture & Threat Modeling
17. Mobile & Client Security
18. Crypto & Key Management
19. Data Security & Privacy
20. Secrets & Supply Chain
21. SOC Operations & Use Cases
22. Purple Teaming
23. Checklists & Examples
24. AI Agent Operating Profiles
25. GRC / Risk / Maturity
26. Automation Patterns
27. Evidence & Logging Spec
28. Tool Selection Matrix
29. Remediation Patterns
30. Report Templates
31. Agent Safety Checklists
32. Domain Taxonomy Extended

Cada módulo es **completamente independiente** pero pueden conectarse vía referencias cruzadas.

---

### Nivel 3: Playbooks Operativos (`playbooks/`)

**Responsabilidad**:
- Convertir conocimiento general de referencias en **secuencias concretas**
- Guiar tareas recurrentes con **entradas claras, salidas definidas, límites explícitos**
- Definir **success criteria**
- Homogeneizar **entregables y formato**
- Conectar referencias con metodología

**Característica**:
- 6 playbooks operativos principales
- Cada uno es **end-to-end**: input → stdout → output
- Incluye ejemplos, templates, checklist
- Define responsabilidades, timelines, owner
- Permite variaciones pero con estructura interna clara

**Estructura de un playbook**:
```
# Playbook: [Nombre]

## Propósito
[Qué problema resuelve]

## Cuándo usar este playbook
[Indicadores de que aplica]

## Entradas requeridas
[Información que el cliente debe dar]

## Pre-requisitos
[Setup, acceso, aprobaciones necesarias]

## Timeline esperado
[Optimista, normal, pesimista]

## Fases del engagement

### Fase 1: Planificación
[Tareas, responsables, outputs]

### Fase 2: Ejecución
[Tareas, responsables, outputs]

### Fase 3: Análisis
[Tareas, responsables, outputs]

### Fase 4: Reporte
[Tareas, responsables, outputs]

## Success criteria
[Cuándo se considera completo]

## Common pitfalls
[Errores frecuentes, cómo evitar]

## Variaciones
[Cuando es corto, cuando es largo, etc.]

## Template de reporte
[Qué incluir en salida]

## Métricas de éxito
[KPIs del engagement]
```

**6 Playbooks principales**:
1. **Authorized Assessment** - Evaluación completa estructurada
2. **Web/API Review** - Auditoría de aplicaciones web
3. **Cloud/K8s Review** - Auditoría de infraestructura cloud
4. **Detection/Hunting** - Diseño de reglas y campañas de hunting
5. **Secure SDLC Review** - Auditoría de pipeline y código
6. **Incident Triage** - Respuesta inicial a incidentes

---

### Nivel 4: Scripts de Automatización pequeña (`scripts/`)

**Responsabilidad**:
- Automatizar tareas **pequeñas y bien definidas**
- Servir como **ejemplos de "agentic coding seguro"**
- Normalizar resultados en formatos reutilizables
- Generar evidencia verificable
- Reducir trabajo manual tedioso

**Características**:
- Máximo 200 líneas de código
- Completamente legibles (comentarios integrados)
- Sin credenciales hardcodeadas
- Con timeout, logging, rollback
- Agnósticos a stack
- Altamente reutilizables

**Scripts actuales**:
- `check_integrity.py` - Validación de referencias documentales
- `http_surface_audit.py` - Auditoría de headers de seguridad HTTP
- `normalize_findings.py` - Normalización de hallazgos (Burp → JSON estándar)
- `log_triage.py` - Triaje automático de logs
- `report_skeleton.py` - Generador de plantilla de reporte
- `run_skill_sanity.py` - Health check del sistema ORION
- `build_singlefile_site.py` - Constructor del sitio HTML monolítico
- `install-safe-tooling.sh` / `.ps1` - Instalador de herramientas auditable

Cada script sigue el patrón:
```
#!/usr/bin/env python3
"""Docstring con lo que hace, entradas, salidas, ejemplos."""

import [minimal deps]

def main() -> int:
    """Lógica principal, con logging y error handling."""
    ...
    return 0  # o 1 si error

if __name__ == "__main__":
    raise SystemExit(main())
```

---

### Nivel 5: Metadocumentación facilitadora (`*.md` en raíz)

**Responsabilidad**:
- Facilitar navegación de todo el sistema
- Conectar capas entre sí
- Explicar relaciones conceptuales
- Ser punto de entrada para usuarios nuevos

**Documentos**:
- `SKILL.md` - Orquestación, principios, guardrails
- `ARCHITECTURE.md` - Este documento; visión de capas
- `MODULE_MAP.md` - Inventario navegable de módulos
- `PLAYBOOK_INDEX.md` - Índice y descripción de playbooks
- `DOMAIN_TAXONOMY.md` - Clasificador de solicitudes por dominio
- `../README.md` - Punto de entrada de proyecto

---

## Flujo de Datos (End-to-End)

```
USER SOLICITUD
        ↓
   SKILL.md (Orquestación)
   ├─ ¿Autorización?
   ├─ ¿Hard stop?
   └─ Selecciona perfil operativo
        ↓
 DOMAIN_TAXONOMY.md (Clasificación)
 ├─ Identifica dominio primario
 └─ Identifica dominios secundarios
        ↓
 ARCHITECTURE.md (Orientación)
 └─ Explica qué capas se usan
        ↓
   MODULE_MAP.md (Navegación)
   └─ Decide qué referencias cargar
        ↓
  REFERENCES/ (Conocimiento)
  ├─ Ref 1: [Dominio principal]
  ├─ Ref 2: [Dominio secundario 1]
  └─ (Ref N opcional)
        ↓
   PLAYBOOKS/ (Metodología)
   └─ Playbook seleccionado (ej: 01-authorized-assessment)
        ↓
   SCRIPTS/ (Automatización)
   ├─ Script 1: normalize_findings.py
   ├─ Script 2: log_triage.py
   └─ (Script N opcional)
        ↓
   REPORTE FINAL
   ├─ Hallazgos normalizados
   ├─ Timeline de remediación
   ├─ Evidencia verificable
   └─ Contactos y next steps
```

---

## Patrones de Interacción Entre Capas

### Patrón 1: Discovery y Assessment
```
References (Network Security)
       ↓ (tool recomendations)
Playbooks (Authorized Assessment)
       ↓ (plan tareas)
Scripts (http_surface_audit.py)
       ↓ (ejecuta, recolecta)
Reporte (con findings normalizados)
```

### Patrón 2: Análisis de Código
```
References (Secure SDLC, Web AppSec)
       ↓ (checklists)
Playbooks (Secure SDLC Review)
       ↓ (plan fases)
References (CWE, OWASP TOP 10)
       ↓ (criterios específicos)
Scripts (custom parser)
       ↓ (normaliza hallazgos)
Reporte (violations + severity)
```

### Patrón 3: Hardening Iterativo
```
References (multiple: IaC, Cloud, Defense)
       ↓ (baselines: CIS, NIST)
Playbooks (Cloud/K8s Review)
       ↓ (gap analysis)
Scripts (check_integrity.py, custom linters)
       ↓ (auto-scan)
Iteration:
  - Identifica gap
  - Recomendación de remediación
  - Re-scan
  - Progreso (%)
```

### Patrón 4: Incident Response
```
SKILL.md (Activate Incident Response mode)
       ↓
References (DFIR, Detection, Defense)
       ↓
Playbooks (Incident Triage)
       ↓
Scripts (log_triage.py, custom parsers)
       ↓
Timeline reconstruction
       ↓
Root cause hypothesis
       ↓
Containment plan
       ↓
Reporte forense
```

---

## Características de Seguridad por Capa

### Nivel 1: Orquestación (SKILL.md)
- **Hard stops** integrados (lista de rechazos)
- **Guardrails de autorización**
- **Máquina de estados** clara (activar → operar → reportar)
- **Auditoría de decisiones**: se loga qué se decidió y por qué

### Nivel 2: Referencias
- **Sin credenciales** (nunca debe haber keys/passwords en ejemplos)
- **Agnósticas** (no favorecen herramienta/vendor)
- **Citable**: cada claim refiere a OWASP/NIST/CWE/etc.
- **Versionadas**: historial de cambios transparente

### Nivel 3: Playbooks
- **Success criteria claros** (cuándo se detiene)
- **Responsabilidades definidas** (quién aprueba qué)
- **Escalation procedures** (qué hacer si algo sale mal)
- **Rollback procedures** (cómo deshacer si es necesario)

### Nivel 4: Scripts
- **Sin credenciales** (solo variables de env)
- **Timeout integrado** (no corren infinito)
- **Logging exhaustivo** (cada paso se registra)
- **Reversible** (no modifica estado sin autorización)
- **Auditable** (código legible, comentado)
- **Testeable** (dry-run, mock, validación previa)

### Nivel 5: Metadocumentación
- **Versionada** (gitops, auditoría de cambios)
- **Verificable** (scripts de validación: run_skill_sanity.py)
- **Accesible** (sin dependencias externas; singlefile HTML también)

---

## Relaciones Clave Entre Capas

### SKILL ↔ REFERENCES
- SKILL no contiene conocimiento técnico
- SKILL solo decide "qué conocimiento cargar"
- Referencias son la fuente de verdad técnica

### REFERENCES ↔ PLAYBOOKS
- Playbooks usan referencias como material base
- Un playbook es "orquestar referencias en secuencia"
- Playbooks agregan: sequencing, timing, responsibility, success criteria

### PLAYBOOKS ↔ SCRIPTS
- Playbooks recomiendan tareas
- Scripts automatizan tareas que playbooks define
- Un playbook puede usar 0 o N scripts (no obligatorio)

### REFERENCES ↔ SCRIPTS
- Scripts implementan heurísticas de referencias
- Ej: normalize_findings.py implementa CVSS + severity de references/07-vulnerability-management.md

### TODAS ↔ ARQUITECTURA
- ARCHITECTURE.md explica cómo cada capa interactúa
- Es meta; no genera salidas por sí solo

---

## Caso de Uso: Auditoría Web End-to-End

```
1. Usuario: "Auditame mi app web"
   
2. SKILL.md
   - ¿Authorization? Sí, por cliente X
   - ¿Hard stop? No
   - Perfil: Assessment rápido (4-8h)
   - Módulos a cargar: Web/AppSec + Governance
   
3. DOMAIN_TAXONOMY.md
   - Dominio primario: Web / API / AppSec
   - Secundarios: Governance, Reporting
   
4. Carga REFERENCES:
   - references/06-web-api-appsec.md (técnica)
   - references/01-authorization-and-governance.md (contexto)
   - references/14-reporting-remediation.md (salida)
   
5. Ejecuta PLAYBOOKS/02-web-api-review-playbook.md
   - Fase 1: Reconnaissance & auth testing
   - Fase 2: Input validation, injection, XXS
   - Fase 3: Session, CORS, CSRF
   - Fase 4: Análisis y reporting
   
6. Usa SCRIPTS:
   - http_surface_audit.py (headers de seguridad)
   - normalize_findings.py (standariza Burp findings)
   - report_skeleton.py (estructura ejecutiva)
   
7. OUTPUT:
   - Hallazgos normalizados (JSON)
   - Reporte ejecutivo
   - Roadmap de remediación
   - Evidencia de validación (screenshots, pasos)
   
8. Cierre
   - Mapping de hallazgos a CVSS
   - Timeline sugerida (30-90-180 días)
   - Contacto post-engagement (soporte 2 semanas)
```

---

## Extensibilidad

### Agregar una Nueva Referencia
1. Crear `references/XX-new-topic.md`
2. Actualizaren MODULE_MAP.md
3. Actualizar DOMAIN_TAXONOMY.md si aplica
4. Script check_integrity.py valida automáticamente

### Agregar un Nuevo Playbook
1. Crear `playbooks/0X-new-workflow-playbook.md`
2. Relacionar con references que usa
3. Actualizar PLAYBOOK_INDEX.md
4. Validar estructura: entradas, fases, outputs, success criteria

### Agregar un Nuevo Script
1. Crear en scripts/ (máx 200 líneas)
2. Documentado, logueable, reversible
3. Agregar a run_skill_sanity.py si es validación
4. Actualizar MODULE_MAP.md

### Actualizar Guardrails o Política
1. Modificar SKILL.md (único punto de verdad)
2. Documentar cambio en SKILL.md
3. Ejecutar run_skill_sanity.py para validación
4. Versionar (git)

---

## Dependencias Externas (Minimizadas)

ORION está diseñado para ser **autónomo**:

- **Sin llamadas de red** (a menos que sea necesario, ej: http_surface_audit.py)
- **Sin keys hardcodeadas** (todo por variablesde entorno)
- **Sin vendor lock-in** (agnóstico a AWS/Azure/GCP, Python/Go/Rust, etc.)
- **Singlefile HTML** (ORION-HACKING-singlefile.html contiene TODO sin dependencias)

Herramientas externas **opcionales**:
- Burp Suite, ZAP (para web testing - recomendado pero no requerido)
- Nmap, Tenable, Qualys (para network scanning - agnóstico a cuál)
- SIEM (Splunk, ELK, Datadog) - para log analysis - agnóstico

---

## Métricas vs Calidad

ORION no mide "cuántos vulnerabilities encontramos" sino:

- **Coverage**: ¿Qué % del alcance fue validado?
- **Confiabilidad**: ¿Cuántas vulnerabs requirieron revalidación?
- **Accionabilidad**: ¿Cuántos hallazgos tienen roadmap claro?
- **Risk reduction**: ¿En cuánto se redujo el riesgo después de remediación?

Less is better si es **verified, documented, actionable**.

---

## Resumen: Los 3 Puntos de la Arquitectura

1. **Separación clara de responsabilidades**: Cada capa hace una cosa bien, no todo mezclado.
2. **Composabilidad**: Cualquier referencia + playbook + script pueden combinarse sin conflictos.
3. **Auditabilidad extrema**: Cada decisión se loga, se explica, se justifica. No hay "magia".

**Siguiente**: Lee SKILL.md para entender políticas, o MODULE_MAP.md para navegar módulos.
