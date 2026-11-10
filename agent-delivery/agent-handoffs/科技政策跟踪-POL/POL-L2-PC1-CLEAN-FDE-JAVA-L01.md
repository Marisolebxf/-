# POL-L2-PC1-CLEAN-FDE-JAVA-L01 · 602 清洗 · 展示层转发与领域服务只读收口

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | 已代认领。本会话未再 `task-claim`。`task-get` 未返回 `claim_type` |
| 说明 | 开工时状态已是 `in_progress` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单强度一致。未用 YAGNI 跳过公开口 OpenAPI、失败日志里的 traceId、以及 display 只调 element 的调用链 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `POL-L2-PC1-CLEAN-ARCH-SEQ` |
| 图 diff | 本单未改图。对照文末时序：浏览器经网关打 display 两条新口；display 只调 element；element Feign `lumen-algo-py` 的候选与五条判定；准确性由 element 只读 `policy_accuracy_demo` |
| 会签态 | 源文件无 YAML frontmatter。文首写的是「已按当日裁定重写。本稿不写会签结论，不把本单标 done」。本单不自填 approved |
| 说明 | 时序真源 `agent-handoffs/科技政策跟踪-POL/sdd/l2/POL-L2-PC1-CLEAN-ARCH.md`。接口真源同目录 `POL-L2-PC1-CLEAN-API.md` |

## 修改内容

- 公开口在 `gkxlumen-display`：`GET /v1/policy/governance/clean-candidates`、`POST /v1/policy/governance/clean-execute`。网关前缀 `/display`。Swagger `@Tag` / `@Operation` 挂在这两条上。
- display 只调 `RemoteElementClient` 的 element 路径。失败收成 `read_failed` + 「读取失败」，响应里不放 `totalPolicyCount`。
- element 内部口 `@Inner`。候选和五条经 `RemotePolicyCleanClient`（服务名 `lumen-algo-py`，`@NoToken`）打 `GET /internal/policy/clean-candidates` 与 `POST /internal/policy/clean-judge`。不走 `RemotePolicySyncClient`，URL 默认不是 demo 服务。
- 没勾选时执行响应没有批次。启用的五条里，读取失败不占用「成功 / 部分 / 失败」；整批都读失败时批次状态留空。
- 「准确性校验」当时启用才 `SELECT {ads}.policy_accuracy_demo`（`source`、`source_id`、`demo_hit_count`）。没有对应行写「这一条还没有演示数」，不造条数。表不存在或查询失败是这一块的读取失败。
- 未改 `governance/results`。未改 Nacos。

## 测试结果

- `mvn -pl gkxlumen-display,gkxlumen-element spring-javaformat:apply`：SUCCESS。该目标会重排整个模块；无关文件已退回，提交里没有那些重排。
- `mvn -pl gkxlumen-display,gkxlumen-element -am test "-Dtest=PolicyCleanServiceTest" "-Dsurefire.failIfNoSpecifiedTests=false" "-Dmaven.build.cache.enabled=false"`：BUILD SUCCESS。
- display `PolicyCleanServiceTest`：1 通过，0 失败。
- element `PolicyCleanServiceTest`：11 通过，0 失败。不连库。
- JDK `17.0.20.1`，Maven `3.9.9`。

## 遗留风险

- Python 两条内部路由不在本单。下游未就绪时，对应块是读取失败。
- `policy_accuracy_demo` 在数据稿里仍是 draft，列名是中文。Java 按 `source` / `source_id` / `demo_hit_count` 读。物理列对不上时查询失败，返回读取失败，不造数。演示命中说明没有英文字段名，这次没选。
- 架构写明本叶不做分布式锁。另一个实例仍可能再收一次执行。
- 未连库，未在集群上打这两条口。

## CI/CD（必填）

- 分支：`lumen-svc-platform` `dev`
- commit：功能提交 `8e40dc6`；推送后的合并提交 `65f48f4`（`git pull --no-rebase` 一次后推 `origin/dev` 成功）
- pipeline URL / ID：本会话未查
- 部署 namespace / 镜像 tag：未查
- K8s rollout：未查
- dev 测试 URL / 命令与结果：只跑了上面的模块测试，未打 dev 环境

## 可观测性（建议）

- OTEL_SERVICE_NAME：沿用 `gkxlumen-display` / `gkxlumen-element`，本单不新造
- traceId（dev 抽样）：无。失败日志用 `Span.current()` 打当前 traceId；单测里是 `no-trace`
- Tempo / Loki：无

## 涉及文件

- `gkxlumen-display/.../controller/PolicyCleanController.java`
- `gkxlumen-display/.../service/PolicyCleanService.java`
- `gkxlumen-display/.../feign/RemoteElementClient.java`
- `gkxlumen-display/.../service/PolicyCleanServiceTest.java`
- `gkxlumen-element/.../GkxlumenElementApplication.java`
- `gkxlumen-element/.../controller/PolicyCleanController.java`
- `gkxlumen-element/.../feign/RemotePolicyCleanClient.java`
- `gkxlumen-element/.../service/PolicyCleanService.java`
- `gkxlumen-element/.../service/PolicyCleanServiceTest.java`
