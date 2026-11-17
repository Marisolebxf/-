# KG-GRAPH-COVER-01 覆盖补齐对账总表

- 执行：human:白鑫凤（脚本与实测）；执行窗口 **2026-11-17 21:20–22:25**（全流程当日完成）
- 依据：[派单-A](./派单-A-燕大-技术点层覆盖补齐.md) + [11-说明 §五/§六/§七](../11-说明-技术点层四项缺口成因与解法-20261117.md) + [13-通知（扩容非前提，请开工）](../13-通知-扩容非前提请开工-20261117.md)
- 环境：图库 `10.50.75.136:9669` / `demo_gkx_chain`（**未扩容未调水位**，PLAT-09 结论）；源 `47.93.119.170:29030` / `gkx_technology_analysis_dev`（只读）
- 脚本（同目录，可复跑、可断点续、默认 dry-run）：`cover01_s1_create_institutions.py` / `cover01_s2_load_edges.py` / `cover01_s3_fill_tech_rel.py` / `cover01_s4_backfill_community.py`

---

## 一、对账总表（派单-A 要求的核心交付）

| 项 | 源表应有 | 图中补后（实测 2026-11-17 22:1x–22:2x） | 新写 | 跳过 | 跳过原因 |
|---|---:|---:|---:|---:|---|
| tech_has_institution（机构边） | **2,428,981**（§五裁定 `is_company=0`；原派单 2,528,802 含企业 99,821 不入分母） | **2,431,091** = 非企业集内 2,428,981 + 图内遗留 2,110 | 2,380,091（试写 10,000 + 正式 2,370,091） | 企业行 99,821（§五裁定）；图内遗留 2,110 对不在当前非企业源集（早期预览灌入，**不删**，见 §四） | 端点缺失 0 |
| tech_rel（技术点关系边） | 587,252 | **587,252（100%）** | 45,824（差分补齐，未整表重灌） | 0 | 缺端点 0（实测） |
| tech_path_step（路径步） | **35,018（跳数口径）**（原 47,909 为节点行口径） | **35,018（100%）** | 0（不补，选项 A） | 12,891（每条路径首节点，无前驱结构性不可成边） | 见[路径步规则确认单](./KG-GRAPH-COVER-01-路径步规则确认单.md) |
| community_id（社群归属） | 19,430 | **19,430（100%，`!= ''` 校验）** | 19,430 条 UPDATE VERTEX | 0 | — |
| tech_institution 点（前置） | 33,026（非企业机构） | **34,769** = 33,026 + 1,743 历史遗留点 | 17,227 | 0 | — |

**DoD 核对**：派单-A「总量 ≥ 2,402,362（95%）」→ 实际 2,431,091 ✅ 超线 28,729。
**业务可见变化**：有机构边的技术点 361 → **18,948**（19,430 个技术点的 97.5%；此前 1.9%）。

## 二、批次台账（每批可对）

| 批号 | 内容 | 条数 | 回读对账 | 证据（执行机 `~/qiliantupu/kg100-work/`，不入仓） | sha256 前 16 位 |
|---|---|---:|---|---|---|
| kg100-cover-01-trial | 试写（第 0 步） | 10,000 | 51,000→61,000，增量核对 ✅；抽验 100/100 | trial_pairs.json / trial_result.json（含首试报错留证） | 54bae4f2e6bae814 |
| kg100-cover-01-s1 | 建 tech_institution 点 | 17,227 | 17,542→34,769 ✅；35 小批全绿 | s1_checkpoint.json / s1_batch_log.csv | — |
| kg100-cover-01-ins-01 | 机构边批 1 | 200,000 | 探活 ✅ 抽验 50/50 | batch_kg100-cover-01-ins-01.json | ead0ba97bcef1ea7 |
| kg100-cover-01-ins-02 | 机构边批 2 | 200,000 | 同上 | batch_…ins-02.json | 51359453611f7a1a |
| kg100-cover-01-ins-03 | 机构边批 3 | 200,000 | 同上 | batch_…ins-03.json | 1c29be77125fcc56 |
| kg100-cover-01-ins-04 | 机构边批 4 | 200,000 | 同上 | batch_…ins-04.json | e0a50466bf93bd65 |
| kg100-cover-01-ins-05 | 机构边批 5 | 200,000 | 同上 | batch_…ins-05.json | 679117d378b971c2 |
| kg100-cover-01-ins-06 | 机构边批 6 | 200,000 | 同上 + **中段全量 count 1,261,000 ✅** | batch_…ins-06.json | 8391771ab80d2096 |
| kg100-cover-01-ins-07 | 机构边批 7 | 200,000 | 探活 ✅ 抽验 50/50 | batch_…ins-07.json | 9e492d108dacecf4 |
| kg100-cover-01-ins-08 | 机构边批 8 | 200,000 | 同上 | batch_…ins-08.json | 39c676092fddcd2b |
| kg100-cover-01-ins-09 | 机构边批 9 | 200,000 | 同上 | batch_…ins-09.json | 5c7a16954f629c95 |
| kg100-cover-01-ins-10 | 机构边批 10 | 200,000 | 同上 | batch_…ins-10.json | e281c535544a8caa |
| kg100-cover-01-ins-11 | 机构边批 11 | 200,000 | 同上 | batch_…ins-11.json | f6508c70dad4d4dd |
| kg100-cover-01-ins-12 | 机构边批 12（末批） | 170,091 | 同上；**终段全量 count 2,431,091 ✅** | batch_…ins-12.json | b0d127c66cb49dc6 |
| kg100-cover-01-rel | tech_rel 差分（单批） | 45,824 | 增量 45,824 ✅ 抽验 50/50 终值 587,252 ✅ | s3_diff_pairs.json / s3_batch_log.csv | b6d7d4cf5ae35244 |
| kg100-cover-01-comm | community_id 回填（单批） | 19,430 | `!= ''` 计数 19,430 ✅ | s4_batch_log.csv | — |

每批明细另有 CSV 台账：`s1_batch_log.csv` / `s2_batch_log.csv` / `s3_batch_log.csv` / `s4_batch_log.csv`（时间/批号/条数/探活/抽验/增量）。

## 三、执行纪律核对（§七四坑逐一）

| 坑 | 防法执行情况 |
|---|---|
| 一口气灌 237 万 | 12 批 × ≤20 万，每批 O(1) 探活 + 50 对抽验；中段/终段全量 count；**全程任何一批失败立即停（实际 0 次触发）** |
| 不去重直接灌 | 写前重导图内全部已有端点对做集合差：61,000 对中 58,890 落在非企业源集内跳过，源内重复 0 |
| 企业行算进机构边 | 只取 `is_company=0`，分母 2,428,981；99,821 企业行未写入 |
| 路径步缺口当漏补 | 按确认单选项 A 裁定，不补数，分母改跳数 35,018 |

**图库健康**：全流程 `num_queries_hit_memory_watermark.sum.600 = 0`（开跑前/中段/收官三次核验）；无假死、无重启。写入速率实测 6.6 万边/秒（试写 1 万条/0.2s 预估后正式批稳定复现）。

## 四、两条说明（防误读）

1. **图内遗留 2,110 对**：补前图内 61,000 对中有 2,110 对不在当前非企业源集（早期预览版灌入，源表后续版本已不含或属企业行）。按「禁止删除任何现有边」**保留不动**，故终值 2,431,091 略高于源集 2,428,981。
2. **institution_type 未入库**：`tech_institution` Tag 无该字段（禁改 schema），源表类型列未写入，记此处备查。`name_zh` 源表仅 184/17,227 家有值，其余按空处理（NULL）。

## 五、与派单原文的一处偏离（须回执确认）

派单-A 第 1 步要求「写入用 `INSERT EDGE tech_has_institution(weight, props)`，props 含 batch 批号；每批回读 CONTAINS 计数」。**实测该边型 schema 仅有 `relation_strength` 一列，无 props/weight 列**（`SHOW CREATE EDGE` 留证；禁改 schema），批号无法落在边上。替代对账法：**分批端点对文件（sha256 留证）+ 每批探活抽验 + 中段/终段全量 count 差**。批号（ins-01…12 / rel / comm）作为台账记录存在于本表与 CSV 日志。此偏离同样适用于试写与 tech_rel（tech_rel 有四个业务属性列，已随写入带上源值；batch 列同样不存在）。

## 六、可复算性

| 结论 | 复核语句（均带 Tag 锚定） |
|---|---|
| 机构边 2,431,091 | `MATCH ()-[e:tech_has_institution]->() RETURN count(e)` |
| tech_rel 587,252 | `MATCH ()-[e:tech_rel]->() RETURN count(e)` |
| 路径步 35,018 | `MATCH ()-[e:tech_path_step]->() RETURN count(e)` |
| community_id 19,430 | `MATCH (v:tech_point) WHERE v.tech_point.community_id != "" RETURN count(v)` |
| 机构点 34,769 | `MATCH (v:tech_institution) RETURN count(v)` |
| 有机构边的技术点 18,948 | `MATCH (v:tech_point)-[:tech_has_institution]->() RETURN count(DISTINCT id(v))` |

源侧口径复核见[路径步规则确认单](./KG-GRAPH-COVER-01-路径步规则确认单.md) §二 与 11-说明 §九。
