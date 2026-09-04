# 要素贡献度与影响路径（M_SYNTH_ELEM_CONTRIB）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_CONTRIB |
| 指标名称 | 要素贡献度与影响路径 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新要素分析 |
| 三级模块 | 要素影响关联分析 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-E-02 |

## 口径定义

选定区域内、统计年度，量化企业、科研机构、高层次人才、科研资金四类创新要素对产业发展与创新成果的贡献份额，并给出要素→产业 / 要素→成果的影响路径。取值各为 0—1（份额，同行和为 1）。对象=要素对产出的关联份额，不是因果归因，不是子指标对活力总指数的贡献（≠ `M_SYNTH_186_1` 权重）。

## 计算逻辑说明

采用份额分解。二维：贡献度 / 影响路径。需求序号 138 已写「贡献度与影响路径」；要素集合按序号 136 取企业、科研机构、高层次人才、科研资金，不扩到 187 的七类。本指标不作回归因果、不跑 Granger。地区生产总值不进本指标。

### 第一步：入集

区域与存续同 `M_SYNTH_187_1`。四类要素主体：

- 企业：存续且 `org_type` 为企业（或非科研机构表内的经营主体）。
- 科研机构：`dwd_research_institute_base_info`。
- 高层次人才：区域学者；产出先记到其对齐机构。
- 科研资金：有研发投入或融资记录的区域机构。资金不单独占产出件。

产业发展靶点 = 高企去重数与营收合计（两子值先各自算区域总量，再按主体对齐份额）。创新成果靶点 = 授权专利去重数与论文去重数。

主体产出对齐：专利 `first_applicant_name`、论文作者单位对齐 `name_cn`。一篇成果只计第一申请人或第一机构，避免重复。

### 第二步：两个子项

1. **贡献度**  
   四类要素对「产业发展」与「创新成果」的份额。  
   - 企业：企业对齐成果除以区域成果；产业侧高企记入企业，营收按企业加总。  
   - 科研机构：机构对齐成果除以区域成果。  
   - 人才：同一件成果优先记机构，不再记人才。人才行只统计「第一机构对齐不上、但作者单位仍落在区域学者」的残余。残余为 0 时，改用学者数除以企业、机构、学者三类主体数之和，作结构代理，结果标「结构代理」。不另待建人才—成果直接对齐键。  
   - 资金：有研发投入机构的营收除以区域营收、有研发投入机构的成果除以区域成果。这是资金要素的正式代理，不是资金台账直读。不另待建资金直接贡献额。  
   同一靶点下四类份额重新归一，使和为 1。输出 4×2 份额表。

2. **影响路径**  
   有向边：要素类型 → 产业发展、要素类型 → 创新成果。边权等于该格贡献份额。按边权从高到低取前 6 条。路径只表示关联强度，不表述「导致」。

输出区域一张份额表 + 一条路径清单。页面演示态若只展示规模占比，须标非因果。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 要素贡献度与影响路径 | 贡献度 | 企业贡献份额 | 企业对产业与成果的对齐份额。 | 企业对齐产出除以区域产出 | dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续；dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗；dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
|  |  | 科研机构贡献份额 | 科研机构对成果的份额。 | 机构对齐产出除以区域成果 | dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗；dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 人才贡献份额 | 机构去重后的人才残余份额；残余为 0 时用学者数结构代理。 | 人才残余产出除以区域成果；残余为 0 则用学者数除以三类主体数 | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者存量,所属机构；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗；dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 资金贡献份额 | 有研发投入机构对产业与成果的份额，正式代理资金要素。 | 有研发投入机构的营收或成果除以区域对应总量 | dwd_org_annual_financial_info(org_id, year, operating_revenue, development_employee, `arch development am`) — 营收,研发人员,研发投入；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发；dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资额,融资时点；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续；dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗 | 无 |
| 要素贡献度与影响路径 | 影响路径 | Top6影响路径 | 按边权从高到低取前 6 条路径。 | 边权等于贡献份额，取前 6 条 | 同贡献度四行源表 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 企业与区域入集,名称对齐
- dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 高层次人才,所属机构
- dwd_org_annual_financial_info(org_id, year, operating_revenue, `arch development am`) — 营收,研发投入
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发
- dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资（资金主体入集）
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业（产业发展靶点）
- dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 创新成果专利
- dwd_zh_paper(id, cover_year_start) — 中文论文
- dwd_en_paper(id, cover_year_start) — 英文论文
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

- 无
