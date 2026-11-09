# 创新价值（M_INNOV_ACHIEVE_VALUE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_ACHIEVE_VALUE |
| 指标名称 | 创新价值 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新成果综合展示 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

单条创新成果的综合分值。统计对象为选定范围内的专利、论文、项目，从技术价值、应用价值、潜在影响力综合评分，取值 0—100。分数越高，创新价值越强，用于列表排序与分档。

## 计算逻辑说明

成果主键按类型自带：专利 `pn`、论文 `id`、项目 `id`。不另建名录主键。资讯/机构动态不入本指标。

### 第一步：入集

页面年窗、空间（可选）。三类分别入集后打 `achieve_type`：

| achieve_type | 主键 | 入集 |
| --- | --- | --- |
| patent | `pn` | `dwd_patent` 去重；`apdt_year` 落年窗 |
| paper | `zh:`/`en:` + `id` | `dwd_zh_paper` / `dwd_en_paper` 去重；`cover_year_start` 落年窗 |
| project | `zh:`/`en:` + `id` | `dwd_zh_project` / `dwd_en_project` 去重；`approval_year` 落年窗 |

空间过滤：专利用 `first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`；论文用作者 `institution` 对齐；项目用 `funded_province`。无命中不剔除，只缩小入集。

### 第二步：三个子项（按类型取现成字段）

同一维在**同一 `achieve_type` 内**极值归一，避免专利价值与论文下载量混比。

1. **技术价值**
   - 专利：`dwd_patent.value`（空则该维缺测）
   - 论文：挂刊 `impact_score`（`publication_id` 对齐期刊；空则缺测）
   - 项目：`funded_amount`（空则缺测）

2. **应用价值**
   - 专利：统计窗内该 `pn` 命中 `dwd_patent_transfer` 的去重件数（无记录当 0）
   - 论文：`download_num`（空当 0；英文论文无该字段则该维缺测）
   - 项目：有非空 `final_report_abstract` 记 1，否则 0

3. **潜在影响力**
   - 专利：`dwd_patent_cited.cited_by_nums`（无行当 0）
   - 论文：挂刊 `jn_zone` 映射（1 区=4，2 区=3，3 区=2，4 区=1，其他/空=0）
   - 项目：`project_level` 映射（国家级=3，省部级=2，其他=1，空=0）

### 第三步：合成

三子项归一后等权 ×100。缺测维不补 0，剩余维权重按比例重归一。

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新价值=\frac{norm(技术价值)+norm(应用价值)+norm(潜在影响力)}{3}\times 100
$$

列表排序用 `value_score`。分档：本批 ≥P70 高、≤P30 低，其余中。

输出：一行一条成果，含 `achieve_type`、主键、三子项原始值、`value_score`（0—100）、`tier`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新价值 | 技术价值 | 成果技术含量代理。 | 专利 value；论文 impact_score；项目 funded_amount | dwd_patent(pn, value, apdt_year) — 专利价值,申请年；dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数；dwd_en_journal(publication_id, impact_score) — 英文刊影响指数；dwd_zh_paper(id, publication_id, cover_year_start) — 中文论文挂刊,统计年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文挂刊,统计年；dwd_zh_project(id, funded_amount, approval_year) — 国内资助金额,立项年；dwd_en_project(id, funded_amount, approval_year) — 国外资助金额,立项年 | 无 |
| 创新价值 | 应用价值 | 成果落地与传播代理。 | 专利转移件数；论文 download_num；项目结题有无 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_zh_paper(id, download_num) — 中文论文下载量；dwd_zh_project(id, final_report_abstract) — 国内结题摘要；dwd_en_project(id, final_report_abstract) — 国外结题摘要 | 无 |
| 创新价值 | 潜在影响力 | 成果扩散潜力代理。 | 专利被引；论文期刊分区映射；项目级别映射 | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_journal(publication_id, jn_zone) — 中文刊分区；dwd_en_journal(publication_id, jn_zone) — 英文刊分区；dwd_zh_project(id, project_level) — 国内项目级别；dwd_en_project(id, project_level) — 国外项目级别 | 无 |

## 源表字段

- dwd_patent(pn, value, first_applicant_name, apdt_year) — 专利去重,专利价值,申请人对齐,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日
- dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文去重,挂刊,下载量,发表年
- dwd_en_paper(id, publication_id, cover_year_start) — 英文论文去重,挂刊,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_zh_journal(publication_id, impact_score, jn_zone) — 中文刊影响指数,分区
- dwd_en_journal(publication_id, impact_score, jn_zone) — 英文刊影响指数,分区
- dwd_zh_project(id, funded_amount, final_report_abstract, project_level, approval_year, funded_province) — 国内项目资助,结题,级别,立项年,资助省
- dwd_en_project(id, funded_amount, final_report_abstract, project_level, approval_year) — 国外项目资助,结题,级别,立项年
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1]创新价值｜国务院办公厅｜国务院办公厅关于完善科技成果评价机制的指导意见：国办发〔2021〕26号｜2021-08-02｜https://www.gov.cn/zhengce/content/2021-08/02/content_5628987.htm.

[2]创新价值｜浙江工商大学统计与数学学院｜国家社会科学基金项目“学术期刊评价——指标创新与方法研究”（21FTQB016）｜俞立平，沈洁. 基于论文下载与被引分区的学术期刊评价研究[J]. 中国科技期刊研究, 2022, 33(2): 260-266.
