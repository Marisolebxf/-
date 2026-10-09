# 检查 gkx-lumen.code-workspace 中 folders 是否在本机存在；缺失则打印并返回非 0。
# 用法（在 gkx-orchestration 根）：.\scripts\check-workspace-folders.ps1

$ErrorActionPreference = "Stop"
$orchRoot = Split-Path -Parent $PSScriptRoot
$wsFile = Join-Path $orchRoot "gkx-lumen.code-workspace"
$gkxRoot = Split-Path -Parent $orchRoot

if (-not (Test-Path $wsFile)) {
  Write-Error "Workspace not found: $wsFile"
}

$raw = Get-Content -LiteralPath $wsFile -Raw -Encoding UTF8
$stripped = [regex]::Replace($raw, '(?m)^\s*//.*$', '')
$stripped = [regex]::Replace($stripped, ',\s*([}\]])', '$1')
$json = $stripped | ConvertFrom-Json

$missing = @()
$ok = @()
foreach ($f in $json.folders) {
  $path = $f.path
  if ([System.IO.Path]::IsPathRooted($path)) {
    $full = $path
  } else {
    $full = [System.IO.Path]::GetFullPath((Join-Path $orchRoot $path))
  }
  if (Test-Path -LiteralPath $full) {
    $ok += "$($f.name) -> $full"
  } else {
    $missing += "$($f.name) -> $full"
  }
}

Write-Host "GKX_ROOT(parent of orch): $gkxRoot"
Write-Host "OK folders: $($ok.Count)"
$ok | ForEach-Object { Write-Host "  OK  $_" }
if ($missing.Count -gt 0) {
  Write-Host "MISSING folders: $($missing.Count)"
  $missing | ForEach-Object { Write-Host "  MISS $_" }
  Write-Host "Fix: remove from gkx-lumen.code-workspace or clone via bootstrap; daily use workspaces/orch-only.code-workspace"
  exit 1
}

Write-Host "All workspace folders exist."
exit 0
