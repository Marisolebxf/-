# sync-feishu-project.ps1
# task-registry.yaml → 飞书项目工作项（upsert）
# 用法：
#   .\scripts\sync-feishu-project.ps1 -DryRun
#   .\scripts\sync-feishu-project.ps1 -DryRun:$false -SprintId "2026-W28"

param(
    [switch]$DryRun,
    [string]$SprintId = '',
    [string]$RegistryPath = (Join-Path $PSScriptRoot "..\agent-delivery\task-registry.yaml"),
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu-project.yaml")
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\feishu-project-api.ps1')

$orchRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path (Join-Path $orchRoot '.env')) {
    . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir $orchRoot
}

$cfg = Get-FeishuProjectConfig -ConfigPath $ConfigPath
if (-not $cfg.SyncEnabled -and -not $DryRun) {
    Write-Warning "feishu-project.yaml sync.enabled=false. Use -DryRun to preview, or set enabled: true after setup."
}
if (-not $cfg.ProjectKey) {
    throw "feishu-project.yaml project.project_key is empty. Run feishu-project-discover.ps1 and fill config."
}

if (-not $PSBoundParameters.ContainsKey('DryRun')) {
    $DryRun = $cfg.DryRunDefault
}

# Parse tasks from registry
$lines = Get-Content -Path $RegistryPath -Encoding UTF8
$inTasks = $false
$tasks = @()
$cur = $null

function Parse-InlineList([string]$value) {
    $value = $value.Trim()
    if ($value -match '^\[(.*)\]$') {
        $inner = $matches[1].Trim()
        if ([string]::IsNullOrWhiteSpace($inner)) { return @() }
        return $inner -split ',\s*' | ForEach-Object { $_.Trim().Trim('"') }
    }
    return @($value.Trim('"'))
}

foreach ($line in $lines) {
    if ($line -match '^tasks:\s*$') { $inTasks = $true; continue }
    if (-not $inTasks) { continue }
    if ($line -match '^\s+- id:\s*(.+)$') {
        if ($cur) { $tasks += [pscustomobject]$cur }
        $cur = [ordered]@{ id = $matches[1].Trim() }
    }
    elseif ($cur -and $line -match '^\s+(\w+):\s*(.+)$') {
        $k = $matches[1]; $v = $matches[2].Trim()
        switch ($k) {
            'status' { $cur.status = $v }
            'title' { $cur.title = $v.Trim('"') }
            'agent' { $cur.agent = $v }
            'epic' { $cur.epic = $v }
            'sprint_id' { $cur.sprint_id = $v.Trim('"') }
            'supervised_by' { $cur.supervised_by = $v.Trim('"') }
            'claimed_by' { $cur.claimed_by = $v.Trim('"') }
            'estimated_tokens' { $cur.estimated_tokens = ($v -replace '_', '') }
            'feishu_work_item_id' { $cur.feishu_work_item_id = $v.Trim('"') }
            'evidence' { $cur.evidence = $v }
        }
    }
}
if ($cur) { $tasks += [pscustomobject]$cur }

$activeStatuses = @('backlog','ready','claimed','in_progress','review','blocked','done')
$toSync = $tasks | Where-Object { $activeStatuses -contains $_.status }
if ($SprintId) {
    $toSync = $toSync | Where-Object { $_.sprint_id -eq "`"$SprintId`"" -or $_.sprint_id -eq $SprintId }
}

Write-Host "Feishu Project sync: $($toSync.Count) task(s) | DryRun=$DryRun | Project=$($cfg.ProjectKey)"

$feishu = Get-FeishuEnv
$token = Get-FeishuPluginToken -HostName $cfg.Host -PluginId $feishu.PluginId -PluginSecret $feishu.PluginSecret

$created = 0; $updated = 0; $skipped = 0

foreach ($task in $toSync) {
    $name = if ($task.title) { "$($task.id) · $($task.title)" } else { $task.id }
    if ($name.Length -gt 200) { $name = $name.Substring(0, 197) + '...' }

    $fields = @()
    if ($cfg.ExternalFieldKey) {
        $fields += @{ field_key = $cfg.ExternalFieldKey; field_value = $task.id }
    }

    $existingId = $null
    if ($task.feishu_work_item_id) {
        $existingId = [long]$task.feishu_work_item_id
    }
    elseif ($cfg.ExternalFieldKey) {
        $found = Search-FeishuWorkItemByExternalId -HostName $cfg.Host -ProjectKey $cfg.ProjectKey `
            -Token $token -UserKey $feishu.UserKey -WorkItemTypeKey $cfg.WorkItemTypeKey `
            -ExternalFieldKey $cfg.ExternalFieldKey -TaskId $task.id
        if ($found -and $found.id) { $existingId = [long]$found.id }
    }

    if ($DryRun) {
        $action = if ($existingId) { "UPDATE $existingId" } else { 'CREATE' }
        Write-Host "  [DRY] $action | $($task.status) | $name"
        continue
    }

    Start-Sleep -Milliseconds $cfg.RateLimitMs

    if ($existingId) {
        Update-FeishuWorkItem -HostName $cfg.Host -ProjectKey $cfg.ProjectKey -Token $token `
            -UserKey $feishu.UserKey -WorkItemTypeKey $cfg.WorkItemTypeKey -WorkItemId $existingId `
            -FieldValuePairs $fields | Out-Null
        Write-Host "  UPDATE $existingId | $($task.id)"
        $updated++
    }
    else {
        $resp = New-FeishuWorkItem -HostName $cfg.Host -ProjectKey $cfg.ProjectKey -Token $token `
            -UserKey $feishu.UserKey -WorkItemTypeKey $cfg.WorkItemTypeKey -Name $name -FieldValuePairs $fields
        $newId = $resp.data
        Write-Host "  CREATE $newId | $($task.id) — add feishu_work_item_id: $newId to registry"
        $created++
    }
}

Write-Host "Done. created=$created updated=$updated skipped=$skipped"
if ($created -gt 0) {
    Write-Host "Tip: backfill feishu_work_item_id in task-registry.yaml for faster updates next run."
}
