# Handoff · FE-SCIENCE-PC-TOKEN-ALIGN-L01  
# lumen-ui-science-pc 对齐 topic 的 Mock / 真网关 token 处理

| 项 | 值 |
|---|---|
| 任务 | `FE-SCIENCE-PC-TOKEN-ALIGN-L01` |
| Epic | `E-PLATFORM` |
| 角色 | `agent:frontend-agent` |
| 监管 | `human:淮政玮` |
| 日期 | 2026-07-30 |
| 状态 | `review`（代码已 push `4a9b230`；CI/CD 由监管人执行） |
| 参考真源 | `lumen-ui-topic` `shouldAttachBearerToken` + `USE_MOCK` + `authRedirect` |
| Commit | `lumen-ui-science-pc` **`4a9b230`** |

---

## 1. 交付结论

对齐 topic：在 **Mock 登录 + 真网关**（`ENABLE_MOCK_AUTH && !USE_MOCK`）时**不**挂 `Authorization`，避免 `admin-mock-token` 触发网关 424；HTTP 424 / token expired /「用户凭证已过期」时清 token 并跳转登录。保留既有 `__traceId` / Message 行为。

---

## 2. 产物清单

| 路径 | 说明 |
|------|------|
| `src/config/app.ts` | 新增 `USE_MOCK`（`VITE_APP_USE_MOCK`，缺省回退 `ENABLE_MOCK_AUTH`） |
| `src/utils/authRedirect.ts` | 新增（对齐 topic，解耦 request↔router） |
| `src/utils/request.ts` | `shouldAttachBearerToken` + 424 清 token + `triggerAuthRedirect` |
| `src/main.ts` | `setAuthRedirectHandler` → login + redirect query |
| `src/api/auth.ts` | 注释：Mock token 不得打真网关 |
| `.env.development` | `USE_MOCK=false` + `ENABLE_MOCK_AUTH=true`（对齐 topic） |
| `.env.production` | `USE_MOCK=false` + `ENABLE_MOCK_AUTH=false` |

---

## 3. 验收要点

1. Dev（Mock Auth 开、USE_MOCK 关）：Network 请求**无** `Authorization: Bearer admin-mock-token`
2. 生产 / 真登录后：Bearer 为真实 OAuth token；可调 `/api/innov/v1/tech-news/*`
3. 若仍带失效 Bearer：HTTP 424 → 清 token → 跳转登录（错误提示仍可带 `__traceId`）

---

## 4. 架构合规自检

| 铁律 | 状态 |
|------|------|
| D2 调用链 FE→Java | ✅ 未越层 |
| D4 可观测性 | ✅ 保留 `__traceId` |
| 不扩 mock-token 白名单 | ✅ |

---

## 5. Cost

| 字段 | 值 |
|------|-----|
| `model_used` | cursor-grok-4.5 |
| `actual_tokens` | ~45000 |
| `actual_cost` | ~0.30 |
| `cost_warn` | green |
