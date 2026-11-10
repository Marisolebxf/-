# 热度指数（M_INNOV_PLAN_HEAT）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PLAN_HEAT |
| 指标名称 | 热度指数 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

热门技术领域在当前周期的受关注程度，取值 0—100。对象=IPC 前 4 位，不是单篇论文/专利计数，也不是专题单一技术 ID。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。需求未列热度构成维度，二级按文献计量。采用加权平均，三维：专利热度（年申请量）/ 论文热度（年论文数）/ 项目热度（年立项数）。本批领域内极值归一。

入集与 `M_INNOV_PLAN_GROWTH` 相同。观测值为当前统计年件数（不是增速）。

本批 IPC4 内三维归一后等权 ×100。热门列表按 `heat_score` 降序。输出一行一个 IPC4。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 热度指数 | 专利热度 | 该 IPC4 年申请量。 | COUNT(DISTINCT pn) | dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年 | 无 |
| 热度指数 | 论文热度 | 题名命中该方向的年论文数。 | COUNT(DISTINCT 论文id) | dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文题名,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文题名,发表年 | 无 |
| 热度指数 | 项目热度 | 名称命中该方向的年立项数。 | COUNT(DISTINCT 项目id) | dwd_zh_project(id, title, approval_year) — 国内项目；dwd_en_project(id, title, approval_year) — 国外项目 | 无 |

## 源表字段

- dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — IPC领域,关键词袋,申请年
- dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文题名,发表年
- dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文题名,发表年
- dwd_zh_project(id, title, approval_year) — 国内项目名称,立项年
- dwd_en_project(id, title, approval_year) — 国外项目名称,立项年

## 待建字段

- 无

## 参考资料

[1]热度指数｜中国科学技术信息研究所｜国家自然科学基金项目“科学基金项目产出专利对产业技术发展的影响研究”（L1624039）；国家社会科学基金项目“面向科技型中小企业创新的技术竞争情报方法体系研究”（12CTQ030）｜毛一雷，刘志辉，刘洢颖，姚长青. 公共基金资助产出及影响研究述评[J]. 情报探索, 2017(11): 97-103.

