# Identity, Endpoint & Active Directory - Defense of the Human & Machine Identity

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe Identity Security?

**The Hard Truth**: 90% of breaches start with compromised credentials (phishing, weak passwords, reuse).

**Attack chain**:
1. Attacker gets credentials (phishing, password spray, OSINT)
2. Attacker logs in legitimately (looks normal in logs)
3. Attacker moves laterally (one account → many accounts)
4. Attacker escalates privilege (user → admin → domain admin)
5. Attacker owns the network (game over)

**Identity Security** breaks this chain at each step:
- ❌ Step 1: MFA + monitoring → attacker can't use stolen password alone
- ❌ Step 2: Behavioral detection → unusual login patterns detected
- ❌ Step 3: Segmentation → lateral movement blocked
- ❌ Step 4: Elevation auditing → privilege escalation alarmed
- ❌ Step 5: Hunting → attacker activity detected

**Why it matters**:
- Identity is the "keys to kingdom"
- If attacker gets valid credentials = hard to detect (logs show legitimate access)
- Traditional firewall/IDS can't help (attacker IS authenticated)
- **Result**: Identity breaches are most costly (breaches often hide for 200+ days undetected)

### 5 Principios Fundamentales de Identity Security

1. **MFA Everywhere (Not Optional)**
   - Password-only = attacker just needs one data breach (uses your password list across sites)
   - MFA = attacker needs password + factor (phone, hardware key, biometric)
   - **Niveles**:
     - Level 1 (Weakest): SMS OTP (interceptable)
     - Level 2: TOTP (Time-based, like Google Authenticator) (good)
     - Level 3: Hardware tokens (YubiKey) or biometric (best)
   - **Donde**: ALL human accounts, especially admin; service accounts less critical

2. **Least Privilege (Minimize Blast Radius)**
   - If user only needs READ to database, don't give ADMIN access
   - If service account only needs to write logs, don't give it EC2 termination rights
   - **Patrón**: Create specific roles (AppServer-ReadDB), not generic (Admin)
   - **Benefit**: If account compromised, damage limited to intended permissions

3. **Separation of Duties (Prevent Insider Abuse)**
   - Single person shouldn't have both: "Approve purchase" + "Pay invoice"
   - Same for tech: Don't let one person approve their own code changes
   - **Implementation**: Require second reviewer, no self-approval
   - **Detección**: Alert if one person trying to do conflicting tasks

4. **Credential Hygiene (Secrets Have Lifecycle)**
   - Passwords age like milk: fresh = good, old = bad
   - Rotate secrets every 90 days (or detection = attacker has stale password)
   - **Tipos de credenciales**:
     - User passwords (rotate every 90 days)
     - API keys (if possible, invalidate on deploy)
     - Service account passwords (rotate every 30-60 days)
     - Certificates (renew before expiry)
   - **Monitoring**: Alert if password hasn't changed in 180 days

5. **Detection Over Prevention (Assume Breach)**
   - Prevention alone doesn't work (humans click phishing)
   - Detection catches compromises when they happen
   - **Pattern**: "Insider logging in from new IP + accessing unusual data" = investigate
   - **Goal**: Reduce dwell time from 200 days (average) to 3 days (your target)

---

## SECCIÓN 2: COMPONENTES TÉCNICOS

### Componente 1: Identity Governance & Access Management (IAM)

**Objetivo**: Audit who has access to what; remove unnecessary permissions.

**Información técnica**:
- **User accounts**: Active, disabled, service, shared
- **Groups**: Membership, nesting (groups inside groups)
- **Roles**: Permissions associated with role
- **Delegation**: Who can create/approve accounts?

**Checklist - IAM Audit**:
- ✅ List all user accounts (human + service)
- ✅ For each: Last login date (if > 1 year = ?)
- ✅ MFA status: Is it enabled? Type (SMS/TOTP/Hardware)?
- ✅ Group memberships: Why is this person in each group?
- ✅ Role analysis: Does role match job?
- ✅ Admin accounts: How many? Who has them? Justified?
- ✅ Service accounts: Are they shared? (should be unique)
- ✅ Credential age: When was password last changed? (> 90 days = overdue)
- ✅ Orphaned accounts: Former employees (disabled? fully removed?)

**Herramientas recomendadas**:
```bash
# Active Directory
Get-ADUser -Filter * -Properties LastLogonDate | Where-Object {$_.LastLogonDate -lt (Get-Date).AddDays(-90)}
# → Find users not logged in 90+ days

Get-ADGroup -Filter * -Properties members | Where {$_.members.count -gt 10}
# → Find large groups (potential misconfiguration)

Get-ADUser -Filter {AdminCount -eq 1}
# → All admin accounts

# Azure AD
Get-AzureADUser -All $true | Where-Object {$_.LastDirSyncTime -lt (Get-Date).AddDays(-90)}

# AWS
aws iam list-users --query 'Users[*].[UserName,CreateDate]' --output table
aws iam list-access-keys --user-name USERNAME  # Check key age
```

---

### Componente 2: Endpoint Security (EDR, Patching, Encryption)

**Objetivo**: Ensure devices are hardened + monitored.

**Información técnica**:
- **EDR (Endpoint Detection & Response)**: CrowdStrike, Microsoft Defender, Sentinel One (monitors for malware/behavior)
- **Encryption**: BitLocker (Windows), FileVault (Mac), dm-crypt (Linux)
- **Patching**: OS patches, driver updates, app updates
- **Inventory**: Who owns what device? Is it approved?

**Checklist - Endpoint Hardening**:
- ✅ EDR agent installed + operational (100% coverage)
- ✅ Disk encryption enabled (BitLocker, FileVault)
- ✅ OS version supported (not EOL versions)
- ✅ Windows Defender or equivalent AV active
- ✅ Firewall enabled (both network + Windows Defender firewall)
- ✅ Automatic patching enabled (OS patches, critical apps)
- ✅ USB/removable media restricted (or monitored)
- ✅ Local admin accounts removed (or monitored)
- ✅ Last patch date < 30 days (not unpatched for months)
- ✅ Antimalware definitions updated (< 7 days old)

**Errores comunes**:
- ❌ EDR disabled "for performance" (false trade-off)
- ❌ Encryption disabled "for convenience" (data at risk)
- ❌ Local admin given to users (can install malware, break controls)
- ❌ No patch enforcement (systems running year-old vulns)

---

### Componente 3: Active Directory Security

**Objetivo**: Hardened directory = harder lateral movement.

**Información técnica**:
- **Kerberos**: Authentication protocol (AD uses this)
- **GPO (Group Policy Objects)**: Configuration pushed from AD to machines
- **Domain trusts**: Relationships between AD domains (can be exploited for lateral movement)
- **Delegation**: Who has rights to reset passwords, create users, modify groups?

**Checklist - AD Security**:
- ✅ LAPS (Local Admin Password Solution) enabled (randomizes local admin passwords)
- ✅ Kerberos signing enforced (blocks certain replay attacks)
- ✅ Credential guard active (protects Kerberos tickets)
- ✅ GPO security practices:
  - [ ] GPOs audited
  - [ ] Restrictive permissions (not "Authenticated Users" = everyone)
  - [ ] Security baseline applied (CIS or NIST)
- ✅ Privileged groups monitored:
  - [ ] Domain Admins (should be 1-2 people)
  - [ ] Enterprise Admins (should exist rarely)
  - [ ] Schema Admins (should exist rarely, rarely used)
- ✅ AD delegation reviewed (who can create/modify accounts?)
- ✅ Legacy protocols disabled (Kerberos RC4 = weak, use AES)
- ✅ Trust relationships minimized (each trust = lateral move risk)

**Herramientas recomendadas**:
```bash
# AD recon (from domain-joined computer)
Get-ADGroupMember -Identity "Domain Admins" -Recursive
# → Who's really a domain admin?

Get-ADObject -Filter {ObjectClass -eq "organizationalUnit"}
# → OU structure (any unusual/suspicious OUs?)

Get-GPO -All
# → All GPOs (review for security baselines)

# Tool: BloodHound (visualizes AD attack paths)
# Import: Get-BloodHoundData
# Analyze: Which users can reach domain admin?
```

---

### Componente 4: Privileged Access Management (PAM)

**Objetivo**: Make admin use temporary elevated access, not permanent.

**Patrón Traditional (BAD)**:
```
- Engineer: "I need to restart service"
- Manager: "OK, I'll make you admin permanently"
- Engineer now: Admin forever (if compromised, attacker has admin forever)
```

**Patrón PAM (GOOD)**:
```
- Engineer: "I need to restart service for 1 hour"
- System: Grants admin rights for exactly 1 hour
- Timer:
  - 00:00 Rights granted, logged
  - 00:59 Warning: "Elevation expires in 1 minute"
  - 01:00 Rights revoked automatically

If compromised within 1 hour: Attacker has limited window
All actions logged: Can forensically trace what was done
```

**Herramientas**:
- HashiCorp Vault (open-source)
- BeyondTrust Privilege Management
- CyberArk PAM
- AWS IAM roles (temporary credentials)

---

### Componente 5: Credential Detection & Monitoring

**Objetivo**: Detect when credentials are compromised BEFORE attacker uses them.

**Monitoring Patterns**:

```markdown
## Alert: Failed Login → Successful Login (Credential Spray Pattern)

Pattern:
1. User account: john.smith
2. 20 failed login attempts from IP 203.0.113.50 (attacker trying password lists)
3. Followed by: 1 successful login from SAME IP (attacker found right password)
4. Followed by: Unusual data access (attacker exploring)

Response:
- Reset john's password immediately
- Reset all service accounts he has access to
- Check what attacker accessed (forensics)
- Revoke attacker's access
```

**Detection Queries** (SIEM/Splunk):

```
# Find failed logins followed by success from same source
index=security (EventID=4625 OR EventID=4624)
| stats count as failures by user, source_ip, EventID
| where failures>10 AND EventID=4624  # >10 failures then success
```

---

## SECCIÓN 3: METODOLOGÍA Identity Audit Paso-a-Paso

### Paso 1: Inventory & Discovery (1 week)

```
1. Export all user accounts (AD, cloud identity, special accounts)
2. Export all groups + membership
3. Export all roles + permissions
4. Document credential types (where are creds stored?)
```

### Paso 2: Access Analysis (1-2 weeks)

```
1. For each account: Determine if active
2. For each account: Justify their permissions
3. For each admin: Is there legitimate reason?
4. For each group: Should members be in it?
```

### Paso 3: Risk Assessment (1 week)

```
1. High-risk accounts: Domain admin, service accounts, shared accounts
2. High-risk permissions: Unrestricted access, excessive privilege
3. High-risk behaviors: Logins outside business hours, new IPs, bulk data access
```

### Paso 4: Remediation (Ongoing)

```
1. Remove unnecessary accounts
2. Reduce privileges
3. Add MFA
4. Rotate credentials
5. Implement PAM for admins
6. Enable monitoring + alerting
```

---

## SECCIÓN 4: CASOS DE ESTUDIO

### Caso 1: Service Account Compromise Led to Domain Admin (Lateral Movement)

**Scenario**: Service account `svc_sql` used by backup job (legitimate).

**Misconfiguration**: SQL DBA made `svc_sql` a domain admin ("easier to manage").

**Attack**:
1. Attacker compromises `svc_sql` (vulnerability in backup software)
2. Attacker now has domain admin rights (unintended)
3. Attacker creates new admin account for persistence
4. Attacker owns domain

**Lesson**: Service accounts should have minimal necessary permissions, not convenience permissions.

---

### Caso 2: Credential Spray Stopped by MFA

**Scenario**: Attacker obtains password list from unrelated breaches; tries passwords against your AD.

**Without MFA**:
- Attacker succeeds on 1% of accounts (common passwords)
- Gets into network
- Moves laterally

**With MFA**:
- Attacker successfully enters password
- MFA prompt appears
- Attacker doesn't have second factor
- Login fails
- Alert triggered (attempted login without MFA?)

**Result**: Attack prevented; attacker gives up

---

## SECCIÓN 5: TEMPLATES & CHECKLISTS

### Template 1: Identity Audit Checklist

```markdown
# Identity & Endpoint Security Audit Checklist

## User Account Audit

- [ ] Total user count: ___
- [ ] MFA adoption: ___% (target: 100%)
- [ ] Users without MFA: ___ (list them)
- [ ] Orphaned accounts (disabled but not deleted): ___
- [ ] Shared accounts: ___ (should be none)
- [ ] Service accounts: ___ (verify they're unique)

## Privileged User Audit

- [ ] Domain Admin count: ___ (should be 1-3)
- [ ] Temporary elevation used: Yes/No (if No, implement PAM)
- [ ] Admin login audit enabled: Yes/No
- [ ] Admin actions logged: Yes/No

## Endpoint Audit

- [ ] EDR coverage: ___% (target: 100%)
- [ ] Disk encryption: ___% (target: 100%)
- [ ] Patch compliance: ___% (target: >95%)
- [ ] Antimalware current: Yes/No
- [ ] Local admin removed: ___% (target: 90%+)

## Active Directory Audit

- [ ] LAPS enabled: Yes/No
- [ ] Kerberos signing enforced: Yes/No
- [ ] Credential Guard active: Yes/No
- [ ] Legacy protocols disabled (RC4, LM): Yes/No
- [ ] Domain trusts documented: Yes/No (minimize)

## Detection & Monitoring

- [ ] Failed login monitoring: Yes/No
- [ ] Privilege escalation alerts: Yes/No
- [ ] Unusual login patterns detected: Yes/No
- [ ] SIEM rule: Credential spray: Yes/No
- [ ] SIEM rule: Golden ticket attacks: Yes/No
```

---

## CONCLUSIÓN

**Identity = Keys to Kingdom**

- Compromised identity = attacker is "legitimate user" (hardest to detect)
- Identity controls = most cost-effective ($ prevents most expensive breaches)
- MFA alone = 99% effective against password-based attacks (highest ROI single control)

**Priority Ranking**:
1. MFA (highest impact)
2. Monitoring (detect breaches)
3. PAM (limit admin damage)
4. Endpoint hardening (prevent infection)
5. Legacy protocol removal (reduce attack surface)
