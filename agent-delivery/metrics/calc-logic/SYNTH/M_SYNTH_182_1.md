# 区域科技创新成果综合评价模型（M_SYNTH_182_1）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-SYNTH-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_182_1 |
| 指标名称 | 区域科技创新成果综合评价模型 |
| 一级模块 | 综合智能分析 |
| 二级模块 | 区域创新活力分析 |
| 三级模块 | 科技创新成果 |
| 更新频率 | 年度 |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

选定区域内、统计年度的科技创新成果指数，从基础科学、应用科技、科研机构三维评定，取值 0—100。分数越高表示科技成果水平越强。对象=区域科技成果，不是单篇论文、不是企业技术力。

本版不进分：重大科学发现、技术成熟度、研究人员结构、国际合作、科研平台。算法库原文有这五项，现表算不了或不进本指数，也不再挂待建。

## 计算逻辑说明

采用加权平均。三维：基础科学 / 应用科技 / 科研机构。算法库序号 182 已给这三维，不另起维度。各维极值归一后等权（也可按评估重点改权，ΣW=1）。

### 第一步：入集

统计窗默认自然年。区域落到 `dwd_org_base_info.city` / `province` / `area`。存续：`reg_status` 含「存续」。专利第一申请人、论文作者单位对齐 `name_cn` 后入该区域。论文年键=`cover_year_start`，专利年键=`pbdt_year`（授权看 `granted_number` 非空）。本批=同一次评估窗口内全部对比区域。

### 第二步：三个子项

1. **基础科学**  
   高质量论文 + 被引影响力。高质量论文口径：被引 ≥ 本批 P70 的论文去重数。中文被引用 `dwd_zh_paper_citation.citation_num`，英文 `dwd_en_paper_reference.citation_count`；无被引行当 0，不进 P70 分子。被引影响力=区域论文被引合计。两子值分别极值归一后等权。

2. **应用科技**  
   高价值专利 + 专利转移。高价值专利=发明授权且 `dwd_patent.value` ≥ 本批 P70（`value` 空不进分位、不算高价值）。专利转移去重数即产业化应用，年键=`transfer_effective_date` 的年。两子值分别极值归一后等权。

3. **科研机构**  
   科研机构存量 + 成果转化率。存量=`dwd_research_institute_base_info` 区域内去重数。成果转化率=机构对齐专利转移去重数 ÷ 机构对齐发明授权去重数。分母为 0 则本子项记空、不进该维。两子值分别极值归一后等权。

维内子项先归一再等权得维得分，三维再等权得指数。输出区域一行，含三维得分与综合分。

| 一级指标 | 二级指标 | 三级指标 | 指标说明 | 计算公式 | 源表字段 | 待建字段 |
| --- | --- | --- | --- | --- | --- | --- |
| 区域科技创新成果综合评价模型 | 基础科学 | 高质量论文 | 被引≥本批P70的论文去重数。 | COUNT(DISTINCT paper \| citation≥P70) | dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_zh_paper_citation(id, citation_num) — 中文被引；dwd_en_paper_reference(id, citation_count) — 英文被引；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 被引影响力 | 区域论文被引合计。 | SUM(citation) | dwd_zh_paper_citation(id, citation_num) — 中文被引；dwd_en_paper_reference(id, citation_count) — 英文被引；dwd_zh_paper(id, cover_year_start) — 中文论文；dwd_en_paper(id, cover_year_start) — 英文论文；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域科技创新成果综合评价模型 | 应用科技 | 高价值专利 | 发明授权且专利价值≥本批P70。 | COUNT(DISTINCT 发明授权 \| value≥P70) | dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year, value) — 发明授权,专利价值,申请人对齐,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 专利转移量 | 专利转移去重数，即产业化应用。 | COUNT(DISTINCT 转移专利) | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 授权专利,申请人对齐,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
| 区域科技创新成果综合评价模型 | 科研机构 | 科研机构存量 | 区域内科研机构去重数。 | COUNT(DISTINCT 科研机构) | dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |
|  |  | 成果转化率 | 科研机构对齐的专利转移数 ÷ 发明授权数。 | 机构转移数/机构发明授权数 | dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移；dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year) — 发明授权,申请人对齐,年窗；dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续 | 无 |

## 源表字段

- dwd_org_base_info(org_id, name_cn, city, province, area, org_type, reg_status) — 区域入集,名称对齐,机构类型,存续
- dwd_research_institute_base_info(org_id, city, org_type, name_cn) — 科研机构入集
- dwd_patent(pn, kind, granted_number, first_applicant_name, pbdt_year, value) — 发明授权,专利价值,申请人对齐,年窗
- dwd_patent_transfer(pn, transfer_effective_date) — 专利转移
- dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年
- dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年
- dwd_zh_author(paper_id, institution) — 中文作者单位,区域对齐
- dwd_en_author(paper_id, institution) — 英文作者单位,区域对齐
- dwd_zh_paper_citation(id, citation_num) — 中文被引
- dwd_en_paper_reference(id, citation_count) — 英文被引

## 待建字段

- 无
