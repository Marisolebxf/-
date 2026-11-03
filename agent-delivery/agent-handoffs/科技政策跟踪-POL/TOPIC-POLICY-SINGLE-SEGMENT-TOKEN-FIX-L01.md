# TOPIC-POLICY-SINGLE-SEGMENT-TOKEN-FIX-L01 — 单段路径令牌被吞修复交接

- **任务**：修复 gkxlumen-topic-policy 单段用户路径（favorites/share/subscriptions）带 Bearer 令牌仍匿名
- **agent**：api-agent（监管人 human:淮政玮）
- **日期**：2026-11-04
- **强度**：ponytail full
- **代码仓 commit**：lumen-svc-platform `dev` 分支 `6c9a60d`（`a0f9e46..6c9a60d`，已推 origin/dev）
- **交接仓 commit**：本文件所在 commit（worktree `E:/zhipu/gkx-lumen/worktrees/gkx-orchestration--POLICY-TOKEN-FIX`，基于 origin/dev `cdee88cc`，用后即删）

---

## 1. 现象

gkxlumen-topic-policy 线上（镜像 a0f9e465，含此前修复 9c7a35e）：

- `GET /topic/v1/policy/favorites`、`/share`、`/subscriptions` **带合法 Bearer 令牌**仍返回匿名（`honesty.unavailable:anonymous`）——令牌被静默吞掉。
- 对照组：两段路径 `GET /topic/v1/policy/favorites/history` 带假令牌正确 401（令牌被正常解析）。
- 对照组：gkxlumen-display 的 `/v1/policy/panorama/favorites` 带假令牌正确 401（display 无单段 `{id}` 兜底）。

## 2. 线上证据（curl 对照表）

| 路径 | 令牌 | 修复前表现 | 结论 |
|---|---|---|---|
| `/topic/v1/policy/favorites` | 合法 Bearer | 200，`unavailable:anonymous` | ❌ 令牌被吞 |
| `/topic/v1/policy/share` | 合法 Bearer | 200，`unavailable:anonymous` | ❌ 令牌被吞 |
| `/topic/v1/policy/subscriptions` | 合法 Bearer | 200，`unavailable:anonymous` | ❌ 令牌被吞 |
| `/topic/v1/policy/favorites/history` | 假 Bearer | 401 | ✅ 两段路径不受影响 |
| `/display/v1/policy/panorama/favorites` | 假 Bearer | 401 | ✅ display 无此问题 |

（线上实证由监管人/派单完成，本单不重复诊断。）

## 3. 根因链（线上已验证）

1. `PolicyFacadeController.getById` 兜底 `@GetMapping("/{id}")` 标了 `@Inner(false)`。
2. `gkxlumen-common-security` 的 `PermitAllUrlProperties.afterPropertiesSet` 把 `{id}` 经 `ReUtil.replaceAll(url, "\\{(.*?)\\}", "*")` 转成 `/topic/v1/policy/*` 加进 `publicUrls`。
3. `AntPathMatcher` 单段通配 `*` 命中同级全部单段静态路径（favorites/share/subscriptions）。
4. `GkxlumenBearerTokenExtractor.resolve` 对 publicUrls 命中路径直接 `return null` 不读 `Authorization` → `SecurityUtils.getUser()` 为空 → 匿名。
5. 对照组 gkxlumen-display 无单段 `{id}` 兜底，故其 favorites 正常。

## 4. 方案取舍（选 A）

**选 A：去掉 getById 兜底上的 `@Inner(false)`。**

### 选 A 的依据（匿名消费者核查，全部为零）

| 潜在调用方 | 核查结果 |
|---|---|
| lumen-ui-topic 前端 | 详情一律走 `/docs/{id}`：`src/api/policy/paths.ts` 的 `policyDocsPath()` 拼 `PolicyTopicPaths.docs + '/' + id`，仓内无单段 `{id}` 调用 |
| lumen-ui-science-pc 前端 | 走 `/display/v1/policy/panorama/**`，自查脚本断言**禁止**出现 `/policy/topic` 与 `/topic/v1/policy`（FE-POL-SENT-LIVE.test.mjs:245,292-294），无单段调用 |
| demo-ui-topic 前端 | 全仓 `topic/v1/policy` 零匹配 |
| gkxlumen-display Feign | `RemoteTopicPolicyClient.docs` 用 `/topic/v1/policy/docs/{id}`，注释明写「**不走 `/{id}` 兜底**」；`RemotePolicyQueryClient`/`RemotePolicySubscriptionClient` 只调 favorites/share/subscriptions 等静态段 |
| gkxlumen-cms | `SmartSearchService` 只调 `/topic/v1/policy/search` |
| 网关路由 | `helm/gkxlumen-platform/configs/gkxlumen-gateway-dev.yml` 只做 `Path=/policy/**` → StripPrefix 转发，不消费 `{id}` 语义 |

### 不选 B 的理由

改 `PermitAllUrlProperties`（如跳过含 `*` 的单段 pattern 登记、或「静态兄弟排除」）是**全仓公共组件语义变更**：所有 `@Inner(false)` 服务的 permitAll 行为都会变，需要逐一评估每个服务的暴露面（见 §8 清单），风险与本次「只修一个已确诊 bug」的范围不符。留作后续架构任务（若登记为治理项再动）。

### 选 A 后的行为变化（如实声明）

- `/{id}`（如 `/topic/v1/policy/pol-123`）**匿名不可用**（会被 `anyRequest().authenticated()` 拦 401），**带有效令牌可用**；
- 匿名详情需求由 `/docs/{id}`（保留 `@Inner(false)`）承接，语义不变；
- favorites/share/subscriptions 恢复令牌解析：无效令牌 401、有效令牌出用户。

## 5. 改动清单（lumen-svc-platform，2 文件 +94/-3）

1. `gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/main/java/com/topcomm/gkxlumen/topic/policy/controller/PolicyFacadeController.java`
   - `getById` 兜底去掉 `@Inner(value = false)`；javadoc 补根因说明；`@Operation(summary)` 改「政策详情（兜底，需令牌）」。
2. `gkxlumen-topic-policy/gkxlumen-topic-policy-biz/src/test/java/com/topcomm/gkxlumen/topic/policy/controller/PolicyFacadeControllerTest.java`
   - `favoritesAndShareAreNotInnerWhileRankStaysPublic` 增加 `assertNoInner("subscriptions")`、`assertNoInner("getById", String.class)`。
   - 新增 `singleSegmentUserPathsNotSwallowedByPublicUrls`：用真实 Spring context（注册 PolicyFacadeController + PolicyVizController 到 `RequestMappingHandlerMapping`）构建 `PermitAllUrlProperties`，断言：
     - 无任何 publicUrls pattern 能 AntPathMatcher 命中 `/topic/v1/policy/favorites|share|subscriptions`；
     - `publicUrls` 含 `/topic/v1/policy/docs/*`（匿名详情入口保留）、不含 `/topic/v1/policy/*`；
     - `GkxlumenBearerTokenExtractor` 对四个单段路径（含 `/topic/v1/policy/pol-123`）均从 Authorization 头解析出 Bearer 令牌；
     - 对照：`/search` 命中 publicUrls 仍跳过解析（保持匿名语义，回归保护）。
   - 辅助方法 `buildPermitAllUrlPropertiesFromRealMappings`（扫描真实 `@Inner` 注解，避免手写 pattern 清单绕过），用后 `clearHolder()` 清理静态 context。

## 6. 测试结果

- 命令（仓根）：
  ```
  mvn -pl gkxlumen-topic-policy/gkxlumen-topic-policy-biz -am test -DskipITs
  ```
  （本机 JAVA_HOME=`E:\gkx-lumen\worktrees\tooling\jdk\jdk-21.0.12+8`，Maven 3.9.9，仓无 mvnw）
- **退出码 0，全绿**。surefire 报告 `PolicyFacadeControllerTest`：`Tests run: 22, Failures: 0, Errors: 0, Skipped: 0`（含新增测试；此前为 21）。
- 被改模块仅 gkxlumen-topic-policy-biz（`-am` 连带 common 依赖模块构建通过）。未改公共组件，无需跑全仓。

## 7. 线上复验步骤（rollout 后）

```bash
# 期望全部 401（令牌被解析且无效）：
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer fake" https://<host>/policy/topic/v1/policy/favorites
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer fake" https://<host>/policy/topic/v1/policy/share
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer fake" https://<host>/policy/topic/v1/policy/subscriptions

# 期望 401（兜底匿名已收，需令牌）：
curl -s -o /dev/null -w "%{http_code}\n" https://<host>/policy/topic/v1/policy/pol-123

# 期望 200（匿名详情入口保留）：
curl -s -o /dev/null -w "%{http_code}\n" https://<host>/policy/topic/v1/policy/docs/pol-123

# 期望 200 且带用户数据（有效令牌；用真令牌替换）：
curl -s -H "Authorization: Bearer <real>" https://<host>/policy/topic/v1/policy/favorites
```

## 8. 同模式影响评估（只登记，不改）

全仓 grep `@Inner(false)` + 路径变量映射，以下服务存在「变量段转 `*` 进 publicUrls」的同款模式（`@GetMapping` 单独列出；类级/其他方法级未含路径变量的不受影响）：

| 服务 | 控制器 | pattern | 现状评估 |
|---|---|---|---|
| gkxlumen-topic | `TopicElementController` | `/topic/v1/{element}/metrics`、`/topic/v1/{element}/graph/summary` → `/topic/v1/*/metrics`、`/topic/v1/*/graph/summary` | **两段 pattern，不会命中单段静态兄弟**；但会把 `/topic/v1/任意段/metrics` 全放行。当前 `/topic/v1` 下无其他两段 `X/metrics` 业务路由，无实际误伤。Wave 1 占位实现，建议接线时复查 |
| gkxlumen-app-server | `AppMobileController` | `/appmobile/{mobile}` → `/appmobile/*` | `/appmobile` 下无其他单段路由，无实际误伤；但语义上「发短信验证码匿名放行整段」本身值得复查（限流/防刷） |
| gkxlumen-visual | `RestTaskDemo`（daemon-quartz demo） | `/{param}` → `/*` | demo 残留，若部署会把**服务根下所有单段 GET** 全放行。建议删除该 demo 类（未随本单改动） |

其余 `@GetMapping("/{id}")`（pay/mp/codegen/upms/innov/app-server 管理接口）均**未标** `@Inner(false)`，不进 publicUrls，无此问题。

## 9. 遗留风险

1. **`/{id}` 匿名收紧**：如有未核查到的外部匿名消费者直打 `/topic/v1/policy/{id}`，rollout 后会 401。迁移方式：改走 `/docs/{id}`（本仓 FE 与 Java Feign 均已如此）。
2. **公共组件语义未改**（方案 B 未做）：`PermitAllUrlProperties` 仍会把任何含路径变量的 `@Inner(false)` 映射转 `*` 放行同级静态路径。新增 `@Inner(false)` + 路径变量映射时仍会复发，§8 清单供后续治理任务引用。
3. 线上复验由监管人 rollout 后执行（§7）；本单不做集成环境验证（按派单约定）。
