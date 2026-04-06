# Authorized Assessment Playbook (01)

## Visión Ejecutiva

El assessment autorizado es el **flujo de trabajo núcleo** de ORION. Estructura una evaluación 
técnica completa de riesgo, gobernanza y postura de una organización o dominio específico, 
desde kick-off hasta reporte y validación de fixes.

**Scope típico**: 2-4 semanas  
**Entregables**: Reporte ejecutivo, hallazgos técnicos, roadmap, evidencia  
**Outcome deseado**: Decisiones informadas de inversión en seguridad  

---

## Cuándo Usar Este Playbook

### ✅ Buena encaje:
- Evaluación técnica amplia (multi-dominio)
- Cliente con presupuesto formal, timeline flexible
- Assessment inicial de nuevo vendor/partner
- Review de postura tras incidente
- Compliance / debido diligence
- Madurez SDLC mejora
- Validación post-remediation

### ❌ Mal encaje:
- Solo web app (→ Playbook 02)
- Solo cloud/K8s (→ Playbook 03)
- Incidente activo (→ Playbook 06)
- Threat hunting puro (→ Playbook 04)

---

## Entradas Requeridas

| Entrada | Descripción | Ejemplo |
|---|---|---|
| **Autorización Escrita** | Consentimiento legal, alcance firmado | ToR (Terms of Reference) |
| **Activos en Scope** | Qué sistemas, datos, usuarios | "3 aplicaciones web + AWS account + 500 usuarios" |
| **Restricciones** | Qué NO tocar | "No tocar BD de producción, no apagar servicios" |
| **Entorno** | On-prem, cloud, hybrid | AWS + on-prem data center |
| **Ventana de Trabajo** | Horarios permitidos | "Lunes-viernes 9-17, zona EST" |
| **Owner Técnico** | Contacto point-of-contact | "John Doe, CTO" |
| **Entregable Esperado** | Reporte, código, Jira? | "PDF ejecutivo + JSON hallazgos" |
| **Presupuesto / Duración** | Límites reales | "4 semanas, $50k" |
| **Escalation Path** | Cómo reportar problemas | "Slack #security, email cto@" |
| **Riesgos Conocidos** | Qué ya se sabe que está roto | "Sabemos que SAP tiene acceso ancho" |

---

## Pre-Engagement (Semana -1)

### Kick-off Meeting

**Objetivo**: Establecer contexto, confirmar scope, identificar red flags

**Personas obligatorias**:
- Tu líder técnico o auditor principal
- CTO/CISO del cliente
- Owner del principal sistema
- Legal/Compliance (reducida, solo si necesario)

**Agenda** (90 min):
1. Bienvenida y expectativas (10 min)
2. Resumen de metodología ORION (10 min)
3. Scope detallado: sistemas, límites, usuarios (20 min)
4. Restricciones y window de trabajo (10 min)
5. Entregables y formato de salida (10 min)
6. Escalation y comunicación (10 min)
7. Q&A (10 min)

**Output**: Documento firmado de ToR (Terms of Reference)

### Planificación Técnica

**Selecciona Perfil Operativo** (de SKILL.md):
- **Rápido** (4 horas/semana): validación superficial, quick wins
- **Estructurado** (40 horas/semana): cobertura completa, rigor
- **Hardening** (60+ horas/semana): profundo + arquitectura
- **Continuo**: múltiples iteraciones, ajustes

**Selecciona Dominios** (de DOMAIN_TAXONOMY.md):
Pregunta: "¿Cuál es el riesgo principal?"
```
Governance → sí/no
Web/API → sí/no
Cloud → sí/no
Identity → sí/no
Network → sí/no
Data → sí/no
SDLC → sí/no
Detection → sí/no
```

**Mapea Referencias** (de MODULE_MAP.md):
Por cada dominio, carga referencias relevantes.
Ejemplo: si Cloud → cargas references 08, 13, 25, 20.

**Define Equipo**:
- Auditor principal (líder, punto de contacto)
- Especialista técnica por dominio
- Escribiente (documentación)
- Red team (si aplica)
- Ops de cliente (facilita acceso)

### Herramientas & Acceso

**Validar acceso**:
- [ ] VPN funciona
- [ ] SSH keys funcionan
- [ ] Cloud console acceso (AWS/Azure/GCP)
- [ ] SIEM access (si aplica)
- [ ] Burp/ZAP license (si web)
- [ ] WiFi guest access (si physical)

**Crear baseline**:
```bash
# Toma snapshots pre-assessment
terraform plan > baseline-tf.txt
aws ec2 describe-instances > baseline-instances.json
kubectl get all -A > baseline-k8s.json
nmap -sV target-network > baseline-nmap.txt
```

**Seguridad**: Auditoría
- Todas las herramientas logean
- Burp usando Portswigger cloud?
- Acceso de red limitado a scope
- Credenciales en password manager encriptado

---

## Durante: Fase de Ejecución (Semanas 1-3)

### Daily Workflow

**07:00-08:00 Stand-up** (30 min)
- Status: qué se completó ayer
- Blockers: qué está atascado
- Plan: qué hoy
- Escalation: hay red flags?

**08:00-17:00 Assessment**
- Discovery: mapeo de activos
- Validación: cheques de configuración
- Testing: pruebas de seguridad
- Documentación: screenshots, evidencia
- Logging: todos los hallazgos → findings.json

**17:00 EOD Sync** (15 min)
- Recap: qué se hizo hoy
- Riesgos emergentes
- Mañana: plan de trabajo

### Por Dominio: Estructura Estándar

Cada dominio sigue plan: Discovery → Validation → Testing

#### Discovery (día 1-2 por dominio)
```
1. Inventario: qué existe?
   - Herramientas de host (nmap, AWS API, kubectl, AD query)
   - Qué versiones, configuraciones
   - Mapa de red (si network-centric)
   
2. Asset tagging:
   - Crítico / Alto / Medio / Bajo
   - Owner / équipo dueño
   - Data classification (if aplicable)
   
3. Documentation
   - Diagrama de arquitectura (Miro, Lucidchart)
   - Inventory JSON
```

#### Validation (día 2-3 por dominio)
```
1. Config review
   - Comparison con benchmarks (CIS, AWS Well-Architected)
   - Herramientas: Checkov, Tfsec, kubesec
   
2. Entrevistar Owner
   - "¿Por qué esto así?"
   - Design decisions vs accidents
   
3. Evidence photobomb
   - Screenshots de misconfig
   - Console output
   - Config extracts
```

#### Testing (día 3-4 por dominio)
```
1. Proof-of-concept
   - Explotar hallazgo (si permitido)
   - Documentar pasos reproducibles
   - Video si crítico
   
2. False positive check
   - Validar es real, no false alarm
   - Documentar assumption si hay duda
```

### Parallelización de Playbooks

Si web/API en scope → Ejecuta **Playbook 02** en paralelo (Semana 1-2)  
Si cloud en scope → Ejecuta **Playbook 03** en paralelo (Semana 1-2)  
Si SDLC en scope → Ejecuta **Playbook 05** en paralelo (Semana 2-3)  

---

## Fase de Análisis (Semana 3-4)

### Normalización de Hallazgos

Todos los hallazgos → JSON estándar vía script:
```bash
python3 normalize_findings.py --input findings-raw/ --output findings.json
```

**Schema**:
```json
{
  "finding_id": "001",
  "discovered": "2024-02-15",
  "title": "S3 bucket públicamente accesible",
  "severity": "CRITICAL",
  "cvss_score": 9.1,
  "cwe": [434],
  "impact": "Exfiltración de datos",
  "remediation": "Bloquear acceso público, habilitar encryption",
  "effort_hours": 2,
  "owner": "John Doe",
  "evidence": ["s3://bucket-name is ListBucket-able from 0.0.0.0/0"]
}
```

### Priorización

Matriz: CVSS × Esfuerzo × Impacto
```
Priority = CVSS(0-10) + Esfuerzo(0-10) - ImpactoBusiness(0-10)

CRÍTICO (15+): Arregla hoy
ALTO (10-15): Arregla en 30 días
MEDIO (5-10): Arregla en 90 días
BAJO (<5): Próximo ciclo
```

### Gap Analysis

| Control | Requerido | Actual | Brecha | Owner | Timeline |
|---------|-----------|--------|--------|-------|----------|
| MFA root | SÍ | NO | CRÍTICA | CTO | 30d |
| Log rotation | SÍ | 90d | MEDIA | Ops | 60d |
| Network seg | SÍ | NO | CRÍTICA | Infra | 90d |

---

## Fase de Reporte (Semana 4)

### Reporte Ejecutivo (5-10 páginas)

**Sección 1: Resumen Ejecutivo**
- Riesgos críticos: 3 (acción ahora)
- Riesgos altos: 12 (acción 30d)
- Overall maturity: 45/100
- Investment needed: $150k over 12 months

**Sección 2: Hallazgos Principales**
```
CRÍTICO: S3 público
  Impacto: 10M records expostos
  Fix: IAM policy
  Timeline: 2 horas

ALTO: No MFA en root
  Impacto: Account takeover
  Fix: Habilitar MFA
  Timeline: 1 día
```

**Sección 3: Roadmap**
```
30 días - Quick wins: 40 horas
90 días - Network redesign: 200 horas
180 días - Compliance automation: 400 horas
```

**Sección 4: Risk Score**
- Before: 7.2/10
- After: 3.1/10
- ROI: $150k spend → $500k risk reduction

### Reporte Técnico (Anexo 50-100 páginas)

- Inventario detallado
- Screenshots de misconfig
- Hallazgos con pasos reproducibles
- Evidence chain
- Compliance mapping

---

## Post-Engagement (Semanas 5-16)

### Follow-up Schedule

- **Semana 6**: Validar críticos fixeados
- **Semana 8** (30-day): Re-test altos
- **Semana 14** (90-day): Re-test medios

### Success Criteria

✅ Todos los sistemas auditados  
✅ Hallazgos reproducibles  
✅ Roadmap aprobado  
✅ Evidence completa  
✅ Equipo cliente capacitado  

---

## Red Flags

| Flag | Acción |
|---|---|
| "Prueba rápido sin reglas" | Ref SKILL.md guardrails. Document in ToR |
| Acceso denegado a sistema crítico | Es hallazgo. Estimar esfuerzo |
| Data sensible en logs | Escalada inmediata a legal |
| Presión para NO reportar | Stop work. Escalada a manager |



<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Operativa 2026 - Authorized Assessment Playbook (01)

Este playbook se amplia para cubrir integraciones y casos de assessment multi-dominio.

### Integraciones de ejecucion

- Jira: usar para coordinacion, backlog, evidencia o telemetria.
- ServiceNow: usar para coordinacion, backlog, evidencia o telemetria.
- Slack/Teams: usar para coordinacion, backlog, evidencia o telemetria.
- OpenSearch: usar para coordinacion, backlog, evidencia o telemetria.
- GitHub Actions: usar para coordinacion, backlog, evidencia o telemetria.
- Splunk: usar para coordinacion, backlog, evidencia o telemetria.

### Casos operativos extendidos

### Caso operativo 01
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 02
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 03
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 04
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: OpenSearch.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 05
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: GitHub Actions.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 06
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Splunk.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 07
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 08
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 09
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 10
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: OpenSearch.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 11
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: GitHub Actions.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 12
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Splunk.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 13
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 14
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 15
- Situacion: engagement de assessment multi-dominio con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

