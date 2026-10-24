# 产业链发展里程碑数（M_CHAIN_DEVELOPMENT_MILESTONE_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_DEVELOPMENT_MILESTONE_COUNT |
| 指标名称 | 产业链发展里程碑数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业发展路线历程 |
| 更新频率 | 月度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链页「发展里程碑」时间线与计数卡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.md` |

## 口径定义

按「政策 ≥5 条/链年」与「融资 ≥5 亿元/事件」两条规则，12 条链共 **235 个**发展里程碑（政策 **9** + 大额投资 **226**），重大技术突破置 `null`；人工智能 94 个最多、智能网联汽车/低空经济/合成生物各 2 个最少。真源 `industry_chain_milestone_event` 两库均无，本件是事件侧替代计数，不是发布快照直读。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.md` §二（M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_event`
- `dwd_industry_chain_news_info`
- `dwd_org_financing_info`
- `dwd_org_invest_info`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：calc-logic 的真源 industry_chain_milestone_event 两库均无（gkx 280 表 milestone 零命中，唯一事件表 dwd_event 只有 20 行且无链键；live 同名表不存在）。三类里程碑里，政策出台可用政策×链×年命中重建、龙头入驻可用大额融资事件代理，两类都能按链汇总并下钻到事件；重大技术突破既无事件表、资讯表也没有 event_type/level 字段、专利表无突破标签，无法用可核口径识别，只能置 null 并留否定性证据。三类缺一类，故判部分支持。
- **基期声明**：融资侧窗口 2021—2026（2026 只到 10 月，属残年，按事件实际发生计，不做年化外推）；政策侧政策表的 publish_year 最新只到 2022，2023 及以后零条，故政策里程碑只用 2001—2022 的真实年份，不把缺失年按 0 摊进任何分母。base_years_used 列融资主窗口 2021—2025。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_DEVELOPMENT_MILESTONE_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

