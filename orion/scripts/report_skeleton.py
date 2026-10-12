"""Generador de una plantilla de informe de seguridad, sin resultados inventados."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE = """# Informe técnico de evaluación de seguridad — ORION

**Estado:** Pendiente de evaluación
**Fecha de generación (UTC):** {timestamp}
**Clasificación:** Definir según la política del responsable

## Resumen ejecutivo

**Objetivo:** Documentar una evaluación autorizada, verificable y reproducible.
**Resultado:** No se han registrado hallazgos. Esta plantilla no acredita una auditoría.
**Riesgo global:** No evaluado. No calcular riesgo sin evidencia y contexto de negocio.

## Alcance y autorización

**Organización y propietario:** Pendiente de completar.
**Referencia documental de autorización:** Pendiente.
**Responsables y contactos de emergencia:** Pendiente.
**Ventana de pruebas y zona horaria:** Pendiente.
**Activos permitidos:** Pendiente.
**Activos excluidos:** Pendiente.
**Acciones prohibidas y límites de frecuencia:** Pendiente.
**Criterios de detención:** Pendiente.

## Metodología y límites

Registrar la metodología efectivamente utilizada, el ambiente, los controles,
las herramientas y versiones verificadas, los pasos ejecutados y las limitaciones.
No afirmar alineación, certificación o conformidad con un estándar sin comprobación
trazable del control correspondiente.

## Resultados de las comprobaciones

| Identificador | Control probado | Método | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| Pendiente | Pendiente | Pendiente | No ejecutado | No disponible |

Estados admitidos: No ejecutado, Aprobado, Fallido, No aplicable, Bloqueado.
Una herramienta instalada o una respuesta HTTP no constituyen, por sí solas,
prueba de ausencia de vulnerabilidades.

## Hallazgos

No se han registrado hallazgos.

Para cada hallazgo comprobado, registrar: identificador, activo, precondiciones,
vector o método de validación autorizado, impacto observado, evidencia reproducible,
severidad justificada, CWE si aplica, CVSS con versión y vector si se calculó,
responsable, recomendación y estado de revalidación.

No rellenar CVSS, CWE, severidad, impacto, número de registros, plazos,
fechas de remediación ni aceptación de riesgo con cifras supuestas.

## Evidencia

**Referencias a archivos o registros originales:** Pendiente.
**Fecha, zona horaria y origen:** Pendiente.
**Integridad (SHA-256) y custodia:** Pendiente.
**Tratamiento de datos sensibles:** Pendiente.
**Limitaciones de reproducción:** Pendiente.

Conservar solamente evidencia necesaria y autorizada. Mantener la evidencia sensible
fuera del repositorio público. Una huella hash no demuestra por sí sola cadena de custodia.

## Plan de remediación

| Hallazgo | Medida correctiva | Responsable | Prioridad | Fecha acordada | Prueba de cierre |
| --- | --- | --- | --- | --- | --- |
| Pendiente | Pendiente | Pendiente | Sin asignar | Sin definir | Pendiente |

Distinguir corrección implementada de corrección verificada. Documentar cambios,
riesgos de regresión y criterios de reversión.

## Revalidación y conclusiones

**Pruebas posteriores a la corrección:** No ejecutadas.
**Riesgo residual:** No evaluado.
**Resultado de la evaluación:** Pendiente.

La generación de este documento no implica que se haya ejecutado una prueba,
que el sistema sea seguro, ni que exista autorización jurídica.

## Referencias

Añadir únicamente fuentes y normas realmente consultadas, con versión, fecha
y correspondencia comprobable con los controles evaluados.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Crear una plantilla de informe sin evidencias ficticias")
    parser.add_argument("salida", help="Ruta de salida .md")
    parser.add_argument("--overwrite", action="store_true", help="Autorizar sobrescritura del informe existente")
    args = parser.parse_args()
    destination = Path(args.salida)
    if destination.suffix.casefold() != ".md":
        parser.error("La ruta de salida debe terminar en .md")
    content = TEMPLATE.format(timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"))
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w" if args.overwrite else "x", encoding="utf-8") as handle:
            handle.write(content)
    except FileExistsError:
        parser.exit(1, "Error: el informe ya existe; utilice --overwrite para reemplazarlo.\n")
    except OSError as exc:
        parser.exit(1, f"Error de escritura: {exc}\n")
    print(f"Plantilla creada: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
