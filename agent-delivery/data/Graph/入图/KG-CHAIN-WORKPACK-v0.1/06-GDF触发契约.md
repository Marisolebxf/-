# GDF 触发契约

GDF 只洗表、只调度。洗完指定的 DWD 表之后，触发知识图谱引擎上已经配好的入图作业。GDF 不写 Nebula。

受理和回执的形态与企业包相同，现网同样没有对外的 Java 受理。本包不把下面的路径写成已经能调，也不要求今天配进 GDF 的 DAG。企业包里的路径说明见 [06-GDF触发契约.md](../KG-ENT-WORKPACK-v0.1/06-GDF触发契约.md)。

## 第一批：哪张表成功后触发哪次作业

只在该表当天 Wave B 作业 `success` 之后触发。表失败、没跑、只做完贴源，都不触发。

| 顺序 | DWD 表 `success` | 引擎作业 | 写入 | 本版 |
|---|---|---|---|---|
| 1 | `gkxlumenx_dwd.industry_chain_node` | 环节点 | Tag `segment`，VID `segment:{node_id}` | 触发 |

读表和跳过空 ID 的规则在 [01-产业链维需求.md](01-产业链维需求.md)。脚本配置到知识图谱引擎，空间固定 `gkx_chain`。同一次识别如果会带出链，不要把链写入图。

## 本版不触发

| DWD 表 | 原因 |
|---|---|
| `industry_chain` | 写出的是 Tag `chain`，不是环节 |
| `industry_chain_node_rel` | 正式行是 `parent_child`，不能当成 `depends_on` |
| `industry_chain_entity_rel` | 企业到环节要等企业点先在 `gkx_chain` 上。服务机构行正式加工不产。本版不触发 |

不因为 demo 里有 `CHAIN_NER_INDUSTRY`、`CHAIN_RE_DEPENDS_ON`、`CHAIN_RE_INDUSTRY_ENTERPRISE`，就把那些入口拿来写 `gkx_chain`。demo 写图继续只写 `demo_gkx_chain`。

产业链贴源包 `12` 里的 `POST /internal/v1/chain/graph/project` 是我方算法在灌链末段自己跑的上图，给后面的向量索引用，会同时写 `chain` 和 `segment`。那不是交给燕大的作业，也不算本包第一批已经完成。本包只让燕大写 `segment`。

## 目标请求（未上线）

Java 对外路径还没有号。号落地之前，禁止写进 GDF 定时任务。`202` 只表示收下了。同一作业还在跑时返回忙。

```http
POST /chain/v1/graph/jobs/{job}/sync
Content-Type: application/json

{
  "graph_space": "gkx_chain",
  "scope": "batch",
  "gdf_job_id": "GDF-DWD-industry_chain_node-日期",
  "source_tables": ["industry_chain_node"],
  "dwd_success_at": "2026-11-02T03:10:00+08:00",
  "callback_url": "由 GDF 线下给出"
}
```

`job` 本版只允许：`segment_vertex`。

立刻：`202`，正文 `{ "task_id", "job", "accepted": true }`。  
忙：`409`，正文 `{ "accepted": false, "reason": "job_busy" }`。

查询：`GET /chain/v1/graph/tasks/{task_id}`。状态只认 `accepted`、`running`、`success`、`failed`、`rejected`。

回执字段与企业包相同：`gdf_job_id`、`task_id`、`kind=graph_job`、`name`、`graph_space`、`status`、`written_nodes`、`written_edges`、`skipped_no_stable_id`、`error`。`status=failed` 必须带 `error`。

## 现在实际怎么交接

今天不要配上面的 `POST`。

`industry_chain_node` 成功之后，用飞书或工单交给本侧，写明：作业名、源表、`gdf_job_id`、完成时间。燕大在知识图谱引擎上跑已经配好的脚本，空间是 `gkx_chain`，做完填 [05-回签.md](05-回签.md)。不要把「表洗完了」或「作业受理了」写成「图已经更新」。
