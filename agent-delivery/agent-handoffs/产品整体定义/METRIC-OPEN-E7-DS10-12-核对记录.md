# METRIC-OPEN-E7-DS10-12-核对记录

> **任务**：POLICY-METRIC-OPEN-L01  
> **角色**：algorithm-agent（主）+ data-agent（协作核对）  
> **监管人**：human:王惠 · 方案 B 双签：human:王惠 + human:唐绍祖  
> **日期**：2026-08-05  
> **上游**：POLICY-PACK-L01 / DS10-12-PACK-L01（integration）· POLICY-UX-L01（integration）  
> **范围**：只做定义与血缘真源，不替甲方拍板权重/口径

---

## §1 适用性结论（Track-MS 五件套 #4 / #5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡 | ✅ 定义闭合（待双签） | 19 条 `M_POLICY_*` 已在 `cfg_metric-POLICY-seed.yaml`；算法定义卡 `metrics/metric-spec-POLICY.yaml` |
| #5 开放项 | ✅ 已登记并回写 | QPOL-01/02/03/05/07 仍为 🟡；gap catalog 提供 Pending 文案 |
| PDR-05 自检 | ✅ | E7 / DS10-12 包内 metric_id 均可回指 seed |
| PDR-06 自检 | ✅ | definition / formula / source_tables 齐全；缺口显式标注 |
| 王惠+唐绍祖双签 | ⏳ pending_signoff | 本记录供签署；未伪造会签 |

**结论**：五件套第 4–5 项**适用且文档闭合**；甲方 🟡 不阻断定义交付，**阻断**宣称 FULL 口径与门 1「无条件闭合」。门 1 可走「有条件闭合」并附 QPOL 清单。

---

## §2 模块消费矩阵

| metric_id | E7 落点 | DS10-12 落点 | mapping | pending |
|-----------|---------|--------------|---------|---------|
| M_POLICY_TOTAL_COUNT | 查询/时序 KPI | 全景 KPI | ✅ | — |
| M_POLICY_LEVEL_DIST | 画像/全景 | 全景环图 | ✅ | — |
| M_POLICY_TYPE_DIST | 分布 | 全景分布 | ⚠️ | QPOL-01 |
| M_POLICY_TIMESERIES | P-70 时序 | 动向 Tab | 🔧 | QPOL-07 |
| M_POLICY_NATIONAL_DIST | 区域对比辅 | 地图 | ✅ | — |
| M_POLICY_SZ_DIST | P-73 | 深圳分布 | ✅ | — |
| M_POLICY_VALIDITY_RATE | 门户/维护 | 治理看板 | 🔧 | — |
| M_POLICY_INTENSITY_INDEX | 门户排行 | 比对/对比 | ⚠️ | QPOL-02 |
| M_POLICY_INDUSTRY_COVERAGE | 力度辅 | 对比 | 🔧 | — |
| M_POLICY_RELATION_DEGREE | 图谱 | 拆解/对比 | 🔧 | QPOL-03 |
| M_POLICY_FOCUS_INDEX | 评价/解读 | DS-11 | 🔧 | QPOL-02 |
| M_POLICY_INTENSITY_SCORE | P-70/对比 | 比对/核增 | 🔧 | QPOL-02 |
| M_POLICY_EFFECT_SCORE | 评价/推演 | DS-11/12 | 🔧 | QPOL-02 + 采购 |
| M_POLICY_SHORTBOARD_COUNT | P-73/评价 | DS-11 | 🔧 | QPOL-02 |
| M_POLICY_OPPORTUNITY_COUNT | 评价 | DS-11 | 🔧 | QPOL-02 |
| M_POLICY_LAYOUT_REC_COUNT | 推荐方案 | 推演/研报 | 🔧 | QPOL-02 |
| M_POLICY_SUPPORT_STRENGTH | P-72/73 | 核增对比 | ⚠️ | QPOL-02 |
| M_POLICY_INDUSTRY_FIT | P-72/73 | 舆情/对比 | 🔧 | QPOL-03 |
| M_POLICY_IMPLEMENTATION_EFFECT | P-73/舆情 | DS-10 舆情 | 🔧 | QPOL-02 + 采购 |

状态分布：✅4 · 🔧12 · ⚠️3 · ❌0（与 seed 汇总一致）。

---

## §3 算法定义卡摘要（algorithm-agent）

权威文件：`agent-delivery/metrics/metric-spec-POLICY.yaml`

| 模型 | 输出指标 | Wave0 权重/阈值（临时） |
|------|----------|-------------------------|
| POLICY_FOCUS_V0 | FOCUS_INDEX | 0.4 / 0.35 / 0.25 |
| POLICY_INTENSITY_V0 | INTENSITY_* / SUPPORT / COVERAGE | effect 三维 0.4/0.35/0.25；support 0.4/0.35/0.25 |
| POLICY_EFFECT_V0 | EFFECT / IMPLEMENTATION | 0.4/0.35/0.25；社会/环境无 ODS |
| POLICY_GAP_V0 | SHORTBOARD_COUNT | 阈值 45 |
| POLICY_OPPORTUNITY_V0 | OPPORTUNITY_COUNT | 阈值 60 |
| POLICY_LAYOUT_V0 | LAYOUT_REC_COUNT | 优先级 55 |
| POLICY_RELATION_V0 | RELATION / INDUSTRY_FIT | 余弦阈值 0.6 |

**冲突登记（须 QPOL-02 归一）**：

1. `settings_policy.yaml` 经验权重  
2. cfg_metric 种子「等权」叙述  
3. 产品演示力度：补贴 40% + 税收 25% + 数量 20% + 周期 15%

POC 实跑证据：`agent-handoffs/政策模块-E7/ALGO-POLICY-fullset.md`（polan 全链路）。

---

## §4 贴源分析（data-agent 协作）

| 层 | 结论 |
|----|------|
| ODS | `dwd_zck_policy` / `dwd_zck_intl_policy` 为政策主源（见映射报告 v2） |
| DWD | 目标 `dwd.policy_base_info`（37 字段，覆盖率约 85.2%） |
| ADS | `ads.policy_*` 系列；Java 只读 ADS |
| 缺口 | 执行监测 / 宏观 / 社会发展 → 效果与落地实效；专家策略库维表 |
| 国际 | QPOL-05：综合统计默认仅国内 |

详情缺口文案：`POLICY-data-gap-catalog.yaml`。

---

## §5 开放项回写（客户决策清单）

| ID | 本轮动作 | 状态保持 |
|----|----------|----------|
| QPOL-01 | 核对落地列指向本记录 + seed/gap | 🟡 |
| QPOL-02 | 登记三处权重冲突；待归一 | 🟡 |
| QPOL-03 | 匹配阈值 0.6 写入定义卡 | 🟡 |
| QPOL-05 | 国内/国际默认写入 scope_notes | 🟡 |
| QPOL-07 | 连续性暂并 TIMESERIES；缺独立 metric 记 GAP | 🟡 |

未关闭任何甲方项（合规：不替甲方拍板）。

---

## §6 UI / 评审挂载要求（给 V1）

- 凡统计数字：ⓘ MetricSpecCard（读 seed 8 件套）  
- Wave0：🧪 MockBadge  
- mapping ⚠️ 或 pending_ref：⚠️「待甲方确认」  
- PendingBadge 文案：优先读 `POLICY-data-gap-catalog.yaml#pending_hint`  
- 展示接待大屏：禁止敏感受众反馈明细下钻  

---

## §7 产物清单

| 产物 | 路径 |
|------|------|
| 本核对记录 | `产品整体定义/METRIC-OPEN-E7-DS10-12-核对记录.md` |
| 算法定义卡 | `metrics/metric-spec-POLICY.yaml` |
| gap catalog | `产品整体定义/POLICY-data-gap-catalog.yaml` |
| seed 核对更新 | `metrics/cfg_metric-POLICY-seed.yaml`（seed_version 0.2.0） |
| 决策表回写 | `客户决策清单跟踪表.md` §2.aa |
| handoff | `agent-handoffs/POLICY-METRIC-OPEN-L01.md` |

---

## §8 签署区（待真人）

| 角色 | 姓名 | 结论 | 日期 |
|------|------|------|------|
| 语义 Owner | 王惠 | _待签_ | |
| 方案 B 双签 | 唐绍祖 | _待签_ | |
