#!/usr/bin/env bash
# Worktree 管理工具：统一在 ${GKX_ROOT}/worktrees/ 下管理
# 用法：
#   ./scripts/worktree-helper.sh add <repo> <epic> <branch>      创建 worktree
#   ./scripts/worktree-helper.sh list                            列出所有 worktree
#   ./scripts/worktree-helper.sh remove <repo> <epic>            清理 worktree
#   ./scripts/worktree-helper.sh prune                           清理失效 worktree
# 命名约定：{repo}--{epic}/   例：demo-ui-topic--E-ENT-IA/
# 仓路径：优先 ${GKX_ROOT}/repos/{repo}；编排仓等顶层仓用 ${GKX_ROOT}/{repo}
# 新分支基线：优先 origin/dev（团队公约），其次 main/master

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# 加载 .env（须在 gkx-orchestration 根目录执行）
if [[ ! -f ".env" ]]; then
    echo -e "${RED}❌ .env 不存在，请先在 gkx-orchestration 根目录执行，或 cp .env.example .env${NC}"
    exit 1
fi
set -a
# shellcheck disable=SC1091
source .env
set +a
GKX_ROOT_EXPANDED=$(eval echo "$GKX_ROOT")

REPOS_DIR="$GKX_ROOT_EXPANDED/repos"
WORKTREES_DIR="$GKX_ROOT_EXPANDED/worktrees"
mkdir -p "$WORKTREES_DIR"

# 解析仓根：repos 子仓 → 顶层仓（如 gkx-orchestration）
resolve_repo_path() {
    local repo="$1"
    local candidate
    for candidate in "$REPOS_DIR/$repo" "$GKX_ROOT_EXPANDED/$repo"; do
        if [[ -d "$candidate/.git" || -f "$candidate/.git" ]]; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

# 已知 git 仓根列表（prune 用）
list_repo_roots() {
    local p
    if [[ -d "$REPOS_DIR" ]]; then
        for p in "$REPOS_DIR"/*; do
            [[ -d "$p/.git" || -f "$p/.git" ]] && echo "$p"
        done
    fi
    for p in "$GKX_ROOT_EXPANDED"/gkx-orchestration; do
        [[ -d "$p/.git" || -f "$p/.git" ]] && echo "$p"
    done
}

default_base_ref() {
    local repo_path="$1"
    if git -C "$repo_path" show-ref --verify --quiet "refs/remotes/origin/dev"; then
        echo "origin/dev"
    elif git -C "$repo_path" show-ref --verify --quiet "refs/heads/dev"; then
        echo "dev"
    elif git -C "$repo_path" show-ref --verify --quiet "refs/remotes/origin/main"; then
        echo "origin/main"
    elif git -C "$repo_path" show-ref --verify --quiet "refs/heads/main"; then
        echo "main"
    else
        echo "main"
    fi
}

usage() {
    cat <<EOF
worktree-helper - gkx-lumen worktree 管理（手册 §14 唯一入口）

用法:
  $0 add <repo> <epic> <branch>      创建 worktree
                                     例：$0 add demo-ui-topic E-ENT-IA feat/ent-elements
                                     例：$0 add gkx-orchestration sysint-0303a feat/sysint-0303a
  $0 list                            列出所有 worktree
  $0 remove <repo> <epic>            清理 worktree（包括目录）
  $0 prune                           git worktree prune（清理失效引用）
  $0 --help                          本帮助

命名约定：{repo}--{epic}
  例：demo-ui-topic--E-ENT-IA/
  例：gkx-orchestration--sysint-0303a/

仓路径：\${GKX_ROOT}/repos/{repo} 或 \${GKX_ROOT}/{repo}（编排仓）
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
    
    local repo_path
    if ! repo_path=$(resolve_repo_path "$repo"); then
        echo -e "${RED}❌ 仓不存在：已试 $REPOS_DIR/$repo 与 $GKX_ROOT_EXPANDED/$repo${NC}"
        exit 1
    fi
    local wt_name="${repo}--${epic}"
    local wt_path="$WORKTREES_DIR/$wt_name"
    
    if [[ -d "$wt_path" ]]; then
        echo -e "${YELLOW}⚠️  worktree 已存在：$wt_path${NC}"
        exit 1
    fi
    
    echo -e "${CYAN}创建 worktree: $wt_name${NC}"
    echo -e "  仓: $repo ($repo_path)"
    echo -e "  epic: $epic"
    echo -e "  分支: $branch"
    echo -e "  位置: $wt_path"
    echo ""
    
    if git -C "$repo_path" show-ref --verify --quiet "refs/heads/$branch"; then
        git -C "$repo_path" worktree add "$wt_path" "$branch"
    elif git -C "$repo_path" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
        git -C "$repo_path" worktree add -b "$branch" "$wt_path" "origin/$branch"
    else
        local base
        base=$(default_base_ref "$repo_path")
        echo -e "${YELLOW}  分支 $branch 不存在，从 $base 创建${NC}"
        git -C "$repo_path" worktree add -b "$branch" "$wt_path" "$base"
    fi
    
    echo ""
    echo -e "${GREEN}✅ worktree 创建成功${NC}"
    echo -e "${CYAN}→ Cursor: File → Open Folder → $wt_path${NC}"
}

cmd_list() {
    echo -e "${CYAN}=== 所有 gkx-lumen worktrees ===${NC}"
    if [[ ! -d "$WORKTREES_DIR" ]] || [[ -z "$(ls -A "$WORKTREES_DIR" 2>/dev/null)" ]]; then
        echo -e "${YELLOW}（空）${NC}"
        return
    fi
    
    for wt in "$WORKTREES_DIR"/*; do
        [[ ! -d "$wt" ]] && continue
        local name
        name=$(basename "$wt")
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
    local repo_path
    if ! repo_path=$(resolve_repo_path "$repo"); then
        echo -e "${RED}❌ 仓不存在：$repo${NC}"
        exit 1
    fi
    
    if [[ ! -d "$wt_path" ]]; then
        echo -e "${RED}❌ worktree 不存在：$wt_path${NC}"
        exit 1
    fi
    
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
    local repo_path name
    while IFS= read -r repo_path; do
        [[ -z "$repo_path" ]] && continue
        name=$(basename "$repo_path")
        git -C "$repo_path" worktree prune
        echo -e "  ${GREEN}✅${NC} $name"
    done < <(list_repo_roots)
}

case "${1:-}" in
    add) shift; cmd_add "$@" ;;
    list|ls) cmd_list ;;
    remove|rm) shift; cmd_remove "$@" ;;
    prune) cmd_prune ;;
    --help|-h|help|"") usage ;;
    *) echo -e "${RED}❌ 未知命令：$1${NC}"; usage; exit 1 ;;
esac
