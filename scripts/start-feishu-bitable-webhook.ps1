# start-feishu-bitable-webhook.ps1
# 启动 Bitable Webhook Handler（RFC-003 Phase C）
#
# 用法：
#   .\scripts\start-feishu-bitable-webhook.ps1
#   .\scripts\start-feishu-bitable-webhook.ps1 -Port 8787
#   .\scripts\start-feishu-bitable-webhook.ps1 -Once -RecordId recxxx
#   .\scripts\start-feishu-bitable-webhook.ps1 -Once -TaskId ENT-MOD-XXX -Status done -DryRun

param(
    [int]$Port = 0,
    [string]$Host = '',
    [switch]$Once,
    [string]$RecordId = '',
    [string]$TaskId = '',
    [string]$Status = '',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$orch = Split-Path $here -Parent

if (Test-Path (Join-Path $orch '.env')) {
    . (Join-Path $here 'lib\load-env.ps1') -OrchestrationDir $orch
}

if ($Port -gt 0) { $env:FEISHU_BITABLE_WEBHOOK_PORT = "$Port" }
if ($Host) { $env:FEISHU_BITABLE_WEBHOOK_HOST = $Host }

$args = @('scripts/feishu-bitable-webhook-handler.mjs')
if ($Once) {
    $args += '--once'
    if ($RecordId) { $args += @('--record-id', $RecordId) }
    if ($TaskId) { $args += @('--task-id', $TaskId) }
    if ($Status) { $args += @('--status', $Status) }
    if ($DryRun) { $args += '--dry-run' }
}

Set-Location $orch
Write-Host "Starting feishu-bitable-webhook-handler..." -ForegroundColor Cyan
& node @args
