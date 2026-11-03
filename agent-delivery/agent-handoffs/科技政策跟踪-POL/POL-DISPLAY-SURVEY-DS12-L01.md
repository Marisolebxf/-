# POL-DISPLAY-SURVEY-DS12-L01 · 科技政策跟踪调研 · 政策效果推演

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:arch-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权。本叶只写分册与本 handoff，不改注册表状态 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义任务，不缩文档。与总派单强度一致 |

## 范围

只覆盖 DS-12 政策效果推演。用户故事 `US-DS-POL-06`。SRS 序号 232–242。对照任务 `FE-POL-03A`（integration）。

展示对外只走 `/display/v1/policy/**`。不写 API-POL 字段表，不改业务仓，不改 WBS，不改别人的分册。`E-E7-POLICY-M1-L06` 不写成实现路径。

指标与任务均经 MCP 核对：`M_POLICY_SIMULATE`（MODEL，D4=mock）、`M_POLICY_DEEP_171_1`（MODEL，D4=mock）、`M_POLICY_LAYOUT_REC_COUNT`（STAT，D4=mock）。未读 `cfg_metric-POLICY-seed.yaml`、`metric-readiness-matrix-POLICY.yaml`、`task-registry.yaml`。

## 产物路径

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/DS-12.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-SURVEY-DS12-L01.md`（本文件）

## 三档计数

| 档 | 条数 |
|---|---|
| 可接统计读面 | 0 |
| 501 | 10 |
| 跨项索引 | 2 |

合计 12 条。明细与依据在 `survey/DS-12.md`。D4 均为 mock 的模型仍记 501，不写成已上线。

## 分键结论

推演与专题「政策布局推荐」分键。布局推荐是跨项索引，不能顶替推演。

- 推演键：`M_POLICY_SIMULATE`，`algorithm_type=MODEL`，D4=`mock`，`srs_refs` 为空。序号 232–234 挂这一个模型，真路径 501。
- 布局推荐键：`M_POLICY_DEEP_171_1`（MODEL，D4=mock，算法库序号 171）与 `M_POLICY_LAYOUT_REC_COUNT`（STAT，D4=mock，171 对冲条数）。计数类型是 STAT，仍然不能当作 DS-12 的可接统计读面。需规把该计数挂到展示序号 241，不改变 241 的判定：路径预测模型未见，241 为 501。
- 关联分析（序号 240）走第 7 项读图，指标 `M_POLICY_RELATION_DEGREE`（GRAPH，D4=mock），判定跨项索引。
- 未见布局推荐的展示专单。`E-E7-POLICY-M1-L03` 只有焦点、力度、效果，不含布局推荐。

## 问题清单

- 无阻塞。口径 🟡（如 QPOL-02）照实留在指标侧，本叶不停工。
- `FE-POL-03A` 停在 integration，handoff 写明改动停本地待人工验收。页头「布局建议」卡是复刻壳，不是布局推荐已接入。

## 修改内容

- 新增 `survey/DS-12.md`：11 条 SRS 叶加 1 条布局推荐分键，共 12 条判定。
- 新增本 handoff。

## 测试结果

- 文档叶。无业务仓测试。
- 三档合计 0+10+2=12，与判定表行数一致。

## 遗留风险

- 契约 `BE-POL-CONTRACT-01` 仍为 backlog。冻结前推演、解析、解读报告的真路径保持 501。
- 序号 241 的需规引用把布局建议条数挂进推演页。详设若沿用该引用，会把跨项索引写成推演结果。本分册已标明不得沿用。

## CI/CD（必填）

- 分支：编排仓本地工作区，未 commit、未 push
- commit：无
- pipeline URL / ID：无
- 部署 namespace / 镜像 tag：无
- K8s rollout：无
- dev 测试 URL / 命令与结果：文档叶，无

## 可观测性（建议）

- 无代码改动，无新埋点

## 涉及文件

- `agent-delivery/agent-handoffs/科技政策跟踪-POL/survey/DS-12.md`
- `agent-delivery/agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-SURVEY-DS12-L01.md`

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 未计 |
| model_used | 未计 |
| actual_cost | 未计 |
| cost_warn | green |
