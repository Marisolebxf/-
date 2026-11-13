# 展示小屏·基础通用建设 · 跑任务提示词（FE-DISPLAY-SMALL-INFRA-L01）

> **用法**：本文件整段复制到**新会话**作为第一条消息即可开工。
> **形态**：`FE-TOPIC-SMALL-PORTAL-L01`（专题小屏门户接入，2026-11-11 完成）的同构移植，目标仓换成展示系统双仓。
> **编写日期**：2026-11-13 · **编写人**：`agent:frontend-agent`（经验萃取自 lumen-ui-topic → lumen-ui-topic-mobile 复刻全程）
> **先例真源**：`agent-handoffs/FE-TOPIC-SMALL-PORTAL-L01.md`（9 个联调坑全记录）+ `repos/lumen-ui-topic-mobile/src/portal/`（已评审实现）

---

## 0. 任务一句话

把 `lumen-ui-topic-mobile` 已验证的**门户接入 / 独立 SSO / 设备切站 / 请求层**四套通用基础设施，移植到 `lumen-ui-science-mobile`（并同步修 `lumen-ui-science-pc` 切站老版本），让展示系统小屏站具备与 PC 站同等的登录、权限、切站、网关调用能力。

**只做基础通用建设，不复刻任何业务功能页面。**

## 0.1 范围铁律（先读三遍）

| # | 约束 | 说明 |
|---|------|------|
| R1 | **禁止触碰业务页面** | `src/views/trend|talent/data/**` 现有 17 页挂点、placeholder 机制、批 A/B 页面一律不动；本任务只改基础设施层 |
| R2 | **不加新依赖** | Vant/Arco/Pinia 已装；portal 层零依赖（纯 postMessage + fetch） |
| R3 | **不复刻 PC 业务交互** | 页面复刻归 `FE-DISPLAY-SMALL-BATCH-*` 业务批次；本任务完成后业务批次只管往 `ADAPTED_PAGES` 挂组件 |
| R4 | **提交纪律** | 前端仓完工**停在本地工作区**，人工确认后才 push（`fe-manual-confirm-push.mdc`）；例外须当次对话显式声明「完工即推」 |
| R5 | **同域双前缀** | 展示系统 PC = `https://edu.itic-sci.com/tid/`，移动 = `https://edu.itic-sci.com/tid/mobile/`；一切切站判定按 **path 前缀**，不比 origin |
| R6 | **调用链铁律 D12** | 只经 `gkxlumen-platform-gateway` 调 `gkxlumen-*`；禁止引用任何 `demo-*` 服务 |

## 0.2 你是谁

执行 agent = `frontend-agent`，双仓作业、按仓切 commit 前缀：

| 仓 | 角色 | 分支 | 改动占比 |
|---|------|------|---------|
| `repos/lumen-ui-science-mobile`（主仓） | `[agent:frontend-agent]` | `origin/dev` | ~85% |
| `repos/lumen-ui-science-pc`（配合） | `[agent:frontend-agent]` | `origin/dev` | ~15%（仅 device-switch 升级 + env） |

禁止 force push；同仓串行，不跨仓留半成品。

---

## 1. 现状与差距（2026-11-13 实测）

### 1.1 lumen-ui-science-mobile 已有（不要重建）

- ✅ `src/router/base.ts`：`MOBILE_BASE = '/tid/mobile/'`，`resolveHistoryBase` / `stripHistoryBase` 已就位（commit 86a82b9）
- ✅ `src/utils/request.ts`：axios 封装、traceparent 头、ApiEnvelope、401 跳本地 /login（待升级三路分流）
- ✅ `src/api/auth.ts`：OAuth2 密码模式登录（mock 态用）
- ✅ Vant 4 + Arco icon、`pnpm test`（node --test scripts/*.test.mjs）框架
- ✅ 路由骨架：`TREND_PAGES` 挂点 + placeholder 兜底 + `/display/*` 旧前缀 redirect

### 1.2 缺口清单（本任务交付物）

| # | 缺口 | 参照实现（topic-mobile 同路径文件） |
|---|------|-----------------------------------|
| G1 | 整个 `src/portal/` 层（0 文件） | `src/portal/` 10 文件：auth / embed / messenger / perms / route-sync / sessionExpired / noPermission / portalMenuCodeResolve / device-switch / index |
| G2 | SSO 四件套 | `src/utils/ssoCallback.mjs` + `.d.mts`、`src/api/sso.ts`、`src/utils/ssoLogin.ts`、`src/utils/authRedirect.ts` |
| G3 | dev 自动登录截获 | `src/utils/captureDevSsoToken.ts`（main.ts 第一行 import） |
| G4 | `systemCode` 请求头 | request.ts 拦截器补 `config.headers.systemCode = 'display'` |
| G5 | 401/424 三路分流 | request.ts：iframe → session_expired 上报门户 / 独立 SSO → 重登跳用户中心 / mock → 本地 /login |
| G6 | 菜单权限接线 | nav 全量对齐 PC `src/router/menu.ts`（40 项）+ permCode + 守卫过滤 |
| G7 | 设备切站（mobile 侧） | `autoLandingByDevice` + `setupDeviceSiteSwitch`（完整版） |
| G8 | env 六件 | `VITE_PORTAL_ORIGINS` / `VITE_PORTAL_LOGIN_URL` / `VITE_SSO_CALLBACK_URL` / `VITE_SCIENCE_MOBILE_URL` / `VITE_SCIENCE_PC_URL` / `VITE_APP_API_URL` 网关口径 |
| G9 | 自检脚本 | portal-wiring / device-switch / nav-paths / router-base / sso-token-capture 五件 |

### 1.3 lumen-ui-science-pc 配合修复（必改，否则切站死链）

- `src/portal/device-switch.ts` 是**老版本**：`if (target.origin === window.location.origin) return` —— 两站同域（edu.itic-sci.com），**这个守卫导致切站永远不执行**。必须升级到 topic 版完整逻辑（见 §3 P3）。
- `.env.production` / `.env.development` 均未配 `VITE_SCIENCE_MOBILE_URL` / `VITE_SCIENCE_PC_URL` → 升级后的 device-switch 无 URL 可跳。

---

## 2. 展示系统专属参数（与专题系统的差异表）

| 参数 | 专题系统（参照） | **展示系统（本次）** |
|------|----------------|-------------------|
| PC 站点 | `/tts/svcz/` | **`https://edu.itic-sci.com/tid/`** |
| Mobile 站点 | `/tts/msvcz/` | **`https://edu.itic-sci.com/tid/mobile/`** |
| history base 常量 | `/tts/msvcz/` | `/tid/mobile/`（**已就位，勿改**） |
| systemCode 头 | `topic` | **`display`** |
| 权限码前缀 | `menu:topic:*` | **`menu:display:<组>:<项>`**（PC `router/menu.ts` 的 `navItem()` 机械推导） |
| SSO 回调 | `…/tts/msvcz/?callback=true` | **`https://edu.itic-sci.com/tid/mobile/?callback=true`** |
| dev 网关 | `…/tts/lumen/api` | **`https://edu.itic-sci.com/tid/api/`**（对齐 PC 仓 .env.development） |
| 设备 URL env 名 | `VITE_TOPIC_*_URL` | **`VITE_SCIENCE_MOBILE_URL` / `VITE_SCIENCE_PC_URL`**（PC 仓老代码已用此名，沿用） |
| portal source 标识 | `lumen-ui-topic-mobile` | **`lumen-ui-science-mobile`** |
| portalMenuCodeResolve | nav path → topic 菜单码 | 按 PC `menu.ts` permCode 映射重写 |

> **开工前外部依赖（阻塞项，开工即确认）**：`https://edu.itic-sci.com/tid/mobile/?callback=true` 须在**统一用户中心登记 redirect_uri**。未登记则独立 SSO 回调 401——发现未登记立即上报监管人，不要自行改回调地址凑合。

---

## 3. 工作分解（P0→P5 串行，每 P 一个 commit 停点）

### P0 · portal 层 10 文件移植

从 `repos/lumen-ui-topic-mobile/src/portal/` 整份复制到 science-mobile，逐文件做四类适配：

1. import 路径里的 `@/utils/request` 泛型签名差异（两仓 request.ts 导出形状不同，以 science-mobile 现状为准微调）
2. `source` / 日志前缀改成 `lumen-ui-science-mobile`
3. `portalMenuCodeResolve.ts`：授权单位改为 PC `router/menu.ts` 的 path + permCode 映射
4. `device-switch.ts`：env 变量名改 `VITE_SCIENCE_*_URL`（逻辑见 P3）

**验收**：`portal.selfcheck.mjs`（PC 仓有同款）在 mobile 仓跑通。

### P1 · 独立 SSO 链路（四件套 + 截获）

1. `ssoCallback.mjs` + `.d.mts` 原样移植（纯函数零依赖，12 个导出逐一核对：`shouldUseStandaloneSso` / `isSsoCallbackSearch` / `readAuthCode` / `readSsoState` / `safeReturnPath` / `pathForSsoState` / `isDevBounceOrigin` / `devBounceState` / `parseDevBounceState` / `devBounceLocation` / `readDevAccessTokenHash` / `stateForSsoRedirect`）
2. `src/api/sso.ts`：`fetchSsoAuthorizeUrl` + `exchangeSsoCode`（走 request.ts，`skipAuth: true`）
3. `ssoLogin.ts` + `authRedirect.ts` 移植，`SSO_CALLBACK_URL` 读 `VITE_SSO_CALLBACK_URL`
4. `captureDevSsoToken.ts`：**main.ts 第一条副作用 import**（在 router 读取 window.location 之前，否则 SSO 回调 hash 被守卫当未登录 → 重新发起授权 → **回跳死循环**，topic 生产实录）
5. 路由守卫加 SSO 分支：未登录且 `useStandaloneSso()` → `redirectToStandaloneSso(to.fullPath)`；回调 search（`?callback=true&code=…`）→ 换票 → `safeReturnPath` 落回

### P2 · 菜单 / 路由 / 权限全量对齐

1. `src/shell/nav.ts` 全量对齐 PC `src/router/menu.ts` **40 个 navItem**（path 一字不差，含 permCode）
2. 未适配页统一挂 `NotAdaptedView`（新写：提示「小屏适配中」+ 返回首页，不 404）
3. 守卫接线：嵌入态 `usePortalPermStore.load()` 拉取 `get-permission-info`，按 permCode 过滤侧栏与路由；无权限 → `notifyPortalNoPermission`
4. **`config/app.ts`：`ENABLE_MOCK_AUTH` 嵌入态强制 false**（否则 get-permission-info 不带 token，必 401）
5. `MobileShell.vue`：嵌入态隐藏顶栏/侧栏（`is-portal-embed` class）+ 侧栏权限交集过滤

### P3 · 设备切站（双仓，含 PC 修复）

**mobile 仓**（topic-mobile `device-switch.ts` 完整版移植）：

- `autoLandingByDevice()`：main.ts 挂载前调用；`import.meta.env.DEV` 不启用（设备仿真会把联调页弹去部署站）；`window.parent !== window`（嵌入态）不自行切站
- `shouldUsePcSite()` 判定线（与 PC 仓对称，防乒乓）：移动 UA → 移动站；触屏 + 宽 ≤767 → 移动站；其余（含 iPad 820/1024）→ PC 站；`sessionStorage['gkx-display-device-manual']='1'` 时跳过
- `switchSite(isMobile)`：**同域双前缀比 path 前缀不比 origin**（`resolveHistoryBase` 判「已在目标站」）；剥当前站前缀拼目标前缀，保留 search/hash（SSO ticket 不丢）
- **切站风暴闸门 3s**（模块级 `lastSwitchAt`）
- `setupDeviceSiteSwitch()`：监听门户 `device.change`（清记忆立即执行）+ `route.change` 携带 `isMobile` 变化时切站；**下行监听不区分嵌入态**（独立打开经 window.open 转发也要响应）

**PC 仓（science-pc，修死链）**：

- `device-switch.ts` 升级为 topic 版完整逻辑：删掉 `origin === origin` 早退守卫（同域前缀切换失效根因），补独立访问 autoLanding + 767 宽度监听（仅独立态）+ 风暴闸门 + 嵌入态正向 UA 兜底（手机 UA → 移动站，方向与门户指令一致不打架）
- 双仓 `.env.production` 补：`VITE_SCIENCE_MOBILE_URL=https://edu.itic-sci.com/tid/mobile/`、`VITE_SCIENCE_PC_URL=https://edu.itic-sci.com/tid/`

### P4 · 请求层口径统一

1. request.ts 拦截器：`config.headers.systemCode = 'display'`（用户中心按此区分子系统）
2. 401/424 分流三路（替换现在「一律跳本地 /login」）：
   - 嵌入态门户 Cookie 失效 → `notifyPortalSessionExpired()`（iframe 上报门户，**不能在 iframe 里渲染本地登录页**）
   - 独立 SSO 态 → `triggerAuthRedirect` → 整页跳用户中心重登
   - mock 态 → 本地 `/login?redirect=…`（现状保留）
3. mock 登录 token 不带给真网关（`ENABLE_MOCK_AUTH=true` 时不挂 Bearer，防 424「用户凭证已过期」）
4. `.env.development`：`VITE_APP_API_URL` 从旧 NodePort `http://10.50.69.111:30891` 对齐 PC 口径 `https://edu.itic-sci.com/tid/api/`；vite proxy 剥 `/api` 前缀逻辑与 PC 一致；清理未接线的 `VITE_PROXY_KEEP_API_PREFIX`（或接线，二选一，不留死配置）
5. `main.ts` 完整接线（顺序即契约）：

```
import '@/utils/captureDevSsoToken'   // ① 永远第一
autoLandingByDevice()                 // ② 挂载前
if (isEmbedded && !hasPortalSession()) redirectToPortalLogin()
if (isEmbedded) { usePortalPermStore.load(); setupPortalRouteSync(router) }
setupDeviceSiteSwitch()               // ③ 不区分嵌入态
setAuthRedirectHandler(...)           // ④ 401 三路分流入口
mount
```

### P5 · 自检 + 联调走查

移植五件自检脚本（`scripts/*.test.mjs`，topic-mobile 同名文件改参数）：

| 脚本 | 断言 |
|------|------|
| `portal-wiring.test.mjs` | portal 10 文件导出齐全、main.ts 接线顺序、env 变量存在 |
| `device-switch.test.mjs` | 同域比 path 前缀、风暴闸门、判定线对称、手动记忆键 |
| `nav-paths.test.mjs` | mobile nav 与 PC menu.ts 40 项 path 全量 diff 为零 |
| `router-base.test.mjs` | `/tid/mobile`、`/tid/mobile/xxx`、根路径三态解析 |
| `sso-token-capture.test.mjs` | hash/search token 截获 + URL 清洗 + returnPath |

全绿后走查清单（每项留证据截图/curl）：

- [ ] 门户 iframe 内打开：Cookie 登录态、get-permission-info 带 token、侧栏按权限过滤
- [ ] 独立手机 UA 打 `https://edu.itic-sci.com/tid/mobile/`：SSO 跳转 → 回调换票 → 落回原 path（无死循环）
- [ ] 桌面 UA 打 mobile 站：自动落 PC 站；门户 device.change 双向切站往返**无闪烁**
- [ ] `?subPath=` 深链刷新恢复；session_expired 上报后门户跳登录
- [ ] `/tid/mobile` 反代下 `/api` 401 响应形状与 PC 站一致（curl 对照）
- [ ] dev 环境 `captureDevSsoToken`：`#access_token=…` URL 自动清洗入 localStorage

---

## 4. 九坑对策表（topic 联调实录，全部前置规避）

| # | 症状 | 根因 | 对策（本任务直接落地） |
|---|------|------|----------------------|
| 1 | 切站按钮点了没反应 | 同域双前缀下 `origin===origin` 早退 | 判「已在目标站」比 **path 前缀**（§3 P3） |
| 2 | 拖窄门户宽度整页每秒闪烁 | 两站互踢 | 移动站嵌入态**不自行切站**（判定权归门户）+ 3s 风暴闸门 |
| 3 | iPad 跨 767 断点两站乒乓 | 判定线不对称 | 统一判定线（§3 P3），两仓同一条代码语义 |
| 4 | 500px 门户宽度切站后权限请求被 cancel | iframe 宽度=容器宽≠设备宽 | 宽度监听**仅独立态**；嵌入态只认门户指令 |
| 5 | 门户头已切移动、iframe 不动 | 方案 §16 isMobile 随 route.change 下发 | route.change 携带 isMobile 且变化时切站 |
| 6 | 生产 SSO 回跳死循环 | 截获晚于 router 读 location | captureDevSsoToken **main.ts 第一行** |
| 7 | get-permission-info 不带 token | 嵌入态 mock auth 没关 | `ENABLE_MOCK_AUTH` 嵌入态强制 false |
| 8 | 本地联调整页弹去部署站 | dev 也启用了落站 | `import.meta.env.DEV` 直接 return |
| 9 | 独立打开收不到门户下行消息 | 监听只挂嵌入态 | 下行监听不区分 isEmbedded；上行 send 仍限嵌入态 |

## 5. 环境（建完后 science-mobile 三个 env 文件最终形态）

```ini
# .env.production / .env.development 共有
VITE_PORTAL_ORIGINS=https://edu.itic-sci.com
VITE_PORTAL_LOGIN_URL=https://edu.itic-sci.com/uc/sso/login
VITE_SSO_CALLBACK_URL=https://edu.itic-sci.com/tid/mobile/?callback=true
VITE_SCIENCE_MOBILE_URL=https://edu.itic-sci.com/tid/mobile/
VITE_SCIENCE_PC_URL=https://edu.itic-sci.com/tid/

# .env.development 额外
VITE_APP_API_URL=https://edu.itic-sci.com/tid/api/     # 对齐 PC 仓
# .env.production 额外
VITE_APP_API_URL=                                        # K8s nginx 反代 /api → gateway
```

> `VITE_REVIEW_MODE` 现状 `true`，属业务批次范畴，本任务**不强制改**（handoff 里注明即可）。

## 6. DoD（验收即本表）

1. G1–G9 九缺口全闭合；R1 红线零违反（`git diff` 不含 `src/views/{trend,talent,data}/**` 业务改动）
2. `pnpm test`（含五件新自检）/ `pnpm type-check` / `pnpm build` 全绿（双仓）
3. §3 P5 走查清单全过，证据入 handoff
4. PC 仓 device-switch 死链修复 + 双仓 env URL 配齐
5. handoff：`agent-handoffs/FE-DISPLAY-SMALL-INFRA-L01.md`（含问题清单、测试证据、cost 四字段回填 registry）
6. 架构合规自检：D12（无 demo-* 引用）、调用链、可观测埋点（traceparent 保持）逐条 ✅

## 7. 完成后

- 代码停在本地工作区，报监管人人工确认后 push（R4）
- registry：`FE-DISPLAY-SMALL-INFRA-L01` → `integration`，note 写「联调确认：…」
- 后续业务批次（`FE-DISPLAY-SMALL-BATCH-B` 及新增页）依赖本任务产出往 `ADAPTED_PAGES` 挂组件即可
