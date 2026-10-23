# 技术–技术关联强度（M_TECH_EDGE_STRENGTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_EDGE_STRENGTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_EDGE_STRENGTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_EDGE_STRENGTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_EDGE_STRENGTH |
| 指标名称 | 技术–技术关联强度 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统 · 技术评估 · 弦线图（线条粗细 = 技术间关联强度） ｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_EDGE_STRENGTH.md` |

## 口径定义

「技术–技术关联强度」在库内**没有结果表**（无「技术关系」「边强度」字段），但依赖侧结构完整：`dwd_patent` 的 `main_classification_ipcr` + `further_classification_ipcr` 可直接构造 IPC4 共类网络——20 万件 PK 分片样本产出 **620 个 IPC4 节点、17,085 个共现对、4,032 条 co≥5 边**（co≥10 为 2,136 条），最大共现 4,376 次，边权 AS 中位 2.487、p90 36.612、跨三个数量级、具充分区分度——**结构与当前数据量均足，现转成立**，按四档口径落 **完全转换支持**（out.json `support_judgment` 同档）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_EDGE_STRENGTH.md` §二（M_TECH_EDGE_STRENGTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_cited`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：「技术–技术关联强度」在库内**没有结果表**（无「技术关系」「边强度」字段），但依赖侧结构完整：`dwd_patent` 的 `main_classification_ipcr` + `further_classification_ipcr` 可直接构造 IPC4 共类网络——20 万件 PK 分片样本产出 **620 个 IPC4 节点、17,085 个共现对、4,032 条 co≥5 边**（co≥10 为 2,136 条），最大共现 4,376 次，边权 AS 中位 2.487、p90 36.612、跨三个数量级、具充分区分度——**结构与当前数据量均足，现转成立**，按四档口径落 **完全转换支持**（out.json `support_judgment` 同档）。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_EDGE_STRENGTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_EDGE_STRENGTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_EDGE_STRENGTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

