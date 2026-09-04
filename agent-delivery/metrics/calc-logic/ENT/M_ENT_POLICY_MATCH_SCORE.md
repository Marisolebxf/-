# 政策匹配度（M_ENT_POLICY_MATCH_SCORE）

> 指标最终唯一解释口径（真源）。由 AI 补漏调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。
>
> **公式由 AI 创作，待算法 Lead 会签。**

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_POLICY_MATCH_SCORE |
| 指标名称 | 政策匹配度 |
| 一级模块 | 企业分析 |
| 二级模块 | 引育推荐 |
| 三级模块 | - |
| 更新频率 | 政策更新后 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q009 / Q015 |

## 口径定义

企业与政策导向的匹配程度评分，跨政策域（产业方向/支持对象/支持方式）综合度量，取值 0—100，招引与培育推荐共用。对象=企业，反映企业与政策扶持方向的契合水平。权重与口径待 Q015 正式闭合（pending_data_lead）。

## 计算逻辑说明

跨政策域三维加权：产业方向匹配 / 支持对象匹配 / 支持方式匹配。

### 第一步：入集

政策取有效 `status`（未失效）；企业标签取 `dwd_org_tech_tag.org_tag` 与 `enterprise_base` 高企/小巨人/独角兽等；产业取 `dwd_org_industry_tags.industry_code` 或 `industry_l1/l2/l3`。

### 第二步：三个子项

1. **产业方向匹配**：企业产业/关键词与政策 `theme` / `keywords` / `policy_support` 的语义匹配度（关键词/主题命中率）。
2. **支持对象匹配**：企业标签（高企/小巨人/独角兽/小微等）命中政策 `policy_support` 支持对象列表的覆盖度。
3. **支持方式匹配**：政策 `type`（财税/人才/金融/产业等）对企业可享受支持方式的覆盖广度。

综合：$MatchScore = \sum_d W_d \times Norm(子项_d)$，0—100。现库已有 `policy_match.match_score` 结果表可复用（口径待核对）。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 政策匹配度 | 产业方向匹配 | 企业产业 vs 政策主题匹配 | 企业产业与政策主题/关键词匹配度。 | 主题/关键词命中率 | dwd_policy_base(id, title, type, theme, keywords, policy_support, city, province, rank, status) — 政策主题/关键词/扶持目标；dwd_org_industry_tags(credit_code, industry_code, industry_name) — 企业产业 | 跨政策域统一匹配口径 |
|  |  | 企业地域 vs 政策地域匹配 | 企业所在地与政策适用地域匹配。 | 地域命中 | dwd_policy_base(id, city, province, status) — 政策适用地域；dwd_org_base_info(org_id, city, province) — 企业地域 | 无 |
| 政策匹配度 | 支持对象匹配 | 企业标签 vs 政策支持对象匹配 | 企业科技标签命中政策支持对象。 | 支持对象覆盖度 | dwd_org_tech_tag(org_id, org_tag) — 企业科技标签；dwd_policy_base(id, policy_support) — 政策支持对象列表 | 支持对象标准化标签表 |
| 政策匹配度 | 支持方式匹配 | 财税/人才/金融政策覆盖匹配 | 政策类型对企业可享支持方式的覆盖。 | 类型覆盖度 | dwd_policy_base(id, type) — 政策类型 | 无 |
|  |  | 政策匹配得分 | 现库政策匹配结果分。 | policy_match.match_score | policy_match(subject_type, subject_id, policy_id, match_score, match_reasons, rank_no) — 政策匹配结果（ADS） | 无 |

## 源表字段

- dwd_policy_base(id, title, type, theme, keywords, policy_support, city, province, rank, status) — 政策主题/类型/扶持目标/地域/级别/状态
- dwd_org_tech_tag(org_id, org_tag) — 企业科技标签（高企/小巨人等）
- dwd_org_base_info(org_id, city, province, industry, industry_l1_code, industry_l2_code) — 企业地域+产业
- dwd_org_industry_tags(credit_code, industry_code, industry_name) — 企业产业链归类
- policy_match(subject_type, subject_id, policy_id, match_score, match_reasons, rank_no) — 政策匹配结果（ADS）

## 待建字段

- 跨政策域统一匹配口径与权重：Q015 pending，多域（产业/对象/方式）匹配规则与权重待确认后落配置。
- 支持对象标准化标签表：政策 `policy_support` 与企业 `org_tag` 的标签体系需统一映射。

## 参考资料

[1] 招引企业综合推荐模型 | 算法库 §1.1.1.1.1.1.1.5.7 | 需求ID ALGO-ENT-DEEP-147 | 政策匹配度维度 | 关联 Q009 / Q015。

[2] 培育企业综合推荐模型 | 算法库 §1.1.1.1.1.1.1.5.8 | 政策匹配度维度（招引与培育共用）。

[3] 高潜力企业智能挖掘 | 需规 SRS《企业分析.md》序号49 | 招引企业推荐分析。
