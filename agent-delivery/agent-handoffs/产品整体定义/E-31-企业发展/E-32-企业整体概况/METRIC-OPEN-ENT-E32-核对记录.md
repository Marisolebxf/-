# METRIC-OPEN-ENT-E32-核对记录
# ENT-MOD-OVERVIEW-E32-METRIC-OPEN-L01 — 企业整体概况（E-32）指标语义与 ODS/DWD 缺口核对

> **任务**：ENT-MOD-OVERVIEW-E32-METRIC-OPEN-L01
> **角色**：algorithm-agent（human:唐绍祖）+ data-agent
> **监管人**：human:王惠（口径主责）/ human:唐绍祖（公式与算法适用性）
> **日期**：2026-08-03
> **上游**：PM-PDR-E32-企业整体概况-评审纪要 + TRACE-E31-企业发展.yaml（E-32 叶子）

---

## §1 适用性结论（Track-MS #4/#5）

| 五件套项 | 状态 | 说明 |
|----------|------|------|
| #4 指标语义卡（MetricSpecCard） | 🟡 部分闭合 | E-32 三个 KPI 已补 8 件套；Q-E32-01 未闭合 |
| #5 开放项（PendingBadge + Popover） | 🟡 部分闭合 | Q-E32-01/Q-E32-02 已登记 gap catalog；2026-08-25 并入 `ENT-SYNTH-METRIC-COVER-P01`（客户决策清单 §2.ag-e32），不另开叶 |
| PDR-05 自检 | 🟡 待会签 | UI 指标已盘点；正式 metric_id 与口径待王惠/何老师确认 |
| PDR-06 自检 | 🟡 待会签 | 新指标已补 seed；贴源字段级核对未完成 |
| 唐绍祖公式/算法适用性 | 🟡 待签署 | 公式依赖 Q-E32-01，未闭合前不得标 done |

## §2 E-32 指标口径摘要（algorithm-agent）

### 2.1 顶部三 KPI（库内全量/全球快照，不随下方选择器联动）

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_TOTAL_COUNT | 企业总数 | 库内全量企业去重总数，全球视角当前快照 | COUNT(DISTINCT enterprise_id) | dwd.enterprise <- dwd_org_reg_info, dwd_company_base | ✅ 已注册 |
| M_ENT_RESEARCHER_COUNT | 企业科研人数 | 企业内科研人员数，当前快照；加工逻辑、正式 metric_id、ADS 来源与更新频率待 Q-E32-01 | pending_algorithm | 无直接贴源 | ❌ 无直接源 |
| M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT | 覆盖未来产业数 | 按当前数据实际覆盖的未来产业去重数；正式 metric_id 与动态口径待 Q-E32-01 | pending_algorithm | future_industry_code（APP 字典，E-32/E-34/E-35 同源） | ⚠️ 待确认 |

### 2.2 企业分布卡片

| metric_id | 中文名 | 定义 | 公式 | 源表 | 状态 |
|-----------|--------|------|------|------|------|
| M_ENT_REGIONAL_COUNT | 区域企业数量 | 全球/全国/区域/深圳四级地域聚合数量；层级边界、聚合口径与默认深圳语义待 Q-E32-02 | COUNT(DISTINCT enterprise_id) GROUP BY 地域层级 | dwd.enterprise.headquarters_city/district <- ods: dwd_org_reg_info, dwd_company_location_tags | ⚠️ Q-E32-02 |

> 口径边界：demo 展示的 12 个未来产业只是固定样例，不等同正式未来产业全集；`employees_number` 是从业人数，不是研发人数；研发投入金额不能当人数。

## §3 指标 × 贴源矩阵（data-agent）

| metric_id | mapping_status | ODS | DWD | ADS | pending_ref | pending_hint |
|-----------|---------------|-----|-----|-----|-------------|-------------|
| M_ENT_TOTAL_COUNT | ✅ | dwd_org_reg_info,dwd_company_base | dwd.enterprise | — | — | 数据可用；库内全量快照 |
| M_ENT_RESEARCHER_COUNT | ❌ | 无研发人数字段 | — | — | Q-E32-01 | 三方贴源无直接研发人数字段；employees_number 是从业人数；research_development_amount 是金额非人数 |
| M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT | ⚠️ | future_industry_code（APP 字典） | ODS/DWD 字段级核对未完成 | — | Q-E32-01 | 正式 metric_id 与动态口径待确认；demo 12 产业为样例 |
| M_ENT_REGIONAL_COUNT | ⚠️ | dwd_org_reg_info,dwd_company_location_tags | dwd.enterprise | — | Q-E32-02 | 四级地域边界与聚合口径待确认；当前 demo 为固定样例 |

## §4 开放项闭合表

| 编号 | metric_id | 当前状态 | 依据 | 待闭合动作 |
|------|-----------|---------|------|-----------|
| Q-E32-01 | M_ENT_RESEARCHER_COUNT / M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT | 🟡 团队临时默认 + 无直接源 | PDR 纪要 | 何老师/北明确认加工逻辑、正式 metric_id、ADS 来源与更新频率；郭万迎登记客户决策清单 |
| Q-E32-02 | M_ENT_REGIONAL_COUNT | 🟡 团队临时默认 | PDR 纪要 | 确认四级地域数据来源、层级边界与聚合口径；郭万迎协调 |

## §5 PDR-05/06 自检清单

| 检查项 | 结果 | 备注 |
|--------|------|------|
| PDR-05: UI → metric_id 盘点 | ✅ | E-32 页面引用 4 个 metric_id（3 KPI + 1 分布）已全部盘点 |
| PDR-05: wireframe 覆盖度 | ✅ | 顶部 KPI、产业排名/趋势、企业分布均有对应 |
| PDR-06: metric ↔ definition 一致性 | ✅ | 新指标已补 cfg_metric-ENT-seed 8 件套 |
| PDR-06: source_tables 完整度 | ❌ | 科研人数无直接三方贴源；未来产业字段级核对未完成 |
| PDR-06: pending_hint ≥80 字 | ✅ | E-32 gap catalog 3 条均达标 |
| PDR-07: 开放项登记 | 🟡 | 待郭万迎登记客户决策清单 |

## §6 语义会签

| 角色 | 签署人 | 日期 | 结果 |
|------|--------|------|------|
| 口径 Owner | human:王惠 | 待确认 | 待签署 |
| 算法适用性 | human:唐绍祖 | 待确认 | 待签署（Q-E32-01 公式未闭合） |
| 执行人/认领 | human:唐绍祖 | 2026-08-03 | 已认领并完成 Agent 侧产物 |
