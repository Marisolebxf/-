# Worktree 管理工具：统一在 ${GKX_ROOT}/worktrees/ 下管理
# Mac / Linux 对等脚本：scripts/worktree-helper.sh
#
# 用法：
#   .\scripts\worktree-helper.ps1 add <repo> <slug> [branch]   创建 worktree
#   .\scripts\worktree-helper.ps1 list                          列出所有 worktree
#   .\scripts\worktree-helper.ps1 remove <repo> <slug>          清理 worktree
#   .\scripts\worktree-helper.ps1 prune                         清理失效 worktree
#
# 命名：{repo}--{slug}/
#   例：gkx-orchestration--pol-l2-ds10-accept
#       demo-ui-topic--E-ENT-IA
# 默认分支：wt/{slug}（基于 origin/dev）

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("add", "list", "ls", "remove", "rm", "prune", "help", "--help", "-h", "")]
    [string]$Command = "help",

    [Parameter(Position = 1)]
    [string]$Repo = "",

    [Parameter(Position = 2)]
    [string]$Slug = "",

    [Parameter(Position = 3)]
    [string]$Branch = ""
)

$ErrorActionPreference = "Stop"

function Write-Info([string]$Message) { Write-Host $Message -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host $Message -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host $Message -ForegroundColor Yellow }
function Write-Err([string]$Message) { Write-Host $Message -ForegroundColor Red }

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OrchRoot = Resolve-Path (Join-Path $ScriptDir "..")

function Get-DotEnvPath {
    $candidates = @(
        (Join-Path $OrchRoot ".env"),
        (Join-Path (Get-Location) ".env")
    )
    foreach ($p in $candidates) {
        if (Test-Path -LiteralPath $p) { return $p }
    }
    return $null
}

function Import-DotEnv([string]$Path) {
    Get-Content -LiteralPath $Path -Encoding UTF8 | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $idx = $line.IndexOf("=")
        if ($idx -lt 1) { return }
        $key = $line.Substring(0, $idx).Trim()
        $val = $line.Substring($idx + 1).Trim()
        if (($val.StartsWith('"') -and $val.EndsWith('"')) -or ($val.StartsWith("'") -and $val.EndsWith("'"))) {
            $val = $val.Substring(1, $val.Length - 2)
        }
        Set-Item -Path "Env:$key" -Value $val
    }
}

$envFile = Get-DotEnvPath
if (-not $envFile) {
    Write-Err ".env 不存在，请先在 gkx-orchestration 根目录 cp .env.example .env"
    exit 1
}
Import-DotEnv $envFile

if (-not $env:GKX_ROOT) {
    Write-Err ".env 未设置 GKX_ROOT"
    exit 1
}

$GkxRoot = $env:GKX_ROOT.TrimEnd("/", "\")
$ReposDir = Join-Path $GkxRoot "repos"
$WorktreesDir = Join-Path $GkxRoot "worktrees"
$OrchDir = Join-Path $GkxRoot "gkx-orchestration"
New-Item -ItemType Directory -Force -Path $WorktreesDir | Out-Null

function Resolve-RepoPath([string]$Name) {
    if ($Name -eq "gkx-orchestration") { return $OrchDir }
    return (Join-Path $ReposDir $Name)
}

function Test-GitRepo([string]$Path) {
    return (Test-Path -LiteralPath (Join-Path $Path ".git"))
}

function Show-Usage {
    @"
worktree-helper - gkx-lumen worktree 管理（Windows PowerShell）
Mac / Linux 请用：./scripts/worktree-helper.sh

用法:
  .\scripts\worktree-helper.ps1 add <repo> <slug> [branch]   创建（branch 默认 wt/{slug}）
    例：.\scripts\worktree-helper.ps1 add gkx-orchestration pol-doc-fix
    例：.\scripts\worktree-helper.ps1 add demo-ui-topic E-ENT-IA feat/ent-elements
  .\scripts\worktree-helper.ps1 list
  .\scripts\worktree-helper.ps1 remove <repo> <slug>
  .\scripts\worktree-helper.ps1 prune
  .\scripts\worktree-helper.ps1 help

命名：{repo}--{slug}
基线：新分支一律基于 origin/dev
位置：$WorktreesDir
"@ | Write-Host
}

function Invoke-Git {
    param(
        [string]$WorkingDirectory,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$GitArgs
    )
    & git -C $WorkingDirectory @GitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "git $($GitArgs -join ' ') 失败 (exit $LASTEXITCODE) @ $WorkingDirectory"
    }
}

function Test-GitRef([string]$RepoPath, [string]$Ref) {
    & git -C $RepoPath show-ref --verify --quiet $Ref
    return ($LASTEXITCODE -eq 0)
}

function Add-Worktree {
    if (-not $Repo -or -not $Slug) {
        Write-Err "用法：.\scripts\worktree-helper.ps1 add <repo> <slug> [branch]"
        exit 1
    }
    if (-not $Branch) { $Branch = "wt/$Slug" }

    $repoPath = Resolve-RepoPath $Repo
    $wtName = "$Repo--$Slug"
    $wtPath = Join-Path $WorktreesDir $wtName

    if (-not (Test-GitRepo $repoPath)) {
        Write-Err "仓不存在或不是 git 仓：$repoPath"
        exit 1
    }
    if (Test-Path -LiteralPath $wtPath) {
        Write-Warn "worktree 已存在：$wtPath"
        exit 1
    }

    Write-Info "创建 worktree: $wtName"
    Write-Host "  仓: $Repo"
    Write-Host "  slug: $Slug"
    Write-Host "  分支: $Branch"
    Write-Host "  位置: $wtPath"
    Write-Host ""

    try {
        Invoke-Git $repoPath fetch origin dev --quiet
    } catch {
        try { Invoke-Git $repoPath fetch origin --quiet } catch { Write-Warn "fetch 失败，继续用本地基线" }
    }

    if (Test-GitRef $repoPath "refs/heads/$Branch") {
        Invoke-Git $repoPath worktree add $wtPath $Branch
    } elseif (Test-GitRef $repoPath "refs/remotes/origin/$Branch") {
        Invoke-Git $repoPath worktree add -b $Branch $wtPath "origin/$Branch"
    } else {
        $baseRef = "origin/dev"
        if (-not (Test-GitRef $repoPath "refs/remotes/origin/dev")) {
            if (Test-GitRef $repoPath "refs/heads/dev") {
                $baseRef = "dev"
            } else {
                Write-Err "找不到 origin/dev（或本地 dev），无法创建分支 $Branch"
                exit 1
            }
        }
        Write-Warn "分支 $Branch 不存在，从 $baseRef 创建"
        Invoke-Git $repoPath worktree add -b $Branch $wtPath $baseRef
    }

    Write-Host ""
    Write-Ok "worktree 创建成功"
    Write-Info "→ cd $wtPath"
}

function List-Worktrees {
    Write-Info "=== 所有 gkx-lumen worktrees ==="
    if (-not (Test-Path -LiteralPath $WorktreesDir) -or -not (Get-ChildItem -LiteralPath $WorktreesDir -Force -ErrorAction SilentlyContinue)) {
        Write-Warn "（空）"
        return
    }
    Get-ChildItem -LiteralPath $WorktreesDir -Directory | ForEach-Object {
        $branch = "?"
        if (Test-Path -LiteralPath (Join-Path $_.FullName ".git")) {
            $branch = (& git -C $_.FullName rev-parse --abbrev-ref HEAD 2>$null)
            if (-not $branch) { $branch = "?" }
        }
        Write-Host ("  ● {0}  ({1})" -f $_.Name, $branch) -ForegroundColor Green
    }
}

function Remove-Worktree {
    if (-not $Repo -or -not $Slug) {
        Write-Err "用法：.\scripts\worktree-helper.ps1 remove <repo> <slug>"
        exit 1
    }
    $wtName = "$Repo--$Slug"
    $wtPath = Join-Path $WorktreesDir $wtName
    $repoPath = Resolve-RepoPath $Repo

    if (-not (Test-Path -LiteralPath $wtPath)) {
        Write-Err "worktree 不存在：$wtPath"
        exit 1
    }

    $dirty = (& git -C $wtPath status --porcelain 2>$null)
    if ($dirty) {
        Write-Warn "worktree 有未提交改动：$wtPath"
        $confirm = Read-Host "强制删除？(y/N)"
        if ($confirm -ne "y" -and $confirm -ne "Y") { exit 1 }
        Invoke-Git $repoPath worktree remove --force $wtPath
    } else {
        Invoke-Git $repoPath worktree remove $wtPath
    }
    Write-Ok "清理：$wtName"
}

function Prune-Worktrees {
    Write-Info "=== 清理失效 worktree ==="
    if (Test-GitRepo $OrchDir) {
        Invoke-Git $OrchDir worktree prune
        Write-Ok "  gkx-orchestration"
    }
    if (Test-Path -LiteralPath $ReposDir) {
        Get-ChildItem -LiteralPath $ReposDir -Directory | ForEach-Object {
            if (-not (Test-GitRepo $_.FullName)) { return }
            Invoke-Git $_.FullName worktree prune
            Write-Ok ("  {0}" -f $_.Name)
        }
    }
}

switch ($Command) {
    "add" { Add-Worktree }
    { $_ -in @("list", "ls") } { List-Worktrees }
    { $_ -in @("remove", "rm") } { Remove-Worktree }
    "prune" { Prune-Worktrees }
    default { Show-Usage }
}
