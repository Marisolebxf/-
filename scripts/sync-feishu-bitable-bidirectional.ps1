# sync-feishu-bitable-bidirectional.ps1
# Phase 1：Bitable 人工改动 → registry，再 registry → Bitable 投影一致
# 用法：
#   .\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun
#   .\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false -SprintId 2026-W28

param(
    [switch]$DryRun,
    [string]$SprintId = '',
    [switch]$SkipInbound,
    [switch]$SkipOutbound
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$dry = if ($PSBoundParameters.ContainsKey('DryRun')) { $DryRun.IsPresent } else { $true }

Write-Host "=== Bitable bidirectional sync ===" -ForegroundColor Cyan
Write-Host "DryRun=$dry SprintId=$SprintId"

if (-not $SkipInbound) {
    Write-Host "`n-- Step 1/2: inbound (Bitable -> registry) --" -ForegroundColor Yellow
    if ($dry) {
        & (Join-Path $here 'sync-feishu-bitable-inbound.ps1') -DryRun
    }
    else {
        & (Join-Path $here 'sync-feishu-bitable-inbound.ps1') -DryRun:$false
    }
}

if (-not $SkipOutbound) {
    Write-Host "`n-- Step 2/2: outbound (registry -> Bitable) --" -ForegroundColor Yellow
    & (Join-Path $here 'sync-task-ready-status.ps1')
    if ($SprintId) {
        if ($dry) {
            & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun -SprintId $SprintId
        }
        else {
            & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun:$false -SprintId $SprintId
        }
    }
    else {
        if ($dry) {
            & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun
        }
        else {
            & (Join-Path $here 'sync-feishu-bitable.ps1') -DryRun:$false
        }
    }
}

Write-Host "`n=== Bidirectional sync complete ===" -ForegroundColor Green
