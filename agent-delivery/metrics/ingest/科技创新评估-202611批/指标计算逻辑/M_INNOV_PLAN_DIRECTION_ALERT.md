# 潜在科技发展方向预警（M_INNOV_PLAN_DIRECTION_ALERT）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PLAN_DIRECTION_ALERT |
| 指标名称 | 潜在科技发展方向预警 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

按 IPC 前 4 位监测潜在科技发展方向并给出预警。方向主键就是 IPC4，不另建方向 ID。六源（专利 / 论文 / 项目 / 人才 / 产业 / 政策）各自算近窗相对基线增速，缺测源不补 0、剩余源权重重归一后加权得融合强度 \(F\)。\(F\) 高且多源同向抬升记为潜在方向并预警。

## 计算逻辑说明

按 IPC 前 4 位入集。采用加权平均，六维：专利 / 论文 / 项目 / 人才 / 产业 / 政策（各源近窗相对基线增速）。

### 第一步：入集

页面年窗、空间（可选）。统计年 \(T\) 默认近窗 \((T-2,\ldots,T)\)、基线窗 \((T-7,\ldots,T-3)\)。

方向键 = `dwd_patent.main_classification_ipcr` 前 4 位。专利按 `pn` 去重，`apdt_year` 落年。空间：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn` 后取 `province`/`city`；无命中不剔除方向，只缩小计入的专利。

每个 IPC4 的关键词袋 \(K\)：该方向专利 `keywords` 去重词（长度 ≥ 2）。\(K\) 为空时论文 / 项目 / 人才 / 政策四源缺测，不参与融合。

一行一个 IPC4。本批专利数 < 3 的方向不出行。

### 第二步：六源信号

各源件数按年计，再取近窗均值 $\bar{y}_{\mathrm{recent}}、基线均值 \bar{y}_{\mathrm{base}}：$

$$
g=\frac{\bar{y}_{\mathrm{recent}}-\bar{y}_{\mathrm{base}}}{\max(\bar{y}_{\mathrm{base}},1)}
$$

1. **专利**  
   该 IPC4 专利申请去重件数（`apdt_year`）。

2. **论文**  
   中英文论文 `cover_year_start` 落年；分类关键词与 \(K\) 有交集才计入。中文取 `dwd_zh_paper_classification.keywords`，英文取 `dwd_en_paper_classification.keywords`（`ch_name`/`en_name`）。

3. **项目**  
   `dwd_zh_project` 按 `id` 去重，`approval_year` 落年；`keywords` 或 `discipline` 与 \(K\) 有交集。

4. **人才**  
   `dwd_scholar_research_direction.fields` 与 \(K\) 有交集的学者，用 `dwd_scholar_paper_relation.year` 计该年发文去重学者数。

5. **产业**  
   该 IPC4 专利申请人去重机构数：`first_applicant_name` 对齐 `dwd_org_base_info.name_cn`，按申请年计新出现或活跃的机构数。

6. **政策**  
   `dwd_policy_base.publish_year` 落年；`keywords` / `theme` / `keypoints` 与 \(K\) 有交集。空间可选：政策 `city`/`province` 与页面一致。

词匹配：切分后小写去空白，长度 ≥ 2 的词有一个相同即命中。不用机构-专利 / 作者-机构关系表。

### 第三步：融合与预警

默认六源等权，页面可改，须 \($\sum w=1$\)。缺测源不补 0，剩余源权重重归一。

$$
F=\sum_{k} w_k\cdot g_k
$$

| 条件 | 等级 |
| --- | --- |
| $F\ge 1$ 且至少两源 \(g>0\) | 2 预警 |
| $F\ge 0.5$ | 1 关注 |
| 其他 | 0 无 |

$F\ge 0.5$的方向记为潜在方向。输出：一行一个 IPC4，含六源 \(g\)、`F`、`alert_level`。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 潜在科技发展方向预警 | 专利 | 该 IPC4 申请量近窗相对基线增速。 | $g=(\bar{y}_{recent}-\bar{y}_{base})/\max(\bar{y}_{base},1)$ | dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,IPC领域,申请年 | 无 |
| 潜在科技发展方向预警 | 论文 | 关键词命中该方向的论文量增速。 | 同上 \(g\) | dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 | 无 |
| 潜在科技发展方向预警 | 项目 | 关键词或学科命中该方向的立项量增速。 | 同上 \(g\) | dwd_zh_project(id, keywords, discipline, approval_year) — 项目关键词,学科,立项年 | 无 |
| 潜在科技发展方向预警 | 人才 | 研究方向命中该方向的发文学者数增速。 | 同上 \(g\) | dwd_scholar_research_direction(scholar_id, fields) — 学者研究方向；dwd_scholar_paper_relation(scholar_id, year) — 学者发文年 | 无 |
| 潜在科技发展方向预警 | 产业 | 该 IPC4 活跃申请机构数增速。 | 同上 \(g\) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤 | 无 |
| 潜在科技发展方向预警 | 政策 | 主题或关键词命中该方向的政策量增速。 | 同上 \(g\) | dwd_policy_base(id, keywords, theme, keypoints, publish_year, city, province) — 政策关键词,主题,要点,发布年,空间 | 无 |
| 潜在科技发展方向预警 | 预警等级 | 融合强度叠加多源同向。 | \($F\ge1$\) 且两源\(g>0\) 为 2；\($F\ge0.5$\) 为 1；否则 0 | 上六源 \(g\) 加权得 \(F\) | 无 |

## 源表字段

- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_project(id, keywords, discipline, approval_year) — 项目关键词,学科,立项年
- dwd_scholar_research_direction(scholar_id, fields) — 学者研究方向
- dwd_scholar_paper_relation(scholar_id, year) — 学者发文年
- dwd_policy_base(id, keywords, theme, keypoints, publish_year, city, province) — 政策关键词,主题,要点,发布年,空间
- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

- 无

## 参考资料

[1]潜在科技发展方向预警｜中国科学技术信息研究所｜国家自然科学基金项目“科学基金项目产出专利对产业技术发展的影响研究”（L1624039）；国家社会科学基金项目“面向科技型中小企业创新的技术竞争情报方法体系研究”（12CTQ030）｜毛一雷，刘志辉，刘洢颖，姚长青. 公共基金资助产出及影响研究述评[J]. 情报探索, 2017(11): 97-103.

[2]潜在科技发展方向预警｜内蒙古大学经济管理学院，中国科学院科技政策与管理科学研究所，中国科学院创新发展研究中心，中国科学院研究生院管理学院｜国家自然科学基金青年项目（71103078、71103173）；内蒙古自然科学基金项目（2011BS1002）；中国博士后科学基金第四批特别项目（201104158）；中国科学院王宽诚博士后工作奖励项目（2011年度）｜高霞，陈凯华，官建成. 标度无关性视角下的我国区域科技创新绩效评价研究[J]. 中国软科学, 2012(8): 65-74.

[3]潜在科技发展方向预警｜浙江工商大学统计与数学学院｜浙江省重点建设高校优势特色学科（浙江工商大学统计学）和“统计数据工程技术与应用协同创新中心”资助｜杨双双，解静. 基于改进CRITIC的中国区域创新能力测度分析[J]. 统计与管理, 2023, 38(9): 40-54. DOI: 10.16722/j.issn.1674-537x.2023.09.007.
