# Secure Engineering & SDLC - Shifting Security Left in Development

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe Secure SDLC?

**Problem**: Traditional security = find problems AFTER deployment → expensive + late.
- Cost to fix in prod: $1M+ (breach, downtime, reputation)
- Cost to fix in code review: $100 (few developer hours)
- Cost to prevent at design: $10 (educated developer + guidelines)

**"Shift Left" Philosophy**: Move security earlier in development lifecycle:
- ❌ Traditional: Code → Deploy → Attack → Breach → Fix
- ✅ Secure: Design → Threat Model → Code → Test → Deploy → Monitor

**Objetivo crítico**:
- ✅ Prevent vulnerabilities BEFORE they reach production
- ✅ Educate developers (security is their job too)
- ✅ Automate checks (SAST, SCA, secret scanning in CI/CD)
- ✅ Balance speed + security (not blocking every PR)
- ✅ Track & measure (metrics on vulnerability injection vs remediation)

### 5 Principios Fundamentales de Secure SDLC

1. **Security by Design (Threat Model First)**
   - Before writing code: Ask "What can go wrong?"
   - Document threats + controls (not implemented yet, but planned)
   - **Exemplo**: New user authentication feature → threat model: "Attacker tries brute force" → control: "Rate limiting + lockout"
   - **Versus**: Build feature, security team finds no rate limiting, retrofit costly

2. **Developers Are Security First Responders**
   - Security team can't review every line of code
   - Developers write code; developers should know security patterns
   - **Investment**: Training > hiring more security people
   - **Patrón**: Secure coding guidelines + code review focus on security

3. **Automate What Can Be Automated (Human Review For Logic)**
   - ✅ Automate: Known bad patterns (SAST runs, finds common flaws)
   - ✅ Automate: Vulnerable dependencies (SCA, dependency checks)
   - ✅ Automate: Secrets (regex scan, block hardcoded keys)
   - ❌ DON'T automate: Business logic flaws (requires human understanding)
   - **Trade-off**: Automation faster but misses context; humans slower but catch logic errors

4. **Fast Feedback Loop (Developer Knows Same Day)**
   - If vulnerability found in code review 2 weeks later: Context lost, fix expensive
   - If SAST tool alerts in IDE WHILE coding: Developer fixes immediately
   - **Velocity**: SAST in IDE + quick fixes >> One-time audit post-deployment

5. **Risk-Based Enforcement (Not All Rules Apply Equally)**
   - Not all code equally risky (authentication tier = high; logging tier = low)
   - Apply strictest rules to highest-risk code
   - **Ejemplo**: PRs modifying auth/crypto/DB = require security review; PRs changing UI = skip
   - **Pragmatic**: Avoid security burden that slows all development; focus on impact

---

## SECCIÓN 2: COMPONENTES DE SECURE SDLC

### Componente 1: Threat Modeling & Secure Design

**Objetivo**: Identify threats BEFORE building.

**Herramientas típicas**: STRIDE, PASTA, DFD (Data Flow Diagrams)

**Ejemplo STRIDE Threat Model**:

```markdown
## Feature: User Authentication API

### Data Flow:
Client → API Server → Database

### STRIDE Analysis

**S (Spoofing Identity)**
- Threat: Attacker impersonates valid user
- Control: MFA required for login
- Status: Implemented

**T (Tampering)**
- Threat: Attacker modifies password hash in transit
- Control: Use HTTPS/TLS
- Status: Implemented

**R (Repudiation)**
- Threat: User denies activity ("I didn't login")
- Control: Log all auth attempts w/ timestamp
- Status: NOT implemented → add audit logging

**I (Information Disclosure)**
- Threat: Attacker reads password hashes from database
- Control: Use bcrypt hashing
- Status: Implemented; review iteration count

**D (Denial of Service)**
- Threat: Attacker brute forces, locks out legitimate users
- Control: Rate limit + account lockout
- Status: Rate limit implemented; lockout missing → add

**E (Elevation of Privilege)**
- Threat: Attacker escalates from guest to admin
- Control: Role-based access control (RBAC)
- Status: Implemented; review privilege assignments

### Remediation
- [ ] Add audit logging (Repudiation gap)
- [ ] Implement account lockout (DoS mitigation)
- [ ] Review bcrypt iterations (currently 10, increase to 12)
- [ ] Validate RBAC assignments in code review

Estimated effort: 3 days
Timeline: Sprint N+1
```

**Checklist - Threat Modeling**:
- ✅ Data flows documented (input, processing, output)
- ✅ Trust boundaries identified (where data enters system)
- ✅ Threats identified per STRIDE (6 categories)
- ✅ Controls mapped to threats (how do you prevent?)
- ✅ Gaps documented (missing controls)
- ✅ Remediation prioritized (which gaps first?)

---

### Componente 2: Static Application Security Testing (SAST)

**Objetivo**: Automated code analysis to find common vulnerabilities.

**Herramientas recomendadas** (language-specific):
- Java: Spotbugs, SonarQube, Checkmarx
- Python: Bandit, Semgrep, PyCharm (IDE)
- JavaScript: ESLint (with security rules), Snyk
- .NET: Roslyn (built-in), Fortify
- Go: gosec, Semgrep

**Ejemplo SAST Detection**:

```python
# Vulnerable code (SQL injection)
user_input = request.get('username')
query = f"SELECT * FROM users WHERE name = '{user_input}'"
db.execute(query)  # VULNERABLE!

# SAST tool detects:
# - String interpolation in SQL query
# - User input not sanitized
# - Alert: "Possible SQL injection"
```

**Checklist - SAST Implementation**:
- ✅ Select tool(s) compatible with your stack
- ✅ Configure in CI/CD pipeline (run on every PR)
- ✅ Set security gate (fail build if > critical issues found)
- ✅ Tune rules (reduce false positives for your codebase)
- ✅ Track metrics (# findings over time)
- ✅ Developer training (explain findings, how to fix)

---

### Componente 3: Software Composition Analysis (SCA) & Dependencies

**Objetivo**: Identify vulnerable libraries before deploying.

**Herramientas recomendadas**:
- npm/Node: npm audit, Snyk, WhiteSource
- Python: safety, Snyk
- Java: OWASP Dependency-Check
- All: Renovate, Dependabot

**Ejemplo SCA Detection**:

```bash
$ npm audit
193 vulnerabilities found
- 15 critical
- 50 high
- 128 low/medium

# Specific finding:
Vulnerability: lodash before 4.17.21
Patterns matching: lodash@4.16.0 (you have this)
Recommendation: Update to lodash@4.17.21
Severity: High (potential RCE in template engine)
```

**Checklist - Dependency Management**:
- ✅ Generate SBOM (Software Bill of Materials) for all apps
- ✅ Scan dependencies weekly for new CVEs
- ✅ Pin sensitive dependencies (lock versions, don't auto-upgrade)
- ✅ Update routine (monthly patches, out-of-band for critical)
- ✅ Track transitive dependencies (library A uses library B with CVE)
- ✅ Monitor for deprecated libraries (EOL = no more patches)

---

### Componente 4: Secret Management

**Objetivo**: Prevent hardcoded credentials in code/images.

**Herramientas recomendadas**:
- git-secrets, pre-commit, TruffleHog (scan code for leaks)
- HashiCorp Vault, AWS Secrets Manager, Azure Key Vault (store secrets)
- Docker: Use build secrets, not ENV vars

**Checklist - Secret Prevention**:
- ✅ Pre-commit hook (blocks commits with "password" or "api_key" strings)
- ✅ CI/CD secret scan (TruffleHog finds leaked patterns)
- ✅ Secrets stored externally (Vault/SecretManager, not in code)
- ✅ Rotation policy (all secrets < 90 days old)
- ✅ Audit logging (who accessed what secret, when)
- ✅ .gitignore configured (never commit .env, config files with secrets)

---

### Componente 5: Infrastructure-as-Code (IaC) Security

**Objetivo**: Scan Terraform/CloudFormation for misconfiguration before deployment.

**Herramientas recomendadas**:
- Terraform: Checkov, tfsec, Sentinel (HashiCorp)
- CloudFormation: cfn-lint, Checkov
- All: Snyk, Bridgecrew

**Ejemplo IaC Misconfiguration**:

```hcl
# Vulnerable Terraform
resource "aws_s3_bucket" "data" {
  bucket = "customer-data"
  acl    = "public-read"  # VULNERABLE! Public access
}

# Checkov detects:
# - CKV_AWS_18: "S3 bucket has public access"
# - Recommendation: Set acl = "private"
```

**Checklist - IaC Scanning**:
- ✅ Scan all IaC in PR (fail if critical misconfiguration)
- ✅ Deny public access by default (force explicit whitelist)
- ✅ Require encryption for storage (S3, EBS, RDS)
- ✅ Network security: No open security groups (0.0.0.0/0)
- ✅ Logging enabled (CloudTrail, access logs, audit)
- ✅ Backup configured (snapshots, replicated)

---

### Componente 6: Code Review & Secure Review Criteria

**Objetivo**: Human review of code for logic flaws + security.

**Security Review Checklist (for each PR)**:
- ✅ Input validation: Is user input validated/escaped?
- ✅ Authentication: Are auth checks enforced?
- ✅ Authorization: Does code check permissions?
- ✅ Secrets: No hardcoded keys/passwords?
- ✅ Dependencies: Any new vulnerable libs?
- ✅ Error handling: Does it leak info (stack traces, paths)?
- ✅ Encryption: Data in transit (TLS) and at rest (encryption)?
- ✅ Logging: Sensitive data NOT logged?

**Ejemplo Code Review Finding**:

```python
# PR changes password reset flow

# Reviewer finds:
if reset_token == provided_token:
    reset_password(new_password)

# Issues identified:
1. Token comparison is string equality (timing attack possible)
2. No rate limiting (brute force token)
3. Token doesn't expire (old tokens valid forever)

# Feedback:
# - Use constant-time comparison (hmac.compare_digest)
# - Add rate limiting + lockout
# - Add expiration (token valid 1 hour only)
# - Add audit logging (who reset password, when)

# Status: Request changes (block merge until fixed)
```

---

## SECCIÓN 3: METODOLOGÍA Secure SDLC Implementation

### Fase 1: Assessment (Week 1)
- Current state: What security practices exist?
- Gaps: What's missing?
- Roadmap: Prioritize improvements

### Fase 2: Design Phase (Week 2-3)
- Threat modeling for new features
- Secure design patterns documented
- Architecture review before coding

### Fase 3: Development Phase (Week 4+)
- Developers write code with security in mind
- SAST + SCA run automatically in CI/CD
- Code review includes security checks

### Fase 4: Testing Phase
- DAST (dynamic testing) in staging environment
- Penetration testing (external security team)
- Security regression testing

### Fase 5: Deployment
- Security gates must pass (no critical issues)
- Secrets scanning one final check
- Artifact signing (provenance tracking)

### Fase 6: Post-Deployment
- Monitoring for security issues
- Metrics tracking (vulnerabilities, fixes, time to remediate)
- Security postmortems (blameless, focus on improving process)

---

## SECCIÓN 4: CASOS DE ESTUDIO

### Caso 1: Threat Modeling Prevented Vulnerability (Proactive)

**Scenario**: Design of API for customer data export.

**Threat Model**:
- Risk: Attacker exports all customer data
- Control: Rate limiting on export endpoint

**Result**: Rate limiting was designed from start, not retrofitted → cheaper, simpler, more effective

---

### Caso 2: SAST Caught SQL Injection (Automated)

**Scenario**: Feature to search orders by customer name.

**Code**: `query = f"SELECT * FROM orders WHERE customer_name = '{input}'"` (vulnerable)

**SAST Alert**: "Possible SQL injection in line 45"

**Developer Fix**: Use parameterized query → `cursor.execute("SELECT * FROM orders WHERE customer_name = ?", (input,))`

**Result**: Vulnerability fixed before review/deployment

---

## SECCIÓN 5: TEMPLATES

### Template 1: Secure Code Review Checklist

```markdown
# Security Code Review Checklist

## Review Checklist

### Authentication
- [ ] Are credentials validated on every sensitive operation?
- [ ] Are weak password requirements not accepted?
- [ ] Is multi-factor authentication supported/enforced?

### Authorization
- [ ] Is access control enforced based on user roles?
- [ ] Can users only access their own data?
- [ ] Are admin operations protected?

### Input Validation
- [ ] Is all user input validated (type, length, format)?
- [ ] Are inputs escaped/sanitized before use in queries?
- [ ] Are file uploads restricted (type, size)?

### Data Protection
- [ ] Is sensitive data encrypted in transit (TLS)?
- [ ] Is sensitive data encrypted at rest?
- [ ] Are passwords hashed with strong algorithms (bcrypt, Argon2)?

### Error Handling
- [ ] Do error messages leak sensitive info (paths, versions, usernames)?
- [ ] Are exceptions caught and handled gracefully?
- [ ] Are stack traces not exposed to users?

### Logging
- [ ] Are security events logged (login attempts, privilege changes)?
- [ ] Are logs NOT logging sensitive data (passwords, tokens)?
- [ ] Is logging tamper-proof (immutable)?

### Status
- [ ] Approved (no issues)
- [ ] Approved with comments (minor issues)
- [ ] Request changes (security issues found)
```

---

## CONCLUSIÓN

**Secure SDLC = Cultural Shift**

Not: "Security team approves code at end"
Actual: "Developers build security in from start; security team enables + validates"

**ROI**:
- Cost of breach: $4M average
- Cost of secure SDLC program: $500K/year
- Breaking even: 1 breach prevented
- Everything else = profit

**Key Success**:
- ✅ Education (developers know secure patterns)
- ✅ Automation (SAST/SCA in every PR)
- ✅ Feedback (developers know same day if issue)
- ✅ Balance (not so strict it slows shipping)


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Secure Engineering & SDLC - Shifting Security Left in Development

### Integraciones ampliadas

- GitHub Actions: integracion recomendada para aumentar profundidad, evidencia y backlog.
- GitLab CI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Semgrep: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Trivy: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: monorepo con secretos.
- Integracion recomendada: GitHub Actions.
- Senal principal: branch protection debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: SBOM faltante.
- Integracion recomendada: GitLab CI.
- Senal principal: dep obsoleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: release sin firmas.
- Integracion recomendada: Semgrep.
- Senal principal: provenance incompleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: monorepo con secretos.
- Integracion recomendada: Trivy.
- Senal principal: branch protection debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: SBOM faltante.
- Integracion recomendada: GitHub Actions.
- Senal principal: dep obsoleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: release sin firmas.
- Integracion recomendada: GitLab CI.
- Senal principal: provenance incompleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: monorepo con secretos.
- Integracion recomendada: Semgrep.
- Senal principal: branch protection debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: SBOM faltante.
- Integracion recomendada: Trivy.
- Senal principal: dep obsoleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: release sin firmas.
- Integracion recomendada: GitHub Actions.
- Senal principal: provenance incompleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: monorepo con secretos.
- Integracion recomendada: GitLab CI.
- Senal principal: branch protection debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: SBOM faltante.
- Integracion recomendada: Semgrep.
- Senal principal: dep obsoleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: release sin firmas.
- Integracion recomendada: Trivy.
- Senal principal: provenance incompleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: monorepo con secretos.
- Integracion recomendada: GitHub Actions.
- Senal principal: branch protection debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: SBOM faltante.
- Integracion recomendada: GitLab CI.
- Senal principal: dep obsoleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: release sin firmas.
- Integracion recomendada: Semgrep.
- Senal principal: provenance incompleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: monorepo con secretos.
- Integracion recomendada: Trivy.
- Senal principal: branch protection debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: SBOM faltante.
- Integracion recomendada: GitHub Actions.
- Senal principal: dep obsoleta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

