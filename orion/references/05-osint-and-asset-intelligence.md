# OSINT and Asset Intelligence - External Surface Mapping & Threat Intelligence

## SECCIÓN 1: CONCEPTO FUNDAMENTAL

### ¿Por qué existe OSINT?

OSINT (Open Source Intelligence) es el descubrimiento y agregación de información disponible públicamente para construir un mapa confiable de la **superficie de ataque** de una organización sin ejecutar acciones intrusivas. La mayoría de brechas comienzan explotando activos que el cliente no sabía que tenía expuestos.

**Objetivo crítico**: Crear un inventario verificado de activos externos, dominios, certificados, DNS, disposiciones de tecnología y exposiciones involuntarias ANTES de hacer preguntas que alertan a la infraestructura.

### 5 Principios Fundamentales de OSINT

1. **Empezar por fuentes propias del cliente (si existen)**
   - Sitios web públicos, reportes anuales, dominios registrados
   - Información del cliente que ya conocen ≠ sorpresas
   - Valida la estrategia de branding y alcance declarado
   - *Ejemplo*: "¿Cuántos dominios tiene registrados tu empresa?" → `whois` bulk search

2. **No confundir "aparece en internet" con "es del alcance"**
   - Un dominio puede ser de un vendor, partner, acquisition anterior o activo abandonado
   - OSINT descubre, pero **ownership verification es obligatorio**
   - Ejemplo: `old.example.com` en Wayback Machine ≠ activo vivo; requiere confirmación
   - **HARD RULE**: "¿Sigue siendo de tu organización?" antes de informar

3. **Cruzar datos de múltiples fuentes antes de afirmarlos como hechos**
   - Un certificado se ve en crt.sh PERO ¿existe DNS resolviendo?
   - Un repositorio de GitHub apareció en búsqueda PERO ¿está actualizado o abandonado?
   - Correlación > Coincidencia: 3+ fuentes independientes = alta confianza
   - *Patrón*: Certificado → DNS → Reverse DNS → Shodan/Censys → Wayback → GitHub patterns

4. **Distinguir histórico de activo vivo (timing crítico)**
   - Certificados vencidos ≠ servicio activo; BUT pueden indicar infraestructura dormida
   - Dominios registrados en 2015 pero nunca resolvieron ≠ activos olvidados
   - WHOIS: fecha de creación ≠ fecha de actualización reciente
   - **Acción**: Verificar timestamp más reciente en cada fuente

5. **Automatizar descubrimiento pero validar manualmente la confianza**
   - Herramientas encuentran dominios y certificados rápidamente (Amass, Shodan, Nuclei)
   - Contexto = humano: "¿Qué es esto? ¿Realmente lo conozemos?"
   - Ejemplo: 500 subdominios descubiertos → 50 verificados → 5 críticos por revisar

### Filosofía OSINT

**"Información pública es información, pero contexto es conocimiento"**

Tu trabajo es transformar datos dispersos en una **imagen coherente de la superficie expuesta**, verificada por alguien que conoce la organización, lista para que los equipos técnicos prioricen qué mirar primero.

---

## SECCIÓN 2: COMPONENTES TÉCNICOS Y METODOLOGÍA

### Componente 1: Reconocimiento Pasivo de Dominios

**Objetivo**: Descubrir todos los dominios, subdominios y marcas registradas sin hacer requests activos.

**Información técnica**:
- WHOIS: Registrante, fecha de renovación, nameservers autorizados
- DNS público: `nslookup`, `dig`, `host` contra servidores públicos (8.8.8.8, 1.1.1.1)
- Certificados SSL: crt.sh, certificate transparency logs, Censys
- Repositorios públicos: GitHub, GitLab, Bitbucket patterns (`site:github.com "example.com"`)

**Checklist - Dominios & Certificados**:
- ✅ Obtener lista COMPLETA de dominios registrados del cliente (WHOIS bulk + registrars)
- ✅ Cruzar con Certificados (crt.sh, Censys, Rapid7 OpenData)
- ✅ Verificar que certificados reflejan dominios actuales (check expiry date, domains listed)
- ✅ Revisar WHOIS histórico (ICANN archives) para activos viejos
- ✅ Buscar dominios parqueados, redirecciones, o migraciones incompletas
- ✅ Nota: Dominios en certificado ≠ servicios activos (must verify next)

**Herramientas recomendadas**:
```bash
# WHOIS bulk
whois -h whois.verisign-grs.com example.com | grep -E "Registrar:|Expir|Updated"

# DNS resolución contra múltiples servidores
for ns in 8.8.8.8 1.1.1.1 208.67.222.222; do
  echo "=== $ns ==="
  nslookup example.com $ns | grep -E "^Name:|Address"
done

# Certificados (usando jq para JSON parsing)
curl -s "https://crt.sh/?q=example.com&output=json" | \
  jq -r '.[] | "\(.name_value)"' | sort -u | grep -E "^(\*\.)?example"

# GitHub patterns (no ejecutar directamente, review manual)
# site:github.com "example.com" "production" OR "deploy" OR "api_key"
# (MANUAL ONLY - no automatizar sin revisión)
```

**Errores comunes**:
- ❌ Afirmar "activo" solo porque DNS resuelve (podría ser legacy redirect)
- ❌ Ignorar dominios históricos (adquisiciones, marcas antiguas)
- ❌ Mezclar WHOIS privado con registrante real (resellers oculten owner)
- ❌ No revisar nuevos dominios agregados recientemente (M&A signals)

**Evidencia típica**:
```markdown
## Dominio Legacy Descubierto
- **Dominio**: legacy.example.com (registrado 2010, renovado 2024)
- **Certificado**: Sí, válido, CN=legacy.example.com (30 dominios totales en cert)
- **DNS Resuelto**: Sí, A-record → 203.0.113.100 (IP antigua, ¿aún monitorizada?)
- **WHOIS Owner**: Same registrant como example.com
- **Status**: ¿Activ or abandoned? (requires client confirmation)
- **Riesgo**: Si abandonado pero resolviendo → puede atraer scanners, malware C2
```

---

### Componente 2: Búsqueda de Tecnología y Marcos de Exposición

**Objetivo**: Identificar qué tecnologías está usando, cuál es la arquitectura visible, y dónde hay cambios recientes.

**Información técnica**:
- HTTP headers: Server, X-Powered-By, X-AspNet-Version, X-Frame-Options, CSP
- Métodos HTTP disponibles: OPTIONS request muestra qué métodos soporta el servidor
- Versiones de software: Algunos servicios exponen versiones en banners (Apache, nginx, IIS)
- Tecnología stack: Frameworks detectables (React, Vue, Angular fingerprints), CMS (WordPress, Joomla)
- Infraestructura: CDN (Cloudflare, Akamai), WAF signals, Load balancer behavior
- Cambios recientes: Certificado nuevo = cambio reciente; DNS cambios = migración en progreso

**Checklist - Tecnología & Arquitectura**:
- ✅ Mapear HTTP headers de todos los servicios (head request contra cada dominio/puerto)
- ✅ Catalogar versiones detectables (pero asumir información incompleta)
- ✅ Identificar WAF/CDN (buscar footprints: Cloudflare, Akamai, ModSecurity signatures)
- ✅ Buscar tecnología stack (framework fingerprinting: React, Django, ASP.NET indicators)
- ✅ Revisar cambios de certificado (emisión reciente = cambios de infraestructura)
- ✅ Identificar DNS changes (NS cambios indican migración o consolidación)
- ✅ Correlacionar con Stack Overflow, GitHub commits, job postings (hints sobre tech)

**Herramientas recomendadas**:
```bash
# HTTP headers (todos)
curl -I -H "User-Agent: Mozilla/5.0" https://app.example.com/ | head -20

# WebGen (fingerprinting - alternativa: Wappalyzer online)
curl -s https://app.example.com | grep -iE "generator|powered|X-Powered|framework"

# Certificate info (Subject Alternative Name, Issuer, dates)
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|^.*Alternate|issuer|not After"

# DNS records (MX, TXT, SPF, DKIM, DMARC)
dig example.com MX +short
dig default._domainkey.example.com TXT +short  # DKIM
dig dmarc._report._dmarc.example.com TXT +short
dig example.com TXT +short | grep -i "v=spf"

# Check nameserver provider (hints infrastructure)
dig +trace example.com | tail -5 | grep "example.com"
```

**Errores comunes**:
- ❌ Confundir versión expuesta en header con vulnerabilidad confirmada (no = explotable aquí)
- ❌ Asumir tecnología basada en 1 fingerprint (correlaciona)
- ❌ No revisar cambios DNS/certificado históricos (Wayback Machine, DNS history tools)

**Evidencia típica**:
```markdown
## Cambio Reciente de Infraestructura Detectado
- **Dominio**: app.example.com
- **Certificado Anterior**: Let's Encrypt (emitido Ene 2024, CN=app.example.com)
- **Certificado Nuevo**: DigiCert (emitido Dic 2024, CN=app.example.com + api.example.com, cdn.example.com)
- **Interpretación**: Migración reciente a nueva infraestructura en diciembre
- **Nueva DNS**: Apunta a Cloudflare NS (fue nginx antes)
- **Riesgo**: Configuración incompleta en nueva infraestructura es tipo 1 bug → revisar permisos, WAF
```

---

### Componente 3: Búsqueda de Exposición de Información Sensible

**Objetivo**: Descubrir accidentes comunes: fugas de credenciales, endpoints de admin, información de debug, etc.

**Información técnica**:
- Archivos públicos accidentales: robots.txt, sitemap.xml, .git/, backups
- Metadatos en archivos: PDFs con propietario, EXIF en imágenes
- Parámetros de debug expuestos: ?debug=1, ?stack=true, verbose logging
- Archives públicos: Wayback Machine, archivo.org, GitHub (code + commit messages)
- Leaks reportados: haveibeenpwned.com, breachdb, GitHub: `"example.com" password` OR `api_key`
- Subdominios staging/testing: staging.example.com, test.example.com, dev-api.example.com (a menudo menos protegidos)

**Checklist - Exposición de Información Sensible**:
- ✅ Revisar robots.txt y sitemap.xml (qué archivos el cliente NO quiere indexados)
- ✅ Buscar archivos comunes: .git/, .env, web.config, backup.sql, debug=true
- ✅ Revisar metadatos de documentos públicos (PDFs, Word docs → propietario, software, autor)
- ✅ Buscar endpoints de admin/debug (actualizaciones de software dejan patrones)
- ✅ Revisar Wayback Machine para cambios históricos (credenciales viejas, APIs no documentadas)
- ✅ GitHub code search: `"example.com"` en comments, deprecated code, hardcoded IPs
- ✅ Buscar en Pastebin, Gist, GitHub gists (leaks de config or logs)
- ✅ Check haveibeenpwned.com, Breach Compilation DBs (empleados, dominios, emails)

**Herramientas recomendadas**:
```bash
# Archivos comunes
for path in robots.txt sitemap.xml .git/ .env web.config backup.sql .DS_Store; do
  curl -s -o /dev/null -w "$path: %{http_code}\n" https://example.com/$path
done

# Búsqueda en Wayback (API)
curl -s "https://archive.org/wayback/available?url=example.com&output=json" | \
  jq '.archived_snapshots | keys | sort | tail -10[]' | \
  while read snapshot; do
    echo "https://web.archive.org/web/$snapshot/https://example.com/"
  done

# GitHub API search (required: token, manual review)
# curl -H "Authorization: token YOUR_TOKEN" \
#  "https://api.github.com/search/code?q=example.com+password+in:file" (NEVER AUTOMATE)

# Metadatos de PDF/doc
exiftool -a https://example.com/document.pdf | grep -E "Creator|Producer|Author"

# SSL Certificate Transparency logs (crt.sh API)
curl -s "https://crt.sh/?q=example.com&output=json" | \
  jq -r '.[] | .issuer_name + " / " + .name_value' | sort -u
```

**Errors comunes**:
- ❌ Automatizar búsquedas en Pastebin/GitHub sin revisión manual (falsos positivos)
- ❌ Reportar "credenciales de prueba` sin verificar si aún están activos
- ❌ No distinguir entre credenciales de 2018 (rotadas) vs 2024 (potencialmente válidas)

**Evidencia típica**:
```markdown
## API Key Staging Descubierta en GitHub gist público
- **Ubicación**: https://gist.githubusercontent.com/user/XXXXX/raw
- **Contenido**: "api_key: sk_live_4eC39HqLyjWDarhtT..." (truncated for security)
- **Timestamp**: Publicado hace 3 años, no actualizado desde
- **Status**: Verificación: ¿Sigue siendo válido? (POST a staging endpoint)
- **Impacto**: Si válido, acceso a testing infrastructure; ≤ media si staging separado
- **Recomendación**: (1) DELETE gist, (2) ROTATE key, (3) Audit logs para uso
```

---

### Componente 4: Reconocimiento de Infraestructura y Redes

**Objetivo**: Mapear la topología de red visible: servidores, servicios, IPs, rangos de red públicos.

**Información técnica**:
- Resolución DNS: Registros A, AAAA, CNAME, MX, TXT (SPF, DKIM, DMARC)
- IP ranges públicos: WHOIS de IPs → ASN → rango CIDR completo
- Reverse DNS: IP → hostname conversions (hints servernames, patterns)
- Shodan/Censys/Greynoise: Índices de servicios expuestos, versiones, configuraciones
- BGP announcements: Para qué rangos anuncia la organización públicamente

**Checklist - Infraestructura**:
- ✅ Resolver DNS de todos los dominios principales + wildcards (A, AAAA, CNAME, MX)
- ✅ Mapear  authoritative nameservers (implica provedor de registración)
- ✅ SPF/DKIM/DMARC policy review (email spoofing, domain hijacking, phishing risks)
- ✅ WHOIS lookup de IPs públicas (identificar ASN, propietario, rango CIDR)
- ✅ Reverse DNS de rangos públicos (hint de servernames, patterns)
- ✅ BGP announcement monitoring (qué anúncia públicamente)
- ✅ Shodan/Censys queries de rangos (servicios, puertos, banners)
- ✅ Verificar DNSSEC configuration (si está habilitado, que sea correcto)

**Herramientas recomendadas**:
```bash
# DNS full record enumeration
dig example.com +nocmd +noall +answer A MX NS TXT AAAA

# SPF/DKIM/DMARC policies
dig default._domainkey.example.com TXT +short
dig dmarc._report._dmarc.example.com TXT +short
dig example.com TXT +short | grep v=spf

# IP WHOIS + ASN
whois 203.0.113.1 | grep -E "^ASN:|^NetRange:|^Organization"

# Reverse DNS (bulk)
for ip in 203.0.113.{1..255}; do
  nslookup $ip 8.8.8.8 | grep "name =" | awk '{print $NF}'
done 2>/dev/null | sort -u

# Censys API (requires account) - example only
# curl -u "API_ID:API_SECRET" \
#   "https://censys.io/api/v2/hosts/search?q=203.0.113.0/24" | jq '.hosts[] | .ip + ": " + (.services[0].service_name)'

# DNSSEC validation
dig example.com +dnssec | grep -i "ad\|RRSIG"
```

**Errores comunes**:
- ❌ No revisar registros MX antiguos (pueden heredar infraestructura vieja)
- ❌ Asumir rango CIDR es completamente del cliente (algunos pueden ser terceros)
- ❌ No verificar DNSSEC (si habilitado mal = DNS spoofing posible)

**Evidencia típica**:
```markdown
## Rango de IP Público Mapeado
- **CIDR**: 203.0.113.0/24 (252 IPs usables)
- **ASN**: AS12345 (Example Corp Inc)
- **Reverse DNS Pattern**: prod-web-{1,2,3}.example.com, prod-db-{1,2,3}.example.com, staging-{...}
- **Servicios Visibles** (Shodan):
  - 203.0.113.10: Apache 2.4.41, port 80,443 (web servers)
  - 203.0.113.50: PostgreSQL 12.x, port 5432 (NO credentials needed! Open!)
  - 203.0.113.100: Kubernetes API, port 6443
- **Riesgo**: DB expuesto sin autenticación; K8s API sin acceso restringido
- **Acción**: (1) Verificar si esto es intencional, (2) Scan interno vs production
```

---

### Componente 5: Correlación y Análisis de Cadenas de Ataque

**Objetivo**: Conectar los datos descubiertos para identificar cadenas de ataque potenciales.

**Information técnica**:
- Conexiones DNS-Certificado-IP: ¿Todos apuntan al mismo lugar firewalled?
- Histórico de cambios: Certificado nuevo + DNS nuevo + IP nuevo = migración (= posible misconfiguration)
- Tecnología + Servicios: Wordpress + versión vieja + plugin conocido vulnerable = PoC existe
- Exposición + Servicio: Certificado expone nombres internos + reverse DNS confirma = attacker já conoce architecture

**Checklist - Correlación**:
- ✅ Crear tabla: Dominio → Certificado → IP → Reverse DNS → Servicios descubiertos
- ✅ Marcar inconsistencias: "Este dominio cree que es X pero resuelve a la infraestructura Y"
- ✅ Identificar tecnología stack de cambios recientes: "¿Por qué cambiaron certificado en Dec pero DNS aún viejo?"
- ✅ Mapear cadenas de ataque potenciales: "Si X es vulnerable (publicado), Y es expuesto, Z es red accessible"
- ✅ Cruzar información histórica: Wayback + certificado histórico + WHOIS histór

ico

**Herramientas / Patrones**:
```bash
# Correlación de mapeo (manual spreadsheet es mejor, pero aquí está script helper)
# Crea tabla: domain | cert_names | ip | reverse_dns | tecnologia | riesgo

# Para cada dominio:
# 1. DNS A record
# 2. Certificado (crt.sh)
# 3. Reverse DNS del IP
# 4. Servicios (Shodan)
# 5. Histórico (Wayback, DNS history)
# 6. Tecnología (headers, fingerprints)
# 7. Correlaciona inconsistencias

# Script template (pseudocode):
for domain in $(cat domains.txt); do
  echo "=== $domain ==="
  ip=$(nslookup $domain 8.8.8.8 | grep "^Address" | tail -1 | awk '{print $NF}')
  reverse=$(nslookup $ip | grep "name =" | awk '{print $NF}')
  cert=$(curl -s "https://crt.sh/?q=$domain&output=json" | jq -r '.[-1].name_value')
  headers=$(curl -sI https://$domain | head -5)
  
  echo "IP: $ip"
  echo "Reverse: $reverse"
  echo "Cert names: $cert"
  echo "Headers: $headers"
  echo ""
done
```

**Errores comunes**:
- ❌ Data silos: Dominio, cert, IP, servicio no correlacionados (no ves patrones)
- ❌ Asumir que todos los servidores en rango son "producción" (algunos son test/staging)
- ❌ No revisar cambios históricos (cadena de ataque necesita entender qué cambió y cuándo)

**Evidencia típica**:
```markdown
## Correlación: Migración de Infraestructura Detectada
**Timeline**:
- Ene 2024: app.example.com → 203.0.113.10 (on-prem, nginx)
- Jul 2024: Certificado nuevo incluye "app-aks.example.com" (hint: Azure)
- Dic 2024: DNS actualizado → Cloudflare NS, IP → Azure data center (20.x.y.z)

**Cadena de Ataque Potencial**:
1. Descubredor público: Los certificados viejos siguen en CT logs (Ene cert visible)
2. Attacker escanea 203.0.113.10: Encuentra nginx viejo abandonado (no actualizado!)
3. Exploit: CVE-2024-1234 en nginx 1.10 conocido, acceso root
4. **Resultado**: Acceso a servidor legacy aún accesible desde internet

**Recomendación**: (1) Verificar 203.0.113.10 aún es parte de scope, (2) Si legacy, apagar o firewllar, (3) Si activo, patchear nginx
```

---

## SECCIÓN 3: METODOLOGÍA OSINT Paso-a-Paso

### Paso 1: Preparación y Scope Verification (30-60 min)

**Qué hacer**:
1. Obtener documentación del cliente: lista oficial de dominios, rangos de IP, proveedores
2. Crear tabla/spreadsheet: Column headers = Dominio, Fuente, Confianza, Status, Notas
3. Verificar scope legal: "¿Podemos revisar asimismo toda la infraestructura de AWS? ¿Solo dominios públicos?"
4. Identificar marca matrix: ¿Cuántas marcas/empresas tiene (adquisiciones, subsidiarias)?

**Comandos**:
```bash
# Plantilla spreadsheet
cat > osint_inventory.csv << EOF
Domino,Tipo,Confianza,Fuente,Status,Cliente_Confirmado,Notas
example.com,dominio-principal,alta,cliente,activo,sí,primary user-facing
api.example.com,subdominio,alta,certificado,activo,?,production api
legacy.example.com,dominio-viejo,media,certificado,?,no,deprecated 2018?
EOF

# Verificar registrador de dominios
whois example.com | grep -i "registrar"
```

**Deliverable**: Tabla inicial de dominios de cliente (verificado por client)

### Paso 2: Búsqueda Pasiva de Dominios y Certificados (1-2 horas)

**Qué hacer**:
1. Certificados (crt.sh): Todos los commonName + subjectAltNames de todos los certificados emitidos
2. WHOIS: Búsqueda bulk de dominios registrados en nombre del cliente
3. Reverso DNS: Qué dominios apuntan a los IPs públicos conocidos
4. GitHub/repos: Búsqueda manual (NO automatizada) de references del cliente

**Comandos**:
```bash
# Récuperer certificados
curl -s "https://crt.sh/?q=example.com&output=json" | jq -r '.[] | .name_value' | \
  tr ',' '\n' | grep -v '^$' | sort -u > certs.txt

# WHOIS dominio (y bulk si da)
whois example.com | grep -E "Domain Name:|Registrar|Registrant|Admin|Tech|Created|Updated|Expires"

# Búsqueda REVERSA DNS (manual, para dominios conocidos)
nslookup 203.0.113.1

# GitHub (MANUAL - NO SCRIPT)
# Ir a: https://github.com/search?q="example.com"
# Revisar: código, commits, PRs, gists
```

**Deliverable**: domains.txt, certs.txt, correlación initial de certificados → dominios

### Paso 3: Búsqueda de Servicios y Tecnología (1-2 horas)

**Qué hacer**:
1. HTTP headers de todos los dominios
2.OpenSSL certificate info (subject, alternative names, issuer, dates)
3. DNS records completos (A, AAAA, MX, TXT, CNAME, NS)
4. Clasificar servicios por tipo (web, mail, DNS, staging, dev)

**Comandos**:
```bash
# HTTP headers batch
while read domain; do
  echo "=== $domain ==="
  curl -sI -L "https://$domain/" 2>/dev/null | head -15
done < domains.txt > http_headers.txt

# OpenSSL certificado info
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|DNS:|CN=|Alternative" > cert_details.txt

# DNS full enumeration
dig example.com @8.8.8.8 +nocmd +noall +answer ANY

# SPF/DKIM/DMARC
dig example.com TXT @8.8.8.8 +short | grep spf
dig default._domainkey.example.com TXT @8.8.8.8 +short
dig _dmarc.example.com TXT @8.8.8.8 +short
```

**Deliverable**: http_headers.txt, cert_details.txt, dns_enumeration.txt, technology_matrix.csv

### Paso 4: Búsqueda de Exposición de Información y Cambios Históricos (2-3 horas)

**Qué hacer**:
1. Robots.txt, sitemap.xml, common files (.git, .env, backup.sql, web.config)
2. Wayback Machine: Historia de dominios (cambios, endpoints viejos)
3. Metadatos de documentos públicos (PDFs disponibles en web)
4. Búsqueda de leaks: haveibeenpwned, breachdb (emails del dominio)

**Comandos**:
```bash
# Archivos comunes (safe - no exploitation)
for file in robots.txt sitemap.xml .git/config .env web.config backup.sql backup.zip; do
  echo "Checking /$file on example.com..."
  curl -sI "https://example.com/$file" | head -1
done

# Wayback Machine
curl -s "https://archive.org/wayback/available?url=example.com/*&output=json" | \
  jq -r '.archived_snapshots.closest | .timestamp + " " + .status' | tail -10

# Metadatos PDF (ejemplo)
exiftool -a your_document.pdf | grep -E "Creator|Producer|Author|Title"

# Búsqueda de emails del dominio en leaks (VERIFICACIÓN MANUAL)
# Ir a: https://haveibeenpwned.com/ y buscar @example.com emails
# NO AUTOMATIZAR ESTO
```

**Deliverable**: exposed_files.txt, wayback_history.txt, metadata_findings.txt, breach_db_summary.txt

### Paso 5: Correlación y Análisis de Tabla Maestra (1-2 horas)

**Qué hacer**:
1. Crear tabla master: Dominio → Certificado → IP → Reverse DNS → Servicios → Tecnología → Riesgos
2. Identificar inconsistencias (qué cosa no cuadra)
3. Análisis de timeline: Cuándo cambiaron certificatos, DNS, IPs (migraciones)
4. Identificar cadenas de ataque (qué explotación depende de qué descubrimiento)

**Formato tabla**:
```markdown
| Dominio | Certificado | IP | Reverse DNS | Servicios | Tecnología | Riesgo | Status |
|---------|-------------|-----|------------|-----------|------------|--------|--------|
| app.example.com | SAN: app,api,staging | 203.0.113.10 | prod-web-1.example.com | Apache 2.4 | React + Node | OLD APACHE VER | Activo |
| legacy.example.com | Legacy cert (2018) | 203.0.113.11 | legacy.example.com | Nginx 1.10 | PHP 5.6 (EOLQ) | DEPRECATED? | ? |
| staging-api.example.com | SAN: staging* | 10.0.1.50 (PRIVADO?) | staging-api.internal | Spring Boot | Java REST | INTERNAL LEAKED | Activo |
```

**Análisis de inconsistencia**:
- ¿Por qué staging está en certificado público (crt.sh) si es "interno"?
- ¿Por qué legado.example.com aún está resolviendo si fue descontinuado?
- ¿Certificado nuevo en Jul pero DNS no cambió hasta Dic? (ventana de 5 meses = dos infraestructuras activas)

**Deliverable**: master_correlation_table.csv, inconsistencies_list.md, attack_chains.md

### Paso 6: Reporteo y Verificación con Cliente (1-2 horas)

**Qué hacer**:
1. Crear documento de hallazgos: "Aquí están todas las superfícies públicas que encontramos"
2. Verificar con cliente: "¿Esto es correcto? ¿Este dominio sigue siendo activo?"
3. Clasificar por confianza: Alta (certificado oficial) vs Media (DNS histórico) vs Baja (corazonada)
4. Marcar qué está within scope para pruebas (explicit client approval)

**Plantilla reporte**:
```markdown
# OSINT & Asset Intelligence Report

## Executive Summary
Identificamos N dominios públicos, M certificados activos, K IPs públicas en uso.
X % confirmados por cliente como activos y in-scope.

## Dominios Activos (confirmado cliente)
- app.example.com (producción API)
- www.example.com (sitio web)
- mail.example.com (correo)

## Dominios Cuestionables (verificación pendiente)
- legacy.example.com (¿activo o deprecated?)
- staging.example.com (¿todavía en uso?)

## Certificados con Dominios Críticos
| Certificado | Dominios Listados | Valido Hasta | Riesgo |
|-------------|------------------|--------------|--------|
| Let's Encrypt #12345 | app, api, www | 2025-06-23 | Expira en 6 meses |

## IPs Públicas Mapeadas
- 203.0.113.0/24: Rango principal (252 IPs)
- Servicios detectados: Web (80,443), API (8080), etc.

## Recomendaciones Siguientes
1. (Cliente) Confirmar activos que están dudosos
2. (Técnico) Escanear puerto completo de rangos confirmados
3. (Técnico) Testear servicios por vulnerabilidades comunes
4. (Técnico) Revisar cambios de configuración recientes
```

**Deliverable**: OSINT_Report.md, verified_assets.csv, scope_confirmation.txt

---

## SECCIÓN 4: CASOS DE ESTUDIO REALES

### Caso 1: Descubrimiento de Subdominio Legacy con Acceso Abierto (Severidad Alta)

**Contexto**:
Empresa de retail con 50 tiendas. Realizó migración de infraestructura en 2021, pero algunos servicios "legacy" quedaron en servidores viejos.

**Descubrimiento OSINT**:
1. Certificados públicos (crt.sh) mostraban: store-admin.example.com, pos-backup.example.com, legacy-db.example.com
2. Cliente confirmó: "Eso was for old POS system, we decommissiond it en 2020"
3. DNS lookup: legacy-db.example.com aún resolvía a 203.0.113.50
4. HTTP request: Acceso abierto a panel de admin (sin credentials)
5. Contenido: Backup de bases de datos de clientes (nombres, emails, compras)

**Análisis de Cadena de Ataque**:
- Paso 1 (Attacker OSINT): Certificate transparency logs → descubre legacy-db.example.com
- Paso 2: DNS resolution → 203.0.113.50 aún activo
- Paso 3: HTTP scan → sin autenticación requerida
- Paso 4: Exfiltración: Acceso a 50M registros de clientes
- **Impacto**: Breach + GDPR fine + lawsuits aún en 2024

**Qué fallió**:
- Certificado no revocado (aún válido, se renovó automáticamente)
- DNS no limpiado
- Servidor nunca fue apagado, solo "olvidado"
- No hay monitoreo de dominios descontinuados

**Cómo se hubiera prevenido**:
- Lista oficial de dominios "deprecated" con fecha de decomisioning
- Certificados revocados + DNS eliminados en decommissioning
- Monitoreo continuo: "¿Qué nuevos dominios aparecieron en CT logs?" (alerta si legacy resurge)
- Escaneo periódico de dominios viejos (Wayback + DNS)

**Descubrimiento en assessment**:
```bash
# Encontramos esto en 30 minutos con OSINT
curl -s "https://crt.sh/?q=example.com&output=json" | jq -r '.[] | .name_value' | \
  tr ',' '\n' | grep -i "legacy\|old\|deprecated\|backup\|archive"
# → legacy-db.example.com, old-admin.example.com, archive-shop.example.com

# Verificación dentro 5 minutos
for domain in legacy-db old-admin archive-shop; do
  curl -sI "https://${domain}.example.com/" | head -1
done
# → Si resuelve sin 404, es un problema
```

---

### Caso 2: Información Sensible en PDF Metadatos (Severidad Media)

**Contexto**:
Consultora de seguridad publica whitepapers sobre "our clients" (sin nombrarlos) en PDF.

**Descubrimiento OSINT**:
1. Búsqueda: Documento "Company X Security Assessment Report 2024"
2. PDF descargado de site público
3. Metadatos EXIF: Creator = "John Smith, Security Analyst, Consultant Company"
4. Datetime: Created 2024-03-15, Modified por 5 diferentes personas
5. **Leakage**: Evidencia de internals, procesos, herramientas usadas

**Información leakeada de metadatos**:
```bash
exiftool Assessment_Report_2024.pdf | grep -E "Creator|Producer|Author|Create|Modify"
# Creator: "John Smith"
# Producer: "Microsoft Word 16.0"  ← Windows + Office version
# Create Date: 2024:03:15 14:32:18  ← Exact time of report generation
# Modify Date: 2024:03:16 by "Review Team Lead"  ← Nombre visible sin sanitizar
```

**Cadena de Ataque**:
- Paso 1: Descubrir PDF público en búsqueda
- Paso 2: Extraer metadatos → John Smith es analista
- Paso 3: LinkedIn buscar "John Smith security analyst" → found, conectar
- Paso 4: Phishing dirigido es más creíble porque sabes el nombre, empresa, trabajo

**Qué fallóq**:
- Reportes NO fueron sanitizados antes de publicación
- Metadatos no fueron removidos
- Procesos internos/herramientas detalléados en documento

**Prevención**:
- Sanitizar reportes: Remover nombres, fechas exactas, versiones de software, personas
- Antes de publicar, extraer metadatos: `exiftool -all= document.pdf`
- Usar herramienta de sanitización: `mat2` o similar

**Descubrimiento OSINT equivalent**:
```bash
# Búsqueda de PDFs públicos
curl -s "https://www.example.com/downloads/whitepaper.pdf" -o /tmp/wp.pdf

# Extrae metadatos
exiftool /tmp/wp.pdf | grep -E "Creator|Producer|Author|Title"

# Si hay metadatos personales, es riesgo (phishing target, social engineering)
```

---

### Caso 3: Certificado Expuesto Nombres Internos + DNS Leak = Architecture Reversal (Severidad Alta)

**Contexto**:
Startup de SaaS con arquitectura multi-tenant. Certificado wildcard emitido para *.internal.example.com

**Descubrimiento OSINT**:
1. Certificados (crt.sh): *.internal.example.com, db1.internal, db2.internal, cache.internal, queue.internal
2. DNS públicamente visible: internal.example.com resuelve (no debería!)
3. Attacker ya conoce toda la arquitectura interna sin acceder
4. Paso siguiente: Scan de puertos en 10.0.0.0/8 buscando esos servidores
5. Encontrado: db1.internal en 10.0.1.100 (SSRF via la app web, escalate a DB)

**Análisis**:
```
Certificado público revela:
- db1.internal, db2.internal (hay redundancia/clustering)
- cache.internal (Redis/Memcached, likely has secrets)
- queue.internal (job queue, message broker)
- api-internal.example.com (internal API)

Attacker ahora sabe:
- Arquitectura de 6+ servidores
- Nombres de máquinas
- Servicios en uso (DB, cache, queue)
- Networking segregation (X.internal = podría ser 10.0.0.0/8 or 172.16.0.0/12)

Sin certificado leak, habría necesitado:
- SSRF vulnerability (lento para descubrimiento)
- Compromiso previo de servidor (no posible sin acceso)
- Configuración incorrecta de buckets S3/etc
```

**Cómo se explotó**:
1. Attacker finds app.example.com
2. OSINT: Certificate shows internal.example.com servernames
3. Educated guess: Try SSRF on web server → http://db1.internal:5432
4. Database responds (no firewall interno)
5. Exploit: SSRF + SQLi = acceso a base de datos

**Prevención**:
- Nunca emitir certificados wildcard *.internal
- Si los necesitas, usar infra interna (private CA, no CT logs)
- O usar nombres genéricos: *.service1.example.com vs *.db.internal.example.com
- Monitoreo: "¿Qué nuevos dominios .internal aparecen en CT logs?" → alerta automática

**Discovery equivalente OSINT**:
```bash
# Búsqueda en crt.sh por ".internal"
curl -s "https://crt.sh/?q=%.internal&output=json" | jq -r '.[] | .name_value' | tr ',' '\n' | sort -u
# Encuentra: db1.internal, db2.internal, cache.internal, api-internal.example.com

# Intenta resolver
for domain in db1.internal db2.internal cache.internal; do
  nslookup ${domain}.example.com 8.8.8.8  # Likely fails
done

# Pero el certificado es evidencia de que existen
# → Attacker ahora busca SSRF para acceder
```

---

## SECCIÓN 5: TEMPLATES, CHECKLISTS Y HERRAMIENTAS

### Template 1: OSINT Asset Inventory Spreadsheet

```csv
Tipo_Activo,Nombre,Fuente_Descubrimiento,IP_Resuelve,Ultima_Verificacion,Owner_Confirmado,Estado_Produccion,Riesgo_Identificado,Notas_Verificacion
Dominio,app.example.com,WHOIS+Client,203.0.113.10,2024-12-20,SI,Sí,Ninguno,Primary API endpoint
Dominio,legacy.example.com,Certificate_CT,?,2024-12-20,NO,No,INVESTIGAR,Certificado aún emitido; DNS no resuelve; ¿decommissioned or forgotten?
Subdominio,staging-api.example.com,Certificate_CT,10.0.1.50,2024-12-20,SI,No,EXPOSICION,Staging apareció en certificado público (should be private)
Subdominio,internal.example.com,Certificate_CT,?,2024-12-20,SI,No,ARQUITECTURA_LEAK,Certificate names exponen db1, db2, cache; internal servers no deberían estar visibles
IP_Range,203.0.113.0/24,WHOIS,SÍ,2024-12-20,SI,Sí,REVISAR,Production servers; 252 IPs publicas, algunos posiblemente legacy
Certificado,Let's Encrypt #45678,crt.sh,SÍ,2024-12-20,SÍ,Sí,OK,Válido hasta 2025-06-30; covers app + www + api subdomains
Certificado,DigiCert (Old),crt.sh,NO,2024-12-20,UNKNOWN,No,LEGACY,Emitido 2018, expiró 2022; por qué aún visible en CT logs?
```

### Template 2: Reporte OSINT Ejecutivo

```markdown
# OSINT & Asset Intelligence Assessment

## Executive Summary
**Período**: 20 Dic 2024  
**Dominio Objetivo**: example.com  
**Activos Descubiertos**: 15 dominios, 8 certificados, 1 rango IP público (203.0.113.0/24)  
**Riesgo Identificado**: 3 activos legacy potencialmente expuestos, 1 leak de arquitectura interna

---

## Inventory Rápido
- **Total Dominios Confirmados Activos**: 7
- **Dominios Questionables (need verification)**: 3
- **Certificados Activos**: 8 (2 expirados pero visible en logs)
- **IP Ranges Públicos**: 203.0.113.0/24 (gestión correcta)

---

## Hallazgos Críticos

### Hallazgo 1: Legacyominio Aún Resolviendo (Severidad: ALTA)
```
Dominio: legacy-db.example.com
Certificado: Sí, Let's Encrypt, válido
DNS: Resuelve a 203.0.113.50
HTTP: Accessible sin credentials (confirmed via curl)
Contenido: Admin panel para sistema POS (descontinuado 2020 según cliente)
Riesgo: Acceso descontrolado a datos históricos
Recomendación Inmediata: (1) Apagar servidor, (2) Revocar certificado, (3) Remover DNS
Temporal (si no puedes apagar): Firewall entrada a 203.0.113.50 desde internet
```

### Hallazgo 2: Certificado Expone Nombres Internos (Severidad: MEDIA)
```
Certificado: *.internal.example.com (CT logs visible)
Dominos expuestos: db1.internal, cache.internal, api-internal
Implicación: Attacker conoce arquitectura sin acceso técnico
Riesgo: SSRF + credenciales = acceso a infrastructure crítica
Recomendación: Revocar certificado; usar private CA para *.internal
Temporal: Monitoreo por intentos SSRF en server de application
```

### Hallazgo 3: Staging Dominio en Certificado Público (Severidad: BAJA-MEDIA)
```
Dominio: staging-api.example.com
Ubicación: IP privada 10.0.1.50 (no debería ser resolvible desde internet)
Problema: Nombre revela que es staging (menos protegido)
Riesgo: Ataques dirigidos a staging (credenciales de test, features no guardadas)
Recomendación: Remover staging de certificados públicos; usar cert privado o IP direkt
```

---

## Recomendación de Próximos Pasos
1. **Inmediato** (24 hrs): Apagar legacy-db.example.com o firewall desde internet
2. **Corto Plazo** (1-2 semanas): Limpiar certificados; revocar dominios legacy/internal
3. **Mediano Plazo** (1-2 meses): Introducir monitoreo de Certificate Transparency (alertas automáticas)
4. **Largo Plazo**: Plan de decommissioning formal (cuando servicios se deprecan, actualizar DNS + certs + docmentation)
```

### Template 3: OSINT Execution Checklist

```markdown
# OSINT Execution Checklist

## Pre-Engagement
- [ ] Scope de OSINT documentado y aprobado por cliente
- [ ] Limitaciones legales claras (qué fuentes sí/no puedo usar)
- [ ] Tabla de dominios iniciales del cliente (para cross-check)
- [ ] Acceso a herramientas: dig, curl, jq, exiftool (o instalador)

## Fase 1: Descubrimiento Pasivo de Dominios (Target: 1-2 hrs)
- [ ] crt.sh: Certificado CT search completo
- [ ] WHOIS: Búsqueda de dominios registrados (bulk si disponible)
- [ ] GitHub (manual): Búsqueda de referencias del cliente code/docs/gists
- [ ] Documentar: dominos.txt, certs.txt, github_findings.txt

## Fase 2: Servicios & Tecnología (Target: 1-2 hrs)
- [ ] HTTP headers de todos dominos (curl -I)
- [ ] OpenSSL certificate details (Subject, SAN, Issuer, dates)
- [] DNS resolución completa (A, AAAA, MX, TXT, CNAME, NS)
- [ ] SPF/DKIM/DMARC records (email security)
- [ ] Documentar: http_headers.txt, cert_details.txt, dns_records.txt

## Fase 3: Búsqueda de Exposición (Target: 2-3 hrs)
- [ ] Archivos comunes: robots.txt, sitemap.xml, .git, .env, web.config
- [ ] Wayback Machine: Historia de dominios (cambios, endpoints viejos)
- [ ] Metadatos documento público (PDFs, Word docs)
- [ ] Búsqueda de emails en leaks (haveibeenpwned, breachdb) - MANUAL
- [ ] GitHub code search (credenciales, API keys, secrets) - MANUAL ONLY
- [ ] Documentar: exposed_files.txt, wayback_history.txt, leaked_credentials.txt

## Fase 4: Infraestructura & Networking (Target: 1-2 hrs)
- [ ] WHOIS IP lookups (ASN, owner, CIDR range)
- [ ] Reverse DNS de rangos públicos
- [ ] Shodan/Censys queries (servicios, versiones) - REVIEW MANUAL
- [ ] BGP announcement check (si aplica)
- [ ] Documentar: ip_ranges.txt, reverse_dns.txt, services_censys.txt

## Fase 5: Correlación & Análisis (Target: 1-2 hrs)
- [ ] Crear tabla master: Dominio → Cert → IP → Reverse DNS → Tech → Risks
- [ ] Identificar inconsistencias: qué cosa no cuadra?
- [ ] Análisis de timeline: cuándo cambiaron cosas?
- [ ] Mapear cadenas de ataque potenciales
- [ ] Documentar: master_table.csv, inconsistencies.md, attack_chains.md

## Fase 6: Verificación con Cliente (Target: 1-2 hrs)
- [ ] Presentar hallazgos al cliente
- [ ] Verificar: "¿Esto es correcto? ¿Este domino está in-scope?"
- [ ] Reclasificar por confianza (Alta/Media/Baja)
- [ ] Obtener aprobación explícita para next fases de testing
- [ ] Documentar: verification_notes.txt, scope_confirmation.txt

## Post-Engagement
- [ ] Sanitizer reportes (remover PII de nombres, fechas exactas, etc)
- [ ] Resumen ejecutivo para leadership
- [ ] Documentar lecciones aprendidas
```

### Template 4: Indicadores de Compromiso (IoC) - OSINT Phase

```markdown
# OSINT Discovery Red Flags

## 🚩 Indicators Que Requieren Acción Inmediata

[ **Dominio/Certificado Legacy Aún Públicamente Resolvible**
- Discovery: Certificado expira en 2018 PERO aún en CT logs + DNS resuelve
- Action: Verificar si está decommissioned; si sí, revocar + remover DNS
- Example: legacy-db.example.com → 203.0.113.50 (abandoned server?)

[ **Arquitectura Interna Expuesta en Certificado Público**
- Discovery: *.internal, *.db, *.cache, *.admin nombres en certificado público
- Action: Revocar certificado; usar private CA para nombres internos
- Example: db1.internal.example.com en crt.sh públicamente visible

[ **Cambio de Infraestructura Detectado (Cert + DNS + IP)**
- Discovery: Certificado emitido mes X, DNS cambió mes Y, IP nuevo mes Z
- Action: Verificar si migración fue correcta; legacy servidor aún accesible?
- Example: Enero cert → Julio cert nuevo → Diciembre DNS actualizado (gap = ambos vivos?)

[ **Contenido de Dos Infraestructuras Activas Simultáneamente**
- Discovery: Dominio apunta a antiguo servidor (203.0.113.10) Y nuevo (Azure IP)
- Action: Confirmar si ambos están en uso; si viejo es legacy, apagarlo
- Example: app.example.com → "nginx 1.10" (viejo) + "Azure App Service" (nuevo)

[ **Credenciale o Secrets en Repositorio Público**
- Discovery: "api_key=sk_live_...", "password=...", "connection_string=..." en GitHub
- Action: Asumir comprometido; rotar key/password INMEDIATAMENTE
- Example: .env o config.js committed con secrets hardcodeados

[ **Dominios Staging/Testing Resolvibles Públicamente**
- Discovery: staging.example.com, test-api.example.com, dev.example.com resolvibles
- Action: Remover del público; usar .local o IP privada; verificar credenciales de test
- Example: TODO: staging-api.example.com sin autenticación

[ **PDF o Documento Público con Metadatos Personales**
- Discovery: Whitepaper PDF tiene Creator="John Smith", Modified="Review Team", etc
- Action: Remover documento; sanitizar metadatos; republish
- Example: whitepaper.pdf → exiftool revela nombres + fechas + versiones software

[ **Certificado Expirado Pero Aún Resolvible**
- Discovery: DNS aún apunta a dirección; certificado vencido 2022 pero aún en CT logs
- Action: Asumir legacy/forgotten; DNS limpiar; servidor apagar o rekeywrap
- Example: old-api.example.com: cert expired Dec 2022, DNS aún resuelve (Feb 2024)
```

### Herramientas Recomendadas (Con Advertencias)

```bash
# Safe, Passive Reconnaissance
curl, nslookup, dig, whois, openssl, exiftool
jq, grep, awk, sort, uniq
nmap (port scan only - VERIFY as in-scope with client first)

# Usadas pero requieren API token + verificación manual
Shodan (shodan.io - requires API key)
Censys (censys.io - requires API key)
VirusTotal (virustotal.com - requires API key)

# Requieren verificación manual (NO AUTOMATIZAR)
GitHub search (site:github.com "example.com")
Wayback Machine (archive.org - manual review)
haveibeenpwned.com (manual email search)
Pastebin/Gist (manual review only)

# NEVER AUTOMATIZAR (Legal/Ethical Risk)
SQL injection tests en OSINT phase
Credential spraying
Malware analysis tools
Exploit execution
Password cracking

# Alternativas Open Source (recomendadas)
Amass (subdomain enumeration)
Nmap (port discovery, versioning)
Pifdns (DNS enumeration)
Recon-ng (OSINT framework)

# Plantilla de script OSINT seguro
#!/bin/bash
# OSINT_safe.sh - Passive reconnaissance only

DOMAIN=$1

echo "=== OSINT Report for $DOMAIN ==="
echo ""
echo "1. Certificados (CT logs):"
curl -s "https://crt.sh/?q=$DOMAIN&output=json" | jq -r '.[] | .name_value' | sort -u
echo ""
echo "2. DNS Records:"
dig $DOMAIN ANY @8.8.8.8
echo ""
echo "3. HTTP Headers:"
curl -sI "https://$DOMAIN/" | head -10
echo ""
echo "4. Archivo común (robots.txt):"
curl -s "https://$DOMAIN/robots.txt" | head -5
echo ""
echo "=== FIN REPORT ==="

# Uso: bash OSINT_safe.sh example.com
# Salida: Solo information pasiva, sin ataques
```

---

## SECCIÓN FINAL: FAQ Y CONCLUSIÓN

### Preguntas Frecuentes

**P: ¿Es legal usar crt.sh y Shodan para OSINT?**
R: Sí, son fuentes públicas. BUT verificar scope del engagement. Si el cliente NO quiere que revises terceros, respeta eso.

**P: ¿Debo escanear ports completos en OSINT phase?**
R: No. OSINT = información pasiva. Port scanning es fase siguiente (ya será más activo). En OSINT solo resolvemos DNS + certificados.

**P: ¿Qué hace si encuentro credenciales en GitHub?**
R: (1) Asumir comprometido, (2) DETENER búsqueda (no copies/uses), (3) Reporta al cliente INMEDIATAMENTE, (4) Recomenda rotación.

**P: ¿Puedo usar información de Wayback Machine?**
R: Sí, es contexto histórico. Pero no afirmes "servicio vulnerable" basado solo en archive old. Verifica que aún es así actualmente.

**P: ¿Cuánto tiempo debe tomar la fase OSINT?**
R: 1-2 días para organización pequeña (5-10 dominios), 3-5 días para grande (50+ dominios). Máximo esfuerzo es correlación + verificación.

**P: ¿Cómo evito falsos positivos?**
R: Regla simple: 2+ fuentes independientes = hecho. 1 fuente = "posible que merezca seguimiento".

---

### Conclusión: El ciclo de OSINT

```
Dominio público (asignación) 
    ↓
Certificado público (CT logs + WHOIS)
    ↓
DNS público + HTTP services
    ↓
Infraestructura (IPs, ranges, servicios)
    ↓
Correlación (qué cambió, cuándo, por qué)
    ↓
Verificación con cliente (ownership, scope)
    ↓
Hallazgos (legacy expuesto, arquitectura leak, exposición data)
    ↓
Próximate fase (port scan, vuln assessment, testing)
```

OSINT es el foundation de todo assessment. Si no sabes QUÉ está públicamente accesible, no puedes defenderte tampoco.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - OSINT and Asset Intelligence - External Surface Mapping & Threat Intelligence

### Integraciones ampliadas

- Shodan: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Censys: integracion recomendada para aumentar profundidad, evidencia y backlog.
- VirusTotal: integracion recomendada para aumentar profundidad, evidencia y backlog.
- SecurityTrails: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: subdominios sombra.
- Integracion recomendada: Shodan.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: secretos filtrados.
- Integracion recomendada: Censys.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: activos legacy.
- Integracion recomendada: VirusTotal.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: subdominios sombra.
- Integracion recomendada: SecurityTrails.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: secretos filtrados.
- Integracion recomendada: Shodan.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: activos legacy.
- Integracion recomendada: Censys.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: subdominios sombra.
- Integracion recomendada: VirusTotal.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: secretos filtrados.
- Integracion recomendada: SecurityTrails.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: activos legacy.
- Integracion recomendada: Shodan.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: subdominios sombra.
- Integracion recomendada: Censys.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: secretos filtrados.
- Integracion recomendada: VirusTotal.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: activos legacy.
- Integracion recomendada: SecurityTrails.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: subdominios sombra.
- Integracion recomendada: Shodan.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: secretos filtrados.
- Integracion recomendada: Censys.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: activos legacy.
- Integracion recomendada: VirusTotal.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: subdominios sombra.
- Integracion recomendada: SecurityTrails.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: secretos filtrados.
- Integracion recomendada: Shodan.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: activos legacy.
- Integracion recomendada: Censys.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: subdominios sombra.
- Integracion recomendada: VirusTotal.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: secretos filtrados.
- Integracion recomendada: SecurityTrails.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: activos legacy.
- Integracion recomendada: Shodan.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: subdominios sombra.
- Integracion recomendada: Censys.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: secretos filtrados.
- Integracion recomendada: VirusTotal.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: activos legacy.
- Integracion recomendada: SecurityTrails.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 25
- Contexto: subdominios sombra.
- Integracion recomendada: Shodan.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 26
- Contexto: secretos filtrados.
- Integracion recomendada: Censys.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 27
- Contexto: activos legacy.
- Integracion recomendada: VirusTotal.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 28
- Contexto: subdominios sombra.
- Integracion recomendada: SecurityTrails.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 29
- Contexto: secretos filtrados.
- Integracion recomendada: Shodan.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 30
- Contexto: activos legacy.
- Integracion recomendada: Censys.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 31
- Contexto: subdominios sombra.
- Integracion recomendada: VirusTotal.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 32
- Contexto: secretos filtrados.
- Integracion recomendada: SecurityTrails.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 33
- Contexto: activos legacy.
- Integracion recomendada: Shodan.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 34
- Contexto: subdominios sombra.
- Integracion recomendada: Censys.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 35
- Contexto: secretos filtrados.
- Integracion recomendada: VirusTotal.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 36
- Contexto: activos legacy.
- Integracion recomendada: SecurityTrails.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 37
- Contexto: subdominios sombra.
- Integracion recomendada: Shodan.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 38
- Contexto: secretos filtrados.
- Integracion recomendada: Censys.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 39
- Contexto: activos legacy.
- Integracion recomendada: VirusTotal.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 40
- Contexto: subdominios sombra.
- Integracion recomendada: SecurityTrails.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 41
- Contexto: secretos filtrados.
- Integracion recomendada: Shodan.
- Senal principal: activo olvidado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 42
- Contexto: activos legacy.
- Integracion recomendada: Censys.
- Senal principal: proveedor no inventariado.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 43
- Contexto: subdominios sombra.
- Integracion recomendada: VirusTotal.
- Senal principal: repo publico.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

