# LUMEN-DISPLAY-PORTAL-IFRAME-L01 · lumen-ui-science-pc 统一门户 iframe 认证对接移植

> **状态**：开发完成，待人工验收（人工验收闸门：改动停本地工作区，未 commit/push） · **监管**：human:孔东 · **执行**：agent:frontend-agent
> **强度**：ponytail full · **移植真源**：lumen-ui-topic `LUMEN-PORTAL-IFRAME-L01`（commit `a4549cf` 契约对齐 + `f1825fe` 前缀 base + 2026-10-21 权限菜单矫正）

---

## 0. 用户六点完整性要求逐条对照

| # | 要求 | 落地 |
|---|---|---|
| 1 | 区分生产/开发环境 | `.env.production`：`VITE_PORTAL_ORIGINS=https://edu.itic-sci.com`（无 mock 行，走真实 `/admin/get-permission-info`）；`.env.development`：同白名单 + `VITE_PORTAL_PERM_SOURCE=mock`（无真 token 本地联调，mock 数据与真实 data 同构走同一规范化路径）。`sessionExpired` toast：PROD 恒提示 / DEV 需 `VITE_PORTAL_SESSION_EXPIRED_TOAST=true` |
| 2 | mock 开关对认证的影响 | `shouldAttachBearerToken()`：`ENABLE_MOCK_AUTH && !USE_MOCK`（mock 登录+真 API）不挂本地 token，避免 424；**嵌入态豁免**——token 一律取门户 Cookie `portal_access_token`，门户认证不被本地 mock 登录干扰。权限源另有独立开关 `VITE_PORTAL_PERM_SOURCE=mock`（与业务 USE_MOCK 解耦） |
| 3 | iframe 嵌入 vs 正常打开 | `isEmbedded = window.parent !== window`（单信号，不依赖 URL 参数）。嵌入态：登录判定读门户 Cookie、未登录整窗跳门户 SSO（不渲染本地 login）、无权限上报 `no.permission`、401/424 上报 `session_expired` 交门户接管、侧栏/顶栏隐藏内容满高。独立态：全部保持本仓现状（本地 token / 本地 login / 本地 roles 比对） |
| 4 | v-permission 体系 | 指令升级双模式：嵌入态比对门户权限码集（`menu:display:*` + `btn:display:*`），未加载先隐藏、权限异步到达 `watch` 重算 + `updated` 钩子；独立态比对 `authStore.roles`（现状语义）。按钮码接入即用：`v-permission="'btn:display:trend:export'"` |
| 5 | 菜单权限统一校验 | navGroups 35 菜单全量注入 `permCode`（`menu:display:<组>:<项>` 机械推导）→ 路由 `meta.perms`；嵌入态 guard 统一拦截：登录失效回落（不发 NO_PERMISSION）/ 拉取错误上报 / 缺码拦截上报，回落同组已授权菜单（`permissionFallback.ts`），`upgrade=1` 时忽略门户回推同深链防死循环；侧栏 `getSidebarNavGroups` 按权限码过滤。权限模型沿袭 topic 2026-10-21 联调结论：all+org 桶合并、忽略 appPermissions、菜单授权 = 门户菜单 URL 反查本地 navItem、按钮码直接收集 |
| 6 | postMessage 集成完整 | `messenger.ts` 单例全量移植：统一消息格式（protocol/version/id/action/data）、origin 白名单 + protocol 双校验、上行逐 origin 指定 targetOrigin 禁 `*`；动作全 family：PAGE_READY（等权限接口成功 + 首屏 nextTick）、ROUTE_CHANGE 双向（上行 code 透传 + subPath；下行深链恢复 + `?subPath=` 启动一次性消费 + upgrade 防死循环）、SESSION_EXPIRED（401 风暴去重）、NO_PERMISSION（生命周期去重）、DEVICE_CHANGE（暂存 + 可选 PC/mobile 站点切换）、LOADING/PORTAL_HREF/SET_TITLE 常量 |

## 1. 与 topic 方案的关键差异（适配本仓）

| 维度 | topic | 本仓（science-pc） |
|---|---|---|
| systemCode | `topic` | **`display`**（用户裁定 2026-10-23） |
| 权限码前缀 | `menu:topic:*` | `menu:display:*`（清单同步更新 71 处） |
| 路由前缀 | `/tts/svcz/` | `/tid/`（`base.ts` 既有，未动） |
| 本地权限矩阵 | `src/perms/matrix.ts`（L0-L4） | **无**——独立态 v-permission 走 `roles`；guard 独立态无权限拦截（现状） |
| navItem query | 同 path 多菜单靠 query 区分 | 静态路由无 query；URL 反查仅按 pathname 后缀匹配（`portalUrlCoversNav` 简化） |
| 无权限回落 | `permissionFallback` + review store | 同款 fallback（无 review 依赖），零授权时落 `home` |
| request.ts | 无 Message.error 通用弹错 | 保留本仓 `Message.error` + traceId 语义；鉴权分支置换为嵌入/独立分流 |
| 登录 | mock 登录为主 | 真实 OAuth2（pigx）仍在——独立态登录流未动，嵌入态由门户接管 |

## 2. 产物清单

**新增 `src/portal/`（9 文件）**：
- `index.ts`（唯一出口）、`embed.ts`（嵌入判定）、`messenger.ts`（iframe-bridge SDK + origin 白名单）
- `auth.ts`（portal_access_token Cookie / resolveAccessToken / SSO 跳转）、`perms.ts`（权限数据源 store + URL 反查）
- `route-sync.ts`（PAGE_READY + ROUTE_CHANGE 双向 + subPath 深链）、`sessionExpired.ts`（401/424/文案统一识别 + 上报去重）
- `noPermission.ts`（no.permission 上报去重）、`device-switch.ts`（device.change → 站点切换，env 未配则不跳）
- `portal.selfcheck.mjs`（静态断言 self-check，含菜单树桶合并语义复算块）

**改造既有（10 文件）**：
- `src/router/menu.ts`：navItem 加 `permCode` 参数（35 菜单机械推导）+ `getSidebarNavGroups` 过滤 + `meta.perms` 注入
- `src/router/guard.ts`：嵌入态登录判定（门户 Cookie）+ 权限统一校验 + 无权限回落
- `src/router/permissionFallback.ts`（新增）：同组回落
- `src/router/types.d.ts`：`RouteMeta.perms`
- `src/directive/permission.ts`：双模式 + watch 重算
- `src/main.ts`：嵌入态接线（load + routeSync + deviceSwitch）
- `src/utils/request.ts`：`systemCode: display` 头 + `resolveAccessToken` + 鉴权错误嵌入/独立分流
- `src/layouts/DefaultLayout.vue`：`is-portal-embed` 类 + 顶栏/侧栏 `v-if="!isEmbedded"` + 侧栏权限过滤
- `src/assets/layout/layout.css`：`.is-portal-embed` 满高贴边规则
- `.env.development` / `.env.production`：`VITE_PORTAL_ORIGINS`（+dev `VITE_PORTAL_PERM_SOURCE=mock`）
- `docs/门户菜单权限注册清单.md`：systemCode `display` + `menu:display:*` 全量替换 + §四 落地状态更新

## 3. 验收证据（三绿）

| 检查 | 结果 |
|---|---|
| `node src/portal/portal.selfcheck.mjs` | ✅ OK（43 条断言 + 桶合并语义复算） |
| `pnpm type-check`（vue-tsc --build） | ✅ 0 error |
| `pnpm build` | ✅ 26.92s 成功（存量 chunk 体积告警与本任务无关） |

## 4. 架构合规自检（公约 §2）

| 铁律 | 结论 |
|---|---|
| 调用链 前端→网关→用户中心 | ✅ `/admin/get-permission-info` 经网关直调 upms-biz（对齐 topic 已实测链路），前端不直连 |
| D12 不接 demo-* | ✅ 无涉及 |
| 可观测 observability | ✅ request.ts X-Trace-Id/traceparent 链路未动，token 透传兼容 |
| USE_MOCK=false 零 fixture | ✅ 权限 mock 独立开关（基础设施，非业务数据），默认关闭 |
| 人工验收闸门 | ✅ 全部改动停本地工作区，未 commit/push，待孔东验收 |
| 公约 §7 registry | ✅ task-create / task-claim（human:孔东）/ update-status 全程 MCP |

## 5. 待联调事项

1. 门户侧以 `systemCode=display` 注册应用与菜单（按 `docs/门户菜单权限注册清单.md`，`menu:display:*` 码值即本仓 `navItem.permCode`）
2. 实嵌联调时删 `.env.development` 的 `VITE_PORTAL_PERM_SOURCE=mock` 走真实接口（payload 反查明细有单行日志）
3. 生产域名确认后核对 `VITE_PORTAL_ORIGINS` 白名单与 Cookie Domain（须同主域）
4. 与门户确认 `SESSION_EXPIRED`（下划线）/`NO_PERMISSION`（点分）值风格（沿袭 topic 待确认项）
5. 按钮码（`btn:display:*`）门户注册后按需启用接口 2.4（1.4 已含全量集合）

## 6. cost

- model：glm-4.6
- actual_tokens：≈ 210k（估） · actual_cost：≈ $1.2 · cost_warn：green
