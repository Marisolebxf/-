# 专利质量（M_INNOV_TINN_PATENT_QUALITY）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_PATENT_QUALITY |
| 指标名称 | 专利质量 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按家族规模、权利要求数、被引次数、技术宽度、法律状态稳定性综合评分，取值 0—100。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。采用加权平均，五维：家族规模（other_Versions）/ 权利要求数（claims 项数）/ 被引次数（cited_by_nums）/ 技术宽度（IPC4 去重数）/ 法律状态稳定性（授权且未失效）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 家族规模 |  | 领域专利平均同族成员数。 | 同族成员数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, other_Versions, apdt_year) — 同族专利,IPC领域 |
| 权利要求数 |  | 领域专利平均权利要求项数。 | 权利要求项数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, claims, apdt_year) — 权利要求,IPC领域 |
| 被引次数 |  | 领域专利被后续专利引用的总次数。 | SUM(cited_by_nums) | dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利去重,IPC领域 |
| 技术宽度 |  | 单件专利覆盖的 IPC 小类广度。 | 每件专利 IPC4 去重数合计 / 专利数 | dwd_patent(pn, main_classification_ipcr, further_classification_ipcr, apdt_year) — 主分类,附加分类 |
| 法律状态稳定性 |  | 仍处于授权/有效且未失效的专利占比。 | 稳定专利数 / 专利数 | dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年 |

## 源表字段

dwd_patent(pn, first_applicant_name, main_classification_ipcr, further_classification_ipcr, claims, other_Versions, apdt_year) — 专利去重,申请人对齐,主分类,附加分类,权利要求,同族,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_legal(pn, status, expiration_year) — 专利状态,到期年；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 141「通过引文分析、权利要求分析、家族专利分析等方法，评估专利的技术创新质量和价值……（如被引次数、权利要求数量、家族规模）」。05 无专叶。禁止 96(8) 领先机构/182 高价值专利/186 专利成果质量顶替。参考权威机构方案。
