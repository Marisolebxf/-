# register-board-sync-watch.ps1
# Register Windows Task Scheduler job for projector machine (optional).
# Does NOT require WSL. Only the designated projector PC needs this.
#
# Usage (Admin PowerShell recommended):
#   .\scripts\register-board-sync-watch.ps1
#   .\scripts\register-board-sync-watch.ps1 -Unregister
#   .\scripts\register-board-sync-watch.ps1 -Minutes 60

param(
    [int]$Minutes = 60,
    [switch]$Unregister,
    [string]$TaskName = 'GKX-BoardSyncWatch'
)

$ErrorActionPreference = 'Stop'
$orch = Split-Path $PSScriptRoot -Parent
$watch = Join-Path $PSScriptRoot 'board-sync-watch.ps1'

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Unregistered: $TaskName"
    exit 0
}

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

$ps = (Get-Command powershell.exe).Source
$arg = "-NoProfile -ExecutionPolicy Bypass -File `"$watch`""
$action = New-ScheduledTaskAction -Execute $ps -Argument $arg -WorkingDirectory $orch
# Windows Task Scheduler rejects [TimeSpan]::MaxValue (P99999999DT23H59M59S). Use ~27y.
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes $Minutes) `
    -RepetitionDuration (New-TimeSpan -Days 9999)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

try {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -ErrorAction Stop | Out-Null
}
catch {
    Write-Error "Failed to register $TaskName : $($_.Exception.Message)"
    exit 1
}

Write-Host "Registered $TaskName every $Minutes min"
Write-Host "  WorkingDirectory: $orch"
Write-Host "  Script: $watch"
Write-Host "  After Feishu sync: commit+push task-registry if changed"
Write-Host "  Log: agent-delivery\_tmp\board-sync-watch.log"
Write-Host "Projector only. Ensure non-interactive git push credentials."
Write-Host "Engineers use update-task-status.ps1 instead."
