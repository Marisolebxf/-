# 技术影响力评估（M_ENT_DS_07_INDUSTRY_POTENTIAL_005）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_07_INDUSTRY_POTENTIAL_005.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_005.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_005_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_07_INDUSTRY_POTENTIAL_005 |
| 指标名称 | 技术影响力评估 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业潜力评估 → 技术影响力雷达图的「被引影响力」轴；SEP 轴置灰并标注「未测」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DS_07_INDUSTRY_POTENTIAL_005.md` |

## 口径定义

被引子项的结构在（`dwd_patent_cited` 有 `pn`、`cited_n`），数据只覆盖 2 万件（0.6803%）；SEP 子项两库连表都没有。一个子项「样本受限」、一个子项「结构缺失」，合成总分不可算，故判**部分支持**，证型 `partial_sample`。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_07_INDUSTRY_POTENTIAL_005.md` §二（M_ENT_DS_07_INDUSTRY_POTENTIAL_005.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_target_item_out`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：被引子项的结构在（`dwd_patent_cited` 有 `pn`、`cited_n`），数据只覆盖 2 万件（0.6803%）；SEP 子项两库连表都没有。一个子项「样本受限」、一个子项「结构缺失」，合成总分不可算，故判**部分支持**，证型 `partial_sample`。
- **基期声明**：截面/存量件：被引次数是截至库内快照的累计值，可回连样本集中在 2021—2023 申请年；不设年度基期，不做跨年 CAGR，不把无被引年份按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_07_INDUSTRY_POTENTIAL_005.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_005.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_005_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

