# 政策与条件保障力综合评估（M_INNOV_PG_COMPOSITE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_COMPOSITE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_COMPOSITE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_COMPOSITE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_COMPOSITE |
| 指标名称 | 政策与条件保障力综合评估 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统／科技发展态势／科技创新评估 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 政策保障力综合卡、城市对比条、权重自定义面板 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PG_COMPOSITE.md` |

## 口径定义

在北京市、上海市、深圳市、广州市这四城里，深圳以 **63.4377** 分排第一，北京 **55.6498**、上海 **43.7593**、广州 **8.0386**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_COMPOSITE.md` §二（M_INNOV_PG_COMPOSITE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industrial_fund_basic_info`
- `dwd_org_base_info`
- `dwd_org_stock_finance_info`
- `dwd_patent`
- `dwd_policy_base`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：在北京市、上海市、深圳市、广州市这四城里，深圳以 **63.4377** 分排第一，北京 **55.6498**、上海 **43.7593**、广州 **8.0386**。
- **基期声明**：近窗用 2021—2023（论文语料这三年的城市归属完整）；前窗用 2016—2020 作基线。missing 记 2017—2020 是**专利侧**的事实（apdt_year 这四年零行），故效果维不用专利、只用论文；2024 论文是回填孤峰（32,379 篇 = 32.09%），不摊入任何一年；2025—2026 论文笔数断崖（796/300 篇）亦不入窗。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_COMPOSITE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_COMPOSITE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_COMPOSITE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

