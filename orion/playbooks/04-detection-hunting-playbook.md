# Detection & Hunting Playbook (04)

## Visión Ejecutiva

Desarrollo de **detecciones operacionales** basadas en TTPs, amenazas específicas, o hallazgos técnicos.
Salida: Sigma rules, queries SIEM, runbooks, hunting library.

**Alcance**: 1-8 semanas depending profundidad

---

## Fase 1: Requerimientos (3-5 días)

### Log Sources Disponibles

```
✅ REQUIRED:
- [ ] Sysmon (evento 22 para DNS, 3 para network, 11 para file, 15 para comand-line)
- [ ] Windows Event Log (4688 command execution, 4624 logon, 1000 crash)
- [ ] Linux: auditd, syslog, filesystem logs
- [ ] Network IDS/IPS logs
- [ ] Proxy logs
- [ ] Cloud audit logs (CloudTrail, Azure Monitor, GCP Logs)

✅ OPTIONAL BUT NICE:
- [ ] EDR (CrowdStrike, Microsoft  Defender, SentinelOne)
- [ ] SIEM (Splunk, ELK, Azure Sentinel)
- [ ] Packet capture (PCAP, Zeek, Suricata)
```

### Threat Context

Pregunta: ¿Cuáles son los **riesgos principales**?

```
1. Lateral movement en red (APT)
2. Credential theft (ransomware droppers)
3. Data exfiltration (insider threat)
4. Supply chain (malicious dependencies)
5. Cloud misconfig exploitation
```

Mapea a MITRE ATT&CK:
```
Lateral Movement → T1021, T1570, T1570
Credential Access → T1110, T1187, T1056
Exfiltration → T1041, T1048, T1537
```

### Data Retention

```bash
# CRITICAL
sysmon_data_retention_days = 90  # Sufficient for hunting
network_data_retention_days = 30
authentication_data_retention_days = 90

# Problema: si retención < 30 días
# → Threat hunting retrospectivo es imposible
# → Escalada como "critical"
```

---

## Fase 2: Behavioral Baselines (3-5 días)

### Command-Line Patterns

```bash
# ¿Qué es "normal" en tu org?

# Normal:
powershell.exe -Command "Get-Process"
cmd.exe C:\Scripts\daily-job.bat

# Anormal (probable malware):
powershell.exe -EncodedCommand <base64-blob>
cmd.exe /c "certutil -decode file.txt outfile.bin"  (download arbitrary binary)
```

### Network Patterns

```bash
# Normal:
outbound HTTPS 443 → AWS S3, Azure Blob (corporate SaaS)
DNS queries → Google, Quad9 (public resolvers)

# Anormal:
outbound HTTPS 443 → 141.98.255.[] (botnet C2)
outbound 6666, 8080 → random IPs (IRC, raw protocols)
DNS queries → dga.examples (domain generation algorithm)
```

### Process Chains

```bash
# Normal:
explorer.exe → notepad.exe  (user opens file)
cmd.exe → powershell.exe → executable  (admin tasks)

# Anormal:
svchost.exe → cmd.exe (service shouldn't spawn shell)
explorer.exe → whoami → systeminfo → ipconfig  (reconnaissance chain)
```

---

## Fase 3: Sigma Rule Writing (2-3 semanas)

### Ejemplo 1: Lateral Movement (T1021) - Pass-the-Hash

```yaml
title: Potential Pass-the-Hash Attack
logsource:
  product: windows
  service: sysmon
detection:
  selection:
    EventID: 3  # Network connection
    DestinationPort:
      - 445  # SMB
      - 139  # Netbios
    Protocol: tcp
  filter:
    SourceIp:
      - 10.0.0.0/8
      - 172.16.0.0/12
      - 192.168.0.0/16
  condition: selection and not filter
falsepositives:
  - Administrative file shares
  - Legitimate backup tools
level: medium
```

### Ejemplo 2: Data Exfiltration (T1041) - Outbound HTTPS Anomaly

```yaml
title: Unusual Outbound HTTPS to Unknown Domain
logsource:
  product: firewall
  service: paloalto
detection:
  selection:
    action: allow
    destination_type: unknown  # Not in whitelist
    destination_port: 443
    bytes_out: '>100000'  # Over 100KB
  filter:
    destination_domain:
      - onedrive.com
      - dropbox.com
      - google.com
  summary: Outbound HTTPS to unknown domain with >100KB transferred
  condition: selection and not filter
falsepositives:
  - SaaS applications
  - Windows Update
  - Package managers
level: high
```

### Ejemplo 3: Privilege Escalation (T1134) - Token Impersonation

```yaml
title: Process Spawned with Create_Token Privilege
logsource:
  product: windows
  service: sysmon
detection:
  selection:
    EventID: 10  # Process access
    GrantedAccess: '0x0008'  # TOKEN_DUPLICATE or TOKEN_IMPERSONATE
    SourceImage|endswith:
      - '\lsass.exe'
      - '\csrss.exe'
  condition: selection
falsepositives:
  - Legitimate tools (NSA BlueTeam)
level: critical
```

---

## Fase 4: SIEM Tuning (1-2 semanas)

### False Positive Reduction

```
Day 1: Regla genera 100 alerts
Days 2-7: Análisis de cada alert
  - 70 son admin scripts  → Whitelist
  - 15 son SaaS apps  → Update filter
  - 10 son verdaderos positivos  → Mantener

Result: 10/100 alerts (10% FP rate)
```

### Threshold Tuning

```
Bad rule: "ANY outbound to unknown domain"
→ 10,000 alerts/día (too noisy)

Good rule: "Outbound to unknown domain + 1MB+ transferred + 10+ different destinations + from non-admin user"
→ 5 alerts/día (manageable)
```

### Testing

```bash
# Create test events
sysmon -i -install
# Generate normal activity baseline

# Run alert logic
rule_query = "EventID=3 AND DestinationPort=445 AND SourceIp NOT IN (10.0.0.0/8)"

# Count:
# Before: 0 alerts (no SMB)
# After: 0-1 alerts (expected)
```

---

## Fase 5: Hunting Library (1-2 semanas)

### Lateral Movement Queries

```spl
# Splunk searching for lateral movement indicators
sourcetype=sysmon EventID=3 DestinationPort IN (445,139,22,3389) 
  | stats count by SourceIp, DestinationIp, Image 
  | where count > 10
  | rename Image as "Lateral Movement Tool"
```

```kql
# Kusto (Azure Sentinel)
SecurityEvent
| where EventID == 4648  // Explicit Credential Use
| summarize connectioncount = dcount(Computer) by Account, TargetServerName
| where connectioncount > 20
| project Account, TargetServerName, connectioncount
```

### Data Exfil Queries

```sql
SELECT timestamp, source_ip, destination_domain, bytes_transferred
FROM network_logs
WHERE destination_port = 443
  AND bytes_transferred > 1000000
  AND destination_domain NOT IN (whitelist_table)
  AND source_ip IN (10.0.0.0/8)
ORDER BY bytes_transferred DESC
```

### Persistence Indicators

```
Buscar para:
- Scheduled tasks creadas
- Registry HKLM\Software\Microsoft\Windows\Run changes
- DLL injection (CreateRemoteThread)
- WMI event suscriptions
```

---

## Fase 6: Runbooks & Response (3-5 días)

### Alert Runbook Ejemplo

```
ALERT: Unusual Outbound HTTPS to Unknown Domain

Trigger: rule T1041_data_exfil_https
  - source_ip: 10.0.50.25
  - destination: 141.98.255.100
  - bytes: 500MB
  - duration: 2 hours

INVESTIGATE:
1. Identify user: whoami for 10.0.50.25
   → Result: john.smith
2. Check running processes:
   powershell.exe C:\temp\exfil.ps1?
   → Confirm or list legitimately
3. Quarantine if suspicious:
   - Drop network rules: 10.0.50.25 → *.*.*.* 443
   - Notify SOC + john's manager
4. Preserve evidence:
   - Memory dump: john's machine
   - Disk image (if critical)
   - Process logs from EDR
5. Remediation:
   - Kill suspicious process
   - Reset password
   - Rebuild machine from golden image
```

---

## Salida Esperada

1. **Sigma Rules**: 20-50 reglas en formato YAML
2. **SIEM Queries**: Tuneadas para tu plataforma
3. **Hunting Library**: 10+ consultas interactivas
4. **Runbooks**: 1 por alerta crítica
5. **Metrics Dashboard**: Alert volume, FP rate, MTTR

---

## Herramientas

| Herramienta | Propósito |
|---|---|
| Sigma | Rule format estándar |
| SIEM_native | Query en tu plataforma |
| Jupyter | Análisis de tendencias |
| Grafana | Dashboards |



<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Operativa 2026 - Detection & Hunting Playbook (04)

Este playbook se amplia para cubrir integraciones y casos de deteccion y hunting.

### Integraciones de ejecucion

- Jira: usar para coordinacion, backlog, evidencia o telemetria.
- ServiceNow: usar para coordinacion, backlog, evidencia o telemetria.
- Slack/Teams: usar para coordinacion, backlog, evidencia o telemetria.
- OpenSearch: usar para coordinacion, backlog, evidencia o telemetria.
- GitHub Actions: usar para coordinacion, backlog, evidencia o telemetria.
- Splunk: usar para coordinacion, backlog, evidencia o telemetria.

### Casos operativos extendidos

### Caso operativo 01
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 02
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 03
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 04
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: OpenSearch.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 05
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: GitHub Actions.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 06
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Splunk.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 07
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 08
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 09
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 10
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: OpenSearch.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 11
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: GitHub Actions.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 12
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Splunk.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 13
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 14
- Situacion: engagement de deteccion y hunting con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

