# SYSINT-05-01B-L01 · 科学技术全景后端装配读图

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:唐绍祖` |
| claim_type | task-get 未返回该字段。开工时状态已是 `in_progress` |
| 说明 | 不改 task-registry，不把任务标 done |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 display 已有的 Feign + `R` 包络。图只经 Python 读，三个数字只 SELECT 分数表。未跳过调用链、D12、D18 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `TS-L2-DS02-ARCH-SEQ`、`TS-L2-DS02-SDD-SEQ` |
| 图 diff | 代码按说明书第 3、4 节接上：页 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `POST /internal/tech-graph/read` → `demo_gkx_chain`；影响力、中心度、路径优先级由 display 按编号只读 `ads_technology_panorama_score`。没有改图 |
| 会签态 | 源文件无 frontmatter。功能架构与说明书已签收。本装配单待联调 |
| 说明 | 不经 `gkxlumen-graph`，不调用 `demo-*`，不改去 `gkx_chain` 或 `entan` |

## 修改内容

- 对外仍是 `POST /display/v1/situation/panorama/graph`（服务内 `/v1/situation/panorama/graph`）。七个字段：`nodes`、`relations`、`keyPathOptions`、`timeline`、`listRecords`、`relationTypeOptions`、`factorItems`。超过上限时多一个 `truncated` 标记，不是第八块业务数据。
- `RemoteTechGraphClient` 直连 `lumen-platform-algo-py` 的 `POST /internal/tech-graph/read`。请求带 `space=demo_gkx_chain`、可选 `techPointId` / `keyword` / `fieldValues` / `includeLowEvidence`，以及上限 200 / 200 / 20 / 20。响应 `space` 不是 `demo_gkx_chain` 则 502。`code` 非 0、连不上、没有 `data`，同样 502，响应里没有七个空数组，也没有 `GRAPH_NOT_READY`。
- 读到的点、关系、实体、路径装进七个字段。未选技术点时只留最多 200 个点，不带边、不带实体、不带路径。选中后丢掉低证据（请求明确 `includeLowEvidence=true` 才保留），关系 200、每类实体 20、路径 20。`currentYear` 只回写时间轴游标，不换图。中文名用 `name_zh`，英文不抄进中文。
- 点列表为空时 `emptyReason=GRAPH_EMPTY`。有点则不带 `emptyReason`。
- 三个数字：`JdbcPanoramaScores` 对 `demo_gkxlumenx_ads.ads_technology_panorama_score` 做只读 `SELECT subject_id, score_kind, score_value`。`influence` 填到实体 `listRecords[].influence`，`centrality` 填到点 `nodes[].centrality`，`path_priority` 填到 `keyPathOptions[].pathPriority`。无行、表不在、连不上，这三格为 null，名单和路径仍返回。请求里不 INSERT / UPDATE。Python 载荷里自带的这三个数会被剥掉，避免把写死分数透传出去。
- 序号 17：`POST /import`、`POST /manual`，以及 `/graph` 里带导入/写入动作，返回 501，不落库。序号 26：`POST /entity-relations`，以及 `/graph` 里 `entityRelations=true`，返回 501。没有新造写入库的接口。

## 测试结果

- `mvn -pl gkxlumen-display -Dtest=SituationPanoramaControllerTest,PanoramaReadAssemblyTest test`
- 模块编译通过（57 个主源文件）。上述测试 12 个，失败 0。`BUILD SUCCESS`（2026-11-05 22:05）。
- 覆盖：空图 `GRAPH_EMPTY`；读失败与错误空间为 502 且 `data` 为 null；未选点不带边；选中后低证据默认去掉、三个数字只来自分数表；顶点/边别名能装配；写入与实体间关系 501 且不调用读图；分数 SQL 只读该 ADS 表，表不存在时三个数字的查找结果为空。
- 未跑 display 模块其余测试。未打线上。

## 遗留风险

- `POST /internal/tech-graph/read` 的代码已在 `lumen-algo-py` `origin/dev`（`a03c52b`）。镜像未滚到集群时，本接口仍返回 502，不再用 `GRAPH_NOT_READY` 空壳。Python 侧按上面的请求体和 `data` 字段对齐；也认 `vertices` / `edges` / `entities` / `paths`。
- 分数表由 `TS-L2-DS02-SCORE-L01` 建。列约定是 `subject_id`、`score_kind`（`influence` / `centrality` / `path_priority`）、`score_value`。列名不同会被当成没有行。
- 集群里 display 还没有 `DISPLAY_ADS_PASSWORD`。未设置时再看环境变量 `ELEMENT_MYSQL_PASSWORD`。两个都空则连库失败，三个数字留空，图仍返回。默认 JDBC 指向 `10.50.11.76:3306/demo_gkxlumenx_ads`，用户 `gkxlumenx`。本次没改 Helm。
- 现有前端 `optionalPost` 把 404/405/501 收成手写空形状。读图失败是 502，会抛错。写操作的 501 仍会被这条前端逻辑收成空形状，要等 `SYSINT-05-01A-L01` 改接线。
- 领域筛选只在点上已经带 `industryId` / `industryIds` / `fieldValues` 时由 Java 再滤一层。都没有这些字段时，原样转发 `fieldValues`，由 Python 滤。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `dev`
- commit：`cbd6f10e1836ec0c0a7510d4ecdf1dffa708ca09`
- push：`origin/dev`（`0c69f1a..cbd6f10`）。未 force，未推 main
- pipeline URL / ID：未查
- 部署 namespace / 镜像 tag：未查
- K8s rollout：未查
- dev 测试 URL / 命令与结果：只跑了上面的模块测试

## 架构合规自检

1. 算法只在 Python。Java 不写 nGQL，不算影响力、中心度、路径优先级。✅
2. 调用链：浏览器 → 网关 `/display/**` → `gkxlumen-display` → `lumen-algo-py` `/internal/tech-graph/read` → `demo_gkx_chain`。✅
3. 图谱不直连、不经 `gkxlumen-graph`。✅
4. 可观测沿用 display 已有 Java Agent，本叶不另建 tracer。✅
5. 已 push `origin/dev`。CI 结果未查。✅（未宣称绿）
6. D12：Feign 名是 `lumen-platform-algo-py`，不调用 `demo-*`。✅
7. D18：三个数字只读 ADS 表。表不在或无行则格子空。接口不写死分数，不回退 fixture。D4 仍是 mock，本叶不改。✅

## 涉及文件

- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/controller/SituationPanoramaController.java`
- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/SituationPanoramaService.java`
- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/TechGraphReader.java`
- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/TechGraphReadAdapter.java`
- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/feign/RemoteTechGraphClient.java`
- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/PanoramaScores.java`
- `gkxlumen-display/src/main/java/com/topcomm/gkxlumen/display/service/JdbcPanoramaScores.java`
- `gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/controller/SituationPanoramaControllerTest.java`
- `gkxlumen-display/src/test/java/com/topcomm/gkxlumen/display/service/PanoramaReadAssemblyTest.java`
- `gkxlumen-display/pom.xml`（增加 `mysql-connector-j`，不启用 `spring.datasource`）
- `gkxlumen-display/src/main/resources/application.yml`
- `gkxlumen-display/src/main/resources/application-local.yml`（本地读图地址 `http://127.0.0.1:8000`）

## 范围与实现

对外仍是一次 `POST /display/v1/situation/panorama/graph`。Java 调 Python 读图，三个数字只读分数表。不写假数。三要素算法不在本叶。

## 偏离

无偏离。读失败用 502，不再用 `GRAPH_NOT_READY` 空壳。

## 产物清单

- `lumen-svc-platform` `cbd6f10`
- 本交接

## 验收证据

`mvn -pl gkxlumen-display -Dtest=SituationPanoramaControllerTest,PanoramaReadAssemblyTest test`：12 个用例，失败 0。

## Cost 回填

- actual_tokens: 80000
- model_used: claude-sonnet-4.5
- actual_cost: 0.43
- cost_warn: green
- 会话模型为 Grok 4.7。注册表枚举无此项，按 sonnet 单价与 api 80/20 计入。

## 未做

- 未改 `lumen-algo-py`。读图代码已由 `TS-L2-DS02-READ-PY-L01` 推到 `origin/dev`，本会话未核对该镜像是否已发布。
- 未建、未灌 `ads_technology_panorama_score`。
- 未改 Helm / Nacos，未给 display 配 `DISPLAY_ADS_PASSWORD`。
- 未改前端。未提交 `gkx-orchestration`。未改 task-registry，未标 done。
- `spring-javaformat:apply` 跑在 `gkxlumen-display`。它顺手改了模块里无关文件，那些格式化差异没有提交。
