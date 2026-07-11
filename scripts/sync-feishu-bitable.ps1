# sync-feishu-bitable.ps1
# task-registry.yaml → 飞书多维表格（upsert）
# 用法：
#   .\scripts\sync-feishu-bitable.ps1 -DryRun
#   .\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId "2026-W28"

param(
    [switch]$DryRun,
    [string]$SprintId = '',
    [string]$RegistryPath = (Join-Path $PSScriptRoot "..\agent-delivery\task-registry.yaml"),
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu-bitable.yaml")
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\feishu-bitable-api.ps1')

$orchRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path (Join-Path $orchRoot '.env')) {
    . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir $orchRoot
}

$cfg = Get-FeishuBitableConfig -ConfigPath $ConfigPath
if (-not $cfg.AppToken -or -not $cfg.TableId) {
    throw "feishu-bitable.yaml: app_token and table_id required. See feishu-bitable-integration.md"
}
if (-not $cfg.SyncEnabled -and -not $DryRun) {
    Write-Warning "sync.enabled=false. Use -DryRun or set enabled: true in feishu-bitable.yaml"
}
if (-not $PSBoundParameters.ContainsKey('DryRun')) { $DryRun = $cfg.DryRunDefault }

# Parse tasks
$lines = Get-Content -Path $RegistryPath -Encoding UTF8
$inTasks = $false; $tasks = @(); $cur = $null
foreach ($line in $lines) {
    if ($line -match '^tasks:\s*$') { $inTasks = $true; continue }
    if (-not $inTasks) { continue }
    if ($line -match '^\s+- id:\s*(.+)$') {
        if ($cur) { $tasks += [pscustomobject]$cur }
        $cur = [ordered]@{ id = $matches[1].Trim() }
    }
    elseif ($cur -and $line -match '^\s+(\w+):\s*(.+)$') {
        $k = $matches[1]; $v = $matches[2].Trim().Trim('"')
        switch ($k) {
            'status' { $cur.status = $v }
            'title' { $cur.title = $v }
            'agent' { $cur.agent = $v }
            'epic' { $cur.epic = $v }
            'sprint_id' { $cur.sprint_id = $v.Trim('"') }
            'supervised_by' { $cur.supervised_by = $v }
            'claimed_by' { $cur.claimed_by = $v }
            'estimated_tokens' { $cur.estimated_tokens = ($v -replace '_', '') }
            'feishu_bitable_record_id' { $cur.record_id = $v }
            'evidence' { $cur.evidence = $v }
        }
    }
}
if ($cur) { $tasks += [pscustomobject]$cur }

$statuses = @('backlog','ready','claimed','in_progress','review','blocked','done')
$toSync = $tasks | Where-Object { $statuses -contains $_.status }
if ($SprintId) {
    $toSync = $toSync | Where-Object { $_.sprint_id -eq $SprintId }
}

Write-Host "Bitable sync: $($toSync.Count) task(s) | DryRun=$DryRun"

$feishu = Get-FeishuOpenPlatformEnv
$token = Get-FeishuTenantAccessToken -AppId $feishu.AppId -AppSecret $feishu.AppSecret

$created = 0; $updated = 0

foreach ($task in $toSync) {
    $statusLabel = if ($cfg.StatusMap.ContainsKey($task.status)) { $cfg.StatusMap[$task.status] } else { $task.status }
    $fields = [ordered]@{
        $cfg.FieldTaskId = $task.id
        $cfg.FieldTitle = if ($task.title) { $task.title } else { $task.id }
        $cfg.FieldStatus = $statusLabel
    }
    if ($task.agent) { $fields[$cfg.FieldAgent] = $task.agent }
    if ($task.epic) { $fields[$cfg.FieldEpic] = $task.epic }
    if ($task.sprint_id) { $fields[$cfg.FieldSprint] = $task.sprint_id }
    if ($task.supervised_by) { $fields[$cfg.FieldSupervised] = $task.supervised_by }
    if ($task.claimed_by) { $fields[$cfg.FieldClaimed] = $task.claimed_by }
    if ($task.estimated_tokens) { $fields[$cfg.FieldTokens] = [int]$task.estimated_tokens }
    if ($task.evidence) { $fields[$cfg.FieldHandoff] = $task.evidence }

    $recordId = $task.record_id
    if (-not $recordId) {
        $found = Search-BitableRecordByTaskId -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token `
            -FieldTaskId $cfg.FieldTaskId -TaskId $task.id
        if ($found) { $recordId = $found.record_id }
    }

    if ($DryRun) {
        $action = if ($recordId) { "UPDATE $recordId" } else { 'CREATE' }
        Write-Host "  [DRY] $action | $($task.status) | $($task.id)"
        continue
    }

    Start-Sleep -Milliseconds $cfg.RateLimitMs
    if ($recordId) {
        Update-BitableRecord -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token -RecordId $recordId -Fields $fields | Out-Null
        Write-Host "  UPDATE $recordId | $($task.id)"
        $updated++
    }
    else {
        $rec = New-BitableRecord -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token -Fields $fields
        Write-Host "  CREATE $($rec.record_id) | $($task.id) — optional: feishu_bitable_record_id in registry"
        $created++
    }
}

Write-Host "Done. created=$created updated=$updated"
