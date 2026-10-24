# 研发投入占比（M_ENT_RD_INVESTMENT_RATIO）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RD_INVESTMENT_RATIO.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RD_INVESTMENT_RATIO.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RD_INVESTMENT_RATIO_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_RD_INVESTMENT_RATIO |
| 指标名称 | 研发投入占比 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题·企业评估·技术力评估「技术投入」维；企业画像与门户「技术优势可视化」看板｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_RD_INVESTMENT_RATIO.md` |

## 口径定义

`enterprise_base.rd_investment_ratio` 与 `enterprise_finance_history.rd_investment` **结构全在**（含分子 `arch_development_am`、分母 `operating_revenue`、研发人员数 `development_employee` 三列），但 2026-10-21 实测 gkx 年报表 90,926 行中**研发投入有效填充 0 行、研发人员有效填充 0 行**——分子恒空、成对可算 0 企，按 §〇 归**部分支持**（值缺失型，灌数即通；不是结构缺失，也不是方法不可行）。

## 计算逻辑说明

```text
rd_ratio = rd_investment / revenue × 100；每企最近完整自然年；分母 0/空或分子空 → 该企不可算
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RD_INVESTMENT_RATIO.md` §二（M_ENT_RD_INVESTMENT_RATIO.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_foreign_org_annual_financial_info`
- `dwd_org_annual_financial_info`
- `dwd_org_stock_finance_info`
- `dwd_rd`
- `dwd_rd_probe`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：公式与源字段均已闭合（arch_development_am / operating_revenue / year 三列齐备），但研发投入列在全库为空：ODS 年报财务 90,926 行填充 0、工商年报资产表 527,034 行填充 0、DWD 财务年表 80,531 行填充 0。唯一有研发费用的上市财务表被口径明令禁止替代年报，且仅覆盖约 0.5% 底册。属「结构与公式齐、值侧为空」的值缺失，按 §〇「始终有部分依赖维度得不到足够数据」判部分支持；灌入真实研发投入后即可现算，方法无需改造。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_RD_INVESTMENT_RATIO.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RD_INVESTMENT_RATIO.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_RD_INVESTMENT_RATIO_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

