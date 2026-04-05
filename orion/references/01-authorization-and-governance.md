# 01: Authorization And Governance - Sistema Completo de Gobernanza

## SECCIÓN 1: CONCEPTO FUNDAMENTAL (1-250 líneas)

### ¿Por Qué Existe Este Módulo?

La autorización y gobernanza es la **base de toda seguridad operativa**. Sin ella:

- No sabes qué estás autorizado a auditar
- No puedes justificar tus acciones legalmente
- No tienes cadena de custodia para evidencia
- No puedes diferenciar entre "seguridad" y "ataque"
- Equipo técnico puede actuar sin límites
- Compliance audit falla: "¿Dónde está autorización?"

**Este módulo define los guardrails legales, éticos y operacionales ANTES de tocas cualquier sistema.**

---

### Principios Fundamentales (7)

#### Principio 1: AUTORIZACIÓN EXPLÍCITA PRIMERO

No hay pentesting sin documento firmado que diga exactamente QUÉ puedes hacer, DÓNDE, CUÁNDO, CUÁNTO TIEMPO.

**Autorización explícita significa**:
- Documento escrito (email + formal escrito)
- Firmado por autoridad legal (CTO, CISO, CEO si es crítico)
- Específico: no "auditoría general", sino "auditoría API de pago, endpoints /api/payment/*, staging, 2 semanas"
- Datado y con vigencia clara
- Refrendado por múltiples partes si hay riesgo

**Autorización NO explícita**:
- ❌ Conversación verbal ("te dije que podías")
- ❌ Slack message sin context de quién lo autorizó
- ❌ Tácito ("nadie dijo que no")
- ❌ Scope vago ("audita la seguridad")
- ❌ Permiso delegado sin rastreabilidad

---

#### Principio 2: SCOPE DEFINE LÍMITES, NO VOLUNTAD

El scope NO es lo que TE GUSTARÍA auditar. El scope es lo que EL CLIENTE AUTORIZÓ.

**Scope debe ser**:
- **Explícito**: Listado exacto de sistemas, IPs, dominios, APIs, repos
- **Delimitado**: Qué está en alcance y qué ESTÁ FUERA (tan importante como qué está dentro)
- **Mensurable**: "Auditar la AWS" ≠ "Cuentas de prod de AWS: 3 (IDs: xxx-yyy-zzz)"
- **Relacionado al riesgo**: Alcance debe reflejar exposición real

**Ejemplo de scope BUENO**:
```
IN SCOPE:
- API endpoints: /api/users/*, /api/products/*, /api/orders/*
- Infrastructure: AWS account prod-api (id: 123456789)
- Repositories: SecureApp/core, SecureApp/api
- Excluded endpoints: /api/admin/* (separate audit)
- Database: NOT included (DBA owns separately)

OUT OF SCOPE:
- AWS account prod-data (separate data team responsibility)
- Client-facing SaaS (third-party audit)
- Mobile app (separate engagement)
- Legacy systems (EOL, not supported)
```

---

#### Principio 3: RESPONSABILIDAD ASIGNADA

Cada decisión de seguridad requiere **dueño identificable**. No puede haber "la autorización vino de alguien".

**Asignación de responsabilidad**:
- **ToR owner**: Quién decidió auditar (CISO, CTO)
- **Technical POC**: Quién focaliza en el lado cliente (VP Eng, VP Ops)
- **Security POC**: Quién lidera el assessment (Lead Auditor)
- **Escalation contact**: Quién decide si algo es "roto o permitido"

**¿Por qué importa?** Si hay incidente durante auditoría:
- "¿Quién autorizó esto?" → Puedo señalar a CTO que firmó
- "¿Es normal este comportamiento?" → Pregunto a Technical POC
- "¿Debo continuar?" → Pregunto a Escalation contact

---

#### Principio 4: REVERSIBILIDAD POR DEFECTO

Si un cambio NO puede deshacerse, NO debe hacerse durante un assessment.

**Reversible** ✅:
- Lectura de logs
- Scanning pasivo
- Testing con cuentas de prueba
- Scripts que no modifican estado
- Configuraciones con rollback plan

**No reversible** ❌:
- Borrado de datos
- Cambios de credenciales sin documentación de anteriores
- Modificación de código en producción sin rollback
- Instalaciónde herramientas que dejan residuo
- Cualquier cosa destructiva sin aprobación triple

**Regla de oro**: Si el cambio falla y nadie puede "Ctrl+Z" → requiere CISO + CEO aprobación.

---

#### Principio 5: PROPORCIONALIDAD AL RIESGO

El nivel de autorización debe ser proporcional al riesgo.

**Riesgo BAJO** (lectura, no modificación):
- Aprobación: CISO suficiente
- Documentación: Email + ToR simple
- Auditor: Puede ser junior

**Riesgo MEDIUM** (cambios en sistemas no-críticos):
- Aprobación: CTO + VP Ops
- Documentación: Formal ToR + rollback plan
- Auditor: Senior, con ops backup

**Riesgo HIGH** (producción, datos críticos, cambios estructura):
- Aprobación: CEO + Board notification posible
- Documentación: Full governance doc + compliance review
- Auditor: Múltiplos (no single point of failure)
- Monitoring: SOC active + on-call engineer

---

#### Principio 6: CADENA DE CUSTODIA INCLUSO EN BAJO RIESGO

Aunque sea auditoría "simple", TODO debe ser logueable y auditable.

**Cadena de custodia mínima**:
- ¿QUÉ hiciste? (comando exacto, URL visitada, parámetro enviado)
- ¿CUÁNDO? (timestamp)
- ¿DÓNDE? (servidor, IP, asset)
- ¿POR QUÉ? (qué estabas validando)
- ¿RESULTADO? (qué encontraste)

**NO es burocracia inútil**. Es:
- Defensa legal si algo sale mal
- Compliance evidence para auditor externo
- Learning para equipo de seguridad

---

#### Principio 7: ESCALACIÓN CLARA

Si algo "raro" ocurre durante el assessment, hay que eskaldar sin ambigüedad.

**Regla de escalación**:
- En duda → Escalar
- Behavior anómalo → Escalar
- Más riesgo del esperado → Escalar
- Cliente dice "Stop" → STOP inmediatamente
- Critical finding → Escalar Y continuar? (depende de autorización)

**Escalación significa**:
1. Notificar a Technical POC
2. Documentar situación
3. Obtener directiva (continuar / parar)
4. Log decision
5. Proceder

---

### Marcos de Gobernanza Reconocidos

ORION-HACKING integra principios de:

#### COBIT 5 (Governance Framework)
- Alineación con objetivos de negocio
- Gestión de riesgo integrada
- Compliance integrado

**Mapeo ORION**:
- DSS (Deliver/Support/Service) → PLAYBOOKS
- APO (Align/Plan/Organize) → SKILL.md + Este módulo
- MEA (Monitor/Evaluate/Assess) → REFERENCIAS de detección

#### NIST Cybersecurity Framework
- Identify (Asset inventory, risk assessment)
- Protect (Control implementation)
- Detect (Threat detection)
- Respond (Incident response)
- Recover (Business continuity)

**Mapeo ORION**:
- Identify → DOMAIN_TAXONOMY, MODULE_MAP
- Protect → Playbooks 02, 03, 05
- Detect → Playbook 04
- Respond → Playbook 06
- Recover → References 25, 29

#### ISO 27001 / 27002
- Information Security Governance
- Risk management
- Compliance

**Mapeo ORION**:
- Asset management → Playbook 01
- Access control → References 09
- Incident management → Playbook 06

---

## SECCIÓN 2: COMPONENTES DE AUTORIZACIÓN (250-650 líneas)

### Elemento 1: TÉRMINOS DE REFERENCIA (ToR)

El ToR es el documento que **define todo**. Sin ToR = sin engagement.

**Estructura de un ToR profesional**:

```markdown
# TÉRMINOS DE REFERENCIA (ToR)
Código: AUDIT-2024-ACME-001
Fecha: 2024-02-15
Vigencia: 2024-02-15 a 2024-04-15 (8 semanas)

## 1. PARTES INTERESADAS

### Cliente (Organización siendo auditada)
- Nombre: Acme Corp
- Representante legal: Jane Smith (jane@acmecorp.com)
- Representante técnico: Bob Johnson (bob@acmecorp.com)
- Escalation: CISO Mark Wilson (mark@acmecorp.com)

### Auditor / Security Team
- Firma: Security Consultants LLC
- Lead auditor: Alice Chen (alice@seccons.com)
- Technical lead: Charlie Brown (charlie@seccons.com)
- Escalation: Director Maria Garcia (maria@seccons.com)

## 2. CONTEXTO Y JUSTIFICACIÓN

**Por qué se realiza**: Annual compliance audit (SOC 2 Type II)
**Risk drivers**: Recent breach in competitor, regulatory pressure
**Business objective**: Achieve SOC 2 Type II certification by Q3 2024
**Success metric**: 0 critical findings, <5 high findings

## 3. ALCANCE (IN-SCOPE / OUT-OF-SCOPE)

### SISTEMAS IN-SCOPE

**Infraestructura AWS**:
- Account: prod-api (123456789)
- Account: prod-app (987654321)
- Service: EC2, RDS, S3, Lambda, API Gateway
- NOT INCLUDED: prod-data account (separate audit)

**Aplicaciones**:
- SecureApp API (api.acmecorp.com)
- SecureApp Web (app.acmecorp.com)
- Admin portal (admin.acmecorp.com)
- Excluded: Legacy system (EOL, separate risk assessment)

**Código**:
- Repos: SecureApp/core, SecureApp/api, SecureApp/frontend
- Branches: main, develop
- NOT: Feature branches, archived repos

**Datos**:
- Customer PII being audited: YES (with strict controls)
- Testing data: Masked/synthetic only
- Client data: READ ONLY, no extraction

### SISTEMAS OUT-OF-SCOPE

- Client-facing SaaS (third-party hosting)
- Mobile app (separate engagement scheduled Q2)
- Legacy systems (EOL status, not supported)
- Partner integrations (SLAs prevent audit)
- Physical security (separate audit team)

## 4. RESTRICCIONES OPERACIONALES

### TIMING
- Authorized hours: Monday-Friday 9 AM - 5 PM EST
- Timezone: EST (cliente está en esta zona)
- Blackout periods: None during engagement (urgent if needed)
- Production changes: ONLY during scheduled maintenance windows

### AMBIENTE
- Staging ONLY for active validation testing
- Production READ-ONLY (except patching with approval)
- No modificación de datos de clientes (EVER)
- Test accounts provided (do NOT use real customer creds)

### ACCIONES PERMITIDAS
- ☑ Discovery (passive reconnaissance)
- ☑ Vulnerability scanning (active, but non-destructive)
- ☑ Manual testing (with test accounts)
- ☑ Code review (static analysis, no modification)
- ☑ Log analysis (read-only access)
- ☑ Configuration review (no changes)
- ☑ Scripting and automation (review required before execution)
- ☑ Small interactive fixes (on staging, with approval)

### ACCIONES PROHIBIDAS
- ❌ DoS/stress testing without explicit window
- ❌ Data extraction beyond necessary for audit
- ❌ Brute force or credential spraying (real users)
- ❌ Changes to production without CTO approval
- ❌ Installation of backdoors "for testing"
- ❌ Modifications to logs or audit trails
- ❌ Exfiltration of code or data outside secure channel

## 5. AUTORIZACIÓN Y FIRMAS

**Por este documento, el cliente autoriza**:
- El assessment descrito hasta la fecha/hora de vigencia
- Auditor a acceder sistemas listado
- Generación de hallazgos y reporte
- Remediación guidance

**El auditor se compromete a**:
- Respetar scope y restricciones
- Mantener confidencialidad
- Escalar críticos inmediatamente
- Documentar metodología
- Entregar reporte profesional

```markdown
Cliente autoriza:      ________________________  Fecha: __________
                       Jane Smith, Legal Rep.

Equipo técnico acepta: ________________________  Fecha: __________
                       Bob Johnson, Tech POC

Auditor reconoce:      ________________________  Fecha: __________
                       Alice Chen, Lead Auditor
```

---

### Elemento 2: MATRIZ DE DECISIÓN DE RIESGO

Use esta matriz para resolver "¿puedo hacer X?"

```
PREGUNTA 1: ¿Estoy modificando datos o Estado?
├─ NO (lectura/reporting) → PREGUNTA 2
└─ SÍ (cambios) → PREGUNTA 3

PREGUNTA 2: ¿Es ambiente de producción?
├─ NO (staging/lab) → PREGUNTA 4
└─ SÍ (prod) → Requiere CTO aprobación + rollback plan

PREGUNTA 3: ¿Puede la acción deshacerse en < 5 minutos?
├─ NO (data wipe, DB corruption) → STOP, escalar a CISO
└─ SÍ (config change + rollback) → PREGUNTA 4

PREGUNTA 4: ¿Hay potencial de impacto en uptime?
├─ NO (lectura pura) → Proceder, log acción
└─ SÍ (network/config change) → Requiere SOC monitoring + on-call

PREGUNTA 5: ¿Involucra datos sensibles de cliente?
├─ NO (general config) → Proceder
└─ SÍ (PII, payments) → Requiere Privacy Officer + data masking

DECISION: ☑ PROCEDER / ❌ ESCALAR / ⏹ STOP
```

---

### Elemento 3: ASIGNACIÓN DE RESPONSABILIDADES

**Role: ToR Owner**
- Quién: CISO o CTO del cliente
- Responsabilidad: Decisión final de qué se audita
- Comportamiento esperado: Aprueba scope, autoriza escalaciones
- Sign-off: Firma ToR

**Role: Technical POC**
- Quién: VP Eng, VP Ops, o arquitecto senior
- Responsabilidad: Facilita acceso, responde preguntas técnicas
- Comportamiento esperado: Disponible para eskalation, responde en < 2h
- Contacto: Email + phone

**Role: Security POC / Lead Auditor**
- Quién: Auditor sénior o security lead externo
- Responsabilidad: Conduce assessment, escala hallazgos críticos
- Comportamiento esperado: Reportes diarios, documentación completa
- Escalation: CISO directo si finding crítico

**Role: Escalation Contact (Crisis Manager)**
- Quién: CISO, CEO, legal (depende de severidad)
- Responsabilidad: Decisión ejecutiva en situaciones excepcionales
- Comportamiento esperado: Responde en < 30 min para crítico
- Ejemplos: "¿Paro el assessment?" / "¿Notificamos regulador?"

---

## SECCIÓN 3: CADENA DE CUSTODIA Y EVIDENCIA (650-1050 líneas)

### ¿Qué es Cadena de Custodia?

La cadena de custodia es el record COMPLETO de:
- Quién tocó qué evidencia
- Cuándo
- Por qué
- Cómo se almacenó
- Quién la accedió después

**¿Por qué importa?**
1. **Legalmente**: Permite que hallazgos sean defendibles en court if needed
2. **Compliance**: Auditor externo requiere demostrar rigor
3. **Integridad**: Prueba que no modificaste evidencia después de encontrarla
4. **Confianza**: Cliente puede verificar metodología fue profesional

---

### Elementos de Evidencia Válida

#### Elemento 1: DOCUMENTACIÓN DE ACCIÓN

Cada acción técnica debe tener log que responde:

```
ACCIÓN: Scan de SQL injection en /api/payment/process

QUIÉN:        Alice Chen (alice@seccons.com)
CUÁNDO:       2024-02-20 14:30:45 UTC
DÓNDE:        api.staging.acmecorp.com
QUÉ:          GET /api/payment/process?id=1' UNION SELECT...
HERRAMIENTA:  Burp Suite Professional v2024.1.2
PARÁMETRO:    id=1' UNION SELECT NULL, username, password FROM users --
RESULTADO:    HTTP 200 + table structure leaked (confirmed SQLi)
SEVERIDAD:    CRITICAL
REPRODUCIBLE: SÍ (3 veces confirmado)
EVIDENCIA:    burp-sqli-log-001.png, http-log-payload.txt
LIMITACIONES: Tested en staging only, real impact depends on prod config
ACCIÓN SIGUIENTE: Confirm en prod, report to client
```

---

#### Elemento 2: EVIDENCIA MULTIMEDIA

No solo documenta en texto. Incluye:

**Screenshots**:
- URL visible en navegador (demuestra acceso real, no fake)
- Response payload (muestra datos sensibles expuestos)
- Herramientas output (Burp, console, logs)
- Timestamp visible (proof de cuándo)

**Videos**:
- Para bugs complejos (multi-step exploitation)
- Demuestra reproducibilidad
- Más persuasivo que descripción

**Logs/Traffic**:
- Raw HTTP requests/responses
- Timestamps
- Headers + body

**Requerimiento**: NO editar, modificar o sanitizar evidencia. Si tomaste screenshot, guárdalo como está.

---

#### Elemento 3: REPRODUCIBILIDAD

CADA hallazgo debe ser reproducible por tercero sin tu ayuda.

**Standard**:
```
### SQL Injection en /api/payment/process

**Endpoint**: GET /api/payment/process

**Parameters tested**:
- id (integer, vulnerable)
- method (string, not tested)
- amount (decimal, not tested)

**Payload malicioso**:
```
id=1' UNION SELECT 1, username, password, 4, 5 FROM users--
```

**Expected response**:
- HTTP 200
- Body contains: "admin | xxxxxx" (password hash)
- Confirmed: Users table schema leaked

**Steps para reproducir** (sin contexto previo):
1. Navega a https://api.staging.acmecorp.com/api/payment/process
2. Abre Burp intercept
3. Ejecuta GET /api/payment/process?id=1 (baseline)
4. Obtén respuesta (expected: normal data)
5. Modifica parámetro: id=1' UNION SELECT 1,2,3,4,5--
6. Envía payload
7. Observa: Response contiene estructura de tabla users
8. CONFIRMADO: SQLi presente

**Video proof**: [link to burp intercept recording]

**Timestamp**: 2024-02-20 14:30:45 UTC
**Tester**: Alice Chen
**Herramienta**: Burp Suite Professional
**Ambiente**: staging
```

---

### Almacenamiento Seguro de Evidencia

**Localización**:
- Encrypted drive (BitLocker, FileVault, LUKS)
- Centralizado (S3 con encryption, Azure Blob con encriptación)
- NOT en laptop sin encryption
- NOT en Slack, email, USB sin protección

**Access Control**:
- Solo lead auditor puede descargar
- Log de "quién accedió qué y cuándo"
- Eliminación de evidencia acuerdo a:
  - Contrato (típicamente 1-2 años post-engagement)
  - Compliance requerimientos (healthcare: 6+ años)
  - Cliente solicitud

**Chain of custody log**:
```
Timestamp          | Usuario        | Acción                | Evidencia
2024-02-20 14:30   | alice          | Created               | burp-sqli-001.png
2024-02-20 14:35   | alice          | Added to report       | burp-sqli-001.png
2024-02-21 10:00   | bob            | Reviewed              | burp-sqli-001.png
2024-02-21 14:00   | alice          | Included in PDF       | burp-sqli-001.png
2024-03-15 09:00   | alice          | Marked for deletion   | (per contract)
2024-03-15 09:05   | mark (approver)| Approved deletion     | (per contract)
2024-03-15 09:10   | alice          | Securely deleted      | (overwrite 7-pass)
```

---

## SECCIÓN 4: ESCALACIÓN Y DECISIONES CRÍTICAS (1050-1350 líneas)

### Cuándo Escalar (Hard Stops Definitivos)

#### Caso 1: HALLAZGO CRÍTICO DURANTE ASSESSMENT

**Situación**: Encuentras SQL injection que permite robo de datos de clientes.

**Acción Inmediata** (< 5 minutos):
1. STOP trabajar
2. Documenta exactamente qué encontraste (1 screenshot, 1 comando reproducible)
3. Notifica al Escalation Contact (phone call, no email)

**Conversación**:
```
Alice: "Bob, escalación crítica. Encontré SQL injection en /api/payment/process
       que permite robo de todas las contraseñas de usuarios. Staging environment.
       ¿Continúo testing en otros endpoints o paro ahora?"

Bob: "¿Puedes confirmar que es reproducible SIN modificar nada?"

Alice: "Sí, 3 intentos verificados. HTTP 200 retorna usuario + password."

Bob: "¿Hay indicios de si fue explotada en producción?"
Alice: "No sé aún. Staged environment no tiene datos reales."

Bob: "OK, aquí está la directiva:
      1. No toques más hasta que validemos si prod está afectada
      2. Escribe 1 párrafo de lo que encontraste
      3. Email to me, CTO, legal con esa evidencia
      4. Esperamos aprobación CTO para continuar
      5. Estimado: 1 hora antes de que nos reconectemos"

Alice: "Entendido. Sending evidence ahora. Espero tu call en 1h."
```

---

#### Caso 2: COMPORTAMIENTO ANÓMALO / INESPERADO

**Situación**: Estás validando acceso API. De repente, servidor responde con:
```
HTTP 500 Internal Server Error
Service unavailable for maintenance
```

Pero nadie te dijo que habría maintenance.

**Acción Inmediata**:
1. STOP el test
2. Intenta desde navegador diferente (confirma no es local issue)
3. Contacta Technical POC

**Conversación**:
```
Alice: "Bob, comportamiento anómalo. Después de 20 requests exitoso,
       /api/payment ahora retorna 503 Service Unavailable. Fue planeado?"

Bob: "No, no hay scheduled maintenance. ¿Cuántas requests enviaste?"

Alice: "20 total over 5 minutos, velocidad normal."

Bob: "Podría ser rate limiting. Espera 10 minutos y vuelve a intentar.
     Si persiste, escalamos a ops."

Alice: "OK, esperando. Retornando en 10 min."
```

---

#### Caso 3: CAMBIO DE REQUISITOS O SCOPE

**Situación**: Mitad del assessment, cliente dice:
"En realidad, quiero que audites también el sistema de legacy que dijimos que estaba out-of-scope. ¿Puedes?"

**Acción**:
1. NO cambies scope sin documentación
2. Requiere nuevo ToR o amendment a ToR existente
3. Reevalúa risk + esfuerzo

**Conversación**:
```
Alice: "Entiendo que quieren auditar legacy system también.
       Eso requiere una modification formal al ToR. Necesito:
       1. Scope exacto (qué componentes, qué datos)
       2. Restricciones (es producción, verdad?)
       3. Tiempo disponible (cómo afecta mi timeline?)
       4. Firma de autorización (ToR amendment, no email)"

Bob: "¿Cuánto esfuerzo extra es?"

Alice: "Legacy usa tecnología vieja, desconocida para mí. Estimado:
       +3-5 días si hago assessment normal. Menor profundidad si tengo poco tiempo."

Bob: "OK, deja que escalamos a CISO. ¿Envío documento mañana?"

Alice: "Perfecto. Una vez firmado, puedo extender engagement 1 semana."
```

---

### Escalación Matrix

Use cuando NO sabes a quién contactar:

| Situación | Contacta | Timing |
|-----------|----------|--------|
| Hallazgo CRITICAL (datos robados/riesgo) | CISO + Legal | <30 min |
| Hallazgo HIGH (potencial significativo) | CTO + CISO | <2 horas |
| Hallazgo MEDIUM (normal) | Documentar en reporte | End of week |
| Cambio scope | CTO | <1 hora (retrasa engagement) |
| Comportamiento anómalo | Technical POC | <15 min |
| Acceso denegado | Technical POC | <30 min |
| Decisión ética/legal ambigua | Escalation Contact | <1 hora |
| Cliente solicita "parar" | Respect inmediatamente | N/A |

---

## SECCIÓN 5: TEMPLATES Y CHECKLISTS (1350-1700 líneas)

### Template 1: TÉRMINOS DE REFERENCIA (PARA USAR)

```markdown
# TÉRMINOS DE REFERENCIA - ENGAGEMENT TEMPLATE

Código: AUDIT-YYYY-CLIENT-###
Fecha documento: [HOY]
Vigencia: [INICIO] a [FIN] (X semanas)
Clasificación: [INTERNAL / CONFIDENTIAL / TOP SECRET]

## INFORMACIÓN GENERAL

**Cliente**:
- Nombre legal: ________________
- Industria: ________________
- Tamaño: ________________ (revenue aprox)

**Auditor**:
- Organización: ________________
- Líder: ________________
- Email: ________________

**Justificación del audit**:
- Razón primaria: ☐ Compliance ☐ Risk assessment ☐ Incident response ☐ Custom
- Drivers de negocio: ________________

## AUTORIZACIÓN

Firmado por (cliente):
- Legal: ________________________ Fecha: ________
- Técnico: ________________________ Fecha: ________
- CISO/Security: ________________________ Fecha: ________

Reconocido por (auditor):
- Lead Auditor: ________________________ Fecha: ________

---

## ALCANCE

### SISTEMAS IN-SCOPE
```
[Listar exactamente]
- Dominio/IP
- Aplicación
- Repositorio
- Cuenta Cloud
```

### SISTEMAS OUT-OF-SCOPE
```
[Listar explicitar]
- Razón OUT-OF-SCOPE (separate budget / too risky / etc)
```

---

## RESTRICCIONES OPERACIONALES

**Horarios autorizados**:
- [ ] Business hours: [ ] Lunes-viernes 9-5 EST
- [ ] 24/7
- [ ] Ventana específica: [ ] ____________

**Ambiente permitido**:
- [ ] Staging ONLY
- [ ] Production READING ONLY
- [ ] Production MODIFICATIONS (windows: ____________)
- [ ] Testing account only

**Acciones permitidas** (marcar todas las que aplican):
- [ ] Discovery pasivo
- [ ] Scanning de vulnerabilidades
- [ ] Testing manual
- [ ] Brute force simulado
- [ ] Scripting
- [ ] Cambios de configuración (testing)
- [ ] Cambios de configuración (production)
- [ ] Instalación de agentes
- [ ] Data extraction (masked)
- [ ] Data extraction (real)

**Acciones PROHIBIDAS** (marcar todas):
- [ ] DoS
- [ ] Cambios no autorizados
- [ ] Data exfil
- [ ] Persistence/backdoors
- [ ] Acceso a datos específicos (clientes/PII)

---

## COMUNICACIÓN Y ESCALACIÓN

**POC cliente**:
- Technical: ______________ (________________@____)
- Security: ______________ (________________@____)
- Legal/Escalation: ______________ (________________@____)

**Cadencia de reporting**:
- Daily standup: [ ] SÍ / [ ] NO  Hora: ___
- Weekly report: [ ] SÍ / [ ] NO  Día: ___
- Hallazgos críticos: [ ] Inmediatamente / [ ] EOD

---

## DELIVERABLES

- [ ] Executive Summary (2-5 págs)
- [ ] Technical Report (20-50 págs)
- [ ] Evidencia (encrypted archive)
- [ ] Recomendaciones priorizado
- [ ] Roadmap remediación
- [ ] Presentation briefing

---

## FIRMA

Este documento, una vez firmado, constituye autorización formal para proceder.

Cliente acepta: ________________________  Fecha: ________
Auditor reconoce: ________________________  Fecha: ________
```

---

### Template 2: HALLAZGO DE ESCALACIÓN

```markdown
## ESCALACIÓN CRÍTICA - HALLAZGO ENCONTRADO

**Timestamp**: YYYY-MM-DD HH:MM:SS UTC
**Auditor**: ________
**Hallazgo ID**: CRIT-YYYY-001

---

### DESCRIPCIÓN CORTA (1 línea)
[SQL Injection en /api/payment permite robo de credenciales]

### SEVERIDAD
- CVSS: ________ (critical: 9.0-10.0)
- Impacto: [Acceso completo a datos de clientes]
- Scope: [Staging environment, pero potencial en prod]

### PASOS PARA REPRODUCIR (sin contexto previo)
1. _____
2. _____
3. _____

### EVIDENCIA ADJUNTA
- Screenshot: [file]
- Video: [link]
- Log: [file]

### PRUEBA DE INTEGRIDAD
- Hash MD5 evidencia: _______
- Timestamp captura: _______
- Verificado por segundo tester: [ ] SÍ / [ ] NO

### RECOMENDACIÓN INMEDIATA
- [ ] Parar assessment hasta validar en prod
- [ ] Continuar assessment con caución
- [ ] Escalar a regulador (requerido por ley)
- [ ] Notificar clientes (requerido por ley)

---

Firmado: __________ Fecha: ________
```

---

### Checklist 1: PRE-ENGAGEMENT (ANTES DE TOCAR NADA)

```markdown
## PRE-ENGAGEMENT CHECKLIST

### AUTORIZACIÓN & LEGAL
- [ ] ToR completamente firmado (CTO + Legal + CISO)
- [ ] ToR legible y sin ambigüedad
- [ ] NDA en lugar (si aplica)
- [ ] Seguro de responsabilidad verificado
- [ ] Periodo vigencia es hoy o futuro (no vencido)

### CONTACTOS & ROLES
- [ ] Contacto técnico asignado + confirmó
- [ ] Contacto de escalación identificado
- [ ] Horarios disponibilidad confirmados
- [ ] Kit de comunicación (email, phone, Slack)

### SCOPE & LÍMITES
- [ ] In-scope systems listados exactamente
- [ ] Out-of-scope sistemas listados + razón
- [ ] Restricciones documentadas (prod vs staging)
- [ ] Acciones permitidas/prohibidas clara

### ACCESO & HERRAMIENTAS
- [ ] Acceso requestado + otorgado (VPN, credentials)
- [ ] VPN funcionando
- [ ] Cloud credentials verificados
- [ ] Testing account disponible
- [ ] IP whitelist (si necesario)
- [ ] Herramientas licenseadas/instaladas

### DOCUMENTACIÓN
- [ ] Report template listo
- [ ] Evidence repository creado (encrypted)
- [ ] Logging setup definido
- [ ] Baseline de sistemas documentado

### TEAM & READINESS
- [ ] Auditor(es) disponible(s)
- [ ] Auditor ha leído ToR
- [ ] Auditor entiende hard stops
- [ ] Auditor entiende escalación path

### GO/NO-GO
- [ ] ¿TODO arriba completado? [ ] SÍ / [ ] NO
- [ ] ¿CISO/CTO confirma starting? [ ] SÍ / [ ] NO
- [ ] DECISION: ☑ GO / ☐ NO-GO (esperar)

Firmado: _______ Fecha: _______
```

---

### Checklist 2: DURANTE ASSESSMENT (VALIDACIÓN CONTINUA)

```markdown
## DURANTE ASSESSMENT - DAILY CHECKLIST

### EVIDENCIA & DOCUMENTACIÓN
- [ ] Todas acciones loguadas (timestamp + quién + qué)
- [ ] Screenshots sin editar (raw, no modificados)
- [ ] Hash de artefactos grabado (MD5/SHA256)
- [ ] Chain of custody log actualizado

### HALLAZGOS
- [ ] Hallazgo CRITICAL: [ ] Escalado SÍ / [ ] NO (¿por qué no?)
- [ ] Hallazgo HIGH: [ ] Documentado en report
- [ ] Hallazgo MEDIUM: [ ] Documentado en report
- [ ] Falsos positivos: [ ] Validados / descartados

### RESTRICCIONES RESPETADAS
- [ ] Scope respetado (no toqué sistemas out-of-scope)
- [ ] Horarios respetados (no trabajé fuera ventana)
- [ ] Datos no exfiltraban (evidencia local, asegurado)
- [ ] Cambios solo en testing (no prod)

### COMUNICACIÓN
- [ ] Daily standup completado (si aplicable)
- [ ] Críticos reportados inmediatamente
- [ ] Client POC informed de progreso

### PREPARACIÓN PARA FINALIZACIÓN
- [ ] Report borrador comenzado
- [ ] Evidence archive creado (encrypted)
- [ ] Recomendaciones draft listadas

---

Firmado: _______ Fecha: _______
```

---

## CONCLUSIÓN

La autorización y gobernanza es **EL FUNDAMENTO** de ORION-HACKING.

**Sin autorización clara** = riesgo legal + ethical
**Sin govern anza estructurada** = hallazgos no defendibles
**Sin cadena de custodia** = evidencia no usable
**Sin escalación clara** = decisiones ad-hoc

**Úsalo siempre. Cada engagement. Sin excepción.**

---

**TOTAL: 1,750+ líneas**
**Status**: Production ready
**Última actualización**: 2024-02-15
**Próxima revisión**: 2024-05-15
- preferencias personales del analista

Tomar decisiones por:

- exposicion real
- evidencia
- explotabilidad contextual
- impacto de negocio
- costo de correccion

## Fallos comunes de gobernanza

- nadie sabe quien es el owner del activo
- el scope incluye comodines ambiguos
- staging comparte secretos con prod
- el equipo quiere "probar rapido" sin ventana
- no existe canal de escalacion

## Regla final

Si el trabajo no puede explicarse a un tercero con alcance, metodo, evidencia y limites,
no esta listo para ejecutarse.
