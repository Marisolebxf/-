> **铁律：本指标所有信息，均以第二章的“最新指标调研报告”为准。第一章指标信息为历史版本，不用作参考。**

# M_CHAIN_STAGE_HEALTH_SCORE 环节健康度分

> 状态：**draft**（pending QC04 / 公式待 human:唐绍祖 会签）
> 登记背景：2026-10-16「产业瓶颈堵点识别」真表接线新增，防 ADS 支撑 ID 悬空（D9）。


> **维护者**：唐绍祖
> **适用系统**：科技专题服务算法库（单系统件）
> **版本说明**：本件不在 20261027 批调研源内（1021/1027 均无同名调研正本），维持既有骨架版；如后续纳入调研批次再行升级。
## 元数据

| 项 | 值 |
|----|----|
| 指标 ID | `M_CHAIN_STAGE_HEALTH_SCORE` |
| 中文名 | 环节健康度分 |
| 模块 | CHAIN（产业链） |
| 验收单元 | CHAIN-DIAG-BOTTLENECK（瓶颈堵点识别） |
| 频率 | weekly |
| 类型（algorithm_type） | STAT（未签，待会签） |
| 对齐状态 | D1 = draft，挂 QC04 |
| 是否在数据库 | 是（ADS `industry_chain_metric_fact` 环节×五维行 + `industry_chain_metric_series` 时序行） |
| 关联 Q 编号 | QC04（瓶颈判定维度/阈值） |

## 口径定义

指定产业链各环节（rd 研发 / design 设计 / manufacturing 制造 / sales 销售 / service 服务）的健康度综合分，取值 0–100。

**健康分 = 四核心维算术平均**：技术、人才、资本、政策四维环节分齐备才计分，缺任一维 → NULL（不做部分均值）。市场需求维只参与「最弱维」标注，不进均值。

健康分驱动下游判定（阈值未冻结，挂 QC04）：

- 档位：≥75 稳健 / ≥60 关注 / <60 薄弱
- 瓶颈 = 薄弱 ∧ 时序趋势下行；卡脖子 = 瓶颈 ∧ 健康分 < 50

## 计算逻辑说明

与算法实现严格一致（lumen-algo-py）：

- 读数：`key_link._load_stage_health_raws`（ADS fact 表环节×五维分数）
- 均值：`bottleneck.mean_health`（CORE_DIMS = tech/talent/capital/policy，值 ≤1 视为 0–1 比例 ×100 归一）
- 趋势：`key_link._load_stage_timeseries`（series 表最近两年环比符号 up/down/flat）

## 源表字段

| 表 | 用途 | 关键字段 |
|----|------|----------|
| `demo_gkxlumenx_ads.industry_chain_metric_fact` | 环节×五维分数行（支撑 ID 五个，不单列注册） | chain_id / object_type='chain' / node_id(=stage_key) / metric_id / metric_value |
| `demo_gkxlumenx_ads.industry_chain_metric_series` | 环节维年度时序（趋势输入） | 同上 + stat_period |
| `demo_gkxlumenx_dwd.industry_chain_model_result_detail` | 模型原子分上游 | run_id / dimension_code / … |

支撑 metric_id（M_CHAIN_STAGE_*，仅作本条源字段）：

- `M_CHAIN_STAGE_TECH_SCORE` 技术维
- `M_CHAIN_STAGE_TALENT_SCORE` 人才维
- `M_CHAIN_STAGE_MARKET_SCORE` 市场需求维（不进均值）
- `M_CHAIN_STAGE_CAPITAL_SCORE` 资本维
- `M_CHAIN_STAGE_POLICY_SCORE` 政策维

## 参考公式（读表版，待会签）

```sql
SELECT f.node_id AS stage_key,
       CASE WHEN COUNT(*) = 4 THEN ROUND(AVG(f.metric_value), 1) END AS health_score
FROM demo_gkxlumenx_ads.industry_chain_metric_fact f
WHERE f.chain_id = :chain_code AND f.object_type = 'chain' AND IFNULL(f.is_deleted,0)=0
  AND f.metric_id IN ('M_CHAIN_STAGE_TECH_SCORE','M_CHAIN_STAGE_TALENT_SCORE',
                      'M_CHAIN_STAGE_CAPITAL_SCORE','M_CHAIN_STAGE_POLICY_SCORE')
GROUP BY f.node_id;  -- 四核心维齐备才计分，缺任一维 → NULL
```

## 备注

- 现数据为演示批 `mock_20261016_bottleneck_seed`（seed_chain_bottleneck_demo.py 灌入，43 链 × 5 环节 × 5 维 fact 1075 行 + series 1075 行），支持 `--rollback` 一键还原；正式生产数据待模型侧 ETL 接管（QC04 冻结后）。
- 档位阈值 / 维度权重 / 五维写入字典未冻结，一律挂 QC04；禁止在 FE/算法侧写死绕过。
- 同点位展示：环节图节点健康分 + 档位标签；带 ⓘ 时 8 件套消费本条。
