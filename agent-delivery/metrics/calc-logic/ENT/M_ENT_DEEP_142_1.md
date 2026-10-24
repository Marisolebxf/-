# 企业发展历程模型（M_ENT_DEEP_142_1）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DEEP_142_1.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DEEP_142_1.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DEEP_142_1_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DEEP_142_1 |
| 指标名称 | 企业发展历程模型 |
| 所属域 | ENT（企业分析） |
| 一级模块 | ENT（企业分析） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业分析 → 企业详情 → 发展历程 / 重大事件 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DEEP_142_1.md` |

## 口径定义

{'unit': '企业×事件', 'event_types': ['E0 成立', 'E1 上市/挂牌', 'E2 股权融资', 'E3 并购当事人', 'E4 对外投资', 'E5 股权结构'], 'dated_types': ['E0（年粒度）', 'E2（日）', 'E3（日）'], 'undated_types': ['E1', 'E4', 'E5'], 'threshold': '对外投资「重大」阈值 1000 万元（库内金额单位按万元解释）'}

> 一句话口径（源件 §0.3）：五类事件的表结构与行数都不缺：融资 25,654 行、并购主表 3,444 行 + 当事人 20,000 行、对外投资 46,967 行、股东 400,286 行、上市状态 1,971 家。但**日期字段严重不均**：`listing_date` 全库 0 行非空；对外投资表只有入库时间 `created_time`（多为 2026-08），没有投资发生日；股东表是当前快照，没有变更日期。五类中只有融资与并购能定位到日 → **部分支持**。本档位与 `code/M_ENT_DEEP_142_1_out.json` 的 `support_judgment.data_support_level` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DEEP_142_1.md` §二（M_ENT_DEEP_142_1.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_merger_acquisition_events_party_info`
- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_invest_info`
- `dwd_org_merger_acquisition_info`
- `dwd_org_shareholder_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：五类事件只有两类带业务日期：E2 融资 24,598 条有 completion_date、E3 并购当事人 12,387 条有公告日 ggrq（另有 1 条 1900-01-01 哨兵值）；E1 上市 listing_date 全库 0 行非空（listing_status 非空 1,971 家只有状态无日期）；E4 对外投资 46,967 行只有入库时间 created_time、无投资发生日；E5 股权结构 400,286 行为当前快照、无变更日期与历史版本。五类中两类可定位到日、一类只有状态、两类无日期 → 时间线只能覆盖部分事件，判部分支持。
- **基期声明**：由产物中实际出现的年度键反推：used=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。
- **复现实测耗时**：约 156.76 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DEEP_142_1.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DEEP_142_1.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DEEP_142_1_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

