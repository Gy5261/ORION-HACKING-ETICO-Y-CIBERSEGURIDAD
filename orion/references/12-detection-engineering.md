# Detection Engineering - SIEM Rules, Alerting & Behavioral Correlation

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe Detection Engineering?

**Problem statement**: You have 1000s of events/day flowing into SIEM. Without intelligent rules:
- ❌ 99.9% are noise (service restarts, routine logins, scheduled jobs)
- ❌ 0.1% are actual attacks hiding in noise
- ❌ If you try to catch everything → 10,000 false alerts/day (alert fatigue kills SOC)
- ❌ If you be conservative → miss real breaches

**Detection Engineering** is the discipline of:
- ✅ Writing rules that detect attacks (high true-positive rate)
- ✅ Minimizing false alerts (high precision)
- ✅ Tuning for your environment (baseline matters; every org is different)
- ✅ Correlating events across systems (single event = noise; pattern = attack)

**Estadística cruda**: Average SOC team drowns in 10,000+ daily alerts. ~99% are false positives. Real incident is lost in noise. → Detection Engineering aims for 10-50 high-confidence alerts/day (actionable, investigated).

### 5 Principios Fundamentales de Detection Engineering

1. **Know Your Baseline (Context is Detectability)**
   - Your environment's "normal" is attacker's noise
   - **Exemplo**: 1000 failed logins/day → normal (users with password expired)
   - If attacker causes +50, you won't see spike
   - **Corrección**: Baseline = 1000/day; alert if > 1050 from same user in 1 hour (contextual detection)
   - **Matemática**: Actual alert threshold = baseline + (sensitivity factor × std_dev)

2. **Correlation > Single Events (Connect the Dots)**
   - Single event = easily faked or coincidental
   - Correlated events = pattern = likely attack
   - **Exemplo**: One failed login = normal; 50 failed logins + successful login = credential spray attack
   - **Pattern**: Failed_logins(50+) → Successful_login within 5 mins + DATA_ACCESS = high confidence

3. **Coverage ≠ Trigger-Happy (Precision Matters)**
   - "Detect everything" = 10,000 false alerts = 0 coverage (team ignores alerts)
   - Better: Detect 50% of threats with 95% precision (team trusts alerts, investigates)
   - **Regla**: If rule triggers >1000x/day = reduce sensitivity, not acceptable

4. **Telemetry Dependency (No Logs = No Detections)**
   - Can't detect what you don't log
   - Before writing rule: Verify logs exist, are forwarded, have required fields
   - **Exemplo**: Want to detect "process injection" → Need Sysmon EventID 8 logs → If not collected = impossible
   - **Audit**: Inventory what you log before designing rules

5. **Attackers Adapt (Rules Are Not Forever)**
   - Rule detects technique X; attacker switches to technique Y (evades rule)
   - Rules degrade over time as attackers find evasion
   - **Maintenance**: Review rule effectiveness quarterly, update based on new TTPs (MITRE ATT&CK updates)

---

## SECCIÓN 2: COMPONENTES TÉCNICOS

### Componente 1: Log Source Assessment & Collection

**Objetivo**: Inventory what logs you have; identify gaps before building rules.

**Checklist - Telemetry Assessment**:
- ✅ Windows Event ID 4625 (failed logons) → configured?
- ✅ Sysmon (process execution, network connections) → installed on % of servers?
- ✅ Firewall logs (allowed/denied connections) → forwarded to SIEM?
- ✅ Cloud logs (CloudTrail for AWS, Azure Audit for Azure) → enabled?
- ✅ DNS logs (which domains queried) → available?
- ✅ Proxy/firewall HTTP logs (URLs, user agents) → retained?
- ✅ EDR logs (process injection, code caves, behavioral) → ingesting?
- ✅ Application logs (authentication, data access) → standardized format?
- ✅ VPN logs (remote access activity) → integrated?
- ✅ Database logs (queries, data access) → monitored?

### Componente 2: Rule Writing & Detection Logic (Sigma/YARA)

**Objetivo**: Write rules in standard format (Sigma, YARA, Splunk SPL).

**Ejemplo Sigma Rule** (Credential Spray Detection):

```yaml
title: Multiple Failed Logins - Credential Spray
description: >
  Detects credential spray: 20+ failed logins in 5 mins followed by success
  
logsource:
  product: windows
  service: security
  
detection:
  failed_logins:
    EventID: 4625
    TargetUserName: '*'
  
  condition: failed_logins > 20
  
falsepositives:
  - Password policy changes (users changing on deadline)
  - Misconfigured applications
  
level: high
references:
  - https://attack.mitre.org/techniques/T1110/
```

### Componente 3: Correlation Rules (Multi-Event Patterns)

**Objetivo**: Combine events from different systems.

**Ejemplo**: Privilege escalation + data access pattern = high-confidence attack signal

### Componente 4: Tuning & Baseline Management

**Objetivo**: Adjust thresholds to match your environment.

**Ejemplo**: Day 1 alert threshold = 10 (too sensitive, 5000 alerts). Adjust to 50 (lower noise). Review FP causes. Final: Exclude known tools, service accounts. Result: 50 good alerts/day.

### Componente 5: MITRE ATT&CK Coverage Analysis

**Objetivo**: Map rules to known attack techniques.

**Coverage Matrix**:

| Technique | Detectability | Rules | Status |
|-----------|--------------|-------|--------|
| T1110 Brute Force | HIGH | R-FailedLogins | ✅ Covered |
| T1021 RDP Lateral | HIGH | R-RDP-Unusual | ✅ Covered |
| T1566 Phishing | MEDIUM | R-Email-URLs | ⚠️ Partial |
| T1078 Valid Accounts | HIGH | None | ❌ Gap |

---

## SECCIÓN 3: METODOLOGÍA Detection Engineering

### Paso 1: Threat Assessment (1-2 weeks)
- Identify threat model (what attacks matter?)
- Map to MITRE ATT&CK
- Prioritize high-impact techniques

### Paso 2: Rule Development (2-4 weeks)
- Write rule based on TTP
- Test on simulated attacks
- Document false positives

### Paso 3: Tuning & Baseline (2-4 weeks)
- Deploy to test environment
- Adjust thresholds based on baseline data
- Review & document exceptions

### Paso 4: Production Deployment (1 week)
- Deploy to SIEM
- Monitor alert volume
- SOC team validates alerts
- Refine based on feedback

### Paso 5: Maintenance (Ongoing)
- Quarterly effectiveness review
- Update based on new ATT&CK techniques
- Adjust as organization grows
- Retire obsolete rules

---

## SECCIÓN 4: CASOS DE ESTUDIO REALES

### Caso 1: Detection Caught Lateral Movement (RDP After-Hours Access)

**Rule**: Windows RDP login outside business hours with success after multiple failures

**Trigger**: 02:15 UTC, RDP login to financial server, preceded by 15 failed attempts

**Investigation**: Attacker using stolen credentials, attempting data exfiltration

**Result**: Detected in 3 hours, contained, attacker evicted before data loss

**Key Learning**: Time-based anomalies + correlation = high-confidence detections

---

### Caso 2: Alert Storm From Naive Rule (False Positive Explosion)

**Rule**: "Alert on any cmd.exe spawning" (too broad)

**Deployment**: 50,000 alerts in 24 hours (scripts, installers, admin tasks)

**Impact**: SOC team drowned, missed real cmd.exe attack in noise

**Lesson**: Don't alert on everything. Correlate with suspicious context:
- Unexpected parent process
- Unusual time
- Non-authorized user
- Followed by data access

**Fix**: Add filters: parent_process NOT IN (powershell, system_tools); trigger only if + suspicious context

---

## SECCIÓN 5: TEMPLATES & CHECKLISTS

### Template 1: Detection Rule Template

```yaml
title: [Descriptive rule name]
description: >
  [What attack does this detect?]
  [Why important?]
logsource:
  product: [windows/linux/firewall]
  service: [security/syslog]
detection:
  selection:
    [Field]: [Value]
  filter_benign:
    [Exclusion fields]
  condition: selection AND NOT filter_benign
falsepositives:
  - [Benign cause 1]
  - [Benign cause 2]
level: [low/medium/high/critical]
references:
  - https://attack.mitre.org/techniques/TXXXX/
```

### Template 2: Detection Coverage Matrix

```markdown
# Coverage Analysis

| MITRE Technique | Likelihood | Detection Rule | Status |
|-----------------|-----------|-----------------|--------|
| T1110 Brute Force | HIGH | R-FailedLogins-Threshold | ✅ |
| T1021 RDP Lateral | HIGH | R-RDP-UnusualPattern | ✅ |
| T1078 Valid Accounts | HIGH | None | ❌ GAP |

**Coverage**: 67% (2 of 3 covered)
**Gaps**: Build detection for valid account abuse
```

---

## CONCLUSIÓN

**Detection Engineering = Continuous Improvement**

Not: "Write rule, run forever"
Actual: "Baseline → test → tune → validate → monitor → update quarterly"

**Success Factors**:
- ✅ Know your environment baseline
- ✅ Correlate events (don't alert on single noise)
- ✅ Map to MITRE ATT&CK (structured)
- ✅ Manage false positives (tune aggressively)
- ✅ Maintain quarterly (rules need updates)


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Detection Engineering - SIEM Rules, Alerting & Behavioral Correlation

### Integraciones ampliadas

- Splunk: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Elastic: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Sentinel: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Sigma: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: abuso de OAuth.
- Integracion recomendada: Splunk.
- Senal principal: false positive alto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: staging PowerShell.
- Integracion recomendada: Elastic.
- Senal principal: lag de ingesta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: hunting IAM.
- Integracion recomendada: Sentinel.
- Senal principal: coverage ATT&CK pobre.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: abuso de OAuth.
- Integracion recomendada: Sigma.
- Senal principal: false positive alto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: staging PowerShell.
- Integracion recomendada: Splunk.
- Senal principal: lag de ingesta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: hunting IAM.
- Integracion recomendada: Elastic.
- Senal principal: coverage ATT&CK pobre.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: abuso de OAuth.
- Integracion recomendada: Sentinel.
- Senal principal: false positive alto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: staging PowerShell.
- Integracion recomendada: Sigma.
- Senal principal: lag de ingesta.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: hunting IAM.
- Integracion recomendada: Splunk.
- Senal principal: coverage ATT&CK pobre.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: abuso de OAuth.
- Integracion recomendada: Elastic.
- Senal principal: false positive alto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

