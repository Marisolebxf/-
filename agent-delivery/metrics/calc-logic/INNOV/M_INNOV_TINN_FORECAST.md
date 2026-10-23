# 技术创新趋势预测（M_INNOV_TINN_FORECAST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_FORECAST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_FORECAST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_FORECAST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_FORECAST |
| 指标名称 | 技术创新趋势预测 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术创新力指标展示页「技术创新趋势预测」卡片（趋势线 + 未来 3 年预测 + 动量榜） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_TINN_FORECAST.md` |

## 口径定义

预测的硬门槛是「每个领域至少 8 个真实年度点」才能拟合 Holt 或做趋势外推；库内专利年度只有 2021—2024 四个真实年（2017—2020 零行、2025/2026 截断），n=4。三维中只有「专利数量」有 IPC4×年序列，年被引 0 个年点（被引表无申请年），年转移只有全域 6 个点、无 IPC4。故**不拟合、不外推**，改交 353 个领域的截面动量（2021→2024 真实增速 + CAGR + 分位），并显式声明不可外推。有数据但不足以支撑「预测」这一动作，故判**部分支持**——不是「完全不支持」，因为动量榜是真实的、可复算的；也不是「完全转换支持」，因为预测本身确实出不来。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_FORECAST.md` §二（M_INNOV_TINN_FORECAST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_family`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：预测的硬门槛是「每个领域至少 8 个真实年度点」才能拟合 Holt 或做趋势外推；库内专利年度只有 2021—2024 四个真实年（2017—2020 零行、2025/2026 截断），n=4。三维中只有「专利数量」有 IPC4×年序列，年被引 0 个年点（被引表无申请年），年转移只有全域 6 个点、无 IPC4。故**不拟合、不外推**，改交 353 个领域的截面动量（2021→2024 真实增速 + CAGR + 分位），并显式声明不可外推。有数据但不足以支撑「预测」这一动作，故判**部分支持**——不是「完全不支持」，因为动量榜是真实的、可复算的；也不是「完全转换支持」，因为预测本身确实出不来。
- **基期声明**：增速分母只取 2021 单年（真实存在）；2017—2020 在库内零行，不按 0 摊入任何均值
- **复现实测耗时**：约 0.1 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_FORECAST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_FORECAST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_FORECAST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

