# Remediation Patterns - Translating Findings Into Actionable Fixes

## Concepto

**Goal**: Take a security finding and create a fix that:
1. **Actually addresses the root cause** (not just the symptom)
2. **Is testable** (how do we confirm it's fixed?)
3. **Accounts for residual risk** (what danger remains?)
4. **Fits in the business timeline** (is it realistic?)

## Core Pattern: Problem → Root Cause → Fix → Test → Residual Risk

### Example: Unencrypted Database

```markdown
## Finding: Database Accessible Without Encryption

**Problem**: Customer data (names, SSNs, addresses) stored unencrypted in PostgreSQL

**Root Cause**: 
- Database enabled when deployed (no security baseline review)
- No TLS requirement in connection strings
- Development practice became production standard

**Fix**:
1. Enable TLS in PostgreSQL (modify postgresql.conf + restart)
2. Force TLS-only connections (update pg_hba.conf)
3. Rotate database credentials (all apps must use new creds)
4. Verify from app side: connection string updated + tested

**Test**:
- Can connect with old connection string? Should FAIL (✓ verified)
- Can connect with TLS required? Should SUCCEED (✓ verified)
- Data still accessible? YES (✓ business function preserved)

**Residual Risk**:
- TLS CA certificate could be compromised (accepted)
- Someone inside network still sees encrypted traffic (insider threat = separate issue)

**Owner**: Database team  
**Timeline**: 24h to implement, 48h for all apps to roll out new creds
```

## Common Remediation Patterns

### Pattern 1: Unnecessary Public Access

**Symptom**: S3 bucket is publicly readable

**Root Cause**:
- Misconfigured bucket policy (somebody copy-pasted whitelist-all policy)
- No automated checks to prevent public configs

**Remediation**:
1. **Immediate**: Restrict bucket to private (remove public read permission)
2. **Verify**: Try accessing as anonymous user (should fail)
3. **Prevent**: Enable S3 Block Public Access at organization level
4. **Detect**: CloudTrail alerting on bucket policy changes

**Test Evidence**:
```bash
# Before: Anonymous user can list objects
aws s3 ls s3://bucket-name --no-sign-request
# Result: Lists all objects (BAD)

# After: Anonymous user access denied
# Result: Access Denied (GOOD)
```

### Pattern 2: Over-Permissioned Service Account

**Symptom**: Database admin accidentally deletes all customer records, nobody can track who did it

**Root Cause**:
- Service account has "admin" role (can do everything)
- No audit logging on admin actions
- No separate roles for different functions

**Remediation**:
1. Create limited-role service account (read: users, orders; NOT alter, delete)
2. Keep admin account separate (only for DBA emergencies)
3. Every admin action: logged + requires approval
4. Quarterly access review (is this account still needed?)

**Test Evidence**:
```
Service Account: "app-database-reader"
Current Permissions: 
- SELECT on users, orders, products (read-only)
- NO INSERT, UPDATE, DELETE

Admin account: "dba-admin"  
- Full permissions (kept separate)
- Requires MFA + approval

Audit Log:
- 2026-04-05 14:20: user1 deleted record (WHERE id=123) — LOGGED
```

### Pattern 3: Secrets Management

**Symptom**: AWS key in GitHub commit history (can't just delete, history is forever)

**Root Cause**:
- Developer didn't know about Secrets Manager
- No pre-commit hook to catch secrets
- No secrets scanning in CI/CD

**Remediation**:
1. **Immediate**: Rotate compromised key (revoke old, issue new)
2. **Verify**: Scan git history for other exposed secrets (TruffleHog)
3. **Implement**: Move all secrets to AWS Secrets Manager
4. **Prevent**: Enable GitGuardian in GitHub (blocks commits with secrets)

**Test Evidence**:
```
Before: 
git log | grep "AKIA" (finds old exposed key)

After:
- Old key: REVOKED (confirmed in AWS IAM)
- New key: In Secrets Manager (retrieved via API, not in code)
- GitGuardian: ENABLED (would have blocked this)
```

### Pattern 4: Insufficient Logging

**Symptom**: Incident happens, nobody knows what occurred (no audit trail)

**Root Cause**:
- Logging disabled by default (performance concerns)
- No centralized log storage
- Logs deleted too quickly

**Remediation**:
1. Define minimum logging (what events MUST be logged?)
   - Failed authentication attempts
   - Admin actions (user creation, permission changes)
   - Data access (who read sensitive data)
2. Ship to central SIEM (AWS CloudWatch, Splunk, etc.)
3. Set 90-day retention (minimum for incident response)
4. Alert on suspicious patterns (100+ failed logins = block)

**Test Evidence**:
```
Logging Policy:
- All auth attempts: logged
- All admin changes: logged + timestamp
- Data access: logged if sensitive (PII, payments)

Sample Log Entry:
2026-04-05T14:20:30Z user1 failed_login attempt=3 source_ip=203.0.113.15
2026-04-05T14:21:15Z user1 successful_login source_ip=203.0.113.15
2026-04-05T14:22:00Z admin1 created_user new_user=john.doe role=engineer
```

### Pattern 5: Outdated Dependency

**Symptom**: Vulnerability CVE-2026-1234 disclosed, affects library we use

**Root Cause**:
- Library dependency pinned to old version (nobody updated)
- No automated checking for vulnerabilities
- Developer didn't think security updates were urgent

**Remediation**:
1. Run vulnerability scan (npm audit, pip audit, Snyk)
2. Update to patched version (if available)
3. Test thoroughly (version change could break something)
4. CI/CD integration (future: auto-alert on new vulnerabilities)

**Test Evidence**:
```
Before: npm audit
  Severity: high
  Package: lodash
  Version: 4.17.15 (vulnerable)

After: npm audit
  Package: lodash
  Version: 4.17.21 (patched)
  Result: No vulnerabilities
```

## Good Remediation Checklist

Every remediation should answer:

- [ ] **What**: Specifically what needs to change?
- [ ] **Where**: Which system/code/config needs change?
- [ ] **Who**: Which team owns this fix?
- [ ] **When**: What's the realistic timeline?
- [ ] **How to verify**: What proves it's fixed?
- [ ] **Residual risk**: What danger remains after fix?
- [ ] **Success criteria**: How do we measure success?

## Real-World Example: 90-Day Remediation Plan

```markdown
## Remediation Project: Zero-Trust Network

Finding: Network lacks microsegmentation (anyone can reach any service)

Timeline:
- Week 1-2: Network audit (document current traffic patterns)
- Week 3-4: Design segmentation rules (which services can talk?)
- Week 5-8: Deploy network policies (firewall rules, ACLs)
- Week 9: Test & tune (validate business still works)
- Week 10: Monitor (watch for new traffic patterns, adjust)
- Week 11-12: Final testing & documentation

Success:
- Network traffic logged & analyzed (who talks to whom)
- Microsegmentation rules enforced (blocked unauthorized traffic)
- Incident response improved (can isolate compromised segment)
- Measurable: Lateral movement time increased from 10 sec to 10 min

Residual Risk:
- Insider threat still possible (internal attacker can still move within segment)
- Application-layer attacks still possible (network can't see inside encrypted traffic)
```

## Checklist

- [ ] Root cause identified (not just symptom)
- [ ] Fix is specific & measurable
- [ ] Testability defined (how to verify)
- [ ] Residual risk acknowledged
- [ ] Owner assigned + timeline realistic
- [ ] Success criteria clear
- [ ] Monitoring in place (to detect regression)
- [ ] Documentation complete

## Quick Wins

1. Take 1 recent finding, document remediation using template above
2. Define "done" criteria for 1 fix type (what proves it's complete?)
3. Add residual risk acknowledgment to next report (show realistic what's left)
4. Document 1 remediation that took longer than hoped (lessons learned)
5. Create 1-page "standard fixes" reference (quick URL to common remediation patterns)
