# 多城市对标排名（M_ENT_CITY_RANK）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → data-agent 正式化入仓。
> 本指标含 4 行子指标（L1+L2+L3），已合并为单文件。
> 维护：data-agent · 对齐状态见 `cfg_metric-ENT-seed.yaml`。

## L1 指标元数据

- **指标ID**：`M_ENT_CITY_RANK`
- **指标名称（一级）**：多城市对标排名
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：多城市对标排名
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **是否在数据库（L1）**：部分
- **关联Q编号**：Q014

## L1 口径定义

在预设对标城市集合中，以选定未来产业范围为筛选条件，从企业规模（平均营业收入）、企业密度（每百平方公里企业数）、产业链完整度三个维度计算各城市综合得分并排名。依照需求文档提供的构建方法。

## L1 计算逻辑说明

```
三维极值归一化加权汇总：企业规模(40%) + 企业密度(30%) + 产业链完整度(30%)。
```

**计算公式文件**：`M_ENT_CITY_RANK.md`

## L1 源表字段

```
gkx.dwd_org_industry_tags(credit_code, company_name, industry_name) — 未来产业筛选（按 industry_name 正则归类）、企业城市提取（company_name 前缀）、去重企业数（三维度共用前置筛选）
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, development_employee, employees_number, `arch development am`, year) — 平均技术力与平均商业力的底层输入（优先年报，覆盖非上市企业）
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 平均技术力的底层输入（研发成果产出，专利预聚合）
gkx.dwd_org_tech_tag(org_id, org_tag) — 平均技术力的底层输入（企业资质标签，辅助五维计算）
```

## L1 备注

1.1.1.2.4.2.3.5.2；依照需求文档提供的构建方法

## 子指标详情（L2 / L3）

### L2：平均技术力

#### L2 详情：平均技术力

- **口径定义**：多城市对标排名中平均技术力维度的得分。
- **计算逻辑**：`各城市该未来产业范围内企业的技术力得分均值。依赖ads_ent_tech_score结果表。`
- **源表字段**：`gkx.dwd_org_industry_tags(credit_code, company_name, industry_name) — 未来产业筛选（按 industry_name 正则归类）、企业城市提取（company_name 前缀）、去重企业数（三维度共用前置筛选）
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, development_employee, employees_number, `arch development am`, year) — 平均技术力与平均商业力的底层输入（优先年报，覆盖非上市企业）
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 平均技术力的底层输入（研发成果产出，专利预聚合）
gkx.dwd_org_tech_tag(org_id, org_tag) — 平均技术力的底层输入（企业资质标签，辅助五维计算）`
- **待建表字段**：`目标结果表 ads_ent_tech_score(tech_score, org_id, 待建) — 企业技术力得分（算法侧五维加权产出，平均技术力维度直接取用）
目标结果表 ads_ent_business_score(business_score, org_id, 待建) — 企业商业力得分（算法侧六维加权产出，平均商业力维度直接取用）
城市辖区面积(百km2) — 外部数据源（现库 dim_admin_area 无面积字段，待补）`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.5.2；依照需求文档提供的构建方法；依赖技术力得分结果表

### L2：商业力

#### L2 详情：商业力

- **口径定义**：多城市对标排名中商业力维度的得分。
- **计算逻辑**：`各城市该未来产业范围内企业的商业力得分均值。依赖ads_ent_business_score结果表。`
- **源表字段**：`gkx.dwd_org_industry_tags(credit_code, company_name, industry_name) — 未来产业筛选（按 industry_name 正则归类）、企业城市提取（company_name 前缀）、去重企业数（三维度共用前置筛选）
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, development_employee, employees_number, `arch development am`, year) — 平均技术力与平均商业力的底层输入（优先年报，覆盖非上市企业）
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 平均技术力的底层输入（研发成果产出，专利预聚合）
gkx.dwd_org_tech_tag(org_id, org_tag) — 平均技术力的底层输入（企业资质标签，辅助五维计算）`
- **待建表字段**：`目标结果表 ads_ent_tech_score(tech_score, org_id, 待建) — 企业技术力得分（算法侧五维加权产出，平均技术力维度直接取用）
目标结果表 ads_ent_business_score(business_score, org_id, 待建) — 企业商业力得分（算法侧六维加权产出，平均商业力维度直接取用）
城市辖区面积(百km2) — 外部数据源（现库 dim_admin_area 无面积字段，待补）`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q014
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.5.2；依照需求文档提供的构建方法；依赖商业力得分结果表

### L2：企业密度

#### L2 详情：企业密度

- **口径定义**：多城市对标排名中企业密度维度的得分。
- **计算逻辑**：`各城市该未来产业范围内去重企业数 / 城市辖区面积(百km2)。`
- **源表字段**：`gkx.dwd_org_industry_tags(credit_code, company_name, industry_name) — 未来产业筛选（按 industry_name 正则归类）、企业城市提取（company_name 前缀）、去重企业数（三维度共用前置筛选）
gkx.dwd_org_annual_financial_info(org_id, operating_revenue, development_employee, employees_number, `arch development am`, year) — 平均技术力与平均商业力的底层输入（优先年报，覆盖非上市企业）
gkx.dwd_org_rd_achiev_info(org_id, inv_pat_auth_num, util_pat_auth_num, des_pat_auth_num) — 平均技术力的底层输入（研发成果产出，专利预聚合）
gkx.dwd_org_tech_tag(org_id, org_tag) — 平均技术力的底层输入（企业资质标签，辅助五维计算）`
- **待建表字段**：`目标结果表 ads_ent_tech_score(tech_score, org_id, 待建) — 企业技术力得分（算法侧五维加权产出，平均技术力维度直接取用）
目标结果表 ads_ent_business_score(business_score, org_id, 待建) — 企业商业力得分（算法侧六维加权产出，平均商业力维度直接取用）
城市辖区面积(百km2) — 外部数据源（现库 dim_admin_area 无面积字段，待补）`
- **更新频率**：年度/模型版本发布时
- **对齐状态**：未对齐
- **关联Q编号**：Q016
- **是否在数据库**：部分
- **备注**：1.1.1.2.4.2.3.5.2；依照需求文档提供的构建方法；城市辖区面积需外部数据

---
*生成自王惠 20260816 Excel 底稿（4 行），data-agent 正式化 2026-08-18*
