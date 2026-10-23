# 技术路径优先级（卡位 × 势头 × 体量）（M_TECH_PATH_PRIORITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PATH_PRIORITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_PRIORITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_PRIORITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_PATH_PRIORITY |
| 指标名称 | 技术路径优先级（卡位 × 势头 × 体量） |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术路径优先级（TOPIC-TECH-05 / DS-02-TECHPATH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_PATH_PRIORITY.md` |

## 口径定义

本件把「先布哪个域」拆成三个 238 点内百分位：**卡位 P**（与关键节点件同一三合一分，40%）、**势头 S**（平滑 CAGR 60% + 2024 同比 40%，35%）、**体量 V**（窗口件数 ln，25%），加权后按 0.75 / 0.55 两条线切三层，得 T1 20 个、T2 70 个、T3 148 个。四套权重情景的 Spearman 最低 0.8875、top20 最小保留 14 个，按自定门禁（tau≥0.90 且 ov≥18 才算完全转换支持）落**部分支持**。关键实测发现是 **P 与 S 的秩相关只有 −0.0899**：卡位与势头几乎正交，所以三因子不是重复计数；但加权后总分与 P 的相关 0.8394、与 V 0.7625、与 S 只有 0.3801，排序仍由卡位与体量主导。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PATH_PRIORITY.md` §二（M_TECH_PATH_PRIORITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件把「先布哪个域」拆成三个 238 点内百分位：**卡位 P**（与关键节点件同一三合一分，40%）、**势头 S**（平滑 CAGR 60% + 2024 同比 40%，35%）、**体量 V**（窗口件数 ln，25%），加权后按 0.75 / 0.55 两条线切三层，得 T1 20 个、T2 70 个、T3 148 个。四套权重情景的 Spearman 最低 0.8875、top20 最小保留 14 个，按自定门禁（tau≥0.90 且 ov≥18 才算完全转换支持）落**部分支持**。关键实测发现是 **P 与 S 的秩相关只有 −0.0899**：卡位与势头几乎正交，所以三因子不是重复计数；但加权后总分与 P 的相关 0.8394、与 V 0.7625、与 S 只有 0.3801，排序仍由卡位与体量主导。
- **基期声明**：势头用 2021→2024 平滑 CAGR 与 2024 同比；2025/2026 不入算（2026 残年）；库内 2017—2020 无专利行，不补零
- **复现实测耗时**：约 6.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_PATH_PRIORITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_PRIORITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_PATH_PRIORITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

