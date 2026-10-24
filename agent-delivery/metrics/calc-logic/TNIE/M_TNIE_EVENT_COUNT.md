# 抽取事件条数（M_TNIE_EVENT_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TNIE-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TNIE_EVENT_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TNIE_EVENT_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TNIE_EVENT_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TNIE_EVENT_COUNT |
| 指标名称 | 抽取事件条数 |
| 所属域 | TNIE（科技新闻） |
| 一级模块 | 创新分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 创新活动监测、区域活动密度对比、活动型报道专题 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/TNIE/M_TNIE_EVENT_COUNT.md` |

## 口径定义

「抽取事件条数」要回答的是「发生了多少场创新活动」。它需要的是一张事件表：每行一场活动，有名称、时间、地点、主办方、参与规模。gkx 的 `dwd_event` 有名称、时间、主办方、URL，看起来像，但只有 20 行、只覆盖两天、全部是同一家主办方的展会系列。用这 20 行算「事件条数」，得到的不是创新活动总量，而是「某场展会的分论坛数」。真事件面不存在，本件只能退到媒体报道侧数「活动型标题」，并反复声明媒体 ≠ 事件，故判 **部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TNIE_EVENT_COUNT.md` §二（M_TNIE_EVENT_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `ads_tech_news_event`
- `ads_tech_news_extraction`
- `dwd_event`
- `dwd_industry_chain_news_info`
- `dwd_innovation_event`
- `dwd_org_important_news_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：真事件计数不可建：`dwd_event` 仅 20 行、只覆盖 2026-05-13/14 两天、20 个名称 19 个组织者全部是国药励展系展会；事件表与抽取结果表在 gkx 均 0 张。只能交「媒体报道中的活动型标题条数」代理，且逐条标注媒体≠事件，故判部分支持。
- **基期声明**：事件表只有 2026-05-13/14 两天；代理口径取 2025-01-01 起（media 表 2026 只到 05-08，是残年）。2018—2024 的报道存在但本件不做年度事件序列，故不进基期；不把 2026 残年摊成全年。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TNIE_EVENT_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TNIE_EVENT_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TNIE_EVENT_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

