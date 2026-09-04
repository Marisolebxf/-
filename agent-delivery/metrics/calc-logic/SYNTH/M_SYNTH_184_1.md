# 区域产业创新人才综合评价模型（M_SYNTH_184_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_184_1 |
| 指标名称 | 区域产业创新人才综合评价模型 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新活力分析 |
| 三级模块 | 产业创新人才 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

选定区域内、统计年度的人才创新成果指数，从创新人才数量、学历结构、年龄结构、成果产出四维评定，取值 0—100。分数越高表示人才结构与产出越强。对象=区域创新人才，不是单名学者、不是企业技术人才维。

## 计算逻辑说明

采用加权平均。四维：创新人才数量 / 学历结构 / 年龄结构 / 成果产出。算法库序号 184 已给这四维，不另起维度。各维极值归一后等权（也可按评估重点改权，ΣW=1）。

### 第一步：入集

统计窗默认自然年。区域落到 `dwd_org_base_info.city` / `province` / `area`。学者机构 `dwd_scholar.scholar_org_name_zh` / `scholar_org_id` 对齐 `name_cn` / `org_id`。研发人员取 `dwd_org_annual_financial_info.development_employee`，年键=`year`。

### 第二步：四个子项

1. **创新人才数量**  
   区域学者去重数 + 区域内企业研发人员合计。两子值分别极值归一后等权。

2. **学历结构**  
   最高学历含硕/博（`dwd_scholar_education_background.degree_zh` / `degree_en` 含硕士、博士、Master、Ph.D、PhD）的学者 / 区域学者去重数。一名学者多条学历取最高一条。

3. **年龄结构**  
   现库无出生年。正式口径用最早任职年推从业年限代理年龄：统计年 − `dwd_scholar_work_experience.start_time` 最早年。青年占比 = 从业年限 < 10 年的学者 / 有任职记录的学者。这是年龄代理，不是真实出生年；不另待建 `birth_year`。

4. **成果产出**  
   四子项极值归一后等权：论文与H指数、对齐授权专利、专利转移、院士学者数。  
   - 论文与H指数：区域学者 `paper_nums` + `h_index` 合计。  
   - 对齐授权专利：区域内机构对齐授权专利去重数，年键=`pbdt_year`。  
   - 专利转移：区域内机构对齐专利的权利转移去重数，年键=`dwd_patent_transfer.transfer_effective_date`。是机构级转移代理技术转化，不是人才转化台账。  
   - 院士学者数：`dwd_scholar_talent_flag.academician=1` 的区域学者去重数。仅覆盖院士荣誉，不含科技奖明细。

四维等权得指数。输出区域一行，含四维得分与综合分。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 区域产业创新人才综合评价模型 | 创新人才数量 | 学者存量 | 区域学者去重数。 | COUNT(DISTINCT scholar_id) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者存量,所属机构；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 研发人员合计 | 企业研发人员求和。 | SUM(development_employee) | dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域产业创新人才综合评价模型 | 学历结构 | 硕博学者占比 | 最高学历含硕博的学者占比。 | COUNT(硕博)/COUNT(学者) | dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者存量,所属机构；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域产业创新人才综合评价模型 | 年龄结构 | 青年学者占比 | 从业年限<10年学者占比。任职年正式代理年龄。 | COUNT(青年)/COUNT(有任职记录) | dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构流动；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者存量,所属机构；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域产业创新人才综合评价模型 | 成果产出 | 论文与H指数 | 学者paper_nums与h_index合计。 | SUM(paper_nums)+SUM(h_index) | dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 学者存量,论文量,H指数；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 对齐授权专利 | 机构对齐授权专利去重数。 | COUNT(DISTINCT 授权专利) | dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 专利转移 | 机构对齐专利权利转移去重数，代理技术转化。 | COUNT(DISTINCT pn) WHERE 转移年=统计年 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,技术转化代理；dwd_patent(pn, first_applicant_name) — 申请人对齐；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 院士学者数 | 区域院士学者去重数，代理获奖/荣誉。 | COUNT(DISTINCT scholar_id) WHERE academician=1 | dwd_scholar_talent_flag(scholar_id, academician) — 院士标识；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者存量,所属机构；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续
- dwd_org_annual_financial_info(org_id, year, development_employee, employees_number) — 研发人员,从业人数
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id, paper_nums, h_index) — 学者存量,所属机构,论文量,H指数
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历
- dwd_scholar_work_experience(scholar_id, start_time, end_time, org_name_zh) — 任职起止,机构
- dwd_scholar_talent_flag(scholar_id, academician) — 院士标识,获奖代理
- dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 机构对齐授权专利
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,技术转化代理

## 待建字段

- 无
