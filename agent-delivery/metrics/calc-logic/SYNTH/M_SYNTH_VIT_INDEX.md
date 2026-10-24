# 区域创新活力指数（M_SYNTH_VIT_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_VIT_INDEX |
| 指标名称 | 区域创新活力指数 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合智能分析／区域创新活力分析／综合评价模型 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024] |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_VIT_INDEX.md` |

## 口径定义

指数三步（极值归一 / 维内加权 / 四维加权）都能落地，四城四维也都有值，所以「能不能算」不是问题；卡住的是**权重从哪来**与**分项齐不齐**：gkx 没有权重表，主口径是按维完整度论证出来的自定义权重（`main_is_official=false`），12 个正本分项缺 3 个。按 §0.1「始终有部分依赖维度无法得到足够数据」判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_INDEX.md` §二（M_SYNTH_VIT_INDEX.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：指数三步（归一 / 维内加权 / 四维加权）都能落地，四城四维都有值；但 12 个正本分项里 3 个四城全缺、人才与政策两维只有一半子维在场，权重没有官方表（自定义 + 熵权对照），且极值归一是四市盘内相对尺度。按 §0.1 判部分支持。
- **基期声明**：统计年 2024；四维时间窗不齐（专利 2024、高被引论文全历史池、政策当前有效集、产品标签当前截面），指数是截面合成而非年度产出
- **复现实测耗时**：约 0.086 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_VIT_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_VIT_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

