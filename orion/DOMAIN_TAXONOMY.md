# ORION-HACKING Domain Taxonomy - Clasificador Avanzado de Solicitudes

## Propósito

Este documento define una **taxonomía exhaustiva** para clasificar, enrutar y priorizar cualquier solicitud de seguridad.
Es una matriz de decisión que responde a: "¿Qué tipo de tarea es esta? ¿Qué modulos necesito cargar? ¿Cuál es el playbook?"

---

## 5 Ejes Principales de Clasificación

### 1. EJE GOVERNANCE (Contexto empresarial, riesgo, control)

Determina el **CÓMO** de la tarea: bajo qué control, autorización, evidencia.

#### 1.1 Autorización
- `explicit`: Autorización escrita, alcance definido
- `implicit`: El usuario asume que está autorizado (requiere validación)
- `none`: Sin autorización (rechazar)

#### 1.2 Alcance
- `internal`: Solo sist emas internos, datos internos
- `external`: APIs públicas, terceros con permiso
- `mixed`: Interno + externo

#### 1.3 Riesgo  Aceptable
- `low-risk`: Validaciones sin modificación, tests no destructivos
- `medium-risk`: Cambios reversibles, downtime planificado
- `high-risk`: Cambios estructurales, potencial impacto severo

#### 1.4 Evidencia Requerida
- `none`: Conocimiento suficiente
- `light`: Screenshots, logs
- `medium`: Pasos exactos, reproducción documentada
- `forensic`: Cadena de custodia, timeline, artefactos forenses

#### 1.5 Madurez del Cliente
- `startup`: Recursos limitados, baja madurez
- `mid-market`: Procesos formalizados
- `enterprise`: SOC, auditoría, compliance complejo

---

### 2. EJE SUPERFICIE TÉCNICA (¿Qué sistemas tocamos?)

Define el **DOMINIO TÉCNICO PRIMARIO**.

#### 2.1 Red y Perímetro
- `perimeter`: Firewalls, routers, switches
- `network-segment`: VLAN, micro-segmentación
- `network-monitoring`: IDS/IPS, NETFLOW, packet inspection
- `wireless`: WiFi, signal scanning, rogue detection
- `remote-access`: VPN, RDP, jump hosts, bastion

#### 2.2 Web y APIs
- `web-apps`: Aplicaciones HTTP/HTTPS tradicionales
- `restful-api`: APIs REST con OAuth/JWT
- `graphql`: APIs GraphQL específicas
- `soap-xml`: SOAP, XML-RPC, legacy services
- `mobile-backend`: APIs for native mobile
- `webhook-event-driven`: Webhooks, event processing

#### 2.3 Cloud y Contenedores
- `aws-account`: AWS resources, IAM, S3, EC2, Lambda, RDS, etc.
- `azure-tenant`: Azure subscription, Entra ID, Azure Storage, VMs
- `gcp-project`: GCP project, Cloud Identity, GCS, Compute Engine
- `kubernetes`: K8s clusters, RBAC, network policies, admission control
- `serverless`: Lambda, Functions,  Step Functions, orchestration
- `infrastructure-as-code`: Terraform, CloudFormation, Ansible, Helm

#### 2.4 Identidad y Acceso
- `directory-services`: Active Directory, LDAP, FreeIPA
- `identity-provider`: Okta, Azure AD, Ping Identity, KeyCloak
- `pam-system`: Privilege Access Management, secret vaults
- `mfa-otherauth`: MFA, FIDO2, TOTP, SmartCards
- `iam-policy`: IAM policies, roles, permission boundaries
- `sso-federation`: SAML, OAuth 2.0, OIDC, federation

#### 2.5 Endpoint y Recursos
- `workstation`: Desktops, laptops, Windows/Mac/Linux
- `server`: Operating systems, hardening, configs
- `mobile-device`: Phones, tablets, MDM
- `iot-embedded`: IoT, industrial, firmware
- `pci-dss-hardware`: Point-of-sale, payment terminals

#### 2.6 Data y Almacenamiento
- `database-sql`: SQL Server, PostgreSQL, MySQL, Oracle
- `database-nosql`: MongoDB, Elasticsearch, Redis, Dynamodb
- `object-storage`: S3, Azure Blob, GCS buckets
- `file-shares`: Samba, NFS, SMB, network shares
- `backup-archive`: Backup systems, archives, disaster recovery

#### 2.7 Mobile
- `ios-security`: iOS hardening, entitlements, signing
- `android-security`: Android hardening, permissions, APK analysis
- `app-store-review`: App store submission, compliance

---

### 3. EJE INGENIERÍA (¿Cómo se construye y mantiene?)

Define técnicas de **SECURE SDLC, infraestructura, supply chain**.

#### 3.1 Secure SDLC
- `secure-design`: Threat modeling, architecture reviews
- `code-security`: SAST, code review, secure patterns
- `dependency-check`: SCA, supply chain, software composition
- `secrets-management`: Vault, env var, secret rotation
- `ci-cd-security`: Pipeline hardening, gate checks
- `commit-signing`: GPG signing, commit verification
- `build-security`: Build artifact integrity, container signing

#### 3.2 Infrastructure as Code
- `terraform-validation`: HCL linting, policy-as-code (Sentinel)
- `ansible-playbook`: Yaml validation, idempotent checks
- `dockerfile-security`: Container image scanning, layer analysis
- `kubernetes-manifest`: YAML validation, network policies
- `gitops`: Declarative infra, deployment automation

#### 3.3 Supply Chain
- `dependency-provenance`: SBOM, SLSAbuild verification
- `artifact-signing`: Cosign, notary, artifact verification
- `third-party-risk`: Vendor assessment, MSA review
- `open-source-licensing`: GPL,MIT, commercial license compliance

---

### 4. EJE DEFENSA (¿Cómo detectamos y respondemos?)

Define técnicas de **DETECCIÓN PROACTIVA, hunting, respuesta**.

#### 4.1 Detección y Monitoreo
- `siem-rules`: Sigma, ELK, Splunk, Datadog rules
- `edr-tuning`: EDR queries, MDE hunting, alerts
- `threat-intelligence`: IOCs, feeds, reputation
- `behavioral-analytics`: ML-based anomaly, behavior baselining
- `log-ingestion`: Centralization, parsing, correlation

#### 4.2 Threat Hunting
- `hypothesis-driven`: Buscar TTP específica (MITRE ATT&CK)
- `anomaly-hunting`: Detectar lo que "no encaja"
- `compliance-hunting`: Auditoría de controles (PCI, HIPAA)
- `data-exfil-hunting`: Búsqueda de data movement inusual

#### 4.3 DFIR
- `live-forensics`: Memory dump, network capture en vivo
- `disk-forensics`: Timeline reconstruction, artifact analysis
- `timeline-analysis`: Event sequencing, causal analysis
- `malware-analysis`: Sandboxing, reverse engineering, yara rules
- `incident-response`: Containment, eradication, recovery

#### 4.4 SOC Operations
- `alert-tuning`: Reducción de false positives
- `escalation-procedures`: Criterios de escalada
- `runbooks`: Procedimiento de respuesta
- `metrics-kpis`: MTTR, mean time to detect, etc.

---

### 5. EJE OPERACIÓN DE AGENTE (¿Cómo automatiza?)

Define técnicas de **código generado por IA, agentic capabilities**.

#### 5.1 Generación de Código
- `safe-script`: Script pequeño, auditable, máx 200 líneas
- `policy-checker`: Validación de configuración contra policies
- `parser-normalizer`: Convertir N formatos a estándar
- `automation-workflow`: Orquestar múltiples pasos

#### 5.2 Ejecución Controlada
- `dry-run`: Simular sin modificar
- `timeout-enforcement`: Max time, no loop infinito
- `logging-audit`: Cada paso se registra
- `rollback-capability`: Undo de cambios

#### 5.3 Formatos de Salida
- `json-normalized`: Hallazgos en JSON estándar
- `csv-reports`: Reportes tabulares
- `html-dashboard`: Visualizaciones interactivas
- `singlefile`: Todo en un HTML autónomo

---

## Matriz de Clasificación: Pregunta-Respuesta

Haz estas preguntas **en orden** para clasificar una solicitud:

### Pregunta 1: ¿Hay autorización explícita?
```
Sí  → Continuar a Pregunta 2
No  → Solicitar: "¿Quién autoriza? ¿Qué exactamente?"
```

### Pregunta 2: ¿Es un hard stop (prohibido)?
```
Sí  → Rechazar y reconducir a defensiva
No  → Continuar a Pregunta 3
```

### Pregunta 3: ¿Cuál es el dominio TÉCNICO PRIMARIO?
```
Red/Perimeter                   → Cargar: Network Security ref
Web/API                         → Cargar: Web AppSec ref
Cloud/K8s                       → Cargar: Cloud ref
Identity/AD                     → Cargar: Identity ref
Endpoint/Mobile                 → Cargar: Endpoint ref
SDLC/Code/IaC                   → Cargar: Engineering ref
Detection/SIEM/Hunting          → Cargar: Detection ref
Incident/Forensics              → Cargar: DFIR ref
(Mixto)                         → Usar Playbook 01 + múltiples refs
```

### Pregunta 4: ¿Cuál es el dominio GOVERNANCE?
```
Startup, bajo recurso            → Escala reducida, automatizar si es posible
Mid-market                       → Estándar (CIS, NIST)
Enterprise, compliance strict    → Auditable, cadena de custodia, reporting formal
```

### Pregunta 5: ¿Cuál es el riesgo aceptable?
```
Low risk                         → OK modificar, no reversible si es automático
Medium risk                      → Requiere dry-run, aprobación, rollback
High risk                        → Manual con segunda opinión, post-engagement support
```

### Pregunta 6: ¿Necesita agentic (código)?
```
Sí, parsear logs                 → use scripts/log_triage.py + custom parser
Sí, normalizar findings          → use scripts/normalize_findings.py
Sí, validar integridad           → use scripts/check_integrity.py
Sí, aud HTTP surface             → use scripts/http_surface_audit.py
No, solo referencia              → cargar references/, no script necesario
```

### Pregunta 7: ¿Cuál es el playbook?
```
Assessment general               → Playbook 01 (authorized-assessment)
Web/API                          → Playbook 02 (web-api-review)
Cloud/K8s                        → Playbook 03 (cloud-k8s-review)
Detection/Hunting                → Playbook 04 (detection-hunting)
SDLC/IaC/Code                    → Playbook 05 (secure-sdlc-review)
Incident imminente               → Playbook 06 (incident-triage)
(Combinación)                    → Playbook 01 + complementar con 02-06 selectivamente
```

---

## Tabla de Composición: Combinaciones Comunes

| Caso de Uso | Dominio Primario | Secundarios | Playbook | Refs Principales |
|---|---|---|---|---|
| "Auditame mi app web" | Web/AppSec | Auth, Network | 02 | 06, 01, 14 |
| "Revisa mi Kubernetes" | Cloud/K8s | Engineering, Defense | 03 | 08, 13, 12 |
| "Implementamos OAuth, ¿bien?" | Identity/Access | Web/AppSec, Governance | 02+01 | 06, 09, 01 |
| "¿Cómo detecto malware?" | Defense/Hunting | Detection, Forensics | 04 | 11, 12, 21 |
| "Asegura mi pipeline CI/CD" | SDLC/Engineering | Cloud, Secrets | 05 | 13, 20, 26 |
| "Brecha de seguridad" | Incident/DFIR | Detection, Forensics | 06 | 11, 27, 21 |
| "¿Está bien mi IaC?" | Engineering/SDLC | Cloud, Governance | 05 | 13, 08, 25 |
| "Hardening de Windows" | Endpoint/Defense | Governance, Secrets | 01+04 | 09, 29, 31 |
| "Cumplo PCI-DSS?" | Governance/Compliance | All relevant | 01 | 01, 25, 27 |
| "Pentesting completo" | Assessment | All domains | 01 | Todas según alcance |

---

## Matriz de Priorización de Hallazgos

Una vez clasificada la tarea, los hallazgos se priorizan por:

```
PRIORIDAD = CVSS_Score + (Effort_Remediation_Inverse * 10%)
            - (Time_to_Patching * 5%)
```

Donde:
- `CVSS_Score`: 0-10 (de references)
- `Effort_Remediation`: 1-10 (bajo=fácil, alto=complejo)
- `Time_to_Patching`: horas para reparar

**Ejemplo**:
- CVE crítico, easy fix: 9.8 + 10 - 5 = 14.8 → FIX FIRST
- CVE medio, difícil fix: 5.0 + 1 - 20 = -14 → TRACK, no urgente

---

## Taxonomía Extendida

Para consulta detallada, ver `references/32-domain-taxonomy-extended.md`.

Contiene:
- Sub-clasificaciones técnicas para cada dominio
- Herramientas recomendadas por tipo de tarea
- TTPs de MITRE ATT&CK por clasificación
- CWEs relevantes por dominio
- Compliance frameworks por tipo

---

## Regla de Oro

**Si una solicitud toca >3 dominios primarios, usa Playbook 01 (Authorized Assessment) como base y complementa selectivamente.**

No cargues 32 referencias a la vez. Eso causa ruido, no claridad.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion de taxonomia 2026

### Reglas adicionales

### Regla ampliada 01
- Entrada ejemplo: API con backlog regulatorio.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 02
- Entrada ejemplo: cluster cloud con IAM heredado.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 03
- Entrada ejemplo: alerta DFIR con IOC externo.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 04
- Entrada ejemplo: pipeline supply chain sin firma OCI.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 05
- Entrada ejemplo: API con backlog regulatorio.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 06
- Entrada ejemplo: cluster cloud con IAM heredado.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 07
- Entrada ejemplo: alerta DFIR con IOC externo.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 08
- Entrada ejemplo: pipeline supply chain sin firma OCI.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 09
- Entrada ejemplo: API con backlog regulatorio.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 10
- Entrada ejemplo: cluster cloud con IAM heredado.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 11
- Entrada ejemplo: alerta DFIR con IOC externo.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 12
- Entrada ejemplo: pipeline supply chain sin firma OCI.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 13
- Entrada ejemplo: API con backlog regulatorio.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 14
- Entrada ejemplo: cluster cloud con IAM heredado.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 15
- Entrada ejemplo: alerta DFIR con IOC externo.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 16
- Entrada ejemplo: pipeline supply chain sin firma OCI.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

### Regla ampliada 17
- Entrada ejemplo: API con backlog regulatorio.
- Dominio primario: el que gobierna el riesgo inmediato.
- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.
- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.

