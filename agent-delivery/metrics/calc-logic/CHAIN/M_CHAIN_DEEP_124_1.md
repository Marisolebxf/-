# 产业链关键环节识别模型（M_CHAIN_DEEP_124_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_124_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_124_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_124_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_124_1 |
| 指标名称 | 产业链关键环节识别模型 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链诊断／关键环节识别 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链图谱「关键环节」高亮、链详情页「关键环节 TOP5」列表 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_124_1.md` |

## 口径定义

旧稿的「关键环节」是三层输入：结构（树 + 企业挂接）、效益（环节营收/附加值）、壁垒（环节专利/集中度）。本库第一层完整（1,273 节点、98.21% 企业可解析），第二三层**连表都不存在**（`chain_key_node`、`chain_node_scoring`、`dwd_org_industry_chain_pat_dtl` 四张全 absent）。**结构层可算、效益与壁垒层无源，故判部分支持。**

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_124_1.md` §二（M_CHAIN_DEEP_124_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_industry_chain_pat_dtl`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：节点结构（1,273 个节点、父子关系、企业挂接）完整，可算企业密度、子树规模、度数与层级，12 条链共 1082 个有企业节点全部出关键性排序；但旧稿的高端化指数三因子（环节附加值、技术壁垒、市场集中度）需要环节级营收与环节级专利，gkx 无 dwd_org_industry_chain_pat_dtl、无 chain_key_node 等结果面，财务表也无环节码，故高端化指数空置，只交付结构关键性。
- **基期声明**：截面件，不涉年度序列：节点挂企数是当前快照的单时点计数（2026-10-22 17:55 拉取）。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_124_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_124_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_124_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

