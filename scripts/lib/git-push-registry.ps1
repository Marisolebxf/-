# git-push-registry.ps1
# After Feishu sync / webhook confirm: commit + push registry YAML and confirm artifacts.
# Soft-fail: never abort the watch solely because push failed.
#
# Whitelist:
#   - agent-delivery/task-registry.yaml
#   - agent-delivery/bitable-inbound-proposals.yaml
#   - agent-delivery/registry-gap-proposals.yaml
#   - agent-delivery/pending-dispatch.yaml
#   - agent-delivery/agent-handoffs/**/*派单条.md / *派单包.md  (changed/untracked only)
#
# Usage:
#   .\scripts\lib\git-push-registry.ps1
#   .\scripts\lib\git-push-registry.ps1 -DryRun

param([switch]$DryRun)

$ErrorActionPreference = 'Continue'
$orch = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $orch

$paths = @(
    'agent-delivery/task-registry.yaml',
    'agent-delivery/bitable-inbound-proposals.yaml',
    'agent-delivery/registry-gap-proposals.yaml',
    'agent-delivery/pending-dispatch.yaml'
)

function Write-GitLog([string]$msg) {
    $logDir = Join-Path $orch 'agent-delivery\_tmp'
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    $line = "[{0}] git-push-registry: {1}" -f (Get-Date -Format 'o'), $msg
    Add-Content -Path (Join-Path $logDir 'board-sync-watch.log') -Value $line -Encoding UTF8
    Write-Host $line
}

$changed = [System.Collections.Generic.List[string]]::new()
foreach ($p in $paths) {
    if (-not (Test-Path $p)) { continue }
    $st = git status --porcelain -- $p 2>$null
    if ($st) { [void]$changed.Add($p) }
}

# confirm 派单条 / 加厚派单包：纳入有变更/未跟踪的 *派单条.md / *派单包.md
$handoffStatus = @(git status --porcelain -u -- 'agent-delivery/agent-handoffs/' 2>$null)
foreach ($line in $handoffStatus) {
    if (-not $line) { continue }
    if ($line -notmatch '派单(条|包)\.md(\s|$)') { continue }
    $pathPart = $line.Substring(3).Trim()
    if ($pathPart.StartsWith('"') -and $pathPart.EndsWith('"')) {
        $pathPart = $pathPart.Substring(1, $pathPart.Length - 2)
    }
    # rename: R  old -> new — take right side
    if ($pathPart -match '->\s*(.+)$') {
        $pathPart = $Matches[1].Trim().Trim('"')
    }
    if ($pathPart -and -not $changed.Contains($pathPart)) {
        [void]$changed.Add($pathPart)
    }
}

if ($changed.Count -eq 0) {
    Write-GitLog 'no registry/dispatch-package changes; skip commit/push'
    exit 0
}

Write-GitLog ("changes: " + ($changed -join ', '))

if ($DryRun) {
    Write-GitLog '[DRY] would commit+push registry (+ dispatch packages if any)'
    exit 0
}

$branch = (git rev-parse --abbrev-ref HEAD 2>$null)
if (-not $branch) {
    Write-GitLog 'ERROR: not a git repo'
    exit 1
}

git pull --rebase origin $branch 2>&1 | ForEach-Object { Write-GitLog "pull: $_" }
if ($LASTEXITCODE -ne 0) {
    Write-GitLog 'WARN: git pull --rebase failed; will still try commit (may need manual fix)'
}

git add -- @($changed)
$commitMsg = $env:GKX_GIT_COMMIT_MSG
if (-not $commitMsg) {
    $hasPkg = $false
    foreach ($c in $changed) {
        if ($c -match '派单(条|包)\.md$') { $hasPkg = $true; break }
    }
    if ($hasPkg) {
        $commitMsg = 'chore(dispatch): sync registry + 派单条/派单包 [agent:coordinator]'
    } else {
        $commitMsg = 'chore(registry): sync from Feishu board watch [agent:coordinator]'
    }
}
git commit -m $commitMsg 2>&1 | ForEach-Object { Write-GitLog "commit: $_" }
if ($LASTEXITCODE -ne 0) {
    $still = git status --porcelain -- @($changed)
    if (-not $still) {
        Write-GitLog 'nothing to commit after staging'
        exit 0
    }
    Write-GitLog 'WARN: git commit failed'
    exit 1
}

git push origin HEAD 2>&1 | ForEach-Object { Write-GitLog "push: $_" }
if ($LASTEXITCODE -ne 0) {
    Write-GitLog 'WARN: git push failed (check credentials / remote); local commit kept'
    exit 1
}

Write-GitLog "ok pushed on $branch"
exit 0
