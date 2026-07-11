# 飞书项目 OpenAPI 薄封装（PowerShell）
# 文档：agent-delivery/feishu-project-integration.md

function Get-FeishuProjectConfig {
    param([string]$ConfigPath)
    if (-not (Test-Path $ConfigPath)) {
        throw "Config not found: $ConfigPath"
    }
    # 简易 YAML 读取（仅解析 sync/project 段用到的键）
    $raw = Get-Content $ConfigPath -Raw -Encoding UTF8
    $cfg = [ordered]@{
        Host = 'project.feishu.cn'
        ProjectKey = ''
        WorkItemTypeKey = 'story'
        SyncEnabled = $false
        DryRunDefault = $true
        ExternalFieldKey = ''
        ExternalFieldAlias = 'gkx_task_id'
        RateLimitMs = 300
    }
    if ($raw -match '(?m)^\s+host:\s*(.+)$') { $cfg.Host = $matches[1].Trim().Trim('"') }
    if ($raw -match '(?m)^\s+project_key:\s*"(.*)"') { $cfg.ProjectKey = $matches[1] }
    if ($raw -match '(?m)^\s+work_item_type_key:\s*"(.+)"') { $cfg.WorkItemTypeKey = $matches[1].Trim() }
    if ($raw -match '(?m)^\s+enabled:\s*(true|false)') { $cfg.SyncEnabled = ($matches[1] -eq 'true') }
    if ($raw -match '(?m)^\s+dry_run_default:\s*(true|false)') { $cfg.DryRunDefault = ($matches[1] -eq 'true') }
    if ($raw -match '(?m)^\s+feishu_field_key:\s*"(.*)"') { $cfg.ExternalFieldKey = $matches[1] }
    if ($raw -match '(?m)^\s+feishu_field_alias:\s*(.+)$') { $cfg.ExternalFieldAlias = $matches[1].Trim() }
    if ($raw -match '(?m)^\s+rate_limit_ms:\s*(\d+)') { $cfg.RateLimitMs = [int]$matches[1] }
    return [pscustomobject]$cfg
}

function Get-FeishuEnv {
    $pluginId = $env:FEISHU_PROJECT_PLUGIN_ID
    $pluginSecret = $env:FEISHU_PROJECT_PLUGIN_SECRET
    $userKey = $env:FEISHU_PROJECT_USER_KEY
    if (-not $pluginId -or -not $pluginSecret -or -not $userKey) {
        throw @"
Missing Feishu Project credentials. Set in gkx-orchestration/.env:
  FEISHU_PROJECT_PLUGIN_ID
  FEISHU_PROJECT_PLUGIN_SECRET
  FEISHU_PROJECT_USER_KEY
See agent-delivery/feishu-project-integration.md §2
"@
    }
    return [pscustomobject]@{
        PluginId = $pluginId
        PluginSecret = $pluginSecret
        UserKey = $userKey
    }
}

function Get-FeishuPluginToken {
    param(
        [string]$HostName = 'project.feishu.cn',
        [string]$PluginId,
        [string]$PluginSecret
    )
    $uri = "https://$HostName/open_api/authen/plugin_token"
    $body = @{
        plugin_id = $PluginId
        plugin_secret = $PluginSecret
        type = 0
    } | ConvertTo-Json
    $resp = Invoke-RestMethod -Method Post -Uri $uri -Body $body -ContentType 'application/json; charset=utf-8'
    if (-not $resp.data.token) {
        throw "Failed to get plugin_token: $($resp | ConvertTo-Json -Compress)"
    }
    return $resp.data.token
}

function Invoke-FeishuProjectApi {
    param(
        [string]$Method,
        [string]$HostName,
        [string]$Path,
        [string]$Token,
        [string]$UserKey,
        [object]$Body = $null
    )
    $uri = "https://$HostName$Path"
    $headers = @{
        'X-PLUGIN-TOKEN' = $Token
        'X-USER-KEY' = $UserKey
        'Content-Type' = 'application/json; charset=utf-8'
    }
    $params = @{
        Method = $Method
        Uri = $uri
        Headers = $headers
    }
    if ($null -ne $Body) {
        $params.Body = ($Body | ConvertTo-Json -Depth 10 -Compress)
    }
    try {
        return Invoke-RestMethod @params
    }
    catch {
        $errBody = $_.ErrorDetails.Message
        throw "Feishu API $Method $Path failed: $errBody"
    }
}

function New-FeishuWorkItem {
    param(
        [string]$HostName,
        [string]$ProjectKey,
        [string]$Token,
        [string]$UserKey,
        [string]$WorkItemTypeKey,
        [string]$Name,
        [array]$FieldValuePairs = @()
    )
    $path = "/open_api/$ProjectKey/work_item/create"
    $body = @{
        work_item_type_key = $WorkItemTypeKey
        name = $Name
    }
    if ($FieldValuePairs.Count -gt 0) {
        $body.field_value_pairs = $FieldValuePairs
    }
    return Invoke-FeishuProjectApi -Method Post -HostName $HostName -Path $path -Token $Token -UserKey $UserKey -Body $body
}

function Update-FeishuWorkItem {
    param(
        [string]$HostName,
        [string]$ProjectKey,
        [string]$Token,
        [string]$UserKey,
        [string]$WorkItemTypeKey,
        [long]$WorkItemId,
        [array]$FieldValuePairs = @(),
        [string]$StateKey = ''
    )
    $path = "/open_api/$ProjectKey/work_item/$WorkItemTypeKey/$WorkItemId"
    $body = @{}
    if ($FieldValuePairs.Count -gt 0) {
        $body.field_value_pairs = $FieldValuePairs
    }
    if ($StateKey) {
        $body.state_key = $StateKey
    }
    return Invoke-FeishuProjectApi -Method Put -HostName $HostName -Path $path -Token $Token -UserKey $UserKey -Body $body
}

function Search-FeishuWorkItemByExternalId {
    param(
        [string]$HostName,
        [string]$ProjectKey,
        [string]$Token,
        [string]$UserKey,
        [string]$WorkItemTypeKey,
        [string]$ExternalFieldKey,
        [string]$TaskId
    )
    if (-not $ExternalFieldKey) { return $null }
    $path = "/open_api/$ProjectKey/work_item/$WorkItemTypeKey/search/params"
    $body = @{
        search_group = @{
            conjunction = 'AND'
            search_params = @(
                @{
                    param_key = $ExternalFieldKey
                    value = $TaskId
                    operator = 'EQ'
                }
            )
        }
        page_num = 1
        page_size = 5
    }
    try {
        $resp = Invoke-FeishuProjectApi -Method Post -HostName $HostName -Path $path -Token $Token -UserKey $UserKey -Body $body
        if ($resp.data -and $resp.data.Count -gt 0) {
            return $resp.data[0]
        }
    }
    catch {
        Write-Warning "Search failed for $TaskId : $_"
    }
    return $null
}

function Get-FeishuWorkItemTypes {
    param(
        [string]$HostName,
        [string]$ProjectKey,
        [string]$Token,
        [string]$UserKey
    )
    $path = "/open_api/$ProjectKey/work_item/all-types"
    return Invoke-FeishuProjectApi -Method Get -HostName $HostName -Path $path -Token $Token -UserKey $UserKey
}

function Get-FeishuWorkItemMeta {
    param(
        [string]$HostName,
        [string]$ProjectKey,
        [string]$Token,
        [string]$UserKey,
        [string]$WorkItemTypeKey
    )
    $path = "/open_api/$ProjectKey/work_item/$WorkItemTypeKey/meta"
    return Invoke-FeishuProjectApi -Method Get -HostName $HostName -Path $path -Token $Token -UserKey $UserKey
}
