#!/usr/bin/env bash
# 扫描主仓中是否有硬编码绝对路径残留（违反 RFC-002 §6 路径解耦）
# 用法：
#   ./scripts/verify-paths.sh            # 默认 warning 模式（M1-M4 阶段，允许残留）
#   ./scripts/verify-paths.sh --strict   # 严格模式（M5 阶段，hard fail）
# 返回码：默认 0；--strict 模式发现残留时 1

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
NC='\033[0m'

STRICT=false
if [[ "${1:-}" == "--strict" ]]; then
    STRICT=true
fi

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} gkx-lumen verify-paths${NC}"
if $STRICT; then
    echo -e "${CYAN} 模式：STRICT（M5 阶段，hard fail）${NC}"
else
    echo -e "${CYAN} 模式：默认（M1-M4 阶段，warning only）${NC}"
fi
echo -e "${CYAN} RFC-002 §6 路径解耦验证${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# 必须在主仓根执行
if [[ ! -d "agent-delivery" ]] || [[ ! -f "README.md" ]]; then
    echo -e "${RED}❌ 请在 gkx-orchestration/ 根目录执行${NC}"
    exit 1
fi

warnings=0
hard_issues=0

# 共享 exclude 列表（这些文件中允许出现历史/示例引用，不计 hard fail）
# 维护说明：2026-07-28 A1 债务清理后，白名单语义细分：
#   - 历史决策文档保真：RFC/ARCHIVE/agent-handoffs（用户 2026-07-28 确认）
#   - 含"老根叙述"的文档（如"与老根 E:/gkx_src 的关系"、"在老根改东西"）：00-path-resolution/README/team-onboarding
#     这些文件需要引用 E:/gkx_src 作为历史叙述，不是配置，允许保留
#   - 功能性必需：paths.yaml/repo-registry.yaml（legacy 声明）、verify-paths.sh（规则字符串）、bootstrap.*（迁移脚本）、.env.example（示例）
EXCLUDE_FILES=(
    'RFC-001-git-workspace-redesign.md'
    'RFC-002-gkx-v2-greenfield-rebuild.md'
    'RFC-003-feishu-bitable-webhook.md'
    'ARCHIVE-OLD-ROOT.md'
    'paths.yaml'
    'repo-registry.yaml'
    'verify-paths.sh'
    'bootstrap.ps1'
    'bootstrap.sh'
    '.env.example'
    'agent-handoffs/'
    # 含合法"老根历史叙述"的文档（非配置声明）
    '00-path-resolution.mdc'
    '00-team-constitution.mdc'
    'README.md'
    'team-onboarding.md'
    'houtai-arch-discussion.md'
)

# Helper: 把数组拼成 grep -v pipe
filter_excludes() {
    local cmd="cat"
    for f in "${EXCLUDE_FILES[@]}"; do
        cmd="$cmd | grep -v '$f'"
    done
    eval "$cmd"
}

# ============================================================
# 检查项 1：硬编码 E:/gkx_src 或 E:\gkx_src
# ============================================================
echo -e "${YELLOW}[1/4] 检查 E:/gkx_src 老根硬编码 ...${NC}"
results=$(grep -rIn --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' --include='*.py' --include='*.mdc' \
    --exclude-dir='.git' --exclude-dir='node_modules' --exclude-dir='_old' \
    -e 'E:/gkx_src' -e 'E:\\gkx_src' -e 'e:/gkx_src' -e 'e:\\gkx_src' \
    . 2>/dev/null | filter_excludes || true)

if [[ -n "$results" ]]; then
    count=$(echo "$results" | wc -l)
    if $STRICT; then
        echo -e "  ${RED}❌ 发现 $count 处残留：${NC}"
        hard_issues=$((hard_issues + 1))
    else
        echo -e "  ${YELLOW}⚠️  发现 $count 处残留（M3-M5 期间逐步替换）${NC}"
        warnings=$((warnings + 1))
    fi
    echo "$results" | head -10
    [[ $count -gt 10 ]] && echo -e "  ${GRAY}（仅显示前 10 行，共 $count 行）${NC}"
else
    echo -e "  ${GREEN}✅ 无残留${NC}"
fi
echo ""

# ============================================================
# 检查项 2：硬编码 E:/gkx-lumen（新根也不应该硬编码！）
# ============================================================
echo -e "${YELLOW}[2/4] 检查 E:/gkx-lumen 新根硬编码 ...${NC}"
results=$(grep -rIn --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' --include='*.py' \
    --exclude-dir='.git' --exclude-dir='node_modules' \
    -e 'E:/gkx-lumen' -e 'E:\\gkx-lumen' -e 'e:/gkx-lumen' -e 'e:\\gkx-lumen' \
    . 2>/dev/null | filter_excludes || true)

if [[ -n "$results" ]]; then
    count=$(echo "$results" | wc -l)
    if $STRICT; then
        echo -e "  ${RED}❌ 发现 $count 处残留（应该用 \${GKX_ROOT}）：${NC}"
        hard_issues=$((hard_issues + 1))
    else
        echo -e "  ${YELLOW}⚠️  发现 $count 处残留（应该用 \${GKX_ROOT}）${NC}"
        warnings=$((warnings + 1))
    fi
    echo "$results" | head -10
else
    echo -e "  ${GREEN}✅ 无残留（仅在示例/文档中允许）${NC}"
fi
echo ""

# ============================================================
# 检查项 3：硬编码老 GitLab group SZCGKX
# ============================================================
echo -e "${YELLOW}[3/4] 检查 SZCGKX 老 GitLab group 硬编码 ...${NC}"
results=$(grep -rIn --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' --include='*.py' \
    --exclude-dir='.git' --exclude-dir='node_modules' \
    -e 'SZCGKX' \
    . 2>/dev/null | filter_excludes || true)

if [[ -n "$results" ]]; then
    count=$(echo "$results" | wc -l)
    echo -e "  ${YELLOW}⚠️  发现 $count 处引用（仅文档历史允许，agent 配置不允许）${NC}"
    warnings=$((warnings + 1))
    echo "$results" | head -5
else
    echo -e "  ${GREEN}✅ 仅 RFC / 迁移文档中允许${NC}"
fi
echo ""

# ============================================================
# 检查项 4：老仓名硬编码（gkx_lumen_fronted_pc 等）
# ============================================================
echo -e "${YELLOW}[4/4] 检查老仓名硬编码（应该用新名） ...${NC}"
# archived / 开源 fork 仓不迁移，保留老名是正确设计（RFC-002 §7.3），不纳入检查
old_names=('gkx_lumen_fronted_pc' 'gkx_lumen_fronted_mobile' 'gkx_lumen_backend' 'gkx_service_demo' 'gkx_demo_ui' 'innov-algo-demo' 'ent-analysis-demo' 'topic_demo')
total_old_refs=0
for name in "${old_names[@]}"; do
    count=$(grep -rIln --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' \
        --exclude-dir='.git' --exclude-dir='node_modules' \
        -e "$name" \
        . 2>/dev/null | filter_excludes | wc -l)
    if [[ $count -gt 0 ]]; then
        total_old_refs=$((total_old_refs + count))
        echo -e "  ${YELLOW}⚠️  $name → 出现在 $count 个文件中${NC}"
    fi
done

if [[ $total_old_refs -eq 0 ]]; then
    echo -e "  ${GREEN}✅ 无老仓名残留${NC}"
else
    echo ""
    echo -e "  ${YELLOW}（warning：M3-M5 期间逐步替换为新名）${NC}"
    warnings=$((warnings + 1))
fi
echo ""

# ============================================================
# 总结
# ============================================================
echo -e "${CYAN}=========================================${NC}"
if $STRICT; then
    if [[ $hard_issues -eq 0 ]]; then
        echo -e "${GREEN}✅ STRICT 模式通过（无 hard 残留）${NC}"
        if [[ $warnings -gt 0 ]]; then
            echo -e "${YELLOW}   注意：仍有 $warnings 项 warning${NC}"
        fi
        exit 0
    else
        echo -e "${RED}❌ STRICT 模式失败：$hard_issues 项 hard 问题${NC}"
        exit 1
    fi
else
    if [[ $warnings -eq 0 ]]; then
        echo -e "${GREEN}✅ 默认模式：完美（无任何残留）${NC}"
    else
        echo -e "${YELLOW}⚠️  默认模式：$warnings 项 warning（M1-M4 阶段可接受）${NC}"
        echo -e "${GRAY}   M5 阶段请运行 ./scripts/verify-paths.sh --strict 验证${NC}"
    fi
    exit 0
fi
