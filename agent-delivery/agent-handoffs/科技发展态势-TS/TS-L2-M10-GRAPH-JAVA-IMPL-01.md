# TS-L2-M10-GRAPH-JAVA-IMPL-01 · 维护技术图谱（34–40）Java 侧实现

- 日期：2026-11-13
- 认领：`agent:api-agent` · 仓库：`repos/lumen-svc-platform`（dev，已 `pull --ff-only` 到 `215de562`）
- 设计真源：`sdd/l2/TS-L2-M10-GRAPH-API.md` v2.1（唯一契约源）、`TS-L2-M10-GRAPH-ARCH.md` v2、`会签/TS-L2-M10-GRAPH-L2-裁定.md`
- 状态：**实现完成，未 commit / 未 push**（按监管人要求，所有仓改完一起看 diff 再提交）

## 1. 改动文件（8 个，全部在 topic / display；未动 gkxlumen-common）

### gkxlumen-topic
| 文件 | 改动 |
|---|---|
| `.../topic/techgraph/TechGraphMaintainController.java` | OPS 白名单 7→10（+`add_node`/`add_edge`/`delete_edge`）；`publish` 加 `@RequestBody(required=false)` 与 `label`/`client_batch_id` 本地校验；新增 `GET /versions`、`GET /versions/{versionId}`、`POST /versions/{versionId}/rollback:preview`、`POST /versions/{versionId}/rollback`；`client_batch_id` ≤64 本地校验；回滚两端点 `base_version` 必填本地校验；`relayCode`：Feign `status<=0`（下游不可达）→ **50303**，50301 不再产生 |
| `.../topic/techgraph/TechGraphMaintainClient.java` | `publishChangeSet` 加 body；新增 `versions` / `versionDetail` / `rollbackPreview` / `rollback` 四个 Feign 方法（`/internal/v1/sci/tech/graph/**`） |

### gkxlumen-display
| 文件 | 改动 |
|---|---|
| `.../display/controller/SituationMaintainEntController.java` | `publish` 加可选 body；新增版本四端点（GET 走 `relay` 匿名只读，POST 走 `relayWrite`）；`changes` / `publish` / `rollback` 用 `SecurityUtils.getUser().getUsername()` 覆盖 body `operator`（`publish`/`rollback` 原 body 为空时合成）；`validate` / `rollback:preview` 走登录守卫但不注入 operator；`relayCode`：下游不可达 → **50303** |
| `.../display/feign/RemoteTechGraphMaintainClient.java` | `publish` 加 body；新增版本四端点 Feign 方法 |
| `.../display/service/SituationPanoramaService.java` | `assemble` 顶层透传 Python 的 `overlay`（仅在 Python 输出该键时追加，叠加关闭时保持逐字节一致）；`category`/`importance`/`origin`/`strengthManual`/`timeRange` 经既有 `maps()`/`normalizeRelation` 原样穿过，未改语义 |

### 单测
| 文件 | 改动 |
|---|---|
| `.../topic/techgraph/TechGraphMaintainControllerTest.java` | 「add_node/add_edge/delete_edge → 400」改正向透传（枚举外仍 400）；50301 断言改为 50302 缺表透传 + 50303 下游不可达；publish 加 body 断言与 label 超长 400；新增版本四端点代理、回滚缺 `base_version` 400、`client_batch_id` 超长 400 |
| `.../display/controller/SituationMaintainEntControllerTest.java` | 50301 → 50303；publish 签名加 body；登录守卫补 rollback/preview；新增 operator 注入（changes/publish/rollback，前端传值被覆盖）、版本 GET 匿名可用透传 |
| `.../display/service/PanoramaReadAssemblyTest.java` | 新增 `overlay` 透传（ok/unavailable）、叠加关闭不输出 `overlay`、节点 `category`/`importance` 与人工边 `origin`/`strengthManual`/`timeRange` 穿透断言 |

## 2. 测试命令与结果

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
mvn -pl gkxlumen-topic,gkxlumen-display -am verify
```

- 结果：**BUILD SUCCESS**
- gkxlumen-topic：**60 tests, 0 failures, 0 errors, 0 skipped**（其中 `TechGraphMaintainControllerTest` 12 个）
- gkxlumen-display：**209 tests, 0 failures, 0 errors, 0 skipped**（其中 `PanoramaReadAssemblyTest` 7 个）
- 合计 269 通过 / 0 失败

## 3. 与契约的一致性

- **无契约冲突**。新端点、错误码（50303 新增、50301 不再产生）、operator 注入点（changes / publish / rollback）、publish body 与 `@RequestBody`（display + topic 两端）均按 API 册 §6.1 / §6.3 / §7、ARCH §6.1 落地。
- `overlay` 透传按 ARCH §4.4-1 / API §6.2 只追加；**全景读图 Python 侧未动**，等 DS02 监管人 `human:淮政玮` 知会回执后再由 PY-IMPL 处理。本次 Java 改动不改全景既有字段语义。
- topic 的 `label ≤128`、`client_batch_id ≤64`、回滚 `base_version` 必填为契约 §7 明列的「topic 本地校验」，按 400/40001 返回；其余取值域（名称唯一、强度、时间范围等）仍由 Python 校验。
- 未改 `gkxlumen-common`，未跑模块级 `spring-javaformat:apply`。

## 4. cost 估算

约 120k input tokens / 25k output tokens（含 3 份设计稿精读、8 个源码/测试文件、全量 `-am verify` 日志）；按平台计价约 $0.5–1 当量。实际耗时约 15 分钟（含 Maven 构建 59s）。
