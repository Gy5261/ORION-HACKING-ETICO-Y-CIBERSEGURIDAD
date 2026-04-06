# 04: Network Security - Descubrimiento de Superficie & Segmentación

## SECCIÓN 1: CONCEPTO FUNDAMENTAL (1-250 líneas)

### ¿Por Qué Network Security Importa?

La red es la autopista. Si no controlas quién entra y sale, los atacantes tienen acceso irrestricto.

**Problemas sin auditoría:**
- ❌ Puertos innecesarios expuestos (legacy services)
- ❌ TLS débil/expirado (man-in-the-middle posible)
- ❌ Segmentación ausente (attacker se mueve lateralmente)
- ❌ Administración expuesta (RDP, SSH, WinRM desde internet)
- ❌ Firewall rules demasiado amplias (172.16.0.0/8 abierto = cualquier cosa)
- ❌ No hay visibilidad (nadie sabe qué servicios corren)

**Solución**: Inventario metódico + baseline + validación segura

---

### 6 Principios de Seguridad de Red

#### Principio 1: DISCOVERY PASIVO PRIMERO

No scanees puertos sin antes entender qué debería estar ahí.

```bash
# ✅ CORRECTO: Primero, documentación
cat /docs/architecture.md  # Qué servicios son esperados?
nslookup *.example.com     # Qué IPs existen?
whois 10.0.0.0/8          # A quién pertenece este rango?

# ❌ INCORRECTO: Scanning aleatorio
nmap -p- 10.0.0.0/8       # Demasiado ruido, demasiado tiempo
```

#### Principio 2: BAJO IMPACTO

Discovery no debe romper nada.

```bash
# ✅ BAJO IMPACTO
nmap -sn 10.10.0.0/24                          # ICMP ping only
nmap --osscan-guess -Pn 10.10.0.15             # OS guessing, no DoS risk
openssl s_client -connect host:443             # TLS check (read-only)

# ❌ ALTO RIESGO
nmap -p- -sS --script vuln 10.10.0.0/24        # Aggressive + scripts
nslookup @external.nameserver internal-ip      # Can cause logging alerts
```

#### Principio 3: SEPARAR INTERNO DE EXTERNO

La exposición desde internet ≠ la exposición desde red corporativa.

```
Severidad según la exposición:

INTERNET → Service X = CRITICAL (cualquiera puede atacar)
Corporate LAN → Service X = MEDIUM (insiders + lateral movement)
Isolated segment → Service X = LOW (defense in depth)
```

#### Principio 4: CONTEXT MATTERS

Un puerto abierto no = vulnerable. Necesitas entender:

```
Puerto 22 abierto:
├─ Si SSH está en DMZ expuesto a internet → CRITICAL ❌
├─ Si SSH está en internal network con VPN required → OK ✅
├─ Si SSH permite key-based only + 2FA → SECURE ✅
└─ Si SSH permite password + no MFA → CRITICAL ❌
```

#### Principio 5: TLS = BASELINE

Si algo cruza la red, debe estar encrypted.

```bash
# ✅ CORRECTO: TLS 1.2+, ciphers modernas
SSLLabs: A+ grade
TLS version: 1.3 preferred, 1.2 minimum
Ciphers: ECDHE-RSA-AES256-GCM-SHA384, CHACHA20-POLY1305

# ❌ INCORRECTO
SSLLabs: F grade (RC4, SSLv3)
Self-signed cert válido 10 años
Diffie-Hellman < 2048 bits
```

#### Principio 6: SEGMENTACIÓN = DEFENSE IN DEPTH

No confíes en un perímetro. Usa microsegmentación.

```
Sin segmentación:
┌─────────────────────────────────┐
│ Firewall                        │
├─────────────────────────────────┤
│ INTERNET-FACING SERVERS         │  ← Comprometido
│ Internal APIs                   │  ← Attacker lo puede alcanzar
│ Database tier                   │  ← Attacker tiene acceso
│ Admin consoles                  │  ← Attacker es admin
└─────────────────────────────────┘

Con segmentación:
┌──────────────┐
│ INTERNET     │
└──┬───────────┘
   │ Firewall (DMZ)
   ├──────────────────────────────┐
   │ Internet-facing servers      │ ← Comprometido, pero...
   ├──────────────────────────────┤
         │ Firewall (internal)
         ├──────────────────────────────┐
         │ Internal APIs (own vlan)     │ ← Attacker NO puede alcanzar
         ├──────────────────────────────┤
               │ Firewall (database)
               ├──────────────────────────────┐
               │ Database tier (own vlan)     │ ← Attacker NO puede entrar
               ├──────────────────────────────┤
                     │ Firewall (admin)
                     ├──────────────────────────────┐
                     │ Admin consoles (MFA only)    │ ← Attacker NO llega aquí
                     └──────────────────────────────┘
```

---

## SECCIÓN 2: COMPONENTES TÉCNICOS (250-700 líneas)

### 1. Discovery & Reconnaissance

**Herramientas pasivas** (zero impacto):
```bash
# Whois + DNS
whois 10.1.0.0/16
dig +trace example.com
dig example.com ANY

# Public info
shodan ip:10.1.0.5  #¿Expuesto a internet?
censys.io          # Certificate interrogation
```

**Herramientas activas de bajo impacto**:
```bash
# Ping scan (identify live hosts)
nmap -sn 10.10.0.0/24

# Service enumeration (safe)
nmap -p 22,80,443,3306,5432 -sV 10.10.0.5
nmap --top-ports 100 10.10.0.5

# SSL/TLS verification
openssl s_client -connect 10.10.0.5:443
testssl.sh example.com
```

**Checklist**:
- [ ] Hosts identificados en scope
- [ ] Servicios documentados
- [ ] Versiones de servicios conocidas
- [ ] TLS status captured
- [ ] No servicios "surprise"

---

### 2. Port Analysis & Interpretation

```
Puerto 22 abierto (SSH):
├─ Expected? ¿Hay documentación?
├─ Public facing? En internet = critical
├─ Service owner? Quién lo mantiene?
├─ Version default? ssh_2.0 = podría ser vulnerable
└─ Alternatives? ¿Podría moverse a VPN only?

Puerto 3389 abierto (RDP):
├─ Expected? ¿Administración remota necesaria?
├─ Public? En internet = CRITICAL FINDING
├─ MFA enabled? ¿O contraseña nomás?
└─ Segmentation? ¿O accessible desde cualquier red?

Puerto 5900 abierto (VNC):
├─ Expected? Legacy admin tool?
├─ Encrypted? ¿O plaintext (muy malo)?
├─ Public? Si yes = CRITICAL
└─ Superseded? ¿Podría usar SSH en su lugar?
```

---

### 3. TLS/SSL Security Assessment

**CRITERIOS DE EVALUACIÓN**:

```
Certificado:
├─ [ ] Valid for domain? (www.example.com vs example.com)
├─ [ ] Not expired?
├─ [ ] Not self-signed (unless internal)?
├─ [ ] Chain of trust completa?
└─ [ ] SHA256, not SHA1?

Protocol:
├─ [ ] TLS 1.2 minimum (preferably 1.3)
├─ [ ] No SSL 3.0, TLS 1.0, TLS 1.1?
└─ [ ] SSLv2 disabled?

Ciphers:
├─ [ ] ECDHE (forward secrecy)?
├─ [ ] No RC4, 3DES, DES, MD5?
├─ [ ] AES-256 o ChaCha20?
├─ [ ] Diffie-Hellman >= 2048 bits?
└─ [ ] HSTS header present?
```

**Tools**:
```bash
openssl s_client -connect example.com:443
nmap --script ssl-enum-ciphers -p 443 example.com
sslscan example.com
testssl.sh example.com  # Most comprehensive
```

---

### 4. Firewall & Access Control Review

**Questions**:
- [ ] Firewall rules documented?
- [ ] Deny-all default, allow-explicit?
- [ ] Rules reviewed regularly (18+ months old = suspicious)?
- [ ] No overly broad rules (0.0.0.0/0)?
- [ ] Logging enabled?

**Antipatterns**:
```
❌ 0.0.0.0/0 → Any Service (allow ANYONE)
❌ 172.16.0.0/12 → 0.0.0.0/0 (allow entire internal → anywhere)
❌ corp-vpn → DB (allow VPN users → sensitive DB)

✅ 10.1.100.0/24 → 10.1.200.5:3306 (specific network → specific service)
✅ VPN-clients → 10.1.200.0/24:22 (admin access controlled)
✅ Internet → DMZ:80,443 only (defense in depth)
```

---

### 5. Network Segmentation

**Baseline checklist**:
```
[ ] DMZ exists (isolates internet-facing servers)?
[ ] Application vlan separate from database vlan?
[ ] Admin vlan isolated (MFA + no direct routes)?
[ ] IoT/Management plane segregated?
[ ] ACLs enforce segmentation (not just VLANs)?
[ ] Logs show if someone tries to break out?
```

---

### 6. Certificate Management

```bash
# Find all certificates in scope
find /etc/ssl /etc/pki -name "*.crt" -o -name "*.pem"

# Check expiry
openssl x509 -in cert.pem -text | grep -A 2 "Not After"

# Check validity
openssl verify -CAfile ca.pem cert.pem

# Inventory
for cert in /path/to/certs/*.pem; do
  echo "$cert: $(openssl x509 -in $cert -noout -subject) - Expires: $(openssl x509 -in $cert -noout -enddate | cut -d= -f2)"
done
```

---

## SECCIÓN 3: METODOLOGÍA (700-1100 líneas)

### Paso 1: Preparación & Documentación

```bash
# Recopila diagrama de red existente
ls -la /docs/*network* /docs/*diagram*
cat /docs/architecture.md

# Identifica rangos IP in-scope
grep -r "10\.|172\.16\.|192\.168\." /docs/

# Documenta expectativas
# services_expected.txt:
#   SSH: 10.1.100.0/24 admin access
#   HTTP: 10.1.200.5 web server
#   HTTPS: 10.1.200.5 web server
#   MySQL: 10.1.250.10:3306 database
#   Unexposed: 10.1.100.5:8080 testing
```

### Paso 2: Passive Intelligence

```bash
# DNS enumeration (no intrusive)
nslookup -type=A example.com
nslookup -type=MX example.com
dig @ns1.example.com example.com AXFR  # Zone transfer (if allowed)

# Whois
whois example.com
whois 1.2.3.4

# Historical data
https://shodan.io  # Search: "example.com" or "1.2.3.4"

# Certificate data
https://crt.sh ?q=example.com
```

### Paso 3: Network Scanning (Controlled)

```bash
# Step 3a: Host discovery
nmap -sn 10.10.0.0/24 -oG hosts.txt
# Parse live hosts
grep "Up" hosts.txt | awk '{print $2}' > live_hosts.txt

# Step 3b: Port enumeration
nmap --top-ports 100 -iL live_hosts.txt -sV -oA network_scan

# Step 3c: Service identification
nmap -p 22,80,443,3306,5432,8080,9200 -sV -Pn 10.10.0.0/24

# Step 3d: Timeouts & rate limiting
nmap --max-rtt-timeout 10000 -iL live_hosts.txt  # Slow, careful
```

### Paso 4: TLS Analysis (Every HTTPS Service)

```bash
# For each service on 443:
for host in $(cat https_hosts.txt); do
  echo "=== Testing $host ==="
  
  # Check certificate
  openssl s_client -connect $host:443 -servername $host < /dev/null
  
  # Check protocol support
  openssl s_client -connect $host:443 -tls1_2 < /dev/null
  openssl s_client -connect $host:443 -tls1_3 < /dev/null
  
  # Check ciphers
  nmap --script ssl-enum-ciphers -p 443 $host
done
```

### Paso 5: Service Verification

```bash
# Verify each open port maps to expected service

# Port 80 should be HTTP
curl -I http://10.1.200.5:80
# Expected: 200 OK, not 500 or timeout

# Port 443 should be HTTPS
curl -k -I https://10.1.200.5:443
# Expected: 200 OK

# Port 22 should be SSH (not telnet or other)
nmap -p 22 -sV 10.1.100.5
# Expected: OpenSSH x.x

# Unexpected ports
nmap -p 5555 10.1.0.0/24
# If anything responds: INVESTIGATE
```

### Paso 6: Segmentation Validation

```bash
# Test if segments are actually isolated

# From DMZ to Internal (should FAIL):
nmap -p 3306 10.1.200.5  # From 10.1.200.x → can't reach 10.1.250.x

# From Admin to Everything (should be ONE-WAY):
ssh admin@10.1.100.1      # OK
telnet 10.1.250.10 3306   # Should FAIL if segmented

# From Internet to Internal (should BLOCK):
nmap -p 22,25,53 10.1.0.0/24 from external IP
# Should all timeout
```

---

## SECCIÓN 4: CASOS DE ESTUDIO (1100-1500 líneas)

### Caso 1: Default SSH on Internet

**Contexto**: Startup's AWS instance. Dev deployed web server, forgot about SSH exposure.

**Discovery**:
```bash
nmap -p 22 instance-ip
# 22/tcp open ssh OpenSSH_7.4 (protocol 2.0)

# Check auth method
ssh -v admin@instance-ip 2>&1 | grep -i "password\|key"
# Can SSH with password (no key required)
```

**Attack Timeline**:
1. Attacker scans for open SSH
2. Tries common credentials (admin/admin, ubuntu/ubuntu)
3. Gets in, installs crypto-miner
4. AWS bill → $5,000/month

**Root Cause**: 
- Security group allowed 0.0.0.0/0:22
- Password auth enabled
- No 2FA

**Fix**:
```bash
# AWS Security Group:
Source: VPN CIDR only (e.g., 203.0.113.0/24)
Port: 22
Protocol: TCP

# Server-side SSH hardening:
echo "PasswordAuthentication no" >> /etc/ssh/sshd_config
echo "PublicKeyOnly yes" >> /etc/ssh/sshd_config
grep -v "^#" /etc/ssh/sshd_config | grep -v "^$"  # Verify
service ssh restart
```

**Impact**: Millions of instances compromised this way. AWS reports >40% of compromised instances via SSH.

---

### Caso 2: Weak TLS Certificate

**Contexto**: Enterprise with internal certificate authority. Certificate expires frequently, people ignore warnings.

**Discovery**:
```bash
openssl s_client -connect api-internal.example.com:443
# Certificate:
#     Subject: CN = api.example.com
#     Issuer: CN = Internal CA (self-signed)
#     Not After: Jan 1 2024 (TODAY IS JAN 15)
#     ⚠️ EXPIRED

# Browser shows "Certificate not trusted" warning
# Users click "Continue anyway"

# Weakness: TLS 1.0 allowed!
nmap --script ssl-enum-ciphers -p 443 api-internal.example.com
# TLS v1.0 supported: true
# Cipher: DES-CBC3-SHA (weak 3DES!)
```

**Impact**: 
- Man-in-the-middle attacks possible over internal network
- Credential harvesting if attacker on same VLAN
- Compliance violation (HIPAA, PCI-DSS require TLS 1.2+)

**Fix**:
```bash
# Generate new certificate with longer validity
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out cert.pem

# Force TLS 1.2+ in nginx.conf
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;

# Check compliance
curl -I --tlsv1.2 https://api-internal.example.com
# Should work

curl -I --tlsv1.0 https://api-internal.example.com
# Should FAIL
```

---

### Caso 3: Lateral Movement via Unsegmented Network

**Contexto**: Company with flat network. Compromised web server = full database access.

**Attack Chain**:
```
1. Attacker compromises web server (10.1.200.5)
   - RCE via vulnerable PHP

2. Attacker gets shell:
   $ whoami
   root

3. Attacker scans internal network from web server:
   $ nmap -p 3306 10.1.0.0/24
   Found database: 10.1.250.10:3306

4. No firewall between web & database:
   $ mysql -h 10.1.250.10 -uroot -ppassword
   > SELECT * FROM users;
   > 100K user accounts dumped

5. Attacker pivots to admin network:
   $ nmap -p 22 10.1.100.0/24
   Found admin jump host: 10.1.100.1

6. Can SSH to admin? Maybe, if same SSH key used:
   $ ssh admin@10.1.100.1
   ✓ Connected (no VPN required!)

7. Now attacker is in admin vlan:
   $ kubectl get secrets
   $ aws sts get-caller-identity --assume-role admin
```

**Impact**: All data + infrastructure compromised

**Fix - Segmentation**:
```
DMZ (web servers):
Inbound: 0.0.0.0/0:80,443 (internet)
Outbound: 10.1.250.10:3306 ONLY (database)
         10.1.100.1:22 ONLY (logging)

Internal (database):
Inbound: 10.1.200.0/24:3306 ONLY (web layer)
Outbound: 10.1.100.1:514 ONLY (logs)

Admin (jump hosts):
Inbound: VPN clients only:22
Outbound: * (full access for ops)
```

---

## SECCIÓN 5: TEMPLATES Y CHECKLISTS (1500-1700+ líneas)

### Template 1: Network Security Audit Checklist

```markdown
# NETWORK SECURITY AUDIT

**Scope**: [10.0.0.0/8, DMZ, etc.]
**Timeline**: [Start-End]
**Baseline**: [Reference architecture, expected services]

---

## Discovery & Reconnaissance

### Passive Reconnaissance
- [ ] DNS records documented
- [ ] Public IPs identified (whois, shodan)
- [ ] Certificate transparency logs reviewed
- [ ] Historical data from crt.sh collected

### Active Scanning (Controlled)
- [ ] Host discovery complete (ping sweep)
- [ ] Service enumeration done (nmap -sV)
- [ ] Live host list: _____ hosts
- [ ] Unexpected services: _____ (list)

### Expected vs Actual
- [ ] Services match documentation? YES/NO
- [ ] Unexpected services identified: _____
- [ ] Owner of each service confirmed

---

## Port & Service Analysis

| Port | Service | Expected | Found | Issue |
|------|---------|----------|-------|-------|
| 22 | SSH | YES | YES | Password auth enabled |
| 80 | HTTP | YES | YES | No redirect to HTTPS |
| 443 | HTTPS | YES | YES | TLS 1.0 allowed |
| 3306 | MySQL | Internal only | Public | CRITICAL |
| 5900 | VNC | Internal | On DMZ | CRITICAL |

---

## TLS/SSL Security

- [ ] Certificates valid for domains?
- [ ] Not expired?
- [ ] Chain of trust complete?
- [ ] TLS 1.2 minimum? TLS 1.3 preferred?
- [ ] Ciphers strong (no DES, RC4, MD5)?
- [ ] HSTS header present?
- [ ] Certificate renewal process documented?

---

## Firewall & Segmentation

- [ ] Firewall rules documented?
- [ ] Rules reviewed in last 12 months?
- [ ] Default-deny policy?
- [ ] No overly broad rules (0.0.0.0/0)?
- [ ] DMZ isolated from internal?
- [ ] Database vlan restricted?
- [ ] Admin vlan access controlled?

---

## Findings Summary

**CRITICAL** (Fix immediately):
- [ ] Exposed admin services (RDP, SSH, WinRM on internet)
- [ ] Expired certificates
- [ ] Weak TLS protocols (< 1.2)
- [ ] No firewall between network segments

**HIGH** (Fix within 2 weeks):
- [ ] Default credentials enabled
- [ ] No MFA on sensitive services
- [ ] Weak ciphers allowed
- [ ] Overly broad firewall rules

**MEDIUM** (Plan remediation):
- [ ] Legacy protocols active
- [ ] Self-signed certs (if not internal)
- [ ] No HSTS headers
- [ ] Manual key rotation (should be automated)

---

## Remediation Roadmap

| Item | Priority | Effort | Timeline |
|------|----------|--------|----------|
| Block SSH from internet | CRITICAL | 30 min | Today |
| Update TLS to 1.2+ | CRITICAL | 2 hours | This week |
| Add segmentation rules | CRITICAL | 4 hours | This week |
| Renew certificates | HIGH | 1 hour each | Next month |
| Enable MFA for admin | HIGH | 4 hours | Next month |

---

## Re-validation Checklist

After remediation:
- [ ] Retest exposed services (should be blocked)
- [ ] TLS scan (should show 1.2+)
- [ ] Segmentation test (lateral movement blocked)
- [ ] Certificate validity checked
- [ ] All rules working as documented
```

---

**TOTAL: 1,700+ líneas**
**Status**: Production ready
**Última actualización**: 2024-02-15


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - 04: Network Security - Descubrimiento de Superficie & Segmentación

### Integraciones ampliadas

- Nmap: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Masscan: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Zeek: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Wazuh: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: segmentacion debil.
- Integracion recomendada: Nmap.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: firewall heredado.
- Integracion recomendada: Masscan.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: servicio expuesto.
- Integracion recomendada: Zeek.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: segmentacion debil.
- Integracion recomendada: Wazuh.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: firewall heredado.
- Integracion recomendada: Nmap.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: servicio expuesto.
- Integracion recomendada: Masscan.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: segmentacion debil.
- Integracion recomendada: Zeek.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: firewall heredado.
- Integracion recomendada: Wazuh.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: servicio expuesto.
- Integracion recomendada: Nmap.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: segmentacion debil.
- Integracion recomendada: Masscan.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: firewall heredado.
- Integracion recomendada: Zeek.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: servicio expuesto.
- Integracion recomendada: Wazuh.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: segmentacion debil.
- Integracion recomendada: Nmap.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: firewall heredado.
- Integracion recomendada: Masscan.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: servicio expuesto.
- Integracion recomendada: Zeek.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: segmentacion debil.
- Integracion recomendada: Wazuh.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: firewall heredado.
- Integracion recomendada: Nmap.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: servicio expuesto.
- Integracion recomendada: Masscan.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: segmentacion debil.
- Integracion recomendada: Zeek.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: firewall heredado.
- Integracion recomendada: Wazuh.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: servicio expuesto.
- Integracion recomendada: Nmap.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: segmentacion debil.
- Integracion recomendada: Masscan.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: firewall heredado.
- Integracion recomendada: Zeek.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: servicio expuesto.
- Integracion recomendada: Wazuh.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 25
- Contexto: segmentacion debil.
- Integracion recomendada: Nmap.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 26
- Contexto: firewall heredado.
- Integracion recomendada: Masscan.
- Senal principal: cifrado debil.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 27
- Contexto: servicio expuesto.
- Integracion recomendada: Zeek.
- Senal principal: baseline roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 28
- Contexto: segmentacion debil.
- Integracion recomendada: Wazuh.
- Senal principal: admin remota.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

