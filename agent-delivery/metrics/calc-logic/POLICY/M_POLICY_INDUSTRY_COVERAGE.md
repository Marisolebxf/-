# 政策产业链覆盖率（M_POLICY_INDUSTRY_COVERAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-POLICY-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_INDUSTRY_COVERAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INDUSTRY_COVERAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INDUSTRY_COVERAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_POLICY_INDUSTRY_COVERAGE |
| 指标名称 | 政策产业链覆盖率 |
| 所属域 | POLICY（政策分析） |
| 一级模块 | 政策 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链政策地图的「节点覆盖」热力、政策分析页的「重点产业链政策覆盖」卡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/POLICY/M_POLICY_INDUSTRY_COVERAGE.md` |

## 口径定义

链路侧结构完整（12 链、1,261 个叶子节点），政策侧结构也完整（`title` 可用），但政策侧四个可匹配字段里三个为空——`keywords`、`keypoints` 全表 0 行，`theme` 只有 2 行。覆盖因此只在标题上发生，且会被 2 字通用名放大。可算，但不能单独作为「产业链政策覆盖」的定论，因此判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_INDUSTRY_COVERAGE.md` §二（M_POLICY_INDUSTRY_COVERAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：链路侧结构完整（12 链、1,261 个叶子节点），政策侧结构也完整（`title` 可用），但政策侧四个可匹配字段里三个为空——`keywords`、`keypoints` 全表 0 行，`theme` 只有 2 行。覆盖因此只在标题上发生，且会被 2 字通用名放大。可算，但不能单独作为「产业链政策覆盖」的定论，因此判**部分支持**。
- **基期声明**：截面指标，覆盖度按库内存量 20,000 条计，不设年度分母。库内 2023—2024 采集断档意味着「当前覆盖」实际停在 2022-08，本件不把它换算成「近年覆盖率」。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_POLICY_INDUSTRY_COVERAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INDUSTRY_COVERAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_POLICY_INDUSTRY_COVERAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

