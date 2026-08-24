# PLAN-ZONGJI-MASTER-L01 · 总集大项目整体计划落盘

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:郭万迎` |
| supervised_by | `human:郭万迎` |
| claim_type | `pull` |
| 说明 | Cursor MCP `task-registry` 本会话未挂载；经 `scripts/task-mcp-cli.mjs` 认领并 `in_progress`。依赖 `PLAN-PROC-02-LAYOUT-L01` 当时为 `review`（目录已在仓） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `N/A`（定义·文档类） |
| 说明 | 未压文档完整性 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶只改编排仓 Markdown |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 本叶不改调用链/存储流图 |
| 会签态 | N/A |
| 说明 | 总集计划摘要，非 ARCH-IMPL |

## 问题清单

- 飞书 Open API 当时无 wiki/sheets 读权限；以本地 Excel 导出为准
- 工作簿无【05】页
- 【08】页名「930」与总览锚点「830」并存（照抄）
- 【09】总览写状态滞后；关键里程碑大量已延期
- 【10】二轮大量「待定」；定增开发日期由序列号换算为 2026-10-08～10-30
- 智库问数/报告「总集准入」结束日空、「上线」多在 11/23，与总览 1115 锚点并存

## 修改内容

- `01-总集大项目整体计划/总集大项目整体计划表.md`：总览 9 系统 + 分系统节点；【03】智库全表明细
- `01-总集大项目整体计划/与总集对齐文档索引.md`：飞书链 + `D:\深圳市国际科技信息中心\0、项目周报\周报&风险&WBS.xlsx` + 页签
- 更新本夹 README、卷 02 INDEX、stub、`工程过程/INDEX.md` 日期

未改：`project-plan.md/.yaml`、`system-wbs.yaml`、`scrum-sprint.yaml`、`PLAN-S5` 状态。未写入对接工作计划、汇报材料清单。未做 S4/S5/S6 对照列（PM 确认）。

## 测试结果

- 源表用 officecli `view … text --range` 抽行；【03】A1:M77 全表入仓
- 相对链接：夹内 README ↔ 计划表 ↔ 索引；上指 `../INDEX.md`

## 遗留风险

- 本地 Excel 不进 git，路径仅本机有效；飞书更新后需重新导出再刷摘要
- 登记表 DoD 仍含对接计划、汇报清单、project-plan 对照——本波按聊天确认裁掉，待 coordinator 改 DoD 或开后续叶

## CI/CD（必填）

- 分支：`dev`（编排主仓）
- commit：待 PM 确认后提交（本 handoff 时尚未 commit）
- pipeline URL / ID：文档叶，无业务镜像
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：打开 `01-总集大项目整体计划/README.md` 点计划表与索引

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId（dev 抽样）：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/总集大项目整体计划表.md`
- `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/与总集对齐文档索引.md`
- `agent-delivery/工程过程/02-策划与监控/01-总集大项目整体计划/README.md`
- `agent-delivery/工程过程/02-策划与监控/INDEX.md`
- `agent-delivery/工程过程/02-策划与监控.md`
- `agent-delivery/工程过程/INDEX.md`
- `agent-delivery/agent-handoffs/PLAN-ZONGJI-MASTER-L01.md`

## 验收对照 DoD

| DoD（登记表原文） | 本波 |
|---|---|
| 已落盘总集大项目整体计划表 | 有；阶段/出门日/表内负责方；专题负责方列照抄，不写合同论述 |
| 与总集对齐的计划文档索引 | 有 |
| 总集对接工作计划 | **暂不做**（PM 确认） |
| 总集汇报材料清单 | **暂不做**（PM 确认） |
| 表与 project-plan S4/S5/S6 对照列 | **暂不做**（PM 确认）；待确认项见计划表 §11 与本 handoff 问题清单 |

## 下一步

1. PM 审摘要与智库明细；同意后 commit（`[human:郭万迎]`）
2. coordinator 收本 handoff；知悉 DoD 裁项
3. 叶 3：`PLAN-ZHISHU-PMBOK-L01`
