# LUMEN-POLICY-SZ3D-DATA-DEMO-L01 · 深圳政策现状演示实例

> 只补演示库里 job 已经在读的政策行。不改口径、不改页面、不改匹配。

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull`（对话派单后认领；认领接口未另写 claim_type） |
| 说明 | 未把本单标 done。 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用同一 `policy_id` 上已有的 `city` / `rank`，没有新建表，没有改 job。D9 / D16 / D18 按全文执行，没有用缺项表或新 ADS 顶数。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | `user-headroom` 已挂载。查询结果不大，没有调用 compress。必读规范按全文阅读。 |

## 图

本单不改存储拓扑，没有图。

## 结论

`POLICY-20261107-002` 条数为 0，是因为 job 正在读的 `demo_gkxlumenx_dwd.policy_base_info` 在 2026-10-27 重载后把 `city` 和 `rank` 清空了。行还在，过滤没改，也不是换成了另一张表。正式库 `gkxlumenx_dwd.policy_base_info` 上同一批 `policy_id` 仍有深圳市 879 条。已把这两列补回 demo 表。页面合法产业选「集成电路 / INB1303」。签发任务 `POLICY-20261107-004` 已成功：支持力度 879 条、分数 33.5585、名次第 5、层级均值 0.4653；落地实效不可算；深圳进入排名，第 5 章有供给结构。

## 1. 条数为什么变成 0

两边都是已签发任务，`honesty.source=dwd`，`degraded=false`。Python 城市截面 SQL 没变：

```text
SELECT policy_id, title, `rank`, province, city, district, region
FROM {dwd}.policy_base_info
WHERE COALESCE(is_deleted,0)=0
LIMIT 39999
```

`{dwd}` 在没有 `x-gkx-plane-policy: live` 时是 `demo_gkxlumenx_dwd`。Java Feign `RemotePolicyJobPythonClient` 不传这个头，默认平面是 demo。城市过滤在 `polan/shenzhen_board.py`：只用 `city` 列；空串和字面量 `NULL` 不进截面；`city` 以「深圳」开头算深圳；一座城市少于 30 条不入榜。产业锚点不参与这张卡。

| 任务 | 时间 | rows_read | city_rows | city_null_rows | 入榜城市 | 深圳条数 | 分数 | 名次 | 层级均值 |
|------|------|----------:|----------:|---------------:|---------:|---------:|-----:|-----:|---------:|
| `POLICY-20261025-010` | 2026-10-25 16:15 | 20000 | 10296 | 9704 | 40 | 879 | 32.6694 | 5 | 0.4579 |
| `POLICY-20261107-002` | 2026-11-07 10:49 | 20008 | 1 | 20007 | 0 | 0 | null | null | null |

对照：

- 库没有换成另一套。两次都读到约 2 万行，和 demo 表行数一致（现 20008）。正式库是 40000 行，对不上 `rows_read`。
- 过滤没有变。两次 diagnostics 都是「无城市名不进分子也不进分母」、门槛 30。
- 行没有删。demo 与正式库按 `policy_id` 相交 20000 条，其中正式库 `city='深圳市'` 的仍是 879。demo 这 20000 条的 `city`、`rank` 在 2026-11-07 查询时为空。demo 行的 `created_time` / `updated_time` 最晚到 2026-10-27 20:58，晚于 10-25 金路径，早于 11-07 截图任务。

`POLICY-20261107-002` 的请求锚点是 `industry_id=INB1303`、`industry_vid=chain:INB1303`，不是备注里的「具身智能 / INB1154」。支持力度不读锚点，所以条数 0 与这个 VID 无关。页面 L0 里具身智能的码是 `INB1354`，目录里没有 `INB1154`。

10-25 的层级均值 0.4579 与本次 0.4653 不同：10-27 重载之后，当时那一版 `rank` 已经不在 demo 表上。补回的是正式库仍在的 `rank`（深圳 757 条市级、96 条区级、26 条园区级），按现行权重算出 0.4653，与 calc-logic 样例一致。

## 2. 所选锚点

页面目录 `GET /api/topic/v1/meta/industry-clusters?include_l0=true`（`policy_version=sz-10+5-2026`）的 L0。按政策标题是否包含链名计数，取命中最多的一条。

| 产业 | VID | 标题含链名 | 其中深圳市 |
|------|-----|----------:|-----------:|
| 集成电路 | `INB1303` | 45 | 3 |
| 生物医药 | `INB2503` | 30 | 0 |
| 人工智能 | `INB1309` | 27 | 3 |
| 机器人 | `INB1204` | 19 | 6 |
| 具身智能 | `INB1354` | 0 | 0 |

选定：**集成电路 / VID `INB1303`**（集群「新一代信息技术」）。有城市名且标题含「集成电路」的城市是上海 13、北京 4、深圳 3、长沙 1，满 4 座，过适配性「本地命中城市不少于 3」的门槛。本次签发仍按页面现况只交 `industry_vid`，不交 `industry_name`。

## 3. 补进行

只更新 `demo_gkxlumenx_dwd.policy_base_info`。按 `policy_id` 连接 `gkxlumenx_dwd.policy_base_info`，仅当 demo 的 `city` 与 `rank` 都为空、正式库这两列都有值、且 `is_deleted=0` 时写入。两表 `policy_id` 都无重复。更新 20000 行，并写 `updated_time`。没有插入新政策，没有写金额，没有写 ODS、供应方库、`gapfill_` 或新 ADS。正式库只读。

补回后 demo 表现状：总行 20008；`city='深圳市'` 879；按 job 规则可入截面的城市行 10295；无城市名 9713（含字面量 `NULL`）。

本地调用现行 `build_shenzhen_board`（不传链名）读到的就是下面这张卡，与随后签发任务一致。

## 4. 演示任务

`POST http://10.50.69.111:30892/api/topicAsync/topic/v1/analysis/tasks`

| 项 | 值 |
|----|-----|
| 任务号 | `POLICY-20261107-004` |
| 状态 | `success`（2026-11-07 11:59:11–11:59:16） |
| 用户 | `guest` |
| 锚点 | `industry_id=INB1303`，`industry_vid=chain:INB1303`，无 `industry_name` |
| 指纹 | `86977506ba81bec49e1b417934081274fd7f9628534d51edb3f8220198d1b714` |
| force | true（不复用当天 `POLICY-20261107-002`） |

`honesty`：`source=dwd`，`fabricated=false`，`degraded=false`。

支持力度：

```json
{
  "metric_id": "M_POLICY_SUPPORT_STRENGTH",
  "computable": true,
  "score": 33.5585,
  "rank": 5,
  "policy_count": 879,
  "level_mean": 0.4653,
  "tier": {"value": null, "reason": "无金额列"},
  "spearman_vs_count": 0.9467
}
```

报告章节（库内 `report_chapters`，模板 `POL-SZ-3D-PDF-v1`）：

| 章 | 内容 |
|----|------|
| 1 分析范围 | 锚点印成「—」（请求没有链名）。任务号与指纹在。 |
| 2 支持力度 | 分数 33.5585，名次 5，条数 879，层级均值 0.4653，档位不可算：无金额列，非资金强度 |
| 3 产业适配性 | 未提供链名 |
| 4 落地实效 | 不可算。实施日、支持对象、反馈全缺 |
| 5 优化建议 | 供给结构：深圳名次第 5，分 33.5585，879 条，层级均值 0.4653，与条数秩相关 0.9467。市级为主，不宜写成政策偏弱。另有扶持档位不可算，没有把档位写成 0 |
| 6 口径与局限 | `city_null_rows=9713`，`city_rows=10295`，`cities_in_table=40`，`min_policies_per_city=30` |

适配性仍是「未提供链名」，因为页面只提交 VID。根因在 `LUMEN-POLICY-SZ3D-E1-DEFECT-C1.md`：`_shenzhen_anchor` 只把 `industry_name` 交给标题匹配。本单不改前端、不改匹配。链名若随请求送入，集成电路已有 4 座城市的标题命中，那是缺陷修完之后的事。

## 测试结果

- 补回前后用同一条城市截面 SQL 对过行数：深圳 0 → 879。
- `build_shenzhen_board` 与签发任务 `POLICY-20261107-004` 的分数、名次、条数、层级均值一致。
- 没有改 Python、Java、前端。

## 遗留

- 10-25 那一版 `rank` 已不在 demo 表，层级均值是现行正式库 `rank` 的 0.4653，不是 0.4579。
- 页面路径仍不送链名，第 3 章继续是「未提供链名」。
- 第 5 章扶持档位那一句经过既有润色，事实仍是无金额列、档位不是 0。
- 无城市名的 9713 行仍不进截面，与口径一致，没有回填城市。

## CI/CD

- 分支：`gkx-orchestration` `origin/dev`
- 代码仓：无业务仓 commit
- 数据：`demo_gkxlumenx_dwd.policy_base_info` 更新 20000 行的 `city`、`rank`、`updated_time`
- 部署：未改镜像

## 架构合规

| 项 | 结果 |
|----|------|
| 算法只在 Python，本单未改算法 | 是 |
| 前端只调 Java；Java 不写算法 | 未改调用链 |
| 未写 ODS、供应方库 | 是 |
| 未让接口返回写死 mock | 是。数来自 job 读表 |
| D16 | 未建 `gapfill_`。job 不读缺项库，不必另开算法叶 |
| D18 | 未新建 ADS。现有 job 读到的就是这张 `policy_base_info` |
| 未 merge demo 进 lumen | 是 |

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 100000 |
| model_used | `claude-sonnet-4.5` |
| actual_cost | 0.54 |
| cost_warn | `green` |
| 说明 | 会话模型是 Grok 4.7，不在 `valid_model_enum`。单价按枚举内同档 Sonnet 4.5（输入 $3/M，输出 $15/M），data-agent 比例 0.80/0.20。`100000×0.8×3/1e6 + 100000×0.2×15/1e6 = 0.54`。无 Console 分项，token 是本会话粗估，不是 `console_precise`。 |

## 涉及文件

- `agent-delivery/agent-handoffs/政策模块-E7/LUMEN-POLICY-SZ3D-DATA-DEMO-L01.md`
- `agent-delivery/task-registry.yaml`（认领与状态）
