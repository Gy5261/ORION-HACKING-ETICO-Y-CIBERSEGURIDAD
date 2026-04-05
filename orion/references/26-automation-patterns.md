# Automation Patterns - Secure & Repeatable Security Processes

## Concepto

**Goal**: Automate repetitive security work WITHOUT introducing new risks

**Golden Rule**: Automation should be:
1. Simple (do ONE thing well)
2. Auditable (log what it did)
3. Isolated (don't write to production without explicit approval)
4. Timeout-aware (fail-safe on hangs)
5. Secret-safe (redact PII/secrets from output)

## Pattern 1: Read → Normalize → Report

**Use Case**: Gathering security data and making it actionable

**Steps**:
1. **Read**: Get raw data (logs, API response, config file)
2. **Normalize**: Convert to consistent format (JSON, CSV)
3. **Redact**: Remove secrets, PII, sensitive data
4. **Report**: Generate markdown or dashboard-friendly output

**Example**: HTTP header audit
```bash
#!/bin/bash
# 1. Read: Get headers from target
curl -Is https://target.com | head -20 > /tmp/headers.raw

# 2. Normalize: Extract key headers
cat /tmp/headers.raw | grep -E "^(Strict-Transport-Security|X-Frame-Options|Content-Security-Policy)" > /tmp/headers.normalized

# 3. Redact: (no secrets in headers, so skip)

# 4. Report: Generate markdown
echo "## HTTP Security Headers" > report.md
cat /tmp/headers.normalized >> report.md
```

## Pattern 2: Validate → Explain → Decide

**Use Case**: Triaging findings (Is this really a problem? What's the priority?)

**Steps**:
1. **Validate**: Confirm finding with minimum evidence (not assumptions)
2. **Explain**: Describe real-world business impact
3. **Riskify**: Assign severity (Critical/High/Medium/Low)
4. **Decide**: Assign owner & remediation timeline

**Example**: Unencrypted database
```yaml
Finding: "Database accessible on network without encryption"

Validate:
  - Query database without credentials? YES
  - Data sensitive? YES (customer PII)
  - Mitigation exists? NO

Explain:
  - Impact: Attacker inside network can steal customer data → lawsuit + $1M+ costs
  - Timeline: Breach could expose months of customer activity

Riskify:
  - Severity: CRITICAL (unencrypted + access + PII)
  - Owner: DBA lead
  - Timeline: 24h to encrypt, 7d complete remediation

Decide:
  - Accept risk? NO
  - Remediation: Enable TLS encryption + IP whitelist
```

## Pattern 3: Monitor → Alert → Escalate

**Use Case**: Continuous security monitoring for runtime issues

**Steps**:
1. **Monitor**: Check status/logs continuously
2. **Alert**: Threshold exceeded = human notification
3. **Escalate**: No human response in X hours = escalate to manager

**Example**: Certificate expiration monitoring
```python
#!/usr/bin/env python3
# 1. Monitor: Check all certificates
certs = get_all_certificates()

# 2. Alert: If expiring soon
for cert in certs:
    days_until_expiry = (cert.expiration_date - today).days
    if days_until_expiry < 30:  # Threshold
        send_slack_alert(f"Cert {cert.domain} expires in {days_until_expiry}d")
        create_jira_ticket(cert)

# 3. Escalate: If no action in 7 days
overdue = jira.search("cert_renewal AND created < 7 days ago AND status != closed")
if overdue:
    notify_manager(overdue)
```

## Pattern 4: Test → Record → Review

**Use Case**: Purple team exercises (test controls, record evidence, improve)

**Steps**:
1. **Test**: Run controlled security test (safely)
2. **Record**: Capture what happened (logs, alerts, timeline)
3. **Review**: Did detection work? What can improve?

**Example**: Credential spray test
```bash
#!/bin/bash
# 1. Test: Attempt 100 logins (safe, test account only)
for i in {1..100}; do
  curl -s https://app.example.com/login \
    -d "user=testaccount&pass=wrong-pass" >> /tmp/spray.log
done

# 2. Record: Capture what happened
echo "Test started: $(date)" >> /tmp/purple_test.log
echo "Attempts: 100" >> /tmp/purple_test.log
echo "Target: testaccount only" >> /tmp/purple_test.log
grep -c "login failed" /tmp/spray.log >> /tmp/purple_test.log

# 3. Review: Did SOC detect?
echo "SOC alerts received: $(curl https://siem.internal/api/alerts?type=login_anomaly)" >> /tmp/purple_test.log
```

## Safe Automation Practices

**DON'Ts** (Creates risk):
- ❌ Automating fixes without approval (you fix prod = you broke it)
- ❌ Storing secrets in code (use vault/Secrets Manager)
- ❌ Giant scripts doing 100 things (hard to audit, big blast radius)
- ❌ No timeout protection (infinite loop on hang)
- ❌ Leaving PII in logs (GDPR violation risk)

**DOs** (Reduces risk):
- ✅ Read-only operations first (learn before changing)
- ✅ Approval gates for any writes (requires human decision)
- ✅ Granular logging (who did what, when)
- ✅ Timeout + fail-close (rather than fail-open)
- ✅ Secret rotation (30-90 day cycles)

## Real Examples

**Example 1: Automated Dependency Scanning**
- Script: Runs `npm audit` weekly, creates Jira ticket for Critical findings
- Approval: Engineer must manually update package.json
- Result: 90% of critical updates fixed within SLA

**Example 2: Log Redaction Automation**
- Script: Strips SSN/credit card from logs before shipping to SIEM
- Audit: Every redaction logged + count reported in metrics
- Result: No PII in logs, detection capability unchanged

**Example 3: Failed Automation Lesson**
- What was automated: Full remediation of misconfigurations (firewall rules)
- Why it failed: Didn't understand business rule, locked out legitimate traffic
- Fix: Automation now creates ticket + requires manual approval before any changes

## Checklist

- [ ] Automation has single clear purpose
- [ ] All secrets externalized (vault/KMS, not hardcoded)
- [ ] Timeout protection (don't infinite-loop)
- [ ] Audit logging: Who ran it, when, what changed?
- [ ] Rollback plan: How to undo if automation fails?
- [ ] Approval gate: Can non-technical understand change?
- [ ] Testing: Dry-run in test environment first
- [ ] Documentation: What it does, who owns it, how to disable

## Quick Wins

1. Automate 1 read-only operation (header scanning, dependency audit)
2. Add timeout + logging to any script
3. Externalize 1 hardcoded credential (move to Secrets Manager)
4. Create runbook: "If automation fails, who do we call?"
5. Set up weekly automation audit (review what changed)
