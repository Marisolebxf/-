# 链中角色（M_ENT_SZ_CHAIN_POSITION）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SZ_CHAIN_POSITION.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_CHAIN_POSITION.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_CHAIN_POSITION_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_SZ_CHAIN_POSITION |
| 指标名称 | 链中角色 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳产业链图谱节点着色、企业详情页「链上位置」标签、链招商补链清单 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_SZ_CHAIN_POSITION.md` |

## 口径定义

「链中角色」要回答的是「这家企业在链条的哪一段」。回答它需要两样东西：一张把链环节分成上/中/下游的字典，和一份企业与环节的对应关系。gkx 有链树、有企业产业标签，但**没有官方字典**（`dwd_industry_chain_info` 的 12 条 INB 记录没有 position 列），所以字典由本工程自建（P17）；企业侧有标签但一企多标，去重后的企业级分布只在专利阈值名录上成立。两处都是「能算、但不是官方口径」，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SZ_CHAIN_POSITION.md` §二（M_ENT_SZ_CHAIN_POSITION.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「链中角色」要回答的是「这家企业在链条的哪一段」。回答它需要两样东西：一张把链环节分成上/中/下游的字典，和一份企业与环节的对应关系。gkx 有链树、有企业产业标签，但**没有官方字典**（`dwd_industry_chain_info` 的 12 条 INB 记录没有 position 列），所以字典由本工程自建（P17）；企业侧有标签但一企多标，去重后的企业级分布只在专利阈值名录上成立。两处都是「能算、但不是官方口径」，故判**部分支持**。
- **基期声明**：截面指标（链标签快照 2026-10-21/23），无年度基期；链标签表无打标时间列，不能按年切片。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SZ_CHAIN_POSITION.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_CHAIN_POSITION.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SZ_CHAIN_POSITION_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

