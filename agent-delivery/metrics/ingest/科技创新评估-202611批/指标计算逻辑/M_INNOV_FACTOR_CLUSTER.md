# 要素聚类（M_INNOV_FACTOR_CLUSTER）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_FACTOR_CLUSTER |
| 指标名称 | 要素聚类 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技全域态势 / 科创要素 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

对选定范围内的会议、项目（含课题）、专利、期刊四类科创要素，用各自影响力得分做无监督分簇。输出每个实体的簇标签、到簇心距离，以及各簇规模与类型构成。本指标不是 0—100 评分。

## 计算逻辑说明

聚类对象只取四类要素，影响力口径分别复用：

| factor_type | 对应指标 | 实体主键 | 影响力分 |
| --- | --- | --- | --- |
| conference | M_INNOV_CONFERENCE_INFLUENCE（会议影响力） | `publication_id` | `influence_score`（0—100） |
| project | M_INNOV_PROJECT_INFLUENCE（项目（含课题）影响力） | `id` | `influence_score`（0—100） |
| patent | M_INNOV_PATENT_INFLUENCE（专利影响力） | `pn` | `influence_score`（0—100） |
| journal | M_INNOV_JOURNAL_INFLUENCE（期刊影响力） | `publication_id` | `influence_score`（0—100） |

入集、子项与合成公式一律跟对应影响力指标，本指标不另造得分。

### 第一步：入集并取影响力分

页面传入空间（可选）、统计年窗（可选）、要素类型集合（默认四类都跑，可只跑一类）。

1. 按上表分别跑四个影响力指标，得到实体主键与 `influence_score`。
2. 每条样本带 `factor_type`。无影响力分的实体不入集（缺测不补 0）。
3. 有效样本数 N*N*：N<5*N*<5 时，若 N≥3*N*≥3，降级为完全图连接（所有点在同一簇，无距离），标记 `algo=fallback_full`，`cluster_id=0`，`distance_to_center=null`；若 N<3*N*<3，标记 `skip_reason=too_few`，不出簇。

### 第二步：构造特征向量

对每个实体拼向量：

$$
\mathbf{x}=[\mathbf{x}_{\mathrm{type}}\,|\,x_{\mathrm{score}}]
$$

**1）类型块 \(\mathbf{x}_{\mathrm{type}}\)**

对 `factor_type` 做独热（conference / project / patent / journal）。单类型批次可省略本块，只按影响力分聚类。

**单类型批次 + DBSCAN 场景**：若业务指定 `algo=dbscan` 且为单类型批次（仅一维影响力分），为避免DBSCAN在高密度区域将相近分数全部聚为一簇，增加一个辅助维度（如实体影响力的排名百分位或随机抖动向量），使DBSCAN能有效区分。辅助维度仅用于DBSCAN距离计算，不参与簇摘要展示。

**2）影响力块 \(x_{\mathrm{score}}\)**

取对应指标的 `influence_score`。该分已在各自指标内按本批极值归一并 ×100，本指标再在**本批入集样本**内做一次极值归一，避免四类分数尺度混用时被某一类拉开：

$$
\mathrm{norm}(s)=\frac{s-\min s}{\max s-\min s}\quad(\text{全相同取 }0.5)
$$

类型块与影响力块先各自标准化，再等权拼接（各 1/2）。缺类型块时权重全部落到影响力分。

不把 IPC、地域、关键词另拼进向量；领域/地域只作簇摘要展示，不参与距离。

### 第三步：选择聚类算法

| 条件 | 算法 | 参数 |
| --- | --- | --- |
| \(N≥30\)（默认） | K-Means | 欧氏距离；\(K\in\{2,3,\ldots,8\}\)，取轮廓系数最大者；若最大轮廓 \(<0.15\) 或最优 \(K=1\)，视为不可分，只输出 1 簇 |
| \(5≤N<30\) | 层次聚类（Ward） | 链接准则 Ward；簇数规则同 K-Means |
| 业务指定 `algo=dbscan` | DBSCAN | `min_pts=5`；`eps`=每点到第 4 近邻距离的中位数 |

同一批次只跑一种方法，结果写入 `algo`（`kmeans` / `hierarchical` / `dbscan`）。

$$
\mathrm{Silhouette}=\frac{1}{N}\sum_{i=1}^{N}\frac{b_i-a_i}{\max(a_i,b_i)}
$$

其中 \(a_i\) 为点 \(i\) 到同簇其他点的平均距离，\(b_i\) 为到最近其他簇的平均距离。

### 第四步：生成簇标签与摘要

1. 为每个实体写入 `cluster_id`（从 0 起编；DBSCAN 噪声点 `cluster_id=-1`）。
2. 到簇心距离：K-Means / Ward 取 ∥xi−ck∥2∥**x***i*−**c***k*∥2；DBSCAN 噪声点距离为空；完全图连接方式距离为空。
3. **簇内归一化距离**：`dist_norm = distance_to_center / 簇内最大距离`，归一化后 0~1，1 代表该成员在簇内最边缘。用于判断成员在簇内的相对位置，噪声点或完全图连接方式该值为空。
4. **自动标签**：基于簇内影响力分中位数和类型分布占比，自动生成简短标签：
   - `score_p50 ≥ 80` → `high_impact`
   - `score_p50 ≤ 40` → `low_impact`
   - `type_mix中某类型占比≥60%` → `{type}_dominant`（如 `patent_dominant`）
   - 若同时满足多个条件，按优先级 `high_impact` > `low_impact` > `type_dominant` 取其一，否则为 `general`。
5. 簇摘要（每个 `cluster_id` 一行）：
   - `member_cnt`：成员数
   - `type_mix`：各 `factor_type` 计数
   - `score_mean`：簇内影响力分均值
   - `score_p50`：簇内影响力分中位数
   - `cluster_label`：自动标签

### 第五步：输出

- **成员表**：`factor_type`，`factor_id`，`influence_score`，`cluster_id`，`distance_to_center`，`dist_norm`，`cluster_label`，`algo`，`src_metric`
- **簇摘要表**：`cluster_id`，`member_cnt`，`type_mix`，`score_mean`，`score_p50`，`cluster_label`
- **聚类质量指标**（随簇摘要输出）：
  - 若聚类成功（非完全图连接），输出 `avg_silhouette`（平均轮廓系数）、`db_index`（Davies-Bouldin指数）、`ch_index`（Calinski-Harabasz指数）
  - 若为完全图连接或DBSCAN噪声点过多，`avg_silhouette`、`db_index`、`ch_index` 置空，并标记 `quality_na_reason`
- 不输出新的 0—100 分（影响力分只作特征，来自上述四个指标）。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 要素聚类 | 会议要素 | 会议实体及其会议影响力分。 | 取 M_INNOV_CONFERENCE_INFLUENCE.influence_score | dwd_zh_journal(publication_id, publication_type, impact_score) — 中文会议入集,影响指数；dwd_en_journal(publication_id, publication_type, impact_score) — 英文会议入集,影响指数；dwd_zh_paper(id, publication_id, publication_type, download_num, cover_year_start) — 中文会议论文,下载量,统计年；dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 英文会议论文,统计年；dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者；dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者 | 无 |
| 要素聚类 | 项目要素 | 项目/课题实体及其项目影响力分。 | 取 M_INNOV_PROJECT_INFLUENCE.influence_score | dwd_zh_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国内项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年；dwd_en_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国外项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年 | 无 |
| 要素聚类 | 专利要素 | 专利实体及其专利影响力分。 | 取 M_INNOV_PATENT_INFLUENCE.influence_score | dwd_patent(pn, value, apdt_year, pbdt_year) — 专利去重,专利价值,申请年,公开年；dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数 | 无 |
| 要素聚类 | 期刊要素 | 期刊实体及其期刊影响力分。 | 取 M_INNOV_JOURNAL_INFLUENCE.influence_score | dwd_zh_journal(publication_id, publication_type, impact_score, paper_nums, cite_nums) — 中文期刊入集,影响指数,发文量,被引用量；dwd_en_journal(publication_id, publication_type, impact_score, paper_nums) — 英文期刊入集,影响指数,发文量；dwd_zh_paper(id, publication_id, cover_year_start) — 中文发文回退,统计年；dwd_en_paper(id, publication_id, cover_year_start) — 英文发文回退,统计年 | 无 |
| 要素聚类 | 簇标签 | 按类型独热 + 影响力分聚类后的簇编号与摘要。 | K-Means / Ward / DBSCAN | 同上四个影响力结果 — 分簇与簇摘要 | 无 |

## 源表字段

- dwd_zh_journal(publication_id, publication_type, zh_name, en_name, impact_score, paper_nums, cite_nums) — 会议/期刊入集,影响指数,发文量,被引用量
- dwd_en_journal(publication_id, publication_type, zh_name, en_name, impact_score, paper_nums) — 会议/期刊入集,影响指数,发文量
- dwd_zh_paper(id, publication_id, publication_type, download_num, cover_year_start) — 会议论文,下载量,期刊发文回退,统计年
- dwd_en_paper(id, publication_id, publication_type, cover_year_start) — 会议论文,期刊发文回退,统计年
- dwd_zh_author(paper_id, author_id, zh_name, en_name) — 中文作者,会议参与人数
- dwd_en_author(paper_id, author_id, zh_name, en_name) — 英文作者,会议参与人数
- dwd_zh_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国内项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年
- dwd_en_project(id, funded_amount, participating_institution, funded_institution, final_report_abstract, approval_year) — 国外项目入集,资助金额,参与机构,受资助机构,结题摘要,立项年
- dwd_patent(pn, value, apdt_year, pbdt_year) — 专利去重,专利价值,申请年,公开年
- dwd_patent_cited(pn, cited_by_nums) — 专利对齐,被引次数

## 待建字段

- 无

## 参考资料

[1]要素聚类｜南京大学信息管理系，中国科学技术信息研究所｜国家十一五支撑计划项目（2006BAH03B05）；国家自然科学基金项目（70673019）｜俞立平，潘云涛，武夷山. 基于因子分析的学术期刊评价指标分类研究[J]. 图书情报工作, 2009, 53(8): 146-149.

[2]要素聚类｜同济大学上海国际知识产权学院，国家知识产权局｜国家自然科学基金项目（71874122、71403188）；国家知识产权局软科学研究项目（SS16-B-06）；江苏省社会科学基金重点项目（20WTA-010）；同济大学研究生课程思政研究项目（2021KCSZYJ28）｜刘谦，姜南，王亚利，等. 国内高价值专利研究热点演进与整合框架——基于SKM的可视化分析[J]. 科技进步与对策, 2022, 39(21): 151-160.
