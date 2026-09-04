# 政策匹配推送（M_POLICY_MATCH）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-POLICY-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_MATCH |
| 指标名称 | 政策匹配推送 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 政策分析 |
| 三级模块 | - |
| 更新频率 | 日 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | QPOL-03 |

## 口径定义

按主体（企业/用户）画像，对「当前有效且未过期」的政策计算产业、地区、诉求、有效性四维加权匹配分，按匹配分降序取 Top-N 推送。对象=有效政策，主体=企业或用户，输出=主体—政策的匹配分与推送清单。政策有效性以 `status` 为有效且 `expire_date` 未过期（或为空）且 `is_deleted=0` 为准。

## 计算逻辑说明

采用四维加权综合匹配：产业匹配度 / 地区匹配度 / 诉求匹配度 / 政策有效性。各维先归一化为 0—100，再按权重加权求和（权重待 QPOL-03 确认，ΣW=1）。匹配规则按「企业规模、行业类型、发展阶段」等登记信息对齐政策扶持对象。

### 第一步：入集

- 政策入集：`dwd_policy_base.status='有效'` 且（`expire_date` 为空 或 `expire_date >= 当前日期`）且 `is_deleted=0`。
- 主体入集：企业主体取 `dwd_org_base_info.reg_status` 含「存续」；外资主体可对齐 `dwd_forg_base_info`；用户主体暂以登记画像为准（待建）。

### 第二步：四维打分

1. **产业匹配度**：主体产业标签与政策主题/支持产业的重合度。主体产业取 `dwd_org_base_info.industry_l1_name/l2_name` 与 `dwd_org_industry_tags.industry_name`；政策产业取 `dwd_policy_base.theme`、`keypoints`、`policy_support` 中命中的产业词。重合词数 ÷ 政策产业词数（或取 Jaccard 相似度）归一。

2. **地区匹配度**：主体所在地区与政策行政辖区的重合度。主体地区取 `dwd_org_base_info.province/city/area`；政策辖区取 `dwd_policy_base.province/city/district`。省级同记 1，市级同记 0.8，区级同记 0.6，不同记 0，取最高命中档。

3. **诉求匹配度**：主体诉求标签与政策扶持对象/支持方式的命中度。政策侧取 `dwd_policy_base.policy_support`（支持对象、支持行为、支持方式、申报条件）与 `policy_entity.entity_name`（扶持对象实体）；主体诉求标签当前库缺失，暂以 `dwd_org_tech_tag.org_tag`、`enterprise_tag.tag_name` 作代理，真实诉求字段待建。

4. **政策有效性**：有效政策记 100，失效/过期记 0。

### 第三步：加权综合匹配分

$$
match\_score = W_1 \cdot S_{产业} + W_2 \cdot S_{地区} + W_3 \cdot S_{诉求} + W_4 \cdot S_{有效}, \quad \sum W_i = 1
$$

权重 `W` 由匹配规则参数（QPOL-03）确定，默认等权（各 0.25）。

### 第四步：Top-N 取数与写表

按主体对 `match_score` 降序取 Top-N（N 默认 10），写入 `ads.policy_match(subject_type, subject_id, subject_name, policy_id, policy_title, match_score, match_reasons, rank_no, model_version, calc_batch_id)`。

```sql
-- 匹配分示意（产业/地区/有效性可直接算，诉求用代理标签）
WITH effective_policy AS (
  SELECT id, title, type, theme, province, city, district, policy_support, keywords
  FROM gkx.dwd_policy_base
  WHERE is_deleted = 0
    AND status = '有效'
    AND (expire_date IS NULL OR expire_date >= CURDATE())
),
subject AS (
  SELECT b.org_id, b.name_cn, b.external_id, b.industry_l1_name, b.province, b.city, b.area,
         GROUP_CONCAT(DISTINCT t.industry_name) AS ind_tags,
         GROUP_CONCAT(DISTINCT g.org_tag) AS tech_tags
  FROM gkx.dwd_org_base_info b
  LEFT JOIN gkx.dwd_org_industry_tags t ON b.external_id = t.credit_code
  LEFT JOIN gkx.dwd_org_tech_tag g ON b.org_id = g.org_id
  WHERE b.reg_status LIKE '%存续%'
  GROUP BY b.org_id, b.name_cn, b.external_id, b.industry_l1_name, b.province, b.city, b.area
)
SELECT s.org_id AS subject_id, 'enterprise' AS subject_type, p.id AS policy_id, p.title,
       (0.25 * s_industry + 0.25 * s_region + 0.25 * s_demand + 0.25 * s_valid) AS match_score
FROM subject s CROSS JOIN effective_policy p;
```

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策匹配推送 | 产业匹配度 | 主体产业与政策产业重合度 | 主体产业标签与政策主题/支持产业的命中程度。 | S_产业 = 重合产业词数 ÷ 政策产业词数 × 100 | dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_name, industry_l2_name) — 企业主体,行业类型；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 企业产业标签；dwd_policy_base(id, theme, keypoints, policy_support) — 政策主题/关键点/支持对象 | 无 |
|  | 地区匹配度 | 主体地区与政策辖区重合度 | 主体所在省市与政策行政辖区的命中档位。 | 省级同=1/市级同=0.8/区级同=0.6/不同=0，取最高档 × 100 | dwd_org_base_info(org_id, province, city, area) — 主体地区；dwd_policy_base(id, province, city, district) — 政策辖区 | 无 |
|  | 诉求匹配度 | 主体诉求与政策扶持方式命中度 | 主体诉求标签与政策扶持对象/支持方式的命中程度。 | S_诉求 = 命中诉求/支持方式词数 ÷ 政策支持词数 × 100 | dwd_org_tech_tag(org_id, org_tag) — 企业科技/资质标签(代理)；enterprise_tag(org_id, tag_code, tag_name, tag_category, tag_score) — 企业通用标签(代理)；dwd_policy_base(id, policy_support, keywords) — 政策扶持对象/支持方式/申报条件；policy_entity(policy_id, entity_type, entity_name, attributes) — 政策扶持对象实体 | 主体诉求标签字段（融资/技术攻关/人才等诉求）；用户(非企业)画像表 |
|  | 政策有效性 | 政策当前有效状态 | 政策是否处于有效且未过期状态。 | S_有效 = status='有效'且未过期 ? 100 : 0 | dwd_policy_base(id, status, expire_date, publish_date, is_deleted) — 政策状态/失效日/逻辑删除 | 无 |

## 源表字段

- dwd_policy_base(id, title, type, theme, province, city, district, status, expire_date, publish_date, policy_support, keywords, keypoints, is_deleted) — 政策对象/主题/辖区/支持对象/有效性
- dwd_org_base_info(org_id, name_cn, external_id, industry, industry_l1_name, industry_l2_name, province, city, area, org_size, org_type, incorporation_year, listing_status, reg_status) — 企业主体画像(产业/地区/规模/发展阶段)
- dwd_org_industry_tags(credit_code, industry_code, industry_name, industry_link_code, industry_link_name) — 企业产业链标签
- dwd_org_tech_tag(org_id, org_tag) — 企业科技/资质标签
- enterprise_tag(org_id, tag_code, tag_name, tag_category, tag_score) — 企业通用标签
- tag_dict(tag_code, tag_name, tag_category) — 标签字典
- policy_entity(policy_id, entity_type, entity_name, attributes, confidence, calc_batch_id) — 政策扶持对象实体

## 待建字段

- 主体「诉求」维度字段：企业诉求标签（融资需求 / 技术攻关需求 / 人才需求等），现库无真实诉求字段，仅以 `dwd_org_tech_tag`、`enterprise_tag` 作代理。
- 用户（非企业）主体画像表。
- 匹配规则权重参数表（QPOL-03）：四维权重 `W1—W4` 与 Top-N 阈值 N。

## 参考资料

[1] 政策匹配与推送｜科技信息展示系统和科技专题服务系统.md｜1.1.1.1.4.2.1.3.6 政策匹配与推送（根据企业或用户登记信息，如企业规模、行业类型、发展阶段，自动匹配适合的政策内容并推送）。

[2] 政策匹配与推送｜科创政策全景.md｜序号 212（智能服务集群/科技信息展示系统/科技政策跟踪/科创政策全景/政策舆情评估/政策匹配与推送）。

[3] 应用场景数据需求分析.md｜科技信息展示系统数据需求｜提供重点领域分析、动态可视化、效果跟踪、受众反馈、智能匹配推送（FR-PO）。

[4] 政策匹配度｜科技专题服务算法库.md｜企业/人才/服务机构招引培育推荐模型均以「政策匹配度」为核心维度之一（1.1.1.1.1.1.1.5.7 / 5.8 / 7.9 / 9.9 / 9.10）。
