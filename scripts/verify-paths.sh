#!/usr/bin/env bash
# 扫描主仓中是否有硬编码绝对路径残留（违反 RFC-002 §6 路径解耦）
# 用法：./scripts/verify-paths.sh
# 返回码：0 = clean / 1 = 发现残留

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}=========================================${NC}"
echo -e "${CYAN} gkx-lumen verify-paths${NC}"
echo -e "${CYAN} 扫描硬编码路径残留 (RFC-002 §6)${NC}"
echo -e "${CYAN}=========================================${NC}"
echo ""

# 必须在主仓根执行
if [[ ! -f "paths.yaml" && ! -f "agent-delivery/paths.yaml" ]]; then
    echo -e "${RED}❌ 请在 gkx-orchestration/ 根目录执行${NC}"
    exit 1
fi

issues_found=0

# 检查项 1：硬编码 E:/gkx_src 或 E:\gkx_src
echo -e "${YELLOW}[1/4] 检查 E:/gkx_src 老根硬编码 ...${NC}"
results=$(grep -rIn --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' --include='*.py' \
    --exclude-dir='.git' --exclude-dir='node_modules' --exclude-dir='_old' \
    -e 'E:/gkx_src' -e 'E:\\gkx_src' -e 'e:/gkx_src' -e 'e:\\gkx_src' \
    . 2>/dev/null | \
    grep -v 'RFC-001-git-workspace-redesign.md' | \
    grep -v 'RFC-002-gkx-v2-greenfield-rebuild.md' | \
    grep -v 'ARCHIVE-OLD-ROOT.md' | \
    grep -v 'paths.yaml' || true)

if [[ -n "$results" ]]; then
    echo -e "  ${RED}❌ 发现 $(echo "$results" | wc -l) 处残留：${NC}"
    echo "$results" | head -20
    [[ $(echo "$results" | wc -l) -gt 20 ]] && echo -e "  ${YELLOW}（仅显示前 20 行）${NC}"
    issues_found=$((issues_found + 1))
else
    echo -e "  ${GREEN}✅ 无残留${NC}"
fi
echo ""

# 检查项 2：硬编码 E:/gkx-lumen（新根也不应该硬编码！）
echo -e "${YELLOW}[2/4] 检查 E:/gkx-lumen 新根硬编码（除示例文件外） ...${NC}"
results=$(grep -rIn --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' --include='*.py' \
    --exclude-dir='.git' --exclude-dir='node_modules' \
    -e 'E:/gkx-lumen' -e 'E:\\gkx-lumen' \
    . 2>/dev/null | \
    grep -v '.env.example' | \
    grep -v 'README.md' | \
    grep -v 'team-onboarding.md' | \
    grep -v 'RFC-002-gkx-v2-greenfield-rebuild.md' | \
    grep -v 'ARCHIVE-OLD-ROOT.md' || true)

if [[ -n "$results" ]]; then
    echo -e "  ${RED}❌ 发现 $(echo "$results" | wc -l) 处残留（应该用 \${GKX_ROOT}）：${NC}"
    echo "$results" | head -20
    issues_found=$((issues_found + 1))
else
    echo -e "  ${GREEN}✅ 无残留（仅在示例/文档中允许）${NC}"
fi
echo ""

# 检查项 3：硬编码老 GitLab group SZCGKX
echo -e "${YELLOW}[3/4] 检查 SZCGKX 老 GitLab group 硬编码 ...${NC}"
results=$(grep -rIn --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' --include='*.py' \
    --exclude-dir='.git' --exclude-dir='node_modules' \
    -e 'SZCGKX' \
    . 2>/dev/null | \
    grep -v 'RFC-001-git-workspace-redesign.md' | \
    grep -v 'RFC-002-gkx-v2-greenfield-rebuild.md' | \
    grep -v 'ARCHIVE-OLD-ROOT.md' | \
    grep -v 'paths.yaml' || true)

if [[ -n "$results" ]]; then
    echo -e "  ${YELLOW}⚠️  发现 $(echo "$results" | wc -l) 处引用（仅文档历史允许，agent 配置不允许）：${NC}"
    echo "$results" | head -10
    # 这是 warning 不 fail
else
    echo -e "  ${GREEN}✅ 仅 RFC / 迁移文档中允许${NC}"
fi
echo ""

# 检查项 4：老仓名硬编码（gkx_lumen_fronted_pc 等）
echo -e "${YELLOW}[4/4] 检查老仓名硬编码（应该用新名） ...${NC}"
old_names=('gkx_lumen_fronted_pc' 'gkx_lumen_fronted_mobile' 'gkx_lumen_backend' 'gkx_service_demo' 'gkx_demo_ui' 'gkx_demo_python' 'gkx_ui_demo' 'gkx_dataease' 'innov-algo-demo' 'ent-analysis-demo' 'topic_demo')
total_old_refs=0
for name in "${old_names[@]}"; do
    count=$(grep -rIln --include='*.md' --include='*.yaml' --include='*.yml' --include='*.json' --include='*.ps1' --include='*.sh' \
        --exclude-dir='.git' --exclude-dir='node_modules' \
        --exclude='RFC-001-git-workspace-redesign.md' \
        --exclude='RFC-002-gkx-v2-greenfield-rebuild.md' \
        --exclude='ARCHIVE-OLD-ROOT.md' \
        --exclude='paths.yaml' \
        --exclude='repo-registry.yaml' \
        -e "$name" \
        . 2>/dev/null | wc -l)
    if [[ $count -gt 0 ]]; then
        total_old_refs=$((total_old_refs + count))
        echo -e "  ${YELLOW}⚠️  $name → 出现在 $count 个文件中${NC}"
    fi
done

if [[ $total_old_refs -eq 0 ]]; then
    echo -e "  ${GREEN}✅ 无老仓名残留${NC}"
else
    echo ""
    echo -e "  ${YELLOW}（这是 warning：M3-M5 期间逐步替换为新名）${NC}"
fi
echo ""

# 总结
echo -e "${CYAN}=========================================${NC}"
if [[ $issues_found -eq 0 ]]; then
    echo -e "${GREEN}✅ verify-paths 通过（hard checks all clean）${NC}"
    exit 0
else
    echo -e "${RED}❌ verify-paths 发现 $issues_found 项 hard 问题${NC}"
    echo -e "${YELLOW}→ 修复后重跑${NC}"
    exit 1
fi
