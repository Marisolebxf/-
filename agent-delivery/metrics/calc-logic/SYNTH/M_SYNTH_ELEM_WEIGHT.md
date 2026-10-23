# 类型/层次/领域权重分布（M_SYNTH_ELEM_WEIGHT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_WEIGHT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_WEIGHT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_WEIGHT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_WEIGHT |
| 指标名称 | 类型/层次/领域权重分布 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／要素评价模型构建 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_WEIGHT.md` |

## 口径定义

权重的**算术面**没有障碍：加权和、熵权、弹性、翻转阈值、单纯形扫描五步全部落地，四城 `elem_score` 与 `M_SYNTH_ELEM_INDEX` 逐城一致（差 < 1e-6）。卡住的是**配置面**：gkx 与 live 开发库都没有权重表，calc-logic 把权重写成「可采用等权重，也可根据评估重点自行制定」，等于甲方未定值；上游另标 `is_mock: true`、Q-SYNTH-E-01 仍 🟡。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_WEIGHT.md` §二（M_SYNTH_ELEM_WEIGHT.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：权重的算术部分可算且闭合（三维各 1/3、合计 1，四城 elem_score 与 M_SYNTH_ELEM_INDEX 逐城一致），但权重本身不是甲方标定值：calc-logic 明写「可采用等权重，也可根据评估重点自行制定」，上游另标 is_mock: true、Q-SYNTH-E-01 仍 🟡，且这 1/3 落在的两个维（类型、领域）各自还有整维缺失，故判部分支持——公式能跑，权重没有权威出处。
- **基期声明**：权重是结构性参数，不带年份；被加权的三条维指数都是 2024 单年截面。2021—2023 未入集（本族设计为单年截面），2025/2026 不完整不进分母。权重不随年份重估——若要按年重估熵权，需先把 2021—2023 的叶子补齐。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_WEIGHT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_WEIGHT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_WEIGHT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

