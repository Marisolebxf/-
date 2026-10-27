# DOC-CHAIN-SZ-FAMILY-L01 · 深圳产业对比与发展 — 完整链路设计 + LLM 落点（05.2.4）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:coordinator-agent`（代持 architect 帽直接撰写——两轮子会话均在动笔前遭 invalid_argument 环境性中断，按停工预案转主会话产出） |
| supervised_by | `human:徐滕强` |
| claim_type | `coordinator_dispatch` |
| 说明 | E-ENT-SCRUM-PDR 产业链队列 C3 / definition / P1 / effort 5 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义/文档任务；不写 repos 实现（prompt 迁移进 SZ-01 实现单建议）。 |

## 问题清单

- 两轮子会话（5e497ab2 / a2849012）均在「准备动笔」阶段遭 `invalid_argument` turn 级错误中断，无产物残留（已核实编排仓无 05.2.4 残稿）。转主会话产出，调研结论直接复用。
- 实码核对修正：development 的硬失败语义=「路径数 <2 判定失败」，与文案润色「失败退稿任务仍 success」**不同族**——SZ-02 特别标注迁移时不得混淆（这是与评估族契约最大的语义差异点）。
- SZ_MOCK 等权 mock 分的 ceiling 为源码既有 ponytail 注释（QC08），本文照录不评判，退役路径登记 SZ-04。
- 条款关联：深圳叶挂 `1.1.1.2.4.2.3.5`「深圳企业现状分析」（产业链定位/多城市对标）+ 专题侧深圳组合页；与招标子叶名的映射在 §1 注明。

## 修改内容

- 新增 `05.2.4-深圳产业对比与发展链路.md`（v0.1）：对比+发展合并族（含快照依赖边）；§2.1 两张 Mermaid（差异 flowchart 双 subgraph + 全链时序图）；§3 两叶 as-built 逐行对照（STAGE_LABELS / 四维 / SZ_MOCK ceiling / NARRATIVE_SYSTEM 与 PATH_SYSTEM 原文 / FORBIDDEN_KPI_BLOCKS / 硬失败语义 / SILENT_KEYS）；§5 落点表 SZ-1~5（流程内 LLM 两落点 as-built + 三处规则锁死 + prompt 迁移治理项）+ G 系列预登记（无 Key 语义未显式建模等）；§8 开放项 SZ-01~04。
- `05.2-产业链.md` 总册加 05.2.4 指针。

## 测试结果

- 文档任务无代码测试；一致性自检：STAGE_LABELS / PROMPT_PACK / DIM_MODEL / NARRATIVE_SYSTEM / PATH_SYSTEM / GOAL_KEYS / FORBIDDEN_KPI_BLOCKS / SILENT_KEYS / 快照多代键 均与两 .py 实码逐一对照；Mermaid 2 张；总册指针已加且编号顺延无冲突。

## 遗留风险

- SZ-02（流程内 LLM 无 Key/失败语义显式建模）是实现单必做项：SZ-2 的「路径数 <2 硬失败」是判定语义不得弱化，而 prompt 迁移后的文案失败应退规则稿/空态——两者边界须在实现单测试里分别锁死。
- FE 缺口行级锚点留实现单核对（本文不臆测行号）。

## CI/CD（必填）

- 分支：`dev`（gkx-orchestration，无业务 CI）
- commit：`[agent:coordinator-agent] DOC-CHAIN-SZ-FAMILY-L01 05.2.4 + 总册指针 + handoff`
- pipeline / 部署 / K8s：不适用

## 可观测性（建议）

- 无新增埋点；实现后沿用族内 narration/honesty 快照指引。

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.2.4-深圳产业对比与发展链路.md`（新增）
- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.2-产业链.md`（§8 指针）
- `agent-delivery/agent-handoffs/DOC-CHAIN-SZ-FAMILY-L01.md`（本文件）
