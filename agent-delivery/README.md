# agent-delivery — 多智能体编排根目录

本目录是 **Coordinator 与各 Agent 的会话入口**。  
路径真源：`${GKX_ROOT}/gkx-orchestration/agent-delivery/`（GitLab：`gkx-lumen/gkx-orchestration`）。

## 团队成员必读 Markdown 索引

> **GitLab 用法**：下表 **「打开」** 列使用 `target="_blank"`，在网页上点击会在**新标签页**打开对应 `.md` 源文件（相对链接，任意分支均有效）。  
> **AI 公约 P0 真源**：见 [`.cursor/rules/00-team-constitution.mdc`](../.cursor/rules/00-team-constitution.mdc)。

### P0 · 全员 / 任何任务开工前

| 文档 | 读者 | 仓库路径 | 打开 |
|------|------|----------|------|
| 招标需求（展示+专题） | 全员 | `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` | <a href="./bid-reference/科技信息展示系统和科技专题服务系统.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 招标需求（算法库） | 全员 | `agent-delivery/bid-reference/科技专题服务算法库.md` | <a href="./bid-reference/科技专题服务算法库.md" target="_blank" rel="noopener noreferrer">打开</a> |
| DS-xx 章节对照 | 按需 | `agent-delivery/bid-reference/README.md` | <a href="./bid-reference/README.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 架构铁律 D1–D8 | 全员 | `agent-delivery/architecture-baseline.md` | <a href="./architecture-baseline.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 团队公约 · 人机分工 | **全员** | `agent-delivery/team-collaboration-playbook.md` | <a href="./team-collaboration-playbook.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 甲方决策项跟踪 | **全员**（动手前查 🟡） | `agent-delivery/客户决策清单跟踪表.md` | <a href="./客户决策清单跟踪表.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 项目计划（交付阶段） | **全员**（看自己的节点与日期） | `agent-delivery/project-plan.md` | <a href="./project-plan.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 数据血缘 D9 | data/algorithm/api/ui/qa/doc/architect | `agent-delivery/data-lineage-policy.md` | <a href="./data-lineage-policy.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 任务认领 + Kanban | **全员** | `agent-delivery/task-claiming-guide.md` | <a href="./task-claiming-guide.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 自动派单与 confirm | **全员** | `agent-delivery/自动派单与确认规约.md` | <a href="./自动派单与确认规约.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 长任务过夜连跑 | **coordinator / 监管人** | `agent-delivery/长任务执行规约.md` | <a href="./长任务执行规约.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 飞书 Kanban 集成 | PM/coordinator/**全员** | `agent-delivery/feishu/feishu-bitable-integration.md` | <a href="./feishu/feishu-bitable-integration.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 飞书双向 sync 站会 | PM/coordinator/**全员** | `agent-delivery/feishu/feishu-bitable-bidirectional-ops.md` | <a href="./feishu/feishu-bitable-bidirectional-ops.md" target="_blank" rel="noopener noreferrer">打开</a> |

### P0 · 按角色追加

| 文档 | 读者 | 仓库路径 | 打开 |
|------|------|----------|------|
| 前端权威 UI（D8） | ux / ui / frontend / qa / architect | `agent-delivery/Design.md` | <a href="./Design.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 交互规范（D10） | ux / ui / frontend / qa / architect | `agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md` | <a href="./agent-handoffs/产品整体定义/UX-UE%20通用交互组件规范.md" target="_blank" rel="noopener noreferrer">打开</a> |

### P1 · 派单 / 协作 / 工程闭环

| 文档 | 读者 | 仓库路径 | 打开 |
|------|------|----------|------|
| 智能体编排与派单 | coordinator / 工程师 | `agent-delivery/智能体编排与派单手册.md` | <a href="./智能体编排与派单手册.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 长任务执行规约 | coordinator / 监管人 / 过夜执行 | `agent-delivery/长任务执行规约.md` | <a href="./长任务执行规约.md" target="_blank" rel="noopener noreferrer">打开</a> |
| Ponytail 编码精简（Cursor） | 前端 / 后端 / 算法 / DevOps / QA + coding agent | `agent-delivery/ponytail-usage.md` | <a href="./ponytail-usage.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 产品定义评审（PDR） | PM / UE / 架构 / 前端 Lead | `agent-delivery/产品定义评审规程.md` | <a href="./产品定义评审规程.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 产品实现（门 3 后） | 前端 / 后端 / 算法 / PM | `agent-delivery/产品实现规程.md` | <a href="./产品实现规程.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 总控铁律 | 全员 | `agent-delivery/项目工程化交付模式.md` | <a href="./项目工程化交付模式.md" target="_blank" rel="noopener noreferrer">打开</a> |
| CI/CD 闭环 | DevOps / 工程师 | `agent-delivery/cicd-pipeline.md` | <a href="./cicd-pipeline.md" target="_blank" rel="noopener noreferrer">打开</a> |
| AI token 预算 | PM / lead / coordinator | `agent-delivery/budget-estimate.md` | <a href="./budget-estimate.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 指标说明卡模板 | doc / data | `agent-delivery/templates/metric-spec-card-template.md` | <a href="./templates/metric-spec-card-template.md" target="_blank" rel="noopener noreferrer">打开</a> |

### 新人 onboarding（建议顺序 · MD）

| 顺序 | 文档 | 仓库路径 | 打开 |
|------|------|----------|------|
| 1 | 主仓总览 | `README.md` | <a href="../README.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 2 | 团队公约 | `agent-delivery/team-collaboration-playbook.md` | <a href="./team-collaboration-playbook.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 3 | 任务认领 | `agent-delivery/task-claiming-guide.md` | <a href="./task-claiming-guide.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 4 | 总控铁律 | `agent-delivery/项目工程化交付模式.md` | <a href="./项目工程化交付模式.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 5 | 角色对比（查自己的节） | `agent-delivery/角色AI协作对比手册.md` | <a href="./角色AI协作对比手册.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 6 | 本目录索引 | `agent-delivery/README.md` | <a href="./README.md" target="_blank" rel="noopener noreferrer">打开</a> |
| + | 1 小时上手指引 | `agent-delivery/team-onboarding.md` | <a href="./team-onboarding.md" target="_blank" rel="noopener noreferrer">打开</a> |
| + | Cursor 多实例并行 | `agent-delivery/Cursor-多实例多角色并行实战.md` | <a href="./Cursor-多实例多角色并行实战.md" target="_blank" rel="noopener noreferrer">打开</a> |

### 专项 · 按需

| 文档 | 读者 | 仓库路径 | 打开 |
|------|------|----------|------|
| 飞书集成文档目录 | PM / coordinator / DevOps | `agent-delivery/feishu/README.md` | <a href="./feishu/README.md" target="_blank" rel="noopener noreferrer">打开</a> |
| Webhook Handler 运维 | coordinator / DevOps | `agent-delivery/feishu/feishu-bitable-webhook-handler.md` | <a href="./feishu/feishu-bitable-webhook-handler.md" target="_blank" rel="noopener noreferrer">打开</a> |
| RFC-003 Webhook 方案 | 架构 / coordinator | `agent-delivery/RFC/RFC-003-feishu-bitable-webhook.md` | <a href="./RFC/RFC-003-feishu-bitable-webhook.md" target="_blank" rel="noopener noreferrer">打开</a> |
| coordinator 自动派单运维 | coordinator | `agent-delivery/coordinator-auto-dispatch.md` | <a href="./coordinator-auto-dispatch.md" target="_blank" rel="noopener noreferrer">打开</a> |
| RFC-002 工作区 greenfield | 管理者 / 架构 / lead | `agent-delivery/RFC/RFC-002-gkx-v2-greenfield-rebuild.md` | <a href="./RFC/RFC-002-gkx-v2-greenfield-rebuild.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 可观测性 | DevOps / 后端 / 算法 | `agent-delivery/observability.md` | <a href="./observability.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 存储设计 | data / 后端 | `agent-delivery/data/data-design/storage/README.md` | <a href="./data/data-design/storage/README.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 图谱引擎 | 算法 / 后端 | `agent-delivery/graph-engine.md` | <a href="./graph-engine.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 飞书 sync K8s 部署 | DevOps | `deploy/feishu-sync/README.md` | <a href="../deploy/feishu-sync/README.md" target="_blank" rel="noopener noreferrer">打开</a> |
| 三方库入站说明 | data / algorithm | `agent-delivery/data/third-party-source/README.md` | <a href="./data/third-party-source/README.md" target="_blank" rel="noopener noreferrer">打开</a> |

### 路径清单（复制用 · 相对 `gkx-orchestration/`）

```text
README.md
agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md
agent-delivery/bid-reference/科技专题服务算法库.md
agent-delivery/bid-reference/README.md
agent-delivery/architecture-baseline.md
agent-delivery/team-collaboration-playbook.md
agent-delivery/客户决策清单跟踪表.md
agent-delivery/project-plan.md
agent-delivery/project-plan.yaml
agent-delivery/data-lineage-policy.md
agent-delivery/task-claiming-guide.md
agent-delivery/自动派单与确认规约.md
agent-delivery/长任务执行规约.md
agent-delivery/feishu/feishu-bitable-integration.md
agent-delivery/feishu/feishu-bitable-bidirectional-ops.md
agent-delivery/Design.md
agent-delivery/agent-handoffs/产品整体定义/UX-UE 通用交互组件规范.md
agent-delivery/智能体编排与派单手册.md
agent-delivery/产品定义评审规程.md
agent-delivery/产品实现规程.md
agent-delivery/项目工程化交付模式.md
agent-delivery/cicd-pipeline.md
agent-delivery/budget-estimate.md
agent-delivery/templates/metric-spec-card-template.md
agent-delivery/team-onboarding.md
agent-delivery/角色AI协作对比手册.md
agent-delivery/README.md
```

---

## 快速开始

1. 在 Cursor **新开 Agent 会话**，工作区打开 `${GKX_ROOT}`（或 `gkx-lumen.code-workspace` 多根工作区）
2. 新人先读上表 **P0 + onboarding**；Coordinator 读 [`智能体编排与派单手册.md`](./智能体编排与派单手册.md) 或 [`整体工作计划.md`](./整体工作计划.md)
3. Coordinator 读取 `task-registry.yaml`，选取 `status=pending` 且依赖已 `done` 的 leaf 派单
4. 执行 Agent 完成后写 `agent-handoffs/{task-id}.md`，更新 task 状态

## 目录结构

```
agent-delivery/
├── paths.yaml                    # 双根路径真源（code_root + docs_root）
├── task-registry.yaml            # 任务队列（Coordinator 派单）
├── system-wbs.yaml               # 七要素 + 34 页 + Wave 0–5
├── repo-registry.yaml            # demo ↔ lumen 仓映射
├── 整体工作计划.md                # Wave0–5 工程检查稿（2026-06）；交付阶段真源见 project-plan.*
├── project-plan.yaml / .md       # ★ PM 交付阶段（S1–S6 / 当前阶段 / 按人日期）
├── 项目工程化交付模式.md          # 总控 Prompt / 铁律
├── scope-and-responsibility.md   # 智树边界
├── requirements-master-index.yaml
├── acceptance-*.yaml / *.md      # 甲方验收体系
├── formal-docs-registry.yaml     # V6 / 时序图 / API 契约索引
├── 数据库设计.md                 # 作废 stub → data/data-design/storage/README.md
├── data/data-design/storage/     # ★ 存储设计现行真源
├── graph-engine.md / observability.md / cicd-pipeline.md
├── agent-handoffs/               # 任务交接证据
├── 验收文档/                      # 测试/演示报告
├── bid-reference/                # 招标需求 MD（主读）+ DOCX 归档
│   ├── 科技信息展示系统和科技专题服务系统.md
│   ├── 科技专题服务算法库.md
│   └── README.md                 # DS-xx ↔ 章节编号对照
├── acceptance-review-workflow.md # qa-agent 验收对照流程
├── templates/                    # handoff / 验收报告模板
├── RFC/                          # 团队级技术评审提案（等 leads 决策）
│   ├── RFC-001-git-workspace-redesign.md  # 工作区布局升级（in-place 改造，已被 RFC-002 supersede）
│   ├── RFC-002-gkx-v2-greenfield-rebuild.md  # ★ gkx-v2 全新根目录重做方案（greenfield，6 个月迁移）
│   └── RFC-003-feishu-bitable-webhook.md     # 飞书 Bitable Webhook 入站 + 飞书-only 状态（方案 B）
├── feishu/                       # 飞书集成说明 / 开通教练 / 看板 YAML 配置
│   ├── README.md
│   ├── feishu-bitable-integration.md
│   ├── feishu-bitable.yaml
│   └── feishu-bitable-webhook-handler.md
└── scripts/                      # 工具脚本
```

## 关键文件

> 必读 **Markdown** 完整索引（含 GitLab 新标签页链接）→ 见上文 **[团队成员必读 Markdown 索引](#团队成员必读-markdown-索引)**。

| 文件 | 读者 | 作用 |
|---|---|---|
| `paths.yaml` | 全部 Agent | 路径解析 |
| `task-registry.yaml` | Coordinator | 派单队列 |
| **`task-claiming-guide.md`** | **全员** | **任务认领 + Kanban 状态机** — <a href="./task-claiming-guide.md" target="_blank" rel="noopener noreferrer">打开</a> |
| **`自动派单与确认规约.md`** | **全员** | **自动 scan / confirm** — <a href="./自动派单与确认规约.md" target="_blank" rel="noopener noreferrer">打开</a> |
| **`长任务执行规约.md`** | **coordinator / 监管人** | **过夜连跑仍走派单体系** — <a href="./长任务执行规约.md" target="_blank" rel="noopener noreferrer">打开</a> |
| **`feishu/feishu-bitable-webhook-handler.md`** | coordinator | Webhook 运维 — <a href="./feishu/feishu-bitable-webhook-handler.md" target="_blank" rel="noopener noreferrer">打开</a> |
| **`scrum-sprint.yaml`** | **PM + coordinator** | **双周 Sprint 容器、仪式、WIP** |
| **`产品定义评审规程.md`** | **PM / UE / 语义 / 架构 / 前端 Lead** | **PDR / 会签 / DG 三门 + Track-MS V2∥门2**（定义阶段真源） |
| **`产品实现规程.md`** | **前端 / 后端 / 算法 / GDF / PM / coordinator** | **门 3 之后 Sprint 工程交付**（开工 I1 / 联调 I2 / 关闭 I3；`dev` 直推） |
| **`delivery_phase`**（registry + 飞书列） | **全员看板** | **`definition` / `implementation` / `crosscut`** → 飞书「交付阶段」；视图见 `feishu/feishu-bitable-integration.md` §2.1.1 |
| **`feishu/feishu-bitable-integration.md`** | **PM + coordinator + 全员** | Phase 0 Kanban — <a href="./feishu/feishu-bitable-integration.md" target="_blank" rel="noopener noreferrer">打开</a> |
| `feishu/feishu-bitable.yaml` | coordinator | Bitable 列名/状态映射 |
| **`feishu/feishu-project-integration.md`** | PM + coordinator | 飞书项目（⏸ 待审批） |
| `sprints/` | PM + coordinator | 当前 Sprint 看板与 burndown |
| `team-roster.yaml` | lead + coordinator | 认领真名花名册 |
| `repo-registry.yaml` | dev/api/front | 仓路径与 CI |
| `scope-and-responsibility.md` | 人工 + Coordinator | 范围边界 |
| `整体工作计划.md` | **人工检查** | Wave 工程波次（2026-06）；**交付阶段改看 `project-plan.md`** |
| **`project-plan.md`** / `project-plan.yaml` | **全员 / PM** | **当前阶段 S1–S6、大节点、按人日期** — <a href="./project-plan.md" target="_blank" rel="noopener noreferrer">打开</a> |
| `team-collaboration-playbook.md` | **全员** | 团队公约 — <a href="./team-collaboration-playbook.md" target="_blank" rel="noopener noreferrer">打开</a> |
| `team-onboarding.md` | 新人 + mentor | 上手指引 — <a href="./team-onboarding.md" target="_blank" rel="noopener noreferrer">打开</a> |
| `角色AI协作对比手册.md` | **全员** | 按角色查 — <a href="./角色AI协作对比手册.md" target="_blank" rel="noopener noreferrer">打开</a> |
| **`Design.md`** | **ux/ui/frontend/qa/architect** | D8 UI 规范 — <a href="./Design.md" target="_blank" rel="noopener noreferrer">打开</a> |
| `budget-estimate.md` | PM + lead + coordinator | AI token 预算、告警阈值、retro 模板、实测回填机制 |
| `agent-handoffs/产品整体定义/` | PM / **product** / architect / ux / frontend / api / data / qa | **产品整体定义合集**（产品经理产出）：`全系统角色权限体系设计.md`（级别 L0–L4 × 身份场景 + 7 模块/企业主题权限矩阵基线）+ `权限点清单-菜单与按钮.md`（菜单/按钮实现级 RBAC 清单）+ `科技信息展示系统-角色权限体系.md`（前序展示系统单系统稿，已被前者取代）+ `产品职责覆盖差距分析.md`（产品经理角色设立背景） |
| `RFC/RFC-001-git-workspace-redesign.md` | （已 Superseded） | in-place 改造方案，已被 RFC-002 替代；目标布局/路径解耦/worktree/onboarding 设计被 RFC-002 §6 直接继承 |
| **`RFC/RFC-002-gkx-v2-greenfield-rebuild.md`** | **团队管理者 + 架构师 / 各 lead / PM 评审** | **★ gkx-v2 全新根目录重做方案（greenfield rebuild）**：在 GitLab 新建 `gkx-v2/` group，6 个月内逐步把所有职责迁移过去，最终把老根 archive；含本轮 6 项战略决议（S1-S3 + E1/E2/E5）+ 12 子仓 inventory + 白/灰/黑名单 + 6 个月路线图（M0-M6）+ 10 项风险 + 10 项 OPEN 决策 |
| `培训/` | 全员（宣讲/排练） | 团队 AI 协作宣讲 PPT + 逐字稿 + build 脚本 + 预览截图 |
| `../.cursor/rules/` | 全部 Agent | 团队共享 AI 规约（00 公约 + 13 角色 mdc：architect/coordinator/pm/**product**/ux/ui/frontend/api/algorithm/data/devops/qa/**doc**） |

## 双根约定

- **code_root**: `${GKX_ROOT}`
- **docs_root**: `${GKX_DOCS_ROOT}`
- 编排内相对路径均相对 `code_root`，除非写绝对路径

## 与智谱项目原目录同步

原编排位于 `智谱项目/5-实施和开发/agent-delivery/`。  
**执行真源：`${GKX_ROOT}\agent-delivery`**

```powershell
# 1. 从智谱项目镜像
robocopy "${GKX_DOCS_ROOT}\5-实施和开发\agent-delivery" "${GKX_ROOT}\agent-delivery" /E

# 2. 恢复 gkx 路径 + 重新生成功能点 catalog
python ${GKX_ROOT}\agent-delivery\scripts\apply_gkx_overlay.py
```

`/E` 会覆盖同名文件；`apply_gkx_overlay.py` 会自动修正 `task-registry` 双根路径、删除废弃 PDF catalog、运行 `extract_feature_catalog.py`。
