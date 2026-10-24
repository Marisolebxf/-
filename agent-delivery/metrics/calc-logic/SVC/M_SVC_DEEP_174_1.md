# 金融服务机构技术力评价模型（M_SVC_DEEP_174_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_174_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_174_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_174_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_DEEP_174_1 |
| 指标名称 | 金融服务机构技术力评价模型 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·服务机构技术力评估（SRS seq 121/122） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2026] |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_DEEP_174_1.md` |

## 口径定义

四维里三维有源：资金规模（资产 + 注册资本，覆盖 3,192 家）、资金风险（资产负债率 + 失信处罚，覆盖全池）、服务质量（资讯条数代理，覆盖 2,149 家）。融资成本全库无利率字段，是结构性无源。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_174_1.md` §二（M_SVC_DEEP_174_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_company_punish`
- `dwd_org_important_news_info`
- `dwd_org_invest_info`
- `dwd_org_org_product_info`
- `dwd_org_recruit_info`
- `dwd_org_risk_shixin`
- `dwd_org_shareholder_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：四维中资金规模、资金风险、服务质量三维可现转；融资成本维全库无利率字段、结构性无源（待建 financing_cost_rate），故为部分支持，不抬档
- **基期声明**：财务表实际覆盖 2007—2025 共 19 个年份，used 记整段；每个机构取自己最近一个有财务值的年份作截面，未把缺年按 0 摊入；2026 无财务行，missing 记 2026

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_DEEP_174_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_174_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_DEEP_174_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

