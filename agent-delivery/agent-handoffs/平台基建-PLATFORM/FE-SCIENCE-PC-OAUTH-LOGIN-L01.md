# Handoff · FE-SCIENCE-PC-OAUTH-LOGIN-L01  
# lumen-ui-science-pc 对接 PigX OAuth2 真登录

| 项 | 值 |
|---|---|
| 任务 | `FE-SCIENCE-PC-OAUTH-LOGIN-L01` |
| Epic | `E-PLATFORM` |
| 角色 | `agent:frontend-agent` |
| 监管 | `human:淮政玮` |
| 日期 | 2026-07-30 |
| 状态 | `review` |
| Commit | `lumen-ui-science-pc` **`558e22e`** |
| 参考 | `demo-ui-system-test` `/auth/oauth2/token` · `gkxlumen-auth` `encode-key: gkx-lumen-gkx-lu` |

---

## 1. 交付结论

将原先假路径 `POST /auth/login` + Mock token，改为与 system-test / admin 一致的 **OAuth2 password**：

- `POST /api/auth/oauth2/token`
- query：`username` / `grant_type=password` / `scope=server`
- body：AES/CFB/NoPadding 加密 password（`VITE_PWD_ENC_KEY=gkx-lumen-gkx-lu`）
- `Authorization: Basic pig:pig`
- 存 `access_token` 为 Bearer

`request.ts`：支持 `skipToken`（不覆盖 Basic）；识别无 `code` 包装的 `access_token` 响应。

---

## 2. 产物

| 路径 | 说明 |
|------|------|
| `src/api/auth.ts` | realLogin → oauth2/token |
| `src/utils/encryption.ts` | AES CFB（对齐 auth encode-key） |
| `src/utils/request.ts` | skipToken + OAuth body 直出 |
| `src/views/LoginView.vue` | 错误兜底 |
| `.env.development` / `.env.production` | Mock Auth=false + enc key + client |
| `env.d.ts` | 新 env 类型 |

---

## 3. 验收

1. 打开 `/login`，用平台账号（如 admin）登录  
2. Network：`/api/auth/oauth2/token` **200**，body 含 `access_token`  
3. 后续 innov 请求带 `Authorization: Bearer <access_token>`（非 `admin-mock-token`）  
4. 科技新闻抽取可过网关鉴权；可继续做 Tempo 三联查  

---

## 4. Cost

| 字段 | 值 |
|------|-----|
| `model_used` | cursor-grok-4.5 |
| `actual_tokens` | ~55000 |
| `actual_cost` | ~0.35 |
| `cost_warn` | green |
