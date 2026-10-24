# 区域营收（M_CHAIN_REG_REVENUE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_REVENUE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_REVENUE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_REVENUE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_REVENUE |
| 指标名称 | 区域营收 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链分析 → 区域产业指数评价 → 区域产业指数 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2016, 2023, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_REVENUE.md` |

## 口径定义

三段依赖（年报营收 → 链归属 → 城市/上市主体）结构全在真实表白名单，管道当日跑通并产出 12 条链的营收；但**营收字段本身极稀**：12 条链最近一个有正营收的年度合计只有 37 家企业年记录、对应链内企业 6,728 家（覆盖率 **0.55%**），深圳侧只能从上市主体表取到 **15 家**、合计 11.62 亿元，其余 6 条链深圳列为 0 → 结构可算、数据不足，判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_REVENUE.md` §二（M_CHAIN_REG_REVENUE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_stock_finance_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：营收—链—城市三段管道在真实表白名单内跑通，12 条链均有值；但年报营收字段九成以上为空，覆盖企业数远小于链内企业数，只能作「有披露企业营收和」。
- **基期声明**：逐链取该链最近一个有正营收的年度，再跨链求和：9 条链落在 2025、生物医药与智能网联汽车落 2023、低空经济落 2016（该链 2017—2025 全无正营收记录，不按 0 摊、不补插值）。2026 年全库 0 行，未纳入；不做同比、不做 CAGR。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_REVENUE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_REVENUE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_REVENUE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

