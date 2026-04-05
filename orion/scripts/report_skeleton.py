#!/usr/bin/env python3
"""
report_skeleton.py - Genera plantilla de reporte de evaluación de seguridad.

Crea esqueleto automatizado de reporte Markdown con secciones estándar
para evaluaciones de seguridad autorizadas, pentesting ético y auditorías.

Uso:
    python3 report_skeleton.py <salida.md>
    python3 report_skeleton.py reporte-cliente-2024.md

Secciones generadas:
- Información ejecutiva
- Alcance y limitaciones
- Metodología
- Hallazgos clasificados por severidad
- Riesggo agregado
- Recomendaciones priorizadas
- Plan de revalidación
- Evidencia y anexos

La plantilla está formateada para Markdown y lista para editar.
"""

import sys
from datetime import datetime


TEMPLATE = """# Reporte de Evaluación de Seguridad - ORION-HACKING

**Información Confidencial**

---

## Resumen Ejecutivo

### Propósito
Evaluación estructurada de seguridad enfocada en riesgos identificables y remediación práctica.

### Alcance
- **Objetivos**: [Describir qué se evaluó]
- **Sistemas**: [Listar sistemas/dominios particulares]
- **Fechas**: {date_generated}
- **Evaluador**: ORION-HACKING Security Team
- **Autorización**: [Documento/referencia de autorización]

### Ubicación Ejecutiva
- **Total Hallazgos**: [#]
  - Críticos: [#]
  - Altos: [#]
  - Medios: [#]
  - Bajos: [#]
- **Riesgo Agregado**: [Muy Alto | Alto | Medio | Bajo]
- **Estado**: [En Progreso | Completado]

---

## 1. Alcance y Limitaciones

### 1.1 Alcance de la Evaluación

#### Incluido
- [Sistema o componente 1]
- [Sistema o componente 2]
- [Dominios de evaluación específicos]

#### Excluido
- [Sistemas/componentes fuera de alcance]
- [Razones técnicas o de negocio]

### 1.2 Limitaciones

- **Técnicas**: [Restricciones de herramientas, acceso]
- **Temporales**: [Período de evaluación]
- **Documentales**: [Información disponible]
- **Operacionales**: [Restricciones de downtime, ventanas]

### 1.3 Disclaimers

Esta evaluación representa el estado de seguridad en la fecha de evaluación.
Cambios posteriores o configuraciones no revisadas pueden afectar los hallazgos.

---

## 2. Metodología

### 2.1 Enfoque
Se utilizó metodología basada en:
- OWASP Testing Guide (para aplicaciones web)
- NIST Cybersecurity Framework (para gobernanza)
- CIS Controls v8 (para baselines)
- Análisis de amenazas específicas del negocio

### 2.2 Fases

#### Fase 1: Reconocimiento y Planificación
- Recopilación de requisitos
- Asset discovery
- Mapeo de arquitectura
- Definición de escenarios de riesgo

#### Fase 2: Enumeración y Análisis
- Identificación de servicios y versiones
- Análisis de configuración
- Evaluación de controles
- Detección de patrones inseguros

#### Fase 3: Validación de Hallazgos
- Pruebas de explotabilidad (donde aplicable)
- Confirmación de riesgos
- Evaluación de impacto
- Valoración de severidad

#### Fase 4: Documentación y Recomendación
- Clasificación según CVSS v3.1
- Elaboración de recomendaciones prácticas
- Estimación de esfuerzo de remediación
- Priorización

### 2.3 Herramientas Utilizadas
- Auditoría HTTP (http_surface_audit.py)
- Análisis documental (check_integrity.py)
- Normalización de hallazgos (normalize_findings.py)
- Herramientas manuales y custom per evaluación

---

## 3. Hallazgos

### 3.1 Hallazgos Críticos

> Afectan directamente la confidencialidad, integridad o disponibilidad de sistemas.
> Requieren remediación inmediata.

#### HALL-XXX-001: [Título del hallazgo crítico]

**Severidad**: CRÍTICA  
**Componente**: [Sistema/Aplicación]  
**CVSS**: 9.0 | Esfuerzo Remediación: 7/10  
**CWE**: CWE-XXX

**Descripción**:
Descripción técnica detallada del problema identificado.

**Evidencia**:
- Prueba 1: [Captura/salida específica]
- Prueba 2: [Pasos de reproducción]
- Impacto Demostrado: [Qué se puede lograr]

**Recomendación**:
Acciones específicas para remediar:
1. Paso 1
2. Paso 2
3. Validación de remediación

**Referencias**:
- https://owasp.org/...
- CWE-XXX: [Descripción]

---

### 3.2 Hallazgos Altos

#### HALL-XXX-002: [Título]

**Severidad**: ALTA  
**Componente**: [Sistema]  
**Esfuerzo Remediación**: 5/10  

**Descripción**: [Descripción técnica]

**Evidencia**: [Pruebas específicas]

**Recomendación**: [Pasos concretos]

---

### 3.3 Hallazgos Medios

#### HALL-XXX-003: [Título]

**Severidad**: MEDIA  
**Componente**: [Sistema]  
**Esfuerzo Remediación**: 3/10  

**Descripción**: [Descripción técnica]

**Recomendación**: [Acciones sugeridas]

---

### 3.4 Hallazgos Bajos e Informativos

#### HALL-XXX-004: [Título]
- **BAJA**: [Descripción breve]
- **Recomendación**: [Mejora sugerida]

#### HALL-XXX-005: [Título]
- **INFORMATIVO**: [Observación no urgente]

---

## 4. Riesgo Agregado

### 4.1 Matriz de Riesgo

| Severidad | # | Esfuerzo Promedio | Riesgo Residual |
|-----------|---|-------------------|-----------------|
| Críticos  | X | X/10              | Alto            |
| Altos     | X | X/10              | Medio-Alto      |
| Medios    | X | X/10              | Medio           |
| Bajos     | X | X/10              | Bajo            |

### 4.2 Timeline de Remediación Sugerida

```
Trimestre 1: Críticos + Altos (reducir riesgo máximo)
Trimestre 2: Medios + inicio de preventivos
Trimestre 3: Validación y pruebas de seguridad
Trimestre 4: Revisión y planificación para año siguiente
```

### 4.3 Factores de Riesgo

- **Madurez de controles**: [Estado actual]
- **Velocidad de evolución**: [Cambios frecuentes = mayor riesgo]
- **Dependencias críticas**: [Servicios/proveedores]
- **Amenazas históricas**: [Incidentes previos]

---

## 5. Recomendaciones Priorizadas

### 5.1 Corto Plazo (0-30 días)

1. **[Acción 1]** - Remedia HALL-XXX-001
   - Responsable: [Equipo]
   - Validación: [Prueba específica]
   - Riesgo residual: Bajo

2. **[Acción 2]** - Remedia HALL-XXX-002
   - Responsable: [Equipo]
   - Validación: [Cómo verificar]

### 5.2 Mediano Plazo (1-3 meses)

- [Iniciativa 1]
- [Iniciativa 2]
- [Mejora de proceso]

### 5.3 Largo Plazo (3-12 meses)

- [Transformación de arquitectura si aplica]
- [Programa de seguridad proactiva]
- [Mejora continua]

---

## 6. Plan de Revalidación

### 6.1 Cronograma

- **Evaluación de Corte**: {date_generated}
- **Primera Revalidación**: [Fecha + 90 días]
- **Segunda Revalidación**: [Fecha + 180 días]
- **Evaluación Completa**: [Fecha + 365 días]

### 6.2 Criterios de Éxito

✓ Todos los hallazgos críticos remediados y validados  
✓ 80%+ de hallazgos altos remediados  
✓ Pruebas de penetración complementarias (si aplica)  
✓ Revisión de cambios de arquitectura  

### 6.3 Punto de Contacto

- **Evaluador**: [Nombre/Equipo]
- **Cliente**: [Contacto]
- **Frecuencia de Sync**: Quincenal/Mensual

---

## 7. Evidencia Técnica y Anexos

### 7.1 Logs de Evaluación

```
[Salidas de herramientas, timestamps, comandos ejecutados]
```

### 7.2 Capturas y Datos

[Agregar evidencia visual/datos específicos]

### 7.3 Referencias de Inteligencia

- Amenazas conocidas en sector
- Cambios recientes en OWASP Top 10
- Vulnerabilidades de día cero que aplican

---

## Conclusión

La evaluación fue completada de acuerdo a los términos acordados.
Los hallazgos reflejan el estado de seguridad actual del sistema.

**Recomendación Ejecutiva**: 
Proceder con remediación de hallazgos críticos y altos según cronograma establecido.
Implementar programa de revisiones periódicas basado en Risk-Based Security Testing.

---

**Documento**: Reporte ORION-HACKING  
**Clasificación**: Confidencial  
**Fecha**: {date_generated}  
**Versión**: 1.0  

"""


def main() -> int:
    """Genera plantilla de reporte."""
    if len(sys.argv) != 2:
        print("Uso: report_skeleton.py <salida.md>")
        print("Ejemplo: report_skeleton.py reporte-evaluacion.md")
        return 1
    
    output_file = sys.argv[1]
    date_generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Substituye variables de fecha
    template_content = TEMPLATE.format(date_generated=date_generated)
    
    try:
        with open(output_file, "w", encoding="utf-8") as fh:
            fh.write(template_content)
        print(f"✓ Plantilla creada: {output_file}")
        print(f"✓ Abierta para edición. Reemplaza placeholders [así].")
        return 0
    except IOError as e:
        print(f"✗ Error al escribir archivo: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
