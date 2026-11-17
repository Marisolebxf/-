# ZMATE-RPT-ARCH-L01 · 架构：Demo 边界 + harness 对照（定档）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 门 1 有条件闭合后解锁；默认签收授权见 G1 简报 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义·架构文档；不以缩代码为目标；未用 YAGNI 跳过 D12/调用链/D9 诚实约束 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机编排仓文档任务，未挂载 headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `ARCH-ZMATE-RPT-DEMO-BOUNDARY` |
| 图 diff | 新增 Demo 态 Mock 调用链与 Graph 阶段对照；正式链保持虚线目标态；禁止事项：lumen 直连 / 假 live / 单页假全链 |
| 会签态 | `approved`（定档 + 默认签收授权） |
| 说明 | Mermaid 在 ARCH 正文 §4.2；节点名对齐建设方案 §9.2 路由 |

## 范围与实现

- 模块：ZMATE 战略报告创作 Demo 样机架构定档
- 实现：仅文档；定档 **Demo 样机 / 纯前端 Mock**；仓边界 `demo-ui-topic`；对照 harness 澄清→Judge；Q161 废稿边界写清
- 对照：`architecture-baseline` D12；建设方案 §9；USM/IA/WF；门 1 有条件闭合

## 偏离说明

- 无偏离。真后端切流 ARCH 明确后置，不在本叶范围（与 FDE「明确跳过」一致）。

## 产物清单

- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/ARCH-ZMATE-战略报告创作.md`
- `agent-delivery/agent-handoffs/ZMATE-RPT-ARCH-L01.md`

## 验收证据

- DoD：纯 Mock 边界、D12、调用链只读、harness 对照表、handoff — 齐
- 门 1 / USM / IA / WF / 建设方案 §9 / harness §6 — 无冲突
- AV-0：handoff + evidence 已设；联调确认关键词：会签通过

## 问题清单

- 无阻断项。Q156–Q161 仍为临时默认（门 1 已采纳）；Q160 导出门禁留实现波次。
- 真后端切流 ARCH 未开单（按定档后置）。

## 修改内容

- 新增定档文档 ARCH-ZMATE-战略报告创作.md（Demo/纯 Mock、D12、调用链只读、harness 阶段对照、Q161 FE 边界）
- 本 handoff
- 未改业务代码 / demo-ui-topic / lumen-*

## 测试结果

- 结构与 DoD 对照通过
- 架构合规自检 7 项均通过（见下）

## 遗留风险

- UI-HIFI 未齐前 FE-DEMO 仍不可开工（会签 C）
- 旧 L01–L08 若未按 Q161 清掉，可能污染新路由语义（FE 叶须显式废弃）

## CI/CD（必填）

- 分支：`dev`
- commit：`2a4195b0f`（定档正文）；本 handoff 补章跟随提交
- pipeline URL / ID：N/A（编排仓文档）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：N/A（定义文档）

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A
- traceId：N/A
- Tempo / Loki：无

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/ZMATE-战略报告创作/ARCH-ZMATE-战略报告创作.md`
- `agent-delivery/agent-handoffs/ZMATE-RPT-ARCH-L01.md`

## 架构合规自检

| 铁律 | 结论 |
|------|------|
| D12 demo/lumen 隔离 | ✅ 定档仅 demo；禁 lumen 直连 |
| 调用链只读声明 | ✅ 目标态 vs Demo 态已写清 |
| 算法只在 Python | ✅ 本阶段无算法实现 |
| D8 Design / Arco | ✅ 指向 UI-HIFI / FE 叶 |
| D9 诚实 Mock / 禁假 live | ✅ 四态示意；不改绿 |
| D10 人闸 / Judge | ✅ 对齐 WF；实现归 FE |
| 禁改业务代码 | ✅ 本叶仅文档 |

## Cost 回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 45000 |
| model_used | claude-opus-4.6 |
| actual_cost | 0.35 |
| cost_warn | green |
