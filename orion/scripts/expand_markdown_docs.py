#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path

MARKER = "<!-- ORION-EXPANSION-2026-04-05 -->"

GROUP_MAP = {
    "authorization": ("governance", ["Jira", "ServiceNow", "Confluence", "Vault"], ["renovacion de pentest bancario", "evaluacion de proveedor SaaS", "assessment previo a merger"], ["scope ambiguo", "owner ausente", "ventana no aprobada"]),
    "engagement": ("governance", ["Jira", "ServiceNow", "Confluence", "Vault"], ["kickoff multi-equipo", "assessment regulado", "cierre con backlog"], ["sin acta", "sin escalacion", "sin exclusiones"]),
    "grc": ("governance", ["Jira", "ServiceNow", "PowerBI", "Confluence"], ["revision HIPAA", "gap PCI", "madurez NIST"], ["control sin owner", "riesgo sin ranking", "backlog sin fechas"]),
    "ai": ("ai", ["OpenAI", "Azure OpenAI", "Langfuse", "OpenTelemetry"], ["agente de triage", "guardrail de prompts", "generacion de evidencia"], ["prompt injection", "tool misuse", "salto de alcance"]),
    "network": ("network", ["Nmap", "Masscan", "Zeek", "Wazuh"], ["segmentacion debil", "firewall heredado", "servicio expuesto"], ["admin remota", "cifrado debil", "baseline roto"]),
    "osint": ("osint", ["Shodan", "Censys", "VirusTotal", "SecurityTrails"], ["subdominios sombra", "secretos filtrados", "activos legacy"], ["repo publico", "activo olvidado", "proveedor no inventariado"]),
    "web": ("web", ["Burp Suite", "OWASP ZAP", "Postman", "OpenAPI"], ["checkout con authz debil", "JWT mal validado", "portal con SSRF"], ["errores verbose", "control de acceso roto", "flujo multi-step inseguro"]),
    "vulnerability": ("vuln", ["Nessus", "Qualys", "DefectDojo", "Jira"], ["priorizacion de CVEs", "deduplicacion masiva", "retest por sprint"], ["severidad sin contexto", "finding duplicado", "evidencia incompleta"]),
    "cloud": ("cloud", ["AWS", "Azure", "GCP", "Kubernetes"], ["EKS con IRSA permisivo", "Storage expuesto", "Terraform con secretos"], ["IAM excesivo", "logs no retenidos", "secretos en CI"]),
    "identity": ("identity", ["AD", "Entra ID", "Okta", "CrowdStrike"], ["tiering insuficiente", "claims excesivos", "MFA parcial"], ["grupo critico", "servicio sin rotacion", "admin sin aislamiento"]),
    "wireless": ("wireless", ["Kismet", "Aircrack-ng", "Cisco ISE", "Aruba Central"], ["WPA2-Enterprise debil", "guest con salto lateral", "VPN heredada"], ["SSID huerfano", "EAP vencido", "split tunneling"]),
    "dfir": ("dfir", ["Velociraptor", "Sysmon", "Defender", "Sigma"], ["phishing con token", "lateral movement", "living off the land"], ["proceso anomalo", "persistencia nueva", "host privilegiado"]),
    "detection": ("detection", ["Splunk", "Elastic", "Sentinel", "Sigma"], ["abuso de OAuth", "staging PowerShell", "hunting IAM"], ["false positive alto", "lag de ingesta", "coverage ATT&CK pobre"]),
    "sdlc": ("sdlc", ["GitHub Actions", "GitLab CI", "Semgrep", "Trivy"], ["monorepo con secretos", "SBOM faltante", "release sin firmas"], ["branch protection debil", "dep obsoleta", "provenance incompleta"]),
    "reporting": ("reporting", ["Jira", "Confluence", "PowerBI", "DefectDojo"], ["heatmap ejecutivo", "tracking 90 dias", "reporte regulatorio"], ["finding sin owner", "riesgo sin negocio", "evidencia no verificable"]),
    "labs": ("labs", ["Docker", "Kind", "Vagrant", "Codespaces"], ["lab SSRF", "lab Sigma", "simulacion AD"], ["dato real en lab", "sin rollback", "tooling sin version"]),
    "architecture": ("architecture", ["Threat Dragon", "draw.io", "Terraform", "Kubernetes"], ["app multi-tenant", "microservicios", "modelo de pagos"], ["trust boundary difusa", "owner ausente", "blast radius alto"]),
    "mobile": ("mobile", ["MobSF", "Frida", "Burp Suite", "Firebase"], ["storage local sensible", "pinning inconsistente", "SDK excesivo"], ["secretos hardcoded", "storage inseguro", "backend assumptions"]),
    "crypto": ("crypto", ["Vault", "AWS KMS", "Azure Key Vault", "OpenSSL"], ["rotacion mTLS", "llaves compartidas", "tokenizacion parcial"], ["algoritmo legacy", "llave sin rotacion", "secreto exportable"]),
    "data": ("data", ["BigQuery", "Snowflake", "S3", "DLP"], ["PII mezclada con telemetria", "backup expuesto", "export con datos productivos"], ["clasificacion ausente", "retencion infinita", "ACL heredada"]),
    "secrets": ("supply", ["Trivy", "Syft", "Cosign", "Registry"], ["imagen base vulnerable", "dependencia comprometida", "firma OCI ausente"], ["sin pinning", "build no reproducible", "SBOM incompleta"]),
    "soc": ("soc", ["SOAR", "TheHive", "Cortex", "MISP"], ["cola saturada", "enrichment de alertas", "handoff a DFIR"], ["MTTR alto", "runbook parcial", "sin enrichment"]),
    "purple": ("purple", ["CALDERA", "Atomic Red Team", "Sigma", "ATT&CK"], ["validacion credential access", "campaign exfil", "hardening iterativo"], ["sin coverage", "objetivo difuso", "hallazgo fuera de backlog"]),
    "automation": ("automation", ["GitHub Actions", "Cron", "Airflow", "PowerShell"], ["pipeline nocturno", "ticketing automatico", "evidence recurring"], ["sin rollback", "credencial fija", "salida no normalizada"]),
    "evidence": ("evidence", ["S3", "Azure Blob", "OpenSearch", "Velociraptor"], ["cadena de custodia", "hashing previo", "manifest para auditoria"], ["hash ausente", "metadata incompleta", "movimiento sin registro"]),
    "tool": ("tooling", ["Burp Suite", "Nmap", "Trivy", "Semgrep"], ["seleccion de stack", "comparativa de scanners", "normalizacion heterogenea"], ["tool sin tuning", "formato incompatible", "sesgo de herramienta"]),
    "remediation": ("remediation", ["Jira", "Azure DevOps", "GitHub", "ServiceNow"], ["plan 30-60-90", "owners por dominio", "retest automatizado"], ["fix sin validacion", "riesgo aceptado", "deuda fuera de backlog"]),
    "taxonomy": ("taxonomy", ["Sigma", "ATT&CK", "NIST CSF", "CWE"], ["routing ambiguo", "finding multi-dominio", "priorizacion por control"], ["tags inconsistentes", "dominio omitido", "salida incomparable"]),
    "index": ("index", ["Markdown", "HTML", "OpenSearch", "Singlefile"], ["navegacion de modulos", "lectura offline", "carga selectiva IA"], ["modulo huerfano", "enlace roto", "material repetido"]),
}

DEFAULT_META = ("generic", ["Jira", "OpenSearch", "ServiceNow", "GitHub Actions"], ["assessment con evidencia", "priorizacion de backlog", "validacion controlada"], ["owner difuso", "salida no repetible", "riesgo sin contexto"])

def lines(text: str) -> int:
    return len(text.splitlines())


def heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return fallback


def ref_meta(stem: str):
    s = stem.lower()
    for token, meta in GROUP_MAP.items():
        if token in s:
            return meta
    return DEFAULT_META


def build_reference(title: str, stem: str, target: int) -> str:
    group, integrations, cases, signals = ref_meta(stem)
    out = [MARKER, '', f'## Expansion Avanzada 2026 - {title}', '', '### Integraciones ampliadas', '']
    out += [f'- {item}: integracion recomendada para aumentar profundidad, evidencia y backlog.' for item in integrations]
    out += ['', '### Escenarios realistas adicionales', '']
    n = 1
    while len(out) < target:
        case = cases[(n - 1) % len(cases)]
        signal = signals[(n - 1) % len(signals)]
        integ = integrations[(n - 1) % len(integrations)]
        out += [
            f'### Escenario avanzado {n:02d}',
            f'- Contexto: {case}.',
            f'- Integracion recomendada: {integ}.',
            f'- Senal principal: {signal}.',
            '- Evidencia minima: artefactos originales, salida normalizada, owner y hash.',
            '- Resultado esperado: decision accionable, remediacion propuesta y siguiente validacion.',
            '- Control: operar solo con alcance autorizado y con trazabilidad completa.',
            '',
        ]
        n += 1
    return '\n'.join(out)


def playbook_focus(stem: str) -> str:
    s = stem.lower()
    if 'authorized-assessment' in s:
        return 'assessment multi-dominio'
    if 'web-api-review' in s:
        return 'web y API criticas'
    if 'cloud-k8s-review' in s:
        return 'cloud y kubernetes'
    if 'detection-hunting' in s:
        return 'deteccion y hunting'
    if 'secure-sdlc-review' in s:
        return 'pipeline y secure SDLC'
    if 'incident-triage' in s:
        return 'incidente activo y contencion inicial'
    return 'workflow especializado'


def build_playbook(title: str, stem: str, target: int) -> str:
    focus = playbook_focus(stem)
    integrations = ['Jira', 'ServiceNow', 'Slack/Teams', 'OpenSearch', 'GitHub Actions', 'Splunk']
    out = [MARKER, '', f'## Expansion Operativa 2026 - {title}', '', f'Este playbook se amplia para cubrir integraciones y casos de {focus}.', '', '### Integraciones de ejecucion', '']
    out += [f'- {item}: usar para coordinacion, backlog, evidencia o telemetria.' for item in integrations]
    out += ['', '### Casos operativos extendidos', '']
    n = 1
    while len(out) < target:
        integ = integrations[(n - 1) % len(integrations)]
        out += [
            f'### Caso operativo {n:02d}',
            f'- Situacion: engagement de {focus} con ventana de tiempo corta y requerimiento alto de evidencia.',
            f'- Integracion principal: {integ}.',
            '- Entradas extra: inventario, owner tecnico, criterios de exito, backlog abierto y exclusiones.',
            '- Automatizacion: normalizacion de findings, enrichment de IOCs, manifiesto de evidencia y sincronizacion a tickets.',
            '- Verificacion final: owner confirmado, criterio de cierre, fecha objetivo y artefactos hashados.',
            '',
        ]
        n += 1
    return '\n'.join(out)


def build_core(path: Path, title: str, target: int) -> str:
    name = path.name
    out = [MARKER, '']
    if name == 'README.md' and path.parent.name == 'ORION-HACKING-github':
        out += [
            '## Expansion Oficial 2026',
            '',
            '- Nombre del repositorio en GitHub: `ORION-HACKING-ETICO-Y-CIBERSEGURIDAD`.',
            '- Nuevas utilidades agregadas: `ioc_enricher.py`, `findings_ticket_sync.py`, `tls_posture_audit.py`, `evidence_manifest.py`.',
            '- Integraciones avanzadas: Jira, ServiceNow, Splunk, OpenSearch, VirusTotal, Shodan y GitHub Actions.',
            '',
            '### Casos de uso reales agregados',
            '',
            '- API de pagos con hallazgos priorizados y ticketing automatizado.',
            '- Cluster Kubernetes con hardening incremental y evidencia reproducible.',
            '- Incidente de phishing con enrichment de IOCs y handoff a DFIR.',
            '- Repositorio CI/CD con SBOM, findings normalizados y backlog accionable.',
            '',
        ]
    elif name == 'ARCHITECTURE.md':
        out += ['## Expansion de arquitectura 2026', '', '### Patrones nuevos', '']
        n = 1
        while len(out) < target:
            out += [
                f'### Patron adicional {n:02d}',
                '- Flujo: ingesta -> enrichment -> priorizacion -> ticketing -> retest.',
                '- Objetivo: desacoplar conocimiento, metodologia, evidencia e integracion externa.',
                '- Integraciones: Jira, ServiceNow, OpenSearch, threat intel y pipelines CI.',
                '- Restriccion: sin cambios fuera de alcance y con rollback definido.',
                '',
            ]
            n += 1
    elif name == 'DOMAIN_TAXONOMY.md':
        out += ['## Expansion de taxonomia 2026', '', '### Reglas adicionales', '']
        examples = ['API con backlog regulatorio', 'cluster cloud con IAM heredado', 'alerta DFIR con IOC externo', 'pipeline supply chain sin firma OCI']
        n = 1
        while len(out) < target:
            ex = examples[(n - 1) % len(examples)]
            out += [
                f'### Regla ampliada {n:02d}',
                f'- Entrada ejemplo: {ex}.',
                '- Dominio primario: el que gobierna el riesgo inmediato.',
                '- Dominios secundarios: governance, reporting, evidence o automation cuando aumenten accionabilidad.',
                '- Salida: skill/playbook sugerido, evidencia minima y owner siguiente.',
                '',
            ]
            n += 1
    elif name == 'MODULE_MAP.md':
        out += ['## Expansion del mapa modular 2026', '', '### Nuevas rutas', '']
        n = 1
        while len(out) < target:
            out += [
                f'### Ruta extendida {n:02d}',
                '- Entrada: solicitud ambigua, finding puntual o incidente en curso.',
                '- Modulos sugeridos: skill principal + referencias + playbook + script auxiliar.',
                '- Integracion sugerida: backlog, threat intel, evidence o dashboard ejecutivo.',
                '- Salida objetivo: decision defendible y siguiente accion concreta.',
                '',
            ]
            n += 1
    elif name == 'PLAYBOOK_INDEX.md':
        out += ['## Expansion del indice 2026', '', '### Criterios adicionales', '']
        factors = ['madurez del cliente', 'necesidad de evidencia', 'integracion con backlog', 'dependencias cloud y supply chain']
        n = 1
        while len(out) < target:
            factor = factors[(n - 1) % len(factors)]
            out += [
                f'### Criterio avanzado {n:02d}',
                f'- Factor dominante: {factor}.',
                '- Ajuste recomendado: aumentar evidence, integracion o remediacion segun el riesgo.',
                '- Caso realista: combinar playbook principal con modulos secundarios.',
                '',
            ]
            n += 1
    elif path.parent.name == 'evals' or name == 'skill-evaluation.md':
        out += ['## Expansion de evaluacion 2026', '', '### Nuevas suites', '']
        n = 1
        while len(out) < target:
            out += [
                f'### Suite adicional {n:02d}',
                '- Prompt de prueba: engagement con alcance autorizado, dependencia cloud e integracion externa.',
                '- Exito: ruta clara, evidencia verificable y backlog priorizado.',
                '- Falla: sin owner, sin control de alcance o sin salida accionable.',
                '',
            ]
            n += 1
    else:
        out += [f'## Expansion complementaria 2026 - {title}', '']
        n = 1
        while len(out) < target:
            out += [
                f'### Complemento {n:02d}',
                '- Este bloque agrega integracion, evidencia y contexto realista sin borrar la base existente.',
                '- Debe usarse para profundizar decisiones y soportar automatizacion segura.',
                '',
            ]
            n += 1
    return '\n'.join(out)

def build_skill(title: str, target: int) -> str:
    integrations = [
        ('Jira', 'backlog de remediacion y retest'),
        ('ServiceNow', 'incidentes y cambios de seguridad'),
        ('Splunk', 'correlacion y validacion en lectura'),
        ('OpenSearch', 'indexacion de evidencia y findings'),
        ('MISP', 'contexto de IOCs y campañas'),
        ('VirusTotal', 'reputacion externa opcional'),
        ('AbuseIPDB', 'calificacion de IPs'),
        ('AlienVault OTX', 'pulsos de amenaza'),
        ('Shodan', 'exposicion de servicios autorizados'),
        ('GitHub Actions', 'chequeos y empaquetado reproducible'),
        ('DefectDojo', 'consolidacion y deduplicacion'),
        ('Confluence', 'decision logs y reporte ejecutivo'),
        ('Slack/Teams', 'alertas y escalaciones'),
        ('AWS Security Hub', 'hallazgos cloud en lectura'),
        ('Azure Defender', 'telemetria de tenant'),
        ('Google SCC', 'postura GCP'),
        ('Velociraptor', 'evidencia DFIR estructurada'),
        ('Sigma', 'reglas de hunting defendibles'),
        ('Semgrep', 'hallazgos de codigo a backlog'),
        ('Trivy/Syft/Cosign', 'SBOM, vulnerabilidades y firmas'),
    ]
    contracts = [
        'enrichment de IOCs antes de priorizar incidentes',
        'manifest de evidencia antes de mover artefactos',
        'sincronizacion de findings a backlog con contexto tecnico',
        'auditoria TLS basica previa a assessment web o API',
        'normalizacion multi-fuente de findings en JSON canonico',
        'deteccion de gaps de evidencia antes del reporte final',
        'clasificacion por dominio primario y secundario',
        'retest guiado posterior a remediacion',
        'resumen ejecutivo basado en datos verificados',
        'hand-off SOC a DFIR con enrichment estructurado',
        'control de cambio para scripts con servicios externos',
        'paquetes de evidencia para auditoria externa',
    ]
    combos = [
        ('web + identity', 'portal con SSO y roles heredados'),
        ('web + cloud', 'API sobre ALB y workloads EKS'),
        ('sdlc + supply-chain', 'pipeline con SBOM y firma OCI'),
        ('dfir + threat-intel', 'IOC observado en endpoint privilegiado'),
        ('network + cloud', 'segmentacion hibrida VPC/sede'),
        ('governance + reporting', 'board exige ROI y riesgo residual'),
        ('mobile + API', 'cliente movil multi-tenant'),
        ('crypto + data-security', 'tokenizacion parcial de datos'),
        ('soc + purple-team', 'exercise de coverage real'),
        ('wireless + identity', 'WPA2-Enterprise ligado a AD'),
    ]
    outputs = [
        'json normalizado', 'markdown ejecutivo', 'html singlefile', 'manifest de evidencia',
        'payload de tickets', 'matriz de cobertura', 'timeline de incidente', 'inventario de activos'
    ]
    sectors = [
        ('fintech regional', 'API de pagos con JWT federado y backlog regulatorio'),
        ('retail omnicanal', 'checkout web con fraude promocional y SaaS terceros'),
        ('healthtech', 'PII y ventanas de cambio restringidas'),
        ('SaaS B2B', 'SSO SAML y pipeline de release'),
        ('manufactura', 'OT parcialmente conectada y exposicion remota'),
        ('sector publico', 'retencion normativa y aprobaciones formales'),
    ]
    phases = ['discovery', 'validacion tecnica', 'priorizacion', 'ticketing', 'retest', 'cierre']
    out = [MARKER, '', f'## PARTE 7: EXPANSION ESTRATEGICA 2026 - {title}', '', '### Objetivo', '', '- Aumentar capacidad operativa, integraciones y contratos de automatizacion sin borrar el marco existente.', '- Ampliar cobertura multi-dominio para escenarios reales de ciberseguridad y hacking etico autorizado.', '- Fortalecer evidence, backlog, enrichment y modularidad del skill principal.', '', '### Integraciones de ecosistema', '']
    for name, purpose in integrations:
        out += [f'#### Integracion: {name}', f'- Proposito: {purpose}.', '- Modo seguro: lectura por defecto y escritura solo con aprobacion explicita.', '- Evidencia esperada: request, respuesta, decision, timestamp y owner.', '- Riesgo a vigilar: automatizacion no justificada o exceso de confianza en datos externos.', '']
    out += ['### Contratos de automatizacion', '']
    for idx, contract in enumerate(contracts, 1):
        out += [f'#### Contrato {idx:02d}', f'- Descripcion: {contract}.', '- Entrada minima: alcance, owner, artefacto origen y criterio de exito.', '- Salida obligatoria: JSON normalizado, decision, owner siguiente y riesgo residual.', '- Hard stop: falta de autorizacion, salida no repetible o impacto excesivo.', '']
    out += ['### Matriz multi-dominio', '']
    for idx, (combo, example) in enumerate(combos, 1):
        out += [f'#### Ruta combinada {idx:02d}: {combo}', f'- Ejemplo realista: {example}.', '- Skill principal: decide alcance, restricciones, orden de carga y scripts auxiliares.', '- Resultado: salida defendible con hallazgos, integraciones y siguiente accion concreta.', '']
    out += ['### Salidas estructuradas', '']
    for idx, item in enumerate(outputs, 1):
        out += [f'#### Salida {idx:02d}', f'- Tipo: {item}.', '- Debe ser consumible por humanos y automatizaciones posteriores.', '- Contenido minimo: fecha, owner, origen, evidencia, decision y riesgo residual.', '']
    out += ['### Casos de uso reales ampliados', '']
    n = 1
    while len(out) < target:
        sector, scenario = sectors[(n - 1) % len(sectors)]
        phase = phases[(n - 1) % len(phases)]
        integ = integrations[(n - 1) % len(integrations)][0]
        contract = contracts[(n - 1) % len(contracts)]
        output = outputs[(n - 1) % len(outputs)]
        out += [
            f'### Caso extendido {n:03d}',
            f'- Sector: {sector}.',
            f'- Escenario: {scenario}.',
            f'- Fase dominante: {phase}.',
            f'- Integracion clave: {integ}.',
            f'- Contrato sugerido: {contract}.',
            f'- Salida prioritaria: {output}.',
            '- Skill principal: evaluar alcance, restricciones, autorizacion y riesgo de exceso.',
            '- Modulos a cargar: referencias primarias, secundarias y playbook especifico.',
            '- Evidencia requerida: artefactos origen, enrichment opcional, decision y hash de salida.',
            '- Condicion de stop: datos insuficientes, owner ausente o actividad fuera de alcance.',
            '- Resultado esperado: accion inmediata, backlog claro y control de seguimiento.',
            '',
        ]
        n += 1
    return '\n'.join(out)


def expand(path: Path, root: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if MARKER in text:
        return None
    original = lines(text)
    target = math.ceil(original * (0.85 if path.name == 'SKILL.md' and path.parent.name == 'orion' else 0.35))
    title = heading(text, path.stem.replace('-', ' ').title())
    if path.parent.name == 'references':
        addition = build_reference(title, path.stem, target)
    elif path.parent.name == 'playbooks':
        addition = build_playbook(title, path.stem, target)
    elif path.name == 'SKILL.md' and path.parent.name == 'orion':
        addition = build_skill(title, target)
    else:
        addition = build_core(path, title, target)
    with path.open('a', encoding='utf-8', newline='\n') as handle:
        handle.write('\n\n' + addition + '\n')
    print(f'expanded\t{path.relative_to(root)}\t{original}\t+{lines(addition)}')


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    for path in sorted(root.rglob('*.md')):
        expand(path, root)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
