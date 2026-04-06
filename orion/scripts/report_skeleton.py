#!/usr/bin/env python3
"""
report_skeleton.py - Genera plantilla de reporte de evaluaciÃ³n de seguridad.

Crea esqueleto automatizado de reporte Markdown con secciones estÃ¡ndar
para evaluaciones de seguridad autorizadas, pentesting Ã©tico y auditorÃ­as.

Uso:
    python3 report_skeleton.py <salida.md>
    python3 report_skeleton.py reporte-cliente-2024.md

Secciones generadas:
- InformaciÃ³n ejecutiva
- Alcance y limitaciones
- MetodologÃ­a
- Hallazgos clasificados por severidad
- Riesggo agregado
- Recomendaciones priorizadas
- Plan de revalidaciÃ³n
- Evidencia y anexos

La plantilla estÃ¡ formateada para Markdown y lista para editar.
"""

import sys
from datetime import datetime


TEMPLATE = """# Reporte de EvaluaciÃ³n de Seguridad - ORION-HACKING

**InformaciÃ³n Confidencial**

---

## Resumen Ejecutivo

### PropÃ³sito
EvaluaciÃ³n estructurada de seguridad enfocada en riesgos identificables y remediaciÃ³n prÃ¡ctica.

### Alcance
- **Objetivos**: [Describir quÃ© se evaluÃ³]
- **Sistemas**: [Listar sistemas/dominios particulares]
- **Fechas**: {date_generated}
- **Evaluador**: ORION-HACKING Security Team
- **AutorizaciÃ³n**: [Documento/referencia de autorizaciÃ³n]

### UbicaciÃ³n Ejecutiva
- **Total Hallazgos**: [#]
  - CrÃ­ticos: [#]
  - Altos: [#]
  - Medios: [#]
  - Bajos: [#]
- **Riesgo Agregado**: [Muy Alto | Alto | Medio | Bajo]
- **Estado**: [En Progreso | Completado]

---

## 1. Alcance y Limitaciones

### 1.1 Alcance de la EvaluaciÃ³n

#### Incluido
- [Sistema o componente 1]
- [Sistema o componente 2]
- [Dominios de evaluaciÃ³n especÃ­ficos]

#### Excluido
- [Sistemas/componentes fuera de alcance]
- [Razones tÃ©cnicas o de negocio]

### 1.2 Limitaciones

- **TÃ©cnicas**: [Restricciones de herramientas, acceso]
- **Temporales**: [PerÃ­odo de evaluaciÃ³n]
- **Documentales**: [InformaciÃ³n disponible]
- **Operacionales**: [Restricciones de downtime, ventanas]

### 1.3 Disclaimers

Esta evaluaciÃ³n representa el estado de seguridad en la fecha de evaluaciÃ³n.
Cambios posteriores o configuraciones no revisadas pueden afectar los hallazgos.

---

## 2. MetodologÃ­a

### 2.1 Enfoque
Se utilizÃ³ metodologÃ­a basada en:
- OWASP Testing Guide (para aplicaciones web)
- NIST Cybersecurity Framework (para gobernanza)
- CIS Controls v8 (para baselines)
- AnÃ¡lisis de amenazas especÃ­ficas del negocio

### 2.2 Fases

#### Fase 1: Reconocimiento y PlanificaciÃ³n
- RecopilaciÃ³n de requisitos
- Asset discovery
- Mapeo de arquitectura
- DefiniciÃ³n de escenarios de riesgo

#### Fase 2: EnumeraciÃ³n y AnÃ¡lisis
- IdentificaciÃ³n de servicios y versiones
- AnÃ¡lisis de configuraciÃ³n
- EvaluaciÃ³n de controles
- DetecciÃ³n de patrones inseguros

#### Fase 3: ValidaciÃ³n de Hallazgos
- Pruebas de explotabilidad (donde aplicable)
- ConfirmaciÃ³n de riesgos
- EvaluaciÃ³n de impacto
- ValoraciÃ³n de severidad

#### Fase 4: DocumentaciÃ³n y RecomendaciÃ³n
- ClasificaciÃ³n segÃºn CVSS v3.1
- ElaboraciÃ³n de recomendaciones prÃ¡cticas
- EstimaciÃ³n de esfuerzo de remediaciÃ³n
- PriorizaciÃ³n

### 2.3 Herramientas Utilizadas
- AuditorÃ­a HTTP (http_surface_audit.py)
- AnÃ¡lisis documental (check_integrity.py)
- NormalizaciÃ³n de hallazgos (normalize_findings.py)
- Herramientas manuales y custom per evaluaciÃ³n

---

## 3. Hallazgos

### 3.1 Hallazgos CrÃ­ticos

> Afectan directamente la confidencialidad, integridad o disponibilidad de sistemas.
> Requieren remediaciÃ³n inmediata.

#### HALL-XXX-001: [TÃ­tulo del hallazgo crÃ­tico]

**Severidad**: CRÃTICA  
**Componente**: [Sistema/AplicaciÃ³n]  
**CVSS**: 9.0 | Esfuerzo RemediaciÃ³n: 7/10  
**CWE**: CWE-XXX

**DescripciÃ³n**:
DescripciÃ³n tÃ©cnica detallada del problema identificado.

**Evidencia**:
- Prueba 1: [Captura/salida especÃ­fica]
- Prueba 2: [Pasos de reproducciÃ³n]
- Impacto Demostrado: [QuÃ© se puede lograr]

**RecomendaciÃ³n**:
Acciones especÃ­ficas para remediar:
1. Paso 1
2. Paso 2
3. ValidaciÃ³n de remediaciÃ³n

**Referencias**:
- https://owasp.org/...
- CWE-XXX: [DescripciÃ³n]

---

### 3.2 Hallazgos Altos

#### HALL-XXX-002: [TÃ­tulo]

**Severidad**: ALTA  
**Componente**: [Sistema]  
**Esfuerzo RemediaciÃ³n**: 5/10  

**DescripciÃ³n**: [DescripciÃ³n tÃ©cnica]

**Evidencia**: [Pruebas especÃ­ficas]

**RecomendaciÃ³n**: [Pasos concretos]

---

### 3.3 Hallazgos Medios

#### HALL-XXX-003: [TÃ­tulo]

**Severidad**: MEDIA  
**Componente**: [Sistema]  
**Esfuerzo RemediaciÃ³n**: 3/10  

**DescripciÃ³n**: [DescripciÃ³n tÃ©cnica]

**RecomendaciÃ³n**: [Acciones sugeridas]

---

### 3.4 Hallazgos Bajos e Informativos

#### HALL-XXX-004: [TÃ­tulo]
- **BAJA**: [DescripciÃ³n breve]
- **RecomendaciÃ³n**: [Mejora sugerida]

#### HALL-XXX-005: [TÃ­tulo]
- **INFORMATIVO**: [ObservaciÃ³n no urgente]

---

## 4. Riesgo Agregado

### 4.1 Matriz de Riesgo

| Severidad | # | Esfuerzo Promedio | Riesgo Residual |
|-----------|---|-------------------|-----------------|
| CrÃ­ticos  | X | X/10              | Alto            |
| Altos     | X | X/10              | Medio-Alto      |
| Medios    | X | X/10              | Medio           |
| Bajos     | X | X/10              | Bajo            |

### 4.2 Timeline de RemediaciÃ³n Sugerida

```
Trimestre 1: CrÃ­ticos + Altos (reducir riesgo mÃ¡ximo)
Trimestre 2: Medios + inicio de preventivos
Trimestre 3: ValidaciÃ³n y pruebas de seguridad
Trimestre 4: RevisiÃ³n y planificaciÃ³n para aÃ±o siguiente
```

### 4.3 Factores de Riesgo

- **Madurez de controles**: [Estado actual]
- **Velocidad de evoluciÃ³n**: [Cambios frecuentes = mayor riesgo]
- **Dependencias crÃ­ticas**: [Servicios/proveedores]
- **Amenazas histÃ³ricas**: [Incidentes previos]

---

## 5. Recomendaciones Priorizadas

### 5.1 Corto Plazo (0-30 dÃ­as)

1. **[AcciÃ³n 1]** - Remedia HALL-XXX-001
   - Responsable: [Equipo]
   - ValidaciÃ³n: [Prueba especÃ­fica]
   - Riesgo residual: Bajo

2. **[AcciÃ³n 2]** - Remedia HALL-XXX-002
   - Responsable: [Equipo]
   - ValidaciÃ³n: [CÃ³mo verificar]

### 5.2 Mediano Plazo (1-3 meses)

- [Iniciativa 1]
- [Iniciativa 2]
- [Mejora de proceso]

### 5.3 Largo Plazo (3-12 meses)

- [TransformaciÃ³n de arquitectura si aplica]
- [Programa de seguridad proactiva]
- [Mejora continua]

---

## 6. Plan de RevalidaciÃ³n

### 6.1 Cronograma

- **EvaluaciÃ³n de Corte**: {date_generated}
- **Primera RevalidaciÃ³n**: [Fecha + 90 dÃ­as]
- **Segunda RevalidaciÃ³n**: [Fecha + 180 dÃ­as]
- **EvaluaciÃ³n Completa**: [Fecha + 365 dÃ­as]

### 6.2 Criterios de Ã‰xito

âœ“ Todos los hallazgos crÃ­ticos remediados y validados  
âœ“ 80%+ de hallazgos altos remediados  
âœ“ Pruebas de penetraciÃ³n complementarias (si aplica)  
âœ“ RevisiÃ³n de cambios de arquitectura  

### 6.3 Punto de Contacto

- **Evaluador**: [Nombre/Equipo]
- **Cliente**: [Contacto]
- **Frecuencia de Sync**: Quincenal/Mensual

---

## 7. Evidencia TÃ©cnica y Anexos

### 7.1 Logs de EvaluaciÃ³n

```
[Salidas de herramientas, timestamps, comandos ejecutados]
```

### 7.2 Capturas y Datos

[Agregar evidencia visual/datos especÃ­ficos]

### 7.3 Referencias de Inteligencia

- Amenazas conocidas en sector
- Cambios recientes en OWASP Top 10
- Vulnerabilidades de dÃ­a cero que aplican

---

## ConclusiÃ³n

La evaluaciÃ³n fue completada de acuerdo a los tÃ©rminos acordados.
Los hallazgos reflejan el estado de seguridad actual del sistema.

**RecomendaciÃ³n Ejecutiva**: 
Proceder con remediaciÃ³n de hallazgos crÃ­ticos y altos segÃºn cronograma establecido.
Implementar programa de revisiones periÃ³dicas basado en Risk-Based Security Testing.

---

**Documento**: Reporte ORION-HACKING  
**ClasificaciÃ³n**: Confidencial  
**Fecha**: {date_generated}  
**VersiÃ³n**: 1.0  

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
        print(f"[OK] Plantilla creada: {output_file}")
        print("[OK] Abierta para edicion. Reemplaza placeholders [asi].")
        return 0
    except IOError as e:
        print(f"[ERROR] Error al escribir archivo: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
