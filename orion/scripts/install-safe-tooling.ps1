#!/usr/bin/env powershell
<#
.SYNOPSIS
ORION-HACKING Safe Tooling Bootstrap para Windows
Instala herramientas seguras y auditables necesarias para evaluaciones de seguridad.

.DESCRIPTION
Script que facilita instalación controlada de herramientas de seguridad via WinGet.
Requiere revisión manual de cada paquete antes de instalación.
Soporta instalación selectiva o completa.

.PARAMETER SkipReview
Omite confirmación interactiva (úsalo solo después de validar)

.PARAMETER Category
Especifica categoría: 'all', 'core', 'network', 'web', 'osint'

.EXAMPLE
./install-safe-tooling.ps1
./install-safe-tooling.ps1 -Category core
./install-safe-tooling.ps1 -SkipReview

.NOTES
Autor: ORION-HACKING
Requiere: PowerShell 5.1+, WinGet instalado, acceso Admin
Política: Revisión manual de cada paquete, documentación de cambios
#>

[CmdletBinding()]
param(
    [switch]$SkipReview,
    [ValidateSet('all', 'core', 'network', 'web', 'osint')]
    [string]$Category = 'all'
)

$ErrorActionPreference = "Stop"

# Colores para salida
$StatusColor = @{
    'Success' = 'Green'
    'Warning' = 'Yellow'
    'Error'   = 'Red'
    'Info'    = 'Cyan'
}

# Definición de herramientas por categoría
$ToolCategories = @{
    'core' = @(
        @{name = 'Python.Python.3.12'; description = 'Lenguaje Python 3.12' },
        @{name = 'Git.Git'; description = 'Control de versiones distribuido' },
        @{name = 'Microsoft.VisualStudioCode'; description = 'Editor de código' }
    )
    'network' = @(
        @{name = 'WiresharkFoundation.Wireshark'; description = 'Análisis de tráfico de red' },
        @{name = 'Insecure.Nmap'; description = 'Scanner de puertos (host discovery)' },
        @{name = 'nmap:ncat'; description = 'Cliente/servidor TCP multipropósito' },
        @{name = 'tcpdump'; description = 'Captura de paquetes línea de comandos' }
    )
    'web' = @(
        @{name = 'Insecure.Burp-Suite-Community'; description = 'Proxy HTTP/HTTPS para testing' },
        @{name = 'zaproxy:zaproxy'; description = 'OWASP ZAP - Scanner web automático' },
        @{name = 'postman:postman'; description = 'Cliente API y testing' }
    )
    'osint' = @(
        @{name = 'amass:amass'; description = 'Enumeración de subdominios y asset discovery' },
        @{name = 'shodan:shodan-cli'; description = 'Cliente CLI de Shodan' }
    )
}

# Herramientas recomendadas adicionales (información)
$AdditionalTools = @(
    @{source = 'chocolatey'; name = 'hashcat'; description = 'Acelerador de password cracking' },
    @{source = 'chocolatey'; name = 'dngrecon'; description = 'Enumeración de DNS' }
)

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "=" * 60
}

function Write-Status {
    param(
        [string]$Message,
        [string]$Type = 'Info'
    )
    $Color = $StatusColor[$Type]
    Write-Host "[$Type]" -ForegroundColor $Color -NoNewline
    Write-Host " $Message"
}

function Confirm-AdminRole {
    $IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]'Administrator')
    
    if (-not $IsAdmin) {
        Write-Status "Este script requiere permisos de Administrador" 'Error'
        Write-Status "Por favor, ejecuta PowerShell como Administrador" 'Error'
        return $false
    }
    return $true
}

function Test-WinGet {
    try {
        $version = winget --version 2>&1
        Write-Status "WinGet encontrado: $version" 'Success'
        return $true
    } catch {
        Write-Status "WinGet no está instalado o no está accesible" 'Error'
        return $false
    }
}

function Show-ToolInfo {
    param(
        [array]$Tools,
        [string]$CategoryName
    )
    
    Write-Host ""
    Write-Host "Herramientas de categoría: $CategoryName" -ForegroundColor Magenta
    Write-Host "-" * 60
    
    foreach ($tool in $Tools) {
        Write-Host "  • " -ForegroundColor Green -NoNewline
        Write-Host "$($tool.name)" -ForegroundColor Yellow -NoNewline
        Write-Host " - $($tool.description)" -ForegroundColor DarkGray
    }
}

function Get-ToolsToInstall {
    $toolsToInstall = @()
    
    if ($Category -eq 'all') {
        foreach ($cat in $ToolCategories.Keys) {
            $toolsToInstall += $ToolCategories[$cat]
        }
    } else {
        $toolsToInstall = $ToolCategories[$Category]
    }
    
    return $toolsToInstall
}

function Show-ReviewPrompt {
    param(
        [array]$Tools
    )
    
    Write-Header "REVISIÓN DE PAQUETES ANTES DE INSTALAR"
    
    Write-Host ""
    Write-Host "Se procede a instalar los siguientes paquetes:" -ForegroundColor Yellow
    Write-Host ""
    
    $count = 1
    foreach ($tool in $Tools) {
        Write-Host "$count. $($tool.name)" -ForegroundColor Cyan
        Write-Host "   Descripción: $($tool.description)" -ForegroundColor DarkGray
        Write-Host ""
        $count++
    }
    
    Write-Status "IMPORTANTE: Revisa cada paquete, su fuente y propósito" 'Warning'
    Write-Status "Asegúrate de que confías en cada herramienta antes de instalarla" 'Warning'
    Write-Host ""
    
    $response = Read-Host "¿Deseas continuar? (si/no)"
    return ($response -eq 'si' -or $response -eq 's')
}

function Install-Tool {
    param(
        [string]$ToolName,
        [int]$Index,
        [int]$Total
    )
    
    try {
        Write-Status "[$Index/$Total] Instalando $ToolName..." 'Info'
        
        $output = winget install --id $ToolName --accept-package-agreements --accept-source-agreements -q | Out-String
        
        if ($LASTEXITCODE -eq 0) {
            Write-Status "[$Index/$Total] ✓ $ToolName instalado exitosamente" 'Success'
            return $true
        } else {
            Write-Status "[$Index/$Total] ✗ Error instalando $ToolName (código: $LASTEXITCODE)" 'Error'
            return $false
        }
    } catch {
        Write-Status "[$Index/$Total] ✗ Excepción: $_" 'Error'
        return $false
    }
}

function Show-Summary {
    param(
        [int]$Successful,
        [int]$Failed,
        [int]$Total
    )
    
    Write-Header "RESUMEN DE INSTALACIÓN"
    
    Write-Host "Total de herramientas procesadas: $Total"
    Write-Host "Instaladas correctamente: " -NoNewline
    Write-Host "$Successful" -ForegroundColor Green
    Write-Host "Errores: " -NoNewline
    if ($Failed -gt 0) {
        Write-Host "$Failed" -ForegroundColor Red
    } else {
        Write-Host "$Failed" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Status "Próximos pasos:" 'Info'
    Write-Host "  1. Verifica que las herramientas estén correctamente instaladas"
    Write-Host "  2. Consulta la documentación de cada herramienta"
    Write-Host "  3. Configura permisos de firewall si es necesario"
    Write-Host "  4. Registra los cambios en tu sistema"
    
    Write-Host ""
    Write-Status "Herramientas adicionales (instalación manual recomendada):" 'Info'
    foreach ($tool in $AdditionalTools) {
        Write-Host "  • $($tool.source):$($tool.name) - $($tool.description)" -ForegroundColor DarkGray
    }
}

function Main {
    Write-Header "ORION-HACKING Safe Tooling Bootstrap"
    Write-Host "Instalación controlada y auditada de herramientas de seguridad"
    Write-Host ""
    
    # 1. Verifica permisos
    if (-not (Confirm-AdminRole)) {
        exit 1
    }
    Write-Status "✓ Acceso de Administrador confirmado" 'Success'
    
    # 2. Verifica WinGet
    if (-not (Test-WinGet)) {
        exit 1
    }
    
    # 3. Obtiene herramientas según categoría
    $tools = Get-ToolsToInstall
    
    if (-not $tools -or $tools.Count -eq 0) {
        Write-Status "No hay herramientas para instalar en la categoría: $Category" 'Warning'
        exit 0
    }
    
    # 4. Muestra información
    Write-Status "Herramientas seleccionadas para instalar ($($tools.Count))" 'Info'
    foreach ($category in $ToolCategories.Keys) {
        if ($Category -eq 'all' -or $Category -eq $category) {
            Show-ToolInfo -Tools $ToolCategories[$category] -CategoryName $category
        }
    }
    
    # 5. Pide confirmación (excepto si -SkipReview)
    if (-not $SkipReview) {
        if (-not (Show-ReviewPrompt -Tools $tools)) {
            Write-Status "Instalación cancelada por usuario" 'Warning'
            exit 0
        }
    } else {
        Write-Status "Omitiendo revisión interactiva (-SkipReview)" 'Warning'
    }
    
    # 6. Instala herramientas
    Write-Header "INICIANDO INSTALACIÓN"
    
    $successful = 0
    $failed = 0
    
    foreach ($tool in $tools) {
        if (Install-Tool -ToolName $tool.name -Index ($successful + $failed + 1) -Total $tools.Count) {
            $successful++
        } else {
            $failed++
        }
    }
    
    # 7. Muestra resumen
    Show-Summary -Successful $successful -Failed $failed -Total $tools.Count
    
    # Retorna código de salida apropiado
    exit ($failed -gt 0 ? 1 : 0)
}

# Punto de entrada
Main
