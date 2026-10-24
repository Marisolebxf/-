# 深圳产业机遇评分（M_CHAIN_SZ_OPPORTUNITY_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_OPPORTUNITY_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_OPPORTUNITY_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_OPPORTUNITY_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_SZ_OPPORTUNITY_SCORE |
| 指标名称 | 深圳产业机遇评分 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／深圳产业发展分析／产业机遇 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 深圳产业链页「机遇评分」卡与链级排名 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_SZ_OPPORTUNITY_SCORE.md` |

## 口径定义

三维结构与等权公式可复现，但 `trend_score` / `policy_score` / `market_score` 三个原始分都无真源，只能用新闻、政策、挂接数代理；新闻数组还被 `varchar(255)` 截断，趋势维有系统偏差，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_OPPORTUNITY_SCORE.md` §二（M_CHAIN_SZ_OPPORTUNITY_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_news_info`
- `dwd_org_industry_tags`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：calc-logic 的三维是 trend_score / policy_score / market_score，源表 chain_sz_opportunity 在 gkx 侧零表；live 侧同名表只有 8 行未来产业种子样例（model_version 后缀 -demo），与 12 链只重名 1 条，不能当结果面。三列本身没有真源，只能各自用可核代理重建：链级新闻关注度增速、深圳市政策按链命中数、深圳挂链次数。三维结构、等权公式、0—100 量纲都能对上，但每个代理与模型原分数不是同一把尺（新闻条数不是趋势、政策命中不是政策力度、挂链次数不是市场空间），且 5 条链缺 2025 新闻基线只能两维加权。故判部分支持。
- **基期声明**：趋势维只用 2025 全年与 2026 年化（截至 10-23，按 296/365 折算），两年都在 gkx 有数据，故 used=[2025,2026]、missing 为空；2024 及更早新闻为 0 行，不构成可用基期，未纳入。政策维与市场维是截面，不带年份。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_SZ_OPPORTUNITY_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_OPPORTUNITY_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_SZ_OPPORTUNITY_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

