#!/usr/bin/env bash
# 打印 .env 解析后的路径（供 agent / 人类核对）
# 用法：在 gkx-orchestration/ 根目录执行 ./scripts/resolve-path.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/load-env.sh
source "$SCRIPT_DIR/lib/load-env.sh"

echo "=== gkx-lumen path resolution (from .env) ==="
echo "GKX_ROOT              = $GKX_ROOT_EXPANDED"
echo "GKX_ORCHESTRATION_DIR = $GKX_ORCHESTRATION_DIR"
echo "GKX_REPOS_DIR         = $GKX_REPOS_DIR"
echo "GKX_WORKTREES_DIR     = $GKX_WORKTREES_DIR"
echo "GKX_AGENT_DELIVERY    = $GKX_AGENT_DELIVERY_DIR"
echo "GKX_DOCS_ROOT         = ${GKX_DOCS_ROOT:-<not set>}"
echo "GKX_GITLAB            = $GKX_GITLAB_BASE/$GKX_GITLAB_GROUP"
echo ""
echo "Key repos:"
for repo in demo-ui-science demo-ui-topic lumen-svc-platform lumen-ui-science-pc demo-svc-platform demo-algo-science; do
    echo "  $repo -> $GKX_REPOS_DIR/$repo"
done
