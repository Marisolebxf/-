# METRIC-OPEN-ENT-RISK-核对记录
# ENT-MOD-RISK-METRIC-OPEN-L01 — 风险洞察指标语义与 ODS/DWD 数据缺口核对

> **任务**：ENT-MOD-RISK-METRIC-OPEN-L01
> **角色**：algorithm-agent + data-agent 双 Agent
> **监管人**：human:唐绍祖（§1.4.1 临时语义 Owner）
> **日期**：2026-07-22
> **上游**：ENT-MOD-RISK-PACK-L01 ✅ done（2026-07-18 冻结）

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | ✅ 已闭合 | 8 个 metric 全部在 cfg_metric-ENT-seed 注册 pending_semantic_review |
| #5 开放项（PendingBadge + Popover） | ✅ 已闭合 | Q017/Q018 已登记; catalog ≥3 条 pending_hint ≥80 字 |
| PDR-05 自检 | ✅ 通过 | IA ↔ USM ↔ TRACE 一致 |
| PDR-06 自检 | ✅ 通过 | 算法边界与 DEMO 临时阈值已明确定义 |
| 唐绍祖会签 §1.4.1 | ✅ 签署 | 2026-07-22 |

## §2 风险洞察指标口径摘要（algorithm-agent）

### 2.1 供应链关系分析（E-28）— 5 个 metric

| metric_id | 中文名 | 定义 | 算法边界 | DEMO临时阈值 |
|-----------|--------|------|---------|-------------|
| M_ENT_SUPPLIER_COUNT | 供应商数量 | 企业上游供应商总数,按投资关系/采购链上下游统计 | 前端不计算,从算法查询展示 | >10=丰富,5~10=一般,<5=薄弱 |
| M_ENT_CORE_SUPPLIER_COUNT | 核心供应商数量 | 关键/一级供应商数量,指供应金额占比前5或独家供应的供应商 | 前端不计算,从算法查询展示 | >3=健康,1~3=集中,0=依赖风险高 |
| M_ENT_NODE_CENTRALITY | 节点中心性 | 企业在供应链网络中的PageRank中心度,反映链主地位 | 复用A4计算结果,不新增计算 | >0.5=链主,0.2~0.5=重要节点,<0.2=普通 |
| M_ENT_SUPPLY_CHAIN_RISK | 供应链风险 | 企业供应链风险综合评分,含失信/异常/处罚加权 | 前端不计算评级,仅展示算法结果 | <0.3=低风险,0.3~0.6=中风险,>0.6=高风险 |
| M_ENT_RELATION_STRENGTH | 关系强度 | 企业与上下游的合作紧密程度,综合交易频次/金额/期限 | 前端不计算,算法输出"强/中/弱"三级 | Q017 待确认 |

### 2.2 企业发展痛难点识别（E-29）— 3 个 metric

| metric_id | 中文名 | 定义 | 算法边界 | DEMO临时阈值 |
|-----------|--------|------|---------|-------------|
| M_ENT_PAINPOINT_COUNT | 痛点数 | 企业在技术研发/市场拓展/融资/管理领域的问题数量 | 从前端独立展示,不汇总为综合分 | 0=待评估(无数据),1~2=少,3~5=多 |
| M_ENT_PAINPOINT_SEVERITY | 痛点严重度 | 各痛点的严重程度评级 | 仅用于阅读排序优先级,不转为排名 | Q018 待确认 |
| M_ENT_PAINPOINT_GAP | 改进空间 | 企业与同行/基准之间的差距量 | 仅展示客观差距值,不推荐解决方案 | 不设硬阈值,展示原始差值 |

### 2.3 关键架构约束

| 约束 | 说明 |
|------|------|
| 前端不计算 | 官方风险等级/中心度/严重度全部由算法计算,前端只展示结果 |
| 不生成综合风险分 | 供应链仅展示各维度度量,不聚合为单一总分 |
| 不生成正式排名 | 痛难点严重度仅用于阅读优先级排序,不转换为企业得分或排名 |

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS源表 | DWD表 | ADS表 | pending_ref | 缺口说明 |
|-----------|---------------|---------|-------|-------|-------------|---------|
| M_ENT_SUPPLIER_COUNT | 🔧 | gkx_dwd_org_invest_info | dwd.enterprise_relation | ads.enterprise_centrality | Q017 | 投资关系可解析供应商但口径待确认 |
| M_ENT_CORE_SUPPLIER_COUNT | 🔧 | gkx_dwd_org_invest_info | dwd.enterprise_relation | ads.enterprise_centrality | Q017 | 核心供应商定义待甲方确认 |
| M_ENT_NODE_CENTRALITY | ✅ | — | — | ads.enterprise_centrality | Q017 | 复用A4 PageRank结果 |
| M_ENT_SUPPLY_CHAIN_RISK | 🔧 | gkx_dwd_company_punish_info,gkx_dwd_company_abnormal_info | dwd.enterprise_risk | ads.realdata_enterprise_risk | Q017 | B1风险评分可用,阈值待确认 |
| M_ENT_RELATION_STRENGTH | 🔧 | gkx_dwd_org_invest_info,gkx_dwd_bid_info | dwd.enterprise_relation | — | Q017 | 关系强度算法待工程化 |
| M_ENT_PAINPOINT_COUNT | 🔧 | — | — | — | Q018 | 需多维度ODS综合判断 |
| M_ENT_PAINPOINT_SEVERITY | 🔧 | — | — | — | Q018 | 严重度评级规则待甲方确认 |
| M_ENT_PAINPOINT_GAP | 🔧 | — | — | — | Q018 | 基线基准方案待确认 |

## §4 开放项闭合表

| 编号 | 关联metric | 状态 | 依据 | 待闭合动作 |
|------|-----------|------|------|-----------|
| Q017 | 供应链5 metric | 🟡 团队临时默认 | TRACE 已有登记 | 甲方/何老师确认正式阈值与等级划分 |
| Q018 | 痛难点3 metric | 🟡 团队临时默认 | TRACE 已有登记 | 甲方/何老师确认严重度评级规则 |

> 注:Q017/Q018 不在本任务中闭合,登记为 🟡 并记录会签栏供后续补充。正式阈值以甲方确认为准。

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: IA ↔ USM ↔ TRACE 一致性 | ✅ | E-28/E-29 全部覆盖 |
| PDR-06: 算法边界与前端约束 | ✅ | 架构约束已明确定义 |
| PDR-06: pending_hint ≥80 字 | ✅ | ≥3 条达标 |
| PDR-06: Q017/Q018 不伪闭合 | ✅ | 均标 🟡 |

## §6 语义会签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 语义 Owner（临时代行） | human:唐绍祖 | 2026-07-22 | ✅ 已签署 |
