# 要素影响力（会议）（M_INNOV_DS_FACTORS_008）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_008.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_008.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_008_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_FACTORS_008 |
| 指标名称 | 要素影响力（会议） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技信息展示系统） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 要素影响力分析（会议要素） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_FACTORS_008.md` |

## 口径定义

`gkx`（三方库，20261021 唯一数据面）**没有「会议」这一实体**：`gkx.dwd_zh_journal` 2,796 行全为 `publication_type='期刊'`、`gkx.dwd_en_journal` 605 行只有 Journal/Book in series/Book（**无 Conference/Proceedings**）、`gkx.dwd_zh_paper` 100,900 篇全为期刊论文；唯一疑似会议的 `gkx.dwd_event` 仅 20 行且无投稿/参与人数/论文关联；`gkx` 280 张表中 `table_name LIKE '%conf%'`、`LIKE '%meeting%'` 命中均 **0**。会议实体数 = 0 → 三个维度的分母全部为 0 → **完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_008.md` §二（M_INNOV_DS_FACTORS_008.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_author`
- `dwd_en_journal`
- `dwd_en_paper`
- `dwd_event`
- `dwd_merger_acquisition_events_party_info`
- `dwd_zh_author`
- `dwd_zh_journal`
- `dwd_zh_paper`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：会议实体的唯一可能落点是期刊/会议录表：gkx.dwd_zh_journal 仅 publication_type='期刊'（2,796 种），gkx.dwd_en_journal 仅 Journal/Book in series/Book（605 种，无 Conference/Proceedings 类型），gkx.dwd_zh_paper 全表 publication_type='期刊'、paper_type='期刊论文'（100,900 篇），名称含 Conference/Proceedings 的英文刊 21 种经核为丛书（Book in series）而非会议录。gkx 280 表中亦无 conference/meeting 专表（information_schema LIKE 检索 0 张；dwd_event 20 行为事件流水，非学术会议）。会议实体数 = 0 → 会议热度、投稿数、参与人数三维全部无分母，指标无法构建。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_FACTORS_008.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_008.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_FACTORS_008_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

