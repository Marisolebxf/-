#!/usr/bin/env bash
# gkx-lumen 一键 onboarding 脚本 (Mac / Linux)
# 用法：在 gkx-orchestration/ 目录下执行 ./scripts/bootstrap.sh
# 作用：验证 .env / 装 commit hooks / clone 10 业务子仓 / 提示下一步
# 参数：--force  跳过路径不匹配检查（不建议，仅在你确认无误时用）

set -e

FORCE=0
for arg in "$@"; do
    case "$arg" in
        --force|-f) FORCE=1 ;;
    esac
done

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} gkx-lumen bootstrap (Mac/Linux)${NC}"
echo -e "${CYAN} RFC-002 §6 onboarding ≤ 1 hour${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# ============================================================
# Step 1: 验证 .env
# ============================================================
echo -e "${YELLOW}[1/5] 验证 .env ...${NC}"

if [[ ! -f ".env" ]]; then
    echo -e "  ${RED}❌ .env 不存在${NC}"
    echo -e "  ${RED}→ 请先：cp .env.example .env，然后编辑 .env 填写 GKX_ROOT${NC}"
    exit 1
fi

# 加载 .env
set -a
source .env
set +a

if [[ -z "${GKX_ROOT:-}" ]]; then
    echo -e "  ${RED}❌ .env 缺少 GKX_ROOT${NC}"
    echo -e "  ${RED}→ 请编辑 .env 填写 GKX_ROOT=<你的工作区根，例 ~/work/gkx-lumen>${NC}"
    exit 1
fi

GKX_GITLAB_BASE="${GKX_GITLAB_BASE:-https://gitlab.htmisoft.net}"
GKX_GITLAB_GROUP="${GKX_GITLAB_GROUP:-gkx-lumen}"

echo -e "  ${GREEN}✅ GKX_ROOT = $GKX_ROOT${NC}"
echo -e "  ${GREEN}✅ GitLab group = $GKX_GITLAB_BASE/$GKX_GITLAB_GROUP${NC}"

# 展开 ~ 等
GKX_ROOT_EXPANDED=$(eval echo "$GKX_ROOT")

# 验证当前位置（强约束：不一致直接 abort，避免误用别处的子仓）
current_path=$(pwd)
expected_path="$GKX_ROOT_EXPANDED/gkx-orchestration"
# 归一化（去尾斜杠、小写比较）
current_norm="${current_path%/}"
expected_norm="${expected_path%/}"
if [[ "${current_norm,,}" != "${expected_norm,,}" ]]; then
    if [[ "$FORCE" -ne 1 ]]; then
        echo -e "  ${RED}❌ 当前位置 $current_path${NC}"
        echo -e "  ${RED}   ≠ .env 期望 $expected_path${NC}"
        echo ""
        echo -e "  ${YELLOW}常见原因 / 修复：${NC}"
        echo -e "  ${YELLOW}  1. 你在错位置 cd 了主仓 → cd \"$expected_path\" 后重跑${NC}"
        echo -e "  ${YELLOW}  2. .env 的 GKX_ROOT 写的是别的机器的路径 → 编辑 .env 改为本机实际路径${NC}"
        echo -e "  ${YELLOW}     例如本机在 ~/work/gkx-lumen 下，.env 应写 GKX_ROOT=~/work/gkx-lumen${NC}"
        echo ""
        echo -e "  ${GRAY}若你确认无误（如调试模式），加 --force 参数重跑：${NC}"
        echo -e "  ${GRAY}  ./scripts/bootstrap.sh --force${NC}"
        exit 1
    else
        echo -e "  ${YELLOW}⚠️  位置不匹配，但 --force 已指定，继续执行${NC}"
    fi
fi

# ============================================================
# Step 2: 安装 commit hooks
# ============================================================
echo ""
echo -e "${YELLOW}[2/5] 安装 commit hooks ...${NC}"

if [[ -d ".git-template/hooks" ]]; then
    git config core.hooksPath .git-template/hooks
    chmod +x .git-template/hooks/*
    echo -e "  ${GREEN}✅ 主仓 hooks 已激活（.git-template/hooks）${NC}"
else
    echo -e "  ${YELLOW}⚠️  .git-template/hooks 不存在，跳过${NC}"
fi

# ============================================================
# Step 3: 验证 GitLab 凭据
# ============================================================
echo ""
echo -e "${YELLOW}[3/5] 验证 GitLab 凭据 ...${NC}"

if [[ -n "${GKX_GITLAB_TOKEN:-}" ]]; then
    GKX_GITLAB_USER="${GKX_GITLAB_USER:-oauth2}"
    # 测试 token
    if response=$(curl -s -f -H "PRIVATE-TOKEN: $GKX_GITLAB_TOKEN" "$GKX_GITLAB_BASE/api/v4/user" 2>&1); then
        username=$(echo "$response" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
        echo -e "  ${GREEN}✅ Token 有效（user: $username）${NC}"
    else
        echo -e "  ${YELLOW}⚠️  Token 验证失败${NC}"
    fi
else
    echo -e "  ${YELLOW}⚠️  未配置 GKX_GITLAB_TOKEN，clone 时会逐个提示账号密码${NC}"
fi

# ============================================================
# Step 4: clone 10 业务子仓
# ============================================================
echo ""
echo -e "${YELLOW}[4/5] clone 10 个业务子仓 ...${NC}"

repos=(
    'demo-ui-science'
    'demo-algo-ent-analysis'
    'dataease'
    'demo-ui-system-test'
    'lumen-svc-platform'
    'lumen-ui-science-pc'
    'lumen-ui-science-mobile'
    'demo-svc-platform'
    'demo-algo-science'
    'demo-ui-topic'
)

repos_dir="$GKX_ROOT_EXPANDED/repos"
mkdir -p "$repos_dir"

success_count=0
skip_count=0
fail_count=0
failed_repos=()

for repo in "${repos[@]}"; do
    target_path="$repos_dir/$repo"
    if [[ -d "$target_path" ]]; then
        echo -e "  ${GRAY}⏭  $repo  (已存在，跳过)${NC}"
        skip_count=$((skip_count + 1))
        continue
    fi
    
    if [[ -n "${GKX_GITLAB_TOKEN:-}" ]]; then
        user="${GKX_GITLAB_USER:-oauth2}"
        base_no_proto="${GKX_GITLAB_BASE#https://}"
        url="https://${user}:${GKX_GITLAB_TOKEN}@${base_no_proto}/$GKX_GITLAB_GROUP/$repo.git"
    else
        url="$GKX_GITLAB_BASE/$GKX_GITLAB_GROUP/$repo.git"
    fi
    
    echo -ne "  ${CYAN}⏳  $repo  ...${NC}"
    if git clone "$url" "$target_path" > /dev/null 2>&1; then
        echo -e " ${GREEN}✅${NC}"
        success_count=$((success_count + 1))
    else
        echo -e " ${RED}❌${NC}"
        fail_count=$((fail_count + 1))
        failed_repos+=("$repo")
    fi
done

echo ""
echo -e "  ${CYAN}结果：$success_count 成功 / $skip_count 跳过 / $fail_count 失败${NC}"
if [[ $fail_count -gt 0 ]]; then
    echo -e "  ${RED}失败仓：${failed_repos[*]}${NC}"
    echo -e "  ${YELLOW}→ 可手动 cd repos/ && git clone $GKX_GITLAB_BASE/$GKX_GITLAB_GROUP/<repo>.git 重试${NC}"
fi

# ============================================================
# Step 5: 提示下一步
# ============================================================
echo ""
echo -e "${YELLOW}[5/5] 下一步 ...${NC}"
workspace_file="$GKX_ROOT_EXPANDED/gkx-orchestration/gkx-lumen.code-workspace"
echo "  1. 用 Cursor 打开 multi-root 工作区（推荐，一次看到主仓 + 11 子仓 + worktrees）："
echo -e "       ${CYAN}File → Open Workspace from File → $workspace_file${NC}"
echo "     （已自动排除 node_modules/target/.venv，避免索引爆炸；缺失的子仓会有 warning，跑 bootstrap 即可补齐）"
echo "  2. 在 Cursor 新开 Agent 会话，输入：'你是哪个角色？必读哪些文件？'"
echo "  3. 按角色装依赖："
echo "       - 前端：cd repos/<repo-name> && npm install"
echo "       - 后端：cd repos/lumen-svc-platform && mvn install -DskipTests"
echo "       - 算法：cd repos/demo-algo-* && pip install -r requirements.txt"
echo "  4. 跟 mentor 跑首个 task（详见 agent-delivery/team-onboarding.md §2）"
echo ""
echo -e "${CYAN}=========================================${NC}"
echo -e "${GREEN} bootstrap 完成！${NC}"
echo -e "${CYAN} 期望用时 ≤ 1 小时（RFC-002 §3 G2 验收标准）${NC}"
echo -e "${CYAN}=========================================${NC}"
