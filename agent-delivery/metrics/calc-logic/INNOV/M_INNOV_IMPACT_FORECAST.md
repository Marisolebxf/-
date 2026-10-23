# 创新影响预测（M_INNOV_IMPACT_FORECAST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_IMPACT_FORECAST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_FORECAST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_FORECAST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_IMPACT_FORECAST |
| 指标名称 | 创新影响预测 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 二级模块 | 科技发展态势 |
| 三级模块 | 全球创新监测 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 实体影响预测卡、贡献度排行 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023] |
| 缺失年份 | [2024] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_IMPACT_FORECAST.md` |

## 口径定义

311 家机构满足「2015—2023 每年都有产出、累计 ≥ 50 篇」，全部拟合成功；2024/2025 两期点预测合计 6,016.4 篇与 6,105.9 篇，2025 年实测 5,384.0 篇，合计高估 **13.41%**；逐家看 MAPE **74.91%**、中位 APE **44.67%**，169 家区间可算者命中 **86.39%**（名义 80%），另 140 家残差 < 5 按正本只出点预测；专利侧 4 点不足 8 期，**明确不发布预测**，只给 2021—2024 动量（+0.324%）。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_IMPACT_FORECAST.md` §二（M_INNOV_IMPACT_FORECAST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：311 家机构满足「2015—2023 每年都有产出、累计 ≥ 50 篇」，全部拟合成功；2024/2025 两期点预测合计 6,016.4 篇与 6,105.9 篇，2025 年实测 5,384.0 篇，合计高估 **13.41%**；逐家看 MAPE **74.91%**、中位 APE **44.67%**，169 家区间可算者命中 **86.39%**（名义 80%），另 140 家残差 < 5 按正本只出点预测；专利侧 4 点不足 8 期，**明确不发布预测**，只给 2021—2024 动量（+0.324%）。
- **基期声明**：2024 论文语料回填孤峰不进入拟合；2025 只作外样本校验；专利 2025/2026 无申请人分年，故专利侧无基线可用。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_IMPACT_FORECAST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_FORECAST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_FORECAST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

