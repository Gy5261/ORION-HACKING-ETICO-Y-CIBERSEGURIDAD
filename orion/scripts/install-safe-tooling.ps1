#requires -Version 7.0
<#
.SYNOPSIS
Operator-controlled, conservative Windows tooling installer.
.DESCRIPTION
Shows a deterministic plan by default, without network or system changes.
With -Apply and -AcceptAgreements, verifies exact WinGet package IDs before
installation. A repository list does not prove that a package exists.
.EXAMPLE
./install-safe-tooling.ps1 -Category core
./install-safe-tooling.ps1 -Category core -Apply -AcceptAgreements
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [ValidateSet('all', 'core', 'network', 'web', 'osint')]
    [string]$Category = 'core',
    [switch]$Apply,
    [switch]$AcceptAgreements
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Catalog = @(
    [pscustomobject]@{ Category = 'core'; Id = 'Python.Python.3.15'; Purpose = 'Python 3.15 estable' },
    [pscustomobject]@{ Category = 'core'; Id = 'Git.Git'; Purpose = 'Control de versiones' },
    [pscustomobject]@{ Category = 'core'; Id = 'Microsoft.PowerShell'; Purpose = 'PowerShell 7' },
    [pscustomobject]@{ Category = 'core'; Id = 'Microsoft.VisualStudioCode'; Purpose = 'Editor de codigo' },
    [pscustomobject]@{ Category = 'network'; Id = 'Insecure.Nmap'; Purpose = 'Inventario de redes autorizadas' },
    [pscustomobject]@{ Category = 'network'; Id = 'WiresharkFoundation.Wireshark'; Purpose = 'Analisis local de trafico' }
)

$Selected = @($Catalog | Where-Object { $Category -eq 'all' -or $_.Category -eq $Category } |
              Sort-Object -Property Category, Id)
$Plan = [ordered]@{
    component = 'ORION controlled tooling bootstrap'
    os = 'Windows'
    mode = if ($Apply) { 'apply' } else { 'plan' }
    selected_category = $Category
    contact_network = [bool]$Apply
    package_count = $Selected.Count
    packages = @($Selected)
    warning = 'Validar procedencia, licencias y alcance antes de instalar.'
}

if (-not $Apply) {
    $Plan | ConvertTo-Json -Depth 6
    exit 0
}

if ($Selected.Count -eq 0) {
    throw "No hay identificadores WinGet comprobados para la categoria '$Category'."
}
if (-not $AcceptAgreements) {
    throw 'Para ejecutar instalaciones, especifique -Apply -AcceptAgreements explicitamente.'
}
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw 'WinGet no esta disponible. Instale o repare App Installer y compruebe winget --version.'
}

$Results = New-Object System.Collections.Generic.List[object]
foreach ($Package in $Selected) {
    $Destination = "$($Package.Id) desde la fuente winget"
    if (-not $PSCmdlet.ShouldProcess($Destination, 'Validar e instalar')) {
        $Results.Add([pscustomobject]@{ id = $Package.Id; status = 'not_applied' })
        continue
    }
    # Exact-ID resolution protects against typos and unsupported package names.
    & winget show --exact --id $Package.Id --source winget --accept-source-agreements |
        Out-Null
    if ($LASTEXITCODE -ne 0) {
        $Results.Add([pscustomobject]@{ id = $Package.Id; status = 'not_found'; exit_code = $LASTEXITCODE })
        continue
    }
    & winget install --exact --id $Package.Id --source winget --silent --accept-source-agreements --accept-package-agreements --disable-interactivity |
        Out-Null
    if ($LASTEXITCODE -ne 0) {
        $Results.Add([pscustomobject]@{ id = $Package.Id; status = 'failed'; exit_code = $LASTEXITCODE })
        continue
    }
    $Results.Add([pscustomobject]@{ id = $Package.Id; status = 'installer_returned_success' })
}

$Output = [ordered]@{
    ok = (@($Results | Where-Object { $_.status -in @('failed', 'not_found') }).Count -eq 0)
    verification = 'WinGet exit codes only; runtime installation must be inspected separately'
    results = @($Results)
}
$Output | ConvertTo-Json -Depth 5
if (-not $Output.ok) { exit 1 }
