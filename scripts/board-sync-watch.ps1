# board-sync-watch.ps1
# Projector machine (Windows, always-on): Feishu sync + commit/push task-registry.
# Default interval: 1 hour (see register-board-sync-watch.ps1).
#
# Usage:
#   .\scripts\board-sync-watch.ps1
#   .\scripts\board-sync-watch.ps1 -OutboundOnly
#   .\scripts\board-sync-watch.ps1 -DryRun
#   .\scripts\board-sync-watch.ps1 -NoGitPush

param(
    [switch]$OutboundOnly,
    [switch]$DryRun,
    [switch]$NoGitPush,
    [string]$SprintId = ''
)

$ErrorActionPreference = 'Continue'
$here = $PSScriptRoot
$orch = Split-Path $here -Parent
$logDir = Join-Path $orch 'agent-delivery\_tmp'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'board-sync-watch.log'

function Write-Log([string]$msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format 'o'), $msg
    Add-Content -Path $log -Value $line -Encoding UTF8
    Write-Host $line
}

if (-not $SprintId) {
    $scrum = Get-Content (Join-Path $orch 'agent-delivery\scrum-sprint.yaml') -Raw -Encoding UTF8
    if ($scrum -match '(?m)^\s*current_sprint:\s*"?([^"\r\n]+)"?') {
        $SprintId = $Matches[1].Trim()
    }
}

Write-Log "board-sync-watch start sprint=$SprintId outboundOnly=$OutboundOnly dryRun=$DryRun noGitPush=$NoGitPush"

try {
    if (-not $OutboundOnly) {
        if ($DryRun) {
            & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun -SprintId $SprintId
        }
        else {
            & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun:$false -SprintId $SprintId
        }
    }
    else {
        $node = Get-Command node -ErrorAction SilentlyContinue
        if ($node) {
            $mjs = Join-Path $here 'lib\board-task-status.mjs'
            $args = @($mjs, '--watch-outbound')
            if ($SprintId) { $args += @('--sprint-id', $SprintId) }
            if ($DryRun) { $args += '--dry-run' }
            & node @args
        }
        else {
            if ($DryRun) {
                & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun -SprintId $SprintId
            }
            else {
                & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun:$false -SprintId $SprintId
            }
        }
    }

    if (-not $NoGitPush) {
        Write-Log 'git-push-registry after Feishu sync'
        if ($DryRun) {
            & (Join-Path $here 'lib\git-push-registry.ps1') -DryRun
        }
        else {
            & (Join-Path $here 'lib\git-push-registry.ps1')
        }
    }
    else {
        Write-Log 'git push skipped (-NoGitPush)'
    }

    Write-Log "board-sync-watch ok"
    exit 0
}
catch {
    Write-Log "board-sync-watch ERROR: $($_.Exception.Message)"
    exit 1
}
