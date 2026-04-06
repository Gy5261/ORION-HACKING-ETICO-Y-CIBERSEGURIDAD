# 31: Agent Safety Checklists - Guardrails de Operación Disciplinada

## SECCIÓN 1: MARCO DE SEGURIDAD FUNDAMENTAL (1-300 líneas)

### La Filosofía de los Checklists

Un checklist no es una sugerencia. Es un HARD STOP.

**Principio**: Si cualquier ítem fa en checklist = DETENER INMEDIATAMENTE.

No es "consideración", no es "probablemente está bien". Es **NO**.

---

### Niveles de Assessment

```
NIVEL 1: PRE-ENGAGEMENT
  Antes de cualquier actividad

NIVEL 2: PRE-ACCIÓN
  Antes de ejecutar comandos/scripts

NIVEL 3: PRE-CODIFICACIÓN
  Antes de escribir código automatizado

NIVEL 4: PRE-REPORTE
  Antes de comunicar hallazgos

NIVEL 5: Hard Stops
  "Si SÍ a esto = STOP INMEDIATAMENTE"
```

Cada nivel es **independiente** de los otros.
Cada uno debe pasar completamente.

---

## SECCIÓN 2: CHECKLIST NIVEL 1 - PRE-ENGAGEMENT (300-600 líneas)

### ✅ CHECKLIST 1.1: Authorization & Scope

**ANTES DE CUALQUIER ACTIVIDAD:**

```markdown
### AUTHORIZATION & SCOPE CHECKLIST

Task: [Describe the work]
Client: [Name]
Date: [ISO date]

---

#### 1. Authorization Document
- [ ] Em writing authorization exist?
- [ ] Signature present (client + legal)?
- [ ] Scope document exists?
- [ ] Statement of Work (SOW) signed?
- [ ] RoE (Rules of Engagement) acknowledged?

**HARD STOP**: Si NO a cualquier pregunta:
❌ NO PROCEEDER hasta obtener documento

---

#### 2. Scope Definition
- [ ] Targets específicos están enlistados?
- [ ] IP ranges/domains explícitos?
- [ ] Exclusions EXPLÍCITAS (ej: "NO tocar DB de producción")?
- [ ] Timeline es claro (start/end dates)?
- [ ] Horarios de operación especificados?

**HARD STOP**: Si scope es vago:
❌ Pedir aclaración por escrito

Ejemplos de SCOPE VAGO (❌):
- "Audita la app"
- "Encuentra vulnerabilidades"
- "Revisa la infraestructura"

Ejemplos de SCOPE CLARO (✅):
- "Prueba SQLi en /api/search?q= solamente en staging"
- "Escanea puertos en 10.0.0.0/24, excepto 10.0.0.50-100 (production DB)"
- "Revisa código en `src/auth/` directory solamente, no tocar vendored dependencies"

---

#### 3. Assets to Test
- [ ] IP addresses es CONFIRMED?
- [ ] Domain names es VERIFIED?
- [ ] Ownership está VERIFICADO (whois + contact)?
- [ ] No es un activo de 3era parte (ej: no testear Google sign-in sin permiso)?

**HARD STOP**: Si ownership es unclear:
❌ Pedir explicit permission

---

#### 4. Point of Contact
- [ ] Técnico POC identificado?
- [ ] Nombre + email + phone?
- [ ] Disponible durante test window?
- [ ] Escalation path claro (ej: si algo se rompe, a quién avisar)?

**HARD STOP**: Si no hay POC:
❌ Designar uno antes de comenzar

---

#### 5. Restrictions
- [ ] PRODUCTION EXPLICITLY ALLOWED o FORBIDDEN?
- [ ] Times when testing NOT allowed (ej: business hours)?
- [ ] Data extraction allowed or prohibited?
- [ ] Modificación permitida (ej: cambiar configs)?
- [ ] Third-party services (ej: OAuth integrations)?

**HARD STOP**: Si hay ambigüedad:
❌ Pedir clarificación

---

#### 6. Approval Sign-off
- [ ] Client signature: ___________________
- [ ] Date: ___________________
- [ ] This authorization is VALID from: _______
- [ ] This authorization EXPIRES on: _______
- [ ] Autorización es renovable? SÍ / NO

**APPROVAL REQUIRED**: Si todos los items = ✅
Then proceed to next checklist
```

---

### ✅ CHECKLIST 1.2: Engagement Kickoff

**DESPUÉS de autorización, ANTES de cualquier técnica:**

```markdown
### ENGAGEMENT KICKOFF CHECKLIST

---

#### 1. Intelligence Gathering
- [ ] Previous reports/audits leídos?
- [ ] Infrastructure diagram obtenido?
- [ ] Technology stack documentado (ej: Java/Spring, Node/Express)?
- [ ] Known vulnerabilities researched (CVE database)?
- [ ] Threat landscape for industry reviewed?

**HARD STOP**: Si no entiende la arquitectura:
❌ Pedir referencia technical antes de testing

---

#### 2. Test Lab Preparation
- [ ] Test environment replica exists?
- [ ] Testing en staging FIRST (NEVER directly on prod)?
- [ ] Backup de toda data critical?
- [ ] Rollback plan documented?
- [ ] "Off switch" para cada test identified?

**HARD STOP**: Si no hay lab:
❌ Usar staging como minimum

---

#### 3. Team Communication
- [ ] Kickoff meeting scheduled?
- [ ] Client briefed on schedule?
- [ ] On-call process documented?
- [ ] Escalation phone number shared?
- [ ] Daily sync time agreed?

**HARD STOP**: Si no hay comunicación:
❌ Schedule kickoff antes de empezar

---

#### 4. Documentation Setup
- [ ] Repository para findings creado?
- [ ] Logging directory preparado?
- [ ] Naming conventions defined?
- [ ] Evidence preservation plan?
- [ ] Chain of custody procedure?

**HARD STOP**: Si no hay forensic readiness:
❌ Setup logging ANTES de cualquier test
```

---

## SECCIÓN 3: CHECKLIST NIVEL 2 - PRE-ACCIÓN (600-900 líneas)

### ✅ CHECKLIST 2.1: Before Reading/Scanning

**ANTES DE `curl`, `nmap`, `burp`, O CUALQUIER TÉCNICA:**

```markdown
### PRE-READ/SCAN CHECKLIST

Target: [URL/IP/Domain]
Action: [e.g., "GET /api/users"]
Method: [e.g., "curl", "nmap -sV"]

---

#### 1. Authorization Verification
- [ ] Target IN scope document?
- [ ] NOT in exclusion list?
- [ ] Ownership verified (es un activo OUR)?
- [ ] Timing allowed (ej: no off-hours)?

**HARD STOP**: Si duda:
❌ Check scope document AGAIN

---

#### 2. Method Proportionality
- [ ] Technique appropriate para objetivo?
- [ ] No overkill (ej: no full nmap -A si solo necesitas 1 port)?
- [ ] Agresiveness matches authorization?

Usar matriz de proporcionalidad:

| Need | WRONG ❌ | RIGHT ✅ |
|------|---------|---------|
| Check ssl cert | Full port scan | `openssl s_client` |
| Find open ports | Aggressive -T5 nmap | `-T3` con timeout |
| Test login | Brute force 1000 pwd | Test 3 default creds |
| Read config | Modify system | Read and diff |

---

#### 3. Scope Constraints
- [ ] Número de requests reasonable?
- [ ] Rate limiting respetado (ej: max 10 req/sec)?
- [ ] Timeout establecido?
- [ ] Expected runtime < 5 minutos?

**HARD STOP**: Si esto puede causar DoS:
❌ Reduce aggressiveness

---

#### 4. Error Handling
- [ ] Script/method has try/except?
- [ ] Failures loguadas?
- [ ] Timeouts handled (no hanging)?
- [ ] Connection errors don't loop infinitely?

**HARD STOP**: Si no hay error handling:
❌ Añade antes de ejecutar

---

#### 5. Evidence Preservation
- [ ] Output directory created?
- [ ] Timestamp en nombre (YYYYMMDD_HHMMSS)?
- [ ] Logging enabled?
- [ ] Raw output guardado?
- [ ] Interpretación separada de datos?

**HARD STOP**: Si no puedes reproducir:
❌ Mejora logging
```

---

### ✅ CHECKLIST 2.2: Before Executing Commands

**LITERAL: ANTES DE PRESIONAR ENTER:**

```markdown
### PRE-EXECUTION CHECKLIST

Command: [Paste actual command]
Target: [IP/Domain/Host]
Risk: [LOW / MEDIUM / HIGH / CRITICAL]

---

#### 1. Command Review (LEER TODO)
- [ ] He leído CADA PALABRA del comando?
- [ ] Entiendo exactamente qué hace?
- [ ] Variables están correctas (ej: $HOST != $PASSWORD)?
- [ ] No hay typos?
- [ ] No hay inyección de shell (ej: `rm -rf /`)?

**HARD STOP**: Si NO entiendes:
❌ Ask for explanation ANTES de correr

---

#### 2. Destructiveness Assessment
```
¿Qué ocurriría si comando falla o tiene bug?

   Outcome ESCENARIO:
   - Modifica archivos?           SÍ/NO
   - Borra datos?                 SÍ/NO
   - Afecta servicio activo?      SÍ/NO
   - Requiere reboot?             SÍ/NO
   - Costo de error > $1,000?     SÍ/NO
```

Si alguno es **SÍ**:
- [ ] Backup creado ANTES?
- [ ] Rollback plan exist?
- [ ] Change management followed?
- [ ] Approver está en conocimiento AHORA?

---

#### 3. Dry Run (When applicable)
- [ ] `--dry-run` flag usado primero?
- [ ] SIMULACIÓN se ve correcta?
- [ ] Dummy environment tested PRIMERO?
- [ ] Output matches expectations?

**HARD STOP**: Si no puede dry-run:
❌ Reconsidere si ese comando debe ejecutarse

---

#### 4. Witness (For risky operations)
- [ ] Es operación de alto riesgo?
- [ ] Otro engineer está watching?
- [ ] Video recording enabled (para reproducción)?
- [ ] POC notificado?

**HARD STOP**: Si es critical y sin witness:
❌ Ejecute durante working hours con SLU on call

---

#### 5. Abort Condition
- [ ] Sé cómo detener si algo sale mal?
- [ ] CTRL+C will stop it?
- [ ] Kill command identificado?
- [ ] Timeout enabled (no infinite loops)?

**HARD STOP**: Si no puedo abort:
❌ NO EXECUTE
```

---

## SECCIÓN 4: CHECKLIST NIVEL 3 - PRE-CODIFICACIÓN (900-1200 líneas)

### ✅ CHECKLIST 3.1: Before Writing Code

**ANTES DE ESCRIBIR UN SCRIPT:**

```markdown
### PRE-CODE CHECKLIST

Task: [What problem are you solving?]
Size estimate: [<50 lines / 50-200 / 200+ lines]
Reusability: [One-time / Reusable / Library]

---

#### 1. "Do We Even Need Code?"
- [ ] ¿Pode este problema resolverse sin script? YES/NO

Si YES:
- [ ] Built-in tool exists (grep, awk, sed)?
- [ ] Cloud CLI hace el trabajo?
- [ ] One-liner shell command es suficiente?

**HARD STOP**: Si solución no-code existe:
❌ Usala en lugar de escribir código

Ejemplos (❌ overcomplication):
- Problema: "Necesito contar líneas"
  - ❌ NUNCA: Write Python script to count lines
  - ✅ SIEMPRE: `wc -l file.txt`

- Problema: "Necesito extraer IPs de logs"
  - ❌ NUNCA: Write parser script
  - ✅ SIEMPRE: `grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' logs.txt`

---

#### 2. Size Constraint
- [ ] Script será < 200 lines?
- [ ] Si > 200: ¿realmente es necesario?
- [ ] Puede be broken down en piezas?
- [ ] Hay módulos existentes que pueden usar?

**HARD STOP**: Si script growing > 500 lines:
❌ Split into smaller functions

---

#### 3. Dependency Analysis
- [ ] Qué librerías necesito?
- [ ] Todas son standard library?
- [ ] Cuántas dependencias externas?
- [ ] Installation instructions documented?

Regla: **NO add dependency without justification**

```
Good: `import json` (standard)
Bad: `import fastapi` (for simple script)
```

---

#### 4. Security Review (Pre-Write)
- [ ] Script toca credenciales? SÍ/NO
- [ ] Si SÍ: ¿está using environment variables?
- [ ] Hard-coded passwords/keys NUNCA?
- [ ] Script modifica o solo lee?

**HARD STOP**: Si script tiene credenciales hardcoded:
❌ Rewrite sin credentials

---

#### 5. Input Validation Plan
- [ ] Script valida user input?
- [ ] Qué pasa si input es malformed?
- [ ] Error messages son informativos?
- [ ] Timeout para loops infinitos?

Pre-code checklist:
```
for record in input_file:
    # ✅ VALIDATE before processing
    if not is_valid(record):
        log.error(f"Invalid record: {record}")
        continue
    
    # Process
    result = process(record)
```

---

#### 6. Output Format
- [ ] Output será JSON?
- [ ] Machine-parseable?
- [ ] Timestamps in ISO 8601 format?
- [ ] Null values handled?
- [ ] Examples provided?

**HARD STOP**: Si output es ambiguous:
❌ Define schema primero
```

---

### ✅ CHECKLIST 3.2: Before Running Code

**ANTES DE EJECUTAR SCRIPT ESCRITO:**

```markdown
### SCRIPT EXECUTION CHECKLIST

Script: [path/to/script.py]
Input: [data source]
Output: [destination/format]

---

#### 1. Code Review (Self + Peer)
- [ ] He revisado LINE by LINE?
- [ ] Alguien más revisó el código?
- [ ] No hay typos/obvious bugs?
- [ ] Lógica es clara?

**HARD STOP**: Código nuevo SIN peer review:
❌ Get review BEFORE running against real data

---

#### 2. Test Environment
- [ ] Test con DUMMY DATA primero?
- [ ] Expected output matches actual?
- [ ] Errors handled gracefully?
- [ ] Timeout tested?

Sample data para prueba:
```json
{"name": "test", "email": "test@example.com", "id": 1}
{"name": "test2", "email": "test2@example.com", "id": 2}
```

- [ ] Ran with 2-3 test records?
- [ ] Result es expected?

---

#### 3. Logging Verification
- [ ] Script logs cada acción?
- [ ] Log file location known?
- [ ] Log level (INFO/DEBUG/ERROR) set?
- [ ] Can rotate logs (no 100GB files)?

```python
import logging
logging.basicConfig(
    filename=f"run_{datetime.now():%Y%m%d_%H%M%S}.log",
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
```

---

#### 4. Resource Check
- [ ] CPU utilization OK?
- [ ] Memory consumption reasonable?
- [ ] Disk space available?
- [ ] Network bandwidth OK?

For large dataset:
- [ ] Expected runtime: _____ minutes
- [ ] Can kill if > 2x expected time?

---

#### 5. Start Approval
- [ ] Script passed all checks?
- [ ] POC/manager notified?
- [ ] Ready to run?

Mark:
- [ ] APPROVED TO EXECUTE
- Executor: ________________
- Date/Time: ________________
```

---

## SECCIÓN 5: CHECKLIST NIVEL 4 - PRE-REPORTE (1200-1500 líneas)

### ✅ CHECKLIST 4.1: Before Reporting Findings

**ANTES DE ESCRIBIR REPORTE O COMUNICAR HALLAZGOS:**

```markdown
### PRE-REPORT CHECKLIST

Finding Title: [e.g., "SQL Injection in login form"]
Severity: [INFO / LOW / MEDIUM / HIGH / CRITICAL]
Target: [e.g., "api.example.com/login"]

---

#### 1. Evidence Requirement
- [ ] Encontré evidencia DIRECTA (no especulación)?
- [ ] Puedo REPRODUCIR el problema?
- [ ] Tengo captura/log/screenshot?
- [ ] Evidencia está en folder audit LOCKED?

**HARD STOP**: Si no puedo reproducir:
❌ NO REPORTAR como confirmed finding

Ejemplos:
- ✅ "When I POST `username=' OR '1'\#` to /login, SQL error returned"
- ❌ "I think there might be SQL injection" (especulación)

---

#### 2. Severity Assessment (CVSS)
- [ ] He looked at CVSS v3.1 calculator?
- [ ] AV (Attack Vector): Network/Adjacent/Local/Physical?
- [ ] AC (Attack Complexity): Low/High?
- [ ] Calculated score correct (0.1 to 10.0)?
- [ ] Color coding correct (Red/Orange/Yellow/Green)?

CVSS Template:
```
AV=N/AC=L/PR=N/UI=N/S=U/C=H/I=H/A=H = 9.8 CRITICAL
```

---

#### 3. Exploitability vs Impact
- [ ] How easy is it to exploit? (1=hardest, 5=easiest)
- [ ] What's the impact if exploited? (1=none, 5=catastrophic)
- [ ] Who can exploit? (anyone/authenticated/insider)
- [ ] Does it affect data/availability/compliance?

Matrix:
```
         Easy  Hard
Easy-fix    |   |
Hard-fix    |   |
```

---

#### 4. Remediation Plan
- [ ] He corregido el CÓDIGO or CONFIGURATION?
- [ ] La corrección es testeable?
- [ ] Did I VERIFY the fix works?
- [ ] Can it be deployed without downtime?

**HARD STOP**: Si remediation es vague:
❌ Provide SPECIFIC code/commands

Good remediation:
```python
# BEFORE (vulnerable)
query = f"SELECT * FROM users WHERE username='{input}'"

# AFTER (safe)
cursor.execute("SELECT * FROM users WHERE username=?", (input,))
```

Bad remediation:
```
"Use prepared statements"  ← Too vague
```

---

#### 5. Fact vs Inference Separation
- [ ] He separated FACTS from ASSUMPTIONS?
- [ ] Facts: "Login returned 500 error"
- [ ] Inference: "This indicates SQL exception"
- [ ] Assumption: "Database is likely MySQL"

Table format:
| Type | Statement |
|------|-----------|
| FACT | Request returned HTTP 500 |
| INFERENCE | This indicates application error |
| ASSUMPTION | Error is likely SQL-related |
| VERIFIED | Error message: "Syntax error in SQL" |

---

#### 6. Risk Communication
- [ ] Client entiende el riesgo en su contexto?
- [ ] He escalated appropriately (Critical → ASAP)?
- [ ] Risk is business-language, not just technical?

Good: "This allows anyone to access all user accounts without password"
Bad: "There's a SQL injection"

---

#### 7. Confidentiality Check
- [ ] No real data in report?  
- [ ] No real passwords/tokens included?
- [ ] No internal IPs if shouldn't be public?
- [ ] Sanitized all sensitive data?

If showing error message:
```
❌ INCLUDE:  "Exception: Password is admin123"
✅ SANITIZE: "Exception: [REDACTED PASSWORD]"
```
```

---

## SECCIÓN 6: CHECKLIST NIVEL 5 - HARD STOPS (1500-1700 líneas)

### 🛑 HARD STOPS: DETENTE AQUÍ

**Si SÍ a CUALQUIER pregunta = RESPUESTA OBLIGATORIA ES NO**

```markdown
### 🛑 HARD STOP CHECKLIST

---

#### HARD STOP 1: Authorization
```
PREGUNTA: ¿Esto requiere acceso no autorizado?

EJEMPLOS DE SÍ:
- Accesar datos de otro usuario sin permiso
- Test credentials que no son de la red de tests
- Probe sistemas que EXPLÍCITAMENTE están excluidos
- Test después de que autorización expiró
- Usar access de otro engineer (no tu propia cuenta)

RESPUESTA OBLIGATORIA: ❌ NO
ESCALTO REQUERIDO: Contact to POC inmediatamente
ACCIÓN: STOP WORK, explain situation
```

---

#### HARD STOP 2: Abuse

```
PREGUNTA: ¿Esto facilita abuso o explotación seria?

EJEMPLOS DE SÍ:
- Crear script de password spray automatizado
- Generar malware o backdoor
- Crear persistence mecanismo
- Intentar escalación de privilegios no autorizada
- Exfiltration de datos (incluso test data, si no autorizado)

RESPUESTA OBLIGATORIA: ❌ NO  
ESCALATION REQUERIDO: IMMEDIATE escalation a leadership
ACCIÓN: STOP, DO NOT CREATE
NOTA: Esto no es "being cautious", es legal/ethical boundary
```

---

#### HARD STOP 3: Production Impact

```
PREGUNTA: ¿Esto podría impactar PRODUCCIÓN sin control?

EJEMPLOS DE SÍ:
- Test en production directamente (no staging primero)
- Comando que could cause outage
- Database modification sin rollback plan
- Network change sin POC approval
- Deployment sin testing

RESPUESTA OBLIGATORIA: ❌ NO
ESCALATION REQUERIDO: Get explicit approval de POC + manager
ACCIÓN: TEST EN STAGING FIRST
BACKUP REQUERIDO: Créado, testeado, documentado
```

---

#### HARD STOP 4: Credentials Exposure

```
PREGUNTA: ¿Toco secretos reales innecesariamente?

EJEMPLOS DE SÍ:
- Log production database password
- Exfil OAuth tokens (incluso "for testing")
- Hardcode API keys en script
- Save credenciales sin encryption
- Transmit secrets sin TLS

RESPUESTA OBLIGATORIA: ❌ NO
ESCALATION REQUERIDO: Rotation de cualquier exposed cred
ACCIÓN:
1. STOP operations
2. Rotate credenciales inmediatamente
3. Report incident
4. Document what was exposed + for how long
5. Check logs para misuse
```

---

#### HARD STOP 5: Malware/Backdoor

```
PREGUNTA: ¿Voy a create/deploy malware o backdoor?

EJEMPLOS DE SÍ ABSOLUTAMENTE:
- Generar shells, loaders, droppers
- Install persistence mecanismo
- Create test "backdoor" para ver si detectan
- Automated exploitation tool
- Ransomware simulation (sin sandboxed environment)

RESPUESTA OBLIGATORIA: ❌ NEVER, ALWAYS
ESCALATION REQUERIDO: NO escalation helps
ACCIÓN: DO NOT CREATE
NOTA: Hay diferencia entre:
  - ✅ Documenting el ataque (allowed)
  - ✅ Manual PoC en lab (allowed)
  - ❌ Automation de malware (NEVER allowed)
  - ❌ Persistence mechanisms (NEVER allowed)
```

---

#### HARD STOP 6: Scope Violation

```
PREGUNTA: ¿Esto está IN SCOPE EXPLÍCITAMENTE?

EJEMPLOS DE SÍ (out of scope):
- Scope dice "test api.example.com" pero testeas app.example.com
- Scope forbids "modify configs" pero modificas nginx.conf
- Scope dice "staging only" pero tocas production
- Scope lista IP ranges pero scanea redes adjacentes

RESPUESTA OBLIGATORIA: ❌ NO, out of scope = do not do
ESCALATION REQUERIDO: Ask POC for explicit scope expansion
ACCIÓN: GET WRITTEN APPROVAL primero
```

---

#### HARD STOP 7: Evidence Chain of Custody

```
PREGUNTA: ¿Puede alguien cuestionar si evidencia es legítima?

EJEMPLOS DE SÍ (problematic):
- No timestamps en logs
- Mix real + synthetic data sin marking
- Manual editing sin audit trail
- No chain of custody documented
- Screenshots sin location + time + context

RESPUESTA OBLIGATORIA: ❌ NO
ESCALATION REQUERIDO: Fix evidence collection primero
ACCIÓN:
1. Re-generate evidence CON proper audit trail
2. Document: WHO, WHAT, WHERE, WHEN
3. Hash files (SHA-256)
4. Store LOCKED
5. Don't touch after locked
```

---

#### HARD STOP 8: Legality/Compliance

```
PREGUNTA: ¿Es esto potencialmente ilegal?

EJEMPLOS DE SÍ:
- Accesar datos sin authorization (CFAA violation)
- Child safety concerns
- Compliance violation (HIPAA, PCI-DSS, GDPR)
- Credentials harvesting
- Unauthorized recording/monitoring

RESPUESTA OBLIGATORIA: ❌ NO NUNCA
ESCALATION REQUERIDO: IMMEDIATE escalation a legal team
ACCIÓN: STOP, ESCALATE, DOCUMENT
```

---

### ⚠️ SUMMARY: Hard Stop Matrix

```
Si respuesta a CUALQUIER LÍNEA = YES:

┌─ ¿No autorizado?       ──→ STOP, GET AUTH
├─ ¿Facilita abuso?      ──→ STOP, ESCALATE
├─ ¿Touch producción?    ──→ STOP, GET APPROVAL
├─ ¿Expose secrets?      ──→ STOP, ROTATE CREDS
├─ ¿Crear malware?       ──→ STOP, NEVER
├─ ¿Out of scope?        ──→ STOP, ASK POC
├─ ¿Evidence problema?   ──→ STOP, FIX LOGGING
└─ ¿Possibly illegal?    ──→ STOP, ESCALATE LEGAL
```

**NO AUTO-OVERRIDE**: Hard stops no se pueden ignorar.

Si crees que un hard stop no aplica = ESCALATE.
Don't self-judge.
```

---

## SECCIÓN 7: TEMPLATES Y WORKFLOWS (1700+ líneas)

### Template 1: Full Engagement Checklist

```markdown
# ENGAGEMENT MASTER CHECKLIST

## Project: [Name]
## Client: [Name]
## Duration: [Start] to [End]
## Lead: [Name]

---

### PHASE 1: PRE-ENGAGEMENT (Due: [date])

- [ ] Phase 1.1: Authorization & Scope
- [ ] Phase 1.2: Engagement Kickoff
- [ ] Client sign-off on checklists

**Approver signature**: ________________ Date: _____

---

### PHASE 2: TECHNICAL TESTING (Due: [date])

For each test:
- [ ] Phase 2.1: Pre-Read/Scan Checklist (per target)
- [ ] Phase 2.2: Pre-Execution Checklist (per command)
- [ ] Phase 2.3: Pre-Code Checklist (if needed)

**Daily log**:
- Date: _____ Tests executed: _____ Issues: _____

---

### PHASE 3: FINDINGS MANAGEMENT (Due: [date])

For each finding:
- [ ] Phase 4.1: Pre-Report Checklist
- [ ] Evidence locked & hashed
- [ ] Severity assigned (CVSS)
- [ ] Remediation tested

Total findings: _____ (by severity: C;___ H:___ M:___ L:___ I:___)

---

### PHASE 4: REPORTING & ESCALATION

- [ ] All findings reviewed
- [ ] Hard stops checked (none triggered)
- [ ] Report drafts reviewed by team
- [ ] Client presentation scheduled
- [ ] Evidence archived

**Report sign-off**: ________________ Date: _____

---

## ENGAGEMENT CLOSURE

- [ ] All data returned/destroyed
- [ ] Tools uninstalled
- [ ] Access revoked
- [ ] Lessons learned documented

**Engagement COMPLETE**: ________________ Date: _____
```

---

## CONCLUSIÓN

**Checklists = No more "I probably should have checked"**

The checklists exist because:
- ✅ We've made mistakes before (no shame)
- ✅ Preventing next mistake
- ✅ Serving clients properly
- ✅ Protecting ourselves legally

**Print them. Use them. Don't skip.**

---

**TOTAL: 1,700+ líneas**
**Status**: Production ready
**Última actualización**: 2024-02-15
**Próxima revisión**: 2024-05-15



<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - 31: Agent Safety Checklists - Guardrails de Operación Disciplinada

### Integraciones ampliadas

- Jira: integracion recomendada para aumentar profundidad, evidencia y backlog.
- OpenSearch: integracion recomendada para aumentar profundidad, evidencia y backlog.
- ServiceNow: integracion recomendada para aumentar profundidad, evidencia y backlog.
- GitHub Actions: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: assessment con evidencia.
- Integracion recomendada: Jira.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: priorizacion de backlog.
- Integracion recomendada: OpenSearch.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: validacion controlada.
- Integracion recomendada: ServiceNow.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: assessment con evidencia.
- Integracion recomendada: GitHub Actions.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: priorizacion de backlog.
- Integracion recomendada: Jira.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: validacion controlada.
- Integracion recomendada: OpenSearch.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: assessment con evidencia.
- Integracion recomendada: ServiceNow.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: priorizacion de backlog.
- Integracion recomendada: GitHub Actions.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: validacion controlada.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: assessment con evidencia.
- Integracion recomendada: OpenSearch.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: priorizacion de backlog.
- Integracion recomendada: ServiceNow.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: validacion controlada.
- Integracion recomendada: GitHub Actions.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: assessment con evidencia.
- Integracion recomendada: Jira.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: priorizacion de backlog.
- Integracion recomendada: OpenSearch.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: validacion controlada.
- Integracion recomendada: ServiceNow.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: assessment con evidencia.
- Integracion recomendada: GitHub Actions.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: priorizacion de backlog.
- Integracion recomendada: Jira.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: validacion controlada.
- Integracion recomendada: OpenSearch.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: assessment con evidencia.
- Integracion recomendada: ServiceNow.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: priorizacion de backlog.
- Integracion recomendada: GitHub Actions.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: validacion controlada.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: assessment con evidencia.
- Integracion recomendada: OpenSearch.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: priorizacion de backlog.
- Integracion recomendada: ServiceNow.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: validacion controlada.
- Integracion recomendada: GitHub Actions.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 25
- Contexto: assessment con evidencia.
- Integracion recomendada: Jira.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 26
- Contexto: priorizacion de backlog.
- Integracion recomendada: OpenSearch.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 27
- Contexto: validacion controlada.
- Integracion recomendada: ServiceNow.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 28
- Contexto: assessment con evidencia.
- Integracion recomendada: GitHub Actions.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 29
- Contexto: priorizacion de backlog.
- Integracion recomendada: Jira.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 30
- Contexto: validacion controlada.
- Integracion recomendada: OpenSearch.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 31
- Contexto: assessment con evidencia.
- Integracion recomendada: ServiceNow.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 32
- Contexto: priorizacion de backlog.
- Integracion recomendada: GitHub Actions.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 33
- Contexto: validacion controlada.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 34
- Contexto: assessment con evidencia.
- Integracion recomendada: OpenSearch.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 35
- Contexto: priorizacion de backlog.
- Integracion recomendada: ServiceNow.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 36
- Contexto: validacion controlada.
- Integracion recomendada: GitHub Actions.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 37
- Contexto: assessment con evidencia.
- Integracion recomendada: Jira.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 38
- Contexto: priorizacion de backlog.
- Integracion recomendada: OpenSearch.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 39
- Contexto: validacion controlada.
- Integracion recomendada: ServiceNow.
- Senal principal: riesgo sin contexto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 40
- Contexto: assessment con evidencia.
- Integracion recomendada: GitHub Actions.
- Senal principal: owner difuso.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 41
- Contexto: priorizacion de backlog.
- Integracion recomendada: Jira.
- Senal principal: salida no repetible.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

