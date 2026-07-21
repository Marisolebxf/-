# ENT-MOD-RISK-METRIC-OPEN-L01 —— 风险洞察指标语义与 ODS/DWD 数据缺口核对

> **任务**：ENT-MOD-RISK-METRIC-OPEN-L01
> **执行人**：algorithm-agent（human:唐绍祖）+ data-agent
> **日期**：2026-07-22
> **状态**：✅ 完工

---

## 1. 产出物清单

| 文件 | 路径 | 说明 |
|------|------|------|
| METRIC-OPEN-ENT-RISK-核对记录.md | agent-handoffs/产品整体定义/ | #4/#5适用性、8 metric 口径、指标×贴源矩阵、PDR自检 |
| ENT-RISK-data-gap-catalog.yaml | agent-handoffs/产品整体定义/E-28_E-29-风险洞察/ | UI 缺口文案真源, ≥3条 ≥80字 pending_hint |
| cfg_metric-ENT-seed.yaml | metrics/ | 风险8指标 8 件套已更新 |

## 2. 核心产出

- 8 个风险 metric 全部完成 definition/formula/算法边界/DEMO 临时阈值定义
- 关键架构约束明确:前端不计算官方风险等级/中心度/严重度
- Q017/Q018 登记为 🟡 不伪闭合

## 3. 架构合规自检

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 算法边界与前端约束明确 | ✅ |
| 2 | 不替甲方闭合 Q017/Q018 正式阈值 | ✅ |
| 3 | 不修改 demo/Java/Python 实现 | ✅ |
| 4 | 不新增 Neo4j 或前端直连图库 | ✅ |
| 5 | cost 四字段已填写 | ✅ |

## 4. Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 120_000 |
| actual_tokens | 90_000 |
| model_used | claude-sonnet-4.5 |
| actual_cost | 0.54 |
| cost_warn | green |
