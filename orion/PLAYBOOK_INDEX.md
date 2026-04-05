# ORION-HACKING Playbook Index - Workflows Operativos Concretos

## Propósito

Los **playbooks** son workflows paso-a-paso que responden a **situaciones específicas**. 
Este índice te ayuda a identificar cuál es el correcto para tu caso.

**Regla de oro**: 
- Un assessment de 2+ semanas → Playbook 01
- Una aplicación web → Playbook 02
- Un cluster Kubernetes → Playbook 03
- Necesitas detecciones → Playbook 04
- Auditando código o pipeline → Playbook 05
- Incidente de seguridad → Playbook 06

---

## Matriz de Decisión Rápida

| Situación | Playbook | Duración | Dominio |
|---|---|---|---|
| "Audítame todo" (multi-dominio) | 01 | 2-4 semanas | Governance, Técnica, Reportes |
| "Tengo una app web" | 02 | 4h - 10 días | Web/API/AppSec |
| "Auditame cloud/K8s/IaC" | 03 | 3-5 días | Cloud, Container, Configuración |
| "Necesito reglas de detección" | 04 | Ongoing | Detection, SIEM, Hunting |
| "Auditame código y pipeline" | 05 | 2-3 semanas | SDLC, Secrets, Dependencies |
| "Tenemos incidente" | 06 | 4h - 2 días | Forensia, DFIR, Triage |

---

# Playbook 01: Authorized Assessment (Multi-Domain)

**Archivo**: `01-authorized-assessment-playbook.md`

## Propósito Ejecutivo

Assessment completo de una organización o dominio específico (si es amplio).
Metodología estructurada que combina gobernanza + técnica + reporte.
Entrega: Evaluación de riesgos, roadmap de remediación, métricas de madurez.

## Cuándo Usar

✅ Assessment general de 2-4 semanas  
✅ Cliente requiere cobertura multi-dominio  
✅ Requiere reporte ejecutivo formal  
✅ Hay equipo interno que debe participar  
✅ Compliance o governance es importante  

❌ Si solo necesitas validar una aplicación web (→ 02)  
❌ Si es solamente Cloud/IaC (→ 03, probablemente más rápido)  
❌ Si es incidente activo (→ 06)  

## Estructura del Workflow

### Fase 1: Pre-Engagement (Semana 1)
- Kick-off meeting: firmar ToR, scope, timeline
- Herramientas: verificar acceso a sistemas, VPN, WiFi
- Baseline: tomar snapshots de configuración relevante
- Equipo: identificar contactos técnicos, escalations
- Exclusiones: qué NO se toca (datos de producción, sistemas críticos)

### Fase 2: Ejecución (Semana 2-3)
Por dominio (en paralelo si es posible):
- **Governance**: revisar políticas, ToR, risk framework
- **Técnica**: por referencia relevante
  - Si web: playbook 02 (parallelize)
  - Si cloud: playbook 03 (parallelize)
  - Si infra: referencias 04, 09 (network, identity)
  - Si data/privacy: referencias 19, 18
- **Observabilidad**: log collection, baseline anomalies
- Daily sync: 15 min con cliente, status update, blockers

### Fase 3: Análisis (Semana 3-4)
- Hallazgos: normalizado vía `normalize_findings.py`
- Priorización: CVSS + esfuerzo + impacto
- Roadmap: 30-90-180 day remediation plan
- Risk scoring: antes/después mitigación
- Compliance mapping: si aplica (PCI, HIPAA, GDPR, SOC2)

### Fase 4: Reporte (Semana 4)
- Ejecutivo: 2-3 páginas, hallazgos top-5, roadmap, ROI
- Técnico: anexo con detalles, pasos reproducibles, evidencia
- Presentación: walkthrough con stakeholders
- Q&A: responder inquietudes

### Fase 5: Post-Engagement (2-4 semanas después)
- Seguimiento: cliente inicia remediación
- Re-testing: validar fixes después de hitos (30/90/180 días)
- Lessons learned: qué salió bien, qué mejorar

## Success Criteria

- [ ] Todos los sistemas in-scope validados
- [ ] Hallazgos → JSON normalizado
- [ ] Roadmap: 0-10 criticales, 0-20 altos, etc.
- [ ] Stakeholders: acuerdo en timeline de remediación
- [ ] Reporte: aprobado por cliente
- [ ] Evidencia: preservada y documentada

## KPIs / Métricas

| Métrica | Target |
|---|---|
| Cobertura de dominio (%) | ≥ 95% |
| Hallazgos críticos (30 días) | < 5 |
| MTTR promedio (remediation time) | < 45 días |
| Re-test pass rate | ≥ 95% |
| Cliente satisfacción | 8/10 |

## Timeline Realista

| Situación | Optimista | Normal | Pesimista |
|---|---|---|---|
| 1 dominio, 1 equipo | 1 semana | 2 semanas | 3 semanas |
| Multi-dominio, 5+ sitios | 2 semanas | 3 semanas | 5 semanas |
| Compliance-heavy (SOC2, PCI) | 3 semanas | 4 semanas | 6+ semanas |

## Salida Esperada

1. **Reporte Ejecutivo**: 5-10 páginas
2. **Technical Findings**: 20-50 páginas (hallazgos + pasos reproducibles)
3. **Roadmap**: Tabla 30-90-180, prioridades, esfuerzo
4. **Compliance Mapping**: Qué controles cumplen qué req
5. **Evidencia**: Screenshots, logs, config snippets (archivo ZIP)
6. **JSON Normalizado**: Todos los hallazgos en `findings.json`

## Variaciones

### Quick Assessment (4-5 días)
- Solo superficies principales (web, cloud, identity)
- Sin hardening detallado
- Reporte técnico corto
- Roadmap: top-10 nada más

### Deep Dive (6-8 semanas)
- Cada dominio según referencias extensas
- Red team ejercicios
- Supply chain audit
- Purple team feedback loops
- Roadmap detallado con arquitectura "después"

## Common Pitfalls & Mitigations

| Pitfall | Mitigación |
|---|---|
| Scope creep | Revisión semanal con cliente, doc cambios en ToR |
| Falsos positivos | Validar cada hallazgo con 2+ métodos, reproducir |
| Falta de contexto | Daily sync + documentation de assumptions |
| Burnout del equipo | Rotación de auditor principal, peer review |
| Cliente no actúa | Roadmap con ROI, reuniones quincenales, seguimiento |

---

# Playbook 02: Web API Appsec Review

**Archivo**: `02-web-api-review-playbook.md`

## Propósito Ejecutivo

Auditoría de seguridad de aplicación web, REST API, GraphQL, o mobile backend.
Cobertura: OWASP Top 10, configuración HTTP, lógica de negocio, integración de third-party.
Entrega: Hallazgos normalizados, prueba de concepto (PoC), remediation guidance.

## Cuándo Usar

✅ Cualquier aplicación web pública  
✅ API REST, GraphQL, gRPC, SOAP  
✅ Mobile backend o serverless  
✅ Multi-tenant SaaS  
✅ Integración de terceros (OAuth, API)  

❌ Si necesitas auditar INFRAESTRUCTURA (→ 01 o 03)  
❌ Si es blockchain (fuera de scope)  

## Estructura del Workflow

### Fase 1: Recon (4-8 horas)
- Mapeo de superficies: endpoints, parámetros, métodos HTTP
- Enumeración: usuario roles, versiones de software
- OSINT: certificados, DNS, API públicas documentadas
- Herramientas: `http_surface_audit.py`, ZAP/Burp passive scan
- Output: API inventory (JSON)

### Fase 2: Validación de Seguridad (2-4 días)
Por cada categoría OWASP:
1. **Authentication**: Bypass, credential stuffing, session fixation
2. **Authorization**: IDOR, privilege escalation, path traversal
3. **Injection**: SQLi, NoSQLi, SSTI, template injection
4. **Weak Crypto**: Hardcoded keys, weak hashing, SSL/TLS issues
5. **Sensitive Data Exposure**: PII in logs, response headers, error messages
6. **XXE / XXSi / SSRF**: External entity, serialization, server-side request forgery
7. **Business Logic**: Rate limiting bypass, price manipulation, workflow abuse
8. **CORS / CSRF**: Cross-origin misconfig, state-changing requests

Herramientas: Burp Suite, ZAP, custom scripts, manual testing  
Documentar: pasos reproducibles, screenshot, impact rating

### Fase 3: Análisis & Deduplicación (1-2 días)
- Agrupar hallazgos similares (ej: múltiples XSS endpoints)
- Priorizar por CVSS + exploit difficulty
- De-duplicate false positives (validar cada uno)
- Normalizar vía `normalize_findings.py`
- Output: `findings.json`

### Fase 4: Reporte & PoC (1-2 días)
- Reporte: hallazgos top-10, impacto, remediation steps
- PoC: vídeo o reproducción paso-a-paso para críticos
- Guidance: qué librerías usar, qué configurar
- Roadmap: 30-90 días (quick wins vs arquitectura)

### Fase 5: Re-validation (Post-remediation, 2-4 semanas después)
- Re-test hallazgos critiales (cliente fixea)
- Validar parches
- Aceptación o rechazo

## Success Criteria

- [ ] Todos los endpoints mapeados
- [ ] Todas las categorías OWASP testeadas
- [ ] Falsos positivos reducidos a < 5%
- [ ] PoCs reproducibles para críticos
- [ ] Reporte: aprobado por cliente
- [ ] Re-test rate: ≥ 90%

## Timeline Realista

| Tipo | Rápido | Normal | Profundo |
|---|---|---|---|
| Landing page + API simple | 4 horas | 8 horas | 16 horas |
| SaaS multi-tenant | 2 días | 4 días | 10 días |
| Microservicios (3+ APIs) | 3 días | 5 días | 15 días |
| Integración compleja (OAuth, etc) | +2 días | +3 días | +5 días |

## Salida Esperada

1. **API Inventory**: `api-inventory.json` (endpoints, métodos, parámetros)
2. **Findings**: `findings.json` (normalizado)
3. **Reporte**: 10-30 páginas
4. **PoCs**: Vídeos o scripts reproducibles
5. **Remediation Guide**: Qué corregir y cómo
6. **Control Checklist**: Web App Security Maturity Model

## Variaciones

### Express Review (4-8 horas)
- Superficies principales nada más
- OWASP Top 3 nada más (Auth, injection, CORS)
- Reporte técnico corto
- Útil para iteraciones rápidas en dev

### Comprehensive (10-15 días)
- Todas las superficies (Web + API + Mobile backend)
- Business logic fuzzing
- API documentation review
- OWASP Top 10 + CWE-25
- Compliance mapping (PCI-DSS 6.5, GDPR security)

## Common Pitfalls & Mitigations

| Pitfall | Mitigación |
|---|---|
| No testeaste "todas" las features | Usar API doc si existe, o enumerar con ZAP |
| Falso positivo en CORS | Validar con curl/python-requests, documentar asunción |
| Cliente dice "es así por diseño" | Preguntar si lo documentaron, de lo contrario: hallazgo |
| Session expires durante test | Automatizar login con script (mirar log_triage.py) |
| Rate limiting bloquea tu scanner | Usar delay, IP rotation, userAgent rotation |
| No acceso a production data | Test en staging; si no hay staging: critical gap |

---

# Playbook 03: Cloud / K8s / IaC Review

**Archivo**: `03-cloud-k8s-review-playbook.md`

## Propósito Ejecutivo

Auditoría de configuración de cloud (AWS/Azure/GCP), Kubernetes, o Infrastructure-as-Code (Terraform, Helm).
Cobertura: IAM, networking, encryption, secrets, RBAC, network policies.
Entrega: Configuración misgaps, hardening guide, risk scoring.

## Cuándo Usar

✅ AWS account, Azure subscription, o GCP project  
✅ Kubernetes cluster (EKS, AKS, GKE, on-prem)  
✅ Terraform / CloudFormation / CDK code review  
✅ Helm charts or deployment manifests  
✅ Container image scanning  

❌ Si es aplicación web (→ 02)  
❌ Si es compliance audit (→ 01, probablemente)  

## Estructura del Workflow

### Fase 1: Inventario (1-2 días)
- Recursos cloud: listar todas las cuentas, regiones, recursos
- IaC: encontrar todos los repos con Terraform, CloudFormation, Helm
- Imágenes: scan de registries (ECR, ACR, GCR) por vulnerabilidades
- Herramientas: AWS/Azure CLI, `helm list`, `terraform plan`, Trivy/Grype
- Output: inventory JSON, image scan report

### Fase 2: Configuración Manual (2-3 días)
**IAM**:
- Root account: ¿tiene access keys? ❌
- Roles: least privilege? ¿hay cruft?
- Policies: wildcard (*) actions? ❌
- MFA: ¿habilitado en todas partes?
- AssumeRole: ¿trust relationships son correctas?

**Networking**:
- Security groups / NSGs: ¿abiertas al mundo (0.0.0.0/0)?
- VPC / subnets: ¿segmentación?
- NAT gateway: ¿configurado para outbound?
- VPN / bastion: ¿cómo accesan usuarios internos?

**Storage**:
- S3 / Blob: ¿público? ¿encryption en reposo?
- Databases: ¿encryption? ¿backups?
- Secrets: ¿en vault o hardcoded? ❌

**Kubernetes**:
- RBAC: ¿restringida?
- Network policies: ¿habilitadas?
- Pod security policy: ¿existe?
- Secrets: ¿cifrados en etcd?
- Admission controller: ¿restricciones de imagen?

Herramientas: manual review + Cloud IAM simulators, `kubectl get`  
Documentar: screenshot de misconfiguration

### Fase 3: Análisis de Código (1-2 días)
Si hay Terraform/CloudFormation/Helm:
- Cheatscan con Checkov, Tfsec, Helm linter
- Code review: patrones inseguros
- Normalizar hallazgos
- Output: `findings.json`

### Fase 4: Risk Scoring & Roadmap (1 día)
- Clasificar por CVSS + exploitability
- Quick wins (1-2 horas): security group changes, secret rotation
- Arquitectura (2-4 semanas): network redesign, RBAC overhaul
- Reporte + roadmap

### Fase 5: Hardening (Post-engagement, 2-4 semanas)
- Cliente implementa fixes
- Re-test: tier 1 (critical) después 30 días
- Validar con automation (Terraform, YAML)

## Success Criteria

- [ ] 100% de recursos inventariados
- [ ] Config validate contra bien-known bad patterns
- [ ] Hallazgos reproducibles (screenshot + pasos)
- [ ] Roadmap: quick wins vs strategic
- [ ] Automation code disponible (Terraform fixes, policies)

## Timeline Realista

| Scope | Rápido | Normal | Profundo |
|---|---|---|---|
| 1 AWS account | 2 días | 3 días | 5 días |
| Multi-cloud (AWS+Azure) | 3 días | 5 días | 10 días |
| Kubernetes cluster + cloud | 2 días | 4 días | 8 días |
| Terraform + deployment (CI/CD) | +1 día | +2 días | +3 días |

## Salida Esperada

1. **Inventory**: `cloud-inventory.json`, `k8s-resources.json`
2. **Findings**: `findings.json` (normalizado)
3. **Hardening Guide**: Terraform/YAML snippets para fixes
4. **Compliance Checklist**: CIS benchmarks (AWS/Azure/GCP)
5. **Roadmap**: 30-90 días con esfuerzo estimado

## Variaciones

### Configuration Audit Only (2-3 días)
- No code review
- Manual configuration validation nada más
- Útil para quick assessment

### Full Stack (1-2 semanas)
- Configuration + code review
- Container image scanning
- Network traffic capture & analysis
- IAM permission reduction (least privilege hardening)
- Compliance mapping (PCI-DSS, HIPAA cloud annexes)

## Common Pitfalls & Mitigations

| Pitfall | Mitigación |
|---|---|
| No acceso a todas las cuentas/suscripciones | Ask before kick-off; documenta limitaciones |
| Roles heredados que nadie conoce | Audit trail: "last accessed X months ago" → remove |
| Terraform distinto de production | Usar `terraform plan` en staging, compare actual state |
| Kubernetes: no acceso a ETCD | Documenta limitation; test RBAC indirectamente |
| Secrets hardcoded en Terraform | Scan con truffleHog o similar, report all |

---

# Playbook 04: Detection & Hunting

**Archivo**: `04-detection-hunting-playbook.md`

## Propósito Ejecutivo

Desarrollo de reglas de detección (Sigma), hunting queries, y mejora de SIEM.
Cobertura: Behavioral analytics, unusual patterns, TTPs (MITRE ATT&CK), IOCs.
Entrega: Sigma rules, SIEM queries, hunting library, runbooks.

## Cuándo Usar

✅ SIEM implementation o mejora  
✅ Threat hunting campaign  
✅ Post-incident: "cómo lo habría detectado?"  
✅ Purple team: validar defensas  
✅ Continuous detection improvement  

❌ Si es respuesta a incidente activo (→ 06; esto es post-análisis)  

## Estructura del Workflow

### Fase 1: Requirements (3-5 días)
- SIEM disponible: acceso a logs, data retention, query language
- Data sources: endpoint logs (Sysmon, EDR), network (Zeek, Suricata), cloud (CloudTrail, audit logs)
- Threat context: qué TTPs son más relevantes? (industria, size)
- Análisis de gap: qué ataques NO se detectan hoy?
- Output: detection roadmap (top-10 TTPs a detectar)

### Fase 2: Hunting Campaign (2-3 semanas)
**Behavioral Baselines**:
- Qué es "normal" para tu organización
- Command-line patterns: qué tools usan legítimamente
- Network: qué destinos son típicos
- Process: qué procesos padres son normales

**Threat Hypothesis Analysis**:
Por cada TTP (MITRE ATT&CK):
- ¿Qué eventos dejaría? (process creation, network connection, file write)
- ¿Qué query los detectaría?
- ¿Qué false positives esperamos?
- Escribe en Sigma format

**Examples**:
- T1136 (Create Account): búsqueda de "net user", "useradd"
- T1018 (Remote System Discovery): "nmap", "ping -a", AD queries
- T1566 (Phishing): attachment types, sender reputation, URL click

Herramientas: Sigma rule format, SIEM query language (KQL, SPL, etc), Jupyter para análisis  
Output: `detection-rules/` directory

### Fase 3: SIEM Implementation (1-2 semanas)
- Importar Sigma rules a tu SIEM
- Tuning: ajustar thresholds, excluir false positive sources
- Testing: trigger cada regla manualmente con data conocida
- Alerting: integración con SOAR, ticketing, escalation (PagerDuty)

Herramientas: SIEM-native rule format, integration APIs  
Output: alert rules deployed

### Fase 4: Hunting Library (1-2 semanas)
Crear queries para búsquedas de amenazas **interactivas** (no solo alerts):
- Lateral movement patterns
- Data exfiltration indicators
- Persistence mechanisms
- Privilege escalation chains

Output: hunting query library (búsquedas en lenguaje SIEM)

### Fase 5: Continuous Improvement (Ongoing)
- Monthly: revisar falsos positivos, desactivar ruido
- Quarterly: análisis de amenazas nuevas, agregar reglas
- Annually: benchmarking contra frameworks (NIST, CIS)

## Success Criteria

- [ ] ≥ 20 Sigma rules escritas
- [ ] Todas sintonizadas (false positive rate < 10%)
- [ ] ≥ 5 hunting queries disponibles
- [ ] Team capacitado en SIEM query language
- [ ] Runbooks para alertas críticas

## Timeline Realista

| Situación | Rápido | Normal | Profundo |
|---|---|---|---|
| Mejorar rules existentes | 1-2 semanas | 2-3 semanas | 4 semanas |
| Nuevas reglas + hunting (desde 0) | 3 semanas | 4-5 semanas | 8 semanas |
| Maturity: Sigma → Korrelator | +1 semana | +2 semanas | +3 semanas |

## Salida Esperada

1. **Sigma Rules**: 20-50 rules en `detection-rules/sigma/`
2. **SIEM Queries**: Tuneadas para tu SIEM específico
3. **Hunting Library**: 10+ interactive queries
4. **Alert Runbooks**: Pasos para responder a cada alert
5. **False Positive Baseline**: log de benign triggers
6. **ATT&CK Mapping**: qué TTPs se detectan, cuáles no

## Variaciones

### Fast Lane (1-2 semanas)
- Solo 10-15 reglas Sigma para TTPs más críticos
- Hunting básica (lateral movement)
- Runbooks mínimos
- Útil para SIEM recién implantado

### Deep Hunting (6-8 semanas)
- 50+ Sigma rules (MITRE ATT&CK: 40+ técnicas)
- Hunting avanzada: timeline analysis, behavioral correlation
- Custom rules + ML
- Tuning exhaustivo
- Purple team exercises para validar

## Common Pitfalls & Mitigations

| Pitfall | Mitigación |
|---|---|
| Demasiados falsos positivos | Whitelist legitimate sources (DC queries, admin commands) |
| Rules lanzan triggers pero nadie responde | Escalation clara, SOC team training, runbooks |
| Sigma rules no se traducen a SIEM | Usar Sigma tooling para validación; test conversion |
| Data retention corta (15 días) | Presupuestar SIEM expansion; hunting retrospectivo limitado |
| No histórico para análisis | Pedir logs archivados (S3, Elasticsearch) para backtest |

---

# Playbook 05: Secure SDLC / Code / Pipeline Review

**Archivo**: `05-secure-sdlc-review-playbook.md`

## Propósito Ejecutivo

Auditoría de seguridad en desarrollo: código, dependencias, secretos, CI/CD, IaC.
Cobertura: SAST (análisis estático), DAST (dinámico), SCA (dependencias), secrets scanning.
Entrega: Hallazgos de código, roadmap de madurez SDLC, fixing guidance.

## Cuándo Usar

✅ Revisión de código base antes de producción  
✅ Pipeline security (GitHub Actions, GitLab CI, Jenkins)  
✅ Terraform / CloudFormation review  
✅ Secrets scanning (API keys, passwords en git)  
✅ Dependency security (supply chain)  

❌ Si solo es web app runtime (→ 02)  
❌ Si es solo cloud config (→ 03)  

## Estructura del Workflow

### Fase 1: Code Inventory (2-3 días)
- Repos: enumerar todos (`git repo-list` o GitLab/GitHub API)
- Lenguajes: Python, Java, Go, Node, C#, etc.
- Frameworks: identificar web frameworks, auth libraries, cryptographic libs
- Dependencies: `pip install -r`, `npm list`, `mvn tree` (cuáles desactualizadas)
- Output: `code-inventory.json`

### Fase 2: Static Analysis (SAST) (3-5 días)
Configurar herramientas:
- **SonarQube** / **Checkmarx**: análisis de bugs y security
- **Semgrep**: custom rules para patterns inseguros de la org
- **Pylint / ESLint**: code quality
- Ejecutar contra todos los repos

Categorías de análisis:
- Injection (SQL, Command, template, SSTI)
- Weak crypto (hardcoded keys, weak hash, predictable RNG)
- Path traversal, XXE, deserialization
- Logic errors: null checks, boundary conditions
- Configuration: hardcoded IPs, ports, credentials

Output: `sast-findings.json`

### Fase 3: Dependency Scanning (SCA) (2-3 días)
Herramientas:
- **Dependabot** / **Snyk**: vulnerability scanning
- **Black Duck** / **WhiteSource**: license compliance
- **Syft**: bill of materials (SBOM) generation

Por repo:
- Identificar dependencias vulnerables
- Versiones desactualizadas
- Licencias restrictivas (GPL en código comercial?)
- Sub-dependencias problemáticas

Output: `sbom.json`, `vulnerable-dependencies.json`

### Fase 4: Secrets Scanning (1-2 días)
Herramientas:
- **TruffleHog** / **GitGuardian**: escanea git history por secrets
- **detect-secrets**: previene commit de datos sensibles
- Custom patterns: API keys, DB passwords, tokens

Scope:
- Todos los repos
- Completo git history (no solo HEAD)
- Documentar hallazgos, notificar de rotación

Output: `secrets-exposed.json`

### Fase 5: Pipeline & IaC Review (2-3 días)
**CI/CD**:
- GitHub Actions / GitLab CI / Jenkins pipeline review
- ¿Approvals antes de deploy?
- ¿Tests están gateados?
- ¿Secrets seguros (no en logs)?
- ¿Artifacts firmados?

**IaC** (si aplicable):
- Terraform / CloudFormation review
- Hardcoded valores? Least privilege IAM?
- Encryption habilitada?
- Herramientas: Checkov, Tfsec

Output: `pipeline-findings.json`, `iac-findings.json`

### Fase 6: Code Review Profundo (3-5 días)
Sampler approach:
- Top 5 "riskiest" modules (authentication, crypto, payments)
- Manual pair-review: 50-100 líneas por modulo
- Buscar lógica insegura, edge cases, race conditions

Output: `code-review-findings.json`

### Fase 7: Roadmap & Fix Plan (1-2 días)
- Priorizar: críticos fijos hoy, altos en 30 días, medios en 90
- Training: dar ejemplos de código inseguro vs seguro
- Governance: qué gates adicionales en pipeline?

Output: SDLC improvement roadmap

## Success Criteria

- [ ] Todos los repos escaneados
- [ ] SAST + SCA + secrets scanning ejecutados
- [ ] Hallazgos de criticos = 0
- [ ] Roadmap aprobado por team lead
- [ ] Team capacitado en gating SDLC improvements

## Timeline Realista

| Scope | Rápido | Normal | Profundo |
|---|---|---|---|
| 1 repo, 20k LOC | 2-3 días | 5 días | 10 días |
| Monorepo, 100k+ LOC | 3-5 días | 7 días | 14 días |
| Multi-repo (5+), orquestación | 1-2 semanas | 2-3 semanas | 4 semanas |

## Salida Esperada

1. **SAST Findings**: `sast-findings.json`, top hallazgos con PoC
2. **SCA Report**: Vulnerabilidades, actualización disponible
3. **Secrets Report**: Qué secrets se encontraron, remediation
4. **Pipeline Review**: Qué gates faltan, qué mejorar
5. **Code Review Findings**: Manual review de módulos riskosos
6. **Roadmap**: 30-90-180 días, effort & owner
7. **Training**: Ejemplos de código inseguro/seguro

## Variaciones

### Express Review (3-5 días)
- Solo SAST + SCA, sin manual code review
- Pipeline basics nada más
- Útil para iteraciones rápidas

### Compliance-Heavy (2-3 semanas)
- Código + SCA + secrets + IaC + licencias
- Manual deep-dive (20+ horas)
- PCI-DSS 6.5 mapping
- SOX / GDPR security mappings

## Common Pitfalls & Mitigations

| Pitfall | Mitigación |
|---|---|
| SAST tool genera 1000+ falsos positivos | Custom tuning, deshabilitar reglas ruidosas |
| Dependencia vulnerable sin fix disponible | Documenta mitigación (ej: feature no usado) |
| Secrets expuestos en history | TruffleHog confirms; rotate secrets, force pushes not allowed |
| Pipeline gates demasiado estrictos | Balance: security vs velocity (no 1 hora per commit) |
| Team resiste cambios SDLC | Celebra quick wins, muestra ROI, training |

---

# Playbook 06: Incident Triage & DFIR

**Archivo**: `06-incident-triage-playbook.md`

## Propósito Ejecutivo

Respuesta rápida a incidente de seguridad activo.
Cobertura: Contención, análisis forense, timeline de evento, IOCs, plan de remediation.
Entrega: Reporte de incidente, evidence chain, remediation plan, lessons learned.

**IMPORTANTE**: Este playbook es TIEMPO-SENSIBLE. Las primeras 4 horas son críticas.

## Cuándo Usar

✅ **BREACH ACTIVO**: datos sendo copied, attack en progreso  
✅ **ANOMALÍA SOSPECHOSA**: login inusual, process anormal, outbound conexión rara  
✅ **MALWARE DETECTED**: EDR alerta, usuario reporta comportamiento anormal  
✅ **DATA EXFILTRATION**: empleado reporta archivos faltando, logs de outbound sospechoso  

❌ Este playbook NO es para threat hunting (→ 04)  
❌ NO para testing de defensas (→ purple team en 01)  

## Estructura del Workflow

### Fase 0: Activación (Primeros 15 minutos)
- **DETENER PROPAGACIÓN**: aísla la máquina (disconnect red, power off si necesario)
- **PRESERVAR EVIDENCIA**: NO reinicies, NO escribas a disco duro
- **ESCALADA**: CTO/CISO → legal → insurance → law enforcement (si aplica)
- **LOGGING**: Todos los pasos documentados con timestamp
- **EQUIPO**: Forense, networking, red team por quién es responsable

### Fase 1: Triage Rápido (30 minutos - 2 horas)

**Scope Assessment**:
- ¿Solo 1 maquina o múltiples?
- ¿Qué data está en riesgo? (PII, trade secrets, customer data)
- ¿Attacker aún activo?

**Contención Inicial**:
- Aislar red: cambiar vlan, kill network connections
- Credenciales: forzar cambio de contraseña para affected users
- Acceso: revoke tokens, certificates si fueron comprometidas

**Evidence Preservation**:
- Memory dump (si aún activo)
- Network capture (misspaced en firewall)
- Snapshots de filesystem
- Cloud audit logs
- Backup de logs

### Fase 2: Análisis Forense (4-24 horas)

**Timeline Reconstruction**:
- Combina datos de múltiples sources: logs de sistema, aplicación, firewall, EDR
- "What happened first?": ataque inicial? (phishing, exploit, credential)
- Secuencia: "User A logged in → Process X started → Outbound connection Y"
- Usar `log_triage.py` para parsing y timeline

**Artifact Analysis**:
- Memory: volatility, carving
- Disk: carving, file system analysis (deleted files, hidden data)
- Network: packet analysis (Wireshark, Zeek)
- Malware: static (strings, hash) + dynamic (sandbox) si aplica

**Indicator Extraction**:
- IOCs: IPs, domains, file hashes, C2 infrastructure
- TTPs: qué atacante technique usó (MITRE ATT&CK mapping)
- Tools: qué malware, scripts, tools
- Output: `iocs.json`, `incident-report.json`

### Fase 3: Impact Assessment (2-6 horas)

**Data Breach Scope**:
- Qué datos fueron accessed/exfiltrated?
- Cuántos records? (for notification obligations)
- PII/PHI? (GDPR, HIPAA obligations)

**Business Impact**:
- Servicios down? Duración?
- Reputación: fue público el incident?
- Financial: recovery cost, downtime, regulatory fines

**Compliance Triggers**:
- GDPR: notificar supervisory authority en 72h
- HIPAA: notificar pacientes en 60 días
- SOX: disclosure si pública company

Output: impact statement, notification checklist

### Fase 4: Remediation Plan (12-48 horas)

**Immediate** (4 horas):
- Patch explotados vulnerabilities
- Cambiar credentials comprometidas
- Bloquear IOCs en firewall, EDR, SIEM

**Short-term** (1-2 semanas):
- Validar no hay persistencia adicional
- Re-imagen maquinas afectadas
- Restore desde backup pre-compromise
- Upgrade firewalls, EDR, SIEM

**Long-term** (2-12 semanas):
- Post-incident improvements: qué falló en defensa?
- Implementar detections para TTPs específicas
- Training del team
- Policy updates (incident response, password policy, etc)

Output: remediation plan, effort estimates

### Fase 5: Post-Incident (2-4 semanas después)

**Lessons Learned**:
- Root cause analysis: ¿por qué fue vulnerable?
- Detection gap: ¿qué alerta debería haber disparado?
- Response gap: ¿qué tardó demasiado?

**Re-testing**:
- Validar remediation fixes
- Red team ejercicio: "¿puedo entrar de nuevo de la misma forma?"

**Communication**:
- Incident statistics: duración, impacto, cost
- Customer/user communication (si fue breach)
- Media statement (si fue grande)

## Success Criteria

- [ ] Threat contenida en < 4 horas
- [ ] Timeline entendida en < 24 horas
- [ ] IOCs extraídos y bloqueados en < 6 horas
- [ ] Impact assessment en < 24 horas
- [ ] Remediation plan aprobado por CISO en < 48 horas
- [ ] Evidence preservada y incluida en reporte
- [ ] Lessons learned documentadas

## Timeline Realista

| Tipo | Triage | Analysis | Remediation |
|---|---|---|---|
| Credential stuffing (no breach) | 1 hora | 4 horas | 8 horas |
| Malware en 1 máquina | 2 horas | 8 horas | 24 horas |
| APT: múltiples máquinas | 4 horas | 48-72 horas | 2-4 semanas |
| Supply chain / ransomware | 6+ horas | 1-2 semanas | 4+ semanas |

## Salida Esperada

1. **Incident Report**: Qué pasó, cuándo, quién, impacto
2. **Forensic Report**: Timeline, artifacts, analysis
3. **IOC List**: IPs, domains, hashes → TIP para futuro
4. **Impact Statement**: Data scope, business impact
5. **Remediation Plan**: Immediate/short/long-term fixes
6. **Lessons Learned**: Root causes, gap analysis
7. **All Evidence**: Disk images, memory dumps, network captures (encrypted archive)

## Variaciones

### False Positive (4-8 horas)
- Rápida determinación: no es breach
- Documentation: qué lancé la falsa alerta
- No fue serious, pero documentar para futuro

### Ransomware / Major Incident (2-4 weeks)
- Escalation a ley enforcement, insurance
- Negotiation con attacker (si applicable)
- Decryption analysis
- Large-scale remediotion + rebuild
- Compliance notifications (GDPR, etc)

## Common Pitfalls & Mitigations

| Pitfall | Mitigación |
|---|---|
| Reiniciar máquina (destruyendo evidencia) | Power off in lugar; preserva memory primero |
| No escalation rápida | Pre-incident: define escalation path, contacts |
| Evidence no documentada (chain of custody) | Fotografía, timestamp, hash cada artefacto |
| Timeline incompleto | Correlate múltiples sources; llenar gaps con asunción |
| Remediation antes de análisis | Forensic primero, remediate después |
| Team burnout | Rotate staff, 24h shifts, mental health check |

---

## Resumen: Cuándo Usar Cada Playbook

| Situación | Playbook | Duración |
|---|---|---|
| "Audítame todo" | 01 | 2-4 semanas |
| "Validá mi app web" | 02 | 4 horas - 10 días |
| "Audítame cloud/K8s" | 03 | 2-5 días |
| "Necesito detecciones" | 04 | 1-8 semanas |
| "Validá mi código y pipeline" | 05 | 3-21 días |
| "TENEMOS INCIDENTE" | 06 | 4 horas - 4 semanas |

**Regla de oro**: Si no sabes cuál usar, empieza con **Playbook 01** (authorized assessment).
Es el más general; los otros 5 son "sub-workflows" más especializados.
