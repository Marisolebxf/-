# 深圳创新载体创新价值排名（M_INNOV_CARRIER_VALUE_RANK_SZ）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CARRIER_VALUE_RANK_SZ |
| 指标名称 | 深圳创新载体创新价值排名 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 创新载体综合展示 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

深圳创新载体的创新价值名次。统计对象为深圳市内存续的高校、科研机构、企业（`org_type` 含工作室的一并纳入），从技术价值、应用价值、潜在影响力综合评分后降序排名。价值分 0—100，名次从 1 起。

## 计算逻辑说明

专利、论文一律用名称对齐，不用机构-专利/作者-机构关系表。不另建价值分字段。

### 第一步：入集

`dwd_org_base_info` 与 `dwd_research_institute_base_info` 按 `org_id` 去重合并；`reg_status` 含「存续」；`city` 去「市」后含「深圳」。名称用 `name_cn`。

### 第二步：三个子项

同一维在**本批深圳载体**内极值归一。

1. **技术价值**  
   统计年该载体专利 `value` 合计（空行不计入）+ 挂刊论文 `impact_score` 合计（`publication_id` 对齐期刊；空则该部分缺测）。专利、论文皆空则该维缺测。

2. **应用价值**  
   统计窗内该载体作为转移前或转移后权利人的专利转移去重件数 + 中文论文 `download_num` 合计（空当 0）。无转移且无下载字段则该维为 0。

3. **潜在影响力**  
   该载体专利 `cited_by_nums` 合计（无行当 0）+ 中文论文 `citation_num` 合计（无行当 0）。

专利：`first_applicant_name` 对齐 `name_cn`，`apdt_year` 落年窗。  
论文：作者 `institution` 对齐 `name_cn`，`cover_year_start` 落年窗。  
转移：`transfer_before.name` 或 `transfer_after.name` 对齐 `name_cn`，`transfer_effective_date` 落窗。

### 第三步：合成与排名

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新价值=\frac{norm(技术价值)+norm(应用价值)+norm(潜在影响力)}{3}\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `value_score` 降序，`rank` 从 1 编（同分并列，下一排名跳过）。无三维有效值的载体不入榜。

输出：一行一个载体，含 `org_id`、三子项原始值、`value_score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳创新载体创新价值排名 | 技术价值 | 专利价值与期刊影响合计。 | SUM(patent.value)+SUM(impact_score) | dwd_patent(pn, first_applicant_name, value, apdt_year) — 专利价值,申请人对齐,申请年；dwd_zh_paper(id, publication_id, cover_year_start) — 中文论文挂刊,发表年；dwd_en_paper(id, publication_id, cover_year_start) — 英文论文挂刊,发表年；dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数；dwd_en_journal(publication_id, impact_score) — 英文刊影响指数；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 深圳创新载体创新价值排名 | 应用价值 | 专利转移与论文下载。 | 转移专利数 + SUM(download_num) | dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人；dwd_zh_paper(id, download_num) — 中文论文下载量 | 无 |
| 深圳创新载体创新价值排名 | 潜在影响力 | 专利与论文被引合计。 | SUM(cited_by_nums)+SUM(citation_num) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 深圳载体入集,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, org_type, reg_status) — 科研机构入集
- dwd_patent(pn, first_applicant_name, value, apdt_year) — 专利去重,申请人对齐,专利价值,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利被引次数
- dwd_patent_transfer(pn, transfer_effective_date, transfer_before, transfer_after) — 专利转移,生效日,转移前后权利人
- dwd_zh_paper(id, publication_id, download_num, cover_year_start) — 中文论文,挂刊,下载量,发表年
- dwd_en_paper(id, publication_id, cover_year_start) — 英文论文,挂刊,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_journal(publication_id, impact_score) — 中文刊影响指数
- dwd_en_journal(publication_id, impact_score) — 英文刊影响指数
- dwd_zh_paper_citation(id, citation_num) — 中文论文被引次数

## 待建字段

- 无

## 参考资料

[1]深圳创新载体创新价值排名｜国务院办公厅｜国务院办公厅关于完善科技成果评价机制的指导意见：国办发〔2021〕26号｜2021-08-02｜https://www.gov.cn/zhengce/content/2021-08/02/content_5628987.htm.

[2]深圳创新载体创新价值排名｜浙江工商大学统计与数学学院｜国家社会科学基金项目“学术期刊评价——指标创新与方法研究”（21FTQB016）｜俞立平，沈洁. 基于论文下载与被引分区的学术期刊评价研究[J]. 中国科技期刊研究, 2022, 33(2): 260-266.
