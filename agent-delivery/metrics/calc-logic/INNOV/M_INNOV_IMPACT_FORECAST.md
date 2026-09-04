# 创新影响预测（M_INNOV_IMPACT_FORECAST）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_IMPACT_FORECAST |
| 指标名称 | 创新影响预测 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对同一套机构与技术领域实体，预测未来产出件数及对同类总体的贡献度。

## 计算逻辑说明

对逐年产出件数做 Holt 外推（满 8 期，年预 2 期）。输出点预测、约 80% 区间与贡献度。

## 源表字段

dwd_org_base_info(org_id, name_cn, province, city) — 机构对齐,空间过滤；dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,机构对齐；dwd_en_author(paper_id, institution) — 英文作者单位,机构对齐

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|全球创新监测.md|序号 71「基于知识图谱和实体节点影响分数，智能预测科技创新对领域创新的积极影响及贡献度，用户可查看预测结果和趋势分析」。招标父句「趋势预测和判断」落本叶。实现通道可 501/pending；未注册不改变差集 missing。参考权威机构方案。
