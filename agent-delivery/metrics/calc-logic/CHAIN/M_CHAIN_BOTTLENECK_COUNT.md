# 产业链瓶颈堵点数（M_CHAIN_BOTTLENECK_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_BOTTLENECK_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_BOTTLENECK_COUNT |
| 指标名称 | 产业链瓶颈堵点数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链监测／堵点识别 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业链监测页「瓶颈堵点」面板、补链强链专题 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_BOTTLENECK_COUNT.md` |

## 口径定义

瓶颈要求「供需缺口/技术依赖/产能利用/交付周期/替代性」五维评分，gkx 五维全无，且不能与「空位环节」混同。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_BOTTLENECK_COUNT.md` §二（M_CHAIN_BOTTLENECK_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_bid_`
- `dwd_en_paper_citation`
- `dwd_industry_chain_info`
- `dwd_macro_index_data`
- `dwd_org_important_news_info`
- `dwd_org_industry_tags`
- `dwd_zh_paper_citation`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：五维输入（供需缺口/技术依赖/产能利用/交付周期/替代性）逐维按 3 类词根扫描 gkx 表名，剔除误匹配后**有节点级载体的维度 0/5**；瓶颈本体词根（bottleneck/chokepoint/constraint）命中 0 张。最像的 `dwd_macro_index_data`（20000 行、287 个指数、1949—2026 年）经查 `dim_cal` 只有 JDZ/TB 两值、按 cap/util/产能检索 0 条，不含产能利用率，且为宏观口径、不落环节，不能救 D3。五维均无一维具备「结构 + 数据」闭环，故不存在「至少一维可算」的部分支持下限，判完全不支持。另：链树 1273 个节点里 `node_company_count>0` 的仅 0 个，「空位环节」是结构占位而非堵点，不能顶替本指标（§1.6 边界）。
- **基期声明**：截面指标：堵点数是「当前存量堵点清单的条数」；五维输入均无年度字段，不构造年度序列。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_BOTTLENECK_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_BOTTLENECK_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

