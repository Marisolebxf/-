# feishu-bitable-discover.ps1
# 列出多维表格 data table 与字段（核对 feishu-bitable.yaml 列名）
param(
    [Parameter(Mandatory = $true)][string]$AppToken,
    [Parameter(Mandatory = $true)][string]$TableId
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\feishu-bitable-api.ps1')
$orchRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path (Join-Path $orchRoot '.env')) {
    . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir $orchRoot
}

$feishu = Get-FeishuOpenPlatformEnv
$token = Get-FeishuTenantAccessToken -AppId $feishu.AppId -AppSecret $feishu.AppSecret

Write-Host "=== Bitable Discover ===" -ForegroundColor Cyan
Write-Host "AppToken: $AppToken"
Write-Host "TableId:  $TableId"
Write-Host ""

Write-Host "--- Fields ---" -ForegroundColor Yellow
$fields = Get-BitableFields -AppToken $AppToken -TableId $TableId -Token $token
foreach ($f in $fields) {
    Write-Host "  name=$($f.field_name)  type=$($f.type)  id=$($f.field_id)"
}

Write-Host ""
Write-Host "Compare with feishu-bitable.yaml#field_names (列名必须完全一致)."
