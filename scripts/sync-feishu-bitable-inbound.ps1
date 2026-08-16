# sync-feishu-bitable-inbound.ps1
# 飞书多维表格 → task-registry.yaml（Phase 1 pull 回写）
# 用法：
#   .\scripts\sync-feishu-bitable-inbound.ps1 -DryRun
#   .\scripts\sync-feishu-bitable-inbound.ps1 -DryRun:$false

param(
    [switch]$DryRun,
    [string]$RegistryPath = (Join-Path $PSScriptRoot "..\agent-delivery\task-registry.yaml"),
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu\feishu-bitable.yaml"),
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\feishu-bitable-api.ps1')

$orchRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path (Join-Path $orchRoot '.env')) {
    . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir $orchRoot
}

$cfg = Get-FeishuBitableConfig -ConfigPath $ConfigPath
if (-not $cfg.InboundEnabled) {
    Write-Warning "inbound.enabled=false in feishu-bitable.yaml — nothing to do."
    exit 0
}
if (-not $cfg.AppToken -or -not $cfg.TableId) {
    throw "feishu-bitable.yaml: app_token and table_id required."
}
if (-not $PSBoundParameters.ContainsKey('DryRun')) { $DryRun = $cfg.DryRunDefault }

$statusReverse = Get-StatusReverseMap -StatusMap $cfg.StatusMap
$allowed = [System.Collections.Generic.HashSet[string]]::new([string[]]$cfg.InboundAllowedFields)

function Get-RegistryTasks {
    param([string]$Path)
    $lines = Get-Content -Path $Path -Encoding UTF8
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
                'sprint_id' { $cur.sprint_id = $v.Trim('"') }
                'supervised_by' { $cur.supervised_by = $v }
                'claimed_by' { $cur.claimed_by = $v }
                'priority' { $cur.priority = $v }
                'feishu_bitable_record_id' { $cur.record_id = $v }
            }
        }
    }
    if ($cur) { $tasks += [pscustomobject]$cur }
    return $tasks
}

function Get-TaskBlockPattern {
    param([string]$TaskId)
    $esc = [regex]::Escape($TaskId)
    return "(?ms)(^  - id: $esc\s*\r?\n)(.*?)(?=^  - id:|\z)"
}

function Set-TaskFieldInContent {
    param(
        [string]$Content,
        [string]$TaskId,
        [string]$FieldName,
        [string]$FieldValue
    )
    $blockPattern = Get-TaskBlockPattern -TaskId $TaskId
    if ($Content -notmatch $blockPattern) { return $Content }
    $block = $Matches[0]
    $newBlock = $block
    $fieldLine = "    ${FieldName}:"
    if ($newBlock -match "(?m)^    $([regex]::Escape($FieldName)):\s*.+$") {
        $newBlock = [regex]::Replace($newBlock, "(?m)^    $([regex]::Escape($FieldName)):\s*.+$", "    ${FieldName}: $FieldValue", 1)
    }
    else {
        $insertAfter = '    status:'
        if ($newBlock -match "(?m)^    status:\s*.+\r?\n") {
            $newBlock = [regex]::Replace($newBlock, "(?m)^    status:\s*.+\r?\n", { param($m) $m.Value + "    ${FieldName}: $FieldValue`r`n" }, 1)
        }
        else {
            $newBlock = $newBlock.TrimEnd() + "`r`n    ${FieldName}: $FieldValue`r`n"
        }
    }
    return $Content.Replace($block, $newBlock)
}

function Remove-TaskFieldInContent {
    param(
        [string]$Content,
        [string]$TaskId,
        [string]$FieldName
    )
    $blockPattern = Get-TaskBlockPattern -TaskId $TaskId
    if ($Content -notmatch $blockPattern) { return $Content }
    $block = $Matches[0]
    $newBlock = [regex]::Replace($block, "(?m)^    $([regex]::Escape($FieldName)):\s*.+\r?\n?", '', 1)
    return $Content.Replace($block, $newBlock)
}

function Test-StatusTransition {
    param([string]$From, [string]$To)
    $allowed = @{
        backlog = @('ready', 'blocked')
        ready = @('claimed', 'blocked', 'backlog')
        claimed = @('in_progress', 'ready', 'blocked')
        in_progress = @('review', 'blocked')
        review = @('done', 'in_progress', 'blocked')
        blocked = @('backlog', 'ready')
        done = @()
    }
    if ($From -eq $To) { return $true }
    if (-not $allowed.ContainsKey($From)) { return $true }
    return $allowed[$From] -contains $To
}

function Read-BitableRow {
    param($Record, $Cfg, [hashtable]$NameToId = $null)
    $f = $Record.fields
    if (-not $f) { return $null }
    $human = Read-BitableHumanFieldsFromRow -Fields $f -Cfg $Cfg -NameToId $NameToId
    return [pscustomobject]@{
        record_id = $Record.record_id
        task_id = Get-BitableRecordField -Fields $f -Name $Cfg.FieldTaskId -NameToId $NameToId
        title = Get-BitableRecordField -Fields $f -Name $Cfg.FieldTitle -NameToId $NameToId
        status_label = Get-BitableRecordField -Fields $f -Name $Cfg.FieldStatus -NameToId $NameToId
        claimed_by = $human.claimed_by
        supervised_by = $human.supervised_by
        sprint_id = Get-BitableRecordField -Fields $f -Name $Cfg.FieldSprint -NameToId $NameToId
        priority = Get-BitableRecordField -Fields $f -Name $Cfg.FieldPriority -NameToId $NameToId
    }
}

function Append-InboundProposal {
    param(
        [string]$ProposalsPath,
        [pscustomobject]$Row,
        [string]$StatusRegistry
    )
    $full = Join-Path (Split-Path $PSScriptRoot -Parent) ($ProposalsPath -replace '/', [IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path $full)) {
        $seed = @"
# Bitable 新增行提案队列（PM / coordinator 审阅后手工并入 task-registry.yaml）
version: 1
updated: "$(Get-Date -Format 'yyyy-MM-dd')"
proposals: []

"@
        Set-Content -Path $full -Value $seed -Encoding UTF8
    }
    $raw = Get-Content -Path $full -Raw -Encoding UTF8
    $tid = if ($Row.task_id) { $Row.task_id } else { "PROPOSE-$($Row.record_id)" }
    $entry = @"
  - record_id: "$($Row.record_id)"
    task_id: "$tid"
    title: "$($Row.title -replace '"','\"')"
    status: "$StatusRegistry"
    sprint_id: "$($Row.sprint_id)"
    claimed_by: "$($Row.claimed_by)"
    supervised_by: "$($Row.supervised_by)"
    captured_at: "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')"
    source: feishu_bitable

"@
    if ($raw -match 'proposals:\s*\r?\n\s*\r?\n\s*$') {
        $raw = $raw -replace 'proposals:\s*\r?\n\s*$', "proposals:`r`n$entry"
    }
    elseif ($raw -match 'proposals:\s*\[\]\s*') {
        $raw = $raw -replace 'proposals:\s*\[\]', "proposals:`r`n$entry"
    }
    else {
        $raw = $raw.TrimEnd() + "`r`n$entry"
    }
    Set-Content -Path $full -Value $raw -Encoding UTF8
}

$registryTasks = Get-RegistryTasks -Path $RegistryPath
$byId = @{}
foreach ($t in $registryTasks) { $byId[$t.id] = $t }

$feishu = Get-FeishuOpenPlatformEnv
$token = Get-FeishuTenantAccessToken -AppId $feishu.AppId -AppSecret $feishu.AppSecret
$fieldNameToId = Get-BitableFieldNameIdMap -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token
$records = Get-BitableAllRecords -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token

Write-Host "Bitable inbound: $($records.Count) record(s) | DryRun=$DryRun"

$content = Get-Content -Path $RegistryPath -Encoding UTF8 -Raw
$updates = 0
$queued = 0
$skipped = 0

foreach ($rec in $records) {
    $row = Read-BitableRow -Record $rec -Cfg $cfg -NameToId $fieldNameToId
    if (-not $row) { continue }

    $taskId = if ($null -ne $row.task_id) { $row.task_id.Trim() } else { '' }
    if ([string]::IsNullOrWhiteSpace($taskId)) {
        if ($cfg.InboundNewTasks -eq 'queue') {
            Write-Host "  [QUEUE] empty Task ID | record $($row.record_id)"
            if (-not $DryRun) { Append-InboundProposal -ProposalsPath $cfg.InboundProposalsFile -Row $row -StatusRegistry 'backlog' }
            $queued++
        }
        else { Write-Host "  [SKIP] empty Task ID | record $($row.record_id)"; $skipped++ }
        continue
    }

    if ($taskId -notmatch $cfg.InboundTaskIdPattern) {
        Write-Host "  [SKIP] invalid Task ID format: $taskId"
        $skipped++
        continue
    }

    if (-not $byId.ContainsKey($taskId)) {
        if ($cfg.InboundNewTasks -eq 'queue') {
            $st = 'backlog'
            if ($row.status_label -and $statusReverse.ContainsKey($row.status_label)) {
                $st = $statusReverse[$row.status_label]
            }
            Write-Host "  [QUEUE] new task proposal | $taskId"
            if (-not $DryRun) { Append-InboundProposal -ProposalsPath $cfg.InboundProposalsFile -Row $row -StatusRegistry $st }
            $queued++
        }
        else {
            Write-Host "  [SKIP] unknown Task ID (not in registry): $taskId"
            $skipped++
        }
        continue
    }

    $reg = $byId[$taskId]
    $changes = @{}

    if ($allowed.Contains('status') -and $row.status_label) {
        if (-not $statusReverse.ContainsKey($row.status_label)) {
            Write-Warning "  [WARN] unknown status label '$($row.status_label)' for $taskId"
        }
        else {
            $newSt = $statusReverse[$row.status_label]
            if ($newSt -ne $reg.status) {
                $ok = Test-StatusTransition -From $reg.status -To $newSt
                if (-not $ok -and $cfg.InboundValidateTransitions -eq 'strict') {
                    Write-Host "  [SKIP] illegal status $($reg.status)->$newSt | $taskId"
                }
                elseif (-not $ok -and $cfg.InboundValidateTransitions -eq 'warn') {
                    Write-Warning "  [WARN] transition $($reg.status)->$newSt | $taskId"
                    $changes['status'] = $newSt
                }
                else {
                    $changes['status'] = $newSt
                }
            }
        }
    }

    if ($allowed.Contains('claimed_by') -and $row.claimed_by) {
        $v = ConvertFrom-FeishuHumanClaim -FeishuValue $row.claimed_by -AddHumanPrefix $cfg.InboundNormalizeHuman `
            -HumanPrefix $cfg.HumanRegistryPrefix -AtPrefix $cfg.HumanBitableAtPrefix
        if ($v -and $v -ne $reg.claimed_by) { $changes['claimed_by'] = $v }
    }

    # supervised_by：registry 真源，inbound 不回写（见 feishu-bitable.yaml#field_authority）

    if ($allowed.Contains('sprint_id') -and $row.sprint_id -and $row.sprint_id -ne $reg.sprint_id) {
        $changes['sprint_id'] = "`"$($row.sprint_id)`""
    }

    if ($allowed.Contains('title') -and $row.title -and $row.title -ne $reg.title) {
        $changes['title'] = $row.title
    }

    if ($allowed.Contains('priority')) {
        $regPri = if ($null -ne $reg.priority) { [string]$reg.priority.Trim() } else { '' }
        $bitPri = if ($row.priority) { [string]$row.priority.Trim() } else { '' }
        if ($bitPri -ne $regPri) {
            if ($bitPri) { $changes['priority'] = $bitPri }
            else { $changes['__remove_priority'] = '1' }
        }
    }

    if ($row.record_id -and $reg.record_id -ne $row.record_id) {
        $changes['feishu_bitable_record_id'] = $row.record_id
    }

    if ($changes.Count -eq 0) { continue }

    $hintParts = @()
    foreach ($kv in $changes.GetEnumerator()) {
        if ($kv.Key -eq '__remove_priority') { $hintParts += 'priority=(cleared)' }
        else { $hintParts += "$($kv.Key)=$($kv.Value)" }
    }
    $hint = $hintParts -join ', '
    if ($DryRun) {
        Write-Host "  [DRY] UPDATE registry | $taskId | $hint"
        $updates++
        continue
    }

    foreach ($kv in $changes.GetEnumerator()) {
        if ($kv.Key -eq '__remove_priority') {
            $content = Remove-TaskFieldInContent -Content $content -TaskId $taskId -FieldName 'priority'
            continue
        }
        $val = $kv.Value
        if ($kv.Key -eq 'title') { $val = $val }
        $content = Set-TaskFieldInContent -Content $content -TaskId $taskId -FieldName $kv.Key -FieldValue $val
    }
    Write-Host "  UPDATE registry | $taskId | $hint"
    $updates++
}

if (-not $DryRun -and $updates -gt 0) {
    [System.IO.File]::WriteAllText($RegistryPath, $content, (New-Object System.Text.UTF8Encoding $false))
    Write-Host "Updated: $RegistryPath"
}

Write-Host "Done. registry_updates=$updates proposals=$queued skipped=$skipped"
