# Reporting & Remediation - Turning Findings Into Fixed Systems

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe Reporting & Remediation?

Un hallazgo de seguridad **no existe hasta que se comunica correctamente**. Findings sin reportes claros = hallazgos perdidos in development silos.

**Estadísticas de la realidad**:
- 60% de hallazgos reportados vagamente = ignorados o deprioritizados
- 80% de findings "not fixed in 90 days" = reportes que no explicaban impacto
- 95% de findings reportados con datos + business context = fixed within SLA

**Objetivo crítico**: Crear reportes que:
- ✅ Comunican qué pasó (evidencia clara)
- ✅ Por qué importa (impacto en negocio, no solo técnico)
- ✅ Cómo fixear (remediación posible, no solo crítica vaga)
- ✅ Quién es responsible (clear ownership)
- ✅ Cuándo lo esperas fixed (SLA realista)

**Verdad incómoda**: "Security issue found" ≠ "Security issue fixed". El reporting es 50% del trabajo.

### 5 Principios Fundamentales de Reportes Efectivos

1. **Evidencia > Inferencia**
   - ❌ "Possibly vulnerable to SQL injection" (inferencia)
   - ✅ "Tested input validation: `'; DROP TABLE users;--` resulted in Syntax Error, confirming parameterized queries insufficient" (evidencia)
   - **Regla**: Todo claim debe estar respaldado por qué viste, no qué crees

2. **Impacto Real, No Severidad Técnica**
   - ❌ "CVSS 9.8, critical" (números)
   - ✅ "Attacker on internet can execute arbitrary commands as root, resulting in: data exfiltration of 2M customer records, lateral movement to internal network, ransomware deployment" (contexto)
   - **Mapeo**: CVSS + Asset Value + Likelihood = Actual Risk

3. **Ownership Claro y Realista**
   - ❌ "Infrastructure team should fix this" (vague)
   - ✅ "Application owner (app-team@company.com) should implement input validation; Security team validates" (clear)
   - **SLA**: Owner knows espera fix in X days; validation plan clara

4. **Remediación > Problemas**
   - ❌ "AWS S3 bucket is publicly writable" (problem solo)
   - ✅ "AWS S3 bucket is publicly writable. Remediation: (a) Block public access (1 hour), (b) Delete public ACL (5 mins), (c) Enable encryption (optional, 30 mins), (d) Verify with bucket policy audit (15 mins). Total time estimate: 2 hours. Owner: Platform engineering" (solution-oriented)
   - **Proporción**: 30% problem description, 70% solution direction

5. **Revalidación = Cierre de Loop**
   - ❌ "Found X, reported Y, reported at end" (no closure)
   - ✅ "Found X, reported Y, owner applies fix Z, we revalidate W. Finding CLOSED when criteria met" (accountability)
   - **Métrica**: % findings with verification documented

---

## SECCIÓN 2: COMPONENTES DE REPORTES EFECTIVOS

### Componente 1: Estructura Ejecutiva (Summary para executives)

**Objetivo**: CEOs, CFOs, CROs entienden riesgo sin detalles técnicos.

**Contenido típico** (2-3 páginas):
```markdown
# Executive Summary

## Organization Overview
- Scope: 50 systems, 15 departments
- Assessment period: 45 days
- Methodology: Architecture review, config audit, penetration testing

## Risk Rating: 6.2/10 (Previously 7.1 - improving!)
- 3 Critical findings (down from 5)
- 8 High findings (down from 12)
- Quick wins available: reduce to 5.5/10 in 30 days

## Business Impact Summary

### Revenue Risk
- Payment processing exposed to unauthorized access (CRITICAL)
- Risk of: Card theft → chargebacks → must notify customers → brand damage
- Estimated exposure: $5M-20M if exploited

### Operational Risk
- Ransomware potential via RDP access exposed
- Risk of: 2-week downtime → lost revenue, customer trust
- Estimated cost: $2M downtime + $5M remediation/forensics

### Compliance Risk
- PII not sufficiently encrypted (customer phone numbers)
- Risk of: SOC 2 audit failure → lose enterprise customers
- Estimated impact: $10M contract value at risk

## Investment Summary
- Recommended remediation investment: $1.2M
- Expected risk reduction: 6.2 → 3.0 within 12 months
- ROI: 8x-17x (risk avoided >> cost of fixing)

## Key Recommendations
1. IMMEDIATE (this week): Fix payment processing exposure ($50K)
2. SHORT-TERM (this month): Hardening + network segmentation ($300K)
3. MID-TERM (3 months): Encryption + monitoring implementation ($600K)
4. LONG-TERM (12 months): Culture change + automation ($250K)

## Next Steps
- Security board meeting: approval of investment plan
- Assign remediation owners from each department
- Monthly tracking meetings to monitor progress
```

**Checklist - Ejecutivo**:
- ✅ Risk rating clara con trend (mejor/peor que antes)
- ✅ Business impact en términos que CFO entienda (dinero, brand, compliance)
- ✅ Quick wins identificados (qué puede fixearse rápido)
- ✅ Investment asks con justificación
- ✅ Timeline realista (not "fix everything next week")

---

### Componente 2: Hallazgos Detallados (Technical Findings)

**Estructura per Hallazgo**:

```markdown
## Finding #5: Database Password Stored in Application Code

### Overview
- **ID**: SEC-2024-005
- **Title**: Database Credential Hardcoded in Production Deployment
- **Severity**: CRITICAL
- **Status**: CONFIRMED
- **Discovery Date**: Dec 15, 2024
- **Owner for Remediation**: Database team (owner: jane@company.com)

### Affected Assets
- **Component**: Order Processing Service (production version 2.3.1)
- **Files**: `/app/db/connection.py` (lines 12-15)
- **Environment**: Production (all 5 instances running)
- **Account**: db_user ("readonly" role, but password allows write access)

### Evidencia

**Step 1: Code Review**
```python
# /app/db/connection.py:12-15
import pymysql
conn = pymysql.connect(
    host="db.internal.company.com",
    user="db_user",
    password="Tr0pic@lP@ss123!",  # ← HARDCODED!
    database="orders"
)
```

**Step 2: Verification of Access**
- Password is actual database password (verified by querying database with these credentials)
- Last rotated: 18 months ago (age is concerning)
- Change log: Added in initial deployment, "never changed"

**Step 3: Blast Radius**
- Commits revealing password: 28 commits in Git history (visible to developers)
- Repository access: 30 engineers have read access
- Deployed instances: 5 production servers running this code
- Container images: Last 3 versions in ECR also contain password

**Evidence artifact**: Git blame output, successful login test, ECR manifest

### Impacto Real

**WORST CASE SCENARIO**:
1. Attacker compromises junior developer laptop
2. Attacker clones repository → finds password in code
3. Attacker connects to production database with credentials
4. Attacker exfiltrates all orders table: 2M transactions, totaling $500M
5. Customer notification required → brand/trust damage
6. Regulatory notification if addresses/CC data leaked → GDPR fine

**TIME TO EXPLOIT**: 10 minutes (password visible in code)

**MITIGATION CURRENTLY ACTIVE**: 
- Database behind firewall (internal IP only) → reduces attack surface
- BUT: If server compromised internally, access is direct
- Lateral movement risk: If app server compromised → database compromised (no extra auth)

### Probabilidad y Precondiciones

**Para el ataque**:
- Precondición 1: Repository access OR deployed server access (medium probability - repos leaked, servers get pwned)
- Precondición 2: Network access to database (likely - internal servers often less protected)
- **Overall likelihood**: MEDIUM (not likely but definite if server is compromised)

**CVSS Score**: 8.1 (High)
- Attack vector: Network (código desplegado openly)
- Attack complexity: Low (password is literal text)
- Privileges required: Low (any deployed instance can use it)
- User interaction: None
- Impact: High (full database access)

### Recomendación de Remediación

**Option A: Quick Fix (2 hours)**
- Remove password from code
- Use AWS Secrets Manager (store password encrypted)
- Update deployments to fetch password from Secrets Manager at runtime
- Rotate password immediately
- Owner: Database team

**Step-by-step:**
```bash
# 1. Create secret in AWS Secrets Manager
aws secretsmanager create-secret --name prod/orders-db/password \
  --secret-string '{"user":"db_user","password":"NewRand0mP@ss2024"}'

# 2. Update application code to fetch
# OLD: password="Tr0pic@lP@ss123!" (hardcoded)
# NEW: password = get_secret("prod/orders-db/password")["password"]

# 3. Update IAM role for app instances
# Grant: secretsmanager:GetSecretValue for prod/orders-db/password

# 4. Deploy new version
# Stop 5 instances, deploy v2.3.2 with secrets fetching, start

# 5. Verify
# Confirm: application still works, database queries succeed
# Confirm: Old password no longer works (rotated)

# 6. Cleanup
# Delete old deployment images containing password
```

**Option B: Long-term (RECOMMENDED - 1 week)**
- Implement Vault (HashiCorp) for ALL credentials
- Rotate all hardcoded secrets
- Add pre-commit hook to prevent future hardcoding
- Audit all 50 repositories for other hardcoded secrets

**Effort estimate**: Option A = 2 hours, Option B = 1 week

**Timeline**: Critical, should be fixed WITHIN 1 WEEK

### Criterio de Cierre

Finding is CLOSED when ALL of:
1. ☐ Password removed from Git history (rebase or BFG used)
2. ☐ New password generated and stored in Secrets Manager
3. ☐ Application code updated to fetch from Secrets Manager (code review + approval)
4. ☐ New deployment v2.3.2 running in production (all 5 instances)
5. ☐ Verification: Application logs show no errors, database queries successful
6. ☐ Verification: Old password tested against database (returns "access denied")
7. ☐ Rebase/merge to main; old code unreachable
8. ☐ Security team revalidates by code inspection + test

**Deadline**: January 8, 2025

### Related Findings
- SEC-2024-006: Similar hardcoded API key in payment processor
- SEC-2024-007: AWS credentials in environment variable (same pattern)

**Recommendation**: Create systemic fix (pre-commit hooks + audit all secrets) to prevent recurrence
```

**Checklist - Technical Finding**:
- ✅ Severity clara con CVSS y business context
- ✅ Evidencia específica (código, pasos, resultados)
- ✅ Impacto real en escenario realista ("worst case")
- ✅ Probabilidad (likelihood) vs Impact (CVSS correla pero no es same)
- ✅ Ownership claro (name + email)
- ✅ Remediación paso-a-paso (not just "fix it")
- ✅ Criterio de cierre (qué significa "fixed"?)
- ✅ Timeline realista (ASAP para críti pero con effort estimado)

---

### Componente 3: Plan de Remediación Priorizado

**Formato**:

```markdown
## Remediation Roadmap

### IMMEDIATE (This Week) - 3 Findings
| Finding | Owner | Effort | Status | Due |
|---------|-------|--------|--------|-----|
| SEC-2024-005: DB password hardcoded | Jane (DB) | 2 hrs | IN PROGRESS | Jan 8 |
| SEC-2024-012: API auth bypass | Mark (API) | 4 hrs | NOT STARTED | Jan 9 |
| SEC-2024-019: Web server DOS exposure | Tom (Infra) | 1 hr | NOT STARTED | Jan 7 |
| **SUBTOTAL** | | **7 hours** | | |

### SHORT-TERM (This Month) - 8 Findings
| Finding | Owner | Effort | Status | Due |
|---------|-------|--------|--------|-----|
| SEC-2024-006: API key hardcoded | Jane | 3 hrs | NOT STARTED | Jan 20 |
| SEC-2024-008: TLS 1.0 still enabled | Tom | 2 hrs | NOT STARTED | Jan 15 |
| ... | ... | ... | ... | ... |
| **SUBTOTAL** | | **35 hours** | | |

### MID-TERM (Next Quarter) - 5 Findings
| Finding | Owner | Effort | Status | Due |
|---------|-------|--------|--------|-----|
| SEC-2024-025: Encryption at rest needed | Infra | 40 hrs | NOT STARTED | Mar 30 |
| SEC-2024-030: SIEM implementation | SOC | 80 hrs | NOT STARTED | Apr 30 |
| ... | ... | ... | ... | ... |
| **SUBTOTAL** | | **150+ hours** | | |

### LONG-TERM (Next Year) - 7 Findings (Structural)
| Finding | Owner | Effort | Status | Due |
|---------|-------|--------|--------|-----|
| SEC-2024-035: SSO implementation needed | IT | 200 hrs | NOT STARTED | Dec 31 |
| SEC-2024-040: Kubernetes hardening | DevOps | 120 hrs | NOT STARTED | Sep 30 |
| ... | ... | ... | ... | ... |
| **SUBTOTAL** | | **400+ hours / 3 FTE** | | |

---

## Capacity Planning

**Available: 4 FTE at 40 hrs/week = 160 hours/month**

**Allocation**:
- IMMEDIATE (7 hours, ~week 1): 5% capacity
- SHORT-TERM (35 hours, ~month 1): 22% capacity
- MID-TERM (150 hours, ~quarter): 30% capacity ongoing
- LONG-TERM: Requires hiring or reprioritization

**Recommendation**: Add 1 FTE security engineer OR deprioritize some mid-term items

---

## Remediation SLA

**Critical findings**: Fixed within 72 hours OR risk escalation
**High findings**: Fixed within 2 weeks OR executive review
**Medium findings**: Fixed within 1 month
**Low findings**: Fixed within quarter OR deprioritized to backlog
```

---

## SECCIÓN 3: METODOLOGÍA DE REPORTING

### Paso 1: Descubrimiento y Documentación Inicial (Durante Testing)

```
WHILE performing tests:
- Document EXACTLY what you did (steps with commands)
- Capture evidence (screenshots, output, logs)
- Note timestamp (when found)
- Determine impact immediately (not "maybe" later)

EXAMPLE:
Testing: SQL injection on login form
Input: `admin' OR '1'='1`
Result: Successfully authenticated as admin user
Implication: Bypassed authentication (CRITICAL impact)
→ Document with timestamp, exact form field, exact payload, exact response

AVOID:
- Speculating on impact ("could maybe access database")
- Vague reproduction steps ("click some buttons and it happened")
- Old screenshots (include timestamp in image metadata)
```

### Paso 2: Análisis de Impacto (Post-Testing)

```
FOR EACH FINDING:

1. Determine worst-case scenario
   - If exploited, what's the absolute worst outcome?
   - Example: "Database exposed" → "2M customer records leaked"

2. Assess preconditions
   - What needs to happen BEFORE attacker can exploit?
   - Example: "Attacker must have network access to X.X.X.X"
   - This affects probability

3. Quantify business impact
   - Revenue at risk? Compliance violation? Brand damage?
   - Example: "Could cost $5M in revenue if payment system hacked"

4. Cross-check with CVSS
   - CVSS is good but not complete
   - High CVSS + Low prob = Medium actual risk
```

### Paso 3: Redacción Inicial (Borrador Técnico)

```
FOR EACH FINDING - Write in this order:

1. Title (1 sentence capturing the problem):
   "PostgreSQL Database Exposed Without Authentication"

2. Evidence (exact steps to reproduce):
   - Command: `psql -h 203.0.113.50 postgres`
   - Result: Logged in as postgres user without password

3. Impact (worst case):
   - Access to 2M customer records
   - Ability to modify/delete data
   - Potential business continuity impact

4. Ownership (who owns the system?):
   - Database team
   - Owner: DBA name + email

5. Remediation (what to do):
   - Require password authentication
   - Update pg_hba.conf to disable trust auth
   - Estimated time: 1 hour

6. Closure (what means "fixed?"):
   - psql without password returns "access denied"
   - Password auth working for legitimate users
   - Verified by security team

This is DRAFT - will be refined
```

### Paso 4: Review y Feedback (Validation Loop)

```
BEFORE FINALIZING:

1. Owner reviews (applicant of the fix)
   - "Is remediation step realistic?"
   - "Do we agree on timeline?"
   - "Do we need any clarifications?"

2. Technical reviewer (peer security engineer)
   - "Is evidence sufficient?"
   - "Is impact realistic or exaggerated?"
   - "Did we miss anything?"

3. Security leader review
   - "Is prioritization correct?"
   - "Does tone match audience?"
   - "Any legal/compliance concerns?"

ITERATE UNTIL CONSENSUS
```

### Paso 5: Finalización y Distribución

```
FINAL REPORT contains:

1. Executive summary (2-3 pages for leadership)
2. Technical findings (detailed, per-finding)
3. Remediation roadmap (prioritized, with effort)
4. Appendix (detailed evidence, tools used, timeline)

DISTRIBUTION:
- Leadership: Executive summary only
- Technical owners: Full findings for their systems
- Security team: Everything (archive for future reference)

CADENCE:
- Draft: 15 days after testing ends
- Final: 20 days after testing (after feedback loop)
- Presentation to stakeholders: 25 days
```

---

## SECCIÓN 4: CASOS DE ESTUDIO REALES

### Caso 1: Reporte Que Funcionó (Finding Fixed in 48 hrs)

**Hallazgo**: Production S3 bucket publicly writable

**Reporte Inicial (BAD)**:
```markdown
## Finding: S3 Bucket Configuration Issue
Severity: High
Issue: Bucket permissions may be too open
Effect: Unauthorized access possible
Recommendation: Restrict bucket policy
```

**Problemas**:
- Vague title ("configuration issue" = anything)
- No specific evidence (which bucket? which permissions?)
- No business impact
- No clear owner
- No remediation steps (just "restrict")

**Resultado**: Owner ignores for 3 weeks, labeled "not understood"

---

**Reporte Final (GOOD)**:
```markdown
## Finding: S3 Bucket "customer-data-prod" Publicly Writable

**Severity**: CRITICAL  
**Owner**: Platform Engineering + Jane (jane@company.com)

**Evidence**:
- Bucket: s3://customer-data-prod (us-east-1)
- Bucket policy: Principal "*", Action "s3:*" (anyone can put/delete/putacl)
- Verification: Uploaded file anonymously without credentials ✓
- Content: Customer addresses, payment history, 2M records

**Impact (Worst Case)**:
1. Attacker uploads malware.exe → customers download → ransomware
2. Attacker deletes all objects → data loss → business disruption
3. Attacker modifies payment records → fraud

**Business Impact**: 
- Revenue loss: 2-week downtime = $200K/day = $2.8M
- Notification costs: $500K
- Regulatory fines: up to $50M (GDPR if EU customers)

**Timeline**: Created 24 hours ago; assume compromised imminently

**Remediation**:
- STEP 1 (10 mins): Delete public ACL
  - `aws s3api put-bucket-acl --bucket customer-data-prod --acl private`
- STEP 2 (5 mins): Add blocking policy
  - `aws s3api put-public-access-block --bucket customer-data-prod --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"`
- STEP 3 (1 hour): Audit contents (check for modifications/uploads)
  - Compare S3 object hashes to backup
- STEP 4 (30 mins): Verify
  - Try uploading anonymously → should fail

**Total Time**: 1.5 hours (2 hours including verification)

**Closure Criteria**:
- ☐ Public access disabled (S3 console shows "Block All Public Access = true")
- ☐ Attempted upload from public IP rejected ("Access Denied")
- ☐ S3 audit logs reviewed for unauthorized activity (last 48 hours)
- ☐ Backup compared to current state (no unauthorized modifications detected)

**Timeline**: IMMEDIATE - fix before end of business today
```

**Resultado**: Owner reads, understands EXACTLY what to do, executes in 45 minutes, reports closure.

**Diferencia**: Specific + Business Impact + Step-by-step = Gets fixed

---

### Caso 2: Reporte QUE NO Funcionó (Finding Ignored for 6 Months)

**Hallazgo**: Weak apikey rotation policy

**Reporte**:
```markdown
## Finding: API Key Rotation Policy Inadequate
Severity: Medium
Issue: API keys not rotated frequently enough
Recommendation: Implement 90-day rotation policy
```

**Problemas**:
- Owner unclear (API team? Infra? Security?)
- Remediation is vague ("implement policy" = what does that mean? How long?)
- Timeline not specified
- No business impact (why should owner care?)
- No closure criteria (how do we know when it's fixed?)

**Owner**: "Yeah, we should do that eventually. Low priority."
**Result**: 6 months later, still not done. Reason: No pressure, unclear effort, no accountability

---

**Reporte Mejorado**:
```markdown
## Finding: API Key Rotation Policy Missing

**Owner**: API Team + Engineering Lead (mike@company.com)

**Evidence**:
- Audit of API keys: Average age = 18 months
- Keys: 23 production keys, 0 rotation in last 12 months
- Risk: Leaked key from 2 years ago could still be valid

**Business Impact**:
- If key leaked today, attacker access for 18+ months (undetectable)
- Could query customer data, modify orders, impersonate users
- Compliance: SOC 2 requires "periodic credential rotation"
- Audit finding from last year: "API key rotation not in evidence"

**Remediation & Effort**:
- STEP 1 (8 hrs): Implement Vault for API key storage
- STEP 2 (4 hrs): Update all services to fetch from Vault (rotate on each
 deploy)
- STEP 3 (2 hrs): Document new policy
- Total: 14 hours = 2-3 days (1 engineer)

**Timeline**: MEDIUM priority, due Feb 15 (6 weeks)

**Closure**:
- ☐ Vault deployment for API keys complete
- ☐ 5 critical services using Vault (automatic rotation)
- ☐ Policy documented in internal wiki
- ☐ All existing API keys rotated
```

**Result**: Owner sees effort + timeline, plans work, delivers on date.

---

### Caso 3: Escalation de Reporte No Actuado (Finding Becomes Incident)

**Initial Report** (12 months ago):
```markdown
## Finding: RDP Access Exposed From Internet
Severity: High
Issue: RDP port (3389) accessible from 0.0.0.0/0
Recommendation: Restrict to corporate VPN only
```

**Status**: Reported as Medium, owners said "will fix next quarter"

**6 months later**: Nothing done

**12 months later (TODAY)**: 
- Attacker brute-forces RDP with common passwords
- Gains access to server, deploys ransomware
- $500K ransom demand
- Systems down 1 week
- Post-incident forensics: Attack vector was that old RDP exposure

**Investigation**: "Why wasn't this fixed?"
- Owner: "Didn't realize it was important"
- Security: "Should have escalated"

**Lesson**: Findings that don't get fixed become incidents. Reporting must include escalation path if not remediated.

---

## SECCIÓN 5: TEMPLATES REUSABLES

### Template 1: Finding Template Completo

```markdown
# [FINDING ID]: [DESCRIPTIVE TITLE]

**Quick Summary** (1 sentence for non-technical people):
"Database credentials are stored in website application code and could be seen by anyone"

---

## Finding Details

| Attribute | Value |
|-----------|-------|
| Finding ID | SEC-2024-XXX |
| Title | [Full title] |
| Severity | CRITICAL / HIGH / MEDIUM / LOW / INFO |
| Status | CONFIRMED / UNCONFIRMED |
| Component Affected | [System/application/service] |
| Estimated Owner | [Name/team] |
|Related Findings | [Other findings with same root cause] |

---

## Evidence (Objective Facts)

### How We Found It
[Step-by-step reproduction, tools used, screenshots, code excerpts]

### Verification
[Confirm the issue exists, measure scope, determine confidence level]

### Scope
- [How many instances/systems/users affected?]
- [Percentage of infrastructure?]

---

## Impact Assessment

### Worst Case Scenario
[Detailed description of full exploitation chain, starting from vulnerability and ending in business harm]

### Financial Impact Estimate
[Potential direct costs: ransom, data loss recovery, notification, fines, etc.]

### Business Impact
[Operational: downtime hours? Revenue loss? Compliance: audit failure? Legal: lawsuit risk?]

### Likelihood of Exploitation
- Preconditions: [What must be true for attacker to exploit this?]
- Probability: [HIGH / MEDIUM / LOW] - why?
- Detectability: [Would we notice if exploited?]

---

## Risk Rating

- **CVSS v3.1 Score**: X.X (combination of attack vector, complexity, privileges, impact)
- **Business Risk**: CRITICAL / HIGH / MEDIUM / LOW
- **Remediation Priority**: IMMEDIATE / SHORT-TERM / MID-TERM / LONG-TERM

---

## Remediation Recommendations

### Option A: Quick Fix (if available)
- Step 1: [Description of action with effort estimate]
- Step 2: [Description of action with effort estimate]
- Step 3: [Verification step]
- **Total Effort**: X hours
- **Timeline**: X days

### Option B: Proper Fix
- Step 1: [Description of architectural change]
- Step 2: [Implementation step]
- Step 3: [Testing/verification]
- **Total Effort**: X weeks
- **Timeline**: X months
- **Benefit**: [Why this is better than quick fix]

---

## Success Criteria / Closure Conditions

Finding is considered CLOSED when:

- ☐ [Specific, measurable condition 1]
- ☐ [Specific, measurable condition 2]
- ☐ [Verification step 1]
- ☐ [Verification step 2]
- ☐ Security team revalidation complete

---

## Timeline & Ownership

- **Owner**: [Name + email] (responsible for executing fix)
- **Target Fix Date**: [Date based on severity]
- **Verification Due**: [Date + 2 days]
- **Escalation Contact**: [If owner doesn't deliver]

---

## Related Findings

- Finding SEC-2024-XXX (similar pattern in system Y)
- Finding SEC-2024-XXX (dependency on this being fixed)
```

### Template 2: Remediation Tracking Spreadsheet

```csv
Finding_ID,Title,Owner,Severity,Status,Target_Date,Effort_Hours,% Complete,Blocker,Notes
SEC-2024-001,DB password hardcoded,jane@company.com,CRITICAL,IN_PROGRESS,2025-01-08,2,75%,None,Deploy v2.3.2 tomorrow
SEC-2024-002,S3 bucket public,mike@company.com,CRITICAL,DONE,2024-12-20,1,100%,None,Fixed; validated
SEC-2024-003,TLS 1.0 enabled,tom@company.com,HIGH,NOT_STARTED,2025-01-15,2,0%,"Awaiting vendor update for legacy app",Vendor says v2.0 in Jan
SEC-2024-004,API key rotation,api-team@company.com,MEDIUM,IN_PROGRESS,2025-02-15,14,30%,None,Vault config done; services in progress
SEC-2024-005,Encryption at rest,infra@company.com,MEDIUM,NOT_STARTED,2025-03-30,40,0%,"Blocked: awaiting KMS key provisioning",KMS key requested Dec 20
```

### Template 3: Executive Status Report

```markdown
# Security Findings Status - Monthly Update

**Month**: January 2025  
**Prepared by**: Security Team  
**Report Date**: January 31, 2025

---

## Summary

| Status | Critical | High | Medium | Low | TOTAL |
|--------|----------|------|--------|-----|-------|
| Done | 2 | 4 | 1 | 3 | 10 |
| In Progress | 1 | 2 | 3 | 5 | 11 |
| Not Started | 0 | 2 | 4 | 8 | 14 |
| **TOTAL** | **3** | **8** | **8** | **16** | **35** |

---

## Status Trends

- Last month: 35 findings | This month: 35 findings | Change: -2 (done) +2 (new)
- Critical closure rate: 2/3 per month (66%)
- High closure rate: 4/8 per month (50%)
- Overall trajectory: On track for 32 findings remaining by March 31

---

## Risk Scorecard

| Dimension | Current | Trend | Notes |
|-----------|---------|-------|-------|
| Identity & Access | 3/5 (Medium) | → | SSO implementation 30% done |
| Vulnerability Mgmt | 2.5/5 (Low) | ↗ | Scanning now automated (was manual) |
| Detection & Response | 1.5/5 (Low) | → | SIEM procurement in progress |
| SDLC Hardening | 2/5 (Low) | ↗ | Code scanning gate now automated |

---

## Red Flags & Blockers

1. **SEC-2024-005 (Encryption at rest)**: Blocked on KMS key provisioning
   - Requested: Dec 20 | Still pending
   - **Action**: CTO to follow up with AWS team

2. **SEC-2024-007 (Vendor security update)**: Depends on vendor release
   - Vendor promised: January | Now saying February
   - **Action**: Evaluate workaround or alternative vendor

---

## Next Month Priorities

1. Close 3-4 more findings (focus on Quick wins)
2. Move SSO to 50% (currently 30%)
3. Deploy SIEM (scheduled for mid-February)
4. Resolve KMS blocker

Forecasted closure rate: 35 → 28 findings by Feb 28
```

---

## CONCLUSIÓN

**Reportes efectivos = Hallazgos arreglados**

Las mejores técanicas de testing no importan si no puedes comunicar el resultado efectivamente.

**FORMULA PARA ÉXITO**:
- Evidencia clara (no speculation)
- Business impact (not just technical severity)
- Clear ownership (not vague "someone should fix")
- Step-by-step remediation (not just "bad thing is bad")
- Closure criteria (specific conditions for "fixed")
- Timeline & accountability (due dates + escalation)

**Métrica de éxito**: % of findings fixed within SLA (target: 95%+)
**Indicador de problema**: % of findings ignored >90 days (target: <5%)


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Reporting & Remediation - Turning Findings Into Fixed Systems

### Integraciones ampliadas

- Jira: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Confluence: integracion recomendada para aumentar profundidad, evidencia y backlog.
- PowerBI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- DefectDojo: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: heatmap ejecutivo.
- Integracion recomendada: Jira.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: tracking 90 dias.
- Integracion recomendada: Confluence.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: reporte regulatorio.
- Integracion recomendada: PowerBI.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: heatmap ejecutivo.
- Integracion recomendada: DefectDojo.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: tracking 90 dias.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: reporte regulatorio.
- Integracion recomendada: Confluence.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: heatmap ejecutivo.
- Integracion recomendada: PowerBI.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: tracking 90 dias.
- Integracion recomendada: DefectDojo.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: reporte regulatorio.
- Integracion recomendada: Jira.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: heatmap ejecutivo.
- Integracion recomendada: Confluence.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: tracking 90 dias.
- Integracion recomendada: PowerBI.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: reporte regulatorio.
- Integracion recomendada: DefectDojo.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: heatmap ejecutivo.
- Integracion recomendada: Jira.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: tracking 90 dias.
- Integracion recomendada: Confluence.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: reporte regulatorio.
- Integracion recomendada: PowerBI.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: heatmap ejecutivo.
- Integracion recomendada: DefectDojo.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: tracking 90 dias.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: reporte regulatorio.
- Integracion recomendada: Confluence.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: heatmap ejecutivo.
- Integracion recomendada: PowerBI.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: tracking 90 dias.
- Integracion recomendada: DefectDojo.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: reporte regulatorio.
- Integracion recomendada: Jira.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: heatmap ejecutivo.
- Integracion recomendada: Confluence.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: tracking 90 dias.
- Integracion recomendada: PowerBI.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: reporte regulatorio.
- Integracion recomendada: DefectDojo.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 25
- Contexto: heatmap ejecutivo.
- Integracion recomendada: Jira.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 26
- Contexto: tracking 90 dias.
- Integracion recomendada: Confluence.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 27
- Contexto: reporte regulatorio.
- Integracion recomendada: PowerBI.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 28
- Contexto: heatmap ejecutivo.
- Integracion recomendada: DefectDojo.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 29
- Contexto: tracking 90 dias.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 30
- Contexto: reporte regulatorio.
- Integracion recomendada: Confluence.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 31
- Contexto: heatmap ejecutivo.
- Integracion recomendada: PowerBI.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 32
- Contexto: tracking 90 dias.
- Integracion recomendada: DefectDojo.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 33
- Contexto: reporte regulatorio.
- Integracion recomendada: Jira.
- Senal principal: evidencia no verificable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 34
- Contexto: heatmap ejecutivo.
- Integracion recomendada: Confluence.
- Senal principal: finding sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 35
- Contexto: tracking 90 dias.
- Integracion recomendada: PowerBI.
- Senal principal: riesgo sin negocio.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

