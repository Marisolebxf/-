# 营收增长率（M_ENT_REVENUE_GROWTH_RATE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REVENUE_GROWTH_RATE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_GROWTH_RATE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_GROWTH_RATE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_REVENUE_GROWTH_RATE |
| 指标名称 | 营收增长率 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业评估／商业力评估 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业详情·营收增长率 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2013] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_REVENUE_GROWTH_RATE.md` |

## 口径定义

gkx 里能算出 **782 个**「企业-年」营收同比，覆盖 **398 家**（占底册 0.2105%），中位数 **9.0409%**；但 2,193 行非空营收里有 **1,411 行**成不了对（上年缺行 373 行、上年为空 1,038 行、上年为 0 行 0 行），且 **96 对**增幅超过 1,000%、**110 对**跌幅超过 90%，绝大多数是「元/万元」混填造成的量级跳变，不是真实增长。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REVENUE_GROWTH_RATE.md` §二（M_ENT_REVENUE_GROWTH_RATE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_report_asset`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：gkx 里能算出 **782 个**「企业-年」营收同比，覆盖 **398 家**（占底册 0.2105%），中位数 **9.0409%**；但 2,193 行非空营收里有 **1,411 行**成不了对（上年缺行 373 行、上年为空 1,038 行、上年为 0 行 0 行），且 **96 对**增幅超过 1,000%、**110 对**跌幅超过 90%，绝大多数是「元/万元」混填造成的量级跳变，不是真实增长。
- **基期声明**：增长率只用「相邻两年」：本年 2014—2025，对应上年 2013—2024。库内财务表更早年份没有成对营收，未按 0 摊入；各年成对数见 by_year，中位数逐年单列

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REVENUE_GROWTH_RATE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_GROWTH_RATE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REVENUE_GROWTH_RATE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

