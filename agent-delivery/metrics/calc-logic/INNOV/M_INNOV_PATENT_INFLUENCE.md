# 专利影响力（M_INNOV_PATENT_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PATENT_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PATENT_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PATENT_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PATENT_INFLUENCE |
| 指标名称 | 专利影响力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | DS-01 科技全域态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 科创要素（专利详情页属性） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PATENT_INFLUENCE.md` |

## 口径定义

王惠口径的两维中，**价值维有 199.5 万件非空（填充 67.85%）、被引维只有 2 万件**；而被引副表与本库 294 万件专利语料按 `pn` 只能对上 **355 件（1.77%）**，价值维在副表里没有对应列、无法按 `pn` 连接。权重 0.80 的主维只能在 0.68% 的样本上出分，且这 2 万件几乎没有题录（申请人、年份、城市要靠哈希 join 才能补到 355 件），故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PATENT_INFLUENCE.md` §二（M_INNOV_PATENT_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_family`
- `dwd_patent_inventors`
- `dwd_patent_legal`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：王惠口径的两维中，**价值维有 199.5 万件非空（填充 67.85%）、被引维只有 2 万件**；而被引副表与本库 294 万件专利语料按 `pn` 只能对上 **355 件（1.77%）**，价值维在副表里没有对应列、无法按 `pn` 连接。权重 0.80 的主维只能在 0.68% 的样本上出分，且这 2 万件几乎没有题录（申请人、年份、城市要靠哈希 join 才能补到 355 件），故判**部分支持**。
- **基期声明**：dwd_patent 的 apdt_year 只有 2021—2026（2017—2020 零行）；被引样本能挂到年份的只有 2021—2023 三年（237/111/12 件），2024—2026 挂接为 0。任何「前 N 年基线」在专利侧只能用 2021—2023，不得把缺失年按 0 摊进分母。
- **复现实测耗时**：约 3.5 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PATENT_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PATENT_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PATENT_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

