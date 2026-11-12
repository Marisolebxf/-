# FE-TOPIC-SMALL-PORTAL-L01 · 专题小屏·门户接入与站点切换

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东`（2026-11-11 用户会话裁定，由曹丽影改） |
| claim_type | `pull` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8/D9/D10、可观测埋点；portal 移植以 PC 仓已评审实现为真源整份复用，仅做仓间适配（nav 结构差异/request 签名/source 标识），未另起一套 |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（前端接入任务，无存储流/架构图变更；调用链 = 前端 → Java REST → /admin/get-permission-info，符合 D2/架构铁律） |
| 图 diff | 无 |
| 会签态 | N/A |

## 问题清单（联调实录与修复账本，按时间序）

| # | 症状 | 根因 | 修复 |
|---|------|------|------|
| 1 | mobile 配置文件未接门户，统一用户中心不可用 | P0 移植缺口 | portal 10 文件 + env（PORTAL_ORIGINS/LOGIN_URL）+ request/main/守卫接线 |
| 2 | `VITE_APP_API_URL` 指旧 NodePort 30891 | 口径漂移 | 对齐 PC：`https://edu.itic-sci.com/tts/lumen/api`，proxy 恒剥 /api |
| 3 | get-permission-info 不带 token | `config/app.ts` 漏 `!isEmbedded &&`（PC 单源逻辑） | 嵌入态 ENABLE_MOCK_AUTH 强制 false |
| 4 | 401 后不触发重新登录 | 缺独立 SSO 链路 | ssoCallback/api/sso/ssoLogin/authRedirect 四件套 + 守卫 SSO 分支 + VITE_SSO_CALLBACK_URL（msvcz） |
| 5 | iframe 内配错站不自切 | 嵌入闸门全挡 | 嵌入态放开 UA 兜底 + 宽度监听（后经 #7 收敛） |
| 6 | iPad/触屏跨 767 断点两站互踢乒乓 | 判定线不对称（PC 按 UA、mobile 按宽度） | 统一判定线 + matchMedia 不直接用 matches |
| 7 | 500px 切移动站后权限请求被 cancel 又弹回 | iframe 宽度=门户容器宽 ≠ 设备宽，与 device.change 双头打架 | 嵌入态仅 UA 兜底，宽度监听回归仅独立态 |
| 8 | 门户头已切移动、iframe 不动 | 方案 §16：isMobile 随 route.change 下发（device.change 可选），未处理 | route.change 携带 isMobile 且变化时 switchSite + messenger 全量打印 |
| 9 | 拖窄门户宽度整页每秒闪烁死循环 | 移动站嵌入态反向 UA 兜底把门户 isMobile=true 顶回 PC | **移动站嵌入态不自行切站**（判定权归门户）+ switchSite 风暴闸门 3s（两仓） |

## 修改内容

**mobile 仓（lumen-ui-topic-mobile，本任务主仓）**：
- `src/portal/` 10 文件：auth/embed/messenger/perms/route-sync/sessionExpired/noPermission/portalMenuCodeResolve/device-switch/index（自 PC 仓移植+适配：授权单位=nav path、source=lumen-ui-topic-mobile、request 泛型签名）
- 独立 SSO 四件套：`src/utils/ssoCallback.mjs`+`.d.mts` / `src/api/sso.ts` / `src/utils/ssoLogin.ts` / `src/utils/authRedirect.ts`
- `src/utils/request.ts`：resolveAccessToken（嵌入态门户 Cookie）+ systemCode=topic + 401/424 分流（iframe 上报/独立 SSO/本地登录三路）
- `src/router/index.ts`：守卫 SSO 分支（未登录跳用户中心/回调换票/dev bounce）+ nav path 权限过滤
- `src/main.ts`：嵌入态预拉权限+route-sync+未登录跳门户 SSO+device 监听+authRedirect handler
- `src/shell/nav.ts`（47 项 PC path 对齐）+ `src/router/index.ts`（59 路由全量）+ `src/views/NotAdaptedView.vue`
- `src/shell/MobileShell.vue`：嵌入态隐藏顶栏/侧栏（is-portal-embed）+ 侧栏权限交集过滤
- `src/config/app.ts`：ENABLE_MOCK_AUTH 嵌入态强制 false
- env：VITE_PORTAL_ORIGINS / VITE_PORTAL_LOGIN_URL / VITE_SSO_CALLBACK_URL / VITE_TOPIC_*_URL / VITE_APP_API_URL 网关口径
- 自检：`scripts/portal-wiring.test.mjs`（门户接线契约）/ `scripts/device-switch.test.mjs` / `scripts/nav-paths.test.mjs` / `scripts/breakpoints.test.mjs` 更新

**PC 仓（lumen-ui-topic，配合改动）**：
- `src/portal/device-switch.ts`：独立访问自动落站 + matchMedia 767 监听（仅独立态）+ 嵌入态正向 UA 兜底 + 风暴闸门
- `src/portal/messenger.ts`：↓recv/↑send 全量控制台打印（生产可见）
- `src/portal/route-sync.ts`：route.change 携带 isMobile 接切站
- env：VITE_TOPIC_MOBILE_URL / VITE_TOPIC_PC_URL

## 测试结果

- mobile：`pnpm test` 20 文件全 pass / `pnpm type-check` exit 0 / `pnpm build` 绿
- PC：`portal.selfcheck.mjs` OK / `pnpm type-check` exit 0 / `pnpm build` 绿
- 线上实测（用户联调确认）：Cookie 登录态 ✅、get-permission-info 鉴权 ✅（修 #3）、门户菜单 code 下发 ✅、SSO 回调已通（用户 2026-11-11 22:20 确认）、切站往返 ✅（修 #9 后无闪烁）、`/tts/msvcz` 反代与 `/api` 网关 401 形状与 PC 一致（curl 验证）

## 遗留风险

- P4 联调清单剩余 3 项未显式验证：no.permission 无权限上报门户表现、session_expired 过期跳登录、?subPath= 刷新深链恢复（建议 QA 段 E 补测）
- 门户 isMobile 断点与设备 UA 不一致的语义分歧（桌面拖窄门户=移动形态）已按"判定权归门户"收敛；若甲方要求"设备形态以 UA 为准"需与门户侧（李占伟团队）对齐
- CMS/VIZ/门户页当前为 NotAdaptedView 兜底，批 5（FE-TOPIC-SMALL-CMS-VIZ-L01）替换
- 规划 v2 待孔东/曹丽影签认（R3 CMS 口径、排期认可）

## CI/CD（必填）

- 分支：`dev`（双仓）
- commit：mobile `aea3ea2..d143367`（8 笔）；PC `8dc4e22..81c7d1b`（6 笔）
- pipeline：push 后 CI 自动（GitLab）；K8s dev 自动 rollout
- 部署：mobile NodePort 30902 / 域名 `https://edu.itic-sci.com/tts/msvcz/`；PC `/tts/svcz`
- dev 测试 URL：门户 iframe 内 + 独立访问均已实测（见测试结果）

## 可观测性（建议）

- 前端 observability.ts 埋点链路保持（X-Trace-Id/traceparent 每请求附带）
- messenger 全量打印保留生产（现场排障依据）；Tempo/Loki 深链配置沿用 PC 口径

## 涉及文件

- 主仓：`agent-delivery/工程过程/02-策划与监控/02-智树工作计划/02-进度/系统-06-专题小屏复刻规划.md`（v2，进度回填见同提交）
- mobile 仓 25+ 文件 / PC 仓 6 文件（明细见"修改内容"）
