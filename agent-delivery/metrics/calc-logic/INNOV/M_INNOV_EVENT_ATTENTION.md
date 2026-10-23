# 事件关注度（M_INNOV_EVENT_ATTENTION）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EVENT_ATTENTION.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_ATTENTION.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_ATTENTION_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_EVENT_ATTENTION |
| 指标名称 | 事件关注度 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新分析 |
| 更新频率 | 不适用 |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 无（不挂载；仅作缺口说明与替代口径登记） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_EVENT_ATTENTION.md` |

## 口径定义

事件关注度要回答的是「一场事件被多少人看见、被多少媒体讨论」。它需要两个前提：有一批事件，有对这批事件的关注信号。gkx 两个前提都不成立——事件面只有一场展会系列的 20 个条目，关注信号则要靠媒体报道，而媒体报道的对象是企业，不是事件。正本公式试图用政策文本的正文规模、主题覆盖、引用政策数来合成关注度，但主题与引用政策两列各有 19,998/20,000 行是字符串 'NULL'，公式实际只剩一维。三个来源同时断掉，故判 **完全不支持**，并且明确拒绝用专利被引或媒体条数替代。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EVENT_ATTENTION.md` §二（M_INNOV_EVENT_ATTENTION.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_event`
- `dwd_event_distinct_name`
- `dwd_event_rows`
- `dwd_innovation_event`
- `dwd_innovation_event_hits`
- `dwd_org_important_news_info`
- `dwd_policy_base`
- `dwd_zh_paper_citation`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：事件关注度需要事件面；gkx 无事件表（innovation_event / dwd_innovation_event 逐字 0），`dwd_event` 20 行且是单一展会系列；正本依赖的 policy 文本三维中 theme/quote_policy 各 19,998/20,000 是字符串 'NULL'。三个来源同时断掉，故判完全不支持，不构造分数、不拿专利被引冒充。
- **基期声明**：媒体读数取 2023—2026 近窗；2026 只到 2026-05-08，是残年，不摊成全年。2018—2022 的报道存在，但本件只做近窗对照，不进基期；事件表只有 2026-05 两天，无法构成年度基期。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EVENT_ATTENTION.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_ATTENTION.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_ATTENTION_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

