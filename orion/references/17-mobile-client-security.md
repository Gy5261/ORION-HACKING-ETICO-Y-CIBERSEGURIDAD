# Mobile Client Security - Apps, Devices & Data Protection

## Concepto Fundamental

**Mobile = Highest Risk Attack Surface**
- 85% of workforce uses mobile for work
- 500% increase in mobile malware (3 years)
- 95% of breaches involve mobile
- Devices: broad app permissions, untrusted networks, theft risk

## 5 Principios Fundamentales

1. **MDM (Mobile Device Management)**: Enforce encryption, password policy, app whitelist, remote wipe, patch management
2. **App Security Testing**: Review for weak auth, insecure storage, plaintext communication, reverse engineering
3. **Certificate Pinning**: App trusts only specific server certificate (prevents MITM)
4. **Strong Authentication**: MFA (biometric + PIN), session timeouts, device attestation
5. **Behavioral Detection**: Monitor unusual app access, detect exploits, fast incident response

## Mobile Device Management (MDM)

### What It Does
- Control app installations (whitelist/blacklist)
- Enforce security policies (encryption, passwords, updates)
- Monitor device health (patch status, encryption)
- Remote management (push updates, disable/wipe)

### Popular Platforms
- **Apple**: Jamf, SOTI, Kandji
- **Android**: Google Play EMM, Microsoft Intune
- **Cross**: MobileIron, Ivanti

### Security Policies
✅ Disk encryption required
✅ Min OS version (no EOL)
✅ Password: 8+ chars, uppercase, numbers
✅ App whitelist (approved only)
✅ Jailbreak/root detection
✅ Patch compliance (30 days)
✅ Session timeout (15 mins)
✅ USB debugging disabled

## App Security Testing

### Vulnerabilities
1. Weak authentication (hardcoded passwords, weak tokens)
2. Insecure storage (plaintext secrets on device)
3. Insecure communication (HTTP, unencrypted)
4. Reverse engineering (decompile, extract logic)
5. Code injection (SQL, command injection)
6. Broken crypto (weak algorithms)

### Assessment Methodology
- Static analysis (code review for flaws)
- Dynamic testing (intercept traffic with Burp)
- Authentication testing (bypass attempts)
- Storage forensics (extract secrets)
- Jailbreak testing (bypass controls)

## Certificate Pinning

**Problem**: MITM if CA compromised
**Solution**: App hardcodes "Only trust certificate XYZ"
**Result**: MITM fails even on hostile networks
**Challenge**: Certificate rotation requires app update

## Assessment Phases

**Phase 1** (1 week): Inventory apps, device types, MDM coverage
**Phase 2** (2 weeks): Deploy MDM, enforce policies, enroll devices, monitor compliance
**Phase 3** (2-3 days/app): Static analysis, dynamic testing, auth testing, storage forensics
**Phase 4**: Remediation (update apps, implement pinning, fix auth, deploy detection)

## Real Examples

**Example 1: Hardcoded API Key**
- Researcher decompiles app, finds API key
- Attacker uses key → full backend access
- $5M breach, reputation damage
- Prevention: Never hardcode secrets

**Example 2: Jailbroken Device Compromise**
- Employee jailbreaks iPhone
- MDM not enforced
- Malware steals credentials
- Prevention: Auto-block non-compliant devices

## Checklist

MDM: ✅ Deployed, ✅ __% enrolled, ✅ Encryption, ✅ Policies
Apps: ✅ Reviewed, ✅ MFA, ✅ TLS, ✅ No secrets, ✅ Pinning
Response: ✅ Remote wipe, ✅ Detection, ✅ Playbook

## Key Metrics

- [ ] MDM enrollment: __% (target 95%+)
- [ ] Patch compliance: __% (target 95%+)
- [ ] Apps with MFA: __% (target 100%)
- [ ] Security incidents: __ (target 0)
