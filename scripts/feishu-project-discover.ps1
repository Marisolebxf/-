# feishu-project-discover.ps1
# 探测飞书项目空间：plugin_token、工作项类型、字段 meta（用于填写 feishu-project.yaml）
# 用法：.\scripts\feishu-project-discover.ps1 -ProjectKey "your_project_key"

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectKey,
    [string]$WorkItemTypeKey = 'story',
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu-project.yaml")
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\load-env.ps1')
. (Join-Path $PSScriptRoot 'lib\feishu-project-api.ps1')

$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) '.env'
if (Test-Path $envFile) { . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir (Split-Path $PSScriptRoot -Parent) }

$cfg = Get-FeishuProjectConfig -ConfigPath $ConfigPath
$feishu = Get-FeishuEnv
$token = Get-FeishuPluginToken -HostName $cfg.Host -PluginId $feishu.PluginId -PluginSecret $feishu.PluginSecret

Write-Host "=== Feishu Project Discover ===" -ForegroundColor Cyan
Write-Host "Host: $($cfg.Host)"
Write-Host "ProjectKey: $ProjectKey"
Write-Host "UserKey: $($feishu.UserKey)"
Write-Host ""

Write-Host "--- Work Item Types ---" -ForegroundColor Yellow
try {
    $types = Get-FeishuWorkItemTypes -HostName $cfg.Host -ProjectKey $ProjectKey -Token $token -UserKey $feishu.UserKey
    $types.data | ForEach-Object {
        Write-Host "  type_key=$($_.type_key)  name=$($_.name)"
    }
}
catch {
    Write-Warning "List types failed (check plugin installed on space + permissions): $_"
}

Write-Host ""
Write-Host "--- Work Item Meta ($WorkItemTypeKey) ---" -ForegroundColor Yellow
try {
    $meta = Get-FeishuWorkItemMeta -HostName $cfg.Host -ProjectKey $ProjectKey -Token $token -UserKey $feishu.UserKey -WorkItemTypeKey $WorkItemTypeKey
    $meta.data.fields | ForEach-Object {
        $alias = if ($_.field_alias) { " alias=$($_.field_alias)" } else { '' }
        Write-Host "  field_key=$($_.field_key)  name=$($_.field_name)  type=$($_.field_type_key)$alias"
    }
    Write-Host ""
    Write-Host "Suggested: create/find field with alias 'gkx_task_id' (text) for task.id upsert key."
}
catch {
    Write-Warning "Meta failed: $_"
}

Write-Host ""
Write-Host "--- Next steps ---" -ForegroundColor Green
Write-Host "1. Fill agent-delivery/feishu-project.yaml:"
Write-Host "     project.project_key: $ProjectKey"
Write-Host "     project.work_item_type_key: $WorkItemTypeKey"
Write-Host "     sync.external_id.feishu_field_key: <gkx_task_id field_key from above>"
Write-Host "2. Set sync.enabled: true after first -DryRun sync looks correct"
Write-Host "3. Run: .\scripts\sync-feishu-project.ps1 -DryRun -SprintId 2026-W28"
