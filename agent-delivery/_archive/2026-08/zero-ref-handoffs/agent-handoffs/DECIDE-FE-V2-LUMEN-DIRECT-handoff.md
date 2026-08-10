# DECIDE-FE-V2-LUMEN-DIRECT · 调度落实 handoff

> **任务**：采纳孔东建议 — Track-MS V2 直落 lumen，取消复刻链  
> **日期**：2026-07-12  
> **执行**：[agent:coordinator]

## 范围与实现

- 新增决策真源：`agent-delivery/decisions/DECIDE-FE-V2-LUMEN-DIRECT-2026-07-12.md`
- `产品定义评审规程.md` 升至 **v2.1**（§5.7 V2 定义、流程图、§9 task 字段、附录 E）
- `task-registry.yaml`：3 条 `ENT-MOD-*-V2-DEMO` → `repo: ui_topic.lumen`、`branch: dev`、DoD 按 lumen 准生产
- `sprints/`、`scrum-sprint.yaml`、`team-members.md`、`paths.yaml`、`repo-registry.yaml` 同步

## 架构合规自检

| 铁律 | 状态 |
|------|------|
| demo 禁止 merge 进 lumen | ✅ 未 merge；直接在 lumen 开发 |
| 前端只调 Java REST | ✅ 不变 |
| D8 Arco 权威栈 | ✅ lumen 为 Vue + @arco-design/web-vue |
| 可观测性 observability.ts | ✅ 复用 lumen-ui-science-pc 框架 |

## 后续（孔东 / 曹丽影）

1. 确认 `lumen-ui-topic` 本地 clone 与 `dev` 分支就绪
2. 从 `lumen-ui-science-pc` 对齐框架骨架（layout / request / observability）
3. V1 完成后启动 `ENT-MOD-SEARCH-V2-DEMO`（优先企业查询）
4. 实现 **内部评审模式** 开关（门 2 walkthrough 用）

## 产物清单

- 决策：`decisions/DECIDE-FE-V2-LUMEN-DIRECT-2026-07-12.md`
- 规程 v2.1、registry、sprint 更新（本 commit）
