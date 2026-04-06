# GRC, Risk & Maturity - Governance, Risk Management & Control Frameworks

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe GRC y Maturity Modeling?

You can find 100 security findings en una organización. PERO **¿cuáles importan?** ¿Cuáles son síntomas de un problema sistémico vs incidentes aislados? GRC traduce **hallazgos técnicos en decisiones de negocio**.

**Objetivo crítico**: Crear un **"fuente de verdad"** que:
- ✅ Convierte "CVE-2024-1234 en Oracle" en "Tenemos proceso de patching débil"
- ✅ Diferencia quick-wins (5 horas fix) de cambios estructurales (6 meses, cultura nueva)
- ✅ Conecta seguridad con riesgo empresarial ("¿Cómo impacta nuestra capacidad de vender?")
- ✅ Mide progreso sin caer en "vanity metrics" (# de findings reduced ≠ risgo reducido)
- ✅ Prioriza remediation por impacto real, no solo severidad técnica

**Ejemplo de razón por qué importa**:
```
Escenario A: Técnico vé
- CVE-2024-5678 en open-source lib (critical CVSS 9.8)
- Reacción: "PATCH IMMEDIATELY!"

Escenario B: GRC perspectiva
- Lib usado en staging environment SOLO (no prod)
- Dependency update rompería build en 20 otros lugares
- "Actual risk" = media (aplazable a siguiente sprint planificado)

Sin GRC → caos (falsos alarmismos)
Con GRC → priorización inteligente
```

### 5 Principios Fundamentales de GRC y Maturity

1. **Risk ≠ Severity**
   - **Severity**: Cuán mal es técnicamente ("CVSS 9.8 = critical")
   - **Risk**: Impacto en negocio × Probabilidad que pase × Detectabilidad
   - **Ejemplo**: Unpatched WordPress plugin (HIGH severity) en servidor aislado sin internet (LOW risk)
   - **Regla**: Priorizar por Risk, no Severity

2. **Controles > Hallazgos**
   - Un hallazgo es síntoma; control es tratamiento
   - En lugar de: "DB password débil" (fixing cada occurrence)
   - Implementar: "Todos los secrets van a Vault; rotation automática 90 días" (control sistémico)
   - **Patrón**: Agrupar hallazgos similares → control abstracto → remediación única

3. **Madurez No es Lineal (8 Patrones de Mejora Típicos)**
   - Algunas áreas pueden estar en Level 5 (optimización); otras en Level 1 (reactivo)
   - NO requiere linearidad (no es "Level 3 en todo before Level 4")
   - **Decisión**: ¿Optimizar el mejor o mejorar el peor? (depende estrategia)

4. **Datos Objetivos > Percepciones**
   - "Creemos que tenemos buenos controles" (percepción) ≠ "SIEM logs muestran..." (dato)
   - Metricas: Credential age, patch lag, MTTR (mean time to remediate), phishing click rate
   - **Medición**: Lo que no se mide no mejora

5. **Madurez es Jounrey, no Destino**
   - Nivel 5 = "optimización continua" (no es "seguridad perfecta")
   - Nivel 1 = "reactivo" (respuesta a crises)
   - Movimiento: 1→2 (6 meses), 2→3 (12 meses), 3→4+ (años)
   - **Expectativa realista**: Mejorar visiblemente en 3-6 meses; transformación total = 2-3 años

---

## SECCIÓN 2: DIMENSIONES DE MADUREZ

### Dimensión 1: Gobernanza y Estrategia

**Nivel 1 (Reactivo)**:
- Política de seguridad existe en documento (no se sigue)
- Decisiones tomadas ad-hoc basado en latest breach news
- Roles/responsibilities oscuros ("quien es el "security owner"?")
- Ejemplo: Detectan malware → crisis → "buy XDR tool"

**Nivel 2 (Definido)**:
- Políticas documentadas y comunicadas
- Roles claramente asignados (CISO, security team, architects)
- Presupuesto anual para seguridad (aunque small)
- Risk committee existe
- Ejemplo: "Tenemos política de password; policy define rotation 90 días"

**Nivel 3 (Repetible)**:
- Seguridad integrada en decisiones de arquitectura
- Excepciones a políticas requieren aprobación formal
- Training anual obligatorio
- Métrica: % of exceptions documentado
- Ejemplo: "Toda nueva app pasa security review; aprobación requerida before deployment"

**Nivel 4 (Gestionado)**:
- Security metrics integrados en KPIs de negocio
- Dashboards de riesgo en tiempo real
- Capacity planning para team seguridad (hiring, tools)
- Regular policy reviews (annual)
- Ejemplo: "Security team tiene presupuesto predecible; no lucha por cash cada quarter"

**Nivel 5 (Optimizado)**:
- Seguridad en cultura empresarial (developers piensan en seguridad daily)
- Continuous improvement: lessons learned incluidos en procesos
- Innovations in security práctica parte del roadmap
- Ejemplo: "Engineers automaticamente propose security improvements; kaizen culture"

---

### Dimensión 2: Gestión de Inventario y Activos

**Nivel 1**: No tenemos idea de qué sistemas existimos; cambios descontrolados
**Nivel 2**: Inventario existe en spreadsheet; actualizaciones ocasionales
**Nivel 3**: CMDB (Configuration Management DB) existe; 80%+ actualizados
**Nivel 4**: CMDB automatizado; cambios synced en tiempo real; alertas por drift
**Nivel 5**: Self-service inventory; teams actualizan automáticamente

---

### Dimensión 3: Gestión de Identidad y Acceso

**Nivel 1**: Passwords compartidos; acceso basado en "asks for it"; sin auditoría
**Nivel 2**: Password policy (complexity, rotation); roles básicos; logs básicos
**Nivel 3**: SSO implementado; RBAC definido; auditoría de acceso; annual reviews
**Nivel 4**: Privileged Access Management (PAM); MFA required; real-time monitoring
**Nivel 5**: Zero-trust implementation; continuous adaptive auth; behavior analytics

---

### Dimensión 4: Hardening y Vulnerabilidad Management

**Nivel 1**: No parches; servicios por defecto; sin hardening
**Nivel 2**: Parches aplicados (eventual); checklist de hardening existe
**Nivel 3**: Patching schedule; vulnerability scanner ejecutado mensual; findings tracked
**Nivel 4**: Automated patching; scanning semanal; SLA de remediation definido
**Nivel 5**: Continuous patching; zero-day response plan; security updates within 24 hrs

---

### Dimensión 5: Detección y Respuesta (Detection & Response)

**Nivel 1**: Sin logs; no sabemos qué pasó; sin incident response
**Nivel 2**: Logs guardados; rudimental alerting; incident response manual
**Nivel 3**: SIEM implementado; baseline of normal defined; playbooks básicos
**Nivel 4**: Real-time detection; automated response para algunos events; MTTR < 4 hrs
**Nivel 5**: ML-based detection; automated containment; MTTR < 1 hr

---

### Dimensión 6: Secure Engineering & SDLC

**Nivel 1**: "Security = testing después"; breach in > patch later
**Nivel 2**: Security gate básico pre-release; code review occasional
**Nivel 3**: SAST tools integrated in build; libraries scanned; threat modeling
**Nivel 4**: Security integrated in PRs; SBOM generated; DAST in staging
**Nivel 5**: Security champions in teams; continuous threat modeling; shift-left cultural change

---

### Dimensión 7: Gestión de Supply Chain

**Nivel 1**: Sin visibilidad en dependencies; vendor security ignored
**Nivel 2**: Vendor questionnaires; lib dependencies listed; basic SLA
**Nivel 3**: Dependency scanning (SCA); vendor due diligence; contracts mention security
**Nivel 4**: Automated dependency updates; vulnerability notifications; supply chain risk model
**Nivel 5**: Third-party monitoring; behavioral analytics para vendors; continuous attestation

---

### Dimensión 8: Backup, Disaster Recovery & Business Continuity

**Nivel 1**: No backups; "hope nothing breaks"; no RTO/RPO defined
**Nivel 2**: Backups exist; occasional restore test; RTO/RPO documented
**Nivel 3**: Automated backups; regular DR drills (annual); documented plans
**Nivel 4**: Real-time replication; automated failover; DR drills quarterly
**Nivel 5**: Zero-RPO architecture; continuous DR validation; ransomware recovery architecture

---

## SECCIÓN 3: METODOLOGÍA DE EVALUACIÓN Y SCORING

### Paso 1: Seleccionar Evaluadores y Scope (1 hora)

```
Evaluadores: Mix de técnicos + managers + áreas de negocio
Scope: Cuáles dimensiones importan más (focus en 4-6 principales)
Timeline: Cuánto tiempo disponible (assessment: 1-2 semanas)
```

### Paso 2: Mapear Estado Actual para Cada Dimensión (2-3 horas)

Para cada dimensión, documentar:

**"¿Dónde estamos hoy?"** (Baseline)
- Evidencia: Qué existe, qué procesos, qué métricas
- Gap analysis: Qué falta comparado con level próximo

**Ejemplo: Gestión de Identidad & Acceso**

```
NIVEL ACTUAL: 2.5 (entre Definido y Repetible)

Evidencia de Level 2:
✅ Password policy existe (complexity, rotation 90 days)
✅ Basic roles (admin, user, viewer)
✅ Logs de login guardados (3 months)

Evidencia de Level 3 (falta):
❌ SSO no implementado (cada app tiene usuarios separados)
❌ RBAC detallado no existe (roles son binary: admin vs user)
❌ Access reviews annual (not done in 2 years)
❌ MFA only in email, not production systems

Gap para Level 3:
- Implementar SSO (3 meses)
- RBAC design (1 mes)
- Annual access reviews process (2 semanas)
- MFA en production systems (2 meses)
```

### Paso 3: Priorizar Mejoras contra Capacidad (1-2 horas)

```
Timeline: 1 año, 2 CISO FTE, $500K presupuesto

Opciones:
A) Focus Identidad: SSO + RBAC + MFA (big bang, Level 4 en 9 meses)
B) Balance: Identidad (Level 3) + Detection (Level 2→3) (50-50 split)
C) Operacional: Detection + Incident Response (already strong governance)

Recomendación: B (diversificado, impacto visible en múltiples dirección)
```

### Paso 4: Definir Target State + Roadmap (2-3 horas)

```
YEAR 1 TARGET STATE:
- Governance: 2 → 3
- Inventory: 2 → 3
- Identidad: 2.5 → 3.5
- Hardening: 1.5 → 2.5
- Detection: 1 → 2
- SDLC: 2 → 2.5
- Supply Chain: 1 → 1.5
- Backup/DR: 2 → 2.5

QUARTERLY MILESTONES:
Q1: SSO pilot, annual access review process, vulnerability scanning SLA
Q2: SSO rollout, RBAC design, SIEM procurement
Q3: SIEM implementation, MFA rollout, supply chain assessment
Q4: Hardening playbook automation, SDLC security gate, assessment readiness

METRICS TO TRACK:
- % users with MFA enabled
- Avg password age (younger = better rotation)
- Avg time to remediate critical vulns
- Access review completion %
- % apps with security gate approval
```

### Paso 5: Ejecutar Roadmap + Iterate (Ongoing)

- Monitor metrics monthly
- Adjust based on capacity/blockers
- Annual reassessment vs target
- Learn from incidents (security post-mortems)

---

## SECCIÓN 4: CASOS DE ESTUDIO REALES

### Caso 1: Level 1 → Level 3 in 18 Months (Retail Company)

**Contexto**:
Retailer con 2000 stores, 50K employees. Después de breach (lost customer cards), nuevo CISO contratado.

**Situación Inicial (Nivel 1)**:
- Sin política de seguridad formal
- Acceso a sistemas basado en "ask manager"
- Passwords rotados never
- Logs guardados máximo 30 dias (overwritten)
- No incident response ("call IT when problem")

**Roadmap Ejecutado**:

```
PERSONAS/ROLES (Mes 1-2):
- Contratar security team (3 FTE)
- Crear governance board (CISO + CIO + heads of ops, finance, HR)
- Define roles: Incident response lead, vulnerability management, security engineers

POLÍTICAS (Mes 2-4):
- Password policy: minimum 14 chars, uppercase, numbers, rotate 90 days
- MFA: mandatory for admin, encouraged for users
- Incident response playbook drafted
- Vendor security requirements added to contracts

SISTEMAS (Mes 5-12):
- SSO pilot in HQ (100 users)
- SIEM implementation (open-source: Wazuh)
- Automated patching tested in test environment
- Vulnerability scanner (Nessus) deployed

OPERACIONALIZACIÓN (Mes 12-18):
- SSO rollout a 5000 corporate users
- SIEM tuned para eliminar false positives
- Automated patching en prod (staged rollout)
- Monthly patch meetings (when, why, prioritization)
- Quarterly security training obligatorio

RESULTADOS POST-ROADMAP:
```

| Métrica | Inicio | Fin | Improvement |
|---------|--------|-----|-------------|
| Conocimiento de ataques (MTTR) | 30+ days | 4 days | 87% faster |
| Unpatched critical systems | 200+ | 5 | 97% reduced |
| % MFA habilitado | 0% | 65% | Significant adoption |
| Annual training completion | 0% | 95% | Cultural change |
| Vulnerability finding/month | 0 (not scanned) | 200 (now visible!) | Visibility gained |

**Key Success Factor**: Executive support ($1.5M investment over 18 months, no shortcuts)

---

### Caso 2: Level 4.5 → Level 2 (Security Regression Post-Acquisition)

**Contexto**:
SaaS company adquirida por mega-corp. New parent company tiene "different security culture" (slower, more bureaucratic).

**Cambios Post-Adquisición**:
- SSO reemplazado con central corp AD (multiple day outages)
- Security scanning disabled ("slowing CI/CD")
- Incident response centralized a global team (respuesta 24hrs instead of immediate)
- Budget recortado ("consolidation savings")

**Resultados**:
- Velocity de deployment ↓ 40% (security blocker ahora)
- Vulnerability remediation SLA violations ↑ (no ownership)
- Turnover de security team: 3 of 5 engineers renuncian

**Lección**: Seguridad en mejora fase "anti-patrón" de: standardization con overhead > decentralized excellence

---

### Caso 3: Level 2 → 2.5 (Focused Execution de Single Dimension)

**Contexto**:
Healthcare startup. Supply chain attacks increasing en industria. Leadership decide: "Vamos a Level 5 en supply chain security, aunque otros dimensions stay at 2".

**Stack approach** (no generalizado):
- Vendor assessment framework formal
- Software Bill of Materials (SBOM) mandatory
- Dependency scanning integrado in CI
- Quarterly vendor security reviews
- Breach notification SLA with 3rd parties

**Resultado**: Mejor posicionado que competidores para supply chain incidents; diferenciador competitivo en sales

**Lección**: Profundidad en áreas críticas puede ser mejor que amplitud mediocre

---

## SECCIÓN 5: TEMPLATES, CHECKLISTS Y MATURITY ASSESSMENT FORMS

### Template 1: Maturity Scoring Sheet

```markdown
# Security Maturity Assessment Scorecard

**Organization**: Example Corp  
**Assessment Date**: Dec 2024  
**Assessors**: CISO, CTO, Security Lead  

---

## Dimensión: Governance & Strategy

| Nivel | Descripción | Evidencia Requerida | ¿Aplica? |
|-------|-----------|-----------|---------|
| 1 (Reactivo) | Policies en docs but not enforced | Algunos documentos viejos | ❌ |
| 2 (Definido) | Policies documentadas, roles asignados, budget | POLICY.md actualizado 2024 | ✅ |
| 3 (Repetible) | Security in architecture decisions, exceptions formal | Monthly arch review con security | ⚠️ (occasional) |
| 4 (Gestionado) | Risk KPIs, dashboards, regular policy reviews | CRO tiene seguridad metrics | Partial |
| 5 (Optimizado) | Security in culture, continuous improvement | N/A |  |

**Current Level**: 2.0  
**Target Level (12 months)**: 3.0  
**Gaps**: Exceptions not formally tracked; policy reviews should be annual not ad-hoc

---

## Dimensión: Identidad & Acceso

| Nivel | Descripción | Current State |
|-------|-----------|-----------|
| 1 | Shared passwords, no auditing | ❌ |
| 2 | **Password policy, basic roles, logs ✅** |  |
| 3 | SSO, RBAC, annual access reviews | ❌ (SSO missing) |
| 4 | PAM, MFA, continuous monitoring | ❌ |
| 5 | Zero-trust, behavior analytics | ❌ |

**Current Level**: 2.0  
**Gaps to 3.0**: SSO implementation, RBAC refinement, access review process

---

## Dimensión: Hardening & Vulnerability

**Current Level**: 1.5  
**Detailed Assessment**: VulnScanning done quarterly (not enough), patching ad-hoc

**Gaps to 2.0**:
- [ ] Vulnerability SLA defined (30 days for critical)
- [ ] Monthly patching schedule implemented
- [ ] Hardening checklist created

---

**OVERALL MATURITY SCORE**: 2.1/5.0

**Top 3 Priorities**:
1. Identity & Access: Implementation of SSO (justification: 80% IT tickets related to password reset)
2. Hardening: Patching automation (justification: 15 unpatched critical CVEs found)
3. Governance: Annual policy reviews (justification: policies are 3 years old, no enforcement)

**Estimated Timeline to Level 3**: 12-18 months, $800K budget, 3 FTE

---

## Action Items with Timeline

| Acción | Due Date | Owner | Status |
|--------|----------|-------|--------|
| Draft SSO RFP | Jan 15 | CTO | Not Started |
| Pilot SSO (100 users) | Mar 1 | IT Lead | Not Started |
| Annual governance review | Feb 28 | CISO | Not Started |
| Patching SLA documented | Jan 31 | Security | In Progress |
```

### Template 2: Risk Scoring Matrix

```markdown
# Risk Assessment & Prioritization Matrix

**Purpose**: Traducir hallazgos técnicos a prioridades de negocio

---

## Matriz de Riesgo (Likelihood × Impact)

```
         LOW IMPACT | MEDIUM IMPACT | HIGH IMPACT | CRITICAL
LOW PROB    5           4             3             2
MED PROB    6           4             2             1
HIGH PROB   7           3             1             1
```

**Score 1**: Do immediately (< 1 week)
**Score 2**: Do this month
**Score 3**: Do this quarter
**Score 4-7**: Backlog (fix when capacity allows)

---

## Ejemplos de Hallazgos Priorizados

### Hallazgo 1: Unpatched Database (CVE-2024-5678)
- **Technical Severity**: Critical (CVSS 9.5)
- **Likelihood**: High (vulnerable database exposed to internet)
- **Impact**: Critical (database has 50M customer records)
- **Risk Score**: 1 (DO IMMEDIATELY)
- **Mitigation**: Patch within 48 hours or firewall access

### Hallazgo 2: Weak TLS cert (TLS 1.0 allowed)
- **Technical Severity**: High (CVSS 7.0)
- **Likelihood**: Medium (would need network intercept + downgrade attack)
- **Impact**: Medium (might expose PII+)
- **Risk Score**: 2 (THIS MONTH)
- **Mitigation**: Disable TLS 1.0, enforce TLS 1.2+

### Hallazgo 3: Outdated SSH Server (version 6.0)
- **Technical Severity**: Medium (older, but patches known)
- **Likelihood**: Medium (would require specific CVE)
- **Impact**: Medium (access to systems)
- **Risk Score**: 3 (THIS QUARTER)
- **Mitigation**: Scheduled update in next maintenance window

### Hallazgo 4: Code reviewer guideline not documented
- **Technical Severity**: Low
- **Likelihood**: Low (not critical path issue)
- **Impact**: Low (minor culture gap)
- **Risk Score**: 4-5 (BACKLOG)
- **Mitigation**: Document and socialize in next team meeting
```

### Template 3: Roadmap Execution Tracking

```markdown
# Security Maturity Roadmap - 2025

## Q1 2025

### Initiative 1: SSO Pilot
- **Current State**: No centralized authentication
- **Target State**: SSO for 100 corporate users
- **Effort**: 6 weeks (architecture, infra, app integration)
- **Owner**: IT Director
- **Success Metrics**:
  - [x] SSO architecture approved (Week 1)
  - [ ] Pilot infrastructure provisioned (Week 2)
  - [ ] 5 test apps integrated (Week 4)
  - [ ] 100 users onboarded (Week 6)
  - [ ] Password resets reduced by 30%

### Initiative 2: Patching SLA
- **Current State**: Ad-hoc patching
- **Target State**: Documented SLA (Critical: 48hrs, High: 7 days)
- **Effort**: 2 weeks (define, communicate, tooling)
- **Owner**: Security Lead
- **Success Metrics**:
  - [ ] SLA drafted and approved (Week 1)
  - [ ] Tools evaluated (Ansible, Puppet, Salt)
  - [ ] Pilot deployment to test environment
  - [ ] Training for ops teams

### Initiative 3: SIEM Implementation
- **Current State**: No centralized log management
- **Target State**: SIEM ingesting logs from 80% systems
- **Effort**: 8 weeks (procurement, config, tuning)
- **Owner**: Infrastructure Lead
- **Success Metrics**:
  - [ ] SIEM tool selected (Week 1-2)
  - [ ] Infrastructure provisioned (Week 3-4)
  - [ ] APIs/agents deployed to 50% systems (Week 5-6)
  - [ ] Initial dashboards deployed (Week 7)
  - [ ] Alert tuning begins (Week 8+)

## Q2-Q4 2025 (High Level)

- SSO full rollout (5000+ users)
- Automated patching in test → production
- SIEM operational (alerting, correlation)
- Annual access review process implementation
- Supply chain assessment begun

## Success Criteria (End of Year)
- Maturity score: 2.1 → 2.8
- MTTR for critical issues: 30 days → 5 days
- Unpatched critical systems: 15 → 2
- User MFA adoption: 0% → 50%
```

---

## CONCLUSIÓN: GRC TRANSFORMATION JOURNEY

```
MONTH 1-3: ESTABLISH FOUNDATION
→ Governance structure (CISO, team, board)
→ Assessment of current state
→ Roadmap defined

MONTH 4-9: QUICK WINS
→ Password policy enforcement
→ Vulnerability scanning operational
→ Incident response process formalized
→ Visible improvements (funding secured)

MONTH 10-18: STRUCTURAL CHANGES
→ SSO/MFA implementation
→ Patching automation
→ SIEM operational
→ Maturity level 1 → 2-3

MONTH 19-36: SUSTAINABILITY & OPTIMIZATION
→ Operational metrics embedded in culture
→ Security champions in teams
→ Continuous improvement mindset
→ Maturity level 3 → 4

LONG-TERM (Year 3+): OPTIMIZATION & INNOVATION
→ Zero-trust principles
→ ML-based detection
→ Security automation everywhere
→ Maturity level 4 → 5
```

**Key Insight**: GRC no es "proyecto finished in 1 year". Es **transformation cultural de 2-3 años** que cambias cómo la organización piensa sobre riesgo, mejora, y responsabilidad compartida.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - GRC, Risk & Maturity - Governance, Risk Management & Control Frameworks

### Integraciones ampliadas

- Jira: integracion recomendada para aumentar profundidad, evidencia y backlog.
- ServiceNow: integracion recomendada para aumentar profundidad, evidencia y backlog.
- PowerBI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Confluence: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: revision HIPAA.
- Integracion recomendada: Jira.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: gap PCI.
- Integracion recomendada: ServiceNow.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: madurez NIST.
- Integracion recomendada: PowerBI.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: revision HIPAA.
- Integracion recomendada: Confluence.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: gap PCI.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: madurez NIST.
- Integracion recomendada: ServiceNow.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: revision HIPAA.
- Integracion recomendada: PowerBI.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: gap PCI.
- Integracion recomendada: Confluence.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: madurez NIST.
- Integracion recomendada: Jira.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: revision HIPAA.
- Integracion recomendada: ServiceNow.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: gap PCI.
- Integracion recomendada: PowerBI.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: madurez NIST.
- Integracion recomendada: Confluence.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: revision HIPAA.
- Integracion recomendada: Jira.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: gap PCI.
- Integracion recomendada: ServiceNow.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: madurez NIST.
- Integracion recomendada: PowerBI.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: revision HIPAA.
- Integracion recomendada: Confluence.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: gap PCI.
- Integracion recomendada: Jira.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: madurez NIST.
- Integracion recomendada: ServiceNow.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: revision HIPAA.
- Integracion recomendada: PowerBI.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: gap PCI.
- Integracion recomendada: Confluence.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: madurez NIST.
- Integracion recomendada: Jira.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: revision HIPAA.
- Integracion recomendada: ServiceNow.
- Senal principal: control sin owner.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: gap PCI.
- Integracion recomendada: PowerBI.
- Senal principal: riesgo sin ranking.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: madurez NIST.
- Integracion recomendada: Confluence.
- Senal principal: backlog sin fechas.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

