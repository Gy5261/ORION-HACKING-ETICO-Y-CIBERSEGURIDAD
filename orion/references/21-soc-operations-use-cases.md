# SOC Operations Use Cases - Playbooks, Triage, Incident Response

## Concepto

**SOC's job**: Detect anomalies, triage, respond, escalate

**5 Core Activities**:
1. Monitor (continuous log/alert review)
2. Detect (identify suspicious activity)
3. Triage (is this real or false positive?)
4. Respond (contain, scan, notify)
5. Escalate (incident investigation by IR team)

## Common Use Cases

**Case 1: Anomalous Login**
- Trigger: 50+ failed logins from unusual IP in 5 minutes
- Validation: New geography? Timing unusual? User confirms?
- Action: Reset password, force re-auth, flag account
- Escalation: If successful login after failures = account compromise

**Case 2: Privilege Escalation**
- Trigger: User adds themself to admin group
- Validation: Expected (new hire setup)? Unauthorized?
- Action: Review action, confirm legitimacy, audit admin activities
- Escalation: If unauthorized = suspected internal threat

**Case 3: Secret in Code Commit**
- Trigger: AWS key detected in GitHub commit
- Validation: Confirm actual secret, not test key
- Action: Rotate key, scan for abuse, force re-commit
- Escalation: If key was used = potential breach investigation

**Case 4: Data Exfiltration Attempt**
- Trigger: 100GB data download from employee laptop
- Validation: Expected? (backup, migration) Or suspicious?
- Action: Block account, quarantine devices, review file access logs
- Escalation: If unauthorized = IP theft investigation

**Case 5: Suspicious API Activity**
- Trigger: API key used from 5 different IPs simultaneously
- Validation: Expected? Shared key? Compromised?
- Action: Rotate key, review recent transactions
- Escalation: If unauthorized = fraud + key compromise

## Runbook Template

```markdown
## Runbook: [Case Title]

**Trigger**: What suspicious event indicates this case

**Data Sources**:
- Authentication logs
- Network logs  
- Endpoint telemetry
- Application logs

**Initial Severity**: Low/Medium/High (before triage)

**Triage Steps**:
1. Validate: Is this real or false positive?
2. Scope: How many users/assets affected?
3. Timeline: When did it start? Still ongoing?
4. User confirmation: Contact user, confirm behavior?

**Key Data to Preserve**:
- Raw logs (unmodified timestamps)
- Memory dumps (if malware suspected)
- Network captures (if advanced attack)

**Escalation Conditions**:
- If unusual continent + successful login after failures
- If more than 3 users affected
- If sensitive data accessed after anomaly

**Containment Actions**:
- Reset password + force re-auth
- Block IP/account temporarily
- Isolate device from network
```

## Real-World Examples

**Example 1: Credential Spray Campaign**
- 10K login attempts across 100 user accounts in 2 hours
- 3 successful logins
- Action: Reset 3 compromised accounts, block attacker IP, review access
- Time to detect: 15 minutes
- Time to contain: 1 hour

**Example 2: Insider Data Copy**
- Database admin exports 50K customer records to personal email
- Validation: Triage shows no legitimate business reason
- Action: Terminate account, legal notification, GDPR breach process
- Cost of delayed response: $500K if not caught

**Example 3: Ransomware Detection**
- Endpoint detects 10K file encryption in users' shared drives
- Action: Isolate network segment, kill malware process, restore from backup
- Time: 10 minutes detection, 30 minutes containment
- Cost: 0 if fast, $1M+ if spread network-wide

## Weekly Metrics to Track

- MTTD (Mean Time To Detect): 15 min target
- MTTR (Mean Time To Respond): 1 hour target
- False positive rate: Aim for <10%
- Alert fatigue: Tune to <50 alerts/analyst/day
- Escalation rate: 5-10% of cases escalate to investigatoin

## Checklist

- [ ] All use cases documented as runbooks
- [ ] Runbooks have data sources specified
- [ ] Escalation criteria clear
- [ ] Team trained on playbooks
- [ ] Weekly metrics reviewed
- [ ] False positives triaged & tuned
- [ ] Postmortems done on incidents
- [ ] On-call rotation defined

## Quick Wins

1. Create 5 runbooks for your top 5 alert types
2. Set up SOAR (security automation) to auto-contain false positives
3. Implement alert fatigue reduction (consolidate low-severity alerts)
4. Track MTTD/MTTR metrics weekly
5. Do weekly training on real cases
