# 明星企业研发投入占比（M_ENT_STAR_RD_RATIO）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_RD_RATIO.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_RD_RATIO.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_RD_RATIO_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_STAR_RD_RATIO |
| 指标名称 | 明星企业研发投入占比 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／创新能力／投入强度 |
| 更新频率 | 季 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 明星企业榜·研发强度列｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | ["2025"] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_STAR_RD_RATIO.md` |

## 口径定义

明星名单 4,561 家（专利授权 ≥50 且剔除非企业主体，阈值本件自定义）；研发投入取利润表 `yffy` 或上市财务 `research_development_amount`，590 家有值（12.9358%），583 个有效比值，中位数 **6.0487%**、P25 4.13%、P75 9.75%、合计口径 **4.9589%**（研发投入合计 60,870,549,414.19 元 / 营收合计 1,227,495,552,754.53 元）。另给 2025 年报子集（120 家，中位数 5.6828%）作为口径敏感性对照。判部分支持，缺口是 3,971 家无财报。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_RD_RATIO.md` §二（M_ENT_STAR_RD_RATIO.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_annual_report_asset`
- `dwd_org_base_info`
- `dwd_org_income_statement`
- `dwd_org_stock_finance_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：研发投入只剩「上市/发债主体财报」一条腿：calc-logic 首选年报口径 arch_development_am 在 90,926 行中非空 0 行，工商年报 yftrje 在 527,034 行中非空 0 行，均整列为空；可用的是 dwd_org_income_statement.yffy 与 dwd_org_stock_finance_info，覆盖 4,561 家明星企业中的 590 家（12.9358%）。有真数、可算比值，但八成以上明星企业（多为非上市）无研发投入披露，故判部分支持。
- **基期声明**：主口径是「每企最新一期」截面（期别分布见 probes.period_mix，最新期多为 2026Q1/2025 年报），不构成统一基期；为可比性另给 annual_2025 子集（120 家有效）。income_statement 的 hjnd 覆盖 38 个年度，但 2017 年前研发费用行基本缺失，故不做跨年序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_STAR_RD_RATIO.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_RD_RATIO.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_STAR_RD_RATIO_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

