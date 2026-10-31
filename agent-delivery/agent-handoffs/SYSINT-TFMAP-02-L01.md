# SYSINT-TFMAP-02-L01 · 技术领域与产业节点关联：子学科同步进本侧表，LLM 关联产业节点

> 范围真源：`agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TFMAP-02-L01.md`（origin/dev `1ed5b9d8`）。图 `SYSINT-TFMAP-02-SEQ` 在该文件「调用时序」。图文冲突以图为准。本叶按该图实现。2026-10-31 用户下令完成并验收。下文「测试结果」是 2026-10-28 当时的记录，以文末复核为准。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 2026-10-28 用户下令认领。`claimed_at` `2026-10-28T11:44:08+08:00`，`lock_until` `2026-10-28T19:44:08+08:00`。依赖 `SYSINT-DICT-02-L01` 在登记表仍是 `in_progress`，子学科字典接口已按派单上线，用户命令开工，未因该依赖停工。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用产业集群映射页、gkx-innov 写库池和 lumen-algo-py 已有智谱客户端。未新加 npm / Maven / pip 包。未跳过调用链、可观测和 handoff。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-TFMAP-02-SEQ` |
| 图 diff | 未改图。实现按图的三条边：同步经字典写入本侧表；关联经 lumen-algo-py `/internal` 再校验写入；统计和关键字查询只读本侧表。 |
| 会签态 | 派单文件未标 `approved`。按用户 2026-10-28 开工令实现，不把会签态改绿。 |
| 说明 | Java 在写入前再丢弃不在候选内的节点 id，与派单正文一致，不改变图上的调用方向。 |

## 范围

- 关联做成与 `industry_cluster_map` 同一业务库的固定表。其他模块只读这张表。同步才打子学科字典。关联才调模型。查询和统计不打字典、不调模型。
- 菜单在 demo-ui-system-test「维护管理」，与「产业集群映射」并列。路由在现有 ops 下。
- 不改政策三页提交逻辑，不替换政策页产业集群下拉。不建技术链、人才、科研机构深度分析页。不改 iticsci 专题仓。不用久新 `ads_industry.industry_id` 充当本侧产业节点。`company` 不作为科研机构。`lumen-topic-py` 字典实现未改。

## 表名

`demo_gkxlumenx_dim.subfield_topic_map`（schema 来自 `gkx.innov.cluster.dim-schema`，默认与产业集群映射同一 dim 库）。

一张表。每个 `subfield_id` 至少一行目录（中文名、`data_version`、`synced_at`）。未映射行的 `node_id` 为空。已映射是同一 `subfield_id` 下每个通过校验的产业节点一行（`node_id`、`industry_id`、`cluster_id`、名称、`model_name`、`linked_at`）。同步只更新已有行的名称、版本和同步时间；没有行才插入空关联占位。不整表清空，不删已有关联。首次成功写入至少一条关联后，才删掉该子学科的空占位行。

表在进程内 `CREATE TABLE IF NOT EXISTS`，没有 Flyway。本会话没有连库建表。账号没有建表权限时接口返回「映射表不可用」，不假装成功。

## 菜单路径

维护管理 → 子学科与专题映射。路由 `/ops/subfield-topic`。菜单项在 `src/views/ops/opsMenuConfig.ts` 的 `OPS_SUB_MENU`。

## 接口路径

页面经 demo 网关（`StripPrefix=1`）：

| 动作 | 页面 | gkx-innov |
|------|------|-----------|
| 同步 | `POST /ops/v1/subfield-topic-maps/sync` | `POST /v1/subfield-topic-maps/sync` |
| 关联 | `POST /ops/v1/subfield-topic-maps/link` | `POST /v1/subfield-topic-maps/link` |
| 统计 | `GET /ops/v1/subfield-topic-maps/stats` | `GET /v1/subfield-topic-maps/stats` |
| 关键字查询 | `GET /ops/v1/subfield-topic-maps/query` | `GET /v1/subfield-topic-maps/query` |

同步下游：`POST /internal/gkx-svc/dict/query`（`lumen-topic-py`，Feign 名 `lumen-topic-dict`，默认 `http://gkxlumen-platform-search-py:8080`）。

关联下游：`POST /internal/subfield-topic/link`（`lumen-algo-py`，Feign 名 `lumen-algo-subfield-topic`，默认 `http://lumen-platform-algo-py:8000`）。

统计标题常量「子学科与专题映射」。已映射 = 至少一条非空且通过校验的 `node_id`。未映射 = 已同步但没有关联。两边都返回中文名、`subfield_id` 和两侧数量。关键字为空不扫描、不调字典、不调模型。

## LLM 落点

只在 `lumen-algo-py`：`lumen_common/algorithms/subfield_topic.py` 复用已有 `OpenAICompatibleClient`。提示词只在 Python。Java 只传子学科 `{subfield_id, name_zh}` 和本侧候选 `{node_id, node_name, industry_id, cluster_id}`，不写提示词，不直连模型。返回的 `node_id` 不在候选内则丢弃，该子学科保持未映射。没有密钥时接口 503，正文含 `LLM API key not configured`，不写假关联。本侧没有产业节点时不调模型。按批 20 条。某批传输或模型失败则停，已写入的批保留，未完成行不标已映射。模型名来自 Python 响应，不填假名。密钥不进 git。Java 写库沿用 gkx-innov 已有业务账号，不用只读账号 `test2`。

## 本侧目录缺口

2026-10-28 对业务库只读计数（与产业集群映射同一主机、同一业务账号，未打印口令）：

| 目录 | 计数 |
|------|------|
| `demo_gkxlumenx_dim` 中 `CL-*` 且启用的集群 | 15 |
| `industry_cluster_map` 启用行 / 去重 `industry_id` | 50 / 42 |
| 其中同时挂在两个集群上的产业 | 8 |
| `demo_gkxlumenx_dwd.industry_chain_node` 未删除行 / 去重 `node_id` | 222 / 194 |
| 上述产业与 demo 链节点产业的交集 | 14 |
| 逻辑库 `gkxlumenx_dwd` 与这 42 个产业的交集 | 0 |

因此节点 SQL 走 `DataPlane.qualifyInnovSql`，读 `demo_gkxlumenx_dwd`。不读交集为 0 的逻辑库，也不用久新 `ads_industry`。

缺口（代码会写入 `catalog_gaps`，不编造节点）：

- `chain_node_partial`：42 个已挂产业里只有 14 个在 demo 链节点上有节点。没有节点的产业不进入候选。
- `industry_multi_cluster`：8 个产业同时挂在两个集群上。不猜其中一个，这些产业的集群列留空，产业和节点仍可作为候选。
- `node_id_ambiguous`：同一 `node_id` 跨多个产业时整组丢弃。本会话没有单独数出被丢弃的个数。
- `chain_node`：只有候选节点为空时才出现。当前 demo 平面有节点，关联会调用模型（密钥缺失则失败并保持未映射）。

跨命名空间短名 `gkxlumen-platform-search-py`、`lumen-platform-algo-py` 未在本会话验证解析。网关路由和 Helm 环境变量已写在仓内，未发布。

## 修改内容

- demo-ui-system-test：ops 菜单、路由、子学科映射页和 API；产业集群映射页头上的集群说明从公共头挪回该页，避免新页误显示。
- demo-svc-platform gkx-innov：映射表、同步 / 关联 / 统计 / 查询，以及网关路由和两个下游基址（无密钥）。
- lumen-algo-py：`POST /internal/subfield-topic/link`。沿用服务已有 TraceHeaderMiddleware，未另接一套追踪。
- lumen-topic-py：未改。

## 测试结果

- `lumen-algo-py`：`pytest tests/test_subfield_topic_link.py`，3 通过。覆盖无密钥失败、候选外节点丢弃、路由 503 且不返回假关联。
- `SubfieldTopicLogicTest`：离线 JUnit，`tests=3 failed=0`。覆盖同步不删除已离开字典的 id、候选外节点丢弃、关键字只匹配中文名或 id。
- `mvn -pl gkx-innov` 未编译。本机解析不到 `nexus.rd.com`，离线也缺 `feign-micrometer`。Spring 服务没有启动。
- 映射表未在库里创建。同步、关联、统计、关键字查询没有打到运行中的 gkx-innov。
- demo-ui-system-test 本机没有在跑的 dev server。浏览器没有走菜单、同步、统计和关键字查询。
- 未部署。无 pipeline、无镜像、无 K8s rollout、无 traceId。

## 架构合规

- 调用链：页面 → demo 网关 → gkx-innov →（同步）lumen-topic-py 字典；（关联）lumen-algo-py `/internal`。前端不直连 Python、久新或模型。
- 算法只在 Python。Java 只转发和校验 id。
- 密钥不进 git。未新增口令或模型密钥。Java 不用 `test2`。
- D12：改动在 demo-ui-system-test、demo-svc-platform 和 lumen-algo-py。未把 demo 服务接到 lumen 前端。
- 本页数字是维护统计，不加指标 ⓘ。

## 问题清单

- 登记表里 `SYSINT-DICT-02-L01` 仍是 `in_progress`。用户已命令开工。本会话没有再数子学科接口条数。
- 认领提交在干净 worktree，推 origin/dev 若被网关 403 挡住，则 origin/dev 仍看不到认领字段和本 handoff。主仓工作区的 `task-registry.yaml` 不提交。

## 遗留风险

- 建表权限、字典 Feign、算法 Feign 和网关发布都未在运行环境验证。没有模型密钥时关联失败是预期，失败行保持未映射。
- 28 个已挂产业没有 demo 链节点。关联只能覆盖有节点的 14 个产业。8 个双集群产业的集群列为空。
- 运行时建表。表结构漂移后需要正式迁移，不能靠 `CREATE TABLE IF NOT EXISTS` 改列。

## CI/CD（必填）

- 分支：业务仓改动停在本地 `dev` 工作区，未 commit、未 push。
- commit：业务仓无。编排仓见本次 handoff 提交。
- pipeline URL / ID：无。
- 部署 namespace / 镜像 tag：无。
- K8s rollout：未部署。
- dev 测试 URL / 命令与结果：见「测试结果」。页面和后端接口未在浏览器或运行服务上验证。

## 可观测性（建议）

- OTEL_SERVICE_NAME：未新增。Python 路由挂在已有 lumen-algo-py 应用上。
- traceId（dev 抽样）：无。
- Tempo / Loki：无。

## 涉及文件

- `repos/demo-ui-system-test`：`src/views/ops/opsMenuConfig.ts`、`src/views/ops/index.vue`、`src/views/ops/pages/ClusterMapPage.vue`、`src/views/ops/pages/SubfieldTopicPage.vue`、`src/router/index.ts`、`src/api/subfield-topic/index.ts`
- `repos/demo-svc-platform`：`gkx-innov` 包 `com.topcomm.gkx.innov.subfield`、`gkx-innov/src/main/resources/application.yml`、`helm/gkx-platform/configs/gkx-gateway-dev.yml`、`helm/gkx-platform/values.yaml`
- `repos/lumen-algo-py`：`lumen_common/algorithms/subfield_topic.py`、`lumen_algo_service/views/subfield_topic.py`、`lumen_algo_service/main.py`、`tests/test_subfield_topic_link.py`
- `agent-delivery/agent-handoffs/SYSINT-TFMAP-02-L01.md`

## 2026-10-31 复核

对 `10.50.11.76` 上的 `demo_gkxlumenx_dim.subfield_topic_map` 只读计数（未打印口令）：

| 项 | 值 |
|---|---|
| 行数 | 390 |
| 子学科 | 252 |
| 已映射子学科（至少一条非空 `node_id`） | 130 |
| 关联行 / 空关联行 | 268 / 122 |
| `synced_at` | 2026-10-29 22:54:51 至 22:59:41 |
| `linked_at` 最晚 | 2026-10-29 22:59:41 |

表结构与代码里的 `CREATE TABLE` 一致。同步和关联已经在 demo 库留下结果。本会话没有再点菜单，也没有重跑同步或关联。

三仓代码在 `origin/dev`，工作区对这批文件是干净的：

- `demo-ui-system-test`：`ab985e5`、`9007013`、`107764f`
- `demo-svc-platform`：`af8144c`、`67a80d5`、`d6064d3`
- `lumen-algo-py`：`6ffece8`

## 范围与实现

DoD 对照：映射表已落在 `demo_gkxlumenx_dim.subfield_topic_map`。菜单、同步、关联、统计和关键字查询的代码已在 `origin/dev`。已映射 130、未映射为已同步但没有 `node_id` 的子学科。本会话用库内行数核对，没有再走浏览器。

## 偏离

2026-10-28 交接写过「表未建、未部署、页面未点」。2026-10-29 库内已有同步和关联结果，该句作废。本会话仍未再点页面。

## 产物清单

- 表：`demo_gkxlumenx_dim.subfield_topic_map`
- 菜单：维护管理 → 子学科与专题映射，`/ops/subfield-topic`
- 上文「涉及文件」和三仓 commit

## 验收证据

2026-10-31 只读计数见上表。用户当日下令验收。证据路径即本 handoff。

## 架构合规自检

- ✅ 调用链：页面 → demo 网关 → gkx-innov；同步再走字典，关联再走 lumen-algo-py `/internal`
- ✅ 算法只在 Python。Java 只转发和校验 id
- ✅ 图谱：本叶不写图库
- ✅ 可观测：Python 路由挂在已有 lumen-algo-py 应用上
- ✅ 密钥不进 git
- ✅ D12：未把 demo 服务接到 lumen 前端
- ✅ 本页数字是维护统计，不加指标 ⓘ

## Cost 回填

本会话没有 Console 精确数。验收复核按会话量级记一笔，价表没有 Grok 档，按主力档（输入 $3/M、输出 $15/M，算法 75/25）估算。

- actual_tokens: 25000
- model_used: grok-4.7
- actual_cost: 0.15
- cost_warn: green

ponytail: full
