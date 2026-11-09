# 增长速度（M_INNOV_PLAN_GROWTH）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_PLAN_GROWTH |
| 指标名称 | 增长速度 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 综合发展规划 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

热门技术领域的发展速度。对象=IPC 前 4 位。看近窗相对基线的件数增幅，不是预警、不是热度指数本身。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。需求未列增长速度构成维度，二级按文献计量。采用加权平均，三维：专利增速 / 论文增速 / 项目增速。近 3 年均值相对前 5 年均值。

领域键 = 专利 `main_classification_ipcr` 前 4 位。论文、项目用题名/名称与该 IPC4 专利 `keywords` 袋相交入集；袋空则该维缺测。

增速=(近窗均值-基线均值)/max(基线均值,1)。

本批领域内对三维增速归一后等权 ×100。输出一行一个 IPC4。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 增长速度 | 专利增速 | 近窗专利相对基线。 | (近3年专利均值-前5年均值)/max(前5年均值,1) | dwd_patent(pn, main_classification_ipcr, apdt_year) — IPC领域,申请年 | 无 |
| 增长速度 | 论文增速 | 近窗命中该方向论文相对基线。 | (近3年论文均值-前5年均值)/max(前5年均值,1) | dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文题名,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文题名,发表年；dwd_patent(pn, keywords, main_classification_ipcr) — 关键词袋 | 无 |
| 增长速度 | 项目增速 | 近窗命中该方向立项相对基线。 | (近3年项目均值-前5年均值)/max(前5年均值,1) | dwd_zh_project(id, title, approval_year) — 国内项目；dwd_en_project(id, title, approval_year) — 国外项目 | 无 |

## 源表字段

- dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — IPC领域,关键词袋,申请年
- dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文题名,发表年
- dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文题名,发表年
- dwd_zh_project(id, title, approval_year) — 国内项目名称,立项年
- dwd_en_project(id, title, approval_year) — 国外项目名称,立项年

## 待建字段

- 无

## 参考资料

[1]增长速度｜中国科学技术信息研究所｜国家自然科学基金项目“科学基金项目产出专利对产业技术发展的影响研究”（L1624039）；国家社会科学基金项目“面向科技型中小企业创新的技术竞争情报方法体系研究”（12CTQ030）｜毛一雷，刘志辉，刘洢颖，姚长青. 公共基金资助产出及影响研究述评[J]. 情报探索, 2017(11): 97-103.
