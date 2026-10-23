# M_TALENT_DEEP_159_1（M_TALENT_DEEP_159_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_159_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_159_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_159_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DEEP_159_1 |
| 指标名称 | M_TALENT_DEEP_159_1 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 人才洞察页「深圳 vs 京沪画像 + 20+8 优势/短板（LQ）」 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DEEP_159_1.md` |

## 口径定义

五维画像（规模/影响力/产出/顶才/帽子）在 `dwd_scholar` 21,316 行上可全量现转，领域维可用 13,955 名双锚定学者的 20+8 簇归属算区位商，优势/短板骨架成立；但需求点名的技能匹配度、招聘难度、薪资水平、发展前景四项市场供需维在库内完全无源（`dwd_job` 仅 10 行、无薪资字段），且深圳可判簇学者只有 100 人，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_159_1.md` §二（M_TALENT_DEEP_159_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_job`
- `dwd_org_annual_financial_info`
- `dwd_org_recruit_info`
- `dwd_scholar`
- `dwd_scholar_talent_flag`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：学者画像五维（规模/影响力/产出/顶才/帽子）在 gkx.dwd_scholar 21,316 行上可全量现转，领域维可用 13,955 名学者的双锚定论文判簇、按区位商给出优势/短板，诊断骨架成立；但需求点名的技能匹配度、招聘难度、薪资水平、发展前景四项市场供需维在库内完全无源（dwd_job 仅 10 行、无薪资字段），对标口径也只有学者库（全国样本实为都市圈 + 京沪）→ 部分支持。
- **基期声明**：截面口径：五维画像取三列生涯累计值（h / citation_nums / paper_nums），领域维取双锚定论文全时段（不做年度截断），因此无基期与增速。刻意不构造「近 N 年」窗口，避免把 2024 年的采集堆积读成增长（见 158 的年度分布）。
- **复现实测耗时**：约 14.1 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DEEP_159_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_159_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DEEP_159_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

