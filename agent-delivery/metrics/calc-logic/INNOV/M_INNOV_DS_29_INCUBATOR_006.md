# 影响力评价（M_INNOV_DS_29_INCUBATOR_006）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_29_INCUBATOR_006 |
| 指标名称 | 影响力评价 |
| 一级模块 | 科技专题服务系统 |
| 二级模块 | 科技专题内容运营中心 |
| 三级模块 | 服务机构管理 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对孵化载体从在孵规模、创新产出、服务能力综合评分，取值 0—100。

## 计算逻辑说明

名称/类型/标签含孵化、众创、加速器。采用加权平均，三维：在孵规模（子公司数）/ 创新产出（载体+子公司专利论文）/ 服务能力（高企覆盖）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 在孵规模 |  | 子公司代理的在孵企业数。 | COUNT(DISTINCT sub_org_id) | dwd_org_subsidiary_info(org_id, sub_org_id, sub_name_cn) — 子公司 |
| 创新产出 |  | 载体与子公司的专利论文。 | COUNT(DISTINCT pn)+COUNT(DISTINCT 论文id) | dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位；dwd_en_author(paper_id, institution) — 英文作者单位 |
| 服务能力 |  | 高企标签覆盖。 | 高企子公司数 + 载体高企标记 | dwd_org_tech_tag(org_id, org_tag) — 高新技术等标签 |

## 源表字段

dwd_org_base_info(org_id, name_cn, city, province, org_type, reg_status) — 孵化载体入集,名称对齐；dwd_org_tech_tag(org_id, org_tag) — 孵化/高新技术标签；dwd_org_subsidiary_info(org_id, sub_org_id, sub_name_cn) — 在孵企业代理；dwd_patent(pn, first_applicant_name, apdt_year) — 专利去重,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

无

## 备注

OPEN draft 身份。05 无孵化载体能级/势能/影响力专叶，不发明 M_*，见 INC-D06 / INC-B01。also_in: DS-04-CARRIER-RANK, DS-06-CARRIER。04-科技专题服务系统 孵化载体影响力（门户内容管理「服务机构」含孵化器），参考权威机构方案。
