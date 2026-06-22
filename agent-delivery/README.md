# agent-delivery — 多智能体编排根目录

本目录是 **Coordinator 与各 Agent 的会话入口**，已从智谱项目镜像至 `E:\gkx_src\agent-delivery`。  
代码在 `E:\gkx_src\*` 各仓修改；设计文档与**验收功能点**在 `docs_root/2-概要设计/2-1需求分析` 只读引用（不读招标 PDF）。

## 快速开始

1. 在 Cursor **新开 Agent 会话**，工作区打开 `E:\gkx_src`（或至少包含本目录 + 目标 repo）
2. 阅读 [`../COORDINATOR-START.md`](../COORDINATOR-START.md) 或 [`整体工作计划.md`](整体工作计划.md)
3. Coordinator 读取 `task-registry.yaml`，选取 `status=pending` 且依赖已 `done` 的 leaf 派单
4. 执行 Agent 完成后写 `agent-handoffs/{task-id}.md`，更新 task 状态

## 目录结构

```
agent-delivery/
├── paths.yaml                    # 双根路径真源（code_root + docs_root）
├── task-registry.yaml            # 任务队列（Coordinator 派单）
├── system-wbs.yaml               # 七要素 + 34 页 + Wave 0–5
├── repo-registry.yaml            # demo ↔ lumen 仓映射
├── 整体工作计划.md                # ★ 人工检查用总计划
├── 项目工程化交付模式.md          # 总控 Prompt / 铁律
├── scope-and-responsibility.md   # 智树边界
├── requirements-master-index.yaml
├── acceptance-*.yaml / *.md      # 甲方验收体系
├── formal-docs-registry.yaml     # V6 / 时序图 / API 契约索引
├── 数据库设计.md / graph-engine.md / observability.md / cicd-pipeline.md
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
│   └── RFC-002-gkx-v2-greenfield-rebuild.md  # ★ gkx-v2 全新根目录重做方案（greenfield，6 个月迁移）
└── scripts/                      # 工具脚本
```

## 关键文件

| 文件 | 读者 | 作用 |
|---|---|---|
| `paths.yaml` | 全部 Agent | 路径解析 |
| `task-registry.yaml` | Coordinator | 派单队列 |
| `repo-registry.yaml` | dev/api/front | 仓路径与 CI |
| `scope-and-responsibility.md` | 人工 + Coordinator | 范围边界 |
| `整体工作计划.md` | **人工检查** | 阶段、并行、里程碑 |
| `team-collaboration-playbook.md` | **全员** | 团队公约、人机分工、Cursor team 配置 |
| `team-onboarding.md` | 新人 + mentor | 1 天上手指引 |
| `角色AI协作对比手册.md` | **全员（按角色查）** | 12 角色 × 8 维度对比（AI 之前 vs AI 之后），含明天起 3 件事 |
| **`Design.md`** | **ux / ui / frontend / qa / architect 必读** | **前端权威 UI 规范（D8 决策，2026-06-18 升级为 Figma 风格稿落地版，14 节）**：§0 给 AI 的执行指令 / §1 设计定位 / §2 视觉气质 / §3 页面骨架 / §4 色彩 / §5 字体 / §6 圆角描边阴影 / §7 通用组件 / §8 地图分析工作区 / §9 图表 / §10 交互状态 / §11 响应式 / §12 AI 生成规则 / §13 推荐实现映射 / §14 验收清单（8 检查 + 6 验收）；新页面权威栈 = React + Vite + `@arco-design/web-react`；主色固定 `#165DFF` |
| `budget-estimate.md` | PM + lead + coordinator | AI token 预算、告警阈值、retro 模板、实测回填机制 |
| `agent-handoffs/产品整体定义/` | PM / **product** / architect / ux / frontend / api / data / qa | **产品整体定义合集**（产品经理产出）：`全系统角色权限体系设计.md`（级别 L0–L4 × 身份场景 + 7 模块/企业主题权限矩阵基线）+ `权限点清单-菜单与按钮.md`（菜单/按钮实现级 RBAC 清单）+ `科技信息展示系统-角色权限体系.md`（前序展示系统单系统稿，已被前者取代）+ `产品职责覆盖差距分析.md`（产品经理角色设立背景） |
| `RFC/RFC-001-git-workspace-redesign.md` | （已 Superseded） | in-place 改造方案，已被 RFC-002 替代；目标布局/路径解耦/worktree/onboarding 设计被 RFC-002 §6 直接继承 |
| **`RFC/RFC-002-gkx-v2-greenfield-rebuild.md`** | **团队管理者 + 架构师 / 各 lead / PM 评审** | **★ gkx-v2 全新根目录重做方案（greenfield rebuild）**：在 GitLab 新建 `gkx-v2/` group，6 个月内逐步把所有职责迁移过去，最终把老根 archive；含本轮 6 项战略决议（S1-S3 + E1/E2/E5）+ 12 子仓 inventory + 白/灰/黑名单 + 6 个月路线图（M0-M6）+ 10 项风险 + 10 项 OPEN 决策 |
| `培训/` | 全员（宣讲/排练） | 团队 AI 协作宣讲 PPT + 逐字稿 + build 脚本 + 预览截图 |
| `../.cursor/rules/` | 全部 Agent | 团队共享 AI 规约（00 公约 + 13 角色 mdc：architect/coordinator/pm/**product**/ux/ui/frontend/api/algorithm/data/devops/qa/**doc**） |

## 双根约定

- **code_root**: `E:/gkx_src`
- **docs_root**: `e:/实施/2025/智谱-深圳国科信`
- 编排内相对路径均相对 `code_root`，除非写绝对路径

## 与智谱项目原目录同步

原编排位于 `智谱项目/5-实施和开发/agent-delivery/`。  
**执行真源：`E:\gkx_src\agent-delivery`**

```powershell
# 1. 从智谱项目镜像
robocopy "e:\实施\2025\智谱-深圳国科信\5-实施和开发\agent-delivery" "E:\gkx_src\agent-delivery" /E

# 2. 恢复 gkx 路径 + 重新生成功能点 catalog
python E:\gkx_src\agent-delivery\scripts\apply_gkx_overlay.py
```

`/E` 会覆盖同名文件；`apply_gkx_overlay.py` 会自动修正 `task-registry` 双根路径、删除废弃 PDF catalog、运行 `extract_feature_catalog.py`。
