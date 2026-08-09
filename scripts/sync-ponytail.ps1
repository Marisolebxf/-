# Sync gkx-orchestration/.cursor/rules/ponytail.mdc → coding repos.
# Usage: powershell -NoProfile -File scripts/sync-ponytail.ps1
# Requires GKX_ROOT in .env (or env). Skips dataease (tool fork).

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$orch = Split-Path -Parent $here
$src = Join-Path $orch ".cursor\rules\ponytail.mdc"
if (-not (Test-Path $src)) { throw "Missing source: $src" }

$envFile = Join-Path $orch ".env"
if (-not $env:GKX_ROOT -and (Test-Path $envFile)) {
  Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*GKX_ROOT\s*=\s*(.+)\s*$') { $env:GKX_ROOT = $Matches[1].Trim().Trim('"') }
  }
}
if (-not $env:GKX_ROOT) { throw "GKX_ROOT not set" }

$skip = @("dataease")
$reposRoot = Join-Path $env:GKX_ROOT "repos"
$n = 0
Get-ChildItem $reposRoot -Directory | ForEach-Object {
  if ($skip -contains $_.Name) { return }
  $destDir = Join-Path $_.FullName ".cursor\rules"
  if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
  $dest = Join-Path $destDir "ponytail.mdc"
  Copy-Item -Path $src -Destination $dest -Force
  Write-Host "ok $($_.Name)"
  $n++
}
Write-Host "synced $n repos from $src"
