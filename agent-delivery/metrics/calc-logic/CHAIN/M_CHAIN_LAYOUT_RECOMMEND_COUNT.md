# 产业链重点布局推荐数（M_CHAIN_LAYOUT_RECOMMEND_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LAYOUT_RECOMMEND_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_RECOMMEND_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_RECOMMEND_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_LAYOUT_RECOMMEND_COUNT |
| 指标名称 | 产业链重点布局推荐数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／深圳产业发展分析／布局推荐 |
| 更新频率 | 周 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳产业链页「重点布局」卡与推荐环节清单 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_LAYOUT_RECOMMEND_COUNT.md` |

## 口径定义

按 $R_1 \land R_2 \land R_3$（全国 ≥ 10 家、≥ 该链中位、深圳 0 家或占比 < 7.952%）筛 954 个叶级环节，得 **251 个**建议布局环节（Tier A 空白强 22、Tier B 空白中 27、Tier C 单点缺口 202），占全部叶的 **26.31%**；生物医药 70 个最多、具身智能 4 个最少。原模型的方案条数与优先级评分不可得，本件是结构侧清单，不是发布快照直读。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LAYOUT_RECOMMEND_COUNT.md` §二（M_CHAIN_LAYOUT_RECOMMEND_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`
- `dwd_org_annual_financial_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：calc-logic v0.2.0（方案A）是读发布快照：industry_chain_metric_fact 按单链直读推荐条数，模型侧由 industry_chain_model_result_detail.priority_level 定档。gkx 侧无这两张表（280 表里 layout/recommend 关键词零命中），live 侧 metric_fact 0 行，推荐模型的权重、档位阈值、评分口径均无真源。本件用链树 + 1,714,457 家链属企业 + 深圳挂链重建「全国有规模、属关键叶、深圳相对缺位」的环节清单并计数，规则可复算、可逐环节下钻；但它不是原模型的推荐结果，只能算结构侧布局建议，故判部分支持。
- **基期声明**：本件是截面指标：链树、叶级企业数、深圳挂链次数均为当日快照，口径内无年度序列，不涉及基期分母，故 used/missing 为空。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_LAYOUT_RECOMMEND_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_RECOMMEND_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_LAYOUT_RECOMMEND_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

