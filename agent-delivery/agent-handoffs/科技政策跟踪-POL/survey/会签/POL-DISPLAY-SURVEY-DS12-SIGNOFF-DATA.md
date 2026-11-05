# POL-DISPLAY-SURVEY-DS12-SIGNOFF-DATA · 政策效果推演调研 · 数据会签

- 角色：`agent:data-agent`
- 日期：2026-11-05
- 对象：`POL-DISPLAY-SURVEY-DS12-L01`
- 监管：`human:淮政玮`
- 范围：只核 DS-12 政策效果推演调研的数据口径。SRS 序号 232–242，另加布局推荐分键一行，合计 12 条。对照 `survey/DS-12.md` 与 `POL-DISPLAY-SURVEY-DS12-L01.md`。血缘只核三件事：缺数不写入 ODS、DWD、ADS 或供应方库；D4=`mock` 不写成已接入；不重开 GDF。说明书第 11.2 节只作观察。本页不定 DDL、不建库、不灌数、不改调研、不改任务注册表。

## 结论

同意会签。

本页可接统计读面为 0。推演模型留在 501，不进入 `BE-POL-DATA-01` 的统计对齐。已记载的 D4 均为 mock，与分册一致。序号 240 归第 7 项读图。本叶不重开政策 GDF 包，也不把缺数写入 ODS、DWD、ADS 或供应方库。

## 核对表

| 核对项 | 分册记载 | 判定 |
|---|---|---|
| 统计读面与 `BE-POL-DATA-01` | 三档计数：可接统计读面 0、501 共 10、跨项索引 2。`M_POLICY_SIMULATE` 为 MODEL、D4=`mock`，序号 232–234 判定 501。`M_POLICY_LAYOUT_REC_COUNT` 类型为 STAT、D4=`mock`，分册把它留在布局推荐键，判定跨项索引。边界写明 `BE-POL-DATA-01` 只对齐统计读面，推演模型不进该单 | 通过 |
| mock 结果与 GDF | 已注册模型记 D4=`mock`，判定为 501 或跨项索引。handoff 写明这些模型不写成已上线，页头「布局建议」卡是复刻壳。`GDF-POLICY-WORKPACK-V2-L01` 记为 done，本叶写明不重开政策 GDF 包。分册未把模型结果写成已有 ADS 读面，未新开政策 GDF 包 | 通过 |
| 序号 240 | 判定跨项索引。指标 `M_POLICY_RELATION_DEGREE`，类型 GRAPH，D4=`mock`。分册写明读图归第 7 项，展示只消费读图。`GDF-POLICY-GRAPH-EXT-L01` 按已有抽取脚本引用。本叶不新建查图表，不新建查图任务 | 通过 |
| D4 与缺数落库 | handoff 与分册一致：凡写出 D4 的指标均为 mock；没有指标的行写「未见」，没有写成 live 或已接入。本叶是文档，没有把缺数写入供应方库或 ODS、DWD、ADS。与 `data-lineage-policy` §2.4 不冲突 | 通过 |
| 说明书第 11.2 节 | 后续架构把 232–234 的退路放在 `gkxlumenx_gapfill.gapfill_policy_sim_forecast`，把 235–242 的缺项表放在 `gapfill_policy_sim_result` 与 `gapfill_policy_sim_stakeholder`，并写明 240 只消费已有子图。这些表不进 ODS、DWD、ADS 和供应方库。调研本身没有为这些表定 DDL，也没有写灌数 | 观察。本轮不要求调研把 501 改成读表口径，本页不补 DDL |

## 签收边界

- 同意范围只限上表数据角。调研三档维持：可接统计读面 0、501 共 10、跨项索引 2。
- 本文件不修改 `survey/DS-12.md` 与 `POL-DISPLAY-SURVEY-DS12-L01.md`。
- 本页不定字段级 DDL，不建库，不灌数。缺数不写入 ODS、DWD、ADS 或供应方库。
- 不重开 `GDF-POLICY-WORKPACK`。不新建查图任务。
- 不改 `task-registry`，不把 `POL-DISPLAY-SURVEY-DS12-L01` 标为 done。
- 说明书第 11.2 节的 `gkxlumenx_gapfill` 缺项表留给后续架构与灌数单。本轮不据此改调研判定，也不在本页补 DDL。
- 签收由 `human:淮政玮` 做。
