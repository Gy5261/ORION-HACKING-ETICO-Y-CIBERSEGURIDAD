# ORION-HACKING v.0.1

ORION-HACKING v.0.1 es una base de skills para ciberseguridad autorizada y automatizacion segura con IA.

Hecho por ORION-IA.

## Contenido

- `orion/SKILL.md`: skill principal
- `orion/ARCHITECTURE.md`: arquitectura del sistema
- `orion/MODULE_MAP.md`: mapa de modulos
- `orion/PLAYBOOK_INDEX.md`: indice de playbooks
- `orion/DOMAIN_TAXONOMY.md`: taxonomia macro
- `orion/references/`: biblioteca modular de seguridad
- `orion/playbooks/`: skills operativos por dominio
- `orion/scripts/`: utilidades seguras de apoyo
- `orion/ORION-HACKING-singlefile.html`: version monolitica con HTML, CSS, JavaScript y dataset embebido

## Dominios cubiertos

- gobernanza y alcance
- pentesting etico y validacion segura
- OSINT y asset intelligence
- web, API y AppSec
- vulnerabilidades y priorizacion
- cloud, contenedores y Kubernetes
- identidad, endpoint y Active Directory
- wireless y acceso remoto
- DFIR, hunting y deteccion
- secure engineering, supply chain y secretos
- threat modeling, privacidad y criptografia
- SOC, purple team, madurez y automatizacion para agentes

## Principios

- solo uso autorizado
- evidencia antes que hype
- bajo impacto antes que agresividad
- automatizacion pequena, auditable y reversible
- sin malware, evasiones, persistence ni abuso operativo

## Uso

Abre `orion/SKILL.md` como skill principal y luego carga solo los modulos de `orion/references/` que apliquen al caso.

Si la tarea es recurrente o muy concreta, entra por `orion/PLAYBOOK_INDEX.md` y desde ahi baja
al skill operativo correspondiente.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Oficial 2026

- Nombre del repositorio en GitHub: `ORION-HACKING-ETICO-Y-CIBERSEGURIDAD`.
- Nuevas utilidades agregadas: `ioc_enricher.py`, `findings_ticket_sync.py`, `tls_posture_audit.py`, `evidence_manifest.py`.
- Integraciones avanzadas: Jira, ServiceNow, Splunk, OpenSearch, VirusTotal, Shodan y GitHub Actions.

### Casos de uso reales agregados

- API de pagos con hallazgos priorizados y ticketing automatizado.
- Cluster Kubernetes con hardening incremental y evidencia reproducible.
- Incidente de phishing con enrichment de IOCs y handoff a DFIR.
- Repositorio CI/CD con SBOM, findings normalizados y backlog accionable.

### Modulos y automatizacion agregada

- Enrichment de IOCs con servicios externos opcionales y salida JSON reutilizable.
- Sincronizacion segura de hallazgos hacia Jira o ServiceNow con prioridad consistente.
- Auditoria de postura TLS para endpoints web antes de assessment o retest.
- Manifiestos de evidencia con SHA-256 para reforzar cadena de custodia.
- Expansiones documentales con escenarios reales por dominio, integraciones y backlog accionable.
