$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
if (-not $here) { $here = Split-Path -Parent $MyInvocation.MyCommand.Path }
$root = Split-Path -Parent $here
$envFile = Join-Path $root ".env.local"
if (-not (Test-Path $envFile)) { Write-Error "missing $envFile" }
Get-Content $envFile | ForEach-Object {
  $line = $_.Trim()
  if (-not $line -or $line.StartsWith("#")) { return }
  $i = $line.IndexOf("=")
  if ($i -lt 1) { return }
  $name = $line.Substring(0, $i).Trim()
  $value = $line.Substring($i + 1).Trim().Trim('"').Trim("'")
  Set-Item -Path ("Env:" + $name) -Value $value
}
Write-Host "Loaded .env.local"
Write-Host ("  HOST=" + $env:ENTAN_MYSQL_HOST + " PORT=" + $env:ENTAN_MYSQL_PORT + " USER=" + $env:ENTAN_MYSQL_USER)
Write-Host ("  ODS_DB=" + $env:ENTAN_MYSQL_ODS_DB)