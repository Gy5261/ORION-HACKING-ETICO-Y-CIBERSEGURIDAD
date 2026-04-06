# DFIR & Threat Hunting - Digital Forensics, Incident Response & Threat Intelligence

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe DFIR?

**DFIR = After-action analysis when things go wrong**. Unlike vulnerability management (prevent), DFIR is incident response (respond + learn).

When breach happens:
- ❌ Wrong: "We were pwned, shut down, pray no more damage"
- ✅ Right: "We were pwned. Let's answer: Since when? How? What was compromised? What do we fix? How do we prevent?"

**Objetivo crítico**:
- ✅ Understand attack chain (how did attacker get in?)
- ✅ Determine breach scope (how many systems? how much data?)
- ✅ Identify attacker (nation-state? cybercriminals? insider?)
- ✅ Contain spread (isolate compromised systems, prevent lateral movement)
- ✅ Eradicate threat (remove attacker access, patch root cause)
- ✅ Recover & Learn (rebuild, implement controls to prevent recurrence)

**Verdad incómoda**: 60% of breaches discovered by EXTERNAL parties (FBI, customers, researchers), not you. DFIR lets you catch the other 40% + understand what already happened.

### 5 Principios Fundamentales de DFIR

1. **Preservación de Evidencia = Prioridad #1 (Chain of Custody)**
   - Evidence improperly handled = inadmissible in court
   - Over-write memory/disk = lose forensic trail
   - **Regla**: Do NOT restart systems (memory lost), do NOT clean logs, do NOT alter timestamps
   - **Correctamente**: Isolate system from network (preserve state), capture image for analysis
   - Ejemplo: Attacker still connected; if you restart, they're gone; memory artifacts lost forever

2. **Timeline = Investigation Backbone (Correlation is Key)**
   - Thousands of logs from different sources (Windows Event, Syslog, firewall, proxy, cloud logs)
   - Timeline connects them: "At 09:12 login, 09:15 privilege escalation, 09:18 sensitive file access"
   - Without timeline: Just data; with timeline: Attack story
   - **Herramienta mental**: Graph time (X-axis) vs events (Y-axis), find patterns

3. **Proactive Threat Hunting (Don't Wait for Alerts)**
   - Most intrusions detected 200+ days AFTER breach started
   - **Why?** Organizations wait for alerts; threat hunting is hypothesis-driven investigation
   - Patrón: "Service accounts shouldn't have after-hours activity" → hunt for it → find attacker
   - **Diferencia**: Detection = reactive (alert fires); hunting = proactive (we look)

4. **Containment Strategy (Isolate If Feasible)**
   - Isolate = disconnect from network, but preserve forensics
   - Trade-off: Lose real-time attacker monitoring vs stop lateral movement
   - **Decisión contextual**: If attacker still active and moving sideways → isolate; if dormant → preserve + investigate
   - Ejemplo: Malware on workstation, not database → likely safe to isolate; malware on database server → isolate but capture network traffic first

5. **Attribution is Hard (Technology is Easy, Intent is Hard)**
   - **Tools**: Detect malware, IP addresses, domains, techniques
   - **Attribution**: Know it's definitely North Korea vs cybercriminals vs script kiddie = hard
   - **Caveat**: Can say "techniques consistent with APT-28" (not "definitely APT-28")
   - **Útil**: For law enforcement prosecution (if prosecuting, need rock-solid attribution)

---

## SECCIÓN 2: COMPONENTES DE DFIR

### Componente 1: Señales de Compromiso (Indicators of Compromise - IoC)

**Objetivo**: Identify technical evidence of attack (files, IPs, domains, hashes, behaviors).

**Información técnica**:
- **File indicators**: MD5/SHA256 hashes de malware
- **Network indicators**: IP addresses, domains, URLs usadas by attacker
- **Host indicators**: Registry keys (Windows), config files (Linux), processes, scheduled tasks
- **Behavioral indicators**: Techniques (T1234 MITRE ATT&CK), patterns (data exfil, lateral movement)

**Tipos de Indicadores**:

| Tipo | Ejemplo | Confiabilidad | Evasión |
|------|---------|---------------|---------|
| **File Hash (MD5/SHA256)** | d41d8cd98f00b204e9800998ecf8427e | HIGH | Attacker re-compiles (hash changes) |
| **File Name/Path** | C:\Windows\Temp\update.exe | MEDIUM | Easy to rename |
| **Registry Key** | HKLM\Software\Microsoft\Windows\CurrentVersion\Run\MalwareName | HIGH | Difficult to hide (persistent) |
| **Process Name** | svchost.exe spawning cmd.exe | MEDIUM | Suspicious behavior (svchost shouldn't shell) |
| **IP Address** | 203.0.113.50 (C2 server) | MEDIUM | Attacker changes IP |
| **Domain** | malicious-cdn.ru | MEDIUM | Attacker buys new domain |
| **Behavior** | Process injection, code caves, process hollowing | HIGH | Difficult to evade all detections |

**Checklist - IoC Gathering**:
- ✅ Malware samples (hash from detection)
- ✅ Malicious IPs (from firewall, proxy logs)
- ✅ Malicious domains (from DNS logs, URLhaus)
- ✅ Persistence mechanisms (registry, scheduled tasks, cron)
- ✅ Lateral movement techniques (observed commands, pass-the-hash attempts)
- ✅ Data exfiltration paths (outbound IP/port/domain)
- ✅ Behavioral indicators (MITRE ATT&CK technique IDs)

**Herramientas recomendadas**:
```bash
# Hash extraction (from file)
md5sum suspicious_file.exe
sha256sum suspicious_file.exe
# Upload to VirusTotal / AlienVault OTX for intelligence

# Registry IoCs (Windows)
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /s

# Process/network IoCs
netstat -abnO  # Processes with network connections
tasklist /v    # All processes with details

# Log analysis (extract IoCs)
grep "malware_string" /var/log/auth.log  # Search logs
cut -d' ' -f1 /var/log/access.log | sort | uniq -c | sort -rn # Top IPs

# Intelligence feeds
# MISP (Malware Information Sharing Platform)
# OpenPhish, URLhaus, Shodan, Abuse.ch
# Commercial: Mandiant, ThreatStream, etc.
```

---

### Componente 2: Timeline & Event Correlation

**Objetivo**: Build chronological narrative of attack from disparate log sources.

**Information técnica**:
- **Event sources**: Windows Event Log, Syslog (Linux), firewall logs, proxy logs, cloud (CloudTrail, Azure Audit), application logs
- **Timestamps**: Normalize to UTC (timezone confusion is common)
- **Correlation**: Cross-reference events (login → command → file access at same time)

**Checklist - Timeline Building**:
- ✅ Export all logs for relevant timeframe (e.g., "last 7 days")
- ✅ Normalize timestamps to UTC (Excel/Python helper)
- ✅ Combine into single timeline (sort by timestamp)
- ✅ Filter for relevant events (skip noise, keep signal)
- ✅ Annotate with context (admin knew? expected? policy violation?)
- ✅ Build attack story (narrative linking events)
- ✅ Identify gaps (where logs missing = blind spots)

**Ejemplo Timeline**:

```markdown
## Incident Timeline

### Initial Compromise (Day 1)
- **09:15 UTC** - Phishing email delivered to user@company.com (detected later by threat intel)
- **09:47 UTC** - user@company.com clicks link, visits malicious.ru
- **09:48 UTC** - Browser downloads payload (update.exe, 3.2MB)
- **09:49 UTC** - Lateral note: No endpoint detection (EDR might be disabled/misconfigured)

### Persistence & Lateral Movement (Days 2-5)
- **09:52 UTC (Day 1)** - update.exe creates scheduled task (every 4 hours)
- **10:15 UTC** - Attacker reconnects via backdoor, executes commands as user
- **Day 2, 14:23 UTC** - Attacker dumps SAM (password hashes) using mimikatz
- **Day 3, 03:45 UTC** - Lateral movement: SSH to server2 using stolen creds
- **Day 4, 11:20 UTC** - Attacker creates service account (backdoor user) on domain

### Data Exfiltration (Days 5-6)
- **Day 5, 19:30 UTC** - Outbound traffic spike (attacker uploading data)
- **Day 5, 19:31-23:59 UTC** - ~4GB transferred to 203.0.113.50:443
- **Day 6, 00:15 UTC** - Attacker covers tracks (clears event logs)

### Detection & Respuesta (Day 6 Afternoon)
- **Day 6, 14:00 UTC** - Customer reports data breach
- **Day 6, 14:15 UTC** - Incident team engaged, investigation begins
- **Day 6, 15:30 UTC** - Attacker detected still active; isolate compromised servers
- **Day 6, 16:45 UTC** - Attacker evicted; network access revoked

### Analysis (Days 7-14)
- Forensics: Determine scope (5 servers + 12 workstations compromised)
- Attribution: Techniques consistent with APT-X
- Root cause: Phishing + weak MFA (only email) + no EDR
```

**Herramientas recomendadas**:
```bash
# Log aggregation & timeline building
# ELK Stack, Splunk, Graylog, CloudSIEM
# Manual approach:
# 1. Export all logs (security, syslog, firewall, cloud)
# 2. Convert to CSV with columns: timestamp, source, event_type, details
# 3. Sort by timestamp (Excel sort or Unix: sort -k1)
# 4. Manually annotate suspicious events

# Example (bash):
cat windows_events.csv linux_logs.csv firewall_logs.csv | \
  sort -t',' -k1 | \
  awk -F',' '{print $1, $2, $3}' > timeline.txt
# Review manually for attack narrative
```

---

### Componente 3: Scope Analysis (Breadth of Compromise)

**Objetivo**: Understand how many systems/users/data were compromised.

**Información técnica**:
- **System scope**: How many servers? workstations? databases?
- **User scope**: How many user accounts accessed?
- **Data scope**: Which datasets were read/written/exfiltrated?
- **Time scope**: Initial compromise date vs detection (dwell time)

**Checklist - Scope Analysis**:
- ✅ Identify patient zero (first compromised system)
- ✅ Lateral movement paths (attacker moved system X → Y → Z)
- ✅ Unique accounts used (attacker accounts vs compromised legitimate accounts)
- ✅ Data accessed (query logs for sensitive data queries/reads)
- ✅ Persistence mechanisms (all places attacker planted backdoors)
- ✅ Dwell time (from first compromise to detection in days)

---

### Componente 4: Threat Hunting (Proactive Investigation)

**Objetivo**: Hunt for attacker BEFORE they're detected by automated alerts.

**Hunting Hypotheses** (Proactive patterns to investigate):

```markdown
## Hunting Hypothesis 1: Service Account Anomalies
**Hypothesis**: Service accounts should have predictable behavior; anomalies = compromise

**Hunt Query**: 
- List all service account logins per week
- Identify after-hours activity (service accounts sign in at 23:00? Suspicious)
- Identify interactive logins (service accounts should be non-interactive)

**Evidence**: 
- svc_admin logged in 50 times at 02:15 UTC (unusual)
- svc_admin spawned cmd.exe (never does this)
- svc_admin accessed C:\Users\Admin\Desktop\passwords.xlsx

**Conclusion**: Service account likely compromised; investigate source

---

## Hunting Hypothesis 2: Unexpected Admin Activity
**Hypothesis**: Admin accounts accessing unusual resources = potential compromise

**Hunt Query**:
- Admin account X accessed user file shares (admins usually work in System32, not user data)
- Admin account Y queried sensitive databases (financial, PII, engineering)
- Admin account Z created new user account (not in change management system)

**Conclusion**: If legit, document; if not, investigate

---

## Hunting Hypothesis 3: Process Behavior Anomalies
**Hypothesis**: Known legitimate processes should behave predictably

**Hunt Query**:
- svchost.exe spawning cmd.exe (never should happen)
- explorer.exe creating network connections (normally doesn't)
- Notepad.exe executing PowerShell scripts (suspicious parent-child relationship)

**Conclusion**: If observed, likely malware masquerading as legitimate process

---

## Hunting Hypothesis 4: Data Exfiltration Indicators
**Hypothesis**: Attackers must move data out; will show patterns in network/storage

**Hunt Query**:
- Large outbound transfers to external IPs (>1GB/day to unknown destination)
- Unusual database queries (SELECT *; from sensitive tables; exporting to CSV)
- Bulk file copies to USB (if not expected for business)

**Conclusion**: If observed, likely data theft in progress
```

**Herramientas recomendadas**:
```bash
# Log-based hunting (SIEM queries)
# Splunk:
index=windows eventlog process_name=svchost.exe command_line="*cmd.exe*"
# → Find svchost spawning unusual processes

# Elastic:
host.process.parent.name:svchost.exe AND host.process.name:cmd.exe
# → Same, different syntax

# Manual approach (if no SIEM):
grep "svchost" /var/log/auth.log | grep "cmd.exe" > suspicious.log

# EDR/XDR tools:
# CrowdStrike, Falcon, Microsoft Defender, Sentinel One
# These automatically hunt patterns (behavioral AI)
```

---

## SECCIÓN 3: METODOLOGÍA Incident Response Paso-a-Paso

### Paso 1: Triage & Initial Assessment (1-2 hours)

- Confirm breach is real (not false alarm)
- Establish incident commander (single decision-maker)
- Initiate isolation plan (preserve evidence first)
- Begin timeline documentation

### Paso 2: Containment (2-4 hours)

- Isolate compromised systems (network segment)
- Revoke credentials (password reset for affected accounts)
- Block attacker C2 (firewall rules for known IPs)
- Preserve forensic images (don't restart systems)

### Paso 3: Investigation (Days-Weeks)

- Analyze logs → build timeline
- Extract IoCs (files, IPs, domains)
- Determine scope (# systems, # users, data accessed)
- Identify attack chain (how entry → lateral → exfil)

### Paso 4: Eradication (Days-Weeks)

- Remove backdoors (scheduled tasks, accounts, persistence)
- Patch root cause (fill vulnerability that attacker used)
- Re-image compromised systems (ensure clean state)
- Credential reset for all affected accounts

### Paso 5: Recovery (Days-Weeks)

- Restore from clean backups
- Rebuild systems if necessary
- Implement detective controls (look for reinfection)
- Deploy new preventive controls

### Paso 6: Post-Incident (Weeks-Months)

- Root-cause analysis (why did it happen?)
- Lessons learned (what controls failed?)
- Implementation of improvements (tech + process)
- Threat intel sharing (report to industry)

---

## SECCIÓN 4: CASOS DE ESTUDIO REALES

### Caso 1: Detected Early (Hunt-Driven Discovery)

**Scenario**: Finance company hunting for privilege escalation anomalies.

**Hunt Query**: "Admin accounts accessing file shares they shouldn't."

**Finding**: CFO's admin account accessed HR salary database (unusual), copied to CSV, uploaded to cloud storage.

**Investigation**: CFO's workstation turned on after hours, admin account active. Timeline shows attack pattern consistent with nation-state APT.

**Result**: 
- Containment: Isolate CFO workstation
- Investigation: 6-month historical review (attacker present for 6 months)
- Credential: Reset all admin passwords, implement hardware security keys
- Learning: Implement privileged activity monitoring (PAM), behavioral detection

**Outcome**: Attack detected & eliminated; estimated $50M fraud prevented (CFO was stealing via database access)

---

### Caso 2: Detected Late (Breach Discovered by Customer)

**Scenario**: SaaS company, customer reports data posted on dark web.

**Initial Response**: "We were fine last I checked!" (No hunting, relied on alerts only)

**Post-Incident Investigation**:
- Timeline: Attacker present for 9 MONTHS
- Root cause: Unpatched RCE vulnerability in legacy API
- Scope: All customers' databases compromised (100M records exposed)
- FBI involvement: International prosecution (attacker in Eastern Europe)

**Lessons Learned**:
- Vulnerability scanning missed because API documentation was wrong
- No behavioral monitoring (attacker activity looked normal in aggregated logs)
- No threat hunting (would have found 9 months sooner)

**Outcome**: $150M settlement, regulatory fines, brand damage (lost enterprise customers)

---

## SECCIÓN 5: TEMPLATES & CHECKLISTS

### Template 1: Incident Response Playbook

```markdown
# Incident Response Playbook - Malware Infection

## Phase 1: TRIAGE (First Hour)

### Step 1: Confirm Incident is Real
- [ ] Endpoint protection alerts confirmed?
- [ ] Can security team reproduce issue?
- [ ] Is this known false positive?

### Step 2: Estimate Severity
- [ ] Malware type (worm? backdoor? ransomware?)
- [ ] Affected systems (1 workstation? entire network?)
- [ ] Data sensitivity at risk (PII? financial? operational?)

### Step 3: Initiate Incident Response
- [ ] Designate incident commander (name + contact)
- [ ] Page on-call security team
- [ ] Lock down network segment (if needed)
- [ ] Document initial observations (timestamp, source, symptoms)

---

## Phase 2: CONTAINMENT (First 4 Hours)

### Step 1: Isolate Affected Systems
- [ ] Disable network connectivity (unplug Ethernet or disable WiFi)
- [ ] Do NOT restart (lose memory forensics)
- [ ] Physical isolation (prevent USB transfer)

### Step 2: Revoke Credentials
- [ ] Force password reset for compromised user accounts
- [ ] Revoke security tokens / API keys if used
- [ ] Monitor for lateral movement (watch other accounts for anomalies)

### Step 3: Block Attacker Access
- [ ] Add firewall rules to block known C2 IPs
- [ ] Block known malicious domains via DNS/proxy
- [ ] Revoke any cloud API credentials attacker may have

### Step 4: Preserve Evidence
- [ ] Create forensic image of affected systems (dd, FTK Imager)
- [ ] Export all relevant logs (Windows Events, Syslog, firewall, proxy)
- [ ] Maintain chain of custody (document who accessed, when)

---

## Phase 3: INVESTIGATION (Days 1-7)

### Step 1: Analyze Malware
- [ ] Extract hash (MD5/SHA256)
- [ ] Submit to VirusTotal / AlienVault OTX (intelligence)
- [ ] Run in sandbox (Cuckoo, Any.run) to observe behavior
- [ ] Identify persistence mechanisms (registry, scheduled tasks)

### Step 2: Build Timeline
- [ ] Export all logs (security, syslog, firewall, cloud)
- [ ] Normalize timestamps to UTC
- [ ] Correlate events (login → process execution → file access)
- [ ] Identify initial compromise (earliest event in timeline)

### Step 3: Determine Scope
- [ ] Lateral movement search (identify all systems accessed)
- [ ] Credential compromise check (check if passwords captured)
- [ ] Data access review (query logs for abnormal data reads)

###Step 4: Track Attacker Activity
- [ ] Outbound connections (IP logs, NetFlow, proxy)
- [ ] Data transfers (volume, destination, time)
- [ ] Attacker commands (if command history preserved)

---

## Phase 4: ERADICATION (Days 5-14)

### Step 1: Remove Malware
- [ ] Delete or quarantine malware files
- [ ] Remove persistence mechanisms (registry keys, tasks, accounts)
- [ ] Verify clean state (re-scan with multiple AV tools)

### Step 2: Patch Root Cause
- [ ] Identify how malware entered (vulnerability? phishing?)
- [ ] Apply fix (patch, config change, security awareness)
- [ ] Verify fix effectiveness

### Step 3: Re-image Compromised Systems
- [ ] If malware deeply embedded, rebuild OS
- [ ] Restore from clean backup (if available and trusted)
- [ ] Verify no signs of re-infection

---

## Phase 5: RECOVERY (Days 14-30)

### Step 1: Restore Functionality
- [ ] Bring systems back online (phased, monitored)
- [ ] Verify critical services operational
- [ ] Restore user access (password resets complete)

### Step 2: Implement Detective Controls
- [ ] Enhanced monitoring for re-infection attempts
- [ ] Behavioral analytics (spot if attacker returns)
- [ ] Increased log retention (learn patterns)

### Step 3: Implement Preventive Controls
- [ ] Patch management process (prevent similar exploits)
- [ ] Security awareness training (phishing prevention)
- [ ] Endpoint protection updates (detect similar malware)

---

## Phase 6: POST-INCIDENT (Weeks-Months)

### Step 1: Root-Cause Analysis
- [ ] Why attack succeeded (vulnerability, policy gap, human error)
- [ ] What controls were bypassed
- [ ] Where early detection failed

### Step 2: Lessons Learned Meeting
- [ ] Security team
- [ ] Affected business units
- [ ] Executive leadership
- [ ] External incident response (if hired)

### Step 3: Improvements Implementation
- [ ] Quick wins (30 days): Enhanced monitoring, training
- [ ] Short-term (90 days): Patch backlog, process improvements
- [ ] Long-term (12 months): Architecture changes, culture shift

---

## Post-Incident Metrics

- **Time to detect**: __ hours (baseline: industry avg = 200+ days!)
- **Time to contain**: __ hours
- **Time to eradicate**: __ days
- **Systems affected**: __
- **Users affected**: __
- **Data records compromised**: __
- **Cost estimate**: __
- **Root cause** (primary): __
- **Failed control**: __
```

### Template 2: Threat Hunting Query Bank

```markdown
# SIEM Threat Hunting Queries

## Query 1: Service Account Anomalies
```
index=security EventID=4624 LogonType=2
| where user_name LIKE "svc_%"
| where hour(timestamp) NOT IN (8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
| table timestamp, user_name, src_ip, failure_reason
| top 20
```

## Query 2: Process Anomalies
```
index=security EventID=1
| where parent_process="svchost.exe" AND process="cmd.exe"
| OR where parent_process="explorer.exe" AND command_line CONTAINS "powershell"
| table timestamp, host, parent_process, process, command_line
| top 20
```

## Query 3: Lateral Movement (Pass-the-Hash)
```
index=security EventID=4625
| where failed_user != user_logged_in_as
| stats count by src_ip, dest_host
| where count > 10  # Multiple failed attempts
| table src_ip, dest_host, count
```

## Query 4: Data Exfiltration
```
index=network src_ip IN (internal_range) dst_ip NOT IN (internal_range)
| where bytes_sent > 1000000000  # > 1GB
| stats sum(bytes_sent) as total_out by src_ip, dst_ip
| where total_out > 1000000000
| table src_ip, dst_ip, total_out
```

## Query 5: Privilege Escalation
```
index=security EventID=4648 OR EventID=4649
| stats count by target_user
| where count > 5_per_day  # Abnormal elevation attempts
| table timestamp, user, target_user, result
```

## Query 6: Suspicious Scheduled Tasks
```
index=security EventID=4698 OR EventID=4702
| where command_line CONTAINS "powershell" OR "cmd.exe" OR "wmic"
| where NOT in_maintenance_window
| table timestamp, host, task_name, command_line
```
```

---

## CONCLUSIÓN

**DFIR = Bridge between detection and prevention**

- _Detection_: "Something bad happened"
- _DFIR_: "What exactly happened, how long, what to fix?"
- _Prevention_: "Never happens again"

**Key Success Factors**:
- ✅ Preserve evidence (don't destroy investigating clues)
- ✅ Build timeline (narrative is powerful)
- ✅ Hunt proactively (don't wait for alerts)
- ✅ Contain wisely (balance isolation vs investigation)
- ✅ Learn systematically (root-cause analysis + implementation)


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - DFIR & Threat Hunting - Digital Forensics, Incident Response & Threat Intelligence

### Integraciones ampliadas

- Velociraptor: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Sysmon: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Defender: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Sigma: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: phishing con token.
- Integracion recomendada: Velociraptor.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: lateral movement.
- Integracion recomendada: Sysmon.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: living off the land.
- Integracion recomendada: Defender.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: phishing con token.
- Integracion recomendada: Sigma.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: lateral movement.
- Integracion recomendada: Velociraptor.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: living off the land.
- Integracion recomendada: Sysmon.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: phishing con token.
- Integracion recomendada: Defender.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: lateral movement.
- Integracion recomendada: Sigma.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: living off the land.
- Integracion recomendada: Velociraptor.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: phishing con token.
- Integracion recomendada: Sysmon.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: lateral movement.
- Integracion recomendada: Defender.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: living off the land.
- Integracion recomendada: Sigma.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: phishing con token.
- Integracion recomendada: Velociraptor.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: lateral movement.
- Integracion recomendada: Sysmon.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: living off the land.
- Integracion recomendada: Defender.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: phishing con token.
- Integracion recomendada: Sigma.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: lateral movement.
- Integracion recomendada: Velociraptor.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: living off the land.
- Integracion recomendada: Sysmon.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: phishing con token.
- Integracion recomendada: Defender.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: lateral movement.
- Integracion recomendada: Sigma.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: living off the land.
- Integracion recomendada: Velociraptor.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: phishing con token.
- Integracion recomendada: Sysmon.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: lateral movement.
- Integracion recomendada: Defender.
- Senal principal: persistencia nueva.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: living off the land.
- Integracion recomendada: Sigma.
- Senal principal: host privilegiado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 25
- Contexto: phishing con token.
- Integracion recomendada: Velociraptor.
- Senal principal: proceso anomalo.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

