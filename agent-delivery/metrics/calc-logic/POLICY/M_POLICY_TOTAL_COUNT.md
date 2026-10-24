# 政策总数（M_POLICY_TOTAL_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TOTAL_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TOTAL_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TOTAL_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_TOTAL_COUNT |
| 指标名称 | 政策总数 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技专题服务系统「政策时序分析」总卡片、科技信息展示系统「政策追踪」首页大数字、科技指数页的政策要素规模 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_TOTAL_COUNT.md` |

## 口径定义

「政策总数」就是底表行数：主键 `id` 20,000 行无重复、`is_deleted` 全 0、`COUNT(*)` 与 `COUNT(DISTINCT id)` 相等，**不需要任何外部补数**；库内没有现成汇总表，由一条聚合即可生成，故判**完全转换支持**而不是「完全直接支持」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TOTAL_COUNT.md` §二（M_POLICY_TOTAL_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：底表 gkx.dwd_policy_base 的 COUNT(*) 与 COUNT(DISTINCT id) 都是 20,000，is_deleted 全为 0，主键无重复；层级、省份、城市、类型、年份五条切分口径都能在同一份底数上闭合（层级合计 20,000、省份 17,476+2,524、城市 10,294+9,706）。没有现成汇总表，但结构（主键+分类字段）与数据量都已足够，现在即可转换生成，故判完全转换支持。
- **基期声明**：截面指标：统计库内存量政策总数，不设年度分母、不做年度增速。publish_year 覆盖 1981—2024（非空 19,997 行，缺 3 行），2025/2026 零行；本件不把缺失年份按 0 摊入任何均值。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_TOTAL_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TOTAL_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_TOTAL_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

