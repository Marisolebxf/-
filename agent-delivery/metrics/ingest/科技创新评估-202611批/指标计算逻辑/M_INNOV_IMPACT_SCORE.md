# 创新影响分数（M_INNOV_IMPACT_SCORE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_IMPACT_SCORE |
| 指标名称 | 创新影响分数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 全球创新实时数据 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

对领域内创新实体赋创新影响分并排名。实体由专利、论文、项目现表拼出（机构、技术领域），不另建知识图谱主键。取值 0—100，分数越高影响越大。

## 计算逻辑说明

图谱没有独立实体表时，节点用机构名与 IPC 前 4 位代替。边用共现关系，分数用度数与产出，不用待建 PageRank 结果表。

### 第一步：入集节点

页面年窗、空间（可选）。两类节点：

| entity_type | 主键 | 入集 |
| --- | --- | --- |
| org | 规范化机构名 | 专利 `first_applicant_name`、论文 `institution`、项目 `funded_institution` 去重；能对齐到 `dwd_org_base_info.name_cn` 的补 `org_id` |
| domain | IPC 前 4 位 | 统计年专利 `main_classification_ipcr` 前 4 位去重 |

空间过滤：机构对齐后取 `province`/`city`；专利落到第一申请人机构所在地。无命中不剔除节点，只缩小用于计分的成果集合。

### 第二步：两个子项

同一维在**同一 `entity_type` 内**极值归一。

1. **产出规模**
   - 机构：统计年专利去重件数 + 中英文论文去重件数（名称对齐）
   - 领域：该 IPC4 下专利去重件数

2. **网络影响**
   - 机构：合作邻居数。同一专利 `applicants` 中其他机构、同一论文其他作者单位、同一项目 `participating_institution` 中其他机构，去重计数
   - 领域：该 IPC4 下专利 `cited_by_nums` 合计（无被引行当 0）

### 第三步：合成与排名

$$
norm(x)=\frac{x-\min(x)}{\max(x)-\min(x)}\quad(\text{全相同取 }0.5)
$$

$$
创新影响分数=\frac{norm(产出规模)+norm(网络影响)}{2}\times 100
$$

缺测维不补 0，剩余维权重重归一。按 `entity_type` 分组降序排名。

输出：一行一个实体，含 `entity_type`、主键、两子项原始值、`impact_score`（0—100）、`rank`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新影响分数 | 产出规模 | 机构或领域的成果件数。 | 机构：专利数+论文数；领域：专利数 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,统计年；dwd_en_paper(id, cover_year_start) — 英文论文,统计年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |
| 创新影响分数 | 网络影响 | 机构合作面或领域被引合计。 | 机构：合作邻居数；领域：SUM(cited_by_nums) | dwd_patent(pn, applicants, first_applicant_name) — 共申请人；dwd_zh_project(id, funded_institution, participating_institution) — 项目合作机构；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数 | 无 |
| 创新影响分数 | 影响分数 | 两维等权合成后的排名分。 | 0.5×norm(产出)+0.5×norm(网络) | 同上子项计算结果 — 合成与排名 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, province, city) — 机构对齐,空间过滤
- dwd_patent(pn, first_applicant_name, applicants, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,共申请人,IPC领域,申请年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,统计年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,统计年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, participating_institution, approval_year) — 受资助机构,参与机构,立项年

## 待建字段

- 无

## 参考资料

[1]创新影响分数｜科学技术部｜生物技术产业创新能力评价指标体系（征求意见稿）｜2013年｜[生物技术产业创新能力评价指标体系 -中华人民共和国科学技术部](https://www.most.gov.cn/zxgz/cxdcwq/zbtx/201311/t20131129_110671.html).
