# 区域融资（M_CHAIN_REG_FINANCING）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_FINANCING.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_FINANCING.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_FINANCING_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_FINANCING |
| 指标名称 | 区域融资 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 / 区域产业分析 / 区域产业指数评价 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域产业指数页「融资活跃度」格、链详情页「深圳融资强度」小卡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025] |
| 缺失年份 | [2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_FINANCING.md` |

## 口径定义

区域 × 链的事件数与同区域链企业数都能取到，分子分母同母体；但城市只能取登记地、20.63% 的事件匹配不到城市、77.42% 的事件集中在深圳，跨区域比较不可用——**结构可算、数据分布不可比**，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_FINANCING.md` §二（M_CHAIN_REG_FINANCING.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：区域×链强度可算且分子分母同母体，但城市只能取登记地、14.5% 的企业行政区划码映射不到市、融资事件 43.6% 挂不上链、61.5% 集中在深圳——跨区域比较不可用，只能做同城链间比较。
- **基期声明**：本件是截面强度（截至 2025 年末），不按年拆分；2026 年残年事件已剔除，2019 年以前事件保留在分子（累计存量口径），故不与年度增长率混用。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_FINANCING.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_FINANCING.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_FINANCING_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

