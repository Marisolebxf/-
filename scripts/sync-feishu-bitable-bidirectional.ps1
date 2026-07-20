# sync-feishu-bitable-bidirectional.ps1
# Phase 1：Bitable 人工改动 → registry，再 registry → Bitable 投影一致
# 用法：
#   .\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun
#   .\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false -SprintId 2026-W28
#   .\scripts\sync-feishu-bitable-bidirectional.ps1 -DryRun:$false -FeishuAuthoritative
#
# -FeishuAuthoritative（board-sync-watch 默认）：
#   看板字段（状态/认领/Sprint/优先级/标题）以飞书最新为准；
#   outbound 不覆盖这些字段（认领列不写出站）；supervised_by 仍以 registry 投影。

param(
    [switch]$DryRun,
    [string]$SprintId = '',
    [switch]$SkipInbound,
    [switch]$SkipOutbound,
    [switch]$FeishuAuthoritative
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$orch = Split-Path $here -Parent
$dry = if ($PSBoundParameters.ContainsKey('DryRun')) { $DryRun.IsPresent } else { $true }
$registryPath = Join-Path $orch 'agent-delivery\task-registry.yaml'

function Get-RegistryStatusMap {
    param([string]$Path)
    $map = @{}
    $lines = Get-Content -Path $Path -Encoding UTF8
    $inTasks = $false
    $curId = $null
    foreach ($line in $lines) {
        if ($line -match '^tasks:\s*$') { $inTasks = $true; continue }
        if (-not $inTasks) { continue }
        if ($line -match '^\s+- id:\s*(.+)$') {
            $curId = $matches[1].Trim().Trim('"')
            continue
        }
        if ($curId -and $line -match '^\s+status:\s*(.+)$') {
            $map[$curId] = $matches[1].Trim().Trim('"')
            $curId = $null
        }
    }
    return $map
}

function Get-RegistryTasksMissingFeishuRecordId {
    param([string]$Path)
    $include = @('backlog', 'ready', 'claimed', 'in_progress', 'review', 'blocked', 'done')
    $ids = New-Object System.Collections.Generic.List[string]
    $lines = Get-Content -Path $Path -Encoding UTF8
    $inTasks = $false
    $cur = $null
    foreach ($line in $lines) {
        if ($line -match '^tasks:\s*$') { $inTasks = $true; continue }
        if (-not $inTasks) { continue }
        if ($line -match '^\s+- id:\s*(.+)$') {
            if ($cur -and $include -contains $cur.status -and -not $cur.record_id) {
                [void]$ids.Add($cur.id)
            }
            $cur = [ordered]@{ id = $matches[1].Trim().Trim('"'); status = ''; record_id = '' }
            continue
        }
        if (-not $cur) { continue }
        if ($line -match '^\s+status:\s*(.+)$') { $cur.status = $matches[1].Trim().Trim('"') }
        if ($line -match '^\s+feishu_bitable_record_id:\s*(.+)$') { $cur.record_id = $matches[1].Trim().Trim('"') }
    }
    if ($cur -and $include -contains $cur.status -and -not $cur.record_id) {
        [void]$ids.Add($cur.id)
    }
    return ,$ids
}

Write-Host "=== Bitable bidirectional sync ===" -ForegroundColor Cyan
Write-Host "DryRun=$dry SprintId=$SprintId FeishuAuthoritative=$FeishuAuthoritative"

if ($FeishuAuthoritative) {
    Write-Host "Kanban precedence: Feishu (inbound absorbs; outbound skips kanban fields on existing rows)" -ForegroundColor Yellow
}

if (-not $SkipInbound) {
    Write-Host "`n-- Step 1/2: inbound (Bitable -> registry) --" -ForegroundColor Yellow
    if ($dry) {
        & (Join-Path $here 'sync-feishu-bitable-inbound.ps1') -DryRun
    }
    else {
        & (Join-Path $here 'sync-feishu-bitable-inbound.ps1') -DryRun:$false
    }
}

$readyChangedIds = @()
if (-not $SkipOutbound) {
    Write-Host "`n-- Step 2/2: outbound (registry -> Bitable) --" -ForegroundColor Yellow
    $before = Get-RegistryStatusMap -Path $registryPath
    & (Join-Path $here 'sync-task-ready-status.ps1')
    $after = Get-RegistryStatusMap -Path $registryPath
    foreach ($k in $after.Keys) {
        if (-not $before.ContainsKey($k)) { continue }
        if ($before[$k] -ne $after[$k]) {
            $readyChangedIds += $k
        }
    }
    if ($readyChangedIds.Count -gt 0) {
        Write-Host ("ready-status changed: " + ($readyChangedIds -join ', '))
    }

    $outArgs = @{
        SprintId = $SprintId
    }
    if ($dry) { $outArgs['DryRun'] = $true }
    else { $outArgs['DryRun'] = $false }

    if ($FeishuAuthoritative) {
        # 投影 Agent/Epic/Handoff 等；不覆盖飞书看板字段
        & (Join-Path $here 'sync-feishu-bitable.ps1') @outArgs -SkipKanbanFields
        # ready-status 自动迁移的 status 允许定向推板（非人工拖拽冲突）
        if ($readyChangedIds.Count -gt 0) {
            Write-Host "`n-- Step 2b: push ready-status auto migrations to Feishu --" -ForegroundColor Yellow
            & (Join-Path $here 'sync-feishu-bitable.ps1') @outArgs -OnlyTaskIds $readyChangedIds
        }
    }
    else {
        & (Join-Path $here 'sync-feishu-bitable.ps1') @outArgs
    }

    # 无 feishu_bitable_record_id 的任务须 CREATE 到看板（不受 current_sprint 过滤）
    $missingRecordIds = Get-RegistryTasksMissingFeishuRecordId -Path $registryPath
    if ($missingRecordIds.Count -gt 0) {
        Write-Host "`n-- Step 2c: CREATE Bitable rows for tasks missing feishu_bitable_record_id ($($missingRecordIds.Count)) --" -ForegroundColor Yellow
        Write-Host ("  ids: " + ($missingRecordIds -join ', '))
        $createArgs = @{
            DryRun = $dry
            OnlyTaskIds = $missingRecordIds
            SprintId = ''
        }
        if ($FeishuAuthoritative) {
            & (Join-Path $here 'sync-feishu-bitable.ps1') @createArgs -SkipKanbanFields
        }
        else {
            & (Join-Path $here 'sync-feishu-bitable.ps1') @createArgs
        }
    }
}

Write-Host "`n=== Bidirectional sync complete ===" -ForegroundColor Green
