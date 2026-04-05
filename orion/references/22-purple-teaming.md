# Purple Teaming - Red Team Capabilities Validated by Blue Team Detection

## Concepto

**Goal**: Test detection capabilities by running controlled attack scenarios

**Purple Team = Red Team + Blue Team**:
- Red team: Attacks (safely) to test defenses
- Blue team: Detects and responds
- Purple team: Both working together to improve detection

**Key Question** → "Did our controls DETECT this attack?" (Not "did we stop it")

## Red Team vs Purple Team

**Red Team**:
- "Can we breach the system?"
- Goal: Compromise objective
- Output: Vulnerability report

**Purple Team**:
- "Can we DETECT the breach?"
- Goal: Improve detection/response
- Output: Detection coverage report, tuning recommendations

## Common Purple Team Exercises

**Exercise 1: Credential Spray**
- Attack: 1000 failed logins in 5 minutes
- Expected Detection: Alert on login anomaly, block IP
- Test: Did SIEM detect? Did SOC get alert? Response time?
- Result: If no alert → add detection rule

**Exercise 2: Process Hollowing (Malware Technique)**
- Attack: Malware injects code into legitimate process (svchost.exe)
- Expected Detection: Endpoint alert on process injection
- Test: Did endpoint detect? Did alert reach SOC?
- Result: If no alert → tune process injection detection

**Exercise 3: Data Exfiltration**
- Attack: Copy large file to USB/cloud
- Expected Detection: Large file access alert
- Test: Was action logged? Did alert fire? Response time?
- Result: If missed → add file access auditing

**Exercise 4: Lateral Movement**
- Attack: Compromise 1 server, pivot to database server
- Expected Detection: Unusual network traffic, authentication failure
- Test: Was lateral movement seen? Alert timing?
- Result: If delayed → reduce detection window alert threshold

**Exercise 5: Privilege Escalation**
- Attack: Local exploit to gain admin rights
- Expected Detection: Process privilege elevation alert
- Test: Did endpoint detect? Time to alert?
- Result: If missed → add syscall-level monitoring

## Purple Team Cycle

**Phase 1: Plan** (1 week)
- Choose attack scenario (credential spray, data exfil, malware)
- Define scope & safety controls (isolated environment, approved users)
- Expected evidence (what logs/alerts should we see)

**Phase 2: Execute** (1 day)
- Red team runs safe controlled attack
- Blue team monitors in real-time
- Evidence collection

**Phase 3: Review** (1 week)
- Questions:
  - What events SHOULD have been logged? Were they?
  - What alerts SHOULD have fired? Did they?
  - How long did detection take? (MTTD)
  - What context was missing for triage?

**Phase 4: Improve** (1-2 weeks)
- Update detection rules
- Adjust log collection
- Tune alert thresholds
- Retrain SOC on new rules

## Real Examples

**Example 1: Credential Spray Test**
- Scenario: 100 failed logins + 2 successful
- Expected: Alert + SOC investigation
- Reality: Alert fired after 30 logins (5 min delay)
- Improvement: Lowered threshold to 10 failures = 30 sec detection
- Value: Caught 3 actual attack campaigns after improvement

**Example 2: Malware Test**
- Scenario: Inject code into Windows process
- Expected: Endpoint detects process injection
- Reality: No detection (signature-based AV missed it)
- Improvement: Enabled behavior-based detection
- Value: Detected 2 zero-days before external disclosure

**Example 3: Lateral Movement Test**
- Scenario: Compromise web server, pivot to database
- Expected: Network segmentation blocks or alerts
- Reality: Segmentation worked, but alert took 45 minutes
- Improvement: Added real-time network analytics
- Value: MTTD reduced from 45 min to 2 min

## Key Metrics

**Detection Coverage** (should be 80%+ of scenarios)
- How many attack scenarios triggered detection?
- Target: 100% coverage of critical attack paths

**Mean Time to Detect (MTTD)**
- How fast did detection fire after attack started?
- Target: <5 min for critical attacks

**Mean Time to Respond (MTTR)**
- How fast did SOC respond after alert?
- Target: <15 min

**False Positive Rate**
- How many legitimate activities trigger alerts?
- Target: <10% (too many → alert fatigue, slower response)

## Governance

**Approval Required**:
- Security team: Scenario approval
- Business: Window approval (non-business hours preferred)
- Compliance: Scope verification (no real data exposure)

**Scope Boundaries**:
- ✅ Allowed: Isolated test environments, approved attack scenarios
- ✅ Allowed: Production detection rules (monitoring only, no changes)
- ❌ NOT ALLOWED: Production systems with business impact
- ❌ NOT ALLOWED: Real customer data in testing

## Checklist

- [ ] Purple team program defined (quarterly exercises)
- [ ] Scenarios documented (5+ attack types)
- [ ] Safety controls (isolation, scope, approval)
- [ ] Detection coverage baseline (80%+ target)
- [ ] MTTD/MTTR tracking
- [ ] Improvements documented & rules updated
- [ ] SOC training on new detection scenarios
- [ ] Regular cadence (monthly or quarterly)

## Quick Wins

1. Run 1 purple team exercise this month (pick easiest: credential spray)
2. Document current detection coverage (what scenarios work)
3. Identify biggest gap (what attack type isn't detected)
4. Update 1 detection rule based on gap
5. Schedule monthly purple team exercise
