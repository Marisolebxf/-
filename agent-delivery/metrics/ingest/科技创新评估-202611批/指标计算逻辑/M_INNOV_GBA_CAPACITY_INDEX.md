# 粤港澳大湾区创新能力指标（M_INNOV_GBA_CAPACITY_INDEX）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_CAPACITY_INDEX |
| 指标名称 | 粤港澳大湾区创新能力指标 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

湾区各城创新能力总指数。统计对象为粤港澳大湾区 11 城，由创新资源、创新机构、创新机制、创新环境四子指数等权合成，取值 0—100。分数越高，创新能力越强。湾区合计取 11 城算术平均。

## 计算逻辑说明

四维分别复用：

| 二级 | 对应指标 | 取值 |
| --- | --- | --- |
| 创新资源指数 | M_INNOV_GBA_RES_INDEX | `res_index`（0—100） |
| 创新机构指数 | M_INNOV_GBA_ORG_INDEX | `org_index`（0—100） |
| 创新机制指数 | M_INNOV_GBA_MECH_INDEX | `mech_index`（0—100） |
| 创新环境指数 | M_INNOV_GBA_ENV_INDEX | `env_index`（0—100） |

入集、子项与合成一律跟对应子指标。本指标不另造得分。

### 第一步：取四子指数

按同一年窗、同一 11 城清单分别跑四个子指标，按城对齐。

### 第二步：合成

四子指数已在 11 城内归一到 0—100，本指标不再做第二次极值归一，直接等权：

$$
创新能力=\frac{res\_index+org\_index+mech\_index+env\_index}{4}
$$

缺测子指数不补 0，剩余维权重重归一。湾区总指数 = 11 城创新能力算术平均。

输出：一行一城，含四子指数与 `capacity_index`（0—100）；另输出一行 `city=湾区`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 粤港澳大湾区创新能力指标 | 创新资源指数 | 专利、论文与研发投入。 | 取 M_INNOV_GBA_RES_INDEX | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员 | 无 |
| 粤港澳大湾区创新能力指标 | 创新机构指数 | 载体数量、产出与科技型机构。 | 取 M_INNOV_GBA_ORG_INDEX | dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 湾区机构；dwd_research_institute_base_info(org_id, city, province, reg_status) — 科研院所；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_patent(pn, first_applicant_name, apdt_year) — 专利产出；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 粤港澳大湾区创新能力指标 | 创新机制指数 | 联合专利、合作项目与转化。 | 取 M_INNOV_GBA_MECH_INDEX | dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 共申请人；dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目；dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移 | 无 |
| 粤港澳大湾区创新能力指标 | 创新环境指数 | 政策供给、主题覆盖与高企密度。 | 取 M_INNOV_GBA_ENV_INDEX | dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_base_info(org_id, city, province, reg_status) — 高企分母 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 湾区机构入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, applicants, first_applicant_name, apdt_year) — 专利去重,共申请人,申请人对齐,申请年
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 合作项目
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_org_annual_financial_info(org_id, year, development_employee) — 年报研发人员
- dwd_org_tech_tag(org_id, org_tag) — 高新技术等科技型标签
- dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

- 无

## 参考资料

[1] 粤港澳大湾区创新能力指标｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf.

[2]粤港澳大湾区创新能力指标｜广东科学技术职业学院｜广州市哲学社会科学发展“十四五”规划2025年度共建课题（2025GZGJ147）；2023年度广东省教育科学规划课题（2023GXJK739）｜周璐瑶，李佳蔚.粤港澳大湾区科技创新能力研究[J]. 合作经济与科技, 2026(04):3-7.

[3]港澳大湾区创新能力指标｜中共中央 国务院｜粤港澳大湾区发展规划纲要｜2019-02-18｜https://www.gov.cn/gongbao/content/2019/content_5370836.htm.

[4]粤港澳大湾区创新能力指标｜中山大学粤港澳发展研究院｜国家社会科学基金项目（19BJY011）｜李小瑛，陈嘉玲. 粤港澳大湾区建设科技创新中心的现状及对策[J]. 长安大学学报(社会科学版), 2023, 25(5): 92-101.
