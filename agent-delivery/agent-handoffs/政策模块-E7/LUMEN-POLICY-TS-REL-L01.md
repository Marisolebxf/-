# LUMEN-POLICY-TS-REL-L01 · 抽取产业错配抽样

> 不改门槛。分数没有落库，本机也到不了集群内向量服务，不能画 50 条分数曲线。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 没有第二张关联表写入，所以没有改 `SCORE_WRITE` / `SCORE_GRAY`。未重跑 2 万条，未加 `match_score` 列。 |

## 写入方

- 现网库是 `demo_gkxlumenx_ads.policy_industry_rel`（不是正式 `gkxlumenx_*`）。
- 向这张表 `INSERT` 的代码只在 `demo-algo-ent-analysis/polan/industry_enrich.py`。
- `lumen-algo-py/lumen_common/algorithms/policy/industry_enrich.py` 只 `UPDATE` 主表 `related_entities`，不写关联表。时序不读这列，不算第二写入方，本叶不因此改口径。
- `chain:INB170401` 有效行 5 条，`update_time` 都在 2026-10-24 00:24–01:28，与 demo 抽取任务同一窗口。带链码的有效行一共 321 条。

## 抽样（按 update_time 最新 50 行，不是分数曲线）

错配很集中。同一条通知经常挂上 4～5 个不相干链码，例如：

| 标题 | 挂上的名称 | 判断 |
|------|------------|------|
| 广东省培育前沿新材料战略性新兴产业集群行动计划 | 高性能与前沿新材料 | 对得上 |
| 山东省新一代信息技术创新发展重点方向和任务 | 新一代信息技术 | 对得上 |
| 甘肃省爆炸事故应急预案 | 应急安全 | 错 |
| 甘肃省就业创业工作实施意见 | 新能源、新能源材料 | 错 |
| 甘肃省促进新型研发机构发展的指导办法 | 高性能与前沿新材料、基础模型等 5 个 | 错 |
| 第二届中国创新挑战赛（安康）技术需求公告 | 高性能与前沿新材料、锂电装备等 5 个 | 错 |
| 组团参加北京国际科技产业博览会 | 新能源材料 | 错 |
| 河南省科学技术奖推荐工作 | 关键功能部件 | 错 |

`chain:INB170401` 这 5 条里，只有广东前沿新材料行动计划明显对题。云南高新技术产业条例、上海纳米专项只是沾边。甘肃新型研发机构、安康挑战赛是错配。时序结果里的「政策总数 5」因此不能当成这个产业的真实政策数。

## 为什么不改 0.55 / 0.45

`industry-match-optimize.md` §5 要求用约 50 条的分数画「定上 / 定错」再换门槛。关联表没有分数字段。复算要打 `gkxlumen-embed-tei`（只在集群内）。本机没有这条地址，不能选出新的阈值。凭标题把 0.55 改高，可能把广东这条对的也丢掉。门槛保持 `SCORE_WRITE=0.55`、`SCORE_GRAY=0.45`。

## 解锁

在能访问嵌入服务的环境，对这 50 条政策只读复算各块最高分，再决定是否改这两个常量。不要重跑 2 万条，不要加列。

段 E 金路径第 3 条按红记：错配还在。不要用时序 SQL 的标题过滤把它们藏起来。

## CI/CD

- 无代码变更，无 commit，无部署

## 涉及文件

- 无代码改动
- 对照：`demo-algo-ent-analysis/polan/industry_enrich.py`（`SCORE_WRITE` / `SCORE_GRAY` 未改）

## cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 20000 |
| model_used | grok-4.7 |
| cost_warn | green |
| 说明 | source: session_estimate。查询只读，未跑嵌入。 |
