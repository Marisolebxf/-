# 覆盖领域数（M_ENT_DOMAIN_COVERAGE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_COVERAGE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DOMAIN_COVERAGE_COUNT |
| 指标名称 | 覆盖领域数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 二级模块 | 重点企业领域分布分析 |
| 三级模块 | 领域分布分析 |
| 更新频率 | 领域标签更新后 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业分析·领域分布分析「覆盖领域数」卡｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DOMAIN_COVERAGE_COUNT.md` |

## 口径定义

按 2026-08-27 锁定的 15 集群口径，本指标不可算——`industry_cluster` 与 `industry_cluster_map` 在 gkx 280 表与 live 259 表中都不存在；按 12 条产业链根码代理可算，1,714,457 家去脏链属企业覆盖 12 条链，但**链不是集群**，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_COVERAGE_COUNT.md` §二（M_ENT_DOMAIN_COVERAGE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_tech_tag`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：按 2026-08-27 锁定的 15 集群口径，本指标不可算——`industry_cluster` 与 `industry_cluster_map` 在 gkx 280 表与 live 259 表中都不存在；按 12 条产业链根码代理可算，1,714,457 家去脏链属企业覆盖 12 条链，但**链不是集群**，故判 **部分支持**。
- **基期声明**：本件是截面计数：链归属表无 stat_year 字段，输出的是当日快照上的集合覆盖数，不存在年度分母，故 used/missing 为空；不是把缺年按 0 摊入。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DOMAIN_COVERAGE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DOMAIN_COVERAGE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

