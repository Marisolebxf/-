# M_CHAIN_REG_REVENUE 营收（链维 / 区域维 / 年维）计算口径细稿

- **版本**：v0.2.0（2026-10-14，路径A：口径前置写实；正式签名待 human:唐绍祖 会签）
- **口径拍板**：human:徐滕强 2026-10-14（固定统计年；缺失如实 0）
- **类型**：STAT（求和）
- **is_mock**：true（链桥数据未灌；灌数后转 live）

## 1. 原始定义档案

- **页面语境**：专题系统 · 产业链分析 · 区域产业评价页（`CHAIN-TOPIC-REGIONAL.yaml` `row_id: TOPIC-REG-010`），主项"营收"，子项"商业力叶子"；页面定义"区域内相关企业营收规模"；页面约束"**不把门户 MARKET_SIZE 算进本页 KPI**"；A1 需规 `ALGO-CHAIN-DEEP-126`；上游合成 `M_CHAIN_ENTERPRISE_POWER`（企业能力）。
- **白话**：深圳这条链上的企业，某一年加起来挣了多少钱——商业体量。
- **兄弟条目先例**：`M_CHAIN_COMPETITIVENESS_INDEX` v1"规模=年报营收合计"（本条为其营收面的独立成条版）。

## 2. 指标定义（v0.2.0）

**指定统计年度、指定区域内、指定产业链链上企业的营业收入合计。**

- **固定统计年**（拍板 ①）：`:stat_year` 必填（如 2024）；营收规模必须同年可比，**禁止**跨多年混加、**不做**"各 org 最新年"回退；
- 求和：`SUM(operating_revenue)`，单位元（库原值），展示层转亿；
- **缺失处理**（拍板 ②）：`operating_revenue IS NULL` 的行不进 SUM（SUM 语义天然忽略），链上企业全缺 → 输出 0；**不推算、不放大、不搞覆盖率注记**——缺失是数据态，不进口径判定；
- 企业集：链桥 `enterprise_industry_chain`（`chain_code` 定链，org_id 维）∩ 主档 `city = :region_city`；
- 键位全 org_id（2026-10-14 已定：企业侧关联禁名称匹配）。

## 3. Formula（SQL）

```sql
SELECT SUM(f.operating_revenue) AS revenue_sum
FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
JOIN demo_gkxlumenx_ods.dwd_org_base_info b
  ON b.org_id = e.org_id AND b.is_deleted = 0 AND b.city = :region_city
JOIN demo_gkxlumenx_ods.dwd_org_annual_financial_info f
  ON f.org_id = e.org_id AND f.is_deleted = 0
 AND f.year = :stat_year
 AND f.operating_revenue IS NOT NULL
WHERE e.chain_code = :chain_code;
```

## 4. 表依赖与实核（2026-10-14 demo）

| 表 | 角色 | 实核 |
|---|---|---|
| `dwd_org_annual_financial_info` | 分子（operating_revenue） | 90,926 行 / 8,127 org / 19 年（2007–2025）；**同 org 同年 0 重复组**——SUM 无重复累加风险；营收非空 2,193 行（2.4%），2024 年 47 行 |
| `dwd_org_base_info` | 主档（city 区域轴） | 189,116 行，org_id 全唯一 |
| `dwd.enterprise_industry_chain` | 链桥 | 1 行测试数据（INB1309）= 数据未灌 |

老稿表名漂移回执：`chain_enterprise`(120) / `chain_enterprise_stat`(209) 为老 mock ADS 表，弃。

## 5. 缺口分型

| 项 | 分型 | 处置 |
|---|---|---|
| 链桥未灌 | 数据未灌（DWD 在案表） | 不报缺；灌数后即真数 |
| 营收填充率 2.4% | 数据态（供应侧覆盖薄） | 不进口径；全缺为 0；F13 的 live 5,352 行旧观测已被 demo 90,926 行覆盖 |

## 6. 验证记录（2026-10-14）

- 唯一性：`GROUP BY org_id, year HAVING c>1` → **0 组**。
- 端到端（不带链过滤，桥未灌）：**深圳 × 2024 = 14 家 / 2,897,422.84 万元 ≈ 289.74 亿元**——管道真实可出数。
