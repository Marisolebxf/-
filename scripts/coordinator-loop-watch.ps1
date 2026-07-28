# coordinator-loop-watch.ps1
# Projector / 本机长开机：git pull → coordinator-loop（Mayor 建议包）→ 可选 lease 回收后 push。
#
# 设计（B4 Path A light · A3）：
#   - 默认只出建议，不 confirm、不开 Cursor agent
#   - 默认不 --apply-leases（避免无人时改 registry）；需要时显式 -ApplyLeases
#   - 与 board-sync-watch 职责分离：本脚本不做飞书 sync
#
# Usage:
#   .\scripts\coordinator-loop-watch.ps1
#   .\scripts\coordinator-loop-watch.ps1 -Limit 10
#   .\scripts\coordinator-loop-watch.ps1 -ApplyLeases          # 回收过期 claimed + 可 push
#   .\scripts\coordinator-loop-watch.ps1 -SkipScan
#   .\scripts\coordinator-loop-watch.ps1 -DryRun
#   .\scripts\coordinator-loop-watch.ps1 -NoGitPull
#   .\scripts\coordinator-loop-watch.ps1 -NoGitPush            # 即使 -ApplyLeases 也不 push

param(
    [int]$Limit = 8,
    [switch]$ApplyLeases,
    [switch]$SkipScan,
    [switch]$DryRun,
    [switch]$NoGitPull,
    [switch]$NoGitPush,
    [switch]$Json
)

$ErrorActionPreference = 'Continue'
$here = $PSScriptRoot
$orch = Split-Path $here -Parent
$logDir = Join-Path $orch 'agent-delivery\_tmp'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'coordinator-loop-watch.log'
$latest = Join-Path $logDir 'coordinator-loop-latest.txt'
$latestJson = Join-Path $logDir 'coordinator-loop-latest.json'

function Write-Log([string]$msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format 'o'), $msg
    Add-Content -Path $log -Value $line -Encoding UTF8
    Write-Host $line
}

function Invoke-OrchGitPull {
    Set-Location $orch
    $branch = (git rev-parse --abbrev-ref HEAD 2>$null)
    if (-not $branch) {
        Write-Log 'ERROR: not a git repo; abort'
        return $false
    }
    Write-Log "git pull --rebase origin $branch"
    if ($DryRun) {
        Write-Log "[DRY] would git pull --rebase origin $branch"
        return $true
    }

    $didStash = $false
    $dirty = git status --porcelain 2>$null
    if ($dirty) {
        Write-Log 'local changes detected; stash before pull'
        git stash push -m "coordinator-loop-watch: auto-stash before pull $(Get-Date -Format o)" 2>&1 |
            ForEach-Object { Write-Log "stash: $_" }
        if ($LASTEXITCODE -ne 0) {
            Write-Log 'ERROR: git stash failed; abort'
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
            Write-Log 'WARN: stash pop failed (conflict?); check git stash list'
        }
    }

    if (-not $pullOk) {
        Write-Log 'ERROR: git pull --rebase failed; abort'
        return $false
    }
    Write-Log "git pull ok on $branch"
    return $true
}

Write-Log "coordinator-loop-watch start limit=$Limit applyLeases=$ApplyLeases skipScan=$SkipScan dryRun=$DryRun json=$Json"

try {
    if (-not $NoGitPull) {
        if (-not (Invoke-OrchGitPull)) { exit 1 }
    }
    else {
        Write-Log 'git pull skipped (-NoGitPull)'
    }

    $node = Get-Command node -ErrorAction SilentlyContinue
    if (-not $node) {
        Write-Log 'ERROR: node not found (need Node 18+)'
        exit 1
    }

    $loop = Join-Path $here 'coordinator-loop.mjs'
    if (-not (Test-Path $loop)) {
        Write-Log "ERROR: missing $loop"
        exit 1
    }

    $args = @($loop, '--limit', "$Limit")
    if ($ApplyLeases) { $args += '--apply-leases' }
    if ($SkipScan) { $args += '--skip-scan' }
    if ($Json) { $args += '--json' }

    if ($DryRun) {
        Write-Log ("[DRY] would: node " + ($args -join ' '))
        Write-Log 'coordinator-loop-watch ok (dry)'
        exit 0
    }

    Write-Log ("run: node " + ($args -join ' '))
    $out = & node @args 2>&1
    $code = $LASTEXITCODE
    $text = ($out | Out-String)
    if ($Json) {
        Set-Content -Path $latestJson -Value $text -Encoding UTF8
        Write-Log "wrote $latestJson"
    }
    else {
        Set-Content -Path $latest -Value $text -Encoding UTF8
        Write-Log "wrote $latest"
    }
    $text -split "`r?`n" | ForEach-Object {
        if ($_ -and $_.Trim().Length -gt 0) { Write-Log "loop: $_" }
    }

    if ($code -ne 0) {
        Write-Log "WARN: coordinator-loop exit=$code (suggestions may still be useful)"
    }

    # 仅当显式回收 lease 时才考虑 push（会改 task-registry）
    if ($ApplyLeases -and -not $NoGitPush) {
        Write-Log 'git-push-registry after --apply-leases'
        & (Join-Path $here 'lib\git-push-registry.ps1')
    }
    elseif ($ApplyLeases -and $NoGitPush) {
        Write-Log 'ApplyLeases set but git push skipped (-NoGitPush)'
    }
    else {
        Write-Log 'git push skipped (default: no ApplyLeases)'
    }

    Write-Log 'coordinator-loop-watch ok'
    exit 0
}
catch {
    Write-Log "coordinator-loop-watch ERROR: $($_.Exception.Message)"
    exit 1
}
