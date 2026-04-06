# Checklists & Examples - Reusable Templates for Rapid Assessment

## Concepto

**Purpose**: Quick-reference templates when you don't need the full deep-dive modules

**Use Cases**:
1. Scoping interview (confirm what assets are in scope)
2. Quick risk assessment (identify biggest top-3 risks quickly)
3. Compliance readiness (fast checklist for audit prep)
4. Remediation tracking (confirm fixes are complete)

## Pre-Assessment Scope Checklist

Use this BEFORE starting deep-dive work to align expectations:

**Environment**:
- [ ] Development environments in scope? (usually NO)
- [ ] Test/staging environments included? (usually NO)
- [ ] Production only? (usual case)
- [ ] Cloud infrastructure included? (yes if AWS/Azure/GCP)
- [ ] On-premises infrastructure included? (yes if exists)

**Users/Systems**:
- [ ] How many servers/applications? (<10, 10-50, 50-100, 100+)
- [ ] How many users? (<100, 100-500, 500-5000, 5000+)
- [ ] Third-party integrations? (list 3-5 key ones)

**Risk Acceptance**:
- [ ] Risk acceptance signed by business owner
- [ ] Scope of acceptable risk document (low/medium/high)
- [ ] Exclusions documented (e.g., "don't test production database")

## Web Application Security Checklist

Quick checklist for reviewing web apps:

**Authentication & Authorization**:
- [ ] Password requirements: 12+ chars, complexity, no reuse
- [ ] Multi-factor authentication (MFA) for admin
- [ ] Session timeout: 30 min inactivity for sensitive, 8 hours for normal
- [ ] Authorization: User can't access other user's data
- [ ] API authentication: Tokens, not just session cookies

**Transport Security**:
- [ ] HTTPS enforced everywhere (not just login)
- [ ] HSTS header enforced (Strict-Transport-Security)
- [ ] TLS 1.2+ only (no SSL 3.0, TLS 1.0)
- [ ] Certificate valid for domain

**Request Handling**:
- [ ] Input validation (whitelist allowed characters)
- [ ] SQL injection: Parameterized queries used
- [ ] XSS protection: Content-Security-Policy header
- [ ] CSRF token on forms
- [ ] File uploads: Type validation, size limit, isolation

**Data Protection**:
- [ ] Sensitive data encrypted at rest (AES-256)
- [ ] Passwords hashed (bcrypt/scrypt, not MD5/SHA1)
- [ ] No PII in logs or error messages
- [ ] Secrets not hardcoded (API keys in config/vault)

**Error Handling**:
- [ ] Generic error messages (don't leak internals)
- [ ] Detailed errors logged (but not shown to users)
- [ ] Stack traces not visible to users

## Cloud Infrastructure Checklist

Quick checklist for AWS/Azure/GCP review:

**Identity & Access**:
- [ ] IAM: Principle of least privilege enforced
- [ ] Root account: MFA enabled, no active keys
- [ ] Service accounts: No overpermissioned accounts
- [ ] Cross-account access: Documented & restricted

**Data Protection**:
- [ ] S3 buckets: Private (not public-read/public-read-write)
- [ ] Encryption: At rest (KMS) and in transit (HTTPS)
- [ ] Database: Encrypted, isolated in VPC, no public access

**Network**:
- [ ] VPC: Segmented by sensitivity tier
- [ ] Security groups: Whitelist rules, not open ports
- [ ] NACLs: Restrict unnecessary inbound/outbound

**Monitoring & Logging**:
- [ ] CloudTrail/logging: All API calls logged
- [ ] Log retention: 90+ days minimum
- [ ] Alerting: On suspicious activities (new IAM user, public resource access)

**Secrets Management**:
- [ ] Secrets stored in Secrets Manager (not hardcoded)
- [ ] Rotation: Auto-rotate every 30-90 days
- [ ] Audit log: Who accessed secrets, when

## Mobile Application Checklist

Quick checklist for mobile/app review:

**Device Security**:
- [ ] MDM enforced (device encryption, PIN requirement)
- [ ] Device posture: OS version current, jailbreak/root detection
- [ ] App installation: Only from app store (not sideload)

**Communication**:
- [ ] Certificate pinning implemented (prevents MITM)
- [ ] TLS 1.2+ used for all network calls
- [ ] No sensitive data in HTTP (log data ok, not secrets)

**Storage**:
- [ ] Sensitive data encrypted locally
- [ ] Credentials NOT stored in plaintext
- [ ] Logs don't contain PII/secrets
- [ ] No SQL injection in local database queries

**Authentication**:
- [ ] Biometric or strong auth (not just PIN)
- [ ] Session timeout: 30 min
- [ ] Logout: Clears cached credentials

## Incident Response Checklist

Quick checklist when incident happens (activate IR team):

**Immediate (First Hour)**:
- [ ] Declare incident, activate IR team
- [ ] Preserve evidence (logs, memory, network captures)
- [ ] Contain: Isolate affected systems if compromise suspected
- [ ] Communicate: Notify legal, compliance, breach notification team

**Investigation (Day 1-2)**:
- [ ] Scope: How many systems? How much data?
- [ ] Timeline: When did it start? When was it detected?
- [ ] Impact: What data was accessed/exfiltrated?
- [ ] Root cause: How did attacker get in?

**Response (Day 2-7)**:
- [ ] Remediation: Fix the root cause vulnerability
- [ ] Monitor: Watch for re-compromise
- [ ] Notify: Communicate to affected users (if data breach)
- [ ] Document: Timeline, findings, lessons learned

## Vulnerability Assessment Findings Template

Use this format when reporting findings:

```markdown
## Finding Title

**Severity**: Critical / High / Medium / Low

**Component**: [System/App/Service affected]

**Description**: 
[What is the issue? 1-2 sentences]

**Impact**: 
[What's the business impact if not fixed?]
- Example: Allows attacker to access customer PII
- Cost if breached: $500K+ legal + reputation

**Evidence**:
[How was it found? Screenshots, command output]

**Recommendation**:
[How to fix it? Be specific]
- Example: Update library from v1.2.0 to v1.3.0 (security patch)
- Or: Add input validation for user-supplied data
- Or: Enable encryption at rest for database

**First Fix Date**: [Target remediation date]
**Severity Expectation**: Critical fixes in 24 hours, High in 1 week, Medium in 30 days
```

## Assessment Report Template

Use this for final deliverable:

```markdown
# Security Assessment Report
**Client**: [Organization]
**Date**: [Start - End dates]
**Scope**: [Systems/applications tested]
**Test Type**: Penetration test / Code review / Architecture review

## Executive Summary
[For non-technical stakeholders]
- Key findings: 3 Critical, 7 High, 15 Medium
- Root causes: Developer training gap (60%), configuration (30%), tooling (10%)
- Recommendation: Focus on developer security training

## Detailed Findings
[List each finding with template above]

## Remediation Timeline
- Critical: 24 hours to fix
- High: 1 week to fix
- Medium: 30 days to fix
- Low: Risk acceptance or backlog

## Metrics
- Total findings: 25
- Known vulnerabilities (outdated libraries): 12
- Design issues: 8
- Configuration: 5

## Conclusion
[Summary of overall security posture]
```

## Checklist

- [ ] Scope checklist completed with stakeholders
- [ ] Applicable domain checklists (web, cloud, mobile, etc.)
- [ ] Finding template defined & examples available
- [ ] Report template established
- [ ] Remediation timeline expectations clear
- [ ] Assessment schedule confirmed

## Quick Wins

1. Create 1-page "pre-assessment" checklist for your common assessment type
2. Document 3 recent findings using the finding template (consistency check)
3. Establish "critical = 24h, high = 1 week" timeline with business
4. Create report template for next assessment
5. Add 3 example findings to reference library
- log source
- senal
- falso positivo esperado
- enriquecimiento
- owner
```

## Ejemplo de salida breve

```markdown
## Resumen
Se observaron 3 quick wins y 1 riesgo sistemico.
No hubo evidencia de explotacion activa.
La prioridad inmediata es cerrar administracion expuesta.
```


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Checklists & Examples - Reusable Templates for Rapid Assessment

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

