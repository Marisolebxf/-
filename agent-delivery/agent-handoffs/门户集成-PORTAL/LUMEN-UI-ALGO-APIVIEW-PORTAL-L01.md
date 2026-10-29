# LUMEN-UI-ALGO-APIVIEW-PORTAL-L01 · 算法库联调台 — 门户 iframe 嵌入 + 统一用户中心接入改造

> 参照实现：`repos/lumen-ui-topic/src/portal/`（任务 `LUMEN-PORTAL-IFRAME-L01`，已评审）
> 方案真源：`agent-delivery/agent-handoffs/门户集成-PORTAL/国科信项目统一门户 iframe 集成技术方案.md`（V1.1，topic 仓 docs 同文）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东`（frontend lead，花名册 `can_supervise_agent: true`） |
| claim_type | `coordinator_dispatch`（用户直接授权创建） |
| 状态 | `integration`（联调中：等 nginx `/dma/algovwz/` 反代 + 门户菜单注册） |
| 说明 | 名词与流程见 [`task-claiming-guide.md`](../../task-claiming-guide.md) |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复刻已评审实现不另起一套；权限链路降级为开关而非删除（服务端接入后恢复接线）；未用 YAGNI 跳过 D8/D9/D10/架构铁律 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 图即契约（架构 / 联调必填）

| 字段 | 值 |
|------|-----|
| diagram_id | 无新增图；复用 `门户集成-PORTAL/统一用户链路图.md` 现有链路 |
| 图 diff | 本仓节点为该图「子系统」位的另一实例（Hash 路由 + /dma/algovwz/ 后缀），未改边与禁止事项 |
| 会签态 | 源图维持原态（未重签） |

## 问题清单

- 服务端（网关/upms）尚未接入统一用户中心校验：`/admin/get-permission-info` 虽可经网关调用，但业务接口鉴权仍走原 PigX OAuth2 token（2026-10-29 用户裁定）。
- 本仓为 **Hash 路由**（topic 为 History）：门户菜单 URL 反查、subPath 深链恢复需取 hash 段路径，已适配并写入 selfcheck 语义复算。
- GitLab 服务器故障（2026-10-29）：本任务全部改动**留本地未 commit/push**（业务仓）；主仓 registry 变更已本地 commit（`72ed6e99`），push 失败待恢复。

## 修改内容

### 一、新增 `src/portal/` 模块（9 文件，复刻 topic 已评审实现 + 本仓适配）

| 文件 | 职责 | 与 topic 差异 |
|---|---|---|
| `embed.ts` | iframe 嵌入判定（`window.parent !== window`，不依赖 URL 参数） | 同构 |
| `messenger.ts` | iframe-bridge postMessage 单例；origin 白名单 + protocol 双校验；Action 常量对齐门户 §16 | 同构 |
| `auth.ts` | Cookie `portal_access_token` 读取 / 嵌入态未登录整窗跳门户 SSO（**real 链路备件，当前 off 未接线**） | 同构 |
| `perms.ts` | 权限源 `/admin/get-permission-info`（v2.5 all/org 双桶合并、忽略 appPermissions、inflight 防并发、loaded 终止态防重拉） | ① **Hash URL 反查**：`…/dma/algovwz/#/entan/basic?embed=true` → 取 hash 段 pathname 匹配 catalog `menuPath`；② 权限码 = **menuPath 恒等映射**（本仓无 PERM_CODES 矩阵）；③ `PORTAL_PERM_OFF` 三态开关 |
| `route-sync.ts` | ROUTE_CHANGE 双向 / `?subPath=` 深链恢复 / PAGE_READY 门禁（等权限就绪；off 态恒真立即发） | 无权限回落 `/home-legacy?noPerm=1`（防 NO_PERMISSION ↔ route.change 死循环）；device.change 仅记录（无移动版仓） |
| `sessionExpired.ts` / `noPermission.ts` | 登录失效 / 无权限上报（去重单发；**real 链路备件，当前 off 未接线**） | source=`lumen-ui-algo-apiview` |
| `index.ts` | 统一出口 | 同构 |
| `portal.selfcheck.mjs` | 纯 Node 静态断言自检（消息格式/嵌入判定/Cookie/权限契约/集成点/Hash URL 反查语义复算） | 本仓版断言 |

### 二、接线（当前态 = 权限 off）

| 文件 | 改动 |
|---|---|
| `src/main.ts` | 嵌入态初始化：`usePortalPermStore().load()`（off 态直接置成功）+ `setupPortalRouteSync(router)` |
| `src/router/index.ts` | 统一「无 token → `loginWithDefaultAccount()` 静默自动登录」，失败才落 `/login` 兜底；无门户 Cookie/权限拦截（off 态） |
| `src/utils/request.ts` | 401/424 → **默认账号静默重登 + 重放一次**（`__retried` 防循环；`/auth/oauth2/token` 端点自身 401 只清 token 不递归）；不跳登录页、不读门户 Cookie、不上报 session_expired（off 态） |
| `src/layout/AlgoShell.vue` + `src/assets/main.css` | `is-portal-embed` 类：嵌入态隐藏侧栏/顶栏/汉堡/按钮区，内容区满高贴边（单列网格） |
| `vite.config.ts` | `base: '/dma/algovwz/'`（门户部署后缀） |
| `env.d.ts` / `.env` / `.env.example` | `VITE_PORTAL_ORIGINS` / `VITE_PORTAL_LOGIN_URL` / `VITE_PORTAL_PERM_SOURCE`（三态 off/real/mock）类型声明与文档化 |

### 三、并行会话产物（同工作区，一并挂本任务验收）

`src/utils/session.ts`（默认账号单飞静默登录）、`src/utils/singleFlight.js`(+d.ts)、`src/utils/singleFlight` 测试、`src/config/app.ts` 的 `DEFAULT_CREDENTIALS`、`LoginView.vue` 预填对齐、`components.d.ts` —— 与本任务 off 态链路天然耦合（request.ts 静默重登直接消费）。

### 四、门户注册清单

`scripts/gen-portal-menu-doc.mjs` 增 `basePath`（与 vite base 一致，防 URL 双前缀）→ regenerate `docs/门户菜单权限注册清单.md`（9 目录 · 92 菜单，path 已带 `/dma/algovwz/#/…` 完整形态，域名仍占位 `algo.itic-sci.com`）。

## 测试结果

| 项 | 命令 | 结果 |
|---|---|---|
| 门户接入自检 | `node src/portal/portal.selfcheck.mjs` | ✅ OK |
| 类型门 | `npm run type-check`（vue-tsc --build） | ✅ |
| 生产构建 | `npm run build` | ✅（dist/index.html 资源已带 `/dma/algovwz/` 前缀） |
| 既有测试 | `npm test`（node --test） | ✅ 120/120 |
| 清单再生成 | `node scripts/gen-portal-menu-doc.mjs` | ✅ pages 91 / excluded 37，无双前缀 |

本地 iframe 自验（建议，参照 topic《门户接入本地联调指南》）：hosts 指向 + mkcert 证书 + 最小宿主页验证 `page.ready`/`route.change`/`?subPath=` 深链。

## 遗留风险

1. **门户联调未做**（integration 阶段待办）：需 nginx `/dma/algovwz/` 反代落地 + 门户侧按清单注册菜单（systemCode=`algo`）后，在体验环境 `https://edu.itic-sci.com/portal` 实测 iframe 通信与 Cookie 域覆盖。
2. **权限链路 off**：服务端接入统一用户中心校验后，`.env` 改 `VITE_PORTAL_PERM_SOURCE=real` 并恢复三处接线（request.ts 的 Cookie token + session_expired、router guard 拦截、systemCode 头）——参照 topic `src/portal/` 同构恢复，selfcheck 已内含 real 链路断言。
3. **并行会话产物归属**：`session.ts`/`singleFlight` 等默认账号静默登录链路由另一会话产出，已核实与本任务互不覆盖；验收时请一并走查。
4. **域名占位**：清单 base 域名 `algo.itic-sci.com` 待正式域名确认后 regenerate。
5. **生产 CSP**：正式域名定后配置 `frame-ancestors https://edu.itic-sci.com`（k8s/nginx 侧）。

## CI/CD（必填）

- 分支：业务仓 `dev`（改动**留本地**，未 commit/push——GitLab 故障）；主仓 `dev`（registry 变更已本地 commit `72ed6e99`，push 失败待恢复）
- commit：无（见上）
- pipeline URL / ID：N/A（GitLab 故障，未触发）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：N/A
- dev 测试 URL / 命令与结果：本地 `npm run dev`（:3100）；验证命令见「测试结果」表，全绿

## 可观测性（建议）

- OTEL_SERVICE_NAME：N/A（本任务未动观测配置；request.ts 既有 X-Trace-Id/traceparent 链路保持）
- traceId（dev 抽样）：未采样（本地静态验证）
- Tempo / Loki：无新增

## 涉及文件

**业务仓 `repos/lumen-ui-algo-apiview`（本地未提交）**

- 新增：`src/portal/{embed,messenger,auth,perms,route-sync,sessionExpired,noPermission,index}.ts`、`src/portal/portal.selfcheck.mjs`、`src/utils/session.ts`、`src/utils/singleFlight.{js,d.ts}`、`scripts/single-flight.test.mjs`、`docs/门户菜单权限注册清单.md`、`scripts/gen-portal-menu-doc.mjs`
- 修改：`src/main.ts`、`src/router/index.ts`、`src/utils/request.ts`、`src/layout/AlgoShell.vue`、`src/assets/main.css`、`vite.config.ts`、`env.d.ts`、`.env`、`.env.example`、`src/config/app.ts`、`src/views/LoginView.vue`、`components.d.ts`

**主仓 `gkx-orchestration`**

- `agent-delivery/task-registry.yaml`（新任务 `LUMEN-UI-ALGO-APIVIEW-PORTAL-L01`，本地 commit `72ed6e99` 待 push）
- `agent-delivery/agent-handoffs/门户集成-PORTAL/LUMEN-UI-ALGO-APIVIEW-PORTAL-L01.md`（本文件）
