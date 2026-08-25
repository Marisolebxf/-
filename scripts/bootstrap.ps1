# gkx-lumen 一键 onboarding 脚本（Windows PowerShell 5.1+）
# 用法：在 gkx-orchestration/ 目录下执行 .\scripts\bootstrap.ps1
# 作用：验证 .env / 装 commit hooks / clone 10 业务子仓 / 提示下一步
# 参数：-Force  跳过路径不匹配检查（不建议，仅在你确认无误时用）

param([switch]$Force)

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " gkx-lumen bootstrap (Windows)" -ForegroundColor Cyan
Write-Host " RFC-002 section-6 onboarding - 1 hour max" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Step 1: 验证 .env
# ============================================================
Write-Host "[1/5] 验证 .env ..." -ForegroundColor Yellow

if (-not (Test-Path ".env")) {
    Write-Host "  [FAIL] .env 不存在" -ForegroundColor Red
    Write-Host "  -> 请先：copy .env.example .env，然后编辑 .env 填写 GKX_ROOT" -ForegroundColor Red
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
    Write-Host "  [FAIL] .env 缺少 GKX_ROOT" -ForegroundColor Red
    Write-Host "  -> 请编辑 .env 填写 GKX_ROOT=<你的工作区根，例 F:/gkx-lumen>" -ForegroundColor Red
    exit 1
}

$gkxRoot = $envVars['GKX_ROOT']
$gitlabBase = if ($envVars.ContainsKey('GKX_GITLAB_BASE')) { $envVars['GKX_GITLAB_BASE'] } else { 'https://gitlab.htmisoft.net' }
$gitlabGroup = if ($envVars.ContainsKey('GKX_GITLAB_GROUP')) { $envVars['GKX_GITLAB_GROUP'] } else { 'gkx-lumen' }

Write-Host "  [OK] GKX_ROOT = $gkxRoot" -ForegroundColor Green
Write-Host "  [OK] GitLab group = $gitlabBase/$gitlabGroup" -ForegroundColor Green

# 验证当前位置是否在 GKX_ROOT 下（强约束：不一致直接 abort，避免误用别处的子仓）
$currentPath = (Get-Location).Path -replace '\\', '/'
$expectedPath = "$gkxRoot/gkx-orchestration"
$currentNorm = $currentPath.TrimEnd('/').ToLower()
$expectedNorm = $expectedPath.TrimEnd('/').ToLower()
if ($currentNorm -ne $expectedNorm) {
    if (-not $Force) {
        Write-Host "  [FAIL] 当前位置 $currentPath" -ForegroundColor Red
        Write-Host "         != .env 期望 $expectedPath" -ForegroundColor Red
        Write-Host ""
        Write-Host "  常见原因 / 修复：" -ForegroundColor Yellow
        Write-Host "    1. 你在错盘符 cd 了主仓 -> cd `"$expectedPath`" 后重跑" -ForegroundColor Yellow
        Write-Host "    2. .env 的 GKX_ROOT 写的是别的机器盘符 -> 编辑 .env 改为本机实际路径" -ForegroundColor Yellow
        Write-Host "       例如本机在 F:\gkx-lumen 下，.env 应写 GKX_ROOT=F:/gkx-lumen" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  若你确认无误（如调试模式），加 -Force 参数重跑：" -ForegroundColor Gray
        Write-Host "    .\scripts\bootstrap.ps1 -Force" -ForegroundColor Gray
        exit 1
    } else {
        Write-Host "  [WARN] 位置不匹配，但 -Force 已指定，继续执行" -ForegroundColor Yellow
    }
}

# ============================================================
# Step 2: 安装 commit hooks
# ============================================================
Write-Host ""
Write-Host "[2/5] 安装 commit hooks ..." -ForegroundColor Yellow

if (Test-Path ".git-template\hooks") {
    git config core.hooksPath .git-template/hooks
    Write-Host "  [OK] 主仓 hooks 已激活（.git-template/hooks）" -ForegroundColor Green
} else {
    Write-Host "  [WARN] .git-template/hooks 不存在，跳过" -ForegroundColor Yellow
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
    $tokenValid = $false
    try {
        $headers = @{ 'PRIVATE-TOKEN' = $token }
        $resp = Invoke-WebRequest -Uri "$gitlabBase/api/v4/user" -Headers $headers -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        $userInfo = ($resp.Content | ConvertFrom-Json)
        $tokenValid = $true
    } catch {
        $tokenValid = $false
    }
    if ($tokenValid) {
        Write-Host "  [OK] Token 有效（user: $($userInfo.username)）" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Token 验证失败" -ForegroundColor Yellow
        Write-Host "      继续 clone 会逐个提示密码 / 失败" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [WARN] 未配置 GKX_GITLAB_TOKEN，clone 时会逐个提示账号密码" -ForegroundColor Yellow
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
    'demo-ui-topic',
    'lumen-ui-topic',
    'lumen-ui-admin',
    'demo-admin-ui',
    'demo-svc-topic-py',
    'lumen-etl-es-py',
    'lumen-algo-py',
    'lumen-ui-algo-apiview',
    'lumen-ui-topic-mobile'

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
        Write-Host "  [SKIP] $repo  (已存在，跳过)" -ForegroundColor Gray
        $skipCount++
        continue
    }

    $url = if ($hasToken) {
        $tk = $envVars['GKX_GITLAB_TOKEN']
        $tu = if ($envVars.ContainsKey('GKX_GITLAB_USER')) { $envVars['GKX_GITLAB_USER'] } else { 'oauth2' }
        "https://${tu}:${tk}@$($gitlabBase -replace 'https://','')/$gitlabGroup/$repo.git"
    } else {
        "$gitlabBase/$gitlabGroup/$repo.git"
    }

    Write-Host "  [CLONE] $repo  ..." -ForegroundColor Cyan -NoNewline
    $cloneOutput = git clone $url $targetPath 2>&1
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        Write-Host " OK" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host " FAIL" -ForegroundColor Red
        $failCount++
        $failedRepos += $repo
    }
}

Write-Host ""
Write-Host "  结果：$successCount 成功 / $skipCount 跳过 / $failCount 失败" -ForegroundColor Cyan
if ($failCount -gt 0) {
    Write-Host "  失败仓：$($failedRepos -join ', ')" -ForegroundColor Red
    Write-Host "  -> 可手动 cd repos/ ; git clone $gitlabBase/$gitlabGroup/<repo>.git 重试" -ForegroundColor Yellow
}

# ============================================================
# Step 5: 提示下一步
# ============================================================
Write-Host ""
Write-Host "[5/5] 下一步 ..." -ForegroundColor Yellow
$workspaceFile = "$gkxRoot/gkx-orchestration/gkx-lumen.code-workspace"
Write-Host "  1. 用 Cursor 打开 multi-root 工作区（推荐，一次看到主仓 + 11 子仓 + worktrees）："
Write-Host "       File -> Open Workspace from File -> $workspaceFile" -ForegroundColor Cyan
Write-Host "     （已自动排除 node_modules/target/.venv，避免索引爆炸；缺失子仓会有 warning，跑 bootstrap 即可补齐）"
Write-Host "  2. 在 Cursor 新开 Agent 会话，输入：你是哪个角色？必读哪些文件？"
Write-Host "  3. 按角色装依赖："
Write-Host "       - 前端：cd repos/<repo-name> ; npm install"
Write-Host "       - 后端：cd repos/lumen-svc-platform ; mvn install -DskipTests"
Write-Host "       - 算法：cd repos/demo-algo-* ; pip install -r requirements.txt"
Write-Host "  4. 跟 mentor 跑首个 task（详见 agent-delivery/team-onboarding.md S2）"
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " bootstrap 完成！" -ForegroundColor Green
Write-Host " 期望用时 - 1 小时（RFC-002 S3 G2 验收标准）" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
