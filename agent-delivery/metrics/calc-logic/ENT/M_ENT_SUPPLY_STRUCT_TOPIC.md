# 供应链结构指标（M_ENT_SUPPLY_STRUCT_TOPIC）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SUPPLY_STRUCT_TOPIC.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_STRUCT_TOPIC.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_STRUCT_TOPIC_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_SUPPLY_STRUCT_TOPIC |
| 指标名称 | 供应链结构指标 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 二级模块 | 企业结构 |
| 三级模块 | 供应链结构 |
| 更新频率 | 年 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 无页面挂载（页面引用、seed 未登记）｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_SUPPLY_STRUCT_TOPIC.md` |

## 口径定义

目标口径要的是「谁向谁供货」的有向边及其交易强度，而 gkx 280 张表、6,312 列里没有任何供应边结构；live 唯一同名表 `enterprise_supply_chain` 是 0 行，唯一的近似物 `graph_edge` 只有 152 条 supply 边、145 个节点（底册 189,116 家的 0.08%），且 `relation_type='supply'` 里同时混着 `type=supplier` 与 `type=customer` 两种方向标注。五个子指标一个都算不出，故判 **完全不支持**，`verdict_kind=negative_evidence`。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SUPPLY_STRUCT_TOPIC.md` §二（M_ENT_SUPPLY_STRUCT_TOPIC.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_base_out`
- `dwd_bid_win_candidate_out`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_org_invest_info`
- `dwd_org_invest_info_rows`
- `dwd_org_shareholder_info`
- `dwd_org_shareholder_info_rows`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：目标口径要的是「谁向谁供货」的有向边及其交易强度，而 gkx 280 张表、6,312 列里没有任何供应边结构；live 唯一同名表 `enterprise_supply_chain` 是 0 行，唯一的近似物 `graph_edge` 只有 152 条 supply 边、145 个节点（底册 189,116 家的 0.08%），且 `relation_type='supply'` 里同时混着 `type=supplier` 与 `type=customer` 两种方向标注。五个子指标一个都算不出，故判 **完全不支持**，`verdict_kind=negative_evidence`。
- **基期声明**：本件不进入数值计算，没有年度序列与基期分母；used/missing 为空。这不是「缺年按 0 摊入」，而是供应边这一层在源上不存在。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_SUPPLY_STRUCT_TOPIC.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_STRUCT_TOPIC.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_SUPPLY_STRUCT_TOPIC_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

