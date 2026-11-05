# SYSINT-TOPICMAP-02-L01 · Topic 与产业节点映射

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:algorithm-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `pull` |
| 说明 | 2026-11-05 监管人下令领取并执行。backlog → ready → claimed → in_progress。不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。调用链、向量只在 Python、网关路由都留了。候选向量缓存在进程内，目录变了才重算。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SYSINT-TOPICMAP-02-SEQ` |
| 图 diff | 时序图写在派单里，本叶按该图实现，没有另改图。 |
| 会签态 | 派单没有 frontmatter，不填 approved。 |
| 说明 | 图文以派单「调用时序」为准。 |

## 修改内容

菜单「Topic与产业映射」，路由 `/ops/topic-map`，排在「技术节点与产业映射」下面。打开页面和查询不触发同步，也不触发向量。

- 字典：`lumen-topic-py` 的 `op=discipline_topic_page` 指向已有 `topic_page`，不另写 SQL。条目补了 `name_zh`（原来只有 `name`）。每页最多 500。
- 本侧表：`dwd_discipline_topic`（按 `topic_id` upsert）和 `dwd_topic_industry_map`（未关联保留 `node_id` 空）。不写 `subfield_topic_map`，不写 `dwd_tech_node_industry_map`。表在服务第一次【同步】时创建，库名走现有 `INNOV_DWD_SCHEMA`，SQL 经 `DataPlane.qualifyInnovSql` 落到 demo 库。
- 关联：人点击后 Java 一次送 20 个未关联 Topic。`lumen-algo-py` `POST /internal/topic-industry/link` 用名称向量，每个 Topic 只留余弦最近的一个本侧产业节点。该节点挂几个集群就写几行。返回的 `node_id` 不在候选里由 Java 丢掉。
- 网关：`gkxx.sys_route_conf` 与 Redis `gl:gateway_route_key` 都有 `gkx-ops-topic-maps`，过滤器 `[]`，与已上线的 `gkx-ops-tech-node-maps` 相同。只发了 `gateway_jvm_route_reload_topic`，没有发 `upms_redis_route_reload_topic`。helm 文件里的同名条目跟着同文件的技术节点路由写了 `StripPrefix=1`；运行时以 Redis 的空过滤器为准。

## 测试结果

- `lumen-algo-py`：`python -m pytest tests/test_topic_industry_link.py -q`，1 通过。较近候选被选中，links 里没有候选外的 id。
- `lumen-topic-py`：`python -m pytest tests/test_jx_dict.py::test_discipline_topic_page_reuses_topic_page tests/test_jx_dict.py::test_unknown_op -q`，2 通过。
- `demo-svc-platform`：本机没有 `mvn` / `java`，`TopicMapLogicTest` 没跑。
- 网关：`GET http://10.50.69.111:30889/api/ops/v1/topic-maps/stats` 为 424 `token expired`，`X-Trace-Id` `cc621aecad60c95cd1d82d4410ad29f1`。不存在的路径 `/api/ops/v1/topic-maps-nope/stats` 为 404。同机技术节点路由同样是 424。
- 页面还没进当前运行的前端镜像，没有在浏览器里点【同步】【关联】。表要等新镜像起来、有人点【同步】之后才出现。

## 遗留风险

- CI 发布完成前，菜单和接口不在正在跑的 Pod 里。路由已经在网关，下游还是旧镜像时，登录后调用会落到旧服务。
- 4,516 个 Topic 按每批 20 个关联，大约 226 批。本叶没有点【关联】灌数。
- helm 静态路由如果以后和 Redis 路由叠在一起，`StripPrefix` 可能被执行两次。技术节点路由现在就是这种文件/现网不一致，本叶没有改它。

## CI/CD（必填）

- 分支：各仓 `origin/dev`
- commit：
  - `lumen-algo-py` `b67f96a`
  - `lumen-topic-py` `c0dae58`
  - `demo-svc-platform` `a8cc7db`
  - `demo-ui-system-test` `ae43cb7`
- pipeline URL / ID：本叶没有查流水线。
- 部署 namespace / 镜像 tag：未见新镜像。
- K8s rollout：未做。
- dev 测试 URL：网关 424 / 404 对照见测试结果。页面 URL 待发布后是算法中台维护管理 `/ops/topic-map`。

## 可观测性（建议）

- 新 Python 路由沿用进程内已有 OTel，没有另建 tracer。
- traceId（dev 抽样）：`cc621aecad60c95cd1d82d4410ad29f1`（未登录，网关 424）。
- Tempo / Loki：未查。

## 涉及文件

- `lumen-algo-py`：`lumen_common/algorithms/topic_industry.py`，`lumen_algo_service/views/topic_industry.py`，`lumen_algo_service/main.py`，`tests/test_topic_industry_link.py`
- `lumen-topic-py`：`gkx_svc_service/jx_dict.py`，`tests/test_jx_dict.py`
- `demo-svc-platform`：`gkx-innov/.../topicmap/*`，`application.yml`，`helm/.../gkx-gateway-dev.yml`，`db/10_sys_route_conf_topic_maps.sql`
- `demo-ui-system-test`：`src/views/ops/pages/TopicMapPage.vue`，`src/api/topic-map/index.ts`，`src/views/ops/opsMenuConfig.ts`，`src/router/index.ts`
- 派单：`agent-delivery/工程过程/04-系统集成/02-对接三要素/派单说明-SYSINT-TOPICMAP-02-L01.md`

## 架构合规自检

- 前端不直连 Python、久新或模型。Java 不算向量。✅
- 不写另外两张映射表，不改政策三页，不建深度页，不改 iticsci。✅
- 密码和模型密钥不进 git。✅
- lumen 前端不调用这个 demo 中台。✅
- 不把任务标 done。✅
