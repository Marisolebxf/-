# update-task-status.ps1
# Cross-platform entry (Windows): update task-registry + optional Feishu sync (soft-fail)
# Requires: Node 18+
#
# Usage:
#   .\scripts\update-task-status.ps1 -TaskId ENT-X -Status review
#   .\scripts\update-task-status.ps1 -TaskId ENT-X -Status claimed -ClaimedBy "human:孔东" -SupervisedBy "human:孔东"
#   .\scripts\update-task-status.ps1 -TaskId ENT-X -Heartbeat
#   .\scripts\update-task-status.ps1 -TaskId ENT-X -Status review -NoSync

param(
    [Parameter(Mandatory = $true)][string]$TaskId,
    [string]$Status = '',
    [string]$ClaimedBy = '',
    [string]$SupervisedBy = '',
    [string]$BlockedBy = '',
    [string]$Evidence = '',
    [switch]$Heartbeat,
    [switch]$NoSync,
    [switch]$DryRun,
    [int]$LockHours = 2
)

$ErrorActionPreference = 'Stop'
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    throw "Node.js 18+ required (not found on PATH). WSL is NOT required."
}

$script = Join-Path $PSScriptRoot 'lib\board-task-status.mjs'
$argsList = @($script, '--task-id', $TaskId)
if ($Status) { $argsList += @('--status', $Status) }
if ($ClaimedBy) { $argsList += @('--claimed-by', $ClaimedBy) }
if ($SupervisedBy) { $argsList += @('--supervised-by', $SupervisedBy) }
if ($BlockedBy) { $argsList += @('--blocked-by', $BlockedBy) }
if ($Evidence) { $argsList += @('--evidence', $Evidence) }
if ($Heartbeat) { $argsList += '--heartbeat' }
if ($NoSync) { $argsList += '--no-sync' } else { $argsList += '--sync-board' }
if ($DryRun) { $argsList += '--dry-run' }
if ($LockHours -ne 2) { $argsList += @('--lock-hours', "$LockHours") }

& node @argsList
exit $LASTEXITCODE
