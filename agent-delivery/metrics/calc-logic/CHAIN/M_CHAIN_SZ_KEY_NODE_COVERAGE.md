# 深圳关键环节覆盖率（M_CHAIN_SZ_KEY_NODE_COVERAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_KEY_NODE_COVERAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_KEY_NODE_COVERAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_KEY_NODE_COVERAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_KEY_NODE_COVERAGE |
| 指标名称 | 深圳关键环节覆盖率 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／深圳产业发展分析／补链强链 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳产业链页「关键环节覆盖率」卡与链级缺口清单 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SZ_KEY_NODE_COVERAGE.md` |

## 口径定义

链树、企业挂链、深圳判定三段都能在 gkx 闭合，覆盖率的分子分母逐位可复算；但「关键」的定义依赖 `importance_level` 值集，该列在 gkx 不存在，只能用全国中位数分位代理，且原口径要求折 L1 后比率恒 100%，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_KEY_NODE_COVERAGE.md` §二（M_CHAIN_SZ_KEY_NODE_COVERAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：覆盖率的分子分母都能在同一条链树上闭合：954 个叶级环节、463 个按全国中位数门槛判定的关键叶、其中 411 个有深圳企业（88.77%），与已交付 M_CHAIN_SZ_KEY_NODE_COUNT 的411/463 逐位一致。但 calc-logic 的『关键』由 importance_level 值集定义，该列在 gkx 不存在（GAP-CHAIN-IMPORTANCE-ENUM 未签），本件只能用全国中位数分位代理；且 calc-logic 要求折 L1，41 个 L1 节点上关键集 25/25 全被覆盖，比率恒为 100%、零区分度。关键定义依赖外部标注，故判部分支持。
- **基期声明**：本件是截面指标：链树与挂链桥都是当日快照，口径内没有年度序列，不涉及基期分母，故 used/missing 为空。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_KEY_NODE_COVERAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_KEY_NODE_COVERAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_KEY_NODE_COVERAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

