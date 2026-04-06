# Domain Taxonomy Extended - Detailed Security Domains

## Concepto

**Purpose**: Break down security into domains so assessments are comprehensive

**Key Principle**: Every domain = questions to ask + controls to evaluate

## Domain 1: Web & API Security

### Headers & Transport
- HTTPS enforced everywhere (not just login)
- HSTS header (force HTTPS future visits)
- X-Frame-Options (clickjacking prevention)
- X-Content-Type-Options: nosniff (prevent MIME-sniffing)
- Content-Security-Policy (prevent XSS)
- TLS 1.2+ (no SSL 3.0, TLS 1.0)

### Authentication & Session
- Multi-factor authentication (MFA) for admin
- Password requirements (12+, complexity, no reuse)
- Session timeout (30 min inactivity for sensitive)
- Logout clears session + cookies
- API authentication (tokens, not just cookies)

### Request Handling
- Input validation (whitelist allowed chars)
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)
- CSRF tokens on forms
- Command injection prevention
- Rate limiting (prevent brute force, DoS)

### Data Protection
- Sensitive data encrypted (at rest AES-256, in transit TLS)
- No PII in logs/error messages
- Secrets not hardcoded (vault/KMS)
- API responses don't leak internals

### File Upload
- File type validation
- File size limits
- Scan for malware
- Isolation (not served as executable)

## Domain 2: Cloud Infrastructure (AWS/Azure/GCP)

### Identity & Access
- IAM: Principle of least privilege
- Root account: MFA enabled, no active keys
- Service accounts: No overpermissioned accounts
- Cross-account access: Restricted + audited
- Temporary credentials: Preferred over static keys

### Data Protection
- Encryption at rest (KMS) on all data stores
- Encryption in transit (HTTPS, VPN)
- Database encryption + isolation in VPC
- No public database access
- Backups encrypted + isolated

### Network & Perimeter
- VPC: Segmented by sensitivity tier
- Security groups: Whitelist rules (not open-all)
- NACLs: Restrict unnecessary inbound/outbound
- VPN for remote access (not direct internet)

### Logging & Monitoring
- CloudTrail / Activity logs enabled (all API calls)
- Log retention 90+ days
- Alerting on suspicious activity
- Centralized log storage (CloudWatch, Splunk)
- No PII in logs

### Compute
- Patching: OS + applications current
- Container security: No root, vulnerability scanning
- Secrets: Not in container images (use Secrets Manager)
- Code: Signed + integrity verified

## Domain 3: Identity & Access (Human + Services)

### Human Identity
- Directory service (AD, Azure AD, Okta)
- MFA enforced for all users (not optional)
- Conditional access (block risky logins)
- Privileged access management (separate admin accounts)

### Service Identity
- Service accounts: Minimal permissions (least privilege)
- No shared service accounts
- Long-lived credentials minimized (use tokens/STS)
- Service-to-service: mTLS for encryption + authentication

### Admin/Privileged Access
- Tiered admin (user ≠ admin ≠ super-admin)
- Temporary elevation (JIT access, requires approval)
- Audit logging (every admin action logged)
- No standing admin rights (minimize exposure window)

### Federation & Remote Access
- Single sign-on (SSO) integration
- VPN: TLS encryption, device posture checks
- Device trust: Endpoint detection + zero-trust validation
- Contractor access: Temporary + scoped (not permanent)

## Domain 4: Defense & Operations

### Telemetry Collection
- Agent: Endpoint detection (EDR)
- Network: IDS/IPS, NetFlow
- Application: APM (Application Performance Monitoring)
- Logs: Central collection (SIEM)
- Metrics: Performance data collection

### Alert & Incident Response
- Alert tuning: <10% false positive rate
- Escalation process: Clear, tested
- Runbooks: Step-by-step response procedures
- Incident classification: Severity levels + templates
- SLA: Response time targets (Critical = 1h, High = 4h)

### Detection Engineering
- Rules: Math-based detection (not just signatures)
- Coverage: 80%+ of attack scenarios detected
- MTTD: Mean time to detect target <5 min
- Testing: Purple team validation of coverage
- Tuning: Iterative improvement based on findings

### Threat Hunting & Investigation
- Proactive: Look for unknown threats (not just alerts)
- Tools: SIEM search, endpoint forensics, network analysis
- Timeline: Establish attack sequence (when did X happen?)
- Scope: How many assets/users affected?

## Domain 5: Engineering & Development

### Repo Security
- Secrets scanning: Pre-commit hook (TruffleHog, GitGuardian)
- Code review: Required before merge
- Branch protection: Admin can't bypass
- History: Immutable (can't rewrite past commits)

### Build Security (SAST/SCA)
- SAST: Static code analysis (Semgrep, SonarQube)
- SCA: Dependency tracking (npm audit, Snyk)
- Artifact signing: How do we know binary is legit?
- Container scanning: Vulnerability scan before deployment

### IaC (Infrastructure as Code)
- Terraform/CloudFormation: Code reviewed
- Configuration: No hardcoded secrets (use data sources)
- Policy: Prevent dangerous configurations (public bucket = block)

### Release Controls
- Build: Automated (not manual, error-prone)
- Testing: Automated + manual gates
- Approval: Defined (who signs off?)
- Observability: Can verify what was deployed

## Domain 6: Data Security & Privacy

### Data Inventory
- What data exists? (PII, payments, trade secrets)
- Where does it live? (databases, files, backups)
- Who accesses it? (humans, services, contractors)
- How long is it retained? (10 years? 6 months?)

### Data Classification
- Level system (PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED)
- Rules: Based on sensitivity (PII = RESTRICTED)
- Handling: Rules per level (RESTRICTED = encrypt + audit)

### PII & Regulatory Compliance
- GDPR: DPO, consent, right to delete
- CCPA: User rights, disclosure
- HIPAA: Patient privacy, encryption required
- PCI-DSS: Payment data handling requirements

### Data Minimization
- Collect only what you need
- Field-level (transmit only 5 fields, not 50)
- Temporal (delete when no longer needed)
- Benefit: Smaller breach surface, easier compliance

## Domain 7: Secrets Management

### Secret Types
- Database passwords
- API keys
- Encryption keys
- Certificates
- Vault credentials
- OAuth tokens

### Lifecycle
1. Generate: Create strong secret (random, 32+ bytes)
2. Store: Vault/KMS (encrypted, access logs)
3. Use: Retrieve at app startup
4. Rotate: 30-90 days automatically
5. Retire: Revoke after rotation, clean logs

### Vault/KMS Protection
- Encryption: Data encrypted even in vault
- Access: Audit log of who accessed secrets
- Approval: Some secrets need manager approval
- Availability: Vault failure = app failure (design for this)

## Domain 8: Vendor & Supply Chain Risk

### VendorVetting
- Due diligence: Security questionnaire before signup
- Contracts: SLAs, data location, notification requirements
- Assessment: Periodically re-assess (annual minimum)

### Dependency Management
- SBOM: Track all dependencies (direct + transitive)
- Vulnerability: Check for known CVEs regularly
- Updates: Security patches within SLA
- Risk: Use open-source? Commercial? Licensed?

### Supply Chain
- Build security: How is vendor's software built?
- Signing: Code signed by vendor (prevent tampering)
- Provenance: Can we trust this came from vendor?

## Domain 9: Detection & Hunting

### Detection Strategy
- Signature-based: Known attacks (fast, limited)
- Behavior-based: Unknown attacks (slower, catches new threats)
- Anomaly: Deviation from normal (high tuning burden)
- Threat-intel-driven: Known indicators of compromise (group with others)

### Hunting
- Question: "What are we not seeing?"
- Data: Logs, telemetry, netflow
- Tools: SIEM, endpoint analysis, network capture
- Cadence: Weekly/monthly hunt (not just alerts)

## Domain 10: Agentic AI & Automation

### When AI Helps
- Repetitive data processing (log parsing, report generation)
- Evidence collection (safe read-only operations)
- Statistical analysis (pattern finding, anomalies)

### AI Risks
- Hallucination: Confidence in wrong answer
- Context: Missing critical constraints (don't test prod!)
- Explosion: Scripts that create bigger problems
- Secrets: AI output might leak sensitive data

### AI Safeguards
- Read-only: No write access without approval
- Audit: Every AI action logged + reviewable
- Sandbox: Test environment, not production
- Review: Human review before any changes

## Quick Reference by Role

**Security Engineer**:
- Domains 1-5, 9 (technical implementation)

**Cloud Architect**:
- Domain 2 (cloud security patterns)

**Security Operations (SOC)**:
- Domains 4, 9 (detection, response)

**DevSecOps**:
- Domains 5, 6, 7, 8 (build security, supply chain)

**Compliance/GRC**:
- Domains 6, 7, 8 (data, secrets, vendor)

**Executive/Risk**:
- All domains (understand entire landscape)

## Checklist

- [ ] All 10 domains covered in assessment plan
- [ ] Scoping tool: Which domains in scope, which out?
- [ ] Interview questions: One question per domain
- [ ] Evidence: At least 1 evidence item per domain
- [ ] Remediation: Fixes span all domains (not just web)
- [ ] Coverage: No domain completely neglected

## Quick Wins

1. Create 1-page checklist for your industry (top 5 domains to check)
2. Pick 1 domain you're weakest on (focus learning there)
3. Interview internal team on 1 domain (what controls exist?)
4. Document 1 finding from each domain type (breadth check)
5. Map your tools to domains (which tools cover which domains?)

- small scripts
- parsing
- normalization
- report generation
- evidence formatting


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Domain Taxonomy Extended - Detailed Security Domains

### Integraciones ampliadas

- OpenAI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Azure OpenAI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Langfuse: integracion recomendada para aumentar profundidad, evidencia y backlog.
- OpenTelemetry: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: agente de triage.
- Integracion recomendada: OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: guardrail de prompts.
- Integracion recomendada: Azure OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: generacion de evidencia.
- Integracion recomendada: Langfuse.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: agente de triage.
- Integracion recomendada: OpenTelemetry.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: generacion de evidencia.
- Integracion recomendada: Azure OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: agente de triage.
- Integracion recomendada: Langfuse.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenTelemetry.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: agente de triage.
- Integracion recomendada: Azure OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: guardrail de prompts.
- Integracion recomendada: Langfuse.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenTelemetry.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

