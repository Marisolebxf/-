# LUMEN-PORTAL-IFRAME-L01 · lumen-ui-topic 统一门户 iframe 嵌入对接

> **状态**：开发完成，待联调（integration） · **监管**：human:孔东 · **执行**：agent:frontend-agent
> **commit**：`34f61c5`（重做版）→ `a4549cf`（契约对齐，2026-10-16） · **强度**：ponytail full

---

## 0. 契约对齐更新（2026-10-16，依据 sso-用户中心api.md）

后端（LUMEN-UAC-JAVA-FACADE-L01）最终方案：**前端经网关直调用户中心 upms-biz**（不做 Java 封装层），契约真源 = [sso-用户中心api.md](./sso-用户中心api.md)。已实测网关 `http://111.198.38.90:50199/admin/get-permission-info` 转发生效（无 token / 假 token 均返 `401 + {"code":401,"msg":"访问令牌不存在"}`，与文档 §6 一致）。`a4549cf` 对齐内容：

| 改动 | 说明 |
|---|---|
| `src/portal/perms.ts` | 假想契约 `GET /portal/v1/permission-info` → 真实接口 1.4 `GET /admin/get-permission-info`（Bearer + systemCode，axios baseURL=/api 剥前缀）。**菜单级码（menu:topic:*）挂 `menus` 树节点 `permission` 字段**，深度收集后与顶层按钮码集合（btn:topic:*）合并去重；`PortalUserInfo` 对齐 `userId/username/realName`；`load()` 共享 inflight Promise（修 main.ts 预取与 router guard 并发时误判未加载 → 误发 NO_PERMISSION 串页的时序 bug）；mock 数据改为与真实 `data` 同构（树形），仍走同一规范化路径 |
| `src/utils/request.ts` | token 失效识别补 **HTTP 401** 与 **『访问令牌不存在』**（原文只认 424/token expired，用户中心口径会漏）；嵌入态触发 `SESSION_EXPIRED` 上报交门户接管 |
| `.env.production` | 补 `VITE_PORTAL_ORIGINS = https://edu.itic-sci.com`（CI 构建产物嵌入态 postMessage 白名单不再为空） |
| `src/portal/portal.selfcheck.mjs` | 断言同步：真实路径 `/admin/get-permission-info`、`collectMenuPermissions`、`inflight`、`status === 401` |

**遗留**：`.env.development` 仍留 `VITE_PORTAL_PERM_SOURCE = mock`（无真 token 时本地联调用；门户侧实嵌联调时删除该行走真实接口）。登出（接口 1.5 `/admin/logout`）与按 menuId 拉按钮权限（2.4 `/admin/page-permission`）本轮未接——1.4 已含完整权限集合，2.4 等门户侧按钮码注册后按需启用。

---

## 1. 范围与实现（对照方案 V1.1）

| 方案条目 | 实现 | 文件 |
|---|---|---|
| §12.2 嵌入模式 | 双信号判定（`?embed=true` && `parent!==window`）；嵌入时隐藏顶栏/侧栏/评审 persona 切换器，内容区满高贴边（`is-portal-embed` 类） | `src/portal/embed.ts`、`DefaultLayout.vue`、`layout.css` |
| §11/§16.1 iframe-bridge | messenger 单例；统一消息格式（protocol/version/id/action/data）；**origin 白名单 + protocol 双校验**（补齐文档示例缺口）；上行逐 origin 指定 targetOrigin 禁 `*` | `src/portal/messenger.ts` |
| §16 接入步骤 2 | 首路由就绪后上报 `PAGE_READY {source:'lumen-ui-topic', title}` | `src/portal/route-sync.ts` |
| §16 ROUTE_CHANGE | 双向：afterEach 上报 `{code(透传门户下发), subPath}`；下行消费 `subPath` 恢复深链（启动 `?subPath=` 一次性消费）；DEVICE_CHANGE 暂存 | 同上 |
| §8.2.1/§16-4 Cookie 登录态 | 读 `portal_access_token`（实测非 HttpOnly、Domain=`.edu.itic-sci.com`）注入 authStore → axios Bearer；嵌入态未登录 **top 跳门户 SSO**，不渲染本地 login（§12.2/12.3） | `src/portal/auth.ts`、`guard.ts`、`main.ts` |
| §13.4 登录过期 | 嵌入态 401/424 → 上报 `SESSION_EXPIRED` 交门户，不清本地不跳转；独立态保持现状 | `request.ts` |
| §13.3 无权限 | 嵌入态守卫拦截 → 上报 `NO_PERMISSION`，本地降级页兜底 | `guard.ts` |
| 权限改造（用户要求） | `v-permission` 嵌入态比对门户权限码集合（恒等映射：门户注册值=本地 PERM_CODES 值），`updated` 钩子支持权限异步到达重算；侧栏 `getSidebarNavGroups` 双模式切换数据源 | `directive/permission.ts`、`DefaultLayout.vue`、`portal/perms.ts` |
| 权限源 | Java 封装用户中心接口 1.4（**human:淮政伟 排期中**）；假想契约 `GET /portal/v1/permission-info`(Bearer)，`VITE_PORTAL_PERM_SOURCE=mock` 同构演示，接口就绪删此行即切真实 | `portal/perms.ts` |
| 本地联调 | mkcert https（证书存在才启用，无证书回落 http 不影响他人）；hosts `topic.edu.itic-sci.com`；宿主页自验模板 | `vite.config.ts`、`docs/门户接入本地联调指南.md` |

集中封装：各页面统一 `import { ... } from '@/portal'`（唯一出口 `src/portal/index.ts`）。

## 2. 偏离说明

1. **docs/ 在 .gitignore 中**：对接文档与联调指南以未跟踪文件存在于仓内 `docs/`（与招标/门户文档同路径惯例）；指南真源已同步本 handoff 摘要。如需入库需调整 ignore 规则（待 PM 决定）。
2. **`NO_PERMISSION`/`SET_TITLE` 消息值**：文档 §11.3/§13.3 未给值，按点分命名空间推断（`no.permission`/`set.title`），联调时与门户实际监听对齐，改常量一行。
3. **`.gitignore`/`vite.config.ts`/`.env.development` 修改**：属任务必要配置变更（+`.certs/` 忽略、dev https、门户 env），按公约报备。

## 3. 产物清单

- 代码：`src/portal/`（7 文件）+ 6 个既有文件改造，`7af1203` → origin/dev ✅
- 文档：`docs/门户接入本地联调指南.md`（含 mkcert 步骤/自验模板/约束表）
- self-check：`node src/portal/portal.selfcheck.mjs`（消息格式/双信号/Cookie/集成点静态断言）

## 4. 验收证据

| 检查 | 结果 |
|---|---|
| `node src/portal/portal.selfcheck.mjs` | ✅ OK |
| `npm run type-check` | ✅ 0 error |
| `npx eslint`（本任务全部改动文件） | ✅ 0 error（仓内存量 44 error 与本任务无关，stash 验证确认） |
| `npm run build` | ✅ 40.63s 成功 |
| CI | push 后观察 Pipeline（K8s dev rollout） |

## 5. 架构合规自检（公约 §2）

| 铁律 | 结论 |
|---|---|
| 调用链 前端→Java→… | ✅ 权限经 Java 封装接口（1.4），前端不直连用户中心 |
| D12 不接 demo-* | ✅ 无涉及 |
| 可观测 observability | ✅ request.ts 埋点链路未动，token 透传兼容 |
| USE_MOCK=false 不 fixture 填数 | ✅ 权限 mock 独立开关（基础设施，非业务数据），默认关闭走真实接口 |
| 公约 §7 registry | ✅ 全程 MCP 操作（claim/in_progress/fields） |

## 6. 待联调事项（下一阶段）

1. 门户体验环境配临时菜单 → 实嵌联调（PAGE_READY/loading/布局/深链）
2. ~~Java 接口（淮政伟）就绪 → 删 `VITE_PORTAL_PERM_SOURCE=mock` 对齐字段~~ → **已对齐**（2026-10-16 前端直调方案，见 §0；mock 开关留待实嵌联调时移除）
3. 与门户确认：`SESSION_EXPIRED` 值风格、`NO_PERMISSION`/`SET_TITLE` 值、Cookie Domain 笔误（`.edu` vs 文档 `.itic-sci.com`）
4. 用户中心注册应用（Client ID/Secret，宋泉）→ ~~Java 侧配置~~ → 前端直调方案下仅需 systemCode=topic 已生效；注册流程用于门户侧菜单/按钮码配置（见 `docs/门户菜单权限注册清单.md`）
5. 正式域名（须 `*.edu.itic-sci.com` 下）→ 生产 CSP `frame-ancestors`

## 7. cost

- model：glm-4.6（本会话累计，含方案评审阶段）
- actual_tokens：≈ 260k（估） · actual_cost：≈ $1.5 · cost_warn：green
