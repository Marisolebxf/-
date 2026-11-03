# POL-L2-DS10-QRY-AUTH-L01 · 收藏与导出解析登录令牌

ponytail: full

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `human:淮政玮` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch`。任务已是 in_progress。本会话不改 task-registry，不把任务标成 done |
| 说明 | 用户授权提交并推送 `origin/dev`。本页不写联调结论 |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 只去掉收藏与导出上的 `@Inner(false)`，与同控制器 `/subscriptions` 一致。未改公共安全组件，未改展示仓，未改 Python。排序保持匿名公开 |

## 范围与实现

展示侧 `RemotePolicyQueryClient` 不标 `@NoToken`，会把浏览器 `Authorization` 转到 `gkxlumen-topic-policy`。`GkxlumenBearerTokenExtractor` 对 `publicUrls` 不读 `Authorization`。`@Inner(false)` 会把路径放进 `publicUrls`，`SecurityUtils.getUser()` 拿不到用户。

本叶从 `PolicyFacadeController` 去掉这 6 个方法上的 `@Inner(false)`，没有改成 `@Inner(true)`：

| 方法 | 路径 |
|------|------|
| `favorites` | `GET /topic/v1/policy/favorites` |
| `saveHistory` | `POST /topic/v1/policy/favorites/history` |
| `replayHistory` | `POST /topic/v1/policy/favorites/history/{id}/search` |
| `saveFavorite` | `POST /topic/v1/policy/favorites` |
| `openFavorite` | `GET /topic/v1/policy/favorites/{policyId}` |
| `share` | `GET /topic/v1/policy/share` |

`GET /rank` 仍是 `@Inner(false)`，排序继续匿名公开。检索、正文、统计、portal、`/{id}` 以及 health、options、graph、metrics、indicators、timeline 的注解未动。

没有令牌时，资源服务器不再把这 6 个路径放进 `permitAll`，请求在过滤器层被拒，到不了控制器。这与同文件的订阅入口相同。

控制器本身没有改身份算法。`currentUserId()` 在 `SecurityUtils.getUser()` 为空或没有 id 时仍返回 null，不采用请求体里的 `user_id`。服务层 `userId` 空白时直接返回空的 history、favorites，`honesty.fabricated=false`，不插入收藏行。单测用 standalone MockMvc，不经过资源服务器：匿名 `GET /favorites` 断言调用 `favorites(null)`，两个列表都空。

展示侧已有的 `PolicyPanoramaQueryController.forward` 会把下游失败收成空列表，并带 `honesty.fabricated=false`。本叶未改这段转发。

## 偏离

无。未改 `gkxlumen-display`，未改 Python，未改 `GkxlumenBearerTokenExtractor`。

## 产物清单

- `repos/lumen-svc-platform` `PolicyFacadeController.java`
- `repos/lumen-svc-platform` `PolicyFacadeControllerTest.java`
- 本 handoff

## 测试结果

`JAVA_HOME=E:\gkx-lumen\worktrees\tooling\jdk\jdk-21.0.12+8`

`mvn -pl gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am test -Dtest=PolicyFacadeControllerTest -Dsurefire.failIfNoSpecifiedTests=false`

`PolicyFacadeControllerTest`：Tests run: 21, Failures: 0, Errors: 0, Skipped: 0。BUILD SUCCESS。

本会话用 Temurin 17（`JAVA_HOME=C:\Users\hzw\AppData\Local\gkx-build-tools\jdk-17.0.20.1+1`）在 `gkxlumen-topic-policy-biz` 再跑同一测试类，结果相同：21 通过，0 失败。

新增 `favoritesAndShareAreNotInnerWhileRankStaysPublic`：上述 6 个方法没有 `@Inner`；`GET /rank` 的 `rank` 仍有 `@Inner(false)`。

## 遗留风险

无令牌时门面拒绝收藏和导出。展示侧已有转发把该失败收成空列表，调用方看到的是空结果加 `honesty.fabricated=false`，不是门面的拒绝体。带令牌的请求才会按登录用户读写收藏和导出对象。

## CI/CD

- 分支：`lumen-svc-platform` `origin/dev`
- commit：`9c7a35ef1075d30f1a6f834f65b36c41e8d18d5a` `fix(policy): 收藏与导出解析登录令牌 [agent:api-agent]`
- push：已推到 `origin/dev`（`3c5d8d6..9c7a35e`）
- 本会话未等 Pipeline
- 本 handoff 在 `gkx-orchestration` `origin/dev`

## 架构合规自检

- 调用链：浏览器仍只打展示资源；展示 Feign 转到 `gkxlumen-topic-policy`。Java 不写算法
- D12：只改 `lumen-svc-platform`，不调用 `demo-*`
- 排序：`GET /rank` 仍 `@Inner(false)`
- 安全组件：未改 `GkxlumenBearerTokenExtractor`
