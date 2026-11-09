# POL-PC1-CASE-FILL-DATA · handoff

- **任务**：POL-PC1-CASE-FILL-DATA（602 清洗 Tab · script_state 缺项演示数据灌数）
- **执行**：agent:data ｜ **监管人**：human:淮政玮 ｜ **日期**：2026-11-09
- **claim_type**：coordinator_dispatch（总控授权「后续认领不必再问」）
- **ponytail**: N/A（数据）
- **批准依据**：human:淮政玮 已批准往 demo 库灌确定性清洗作业行（仅 `demo_gkxlumenx_dwd.script_state`）

## 调研（2026-11-09 15:2x，主机 10.50.11.76，用户 gkxlumenx）

| 库表 | 结果 |
|---|---|
| `demo_gkxlumenx_dwd.script_state` | 灌前 **0 行**。真实列：`job`(varchar16, PRI)、`policy_id`(varchar100, PRI)、`content_hash`(varchar32, NOT NULL DEFAULT '')、`status`(varchar20)、`batch_id`(varchar32)、`tried_at`(datetime)、`next_try_at`(datetime NULL)、`try_count`(int DEFAULT 0)、`note`(varchar500)。主键 = (job, policy_id)，故每 job × 每政策仅 1 行 |
| `demo_gkxlumenx_dwd.policy_base_info` | 未删除 **20169** 条（is_deleted=0） |
| `demo_gkxlumenx_ads.policy_text_parse` | 20168 行，覆盖 20168 个政策 id（全库广覆盖） |
| `gkxlumenx_gapfill.gapfill_policy_lineage_index` | 10 行，政策 id = **18318861 / 18319069 / 18319394** |
| `gkxlumenx_gapfill.gapfill_policy_indicator_lib` | 12 行，政策 id = 18318861 / 18319069 / 18319394 |
| gapfill∩dwd 未删除 | `['18318861', '18319069', '18319394']` → 全部用作 policy_id |

## 表结构差异说明（重要）

表真实列含 `content_hash`（NOT NULL，默认 ''）与 `next_try_at`（NULL 可空），且 (job, policy_id) 为联合主键。任务简报所列列名基本吻合，插入时未显式给 `content_hash`/`next_try_at`（走默认值），安全无冲突。job 列注释原口径为 c1/c2 产业/条款作业，本批按用户批准的「清洗管线阶段口径」灌入中文规则名（页面 Tab 文案同源），无值域约束（varchar16，中文 6 字内安全）。

## INSERT 依据（19 行，1 条 executemany，批量 idempotent 于主键）

- **批次**：`batch_id = pc1-clean-20261109`；`tried_at = NOW()`（2026-11-09 15:25:24）；`try_count` 1–3；`note` 全部「缺项演示作业行：…」中文说明。
- **job 名**：与治理页「清洗规则与校验」6 规则同源（去重合并/格式标准化/噪声过滤/完整性校验/一致性校验/准确性校验）+ 批次明细标题的「采集接入」，无「Mock」字样。
- **status**：success / failed / skipped（前端 batchStatus Tag：success→成功、failed→失败、其他→部分，skipped 落「部分」档语义合理）。
- **policy_id × job 矩阵**（确定性，无随机）：

| job | 18318861 | 18319069 | 18319394 |
|---|---|---|---|
| 采集接入 | success | success | success |
| 去重合并 | success | success | failed(try_count=3) |
| 格式标准化 | success | success | skipped |
| 噪声过滤 | success | success | failed |
| 完整性校验 | success | failed | skipped |
| 一致性校验 | success | success | —（主键去重，不再加） |
| 准确性校验 | success | failed | — |

（18319394 在采集接入行 note 标注为扫描件，链路语义一致。）

## 回读核对（灌后 SELECT）

`GROUP BY job, status`（= Java `PolicyGovernanceController.QUALITY_SQL` / qualityAgg 形状）：

| job | status | row_count |
|---|---|---|
| 一致性校验 | success | 2 |
| 准确性校验 | failed | 1 |
| 准确性校验 | success | 1 |
| 去重合并 | failed | 1 |
| 去重合并 | success | 2 |
| 噪声过滤 | failed | 1 |
| 噪声过滤 | success | 2 |
| 完整性校验 | failed | 1 |
| 完整性校验 | skipped | 1 |
| 完整性校验 | success | 1 |
| 格式标准化 | skipped | 1 |
| 格式标准化 | success | 2 |
| 采集接入 | success | 3 |

合计 **19 行 / 13 个 job×status 组** → qualityAgg 非空、失败样例列有内容、明细列表可按 status 过滤。

## 边界遵守

- 只写 `demo_gkxlumenx_dwd.script_state`；未碰其他任何表；未写正式库 `gkxlumenx_dwd`；未跑 `--apply`。
- 口令经严格正则 `LUMEN_ALGO_MYSQL_PASSWORD\s*,\s*value:\s*"([^"]*)"` 进程内读取，未落盘、未打印；一次性脚本已删除。
- 过程发现 `gkxlumenx_gapfill` 与 `demo_gkxlumenx_dwd` 之间 JOIN 报 collation 混排（utf8mb4_0900_ai_ci vs utf8mb4_unicode_ci），改 Python 侧内存交集规避，未改任何表结构。
- 不 commit / 不 push / 不改代码仓（收口叶负责）。

## 待收口

- 前端 602 清洗 Tab（lumen-ui-science-pc `/policy/governance`，live 链路 `results.qualityAgg`）灌数后应显示 7 个批次行；收口叶联调核验即可。
