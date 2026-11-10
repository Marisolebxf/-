# 湾区创新热点区域（M_INNOV_GBA_HOTSPOT）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_GBA_HOTSPOT |
| 指标名称 | 湾区创新热点区域 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 湾区创新监测 / 创新成果综合展示 |
| 口径版本 | V1.5-20260830 |
| 更新频率 | 待确认（pending） |

## 口径定义

识别粤港澳大湾区内创新成果更密的区县，给出创新密度、主要创新类型与是否热点。区域主键就是 `city`+`area`，不另建名录。

## 计算逻辑说明

成果落到机构所在区县。经纬度只供落图，不参与热点判定。

湾区城市：广州、深圳、珠海、佛山、惠州、东莞、中山、江门、肇庆、香港、澳门。`city`/`province` 去「市」「特别行政区」后命中即入集。

### 第一步：入集并落区

湾区内存续机构：`dwd_org_base_info`、`dwd_research_institute_base_info` 按 `org_id` 去重，`reg_status` 含「存续」；港澳补 `dwd_forg_base_info`。名称对齐：国内 `name_cn`，海外 `name_en`/`name_alias`。

区域主键 `region_key` = `city` + `area`（`area` 空则只用 `city`）。机构无 `city` 不入集。

统计年成果按名称对齐后继承机构区县：

| 成果 | 对齐 | 年键 | 计数 |
| --- | --- | --- | --- |
| 专利 | `first_applicant_name` | `apdt_year` | `COUNT(DISTINCT pn)` |
| 论文 | 作者 `institution` | `cover_year_start` | 中英文 `COUNT(DISTINCT id)` |
| 项目 | `funded_institution` | `approval_year` | `COUNT(DISTINCT id)` |

### 第二步：两个子项

1. **创新密度**

$$
创新密度=\frac{专利数+论文数+项目数}{该区县存续机构数}
$$

机构数为 0 的区县不出行。

2. **主要创新类型**

该区县专利、论文、项目三件数取最大者，记 `patent` / `paper` / `project`。并列取专利优先，其次论文。专利领先时附带该区县专利 `main_classification_ipcr` 前 4 位众数，作类型细节。

### 第三步：热点标签

本批有效区县（机构数 ≥ 3）内，创新密度 ≥ 第 70 百分位记 1，否则 0。有效区县 < 5 时不出热点标签，只出密度与类型。

输出：一行一个区县，含 `region_key`、`city`、`area`、三类件数、机构数、`density`、`main_type`、`is_hotspot`。有 `addr_lng`/`addr_lat` 的机构可叠加热力点，不另算密度。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 湾区创新热点区域 | 创新密度 | 区县单位机构的成果件数。 | (专利数+论文数+项目数) / 存续机构数 | dwd_org_base_info(org_id, name_cn, city, province, area, reg_status) — 机构入集,区县主键；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年 | 无 |
| 湾区创新热点区域 | 主要创新类型 | 该区县成果件数最大的类型。 | 专利/论文/项目取最大；并列专利优先 | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利件数,IPC众数；dwd_zh_paper(id, cover_year_start) — 中文论文件数；dwd_en_paper(id, cover_year_start) — 英文论文件数；dwd_zh_project(id, funded_institution, approval_year) — 项目件数 | 无 |
| 湾区创新热点区域 | 热点标签 | 密度是否达到本批高位。 | 密度 ≥ P70 且机构数≥3 记 1 | 同上密度结果 — 分位判定 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status, addr_lng, addr_lat) — 湾区机构入集,区县主键,名称对齐,落图
- dwd_research_institute_base_info(org_id, name_cn, city, province, area, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 港澳机构入集
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC类型,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_zh_project(id, funded_institution, approval_year) — 受资助机构,立项年

## 待建字段

- 无

## 参考资料

[1]湾区创新热点区域｜重庆生产力促进中心，重庆工商大学数学与统计学院，重庆市科学技术情报学会｜《重庆科技创新指数报告2023》[R]. 西南财经大学出版社, 2024-09-25.

[2]湾区创新热点区域｜广州大学地理科学与遥感学院｜国家自然科学基金项目（41771127）｜陈小兰，千庆兰，张凯煌. 广州创新区的分布、类型及资产特征[J]. 现代城市研究, 2021(1): 39-44.

[3]湾区创新热点区域｜武汉理工大学土木工程与建筑学院｜李文诗. 基于DBSCAN算法的武汉东湖高新区创新空间集群识别与分布特征研究[J]. 建筑与文化, 2025(7): 67-69. DOI: 10.19875/j.cnki.jzywh.2025.07.022.
