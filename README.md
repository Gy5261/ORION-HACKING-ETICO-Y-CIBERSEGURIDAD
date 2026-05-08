# ORION - Hacking Ético y Ciberseguridad Profesional

![ORION](https://img.shields.io/badge/ORION-HACKING%20ÉTICO-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Markdown](https://img.shields.io/badge/Markdown-Standard-green)

**ORION** es un framework profesional, ético y escalable de **skills para hacking ético, ciberseguridad defensiva y automatización con IA/MCP**.

Repositorio diseñado para ser consumido tanto por humanos como por **agentes de IA (MCP, LLMs, asistentes autónomos)** de forma estructurada y segura.

## 🎯 Objetivo Principal

Proporcionar un repositorio limpio, mantenible, documentado y **listo para agentes IA** con:
- Playbooks operativos de ethical hacking
- Referencias técnicas modulares
- Scripts Python seguros y reutilizables
- Sistema avanzado de **skills estandarizados para IA**
- Workflows de CI/CD profesionales

## ⚠️ Disclaimer Ético (IMPORTANTE LEER)

- **Uso exclusivamente autorizado**: Solo en entornos donde tengas permiso explícito y por escrito.
- Prohibido cualquier uso malicioso, no autorizado o ilegal.
- Enfoque 100% en **defensa, auditoría ética, hardening y aprendizaje responsable**.
- El propietario del repositorio no se hace responsable del mal uso.

## 📁 Estructura Profesional del Proyecto

| Carpeta                  | Propósito                                      | Destacado para IA                  |
|--------------------------|------------------------------------------------|------------------------------------|
| `.github/workflows/`     | GitHub Actions (Lint, Build)                   | Automatización y calidad          |
| `orion/`                 | Núcleo del framework (playbooks + references)  | Contenido principal               |
| `orion/scripts/`         | Scripts Python seguros                         | Automatizaciones reutilizables    |
| `orion/playbooks/`       | Playbooks paso a paso                          | Guías operativas                  |
| `skills/`                | **Sistema de Skills para Agentes IA/MCP**      | **Manifiesto legible por IA**     |
| `samples/`               | Datos de ejemplo JSON                          | Testing e integración             |
| `pyproject.toml`         | Configuración Python moderna                   | Estándares de calidad             |
| `requirements.txt`       | Dependencias (stdlib-first)                    | Reproducibilidad                  |

## 🤖 Sistema Avanzado de Skills para IA (Carpeta `/skills/`)

Esta es una de las características más importantes del repositorio.

La carpeta [`/skills/`](https://github.com/Gy5261/ORION-HACKING-ETICO-Y-CIBERSEGURIDAD/tree/main/skills) contiene todo lo necesario para que **cualquier agente IA** pueda entender y usar el repositorio de forma estandarizada y segura:

- `skills.json` → Manifiesto principal legible por máquinas
- `ai-entrypoint.md` → Punto de entrada para agentes IA
- `agent-instructions.md` → Reglas estrictas de seguridad y uso ético
- `skills.md` → Documentación humana detallada

**Cualquier IA puede leer directamente:**
`https://github.com/Gy5261/ORION-HACKING-ETICO-Y-CIBERSEGURIDAD/tree/main/skills`

## 🛠️ GitHub Workflows Activos

- **Python Lint** (`python-lint.yml`): Ruff + best practices
- **Markdown Lint** (`markdown-lint.yml`): Con `.markdownlint.json`
- **Build Singlefile** (`build-singlefile.yml`): Genera HTML monolítico

## 🚀 Cómo Usar este Repositorio

### Para Humanos
1. Clona el repositorio
2. Revisa `orion/SKILL.md` y `orion/PLAYBOOK_INDEX.md`
3. Explora los scripts en `orion/scripts/`

### Para Agentes IA / MCP
1. Lee `skills/ai-entrypoint.md`
2. Carga `skills/skills.json`
3. Sigue `skills/agent-instructions.md` estrictamente

## 🔧 Scripts Python Disponibles

Ver carpeta [`orion/scripts/`](https://github.com/Gy5261/ORION-HACKING-ETICO-Y-CIBERSEGURIDAD/tree/main/orion/scripts)

## 📄 Licencia y Contribuciones

Licencia: MIT
Contribuciones bienvenidas bajo las reglas éticas del proyecto.

---

*Proyecto mantenido con altos estándares de calidad, seguridad y profesionalismo.*

Última mejora significativa: Mayo 2026