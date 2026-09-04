# 监测异常点识别（M_INNOV_FACTOR_ANOMALY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_FACTOR_ANOMALY |
| 指标名称 | 监测异常点识别 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对选定范围内的科创要素监测时序，识别异常点（相对序列中枢的离群期）与突变点（邻期跳变过大的期次）。输出命中的期次与标签。

## 计算逻辑说明

用专利apdt_year、论文cover_year_start、机构/学者存量按年聚合，拼成长度≥8 的监测时序。异常点：默认 MAD（|x−median|/MAD > 3.5）；备选孤立森林。突变点：邻期绝对变化量超过序列 MAD×3 的期次。只输出命中行。

## 源表字段

dwd_patent(pn, apdt_year, first_applicant_name, main_classification_ipcr) — 专利去重,申请年聚合,申请人名称对齐,IPC领域切片
dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年聚合
dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年聚合
dwd_zh_author(paper_id, institution) — 中文作者单位,挂论文与机构对齐
dwd_en_author(paper_id, institution) — 英文作者单位,挂论文与机构对齐
dwd_org_base_info(org_id, name_cn, province, city, org_type, reg_status) — 机构主键,名称对齐,空间过滤,入集
dwd_scholar(scholar_id, paper_nums, citation_nums, h_index, status) — 学者存量,截面离群备选

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技全域态势.md|序号 12「提供异常监测功能，自动识别和标记数据异常点和突变点」。库无监测异常检测专叶，保持 missing。清洗阶段「异常值剔除」不是本核。参考权威机构方案。
