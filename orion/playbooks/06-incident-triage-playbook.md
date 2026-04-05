# Incident Triage & Response Playbook (06)

## Visión Ejecutiva

**TIEMPO-CRÍTICO** respuesta a incidente de seguridad activo.
Cobertura: Contención, timeline, IOCs, scope, plan de remediation.
Entrega: Incident report, evidence, root cause analysis.

**THIS PLAYBOOK CAN MEAN DIFFERENCE BETWEEN $10K vs $10M IMPACT.**

---

## Fase 0: ACTIVACIÓN (Primeros 15 minutos)

### STOP & ASSESS

**IMMEDIATE ACTIONS (DO NOT SKIP)**:

1. **PRESERVE EVIDENCE** (before any action)
   ```bash
   # Memory dump
   sudo dd if=/proc/kcore of=/mnt/usb/memdump.bin
   
   # Network capture
   tcpdump -i any -w /mnt/usb/traffic.pcap &
   
   # filesystem snapshot
   tar --exclude=/dev --exclude=/proc --exclude=/sys -czf /mnt/usb/disk.tar.gz /
   ```

2. **ESCALATE** (call immediately)
   ```
   ☎️ CTO / CISO / Security Lead
   ☎️ Legal / Compliance
   ☎️ Insurance (if applicable)
   ☎️ Law enforcement (if required)
   ```

3. **ISOLATE** (but carefully)
   ```
   ❌ DON'T power off (lose memory evidence)
   ❌ DON'T delete logs
   ❌ DON'T restart services (lose in-memory state)
   
   ✅ DO disconnect network (pull cable, not wireless)
   ✅ DO note timeline: "Power off time: 14:32 EST"
   ```

4. **PROTECT EVIDENCE CHAIN**
   - Photograph machine state
   - Document everyone who touched it (names, time)
   - Store in secure location
   - Hash all files: SHA256 each evidence item

### Initial Context Gathering (30 minutes)

```
CRITICAL QUESTIONS:
1. What triggered the alert?
   Answer: "EDR detected suspicious process"
   
2. On how many machines?
   Answer: "3 servers cluster-01 to cluster-03"
   
3. What data is in scope?
   Answer: "Customer database (PII), source code (IP)"
   
4. Is attacker still active?
   Answer: "Unknown. C2 domain still resolving"
   
5. Who is on-call?
   Names + phone numbers
```

**Output**: Incident ticket in Jira/ServiceNow with severity, scope, timeline

---

## Fase 1: Triage Rápido (30 min - 2 horas)

### Scope Estimation

```
SCENARIOS:

Scenario A: Single workstation
  - Isolated breach (1 user's laptop)
  - Risk: LOW (if no credential theft)
  - Containment risk: Workstation rebuild
  - Timeline: 4-8 hours to remediate

Scenario B: Server with credentials
  - Active system potentially compromised
  - Risk: MEDIUM-HIGH (credential leakage possible)
  - Containment risk: Lateral movement chain starting
  - Timeline: 4-24 hours

Scenario C: Multi-server, active C2
  - APT scenario
  - Risk: CRITICAL
  - Containment risk: Widespread lateral movement
  - Timeline: 24-72 hours containment + weeks analysis
```

### Initial Timeline

```
14:30 - EDR alert: suspicious powershell process
        → Logged by Sysmon EventID 1
        
14:35 - Network connection detected: outbound 443 to 185.233.100.50
        → Logged by Sysmon EventID 3
        
14:45 - File write detected: C:\temp\exfil.zip (500MB)
        → Logged by Sysmon EventID 11
        
14:52 - Network connection closed (attacker left?)
        
IMPLICATION: Active attack lasted ~20 minutes
```

### Containment Options

```
CHOICE 1: Immediate Kill (aggressive)
  - Kill suspicious process
  - Block outbound IPs
  - Risk: Attacker knows you detected them
  - Benefit: Stops data exfil NOW

CHOICE 2: Forensic First (cautious)
  - Let process continue (so far)
  - Capture network traffic
  - Full memory/disk imaging
  - Risk: More data might exfil
  - Benefit: Complete forensic evidence

CHOICE 3: Hybrid (recommended)
  - Immediate network kill (firewall rule)
  - Process continues locally (memory capture ongoing)
  - After 30 min: kill process and isolate machine
```

---

## Fase 2: Investigation (4-24 horas)

### Timeline Reconstruction

Combine múltiples log sources:

```
SOURCE 1: Sysmon (Windows Event Log)
14:30:42 - Process creation: C:\Windows\System32\powershell.exe
          CommandLine: powershell -enc <base64>
          ParentImage: C:\Windows\System32\svchost.exe  ← SUSPICIOUS (svchost shouldn't spawn PS)

SOURCE 2: Network IDS (Zeek alerts)
14:35:15 - DNS query: dga.malware.com  ← C2 communication

SOURCE 3: Windows Defender
14:40:00 - Alert: Trojan.Generic (malware signature match)

SOURCE 4: Cloud logs (if AWS/Azure)
14:32:18 - API call: assume-role (cross-account access)  ← Lateral movement!

CONSOLIDATED TIMELINE:
1. svchost spawns powershell (unlikely, attack entry point?)
2. Powershell establishes C2 (dga.malware.com)
3. Malware signature detected 8 min later
4. Cross-account assume-role 2 min later
5. Continued for ~20 minutes total
```

### Artifact Analysis

#### Memory Dump

```bash
# Volatility (memory forensics)
python3 volatility3 -f memdump.bin windows.pslist  # Running processes
python3 volatility3 -f memdump.bin windows.netscan  # Network connections
python3 volatility3 -f memdump.bin windows.registry  # Registry changes

# Carving: search for suspicious patterns
strings memdump.bin | grep -E "cmd.exe|powershell" | head -20
```

#### Disk Analysis

```bash
# Filesystem carving
photorec -d ./recovery memdump.bin  # Recover deleted files

# File integrity check
md5deep -r system_baseline/ | sort > baseline.txt
md5deep -r /suspicious/system | sort > current.txt
diff baseline.txt current.txt  # What's changed?

# Timeline creation
fls -m /suspicious/system | mactime -b bodyfile -d timeline/ | sort | uniq
```

#### Network Capture

```bash
# Wireshark analysis
tshark -r traffic.pcap -Y "ip.src == 192.168.1.100" -T fields -e frame.time -e ip.dst -e tcp.dstport
# Shows: what IPs/ports did attacker communicate with?

# Malware domain analysis
grep -h "^GET\|^POST" traffic.pcap | sort | uniq
# Shows: what URLs did attacker visit?
```

### IOC Extraction

```json
{
  "iocs": {
    "ips": [
      {
        "ip": "185.233.100.50",
        "reputation": "MALICIOUS (C2 server)",
        "action": "Block on firewall, all ports"
      }
    ],
    "domains": [
      {
        "domain": "dga.malware.com",
        "reputation": "C2 infrastructure",
        "action": "Block DNS resolution"
      }
    ],
    "file_hashes": [
      {
        "hash": "sha256:abc123def456",
        "filename": "exfil.zip",
        "malware": "Trojan.Generic",
        "action": "Quarantine all matches"
      }
    ],
    "mitre_att&ck": [
      "T1059 - Command and Scripting Interpreter (powershell)",
      "T1041 - Exfiltration Over C2 Channel",
      "T1570 - Lateral Tool Transfer"
    ]
  }
}
```

---

## Fase 3: Impact Assessment (2-6 horas)

### Data Breach Scope

```
Question: What data accessed/exfiltrated?

Answer analysis:
1. Check process: what files did powershell access?
2. Check network: 500MB exfiltrated = what files?
3. Check file integrity: are files modified?

EXAMPLE RESULT:
- Customer database accessed (read): 10,000 PII records (names, emails, hashed passwords)
- Source code accessed (read): 1 proprietary algorithm file
- Log files were overwritten: evidence tampering

RISK ASSESSMENT:
- PII breach = GDPR violation = CRITICAL
- Must notify customers within 72 hours
- Must notify DPA within 72 hours
```

### Business Impact

```
Financial impact estimate:
  - Incident response: $50k (team + forensics)
  - System rebuild: $10k 
  - Downtime (if happened): $100k (1 day SaaS outage)
  - Regulatory fines: $500k+ (GDPR: up to €20M or 4% revenue)
  - Class action lawsuit risk: $1M+ (if PII compromised)
  - Reputational: TBD
  
Total: $600k+ MINIMUM
```

---

## Fase 4: Remediation (12-48 horas)

### IMMEDIATE (next 4 hours)

```
DONE ALREADY in Phase 0-1:
- [ ] Isolate affected machines
- [ ] Kill malicious processes
- [ ] Block IOCs on firewall

STILL TO DO:
- [ ] Reset all affected employee passwords (force them to change next login)
- [ ] Revoke all active sessions / tokens
- [ ] Revoke API keys if in scope
- [ ] Kill SSH sessions if applicable
- [ ] BLOCK on firewall + SIEM:
      Block outbound to all IOC IPs
      Block DNS to all IOC domains
```

### SHORT-TERM (1-2 weeks)

```
- [ ] Re-image all affected machines
  - Wipe master boot record
  - Restore from trusted backup (pre-incident)
  
- [ ] Verify backups are clean
  - Last backup BEFORE incident?
  - Ransomware didn't touch backup infrastructure?
  
- [ ] Update EDR signatures
  - Submit file hashes to vendor
  - Import sigma rules to SIEM
  
- [ ] Patch root cause
  - If was exploit: patch the vulnerability ASAP
  - If was credential theft: implement MFA
  - If was phishing: security awareness training
  
- [ ] Validate remediation
  - Re-test: can we still detect same attack pattern?
  - Red team test: "can I re-exploit same way?"
```

### LONG-TERM (2-12 weeks)

```
DEFENSE IMPROVEMENTS:
1. Detection gaps identified? Add Sigma rules
2. Logging gaps? Enable audit logging missed areas
3. Access gaps? Implement micro-segmentation
4. Backup gaps? Isolate backups from network

PROCESS IMPROVEMENTS:
1. Incident response plan review
2. Update runbooks based on learnings
3. Training: team received training post-incident?
4. Communication: was escalation path clear?

COMPLIANCE:
1. Document all actions taken (evidence for regulators)
2. Finalize breach notification (customer comms)
3. Prepare for potential audit
```

---

## Fase 5: Post-Incident (2-4 semanas después)

### Lessons Learned

```
ROOT CAUSE:
  How did attacker get in?
  - Phishing link (user clicked)
  - Unpatched system (exploit T1190)
  - Weak credentials (password spray T1110)
  - Compromised third party

DETECTION FAILURE:
  Why didn't we catch earlier?
  - EDR not installed on that machine? → Fix
  - Sigma rules didn't match? → Tune rules
  - Alert saturation (too noisy)? → Reduce FP

RESPONSE FAILURE:
  What could we have done faster?
  - Access to forensic tools? → Pre-stage them
  - Communication breakdown? → Clearer escalation
  - Authority to disconnect? → Pre-authorize IR team
```

### Red Team Re-Test

```
"Can we be compromised the same way again?"

Test 1: Phishing to same user
  Expected: Blocked by new tools / training
  
Test 2: Exploit CVE-202X-XXXXX (if that was entry)
  Expected: System now patched, exploit fails
  
Test 3: Lateral movement down-level SMB
  Expected: Network policies now block
```

### Update Incident Response Plan

```
ORION assessment → Incident Response capability
- [ ] Updated IR contacts (if people moved)
- [ ] Updated escalation paths
- [ ] New tools deployed (forensic, endpoint isolation)
- [ ] Updated runbooks per this incident
- [ ] Training for new team members
```

---

## Salida Esperada

1. **Incident Report**: 20-50 páginas
   - Executive summary (1 page)
   - Timeline (step-by-step reconstruction)
   - Root cause analysis
   - Impact quantification

2. **Forensic Report**: Technical details
   - Memory analysis
   - Disk findings
   - Network evidence
   - Artifact catalog

3. **IOC List**: Shared with threat intelligence partners
   - IP addresses
   - Domains
   - File hashes

4. **Remediation Plan**: Next 90 days
   - Immediate fixes (done)
   - Short-term improvements (2 weeks)
   - Strategic changes (3 months)

5. **Evidence Archive**: Encrypted, evidentialed
   - All disk images
   - Memory dumps
   - Network captures
   - Logs

---

## Severity Classification

| nivel | Criteria | Timeline |
|---|---|---|
| CRITICAL | Ransomware, active data theft, >100K PII | 1-4 hours |
| HIGH | Malware, breach detected, <100K records | 4-8 hours |
| MEDIUM | Suspicious activity, no confirmed breach | 8-24 hours |
| LOW | Unusual events, no security risk confirmed | 24+ hours |

