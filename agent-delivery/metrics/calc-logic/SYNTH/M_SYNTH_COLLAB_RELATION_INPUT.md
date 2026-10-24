# 协同关系输入统计（M_SYNTH_COLLAB_RELATION_INPUT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SYNTH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_RELATION_INPUT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_RELATION_INPUT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_RELATION_INPUT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SYNTH_COLLAB_RELATION_INPUT |
| 指标名称 | 协同关系输入统计 |
| 所属域 | SYNTH（综合智能分析） |
| 一级模块 | 综合 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SYNTH/M_SYNTH_COLLAB_RELATION_INPUT.md` |

## 口径定义

本指标不做打分，只做「协同关系的输入盘点」：按 calc-logic 0.3.2 的三类关系（联合专利 / 合作项目 / 人才流动），把库内原始表折算成事件级计数，并给出区域切片。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_RELATION_INPUT.md` §二（M_SYNTH_COLLAB_RELATION_INPUT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_applicants`
- `dwd_scholar_paper_relation`
- `dwd_scholar_work_experience`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三类关系中联合专利与人才流动两路可现转（全国事件级 6477 / 18553；四城中可归城事件 122（1.88%）/ 32（0.17%）），但合作项目一路结构性缺失——dwd_zh_project 58453 行中funded_institution 非空 0 行，participating_institution 每项目仅 1 家机构、无参与单位列表字段，无法按『跨 ≥2 机构』成事件；三类口径只能出两类（66.7%），且联合专利一侧用的是 20,000 件抽样表、不是 293.99 万件全量，区域维可归城率不足 2%。按四档定义判部分支持。
- **基期声明**：三类事件都是**全历史累计**口径（专利申请人表无年份字段、任职经历按 start_time 排序但不按年截断、项目表为存量），本指标不做跨年除法，因此没有分母年、也没有缺失年可摊 0。
- **复现实测耗时**：约 0.5 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SYNTH_COLLAB_RELATION_INPUT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_RELATION_INPUT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SYNTH_COLLAB_RELATION_INPUT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

