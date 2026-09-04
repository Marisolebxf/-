# 科学创造力趋势预测（M_INNOV_SCI_FORECAST）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCI_FORECAST |
| 指标名称 | 科学创造力趋势预测 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对选定领域论文数量、网络中心性、科学研究前沿性的逐年件数做短期外推，输出点预测与约 80% 区间。

## 计算逻辑说明

按题名关键词入集领域论文。采用加权平均，三维：论文数量（中英论文）/ 网络中心性（作者单位去重）/ 科学研究前沿性（当年新单位）。对逐年件数 Holt 外推，输出点预测与区间。

## 源表字段

dwd_zh_paper(id, zh_name, en_name, cover_year_start) — 中文论文去重,题名入集,发表年；dwd_en_paper(id, zh_name, en_name, cover_year_start) — 英文论文去重,题名入集,发表年；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

OPEN draft 身份，口径/计算逻辑对齐正式指标 M_INNOV_SCI_FORECAST（科学创造力趋势预测）。05 无科学创造力趋势预测专叶。见 SCI-D04。统计窗口与对象范围待 T0-X 核对；公式与 algorithm_type 未签。
