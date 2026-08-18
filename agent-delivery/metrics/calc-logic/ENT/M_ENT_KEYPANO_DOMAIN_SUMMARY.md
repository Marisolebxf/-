# 重点企业全景图（M_ENT_KEYPANO_DOMAIN_SUMMARY）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_KEYPANO_DOMAIN_SUMMARY`
- **指标名称**：重点企业全景图
- **一级模块**：企业分析
- **二级模块**：企业发展
- **三级模块**：重点企业全景图
- **更新频率**：论文/专利数据更新后
- **对齐状态**：部分对齐
- **是否在数据库**：部分
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q013

## 口径定义

从目标产业链当前链位（上游/中游/下游）的重点企业论文、专利中抽取关键词，将关键词映射到产业链细分领域，计算映射覆盖率并生成证据摘要。映射覆盖率 = 已映射关键词数 / 该链位关键词总数 * 100%。覆盖率>=60%判定为"证据充分"，否则为"证据不足"。

## 计算逻辑说明

```
1.链位归集：dwd_org_industry_tags关联dwd_industry_chain_info按level（上游/中游/下游）分组企业；2.关键词抽取：从该链位重点企业论文标题/摘要、专利名称/摘要中抽取技术关键词；3.领域映射：关键词与产业链细分领域匹配，统计命中率；4.覆盖率=命中关键词数/该链位关键词总数*100%；5.汇总论文关键词、专利关键词及关联重点企业形成证据摘要。
```

**计算公式文件**：`M_ENT_KEYPANO_DOMAIN_SUMMARY.md`

## 源表字段

```
gkx.dwd_org_industry_tags(credit_code, industry_code, industry_link_code) — 企业与产业链节点关联（链位归集）
gkx.dwd_industry_chain_info(industry_code, industry_link_code, level) — 产业链节点层级（上/中/下游分组）
gkx.dwd_org_base_info(org_id, name_cn, external_id) — 企业基础信息（关联重点企业名称）
gkx.dwd_patent_base(patent_id, org_id, patent_name, abstract) — 企业专利关键词抽取来源
gkx.dwd_paper_base(paper_id, org_id, title, abstract) — 企业论文关键词抽取来源
```

## 待建表字段

```
ads.enterprise_keypano_domain_evidence(industry_code, link_level, domain_name, paper_keywords, patent_keywords, coverage_rate, evidence_status, enterprise_ids) — 领域证据摘要预聚合视图（未建）；关键词→领域→环节→链位映射规则表（未建）
```

---
*生成自王惠 20260816 Excel 底稿，data-agent 正式化 2026-08-18*
