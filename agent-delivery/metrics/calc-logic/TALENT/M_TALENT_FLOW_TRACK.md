# M_TALENT_FLOW_TRACK（M_TALENT_FLOW_TRACK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_FLOW_TRACK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_FLOW_TRACK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_FLOW_TRACK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_FLOW_TRACK |
| 指标名称 | M_TALENT_FLOW_TRACK |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技人才态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [1990, 2026] |
| 缺失年份 | [2021, 2022, 2023] |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_FLOW_TRACK.md` |

## 口径定义

旧稿把"流动"等同于"换单位"，未区分同机构晋升与真流动，也未处理并行任职；分母在"有履历人数"与"全库人数"之间来回切。本件固定三个分母并全程标注：

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_FLOW_TRACK.md` §二（M_TALENT_FLOW_TRACK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：旧稿把"流动"等同于"换单位"，未区分同机构晋升与真流动，也未处理并行任职；分母在"有履历人数"与"全库人数"之间来回切。本件固定三个分母并全程标注：
- **基期声明**：履历起止年覆盖 1950s—2026，但招聘/流动的宏观基期（2021—2023 三年对比）没有同期快照；本件只做「全历史轨迹」一张截面，不做逐年净流入率。「止年空」一律按 2026（当前）处理，会低估 2026 年之后的流出

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_FLOW_TRACK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_FLOW_TRACK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_FLOW_TRACK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

