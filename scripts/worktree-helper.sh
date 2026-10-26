#!/usr/bin/env bash
# Worktree 管理工具：统一在 ${GKX_ROOT}/worktrees/ 下管理
# 用法：
#   ./scripts/worktree-helper.sh add <repo> <epic> <branch>      创建 worktree
#   ./scripts/worktree-helper.sh list                            列出所有 worktree
#   ./scripts/worktree-helper.sh remove <repo> <epic>            清理 worktree
#   ./scripts/worktree-helper.sh prune                           清理失效 worktree
# 命名约定：{repo}--{epic}/   例：demo-ui-topic--E-ENT-IA/

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 加载 .env
if [[ ! -f ".env" ]]; then
    echo -e "${RED}❌ .env 不存在，请先 cp .env.example .env${NC}"
    exit 1
fi
set -a
source .env
set +a
GKX_ROOT_EXPANDED=$(eval echo "$GKX_ROOT")

REPOS_DIR="$GKX_ROOT_EXPANDED/repos"
WORKTREES_DIR="$GKX_ROOT_EXPANDED/worktrees"
mkdir -p "$WORKTREES_DIR"

usage() {
    cat <<EOF
worktree-helper - gkx-lumen worktree 管理

用法:
  $0 add <repo> <epic> <branch>      创建 worktree
                                     例：$0 add demo-ui-topic E-ENT-IA feat/ent-elements
  $0 list                            列出所有 worktree
  $0 remove <repo> <epic>            清理 worktree（包括目录）
  $0 prune                           git worktree prune（清理失效引用）
  $0 --help                          本帮助

命名约定：{repo}--{epic}
  例：demo-ui-topic--E-ENT-IA/

worktree 位置：${WORKTREES_DIR}/
EOF
}

cmd_add() {
    local repo="$1"
    local epic="$2"
    local branch="$3"
    
    if [[ -z "$repo" || -z "$epic" || -z "$branch" ]]; then
        echo -e "${RED}❌ 用法：$0 add <repo> <epic> <branch>${NC}"
        exit 1
    fi
    
    local repo_path="$REPOS_DIR/$repo"
    local wt_name="${repo}--${epic}"
    local wt_path="$WORKTREES_DIR/$wt_name"
    
    if [[ ! -d "$repo_path/.git" ]]; then
        echo -e "${RED}❌ 仓不存在：$repo_path${NC}"
        exit 1
    fi
    
    if [[ -d "$wt_path" ]]; then
        echo -e "${YELLOW}⚠️  worktree 已存在：$wt_path${NC}"
        exit 1
    fi
    
    echo -e "${CYAN}创建 worktree: $wt_name${NC}"
    echo -e "  仓: $repo"
    echo -e "  epic: $epic"
    echo -e "  分支: $branch"
    echo -e "  位置: $wt_path"
    echo ""
    
    # 检查分支是否存在
    if git -C "$repo_path" show-ref --verify --quiet "refs/heads/$branch"; then
        # 已有本地分支
        git -C "$repo_path" worktree add "$wt_path" "$branch"
    elif git -C "$repo_path" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
        # 有 remote 分支，本地 track
        git -C "$repo_path" worktree add -b "$branch" "$wt_path" "origin/$branch"
    else
        # 全新分支，基于 main 创建
        echo -e "${YELLOW}  分支 $branch 不存在，从 main 创建${NC}"
        git -C "$repo_path" worktree add -b "$branch" "$wt_path" "main"
    fi
    
    echo ""
    echo -e "${GREEN}✅ worktree 创建成功${NC}"
    echo -e "${CYAN}→ cd $wt_path${NC}"
}

cmd_list() {
    echo -e "${CYAN}=== 所有 gkx-lumen worktrees ===${NC}"
    if [[ ! -d "$WORKTREES_DIR" ]] || [[ -z "$(ls -A "$WORKTREES_DIR" 2>/dev/null)" ]]; then
        echo -e "${YELLOW}（空）${NC}"
        return
    fi
    
    for wt in "$WORKTREES_DIR"/*; do
        [[ ! -d "$wt" ]] && continue
        local name=$(basename "$wt")
        local branch=""
        if [[ -d "$wt/.git" ]] || [[ -f "$wt/.git" ]]; then
            branch=$(git -C "$wt" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "?")
        fi
        echo -e "  ${GREEN}●${NC} $name  ($branch)"
    done
}

cmd_remove() {
    local repo="$1"
    local epic="$2"
    
    if [[ -z "$repo" || -z "$epic" ]]; then
        echo -e "${RED}❌ 用法：$0 remove <repo> <epic>${NC}"
        exit 1
    fi
    
    local wt_name="${repo}--${epic}"
    local wt_path="$WORKTREES_DIR/$wt_name"
    local repo_path="$REPOS_DIR/$repo"
    
    if [[ ! -d "$wt_path" ]]; then
        echo -e "${RED}❌ worktree 不存在：$wt_path${NC}"
        exit 1
    fi
    
    # 检查是否 dirty
    if [[ -n "$(git -C "$wt_path" status --porcelain 2>/dev/null)" ]]; then
        echo -e "${YELLOW}⚠️  worktree 有未提交改动：$wt_path${NC}"
        read -r -p "强制删除？(y/N) " confirm
        [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 1
        git -C "$repo_path" worktree remove --force "$wt_path"
    else
        git -C "$repo_path" worktree remove "$wt_path"
    fi
    
    echo -e "${GREEN}✅ 清理：$wt_name${NC}"
}

cmd_prune() {
    echo -e "${CYAN}=== 清理失效 worktree ===${NC}"
    for repo_path in "$REPOS_DIR"/*; do
        [[ ! -d "$repo_path/.git" ]] && continue
        local name=$(basename "$repo_path")
        git -C "$repo_path" worktree prune
        echo -e "  ${GREEN}✅${NC} $name"
    done
}

case "${1:-}" in
    add) shift; cmd_add "$@" ;;
    list|ls) cmd_list ;;
    remove|rm) shift; cmd_remove "$@" ;;
    prune) cmd_prune ;;
    --help|-h|help|"") usage ;;
    *) echo -e "${RED}❌ 未知命令：$1${NC}"; usage; exit 1 ;;
esac
