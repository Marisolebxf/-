# 技术创新趋势预测（M_INNOV_TINN_FORECAST）

> 指标最终唯一解释口径（真源）。由王惠调研结果规范化迁移，对齐 metrics/registry/cfg_metric-INNOV-seed.yaml。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_FORECAST |
| 指标名称 | 技术创新趋势预测 |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 科技创新评估 |
| 更新频率 | 待确认（pending） |
| 对齐状态判定 | 待口径确认 |
| 是否在数据库 | 否 |
| 关联Q编号 | GAP-ALGO-TYPE-UNSIGNED |

## 口径定义

对选定领域专利数量、专利质量、技术市场潜力的逐年件数做短期外推，输出点预测与约 80% 区间。

## 计算逻辑说明

按IPC前4位入集技术领域。采用加权平均，三维：专利数量（年申请量）/ 专利质量（年被引）/ 技术市场潜力（年转移）。对逐年件数 Holt 外推，输出点预测与区间。

## 源表字段

dwd_patent(pn, first_applicant_name, main_classification_ipcr, apdt_year) — 专利去重,申请人对齐,IPC领域,申请年；dwd_patent_cited(pn, cited_by_nums) — 专利被引次数；dwd_patent_transfer(pn, transfer_effective_date) — 专利转移,生效日；dwd_org_base_info(org_id, name_cn, city, province, reg_status) — 名称对齐,空间过滤

## 待建字段

无

## 备注

02-科技信息展示系统|科技发展态势|科技创新评估.md|序号 145「基于历史数据和算法模型，预测特定领域技术创新力的未来发展趋势，用户可查看预测结果和置信区间」。详设「趋势预测可 501」=实现通道，未注册；501 pending 不是覆盖证明，差集 missing 保持。参考权威机构方案。
