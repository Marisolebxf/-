# 政策机遇识别模型（M_POLICY_DEEP_170_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DEEP_170_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_170_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_170_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_DEEP_170_1 |
| 指标名称 | 政策机遇识别模型 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | DS-11-POLICY-EVAL（政策分析评价报告页；算法库模型件） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_DEEP_170_1.md` |

## 口径定义

王惠五子指标中「关键词聚合强度」依赖的 `keywords` 整列为空（0/20,000），「主题密度 / 部门覆盖 / 政策引用 / 发文持续」四个子指标依赖的 `theme` 只有 2 行、`quote_policy` 只有 2 行，导致 20,000 条政策里只有 2 条能进入评分；两个可算维（部门覆盖、发文持续）虽满量，但它们的分组键仍是 `theme`，无主题即无组。故落**部分支持**，不落「完全转换支持」——后者要求「现在就能经转换得到」，而本件的核心分组键不是转换能补出来的，是要补采/补标的数据。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DEEP_170_1.md` §二（M_POLICY_DEEP_170_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠五子指标中关键词聚合强度整列无值（keywords 0/20,000）；主题密度、部门覆盖、政策引用、发文持续性四个子指标只对 2 条政策有值，20,000 条里 19,998 条因 theme 缺失无法分组 → 有必需子指标始终无法取值，判部分支持。
- **基期声明**：本指标为截面评分，不设跨年基期，故 used/missing 均为空。publish_year 仅用于「发文持续性」的连续年计数（两条 theme 政策分别为 2015、2010 年），不进入任何增长率分母。政策表 2022 年后为采集残片（2023 年 0 行），任何年度趋势都不做外推。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_DEEP_170_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_170_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_DEEP_170_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

