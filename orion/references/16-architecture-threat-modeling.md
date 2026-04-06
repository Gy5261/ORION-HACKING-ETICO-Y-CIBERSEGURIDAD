# Architecture & Threat Modeling - Design Before Code

## Concepto Fundamental

**Core Idea**: Architects + security team = identify threats BEFORE building

**Cost of fixes**:
- In design: $10, 1-2 days
- In code review: $500, 1-2 weeks  
- In production: $500K+, months, reputation damage

**What is Threat Modeling?**: Structured analysis of:
1. What we're protecting (assets)
2. Who attacks (threat actors)
3. How they attack (attack vectors)
4. What stops them (controls)

## Key Questions Before Code

1. **What data is sensitive?** (PII, payments, source code, customer secrets)
2. **Who are the attackers?** (script kiddies, organized crime, nation-state, insiders)
3. **What are attack vectors?** (code flaws, social engineering, supply chain, physical)
4. **What controls prevent attacks?** (validation, encryption, auth, logging)

## Data Flow Diagrams (DFD)

**Shows**: How data moves through system

```
User → [login] → Web Server → Auth Service → Database
                                  ↓
                            Logging Service
```

**Analysis**:
- Trust boundaries (internet ↔ server = untrusted input)
- Data classification (what's sensitive?)
- Risk per flow (theft, manipulation, exposure)
- Required controls (encryption, validation, auth)

## Asset & Risk Identification

**Assets**: PII, payment data, source code, trade secrets

**Risk Analysis Example**:
```
Asset: Credit card data
Risk 1: Stolen in transit (MITM) → Control: TLS encryption
Risk 2: Exposed in logs → Control: Never log card data
Risk 3: Stolen from database → Control: PCI-DSS compliance
```

## Trust Boundaries

**Every boundary = testing challenge**:
- Internet ↔ Web Server: Untrusted (validate everything)
- Web Server ↔ Database: Partially trusted (still validate, defend against lateral move)
- Database ↔ Payment Processor: Vendor risk (verify signatures, rate limit)

**Rule**: Don't increase trust without justification

## Dependency Risk

**Supply Chain Threats**:
- Your app uses library X (open source, 100K downloads)
- Attacker compromises library → 100K apps compromised
- Control: Vendor dependencies, update monitoring, SCA (software composition analysis)

## Threat Modeling Phases

**Phase 1: Inventory** (2-3 days)
- All components (web server, API, database, third-party services)
- All data flows (user → database paths)
- Trust boundaries
- External dependencies and integrations

**Phase 2: Identify Threats** (3-5 days)
- Per component: "What can go wrong?"
- Use STRIDE (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation)
- List 10+ threats for complex systems

**Phase 3: Map Controls** (2-3 days)
- For each threat: "What mitigates it?"
- Is control implemented? If not → backlog
- Estimate implementation effort

**Phase 4: Prioritize** (1 day)
- Highest risk threats first
- Highest ROI controls first
- Create roadmap

## Real Example: Prevented Breach

**Scenario**: Payment API design
1. Q: What trust boundaries?
   A: Internet → API, API → Payment processor
2. Q: Risk: Card data in logs?
   A: CRITICAL
3. Q: Control: Don't log card data?
   A: Implement immediately (2 days)

**Result**: 6 months later, a bug logs card numbers. Due to threat modeling, logs excluded cards. Breach prevented.

## Threat Model Checklist

✅ **Assets identified** (data types, locations)
✅ **Trust boundaries defined** (where trust changes)
✅ **Threats documented** (per STRIDE framework)
✅ **Controls mapped** (per threat)
✅ **Gaps identified** (missing controls)
✅ **Remediation prioritized** (by risk)
✅ **DFD created** (for communication)

## Deliverables

1. **Data Flow Diagram** (visual representation)
2. **Asset inventory** (what we're protecting)
3. **Threat list** (prioritized by risk)
4. **Control inventory** (existing mitigations)
5. **Remediation roadmap** (implementation plan by priority)


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - Architecture & Threat Modeling - Design Before Code

### Integraciones ampliadas

- Threat Dragon: integracion recomendada para aumentar profundidad, evidencia y backlog.
- draw.io: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Terraform: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Kubernetes: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: app multi-tenant.
- Integracion recomendada: Threat Dragon.
- Senal principal: trust boundary difusa.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: microservicios.
- Integracion recomendada: draw.io.
- Senal principal: owner ausente.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: modelo de pagos.
- Integracion recomendada: Terraform.
- Senal principal: blast radius alto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 04
- Contexto: app multi-tenant.
- Integracion recomendada: Kubernetes.
- Senal principal: trust boundary difusa.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

