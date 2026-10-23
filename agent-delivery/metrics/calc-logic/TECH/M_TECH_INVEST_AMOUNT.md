# 技术投入金额（M_TECH_INVEST_AMOUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TECH-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_INVEST_AMOUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_INVEST_AMOUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_INVEST_AMOUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TECH_INVEST_AMOUNT |
| 指标名称 | 技术投入金额 |
| 所属域 | TECH（科技发展态势） |
| 一级模块 | 技术 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·技术投入结构（TOPIC-TECH-05 / DS-02-TECHGRAPH）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/TECH/M_TECH_INVEST_AMOUNT.md` |

## 口径定义

以**深圳上市主体**为唯一金额主体，用 2021—2024 年年报研发费用（784.24 → 1,545.04 亿元）按各主体在 238 个 IPC4 合格域上的专利件数结构分摊，得到域级年度金额合计 **4,039.75 亿元**；非上市企业研发、政府科技专项、基金投资项目金额三项在本库无字段可算（`arch_development_am` 整列为空 0/90,926，基金表只有基金级资本、无项目与 IPC），故按四档口径落**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_INVEST_AMOUNT.md` §二（M_TECH_INVEST_AMOUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industrial_fund_basic_info`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_stock_finance_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：金额侧只有上市主体年报研发费用（深圳 412 家、1,545.04 亿元），非上市企业、政府专项、基金投资项目金额三项缺源：`dwd_org_annual_financial_info` 的`arch_development_am` 整列为空（0/90,926），基金表只有基金级认缴/实缴、无项目级金额与 IPC 字段。故只能交付「上市主体研发费用域级分摊」，不能交付「政府专项+社会资本」全口径技术投入。
- **基期声明**：研发费用缓存覆盖 2007—2025，但专利面板只有 2021—2026（2017—2020 零行），为保证「金额年 × 专利结构年」同窗，只取 2021—2024；2025 有金额但无同窗专利，不进入增速与均值。缺失年不按 0 摊入。
- **复现实测耗时**：约 1.2 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TECH_INVEST_AMOUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_INVEST_AMOUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TECH_INVEST_AMOUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

