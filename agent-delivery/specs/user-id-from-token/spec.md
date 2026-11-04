# Spec · 专题系统 user_id 改为从 access_token 获取

- 状态：**待评审**（本文档不改代码、不改配置、不做部署）
- 提出场景：`lumen-ui-topic` 已带 Bearer token，但接口侧仍依赖前端传入的 `user_id`（当前恒为 `'guest'`）
- 关联任务：`LUMEN-PORTAL-IFRAME-L01`（门户 iframe 嵌入，integration 中）
- 关联前案：`POL-L2-DS10-QRY-DISP-L01`、`TOPIC-POLICY-SINGLE-SEGMENT-TOKEN-FIX-L01`、`USER-BEHAVIOR-UNIFIED-TABLE-20261102`、`specs/topic-424-auth-header`
- 决策：**匿名一律 401**（human:淮政玮 2026-11-04 选定），不做「可选令牌」公共组件改造

---

## 0. 一句话结论

「从 token 取 userId」的能力**已经实现并在线运行**（`gkxlumen-display` / `gkxlumen-topic-policy` 已在用），缺的不是能力而是**三处断点**：前端 `user_id` 恒为 `'guest'`、端点 `@Inner(false)` 吞掉 Bearer、Service 层 `resolveUserId()` 仍读入参。本文档给出逐端点分类与逐文件改动点。

---

## 1. 现状链路（已核实）

### 1.1 token 校验链路

```
前端  Authorization: Bearer <portal_access_token>  +  systemCode: topic
  ↓ lumen-ui-topic/src/utils/request.ts:60,72-81
网关  GkxlumenRequestGlobalFilter：剥路径前缀 / 删 from 头 / 注入 trace
       —— 不校验 token（gateway/src/main/java/.../filter/GkxlumenRequestGlobalFilter.java:72-101）
  ↓
资源服务器  GkxlumenResourceServerConfiguration.securityFilterChain
       ignoreUrls（PermitAllUrlProperties 收集）→ permitAll
       其余 anyRequest().authenticated()   ← :68-71
  ↓
令牌抽取  GkxlumenBearerTokenExtractor.resolve
       publicUrls 命中 → return null（不读 Authorization）   ← :60-67
       否则读 Authorization，兜底读 ?access_token=            ← :73-81, :110-118
  ↓
内省  GkxlumenCustomOpaqueTokenIntrospector.introspect
       sso.enabled=true（默认）→ introspectViaSso            ← :51-56
         → SsoTokenChecker.check(token, systemCode)
            → POST {userCenterUrl}/admin-api/system/oauth2/check-token
            → SsoCheckTokenVO{ userId, tenantId, userType, exp }
         → 组装 GkxlumenUser{ id=userId, tenantId, userType, NO_AUTHORITIES }
  ↓
业务  SecurityUtils.getUser().getId()
```

关键事实：

| 项 | 值 | 出处 |
|---|---|---|
| 能拿到 | `userId` / `tenantId` / `userType` / `exp` | `SsoCheckTokenVO` |
| 拿不到 | `roleIds`（空）、`deptId`/`nickname`/`email`（null）、`authorities`（`NO_AUTHORITIES`） | `GkxlumenCustomOpaqueTokenIntrospector:143-160` |
| `username` 语义 | `systemCode + ":" + clientId`（如 `topic:xxx`），**不是真实用户名** | 同上 :145 |
| 与 `sys_user.user_id` | **不同源**，不可 join | `USER-BEHAVIOR-UNIFIED-TABLE-20261102` §三 |
| 校验缓存 | **无**，每请求打一次 check-token | 同文档「性能提示」 |

### 1.2 `@Inner` 三态语义（本文档的核心风险点）

`PermitAllUrlProperties.afterPropertiesSet`（:74-91）：

```java
Inner effective = method != null ? method : controller;
boolean open = !effective.value();
getPatternValues().forEach(url -> {
    String pattern = ReUtil.replaceAll(url, PATTERN, "*");   // {id} → *
    ignoreUrls.add(pattern);
    if (open) { publicUrls.add(pattern); }
});
```

| 端点注解 | 进 ignoreUrls | 进 publicUrls | Bearer 解析 | `GkxlumenSecurityInnerAspect` 要求 `from: Y` |
|---|---|---|---|---|
| 无注解 | ❌ | ❌ | ✅ | — |
| `@Inner(false)` | ✅ | ✅ | **❌ 丢弃** | ❌ |
| `@Inner`（默认 true） | ✅ | ❌ | ✅ | ✅ 外部调用 403 |

`GkxlumenBearerTokenExtractor:64-67` 对 `publicUrls` 命中路径直接 `return null`，**因此 `@Inner(false)` 端点上 `SecurityUtils.getUser()` 必然为 null，与前端是否带 token 无关。**

### 1.3 为什么现在「能跑」

因为 `resolveUserId()` 读的是前端参数，而前端参数恒为 `'guest'`：

```typescript
// lumen-ui-topic/src/utils/currentUser.ts:8-16
export function resolveUserId(): string {
  const auth = useAuthStore()
  const name = String(unref(auth.username) ?? '').trim()
  return name || 'guest'
}
```

`authStore.username` 初值 `'guest'`（`stores/auth.ts:9`），**全仓无任何赋值**（只有 `setAuthToken` 写 token）。

**后果：所有用户共享 `guest` 一个数据分区**——对比篮、检索历史、筛选模板、分析任务全部串号。这不是"未接入"，是**已发生的数据正确性缺陷**。

---

## 2. 已有实现（可直接照抄，不新造）

| 模块 | 文件 | 做法 | 状态 |
|---|---|---|---|
| display | `display/controller/UserBehaviorController.java` | 13 个端点逐个 `SecurityUtils.getUser()`，null 返 `R.failed("未登录：缺少有效 token")`，再把 userId/tenantId **覆盖**进 DTO 转发 upms | ✅ 在线 |
| topic-policy | `topic-policy-biz/controller/PolicyFacadeController.java:306-312` | 私有 `currentUserId()`，忽略 body `user_id`，匿名返 null 走诚实降级空数据 | ✅ 在线 |
| display | `PolicyPanoramaService:429`、`PolicyEvaluationService:258` | service 层同名同款私有方法 | ✅ 在线 |
| topic-async | `support/analysis/AnalysisUserSupport.java:19-31` | 仅 TODO 注释，**读入参** | ❌ 未实装 |
| topic-enterprise | 8 个 `*ServiceImpl.resolveUserId()` | 仅 TODO 注释，**读入参** | ❌ 未实装 |
| topic-svc | `SvcCompareBasketServiceImpl` | 纯 Feign 透传，无身份解析 | ❌ 未实装 |

**结论：这是「迁移」，不是「研发」。**

---

## 3. 端点分类清单（唯一需要人工裁定的部分）

### 3.1 A 类 — 用户相关，**去掉 `@Inner(false)`**

> 改后：匿名访问 → 401；有效 token → 按 token 身份

#### A1 `gkxlumen-topic-enterprise` / `CompareBasketController`（19 处，全量）

`GET /compare-basket`、`POST /compare-basket/items`、`DELETE /compare-basket/items/{enterprise_code}`、`DELETE /compare-basket/items/batch`、`GET /compare-basket/search`、`POST /compare-basket/dispatch`、`GET /compare-basket/return-context/{context_id}`、`GET|POST /compare-basket/recruit-candidates`、`GET|POST /compare-basket/cultivate-candidates`、`DELETE /compare-basket/recruit-candidates/{code}`、`DELETE /compare-basket/recruit-candidates/batch`、`DELETE /compare-basket/cultivate-candidates/{code}`、`DELETE /compare-basket/cultivate-candidates/batch`、`GET|POST /compare-basket/org-items`、`DELETE /compare-basket/org-items/{org_id}`、`DELETE /compare-basket/org-items/batch`

#### A2 `gkxlumen-topic-enterprise` / `EnterpriseSearchBizController`（history 3 处）

`POST /search-biz/history/list`、`/history/save`、`/history/clear`

> ⚠️ 同 Controller 的 `examples/*`、`scenes/*`（各 3 处）是**全局公共元数据**（表无 `user_id` 列，见 `db/9x_gkxlumenx_topic_enterprise.sql:63-76`），**保留 `@Inner(false)`**，归 C 类。

#### A3 `gkxlumen-topic-enterprise` / `EnterpriseFilterTemplateController`（5 处全量）

`POST /filter-template/list|save|delete|get|set-default`

#### A4 `gkxlumen-topic-enterprise` / `ChainUxInternalController`（17 处中 13 处属 A 类）

`/compare-basket`（4）、`/search-biz/history/*`（3）、`/filter-template/*`（3）、`/regional/templates/mine/*`（3）

> **保留 C 类**：`/search-biz/examples/list`、`/search-biz/scenes/list`（:70-79）、`/regional/metrics`（:120）、`/regional/templates/official`（:127）——公共元数据，无 `user_id`。

#### A5 `gkxlumen-topic-svc` / `SvcCompareBasketController`（4 处全量）

`GET /service/compare-basket`、`POST /items`、`DELETE /items/{org_id}`、`DELETE /items/batch`

#### A6 `gkxlumen-topic-async-service` / `AnalysisTaskController`（14 处中 10 处属 A 类）

`/tasks`（create）、`/tasks/list`、`/tasks/{taskId}`、`/tasks/{taskId}/result`、`/tasks/{taskId}/events`、`/tasks/{taskId}/asset`、`/tasks/{taskId}/cancel`、`DELETE /tasks/{taskId}`、`/tasks/running`、`/tasks/stream`

#### A7 `gkxlumen-topic-async-service` / `EvaluationTemplateController`（5 处全量）

`GET|POST /evaluation/templates`、`PUT|DELETE /evaluation/templates/{templateId}`、`PUT /templates/{templateId}/default`

> 同模块 `controller/evaluation/EvaluationAssistController`（industries / indicators / precheck / tasks/compare）—— `precheck`（:57）、`tasks/compare`（:66）带 `user_id`，**归 A 类（+2）**；`industries`（:38）、`indicators`（:48）是公共字典，**归 C 类**。

#### A8 `gkxlumen-topic-async-service` / `TrackingEvaluationController`（9 处）

当前已是 `@Inner`（默认 true，要求 `from: Y`），**需单独裁定**：若由 `lumen-ui-science-pc` 浏览器直调，则应改为无注解（authenticated）；若仅内部调用，保持现状。**lumen-ui-science-pc 全仓 grep `tracking/evaluation` 零命中**，倾向保持现状，本次不动。

### 3.2 B 类 — 系统回调，**改为 `@Inner`（默认 true）**

| 端点 | 现有 | 建议 | 理由 |
|---|---|---|---|
| `POST /analysis/callback/eval` | `@Inner(false)` | `@Inner` | Python `gkx_ai_service` 调用，应带 `from: Y` |
| `POST /analysis/callback/risk` | `@Inner(false)` | `@Inner` | 同上 |
| `POST /analysis/callback/recommend` | `@Inner(false)` | `@Inner` | 同上 |
| `POST /analysis/callback/svc` | `@Inner(false)` | `@Inner` | `gkx_svc_service/views/task.py:111` **已发 `from: Y`**，改后立即可用 |
| `POST /internal/v1/analysis-jobs/{taskId}/stages` | `@Inner(false)` | `@Inner` | `lumen-algo-py` 带 `Bearer LUMEN_ALGO_CHAIN_JOB_CALLBACK_TOKEN`（`job_runtime.py:288-297`）：改成 authenticated 也能过，但需该 token 被 SSO 认可 → **建议保持 `@Inner(false)`，改由 `LUMEN_ALGO_CHAIN_JOB_CALLBACK_TOKEN` 独立校验**（见 §7 风险 R5） |
| `POST /internal/v1/analysis-jobs/{taskId}/complete` | 同上 | 同上 | 同上 |

> ⚠️ 回调端点**不能**简单收紧到 authenticated：它们没有用户 token。正确做法是要么 `@Inner` + `from: Y`（Python 侧已支持且需补 header），要么保持匿名 + 独立共享密钥校验。

### 3.3 C 类 — 公共元数据，**保持 `@Inner(false)` 不动**

- `gkxlumen-topic-svc`：`ServiceFacadeController`（6 处：health / search/orgs / profile/get / eco-graph / rec-list / meta）、`ServicePortalFacadeController`（7 处全部）、`TopicDictController`（11 处）
- `gkxlumen-topic-enterprise`：`EnterpriseOpenApiController`（19 处检索接口）、`EnterpriseVizController`、`EnterpriseMetaDictController`、`EnterpriseStatsOverviewController` 等只读聚合
- 各 `*VizController`

> 这些端点**不带用户身份**，改为 authenticated 会破坏匿名浏览能力。**本次不动。**

### 3.4 分类统计

| 类别 | 端点数量 | 动作 |
|---|---|---|
| A（用户相关） | ~54（16+19+3+5+13+4+10+2 = 72 处注解中，去重后约 54 个端点） | 去 `@Inner(false)` + Service 改身份源 |
| B（系统回调） | 6 | 按 §3.2 分别处理 |
| C（公共元数据） | ~100+ | 不动 |
| 待裁定（tracking） | 9 | 本次不动 |

---

## 4. Service 层改动点（逐文件）

**统一改法**：私有 `resolveUserId()` 内部换源，签名不变，调用方零改动。匿名返回 `null` 的既有语义保持不变（下游已全部按匿名降级处理）。

```java
/** 解析当前操作用户 ID。身份只取鉴权上下文，忽略前端传入的 user_id。 */
private String resolveUserId(String requestUserId) {
    GkxlumenUser user = SecurityUtils.getUser();
    return user == null || user.getId() == null ? null : String.valueOf(user.getId());
}
```

### 4.1 `gkxlumen-topic-enterprise`

| 文件 | 行 | 现写法 |
|---|---|---|
| `service/impl/CompareBasketServiceImpl.java` | 69-72 | `StringUtils.hasText(requestUserId) ? trim : null` |
| `service/impl/OrgCompareBasketServiceImpl.java` | 162-164 | 同上（无 TODO 注释，需补） |
| `service/impl/EntSearchHistoryServiceImpl.java` | 67-70 | 同上 |
| `service/impl/EntFilterTemplateServiceImpl.java` | 48-50 | 同上 |
| `service/impl/ChainCompareBasketServiceImpl.java` | 78, 151 | `trimToNull(request.getUserId())` **直读，无 resolve 方法** → 需新增统一方法 |
| `service/impl/ChainFilterTemplateServiceImpl.java` | 30, 54, 111 | 同上 |
| `service/impl/ChainRegionalTemplateServiceImpl.java` | 63, 86, 114 | 同上 |
| `service/impl/ChainSearchAuxServiceImpl.java` | 67, 97, 131 | 同上（已有 `trimToNull`，:170） |
| `service/impl/EnterpriseSearchAuxServiceImpl.java` | 100 | `autoRecord(request.getUserId(), ...)` 直传 → 改为 `resolve` |
| `service/impl/EnterpriseOpenApiServiceImpl.java` | 72 | 同上 |

> `Chain*ServiceImpl` 五个类都是 `trimToNull(request.getUserId())` 直接取参，**没有 resolveUserId 方法**。建议抽出 `TopicCurrentUserSupport`（`@Component`，照 `AnalysisUserSupport` 的形状）统一供这 5 个类注入，避免五份重复实现——符合「第二处出现即封装」。

### 4.2 `gkxlumen-topic-svc`

`SvcCompareBasketServiceImpl` 四方法全是 Feign 透传 `userId`，**无解析点**。改法：在 Controller 层取 `SecurityUtils.getUser()` 覆盖入参（照 `UserBehaviorController` 的形状），Service 签名不变。

### 4.3 `gkxlumen-topic-async-service`

唯一收口点 `support/analysis/AnalysisUserSupport.java:19-31`，改一行即可覆盖全部调用方：

| 调用方 | 位置 |
|---|---|
| `AnalysisTaskServiceImpl` | 133, 768, 874, 939, 1016, 1206 |
| `EvaluationAssistServiceImpl` | 95 |
| `EvaluationTemplateServiceImpl` | 67, 104, 250 |
| `AnalysisTaskController` | 180, 379 |

> `loadOwnedTask`（:1204-1210）在 uid 为 null 时返 `R.failed("未获取到当前用户")`——改成去 `@Inner(false)` 后，匿名根本进不来（401 前置拦截），此分支自然只在内部异常时触发，**保留不动**。

---

## 5. 前端改动点

| 文件 | 现状 | 改动 | 必要性 |
|---|---|---|---|
| `src/utils/currentUser.ts` | `auth.username || 'guest'` | **保留但降级为 UI 展示专用**；`user_id` 参数保留（后端已忽略） | 可选 |
| `src/api/enterprise/analysisTask.ts:300-310` | `EventSource(url + '?user_id=')` | 改 `?access_token=<token>`，去 `user_id` | **必须**（见 §6） |
| `src/stores/auth.ts` | `username` 恒 `'guest'` | 若仍要前端展示真实姓名，从 `usePortalPermStore().userInfo.realName` 取（`portal/perms.ts:132-146` 已有） | 可选 |

> `user_id` 查询参数保留不删：后端忽略后传不传都行，留作灰度期双方解耦。

---

## 6. SSE 单独处理（最容易漏的一条）

```typescript
// lumen-ui-topic/src/api/enterprise/analysisTask.ts:300-310
 * EventSource 无法携带 Authorization 头，依赖 user_id 会话键 + 网关匿名可达。
 */
real: (params) => createEventStreamHandle(`${BASE_URL}${AnalysisTaskPaths.tasksStream}?user_id=${...}`)
```

`EventSource` 不能带自定义头。但 extractor **已支持 query 兜底**：

```java
// GkxlumenBearerTokenExtractor:110-118
private static String resolveFromRequestParameters(HttpServletRequest request) {
    String[] values = request.getParameterValues("access_token");
```

**改法**：`/tasks/stream?access_token=<token>`，去掉 `@Inner(false)`。
**代价**：token 进 URL，可能落 nginx/网关访问日志；属过渡方案，需在 handoff 注明并在正式方案（门户提供 Cookie 鉴权或 fetch-stream）时移除。

备选（更干净但工作量大）：前端改用 `fetch` + `ReadableStream` 手动解析 SSE，可带 Authorization 头。**本次建议先用 query 方案，登记技术债。**

---

## 7. 风险与阻塞项

| # | 风险 | 影响 | 处置 |
|---|---|---|---|
| **R1** | **单段 `{id}` 兜底连带放行静态兄弟路径** | 新增 `@Inner(false)` + 路径变量会复发「令牌被吞」 | 已确诊（`TOPIC-POLICY-SINGLE-SEGMENT-TOKEN-FIX-L01` §3、§8）。本次只**删除** `@Inner(false)`，不新增，风险降低；但 `AnalysisTaskController` 的 `/tasks/{taskId}` 等若将来回退会复发。**验收必须含「假 token 应 401」回归** |
| **R2** | **历史数据全部成孤儿** | `ent_search_history` / `ent_filter_template` / `ent_compare_basket` / `chain_*` / `analysis_task` 现有 `user_id` 全是 `'guest'` | 切换后新用户看不到旧数据。**需产品裁定**：直接清空（演示期数据无价值）或保留 `guest` 行做只读归档。DDL 已确认全部是 `varchar(64)`，`Long` 转 String 无需改表 |
| **R3** | **`tenantId` 未落库** | 上述表只有 `user_id`，无 `tenant_id` | 单租户部署下无影响；多租户需补列。**建议补 `tenant_id` 列**（`USER-BEHAVIOR-UNIFIED-TABLE` 已定 `bigint`） |
| **R4** | **SSO 校验无缓存** | 每请求打一次 check-token（connect 3s / read 5s 超时） | 对比篮/历史读接口明显变慢。**建议加 `token → userId` 本地缓存**（Caffeine，TTL < token 有效期）。可先上线再补 |
| **R5** | **链回调 `Bearer LUMEN_ALGO_CHAIN_JOB_CALLBACK_TOKEN` 不是 SSO token** | 若改成 authenticated 会被 SSO 校验拒绝 | `job_runtime.py:288-297` 已带该 token。**建议保持 `@Inner(false)`**，改由独立共享密钥 Filter 校验（后续单独任务） |
| **R6** | **`authorities` 全空** | 无法用 `@PreAuthorize` 做角色鉴权 | 归属校验只能用 `task.getUserId().equals(uid)` 形式（`loadOwnedTask` 已是此模式），**不新增角色依赖** |
| **R7** | **`username` 是 `systemCode:clientId`** | 无法反查 `sys_user` | 收藏表不 join `sys_user`（已定）；展示真实姓名走 `/admin/get-permission-info` |
| **R8** | **Nacos 配置未在仓内** | 无法靠 grep 确认 async-service 的 `sso.apps[code=topic]` 是否配好 | **前置阻塞项**，必须先跑 §8 的探针 |
| **R9** | **匿名语义变更需产品确认** | A 类端点从「200 + 空数据」变「401」 | 已由决策「匿名一律 401」覆盖；前端需确保 401 走 `notifyPortalSessionExpired` 而非静默吞（`request.ts:139-145` 已实现，但部分调用方带 `optional:true` 会绕过——需逐页核查） |

---

## 8. 前置验证（改代码前必须做）

```bash
# 1) async-service 的 SSO 配置是否生效（期望 401，不是 200 也不是 424）
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer fake" -H "systemCode: topic" \
  "https://<host>/topicAsync/topic/v1/analysis/tasks/running?user_id=x"

# 2) 对照：topic-enterprise（期望同为 401 或 200，但日志不应出现 unknown systemCode）
curl -s -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer fake" -H "systemCode: topic" \
  "https://<host>/enterprise/topic/v1/compare-basket?user_id=x"

# 3) 真实 token 应拿到真实 userId
curl -s -H "Authorization: Bearer <real>" -H "systemCode: topic" \
  "https://<host>/policy/topic/v1/policy/favorites" | head -c 300
```

**判定标准**：
- 返回 401 → SSO 配置已就绪，可开工
- 返回 200 且日志有 `unknown systemCode=null` → 该服务缺 `sso:` 配置，**先补 Nacos**
- 返回 424 → 线上仍是旧镜像

> 依据：`specs/topic-424-auth-header` §3.3 已指出 `sso:` 块不在仓内 `helm/` 配置中（全在 Nacos），且 `SsoProperties.enabled` 默认 `true`。`gkxlumen-topic-policy` 能正常解 token，说明 topic 的 app 凭证已注册；async-service 是否共享同一配置**未验证**。

---

## 9. 建议执行顺序（分 4 个任务，不合并）

| 批次 | 范围 | 理由 | 验收 |
|---|---|---|---|
| **T1 试点** | `compare-basket`（`CompareBasketController` 16 处 + `CompareBasketServiceImpl:69`） | 隔离性好、有匿名降级兜底、`Chain`/`Org` 系列可参照 | 假 token→401；真 token→独立 userId；换用户看到各自篮子 |
| **T2 检索类** | `search-biz/history`(3) + `filter-template`(5) + `Chain` 用户系列(13) + `TopicCurrentUserSupport` 封装 | 同构，可批量；封装后 diff 更小 | 同上 + 历史不串号 |
| **T3 分析任务** | `AnalysisTaskController`(10) + `AnalysisUserSupport` + SSE 改 `access_token` + `EvaluationTemplateController`(5) | 最复杂：含 SSE、归属校验、回调分类 | 同上 + SSE 能收到事件 + 回调仍通 |
| **T4 收尾** | `SvcCompareBasketController`(4) + 回调端点分类 + 前端 `currentUser` 清理 + 旧 `guest` 数据处置 | 依赖 T3 结论 | 全链路无 `user_id` 依赖 |

**每批必跑的回归**（防止 R1 复发）：

```bash
# 所有改动端点：假 token 必须 401
curl -s -o /dev/null -w "%{http_code}\n" -H "Authorization: Bearer fake" -H "systemCode: topic" \
  "https://<host>/enterprise/topic/v1/compare-basket?user_id=x"   # 期望 401
```

---

## 10. 不在本次范围

- 不修改 `gkxlumen-common-security` 任何公共组件（`PermitAllUrlProperties` / `GkxlumenBearerTokenExtractor` / `GkxlumenCustomOpaqueTokenIntrospector` / `SsoTokenChecker`）——全仓语义变更，须架构单独评估
- 不改 `@Inner(false)` 的 C 类公共元数据端点
- 不实装「可选令牌」能力（匿名可读 + 有 token 则带身份）——本次决策为匿名一律 401
- 不实装 SSO 校验缓存（建议单开任务）
- 不改 `TrackingEvaluationController`（9 处，待裁定调用方）
- 不改 Python 侧回调 header（除 §3.2 已列需补 `from: Y` 的 eval/risk/recommend 三处）
- 不处理 `gkxlumen-topic-chain`、`gkxlumen-cms`、`gkxlumen-innov`（本轮无 user_id 依赖）

---

## 11. 架构合规自检

| 铁律 | 结论 |
|---|---|
| D1 算法只在 Python | ✅ 无算法改动 |
| D2 调用链 | ✅ 前端→Java→Python 不变；不新增越层 |
| D3 NebulaGraph | ✅ 未涉及 |
| D4 可观测 | ✅ 沿用 `X-Trace-Id` / `traceparent` 注入，不新增 |
| D8/D10 前端规范 | ✅ 不改 UI/交互 |
| D9 指标 8 件套 | ✅ 不涉指标口径；无 D4 状态变化 |
| D12 demo/lumen 隔离 | ✅ 只改 lumen 侧 |
| D16/D18 | ✅ 无新表、无 mock 行 |

---

## 12. 待产品 / 架构裁定项（阻塞开工）

| # | 问题 | 建议 | owner |
|---|---|---|---|
| Q1 | R2：现有 `'guest'` 数据如何处置（清空 / 归档 / 迁移） | 演示期直接清空，上线前重置 | PM |
| Q2 | R3：是否本次补 `tenant_id` 列 | 建议补（单租户也不亏） | 架构师 |
| Q3 | §3.2 链回调（`/internal/v1/analysis-jobs/**`）是否改共享密钥校验 | 本次保持 `@Inner(false)`，单开任务 | 架构师 |
| Q4 | §3.1 A8 `TrackingEvaluationController` 调用方确认 | 本次不动 | PM |
| Q5 | SSE 用 `?access_token=` 还是改 fetch-stream | 先用 query，登记技术债 | 架构师 |
