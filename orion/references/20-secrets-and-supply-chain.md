# Secrets & Supply Chain Security - API Keys, Credentials, Dependencies

## Concepto

**Two Core Threats**:
1. Secrets in code (API keys, passwords, tokens → exposed if source revealed)
2. Compromised dependencies (malicious package, outdated libraries → supply chain attack)

## Secrets Problem

**Bad**: API key hardcoded in source
```
api_key = "sk-12345abcde"  // EXPOSED
```

**Good**: API key in environment variable
```
api_key = os.environ['API_KEY']  // Only in deployed system
```

## Types of Secrets

- API keys (AWS, payment processors, third-party services)
- Database passwords
- OAuth tokens
- Certificates & keys
- Private encryption keys
- SSH keys
- Webhook signatures

## Secret Management Solutions

**Local/Self-Hosted**:
- HashiCorp Vault (industry standard)
- Sealed Secrets (Kubernetes)
- SOP/age (file encryption layer)

**Cloud-Native**:
- AWS Secrets Manager
- Azure Key Vault
- GCP Secret Manager

**What They Do**:
1. Store secrets encrypted
2. Rotate keys on schedule (30-90 days)
3. Audit log all access
4. Distribute to applications at runtime
5. Revoke immediately if compromised

## Secret Exposure Detection

**Tools**:
- TruffleHog (scans git history for hardcoded secrets)
- GitGuardian (CI/CD integration, blocks commits with exposed secrets)
- SAST scanners (find hardcoded secrets in code)

**Real Example**: Developer accidentally commits API key
- GitGuardian alerts immediately
- Key revoked before deployment
- New key distributed
- Cost: Minutes of delay, Zero breach

## Supply Chain Attacks

**Attack**: Attacker compromises npm/PyPI package
- 1M projects depend on package A
- Attacker injects malware (steals secrets, backdoor)
- All 1M projects compromised transitively

**Real Example**: "left-pad" package removed from npm
- 500+ packages broke (dependency on left-pad)
- Shows fragility of supply chain

## Dependency Management

**Strategy**:
1. Software Bill of Materials (SBOM) - list all dependencies
2. Vulnerability scanning (npm audit, pip audit, trivy)
3. Update policy (patch critical within 1 week)
4. Frozen dependencies (pin versions, don't auto-upgrade)
5. Audit log (why, who, when updated)

**Tools**:
- npm audit (Node.js)
- pip audit (Python)
- Dependabot (GitHub, auto-PRs for updates)
- Snyk (SaaS vulnerability scanning)

## Vendor Risk Management

**Before using vendor**:
- Security questionnaire (SOC 2, penetration test, incident response)
- Contracts: SLAs, data location, incident notification
- Access review: What data, how long, can delete?
- Monitoring: Security breaches in news

**Ongoing**:
- Annual renewal (refresh security posture)
- Incident reports (if vendor has breach)
- Access revocation (if vendor contract expired)

## Assessment Phases

**Phase 1** (1 week): Audit secrets in code (TruffleHog, SAST)
**Phase 2** (1 week): Install secret manager, migrate secrets from code
**Phase 3** (1 week): Dependency audit (SBOM, vulnerability scan, update policy)
**Phase 4** (ongoing): Vendor risk management, continuous scanning

## Real Examples

**Example 1**: npm malware package
- Attacker @typosquatted popular package
- 1000+ projects installed silently
- Stole shipping information from CI/CD
- Detected: 6 hours, fixed: 12 hours

**Example 2**: AWS key in GitHub
- Developer commits production key
- Attacker scans GitHub for keys (automated)
- Spins up EC2 instances, mines crypto
- Cost: $50K+ in 4 hours
- Prevented by: GitGuardian (had it enabled)

## Checklist

- [ ] Secrets audit: No hardcoded secrets in code
- [ ] Secret manager: Implemented & operational
- [ ] Rotation: Keys rotate 30-90 days
- [ ] Access: Audit log of all secret access
- [ ] Git scanning: TruffleHog/GitGuardian enabled
- [ ] SBOM: Dependency list maintained
- [ ] Vuln scan: npm/pip/trivy running regularly
- [ ] Update policy: Critical patches within 1 week
- [ ] Vendor list: All vendors documented
- [ ] Vendor risk: Periodic security review (annual)

## Quick Wins

1. Run TruffleHog on git history now (find existing secrets)
2. Enable GitGuardian in GitHub
3. Run `npm audit` or `pip audit` (find vulnerable dependencies)
4. Create update policy (critical = 1 week)
5. Establish vendor risk documentation (sheet with all vendors)
