# 多企业竞争情报比对（M_INNOV_RES_CI_COMPARE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_RES_CI_COMPARE |
| 指标名称 | 多企业竞争情报比对 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 研究领域分析 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

比对多家企业的竞争情报等级，并给出竞争矩阵与战略定位图。对象=用户选定的至少 2 家企业。分值与等级复用 `M_INNOV_RES_CI_LEVEL`（重叠度 ×100，阈值同 `M_INNOV_RES_GRADE`）。

## 计算逻辑说明

选定企业入集。三维：竞争情报等级 / 竞争矩阵 / 战略定位图。重叠度计算同 `M_INNOV_RES_OVERLAP`（IPC / 关键词 / 学者 Jaccard），本指标不另起一套领域维。

### 第一步：入集与重叠度

用户选择至少 2 家存续企业。企业对重叠度、分值、等级同 `M_INNOV_RES_OVERLAP`、`M_INNOV_RES_CI_LEVEL`。

### 第二步：三个子项

1. **竞争情报等级**  
   分值 = overlap ×100；≥P70 高，P30–P70 中，<P30 低（页面可改）。对角（同一企业）分值 100、等级高。

2. **竞争矩阵**  
   行、列均为所选企业，单元格为分值（或等级）。对角=100。

3. **战略定位图**  
   横轴=该企业产出规模（专利去重件数+论文去重件数），纵轴=与其他企业重叠度均值。不另造第三套公式。

输出：企业对清单 + \(n\times n\) 矩阵 + 各企业定位坐标。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 多企业竞争情报比对 | 竞争情报等级 | 企业对重叠度换算后分高/中/低。 | overlap×100；≥P70 高；P30–P70 中；<P30 低 | 同 M_INNOV_RES_OVERLAP — IPC/关键词/学者 Jaccard | 无 |
| 多企业竞争情报比对 | 竞争矩阵 | 所选企业两两分值表。 | n×n 矩阵，对角=100 | 同上企业对结果 — 矩阵 | 无 |
| 多企业竞争情报比对 | 战略定位图 | 规模对平均重叠度的散点。 | 横轴=专利数+论文数；纵轴=平均 overlap | dwd_patent(pn, first_applicant_name, apdt_year) — 专利规模；dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐
- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1]多企业竞争情报比对｜西北工业大学管理学院｜无基金项目资助｜王吉林，刘西林. 构建现代企业竞争情报系统[J]. 情报杂志, 2007(3): 31-33.

[2]多企业竞争情报比对｜上海理工大学管理学院，上海商学院｜国家自然科学基金项目（70472075、70672110）；教育部全国博士点基金项目（20060252004）；上海市重点学科建设项目（T0502）；上海市教育委员会重点科研项目（06ZS103）｜周丹，吴晓伟，徐福缘. 基于企业竞争力综合评价模型的竞争对手分析[J]. 情报杂志, 2008, 27(3): 25-28.

[3]多企业竞争情报比对｜辽宁工业大学经济管理学院｜辽宁省社会科学规划基金项目（L07BJY030）；全国统计科学研究项目（2006C07）｜尹子民，佟会文. 增长率—企业竞争能力战略决策图的研究与应用[J]. 科技管理研究, 2008(8): 186-187+193.

