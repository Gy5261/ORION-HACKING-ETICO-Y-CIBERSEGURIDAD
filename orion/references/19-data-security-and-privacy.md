# Data Security & Privacy - Classification, Protection, Minimization

## Concepto

**Core Questions**:
1. What sensitive data exists? (PII, payments, trade secrets)
2. Where does it live? (databases, files, logs, backups)
3. Who accesses it? (humans, services, contractors)
4. How to minimize exposure? (encrypt, redact, limit access)

## Data Classification

**Levels**:
- PUBLIC: Can share externally (marketing, public docs)
- INTERNAL: Employees only (internal procedures, strategy)
- CONFIDENTIAL: Executive/sensitive (financial, customer data)
- RESTRICTED: PII, legal, regulatory (SSN, credit cards, health)

**Process**:
1. Identify all data types
2. Classify each (PUBLIC to RESTRICTED)
3. Define handling rules (encryption, access, retention)
4. Apply controls (encryption, access controls, monitoring)

## PII & Regulatory Data

**PII Example**: SSN, credit card, email, phone, home address

**Regulations**:
- GDPR (Europe): DPO required, consent for collection, right to delete
- CCPA (California): User rights, disclosure requirements
- HIPAA (Healthcare): Patient privacy, encryption required
- PCI-DSS (Payments): Encryption, access controls, auditing

**Controls Required**:
✅ Encryption at rest (AES-256)
✅ Encryption in transit (TLS)
✅ Limited access (principle of least privilege)
✅ Data minimization (collect only what needed)
✅ Retention limits (keep only as long as needed)
✅ Audit logging (track access)

## Unnecessary Data Exposure

**Common Problems**:
- Production data in test/dev (PII exposure)
- Sensitive data in logs (debugging leaves secrets)
- Unencrypted backups
- Overpermissioned service accounts
- Unnecessary field transmission

**Example**: Database has 100 fields, app only needs 5 → exposing 95 unnecessarily

## Data Minimization

**Principle**: Collect & store ONLY what's needed

**Example**:
- Full SSN not needed (last 4 digits sufficient)
- Full credit card not needed (tokenize with payment processor)
- Full email not needed (hashed for verification)

**Benefits**:
- Smaller breach surface
- Easier compliance
- Reduced storage costs

## Assessment Phases

**Phase 1** (2 weeks): Data inventory (what data exists, classification, location)
**Phase 2** (2 weeks): Access review (who accesses what, is it justified)
**Phase 3** (2 weeks): Exposure testing (unencrypted backups, logs with PII, unnecessary fields)
**Phase 4**: Remediation (encryption, access controls, data purge, log redaction)

## Real Example

**Finding**: Production customer data in QA database
- PII: Names, emails, SSNs, addresses
- Accessed by: 50 QA engineers
- Risk: Exposure if database breached
- Fix: Use synthetic data (fake names, dummy SSNs)
- Impact: Reduced breach surface

## Checklist

- [ ] Data classification: Complete
- [ ] PII encryption: At rest & in transit
- [ ] Unnecessary data: Removed (minimization)
- [ ] Logs: No sensitive data included
- [ ] Access: Restricted to needed only
- [ ] Retention: Policy documented
- [ ] Backups: Encrypted & isolated
- [ ] Compliance: GDPR/CCPA/HIPAA applicable?

## Quick Wins

1. Redact PII from logs (use last-4-digit format for SSN)
2. Remove test data with production PII
3. Encrypt backups (they're stored less securely)
4. Limit fields transmitted (only what's needed)
5. Implement data retention policy (auto-delete old data)

- clasificacion de datos
- retencion definida
- cifrado
- controles de acceso
- segregacion por entorno
- redaccion en logs

## Ejemplo de hallazgo

```markdown
## Datos reales en entorno de pruebas
Estado: confirmado
Severidad: alta
Activo: base de datos qa
Evidencia: registros de clientes reales
Impacto real: aumenta superficie de privacidad y cumplimiento
Recomendacion: usar datasets anonimizados y revisar politicas de replicacion
```
