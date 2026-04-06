# ORION-HACKING Module Map - Inventario Navegable Completo

## Propósito

Este documento es una **guía interactiva** para navegar todos los módulos de ORION. Cada módulo es independiente
pero se conecta con otros vía referencias cruzadas. Use esto cuando:
- No sepa por dónde empezar
- Necesite una visión de 30,000 pies
- Busque un módulo específico por tema

---

## Nivel 0: Metadocumentación (Comence aquí)

Estos archivos **no contienen técnica** sino que te **orientan** a dónde ir.

| Archivo | Propósito | Cuándo Leer |
|---|---|---|
| `README.md` | Punto de entrada del proyecto | Primera vez |
| `SKILL.md` | Guardrails, principios, modos operativos | Siempre, antes de empezar |
| `ARCHITECTURE.md` | Cómo se estructura el sistema (5 capas) | Entender visión general |
| `DOMAIN_TAXONOMY.md` | Cómo clasificar solicitudes | Cuando llegue tarea ambigua |
| `MODULE_MAP.md` | Este archivo (navegación de módulos) | Buscar módulo específico |
| `PLAYBOOK_INDEX.md` | Índice de workflows concretos | Cuando identifies "es un X" |

---

## Nivel 1a: Governance y Contexto (¿Tengo autorización?)

Estos módulos establecen el **marco legal, de riesgo y control**.

### `references/01-authorization-and-governance.md`
**Temas**:
- Autorización explícita (escrita, no verbal)
- Términos de referencia (ToR)
- Scope definition (what/where/when)
- Risk allocation (quién asume qué riesgo)
- Evidence and audit trail required
- Stakeholder identification

**Cargar si**: Cualquier engagement corporativo, compliance, o tarea grande.
**Combina con**: Playbook 01-authorized-assessment.md

### `references/02-engagement-workflow.md`
**Temas**:
- Pre-engagement: kick-off, tools testing, baseline
- During: daily syncs, escalation procedures
- Post-engagement: remediation tracking, re-testing, closure
- Staffing and responsibilities
- Communication protocols

**Cargar si**: Ejecutando un assessment formal de 2+ semanas.
**Combina con**: Cualquier playbook; es orthogonal a la técnica.

---

## Nivel 1b: Gobernanza Avanzada (GRC / Madurez)

### `references/25-grc-risk-and-maturity.md`
**Temas**:
- Risk frameworks (NIST, ISO, CIS)
- Maturity models (CMMC, IMMI, others)
- Compliance mappings (PCI-DSS, HIPAA, GDPR, SOC2)
- Gap analysis
- Remediation roadmaps
- Vendor risk assessment

**Cargar si**: Cliente pregunta "¿somos SEC level 3?" o "¿cumplimos HIPAA?"
**Combina con**: Playbook 01, referencias técnicas relevantes.

---

## Nivel 2: Descarga y Asset Intelligence (¿Qué hay?)

Estos módulos te dicen **qué existe, de dónde viene, qué riesgos trae**.

### `references/05-osint-and-asset-intelligence.md`
**Temas**:
- Passive reconnaissance (whatsmydns, shodan,  certificate transparency)
- Active discovery (nmap, subnet enumeration, service probing)
- Asset tagging and inventory
- Exposed secrets (git repos, pastebin, other leaks)
- Supply chain discovery (dependencies, 3rd party SaaS)
- Threat intelligence feeds and IOCs

**Cargar si**: Necesitas identificar "qué existe" antes de validar.
**Combina con**: Cualquier assessment; es foundational.

### `references/28-tool-selection-matrix.md`
**Temas**:
- Herramientas recomendadas por tarea
- Comparativa: Burp vs ZAP, Nmap vs Shodan, etc.
- Agnositismo: no se favorece tool
- Setup y validación
- Output formats (JSON, CSV, XML)
- Integration con SIEM/reporting

**Cargar si**: "¿Cuál herramienta debería usar?"
**No combina con nada; es referencia transversal.**

---

## Nivel 3: Assessment Técnico (¿Está bien hecho?)

### Nivel 3A: Web / API / AppSec

### `references/06-web-api-appsec.md`
**Temas**:
- Authentication & session management
- Authorization and access control
- Input validation & injection (SQLi, XSS, XXE, SSTI)
- Output encoding
- CORS, CSRF, SSRF
- Business logic flaws
- Error handling & info disclosure
- Crypto & hash functions
- API-specific (REST, GraphQL, gRPC)
- Mobile backends
- Third-party integrations

**Cargar si**: Validando aplicación web, API, cualquier cosa HTTP.
**Combina con**: Playbook 02 (web-api-review), scripts (http_surface_audit.py).

### `references/07-vulnerability-management.md`
**Temas**:
- CVSS scoring (v3.1)
- CWE categories
- Prioritization matrix
- Nessus/Qualys output parsing
- Patch management
- Vulnerability tracking (Jira, Azure DevOps)
- SLA targets (critical/high/medium/low)

**Cargar si**: Triageando un montón de vulnerabilidades, necesitas priorizar.
**Combina con**: normalize_findings.py, Playbook 01.

---

### Nivel 3B: Cloud / Container / Kubernetes

### `references/08-cloud-container-k8s.md`
**Temas**:
- AWS: IAM, S3, EC2, Lambda, RDS, ECS, VPC
- Azure: Entra ID, Storage, VMs, Functions, AKS
- GCP: Cloud IAM, GCS, Compute, BigQuery, GKE
- Kubernetes: RBAC, network policies, admission control, secrets, ETCD
- Container security: image scanning, layer analysis, runtime
- Serverless: function security, cold start, side-channel
- IaC security: Terraform, CloudFormation, Helm

**Cargar si**: Auditando infraestructura cloud (cualquier proveedor).
**Combina con**: Playbook 03 (cloud-k8s-review), references/13 (IaC).

---

### Nivel 3C: Identity / Access / Directory

### `references/09-identity-endpoint-ad.md`
**Temas**:
- Active Directory: domain join, Group Policy, Kerberos
- LDAP: schema, bind, search, injection
- IAM: roles, policies, service accounts
- PAM: privilege escalation, secret management, logging
- MFA: TOTP, FIDO2, push auth, risk-based
- SSO: SAML, OAuth 2.0, OIDC
- Federation: trust models, attribute passing
- Endpoint hardening: OS baselines, EDR, AppLocker

**Cargar si**: Auditando identidad, acceso, o hardening de máquinas.
**Combina con**: Hardening playbooks, Playbook 01.

---

### Nivel 3D: Network Security

### `references/04-network-security.md`
**Temas**:
- Network segmentation: VLANs, subnets, micro-segmentation
- Firewalls: rules, logs, false-positive reduction
- IDS/IPS: signatures, tuning, performance
- VPN: protocols (IPSec, WireGuard, OpenVPN), configuration
- DNS security: zone transfers, amplification, poisoning
- DDoS mitigation: rate limiting, geo-blocking
- Wireless: WPA2/WPA3, 802.1X, rogue detection
- Remote access: VPN, bastion, jump hosts, session recording

**Cargar si**: Auditando perimetro, segmentación, o wireless.
**Combina con**: Playbook 01, references/04.

### `references/10-wireless-remote-access.md`
**Temas**:
- WiFi security: WPA2/WPA3, Pre-Shared Key, Enterprise
- Rogue AP detection
- Packet capture and analysis
- VPN protocols: IPSec, TLS-VPN, WireGuard
- Jump hosts and bastion configurations
- Session recording and audit
- Acceptable use policies

**Cargar si**: Wireless or remote access audit.
**Combina con**: Playbook 01, referencias de governance.

---

### Nivel 3E: Mobile & Client

### `references/17-mobile-client-security.md`
**Temas**:
- iOS: codesigning, entitlements, sandboxing, jailbreak detection
- Android: permissions, signing, rooting, SELinux
- MDM: mobile device management, policy enforcement
- App store review: compliance, malware scanning
- Client-side security: XSS in WebView, insecure storage
- Update mechanisms: patch deployment, rollback

**Cargar si**: Auditando aplicación móvil o programa MDM.
**Combina con**: Playbook 01, referencias de AppSec.

---

### Nivel 3F: Data & Privacy

### `references/19-data-security-and-privacy.md`
**Temas**:
- Encryption: at-rest, in-transit, key management
- Data classification
- GDPR, CCPA, LGPD compliance
- PII/PHI protection
- Data retention policies
- Anonymization techniques
- Breaches: notification, remediation
- DLP: data loss prevention tools

**Cargar si**: Cliente maneja datos sensibles o requiere compliance.
**Combina con**: All playbooks si hay datos involucrados.

### `references/18-crypto-key-management.md`
**Temas**:
- Symmetric encryption (AES)
- Asymmetric encryption (RSA, ECC)
- Hashing (SHA-2, SHA-3)
- Key generation, storage, rotation
- PKI: certificates, CAs, trust models
- Hardware security modules (HSM)
- Key derivation functions (PBKDF2, Argon2)

**Cargar si**: Auditando criptografía (no solo "uses SSL").
**Combina con**: referencias de secrets, cloud, data.

---

## Nivel 4: Secure Engineering (¿Cómo se construye?)

### `references/13-secure-engineering-sdlc.md`
**Temas**:
- Threat modeling: STRIDE, PASTA, attack trees
- Secure design principles: least privilege, defense in depth, fail-safe
- SAST tools: SonarQube, Checkmarx, Semgrep
- DAST tools: OWASP ZAP, Burp
- Code review checklists
- Testing: unit, integration, security testing
- Dependency management: SCA, supply chain
- Secrets management: rotation, vault integration
- Pipeline security: approvals, scanning gates

**Cargar si**: Auditando código, pipeline, o SDLC.
**Combina con**: Playbook 05 (secure-sdlc-review), references/20 (secrets).

### `references/20-secrets-and-supply-chain.md`
**Temas**:
- Secret types: API keys, passwords, tokens, certificates
- Secret storage: vault, environment variables, managed services
- Secret rotation: policies, automation
- Credential leakage scanning: git, Docker registries, cloud
- Dependency scanning: software composition analysis (SCA)
- SBOM: software bill of materials
- Artifact signing: Cosign, Notary
- Third-party risk: vendor assessment
- Open source licensing: GPL, MIT, copyleft compliance

**Cargar si**: Asegurando código, o auditando supplychain.
**Combina con**: Playbook 05, references/13.

### `references/16-architecture-threat-modeling.md`
**Temas**:
- Threat models: STRIDE, PASTA, LINDDUN
- Attack trees and risk matrices
- Asset identification
- Threat identification (MITRE ATT&CK mapping)
- Mitigation strategies
- Control baselines
- Risk quantification
- Scenario analysis

**Cargar si**: Diseño seguro o risk-based assessment.
**Combina con**: Playbook 01, todas las referencias técnicas según amenazas.

---

## Nivel 5: Defensa y Operaciones (¿Cómo defendemos?)

### Nivel 5A: Detection / SIEM / Hunting

### `references/12-detection-engineering.md`
**Temas**:
- Sigma rule format and lifecycle
- SIEM rule tuning
- Behavioral analytics
- Alert fatigue and false-positive reduction
- Threat hunting methodologies
- IOC and indicator management
- Telemetry requirements (logs, events, flows)
- Detection maturity (CMatcher/CMM)

**Cargar si**: Diseñando o validando reglas de detección.
**Combina con**: Playbook 04 (detection-hunting), referencias/21 (SOC).

### `references/11-dfir-threat-hunting.md`
**Temas**:
- Forensic readiness
- Live forensics: memory, network, process
- Post-mortem analysis: disk images, timeline
- Log analysis and correlation
- Incident response workflow
- Evidence preservation (chain of custody)
- Malware analysis: static, dynamic, behavior
- Threat intelligence: IOCs, signatures
- Hunting playbooks: lateral movement, persistence, data exfil

**Cargar si**: Incidente real, evidencia forense, o threat hunting.
**Combina con**: Playbook 06 (incident-triage), referencias de detection.

### `references/21-soc-operations-use-cases.md`
**Temas**:
- Typical SOC workflows
- Alert triage procedures
- Escalation policies
- Runbooks for common scenarios
- Tool integrations (SIEM, SOAR, ticketing)
- Metrics and KPIs
- Training and certifications
- Shift scheduling and coverage

**Cargar si**: Cliente está buildendo o mejorando SOC.
**Combina con**: Playbook 01, referencias de detection/hunting.

### `references/22-purple-teaming.md`
**Temas**:
- Purple team methodology
- Red team (attack) vs Blue team (defense)
- Collaborative exercises
- Simulation scenarios
- Feedback loops
- Metrics for exercises
- Tool recommentations
- Roadmap planning

**Cargar si**: Cliente quiere tests realistas de defensas.
**Combina con**: Playbook 01, referencias técnicas por dominio.

---

### Nivel 5B: Hardening & Baselines

Hardening se cubre en referencias **técnicas por dominio** (9, 17, etc.) y en:

### `references/29-remediation-patterns.md`
**Temas**:
- Common remediation patterns
- Patch management
- Configuration change procedures
- Approval workflows
- Change impact assessment
- Rollback procedures
- Testing before production deployment
- Documentation and audit trails

**Cargar si**: Cliente implementando fixes.
**Combina con**: Todos los playbooks, en post-remediation fase.

---

## Nivel 6: Agentic / Automation

### `references/03-ai-code-execution.md`
**Temas**:
- Safe code generation patterns
- Timeout and resource limits
- Logging and auditability
- Reversibility (no mutation)
- Credential handling (env vars, never hardcoded)
- Error handling and fallbacks
- Testing and validation
- Examples: log parser, config checker, normalizer

**Cargar si**: Necesitas generar código o script.
**Combina con**: scripts/ folder, Playbook 01 (agentic capability).

### `references/24-ai-agent-operating-profiles.md`
**Temas**:
- Agent personas: aggressive vs conservative
- Risk tolerance settings
- Tool restrictions
- Output constraints
- Escalation triggers
- Learning and feedback loops
- Benchmark of capabilities

**Cargar si**: Configurando agente con restricciones específicas.
**Combina con**: SKILL.md (modos operativos).

### `references/31-agent-safety-checklists.md`
**Temas**:
- Pre-execution safety checks
- Credential protection
- Resource limits verification
- Logging enablement
- Rollback planning
- Post-execution validation
- Incident procedures if agent misbehaves

**Cargar si**: Cualquier ejecución de agente o script.
**Combina con**: references/03-ai-code-execution.md

---

## Nivel 7: Reporting y Evidencia

### `references/14-reporting-remediation.md`
**Temas**:
- Report structure: executive, technical, appendix
- Severity classification
- Remediation recommendations
- Timeline suggestions (30-90-180 days)
- Risk quantification
- ROI justification for fixes
- Compliance mapping
- Post-engagement support

**Cargar si**: Escribiendo reporte o presentando hallazgos.
**Combina con**: report_skeleton.py, cualquier playbook.

### `references/27-evidence-and-logging-spec.md`
**Temas**:
- Evidence types: screenshots, logs, network captures
- Reproducibility: step-by-step documentation
- Chain of custody
- Logging requirements
- Data protection for evidence
- Retention policies
- Legal considerations
- Artifact preservation

**Cargar si**: Documentando hallazgo o preservando evidencia.
**Combina con**: referencias técnicas específicas.

### `references/30-report-templates.md`
**Temas**:
- Executive summary template
- Technical findings template
- Roadmap template
- Metrics dashboard template
- Email templates
- Slide deck outline
- Vendor report templates

**Cargar si**: Estructurando conclusiones.
**Combina con**: report_skeleton.py.

---

## Nivel 8: Learning & Labs

### `references/15-labs-learning.md`
**Temas**:
- Lab environments setup (AWS, Azure, GCP, on-prem)
- HackTheBox, TryHackMe, exploitation labs
- Vulnerable applications (WebGoat, DVWA, bWapp)
- Capture-the-flag (CTF) exercises
- Purple team exercises
- Sandbox configurations
- Training roadmaps
- Certifications (OSCP, CEH, GPEN, etc.)

**Cargar si**: Entrenamiento del equipo o validación segura.
**Combina con**: Playbook 01 (labs capability), referencias técnicas.

---

## Nivel 9: Extended Taxonomy

### `references/32-domain-taxonomy-extended.md`
**Temas**:
- Detailed breakdowns of each domain
- Sub-classifications (ej: K8s → auth, network, secrets, compute)
- Tools mapped to domain
- MITRE ATT&CK mappings
- CWE mappings
- Frameworks per domain
- Common misconfigurations per technology

**Cargar si**: Necesitas profundidad en un dominio.
**Combina con**: referencias técnicas específicas, DOMAIN_TAXONOMY.md.

---

## Playbooks (Metodología Operativa)

### `playbooks/00-playbook-index.md`
Lista y descripción de todos los playbooks. Lee primero si no sabes cuál elegir.

### `playbooks/01-authorized-assessment-playbook.md`
**Cuándo**: Assessment general, multi-domain, bien scoped
**Tiempo**: 2-4 semanas
**Salida**: Reporte ejecutivo + técnico, roadmap
**Cargas referencias**: Todas las relevantes
**Cargas scripts**: Normalized output, reporting

### `playbooks/02-web-api-review-playbook.md`
**Cuándo**: Web app, REST API, GraphQL, mobile backend
**Tiempo**: 4-8 horas (rápido) o 5-10 días (profundo)
**Salida**: Hallazgos web normalizados, roadmap
**Requiere**: references/06-web-api-appsec.md, scripts/http_surface_audit.py

### `playbooks/03-cloud-k8s-review-playbook.md`
**Cuándo**: Cloud account, Kubernetes cluster, IaC
**Tiempo**: 3-5 días
**Salida**: Config gaps, hardening guide
**Requiere**: references/08-cloud-container-k8s.md, references/13-sdlc.md

### `playbooks/04-detection-hunting-playbook.md`
**Cuándo**: SIEM rule development, threat hunting campaign
**Tiempo**: Ongoing (continuous)
**Salida**: Sigma rules, detections, hunting query library
**Requiere**: references/12-detection.md, references/11-dfir.md

### `playbooks/05-secure-sdlc-review-playbook.md`
**Cuándo**: Code,  pipeline, IaC, secret management
**Tiempo**: 2-3 semanas
**Salida**: Gap report, remediation script library
**Requiere**: references/13-sdlc.md, references/20-secrets.md

### `playbooks/06-incident-triage-playbook.md`
**Cuándo**: Active breach, anomalous activity
**Tiempo**: Hours to 1-2 days
**Salida**: Timeline, IOCs, containment plan, forensic report
**Requiere**: references/11-dfir.md, references/12-detection.md

---

## Scripts (Automatización auditable)

### Pre-Assessment
- `orion/scripts/install-safe-tooling.sh / .ps1` - Setup de herramientas recomendadas

### During Assessment
- `orion/scripts/check_integrity.py` - Valida documentó
- `orion/scripts/http_surface_audit.py` - Auditoría HTTP headers
- `orion/scripts/log_triage.py` - Parsea eventos de log

### Post-Assessment
- `orion/scripts/normalize_findings.py` - Convierte Burp/ZAP → JSON estándar
- `orion/scripts/report_skeleton.py` - Genera plantilla de reporte

### Validation
- `orion/scripts/run_skill_sanity.py` - Valida integridad de ORION mismo
- `orion/scripts/build_singlefile_site.py` - Construye ORION-HACKING-singlefile.html

---

## Cómo Navegar por Casos Reales

### Caso 1: "Auditame mi app web"
```
1. SKILL.md → Verificar autorización
2. DOMAIN_TAXONOMY.md → Clasifica como Web/AppSec
3. Referencias:
   - 06-web-api-appsec.md (técnica)
   - 14-reporting-remediation.md (salida)
4. Playbook: 02-web-api-review-playbook.md
5. Scripts:
   - http_surface_audit.py
   - (custom parser para Burp findings)
   - normalize_findings.py
   - report_skeleton.py
6. Reporte final
```

### Caso 2: "¿Cómo detecto intrusiones?"
```
1. SKILL.md → Verificar contexto (es defensa, no ataque)
2. DOMAIN_TAXONOMY.md → Detection/Hunting/SOC
3. Referencias:
   - 12-detection-engineering.md
   - 11-dfir-threat-hunting.md
   - 21-soc-operations-use-cases.md
4. Playbook: 04-detection-hunting-playbook.md
5. Scripts:
   - log_triage.py (análisis de logs)
   - (custom Sigma rule generator)
6. Deliverables: reglas, queries, hunting library
```

### Caso 3: "Incidente de seguridad"
```
1. SKILL.md → Activate Incident Response mode
2. References:
   - 11-dfir-threat-hunting.md (prioritario)
   - 27-evidence-and-logging-spec.md
3. Playbook: 06-incident-triage-playbook.md
4. Scripts:
   - log_triage.py
   - (custom memor dump analyzer, si aplica)
5. Output: Timeline, IOCs, remediation
```

---

## Resumen: Estructura de Navegación

```
USUARIO llega con solicitud
        ↓
SKILL.md (¿Es legal? ¿Es ético? ¿Qué modo?)
        ↓
DOMAIN_TAXONOMY.md (¿Qué tipo de solicitud es?)
        ↓
MODULE_MAP.md (¿Qué módulos existen?)
        ↓
Referencias (¿Qué debo saber técnicamente?)
Playbooks (¿Cuál es el workflow?)
Scripts (¿Qué puedo automatizar?)
        ↓
REPORTE + FOLLOWUP
```

No necesitas cargar todo. Este map es para **orientación**, no para que lo uses entero.

**Regla de oro**: Si no sabes dónde ir, empieza con SKILL.md + DOMAIN_TAXONOMY.md.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion del mapa modular 2026

### Nuevas rutas

### Ruta extendida 01
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 02
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 03
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 04
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 05
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 06
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 07
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 08
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 09
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 10
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 11
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 12
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 13
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 14
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 15
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 16
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 17
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 18
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 19
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 20
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 21
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 22
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 23
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 24
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 25
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 26
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 27
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 28
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 29
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 30
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 31
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 32
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 33
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 34
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 35
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 36
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

### Ruta extendida 37
- Entrada: solicitud ambigua, finding puntual o incidente en curso.
- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.
- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.
- Salida objetivo: decision defendible y siguiente accion concreta.

