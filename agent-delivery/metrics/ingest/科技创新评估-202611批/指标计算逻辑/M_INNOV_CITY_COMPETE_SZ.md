# 深圳科技竞争力（M_INNOV_CITY_COMPETE_SZ）

## 基础信息

| 项目 | 内容 |
| --- | --- |
| 指标ID | M_INNOV_CITY_COMPETE_SZ |
| 指标名称 | 深圳科技竞争力 |
| 使用位置 | 科技信息展示系统 / 科技发展态势 / 深圳创新监测 / 科技发展城市分析展示 |
| 口径版本 | V1.6-20260901 |
| 更新频率 | 待确认（pending） |

## 口径定义

深圳市相对对标城的科技竞争力。对象=深圳。由需求给定三维合成：优势领域、薄弱环节、发展潜力。不另加发展水平维。

## 计算逻辑说明

深圳与对标城入集。采用加权平均，三维：优势领域（区位商>1 的 IPC4 数）/ 薄弱环节（区位商偏低且全域份额高的 IPC4 数）/ 发展潜力（近窗产出增速）。

对标宇宙与 `M_INNOV_CITY_COMPARE_SZ` 相同。领域键 = 专利 `main_classification_ipcr` 前 4 位。

区位商：深圳该 IPC4 专利份额 / 对标宇宙该 IPC4 专利份额。分母为 0 缺测。

1. **优势领域**  
   区位商 > 1 的 IPC4 去重数。

2. **薄弱环节**  
   区位商 < 0.5 且该 IPC4 在对标宇宙专利份额 ≥ 本批中位数的 IPC4 数。

3. **发展潜力**  
   近 3 年（专利+论文）均值相对前 5 年均值的增幅。

三维在本批对标宇宙内极值归一后等权 ×100。输出：深圳一行含三子项原始值与综合分；优势/薄弱 IPC4 清单另表。

| 一级指标 | 二级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- |
| 深圳科技竞争力 | 优势领域 | 相对对标宇宙区位商大于 1 的 IPC4 数。 | COUNT(IPC4 WHERE LQ>1) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — IPC领域,申请人对齐 | 无 |
| 深圳科技竞争力 | 薄弱环节 | 区位商偏低且全域份额高的 IPC4 数。 | COUNT(IPC4 WHERE LQ<0.5 且全域份额≥中位数) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — IPC领域,申请人对齐 | 无 |
| 深圳科技竞争力 | 发展潜力 | 近窗产出相对基线的增幅。 | (近3年均值-前5年均值)/max(前5年均值,1) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 深圳与对标城机构,名称对齐
- dwd_research_institute_base_info(org_id, name_cn, city, province, reg_status) — 科研机构入集
- dwd_forg_base_info(org_id, name_en, name_alias, country, city) — 海外对标机构
- dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位
- dwd_en_author(paper_id, institution) — 英文作者单位

## 待建字段

- 无

## 参考资料

[1] 深圳科技竞争力｜中核工程咨询有限公司｜无基金项目资助｜王铮，孙林，孟春艳. 基于区位熵的关键技术点识别模型[J]. 中国科技资源导刊, 2025, 57(5): 77-86.
