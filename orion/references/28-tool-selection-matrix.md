# Tool Selection Matrix - Choosing Right Tool for Right Job

## Concepto

**Golden Rule**: The best tool is NOT the most powerful, but the one that:
1. **Solves the specific problem** (don't overkill)
2. **Minimizes new risk** (simplicity = fewer bugs)
3. **Produces usable evidence** (auditors can understand it)
4. **Reduces attack surface** (fewer dependencies = fewer vulnerabilities)

## Assessment Tool Matrix

| Need | Preferred Method | Why | Avoid |
|------|-----------------|-----|-------|
| **HTTP Headers** | `curl -I` | Fast, no tool, output clear | Heavy scanner (aggressive, noisy) |
| **TLS Certificate** | `openssl s_client` | Built-in, parseable, shows expiry | Creating custom scripts |
| **Port Scan** | Nessus / nmap (scoped) | Approved, documented, has support | Custom scripts (easier to abuse) |
| **Web Vulnerability** | OWASP ZAP (passive) | Good balance, free, FP manageable | Aggressive scanning (avoids production impact) |
| **Code Analysis** | Semgrep / GitHub CodeQL | Language-aware, fast, low FP | Generic grep (misses context) |
| **Cloud Config** | Prowler / ScoutSuite | Built for cloud, maps to standards | Custom scripts (cloud APIs change frequently) |
| **Dependency Audit** | npm/pip audit or Snyk | Standard, integrated, updates current | Manual review (incomplete, slow) |
| **Log Analysis** | ELK / Datadog | Searchable, correlates events | Grep'ing raw logs (error-prone) |

## Attack Surface Reduction Principle

**High-Surface Tools**:
- ❌ Container-based scanners (docker install + config + secrets)
- ❌ Python script with 50 dependencies (pip install → dependency chain)
- ❌ Agents on every endpoint (communication channel, privileges)

**Low-Surface Tools**:
- ✅ Built-in OS tools (curl, openssl, grep, cut, awk)
- ✅ Single-binary tools (go-compiled tools, no runtime)
- ✅ Read-only tools (no code execution capability)

**Example Decision**:
- Goal: Find API endpoints
- Option A: Burp Suite Pro (enterprise, 500+ features, requires license + config + training)
- Option B: Custom Python script (10 dependencies, ongoing maintenance, potential bugs)
- Option C: `curl` + `grep` + `sed` (built-in, 0 dependencies, works everywhere)
- **Choice**: Option C (lowest risk, solves the problem)

## Real-World Examples

**Example 1: Header Audit**

Bad approach:
```bash
# Using heavy web vulnerability scanner
./scanner --full-scan --aggressive https://target.com > report.html
# Issues: 
# - 30 min runtime, lots of noise
# - May overload target
# - False positives for headers
# - Requires licensing
```

Good approach:
```bash
# Using curl (2 seconds)
curl -Is https://target.com | grep -E "X-Frame-Options|X-Content-Type-Options|Strict-Transport"
# Fast, clear, auditable, no licensing
```

**Example 2: Vulnerability Scanning**

**Before**: Full network scanner (aggressive)
- Problem: Client production system crashed during scan
- Cause: Aggressive OS fingerprinting + DoS checks
- Cost: $200K production incident

**After**: Targeted, approved scan
- Plan: Coordinate with client, scope defined
- Tool: Nessus with "lite" profile
- Result: Found same issues, 0 impact

**Example 3: Dependency Check**

**Before**: Created custom script to parse package files
- Problem 1: Missed indirect dependencies
- Problem 2: Vulnerability database out of date
- Problem 3: Maintenance burden (update script constantly)

**After**: Used Snyk + npm audit
- Problem 1 fixed: Snyk knows dependency tree
- Problem 2 fixed: Vulnerability DB updated in real-time
- Problem 3 fixed: Snyk maintains database

## Decision Framework

When choosing a tool, ask:

**1. Does tool solve THIS specific problem? (Not "can it do X")**
```
Goal: Find missing security headers
Tool Option A: Full web app scanner (can do 50 things, I need 1)
Tool Option B: curl (does exactly what I need)
→ Choose B
```

**2. What's the new risk introduced?**
```
Tool Option A: Python script (requires 15 pip packages, 3 could have vulns)
Tool Option B: Go binary (compiled, no runtime, audited)
→ Choose B
```

**3. Can auditor/client understand the evidence?**
```
Tool Option A: Custom JSON output (weird format, hard to interpret)
Tool Option B: curl output (standard HTTP, everyone understands)
→ Choose B
```

**4. What's the support/maintenance burden?**
```
Tool Option A: Custom script (I maintain forever, API changes break it)
Tool Option B: Mature open-source (100+ contributors, community maintained)
→ Choose B
```

## Tool Risks by Category

**Heavy Enterprise Tools** (Burp Suite, Nessus, etc.)
- ✅ Pros: Full-featured, vendor support, many integrations
- ❌ Cons: License costs, slow, complex configuration, often overkill
- ✅ Use when: Client has budget, complex use case, long-term relationship

**Custom Scripts** (Python, Bash, etc.)
- ✅ Pros: Tailored to exact need, understand code, no licensing
- ❌ Cons: Maintenance burden, potential bugs, dependency management
- ✅ Use when: Simple problem, you maintain it, open-source alternatives don't exist

**Open-Source Tools** (Semgrep, Prowler, OWASP ZAP)
- ✅ Pros: Community-maintained, free, auditable, actively developed
- ❌ Cons: Community support (not vendor), potential false positives
- ✅ Use when: Problem is common (community has solution), you can troubleshoot

**Built-in OS Tools** (curl, openssl, grep, awk)
- ✅ Pros: Zero dependencies, always available, lowest risk
- ❌ Cons: Limited features, requires scripting knowledge
- ✅ Use when: Simple information gathering, evidence must be crystal clear

## Approved Tools for ORION

**Read-Only Assessment**:
- ✅ curl (HTTP headers, APIs)
- ✅ openssl (TLS certificate inspection)
- ✅ nmap (scoped port discovery, requires approval)
- ✅ Semgrep (code analysis)
- ✅ OWASP ZAP (passive scanning)
- ✅ Prowler (AWS configuration)

**Analysis/Reporting**:
- ✅ Python + standard libs (CSV, JSON parsing)
- ✅ jq (JSON query)
- ✅ grep/sed/awk (log analysis)

**NOT APPROVED** (Without explicit approval):
- ❌ Sqlmap / Nikto (aggressive, can break things)
- ❌ Metasploit (exploitation tool, very risky)
- ❌ Commercial tools (licensing, client must approve)
- ❌ Custom exploit code (legal + liability issues)

## Checklist

- [ ] Tool solves SPECIFIC problem (not "as many as possible")
- [ ] Security dependencies documented
- [ ] No unauthorized modifications to client systems
- [ ] Evidence format is auditor-friendly
- [ ] Tool licensed/approved (commercial tools need approval)
- [ ] Scan scoping documented (what are we testing, what are we NOT testing)
- [ ] False positive rate acceptable (<5% for good tools)
- [ ] Support/maintenance plan (who fixes it if broken?)

## Quick Wins

1. Create 1-page "approved tools" list for your team
2. Document 1 tool you currently use (why it was chosen, when to use it)
3. Replace 1 custom script with open-source equivalent (maintain fewer tools)
4. Add "tool selection" question to assessment planning checklist
5. Document 1 tool risk (something you've seen go wrong)
