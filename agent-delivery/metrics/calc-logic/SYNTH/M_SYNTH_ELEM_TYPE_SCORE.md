# 七要素类型维得分（M_SYNTH_ELEM_TYPE_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_TYPE_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_ELEM_TYPE_SCORE |
| 指标名称 | 七要素类型维得分 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新要素分析／要素评价模型构建 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_ELEM_TYPE_SCORE.md` |

## 口径定义

维得分是类型指数的中间层，算法只有一步「维内等权平均」，四城 24 个格子都能从面板叶子 z 值直接复算（误差 < 1e-6）。卡住的是覆盖与稳定性：第七维整维空缺，三个维只剩一个叶子，企业维内部次序随叶子取舍翻转。按 §0.1 判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_TYPE_SCORE.md` §二（M_SYNTH_ELEM_TYPE_SCORE.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：七个维里 6 个能出分（企业、政策、服务机构、科研机构、资金、空间），创新人才维整维空缺——研发人员列整列为空、硕博学者四城仅 111 人。6 个有值维的分与其叶子构成都能逐城复算（维得分 = 维内叶子 z 的等权均值，误差 < 1e-6），但每维的叶子覆盖参差（1/3、2/2、1/2、3/3），且空间维与资金维均为代理口径，故判部分支持，不称完全转换支持。
- **基期声明**：维得分是 2024 单年截面的极值归一结果，不是多年均值。min/max 取本批 4 城，换区域集合同一城的分数必变。2021—2023 未入集（单年截面设计），2025/2026 不完整不进分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_ELEM_TYPE_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_ELEM_TYPE_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

