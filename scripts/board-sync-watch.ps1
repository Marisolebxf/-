# board-sync-watch.ps1
# Projector machine (Windows, always-on): git pull 主仓 → Feishu outbound → commit/push task-registry.
# Default interval: 1 hour (see register-board-sync-watch.ps1).
#
# 2026-07-28：飞书 = 纯看板。默认不做 inbound（飞书改动不回写 registry）；
# outbound 全量投影 registry→飞书（含状态/认领）。改状态请用 update-task-status。
# 逃生阀：-AllowInbound 恢复旧双向（不推荐）。
#
# Usage:
#   .\scripts\board-sync-watch.ps1
#   .\scripts\board-sync-watch.ps1 -OutboundOnly
#   .\scripts\board-sync-watch.ps1 -DryRun
#   .\scripts\board-sync-watch.ps1 -NoGitPush
#   .\scripts\board-sync-watch.ps1 -AllowInbound   # 旧行为：飞书→registry（已不推荐）

param(
    [switch]$OutboundOnly,
    [switch]$DryRun,
    [switch]$NoGitPush,
    [string]$SprintId = '',
    [switch]$AllowInbound
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

function Invoke-OrchGitPull {
    # Prerequisite: sync must run on latest main-orch registry to avoid overwrite/conflict.
    Set-Location $orch
    $branch = (git rev-parse --abbrev-ref HEAD 2>$null)
    if (-not $branch) {
        Write-Log 'ERROR: not a git repo; abort before Feishu sync'
        return $false
    }
    Write-Log "git pull --rebase origin $branch (before Feishu sync)"
    if ($DryRun) {
        Write-Log "[DRY] would git pull --rebase origin $branch"
        return $true
    }

    $didStash = $false
    $dirty = git status --porcelain 2>$null
    if ($dirty) {
        Write-Log 'local changes detected; stash before pull'
        git stash push -m "board-sync-watch: auto-stash before pull $(Get-Date -Format o)" 2>&1 | ForEach-Object { Write-Log "stash: $_" }
        if ($LASTEXITCODE -ne 0) {
            Write-Log 'ERROR: git stash failed; abort Feishu sync'
            return $false
        }
        $didStash = $true
    }

    git fetch origin 2>&1 | ForEach-Object { Write-Log "fetch: $_" }
    git pull --rebase origin $branch 2>&1 | ForEach-Object { Write-Log "pull: $_" }
    $pullOk = ($LASTEXITCODE -eq 0)

    if ($didStash) {
        Write-Log 'restore stash after pull'
        git stash pop 2>&1 | ForEach-Object { Write-Log "stash-pop: $_" }
        if ($LASTEXITCODE -ne 0) {
            Write-Log 'WARN: stash pop failed (conflict?); keep stash on stack, check git stash list'
        }
    }

    if (-not $pullOk) {
        Write-Log 'ERROR: git pull --rebase failed; abort Feishu sync'
        return $false
    }
    Write-Log "git pull ok on $branch"
    return $true
}

if (-not $SprintId) {
    $scrum = Get-Content (Join-Path $orch 'agent-delivery\scrum-sprint.yaml') -Raw -Encoding UTF8
    if ($scrum -match '(?m)^\s*current_sprint:\s*"?([^"\r\n]+)"?') {
        $SprintId = $Matches[1].Trim()
    }
}

$feishuAuth = $false   # 纯看板：outbound 覆盖飞书展示列
$skipInbound = -not [bool]$AllowInbound
Write-Log "board-sync-watch start sprint=$SprintId outboundOnly=$OutboundOnly dryRun=$DryRun noGitPush=$NoGitPush allowInbound=$AllowInbound skipInbound=$skipInbound"

try {
    if (-not (Invoke-OrchGitPull)) {
        exit 1
    }

    if (-not $OutboundOnly -and -not $skipInbound) {
        if ($DryRun) {
            & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun -SprintId $SprintId
        }
        else {
            & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun:$false -SprintId $SprintId
        }
    }
    else {
        # 默认：仅 outbound，全量投影看板字段（registry → 飞书）
        Write-Log 'Outbound: full kanban fields from registry (display-only Feishu)'
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

    # coordinator 自动派单：扫描 done 触发 + 门3 auto-ready
    $node = Get-Command node -ErrorAction SilentlyContinue
    if ($node -and -not $DryRun) {
        $dispatchMjs = Join-Path $here 'coordinator-dispatch.mjs'
        if (Test-Path $dispatchMjs) {
            Write-Log 'coordinator-dispatch scan (post-sync)'
            $scanArgs = @($dispatchMjs, 'scan')
            & node @scanArgs 2>&1 | ForEach-Object { Write-Log "dispatch: $_" }
        }
    }

    Write-Log "board-sync-watch ok"
    exit 0
}
catch {
    Write-Log "board-sync-watch ERROR: $($_.Exception.Message)"
    exit 1
}
