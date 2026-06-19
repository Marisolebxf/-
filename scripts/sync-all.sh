#!/usr/bin/env bash
# 一键 git pull 所有业务子仓 + 主仓
# 用法：./scripts/sync-all.sh [--dry-run]
# 注意：Windows 用 git-bash 跑

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

# 解析 .env
if [[ ! -f ".env" ]]; then
    echo -e "${RED}❌ .env 不存在，请先 cp .env.example .env${NC}"
    exit 1
fi
set -a
source .env
set +a
GKX_ROOT_EXPANDED=$(eval echo "$GKX_ROOT")

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo -e "${YELLOW}[DRY-RUN 模式：仅显示要做什么，不真的 pull]${NC}"
fi

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} gkx-lumen sync-all${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# 主仓 + 业务子仓列表
declare -a repos=(
    "$GKX_ROOT_EXPANDED/gkx-orchestration|主仓"
    "$GKX_ROOT_EXPANDED/repos/demo-ui-science|demo-ui-science"
    "$GKX_ROOT_EXPANDED/repos/demo-algo-ent-analysis|demo-algo-ent-analysis"
    "$GKX_ROOT_EXPANDED/repos/dataease|dataease"
    "$GKX_ROOT_EXPANDED/repos/demo-ui-system-test|demo-ui-system-test"
    "$GKX_ROOT_EXPANDED/repos/lumen-svc-platform|lumen-svc-platform"
    "$GKX_ROOT_EXPANDED/repos/lumen-ui-science-pc|lumen-ui-science-pc"
    "$GKX_ROOT_EXPANDED/repos/lumen-ui-science-mobile|lumen-ui-science-mobile"
    "$GKX_ROOT_EXPANDED/repos/demo-svc-platform|demo-svc-platform"
    "$GKX_ROOT_EXPANDED/repos/demo-algo-science|demo-algo-science"
    "$GKX_ROOT_EXPANDED/repos/demo-ui-topic|demo-ui-topic"
)

total=0
ok=0
skipped=0
dirty=0
failed=0
dirty_repos=()
failed_repos=()

for entry in "${repos[@]}"; do
    path="${entry%|*}"
    name="${entry#*|}"
    total=$((total + 1))
    
    if [[ ! -d "$path/.git" ]]; then
        echo -e "  ${GRAY}⏭  $name  (不存在，跳过；运行 bootstrap.sh 创建)${NC}"
        skipped=$((skipped + 1))
        continue
    fi
    
    # 检查工作区是否 dirty
    if [[ -n "$(git -C "$path" status --porcelain 2>/dev/null)" ]]; then
        echo -e "  ${YELLOW}⚠️  $name  (工作区 dirty，跳过 pull)${NC}"
        dirty=$((dirty + 1))
        dirty_repos+=("$name")
        continue
    fi
    
    # 获取当前分支
    branch=$(git -C "$path" rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')
    
    if $DRY_RUN; then
        echo -e "  ${CYAN}🔍  $name  (${branch}) - DRY-RUN${NC}"
        ok=$((ok + 1))
    else
        echo -ne "  ${CYAN}⏳  $name  (${branch}) ...${NC}"
        if git -C "$path" pull --ff-only > /dev/null 2>&1; then
            echo -e " ${GREEN}✅${NC}"
            ok=$((ok + 1))
        else
            echo -e " ${RED}❌（非 fast-forward 或 fetch 失败）${NC}"
            failed=$((failed + 1))
            failed_repos+=("$name")
        fi
    fi
done

echo ""
echo -e "${CYAN}总览：${NC}"
echo -e "  总: $total  /  成功: ${GREEN}$ok${NC}  /  跳过: ${GRAY}$skipped${NC}  /  dirty: ${YELLOW}$dirty${NC}  /  失败: ${RED}$failed${NC}"

if [[ $dirty -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}dirty 仓（需手动 commit / stash / discard）：${dirty_repos[*]}${NC}"
fi
if [[ $failed -gt 0 ]]; then
    echo ""
    echo -e "${RED}失败仓：${failed_repos[*]}${NC}"
    echo -e "${YELLOW}→ 可能是非 fast-forward，需手动 git pull --rebase${NC}"
fi
