# 政策与条件保障力综合评估（M_INNOV_PG_COMPOSITE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PG_COMPOSITE |
| 指标名称 | 政策与条件保障力综合评估 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技创新评估 / 政策与条件保障力指标展示 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

将引导力、扶持力度、经费、项目、效果按自定义权重计算的政策与条件保障力综合得分与排名。对象=城市（或页面指定领域切片），取值 0—100。分数越高保障力越强。发展战略引导力三维与 `M_INNOV_PG_GUIDE` 一致。

## 计算逻辑说明

选定城市入集。采用加权平均，五维：发展战略引导力（前瞻性 / 系统性 / 针对性，与 `M_POLICY_DS_07_POLICY_GUARD_001` 同一套覆盖率）/ 政策扶持力度（政策数量 / 政策类型 / 政策覆盖面）/ 经费支持（科研经费 / 产业基金）/ 项目支持（项目数量 / 资助金额 / 实施效果）/ 政策实施效果（实施前后对比）。

### 第一步：入集

页面年窗、空间（`province`/`city`，可选）、领域（政策 `theme` 含关键词，可选）。

政策：`dwd_policy_base` 按 `id` 去重；`status` 含「有效」或 `expire_date` 晚于统计年末；`publish_year` 落年窗。  
机构：`dwd_org_base_info` 存续，名称用 `name_cn`。  
项目：`dwd_zh_project` 按 `id` 去重；`approval_year` 落年窗；`funded_institution` 对齐机构名后取城市，或 `funded_province` 命中空间。  
产业基金：`dwd_industrial_fund_basic_info`，`reg_region` 含该城，`est_date` 落年窗。

一行一个城市。本批至少 2 个城市才做极值归一。缺测维不补 0，剩余维权重重归一。不用专家评分、不用机构-项目关系表。

### 第二步：各指标标准化

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

指标得分 \(=norm(x)\times 100\)。同一维在**本批城市**内归一。默认维内等权，页面可改，须 \(\sum w=1\)。

### 第三步：各维度得分

1. **发展战略引导力**（与 `M_INNOV_PG_GUIDE`、`M_POLICY_DS_07_POLICY_GUARD_001` 同一三级）  
   前瞻性 = 四字段含「规划」或「纲要」或「远景」的政策数 ÷ 政策总数。  
   系统性 = `quote_policy` 非空且不为空数组的政策数 ÷ 政策总数。  
   针对性 = `policy_support.support_way` 至少 1 条非空的政策数 ÷ 政策总数。

$$
引导力=\frac{norm(前瞻性)+norm(系统性)+norm(针对性)}{3}
$$

2. **政策扶持力度**

$$
扶持力度=\frac{norm(政策数量)+norm(政策类型)+norm(政策覆盖面)}{3}
$$

3. **经费支持**

$$
经费支持=\frac{norm(科研经费)+norm(产业基金)}{2}
$$

4. **项目支持**

$$
项目支持=\frac{norm(项目数量)+norm(资助金额)+norm(实施效果)}{3}
$$

5. **政策实施效果**  
   近窗 \((T-2,\ldots,T)\) 相对基线 \((T-7,\ldots,T-3)\) 的成果增幅（专利去重件数 + 中英文论文去重件数，名称对齐）：

$$
效果=\frac{\bar{y}_{\mathrm{recent}}-\bar{y}_{\mathrm{base}}}{\max(\bar{y}_{\mathrm{base}},1)}
$$

### 第四步：综合得分

默认五维等权，页面可改，须 \(\sum W=1\)。

$$
保障力=\sum_{k=1}^{5} W_k\cdot 维度得分_k\times 100
$$

输出：一行一城，含各三级原始值、五维得分、`score`（0—100）、`rank`。

| 维度 | 指标 | 指标说明 | 计算方法 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| **发展战略引导力** | 前瞻性 | 政策是否包含规划/纲要/远景等顶层设计词。 | 四字段含「规划」或「纲要」或「远景」的政策数 ÷ 政策总数 | dwd_policy_base(title, keywords, keypoints, theme) — 四字段命中 | 无 |
| | 系统性 | 政策是否明确引用或承接过往相关政策。 | quote_policy 非空且不为空数组的政策数 ÷ 政策总数 | dwd_policy_base(quote_policy) — 政策承接 | 无 |
| | 针对性 | 政策是否包含明确扶持细则。 | policy_support.support_way 至少 1 条非空的政策数 ÷ 政策总数 | dwd_policy_base(policy_support.support_way) — 扶持措施 | 无 |
| **政策扶持力度** | 政策数量 | 有效政策去重件数。 | COUNT(DISTINCT id) | dwd_policy_base(id, city, status, expire_date, publish_year) — 政策件数,有效 | 无 |
| | 政策类型 | 政策类型覆盖数。 | COUNT(DISTINCT type) | dwd_policy_base(id, city, type, status, expire_date, publish_year) — 政策类型 | 无 |
| | 政策覆盖面 | 政策触及的区县广度；`district` 全空则改用主题数。 | COUNT(DISTINCT district)；全空则 COUNT(DISTINCT theme) | dwd_policy_base(id, city, district, theme, status, expire_date, publish_year) — 区县,主题 | 无 |
| **经费支持** | 科研经费 | 该城机构上市研发投入合计。 | SUM(research_development_amount) | dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 机构对齐,空间 | 无 |
| | 产业基金 | 注册地落在该城的产业基金数。 | COUNT(DISTINCT industrial_fund_id) | dwd_industrial_fund_basic_info(industrial_fund_id, reg_region, est_date) — 基金注册地,设立日 | 无 |
| **项目支持** | 项目数量 | 立项项目去重件数。 | COUNT(DISTINCT id) | dwd_zh_project(id, funded_institution, funded_province, approval_year) — 项目去重,立项年 | 无 |
| | 资助金额 | 项目资助额合计。 | SUM(funded_amount) | dwd_zh_project(id, funded_amount, funded_institution, funded_province, approval_year) — 资助金额,立项年 | 无 |
| | 实施效果 | 有结题摘要的项目占比。 | 结题项目数 / 项目数 | dwd_zh_project(id, final_report_abstract, funded_institution, funded_province, approval_year) — 结题摘要 | 无 |
| **政策实施效果** | 实施前后对比 | 近窗成果相对基线的增幅。 | (近3年均值 − 前5年均值) / max(前5年均值, 1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |

## 源表字段

- dwd_policy_base(id, title, keywords, keypoints, theme, quote_policy, policy_support, city, province, district, status, expire_date, publish_year, rank, type) — 四字段前瞻词,政策承接,扶持措施,有效,级别,类型,区县
- dwd_zh_project(id, funded_amount, funded_institution, funded_province, approval_year, final_report_abstract) — 项目资助,机构对齐,立项年,结题
- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 机构入集,名称对齐,空间
- dwd_org_stock_finance_info(org_id, occur_period, research_development_amount) — 上市研发投入
- dwd_industrial_fund_basic_info(industrial_fund_id, reg_region, est_date) — 产业基金注册地,设立日
- dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

- 无

## 参考资料

[1] 政策与条件保障力综合评估|浙江大学科教发展战略研究中心|浙江省科技厅重点软科学项目（2016C25G2010003）|张炜, 费小燕, 方辉. 区域创新政策多维度评价指标体系设计与构建[J]. 科技进步与对策, 2016, 33(1): 142-147.

[2]政策与条件保障力综合评估｜浙江大学科教发展战略研究中心｜浙江省自然科学基金项目（LY15G030009）；浙江省科技厅重点软科学项目（2016C25G2010003）｜张炜，费小燕，肖云，等. 基于多维度评价模型的区域创新政策评估——以江浙沪三省为例[J]. 科研管理, 2016, 37(S1): 614-622. DOI: 10.19571/j.cnki.1000-2995.2016.s1.088.

[3]政策与条件保障力综合评估｜四川工商学院｜赵江红. 四川省财政科技支出动态绩效评价指标研究[J]. 投资与合作, 2025(6): 74-76.
