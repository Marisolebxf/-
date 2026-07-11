# 从 gkx-orchestration/.env 加载环境变量（RFC-002 §6 路径真源）
# 用法（在主仓根目录）：
#   . .\scripts\lib\load-env.ps1
#   . .\scripts\lib\load-env.ps1 -OrchestrationDir E:\gkx-lumen\gkx-orchestration

param(
    [string]$OrchestrationDir = ""
)

function Import-GkxEnv {
    param([string]$RootDir)

    if ([string]::IsNullOrWhiteSpace($RootDir)) {
        if ((Test-Path ".env") -and (Test-Path "agent-delivery")) {
            $RootDir = (Get-Location).Path
        } else {
            $RootDir = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
        }
    }

    $envFile = Join-Path $RootDir ".env"
    if (-not (Test-Path $envFile)) {
        throw "load-env.ps1: missing $envFile (copy from .env.example)"
    }

    $script:GKX_ENV = @{}
    Get-Content $envFile | Where-Object { $_ -match '^\s*[^#]' -and $_ -match '=' } | ForEach-Object {
        $kv = $_ -split '=', 2
        if ($kv.Length -eq 2) {
            $key = $kv[0].Trim()
            $val = $kv[1].Trim().Trim('"').Trim("'")
            $script:GKX_ENV[$key] = $val
        }
    }

    if (-not $script:GKX_ENV.ContainsKey('GKX_ROOT') -or [string]::IsNullOrWhiteSpace($script:GKX_ENV['GKX_ROOT'])) {
        throw "load-env.ps1: GKX_ROOT is required in $envFile"
    }

    $global:GKX_ROOT = $script:GKX_ENV['GKX_ROOT']
    $global:GKX_ROOT_EXPANDED = $global:GKX_ROOT
    $global:GKX_ORCHESTRATION_DIR = Join-Path $global:GKX_ROOT_EXPANDED "gkx-orchestration"
    $global:GKX_REPOS_DIR = Join-Path $global:GKX_ROOT_EXPANDED "repos"
    $global:GKX_WORKTREES_DIR = Join-Path $global:GKX_ROOT_EXPANDED "worktrees"
    $global:GKX_AGENT_DELIVERY_DIR = Join-Path $global:GKX_ORCHESTRATION_DIR "agent-delivery"

    $global:GKX_DOCS_ROOT = $script:GKX_ENV['GKX_DOCS_ROOT']
    $global:GKX_GITLAB_BASE = if ($script:GKX_ENV.ContainsKey('GKX_GITLAB_BASE')) { $script:GKX_ENV['GKX_GITLAB_BASE'] } else { 'https://gitlab.htmisoft.net' }
    $global:GKX_GITLAB_GROUP = if ($script:GKX_ENV.ContainsKey('GKX_GITLAB_GROUP')) { $script:GKX_ENV['GKX_GITLAB_GROUP'] } else { 'gkx-lumen' }
    $global:GKX_GITLAB_USER = $script:GKX_ENV['GKX_GITLAB_USER']
    $global:GKX_GITLAB_TOKEN = $script:GKX_ENV['GKX_GITLAB_TOKEN']

    foreach ($key in $script:GKX_ENV.Keys) {
        Set-Item -Path "env:$key" -Value $script:GKX_ENV[$key]
    }
}

Import-GkxEnv -RootDir $OrchestrationDir
