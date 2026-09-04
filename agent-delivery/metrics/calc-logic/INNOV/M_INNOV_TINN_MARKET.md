# 技术市场潜力（M_INNOV_TINN_MARKET）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_MARKET |
| 指标名称 | 技术市场潜力 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

按转让、许可、诉讼、质押、开放许可综合评分，取值 0—100。不另建许可/诉讼/质押专表。

## 计算逻辑说明

按 IPC 前 4 位入集技术领域。采用加权平均，五维：转让（转移专利/专利）/ 许可 / 诉讼 / 质押 / 开放许可（后四项由 legal_events 解析）。

| 指标二级 | 指标三级 | 口径定义 | 计算逻辑 | 源表字段 |
|---|---|---|---|---|
| 转让 |  | 发生权利转移的专利占比。 | 转移专利数 / 专利数 | dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent(pn, main_classification_ipcr, apdt_year) — 专利分母,IPC领域 |
| 许可 |  | 实施许可（不含开放许可）的专利占比。 | 许可专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |
| 诉讼 |  | 涉及诉讼或无效宣告的专利占比。 | 诉讼专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |
| 质押 |  | 发生质押登记的专利占比。 | 质押专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |
| 开放许可 |  | 声明开放许可的专利占比。 | 开放许可专利数 / 专利数 | dwd_patent_legal(pn, legal_events) — 法律事件 |

## 源表字段

dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_patent_legal(pn, legal_events) — 法律事件（许可,诉讼,质押,开放许可）；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 142「基于专利转让、许可、诉讼等市场活动数据，分析技术的市场潜力和商业化价值……（技术市场活跃度、技术成熟度、商业化前景）」。对照 seq 135 实现类（专题已 third_party 同叶）。本页不跑 TOPIC-TECH Job、不伪展开三维加权。参考权威机构方案。
