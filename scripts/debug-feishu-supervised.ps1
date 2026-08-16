# debug-feishu-supervised.ps1 — 核对监管人 outbound 写入
param(
    [string[]]$TaskIds = @('ENT-MOD-SEARCH-UX-L01', 'ENT-MOD-SEARCH-METRIC-OPEN-L01', 'ENT-MOD-SEARCH-V1-HIFI')
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$orch = Split-Path $here -Parent
. (Join-Path $here 'lib\load-env.ps1') -OrchestrationDir $orch
. (Join-Path $here 'lib\feishu-bitable-api.ps1')

$cfgPath = Join-Path $orch 'agent-delivery\feishu\feishu-bitable.yaml'
$regPath = Join-Path $orch 'agent-delivery\task-registry.yaml'
$cfg = Get-FeishuBitableConfig -ConfigPath $cfgPath

Write-Host "FieldSupervised=[$($cfg.FieldSupervised)] FieldClaimed=[$($cfg.FieldClaimed)] HumanMode=$($cfg.HumanDisplayMode)"

$feishu = Get-FeishuOpenPlatformEnv
$token = Get-FeishuTenantAccessToken -AppId $feishu.AppId -AppSecret $feishu.AppSecret
$openIdMap = Get-FeishuUserOpenIdMap -OrchestrationRoot $orch -RosterFile $cfg.RosterFile -UserMapFile $cfg.UserMapFile

# parse tasks (minimal)
$lines = Get-Content -Path $regPath -Encoding UTF8
$inTasks = $false; $tasks = @{}; $cur = $null
foreach ($line in $lines) {
    if ($line -match '^tasks:\s*$') { $inTasks = $true; continue }
    if (-not $inTasks) { continue }
    if ($line -match '^\s+- id:\s*(.+)$') {
        if ($cur) { $tasks[$cur.id] = [pscustomobject]$cur }
        $cur = [ordered]@{ id = $matches[1].Trim().Trim('"') }
        continue
    }
    if (-not $cur) { continue }
    if ($line -match '^\s+supervised_by:\s*(.+)$') { $cur.supervised_by = $matches[1].Trim().Trim('"') }
    if ($line -match '^\s+feishu_bitable_record_id:\s*(.+)$') { $cur.record_id = $matches[1].Trim().Trim('"') }
    if ($line -match '^\s+status:\s*(.+)$') { $cur.status = $matches[1].Trim().Trim('"') }
}
if ($cur) { $tasks[$cur.id] = [pscustomobject]$cur }

# direct unit test
$probe = [pscustomobject]@{ supervised_by = 'human:高颖' }
$probeFields = [ordered]@{}
Set-BitableHumanFieldsOnPayload -Fields $probeFields -Cfg $cfg -Task $probe -OpenIdMap $openIdMap
Write-Host "`n--- probe PSCustomObject ---"
Write-Host "  keys: $($probeFields.Keys -join ', ')"
if ($probeFields.Contains($cfg.FieldSupervised)) { Write-Host "  probe[$($cfg.FieldSupervised)]=$($probeFields[$cfg.FieldSupervised])" }

$nameToId = Get-BitableFieldNameIdMap -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token
Write-Host "`n--- Bitable columns (supervisor-related) ---"
foreach ($f in (Get-BitableFields -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token)) {
    if ($f.field_name -match '监管|认领') {
        Write-Host "  name=$($f.field_name) type=$($f.type) id=$($f.field_id)"
    }
}

foreach ($tid in $TaskIds) {
    Write-Host "`n=== $tid ===" -ForegroundColor Cyan
    if (-not $tasks.ContainsKey($tid)) { Write-Host "  NOT IN REGISTRY"; continue }
    $t = $tasks[$tid]
    Write-Host "  registry supervised_by=[$($t.supervised_by)] record_id=[$($t.record_id)]"
    Write-Host "  cfg useText=$([bool]($cfg.HumanDisplayMode -in @('text_at','both'))) FSP=[$($cfg.FieldSupervisedPerson)] FS=[$($cfg.FieldSupervised)]"

    $fields = [ordered]@{ $cfg.FieldTaskId = $tid }
    Set-BitableHumanFieldsOnPayload -Fields $fields -Cfg $cfg -Task $t -OpenIdMap $openIdMap -SkipClaimed
    $supKey = $cfg.FieldSupervised
    if ($fields.Contains($supKey)) {
        Write-Host "  payload[$supKey]=[$($fields[$supKey])]"
    } else {
        Write-Host "  payload: NO supervised field key [$supKey]" -ForegroundColor Red
        Write-Host "  payload keys: $($fields.Keys -join ', ')"
    }

    if ($t.record_id) {
        $path = "/bitable/v1/apps/$($cfg.AppToken)/tables/$($cfg.TableId)/records/$($t.record_id)"
        $resp = Invoke-FeishuOpenApi -Method Get -Path $path -Token $token
        $rf = $resp.data.record.fields
        $supVal = Get-BitableRecordField -Fields $rf -Name $cfg.FieldSupervised -NameToId $nameToId
        Write-Host "  feishu current[$supKey]=[$supVal]"
    }
}
