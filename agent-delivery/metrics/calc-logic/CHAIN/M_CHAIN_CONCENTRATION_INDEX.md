---
metric_id: M_CHAIN_CONCENTRATION_INDEX
metric_name_zh: 产业集中度
algorithm_type: COMPUTE
version: 0.2.0
updated: 2026-10-14
owner: data-agent / human:淮政玮
status: 三段式（临时出数 + 正式口径完整保留 + 切换条件）
---

# M_CHAIN_CONCENTRATION_INDEX 产业集中度 — 计算逻辑说明

> 2026-10-14 human:徐滕强 拍板三段式：「就想定一个出来，错一点无所谓，毕竟是临时的」+「**真实口径计算也要保留，临时不污染正式**」。结构同 `M_CHAIN_HOT_NEWS_COUNT` 先例。

## 1. 三段结构

| 段 | 内容 | 状态 |
|---|---|---|
| 临时口径 | HHI + 融资额份额（资本集中度代市场集中度） | **当前生效** |
| 正式口径 | 四决策点（HHI/CR_N、营收基准、粒度、形态）| **锁定待签，零预拍** |
| 切换条件 | QC02 签发 + 营收聚合落库 | 择期 |

## 2. 临时口径（当前生效）

**基准**：企业 `i` 在该链的**累计融资额（元）**份额。

**金额解析规则**（`funding_amount` 为中文带单位文本）：
- `亿人民币` 前缀数字 × 1e8；`万人民币` 前缀数字 × 1e4
- 非 CNY（USD 397 行）或空值（16,828 行 / 65.6%）**逐企业剔除**
- 剔除语义：剔"无金额记录的企业"非"无融资的企业"——占比公式里零融资企业本就不进分母，不构成幸存者偏差的一部分

**公式**：`HHI = Σ share_i² × 10000`（0-10000 点分；司法部分级叙事可借用：<100 分散 / 100-1500 未集中 / 1500-2500 中度 / >2500 高集中）

**桥接**：`enterprise_industry_chain`（复用 `M_CHAIN_INVEST_COUNT` v0.2.0 已定路径）；现 0 行 → NULL（无数据，数据事不挡口径）。

**语义偏移声明**（定义层如实标注）：临时=资本集中度代市场集中度。融资额集中 ≠ 市场份额集中（重资产链 vs 风投驱动链会系统性偏移）。UI 侧不体现临时标注（沿 HOT_NEWS 2026-10-14 拍板先例）。

```sql
WITH ent_amt AS (
  SELECT e.org_id,
         SUM(CASE
           WHEN f.funding_amount LIKE '%亿%' THEN CAST(REGEXP_SUBSTR(f.funding_amount,'^[0-9.]+') AS DECIMAL(20,2)) * 100000000
           WHEN f.funding_amount LIKE '%万%' THEN CAST(REGEXP_SUBSTR(f.funding_amount,'^[0-9.]+') AS DECIMAL(20,2)) * 10000
           ELSE NULL END) AS amt_cny
  FROM demo_gkxlumenx_dwd.enterprise_industry_chain e
  JOIN demo_gkxlumenx_ods.dwd_org_financing_info f
    ON f.org_id = e.org_id AND f.is_deleted = 0
  WHERE e.chain_code = :chain_code
  GROUP BY e.org_id
  HAVING amt_cny IS NOT NULL
)
SELECT ROUND(SUM(POWER(amt_cny / SUM(amt_cny) OVER (), 2)) * 10000, 1) AS temp_concentration_hhi
FROM ent_amt;
```

**实核数据基础**（2026-10-14）：`dwd_org_financing_info` 25,654 行；万 4,783 / 亿 4,043 / 空 16,828 / USD 397。

## 3. 正式口径（锁定待签，完整保留）

| 决策点 | 候选 | 状态 |
|---|---|---|
| 公式形态 | HHI（Σ份额²）vs CR_N（TopN 份额和；N=4/8） | QC02 + 唐绍祖 |
| 份额基准 | **营收份额**（目标）/ 专利 / 其他 | 营收聚合表未建（QC06 后置） |
| 统计粒度 | 环节级（每环节一个集中度）vs 全链级 | 未签（seed 旧稿"企业分布"与 calc 旧稿"环节级"分叉待并） |
| 输出形态 | 连续指数 vs 分级（中高/中低） | 未签 |

**两案参考**（决策卡素材，非预拍）：

- HHI：捕捉全部企业分散/集中，平方项天然稀释小企业份额噪声、对数据精度容忍度高；无 N 参数；阈值体系成熟（司法部 0.01/0.15/0.25 小数制 ≈ 100/1500/2500 点分制）。
- CR_N：直观（"前 4 家占 X%"）；但 N 是额外决策点，头部边界企业份额精度要求高。

**禁止项**：`dwd_org_industry_chain_dtl.chain_score` 是链企匹配置信分**不是市场份额**，正式与临时口径均禁止冒充（语义事故风险，证据卡已警告）。

**解挂双条件**：① QC02 签发（四决策点拍定）② 企业×链营收聚合表落库。解挂后弃临时、启用正式、ⓘ 卡口径说明同步切换。

## 4. 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `:chain_code` | 产业链编码（INB） | 必填 |

## 5. 版本与变更

| 版本 | 日期 | 变更 | 拍板 |
|---|---|---|---|
| 0.1.0 | — | 旧稿：pending_algorithm，源指向废弃壳 | — |
| 0.2.0 | 2026-10-14 | 三段式：临时 HHI+融资额份额；正式四决策点完整保留 | human:徐滕强 |

正式签名待 human:唐绍祖 会签。
