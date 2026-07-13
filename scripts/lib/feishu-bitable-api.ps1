# 飞书 OpenAPI 薄封装 — 多维表格（Bitable）
# 文档：agent-delivery/feishu-bitable-integration.md

function Get-FeishuBitableConfig {
    param([string]$ConfigPath)
    if (-not (Test-Path $ConfigPath)) { throw "Config not found: $ConfigPath" }
    $raw = Get-Content $ConfigPath -Raw -Encoding UTF8
    $cfg = [ordered]@{
        AppToken = ''
        TableId = ''
        SyncEnabled = $false
        DryRunDefault = $true
        RateLimitMs = 200
        FieldTaskId = 'Task ID'
        FieldTitle = '标题'
        FieldStatus = '状态'
        FieldAgent = 'Agent'
        FieldEpic = 'Epic'
        FieldSprint = 'Sprint'
        FieldSupervised = '监管人'
        FieldClaimed = '认领'
        FieldTokens = 'Token估算'
        FieldPriority = '优先级'
        FieldHandoff = 'Handoff'
        FieldModule = '功能模块'
        FieldNote = '备注'
        FieldDefinitionOfDone = '验收标准'
        FieldEffortPoints = '贡献分'
        FieldDifficulty = '难度'
        StatusMap = @{}
        EpicModuleMap = @{}
        EpicModulePrefix = @{}
        EpicModuleDefault = '其他'
        SyncDirection = 'registry_to_bitable'
        InboundEnabled = $false
        InboundAllowedFields = @('status', 'claimed_by', 'supervised_by', 'sprint_id', 'title', 'priority')
        InboundNewTasks = 'queue'
        InboundProposalsFile = 'agent-delivery/bitable-inbound-proposals.yaml'
        InboundNormalizeHuman = $true
        InboundValidateTransitions = 'warn'
        InboundTaskIdPattern = '^[A-Z][A-Za-z0-9-]+$'
        HumanDisplayEnabled = $true
        HumanDisplayMode = 'text_at'
        HumanRegistryPrefix = 'human:'
        HumanBitableAtPrefix = '@'
        RosterFile = 'agent-delivery/team-roster.yaml'
        UserMapFile = 'agent-delivery/feishu-user-map.yaml'
        FieldSupervisedPerson = ''
        FieldClaimedPerson = ''
        ClaimedByFormat = 'mention'
        SupervisedByFormat = 'user'
        HandoffLinkEnabled = $true
        HandoffWriteMode = 'plain'
        HandoffGitlabBase = 'https://gitlab.htmisoft.net'
        HandoffGitlabGroup = 'gkx-lumen'
        HandoffRepo = 'gkx-orchestration'
        HandoffBranch = 'dev'
        HandoffPathPrefix = 'agent-delivery'
    }
    if ($raw -match '(?m)^\s+app_token:\s*"(.*)"') { $cfg.AppToken = $matches[1] }
    if ($raw -match '(?m)^\s+table_id:\s*"(.*)"') { $cfg.TableId = $matches[1] }
    if ($raw -match '(?m)^\s+direction:\s*(\w+)') { $cfg.SyncDirection = $matches[1] }
    if ($raw -match '(?m)^\s+enabled:\s*(true|false)') { $cfg.SyncEnabled = ($matches[1] -eq 'true') }
    if ($raw -match '(?m)^\s+dry_run_default:\s*(true|false)') { $cfg.DryRunDefault = ($matches[1] -eq 'true') }
    if ($raw -match '(?m)^\s+rate_limit_ms:\s*(\d+)') { $cfg.RateLimitMs = [int]$matches[1] }
    if ($raw -match '(?m)^\s+task_id:\s*"(.+)"') { $cfg.FieldTaskId = $matches[1] }
    if ($raw -match '(?m)^\s+title:\s*"(.+)"') { $cfg.FieldTitle = $matches[1] }
    if ($raw -match '(?m)^\s+status:\s*"(.+)"') { $cfg.FieldStatus = $matches[1] }
    if ($raw -match '(?m)^\s+agent:\s*"(.+)"') { $cfg.FieldAgent = $matches[1] }
    if ($raw -match '(?m)^\s+epic:\s*"(.+)"') { $cfg.FieldEpic = $matches[1] }
    if ($raw -match '(?m)^\s+sprint_id:\s*"(.+)"') { $cfg.FieldSprint = $matches[1] }
    if ($raw -match '(?m)^\s+supervised_by:\s*"(.+)"') { $cfg.FieldSupervised = $matches[1] }
    if ($raw -match '(?m)^\s+claimed_by:\s*"(.+)"') { $cfg.FieldClaimed = $matches[1] }
    if ($raw -match '(?m)^\s+estimated_tokens:\s*"(.+)"') { $cfg.FieldTokens = $matches[1] }
    if ($raw -match '(?m)^\s+priority:\s*"(.+)"') { $cfg.FieldPriority = $matches[1] }
    if ($raw -match '(?m)^\s+handoff:\s*"(.+)"') { $cfg.FieldHandoff = $matches[1] }
    if ($raw -match '(?m)^\s+module:\s*"(.+)"') { $cfg.FieldModule = $matches[1] }
    if ($raw -match '(?m)^\s+note:\s*"(.+)"') { $cfg.FieldNote = $matches[1] }
    if ($raw -match '(?m)^\s+definition_of_done:\s*"(.+)"') { $cfg.FieldDefinitionOfDone = $matches[1] }
    if ($raw -match '(?m)^\s+effort_points:\s*"(.+)"') { $cfg.FieldEffortPoints = $matches[1] }
    if ($raw -match '(?m)^\s+difficulty:\s*"(.+)"') { $cfg.FieldDifficulty = $matches[1] }
    if ($raw -match '(?m)^\s+epic_module_default:\s*"(.+)"') { $cfg.EpicModuleDefault = $matches[1] }
    foreach ($m in [regex]::Matches($raw, '(?m)^\s+(backlog|ready|claimed|in_progress|review|done|blocked):\s*"(.+)"')) {
        $cfg.StatusMap[$m.Groups[1].Value] = $m.Groups[2].Value.Trim()
    }
    if ($raw -match '(?m)epic_module_map:\s*\r?\n((?:  .+\r?\n)+)') {
        foreach ($m in [regex]::Matches($matches[1], '(?m)^  (E-[A-Za-z0-9-]+):\s*"(.+)"')) {
            $cfg.EpicModuleMap[$m.Groups[1].Value] = $m.Groups[2].Value.Trim()
        }
    }
    if ($raw -match '(?m)epic_module_prefix:\s*\r?\n((?:  .+\r?\n)+)') {
        foreach ($m in [regex]::Matches($matches[1], '(?m)^  (E-[A-Za-z0-9-]+):\s*"(.+)"')) {
            $cfg.EpicModulePrefix[$m.Groups[1].Value] = $m.Groups[2].Value.Trim()
        }
    }
    if ($raw -match '(?m)inbound:\s*\r?\n((?:  .+\r?\n)+)') {
        $inBlock = $matches[1]
        if ($inBlock -match '(?m)^  enabled:\s*(true|false)') { $cfg.InboundEnabled = ($matches[1] -eq 'true') }
        if ($inBlock -match '(?m)^  new_tasks:\s*(\w+)') { $cfg.InboundNewTasks = $matches[1] }
        if ($inBlock -match '(?m)^  proposals_file:\s*(\S+)') { $cfg.InboundProposalsFile = $matches[1] }
        if ($inBlock -match '(?m)^  normalize_human_prefix:\s*(true|false)') { $cfg.InboundNormalizeHuman = ($matches[1] -eq 'true') }
        if ($inBlock -match '(?m)^  validate_transitions:\s*(\w+)') { $cfg.InboundValidateTransitions = $matches[1] }
        if ($inBlock -match '(?m)^  task_id_pattern:\s*"(.+)"') { $cfg.InboundTaskIdPattern = $matches[1] }
        if ($inBlock -match '(?m)allowed_fields:\s*\[(.*?)\]') {
            $cfg.InboundAllowedFields = @($matches[1] -split ',\s*' | ForEach-Object { $_.Trim() } | Where-Object { $_ })
        }
    }
    if ($raw -match '(?m)human_display:\s*\r?\n((?:  .+\r?\n)+)') {
        $hd = $matches[1]
        if ($hd -match '(?m)^  enabled:\s*(true|false)') { $cfg.HumanDisplayEnabled = ($matches[1] -eq 'true') }
        if ($hd -match '(?m)^  mode:\s*(\w+)') { $cfg.HumanDisplayMode = $matches[1] }
        if ($hd -match '(?m)^  registry_human_prefix:\s*"(.+)"') { $cfg.HumanRegistryPrefix = $matches[1] }
        if ($hd -match '(?m)^  bitable_at_prefix:\s*"(.+)"') { $cfg.HumanBitableAtPrefix = $matches[1] }
        if ($hd -match '(?m)^  roster_file:\s*(\S+)') { $cfg.RosterFile = $matches[1] }
        if ($hd -match '(?m)^  user_map_file:\s*(\S+)') { $cfg.UserMapFile = $matches[1] }
        if ($hd -match '(?m)person_field_names:\s*\r?\n((?:    .+\r?\n)+)') {
            $pf = $matches[1]
            if ($pf -match '(?m)^    supervised_by:\s*"(.+)"') { $cfg.FieldSupervisedPerson = $matches[1].Trim() }
            if ($pf -match '(?m)^    claimed_by:\s*"(.+)"') { $cfg.FieldClaimedPerson = $matches[1].Trim() }
        }
        if ($hd -match '(?m)field_formats:\s*\r?\n((?:    .+\r?\n)+)') {
            $ff = $matches[1]
            if ($ff -match '(?m)^    claimed_by:\s*(\w+)') { $cfg.ClaimedByFormat = $matches[1].Trim() }
            if ($ff -match '(?m)^    supervised_by:\s*(\w+)') { $cfg.SupervisedByFormat = $matches[1].Trim() }
        }
    }
    if (-not $cfg.FieldClaimedPerson -and $cfg.HumanDisplayMode -in @('person', 'both')) {
        $cfg.FieldClaimedPerson = $cfg.FieldClaimed
    }
    if ($raw -match '(?m)handoff_link:\s*\r?\n((?:  .+\r?\n)+)') {
        $hl = $matches[1]
        if ($hl -match '(?m)^  enabled:\s*(true|false)') { $cfg.HandoffLinkEnabled = ($matches[1] -eq 'true') }
        if ($hl -match '(?m)^  write_mode:\s*(\w+)') { $cfg.HandoffWriteMode = $matches[1].Trim() }
        if ($hl -match '(?m)^  gitlab_base:\s*"(.+)"') { $cfg.HandoffGitlabBase = $matches[1].Trim().TrimEnd('/') }
        if ($hl -match '(?m)^  gitlab_group:\s*"(.+)"') { $cfg.HandoffGitlabGroup = $matches[1].Trim() }
        if ($hl -match '(?m)^  repo:\s*"(.+)"') { $cfg.HandoffRepo = $matches[1].Trim() }
        if ($hl -match '(?m)^  branch:\s*"(.+)"') { $cfg.HandoffBranch = $matches[1].Trim() }
        if ($hl -match '(?m)^  path_prefix:\s*"(.+)"') { $cfg.HandoffPathPrefix = $matches[1].Trim().Trim('/') }
    }
    return [pscustomobject]$cfg
}

function ConvertTo-GitLabBlobUrl {
    param(
        [string]$EvidencePath,
        [object]$Cfg
    )
    if ([string]::IsNullOrWhiteSpace($EvidencePath)) { return $null }
    $p = $EvidencePath.Trim().Trim('"').Replace('\', '/')
    if ($p -match '^https?://') { return $p }

    $prefix = if ($Cfg.HandoffPathPrefix) { $Cfg.HandoffPathPrefix.Trim('/') } else { 'agent-delivery' }
    if ($p -notmatch "^$([regex]::Escape($prefix))(/|$)") {
        $p = "$prefix/$p"
    }
    $p = $p.TrimStart('/')

    $encoded = ($p -split '/' | ForEach-Object { [Uri]::EscapeDataString($_) }) -join '/'
    $base = $Cfg.HandoffGitlabBase.TrimEnd('/')
    $group = $Cfg.HandoffGitlabGroup
    $repo = $Cfg.HandoffRepo
    $branch = $Cfg.HandoffBranch
    return "$base/$group/$repo/-/blob/$branch/$encoded`?ref_type=heads"
}

function ConvertTo-BitableHandoffFieldValue {
    param(
        [string]$EvidencePath,
        [object]$Cfg
    )
    if ([string]::IsNullOrWhiteSpace($EvidencePath)) { return $null }
    if (-not $Cfg.HandoffLinkEnabled) { return $EvidencePath.Trim() }

    $url = ConvertTo-GitLabBlobUrl -EvidencePath $EvidencePath -Cfg $Cfg
    if (-not $url) { return $EvidencePath.Trim() }

    $display = ($EvidencePath.Trim().Replace('\', '/') -split '/')[-1]
    if ([string]::IsNullOrWhiteSpace($display)) { $display = 'Handoff' }

    $mode = if ($Cfg.HandoffWriteMode) { $Cfg.HandoffWriteMode } else { 'url_text' }
    switch ($mode) {
        'hyperlink' {
            return @{ text = $display; link = $url }
        }
        'plain' {
            return $url
        }
        default {
            # 文本列富文本超链接（与飞书 UI 可点击链接一致）
            return ,@(@{ type = 'url'; text = $display; link = $url })
        }
    }
}

function Resolve-EpicModuleName {
    param(
        [string]$Epic,
        [hashtable]$ExactMap,
        [hashtable]$PrefixMap,
        [string]$Default
    )
    if (-not $Epic) { return $Default }
    if ($ExactMap.ContainsKey($Epic)) { return $ExactMap[$Epic] }
    $bestPrefix = $null
    foreach ($pfx in $PrefixMap.Keys) {
        if ($Epic.StartsWith($pfx) -and ($null -eq $bestPrefix -or $pfx.Length -gt $bestPrefix.Length)) {
            $bestPrefix = $pfx
        }
    }
    if ($bestPrefix) { return $PrefixMap[$bestPrefix] }
    return $Default
}

function Get-FeishuOpenPlatformEnv {
    $appId = $env:FEISHU_APP_ID
    $appSecret = $env:FEISHU_APP_SECRET
    if (-not $appId -or -not $appSecret) {
        throw @"
Missing Feishu Open Platform credentials. Set in gkx-orchestration/.env:
  FEISHU_APP_ID
  FEISHU_APP_SECRET
See feishu-bitable-integration.md §2
"@
    }
    return [pscustomobject]@{ AppId = $appId; AppSecret = $appSecret }
}

function Get-FeishuTenantAccessToken {
    param([string]$AppId, [string]$AppSecret)
    $uri = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    $body = @{ app_id = $AppId; app_secret = $AppSecret } | ConvertTo-Json
    $resp = Invoke-RestMethod -Method Post -Uri $uri -Body $body -ContentType 'application/json; charset=utf-8'
    if ($resp.code -ne 0 -or -not $resp.tenant_access_token) {
        throw "tenant_access_token failed: $($resp | ConvertTo-Json -Compress)"
    }
    return $resp.tenant_access_token
}

function Invoke-FeishuOpenApi {
    param(
        [string]$Method,
        [string]$Path,
        [string]$Token,
        [object]$Body = $null,
        [string]$QueryString = ''
    )
    $uri = "https://open.feishu.cn/open-apis$Path"
    if ($QueryString) { $uri += "?$QueryString" }
    $headers = @{ Authorization = "Bearer $Token"; 'Content-Type' = 'application/json; charset=utf-8' }
    $params = @{ Method = $Method; Uri = $uri; Headers = $headers }
    $json = $null
    if ($null -ne $Body) {
        $json = $Body | ConvertTo-Json -Depth 12 -Compress
        $params.Body = [System.Text.Encoding]::UTF8.GetBytes($json)
    }
    try {
        $resp = Invoke-RestMethod @params
        if ($resp.code -ne 0) {
            $detail = if ($json) { " body=$json" } else { '' }
            throw "code=$($resp.code) msg=$($resp.msg)$detail"
        }
        return $resp
    }
    catch {
        $detail = if ($json) { " body=$json" } else { '' }
        throw "Feishu OpenAPI $Method $Path failed: $($_.Exception.Message)$detail"
    }
}

function Search-BitableRecordByTaskId {
    param(
        [string]$AppToken, [string]$TableId, [string]$Token,
        [string]$FieldTaskId, [string]$TaskId
    )
    $path = "/bitable/v1/apps/$AppToken/tables/$TableId/records/search"
    $body = @{
        filter = @{
            conjunction = 'and'
            conditions = @(
                @{
                    field_name = $FieldTaskId
                    operator = 'is'
                    value = @($TaskId)
                }
            )
        }
        page_size = 5
    }
    $resp = Invoke-FeishuOpenApi -Method Post -Path $path -Token $Token -Body $body
    if ($resp.data.items -and $resp.data.items.Count -gt 0) {
        return $resp.data.items[0]
    }
    return $null
}

function Get-BitableFieldNameIdMap {
    param([string]$AppToken, [string]$TableId, [string]$Token)
    $items = Get-BitableFields -AppToken $AppToken -TableId $TableId -Token $Token
    $map = @{}
    foreach ($item in $items) { $map[$item.field_name] = $item.field_id }
    return $map
}

function ConvertTo-BitableFieldPayloadById {
    param(
        [hashtable]$FieldsByName,
        [hashtable]$NameToIdMap
    )
    $out = [ordered]@{}
    foreach ($name in $FieldsByName.Keys) {
        if (-not $NameToIdMap.ContainsKey($name)) {
            throw "Bitable column not found: [$name]. Run feishu-bitable-discover.ps1 and fix field_names / table columns."
        }
        $out[$NameToIdMap[$name]] = $FieldsByName[$name]
    }
    return $out
}

function Update-BitableRecord {
    param(
        [string]$AppToken, [string]$TableId, [string]$Token,
        [string]$RecordId, [hashtable]$Fields
    )
    $path = "/bitable/v1/apps/$AppToken/tables/$TableId/records/$RecordId"
    $body = @{ fields = $Fields }
    $resp = Invoke-FeishuOpenApi -Method Put -Path $path -Token $Token -Body $body -QueryString 'user_id_type=open_id'
    return $resp.data.record
}

function New-BitableRecord {
    param(
        [string]$AppToken, [string]$TableId, [string]$Token,
        [hashtable]$Fields
    )
    $path = "/bitable/v1/apps/$AppToken/tables/$TableId/records"
    $body = @{ fields = $Fields }
    $resp = Invoke-FeishuOpenApi -Method Post -Path $path -Token $Token -Body $body -QueryString 'user_id_type=open_id'
    return $resp.data.record
}

function Get-StatusReverseMap {
    param([hashtable]$StatusMap)
    $rev = @{}
    foreach ($k in $StatusMap.Keys) { $rev[$StatusMap[$k]] = $k }
    return $rev
}

function ConvertFrom-BitableFieldValue {
    param($Value)
    if ($null -eq $Value) { return $null }
    if ($Value -is [string] -or $Value -is [int] -or $Value -is [long] -or $Value -is [double]) { return [string]$Value }
    if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
        $arr = @($Value)
        if ($arr.Count -ge 1 -and $null -ne $arr[0]) {
            $item = $arr[0]
            if ($item.name) { return [string]$item.name }
            if ($item.text) { return [string]$item.text }
        }
        $parts = @($Value | ForEach-Object {
            if ($_ -is [string]) { $_ }
            elseif ($_.text) { $_.text }
            elseif ($_.name) { $_.name }
            else { "$_" }
        })
        return ($parts -join '')
    }
    if ($Value.text) { return [string]$Value.text }
    if ($Value.name) { return [string]$Value.name }
    return [string]$Value
}

function ConvertTo-FeishuHumanDisplay {
    param(
        [string]$RegistryValue,
        [bool]$Enabled = $true,
        [string]$HumanPrefix = 'human:',
        [string]$AtPrefix = '@'
    )
    if (-not $Enabled -or [string]::IsNullOrWhiteSpace($RegistryValue)) { return $RegistryValue }
    $v = $RegistryValue.Trim()
    $hp = [regex]::Escape($HumanPrefix)
    if ($v -match "^$hp(.+)$") {
        $name = $matches[1].Trim().TrimStart('@')
        return "$AtPrefix$name"
    }
    if ($v -match '^agent:') { return $v }
    return $v
}

function ConvertFrom-FeishuHumanClaim {
    param(
        [string]$FeishuValue,
        [bool]$AddHumanPrefix = $true,
        [string]$HumanPrefix = 'human:',
        [string]$AtPrefix = '@'
    )
    if ([string]::IsNullOrWhiteSpace($FeishuValue)) { return $null }
    $v = $FeishuValue.Trim()
    $hp = [regex]::Escape($HumanPrefix)
    if ($v -match "^$hp(.+)$") {
        $name = $matches[1].Trim().TrimStart($AtPrefix)
        return "${HumanPrefix}$name"
    }
    if ($v -match '^agent:') { return $v }
    $name = $v.TrimStart($AtPrefix)
    if (-not $AddHumanPrefix) { return $name }
    return "${HumanPrefix}$name"
}

function Normalize-HumanClaimValue {
    param([string]$Value, [bool]$AddPrefix, [string]$HumanPrefix = 'human:', [string]$AtPrefix = '@')
    return ConvertFrom-FeishuHumanClaim -FeishuValue $Value -AddHumanPrefix $AddPrefix `
        -HumanPrefix $HumanPrefix -AtPrefix $AtPrefix
}

function Get-FeishuUserOpenIdMap {
    param(
        [string]$OrchestrationRoot,
        [string]$RosterFile,
        [string]$UserMapFile
    )
    $byRegistry = @{}
    $byName = @{}

    function Register-OpenId {
        param([string]$OpenId, [string]$Name, [string]$RegistryName)
        if ([string]::IsNullOrWhiteSpace($OpenId)) { return }
        if ($RegistryName) { $byRegistry[$RegistryName] = $OpenId }
        if ($Name) { $byName[$Name.Trim()] = $OpenId }
    }

    function Import-OpenIdsFromYaml {
        param([string]$Path, [switch]$ListUsesRegistryName)
        if (-not (Test-Path $Path)) { return }
        $lines = Get-Content $Path -Encoding UTF8
        $curName = $null
        $curReg = $null
        $curOid = $null

        foreach ($line in $lines) {
            if ($line -match '^\s+- name:\s*(.+)') {
                if ($curOid) { Register-OpenId -OpenId $curOid -Name $curName -RegistryName $curReg }
                $curName = $matches[1].Trim().Trim('"'); $curReg = $null; $curOid = $null
                continue
            }
            if ($ListUsesRegistryName -and $line -match '^\s+- registry_name:\s*(.+)') {
                if ($curOid) { Register-OpenId -OpenId $curOid -Name $curName -RegistryName $curReg }
                $curReg = $matches[1].Trim().Trim('"'); $curName = $null; $curOid = $null
                continue
            }
            if ($line -match '^\s+name:\s*(.+)') { $curName = $matches[1].Trim().Trim('"'); continue }
            if ($line -match '^\s+registry_name:\s*(.+)') { $curReg = $matches[1].Trim().Trim('"'); continue }
            if ($line -match '^\s+feishu_open_id:\s*(.+)') { $curOid = $matches[1].Trim().Trim('"') }
        }
        if ($curOid) { Register-OpenId -OpenId $curOid -Name $curName -RegistryName $curReg }
    }

    $mapPath = Join-Path $OrchestrationRoot ($UserMapFile -replace '/', [IO.Path]::DirectorySeparatorChar)
    Import-OpenIdsFromYaml -Path $mapPath

    $rosterPath = Join-Path $OrchestrationRoot ($RosterFile -replace '/', [IO.Path]::DirectorySeparatorChar)
    Import-OpenIdsFromYaml -Path $rosterPath -ListUsesRegistryName

    return [pscustomobject]@{ ByRegistry = $byRegistry; ByName = $byName }
}

function Resolve-FeishuOpenIdFromRegistry {
    param(
        [string]$RegistryValue,
        [object]$OpenIdMap,
        [string]$HumanPrefix = 'human:'
    )
    if ([string]::IsNullOrWhiteSpace($RegistryValue)) { return $null }
    $v = $RegistryValue.Trim()
    if ($OpenIdMap.ByRegistry.ContainsKey($v)) { return $OpenIdMap.ByRegistry[$v] }
    $hp = [regex]::Escape($HumanPrefix)
    if ($v -match "^$hp(.+)$") {
        $name = $matches[1].Trim().TrimStart('@')
        if ($OpenIdMap.ByRegistry.ContainsKey("${HumanPrefix}$name")) {
            return $OpenIdMap.ByRegistry["${HumanPrefix}$name"]
        }
        if ($OpenIdMap.ByName.ContainsKey($name)) { return $OpenIdMap.ByName[$name] }
    }
    return $null
}

function ConvertTo-BitablePersonFieldValue {
    param([string]$OpenId)
    if ([string]::IsNullOrWhiteSpace($OpenId)) { return $null }
    return ,@(@{ id = $OpenId.Trim() })
}

function ConvertTo-BitableMentionFieldValue {
    param(
        [string]$OpenId,
        [string]$DisplayName,
        [string]$AtPrefix = '@',
        [bool]$MentionNotify = $false
    )
    if ([string]::IsNullOrWhiteSpace($OpenId) -or [string]::IsNullOrWhiteSpace($DisplayName)) { return $null }
    $name = $DisplayName.Trim().TrimStart('@')
    return ,@(@{
        type = 'mention'
        text = "$AtPrefix$name"
        token = $OpenId.Trim()
        name = $name
        mentionType = 'User'
        mentionNotify = $MentionNotify
    })
}

function Get-HumanDisplayNameFromRegistry {
    param([string]$RegistryValue, [string]$HumanPrefix = 'human:')
    if ([string]::IsNullOrWhiteSpace($RegistryValue)) { return $null }
    $v = $RegistryValue.Trim()
    $hp = [regex]::Escape($HumanPrefix)
    if ($v -match "^$hp(.+)$") { return $matches[1].Trim().TrimStart('@') }
    return $v.TrimStart('@')
}

function Get-BitablePersonDisplayName {
    param($Fields, [string]$Name, [hashtable]$NameToId = $null)
    $raw = Get-BitableRecordFieldRaw -Fields $Fields -Key $Name
    if ($null -eq $raw -and $NameToId -and $NameToId.ContainsKey($Name)) {
        $raw = Get-BitableRecordFieldRaw -Fields $Fields -Key $NameToId[$Name]
    }
    if ($null -eq $raw) { return $null }
    $names = @()
    $items = @($raw)
    foreach ($item in $items) {
        if ($null -eq $item) { continue }
        if ($item -is [string]) { $names += $item.TrimStart('@'); continue }
        if ($item.type -eq 'mention' -and $item.name) { $names += [string]$item.name; continue }
        if ($item.name) { $names += [string]$item.name }
        elseif ($item.text) { $names += [string]$item.text.TrimStart('@') }
    }
    if ($names.Count -eq 0) { return $null }
    return ($names -join '、')
}

function Set-BitableHumanFieldsOnPayload {
    param(
        [hashtable]$Fields,
        [object]$Cfg,
        [object]$Task,
        [object]$OpenIdMap
    )
    if (-not $Cfg.HumanDisplayEnabled) { return }

    $mode = if ($Cfg.HumanDisplayMode) { $Cfg.HumanDisplayMode } else { 'text_at' }
    $usePerson = $mode -in @('person', 'both')
    $useText = $mode -in @('text_at', 'both')

    if ($Task.supervised_by) {
        if ($usePerson -and $Cfg.FieldSupervisedPerson) {
            $oid = Resolve-FeishuOpenIdFromRegistry -RegistryValue $Task.supervised_by -OpenIdMap $OpenIdMap `
                -HumanPrefix $Cfg.HumanRegistryPrefix
            $displayName = Get-HumanDisplayNameFromRegistry -RegistryValue $Task.supervised_by -HumanPrefix $Cfg.HumanRegistryPrefix
            if ($oid) {
                if ($Cfg.SupervisedByFormat -eq 'mention') {
                    $Fields[$Cfg.FieldSupervisedPerson] = ConvertTo-BitableMentionFieldValue -OpenId $oid `
                        -DisplayName $displayName -AtPrefix $Cfg.HumanBitableAtPrefix
                }
                else {
                    $Fields[$Cfg.FieldSupervisedPerson] = ConvertTo-BitablePersonFieldValue -OpenId $oid
                }
            }
            else {
                Write-Warning "  [WARN] no feishu_open_id for supervised_by $($Task.supervised_by) — run feishu-bitable-harvest-person-ids.ps1"
            }
        }
        if ($useText -and $Cfg.FieldSupervised) {
            $Fields[$Cfg.FieldSupervised] = ConvertTo-FeishuHumanDisplay -RegistryValue $Task.supervised_by `
                -Enabled $true -HumanPrefix $Cfg.HumanRegistryPrefix -AtPrefix $Cfg.HumanBitableAtPrefix
        }
        elseif ($Cfg.FieldSupervised -and -not $Cfg.FieldSupervisedPerson) {
            $Fields[$Cfg.FieldSupervised] = ConvertTo-FeishuHumanDisplay -RegistryValue $Task.supervised_by `
                -Enabled $true -HumanPrefix $Cfg.HumanRegistryPrefix -AtPrefix $Cfg.HumanBitableAtPrefix
        }
    }

    if ($Task.claimed_by) {
        $claimedCol = if ($Cfg.FieldClaimedPerson) { $Cfg.FieldClaimedPerson } else { $Cfg.FieldClaimed }
        if ($usePerson -and $claimedCol) {
            $oid = Resolve-FeishuOpenIdFromRegistry -RegistryValue $Task.claimed_by -OpenIdMap $OpenIdMap `
                -HumanPrefix $Cfg.HumanRegistryPrefix
            if ($oid) {
                if ($Cfg.ClaimedByFormat -eq 'mention') {
                    $displayName = Get-HumanDisplayNameFromRegistry -RegistryValue $Task.claimed_by -HumanPrefix $Cfg.HumanRegistryPrefix
                    $Fields[$claimedCol] = ConvertTo-BitableMentionFieldValue -OpenId $oid `
                        -DisplayName $displayName -AtPrefix $Cfg.HumanBitableAtPrefix
                }
                else {
                    $Fields[$claimedCol] = ConvertTo-BitablePersonFieldValue -OpenId $oid
                }
            }
            else {
                Write-Warning "  [WARN] no feishu_open_id for claimed_by $($Task.claimed_by) — run feishu-bitable-harvest-person-ids.ps1"
            }
        }
        elseif ($useText -and $Cfg.FieldClaimed -and -not $usePerson) {
            $Fields[$Cfg.FieldClaimed] = ConvertTo-FeishuHumanDisplay -RegistryValue $Task.claimed_by `
                -Enabled $true -HumanPrefix $Cfg.HumanRegistryPrefix -AtPrefix $Cfg.HumanBitableAtPrefix
        }
    }
}

function Read-BitableHumanFieldsFromRow {
    param($Fields, [object]$Cfg, [hashtable]$NameToId = $null)
    $claimed = $null
    $supervised = $null

    $claimedPersonCol = if ($Cfg.FieldClaimedPerson) { $Cfg.FieldClaimedPerson } else { $Cfg.FieldClaimed }
    if ($Cfg.FieldSupervisedPerson) {
        $supervised = Get-BitablePersonDisplayName -Fields $Fields -Name $Cfg.FieldSupervisedPerson -NameToId $NameToId
    }
    if (-not $supervised -and $Cfg.FieldSupervised) {
        $supervised = Get-BitableRecordField -Fields $Fields -Name $Cfg.FieldSupervised -NameToId $NameToId
    }

    if ($claimedPersonCol) {
        $claimed = Get-BitablePersonDisplayName -Fields $Fields -Name $claimedPersonCol -NameToId $NameToId
    }
    if (-not $claimed -and $Cfg.FieldClaimed -and $Cfg.FieldClaimed -ne $claimedPersonCol) {
        $claimed = Get-BitableRecordField -Fields $Fields -Name $Cfg.FieldClaimed -NameToId $NameToId
    }

    return [pscustomobject]@{ claimed_by = $claimed; supervised_by = $supervised }
}

function Get-BitableRecordField {
    param($Fields, [string]$Name, [hashtable]$NameToId = $null)
    $val = Get-BitableRecordFieldRaw -Fields $Fields -Key $Name
    if ($null -ne $val) { return ConvertFrom-BitableFieldValue -Value $val }
    if ($NameToId -and $NameToId.ContainsKey($Name)) {
        $fid = $NameToId[$Name]
        $val = Get-BitableRecordFieldRaw -Fields $Fields -Key $fid
        if ($null -ne $val) { return ConvertFrom-BitableFieldValue -Value $val }
    }
    return $null
}

function Get-BitableRecordFieldRaw {
    param($Fields, [string]$Key)
    if ($null -eq $Fields -or [string]::IsNullOrWhiteSpace($Key)) { return $null }
    if ($Fields -is [System.Collections.IDictionary]) {
        if (-not $Fields.Contains($Key)) { return $null }
        return $Fields[$Key]
    }
    $prop = $Fields.PSObject.Properties | Where-Object { $_.Name -eq $Key } | Select-Object -First 1
    if (-not $prop) { return $null }
    return $prop.Value
}

function Get-BitableAllRecords {
    param(
        [string]$AppToken, [string]$TableId, [string]$Token,
        [int]$PageSize = 500
    )
    $all = @()
    $pageToken = $null
    do {
        $qs = "page_size=$PageSize"
        if ($pageToken) { $qs += "&page_token=$pageToken" }
        $path = "/bitable/v1/apps/$AppToken/tables/$TableId/records?$qs"
        $resp = Invoke-FeishuOpenApi -Method Get -Path $path -Token $Token
        if ($resp.data.items) { $all += $resp.data.items }
        $pageToken = $resp.data.page_token
    } while ($pageToken)
    return $all
}

function Get-BitableTables {
    param([string]$AppToken, [string]$Token)
    $path = "/bitable/v1/apps/$AppToken/tables"
    return (Invoke-FeishuOpenApi -Method Get -Path $path -Token $Token).data.items
}

function Get-BitableFields {
    param([string]$AppToken, [string]$TableId, [string]$Token)
    $path = "/bitable/v1/apps/$AppToken/tables/$TableId/fields"
    return (Invoke-FeishuOpenApi -Method Get -Path $path -Token $Token).data.items
}

# Create missing columns. Soft-warn on failure so sync can continue for other fields.
# $Columns: array of @{ Name = '...'; Type = 1|2 }  (1=text, 2=number)
function Ensure-BitableColumns {
    param(
        [string]$AppToken,
        [string]$TableId,
        [string]$Token,
        [object[]]$Columns,
        [switch]$DryRun
    )
    if (-not $Columns -or $Columns.Count -eq 0) { return }
    $existing = @{}
    foreach ($f in (Get-BitableFields -AppToken $AppToken -TableId $TableId -Token $Token)) {
        if ($f.field_name) { $existing[$f.field_name] = $true }
    }
    foreach ($col in $Columns) {
        $name = $col.Name
        $type = if ($col.Type) { [int]$col.Type } else { 1 }
        if ([string]::IsNullOrWhiteSpace($name)) { continue }
        if ($existing.ContainsKey($name)) { continue }
        $typeLabel = if ($type -eq 2) { 'number' } else { 'text' }
        if ($DryRun) {
            Write-Host "  [DRY] would create $typeLabel column: $name"
            continue
        }
        try {
            $path = "/bitable/v1/apps/$AppToken/tables/$TableId/fields"
            $null = Invoke-FeishuOpenApi -Method Post -Path $path -Token $Token -Body @{
                field_name = $name
                type       = $type
            }
            Write-Host "  CREATE column [$name] ($typeLabel)"
            $existing[$name] = $true
        }
        catch {
            Write-Warning "Failed to create Bitable column [$name]: $($_.Exception.Message). Create it manually."
        }
    }
}

function Ensure-BitableTextColumns {
    param(
        [string]$AppToken,
        [string]$TableId,
        [string]$Token,
        [string[]]$FieldNames,
        [switch]$DryRun
    )
    $cols = @($FieldNames | Where-Object { $_ } | ForEach-Object { @{ Name = $_; Type = 1 } })
    Ensure-BitableColumns -AppToken $AppToken -TableId $TableId -Token $Token -Columns $cols -DryRun:$DryRun
}
