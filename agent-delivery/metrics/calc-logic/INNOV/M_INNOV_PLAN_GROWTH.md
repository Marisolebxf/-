# 增长速度（M_INNOV_PLAN_GROWTH）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_GROWTH.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_GROWTH.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_GROWTH_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_GROWTH |
| 指标名称 | 增长速度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技发展规划页「全球热点技术捕捉」——热点技术列表及其发展趋势分析 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022] |
| 缺失年份 | [2016, 2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PLAN_GROWTH.md` |

## 口径定义

无「增长速度」现成结果表 → 非完全直接支持；专利表结构与 2021—2024 年数据足量，但王惠原式要求的**前 5 年基线（2016—2020）在专利表中整段缺失**（`apdt_year` 只有 2021—2026），只能降级为 2 年 vs 2 年；论文维被单日回填污染、项目维 2022 起停录 → 三维合成不可交付，判**部分支持**。

## 计算逻辑说明

```text
{'wanghui': 'g=(近3年均值-前5年均值)/max(前5年均值,1)', 'used': 'g=(近窗年均值-基期年均值)/max(基期年均值,1)', 'recent_years': [2023, 2024], 'base_years': [2021, 2022], 'direction_key': 'IPC4（LEFT(main_classification_ipcr,4)）'}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_GROWTH.md` §二（M_INNOV_PLAN_GROWTH.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：专利维可算（258 个方向、中位 −3.20%），但王惠原式的前 5 年基线（2016—2020）在 dwd_patent 整段缺失，只能降级为 2 年对 2 年；论文维单日回填、项目维 2022 起停录，三维合成不可交付
- **基期声明**：王惠原式要求 2016—2020 五年基线；dwd_patent 的 apdt_year 只有 2021—2026，2017—2020 零行、2016 更无。故基期只能取 2021—2022 两年，分母未把缺失年按 0 摊入。
- **复现实测耗时**：约 27.3 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_GROWTH.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_GROWTH.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_GROWTH_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

