# 创新影响预测（M_INNOV_DS_04_REALTIME_005）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_REALTIME_005.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_REALTIME_005.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_REALTIME_005_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_04_REALTIME_005 |
| 指标名称 | 创新影响预测 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技发展态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 全球创新监测 → 创新监测与分析 → 创新影响（**预测视图**） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_04_REALTIME_005.md` |

## 口径定义

对同一套机构/领域实体的逐年产出件数做 Holt 线性指数平滑外推（α=0.5、β=0.3、满 8 期、年预 2 期），输出点预测、约 80% 区间与贡献度。

> 一句话口径（源件 §0.3）：结构上，训练序列所需的一切都在：`dwd_patent.apdt_year` 有年份、`main_classification_ipcr` 有 IPC、`applicants` 有申请人，634 个领域 × 6 年、6,958 个机构 × 4 年的逐年件数都能逐条复核。但**数据量不够做外推**：完整年只有 2021、2022、2023、2024 四期，Holt 门槛要 8 期。缺口不是「没采集」，而是源表年份就没有——2017—2020 在 `apdt_year` 上**零行**（DATA_FACTS §3.16），2025 只到四年均值的 72.65%（公开滞后），2026 是残年（12.34%）。按 §〇 定义，「始终有部分依赖维度无法得到足够数据」成立，判**部分支持**，不判完全转换支持。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_REALTIME_005.md` §二（M_INNOV_DS_04_REALTIME_005.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：结构上，训练序列所需的一切都在：`dwd_patent.apdt_year` 有年份、`main_classification_ipcr` 有 IPC、`applicants` 有申请人，634 个领域 × 6 年、6,958 个机构 × 4 年的逐年件数都能逐条复核。但**数据量不够做外推**：完整年只有 2021、2022、2023、2024 四期，Holt 门槛要 8 期。缺口不是「没采集」，而是源表年份就没有——2017—2020 在 `apdt_year` 上**零行**（DATA_FACTS §3.16），2025 只到四年均值的 72.65%（公开滞后），2026 是残年（12.34%）。按 §〇 定义，「始终有部分依赖维度无法得到足够数据」成立，判**部分支持**，不判完全转换支持。
- **基期声明**：本件的「基期」是训练期：库内完整年只有 2021—2024 四期，公式要 8 期；2017—2020 在 dwd_patent.apdt_year 上零行，2025 含公开滞后、2026 为残年，均不进训练。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_04_REALTIME_005.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_REALTIME_005.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_04_REALTIME_005_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

