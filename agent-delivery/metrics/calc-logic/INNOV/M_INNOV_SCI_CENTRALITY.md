# 科学网络中心性（M_INNOV_SCI_CENTRALITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCI_CENTRALITY |
| 指标名称 | 科学网络中心性 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | — |

## 口径定义

科学合作网络中学者或研究机构的度中心性、接近中心性、中介中心性，并给出排名。对象=作者单位或作者姓名。三类中心性共核一条 ID。不建引文网络。

## 计算逻辑说明

按题名关键词入集领域论文。三维：度中心性（合作邻居）/ 接近中心性（归一化度）/ 中介中心性（跨机构合写）。本批节点内极值归一后排名。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 度中心性 |  | 合作邻居去重数。 | COUNT(DISTINCT 邻居) | dwd_zh_author(paper_id, institution, zh_name) — 中文作者单位,姓名；dwd_en_author(paper_id, institution, zh_name) — 英文作者单位,姓名 |
| 接近中心性 |  | 归一化度。 | 度数 / (本批节点数-1) | 同上合作图 — 归一化度 |
| 中介中心性 |  | 出现在不少于 3 个节点的合写论文数。 | COUNT(DISTINCT 论文id WHERE 节点数≥3) | dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文 |

## 源表字段

dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文去重,题名入集,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文去重,题名入集,发表年；dwd_zh_author(paper_id, institution, zh_name) — 中文作者单位,姓名；dwd_en_author(paper_id, institution, zh_name) — 英文作者单位,姓名

## 待建字段

无

## 备注

依照需求文档构建。02-科技信息展示系统|科技发展态势|科技创新评估.md|科学网络中心性评估 · 序号 137(包括度中心性、接近中心性、中介中心性)
