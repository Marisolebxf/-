# POL-EFFECT-MACRO-CALIBER-L01 · 落地实效宏观结果面代理：口径双轨 + calc-logic + 详设

> 总控：[`POL-EFFECT-MACRO-长任务总控.md`](./POL-EFFECT-MACRO-长任务总控.md) §0 · 总派单：[`POL-EFFECT-MACRO-总派单.md`](./POL-EFFECT-MACRO-总派单.md) 段 A0
> 日期：2026-11-09 · 类型：definition · Epic：`E-POLICY-PDR` · 故事：`US-E7-POL-04`

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:architect-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 监管人 2026-11-09 授权长任务 POL-EFFECT-MACRO，后续认领不必再问。协同口径：product-agent（业务读法）、data-agent（白名单/区划，由 A1 承接） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `off` |
| 说明 | 定义任务，不以缩文为目标；口径诚实、双轨分节、ext 契约与 ⚠️ 约束须写全。未用 YAGNI 跳过 D8/D9/D10、可观测、架构铁律（D9 ⚠️ 角标、D16/D17/D18 均已入稿）。未写代码。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本叶为文档定义，未触发大输出压缩） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（未改 05.6.2 §2 时序图；调用链不变） |
| 图 diff | 无。前端 → Java → Python `/internal/*` 不变；仅 Python 取数源增加只读 `gkx` 宏观表 |
| 会签态 | N/A |
| 说明 | 若 B 叶新增 Python 读取模块与 Feign 字段，由 B/C 叶在各自 handoff 更新图 |

## 范围与实现（对照 bid-reference / 需规 114–116）

范围：只改口径与详设，**不写算法、不灌数、不改 FE**。需规 115「自动计算政策指标得分」落地实效一项由本叶冻结「可算路径」口径；需规 114/116 无变化。

### 改动文件

| 文件 | 改动 |
|---|---|
| `agent-delivery/metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md` | 顶部新增 v3 addendum；基础信息「数据支持度」行加限定；新增「口径双轨」节：**A 正本三维轨（当前不可算）** 与 **B 宏观结果面代理轨（`macro_outcome_proxy` 临时默认可算）** 分节；B.1 诚实性、B.2 `ext` 契约、B.3 D17、B.4 D4/D16/D18、B.5 与 v2 公式/gapfill 关系、B.6 归一选项。正本全文与判档「完全不支持」**未改** |
| `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md` | v0.5；§3 引言与「落地实效」行改双轨读法；新增 §3.2（代理读法、主辅源、`ext.caliber`、与 gapfill 并存、⚠️、空态、分层、D17、归一选项）；§4.2 `cards.effect` 行；§8 增补「不宣称两库支持正本三维」 |
| `agent-delivery/客户决策清单跟踪表.md` | QPOL-02 已有 2026-11-09 增补行，措辞与本叶一致，**本叶未再改动** |
| 本 handoff | 新增 |

### 冻结的口径要点

1. 正本三维：**当前不可算**；宏观库 / 行业分析库**不直接支持**正本三维，全仓禁止此类表述。
2. 临时默认：`cards.effect` 继续挂 `M_POLICY_IMPLEMENTATION_EFFECT`，`ext.caliber=macro_outcome_proxy`，UI ⚠️「待甲方确认」，不出综合分。
3. 主源 `dwd_macro_index_data` + `dwd_dim_index_attribute` + `dwd_dim_admin_area`（只读）；辅源 `dwd_industry_analysis_*` 仅叙述，`companies`（102 行）禁用。
4. 指标白名单（≤12）、窗口、区划键、指标方向：**A0 不写死，由 A1 冻结**。
5. 可算条件：窗口内至少 1 个白名单指标有有效值；否则 `computable=false`，不写 0。
6. 与 v2 公式：不并入同一张城市卡；与 gapfill：并存、不拼平均、同卡仅一个 caliber。

## 偏离说明

- 派单要求「客户决策清单 QPOL-02 增补一行」：registry DoD 含此项，但 2026-11-09 增补行已由总控建单提交落库（`4b723dd9`），措辞核对一致，故不重复写。
- 总控 §0.4 写「正本三维公式保留在 calc-logic」：已保留且未改一字，新增内容均落在独立「口径双轨」节。

## 会签说明

| 角色 | 口径 | 状态 |
|---|---|---|
| architect-agent | 双轨分节、ext 契约、调用链不变、D16/D17/D18 | 本叶主写，通过 |
| product-agent | 「结果面代理」读法、禁用「落地率/兑现率/满意度」措辞 | 已按总控 §0.10 与 §0.4 对齐文案，通过 |
| data-agent | 主辅源范围、`companies` 禁用、白名单留 A1 | 范围对齐，具体白名单由 A1 交付 |
| 监管人 | `human:淮政玮` 总控 §0 已拍板（授权句落款 2026-11-09） | 引用，不另签 |

结论：**会签通过**（definition：口径稿落盘，可推进 integration → ready_to_sign）。甲方口径仍为 QPOL-02 🟡，归一前一切为团队临时默认。

## 产物清单

| 类型 | 路径 |
|---|---|
| calc-logic | `agent-delivery/metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md`（口径双轨节） |
| 详设 | `05.6.2-深圳政策现状分析.md` v0.5（§3.2） |
| handoff | 本文件 |
| 代码 / CI / 截图 | 无（定义任务） |

## 验收证据

| DoD 项 | 证据 |
|---|---|
| 正本「当前不可算」与代理可算路径分节；禁止宣称两库直接支持正本三维 | calc-logic「口径双轨」A/B 两节；A 节明文禁止；05.6.2 §8 同步 |
| 05.6.2 §3/§3.1 增补代理读法、`ext.caliber`、与 gapfill 并存、⚠️ | 05.6.2 §3 引言 + 落地实效行 + §3.2 |
| QPOL-02 增补一行 | 客户决策清单已有 2026-11-09 增补行，核对一致 |
| handoff + 会签关键词 | 本文件「会签说明」；registry note 含「会签通过」 |

## 架构合规自检（00-team-constitution §2）

| 铁律 | 结论 |
|---|---|
| 1 算法只在 Python | ✅ 宏观读取与合成只在 Python |
| 2 调用链 前端→Java→Python | ✅ 不变；Java 只透传 ext |
| 3 NebulaGraph | ✅ 不涉及图谱 |
| 4 可观测性 | ✅ 不改；B/C/D 叶沿用 |
| 5 CI/CD | ✅ 设计类 cicd: skip |
| 6 demo2 只读 | ✅ 未触碰 |
| 7 共享聚合核心 | ✅ 不改 |
| 8 数据策略 | ✅ 三方源只读，不写供应方 |
| 9 前端规范 D8 | ✅ 未改 FE；⚠️ 角标沿用 Arco 图标家族 |
| 10 数据血缘 D9 | ✅ metric_id 不变；D3 PendingBadge ⚠️；D4 在代理实算后可 live，归一前仍带 ⚠️ |
| 11 交互 D10 | ✅ 无新交互 |
| 12 D12 demo/lumen 隔离 | ✅ 不涉及 demo 服务调用 |
| 13 D14 对象存储 | ✅ 不涉及 |
| 14 D16 缺项 | ✅ gapfill 仅 `gapfill_`，与代理并存 |
| 15 D17 合规/合理 | ✅ B.3 规定冲突时成对展示名，由 B 叶核对 |
| 16 D18 可实现 | ✅ 禁止接口写死 mock |

## 问题清单

- 白名单 / 窗口 / 指标方向未冻（A1）。
- 宏观表实际列名与区划键对齐方式未在本叶核对（只读库探查属 A1）。
- 009/011 样本 `score=50` 将在 B 叶落地后变化，E1 断言以总控 §3 为准。

## 测试结果

文档类任务，无代码自检。人工核对：calc-logic 正本章节未被改写（仅在文首与「口径定义」后插入新节）；05.6.2 §3.1（gapfill 双入口）未改动。

## 遗留风险

- B 叶若发现与唐绍祖锁定合规闭包冲突，须按 D17 落副本包 + 成对展示名，并回写本口径 B.3。
- 宏观结果面代理被误读为「落地率」：靠 ⚠️ + 文案禁用词 + `ext.track_a_status` 约束，FE/E1 需断言。
- 甲方归一前，三选一（保留代理 / 回切三维 / 双轨）未定，下游文案须保持「待甲方确认」。

## 下游放行建议

- `POL-EFFECT-MACRO-DATA-L01`（A1）：A0 达 `integration` 即可开工，可升 ready。
- `POL-EFFECT-MACRO-ALGO-L01`（B）：口径稿已落盘；但**白名单与区划键**未冻，须 A1 完成后才升 ready / 标 integration。

## CI/CD

- 分支：`origin/dev`
- commit：见 registry note（设计类 `cicd: skip`）
- pipeline / K8s：N/A（文档任务）

## 可观测性

N/A（未改运行时）。

## 涉及文件

- `agent-delivery/metrics/calc-logic/POLICY/M_POLICY_IMPLEMENTATION_EFFECT.md`
- `agent-delivery/agent-handoffs/产品整体定义/科技专题服务系统-完整详细设计/05.6.2-深圳政策现状分析.md`
- `agent-delivery/agent-handoffs/政策模块-E7/POL-EFFECT-MACRO-CALIBER-L01.md`

## 成本（回填 registry）

| 字段 | 值 |
|---|---|
| actual_tokens | 约 90000 |
| model_used | claude-sonnet-5.5 |
| actual_cost | 0.8 |
| cost_warn | green |
