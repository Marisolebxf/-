# 产业链高价值环节占比（M_CHAIN_HIGH_VALUE_RATIO）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HIGH_VALUE_RATIO.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HIGH_VALUE_RATIO.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HIGH_VALUE_RATIO_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_HIGH_VALUE_RATIO |
| 指标名称 | 产业链高价值环节占比 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链图谱／价值链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 链全景页「高价值环节」占比环、招商靶点面板 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_HIGH_VALUE_RATIO.md` |

## 口径定义

分子要求「哪些环节属高价值」，gkx 链树无重要性/价值字段；唯一带「量」的列 `node_company_count` 全表 1,273 行恒为 0，连「企业数」这个代理量都不存在，属零等价。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HIGH_VALUE_RATIO.md` §二（M_CHAIN_HIGH_VALUE_RATIO.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_industry_chain_news_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：链树 `dwd_industry_chain_info`（1273 行、1 个层级）没有任何价值类字段（value/importance/weight/scale/score 逐个扫，命中 0 个）；全库按 6 类词根扫环节价值表，命中 0 张。唯一沾边的 `node_company_count` 是「节点内企业数」，非 NULL 1273 行（填充率 1.0）但正值只有 0 行——整列恒为 0，是空壳字段，语义既不是价值、也没有值。「高价值」这一维在 gkx 无结构与数据闭环，故判完全不支持。
- **基期声明**：截面指标：占比是「当前链树内高价值环节数 / 环节总数」，链树无版本列、无有效期列，不构造年度序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_HIGH_VALUE_RATIO.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HIGH_VALUE_RATIO.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_HIGH_VALUE_RATIO_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

