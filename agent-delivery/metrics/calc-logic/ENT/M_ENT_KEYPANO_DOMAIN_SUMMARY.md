# 领域摘要（M_ENT_KEYPANO_DOMAIN_SUMMARY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_KEYPANO_DOMAIN_SUMMARY |
| 指标名称 | 领域摘要 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业发展 |
| 三级模块 | 重点企业全景图 |
| 更新频率 | 论文/专利数据更新后 |
| 对齐状态判定 | 部分对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q013 |


## 口径定义

从目标产业链当前链位（上游/中游/下游）的重点企业论文、专利中抽取关键词，将关键词映射到产业链细分领域，计算映射覆盖率并生成证据摘要。映射覆盖率 = 已映射关键词数 / 该链位关键词总数 * 100%。覆盖率>=60%判定为"证据充分"，否则为"证据不足"。

## 计算逻辑说明

1.链位归集：dwd_org_industry_tags关联dwd_industry_chain_info按level（上游/中游/下游）分组企业；2.关键词抽取：从该链位重点企业论文标题/摘要、专利名称/摘要中抽取技术关键词；3.领域映射：关键词与产业链细分领域匹配，统计命中率；4.覆盖率=命中关键词数/该链位关键词总数*100%；5.汇总论文关键词、专利关键词及关联重点企业形成证据摘要。

## 源表字段

gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联（链位归集）
gkx.dwd_industry_chain_info(industry_code, industry_link_code, level) — 产业链节点层级（上/中/下游分组）
gkx.dwd_org_base_info(org_id, name_cn, external_id) — 企业基础信息（关联重点企业名称）
gkx.dwd_patent_base(patent_id, org_id, patent_name, abstract) — 企业专利关键词抽取来源
gkx.dwd_paper_base(paper_id, org_id, title, abstract) — 企业论文关键词抽取来源

## 待建字段

ads.enterprise_keypano_domain_evidence(industry_code, link_level, domain_name, paper_keywords, patent_keywords, coverage_rate, evidence_status, enterprise_ids) — 领域证据摘要预聚合视图（未建）；关键词→领域→环节→链位映射规则表（未建）
