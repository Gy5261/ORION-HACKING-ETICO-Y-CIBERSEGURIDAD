# Report Templates - Standard Formats for Deliverables

## Concepto

**Goal**: Consistent report structure so clients know what to expect

**Report Purpose**:
1. **Executive Summary**: For business leaders (risk, budget impact)
2. **Technical Findings**: For engineers (what to fix, how to fix)
3. **Remediation Roadmap**: For project managers (timeline, who, what, when)
4. **Appendix**: For auditors (evidence, methodology, scope)

## Template 1: Executive Summary

**For**: Non-technical stakeholders (CEO, CTO, risk manager)
**Length**: 1-2 pages
**Tone**: Business-focused (what's the risk, what does it cost?)

```markdown
# Security Assessment Report - Executive Summary
**Organization**: Acme Corp  
**Assessment Date**: April 1-5, 2026  
**Assessed By**: Security Team  

## Security Posture Overview

Overall Risk Rating: **HIGH** (was CRITICAL 6 months ago)

**Improvement**: Auth controls + incident response process = 40% risk reduction YoY

## Critical Findings (Must Fix in 24 hours)

1. **Unencrypted customer database** (High)
   - Impact: 100K customer records (names, SSNs, payment info) could be stolen
   - Cost to fix: $15K + 1 week engineering
   - Cost if breached: $5M (legal, notification, reputation)
   - Owner: Database team
   - Timeline: Acceptable risk if encrypted by April 12

2. **Production credentials in GitHub** (High)
   - Impact: Attacker could access production AWS account + customer data
   - Cost to fix: $2K + 2 days (rotate keys + audit access)
   - Cost if breached: $1M+ (incident response + downtime)
   - Owner: DevOps team
   - Timeline: Fix immediately (within 24h)

## Summary of All Findings

| Severity | Count | Trend | Timeline |
|----------|-------|-------|----------|
| Critical | 2 | ↓ (was 4) | 24 hours |
| High | 7 | ↓ (was 12) | 1 week |
| Medium | 15 | → (was 15) | 30 days |
| Low | 22 | ↑ (was 10) | Risk accept |

## Key Wins This Year

- ✅ Authentication controls: Implemented MFA organization-wide
- ✅ Network segregation: 80% of servers now in zero-trust zones
- ✅ Incident response: Reduced MTTD from 2 hours to 15 minutes
- ✅ Vulnerability management: 95% critical patches applied within SLA

## Recommended 90-Day Plan

**Phase 1 (Week 1-2): Stop the Bleeding**
- Fix critical findings (2 items above)
- Cost: < $50K
- Timeline: 2 weeks

**Phase 2 (Week 3-8): Improve Fundamentals**
- Implement secret management (vault)
- Enable comprehensive logging
- Deploy endpoint detection
- Cost: $100K (mostly engineering time)
- Timeline: 6 weeks

**Phase 3 (Week 9-12): Mature the Program**
- Automated scanning in CI/CD
- Purple team exercises
- Security training for engineers
- Cost: $40K
- Timeline: 4 weeks

**Total 90-Day Investment**: ~$200K / 12 weeks = **$16,667/week**  
**Risk Reduction**: HIGH → MEDIUM (60% improvement)

## Next Steps

1. Schedule remediation kickoff (April 6, 9 AM)
2. Assign owners for critical findings (24h approval)
3. Establish weekly reporting cadence (every Friday)
```

## Template 2: Technical Finding Detail

**For**: Engineers who will fix it
**Length**: 1-2 pages per finding
**Tone**: Technical (what, where, how to fix)

```markdown
## Finding: SQL Injection in Login Form

**Severity**: HIGH  
**Component**: Web application (login.example.com)  
**Affected Asset**: User authentication system  
**Control**: Input validation + parameterized queries

### Description

The login form accepts user input and uses it directly in SQL queries without sanitization.

**Vulnerable Code**:
```python
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
result = db.execute(query)
```

Attacker can bypass authentication by entering:
- Username: `admin' OR '1'='1`
- Password: (anything)

Result: Query becomes `SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='...'` which returns admin user without checking password.

### Impact

- **Confidentiality**: Attacker can read any user data (emails, payments, PII)
- **Integrity**: Attacker can modify user accounts, change passwords
- **Availability**: Attacker could drop tables (`'; DROP TABLE users; --`)

**Real-World Cost**: Historical SQL injection attacks cost $500K-$5M+ (legal, notification, remediation)

### Proof of Concept

```bash
curl "https://login.example.com/login" \
  -d "username=admin' OR '1'='1&password=test"
  
# Result: Login bypassed, admin access granted
```

### Recommendation

**Use parameterized queries** (prepared statements):

```python
username = request.form['username']
password = request.form['password']

# SAFE: Parameter binding prevents injection
query = "SELECT * FROM users WHERE username=? AND password=?"
result = db.execute(query, (username, password))
```

This way, the database treats user input as DATA, not executable code.

**Alternative Approaches**:
1. ORM (SQLAlchemy, Django ORM) = automatic parameterization
2. Escape input (less safe, use parameterization if possible)
3. WAF rule blocking SQL keywords (brittle, not primary defense)

### Remediation Steps

1. **Code Review** (1 day)
   - Find all database queries
   - Identify non-parameterized queries
   
2. **Code Changes** (3 days)
   - Rewrite queries using parameterization
   - Add unit tests (verify injection blocked)
   
3. **Testing** (2 days)
   - Manual testing: Try SQL injection payloads (should fail)
   - Automated testing: SAST scanner should find no SQL injection
   
4. **Deployment** (1 day)
   - Deploy to staging first
   - Verify all login workflows work
   - Deploy to production

**Total Timeline**: 1 week

### Verification

**How will we know it's fixed?**

- [ ] Parameterized queries in use (code review confirms)
- [ ] SQL injection test fails (attacker payload rejected)
- [ ] SAST scan: No SQL injection findings
- [ ] Users can still login (functionality preserved)

### Residual Risk

- **Risk**: Prepared statements don't prevent all attacks
- **Mitigation**: Also implement input validation (whitelist allowed characters)

### Owner & Timeline

- **Owner**: Backend team lead (John Smith)
- **Timeline**: Start April 6, complete by April 13
- **Block-by**: Mobile team (if they also have SQL queries)

```

## Template 3: Remediation Roadmap

**For**: Project managers (who does what, when?)
**Length**: 1 page
**Tone**: Timeline-focused

```markdown
## 90-Day Remediation Roadmap

### Priority 1: Stop the Bleeding (Week 1-2)

| Item | Owner | Timeline | Success Criteria |
|------|-------|----------|------------------|
| Encrypt database | DBA team | Week 1 | Database encrypted, zero impact |
| Rotate production keys | DevOps | Week 1 | Old keys revoked, new keys in use |
| Enable MFA for admin | SecOps | Week 2 | 100% of admins require MFA |

**Budget**: $50K  
**Risk Reduction**: HIGH → MEDIUM

### Priority 2: Improve Fundamentals (Week 3-8)

| Item | Owner | Timeline | Success Criteria |
|------|-------|----------|------------------|
| Implement secret vault | DevOps | Week 3-4 | All secrets in vault, zero hardcoded |
| Enable comprehensive logging | SecOps | Week 4-5 | Logs shipping to SIEM, retention 90d |
| Deploy EDR + vulnerability scanner | SecOps | Week 5-7 | 100% endpoints covered, alerts routing |
| Code remediation (SQL injection, etc.) | Dev team | Week 3-8 | All findings fixed + SAST clean |

**Budget**: $100K  
**Risk Reduction**: MEDIUM → LOW-MEDIUM

### Priority 3: Mature Program (Week 9-12)

| Item | Owner | Timeline | Success Criteria |
|------|-------|----------|------------------|
| Automate scanning in CI/CD | DevOps | Week 9-10 | Every PR scanned before merge |
| Purple team exercise | SecOps | Week 11 | 1 successful attack scenario detected |
| Security training | HR + SecOps | Week 12 | 90%+ employees trained |

**Budget**: $40K  
**Risk Reduction**: LOW-MEDIUM → LOW

### Overall Timeline

```
Week  1  2  3  4  5  6  7  8  9 10 11 12
P1    |==|==|
P2         |==|==|==|==|==|
P3                          |==|==|==|
Risk  H     M        LM        L
Budget 50K    100K            40K
```

**Total**: 12 weeks, $190K investment = **$16K/week**

```

## Template 4: Appendix - Methodology & Evidence

**For**: Auditors, compliance teams
**Length**: As needed
**Tone**: Formal, documentary

```markdown
## Appendix A: Assessment Methodology

**Scope**:
- Web application: login.example.com, API at api.example.com
- Infrastructure: AWS account prod-main
- Timeframe: April 1-5, 2026
- EXCLUDED: Development environment, third-party integrations

**Methods Used**:
1. Source code review (SAST scanning + manual review)
2. Runtime testing (curl, Burp Suite, network capture)
3. Infrastructure audit (AWS IAM, S3 configuration review)
4. Interviews (2h with security team, 1h with platform team)

**Standard Applied**:
- OWASP Top 10 (2021)
- CWE Top 25
- Cloud Security Alliance (CSA) Cloud Controls Matrix

**Tools**:
- Semgrep (code analysis) - v1.42
- OWASP ZAP (passive scanning) - v2.13
- Nmap (scoped port scan) - v7.93
- Curl (HTTP inspection) - v7.88

## Appendix B: Finding Evidence

[Detailed evidence for each finding - see Evidence Template in Reference 27]

### Evidence 1: SQL Injection

- Timestamp: 2026-04-03T14:20:30Z
- Asset: login.example.com
- Payload: `admin' OR '1'='1`
- Result: Login bypassed
- Screenshot: [attach image]

## Appendix C: Limitations & Caveats

- Assessment is point-in-time (specific to April 1-5, 2026)
- Code review covered 95% of codebase (some components excluded at client request)
- Infrastructure review was read-only (no exploitation/persistence testing)
- Third-party vendor security NOT included in scope
```

## Checklist

- [ ] Executive summary: High-level, business language
- [ ] Technical findings: Specific, evidence-based, reproducible
- [ ] Remediation roadmap: Owners, timelines, success criteria
- [ ] Appendix: Methodology, tools, evidence, limitations clear
- [ ] Tone matches audience (executives ≠ engineers)
- [ ] No PII/secrets in report (properly redacted)
- [ ] Timeline realistic (not optimistic)
- [ ] Residual risk acknowledged (honesty about what remains)

## Quick Wins

1. Create 1-page executive summary template for your assessment type
2. Document 1 major finding using template above
3. Draft 90-day remediation roadmap (3 phases)
4. Add "how we measured success" to next report
5. Get feedback from client (was report useful? Missing anything?)


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Report Templates - Standard Formats for Deliverables

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

