# feishu-bitable-harvest-person-ids.ps1
# 从 Bitable 已有「人员」列采集 open_id → feishu-user-map.yaml
# 用法：
#   .\scripts\feishu-bitable-harvest-person-ids.ps1
#   .\scripts\feishu-bitable-harvest-person-ids.ps1 -DryRun:$false

param(
    [switch]$DryRun,
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu\feishu-bitable.yaml"),
    [string]$OutputPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu\feishu-user-map.yaml")
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\feishu-bitable-api.ps1')

$orchRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path (Join-Path $orchRoot '.env')) {
    . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir $orchRoot
}

$cfg = Get-FeishuBitableConfig -ConfigPath $ConfigPath
$feishu = Get-FeishuOpenPlatformEnv
$token = Get-FeishuTenantAccessToken -AppId $feishu.AppId -AppSecret $feishu.AppSecret

$personCols = @($cfg.FieldSupervisedPerson, $cfg.FieldClaimedPerson) | Where-Object { $_ } | Select-Object -Unique
$textMentionCols = @()
if ($cfg.FieldClaimedPerson -and $cfg.ClaimedByFormat -eq 'mention') { $textMentionCols += $cfg.FieldClaimedPerson }
if ($personCols.Count -eq 0) {
    throw "No person_field_names configured in feishu-bitable.yaml human_display section."
}

$fieldNameToId = Get-BitableFieldNameIdMap -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token
$records = Get-BitableAllRecords -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token

$discovered = @{}  # open_id -> { name, registry_name, sources }

foreach ($rec in $records) {
    $f = $rec.fields
    if (-not $f) { continue }
    foreach ($col in ($personCols + $textMentionCols | Select-Object -Unique)) {
        $raw = Get-BitableRecordFieldRaw -Fields $f -Key $col
        if ($null -eq $raw -and $fieldNameToId.ContainsKey($col)) {
            $raw = Get-BitableRecordFieldRaw -Fields $f -Key $fieldNameToId[$col]
        }
        if ($null -eq $raw) { continue }
        foreach ($item in @($raw)) {
            if ($null -eq $item) { continue }
            $oid = $null; $name = $null
            if ($item -is [string]) { continue }
            if ($item.type -eq 'mention') {
                if ($item.token) { $oid = [string]$item.token }
                if ($item.name) { $name = [string]$item.name }
            }
            else {
                if ($item.id) { $oid = [string]$item.id }
                if ($item.open_id) { $oid = [string]$item.open_id }
                if ($item.name) { $name = [string]$item.name }
            }
            if (-not $oid -or -not $name) { continue }
            if (-not $discovered.ContainsKey($oid)) {
                $discovered[$oid] = @{
                    name = $name
                    registry_name = "human:$name"
                    sources = @($col)
                }
            }
            elseif ($discovered[$oid].sources -notcontains $col) {
                $discovered[$oid].sources += $col
            }
        }
    }
}

Write-Host "Harvested $($discovered.Count) person(s) from $($records.Count) record(s):"
foreach ($oid in ($discovered.Keys | Sort-Object)) {
    $p = $discovered[$oid]
    Write-Host "  $($p.name) | $oid | from: $($p.sources -join ', ')"
}

if ($DryRun) {
    Write-Host "DryRun — not writing $OutputPath"
    exit 0
}

$existing = Get-FeishuUserOpenIdMap -OrchestrationRoot $orchRoot -RosterFile $cfg.RosterFile -UserMapFile $cfg.UserMapFile
foreach ($oid in $discovered.Keys) {
    $p = $discovered[$oid]
    if ($existing.ByName.ContainsKey($p.name) -and $existing.ByRegistry.Count -gt 0) {
        foreach ($kv in $existing.ByRegistry.GetEnumerator()) {
            if ($kv.Value -eq $existing.ByName[$p.name]) {
                $p.registry_name = $kv.Key
                break
            }
        }
    }
}

# Merge: keep existing map entries not present in this harvest (avoid dropping 高颖 etc.)
$merged = @{}  # open_id -> @{ name, registry_name }
foreach ($kv in $existing.ByRegistry.GetEnumerator()) {
    $oid = [string]$kv.Value
    if ([string]::IsNullOrWhiteSpace($oid)) { continue }
    $reg = [string]$kv.Key
    $name = if ($reg -match '^human:(.+)$') { $matches[1] } else { $reg }
    if (-not $merged.ContainsKey($oid)) {
        $merged[$oid] = @{ name = $name; registry_name = $reg }
    }
}
foreach ($oid in $discovered.Keys) {
    $p = $discovered[$oid]
    $merged[$oid] = @{ name = $p.name; registry_name = $p.registry_name }
}

$yaml = @"
# 飞书 open_id ↔ 团队真名映射（人员字段 sync 用）
# 维护：PM / coordinator · 可用 feishu-bitable-harvest-person-ids.ps1 从看板已有 @人员 采集
# 优先于 team-roster.yaml 内 feishu_open_id（若两处都有，本文件优先）
# harvest 会合并写入：已有映射不会因本次未出现在看板而被删除

version: 1
updated: "$(Get-Date -Format 'yyyy-MM-dd')"
roster_ref: $($cfg.RosterFile)

users:
"@

foreach ($oid in ($merged.Keys | Sort-Object { $merged[$_].name })) {
    $p = $merged[$oid]
    $yaml += "`n  - name: `"$($p.name)`""
    $yaml += "`n    registry_name: `"$($p.registry_name)`""
    $yaml += "`n    feishu_open_id: `"$oid`""
}

[System.IO.File]::WriteAllText($OutputPath, $yaml + "`n", (New-Object System.Text.UTF8Encoding $false))
Write-Host "Wrote: $OutputPath ($($merged.Count) user(s), harvested $($discovered.Count))"
