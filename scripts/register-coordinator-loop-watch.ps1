# register-coordinator-loop-watch.ps1
# 本机投影机：注册 Windows 计划任务，定期跑 Mayor 建议包（A3）。
# 不要求 WSL。默认不 --apply-leases（只写 _tmp 建议文件）。
#
# Usage (建议管理员 PowerShell):
#   .\scripts\register-coordinator-loop-watch.ps1
#   .\scripts\register-coordinator-loop-watch.ps1 -Minutes 120
#   .\scripts\register-coordinator-loop-watch.ps1 -ApplyLeases   # 任务带 -ApplyLeases（会写 registry + push）
#   .\scripts\register-coordinator-loop-watch.ps1 -Unregister

param(
    [int]$Minutes = 120,
    [switch]$Unregister,
    [switch]$ApplyLeases,
    [int]$Limit = 8,
    [string]$TaskName = 'GKX-CoordinatorLoopWatch'
)

$ErrorActionPreference = 'Stop'
$orch = Split-Path $PSScriptRoot -Parent
$watch = Join-Path $PSScriptRoot 'coordinator-loop-watch.ps1'

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Unregistered: $TaskName"
    exit 0
}

if (-not (Test-Path $watch)) {
    Write-Error "Missing watch script: $watch"
    exit 1
}

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

$ps = (Get-Command powershell.exe).Source
$extra = @()
if ($ApplyLeases) { $extra += '-ApplyLeases' }
if ($Limit -ne 8) { $extra += "-Limit $Limit" }
$extraArg = if ($extra.Count) { ' ' + ($extra -join ' ') } else { '' }
$arg = "-NoProfile -ExecutionPolicy Bypass -File `"$watch`"$extraArg"
$action = New-ScheduledTaskAction -Execute $ps -Argument $arg -WorkingDirectory $orch
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $Minutes) `
    -RepetitionDuration (New-TimeSpan -Days 9999)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger `
        -Settings $settings -Principal $principal -ErrorAction Stop | Out-Null
}
catch {
    Write-Error "Failed to register $TaskName : $($_.Exception.Message)"
    exit 1
}

Write-Host "Registered $TaskName every $Minutes min"
Write-Host "  WorkingDirectory: $orch"
Write-Host "  Script: $watch$extraArg"
Write-Host "  Latest: agent-delivery\_tmp\coordinator-loop-latest.txt"
Write-Host "  Log:    agent-delivery\_tmp\coordinator-loop-watch.log"
Write-Host "Default: suggestions only (no confirm / no Cursor agent)."
if ($ApplyLeases) {
    Write-Host "ApplyLeases=ON → expired claimed may be cleared + git-push-registry."
}
else {
    Write-Host "ApplyLeases=OFF → registry unchanged; enable with -ApplyLeases if needed."
}
Write-Host "Pair with board-sync watch for Feishu; this task does NOT sync Bitable."
