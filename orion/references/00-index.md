# ORION-HACKING Reference Index

Este indice existe para que el skill sea grande sin volverse torpe. La regla es simple:
abre solo lo que haga falta para la tarea actual.

## Mapa de navegacion

| Necesidad | Archivo |
|---|---|
| Falta alcance, reglas o autorizacion | `01-authorization-and-governance.md` |
| Necesitas estructurar un trabajo completo | `02-engagement-workflow.md` |
| La IA va a escribir o ejecutar scripts | `03-ai-code-execution.md` |
| Discovery, red, puertos, servicios o TLS | `04-network-security.md` |
| OSINT, superficies externas o inventario publico | `05-osint-and-asset-intelligence.md` |
| Web, API, sesion, auth, headers o input handling | `06-web-api-appsec.md` |
| CVEs, scanners, priorizacion o revalidacion | `07-vulnerability-management.md` |
| Cloud, IAM, contenedores o Kubernetes | `08-cloud-container-k8s.md` |
| AD, endpoint, IAM o privilegios | `09-identity-endpoint-ad.md` |
| Wi-Fi, NAC, VPN o acceso remoto | `10-wireless-remote-access.md` |
| Incidentes, hunting o evidencia | `11-dfir-threat-hunting.md` |
| Sigma, YARA, SIEM o telemetria | `12-detection-engineering.md` |
| SDLC, SAST, IaC, secretos, PRs o pipelines | `13-secure-engineering-sdlc.md` |
| Reportes, risk register o remediation | `14-reporting-remediation.md` |
| Practica, labs o reproduccion segura | `15-labs-learning.md` |
| Threat modeling o arquitectura | `16-architecture-threat-modeling.md` |
| Mobile, desktop client o thick client | `17-mobile-client-security.md` |
| Cifrado, secretos o llaves | `18-crypto-key-management.md` |
| Datos, privacidad y minimizacion | `19-data-security-and-privacy.md` |
| Supply chain, SBOM, artefactos y secretos | `20-secrets-and-supply-chain.md` |
| SOC, runbooks y use cases | `21-soc-operations-use-cases.md` |
| Purple team y validacion de cobertura | `22-purple-teaming.md` |
| Plantillas cortas y ejemplos | `23-checklists-and-examples.md` |
| Perfiles de agente y patrones operativos | `24-ai-agent-operating-profiles.md` |
| Riesgo, madurez y roadmap | `25-grc-risk-and-maturity.md` |
| Patrones de automatizacion segura | `26-automation-patterns.md` |
| Especificacion de evidencia y logging | `27-evidence-and-logging-spec.md` |
| Matriz de seleccion de herramientas | `28-tool-selection-matrix.md` |
| Patrones de remediation | `29-remediation-patterns.md` |
| Plantillas de reporte | `30-report-templates.md` |
| Checklists de seguridad para agentes | `31-agent-safety-checklists.md` |
| Taxonomia extendida | `32-domain-taxonomy-extended.md` |

## Secuencias sugeridas

### Evaluacion tecnica autorizada
1. `01-authorization-and-governance.md`
2. `02-engagement-workflow.md`
3. Modulo tecnico aplicable
4. `14-reporting-remediation.md`

### Automatizacion con IA
1. `03-ai-code-execution.md`
2. `24-ai-agent-operating-profiles.md`
3. `26-automation-patterns.md`
4. `27-evidence-and-logging-spec.md`
5. Modulo tecnico aplicable
6. `14-reporting-remediation.md`

### Incidente o cazado de amenazas
1. `01-authorization-and-governance.md`
2. `11-dfir-threat-hunting.md`
3. `12-detection-engineering.md`
4. `21-soc-operations-use-cases.md`
5. `27-evidence-and-logging-spec.md`

### Secure engineering
1. `13-secure-engineering-sdlc.md`
2. `20-secrets-and-supply-chain.md`
3. `16-architecture-threat-modeling.md`
4. `14-reporting-remediation.md`

### Casos repetibles o muy operativos
1. `../PLAYBOOK_INDEX.md`
2. el playbook correspondiente
3. referencias puntuales del dominio

## Convenciones

- Confirmado: evidencia directa.
- Sospecha: evidencia parcial.
- No observado: no hubo evidencia, no equivale a seguro.
- Fuera de alcance: existe riesgo potencial pero no puede validarse.
- Requiere decision del dueno: el equipo tecnico no debe asumir por negocio.


<!-- ORION-EXPANSION-2026-04-05 -->

## Expansion Avanzada 2026 - ORION-HACKING Reference Index

### Integraciones ampliadas

- Markdown: integracion recomendada para aumentar profundidad, evidencia y backlog.
- HTML: integracion recomendada para aumentar profundidad, evidencia y backlog.
- OpenSearch: integracion recomendada para aumentar profundidad, evidencia y backlog.
- Singlefile: integracion recomendada para aumentar profundidad, evidencia y backlog.

### Escenarios realistas adicionales

### Escenario avanzado 01
- Contexto: navegacion de modulos.
- Integracion recomendada: Markdown.
- Senal principal: modulo huerfano.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 02
- Contexto: lectura offline.
- Integracion recomendada: HTML.
- Senal principal: enlace roto.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

### Escenario avanzado 03
- Contexto: carga selectiva IA.
- Integracion recomendada: OpenSearch.
- Senal principal: material repetido.
- Evidencia minima: artefactos originales, salida normalizada, owner y hash.
- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.
- Control: operar solo con alcance autorizado y con trazabilidad completa.

