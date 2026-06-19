# gkx-lumen 一键 onboarding 脚本（Windows PowerShell）
# 用法：在 gkx-orchestration/ 目录下执行 .\scripts\bootstrap.ps1
# 作用：验证 .env / 装 commit hooks / clone 10 业务子仓 / 提示下一步

$ErrorActionPreference = "Stop"
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " gkx-lumen bootstrap (Windows)" -ForegroundColor Cyan
Write-Host " RFC-002 §6 onboarding ≤ 1 hour" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Step 1: 验证 .env
# ============================================================
Write-Host "[1/5] 验证 .env ..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Write-Host "  ❌ .env 不存在" -ForegroundColor Red
    Write-Host "  → 请先：copy .env.example .env，然后编辑 .env 填写 GKX_ROOT" -ForegroundColor Red
    exit 1
}

# 读取 .env 到环境变量（简单解析）
$envVars = @{}
Get-Content .env | Where-Object { $_ -match '^\s*[^#]' -and $_ -match '=' } | ForEach-Object {
    $kv = $_ -split '=', 2
    if ($kv.Length -eq 2) {
        $key = $kv[0].Trim()
        $val = $kv[1].Trim().Trim('"').Trim("'")
        $envVars[$key] = $val
    }
}

if (-not $envVars.ContainsKey('GKX_ROOT') -or [string]::IsNullOrWhiteSpace($envVars['GKX_ROOT'])) {
    Write-Host "  ❌ .env 缺少 GKX_ROOT" -ForegroundColor Red
    Write-Host "  → 请编辑 .env 填写 GKX_ROOT=<你的工作区根，例 E:/gkx-lumen>" -ForegroundColor Red
    exit 1
}

$gkxRoot = $envVars['GKX_ROOT']
$gitlabBase = if ($envVars.ContainsKey('GKX_GITLAB_BASE')) { $envVars['GKX_GITLAB_BASE'] } else { 'https://gitlab.htmisoft.net' }
$gitlabGroup = if ($envVars.ContainsKey('GKX_GITLAB_GROUP')) { $envVars['GKX_GITLAB_GROUP'] } else { 'gkx-lumen' }

Write-Host "  ✅ GKX_ROOT = $gkxRoot" -ForegroundColor Green
Write-Host "  ✅ GitLab group = $gitlabBase/$gitlabGroup" -ForegroundColor Green

# 验证当前位置是否在 GKX_ROOT 下
$currentPath = (Get-Location).Path -replace '\\', '/'
$expectedPath = "$gkxRoot/gkx-orchestration"
if ($currentPath -notlike "*$($expectedPath -replace ':', '*')*") {
    Write-Host "  ⚠️  当前位置 $currentPath 不在 $expectedPath 下" -ForegroundColor Yellow
    Write-Host "      继续？这可能引起路径混乱（按 Ctrl+C 退出，或 Enter 继续）"
    Read-Host
}

# ============================================================
# Step 2: 安装 commit hooks
# ============================================================
Write-Host ""
Write-Host "[2/5] 安装 commit hooks ..." -ForegroundColor Yellow

if (Test-Path ".git-template\hooks") {
    git config core.hooksPath .git-template/hooks
    Write-Host "  ✅ 主仓 hooks 已激活（.git-template/hooks）" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  .git-template/hooks 不存在，跳过" -ForegroundColor Yellow
}

# ============================================================
# Step 3: 验证 GitLab 凭据（如有 TOKEN）
# ============================================================
Write-Host ""
Write-Host "[3/5] 验证 GitLab 凭据 ..." -ForegroundColor Yellow

$hasToken = $envVars.ContainsKey('GKX_GITLAB_TOKEN') -and -not [string]::IsNullOrWhiteSpace($envVars['GKX_GITLAB_TOKEN'])
if ($hasToken) {
    $token = $envVars['GKX_GITLAB_TOKEN']
    $user = if ($envVars.ContainsKey('GKX_GITLAB_USER')) { $envVars['GKX_GITLAB_USER'] } else { 'oauth2' }
    # 测试 token 是否有效（API call）
    try {
        $headers = @{ 'PRIVATE-TOKEN' = $token }
        $resp = Invoke-WebRequest -Uri "$gitlabBase/api/v4/user" -Headers $headers -UseBasicParsing -TimeoutSec 10
        $userInfo = ($resp.Content | ConvertFrom-Json)
        Write-Host "  ✅ Token 有效（user: $($userInfo.username)）" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  Token 验证失败：$_" -ForegroundColor Yellow
        Write-Host "      继续 clone 会逐个提示密码 / 失败" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  未配置 GKX_GITLAB_TOKEN，clone 时会逐个提示账号密码" -ForegroundColor Yellow
}

# ============================================================
# Step 4: clone 10 个业务子仓
# ============================================================
Write-Host ""
Write-Host "[4/5] clone 10 个业务子仓 ..." -ForegroundColor Yellow

$repos = @(
    'demo-ui-science',
    'demo-algo-ent-analysis',
    'dataease',
    'demo-ui-system-test',
    'lumen-svc-platform',
    'lumen-ui-science-pc',
    'lumen-ui-science-mobile',
    'demo-svc-platform',
    'demo-algo-science',
    'demo-ui-topic'
)

$reposDir = "$gkxRoot/repos"
if (-not (Test-Path $reposDir)) {
    New-Item -ItemType Directory -Path $reposDir -Force | Out-Null
}

$successCount = 0
$skipCount = 0
$failCount = 0
$failedRepos = @()

foreach ($repo in $repos) {
    $targetPath = "$reposDir/$repo"
    if (Test-Path $targetPath) {
        Write-Host "  ⏭  $repo  (已存在，跳过)" -ForegroundColor Gray
        $skipCount++
        continue
    }
    
    $url = if ($hasToken) {
        $token = $envVars['GKX_GITLAB_TOKEN']
        $user = if ($envVars.ContainsKey('GKX_GITLAB_USER')) { $envVars['GKX_GITLAB_USER'] } else { 'oauth2' }
        "https://${user}:${token}@$($gitlabBase -replace 'https://','')/$gitlabGroup/$repo.git"
    } else {
        "$gitlabBase/$gitlabGroup/$repo.git"
    }
    
    Write-Host "  ⏳  $repo  ..." -ForegroundColor Cyan -NoNewline
    try {
        git clone $url $targetPath 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host " ✅" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host " ❌" -ForegroundColor Red
            $failCount++
            $failedRepos += $repo
        }
    } catch {
        Write-Host " ❌ $_" -ForegroundColor Red
        $failCount++
        $failedRepos += $repo
    }
}

Write-Host ""
Write-Host "  结果：$successCount 成功 / $skipCount 跳过 / $failCount 失败" -ForegroundColor Cyan
if ($failCount -gt 0) {
    Write-Host "  失败仓：$($failedRepos -join ', ')" -ForegroundColor Red
    Write-Host "  → 可手动 cd repos/ && git clone $gitlabBase/$gitlabGroup/<repo>.git 重试" -ForegroundColor Yellow
}

# ============================================================
# Step 5: 提示下一步
# ============================================================
Write-Host ""
Write-Host "[5/5] 下一步 ..." -ForegroundColor Yellow
Write-Host "  1. 用 Cursor 打开 $gkxRoot 工作区（File → Open Folder）"
Write-Host "  2. 在 Cursor 新开 Agent 会话，输入：'你是哪个角色？必读哪些文件？'"
Write-Host "  3. 按角色装依赖："
Write-Host "       - 前端：cd repos/<repo-name> && npm install"
Write-Host "       - 后端：cd repos/lumen-svc-platform && mvn install -DskipTests"
Write-Host "       - 算法：cd repos/demo-algo-* && pip install -r requirements.txt"
Write-Host "  4. 跟 mentor 跑首个 task（详见 agent-delivery/team-onboarding.md §2）"
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " bootstrap 完成！" -ForegroundColor Green
Write-Host " 期望用时 ≤ 1 小时（RFC-002 §3 G2 验收标准）" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
