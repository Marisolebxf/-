# 关联企业数（M_CHAIN_ENTERPRISE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_ENTERPRISE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_ENTERPRISE_COUNT |
| 指标名称 | 关联企业数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链全景页「链上企业数」计数卡（产业链基础指标模型·「产业企业规模」维） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_ENTERPRISE_COUNT.md` |

## 口径定义

读表面在 gkx 没有对应表，因此不是「完全直接支持」；`gkx.dwd_org_industry_tags`（2,283,762 行、2,283,762 家去重企业）与 `gkx.dwd_industry_chain_info`（1,273 节点、12 条顶层链）结构闭合、当前量足，12 条链当日现算出 **5,450—1,014,992** 家非退化值、挂链覆盖 **2,283,761/2,283,762** 行；但需求把「计算每年企业成立数量 + 环比算增长率」写进同一维度，tags 表无业务统计期字段，唯一可回填年份只能覆盖 **52,621 / 2,464,659 = 2.13%** 的链位 → **截面可交付、年度不可交付**，判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_ENTERPRISE_COUNT.md` §二（M_CHAIN_ENTERPRISE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_tags`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 条顶层链的截面企业数全部可现算且非退化（5,450—1,014,992 家，挂链覆盖 2,283,761/2,283,762 行）；但需求把「计算每年该产业链的企业成立数量、并按环比算增长率」写进同一维度的交付要求，tags 表没有业务统计期字段，唯一可回填年份来自 189,116 行底册的成立年，只能覆盖 52,621 个链—年计位（占 2.13%），年度序列与环比不可交付，故判部分支持。
- **基期声明**：截面存量指标，不设统计期。年度维实测不可用：tags 表无业务统计期字段，底册成立年只能回填 52,621 个链—年计位（2,464,659 个链位的 2.13%），因此不输出年度序列，也不把 2017—2026 中的任何一年按 0 摊进分母；年度件另见 M_CHAIN_ENTERPRISE_NEW_COUNT（其年份同样只能由底册成立年代理）。
- **复现实测耗时**：约 0.01 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_ENTERPRISE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_ENTERPRISE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

