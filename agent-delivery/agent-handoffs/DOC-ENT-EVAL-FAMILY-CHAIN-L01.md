# DOC-ENT-EVAL-FAMILY-CHAIN-L01 · 企业评估族 — 商业力+竞争力完整链路设计与 LLM 落点（合并包）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent`（algorithm 协作：as-built 事实源由 LUMEN-ENT-EVAL-NARRATE-L01 同会话提供） |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | E-ENT-SCRUM-PDR / definition / P1 / effort 5；原 DOC-ENT-BUSINESS-ANALYSIS-CHAIN-L01 已并入本单不再单独执行 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义/文档任务；产品定义与会签产物完整性优先。未写任何 repos 实现（narrate_eval 代码属 LUMEN-ENT-EVAL-NARRATE-L01 已交付范围，本文只做 as-built 记录）。 |

## 问题清单

- 派单问询确认：不同菜单必须**分立两文**（05.3.3 / 05.3.4），不做一文两章。
- 监管人纠正（已执行）：**口径零改动零评判**——设计范围=现状梳理成文 + LLM 落点 as-built 复用与缺口；初稿 A 表中的口径类开放项（comp_index 权重、单企业 set_mean 退化等）已全部撤回，不登记不展开。
- 条款号核对：E-24=`1.1.1.2.4.2.3.4`（bid-reference L4513）；E-30 对应叶为 `.10`「企业竞争力分析」（bid-reference L4597，页面名「企业综合竞争力评估」）——两文头部已按实核写。
- 写作期间发现 FE REPORT-WIRE（ENT-NARRATE-05 路径 A）**已由 frontend-agent 交付**（lumen-ui-topic `22e1d57`）：`evalReportDocument.ts` 已消费 `diagnosisByCode`（technology=gapText / business=diagnosisText，competitiveness 走 weakLines 既有消费）。两文按**已接线** as-built 书写，非缺口。

## 修改内容

- 新增 `05.3.3-企业商业力评估对比分析.md`（v1.0）：商业力叶链路差异文。A 对照（与 05.3.1 共享六节点骨架）/ B 链路（差异仅 compute=biz_power.run）/ C 取数组装（六维 minmax+weighted、ADVICE 规则、tabs 恒定空态）/ D 润色（as-built 复用 narrate_eval：business 分支、`(enterprise,code)` 键、事实包无六维明细=ENT-EVAL-13 缺口、报告已接线）/ E 契约引用与三态 / F 与技术力差异集中表 / G 开放项（ENT-EVAL-13/14）。
- 新增 `05.3.4-企业综合竞争力评估.md`（v1.0）：竞争力叶链路差异文。双表合成 as-built 公式（三维直取/等权平均、set_average/set_leader）/ `dimension_rows` 每企业 3 行 / 润色按 `(enterprise,code,dimension)` 三元组逐行（审查修正后的协议）/ 报告零改动即同源（weakLines 既有消费）/ G 开放项（ENT-EVAL-15 线上抽样待 QA）。
- `05.3-企业.md` §5 总册加两文指针（05.3.3 / 05.3.4）。
- 落点表 05.3.2 未改动（全域落点真源 v0.9 对三叶的判定未被本单推翻；报告接线态已在其 P1 行语义内）。

## 测试结果

- 文档任务无代码测试；一致性自检：
  - 两文头部条款号与 bid-reference 实文核对一致（E-24 L4513 / E-30 L4597）；
  - 润色契约参数与代码实况逐项核对一致（`TEXT_LIMIT=100` / `timeout=20` / `max_retries=0` / `temperature=0.1` / `PROMPT_PACK=ent.eval.narrate.v3` / 卡协议三元组 / 原因码 `row{i}:long{N}|cause|num:{x}` / `missing:N`）；
  - 结果信封字段名与 `executor.py` 分支实码逐一对照（operating_indicators/tabs/revenue_trend 恒定空态；dimension_rows/set_average/set_leader）；
  - 共享章节一律「引用 05.3.1 不重写」，无双源风险；
  - 金样体例对齐：元信息表 / §1 做什么 / §2 完整逻辑 / §3 取数 / §4 组装 / §5 润色（5.0–5.7）/ §6 执行框架 / §7 报告双路径 / §8 相关文档与开放项 / §9 修订记录。

## 遗留风险

- business / competitiveness 两叶的润色**线上抽样未做**（technology 已验 ok）；QA 批次覆盖后两文 §5.7 状态行同步打勾（观测补记：`narration` 随快照，日志检索 `narrate_eval sub_type=`）。
- ENT-EVAL-13（business 事实包无六维明细）若后续要做，属 LLM 落点增强，需另开实现单；本文只登记不实现。
- 页面名「企业综合竞争力评估」与招标叶名「企业竞争力分析」存在菜单/条款用词差，以五件套 IA 为准，本文两处均标注。

## CI/CD（必填）

- 分支：`dev`（gkx-orchestration，编排仓无业务 CI）
- commit：本文档批次 `[agent:architect-agent] DOC-ENT-EVAL-FAMILY-CHAIN-L01 05.3.3+05.3.4+总册指针+handoff`
- pipeline URL / ID：不适用（无业务 CI）
- 部署 namespace / 镜像 tag：不适用
- K8s rollout：不适用
- dev 测试 URL / 命令与结果：不适用

## 可观测性（建议）

- 无新增埋点（文档任务）；两叶线上验证依赖既有 `narration` 快照与 `narrate_eval` 日志（指引见 05.3.1 §5.3 与 LUMEN-ENT-EVAL-NARRATE-L01 handoff）。

## 涉及文件

- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.3-企业商业力评估对比分析.md`（新增）
- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3.4-企业综合竞争力评估.md`（新增）
- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.3-企业.md`（§5 加指针）
- `agent-delivery/agent-handoffs/DOC-ENT-EVAL-FAMILY-CHAIN-L01.md`（本文件）
