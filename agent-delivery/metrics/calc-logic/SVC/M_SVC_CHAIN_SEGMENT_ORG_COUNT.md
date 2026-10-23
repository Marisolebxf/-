# 环节服务机构数（M_SVC_CHAIN_SEGMENT_ORG_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-SVC-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_CHAIN_SEGMENT_ORG_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_ORG_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_ORG_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_SVC_CHAIN_SEGMENT_ORG_COUNT |
| 指标名称 | 环节服务机构数 |
| 所属域 | SVC（产业服务链分析） |
| 一级模块 | SVC 服务机构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技专题服务系统·产业服务链分析·全链路可视化（SRS seq 123） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/SVC/M_SVC_CHAIN_SEGMENT_ORG_COUNT.md` |

## 口径定义

六环节计数的「正式口径」依赖一张机构×环节成员表（SVC-P0-3），gkx 与 live 都没有这张表。可执行的替代是「经营范围词表命中」：机构在经营范围里写了某环节的关键词，就认为它在该环节有供给。这是代理，不是事实表——一家机构可能写了但没做，也可能做了但没写。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_CHAIN_SEGMENT_ORG_COUNT.md` §二（M_SVC_CHAIN_SEGMENT_ORG_COUNT.py 零改语义复算）。

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
- **判档理由**：六环节家数可词表代理现转（pool 44,153 家，六环节去重 34,578 家）；正式「机构×环节」成员事实表在 gkx 与 live 均不存在（SVC-P0-3 待供方），正式口径不可执行
- **基期声明**：截面指标：人口与环节计数均为「当前存量」，不含年度分母；库内年度序列 2018—2025 仅用于 §四 的成立年分布披露，不参与计数。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_SVC_CHAIN_SEGMENT_ORG_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_ORG_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_SVC_CHAIN_SEGMENT_ORG_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版
- 2026-10-13: 0.2.0 目标口径锁定（六环节 + 人口 circle + COUNT DISTINCT org）；环节字典与禁止项写死；事实表缺口保留
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

