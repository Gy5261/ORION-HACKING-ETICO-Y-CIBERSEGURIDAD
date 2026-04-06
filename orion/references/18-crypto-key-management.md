# Cryptography & Key Management - Securing Secrets

## Concepto Fundamental

**Core Truth**: If attacker has encrypted data, strong crypto = data stays secret (if done right)

**Statistics**:
- 80% of breaches could be prevented by encryption
- Key management failures = 60% of crypto breaches
- Weak algorithms still surprisingly common

## Bad vs Good Crypto

**❌ Don't Use**:
- MD5 (broken, collision attacks)
- DES (too weak)
- RC4 (probabilistic, not for sensitive data)
- Custom algorithms (almost always broken)

**✅ Use These**:
- AES-256 (encryption, symmetric)
- RSA-2048+ (encryption, asymmetric)
- SHA-256/SHA-3 (hashing)
- TLS 1.2+ (transport)
- Argon2 (password hashing)

## 5 Principios Fundamentales

1. **Don't Build Your Own Crypto**: Cryptography extremely hard. Use libraries (OpenSSL, libsodium, BoringSSL)
2. **Key Rotation**: Encrypt with key A → after 6 months switch to key B (old key = compromised = affects only old data)
3. **Key Storage**: Keys NEVER in code (use Vault, KMS, HSM)
4. **Encrypt Everywhere**: In transit (TLS), at rest (AES-256), in memory (while processing)
5. **Audit & Monitor**: Log all key access, alert on unusual use, track lifecycle

## Symmetric Encryption (AES)

**What**: Both parties share same key

```
Alice & Bob both have key ABC123
Alice: "Secret" + ABC123 = encrypted_data
Bob: encrypted_data + ABC123 = "Secret"
```

**Use Cases**: Database encryption, file encryption, disk encryption, service-to-service

**Variants**:
- AES-128 (128-bit) = okay
- AES-192 (192-bit) = good
- AES-256 (256-bit) = excellent (use this)

## Asymmetric Encryption (RSA)

**What**: Public key (everyone) + Private key (secret)

```
Alice public: PUBLIC123 (everyone knows)
Alice private: SECRET456 (only Alice)

Bob: message + PUBLIC123 = encrypted
Alice: encrypted + SECRET456 = message
```

**Use Cases**: TLS/HTTPS, digital signatures, SSH keys, API token signing

## Hashing (One-Way)

**What**: Input → Hash (can't reverse)

```
"password123" → SHA256 → a4b9d8f... (irreversible)
```

**Use Cases**: Password storage, integrity checking, digital signatures

**Algorithms**:
- ❌ MD5 (broken)
- ❌ SHA-1 (weak)
- ✅ SHA-256 (good)
- ✅ SHA-3 (excellent)
- ✅ Argon2 (password hashing)

## Key Lifecycle

```
Generate → Store → Use → Rotate → Retire
   ↓        ↓       ↓      ↓        ↓
 Secure   Vault  Log &  New key  Archive
randomness access monitor replace  safely
```

**Each Stage Critical**:
- Generation: Use cryptographic randomness (not time-based)
- Storage: Never plaintext (use KMS/Vault)
- Use: Log access, alert on unusual pattern
- Rotation: Plan before expiry
- Retirement: Securely destroy (not just delete)

## Assessment Methodology

**Phase 1** (1 week): Inventory what's encrypted, algorithms used, key storage, rotation policy

**Phase 2** (2-3 weeks): Review algorithms (weak ones?), key storage (hardcoded?), rotation (documented?)

**Phase 3** (2-4 weeks): Testing (extract keys from config? from memory? use old lost-key data?)

**Phase 4**: Remediation (replace weak algorithms, implement KMS, enforce rotation, remove hardcoded keys)

## Real Examples

**Example 1: Hardcoded Key Breach**
```
Code: ENCRYPTION_KEY = "SecretKey123"  # Problem!
Risk: Everyone with code access knows key
Attack: Any encrypted data is decryptable
Fix: Use Vault/KMS to store keys externally
```

**Example 2: Never-Rotated Keys**
- Production used same key for 5 years
- Key leaked (backup stolen)
- ALL 5 years of data compromised
- Prevention: Rotate every 90 days (old data = old key impact only)

## Checklist

✅ Encryption algorithms: AES-256 (not DES, RC4)
✅ Hashing: SHA-256+ (not MD5, SHA-1)
✅ Asymmetric: RSA-2048+ or ECDH
✅ TLS: 1.2+ configured
✅ Keys: Never hardcoded (use KMS)
✅ Storage: Accessed via vault/KMS only
✅ Rotation: Every __ days (target: 90)
✅ Monitoring: All access logged, unusual access alerted

## Priorities

1. Replace weak algorithms
2. Implement key management system (KMS/Vault)
3. Enforce key rotation policy
4. Remove hardcoded keys from code/config
- los secretos se registran en logs?

## Anti patrones frecuentes

- llaves hardcodeadas
- reuse entre dev y prod
- algoritmos legacy
- expiracion indefinida
- backups de llaves sin control

## Checklist

- TLS moderno
- rotacion documentada
- KMS o vault equivalente
- segregacion por entorno
- acceso auditado
- redaccion de secretos en observabilidad

## Ejemplo de hallazgo

```markdown
## Clave compartida entre staging y produccion
Estado: confirmado
Severidad: alta
Activo: servicio de colas
Evidencia: misma referencia de secreto en ambos entornos
Impacto real: aumenta radio de impacto ante fuga o uso indebido
Recomendacion: separar materiales criptograficos por entorno y rotar
```


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Cryptography & Key Management - Securing Secrets

### Integraciones ampliadas

- Vault: integracion recomendada para aumentar profundidad, evidencia y backlog.
- AWS KMS: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Azure Key Vault: integracion recomendada para aumentar profundidad, evidencia y backlog.
- OpenSSL: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: rotacion mTLS.
- Integracion recomendada: Vault.
- Senal principal: algoritmo legacy.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: llaves compartidas.
- Integracion recomendada: AWS KMS.
- Senal principal: llave sin rotacion.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: tokenizacion parcial.
- Integracion recomendada: Azure Key Vault.
- Senal principal: secreto exportable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: rotacion mTLS.
- Integracion recomendada: OpenSSL.
- Senal principal: algoritmo legacy.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 05
- Contexto: llaves compartidas.
- Integracion recomendada: Vault.
- Senal principal: llave sin rotacion.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 06
- Contexto: tokenizacion parcial.
- Integracion recomendada: AWS KMS.
- Senal principal: secreto exportable.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

