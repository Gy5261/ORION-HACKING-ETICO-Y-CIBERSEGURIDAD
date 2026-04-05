# Secure SDLC Review Playbook (05)

## Visión Ejecutiva

Auditoría de seguridad en **código, pipelines, IaC, y dependencias**.
Cobertura: SAST, DAST, SCA, secrets scanning, supply chain.
Entrega: Code gaps, remediation scripts, SDLC improvements.

**Scope típico**: 3-21 días dependiendo tamaño

---

## Fase 1: Code Inventory (2-3 días)

### Repository Discovery

```bash
# Enumera todos los repos
curl -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/orgs/myorg/repos?per_page=100 | jq '.[] | .name'

# Clona para análisis local
for repo in $(cat repo-list.txt); do
  git clone https://github.com/myorg/$repo analysis/$repo
done
```

### Metadata

```json
{
  "repos": [
    {
      "name": "api-backend",
      "language": "Python",
      "framework": "Django",
      "size_loc": 45000,
      "dependencies": 42,
      "last_update": "2024-02-10"
    }
  ]
}
```

---

## Fase 2: SAST Analysis (3-5 días)

### Automated Scanning

```bash
# SonarQube
sonar-scanner -Dsonar.projectKey=myapp

# Checkmarx
/opt/Checkmarx/CheckmarxCommandLineInterface.sh \
  -LocationType folder \
  -LocationPath ./src \
  -ReportType PDF

# Semgrep
semgrep --config=p/security-audit ./src --json > sast-findings.json
```

### What to Look For

```
Injection Vulnerabilities:
  - SQL injection (string concat in queries)
  - Command injection (shell.exec() with user input)
  - Template injection (eval, template engines)

Crypto Issues:
  - Hardcoded secrets (API keys, passwords)
  - Weak algorithms (MD5, DES)
  - Predictable RNG (random.randint()  vs secrets.token_*)

Access Control:
  - Missing authorization checks
  - Insecure deserialization
  - XML External Entity (XXE)
```

### Example Custom Rule (Semgrep)

```yaml
rules:
  - id: hardcoded-password
    pattern: |
      password = "..."
    message: "Hardcoded password detected"
    languages: [python]
    severity: ERROR
```

---

## Fase 3: SCA - Dependency Scanning (2-3 días)

### Automated Tools

```bash
# OWASP Dependency-Check
dependency-check --project "myapp" --scan ./

# Snyk
snyk test --json > snyk-findings.json

# Trivy (supports many package managers)
trivy fs ./
```

### Vulnerability Analysis

```
High Priority Vulns:
1. Log4j (CVE-2021-44228) CRITICAL
   - Current: 2.14.1 (vulnerable)
   - Fix: Update to 2.17.1+
   - Effort: 2 hours (test + deploy)

2. Django (CVE-2024-XXXXX) HIGH
   - Current: 3.2.0
   - Fix: 3.2.18
   - Effort: 4 hours (regression test)
```

### Supply Chain

```bash
# Generate SBOM (Software Bill of Materials)
syft -o json ./src > sbom.json

# Check for typosquatting
curl https://api.libraries.io/packages/npm/express-typo

# License compliance
licensecheck --json > licenses.json
# Busca: GPL en código comercial ❌
```

---

## Fase 4: Secrets Scanning (1-2 días)

### Git History Scanning

```bash
# TruffleHog - busca credentials en git history
truffleHog git https://github.com/myorg/repo --json > secrets.json

# Gitleaks
gitleaks detect --source github --repo myorg/repo --json > gitleaks.json

# Manual check: common patterns
git log -p | grep -i "password\|apikey\|secret\|token" | head -20
```

### Remediation

```bash
# PROBLEMATIC:
conn_str = "Server=sql.example.com;User=admin;Pass=MySecurePass123"

# CORRECT (use environment variables):
import os
conn_str = f"Server={os.getenv('DB_SERVER')};User={os.getenv('DB_USER')};Pass={os.getenv('DB_PASS')}"

# Or use vault:
from hvac import Client
client = Client(url='https://vault.example.com', token=os.getenv('VAULT_TOKEN'))
secret = client.secrets.kv.read_secret_version(path='database')['data']['data']
```

---

## Fase 5: Pipeline & IaC Review (2-3 días)

### GitHub Actions / GitLab CI Review

```yaml
# BAD: Runs arbitrary PR code
name: Test
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: bash script-from-pr.sh  # ❌ DANGEROUS

# GOOD: Controlled, signed steps
name: Test (Secure)
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: refs/heads/main  # Merge commit, not PR source
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pytest tests/
      - name: SAST Check
        uses: semgrep/semgrep-action@v1
```

### Terraform Review

```bash
# Automated check
checkov -d . --framework terraform --output json > tf-audit.json

# Look for:
- [ ] Hardcoded passwords in default values
- [ ] Public = true on database / storage
- [ ] Security groups with 0.0.0.0/0
- [ ] No encryption at rest specified
```

---

## Fase 6: Code Review (3-5 días)

### Risk-Based Sampling

**Don't review everything** (too slow), focus on **high-risk modules**:

```
1. Authentication (30 lines)
2. Cryptography (50 lines)
3. Authorization (40 lines)
4. Payment processing (100 lines)
5. Admin functions (150 lines)

Total: ~370 lines of deep review per repo
```

### What To Check

```
- Input validation: all user inputs validated?
- Output encoding: XSS prevention?
- Crypto: keys rotated, appropriate algorithms?
- Session management: secure cookies, expiration?
- Error handling: no stack traces in responses?
- Logging: sensitive data masked (PII, passwords)?
```

### Example Finding

```
FILE: src/auth.py, Line 42

ISSUE: Hardcoded JWT secret
  secret = "my-super-secret"

RISK: If repo leaked, anyone can forge tokens

REMEDIATION:
  secret = os.getenv('JWT_SECRET')
  env vars set in CI/CD, never in git

EFFORT: 1 hour
```

---

## Fase 7: Roadmap & Gates (1 día)

### SDLC Improvements

```
IMMEDIATE (this week):
- [ ] Enable branch protection (require reviews)
- [ ] Set up Semgrep in CI
- [ ] Secrets scanning in pre-commit hooks

SHORT-TERM (30 days):
- [ ] Migrate to HashiCorp Vault
- [ ] Add SCA tool (Snyk)
- [ ] Code review standards document

LONG-TERM (90 days):
- [ ] Customer secure coding training
- [ ] SBOM generation automated
- [ ] Artifact signing (all releases)
```

### Quality Gates

```
Definition: Code can't merge to main if:
✗ SAST findings > 0 critical
✗ Secrets detected
✗ Test coverage drops
✗ SCA findings > 5 high

Exception process: CTO approval only
```

---

## Salida Esperada

1. **SAST Report**: Hallazgos por severidad
2. **SCA Report**: Vulnerable dependencies + SBOM
3. **Secrets Report**: Exposed credentials, rotation plan
4. **Pipeline Review**: Gates adding checklist
5. **Roadmap**: 30-90 días, effort, owner

---

## Herramientas

| Herramienta | Propósito |
|---|---|
| SonarQube | Code quality + SAST |
| Snyk | Vulnerable dependencies |
| TruffleHog | Secrets in git |
| Checkov | IaC scanning |
| OWASP Dep-Check | CVE database scan |

