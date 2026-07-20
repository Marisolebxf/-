# board-sync-watch.ps1
# Projector machine (Windows, always-on): git pull 主仓 → Feishu sync → commit/push task-registry.
# Default interval: 1 hour (see register-board-sync-watch.ps1).
#
# 看板字段真源：飞书最新状态（status/认领/Sprint/优先级/标题）；监管人 registry → 飞书。
# 双向默认 -FeishuAuthoritative：inbound 吸收飞书 → outbound 不覆盖看板字段（监管人除外）。
# Sprint 过滤读 agent-delivery/scrum-sprint.yaml#current_sprint；Step 2c 仍会 CREATE 缺 record_id 的任务。
# 改状态请用 update-task-status（同时写 YAML + 飞书）；禁止只改 YAML 指望 watch 盖板。
#
# Usage:
#   .\scripts\board-sync-watch.ps1
#   .\scripts\board-sync-watch.ps1 -OutboundOnly
#   .\scripts\board-sync-watch.ps1 -DryRun
#   .\scripts\board-sync-watch.ps1 -NoGitPush
#   .\scripts\board-sync-watch.ps1 -NoFeishuAuthoritative   # 站会全量投影（YAML→飞书含状态）

param(
    [switch]$OutboundOnly,
    [switch]$DryRun,
    [switch]$NoGitPush,
    [string]$SprintId = '',
    [switch]$NoFeishuAuthoritative
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

$feishuAuth = -not [bool]$NoFeishuAuthoritative
Write-Log "board-sync-watch start sprint=$SprintId outboundOnly=$OutboundOnly dryRun=$DryRun noGitPush=$NoGitPush feishuAuthoritative=$feishuAuth"

try {
    if (-not (Invoke-OrchGitPull)) {
        exit 1
    }

    if (-not $OutboundOnly) {
        if ($DryRun) {
            if ($feishuAuth) {
                & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun -SprintId $SprintId -FeishuAuthoritative
            }
            else {
                & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun -SprintId $SprintId
            }
        }
        else {
            if ($feishuAuth) {
                & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun:$false -SprintId $SprintId -FeishuAuthoritative
            }
            else {
                & (Join-Path $here 'sync-feishu-bitable-bidirectional.ps1') -DryRun:$false -SprintId $SprintId
            }
        }
    }
    else {
        # OutboundOnly：默认仍跳过看板字段，避免 YAML 旧状态盖飞书
        if ($feishuAuth) {
            Write-Log 'OutboundOnly + FeishuAuthoritative: SkipKanbanFields outbound'
            if ($DryRun) {
                & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun -SprintId $SprintId -SkipKanbanFields
            }
            else {
                & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun:$false -SprintId $SprintId -SkipKanbanFields
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
