# POL-L2-DS10-SENT-JOBQ-L01 · 科创政策全景 · 任务查询端点（display）

- 任务：`POL-L2-DS10-SENT-JOBQ-L01`
- 日期：2026-11-03
- 监管：`human:淮政玮`
- 认领/执行：`agent:api-agent`
- 强度：ponytail full
- 前置：前端伴单 `POL-L2-DS10-SENT-FE-L01`（lumen-ui-science-pc @ `73cc1e8`，其 §5 记录了本端点缺口与补法建议）
- 代码仓：`lumen-svc-platform` @ `origin/dev` commit **`387502a`**（4 文件，+151/−1）

## 1. 问题

`PolicyPanoramaController` 只有 `POST /v1/policy/panorama/jobs`（受理）。前端舆情评估四卡里的「政策实施效果跟踪」「政策匹配与推送」受理后无法轮询、无法当天复用、无法重新分析回读（I2-12 后半段卡在 TODO）。上游 `gkxlumen-topic-async-service` 有 `GET /topic/v1/analysis/tasks/{taskId}`，但浏览器禁止直打（D12 调用链红线：浏览器只打 `/display/**`）。

## 2. 改动（最小 diff，4 文件）

| 文件 | 改动 |
|---|---|
| `gkxlumen-display/.../feign/RemoteTopicAsyncClient.java` | 新增 `detail(taskId, userId)`：`@NoToken @GetMapping("/topic/v1/analysis/tasks/{taskId}")`，风格与同接口 `create` 一致 |
| `gkxlumen-display/.../service/PolicyPanoramaService.java` | 新增 `job(taskId)` 查询方法；类 javadoc 同步（POST 建任务 / GET 查任务同委托 topic-async） |
| `gkxlumen-display/.../controller/PolicyPanoramaController.java` | 新增 `@GetMapping("/jobs/{taskId}")` 委托 `service.job(taskId)` |
| `gkxlumen-display/.../service/PolicyPanoramaServiceTest.java`（测试） | 新增 5 用例（见 §5） |

## 3. 委托链与行为契约

```
浏览器 GET /display/v1/policy/panorama/jobs/{taskId}
  → 网关 StripPrefix=1 → display GET /v1/policy/panorama/jobs/{taskId}
    → PolicyPanoramaController.job → PolicyPanoramaService.job
      → RemoteTopicAsyncClient.detail(taskId, userId)
        → topic-async GET /topic/v1/analysis/tasks/{taskId}（上游已有，归属校验 task.userId == user_id）
```

行为要点（均按任务指令）：

- **原样透传**：display 不改写、不缓存、不造进度百分比。上游 `R<AnalysisTaskEntity>` 成功时取 `data` 放进 `R.ok(data)` 返回；`AnalysisTaskEntity` 的状态字段（`status`/`resultData` 等）前端按 `taskId`/`task_id` 双读法消费（FE handoff §2.3 已兼容）。
- **任务不存在/过期 → 空体**：上游 miss 返回 `R.failed`（HTTP 200，code=1）。display 转为 `R.ok(null)`（HTTP 200 空 data），不 500 不 501，也不把上游内部拒绝语义（「任务不存在/无权/未获取到当前用户」）原样外泄。`FeignException`、空 taskId 同样落空体。
- **鉴权与 POST /jobs 一致**：`user_id` 复用 `currentUserId()`（`SecurityUtils.getUser()`），匿名不补用户（与 `jobs()` 同源同款，无新增注解差异）。Feign 侧 `@NoToken` 与 `create` 相同（服务间无 token 调用声明，仓内既有模式）。
- **未动**：POST /jobs 逻辑零改动；Python、前端、D4 均未触碰。

## 4. 与前端 TODO 对接点

FE handoff（POL-L2-DS10-SENT-FE-L01 §5）写的「缺口补法建议」本单已按原样落地：`GET /display/v1/policy/panorama/jobs/{taskId}` 委托 `GET /topic/v1/analysis/tasks/{taskId}`。前端后续接：

1. **轮询** → 结果渲染：区域效果行 `scope_type=region_effect`、时序 `M_POLICY_IMPLEMENTATION_EFFECT`；匹配行 `policy_title/match_score/match_reasons/rank_no`（实体透传，字段与 topic-async `AnalysisTaskEntity` 序列化一致，`taskId`/`task_id` 双读）
2. **当天复用**：当天已成功同条件直接打开结果
3. **重新分析**：`POST jobs` 传 `force:true`（`jobBodyOf` 已支持，display `toAsyncCreateBody` 白名单含 `force`）

成功响应样例：`{"code":0,"data":{"taskId":"...","status":"success","resultData":"{...}",...}}`；空体：`{"code":0,"data":null}`。running/failed 状态原样透传（前端按 status 分支，不做假进度）。

## 5. 测试

命令（本机 JDK17 + Maven 3.9.9，`C:\Users\hzw\AppData\Local\gkx-build-tools`）：

```
mvn -pl gkxlumen-display -am "-Dtest=PolicyPanoramaServiceTest" "-Dsurefire.failIfNoSpecifiedTests=false" test   # 8/8 绿
mvn -pl gkxlumen-display test   # 全模块回归 43/43 绿
```

新增 5 用例（`PolicyPanoramaServiceTest`）：

| 用例 | 断言 |
|---|---|
| `jobRelaysTaskStatusAndResultVerbatim` | 成功任务原样透传（taskId/status/resultData 不改写） |
| `jobMissingTaskReturnsEmptyBodyNotError` | 上游 R.failed（不存在）/ null（过期）/ FeignException（挂）三种都返回 `code=0 data=null`，不 500 |
| `jobBlankTaskIdShortCircuitsWithoutFeign` | 空白 taskId 直接空体，不打 Feign |
| `jobPassesCurrentUserAsUserIdAndTrims` | 登录态 user_id=7 时以 `"7"` 传上游；taskId 去空白 |
| `jobPathsFollowControllerMapping` | 路由锚点：`/v1/policy/panorama` + `/jobs`（POST）+ `/jobs/{taskId}`（GET） |

## 6. 架构合规自检

- ✅ 调用链：前端 → display REST → topic-async-service（Java→Java Feign），未越层、未直连 Python
- ✅ D12：无 `demo-*` 依赖；浏览器仍只打 `/display/v1/policy/**`
- ✅ 诚实性：不改写状态、不缓存、不造进度；不存在/过期=空体，不伪造任务
- ✅ 鉴权：与 POST /jobs 同源（currentUserId / @NoToken），无新增注解差异
- ✅ 只加不改：POST /jobs 与其余端点零改动（diff 4 文件全部为新增行，唯一删行是 service javadoc 一句话替换）
- ✅ commit `[agent:api-agent]`；push `origin/dev`（pull --no-rebase 后直推成功，无 force）

## 7. 产物清单

- `lumen-svc-platform` @ dev：**`387502a`**（PolicyPanoramaController / PolicyPanoramaService / RemoteTopicAsyncClient / PolicyPanoramaServiceTest）
- 本 handoff（gkx-orchestration @ dev）

## 8. 遗留 / 边界说明

- 本端点只做详情查询（`GET tasks/{taskId}`）。`/result`、`/running`、`/events` 未开透传——前端当前 TODO 只需详情轮询即可闭环（FE handoff §5 补法建议同样只列了详情端点）；若后续要 SSE/事件流再单开任务。
- 未联调（任务指令禁止标注「联调通过」）；上游契约以 topic-async 仓 `AnalysisTaskController.detail` + `loadOwnedTask` 源码为准做了单元级验证。
- 状态推进：留在 in_progress 等监管人验收；task-registry 未动（父会话负责）。

ponytail: full —— 全部改动为增量委托（1 个 Feign 方法 + 1 个 service 方法 + 1 个 controller 端点 + 5 个用例），无新抽象、无新依赖、无配置改动。
