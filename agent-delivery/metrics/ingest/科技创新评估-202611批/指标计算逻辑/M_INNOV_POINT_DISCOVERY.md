# 创新点发现（M_INNOV_POINT_DISCOVERY）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_POINT_DISCOVERY |
| 指标名称 | 创新点发现 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 全球创新监测 / 创新监测与分析 |
| 口径版本 | V1.5-20260829 |
| 更新频率 | 待确认（pending） |

## 口径定义

从专利与论文的关键词、IPC 分类中识别近期突现或新出现的创新点，输出候选列表与详情。创新点主键就是规范化词条，不另建名录。本指标不是 0—100 评分。

## 计算逻辑说明

资讯正文没有结构化词表，不入本指标。词条从现表字段拆出。

### 第一步：入集词条

页面年窗终点记为 \(T\)（默认最近有数据年），空间可选。两类词条：

| point_type | 主键 | 入集 |
| --- | --- | --- |
| keyword | 规范化关键词 | 专利 `keywords` JSON 逐词；中文论文 `dwd_zh_paper_classification.keywords` 按逗号拆；英文论文 `dwd_en_paper_classification.keywords` 取 `ch_name`（空则 `en_name`）。去空白，英文小写 |
| ipc4 | IPC 前 4 位 | 统计年专利 `main_classification_ipcr` 前 4 位去重 |

年键：专利 `apdt_year`；论文 `cover_year_start`。空间过滤：专利 `first_applicant_name`、论文作者 `institution` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`。无命中不剔除词条，只缩小计入件数的成果。

### 第二步：逐年件数

每个 `(point_type, point_key)` 按自然年计去重成果件数：该年命中该词条的专利 `pn` 数 + 中英文论文 `id` 数。首尾观测年之间缺年补 0。

### 第三步：两个子项

基线窗 \(T-7,\ldots,T-3\)（5 年），近窗 \(T-2,\ldots,T\)（3 年）。\(\bar{y}_{\mathrm{base}}\)、\(\bar{y}_{\mathrm{recent}}\) 为窗内年均件数。

1. **突现强度**

$$
\mathrm{burst}=\frac{\bar{y}_{\mathrm{recent}}-\bar{y}_{\mathrm{base}}}{\max(\bar{y}_{\mathrm{base}},1)}
$$

2. **新主题**

首次出现年 \(t_0=\min\{t:y_t>0\}\)。\(t_0\ge T-2\) 记 1，否则 0。

### 第四步：候选点

入选：`burst ≥ 1` 或新主题=1，且近窗合计件数 ≥ 3。按突现强度降序。

输出：一行一个词条，含 `point_type`、主键、`burst`、`is_new`、近窗件数、`t_0`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 创新点发现 | 突现强度 | 近窗相对基线的增幅。 | (近3年均值 − 前5年均值) / max(前5年均值, 1) | dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — 专利关键词,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词 | 无 |
| 创新点发现 | 新主题 | 是否在近窗首次出现。 | 首次出现年 ≥ T−2 记 1，否则 0 | 同上年序列 — 首次出现年 | 无 |
| 创新点发现 | 候选点 | 达标词条列表。 | 突现≥1 或新主题，且近窗件数≥3 | 同上子项计算结果 — 入选与排序 | 无 |

## 源表字段

- dwd_patent(pn, keywords, main_classification_ipcr, first_applicant_name, apdt_year) — 专利关键词,IPC领域,申请人对齐,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐
- dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1] 研究前沿识别|Drexel University|—|Chen C. CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature[J]. Journal of the American Society for Information Science and Technology, 2006, 57(3): 359-377.

[2]创新点发现｜北京大学信息管理系｜国家社会科学基金重大项目（21&ZD329）｜汪大锟，化柏林. 基于BERTopic的新兴技术主题识别研究[J]. 科技情报研究, 2025, 7(1): 131-140.



