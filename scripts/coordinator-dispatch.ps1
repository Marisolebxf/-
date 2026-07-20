# coordinator-dispatch.ps1 — 自动派单 CLI 入口（Windows）
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('scan', 'list', 'confirm', 'ready-engine')]
    [string]$Command,
    [string]$CauseTask = '',
    [switch]$All,
    [string]$Ids = '',
    [Parameter(Mandatory = $false)]
    [string]$ApprovedBy = '',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$orch = Split-Path $here -Parent
$mjs = Join-Path $here 'coordinator-dispatch.mjs'

$args = @($Command)
if ($CauseTask) { $args += @('--cause-task', $CauseTask) }
if ($All) { $args += '--all' }
if ($Ids) { $args += @('--ids', $Ids) }
if ($ApprovedBy) { $args += @('--approved-by', $ApprovedBy) }
if ($DryRun) { $args += '--dry-run' }

Push-Location $orch
try {
    & node $mjs @args
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
