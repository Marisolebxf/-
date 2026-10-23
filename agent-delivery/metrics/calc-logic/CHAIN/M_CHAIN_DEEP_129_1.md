# 重点布局产业推荐模型（M_CHAIN_DEEP_129_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_129_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_129_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_129_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEEP_129_1 |
| 指标名称 | 重点布局产业推荐模型 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 二级模块 | 深圳产业发展分析 |
| 更新频率 | 季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEEP_129_1.md` |

## 口径定义

推荐指数 = 1/3 × 深圳产业优势分 + 1/3 × 产业机遇分 + 1/3 × 政策匹配分；>=70 优先布局，55—70 重点培育，<55 观察。权重与阈值均为本件自定义，非甲方确认参数

> 一句话口径（源件 §0.3）：以深圳产业优势分、产业机遇分、政策匹配分三等权合成推荐指数，12 条链中 **集成电路 88.99 分排第 1**，是唯一进入“优先布局”的链；智能网联汽车 68.07、智能终端 59.83、生物医药 59.62 等 7 条链为“重点培育”，数字创意、合成生物、具身智能、低空经济 4 条为“观察”。但三个维度几乎不相关（Spearman −0.133—0.046），权重稍变排名就大幅换位，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_129_1.md` §二（M_CHAIN_DEEP_129_1.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：本件回答“深圳应该优先布局哪几条产业链”。按 `calc-logic` 的三维框架：优势分取 `M_CHAIN_SZ_ADVANTAGE_SCORE_out.json` 的 `sz_score_available_dims`，机遇分取 `M_CHAIN_DEEP_128_1_out.json` 的 `opportunity_index`，政策分取 `M_CHAIN_POLICY_MATCH_SCORE_out.json` 的 `match_score`，三等权合成推荐指数。
- **基期声明**：截面合成指标，无年度基期；三个输入件各自的口径与基期见其产物文件

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEEP_129_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_129_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEEP_129_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

