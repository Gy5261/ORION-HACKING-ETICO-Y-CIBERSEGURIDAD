# Evidence & Logging Spec - Forensic Data Collection & Reporting

## Concepto

**Goal**: Collect evidence that:
1. Proves what happened (forensic value)
2. Doesn't expose more secrets/PII (redaction)
3. Is reproducible (timestamp, method, asset)
4. Is audit-safe (can be used in court/compliance)

## Minimum Evidence Components

Every piece of evidence should include:

**Timestamp**: When was this captured?
- Format: ISO 8601 (2026-04-05T14:20:30Z)
- Timezone: Always explicit (UTC recommended)
- Why: Establishes timeline, prevents tampering

**Asset Identifier**: What was tested?
- Example: "api.example.com" (domain/hostname/IP)
- Why: Scope clarity, avoids confusion with similar systems

**Method Used**: How was evidence gathered?
- Example: `curl -H "Authorization: Bearer $token" https://api.example.com/admin`
- Why: Reproducibility, auditor can verify

**Raw Result**: What came back?
- Example: HTTP 200, JSON response with user list
- Why: Unmodified evidence is forensically stronger

**Brief Interpretation**: What does this mean?
- Example: "API endpoint accessible without authentication, leaking user emails/phones/addresses"
- Why: Context for non-technical stakeholders

**Redactions Applied**: What was sanitized?
- Example: "Redacted token value (was 48-char hex string)"
- Why: Shows we removed secrets, but honest about what was hidden

## Evidence Logging Template

```markdown
### Evidence: [Title]

**Timestamp**: 2026-04-05T14:20:30Z  
**Asset**: api.example.com  
**Method**: `curl -I https://api.example.com`  
**Result**: 
```
HTTP/2 200 
Content-Type: application/json
Server: nginx/1.18.0
X-Frame-Options: (not present)
X-Content-Type-Options: (not present)
```

**Interpretation**: API lacks SAMEORIGIN frame protection and NOSNIFF header. Server type exposed (nginx). Combined with CORS-open configuration, allows potential clickjacking attacks.

**Redactions**: No secrets in this evidence.
```

## Data Redaction Rules

**MUST REDACT**:
- Full credit card numbers (show only last-4: ```****1234```)
- Full SSN (show only last-4: ```***-**-1234```)
- API keys / tokens (show only type + length: ```[AWS_KEY_48_chars]```)
- Passwords / authentication tokens (show only token type: ```[JWT_TOKEN]```)
- PII details (names, home addresses, phone) → generalize (```[INTERNAL_USER_1]```)
- Internal IP addresses (if sensitive) → mask (```[INTERNAL_IP_1]```)
- Email addresses when unnecessary → redact domain (```analyst@[REDACTED_DOMAIN]```)

**OK TO INCLUDE**:
- HTTP status codes (200, 401, 500)
- Header names (Content-Type, Authorization, X-Frame-Options)
- Domain names / public IPs (scope is already known)
- Generic error messages (sanitized)
- Methodology descriptions
- Business impact
- Timing/performance data

## Evidence Size Management

**Problem**: Raw device output = 10GB, most irrelevant

**Solution**: Capture & summarize

```markdown
### Network Capture Evidence

**Full Capture**: Stored in `/secure/pcap/2026-04-05-14-20.pcap` (48 GB)  
**Relevant Packets**: 
- Packet 45: DNS query for suspicion.example.com (no response)
- Packet 120: HTTP GET to malware.net (200 response, 2MB payload)
- Packet 1240: Callback to C2 server (encrypted, TLS 1.2)

**Summary**: Host initiated DNS request to suspicious domain, received 404 from malware.net CDN, established encrypted callback channel to external C2.
```

## Logging for Assessment Scripts

Every script should be able to capture:

```yaml
Assessment Log Entry:
  timestamp: 2026-04-05T14:20:30Z
  script: http_surface_audit.py
  input_params:
    target: api.example.com
    port: 443
    timeout: 30s
  execution:
    start: 2026-04-05T14:20:30Z
    end: 2026-04-05T14:22:15Z
    duration: 105s
  results:
    checks_run: 42
    issues_found: 7
    timeout_errors: 0
  errors: null
  summary: "7 critical findings: CORS open, missing security headers, outdated TLS"
```

## Real-World Examples

**Example 1: SQL Injection Evidence**
```markdown
### Evidence: SQL Injection in Search Parameter

**Timestamp**: 2026-04-05T14:20:30Z  
**Asset**: shop.example.com  
**Method**: `curl "https://shop.example.com/search?q=1' OR '1'='1"`  
**Result**: 
```
HTTP 200
[HTML showing all products unfiltered, bypassing search]
[Database error: Unclosed quotation]
```

**Interpretation**: Application uses unsanitized user input in SQL query. Attacker can bypass authorization, read all data, modify data, potentially execute commands on database server.

**Evidence Quality**: Reproducible, timestamped, shows exact payload + result
```

**Example 2: Secret in Code Evidence**
```markdown
### Evidence: AWS Key Hardcoded in Source

**Timestamp**: 2026-04-05T16:45:22Z  
**Asset**: GitLab repo / internal-tools / main branch  
**Method**: `grep -r "AKIA" .` (AWS access key pattern search)  
**Result**:
```
src/config.py:67: AWS_ACCESS_KEY_ID="AKIA12345ABCDEFGHIJK"
```

**Interpretation**: Production AWS credentials exposed in source code repository. Visible to: all employees with repo access, all CI/CD logs, GitHub if ever made public. Risk: Unauthorized AWS resource access, data exfiltration, crypto mining.

**Action Taken**: Key immediately rotated + revoked
```

## Audit Trail for Sensitive Operations

When dealing with sensitive data/findings:

```markdown
## Audit Trail: Evidence Handling

| Timestamp | Action | Who | Reason |
|-----------|--------|-----|--------|
| 2026-04-05 14:20 | Evidence collected | analyst1 | Initial assessment |
| 2026-04-05 16:30 | Evidence reviewed | manager1 | Severity confirmation |
| 2026-04-05 18:00 | Evidence archived | compliance1 | Legal hold (data breach) |
| 2026-04-06 09:00 | Evidence destroyed | analyst1 | Post-incident cleanup (60d retention) |

**Retention Policy**: 60 days for non-breach assessments, 7 years for data breaches (legal requirements)
```

## Checklist

- [ ] Every evidence piece has timestamp (ISO 8601 format)
- [ ] Asset clearly identified (domain/IP/system name)
- [ ] Method documented (command/tool/steps used)
- [ ] Raw result included (unmodified output)
- [ ] Brief interpretation provided (what it means)
- [ ] Redactions documented (what was hidden, why)
- [ ] Evidence stored securely (encrypted, access logs)
- [ ] Retention policy clear (when to delete)
- [ ] Audit trail for sensitive findings (who handled it, when)

## Quick Wins

1. Create 1 evidence template specific to your assessment type (web, cloud, etc.)
2. Document your redaction policy (which data MUST be hidden)
3. Version your logging scripts (timestamp every execution)
4. Establish 1 secure evidence store (encrypted folder + access logs)
5. Create 1 example "well-written" finding using template above
