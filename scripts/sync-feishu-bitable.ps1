# sync-feishu-bitable.ps1
# task-registry.yaml → 飞书多维表格（upsert）
# 用法：
#   .\scripts\sync-feishu-bitable.ps1 -DryRun
#   .\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SprintId "2026-W28"
#   .\scripts\sync-feishu-bitable.ps1 -DryRun:$false -SkipKanbanFields
#   .\scripts\sync-feishu-bitable.ps1 -DryRun:$false -OnlyTaskIds @('E-E7-POLICY-M1-L01')

param(
    [switch]$DryRun,
    [string]$SprintId = '',
    [string]$RegistryPath = (Join-Path $PSScriptRoot "..\agent-delivery\task-registry.yaml"),
    [string]$ConfigPath = (Join-Path $PSScriptRoot "..\agent-delivery\feishu\feishu-bitable.yaml"),
    # 不写出站覆盖飞书看板字段（状态/认领/Sprint/优先级/标题）；监管人仍以 registry 为准始终投影
    [switch]$SkipKanbanFields,
    # 仅同步指定 Task ID（用于 ready-status 自动迁移后的定向推板）
    [string[]]$OnlyTaskIds = @()
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'lib\feishu-bitable-api.ps1')

$orchRoot = Split-Path $PSScriptRoot -Parent
if (Test-Path (Join-Path $orchRoot '.env')) {
    . (Join-Path $PSScriptRoot 'lib\load-env.ps1') -OrchestrationDir $orchRoot
}

$cfg = Get-FeishuBitableConfig -ConfigPath $ConfigPath
if (-not $cfg.AppToken -or -not $cfg.TableId) {
    throw "feishu-bitable.yaml: app_token and table_id required. See feishu/feishu-bitable-integration.md"
}
if (-not $cfg.SyncEnabled -and -not $DryRun) {
    Write-Warning "sync.enabled=false. Use -DryRun or set enabled: true in feishu-bitable.yaml"
}
if (-not $PSBoundParameters.ContainsKey('DryRun')) { $DryRun = $cfg.DryRunDefault }

# Parse tasks (incl. multiline note: | and definition_of_done list)
$lines = Get-Content -Path $RegistryPath -Encoding UTF8
$inTasks = $false; $tasks = @(); $cur = $null
$collectMode = $null  # 'note' | 'dod'
$collectBuf = New-Object System.Collections.Generic.List[string]

function Complete-BitableTaskCollect {
    param($Task, [string]$Mode, $Buf)
    if (-not $Task -or -not $Mode) { return }
    $text = ($Buf -join "`n").TrimEnd()
    if ($Mode -eq 'note') { $Task.note = $text.Trim() }
    elseif ($Mode -eq 'dod') { $Task.definition_of_done = $text.Trim() }
}

foreach ($line in $lines) {
    if ($line -match '^tasks:\s*$') { $inTasks = $true; continue }
    if (-not $inTasks) { continue }

    if ($line -match '^\s+- id:\s*(.+)$') {
        if ($collectMode) {
            Complete-BitableTaskCollect -Task $cur -Mode $collectMode -Buf $collectBuf
            $collectMode = $null
            $collectBuf.Clear()
        }
        if ($cur) { $tasks += [pscustomobject]$cur }
        $cur = [ordered]@{ id = $matches[1].Trim().Trim('"') }
        continue
    }

    if ($collectMode -and $cur) {
        # Next top-level task field (4 spaces + key:) ends block collect
        if ($line -match '^\s{4}(\w+):\s*(.*)$' -and $line -notmatch '^\s{6,}') {
            Complete-BitableTaskCollect -Task $cur -Mode $collectMode -Buf $collectBuf
            $collectMode = $null
            $collectBuf.Clear()
            # fall through to parse this key line below
        }
        else {
            if ($collectMode -eq 'dod' -and $line -match '^\s+-\s+(.+)$') {
                [void]$collectBuf.Add(('- ' + $matches[1].Trim()))
            }
            elseif ($collectMode -eq 'note') {
                if ($line -match '^\s{6,}(.*)$') {
                    [void]$collectBuf.Add($matches[1].TrimEnd())
                }
                elseif ($line -match '^\s*$') {
                    [void]$collectBuf.Add('')
                }
            }
            continue
        }
    }

    if (-not $cur) { continue }

    if ($line -match '^\s+note:\s*\|\s*$' -or $line -match '^\s+note:\s*>\s*$') {
        $collectMode = 'note'
        $collectBuf.Clear()
        continue
    }
    if ($line -match '^\s+note:\s*(.+)$') {
        $cur.note = $matches[1].Trim().Trim('"')
        continue
    }
    if ($line -match '^\s+definition_of_done:\s*$') {
        $collectMode = 'dod'
        $collectBuf.Clear()
        continue
    }
    if ($line -match '^\s+(\w+):\s*(.+)$') {
        $k = $matches[1]; $v = $matches[2].Trim().Trim('"')
        switch ($k) {
            'status' { $cur.status = $v }
            'title' { $cur.title = $v }
            'agent' { $cur.agent = $v }
            'epic' { $cur.epic = $v }
            'sprint_id' { $cur.sprint_id = $v.Trim('"') }
            'supervised_by' { $cur.supervised_by = $v }
            'claimed_by' { $cur.claimed_by = $v }
            'priority' { $cur.priority = $v }
            'estimated_tokens' { $cur.estimated_tokens = (($v -replace '_', '') -replace '\s+#.*$', '').Trim() }
            'feishu_bitable_record_id' { $cur.record_id = $v }
            'evidence' { $cur.evidence = $v }
            'effort_points' { $cur.effort_points = (($v -replace '\s+#.*$', '').Trim()) }
            'difficulty' { $cur.difficulty = $v.Trim().Trim('"') }
            'delivery_phase' { $cur.delivery_phase = (($v -replace '\s+#.*$', '').Trim().Trim('"')) }
            default {
                if (-not $cur.evidence -and $v -match '^(?:agent-handoffs|验收文档|agent-delivery)/.+') {
                    $cur.evidence = $v
                }
            }
        }
    }
}
if ($collectMode) {
    Complete-BitableTaskCollect -Task $cur -Mode $collectMode -Buf $collectBuf
}
if ($cur) { $tasks += [pscustomobject]$cur }

$statuses = @('backlog','ready','claimed','in_progress','review','blocked','done')
$toSync = $tasks | Where-Object { $statuses -contains $_.status }
if ($OnlyTaskIds -and $OnlyTaskIds.Count -gt 0) {
    $idSet = [System.Collections.Generic.HashSet[string]]::new([string[]]$OnlyTaskIds)
    $toSync = @($toSync | Where-Object { $idSet.Contains($_.id) })
    Write-Host "OnlyTaskIds filter: $($OnlyTaskIds.Count) id(s) → $($toSync.Count) task(s) to sync"
}
if ($SkipKanbanFields) {
    Write-Host "SkipKanbanFields=ON (status/claim/sprint/priority/title skipped; supervised_by always from registry)"
}
# OnlyTaskIds 为显式定向同步，不受 Sprint 过滤（避免 current_sprint 滞后导致新任务漏推飞书）
if ($SprintId -and (-not $OnlyTaskIds -or $OnlyTaskIds.Count -eq 0)) {
    $toSync = $toSync | Where-Object { $_.sprint_id -eq $SprintId }
}

Write-Host "Bitable sync: $($toSync.Count) task(s) | DryRun=$DryRun"

$feishu = Get-FeishuOpenPlatformEnv
$token = Get-FeishuTenantAccessToken -AppId $feishu.AppId -AppSecret $feishu.AppSecret
$openIdMap = Get-FeishuUserOpenIdMap -OrchestrationRoot $orchRoot -RosterFile $cfg.RosterFile -UserMapFile $cfg.UserMapFile

Ensure-BitableColumns -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token -DryRun:$DryRun -Columns @(
    @{ Name = $cfg.FieldNote; Type = 1 },
    @{ Name = $cfg.FieldDefinitionOfDone; Type = 1 },
    @{ Name = $cfg.FieldEffortPoints; Type = 2 },
    @{ Name = $cfg.FieldDifficulty; Type = 1 },
    @{ Name = $cfg.FieldDeliveryPhase; Type = 1 }
)

$created = 0; $updated = 0

foreach ($task in $toSync) {
    $statusLabel = if ($cfg.StatusMap.ContainsKey($task.status)) { $cfg.StatusMap[$task.status] } else { $task.status }

    $recordId = $task.record_id
    if (-not $recordId) {
        $found = Search-BitableRecordByTaskId -AppToken $cfg.AppToken -TableId $cfg.TableId -Token $token `
            -FieldTaskId $cfg.FieldTaskId -TaskId $task.id
        if ($found) { $recordId = $found.record_id }
    }

    # 已有行 + SkipKanbanFields：状态/标题/Sprint/优先级以飞书为准；认领不写出站；监管人仍以 registry 投影
    $omitKanbanCore = $SkipKanbanFields -and $recordId
    $skipClaimedOutbound = [bool]$SkipKanbanFields
    $fields = [ordered]@{
        $cfg.FieldTaskId = $task.id
    }
    if (-not $omitKanbanCore) {
        $fields[$cfg.FieldTitle] = if ($task.title) { $task.title } else { $task.id }
        $fields[$cfg.FieldStatus] = $statusLabel
        if ($task.sprint_id) { $fields[$cfg.FieldSprint] = $task.sprint_id }
        if ($task.priority) { $fields[$cfg.FieldPriority] = $task.priority }
    }
    Set-BitableHumanFieldsOnPayload -Fields $fields -Cfg $cfg -Task $task -OpenIdMap $openIdMap `
        -SkipClaimed:$skipClaimedOutbound
    if ($task.agent) { $fields[$cfg.FieldAgent] = $task.agent }
    if ($task.epic) {
        $fields[$cfg.FieldEpic] = $task.epic
        if ($cfg.FieldModule) {
            $fields[$cfg.FieldModule] = Resolve-EpicModuleName -Epic $task.epic `
                -ExactMap $cfg.EpicModuleMap -PrefixMap $cfg.EpicModulePrefix -Default $cfg.EpicModuleDefault
        }
    }
    if ($task.estimated_tokens) { $fields[$cfg.FieldTokens] = [int]$task.estimated_tokens }
    if ($task.evidence) {
        $fields[$cfg.FieldHandoff] = ConvertTo-BitableHandoffFieldValue -EvidencePath $task.evidence -Cfg $cfg
    }
    if ($task.note -and $cfg.FieldNote) {
        $fields[$cfg.FieldNote] = [string]$task.note
    }
    if ($task.definition_of_done -and $cfg.FieldDefinitionOfDone) {
        $fields[$cfg.FieldDefinitionOfDone] = [string]$task.definition_of_done
    }
    if ($task.effort_points -and $cfg.FieldEffortPoints) {
        $ep = 0
        if ([int]::TryParse([string]$task.effort_points, [ref]$ep)) {
            $fields[$cfg.FieldEffortPoints] = $ep
        }
    }
    if ($task.difficulty -and $cfg.FieldDifficulty) {
        $fields[$cfg.FieldDifficulty] = [string]$task.difficulty
    }
    if ($cfg.FieldDeliveryPhase) {
        $fields[$cfg.FieldDeliveryPhase] = Resolve-DeliveryPhaseLabel `
            -TaskId $task.id -Epic $task.epic -ExplicitPhase $task.delivery_phase -Cfg $cfg
    }

    if ($DryRun) {
        $action = if ($recordId) { "UPDATE $recordId" } else { 'CREATE' }
        $mod = if ($fields.Contains($cfg.FieldModule)) { $fields[$cfg.FieldModule] } else { '' }
        $modHint = if ($mod) { " | $mod" } else { '' }
        $extra = @()
        if ($omitKanbanCore) { $extra += 'omit-kanban-core' }
        if ($skipClaimedOutbound) { $extra += 'skip-claimed-outbound' }
        if ($task.note) { $extra += "note=$($task.note.Length)c" }
        if ($task.definition_of_done) { $extra += "dod=$($task.definition_of_done.Length)c" }
        $extraHint = if ($extra.Count) { ' | ' + ($extra -join ' ') } else { '' }
        Write-Host "  [DRY] $action | $($task.status) | $($task.id)$modHint$extraHint"
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
