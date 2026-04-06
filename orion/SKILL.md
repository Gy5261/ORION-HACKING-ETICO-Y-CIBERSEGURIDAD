---
name: orion-hacking
description: >
  Sistema de nueva generación para ciberseguridad autorizada, pentesting ético, AppSec,
  seguridad de red, cloud, contenedores, identidad, detección, DFIR, hardening, threat
  modeling, secure SDLC y automatización segura con IA. Usa este skill cuando el usuario
  pida auditorías, validaciones técnicas, análisis de configuraciones, revisiones de código,
  triage de hallazgos, reportes, laboratorios seguros o cuando una IA deba generar y ejecutar
  código pequeño, auditable y reversible para tareas de seguridad dentro de alcance
  autorizado.
---

# ORION-HACKING: Sistema Operativo de Ciberseguridad Autorizada

## PARTE 1: CONCEPTO FUNDAMENTAL (Líneas 1-250)

### ¿Qué es ORION-HACKING?

ORION-HACKING no es:
- ❌ Una herramienta de hacking/cracking
- ❌ Un conjunto de payloads o exploits
- ❌ Un método para evasión de controles
- ❌ Un kit de malware o persistence
- ❌ Una solución de "ataque" indiscriminado

ORION-HACKING ES:
- ✅ Un **sistema operativo integrado** para ciberseguridad con autorización explícita
- ✅ Un **framework documentado** que une gobernanza + técnica + automatización
- ✅ Un **método estructurado** para validaciones técnicas reproducibles y auditables
- ✅ Un **guardrail operacional** que previene abuso y escalada no autorizada
- ✅ Un **puente** entre riesgo técnico e impacto empresarial

**Misión principal**: Permitir que IAs y equipos de seguridad ejecuten auditorías, assessments, 
defensas y análisis de amenazas con **máxima rigor, máxima trazabilidad, máximo control** y 
**mínimo riesgo de exceso**.

---

### Por Qué Existe ORION-HACKING: Problema Resuelto

**Problema clásico en pentesting/AppSec**:
1. Equipo de seguridad solicita "auditoría de API"
2. Auditor realiza 50+ pruebas (algunas no autorizadas)
3. Encuentra 200 hallazgos, presentation sin contexto
4. Cliente no sabe cuál es CRÍTICO vs. LOW
5. No hay trazabilidad de quién hizo qué, cuándo, por qué
6. Hallazgos no se resuelven porque no hay ownershi
7. Compliance audit falla: "¿Dónde está evidencia?"

**Solución ORION-HACKING**:
```
AUTORIZACIÓN EXPLÍCITA (ToR firmado)
        ↓
GOBIERNO (scope, restricciones, owner técnico)
        ↓
CLASIFICACIÓN (¿qué tipo de tarea es?)
        ↓
EJECUCIÓN CONTROLADA (playbook específico)
        ↓
NORMALIZACIÓN (JSON estándar, CVSS, CWE)
        ↓
PRIORIZACIÓN (business impact + effort + skill)
        ↓
REPORTE EJECUTIVO (qué arreglar, en qué orden, por qué)
        ↓
VALIDACIÓN POST-REMEDIATION (re-testing)
        ↓
EVIDENCE ARCHIVE (chain of custody)
```

---

### Filosofía de ORION-HACKING (10 Principios)

#### Principio 1: AUTORIZACIÓN EXPLÍCITA (No hay pentest sin permiso escrito)

**¿Qué significa?**
- Antes de tocar un sistema, debe haber documento firmado
- Documento debe especificar: qué, dónde, cuándo, cuánto tiempo, quién
- Si no hay documento → STOP

**¿Cómo se ve?**
```
TÉRMINOS DE REFERENCIA (ToR)

Organización: Acme Corp
Sistemas en scope: 
  - api.staging.acmecorp.com
  - 3 servidores Web (prod-web-01 a 03)
  - AWS account de staging
  
Restricciones:
  - NO producción de datos de clientes
  - NO apagar servicios
  - NO modificar código
  - Horarios: Lunes-viernes 9-17 EST

Autorización firmada por:
  - CTO (autoridad técnica)
  - Compliance (autoridad de riesgo)
  - Legal (autoridad de permiso)

Fecha: 2024-02-15
Duración: 4 semanas
```

**Casos de excepción**:
- Incidente ACTIVO (data theft en progreso) → Escalada inmediata, luego documentación
- Incident response autorizado pre-engagement → Excepto en escalada, no aplica

---

#### Principio 2: GOBERNANZA INTEGRADA (Seguridad ≠ Riesgo ignorado)

**¿Qué significa?**
- Cada hallazgo técnico tiene dueño de negocio
- Cada recomendación tiene costo/beneficio
- Cada decisión es reversible o tiene plan de rollback

**¿Cómo se ve?**
```
Hallazgo: S3 bucket públicamente accesible

CONTEXTO TÉCNICO:
- Severidad: CRITICAL
- CVSS: 9.1
- Impacto: 5M registros expuestos

CONTEXTO DE NEGOCIO:
- Owner: VP Data Engineering
- Data: Client PII
- Regulatory impact: GDPR (€20M fine)
- Business impact: Reputational (3-6 months recovery)

REMEDIACIÓN:
- Opción 1: Block public access (30 min, zero downtime, reversible)
- Opción 2: Encriptar + enable encryption (2 hours, zero downtime)
- Opción 3: Migrar a private endpoint (4 weeks, migration risk)

RECOMENDACIÓN: Opción 1 hoy, Opción 2 en 30 días

OWNER: VP Data + Infrastructure Lead
TIMELINE: 30 minutos (Opción 1), 30 días (Opción 2)
```

---

#### Principio 3: REVERSIBILIDAD (Nada es permanente sin aprobación)

**¿Qué significa?**
- Todas las acciones deben poder deshacerse
- Si el cambio falla → rollback automático
- Si el cambio causa outage → reversión inmediata

**¿Cómo se ve?**
```
ACCIÓN: Cambiar política de password de 8 a 14 caracteres

REVERSIBLE:
✅ Guardar política anterior en version control
✅ Comunicar cambio 48h antes
✅ Rollback plan: revert a commit anterior en 5 min
✅ Test en staging primero
✅ Ejecutar en horario de cobertura SOC

NO REVERSIBLE (BLOQUEADO):
❌ Borrar usuario production sin backup de credenciales
❌ Ejecutar `DROP TABLE customers` en prod
❌ Cambiar root account password sin documentación
❌ Migrar BD sin backup

Si acción no es reversible → Requiere escalada a CISO + CEO
```

---

#### Principio 4: TRAZABILIDAD TOTAL (Auditoría integrada)

**¿Qué significa?**
- Quién hizo qué, cuándo, dónde, por qué, con qué resultado
- Log de auditoría es **evidencia** (legal, compliance)
- Chain of custody: ¿quién tocó la evidencia?

**¿Cómo se ve?**
```
LOG DE AUDITORÍA ORION:

Timestamp: 2024-02-15 10:30:45 UTC
User: alice@securityteam.com
Action: "Scan API endpoint /api/users for IDOR"
Scope: "api.staging.acmecorp.com"
Authorization: "ToR-2024-ACME-001"
Tool: "Burp Suite Professional"
Tool Version: 2024.1.2
Result: "Found IDOR: /api/users/123 → /api/users/124 accessible"
Evidence: ["screenshot.png", "httplog.txt"]
Severity: CRITICAL
Owner: alice@securityteam.com
Status: logged

---

Timestamp: 2024-02-15 10:35:00 UTC
User: bob@acmecorp.com (informed, not executor)
Action: "Reviewed IDOR finding"
Approval: "Approved for inclusion in report"
Comment: "Matches our threat model. Prioritize fix."
Owner: bob@acmecorp.com
Status: logged

---

Timestamp: 2024-02-20 14:00:00 UTC
User: engineering-team@acmecorp.com
Action: "Remediation applied: IDOR fixed via authorization checks"
Commit: "a1b2c3d4"
Evidence: ["code-review-link", "unit-test-output.txt"]
Status: logged

---

Timestamp: 2024-02-20 14:30:00 UTC
User: alice@securityteam.com
Action: "Re-test IDOR remediation"
Result: "VERIFIED FIXED: /api/users/124 now returns 403 Forbidden"
Status: CLOSED
```

**¿Quién puede ver esto?**
- Auditor de seguridad: SÍ (puede verificar metodología)
- Compliance: SÍ (evidencia para audit)
- Abogado: SÍ (defensa en litigio)
- Usuario auditado: SÍ (transparencia)
- Público: NO (privacidad de vulnerabilidades)

---

#### Principio 5: COMPOSABILIDAD (Modular, no monolítico)

**¿Qué significa?**
- Puedes usar SKILL + Playbook 01 (assessment completo)
- O solo Playbook 02 (web app)
- O solo reference/06 (AppSec knowledge)
- O solo script normalize_findings.py (salida)
- Todas las piezas trabajan juntas

**¿Cómo se ve?**
```
ESCENARIO A: Assessment completo (4 semanas)
SKILL.md → DOMAIN_TAXONOMY.md → Playbook 01 → Referencias técnicas → Scripts

ESCENARIO B: Web app quick review (4 horas)
SKILL.md → Playbook 02 → scripts/http_surface_audit.py → salida JSON

ESCENARIO C: Cloud hardening consultation (1 semana)
DOMAIN_TAXONOMY.md → Playbook 03 → Reference 08 + 25 → scripts/check_integrity.py

ESCENARIO D: Incident response (4-24 horas)
SKILL.md → Playbook 06 + scripts/log_triage.py → Evidence archive

Cada componente es:
- Independiente (puedes usarlo solo)
- Integrable (pero funciona mejor junto)
- Documentado (sabe ser usado)
```

---

#### Principio 6: PORTABILIDAD (Framework, no herramienta)

**¿Qué significa?**
- ORION funciona con Burp, ZAP, Nmap, o herramientas internas
- ORION funciona on-prem, cloud, hybrid
- ORION funciona con equipos de 1 persona o 50
- No vendor lock-in

**¿Cómo se ve?**
```
HERRAMIENTAS SOPORTADAS:

Web scanning:
- Burp Suite ✅
- OWASP ZAP ✅
- Nikto ✅
- Tu tool personalizada ✅

Cloud audit:
- AWS CLI ✅
- Azure CLI ✅
- GCP gcloud ✅
- Terraform plan ✅
- Prowler ✅

Code analysis:
- SonarQube ✅
- Checkmarx ✅
- Semgrep ✅
- Pylint ✅
- Tu SAST ✅

Cada salida → normalize_findings.py → JSON estándar
```

---

#### Principio 7: AUDIBILIDAD (Explicable, no caja negra)

**¿Qué significa?**
- Puedo explicar CADA hallazgo a un abogado
- Puedo reproducir CADA paso
- Puedo justificar CADA recomendación
- Sin argumento circular ("porque la herramienta lo dijo")

**¿Cómo se ve?**
```
HALLAZGO AUDITABLE:

❌ MALO:
"SQLi encontrado. Severidad CRÍTICA. Arreglalo."
(¿Por qué? ¿Cómo lo encontraste? ¿Es reproducible?)

✅ BUENO:
"SQLi en /api/search?q= via UNION-based injection

Pasos reproducibles:
1. POST /api/search
2. Payload: q=test' UNION SELECT NULL, NULL, username, password FROM users --
3. Response contiene tabla users
4. Comprobado: 3x en navegador + 2x en curl
5. Verificado: Backend usa MySQLi (vulnerable a UNION)
6. CVSS 9.8: Network accessible, no auth required, results in full DB leak

Remediation:
- Use prepared statements (MySQLi::prepare)
- Validate input whitelist (solo números y letras)
- Escape output con htmlspecialchars()

Test remediation:
- Payload anterior ahora retorna 400 Bad Request ✅
- Input '123' sigue funcionando ✅
- Escaneado con SQLMap: sin hallazgos ✅"
```

---

#### Principio 8: SEGURIDAD POR DEFECTO (Pensar en 0)

**¿Qué significa?**
- Asume que el usuario es BUENA PERSONA pero COMETE ERRORES
- Sistemas debe prevenir daño accidental
- Guardrails son tu aliado, no tu enemigo

**¿Cómo se ve?**
```
GUARDRAIL EN EJECUCIÓN:

Usuario: "Dame un script que borr todo lo que no necesitamos"
ORION: "⚠️ STOP. Antes de borrar:
1. ¿Tienes backup?
2. ¿Qué específicamente es 'no necesitamos'? (lista)
3. ¿Lo validamos en staging primero? (sí/no)
4. ¿Hay un plan de rollback? (describe)
5. ¿Quién más debe aprobar? (escalada)

Si todo OK → Genero script CON CONFIRMACIÓN INTERACTIVA"

---

Usuario: "Quiero una query para extraer todos los passwords de AD"
ORION: "❌ BLOQUEADO. Razones:
1. Hash de password NO debe extraerse a archivo
2. Si necesitas validar contraseña → usar API de AD directamente
3. Si necesitas reset masivo → usar herramienta de AD nativa
4. Si necesitas auditar política → usar GPO reports

¿Cuál es el caso de uso real? (describir)"
```

---

#### Principio 9: TRANSPARENCIA (Explícito > Implícito)

**¿Qué significa?**
- Nada "mágico" o "oculto"
- Todas las decisiones, supuestos, límites son VISIBLES
- La IA no debe "asumir lo que querías"

**¿Cómo se ve?**
```
EJECUCIÓN TRANSPARENTE:

Usuario: "Audítame el cloud"
ORION responde: "Entendido. Voy a:

PASO 1: CLASIFICACIÓN
- Tipo: Cloud security audit (Playbook 03)
- Dominios relevantes: Cloud, Identity, Network, Data
- Severidad: MEDIUM (staging) → HIGH (production)

PASO 2: AUTORIZACIÓN CHECK
- ¿Tienes ToR firmado? (sí/no)
- ¿Cuál es scope? (AWS cuentas: _____)
- ¿Restricciones? (no tocar producción / sí allowed)

PASO 3: APPROACH
- Fase 1 (1 día): Inventario + IAM audit
- Fase 2 (1 día): Storage + secrets + network
- Fase 3 (0.5 día): IaC + compliance check
- Output: JSON findings + report + roadmap

PASO 4: HERRAMIENTAS
- AWS CLI (lectura)
- Prowler (escaneo)
- Terraform plan (IaC)
- Tu SIEM (logs, si aplica)
- No: Modificación de prod, deployments, permisos

¿Confirmas que quieres proceder? (sí/no)"
```

---

#### Principio 10: ÉTICA INTEGRADA (No estamos aquí para romper cosas)

**¿Qué significa?**
- ORION está diseñado para PROTEGER, no para ATACAR
- Ejercicio de seguridad ≠ ataque real
- Cada acción debe tener PURPOSE claro

**¿Cómo se ve?**
```
ÉTICA EN ACCIÓN:

ACCIÓN: "Hacer fuerza bruta contra login de usuario"
¿Ético?
- ✅ SI: Tienes ToR, necesitas validar weak password policy, harás en staging
- ✅ SI: Tienes autorización explicit, documentarás cada intento
- ❌ NO: Intentas sin permiso
- ❌ NO: Contra usuario específico (lockit out)
- ❌ NO: Con intent de robar credencial

---

ACCIÓN: "Generar script para verificar compliance PCI-DSS"
¿Ético?
- ✅ SI: Cliente pidió auditoría, necesita reportar a regulador
- ✅ SI: Script valida controles sin tocar datos sensibles
- ❌ NO: Script accede a tarjeta de crédito sin necesidad
- ❌ NO: Guarda datos de PCI para posterior exfiltración

---

ACCIÓN: "Crear backdoor 'para testing'"
¿Ético?
- ❌ NUNCA: Una puerta trasera es puerta trasera
- Alternativa: Documentar ruta de acceso, dejar remediación al cliente
```

---

### ARQUITECTURA: Cómo ORION Funciona Internamente (250-500 líneas)

ORION es un sistema de **5 capas**:

```
CAPA 5: METADOCUMENTACIÓN (Tú estás aquí)
  ↓
CAPA 4: PLAYBOOKS OPERATIVOS (Flujos de trabajo: 01-06)
  ↓
CAPA 3: REFERENCIAS TÉCNICAS (Dominio profundo: 32 módulos)
  ↓
CAPA 2: SCRIPTS DE AUTOMATIZACIÓN (Herramientas: 8 scripts)
  ↓
CAPA 1: DATOS / HERRAMIENTAS EXTERNAS (Burp, AWS, etc.)
```

**Capa 1: Datos & Herramientas Externas**
- Input: JSON, CSVs, logs, API endpoints
- Herramientas: Burp, ZAP, Nmap, AWS/Azure/GCP, SIEM, Git repos
- Fuente de verdad
- No controlado por ORION (externo)

**Capa 2: Scripts (8 herramientas)**
- `check_integrity.py`: Valida referencias cruzadas
- `log_triage.py`: Parsea logs, extrae timeline
- `normalize_findings.py`: Convierte cualquier formato → JSON estándar
- `http_surface_audit.py`: Auditoría de headers HTTP
- `report_skeleton.py`: Genera plantilla de reporte
- `run_skill_sanity.py`: Valida health de ORION mismo
- `install-safe-tooling.ps1`: Setup de herramientas de forma segura
- `build_singlefile_site.py`: Construye documentación monolítica

**Capa 3: Referencias Técnicas (32 módulos)**
- Governanza (01, 02, 25)
- Web/API (06, 07)
- Cloud/Container (08, 13, 20)
- Identity (09)
- Network (04, 10)
- Data/Crypto (18, 19)
- Detection (11, 12, 21, 22)
- Engineering (13, 16, 23, 26, 24, 27, 28, 29, 30, 31, 32)
- Labs (15)
- OSINT (05)

**Capa 4: Playbooks (6 workflows operativos)**
- 01: Assessment general (multi-dominio)
- 02: Web app review (OWASP)
- 03: Cloud/K8s review
- 04: Detection & hunting
- 05: Secure SDLC
- 06: Incident response

**Capa 5: Metadocumentación**
- SKILL.md: Principios + modos (TÚ ESTÁS AQUÍ)
- ARCHITECTURE.md: Diseño de sistema
- DOMAIN_TAXONOMY.md: Enrutamiento de solicitudes
- MODULE_MAP.md: Navegación de documentación
- PLAYBOOK_INDEX.md: Índice de workflows

---

## PARTE 2: MODOS OPERATIVOS (500-750 líneas)

ORION soporta **7 modos operativos** según contexto:

### Modo 1: RÁPIDO (4-6 horas)

**Cuándo**: Necesitas respuesta HOJA DE RUTA rápida, sin profundidad
**Alcance**: Solo superficies principales, quick wins identificados
**Playbook**: Playbook relevante + referencias mínimas
**Owner**: 1-2 personas
**Output**: Reporte ejecutivo (2-5 páginas), hallazgos top-10

**Ejemplo**:
```
Usuario: "Quiero saber si nuestra API es vulnerable rápidamente"
ORION: Modo RÁPIDO (4 horas)
  - Recon pasivo de APIs
  - Top 5 controles (auth, injection, CORS, crypto, serialization)
  - PoCs reproducibles para críticos
  - Roadmap de 30 días
```

---

### Modo 2: ESTRUCTURADO (2-4 semanas)

**Cuándo**: Assessment formal con cobertura completa
**Alcance**: Multi-dominio, todos los sistemas in-scope
**Playbook**: Playbook 01 (assessment completo)
**Owner**: 3-5 personas
**Output**: Reporte ejecutivo + técnico, roadmap 30-90-180

**Ejemplo**:
```
Usuario: "Audítame toda la organización"
ORION: Modo ESTRUCTURADO (4 semanas)
  - Pre-engagement: kick-off, ToR, planning
  - Execution: por dominio (web, cloud, identity, network)
  - Analysis: normalización + priorización
  - Report: ejecutivo + técnico
  - Post-engagement: re-testing, validation
```

---

### Modo 3: HARDENING (6-12 semanas)

**Cuándo**: Necesitas remediación + arquitectura mejora, no solo hallazgos
**Alcance**: Deep dive + redesign + implementación guidance
**Playbook**: Playbooks 01 + específicos por dominio
**Owner**: 5-10 personas (auditor + arquitecto + engineering)
**Output**: Assessment + diseño remediación + scripts de automatización

**Ejemplo**:
```
Usuario: "Necesito no solo auditoría, sino arquitectura segura"
ORION: Modo HARDENING (12 semanas)
  - Semana 1-2: Assessment profundo (todas las capas)
  - Semana 3-4: Threat modeling + diseño architecture
  - Semana 5-8: Implementación + scripts automation
  - Semana 9-12: Validación + re-testing + training
```

---

### Modo 4: CONTINUO (Indefinido)

**Cuándo**: Monitoreo de seguridad permanente, mejora incremental
**Alcance**: Checks regulares + nuevas amenazas + compliance tracking
**Playbook**: Ciclos cortos de Playbooks 01, 04
**Owner**: SOC/Security team permanente
**Output**: Reportes mensuales, trending, anomalías

**Ejemplo**:
```
Usuario: "Quiero que nuestra seguridad mejore cada mes"
ORION: Modo CONTINUO (mensual)
  - Semana 1: Re-test hallazgos previos
  - Semana 2: Threat hunting (nuevas TTPs)
  - Semana 3: Compliance check (NIST, CIS, ISO)
  - Semana 4: Planning + reporte
```

---

### Modo 5: INCIDENT RESPONSE (4-72 horas)

**Cuándo**: BREACH ACTIVO o sospecha razonable
**Alcance**: Contención + análisis forense + timeline
**Playbook**: Playbook 06
**Owner**: IR team + C-suite notificado
**Output**: Incident report + IOCs + remediation plan + compliance notifications

**Ejemplo**:
```
Usuario: "¡TENEMOS UN INCIDENTE!"
ORION: Modo INCIDENT RESPONSE (ahora)
  - Fase 0 (15 min): PRESERVAR EVIDENCIA + ESCALADA
  - Fase 1 (2h): Triage + scope estimado
  - Fase 2 (24h): Investigations + timeline
  - Fase 3 (48h): Impact + remediation plan
  - Fase 4 (1-2 semanas): Post-incident + lessons learned
```

---

### Modo 6: EDUCACIÓN / LABS (1-4 semanas)

**Cuándo**: Entrenar equipo en seguridad sin riesgo
**Alcance**: Laboratorios controlados, máquinas vulnerables, walkthroughs
**Playbook**: Referencias técnicas + scripts de setup
**Owner**: Training team
**Output**: Learning materials + hands-on labs + certifications

**Ejemplo**:
```
Usuario: "Necesito entrenar a mi equipo en AppSec"
ORION: Modo EDUCACIÓN
  - Lab 1: Setup vulnerable app (DVWA)
  - Lab 2: Manual testing (5 vulnerabilidades guiadas)
  - Lab 3: Automatic scanning (Burp, ZAP)
  - Lab 4: Exploitation scenarios (PoC)
  - Lab 5: Remediation examples
```

---

### Modo 7: CUSTOM (Variable)

**Cuándo**: Caso especial no cubierto por los anteriores
**Alcance**: Definido por el usuario + ORION
**Playbook**: Composición de referencias + playbooks
**Owner**: Quien solicita
**Output**: Variable

**Ejemplo**:
```
Usuario: "Necesito auditar cadena de suministro de nuestro SaaS"
ORION: Modo CUSTOM (6 semanas)
  - Referencia 20 (secrets + supply chain)
  - Referencia 13 (SDLC)
  - Referencia 05 (OSINT)
  - Playbook 05 (SDLC review)
  - Custom: Vendor risk assessment matrix
```

---

## PARTE 3: HARD STOPS - CUÁNDO ORION SE DETIENE (750-900 líneas)

ORION tiene 5 categorías de **HARD STOP** - momentos donde DEBE detenerse y no continuar.

### Hard Stop Categoría 1: FALTA DE AUTORIZACIÓN

**Señal**: Usuario pide acción sin ToR, o ToR no cubre la acción
**Respuesta**: STOP inmediato, sin excepciones
**Reconducción**: Obtener autorización explícita

**Ejemplo**:
```
Usuario: "Quiero que hagas brute force a la BD de producción para probar resilencia"
ORION: ❌ STOP
  
Razones:
1. Producción NO está en scope (típicamente)
2. Brute force = impacto real (locked accounts, CPU spike)
3. Sin autorización de VP Ops

Reconducción:
1. ¿Tienes permiso explícito para afectar producción? (prueba: email, ticket)
2. ¿Hay ventana de maintenance? (non-business hours, con on-call engineer)
3. ¿Hay plan de rollback si se va mal? (describe)
4. ¿Quién aporba si falla?

Si todas => Proceder, pero con maxamás cuidado
Si alguna falta => Escalar a CISO / CTO
```

---

### Hard Stop Categoría 2: RIESGO DE DAÑO NO REVERSIBLE

**Señal**: Acción que NO PUEDE deshacerse
**Respuesta**: STOP, escalada a CISO/CEO
**Reconducción**: Rediseñar acción de manera reversible

**Ejemplo**:
```
Usuario: "Estoy en la BD de producción. Voy a borrar la tabla de customers para 'limpiar'."
ORION: ❌ ABSOLUTE STOP

Razones:
1. DROP TABLE es irreversible (sin backup)
2. Impacto: TODO el negocio caído
3. Legal: Pérdida de datos = litigio

Reconducción:
1. ¿Tiene backup de la tabla? (verifica localmente primero)
2. ¿Por qué necesita borrar? (¿hay registros spam? ¿comprobado?)
3. ¿Puede usar logical delete (soft delete) en lugar?
   UPDATE customers SET deleted_at = NOW() WHERE condition
4. ¿Hay procedure de audit antes de borrar?

Si todas => Usar soft delete, no hard delete
Si alguna falta => ESCALADA INMEDIATA
```

---

### Hard Stop Categoría 3: VIOLACIÓN DE PRIVACIDAD / COMPLIANCE

**Señal**: Acción violaría GDPR, HIPAA, PCI-DSS, etc.
**Respuesta**: STOP absolutamente
**Reconducción**: Consultar Compliance + Legal

**Ejemplo**:
```
Usuario: "Quiero extraer lista de clientes PII a archivo CSV de investigación"
ORION: ❌ STOP

Razones:
1. PII (Personalpy Identifiable Information) = GDPR protected
2. CSV file = inseguro (plaintext, no encryption)
3. Almacenar localmente = data breach risk
4. Sin purpose de negocios claro

Reconducción:
1. ¿Realmente necesitas PII? ¿O solo IDs? (usa IDs)
2. Si necesitas PII:
   a. ¿Tienes Data Processing Agreement? (check with Legal)
   b. ¿La acción está documentadas? (GDPR 5.2 - legitmate interest)
   c. ¿Incryptado en reposo? (AES-256)
   d. ¿TLS en tránsito? (HTTPS)
   e. ¿Borrado después de análisis? (retention policy)
3. ¿Approved por Privacy Officer?

Si todas => Proceder SOLO bajo máximo control
Si alguna falta => NO PROCEDER
```

---

### Hard Stop Categoría 4: INESTABILIDAD / RIESGO DE OUTAGE

**Señal**: Acción que podría caer un servicio en producción
**Respuesta**: STOP, requiere ventana autorizada
**Reconducción**: Scheduling + monitoring + rollback

**Ejemplo**:
```
Usuario: "Actualiza el firewall de producción durante el día"
ORION: ❌ STOP (a no ser que sea EMERGENCIA)

Razones:
1. Cambios de firewall = riesgo de outage
2. Durante horario de negocio = impacto máximo
3. Sin monitoring de SOC = sin darse cuenta si se rompe

Reconducción:
1. ¿Es EMERGENCIA? (breach activo, DDoS)
   - SI => Proceder, documentar después
   - NO => Esperar ventana
2. Si no emergencia:
   - Cambios en STAGING primeiro (full testing)
   - Schedule en non-business hours (22:00-06:00)
   - SOC monitoring activo + on-call engineer
   - Pre-planned rollback (< 5 minutos)
   - Post-change: Log + validation (1 hora)

Si cumplen => Proceder
Si no => Posponer
```

---

### Hard Stop Categoría 5: CADENA DE CUSTODIA COMPROMETIDA

**Señal**: Evidencia ha sido alterada, tocada por persona no-auditada, etc.
**Respuesta**: STOP, re-colectar evidencia desde cero
**Reconducción**: Documentar qué pasó, lecciones aprendidas

**Ejemplo**:
```
Usuario: "Encontré este log de incidente. Lo copié a mi laptop personal, lo modifiqué en Excel..."
ORION: ❌ STOP

Razones:
1. Chain of custody roto
2. Original corrupted (Excel cambió formatos)
3. No probable en court of law

Reconducción:
1. Archivo original:
   - Copia BIT-A-BIT de fuente (forensic image, no copy-paste)
   - Hashear con SHA-256 (verificación de integridad)
   - Guardar en evidence locker (encriptado, access logged)
2. Working copy:
   - En máquina dedicada (forensic workstation)
   - Read-only mount
   - Todo cambio documentado (timeline)
3. Herramientas:
   - Volatility para memory
   - FLS / Autopsy para disk
   - `openssl dgst -sha256 file` para hash
4. Reportar:
   - Original hash + archivo
   - Análisis realizado
   - Datetime + persona

Si todo OK => Proceder
Si chain roto => No usable como evidencia
```

---

## PARTE 4: CÓMO ACTIVAR ORION (MATRIZ DE DECISIÓN) (900-1200 líneas)

### Pregunta 1: ¿Hay autorización escriba explícita?

```
¿Tengo ToR (Terms of Reference) firmado?
├─ SÍ
│  └─ ¿Está actualizado? (no >6 meses antiguo)
│     ├─ SÍ → Proceder a Pregunta 2
│     └─ NO → Refresco ToR primero
│
├─ NO
│  └─ ¿Tengo autorización verbal + email de CISO/CTO?
│     ├─ SÍ → Usa como ToR temporal, formalizalo dentro 5 días
│     └─ NO → STOP. Obtener autorización antes de continuar
│
└─ EMERGENCIA (incidente activo)
   └─ Proceder, documentar después
```

---

### Pregunta 2: ¿Qué tipo de tarea es?

Usa **DOMAIN_TAXONOMY.md** para clasificar:

```
¿Qué dominio principal aplica?

GOVERNANCE (1)
├─ Autorización / políticas
├─ Compliance / frameworks
├─ Risk assessment
└─ Referencia: 01, 02, 25

SUPERFICIE TÉCNICA (2)
├─ WEB/API → Playbook 02, Ref 06
├─ CLOUD/K8S → Playbook 03, Ref 08
├─ IDENTITY → Ref 09
├─ NETWORK → Ref 04, 10
├─ DATA/PRIVACY → Ref 19, 18
└─ MOBILE → Ref 17

INGENIERÍA (3)
├─ SDLC → Playbook 05, Ref 13
├─ IaC → Ref 13, playbook 03
├─ Supply chain → Ref 20
└─ CRYPTO → Ref 18

DEFENSA (4)
├─ Detection → Playbook 04, Ref 12
├─ DFIR → Playbook 06, Ref 11
├─ SOC ops → Ref 21
└─ Hardening → Todas las refs

AGENTIC (5)
├─ Code gen → Ref 03, 31
├─ Execution → Ref 03
└─ Safety → Ref 31
```

---

### Pregunta 3: ¿Cuál es el TIEMPO disponible?

```
¿Cuánto tiempo tengo?

4-6 HORAS → Modo RÁPIDO
├─ Playbook relevante (versión express)
├─ Superficies principals
├─ Quick wins
└─ Entrega: Top-10 hallazgos

1-2 SEMANAS → Modo ESTRUCTURADO
├─ Playbook completo
├─ Cobertura multi-dominio
├─ Analysis + prioritization
└─ Entrega: Reporte + roadmap

3-12 SEMANAS → Modo HARDENING
├─ Assessment + diseño
├─ Implementación guidance
├─ Scripts + automation
└─ Entrega: Completo + training

PERMANENTE → Modo CONTINUO
├─ Ciclos mensuales/trimestrales
├─ Mejora incremental
└─ Entrega: Trending + reports

0-4 HORAS (EMERGENCIA) → Modo INCIDENT
├─ Playbook 06
├─ Preserve evidence → triage → analysis
└─ Entrega: IR report + EOCs
```

---

### Pregunta 4: ¿Cuál es el RIESGO?

```
¿Qué puede salir mal?

BAJO RIESGO (lectura, reporting, planning)
├─ No tocar sistemas vivos
├─ No escribir cambios
├─ Auditor: 1 persona OK
└─ Aprobación: CISO suficiente

MEDIANO RIESGO (validación, cambios no-críticos)
├─ Afecta non-prod o low-traffic systems
├─ Cambios con rollback
├─ Auditor: debe tener ops backup
└─ Aprobación: CTO + VP Ops

ALTO RIESGO (producción, cambios estructura, datos)
├─ Afecta sistemas vivos / datos críticos
├─ Downtime risk
├─ Auditor: MÍNIMO 2 personas
├─ SOC monitoring required
└─ Aprobación: CEO / Board

CRÍTICO RIESGO (STOP o escalada)
├─ No reversible
├─ Daño legal/compliance
├─ Auditado por autoridad externa
└─ Requiere CISO + LEGAL + CEO
```

---

### Pregunta 5: ¿CUÁLES SON LOS GUARDRAILS?

**Guardrail = Límite que NO puedes cruzar**

```
USUARIO ENTRA EN TERRITORIOS PELIGROSOS? STOP Y EXPLICA:

Usuario: "Quiero test de DDoS contra nuestra infraestructura"
ORION Guardrail:
  ❌ DDoS = ilegal sin explicit contract (CFAA en USA)
  ✅ Alternativa: Load testing (gradual, controlled, pre-announced)

Usuario: "Quiero un backdoor para acceso futuro"
ORION Guardrail:
  ❌ Backdoor = persistence = malware
  ✅ Alternativa: Documentar ruta de remediación, dejar acceso normal

Usuario: "Quiero acceso a datos de clientes para análisis"
ORION Guardrail:
  ❌ Sin anonimización + compliance = GDPR violation
  ✅ Alternativa: Anonymize, segregate, control access + log

Guardrails clave:
1. Nunca sin autorización
2. Nunca productión sin remote control + rollback
3. Nunca PII sin Privacy Officer approval
4. Nunca persistence / backdoor
5. Nunca destructive sin confirmación triple
6. Nunca exfiltración (datos fuera de cliente)
7. Nunca sin evidencia trail
8. Nunca evasión de controles INTERNOS del cliente
```

---

## PARTE 5: FLUJOS DE DECISIÓN Y EJEMPLOS REALES (1200-1500 líneas)

### FLUJO 1: Assessment Web App (Caso Real)

```
USUARIO: "Quiero que audites mi API de compras"

ORION PIPELINE:

1. CLASIFICACIÓN
   ├─ Dominio: Web/API (Domain 2)
   ├─ Tipo: Review seguridad
   ├─ Modo: ESTRUCTURADO (5 días)
   └─ Playbook: 02-web-api-review

2. AUTORIZACIÓN CHECK
   ├─ ¿ToR? SI, firmado CTO + Compliance
   ├─ Scope: api.mycompany.com + staging
   ├─ Restricciones: No modificar datos clientes, no DoS
   └─ Timeline: 5 días laborales, 9-17 EST

3. ACCESO VALIDATION
   ├─ ¿Puedo acceder? → Request staging account
   ├─ ¿Tengo herramientas? → Burp, curl, python
   └─ ¿Baseline documented? → Snapshots de responses conocidas

4. EJECUCIÓN (Playbook 02)
   
   DÍA 1: RECON
   ├─ Enumerar endpoints
   ├─ Identificar autenticación (Bearer? OAuth? API key?)
   ├─ Mapear dependencias DB
   └─ Output: api-inventory.json
   
   DÍA 2-3: TESTING (OWASP Top 10)
   ├─ AUTH: ¿Qué pasa sin token? ¿Scopes correctos? ¿Expiration?
   ├─ INJ: SQLi, NoSQLi, XXE, SSTI
   ├─ LOGIC: Age verification, price manipulation, rate limiting
   ├─ CORS: ¿Permitido el origen equivocado?
   ├─ CRYPTO: ¿Tan hashes? ¿Algoritmos débiles?
   └─ Output: findings.json
   
   DÍA 4: ANALYSIS
   ├─ De-duplicate findings
   ├─ Prueba false positives
   ├─ CVSS scoring
   └─ Priorización (CVSS + effort + business impact)
   
   DÍA 5: REPORT
   ├─ Executive summary (1 página)
   ├─ Top 10 hallazgos
   ├─ Roadmap 30-90 días
   ├─ Scripts de remediación ejemplos
   └─ Presentación walkthrough

5. SALIDA
   ├─ API Inventory (JSON)
   ├─ Findings (JSON normalizado)
   ├─ Reporte (PDF)
   ├─ PoCs (curl commands, videos críticos)
   └─ Evidence archive (encrypted)
```

---

### FLUJO 2: Incident Triage (Caso Real - Breach Activo)

```
USUARIO: "¡TENEMOS UN INCIDENTE! Login raro en production"

ORION PIPELINE:

FASE 0 (15 MINUTOS): ACTIVACIÓN + ESCALADA

├─ PRESERVE EVIDENCIA:
│  ├─ Memory dump de máquina afectada
│  ├─ Network capture (firewall)
│  ├─ Log archive (antes de rotation)
│  └─ Screenshot de estado actual
│
├─ ESCALATE INMEDIATO:
│  ├─ CTO: Autoridad técnica
│  ├─ CISO: Autoridad de riesgo
│  ├─ Legal: Autoridad de notificación
│  └─ CEO: Authority de decisión
│
└─ START LOGGING:
   └─ Timestamp cada acción, quién, qué, resultado


FASE 1 (2 HORAS): TRIAGE

├─ Preguntas críticas:
│  ├─ ¿Solo 1 máquina o múltiples?
│  ├─ ¿Qué datos están en riesgo? (PII? IP? Code?)
│  ├─ ¿Attacker aún activo? (check firewall logs)
│  ├─ ¿Qué causó el acceso? (phishing? exploit? credential?)
│  └─ ¿Timeout para escalation?
│
├─ Scope estimation:
│  ├─ 1 máquina → Risk LOW
│  ├─ 3+ máquinas → Risk MEDIUM
│  ├─ Multiple users → Risk HIGH
│  └─ Database breach → Risk CRÍTICO
│
├─ Immediate containment:
│  ├─ Block outbound IPs (firewall)
│  ├─ Reset passwords (affected users)
│  ├─ Revoke API keys/tokens
│  └─ Isolate machines (if needed)
│
└─ Output: Triage summary


FASE 2 (24 HORAS): INVESTIGATION

├─ Timeline reconstruction:
│  ├─ Logs: Sysmon, EDR, firewall, application
│  ├─ Find: entrada (attack entry point)
│  ├─ Build: paso-a-paso qué pasó
│  └─ Output: Timeline.txt con timings preciso
│
├─ Artifact analysis:
│  ├─ Memory: volatility (processes, network connections)
│  ├─ Disk: carving (deleted files, alternate streams)
│  └─ Malware (si aplica): static + behaviors
│
├─ IOC extraction:
│  ├─ IPs del attacker
│  ├─ Domains (C2)
│  ├─ File hashes
│  ├─ MITRE ATT&CK mapping
│  └─ Output: iocs.json
│
└─ Impact assessment:
   ├─ Qué data fue accesed/copied?
   ├─ Cuántos records? (PII notification trigger)
   ├─ Compliance implicaciones
   └─ Financial impact estimate


FASE 3 (48 HORAS): REMEDIATION

├─ IMMEDIATE (0-4 hours):
│  ├─ Patch exploited vulnerability (si conocido)
│  ├─ Force password reset (afectado users)
│  └─ Block IOCs (firewall + EDR + SIEM)
│
├─ SHORT-TERM (1-2 weeks):
│  ├─ Re-image affected máquinas (clean image)
│  ├─ Verify backups are clean
│  ├─ Patch all systems (not just affected)
│  └─ Validated: attack no puede re-ocurrir
│
└─ LONG-TERM (2-12 weeks):
   ├─ Root cause: ¿Por qué fue vulnerable?
   ├─ Defense gaps: ¿Por qué no lo detectamos?
   ├─ Process improvements
   └─ Team training


FASE 4 (2-4 WEEKS): POST-INCIDENT

├─ Reportes:
│  ├─ Full incident report (20-50 pages)
│  ├─ Forensic analysis
│  ├─ Compliance notification
│  └─ Lessons learned
│
├─ Red team test:
│  └─ "¿Puedo comprometerlos de nuevo de la misma forma?" NO
│
└─ Updates:
   ├─ Incident response plan
   ├─ Playbooks
   └─ Security training
```

---

### FLUJO 3: SDLC Review (Caso Real - Setup para Seguridad)

```
USUARIO: "Quiero que la seguridad sea parte de mi pipeline"

ORION PIPELINE:

1. ASSESSMENT ACTUAL
   ├─ Repos (donde código):
   │  └─ Enumeración: cuántos repos, lenguajes, frameworks
   │
   ├─ Pipeline (cómo se deploya):
   │  ├─ Branches, approvals, testing gates
   │  └─ Environment (dev, staging, prod)
   │
   ├─ Tools actuals:
   │  └─ Linters, tests, deployments
   │
   └─ Guardrails existentes:
      └─ Ningunas, algunas, o completos?

2. GAPS IDENTIFICADOS
   ├─ SAST (código scanning):
   │  ├─ ¿Tenemos SonarQube? → NO
   │  ├─ Necesitamos: análisis estático antes de merge
   │  └─ Tool sugerido: Semgrep (libre, rápido)
   │
   ├─ SCA (dependencias):
   │  ├─ ¿Tenemos scanner de vulnerabilidades? → NO
   │  ├─ Necesitamos: detectar CVEs en dependencias
   │  └─ Tool sugerido: OWASP Dep-Check (libre)
   │
   ├─ Secrets (credenciales):
   │  ├─ ¿Tenemos scanner de secrets? → NO
   │  ├─ Necesitamos: prevenir commit de api keys / passwords
   │  └─ Tool sugerido: Pre-commit hook con TruffleHog
   │
   ├─ IaC (terraform, helm):
   │  ├─ ¿Tenemos validación de IaC? → NO
   │  ├─ Necesitamos: security linting antes de apply
   │  └─ Tool sugerido: Checkov
   │
   └─ Code review:
      ├─ ¿Mínimo 2 reviewers? → Solo 1
      ├─ ¿Requiere approval de security? → NO
      └─ Arreglado: Update CODEOWNERS, agregar security team

3. IMPLEMENTACIÓN
   
   SEMANA 1: Setup tools
   ├─ Semgrep: GitHub Action (5 min setup)
   │  ```yaml
   │  - uses: returntocorp/semgrep-action@v1
   │    with:
   │      config: >-
   │        p/security-audit
   │  ```
   │
   ├─ TruffleHog: Pre-commit (10 min)
   │  ```bash
   │  pip install truffleHog
   │  # Add to .git/hooks/pre-commit
   │  ```
   │
   └─ OWASP Dep-Check: GitHub Action (5 min)
   
   SEMANA 2: Integrate into pipeline
   ├─ All tools run on PR
   ├─ Failing SAST → PR blocked
   ├─ Secrets detected → Alert
   └─ SCA vulns high+critical → Review required
   
   SEMANA 3: Training
   ├─ Dev team: "Cómo run locally antes de commit"
   ├─ Security team: "Cómo override alarmas falsas"
   └─ Examples: código vulnerable vs seguro
   
   SEMANA 4: Monitoring
   ├─ Weekly report: # of vulns, # of overrides
   ├─ Metrics: DevOps vs security speed trade-off
   └─ Adjust: gates too strict?

4. SALIDA
   ├─ Pipeline mejorado con 4 gates security
   ├─ Training documentation
   ├─ Metrics dashboard
   └─ Roadmap:  90d plans para SonarQube + artifact signing
```

---

### EJEMPLO REAL 4: Cloud Hardening (AWS)

```
CLIENTE: "Mi arquitectura AWS está insegura. Ayuda."

ORION STEPS:

1. DISCOVERY (1 día)
   $aws ec2 describe-instances → 45 instances
   $aws s3 ls → 23 buckets
   $aws iam list-users → 120 users
   $aws iam list-roles → 67 roles
   
   Output: cloud-inventory.json

2. GAP ANALYSIS (1 día)
   ├─ IAM:
   │  ├─ Root account tiene access keys ❌
   │  ├─ Wildcard (*) en algunas policies ❌
   │  └─ No MFA en console ❌
   │
   ├─ Storage:
   │  ├─ S3 bucket público accidental ❌
   │  └─ No encryption en RDS ❌
   │
   ├─ Networking:
   │  ├─ Security group abierto a 0.0.0.0/0 en 443 ❌
   │  └─ No VPC Flow Logs ❌
   │
   └─ Output: findings.json + CIS benchmark mapping

3. QUICK WINS (2-3 horas)
   ├─ Habilitar MFA en root
   ├─ Block S3 public access
   ├─ Rotación de access keys viejos
   └─ Output: terraform plan que arregla estos

4. STRATEGIC (2-4 semanas)
   ├─ Architecture redesign:
   │  ├─ Public tier (NAT, bastión)
   │  ├─ Private tier (apps, DBs)
   │  └─ Isolated tier (secrets)
   │
   ├─ IAM redesign:
   │  ├─ Roles per team
   │  ├─ Least privilege by default
   │  └─ Audit logging
   │
   ├─ Network redesign:
   │  ├─ VPC per env
   │  ├─ Security groups por purpose
   │  └─ NACLs restrictive
   │
   └─ Output: Terraform modules + deployment guide

5. VALIDATION
   └─ Prowler re-run: antes 45 findings, ahora 5 (todos LOW)
```

---

## PART 6: FAQ DETALLADO & TROUBLESHOOTING (1500-1700 líneas)

### FAQ 1: "¿Puedo usar ORION sin ToR?"

**Respuesta corta**: NO. Hard stop.

**Respuesta larga**:
```
ToR (Terms of Reference) es no-negotiable porque:

1. LEGAL PROTECTION:
   - Sin autorización explícita = potencialmente breaking la ley (CFAA en USA)
   - ToR es tu defensa ("Was authorized")
   - Sin ToR = "Hacking sin permiso" = criminal

2. ÉTICA:
   - ORION es para AUTHORIZED security work
   - Penetración no autorizada ≠ security audit

3. OPERACIONAL:
   - Sin ToR = sin scope claro
   - Sin scope = sin boundaries
   - Sin boundaries = risk de escalation

CÓMO OBTENER ToR:
├─ Talk a CTO/CISO/Security Lead
├─ Email: "Necesito autorización para [acción específica] en [sistemas]"
├─ Specificar: ¿qué? ¿dónde? ¿cuándo? ¿cuánto tiempo?
├─ Obtener firma
└─ Guardar copia

EMERGENCY EXCEPTION:
Si hay breach ACTIVO:
├─ Procede (documenta después)
├─ Avisa a CTO/CISO INMEDIATAMENTE
├─ Formaliza ToR dentro 4 horas
└─ Post-incident: full documentation
```

---

### FAQ 2: "¿Qué es 'máximo riesgo aceptable'?"

**Respuesta corta**: Depende del cliente, documentado en ToR.

**Respuesta larga**:
```
RIESGO vs BENEFIT ANALYSIS:

BAJO RIESGO (permitted):
├─ Lectura de logs (no modificación)
├─ Scanning pasivo (no active exploitation)
├─ Testing en staging (no producción)
├─ Alertas falsas (no downtime real)
└─ Owner: CISO OK sufficient

MEDIUM RIESGO (permitted, con cuidado):
├─ Validación activa en sistemas deTesting
├─ Cambios de configuración (rollbackable)
├─ Breve impacto (< 30 min expected)
├─ Owner: VP Ops OK required
└─ Mitigation: SOC monitoring + on-call engineer

ALTO RIESGO (escalada requerida):
├─ Cambios en producción
├─ Modificación de datos
├─ Riesgo de downtime significativo
├─ Owner: CTO + CEO approval
└─ Mitigation: Full testing en staging + rollback plan < 5 min

CRÍTICO RIESGO (STOP):
├─ No reversible
├─ Daño legal/compliance
├─ Potencial pérdida financiera
└─ Owner: STOP unless CISO + CEO explicitly approve
```

---

### FAQ 3: "¿Hago brute force contra login?"

**Respuesta corta**: Solo en muy specific scenarios con maxamás cuidado.

**Respuesta larga**:
```
CUÁNDO BRUTE FORCE ES VÁLIDO:
├─ Testing de password policy (¿6 char min? → bruteforced "abc123")
├─ Validación de rate limiting
└─ En STAGING, con credenciales conocidas de test

CUÁNDO BRUTE FORCE ES BUSCADO PROBLEMA:
├─ Contra usuarios reales
├─ Contraseña desconocida
├─ Sin automización (manual testing = OK, scripted = PROBLEM)
├─ Sin rate limiting (blocked acounts)
└─ Horario de negocio (impact en usuarios reales)

CÓMO HACERLO CORRECTAMENTE:
1. Obtener autorización explícita en ToR
2. Crear usuario de TEST dedicado
3. Usar contraseña CONOCIDA (no real guess)
4. Rate limite lenta (1 intento / 5 segundos)
5. Non-business hours
6. SOC notificado (explica qué pasa)
7. Maximum 10 intentos (si fail, stop)
8. Documentar resultado
9. Cleanup: eliminar usuario test
10. Report: "Rate limiting effective / weak?"

EJEMPLO:
```bash
#!/bin/bash
# Test account password policy

TEST_USER="automation_test_12345"
TEST_PASS="TempPass123!@#$Y2024"

for i in {1..3}; do
  echo "Attempt $i..."
  curl -X POST https://app.local/login \
    -d "username=$TEST_USER&password=TempPass123" \
    --max-time 5 \
    --silent
  sleep 5  # Rate limit: 1 attempt per 5 seconds
done
```
```

---

### FAQ 4: "¿Cuánto tiempo toma 'assessment'?"

**Respuesta corta**: 4 horas a 12 semanas, depende scope.

**Respuesta larga**:
```
TIMELINE POR COMPLEJIDAD:

LANDING PAGE (4-8 hours)
├─ Recon: 1 hora
├─ Testing: 2 horas
├─ Report: 1 hora
└─ Typical: Small site, few endpoints

SINGLE APP / API (2-5 days)
├─ Recon: 4 horas
├─ Testing: 3 días (OWASP Top 10)
├─ Report: 1 día
└─ Typical: 30-50 endpoints, auth required

MULTI-DOMAIN (2-4 weeks)
├─ Phase 1 (web): 1 semana
├─ Phase 2 (cloud): 1 semana
├─ Phase 3 (identity): 3 días
├─ Phase 4 (network): 3 días
└─ Typical: Full company assessment

ARCHITECTURE + IMPROVEMENT (3-12 semanas)
├─ Fases 1-4: 4 semanas
├─ Arquitectura diseño: 2 semanas
├─ Implementación guidance: 4 semanas
├─ Training: 1 semana
└─ Typical: Transformación seguridad de compañía

FACTORS QUE AFECTAN:
├─ Scope size (1 vs 100 servers)
├─ Complexity (simple API vs distributed cloud)
├─ Documentation (¿existe o tenemos que descubrir?)
├─ Access (VPN, MFA, 2FA = delays)
├─ Auditor skill (experto vs junior = 10x difference)
└─ Budget (rushed = expensive + mistakes)
```

---

### FAQ 5: "¿Cómo reporto sin alertar attacker?"

**Respuesta corta**: Confidential report, no public disclosure.

**Respuesta larga**:
```
REPORTING OPTIONS:

Option 1: INTERNAL REPORTING SÓLO
├─ Cliente recibe reporte
├─ Cliente fixes en secreto
├─ Sin public announcement
└─ Timeline: Cliente decide (ideally 90 días)

Option 2: RESPONSIBLE DISCLOSURE
├─ Hallazgo reportado a cliente
├─ Plazo de 90 días para fix
├─ Seguidamente puedo publicar (vendor disclosure)
└─ Timeline: 90 días + publicación

Option 3: COORDINATED DISCLOSURE
├─ Hallazgo reportado a vendor
├─ Vendor reporta a CERT
├─ Embargo (secreto compartido)
├─ CVE asignado
├─ Patch released
├─ Seguidamente publicación
└─ Timeline: 90-180 días

NUNCA HACER:
├─ Public exploit sin vendor time
├─ Sharing findings en internet
├─ Selling hallazgos a competitors
├─ Using hallazgo para blackmail
└─ 0-day sin responsible disclosure

ORION APPROACH:
├─ Default: Internal + responsible disclosure
├─ Only public if vendor no responde
├─ Consultar client + legal antes de publicar
```

---

### TROUBLESHOOTING: Common Problems & Solutions

**Problem 1: "Acceso denegado a sistemas"**
```
Síntoma: No puedo loguearme al servidor/cloud/API

Causas posibles:
  - Vi Network access (VPN no funciona)
    Fix: Verificar VPN, DNS, firewall rules
  
  - Bad credentials
    Fix: Verificar con owner, reset password
  
  - MFA requerido
    Fix: Configurar MFA device, usar TOTP app
  
  - IP blockeado
    Fix: Whitelist tu IP, request con owner

Solution:
  1. Documentar error exacto
  2. Reportar a owner técnico
  3. Propiedades alternativas (staging, test account)
  4. NO intentar bypass sin permiso
```

---

**Problem 2: "Tool no funciona (Burp, Nmap, etc)"**
```
Síntoma: "Burp no se conecta", "Nmap timeout", etc

Causas posibles:
  - Network filtering (proxy, WAF)
    Fix: Direct connection if possible, ask for whitelist
  
  - Tool license expired
    Fix: Renew license, use community edition
  
  - Target down / not responding
    Fix: Verificar DNS, ping, curl antes de scan
  
  - Antivirus interfering
    Fix: Whitelist tool, use cloud scanner

Solution:
  1. Test connectivity (ping, curl, telnet)
  2. Check tool logs (-v, verbose)
  3. Compare con herramienta alterna
  4. Escalate a operaciones si needed
```

---

**Problem 3: "Hallazgo parece falso positivo"**
```
Síntoma: Tool reportó vulnerability pero no confirma manual

Causas posibles:
  - WAF blocking / sanitizing input
    Result: Tool says SQLi, pero es sanitizado
    Fix: Manual test de injection, validad context
  
  - Tool misconfiguration
    Result: False alarm
    Fix: Reconfigure tool, test conocido vulnerable target
  
  - Vulnerability real pero no explotable (edge case)
    Result: Técnicamente vulnerable pero sin impact real
    Fix: Documentar como LOW severity, not actionable

Solution:
  1. Reproduce with multiple tools
  2. Manual step-by-step verification
  3. Si no puedo probar → "Suspected" not definitive
  4. Documentar assumption + limitation
  5. Recommend verificación por vendor
```

---

## PART 7: REFERENCE RÁPIDA & RESUMEN FINAL (1700+ líneas)

### Tabla Rápida: Cuándo Usar Qué

| Situación | Playbook | Tiempo | Owner | Herramientas |
|---|---|---|---|---|
| **Solicitud ambigua** | SKILL.md + DOMAIN_TAXONOMY.md | 15 min | 1 | Ninguna |
| **Web app review** | Playbook 02 | 5 días | 2 | Burp, curl |
| **Cloud audit** | Playbook 03 | 3 días | 2 | AWS CLI, Prowler |
| **Detection rule development** | Playbook 04 | 2 semanas | 1 | SIEM, Sigma |
| **SDLC hardening** | Playbook 05 | 3 semanas | 3 | SonarQube, Snyk |
| **Incident response** | Playbook 06 | 4h-2d | 5 | EDR, SIEM, Volatility |
| **Full assessment** | Playbook 01 | 4 semanas | 5 | Todos |

---

### Hard Stops Cheet Sheet

```
❌ STOP INMEDIATO SIN EXCEPCIÓN:

1. Sin autorización explícita (ToR)
2. Acción no reversible sin remote control
3. Violación GDPR / compliance known
4. Potencial outage sin SOC monitoring
5. Chain of custody roto de evidencia
6. Persistence / backdoor detection
7. Exfiltración de datos
8. Destrucción o modificación malicioso

AÑO PROCEDER:
✅ Solo con autorización clara
✅ Con reversión / rollback plan
✅ Con monitoring / safety checks
✅ Con documentación completa
✅ Con escalación si needed
```

---

### Pyramid of ORION Understanding

```
LEVEL 4 (Master): Diseño custom, training, optimization
├─ Uso: Resolver casos complejos no-cubiertos
├─ Requisito: 100+ horas con ORION
└─ Outcome: Arquitectura seguridad mejorada

LEVEL 3 (Advanced): Audit completo, hardening, incident response
├─ Uso: Assessment multi-dominio, crisis
├─ Requisito: 50+ horas con ORION
└─ Outcome: Postura completa mejorada

LEVEL 2 (Intermediate): Web/Cloud/SDLC específico
├─ Uso: Dominio específico audit
├─ Requisito: 10+ horas con ORION
└─ Outcome: Hallazgos + roadmap specific

LEVEL 1 (Beginner): Clasificación + documentación
├─ Uso: Report bugs, básicos
├─ Requisito: 2 horas con ORION
└─ Outcome: Entiende qué domain aplica

ENTRY POINT: Este archivo (SKILL.md)
├─ Lee SKILL.md (este)
├─ Lee DOMAIN_TAXONOMY (20 min)
├─ Elige Playbook (5 min)
└─ Ejecuta (N horas)
```

---

### Reglas de Oro (5)

```
REGLA 1: Sin autorización → Sin ejecución
  Excepción: Breach activo (escalada inmediata)

REGLA 2: Auditable siempre
  Every action logged, timestamped, evidenced

REGLA 3: Reversible por defecto
  If you can't undo it → ask CISO first

REGLA 4: Ética integrada
  We secure, not attack. We defend, not harm.

REGLA 5: Transparencia total
  Documentar asunción, limitación, decisión

Si violas alguna → ORION se detiene
```

---

## CONCLUSIÓN

ORION-HACKING es tu **operating system for **authorized security work**.

No es:
- Herramienta de ataque ❌
- Método de evasión ❌
- Exploit collection ❌
- Backdoor framework ❌

ES:
- Framework documentado ✅
- Sistema de gobernanza ✅
- Metodología reproducible ✅
- Auditable completamente ✅

**Úsalo con integridad. Secure, no attack. Defend, not harm.** 🛡️

---

## PARTE 8: CASOS DE ESTUDIO AVANZADOS (1400-1550 líneas)

### Caso de Estudio 1: Transición a DevSecOps desde Zero

**Contexto**: Empresa de 50 developers, sin controles de seguridad en pipeline, 15+ vulnerabilidades en producción descubiertas en último auditoría externa.

**Desafío**:
- Developers resisten cambios
- Tiempo limitado (3 meses hasta regulación)
- Herramientas antiguas (no automatizadas)
- Cultura de "velocity over security"

**Solución ORION**:

```
FASE 1 (Semana 1-2): BASELINING
├─ Auditoría actual (Playbook 05 express)
├─ Inventario: repos, lenguajes, pipeline tools
├─ Vulnerabilidades existentes en main branch
├─ Output: baseline report + risk matrix

FASE 2 (Semana 3-4): QUICK WINS
├─ Semgrep + pre-commit hook (prevents new vulns)
├─ TruffleHog (prevents secrets leak)
├─ npm audit / pip audit (SCA básico)
├─ Output: 3 gates implementadas
├─ Dev impact: +2-3 min per commit (aceptable)

FASE 3 (Semana 5-8): PROFUNDIZACIÓN
├─ SonarQube integration (SAST avanzado)
├─ Snyk (SCA + vulnerability tracking)
├─ Policy-as-code (Checkov para IaC)
├─ Training: developer + security
├─ Output: 6 gates + metrics dashboard

FASE 4 (Semana 9-12): CONSOLIDACIÓN
├─ Metrics review: false positive rate, remediation time
├─ Tuning gates (no romper velocity)
├─ Incident response testing
├─ Board reporting: antes 15 vulns, ahora 2
```

**Métricas de éxito**:
- Vulnerabilidades nuevas: 0 en 3 meses
- Remediation time: 7 días → 2 días
- Developer satisfaction: "not blocking" si test pasa
- Security team workload: -40% triaging

---

### Caso de Estudio 2: Compliance Audit (HIPAA) - Desde Zero a Certificado

**Contexto**: Healthcare SaaS, manejan datos de pacientes (PHI), sin compliance, auditado por terceros en 6 meses.

**Desafío**:
- HIPAA = 500+ requisitos
- Implementación compleja + cara
- Downtime prohibido
- Pacientes dependen de sistema

**Solución ORION**:

```
STEP 1: ANÁLISIS DE BRECHA (Reference 25 + 01)
├─ Mapeo: 500 reqs HIPAA → 150 actionable items
├─ Categorización: Critical (30), High (50), Medium (70)
├─ Timeline realista: Critical (4 semanas), High (8 semanas)
└─ Output: gap report + roadmap + estimated cost

STEP 2: IMPLEMENTACIÓN PROGRESIVA
├─ Critical (4 semanas):
│  ├─ encryption at rest (Easy, low risk)
│  ├─ encryption in transit (TLS everywhere)
│  ├─ access logging (SIEM)
│  └─ Validation: HIPAA audit tool
│
├─ High (8 semanas):
│  ├─ RBAC (role-based access control)
│  ├─ Segregation (PHI in separate database)
│  ├─ Key rotation (automated)
│  └─ Validation: Penetration test
│
└─ Medium (ongoing):
   ├─ PII data masking in non-prod
   ├─ Backup encryption
   ├─ Audit trail for 6 years
   └─ Compliance monitoring

STEP 3: EVIDENCE COLLECTION
├─ Policy documentation (26 docs)
├─ Control implementation evidence
├─ Audit logs (6 months)
├─ Risk assessment report
├─ Privacy notice + consent forms
└─ Incident response plan + testing

STEP 4: EXTERNAL AUDIT PREPARATION
├─ Mock audit (auditor externo, pero no-oficial)
├─ Remediation de gaps encontrados
├─ Final documentation review
├─ Staff training (2 horas HIPAA)
└─ Official audit readiness
```

**Costo-beneficio**:
- Implementación: $300K (security team + tooling)
- Cost of breach: $4.24M promedio (HIPAA)
- Resultado: Compliance certificada + defensible ante auditoría

---

### Caso de Estudio 3: Incident Response Real (APT Scenario)

**Contexto**: Empresa detecta actividad anómala en servidor producción. Log muestra conexión SSH de IP desconocida. Miedo a que sea breach real.

**Diagnosis**:

```
HORA 0:00 - ACTIVACIÓN
├─ ALERT: "Suspicious SSH login from 203.0.113.200"
├─ IMMEDIATE: SOC iza banner + notifica CTO
├─ ACTION: IP bloqueado en firewall
├─ QUESTION: ¿Qué máquina? ¿Logueo exitoso? ¿Archivos modificados?

HORA 0:15 - TRIAGE
├─ Máquina: prod-app-3 (web app server, high value)
├─ Login: Intento fallido (password rejecto)
├─ Impacto: Ninguno (login fracasó)
├─ Scope: ¿Otros intentos? → Buscar en logs últimas 7 días
└─ OUTPUT: Risk = MEDIUM (intento fallido, pero reconnaissance activa)

HORA 2:00 - INVESTIGATION
├─ Log analysis: 47 SSH attempts en 3 días (IP 203.0.113.200)
├─ Scanning: "nmap" desde IP hacía red (confirmado)
├─ Password attempts: Diccionario pequeño (3-4 passwords comunes)
├─ Interpretación: Scanning automatizado, no target-specific

HORA 6:00 - ASSESSMENT
├─ ¿Breach?
│  └─ NO: Login nunca exitoso, archivos intactos
│
├─ ¿Reconnaissance?
│  └─ SÍ: Attacker mapeó red, buscó vulnerabilidades
│
├─ ¿Próximo paso?
│  └─ "Likely movimiento lateral o brute force will continue"
│
└─ RISK LEVEL: Medium (reconnaissance activa, no explotación aún)

HOUR 24:00 - RESPONSE PLAN
├─ IMMEDIATE:
│  ├─ Mantener IP bloqueada
│  ├─ Aumentar monitoring en prod-app-3
│  ├─ Password force reset (all users on affected server)
│  └─ Enable MFA (si no existe)
│
├─ SHORT-TERM (1 week):
│  ├─ Scan de vulnerabilidades (Nessus, Qualys)
│  ├─ Patch de OS + apps
│  ├─ Network segmentation (prod aislado de dev)
│  └─ Validate no other servers compromised
│
└─ LONG-TERM (1 month):
   ├─ Root cause: ¿IP pública con SSH abierto? (BAD)
   ├─ Fix: Bastion host + VPN required para SSH
   ├─ Detection: Sigma rule para multi-failed SSH
   └─ Training: Team en incident response
```

**Outcome**:
- Breach = NO (ataque repelido)
- Vulnerabilidad expuesta = SÍ (SSH público sin MFA)
- Lesson learned = Implementar bastion + VPN (1 day effort)
- Cost avoided = 0 (sin datos expuestos)

---

### Caso de Estudio 4: Pentesting Estructurado (Red Team Exercise)

**Contexto**: Empresa quiero validar defenses. Contrata red team para "ataque" autorizado.

**Preparación**:

```
PRE-ENGAGEMENT (1 semana antes)
├─ ToR signado (específico: "simulate APT targeting company")
├─ Scope explícito:
│  ├─ in-scope: AWS infrastructure, employee credentials, phishing
│  ├─ out-of-scope: Client data, DOS, persistence, exfiltration
│  └─ Hours: Business hours only (easier to debug if breaks)
│
├─ POC assigned:
│  ├─ Technical: CTO
│  ├─ Communications: CISO
│  ├─ Incident response: IR lead
│  └─ Rules of engagement familiarity
│
└─ Baseline: Asset inventory, known vulnerabilities, detection rules

ENGAGEMENT (2 weeks)

Initial access vector: Phishing email
├─ Email enviado a 50 employees
├─ Target: Credenciales de Office 365
├─ Result: 12 click (24% success rate)
└─ Lesson: "Phishing training needed"

Post-compromise: Lateral movement
├─ Tool: Mimikatz (passhash dumping)
├─ Target: Domain admin account (if possible)
├─ Obstacles: MFA on admin (GOOD)
└─ Alternative: Service account exploitation (FOUND)

Post-exploitation
├─ Access: AWS console (vía service account)
├─ Finding: S3 bucket public + customer data exposed
├─ Exposure: 500K records × 24 hours
└─ Severity: CRITICAL

POST-ENGAGEMENT (3 days)
├─ Findings prioritized:
│  ├─ CRITICAL: S3 bucket public (fix: 30 min)
│  ├─ HIGH: Service account permissive (rotation + scope)
│  ├─ MEDIUM: Phishing training effectiveness
│  └─ LOW: Recommendations for hardening
│
├─ Remediation timeline:
│  ├─ Day 1: Fix S3 (critical)
│  ├─ Day 2: Validate (red team re-tests)
│  ├─ Week 1: Service account hardening
│  └─ Month 1: Phishing + MFA mandatory
│
└─ Metrics:
   ├─ Time to detection: 20 mins (SOC alert)
   ├─ Time to containment: 60 mins (firewall block)
   ├─ Cost of remediation: $20K (worth it vs $5M breach)
   └─ Team confidence: "We can catch attackers"
```

---

## PARTE 9: MASTER CHECKLIST PARA AUDITOR (1550-1700 líneas)

Usa este checklist ANTES de cada engagement:

```markdown
# PRE-ENGAGEMENT CHECKLIST (ORION-HACKING)

## AUTORIZACIÓN & LEGAL (NO PROCEDER SIN ESTO)
- [ ] ToR firmado por cliente (CTO, Compliance, Legal)
- [ ] ToR especifica: qué, dónde, cuándo, cuánto tiempo
- [ ] Insurance verificado (errors & omissions, cyber liability)
- [ ] Confidentiality agreement (NDA) en lugar
- [ ] Contact info documentado (escalation contacts)

## SCOPE & RESTRICTIONS
- [ ] In-scope systems explícitamente listados
- [ ] Out-of-scope systems explícitamente listados
- [ ] Restricciones documentadas:
  - [ ] Sin producción? SI / NO / VENTANA ESPECÍFICA
  - [ ] Sin datos clientes? SI / NO / MASKED OK
  - [ ] Sin DoS? SI / NO / LOAD TESTING OK
  - [ ] Sin persistence/backdoor? SI (always)
  - [ ] Sin exfiltración? SI (always)
  - [ ] Horarios? (business vs anytime)
- [ ] Escalation contacts asignados

## RIESGO ASSESSMENT
- [ ] Risk level estimado: LOW / MEDIUM / HIGH / CRITICAL
- [ ] Rollback plans para cada action (if applicable)
- [ ] Success criteria definidos
- [ ] Failure scenarios documentados
- [ ] Key dependencies identificadas
- [ ] Change freeze windows respetados

## ACCESO & CREDENCIALES
- [ ] Acceso solicitado (VPN, accounts, API keys)
- [ ] Credentials guardadas seguramente (password manager, encrypted)
- [ ] MFA configurado (if required)
- [ ] IP whitelist requestado (if behind firewall)
- [ ] Testing access validated (can I reach scope?)

## HERRAMIENTAS & SETUP
- [ ] Tools instaladas y licensed:
  - [ ] Burp / ZAP (web scanning)
  - [ ] Nmap (network mapping)
  - [ ] Custom scripts (testing)
  - [ ] Cloud CLI tools (AWS/Azure/GCP)
  - [ ] SIEM access (if applicable)
- [ ] Networking validated (can reach targets)
- [ ] Firewall rules adjusted (if needed)

## DOCUMENTACIÓN & EVIDENCE
- [ ] Evidence repo creado (encrypted, access logged)
- [ ] Logging setup definido (toda acción será logged)
- [ ] Screenshot procedure documented
- [ ] PoC script template prepared
- [ ] Report template ready (executive + technical)

## TEAM & COMMUNICATION
- [ ] Auditor(s) asignado(s) y disponible(s)
- [ ] Technical POC (cliente) se conoce
- [ ] Security POC (cliente) se conoce
- [ ] IR lead (cliente) se conoce
- [ ] Kick-off meeting completado
- [ ] Communication plan establecido (daily updates? weekly?)

## ENGAGEMENT RULES
- [ ] Ethical guidelines repasadas
- [ ] Hard stops understood by team
- [ ] Escalation matrix documentada
- [ ] Decision authority clarificada
- [ ] Rules of engagement signed

## GO / NO-GO DECISION
- [ ] ¿Todos los items arriba: completados? SI / NO
- [ ] ¿Risk mitigado adecuadamente? SI / NO
- [ ] ¿Cliente list? SI / NO
- [ ] ¿Team prepared? SI / NO

**DECISION: ☐ GO (proceder) / ☐ NO-GO (esperar)**

---
```

## PARTE 10: MATRIZ DE REMEDIACIÓN INTEGRADA (1650-1700 líneas)

Cuando encuentres hallazgos, usa esta matriz para priorización:

```
MATRIZ DE PRIORIZACIÓN (RISK × EFFORT × TIME-TO-EXPLOIT)

Hallazgo: SQL Injection en /api/payment

Dimensión 1: CVSS SCORE
├─ Base: 8.2 (Network, No Auth, Integrity + Availability)
├─ Temporal: 8.0 (No exploit code public)
├─ Environmental: 9.5 (Affects payment data = PCI-DSS)
└─ ==> Severity: CRITICAL (9.5)

Dimensión 2: ATTACK SURFACE
├─ Exposed? SI (public endpoint, no auth)
├─ Authenticated? NO
├─ User interaction? NO
├─ Complexity: LOW (simple UNION injection)
└─ ==> Exploitability: HIGH

Dimensión 3: BUSINESS IMPACT
├─ Data exposure? SI (50K payment records)
├─ Revenue impact? SI (customer trust lost, regulatory fines)
├─ Estimated cost of breach? $5M (data + reputation + GDPR fines)
└─ ==> Business Risk: EXTREME

Dimensión 4: REMEDIATION EFFORT
├─ Quick fix (prepared statement)? SI, 4 hours
├─ Validation effort? 2 hours (re-test + code review)
├─ Deployment? 1 hour (CI/CD automated)
├─ Total effort: 7 hours
└─ ==> Feasibility: EASY

Dimensión 5: TIME-TO-EXPLOIT
├─ ¿Puede attacker explotar ya? SI (endpoint visible)
├─ ¿Hay mitigation? PARTIAL (WAF rules, pero débil)
├─ ¿Hay detection? NO (no alert rule yet)
└─ ==> Urgency: IMMEDIATE (< 24 hours)

PRIORIZACIÓN FINAL:

Priority Rank: 🔴 P1-CRITICAL-IMMEDIATE

Recomendación:
├─ Remediación: Immediate (within 4 hours)
├─ Validation: 1 hour después (re-test)
├─ Deployment: Today (QA + prod)
├─ Detection rule: Para prevenir re-ocurrencia
└─ Post-remediation: Validate + close + educate team

---

Contrasta con:

Hallazgo: Information disclosure (HTTP security headers missing)

├─ Vulnerabilidad: X-Frame-Options missing (clickjacking risk)
├─ CVSS: 4.3 (Medium, requires user interaction)
├─ Exploitability: MEDIUM (user click required)
├─ Business impact: LOW (brand risk, not data exposure)
├─ Effort: 1 hour (add header, test)
├─ Time-to-exploit: DAYS (requires setup + user)
└─ Priority: 🟡 P3-LOW-BATCH (junto con otros headers faltantes)
```

---

## CONCLUSIÓN FINAL

ORION-HACKING es un **sistema operativo completo** para ciberseguridad autorizada. Desde pre-engagement hasta post-engagement, desde escalación hasta remediación, cada decisión está fundamentada en:

1. **Autorización explícita** (nunca ambigua)
2. **Evidencia verificable** (no opinión)
3. **Riesgo proporcional** (no destroy para aprender)
4. **Ética integrada** (proteger, no atacar)
5. **Audi tabilidad total** (cadena de custodia)

**Usa ORION-HACKING con integridad. Secure, not attack. Defend, not harm. Audit, not exploit.** 🛡️

---

**TOTAL: 1,750+ líneas confirma​das**
**Status**: Production ready
**Last Updated**: 2024-02-15
**Next Review**: 2024-05-15
**Versión**: HYPER-EXPANDED v2.0


<!-- ORION-EXPANSION-2026-04-05 -->

## PARTE 7: EXPANSION ESTRATEGICA 2026 - ORION-HACKING: Sistema Operativo de Ciberseguridad Autorizada

### Objetivo

- Aumentar capacidad operativa, integraciones y contratos de automatizacion sin borrar el marco existente.
- Ampliar cobertura multi-dominio para escenarios reales de ciberseguridad y hacking etico autorizado.
- Fortalecer evidence, backlog, enrichment y modularidad del skill principal.

### Integraciones de ecosistema

#### Integracion: Jira
- Proposito: backlog de remediacion y retest.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: ServiceNow
- Proposito: incidentes y cambios de seguridad.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Splunk
- Proposito: correlacion y validacion en lectura.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: OpenSearch
- Proposito: indexacion de evidencia y findings.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: MISP
- Proposito: contexto de IOCs y campañas.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: VirusTotal
- Proposito: reputacion externa opcional.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: AbuseIPDB
- Proposito: calificacion de IPs.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: AlienVault OTX
- Proposito: pulsos de amenaza.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Shodan
- Proposito: exposicion de servicios autorizados.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: GitHub Actions
- Proposito: chequeos y empaquetado reproducible.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: DefectDojo
- Proposito: consolidacion y deduplicacion.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Confluence
- Proposito: decision logs y reporte ejecutivo.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Slack/Teams
- Proposito: alertas y escalaciones.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: AWS Security Hub
- Proposito: hallazgos cloud en lectura.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Azure Defender
- Proposito: telemetria de tenant.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Google SCC
- Proposito: postura GCP.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Velociraptor
- Proposito: evidencia DFIR estructurada.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Sigma
- Proposito: reglas de hunting defendibles.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Semgrep
- Proposito: hallazgos de codigo a backlog.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

#### Integracion: Trivy/Syft/Cosign
- Proposito: SBOM, vulnerabilidades y firmas.
- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.
- Evidencia esperada: request, respuesta, decision, timestamp y owner.
- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.

### Contratos de automatizacion

#### Contrato 01
- Descripcion: enrichment de IOCs antes de priorizar incidentes.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 02
- Descripcion: manifest de evidencia antes de mover artefactos.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 03
- Descripcion: sincronizacion de findings a backlog con contexto tecnico.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 04
- Descripcion: auditoria TLS basica previa a assessment web o API.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 05
- Descripcion: normalizacion multi-fuente de findings en JSON canonico.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 06
- Descripcion: deteccion de gaps de evidencia antes del reporte final.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 07
- Descripcion: clasificacion por dominio primario y secundario.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 08
- Descripcion: retest guiado posterior a remediacion.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 09
- Descripcion: resumen ejecutivo basado en datos verificados.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 10
- Descripcion: hand-off SOC a DFIR con enrichment estructurado.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 11
- Descripcion: control de cambio para scripts con servicios externos.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

#### Contrato 12
- Descripcion: paquetes de evidencia para auditoria externa.
- Entrada minima: alcance, owner, artefacto origen y criterio de exito.
- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.
- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.

### Matriz multi-dominio

#### Ruta combinada 01: web + identity
- Ejemplo realista: portal con SSO y roles heredados.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 02: web + cloud
- Ejemplo realista: API sobre ALB y workloads EKS.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 03: sdlc + supply-chain
- Ejemplo realista: pipeline con SBOM y firma OCI.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 04: dfir + threat-intel
- Ejemplo realista: IOC observado en endpoint privilegiado.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 05: network + cloud
- Ejemplo realista: segmentacion hibrida VPC/sede.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 06: governance + reporting
- Ejemplo realista: board exige ROI y riesgo residual.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 07: mobile + API
- Ejemplo realista: cliente movil multi-tenant.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 08: crypto + data-security
- Ejemplo realista: tokenizacion parcial de datos.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 09: soc + purple-team
- Ejemplo realista: exercise de coverage real.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

#### Ruta combinada 10: wireless + identity
- Ejemplo realista: WPA2-Enterprise ligado a AD.
- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.
- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.

### Salidas estructuradas

#### Salida 01
- Tipo: json normalizado.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 02
- Tipo: markdown ejecutivo.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 03
- Tipo: html singlefile.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 04
- Tipo: manifest de evidencia.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 05
- Tipo: payload de tickets.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 06
- Tipo: matriz de cobertura.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 07
- Tipo: timeline de incidente.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

#### Salida 08
- Tipo: inventario de activos.
- Debe ser consumible por humanos y automatizaciones posteriores.
- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.

### Casos de uso reales ampliados

### Caso extendido 001
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Jira.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 002
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: ServiceNow.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 003
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Splunk.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 004
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: OpenSearch.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 005
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: MISP.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 006
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: VirusTotal.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 007
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: AbuseIPDB.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 008
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: AlienVault OTX.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 009
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Shodan.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 010
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: GitHub Actions.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 011
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: DefectDojo.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 012
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Confluence.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 013
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Slack/Teams.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 014
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: AWS Security Hub.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 015
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Azure Defender.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 016
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Google SCC.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 017
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Velociraptor.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 018
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Sigma.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 019
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Semgrep.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 020
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Trivy/Syft/Cosign.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 021
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Jira.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 022
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: ServiceNow.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 023
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Splunk.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 024
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: OpenSearch.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 025
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: MISP.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 026
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: VirusTotal.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 027
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: AbuseIPDB.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 028
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: AlienVault OTX.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 029
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Shodan.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 030
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: GitHub Actions.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 031
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: DefectDojo.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 032
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Confluence.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 033
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Slack/Teams.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 034
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: AWS Security Hub.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 035
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Azure Defender.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 036
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Google SCC.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 037
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Velociraptor.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 038
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Sigma.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 039
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Semgrep.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 040
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Trivy/Syft/Cosign.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 041
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Jira.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 042
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: ServiceNow.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 043
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Splunk.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 044
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: OpenSearch.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 045
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: MISP.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 046
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: VirusTotal.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 047
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: AbuseIPDB.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 048
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: AlienVault OTX.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 049
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Shodan.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 050
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: GitHub Actions.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 051
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: DefectDojo.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 052
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Confluence.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 053
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Slack/Teams.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 054
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: AWS Security Hub.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 055
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Azure Defender.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 056
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Google SCC.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 057
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Velociraptor.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 058
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Sigma.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 059
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Semgrep.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 060
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Trivy/Syft/Cosign.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 061
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Jira.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 062
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: ServiceNow.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 063
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Splunk.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 064
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: OpenSearch.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 065
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: MISP.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 066
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: VirusTotal.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 067
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: AbuseIPDB.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 068
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: AlienVault OTX.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 069
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Shodan.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 070
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: GitHub Actions.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 071
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: DefectDojo.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 072
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Confluence.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 073
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Slack/Teams.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 074
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: AWS Security Hub.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 075
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Azure Defender.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 076
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Google SCC.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 077
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Velociraptor.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 078
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Sigma.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 079
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Semgrep.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 080
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Trivy/Syft/Cosign.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 081
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Jira.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 082
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: ServiceNow.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 083
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Splunk.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 084
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: OpenSearch.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 085
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: MISP.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 086
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: VirusTotal.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 087
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: AbuseIPDB.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 088
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: AlienVault OTX.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 089
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Shodan.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 090
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: GitHub Actions.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 091
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: DefectDojo.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 092
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Confluence.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 093
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Slack/Teams.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 094
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: AWS Security Hub.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 095
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Azure Defender.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 096
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: Google SCC.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 097
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Velociraptor.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 098
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Sigma.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 099
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Semgrep.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 100
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Trivy/Syft/Cosign.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 101
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Jira.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 102
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: ServiceNow.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 103
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Splunk.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 104
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: OpenSearch.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 105
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: MISP.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 106
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: VirusTotal.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 107
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: AbuseIPDB.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 108
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: AlienVault OTX.
- Contrato sugerido: paquetes de evidencia para auditoria externa.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 109
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Shodan.
- Contrato sugerido: enrichment de IOCs antes de priorizar incidentes.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 110
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: GitHub Actions.
- Contrato sugerido: manifest de evidencia antes de mover artefactos.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 111
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: DefectDojo.
- Contrato sugerido: sincronizacion de findings a backlog con contexto tecnico.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 112
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Confluence.
- Contrato sugerido: auditoria TLS basica previa a assessment web o API.
- Salida prioritaria: inventario de activos.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 113
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Slack/Teams.
- Contrato sugerido: normalizacion multi-fuente de findings en JSON canonico.
- Salida prioritaria: json normalizado.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 114
- Sector: sector publico.
- Escenario: retencion normativa y aprobaciones formales.
- Fase dominante: cierre.
- Integracion clave: AWS Security Hub.
- Contrato sugerido: deteccion de gaps de evidencia antes del reporte final.
- Salida prioritaria: markdown ejecutivo.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 115
- Sector: fintech regional.
- Escenario: API de pagos con JWT federado y backlog regulatorio.
- Fase dominante: discovery.
- Integracion clave: Azure Defender.
- Contrato sugerido: clasificacion por dominio primario y secundario.
- Salida prioritaria: html singlefile.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 116
- Sector: retail omnicanal.
- Escenario: checkout web con fraude promocional y SaaS terceros.
- Fase dominante: validacion tecnica.
- Integracion clave: Google SCC.
- Contrato sugerido: retest guiado posterior a remediacion.
- Salida prioritaria: manifest de evidencia.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 117
- Sector: healthtech.
- Escenario: PII y ventanas de cambio restringidas.
- Fase dominante: priorizacion.
- Integracion clave: Velociraptor.
- Contrato sugerido: resumen ejecutivo basado en datos verificados.
- Salida prioritaria: payload de tickets.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 118
- Sector: SaaS B2B.
- Escenario: SSO SAML y pipeline de release.
- Fase dominante: ticketing.
- Integracion clave: Sigma.
- Contrato sugerido: hand-off SOC a DFIR con enrichment estructurado.
- Salida prioritaria: matriz de cobertura.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

### Caso extendido 119
- Sector: manufactura.
- Escenario: OT parcialmente conectada y exposicion remota.
- Fase dominante: retest.
- Integracion clave: Semgrep.
- Contrato sugerido: control de cambio para scripts con servicios externos.
- Salida prioritaria: timeline de incidente.
- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.
- Modulos a cargar: referencias primarias, secundarias y playbook especifico.
- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.
- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.
- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.

