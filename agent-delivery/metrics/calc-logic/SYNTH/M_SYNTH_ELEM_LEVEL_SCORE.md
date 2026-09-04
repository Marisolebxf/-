# 七大结构层次评价（M_SYNTH_ELEM_LEVEL_SCORE）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_LEVEL_SCORE |
| 指标名称 | 七大结构层次评价 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新要素分析 |
| 三级模块 | 要素评价模型构建 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | Q-SYNTH-E-01 |

## 口径定义

选定区域内、统计年度，对七大结构（人才/企业/政策/服务机构/科研机构/资金/空间）分别给出成熟度、均衡度、达标。页面「层次·结构」Tab 展示 7 行，未达标橙/红。

本指标不是层次指数。层次指数见 `M_SYNTH_ELEM_LEVEL_INDEX`。本指标使用 `M_SYNTH_ELEM_TYPE_INDEX` 已算好的各结构叶子标准化得分，输出结构层评价（成熟度、均衡度、达标），不再加权成总指数。

## 计算逻辑说明

叶子口径、源表一律同 `M_SYNTH_ELEM_TYPE_INDEX`（高学历用学者学历表；服务机构用 svc_org_card 规则 A 六类；园区用机构名称弱代理）。缺叶子不进分母，不填 0。成熟度与均衡度公式与层次指数相同。

记结构 \(k\) 下有值叶子标准化得分为 \(s_{k1},\ldots,s_{kn}\)，\(n\) 为该结构本区域有值叶子数，\(s_{kj}\in[0,100]\)。本批入集区域集合记为 \(R\)，与类型指数做极值归一化的区域集合相同。二级下可能只有一个三级，\(n=1\) 时该结构仍应有均衡度得分。

第一步：成熟度

$$
成熟度_k = \sum_{j=1}^{n} w_{kj}\, s_{kj},\qquad \sum_{j=1}^{n} w_{kj}=1
$$

默认等权 \(w_{kj}=1/n\)。\(n=0\) 时该结构成熟度空缺，不填 0。

第二步：均衡度（熵）

叶子得分占该结构合计的份额：

$$
p_{kj}=\frac{s_{kj}}{\sum_{i=1}^{n}s_{ki}}
$$

$$
H_k=-\sum_{j=1}^{n} p_{kj}\ln p_{kj}
$$

约定 \(p_{kj}=0\) 时 \(p\ln p=0\)。均衡度：

$$
均衡度_k=
\begin{cases}
0 & n=0 \text{ 或 } \sum_{i=1}^{n}s_{ki}=0 \\
60 & n=1 \\
\dfrac{H_k}{\ln n}\times 100 & n\ge 2
\end{cases}
$$

\(n\ge 2\) 时叶子得分越均匀，\(H_k\) 越接近 \(\ln n\)，均衡度越接近 100。\(n=1\)（该二级下只有一个有值三级）记 60，表示单叶子仍有得分、但无从判断内部是否齐整。合计为 0 记 0。

第三步：达标

$$
达标_k=\begin{cases}
1 & 成熟度_k \ge \overline{成熟度}_k\\
0 & 成熟度_k < \overline{成熟度}_k
\end{cases}
,\qquad \overline{成熟度}_k=\frac{1}{|R_k|}\sum_{r\in R_k}成熟度_{r,k}
$$

\($R_k$\) 为本批中该结构成熟度非空的区域。达标=1 为达标，=0 为未达标（页面橙/红）。本区域该结构成熟度空缺则达标空缺。

第四步：输出

输出 7 行，每行三列：成熟度、均衡度、达标。不汇总成总指数。

| 维度 | 指标说明 | 计算方法 | 源表字段 | 待建字段 |
| :----------- | :----------------------------------------------------------- | :------------------------------------------------- | -------- | -------- |
| **人才结构** | 研发人员占比、高学历人才占比的结构评价 | 成熟度=两叶子极值归一后等权；均衡度=熵（n=1记60，合计0记0）；达标=成熟度≥本批人才结构均值 | dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历；dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者入集；dwd_org_annual_financial_info(org_id, year, employees_number, development_employee) — 从业人员,研发人员；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无 |
| **企业结构** | 企业注册数量、科技型企业占比、企业规模分布的结构评价 | 同上三步，叶子为 INDEX 企业维。大型企业=org_size='大型' | dwd_org_base_info(org_id, name_cn, city, province, area, org_size, org_type, reg_status, incorporation_year) — 区域入集,机构规模,成立年；dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签 | 无 |
| **政策结构** | 政策文件数量、政策类型覆盖率的结构评价 | 同上三步，叶子为 INDEX 政策维 | dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策去重,城市,类型,主题,级别 | 无 |
| **服务机构结构** | 服务机构数量、服务机构类型数的结构评价 | 同上三步；入集=svc_org_card 规则 A 六类 | demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 服务机构清单,规则A六类；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无 |
| **科研机构结构** | 科研机构数量、类型数、科研产出总量的结构评价 | 同上三步，叶子为 INDEX 科研机构维 | dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利；dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无 |
| **资金结构** | R&D经费投入规模、融资总额的结构评价 | 同上三步。已删除财政科技支出占比 | dwd_org_annual_financial_info(org_id, year, `arch development am`, operating_revenue) — 研发投入；dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发；dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资额,融资时点；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集 | 无 |
| **空间结构** | 产业园区数量、创新空间面积、创新空间密度的结构评价 | 同上三步；面积/密度无值不进分母；园区数量用机构名称弱代理 | dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, incorporation_year) — 区域入集,机构类型,名称 | innovation_space_area-创新载体/园区面积；regional_area-区域总面积 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, org_size, reg_status, incorporation_year) — 区域入集,名称对齐,机构类型,机构规模,存续,成立年
- dwd_org_annual_financial_info(org_id, year, operating_revenue, development_employee, employees_number, total_assets, `arch development am`) — 营收,研发人员,从业人数,资产,研发投入
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发
- dwd_org_financing_info(org_id, funding_amount, completion_date) — 融资额,融资时点
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签
- dwd_policy_base(id, city, status, expire_date, type, theme, publish_year, rank) — 有效政策
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_id) — 学者入集
- dwd_scholar_education_background(scholar_id, degree_zh, degree_en) — 最高学历
- demo_gkxlumenx_ads.svc_org_card(org_id, name_cn, city, service_type_candidate) — 服务机构清单,规则A六类
- dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集
- dwd_patent(pn, kind, granted_number, first_applicant_name, applicants, pbdt_year, apdt_year) — 专利
- dwd_zh_paper(id, cover_year_start) — 中文论文
- dwd_en_paper(id, cover_year_start) — 英文论文
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

- innovation_space_area-创新载体/园区面积
- regional_area-区域总面积
