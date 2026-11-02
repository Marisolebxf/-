# GDF 触发契约

GDF 只洗表、只调度。洗完指定的 DWD 表之后，触发知识图谱引擎上已经配好的入图作业。GDF 不写 Nebula，不连 graphd，不直连燕大的 Python。

本页是目标契约。现网还没有对外的 Java 受理，也没有完成回执。企业贴源包 `15` 的现网做法仍是飞书值班，图谱日批没有和 ETL 一样的异步任务。本包不把下面的路径写成已经能调，也不要求今天配进 GDF 的 DAG。

## 第一批：哪张表成功后触发哪次作业

只在该表当天 Wave B 作业 `success` 之后触发。表失败、没跑、只做完贴源，都不触发。企业点作业成功之前，不触发两条边。

| 顺序 | DWD 表 `success` | 引擎作业 | 写入 | 本版 |
|---|---|---|---|---|
| 1 | `gkxlumenx_dwd.enterprise_base` | 企业点 | Tag `enterprise`，VID `ent:{org_id}` | 触发 |
| 2 | `gkxlumenx_dwd.enterprise_supply_chain` | 供给边 | Edge `supply`，企业 → 企业 | 企业点作业成功之后再触发 |
| 3 | `gkxlumenx_dwd.enterprise_parent_subsidiary` | 母子边 | Edge `parent_sub`，母公司 → 子公司 | 企业点作业成功之后再触发 |

读表、跳过空 ID、写入 `gkx_chain` 的规则在 [01-企业维需求.md](01-企业维需求.md)。这三支作业由燕大写成 Python 脚本，配置到知识图谱引擎平台。空间固定 `gkx_chain`。

## 本版不触发

| DWD 表 | 原因 |
|---|---|
| `enterprise_cooperation` | 双向 `cooperate` 还没落地。有向边不算本版入库 |
| `enterprise_industry_chain` | 现有写出的边名不是 `participates` |
| `enterprise_invest` | 投资不进本包 |
| 合作表里科研、技术、人才、服务、政策那几类对端 | 不在企业维第一批，也不建企业到科研、技术、人才 |

不因为企业贴源包里登记过 `ENT_NER_ORG`、`ENT_RE_SUPPLY`、`ENT_RE_BELONG`，就把那些 demo 入口拿来写 `gkx_chain`。demo 写图继续只写 `demo_gkx_chain`。

## 目标请求（未上线）

Java 对外路径还没有号。号落地之前，禁止写进 GDF 定时任务。语义先按下面固定。受理超时只等十几秒。`202` 只表示收下了，不表示图已经写完。同一作业还在跑时返回忙，不要并行再打一枪。

```http
POST /ent/v1/graph/jobs/{job}/sync
Content-Type: application/json

{
  "graph_space": "gkx_chain",
  "scope": "batch",
  "gdf_job_id": "GDF-DWD-enterprise_base-日期",
  "source_tables": ["enterprise_base"],
  "dwd_success_at": "2026-11-02T03:10:00+08:00",
  "callback_url": "由 GDF 线下给出"
}
```

`job` 只允许：`enterprise_vertex`、`supply`、`parent_sub`。

立刻：`202`，正文 `{ "task_id", "job", "accepted": true }`。  
忙：`409`，正文 `{ "accepted": false, "reason": "job_busy" }`。

查询：`GET /ent/v1/graph/tasks/{task_id}`。状态只认 `accepted`、`running`、`success`、`failed`、`rejected`。

## 目标回执（未上线）

任务结束至少回一次。GDF 按 `gdf_job_id` 幂等接收。

```json
{
  "gdf_job_id": "GDF-DWD-enterprise_base-日期",
  "task_id": "graph-enterprise_vertex-日期",
  "kind": "graph_job",
  "name": "enterprise_vertex",
  "graph_space": "gkx_chain",
  "status": "success",
  "written_nodes": 0,
  "written_edges": 0,
  "skipped_no_stable_id": 0,
  "error": null
}
```

`status=failed` 必须带 `error`。失败不把图写成已经更新。回执没送到时，用查询结果关单。

## 现在实际怎么交接

对外路径和回执都没有。今天不要配上面的 `POST`。

表 `success` 之后，用飞书或工单交给本侧，写明：作业名、源表、`gdf_job_id`、完成时间。燕大在知识图谱引擎上跑已经配好的脚本，空间是 `gkx_chain`，做完填 [05-回签.md](05-回签.md)。不要把「表洗完了」或「作业受理了」写成「图已经更新」。
