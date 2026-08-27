# 商业力得分（M_ENT_BUSINESS_POWER_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-ENT-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_BUSINESS_POWER_SCORE |
| 指标名称 | 商业力得分 |
| 一级模块 | 企业分析 |
| 二级模块 | 企业评估 |
| 三级模块 | 商业力评估 |
| 更新频率 | 年度/模型版本发布时 |
| 对齐状态判定 | 未对齐 |
| 是否在数据库 | 部分 |
| 关联Q编号 | Q014 |


## 口径定义

企业商业力评估的综合得分，满分0—100分，综合反映企业在市场、产品、品牌、技术合作、产业链覆盖及关键环节参与等方面的综合表现。

## 计算逻辑说明

| 一级维度           | 三级指标               | 指标说明                                               | 源表字段                    |
| :----------------- | :--------------------- | :----------------------------------------------------- | --------------------------- |
| **市场**           | 营业收入               | 企业年度营业收入总额                                   | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 企业年度营业收入 |
|                    | 市场占有率             | 企业营收 ÷ 行业总营收 × 100%                           | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 企业营收<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业归属，需行业营收汇总 |
|                    | 盈利能力               | 销售净利润 ÷ 营业收入 × 100%                           | gkx.dwd_org_annual_financial_info(org_id, pure_profit, operating_revenue, year) — 盈利能力=净利润÷营业收入×100% |
| **产品**           | 产品线覆盖广度         | 企业覆盖的产业链产品数                                 | gkx.dwd_org_industry_chain_dtl(credit_code, node_name) — 企业覆盖的产业链节点数<br>gkx.dwd_org_org_product_info(org_id, main_prod) — 企业主营产品（辅助） |
|                    | 新产品收入占比         | 新产品销售收入 ÷ 主营业务收入 × 100%                   | gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 主营业务收入（分母）<br>gkx 现库无新产品销售收入字段（待建）— 新产品销售收入 |
|                    | 产品质量水平           | 产品合格率等质量指标                                   | gkx 现库无产品质量字段（待建）— 产品合格率等质量指标 |
| **品牌**           | 品牌声量               | 自身产品品牌资讯内容量 ÷ 行业总资讯内容量              | gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 企业品牌资讯内容量 |
|                    | 行业声誉               | 企业品牌获得的国家级/省级/市级行业类荣誉排名加权得分。 | gkx.dwd_org_tech_tag(org_id, org_tag) — 资质/荣誉标签（如中国驰名商标、省著名商标），按级别加权计分 |
| **技术合作**       | 产学研合作项目数量     | 企业与高校/科研院所合作专利数                          | gkx.dwd_patent(patent_id,applicants)— 联合专利多申请人解析   |
|                    | 外部专家参与研发人月数 | 来企业从事研发工作的外部专家工作量                     | gkx 现库无外部专家人月数字段（待建）— 外部专家工作量数据 |
| **产业链覆盖率**   | 产业链环节覆盖率       | 企业覆盖产业链环节数 / 目标产业链环节总数 × 100%       | gkx.dwd_org_industry_chain_dtl(credit_code, node_name) — 企业覆盖的产业链环节数<br>gkx.dwd_industry_chain_info(industry_code, chain_name, downstream_link_code) — 产业链标准环节总数 |
| **关键环节参与度** | 关键环节参与度         | 企业覆盖关键环节数 / 全链关键环节数 × 100%             | gkx.dwd_org_industry_chain_dtl(credit_code, node_name, chain_score) — 企业覆盖的关键环节数<br>gkx.dwd_industry_chain_info(industry_code, chain_name, node_stage) — 关键环节识别（参考 M_ENT_KEY_NODE_COUNT） |

## 源表字段

gkx.dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 市场维度（营业收入、市场占有率、盈利能力），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 市场占有率维度的行业归属与行业营收汇总
gkx.dwd_org_industry_chain_dtl(credit_code, node_name, chain_score) — 产品维度（产品线覆盖广度）、产业链覆盖率维度（覆盖环节数）、关键环节参与度维度（关键环节覆盖）
gkx.dwd_industry_chain_info(industry_code, chain_name, downstream_link_code, node_stage) — 产业链覆盖率维度（标准环节总数）、关键环节参与度维度（关键环节识别）
gkx.dwd_org_org_product_info(org_id, main_prod) — 产品维度（企业主营产品，辅助产品线覆盖广度评估）
gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 品牌维度（品牌声量，企业品牌资讯内容量）
gkx.dwd_org_tech_tag(org_id, org_tag) — 品牌维度（行业声誉，资质/荣誉标签按级别加权计分）-待定
gkx.dwd_patent(patent_id,applicants) — 技术合作维度（联合专利解析产学研合作）
新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建

dwd_org_tech_tag是否有品牌荣誉资质，待定

注：商业力得分由市场、产品、品牌、技术合作、产业链覆盖率、关键环节参与度六个维度加权汇总，各指标经极值归一化后按权重加权计算，权重待甲方确认（Q014）。行业声誉：国家级5分；省级3分；地市级2分，计高分不重复计分。结果表 ads_ent_business_score(business_score, org_id, 待建)。

## 待建字段

新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定
