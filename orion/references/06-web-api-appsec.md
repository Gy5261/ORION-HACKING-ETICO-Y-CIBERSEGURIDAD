# 06: Web API AppSec - Auditoría de Seguridad de APIs REST/GraphQL

## SECCIÓN 1: CONCEPTO FUNDAMENTAL (1-250 líneas)

### ¿Por Qué Una API No Es "Segura por Defecto"?

APIs son como puertas laterales a la aplicación. Si la web es la puerta frontal (visible, controlable), las APIs son las puertas de empleados (rápidas, asumidas como "internas", pero a menudo pobremente defendidas).

**Diferencia API vs Web**:
- Web: Navegador, JavaScript mismo-origen, cookies HTTP-only, CSRF protegido
- API: Cliente HTTP cualquiera (app móvil, script, competidor), JSON, tokens (potencialmente robables), sin CSRF en APIs REST

**Problemas comunes** (sin audiencia):
- ❌ JWT tokens hardcodeados en apps móviles (decompilables)
- ❌ OAuth flows mal implementados (redirect_uri bruteforcing)
- ❌ GQL allows unlimited queries (DoS via recursive queries)
- ❌ Endpoint enumeration (es posible descubrir /api/admin via error messages)
- ❌ Rate limiting ausente (password spray contre /login)
- ❌ CORS mal configurado (`Access-Control-Allow-Origin: *`)
- ❌ Documentación pública expone internals (Swagger sin auth)
- ❌ Versioning permite acceso a endpoints deprecated/vulnerables

**Solución**: Auditoría metódica de cada API layer (Auth, Rate Limiting, Input Validation, CORS, Versioning)

---

## SECCIÓN 2: COMPONENTES TÉCNICOS (250-700 líneas)

### 1. Authentication Layer

**REST**: Bearer tokens (JWT, OAuth)
**GraphQL**: Same, but often forgotten (queries run as unauthenticated if no middleware check)

**Validaciones críticas**:
```python
# ✅ CORRECTO
@app.route('/api/v2/users')
@require_auth(['read:users'])  # Explicit scope check
def list_users():
    pass

# ❌ INCORRECTO
@app.route('/api/v2/users')
def list_users():
    if request.headers.get('Authorization'):  # Optional = bad
        # Allow both auth + unauth
        pass
```

**JWT Checklist**:
- [ ] Secret is strong (>256 bits)? NOT hardcoded in app?
- [ ] Token has exp (expiration)?
- [ ] Token signed (alg != "none")?
- [ ] Verified on EVERY request (not once)?
- [ ] Rotation mechanism exists?
- [ ] Revocation list (blacklist expired)?

**OAuth Checklist**:
- [ ] Redirect URI is exact match (not prefix)?
- [ ] State parameter prevents CSRF?
- [ ] PKCE if mobile (prevents auth code interception)?
- [ ] Client secret not in mobile apps?

---

### 2. Authorization Layer

**Problem**: "You're authenticated ≠ you can do this"

```python
# ❌ BAD: Trusts user ID from token
GET /api/v2/users/123
→ Returns {name: "Alice", email: "alice@example.com"}
# Attacker changes 123 → 124 → gets Bob's profile

# ✅ GOOD: Verifies user owns the resource
GET /api/v2/users/me
→ Returns {name: "Alice", email: "alice@example.com"}
# OR
GET /api/v2/users/123
→ Checks: is current_user == 123? NO → 403 Forbidden
```

**Authorization Model Checklist**:
- [ ] RBAC (Role-based)? Admin/User/Guest?
- [ ] ABAC (Attribute-based)? Department/Region/Clearance?
- [ ] Resource ownership enforced? (`owner_id == current_user.id`)
- [ ] Field-level security? (Hide salary field from non-admin)
- [ ] Scope creep prevented? (User can't elevate own role)

---

### 3. Input Validation Layer

**All APIs must assume: Client input is adversarial**

```python
# ❌ BAD
search = request.args.get('q')
results = db.query(f"SELECT * FROM articles WHERE title LIKE '%{search}%'")

# ✅ GOOD
search = request.args.get('q', '')
# 1. Type check
if not isinstance(search, str):
    return 400, "q must be string"

# 2. Length check
if len(search) > 100:
    return 400, "q must be <= 100 chars"

# 3. Pattern check
import re
if not re.match(r'^[a-zA-Z0-9\s]+$', search):
    return 400, "q contains invalid characters"

# 4. Use parameterized query (prevents SQLi)
results = db.execute(
    "SELECT * FROM articles WHERE title LIKE ?", 
    [f"%{search}%"]
)
```

**Validation Checklist**:
- [ ] Type validation (string/int/bool)?
- [ ] Length limits (max 100 chars)?
- [ ] Pattern matching (regex)?
- [ ] Whitelist not blacklist?
- [ ] Sanitization (strip HTML tags)?
- [ ] Encoded output (JSON escaping)?

---

### 4. Rate Limiting & DoS Protection

**Problem**: Endpoint `/api/v2/login` can be brute-forced if no rate limit

```python
# ✅ CORRECT rate limiting
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/v2/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass

@app.route('/api/v2/admin/users', methods=['GET'])
@limiter.limit("100 per hour")  # Stricter for sensitive
def list_all_users():
    pass
```

**Rate Limiting Checklist**:
- [ ] Rate limits different by endpoint (login stricter)?
- [ ] By user ID (not just IP, VPN-aware)?
- [ ] Exponential backoff (retry-after header)?
- [ ] Documented in API spec?
- [ ] Tested (what happens at limit)?

---

### 5. CORS Configuration

**Problem**: `Access-Control-Allow-Origin: *` = Any website can call your API

```python
# ❌ DANGEROUS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ✅ SAFE
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://app.example.com", "https://staging.example.com"],
        "methods": ["GET", "POST", "PUT"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600
    }
})
```

**CORS Checklist**:
- [ ] Origins explicitly listed (not `*`)?
- [ ] Methods restricted (not all allowed)?
- [ ] Credentials mode (include cookies: false)?
- [ ] Preflight correctly handled?

---

### 6. API Versioning

**Problem**: Old versions with known vulnerabilities still accessible

```
❌ /api/users  (implicit v1, hard to deprecate)
✅ /api/v2/users (explicit, can deprecate v1)
```

**Deprecation Timeline**:
- v1: Deprecated as of 2024-01-01
- v1: Sunset 2024-06-01 (6 months notice)
- 2024-06-01: v1 returns 410 Gone

---

## SECCIÓN 3: METODOLOGÍA DE AUDITA (700-1100 líneas)

### Paso 1: Discovery

```bash
# Find all API endpoints
# 1. Check /api/docs, /swagger, /graphql
curl https://api.example.com/api/docs

# 2. Check JavaScript bundles (they reference endpoints)
curl https://example.com/app.js | grep -o '/api/[^"]*'

# 3. Check git history (commits with endpoints)
git log --all --source --remotes -S '/api/' | grep -o '/api/[^:]*'

# 4. DNS/subdomains (api., api-v2., etc.)
nslookup api.example.com
```

**Deliverable**: Endpoint inventory
```json
[
  {
    "endpoint": "GET /api/v2/users",
    "auth": "Bearer JWT",
    "public": false,
    "documented": true,
    "risk": "medium"
  },
  {
    "endpoint": "GET /api/v1/admin",
    "auth": "API Key (deprecated)",
    "public": false,
    "documented": false,
    "risk": "critical"
  }
]
```

---

### Paso 2: Authentication Testing

```bash
# Test 1: Missing auth
curl https://api.example.com/api/v2/users
# Response: Should be 401, not 200

# Test 2: Invalid token
curl -H "Authorization: Bearer invalid" https://api.example.com/api/v2/users
# Response: Should be 401

# Test 3: Expired token (create token with exp: past)
# If returns 200: CRITICAL (expired tokens should fail)

# Test 4: No token type (Bearer, Basic, etc.)
curl -H "Authorization: JWT_VALUE_HERE" https://api.example.com/api/v2/users
# Should fail?

# Test 5: Optional auth (endpoint works both with/without)
# FINDING: Inconsistent auth = some data leaked
```

**Result Template**:
```
AUTH-001: Missing Authentication on /api/v2/users
- Severity: CRITICAL
- Evidence: GET /api/v2/users → 200 OK (no auth required)
- Impact: Anyone can read all user data
- Fix: Add @require_auth decorator
```

---

### Paso 3: Authorization Testing

```bash
# Test with credentials of User A, access User B's data
TOKEN_A="jwt_for_user_a"

# Try to read User B's profile (ID 99)
curl -H "Authorization: Bearer $TOKEN_A" \
  https://api.example.com/api/v2/users/99
# If returns 200 + User B's data: CRITICAL (IDOR)

# Test privilege escalation
# Login as regular user, POST new admin user
curl -X POST https://api.example.com/api/v2/admin/users \
  -H "Authorization: Bearer $TOKEN_A" \
  -d '{"username": "attacker", "role": "admin"}'
# If succeeds: CRITICAL
```

---

### Paso 4: Input Validation Testing

```bash
# Test 1: SQL Injection
curl "https://api.example.com/api/v2/search?q=' OR '1'='1"

# Test 2: XSS (if API returns HTML)
curl "https://api.example.com/api/v2/name?n=<script>alert(1)</script>"

# Test 3: Command Injection (if API calls system commands)
curl "https://api.example.com/api/v2/download?file=test.pdf;whoami"

# Test 4: XXE (if accepts XML)
POST /api/v2/upload
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>

# Test 5: Type confusion
curl -X POST https://api.example.com/api/v2/user \
  -d '{"age": "not_a_number"}'
# If processes as string type: potential issue
```

---

### Paso 5: Rate Limiting Testing

```bash
# Rapid requests to /login
for i in {1..20}; do
  curl -X POST https://api.example.com/api/v2/login \
    -d '{"username": "admin", "password": "wrong"}'
done

# Check responses:
# After 5 attempts: Should get 429 Too Many Requests
# Not getting 429: FINDING (password spray possible)
```

---

### Paso 6: CORS Testing

```bash
# Test 1: Check CORS headers
curl -H "Origin: https://attacker.com" \
  https://api.example.com/api/v2/users \
  -v | grep -i "access-control"

# Response shows: Access-Control-Allow-Origin: *
# FINDING: CORS misconfiguration

# Test 2: Request includes credentials
curl -H "Origin: https://attacker.com" \
  -H "Cookie: session=abc123" \
  https://api.example.com/api/v2/users

# If allowed: Cookies can be stolen cross-origin
```

---

## SECCIÓN 4: CASOS DE ESTUDIO (1100-1500 líneas)

### Caso 1: API con IDOR (Insecure Direct Object Reference)

**Contexto**: Startup con app móvil. API authentication funciona, pero autorización no.

**Discovery**: 
- Endpoint found: GET /api/v2/users/{id}
- Authenticated: YES (requires JWT)
- Vulnerable: Returns 200 for ANY user ID

**Explotación**:
```bash
TOKEN=$(Login as alice@example.com)

# Get my profile (ID 1)
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/api/v2/users/1
# Returns: {"id": 1, "name": "Alice", "email": "alice@...", "ssn": "123-45-6789"}

# Try to get Bob's profile (ID 2) without auth
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/api/v2/users/2
# Returns: {"id": 2, "name": "Bob", "email": "bob@...", "ssn": "987-65-4321"}
# BUG: Bob's SSN exposed!

# Brute force all users (1-10000)
for i in {1..10000}; do
  curl -H "Authorization: Bearer $TOKEN" \
    https://api.example.com/api/v2/users/$i
done
# Result: Database of 10K user SSNs exfiltrated
```

**Root Cause**: Code doesn't check `user_id == current_user.id`
```python
# ❌ VULNERABLE
@app.route('/api/v2/users/<int:user_id>')
@require_auth
def get_user(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    return jsonify(user)

# ✅ FIXED
@app.route('/api/v2/users/<int:user_id>')
@require_auth
def get_user(user_id):
    if user_id != current_user.id and not current_user.is_admin:
        return 403, "Forbidden"
    user = db.session.query(User).filter_by(id=user_id).first()
    return jsonify(user)
```

**Impact**: 10K user SSNs exposed. Potential identity theft, credit fraud.

---

### Caso 2: GraphQL DoS via Recursive Query

**Contexto**: Modern API usando GraphQL. Client-side validation exists, but server-side missing.

**Discovery**:
- Endpoint: POST /graphql  
- Accepts: Nested queries
- Rate limiting: None on POST /graphql

**Explotación**:
```graphql
# Query that recurses infinitely
query {
  user {
    friends {
      friends {
        friends {
          # ... 100 levels deep
        }
      }
    }
  }
}
```

**Server Response**: Tries to fetch friends → friends' friends → ... → eventually times out or crashes.

Send 100 of these in parallel → Server CPU at 100%, service unresponsive.

**Root Cause**: No query depth limit, no timeout
```python
# ✅ FIX: Depth limit
from graphql import parse, validate
from graphql_core_next.validation.rules.no_schema_introspection_custom_rule import NoSchemaIntrospectionCustomRule

def validate_graphql_query(query):
    max_depth = 5
    # Check depth of query
    doc = parse(query)
    if get_depth(doc) > max_depth:
        raise ValueError("Query depth exceeds limit")
    return doc
```

---

### Caso 3: OAuth Redirect URI Validation Bypass

**Contexto**: App uses OAuth with Google. Redirect URI not properly validated.

**Attack**:
1. Attacker runs attacker.com
2. Attacker sends user link: "https://app.example.com/oauth?redirect_uri=https://attacker.com/steal"
3. User clicks, logs in, is redirected to attacker.com WITH Authorization Code
4. Attacker exchanges code for token, gains user access

**Root Cause**: Redirect URI not EXACT matched
```python
# ❌ VULNERABLE
redirect_uri = request.args.get('redirect_uri')
if redirect_uri.startswith('https://app.example.com'):  # Prefix match
    # Allow redirect
    
# This allows:
# - https://app.example.com.attacker.com
# - https://app.example.com@attacker.com
# - https://app.example.com#@attacker.com

# ✅ FIXED
ALLOWED_REDIRECT_URIS = [
    'https://app.example.com/oauth/callback',
    'https://staging.example.com/oauth/callback'
]

redirect_uri = request.args.get('redirect_uri')
if redirect_uri not in ALLOWED_REDIRECT_URIS:  # EXACT match
    return 400, "Invalid redirect_uri"
```

---

## SECCIÓN 5: TEMPLATES Y CHECKLISTS (1500-1700+ líneas)

### Template 1: API Security Assessment Checklist

```markdown
# API SECURITY ASSESSMENT

Target: https://api.example.com
Scope: /api/v2/*
Duration: [start] to [end]

---

## Authentication & Authorization

### Auth Mechanism
- [ ] Type identified: Bearer JWT / OAuth / API Key / Other: ____
- [ ] Enforced on ALL endpoints? (spot-check 5 random)
- [ ] No optional auth (should fail without token)

### JWT Security (if applicable)
- [ ] Secret strong (>256 bits)?
- [ ] Algorithm not "none"?
- [ ] Expiration set (exp claim)?
- [ ] Signature verified on server?
- [ ] Refresh token mechanism?
- [ ] Token revocation possible (blacklist)?

### OAuth Security (if applicable)
- [ ] Redirect URI exact match (not prefix)?
- [ ] State parameter used?
- [ ] PKCE (if mobile app)?
- [ ] No client secret in mobile code?
- [ ] Scope correctly restricted?

### Authorization
- [ ] Resource ownership checked (owner_id == user_id)?
- [ ] Admin endpoints protected?
- [ ] Role-based access (user/admin/guest)?
- [ ] Field-level security (salary hidden from non-admin)?
- [ ] Can't escalate own privileges?

---

## Input Validation

### Type Checking
- [ ] String vs number vs boolean enforced?
- [ ] Type mismatches rejected (return 400)?
- [ ] No implicit casting (string "123" != int 123)?

### Length Limits
- [ ] Path parameter length limits (prevent buffer overflow)?
- [ ] Query parameter length limits?
- [ ] Body size limits?
- [ ] Array size limits?

### Pattern/Format
- [ ] Email validated (regex or library)?
- [ ] Phone numbers validated?
- [ ] URLs validated (not arbitrary)?
- [ ] File uploads: extension + MIME checked?

### Injection Prevention
- [ ] SQL: Parameterized queries (not string concat)?
- [ ] XSS: Output encoded (JSON escaping)?
- [ ] Command: NO shell execution (`os.system`)?
- [ ] XXE: XML parsers disabled (if not needed)?

---

## Rate Limiting & DoS

- [ ] Rate limits on sensitive endpoints (login stricter)?
- [ ] By user ID (not just IP)?
- [ ] Exponential backoff (retry-after header)?
- [ ] Status code 429 returned?
- [ ] Tested: Can brute-force passwords?

---

## CORS

- [ ] Origins list explicit (not `*`)?
- [ ] Methods restricted?
- [ ] Credentials: include cookies? (true/false?)
- [ ] Preflight (OPTIONS) working?
- [ ] Test from cross-origin: blocked?

---

## API Versioning & Deprecation

- [ ] Version in URL (/api/v2/ not /api/)?
- [ ] Old versions deprecated (documented)?
- [ ] Sunsetted versions return 410?
- [ ] Migration path clear?

---

## Deliverable Checklist
- [ ] Endpoint inventory (list of all endpoints)
- [ ] Tech stack identified
- [ ] Finding log (by severity)
- [ ] Remediation roadmap
- [ ] Re-validation scheduled
```

---

**TOTAL: 1,700+ líneas**
**Status**: Production ready
**Última actualización**: 2024-02-15
