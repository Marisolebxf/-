# 上游环节数（M_CHAIN_UPSTREAM_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_UPSTREAM_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_UPSTREAM_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_UPSTREAM_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_UPSTREAM_COUNT |
| 指标名称 | 上游环节数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链全景／链条结构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链图谱「上游」段着色计数、链详情页结构卡片 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_UPSTREAM_COUNT.md` |

## 口径定义

每条产业链取 L1 中编码最小的一支为首段分支，统计该分支下全部节点（含 L1 自身、容器与叶子都计 1），12 条链求和。编码序位是代理，不等于官方 chain_stage='upstream'。

> 一句话口径（源件 §0.3）：「上游环节」需要两样东西：**阶段标注**（哪些节点是上游）与**环节清单**（这些节点有多少个）。清单在 `gkx.dwd_industry_chain_info` 完整（1,273 节点），阶段标注**完全没有**——16 列里没有 `chain_stage`，唯一可能承载层级的 `level` 全表恒为 0。本件用「编码序位」代理阶段，等于用结构假设换掉语义字段，因此判 **部分支持**。

## 计算逻辑说明

```text
Upstream = Σ_k |{c ∈ C : code(c) 以 code(head_k) 为前缀}|，head_k = min(L1_k)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_UPSTREAM_COUNT.md` §二（M_CHAIN_UPSTREAM_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：「上游环节」需要两样东西：**阶段标注**（哪些节点是上游）与**环节清单**（这些节点有多少个）。清单在 `gkx.dwd_industry_chain_info` 完整（1,273 节点），阶段标注**完全没有**——16 列里没有 `chain_stage`，唯一可能承载层级的 `level` 全表恒为 0。本件用「编码序位」代理阶段，等于用结构假设换掉语义字段，因此判 **部分支持**。
- **基期声明**：截面指标：链树为静态维表，无版本列、无年度分区，不涉及年份分母，故 used/missing 均为空，不属于「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_UPSTREAM_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_UPSTREAM_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_UPSTREAM_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

