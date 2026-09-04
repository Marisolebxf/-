# 创新点发现（M_INNOV_POINT_DISCOVERY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_POINT_DISCOVERY |
| 指标名称 | 创新点发现 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

从专利与论文的关键词、IPC 分类中识别近期突现或新出现的创新点，输出候选列表。

## 计算逻辑说明

对关键词与 IPC4 逐年件数做突现检测。输出突现强度、新主题与候选点。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 突现强度 |  | 近窗相对基线的增幅。 | (近3年均值 − 前5年均值) / max(前5年均值, 1) | dwd_patent(pn, keywords, main_classification_ipcr, apdt_year) — 专利关键词,IPC领域,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文,发表年；dwd_en_paper(id, cover_year_start) — 英文论文,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词 |
| 新主题 |  | 是否在近窗首次出现。 | 首次出现年 ≥ T−2 记 1，否则 0 | 同上年序列 — 首次出现年 |
| 候选点 |  | 达标词条列表。 | 突现≥1 或新主题，且近窗件数≥3 | 同上子项计算结果 — 入选与排序 |

## 源表字段

dwd_patent(pn, keywords, main_classification_ipcr, first_applicant_name, apdt_year) — 专利关键词,IPC领域,申请人对齐,申请年；dwd_zh_paper(id, cover_year_start) — 中文论文去重,发表年；dwd_en_paper(id, cover_year_start) — 英文论文去重,发表年；dwd_zh_paper_classification(id, keywords) — 中文论文关键词；dwd_en_paper_classification(id, keywords) — 英文论文关键词；dwd_zh_author(paper_id, institution) — 中文作者单位,空间对齐；dwd_en_author(paper_id, institution) — 英文作者单位,空间对齐；dwd_org_base_info(org_id, name_cn, province, city) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|全球创新监测.md|序号 78「通过算法模型自动发现创新点，用户可查看识别的创新点列表和详细信息」。对象≠技术链热点领域（seq 134）、≠区域综合评价。参考权威机构方案。
