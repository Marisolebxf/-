# ENT-COMPARE Action Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将对比篮收缩为无推荐、仅企业名称搜索，并以两个分组下拉入口明确分发到五种分析类型。

**Architecture:** 不改变对比篮“对象暂存与分发”边界；只修订 IA、TRACE、USM、Wireframe 的空态、搜索和批量分发契约。目标模块继续负责对象数量、字段、权限和模型条件校验。

**Tech Stack:** Markdown, YAML, Ruby YAML validation, ripgrep, Git

---

### Task 1: 修订四件套产品契约

**Files:**
- Modify: `agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/IA-ENT-COMPARE.md`
- Modify: `agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/TRACE-ENT-COMPARE.yaml`
- Modify: `agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/USM-ENT-COMPARE.md`
- Modify: `agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/Wireframe-ENT-COMPARE.md`

- [x] **Step 1: 移除对比篮推荐企业契约**

删除空态推荐卡片、Q037 对比篮开放项和 E-33/E-34 空态推荐映射；保留“去企业查询”主操作。

- [x] **Step 2: 收缩篮内搜索**

将允许搜索字段改为仅 `enterprise_name`；保留统一社会信用代码作为展示字段和去重键。

- [x] **Step 3: 拆分两组五种分析动作**

统一写入以下类型：

```text
企业评估: technology | business | competitiveness
风险洞察: supply-chain | pain-points
```

对应用户文案为“技术力评估 / 商业力评估 / 综合竞争力评估”和“供应链关系分析 / 发展痛难点分析”。

- [x] **Step 4: 更新验收、状态和差异记录**

四件套中明确未选对象时两个分组入口不可执行，权限不足的菜单项保留并解释原因，选择具体类型后携带 `analysis_type` 进入目标模块。

### Task 2: 更新任务评审记录

**Files:**
- Modify: `agent-delivery/task-registry.yaml`

- [x] **Step 1: 记录本次人工评审纠偏**

保持 `ENT-MOD-COMPARE-PACK-L01` 为 `review`，保留 Owner 与 Supervisor，在 note 中记录去推荐、去信用代码搜索和 3+2 分析分组。

### Task 3: 校验并发布

**Files:**
- Validate: `agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/*`
- Validate: `agent-delivery/task-registry.yaml`

- [x] **Step 1: 验证 YAML 和四件套一致性**

Run:

```bash
ruby -ryaml -e 'YAML.load_file("agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE/TRACE-ENT-COMPARE.yaml"); YAML.load_file("agent-delivery/task-registry.yaml")'
```

Expected: exit 0.

- [x] **Step 2: 验证禁止文案与必需动作**

Run targeted `rg` checks. Expected: 四件套不再包含对比篮推荐 / Q037 / 信用代码搜索契约，且五个具体分析名称都存在。

- [x] **Step 3: 提交并推送 `dev`**

```bash
git diff --check
git add agent-delivery/agent-handoffs/产品整体定义/ENT-COMPARE agent-delivery/task-registry.yaml docs/superpowers/plans/2026-07-15-ent-compare-action-refinement.md
git commit -m "docs(product): 修订对比篮分析分发交互 [agent:ux-agent]"
git push origin dev
```

Expected: push succeeds without force.
