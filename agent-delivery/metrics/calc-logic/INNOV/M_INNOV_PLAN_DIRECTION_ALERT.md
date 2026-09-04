# 潜在科技发展方向预警（M_INNOV_PLAN_DIRECTION_ALERT）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_DIRECTION_ALERT |
| 指标名称 | 潜在科技发展方向预警 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技发展规划 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按 IPC 前 4 位监测潜在方向并预警。方向主键就是 IPC4。六源近窗相对基线增速加权得 F。

## 计算逻辑说明

按 IPC 前 4 位入集。采用加权平均，六维：专利 / 论文 / 项目 / 人才 / 产业 / 政策（各源近窗相对基线增速）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 专利 |  | 该 IPC4 申请量近窗相对基线增速。 | g=(近窗均值-基线均值)/max(基线均值,1) | dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,IPC领域,申请年 |
| 论文 |  | 关键词命中该方向的论文量增速。 | g=(近窗均值-基线均值)/max(基线均值,1) | dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词 |
| 项目 |  | 关键词或学科命中该方向的立项量增速。 | g=(近窗均值-基线均值)/max(基线均值,1) | dwd_zh_project(id, keywords, discipline, approval_year) — 项目关键词,学科,立项年 |
| 人才 |  | 研究方向命中该方向的发文学者数增速。 | g=(近窗均值-基线均值)/max(基线均值,1) | dwd_scholar_research_direction(scholar_id, fields) — 学者研究方向；dwd_scholar_paper_relation(scholar_id, year) — 学者发文年 |
| 产业 |  | 该 IPC4 活跃申请机构数增速。 | g=(近窗均值-基线均值)/max(基线均值,1) | dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 申请人对齐,IPC领域；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤 |
| 政策 |  | 主题或关键词命中该方向的政策量增速。 | g=(近窗均值-基线均值)/max(基线均值,1) | dwd_policy_base(id, keywords, theme, keypoints, publish_year, city, province) — 政策关键词,主题,要点,发布年,空间 |
| 预警等级 |  | 融合强度叠加多源同向。 | F≥1且两源g>0为2；F≥0.5为1；否则0 | 上六源 g 加权得 F |

## 源表字段

dwd_patent(pn, keywords, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,关键词袋,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文关键词；dwd_en_paper_classification(id, keywords) — 英文关键词；dwd_zh_project(id, keywords, discipline, approval_year) — 项目关键词,学科,立项年；dwd_scholar_research_direction(scholar_id, fields) — 学者研究方向；dwd_scholar_paper_relation(scholar_id, year) — 学者发文年；dwd_policy_base(id, keywords, theme, keypoints, publish_year, city, province) — 政策关键词,主题,要点,发布年,空间；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技发展规划.md|序号 184「结合论文、专利、项目、人才、产业和政策等多源数据，对潜在科技发展方向进行持续监测与预警分析」。招标父句「潜在的科技发展方向预警」收口本叶。对象≠134 已识别热点趋势预测。参考权威机构方案。
