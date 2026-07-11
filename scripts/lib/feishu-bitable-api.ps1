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
        StatusMap = @{}
    }
    if ($raw -match '(?m)^\s+app_token:\s*"(.*)"') { $cfg.AppToken = $matches[1] }
    if ($raw -match '(?m)^\s+table_id:\s*"(.*)"') { $cfg.TableId = $matches[1] }
    if ($raw -match '(?m)^\s+enabled:\s*(true|false)') { $cfg.SyncEnabled = ($matches[1] -eq 'true') }
    if ($raw -match '(?m)^\s+dry_run_default:\s*(true|false)') { $cfg.DryRunDefault = ($matches[1] -eq 'true') }
    if ($raw -match '(?m)^\s+rate_limit_ms:\s*(\d+)') { $cfg.RateLimitMs = [int]$matches[1] }
    if ($raw -match '(?m)^\s+task_id:\s*"(.+)"') { $cfg.FieldTaskId = $matches[1] }
    if ($raw -match '(?m)^\s+title:\s*"(.+)"') { $cfg.FieldTitle = $matches[1] }
    if ($raw -match '(?m)^\s+status:\s*"(.+)"') { $cfg.FieldStatus = $matches[1] }
    foreach ($m in [regex]::Matches($raw, '(?m)^\s+(backlog|ready|claimed|in_progress|review|done|blocked):\s*"(.+)"')) {
        $cfg.StatusMap[$m.Groups[1].Value] = $m.Groups[2].Value.Trim()
    }
    return [pscustomobject]$cfg
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
        [object]$Body = $null
    )
    $uri = "https://open.feishu.cn/open-apis$Path"
    $headers = @{ Authorization = "Bearer $Token"; 'Content-Type' = 'application/json; charset=utf-8' }
    $params = @{ Method = $Method; Uri = $uri; Headers = $headers }
    if ($null -ne $Body) { $params.Body = ($Body | ConvertTo-Json -Depth 12 -Compress) }
    try {
        $resp = Invoke-RestMethod @params
        if ($resp.code -ne 0) { throw "code=$($resp.code) msg=$($resp.msg)" }
        return $resp
    }
    catch {
        throw "Feishu OpenAPI $Method $Path failed: $_"
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

function New-BitableRecord {
    param(
        [string]$AppToken, [string]$TableId, [string]$Token,
        [hashtable]$Fields
    )
    $path = "/bitable/v1/apps/$AppToken/tables/$TableId/records"
    $body = @{ fields = $Fields }
    $resp = Invoke-FeishuOpenApi -Method Post -Path $path -Token $Token -Body $body
    return $resp.data.record
}

function Update-BitableRecord {
    param(
        [string]$AppToken, [string]$TableId, [string]$Token,
        [string]$RecordId, [hashtable]$Fields
    )
    $path = "/bitable/v1/apps/$AppToken/tables/$TableId/records/$RecordId"
    $body = @{ fields = $Fields }
    $resp = Invoke-FeishuOpenApi -Method Put -Path $path -Token $Token -Body $body
    return $resp.data.record
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
