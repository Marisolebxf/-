# 子指标贡献度（M_INNOV_GBA_SUBINDEX_CONTRIB）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_SUBINDEX_CONTRIB |
| 指标名称 | 子指标贡献度 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新能力 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

解释选定湾区城市总指数的结构：创新资源、创新机构、创新机制、创新环境各占多少。取值 0—1，四维合计为 1。本指标不另造 0—100 分。

## 计算逻辑说明

四子指数与总指数一律复用，不重算底层件数：

| 维 | 对应指标 | 取值 |
| --- | --- | --- |
| 创新资源 | M_INNOV_GBA_RES_INDEX | `res_index` |
| 创新机构 | M_INNOV_GBA_ORG_INDEX | `org_index` |
| 创新机制 | M_INNOV_GBA_MECH_INDEX | `mech_index` |
| 创新环境 | M_INNOV_GBA_ENV_INDEX | `env_index` |

总指数口径同 `M_INNOV_GBA_CAPACITY_INDEX`：四维等权。缺测维不补 0，剩余维权重重归一，贡献度分母只含有效维。

### 第一步：取数

同一年窗、同一 11 城跑四个子指标，按城对齐。页面传入城市（默认深圳）；`city=湾区` 时用 11 城各子指数的算术平均再算贡献。

### 第二步：贡献度

$$
贡献度_i=\frac{s_i}{\sum_j s_j},\quad s\in\{res\_index,org\_index,mech\_index,env\_index\}
$$

分母为 0 则四维贡献度皆空。等权时贡献度就是该维指数占四维合计的比例，不必再乘 1/4。

输出：一行一城，含四维贡献度（0—1）及合计校验（应为 1）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 子指标贡献度 | 创新资源贡献 | 资源指数占总指数结构的比例。 | res_index / 四维合计 | 取 M_INNOV_GBA_RES_INDEX — 资源指数 | 无 |
| 子指标贡献度 | 创新机构贡献 | 机构指数占总指数结构的比例。 | org_index / 四维合计 | 取 M_INNOV_GBA_ORG_INDEX — 机构指数 | 无 |
| 子指标贡献度 | 创新机制贡献 | 机制指数占总指数结构的比例。 | mech_index / 四维合计 | 取 M_INNOV_GBA_MECH_INDEX — 机制指数 | 无 |
| 子指标贡献度 | 创新环境贡献 | 环境指数占总指数结构的比例。 | env_index / 四维合计 | 取 M_INNOV_GBA_ENV_INDEX — 环境指数 | 无 |

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
- dwd_org_tech_tag(org_id, org_tag) — 高新技术标签
- dwd_policy_base(id, city, province, status, expire_date, publish_year, rank, theme) — 政策供给,主题,有效

## 待建字段

- 无

## 参考资料

[1]创新资源/机构指数｜科技部｜创新型国家评价指标体系｜2017年https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/P020131204326192340968.pdf.

[2]创新资源/机构指数｜科技部｜—｜国家高新技术产业开发区综合评价指标体系｜2021年｜https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/gfxwj/gfxwj2021/202104/t20210429_174232.html

[3] 创新机制指数｜山西省科学技术厅｜省校合作科研机构建设运行与绩效评价管理办法｜2025-01-24｜https://www.shanxi.gov.cn/zcwjk/bmgfxwj/202501/t20250124_9758132.shtml.

[4]创新机制指数｜中国科学院成都文献情报中心，中国科学院大学｜中国科学院知识产权管理支撑专项项目（E4C00005）；中国科学院文献情报能力建设专项项目（E3201106）｜雷聪仪，张娴，等.基于三阶段DEA模型的科研机构专利技术转移效率评价研究[J]. 科技成果管理与研究, 2025, 20(1): 15-23.

[5] 创新环境指数｜上海交通大学安泰经济与管理学院｜国家社会科学基金项目（23BJY108）｜石桂峰，李蕙均，李娜. 地方政府创新政策强度与企业创新[J]. 会计与经济研究, 2024, 38(6): 3-32. DOI: 10.16314/j.cnki.31-2074/f.2024.06.002.

[6]创新环境指数｜湖北宏泰集团，中南财经政法大学统计与数学学院，杭州银行股份有限公司｜黄骏飞，张博文，熊霖霏. 中国科技创新政策的演化与量化评价[J]. 统计与决策, 2023(14): 168-173.
