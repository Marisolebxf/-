# 研究领域等级划分（M_INNOV_RES_GRADE）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_RES_GRADE |
| 指标名称 | 研究领域等级划分 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 科技发展规划 / 研究领域分析 |
| 口径版本 | V1.5-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

对企业对的研究领域重叠度做高 / 中 / 低分档，可查看划分标准并自定义阈值。对象=企业对。重叠度复用 `M_INNOV_RES_OVERLAP`，不另建等级字段。与 `M_INNOV_RES_CI_LEVEL` 同一套阈值，本号输出分档标准与结果。

## 计算逻辑说明

选定企业入集。复用重叠度，按阈值分档：高 / 中 / 低（默认 P70 / P30，页面可改）。

### 第一步：入集

与 `M_INNOV_RES_OVERLAP` 同一批企业对。先算合成重叠度 \(overlap\in[0,1]\)。本批有效对数 < 3 时不用分位数，改固定阈值 0.5 / 0.2。

### 第二步：分档

默认：本批 \(overlap\) 的第 70、第 30 百分位为 \(t_{\mathrm{high}}\)、\(t_{\mathrm{low}}\)。页面可改成固定阈值，须 \(t_{\mathrm{high}}>t_{\mathrm{low}}\)。

| 条件 | 等级 |
| --- | --- |
| \(overlap\ge t_{\mathrm{high}}\) | 高 |
| \(t_{\mathrm{low}}\le overlap< t_{\mathrm{high}}\) | 中 |
| \(overlap< t_{\mathrm{low}}\) | 低 |

输出：一行一个企业对，含 `overlap`、`grade`、所用 \(t_{\mathrm{high}}\) / \(t_{\mathrm{low}}\)。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 研究领域等级划分 | 重叠度 | 企业对研究领域合成重叠度。 | 复用 M_INNOV_RES_OVERLAP | 同 M_INNOV_RES_OVERLAP — IPC/关键词/学者 Jaccard | 无 |
| 研究领域等级划分 | 等级 | 按阈值把重叠度分成高/中/低。 | ≥P70 高；P30–P70 中；<P30 低（可改） | 本批 overlap 分位或页面阈值 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 企业入集,名称对齐,空间过滤
- dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, further_classification_ipcr, apdt_year) — 专利去重,关键词,申请人对齐,主分类,附加分类,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_paper_classification(id, keywords) — 中文论文关键词
- dwd_en_paper_classification(id, keywords) — 英文论文关键词
- dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐
- dwd_scholar(scholar_id, scholar_org_name_zh, scholar_org_name_en) — 学者所属机构名

## 待建字段

- 无

## 参考资料

[1]研究领域等级划分｜浙江工商职业技术学院，首都经济贸易大学工商管理学院｜国家社会科学基金重大项目（19ZDA077）；浙江省哲社规划项目（15NDJC162YB）｜朱正浩，戚聿东，赵志栋. 技术生态位对企业绩效的影响研究：技术宽度和技术重叠度整合视角[J]. 南方经济, 2021(4): 86-105. DOI: 10.19592/j.cnki.scje.380866.
