# 商业力得分（M_ENT_BUSINESS_POWER_SCORE）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 本指标含 13 行子指标（L1+L2+L3），已合并为单文件。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## L1 指标元数据

- **指标ID**：`M_ENT_BUSINESS_POWER_SCORE`
- **指标名称（一级）**：商业力得分
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：商业力评估
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **是否在数据库（L1）**：部分
- **关联Q编号**：Q014

## L1 口径定义

企业商业力评估的综合得分，满分0-100分，综合反映企业在市场、产品、品牌、技术合作、产业链覆盖率、产业关键环节参与度六个维度的综合水平。

## L1 计算逻辑说明

```
采用主成分分析法。六维：市场/产品/品牌/技术合作/产业链覆盖率/关键环节参与度。
```

**计算公式文件**：`M_ENT_BUSINESS_POWER_SCORE.md`

## L1 源表字段

```
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 市场维度（营业收入、市场占有率、盈利能力），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 市场占有率维度的行业归属与行业营收汇总
gkx.dwd_org_industry_chain_dtl(credit_code, node_name, chain_score) — 产品维度（产品线覆盖广度）、产业链覆盖率维度（覆盖环节数）、关键环节参与度维度（关键环节覆盖）
gkx.dwd_industry_chain_info(industry_code, chain_name, downstream_link_code, node_stage) — 产业链覆盖率维度（标准环节总数）、关键环节参与度维度（关键环节识别）
gkx.dwd_org_org_product_info(org_id, main_prod) — 产品维度（企业主营产品，辅助产品线覆盖广度评估）
gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 品牌维度（品牌声量，企业品牌资讯内容量）
gkx.dwd_org_tech_tag(org_id, org_tag) — 品牌维度（行业声誉，资质/荣誉标签按级别加权计分）
gkx.dwd_org_industry_chain_pat_dtl(credit_code, current_assignee) — 技术合作维度（联合专利解析产学研合作）
```

## L1 备注

1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

## 子指标详情（L2 / L3）

### L2：市场

#### L3：营业收入

- **口径定义**：从营收规模、市场占有率、盈利能力维度评估企业在目标市场中的竞争地位与市场份额。
- **计算逻辑**：`营业收入（最新年度 operating_revenue）`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 企业年度营业收入`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

#### L3：市场占有率

- **口径定义**：从营收规模、市场占有率、盈利能力维度评估企业在目标市场中的竞争地位与市场份额。
- **计算逻辑**：`企业营收 / 行业总营收 × 100%`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 企业营收<br>gkx.dwd_org_base_info(org_id, industry_l1_code) — 行业归属，需行业营收汇总`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

#### L3：盈利能力

- **口径定义**：从营收规模、市场占有率、盈利能力维度评估企业在目标市场中的竞争地位与市场份额。
- **计算逻辑**：`销售净利润 / 营业收入 × 100%`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, pure_profit, operating_revenue, year) — 盈利能力=净利润÷营业收入×100%`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

### L2：产品

#### L3：产品线覆盖广度

- **口径定义**：从产品线覆盖广度、新产品营收贡献、产品质量水平等维度评估企业产品竞争力
- **计算逻辑**：`企业产业链产品数去重`
- **源表字段**：`gkx.dwd_org_industry_chain_dtl(credit_code, node_name) — 企业覆盖的产业链节点数<br>gkx.dwd_org_org_product_info(org_id, main_prod) — 企业主营产品（辅助）`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

#### L3：新产品收入占比

- **口径定义**：从产品线覆盖广度、新产品营收贡献、产品质量水平等维度评估企业产品竞争力
- **计算逻辑**：`新产品销售收入 / 主营业务收入 × 100%`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, year) — 主营业务收入（分母）<br>gkx 现库无新产品销售收入字段（待建）— 新产品销售收入`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：否
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

#### L3：产品质量

- **口径定义**：从产品线覆盖广度、新产品营收贡献、产品质量水平等维度评估企业产品竞争力
- **计算逻辑**：`产品合格率`
- **源表字段**：`gkx 现库无产品质量字段（待建）— 产品合格率等质量指标`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：否
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

### L2：品牌

#### L3：品牌声量

- **口径定义**：从品牌声量、行业声誉等维度评估企业品牌影响力与市场认知度。
- **计算逻辑**：`企业资讯条数 / 行业总资讯条数 × 100%`
- **源表字段**：`gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 企业品牌资讯内容量`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法；品牌声量数据待建

#### L3：行业声誉

- **口径定义**：从品牌声量、行业声誉等维度评估企业品牌影响力与市场认知度。
- **计算逻辑**：`荣誉级别加权（国家级5/省级3/市级2，取最高不重复）`
- **源表字段**：`gkx.dwd_org_tech_tag(org_id, org_tag) — 资质/荣誉标签（如中国驰名商标、省著名商标），按级别加权计分`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法；品牌声量数据待建

### L2：技术合作

#### L3：产学研合作项目数量

- **口径定义**：从产学研合作活跃度、外部专家参与深度等维度评估企业技术合作与开放创新能力
- **计算逻辑**：`COUNT(DISTINCT patent_id) WHERE 申请人类型含企业且含高校/科研机构`
- **源表字段**：`gkx.dwd_org_industry_chain_pat_dtl(credit_code, current_assignee) — 联合专利多申请人解析`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

#### L3：外部专家参与研发的人数

- **口径定义**：从产学研合作活跃度、外部专家参与深度等维度评估企业技术合作与开放创新能力
- **计算逻辑**：`外部专家人数，单位：人月`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 市场维度（营业收入、市场占有率、盈利能力），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 市场占有率维度的行业归属与行业营收汇总
gkx.dwd_org_industry_chain_dtl(credit_code, node_name, chain_score) — 产品维度（产品线覆盖广度）、产业链覆盖率维度（覆盖环节数）、关键环节参与度维度（关键环节覆盖）
gkx.dwd_industry_chain_info(industry_code, chain_name, downstream_link_code, node_stage) — 产业链覆盖率维度（标准环节总数）、关键环节参与度维度（关键环节识别）
gkx.dwd_org_org_product_info(org_id, main_prod) — 产品维度（企业主营产品，辅助产品线覆盖广度评估）
gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 品牌维度（品牌声量，企业品牌资讯内容量）
gkx.dwd_org_tech_tag(org_id, org_tag) — 品牌维度（行业声誉，资质/荣誉标签按级别加权计分）
gkx.dwd_org_industry_chain_pat_dtl(credit_code, current_assignee) — 技术合作维度（联合专利解析产学研合作）`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

### L2：产业链覆盖率

#### L2 详情：产业链覆盖率

- **口径定义**：企业覆盖产业链环节数占目标产业链环节总数比例
- **计算逻辑**：`企业覆盖环节数 / 全链环节总数 × 100%（COUNT(DISTINCT industry_link_code) WHERE credit_code=企业 / COUNT(DISTINCT industry_link_code) WHERE industry_code=产业链）`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 市场维度（营业收入、市场占有率、盈利能力），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 市场占有率维度的行业归属与行业营收汇总
gkx.dwd_org_industry_chain_dtl(credit_code, node_name, chain_score) — 产品维度（产品线覆盖广度）、产业链覆盖率维度（覆盖环节数）、关键环节参与度维度（关键环节覆盖）
gkx.dwd_industry_chain_info(industry_code, chain_name, downstream_link_code, node_stage) — 产业链覆盖率维度（标准环节总数）、关键环节参与度维度（关键环节识别）
gkx.dwd_org_org_product_info(org_id, main_prod) — 产品维度（企业主营产品，辅助产品线覆盖广度评估）
gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 品牌维度（品牌声量，企业品牌资讯内容量）
gkx.dwd_org_tech_tag(org_id, org_tag) — 品牌维度（行业声誉，资质/荣誉标签按级别加权计分）
gkx.dwd_org_industry_chain_pat_dtl(credit_code, current_assignee) — 技术合作维度（联合专利解析产学研合作）`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

### L2：产业关键环节参与度

#### L2 详情：产业关键环节参与度

- **口径定义**：企业覆盖关键环节数占全链关键环节总数比例
- **计算逻辑**：`企业覆盖关键环节数 / 全链关键环节数 × 100%（WHERE is_key_node=1）`
- **源表字段**：`gkx.dwd_org_annual_financial_info(org_id, operating_revenue, pure_profit, year) — 市场维度（营业收入、市场占有率、盈利能力），优先年报，覆盖非上市企业
gkx.dwd_org_base_info(org_id, industry_l1_code) — 市场占有率维度的行业归属与行业营收汇总
gkx.dwd_org_industry_chain_dtl(credit_code, node_name, chain_score) — 产品维度（产品线覆盖广度）、产业链覆盖率维度（覆盖环节数）、关键环节参与度维度（关键环节覆盖）
gkx.dwd_industry_chain_info(industry_code, chain_name, downstream_link_code, node_stage) — 产业链覆盖率维度（标准环节总数）、关键环节参与度维度（关键环节识别）
gkx.dwd_org_org_product_info(org_id, main_prod) — 产品维度（企业主营产品，辅助产品线覆盖广度评估）
gkx.dwd_org_important_news_info(org_id, name_cn, news_content, news_date) — 品牌维度（品牌声量，企业品牌资讯内容量）
gkx.dwd_org_tech_tag(org_id, org_tag) — 品牌维度（行业声誉，资质/荣誉标签按级别加权计分）
gkx.dwd_org_industry_chain_pat_dtl(credit_code, current_assignee) — 技术合作维度（联合专利解析产学研合作）`
- **待建表字段**：`新产品销售收入字段 — 现库无此字段，待建
产品质量字段 — 现库无此字段，待建
外部专家参与研发人月数字段 — 现库无此字段，待建
dwd_org_tech_tag是否有品牌荣誉资质，待定`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.4 + 算法库5.6；依照需求文档提供的构建方法

---
*生成自王惠 20260816 Excel 底稿（13 行），data-agent 正式化 2026-08-18*
