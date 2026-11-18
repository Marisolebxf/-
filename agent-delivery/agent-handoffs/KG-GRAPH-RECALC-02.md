# Handoff · KG-GRAPH-RECALC-02（技术点层指标重算与榜单刷新）

- 执行：human:韩梦蕊（Claude Code 辅助）；完成 2026-11-18（当日完成全部六项范围）
- 状态：**integration**（数据面、diff、证据齐，待唐绍祖复核；不写 done——由验收签）
- evidence：[KG-GRAPH-RECALC-02-重算与diff.md](../工程过程/04-系统集成/07-图数据库集成/派单-20261113-图谱100/KG-GRAPH-RECALC-02-重算与diff.md)（四张 diff 表 + 归因 + 生成命令）
- 归档：[对接文档/燕大/KG-GRAPH-RECALC-02/](../工程过程/04-系统集成/07-图数据库集成/对接文档/燕大/KG-GRAPH-RECALC-02/)（七项数据面 JSON + 435 汇总 md + 可复跑脚本 + verification）

## 一、七项产物 · 路径 / 行数 / 与旧版 diff 摘要

| 项 | 文件（归档目录内） | 行数 | 旧→新摘要 |
|---|---|---:|---|
| 428 度整榜 | degree-full.json | 19,430 | 13,812 点度变化；ΣΔ度=91,648=2×45,824；锚点 2,914→3,378 |
| 中台 1 加权度整榜 | weighted-degree-full.json | 19,430 | 口径未动（入射 Σconf/100）；锚点 1,478.05→1,766.95 |
| 428 人口对照 | degree-1500.json | 1,500 | 新度 Top1500：1,458 沿用，42 出 42 入 |
| 431 PageRank 整榜 | pagerank-full.json | 19,430 | 新增交付（旧档只有 1500 人口 raw 值）；Σ=1、不动点残差达标 |
| 429 紧密 | closeness-1500.json | 1,500 | 新人口重算（无权 wf_improved 同 T09） |
| 430 中介 | betweenness-1500.json | 1,500 | 新人口重算（k=300 seed=42 同 T09） |
| 432 综合榜 | composite-recomputed.json | 1,500 | 四项全部新数据重算（T09-S1 版只换 degree，差异已在 scope 注明）；rank 连续单调 |
| 434 partition | community-partition.json | 19,430 | Louvain 同参同实现：287→282 群 |
| 435/437 汇总 | community-summary.json + 435 属性汇总.md | 282 | 成形 180→**181**；密度/平均度=T10 修订口径（无序点对去重） |
| 范围④ 校验 | community-id-check.json | — | 图内 tgc_*（1,731 群）与重算不同源，以图内为准，差异 15,165 条在案 |
| 范围⑤ diff | diff-summary.json | — | 四张表 Top20 全量 + 恒等式归因 |

全部门检在 verification.json：快照 SHA256、质量四零（0 重复对/自环/空 conf/缺端点）、SQLite 独立对拍 19,430 点（误差 1.3e-11）、双握手恒等式、PageRank 不动点、综合榜逐行复算、旧档前后 SHA256 不变。

## 二、社群数变化（派单点名须说明项）

成形 180→181（**+0.56%，±10% 内，未改任何口径**）；总数 287→282、单点 107→101（新边把 6 个孤点连入社群）；模块度 0.2786→0.2867。同参同实现同版本栈（python-louvain 0.16 / seed 42 / r8.0 / 全边无权）重跑，变化全部由 +45,824 条边解释。

## 三、community_id 结论（下游接线必读）

图内 `community_id` = 源表 tgc_* 值（1,731 群，仅 23 成形），与 T10 签收 partition、本次 partition 均非同源（结构性差异，非本次新边造成）。**接口读 community_id 以图内为准**；434/435/437 若采用本次 partition/summary，社群编号与 tgc_* 不可混用（T12 §4.3「社群编号随快照变化」已预留该语义）。需 D 包在 434/437 数据源上二选一后固定透传。

## 四、未完成项与原因

无未完成项。两点备查：
1. 431 旧版无整榜归档，本单 diff 的 PageRank 对比以「旧 1500 人口 raw 值」为左基线（可比口径为旧人口内排名，diff-summary 已注明）。
2. 快照与 community-ids 导出留在执行机 `.local/kg-recalc02-20261118/`（gitignore 覆盖，仓库仅提交派生数据与证据）；复算须按批准方式取得与 manifest 哈希一致的快照。

## 五、下游解锁

- D 包（KG-GRAPH-API-04）：428–432/435/437/中台 1 的数据面 JSON 已就位，行结构与 T09-S1 一致（T12 透传方式不变）；434/437 接线前先定 community_id 数据源（§三）。
- 11-19 系统测试 / 11-20 总集核验：榜首与社群数字已刷新至新边状态，「为什么新加的机构没进榜」类问题可用 diff-summary 的归因列当场回答。
