# Spec · 专题系统接口携带 Authorization 头即返回 424

- 提出人：human:李伟（展示系统负责人）
- 状态：**排查完成，待用户选定修复路径**（用户已选定「D 先只出结论、不改动」）
- 本轮已发生的改动：**无**（零代码 / 零配置 / 零部署变更）
- 环境：`http://111.198.38.90:50199`（外网网关）→ lumen 专题 Java 服务

---

## 1. 问题陈述（现象）

> 「专题系统接口目前 Header 只要传递了 Authorization 参数，就会直接 424」

- 不带 `Authorization`：正常返回（200）
- 带 `Authorization`（无论 token 真假）：HTTP **424 Failed Dependency**，body：
  ```json
  {"code":1,"msg":"token expired","data":"<传入的token原文>","ok":false}
  ```

## 2. 复现与运行时证据（实测）

| 请求 | 结果 |
|---|---|
| `POST /enterprise/topic/v1/search/meta/filters`（`systemCode: topic`，body `{}`，**无** token） | **200**，0.115s |
| 同上 + `Authorization: Bearer FAKE-TOKEN-123` | **424**，`{"code":1,"msg":"token expired","data":"FAKE-TOKEN-123","ok":false}` |
| `GET /innov/v1/health` + 假 token | **424**，同 body |

结论：**与 token 真伪无关，任意 token 一律被拒。**

## 3. 根因（三层）

### 3.1 机制层 —— 白名单接口携带 token 仍触发认证

- 专题全部接口标注 `@Inner(value = false)`，经 `PermitAllUrlProperties` 收集进 permitAll 白名单（匿名可达）。
- 无 `Authorization` 时：Spring Security 直接放行 → 200。
- 有 `Authorization` 时：`GkxlumenBearerTokenExtractor` 解析出 token → `GkxlumenCustomOpaqueTokenIntrospector` 校验 → 失败抛 `InvalidBearerTokenException` → `ResourceAuthExceptionEntryPoint` 输出 **424**。
- 仓内已有 `skipPublicUrl` 开关可规避此行为，但**当前未启用**（默认 `false`，全仓无该配置项引用）。

### 3.2 部署层 —— 线上仍是旧包

- 424（而非 401）说明线上 lumen 专题镜像仍是 **`c1b7a38 对接统一用户中心`（2026-10-15 16:49）之前的旧包**。
- 旧包只认 pigX 本地 Redis（`oauth2_authorization`）签发的 token；用户中心 / 门户下发的 token 不在其中 → 必然 `InvalidBearerToken` → 424。
- 佐证：工作区唯一硬编码 424 的位置在 demo 侧同源文件，线上行为与之逐字一致（`"token expired"`）。

### 3.3 配置层 —— 即使重新部署仍会复现（且影响面 > topic）

- `SsoProperties.enabled` **默认 `true`**，但 `lumen-svc-platform` 全仓**没有任何 `sso:` 配置块**：
  - `userCenterUrl` 为空、`apps[]` 为空 → `SsoTokenChecker.findByCode("topic")` 返回 null → 调用方仍抛 `InvalidBearerTokenException`。
  - 新包只会把现象从 **424** 改为 **401 + 「访问令牌不存在」**，不消除故障。
- **该缺陷作用于所有 lumen 资源服务器（innov / topic-* / upms 等），非 topic 独有。**

### 3.4 现有临时规避

- 前端 `lumen-ui-topic/src/utils/request.ts`：`ENABLE_MOCK_AUTH && !USE_MOCK` 时**不附加 Bearer**（当前 `.env.development` / `.env.production` 正是该组合）→ 这就是目前接口能调通的原因。
- 与门户正式方案冲突：`门户集成-PORTAL/LUMEN-PORTAL-IFRAME-L01.md` §0 要求前端带 `Bearer + systemCode=topic`。

## 4. 涉及文件与函数（精确定位）

| # | 文件 | 关键点 | 现状 |
|---|---|---|---|
| F1 | [ResourceAuthExceptionEntryPoint.java](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-svc-platform/gkxlumen-common/gkxlumen-common-security/src/main/java/com/topcomm/gkxlumen/common/security/component/ResourceAuthExceptionEntryPoint.java) | `commence()` 中 `FAILED_DEPENDENCY`→`UNAUTHORIZED` 分支 | HEAD 已改 401（=c1b7a38），线上未部署 |
| F2 | [SsoProperties.java](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-svc-platform/gkxlumen-common/gkxlumen-common-security/src/main/java/com/topcomm/gkxlumen/common/security/component/SsoProperties.java#L38) | `private boolean enabled = true;` | 默认开启但无配置 |
| F3 | [SsoTokenChecker.java](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-svc-platform/gkxlumen-common/gkxlumen-common-security/src/main/java/com/topcomm/gkxlumen/common/security/component/SsoTokenChecker.java) | `props.findByCode(systemCode)` 未命中 → `return null` | 含 `[TEMP-DEBUG]` 日志 |
| F4 | [GkxlumenCustomOpaqueTokenIntrospector.java](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-svc-platform/gkxlumen-common/gkxlumen-common-security/src/main/java/com/topcomm/gkxlumen/common/security/component/GkxlumenCustomOpaqueTokenIntrospector.java) | `introspectViaSso()` / `introspectViaGkx()` 分支 | — |
| F5 | [PermitAllUrlProperties.java](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-svc-platform/gkxlumen-common/gkxlumen-common-security/src/main/java/com/topcomm/gkxlumen/common/security/component/PermitAllUrlProperties.java#L53-L60) | `skipPublicUrl = false` | 未启用 |
| F6 | [GkxlumenBearerTokenExtractor.java](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-svc-platform/gkxlumen-common/gkxlumen-common-security/src/main/java/com/topcomm/gkxlumen/common/security/component/GkxlumenBearerTokenExtractor.java#L63-L69) | `isSkipPublicUrl()` 门控 `return null` | 未启用 |
| F7 | `repos/lumen-svc-platform/helm/gkxlumen-platform/configs/` | `gkxlumen-{gateway,topic-*-biz,innov,upms-biz,auth}-dev.yml` + `application-dev.yml` | **无 `sso:` 块** |
| F8 | [request.ts](file:///e:/work/上达通/项目/深圳GKX/gkx-lumen/repos/lumen-ui-topic/src/utils/request.ts) | `shouldAttachBearerToken()`；424/401 视为登录失效 | 现有规避 |

## 5. 修复方案（决策点 · 待批准后才能执行）

| 方案 | 内容 | 影响面 | 前置依赖 | 结果 |
|---|---|---|---|---|
| **A（推荐）** | (a) 在 F7 的 `application-dev.yml`（共享）+ 各 `gkxlumen-topic-*-biz-dev.yml` 补 `sso:` 块（`userCenterUrl`、`tenantId`、`apps[{code:"topic", clientId, clientSecret}]`）；(b) 重新部署 topic-* / innov / upms 等 lumen 服务，使 c1b7a38 生效 | 跨服务、跨模块 | **需用户中心注册应用拿 Client ID/Secret（原文档联系人：宋泉）** | 根因修复：门户/用户中心 token 可校验通过 |
| **B（止血）** | 在 F7 各资源服务 yml 加 `security.oauth2.client.skip-public-url: true` | 配置级，单行 | 无 | permitAll 接口即使带 Authorization 也不再解析 token → 恢复 200 |
| **C（维持）** | 前端继续不传 token（现状） | 前端 | 无 | 能跑通，但与门户 `Bearer + systemCode=topic` 正式方案冲突 |
| **D（用户已选）** | 仅交付本排查结论，不改动任何文件 | — | — | 本轮结束，由后续流程决定 A/B/C |

## 6. 验收标准（任一方案执行后）

1. `POST /enterprise/topic/v1/search/meta/filters`（`systemCode: topic`，body `{}`）
   - 不带 Authorization → **200**（回归不变）
   - 带合法用户中心 token → **200**
2. 带**非法/过期** token → **401 + `{"code":401,"msg":"访问令牌不存在"}`**（方案 A），或 **200**（方案 B，白名单接口忽略 token）；**不得再出现 424**。
3. 方案 A 额外：`SsoTokenChecker` 日志无 `unknown systemCode=topic`。
4. 全仓 grep 复检：`FAILED_DEPENDENCY` 在 lumen 侧仅剩历史无引用。

## 7. 审批与责任人

- 决策审批：human:李伟（展示系统负责人）
- 用户中心应用注册（Client ID/Secret）：去接口文档登记的联系人 **宋泉**
- 部署执行：部署/运维侧（K8s dev rollout）
- 后端改动（若走 A 的配置或 B 的开关）：lumen-svc-platform 相关负责人
- **本 Spec 未获批准前，不执行任何 A/B/C 改动。**

## 8. 不在本次范围

- 不对 F1–F6 的 Java 代码做逻辑改写（HEAD 已满足 401 语义）。
- 不调整前端门户 iframe 方案。
- 不处理工作区 grep 命中的无关 SQL / demo 侧噪音。
