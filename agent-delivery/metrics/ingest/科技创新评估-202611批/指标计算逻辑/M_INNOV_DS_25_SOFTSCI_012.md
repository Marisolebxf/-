# 影响力评价与应用反馈（M_INNOV_DS_25_SOFTSCI_012）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_DS_25_SOFTSCI_012 |
| 指标名称 | 影响力评价与应用反馈 |
| 使用位置 | 科技专题服务系统 / 科技专题战略分析 / 软科学课题分析 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

软科学课题的影响力与应用反馈。统计对象为国内项目表中筛出的软科学课题，从课题能级、成果影响、应用反馈综合评分，取值 0—100。分数越高，影响越大。反馈正文用结题摘要，不另建反馈表。

## 计算逻辑说明

课题主键就是 `dwd_zh_project.id`。只跑国内项目。不用机构-项目关系表，不用用户态评价表。

### 第一步：入集

`dwd_zh_project` 按 `id` 去重；`approval_year` 落年窗。软科学入集（满足任一）：

- `discipline` / `keywords` / `title` / `fund_category` 含「软科学」
- 或 `discipline` 含「管理学」「公共管理」「应用经济」「社会学」「政治学」

空间可选：`funded_province`，或 `funded_institution` 对齐 `dwd_org_base_info.name_cn` 后取 `city`。

产出：`dwd_zh_project_output.id` 对齐课题 `id`；无产出行各计数字段当 0。

### 第二步：三个子项

同一维在**本批软科学课题**内极值归一。

1. **课题能级**  
   `funded_amount`（空则缺测）与 `project_level` 映射（国家级=3，省部级=2，其他=1，空=0）。两子项本批归一后等权。

2. **成果影响**  
   `journal_articles_count + conference_papers_count + patents_count + awards_count`（空当 0）。有 `total_outputs` 且大于该合计时改用 `total_outputs`。

3. **应用反馈**  
   结题摘要非空记 1，否则 0；加上 `reports_count`（空当 0）。反馈记录展示 `final_report_abstract`，不另建字段。

### 第三步：合成

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
影响力评价=\frac{norm(课题能级)+norm(成果影响)+norm(应用反馈)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。

输出：一行一个课题，含 `id`、三子项原始值、`influence_score`（0—100）、结题摘要（反馈正文）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 影响力评价与应用反馈 | 课题能级 | 资助金额与项目级别。 | 0.5×norm(funded_amount)+0.5×norm(级别映射) | dwd_zh_project(id, funded_amount, project_level, approval_year) — 资助金额,项目级别,立项年 | 无 |
| 影响力评价与应用反馈 | 成果影响 | 论文、专利与奖项产出件数。 | 期刊+会议+专利+奖项件数 | dwd_zh_project_output(id, journal_articles_count, conference_papers_count, patents_count, awards_count, total_outputs) — 期刊文章,会议论文,专利,奖项,总产出 | 无 |
| 影响力评价与应用反馈 | 应用反馈 | 结题摘要与报告产出。 | I(结题摘要非空)+reports_count | dwd_zh_project(id, final_report_abstract) — 结题摘要；dwd_zh_project_output(id, reports_count) — 报告数量 | 无 |

## 源表字段

- dwd_zh_project(id, title, discipline, keywords, fund_category, funded_amount, project_level, funded_institution, funded_province, final_report_abstract, approval_year) — 软科学入集,资助,级别,机构对齐,结题摘要,立项年
- dwd_zh_project_output(id, journal_articles_count, conference_papers_count, patents_count, awards_count, reports_count, total_outputs) — 课题产出对齐,论文专利奖项报告
- dwd_org_base_info(org_id, name_cn, city, province) — 受资助机构名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 发展战略引导力评估|浙江大学科教发展战略研究中心|浙江省科技厅重点软科学项目（2016C25G2010003）|张炜, 费小燕, 方辉. 区域创新政策多维度评价指标体系设计与构建[J]. 科技进步与对策, 2016, 33(1): 142-147.

[2]影响力评价与应用反馈｜安徽中医药大学财务处｜无基金项目资助｜林永格，刘喾婴. 高校科研经费投入与产出的研究分析[J]. 安徽农业大学学报(社会科学版), 2017, 26(3): 59-63, 105. DOI: 10.19747/j.cnki.1009-2463.2017.03.011.

[3]影响力评价与应用反馈｜北京化工大学经济管理学院，国家自然科学基金委员会计划局｜吴卫红，王晓雨，李志兰，等. 联合基金结题项目成果绩效分析与思考[J]. 中国科学基金, 2021, 35(4): 636-642. DOI: 10.16262/j.cnki.1000-8217.2021.04.014.
