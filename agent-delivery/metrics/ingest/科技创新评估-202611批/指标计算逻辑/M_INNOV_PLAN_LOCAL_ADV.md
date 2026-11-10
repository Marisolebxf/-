# 本地科技创新特色与优势（M_INNOV_PLAN_LOCAL_ADV）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PLAN_LOCAL_ADV |
| 指标名称 | 本地科技创新特色与优势 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

本地（未选时默认深圳）相对全域的科技创新特色与优势。领域主键就是 IPC 前 4 位，不另建优势领域 ID。三维区位商：专利 / 论文 / 创新资源。专利区位商 \(>1\) 记为本地优势领域，并给出与全域的对比。

## 计算逻辑说明

本地（默认深圳）按 IPC 前 4 位入集。三维：专利区位商 / 论文区位商 / 创新资源区位商。区位商 \(>1\) 为优势领域。

### 第一步：入集

页面年窗、本地城市（空则 `city` 含「深圳」）。

本地机构：`dwd_org_base_info` 按 `org_id` 去重，`reg_status` 含「存续」，`city` 命中本地。名称用 `name_cn`。

专利：`dwd_patent` 按 `pn` 去重；`apdt_year` 落年窗；领域键 = `main_classification_ipcr` 前 4 位。本地专利：`first_applicant_name` 对齐本地机构名。全域专利不过滤城市。

每个 IPC4 的关键词袋 \(K\)：该方向专利 `keywords` 去重词（长度 ≥ 2）。\(K\) 为空时论文区位商缺测。

一行一个 IPC4。本地与全域在该方向专利数均为 0 的不出行。

不用机构-专利 / 作者-机构关系表。

### 第二步：三个子项

区位商：

$$
LQ=\frac{本地该方向值/本地合计}{全域该方向值/全域合计}\qquad(\text{分母为 }0\text{ 缺测})
$$

1. **专利区位商**  
   值为专利申请去重件数。

2. **论文区位商**  
   值为论文去重件数。论文 `cover_year_start` 落年窗；分类关键词与 \(K\) 有交集。本地论文：作者 `institution` 对齐本地机构名；中文 `dwd_zh_author`、英文 `dwd_en_author`。

3. **创新资源区位商**  
   值为该方向活跃机构数：在该 IPC4 有本地/全域专利的申请人去重机构数。展示用可并列本地高企数（`dwd_org_tech_tag.org_tag` 含「高新技术」）和研发人员合计（`dwd_org_annual_financial_info.development_employee`，`year` 落窗）。

### 第三步：优势判定

专利区位商 \(>1\) 记为本地优势领域。三项均有值时给出综合优势比（等权平均，页面可改权重）。

输出：一行一个 IPC4，含三项 \(LQ\)、`is_advantage`、本地/全域原始件数；另可附本地机构数、高企数、研发人员合计供资源分布图。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 本地科技创新特色与优势 | 专利区位商 | 本地该 IPC4 专利份额相对全域份额。 | (本地该方向专利/本地专利) / (全域该方向专利/全域专利) | dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 本地机构,名称对齐 | 无 |
| 本地科技创新特色与优势 | 论文区位商 | 本地该方向论文份额相对全域份额。 | (本地该方向论文/本地论文) / (全域该方向论文/全域论文) | dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 本地科技创新特色与优势 | 创新资源区位商 | 本地该方向活跃机构份额相对全域份额。 | (本地该方向机构/本地机构) / (全域该方向机构/全域机构) | dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 本地机构；dwd_org_tech_tag(org_id, org_tag) — 高新技术标签；dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 本地机构入集,名称对齐
- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_org_tech_tag(org_id, org_tag) — 高新技术企业等科技型标签
- dwd_org_annual_financial_info(org_id, year, development_employee) — 研发人员

## 待建字段

- 无

## 参考资料

[1]本地科技创新特色与优势｜中国科学技术信息研究所｜国家自然科学基金项目“科学基金项目产出专利对产业技术发展的影响研究”（L1624039）；国家社会科学基金项目“面向科技型中小企业创新的技术竞争情报方法体系研究”（12CTQ030）｜毛一雷，刘志辉，刘洢颖，姚长青. 公共基金资助产出及影响研究述评[J]. 情报探索, 2017(11): 97-103.

[2]本地科技创新特色与优势｜内蒙古大学经济管理学院，中国科学院科技政策与管理科学研究所，中国科学院创新发展研究中心，中国科学院研究生院管理学院｜国家自然科学基金青年项目（71103078、71103173）；内蒙古自然科学基金项目（2011BS1002）；中国博士后科学基金第四批特别项目（201104158）；中国科学院王宽诚博士后工作奖励项目（2011年度）｜高霞，陈凯华，官建成. 标度无关性视角下的我国区域科技创新绩效评价研究[J]. 中国软科学, 2012(8): 65-74.
