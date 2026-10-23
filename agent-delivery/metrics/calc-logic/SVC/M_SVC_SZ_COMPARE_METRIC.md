# 城市对比指标值（M_SVC_SZ_COMPARE_METRIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_COMPARE_METRIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_COMPARE_METRIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_COMPARE_METRIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_SZ_COMPARE_METRIC |
| 指标名称 | 城市对比指标值 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构（产业服务链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统·产业服务链分析·深圳对比页对比柱（§1.1.1.2.4.2.7） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_SZ_COMPARE_METRIC.md` |

## 口径定义

「城市对比指标值」不是单一数字，而是「城市 × 小项」的多格面板（3 小项 × 8 行 = 24 格）。24 格里只有「深圳 × orgCount」一格可发布（25,597，与 `M_SVC_PT_SZ_TOTAL` 同数）；外市 orgCount 在同池内可数但池 100% 落广东、北京/上海 0 家；avgTechScore 因模型未签且两子指标分子整列为空而整列不可发布；networkDensity 因无服务机构间边源而整列不可发布。24 格里只有 1 格可发布，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_COMPARE_METRIC.md` §二（M_SVC_SZ_COMPARE_METRIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_invest_info`
- `dwd_org_org_product_info`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三小项 × 多城市的面板里，只有「深圳 × orgCount」一格可发布（25,597，与 M_SVC_PT_SZ_TOTAL 同数）；外市 orgCount 虽在同池内可数，但池 100% 落广东省、北京/上海 0 家，不构成城市基准；avgTechScore 三子指标有两个分子整列为空且模型未签；networkDensity 无服务机构间边源。九格中一格可发布、其余不可，故判部分支持。
- **基期声明**：本件是当期面板（截面），不使用基期年份；技术力若将来解挂，需要三子指标同一年份，而营收/员工最新有值年集中在 2014—2016，年份对齐是解挂前置条件之一。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_SZ_COMPARE_METRIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_COMPARE_METRIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_SZ_COMPARE_METRIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-08-28: 侯佳伟 1B2A3A（仅深圳机构数可跟第 11 条）
- 2026-10-13: 0.2.0 写入真实情况：多格面板、服务机构口径、外市样本+Q-04、技术力/无边源密度；不写死 1355
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

