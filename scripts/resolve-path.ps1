# 打印 .env 解析后的路径（供 agent / 人类核对）
# 用法：在 gkx-orchestration/ 根目录执行 .\scripts\resolve-path.ps1

. "$PSScriptRoot\lib\load-env.ps1"

Write-Host "=== gkx-lumen path resolution (from .env) ===" -ForegroundColor Cyan
Write-Host "GKX_ROOT              = $GKX_ROOT_EXPANDED"
Write-Host "GKX_ORCHESTRATION_DIR = $GKX_ORCHESTRATION_DIR"
Write-Host "GKX_REPOS_DIR         = $GKX_REPOS_DIR"
Write-Host "GKX_WORKTREES_DIR     = $GKX_WORKTREES_DIR"
Write-Host "GKX_AGENT_DELIVERY    = $GKX_AGENT_DELIVERY_DIR"
Write-Host "GKX_DOCS_ROOT         = $(if ($GKX_DOCS_ROOT) { $GKX_DOCS_ROOT } else { '<not set>' })"
Write-Host "GKX_GITLAB            = $GKX_GITLAB_BASE/$GKX_GITLAB_GROUP"
Write-Host ""
Write-Host "Key repos:"
@('demo-ui-science','demo-ui-topic','lumen-svc-platform','lumen-ui-science-pc','demo-svc-platform','demo-algo-science') | ForEach-Object {
    Write-Host "  $_ -> $GKX_REPOS_DIR\$_"
}
