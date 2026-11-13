# FE-DISPLAY-SMALL-INFRA-L01 · 展示小屏·基础通用建设（portal/SSO/设备切站/请求层）

> 任务：把 lumen-ui-topic-mobile 已验证的门户接入 / 独立 SSO / 设备切站 / 请求层四套基础设施移植到 lumen-ui-science-mobile，并同步修 lumen-ui-science-pc 切站死链。只做基础通用建设，不复刻业务页面。
> 提示词真源：`agent-delivery/prompts/FE-DISPLAY-SMALL-INFRA-L01-展示小屏基础通用建设提示词.md`
> 先例 handoff：`FE-TOPIC-SMALL-PORTAL-L01.md`（九坑全记录）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull` |
| 锁定窗口 | 2026-11-13 14:43 +08:00 起 4h |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 同构移植任务：优先整份复制已评审实现、只做四类参数适配（R1–R6 / §2 差异表），零新依赖（R2），未用 YAGNI 跳过任何公约要求 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A（基础设施移植，无存储流/架构图改动） |
| 图 diff | 无 |
| 会签态 | N/A |

## 问题清单

1. **外部依赖（上线前必须确认）**：`https://edu.itic-sci.com/tid/mobile/?callback=true` 须在统一用户中心登记为 redirect_uri。本机无法核验用户中心控制台，未登记则独立 SSO 回调 401——**联调时发现未登记立即上报监管人，不自行改回调地址凑合**（提示词 §2 阻塞项）。
2. 提示词 §1.2 G6 写「nav 全量对齐 PC menu.ts 40 项」：PC `router/menu.ts` 实际为 **39 项** navItem（含 `trend/tech-situation-maintain` 维护管理 + policy 组 7 项）。本次按 PC 实际 39 项全量对齐（`nav-paths.test.mjs` 双向 diff 为零）。
3. `VITE_REVIEW_MODE=true` 现状保留未动（提示词 §5：属业务批次范畴）。
4. `VITE_PROXY_KEEP_API_PREFIX` 已随 `.env.development` 重写移除（提示词 P4 第 4 条「清理未接线的死配置」选项 A）；vite proxy 现与 PC 仓同语义（目标为非本机网关 URL 时不剥 `/api` 前缀，由网关处理）。
5. science-mobile 工作区在开工前已有 2 个业务文件未提交改动（`TechDevelopmentPlanView.vue`、`planSamples.ts`，内容为预警文案去时间戳），属其他会话活产物，本任务未触碰（R1 红线核验时排除这两文件）。
6. 本机为孔东机（`fe-local-no-auto-commit.mdc` 2026-11-12）：全程零自动 commit / 零自动 push，改动停在工作区；提示词「每 P 一个 commit 停点」降级为「每 P 一个自检停点」。**2026-11-13 用户逐字指令「commit、push」后已提交推送**（见 CI/CD 节），其他会话的 2 个业务文件（`TechDevelopmentPlanView.vue`、`planSamples.ts`）仍未提交、留在工作区。

## 修改内容

### lumen-ui-science-mobile（主仓，G1–G9）

| 缺口 | 交付 |
|------|------|
| G1 portal 层 | `src/portal/` 10 文件（auth/embed/messenger/perms/route-sync/sessionExpired/noPermission/portalMenuCodeResolve/device-switch/index）；source 标识 `lumen-ui-science-mobile`；perms mock 菜单 URL 换 `/tid/` 前缀；device-switch env 名 `VITE_SCIENCE_*_URL`、记忆键 `gkx-display-device-manual` |
| G2 SSO 四件套 | `src/utils/ssoCallback.mjs` + `.d.mts`（纯函数逐字移植）、`src/api/sso.ts`（1.1/1.2/1.3）、`src/utils/ssoLogin.ts`、`src/utils/authRedirect.ts` |
| G3 dev 截获 | `src/utils/captureDevSsoToken.ts`；main.ts **第一条副作用 import**（先于 router 读 location，防回跳死循环） |
| G4 systemCode | request.ts 拦截器 `config.headers.systemCode = 'display'` |
| G5 401/424 三路分流 | request.ts：嵌入态 → `notifyPortalSessionExpired`（iframe 上报门户）；独立 SSO 态 → `triggerAuthRedirect` 整页跳用户中心；mock 态 → 本地 /login。mock token 不带 Bearer（`shouldAttachBearerToken`） |
| G6 菜单/权限 | `src/shell/nav.ts` 全量对齐 PC menu.ts **39 项**（新增 trend 维护管理 + policy 4 页）；`navIcons.ts` 补 5 个 icon key（governance/parse/compare/report/maintain）；路由表由 `allNavItems()` 生成，未适配页挂新 `NotAdaptedView.vue`（提示 + PC 深链 + 返回首页）；守卫接 `shouldLoadPortalPerms` + nav path 授权单位过滤；`config/app.ts` `ENABLE_MOCK_AUTH = !isEmbedded && …`（嵌入态强制 false）；MobileShell 嵌入态隐藏顶栏/侧栏（`is-portal-embed`）+ 侧栏权限交集过滤；main.css 补嵌入态满高贴边 |
| G7 设备切站 | `device-switch.ts` topic 完整版：同域比 path 前缀（`resolveHistoryBase`）、风暴闸门 3s、嵌入态不自行切站、DEV 不落站、767 断点监听仅独立态、`setupDeviceSiteSwitch` 下行监听不区分嵌入态 |
| G8 env 六件 | `.env.development` / `.env.production`：`VITE_PORTAL_ORIGINS` / `VITE_PORTAL_LOGIN_URL` / `VITE_SSO_CALLBACK_URL=https://edu.itic-sci.com/tid/mobile/?callback=true` / `VITE_SCIENCE_MOBILE_URL` / `VITE_SCIENCE_PC_URL`；dev `VITE_APP_API_URL` 从 NodePort 30891 对齐 PC 网关口径 `https://edu.itic-sci.com/tid/api/` |
| G9 五件自检 | `scripts/portal-wiring.test.mjs`（含 PC 仓联动断言）、`device-switch.test.mjs`、`nav-paths.test.mjs`（双向 diff 零 + 标题对齐）、`sso-token-capture.test.mjs`、`router-base.test.mjs`（补切站剥/拼前缀复算） |

附带：`src/utils/auth.ts` TOKEN_KEY 统一为 `access_token` + 旧 key 迁移（同域双前缀与 PC 共享 localStorage，key 不一致切站后对侧读不到令牌——topic 2026-11-12 同款坑前置规避）；`src/api/auth.ts` 适配 request 泛型新签名（剥 envelope 后直取 `access_token`）。

### lumen-ui-science-pc（配合修复）

- `src/portal/device-switch.ts`：升级 topic 版完整逻辑——**删除 `origin === origin` 早退守卫**（同域双前缀下切站永远不执行的死链根因），补 path 前缀判定 + `stripHistoryBase` 剥前缀拼目标前缀 + 风暴闸门 3s + 独立访问 autoLanding（UA+宽度）+ 767 断点监听（仅独立态）+ 嵌入态正向 UA 兜底（手机 UA → 移动站，方向与门户指令一致不打架）+ 手动记忆键 `gkx-display-device-manual`
- `src/main.ts`：挂载前 `autoLandingByDevice()`
- `src/portal/index.ts`：导出 `autoLandingByDevice` / `switchSite`
- `.env.development` / `.env.production`：补 `VITE_SCIENCE_MOBILE_URL=https://edu.itic-sci.com/tid/mobile/`、`VITE_SCIENCE_PC_URL=https://edu.itic-sci.com/tid/`

### 测试脚本适配

- `scripts/breakpoints.test.mjs`：路由断言从 `TREND_PAGES[...] ?? placeholder` 更新为 `ADAPTED_PAGES[...] ?? notAdapted`（placeholder 机制升级为 NotAdaptedView 兜底，断言意图不变）

## 测试结果

| 检查 | 命令 | 结果 |
|------|------|------|
| mobile 自检（25 项含五件新脚本） | `pnpm test` | ✅ 25 pass / 0 fail |
| mobile 类型 | `pnpm type-check` | ✅ exit 0 |
| mobile 构建 | `pnpm build` | ✅ built in 7.83s |
| PC portal selfcheck | `node src/portal/portal.selfcheck.mjs` | ✅ OK |
| PC 类型 | `pnpm type-check` | ✅ exit 0 |
| PC 构建 | `pnpm build` | ✅ built in 41.16s |
| R1 红线 | `git diff`（双仓） | ✅ 无 `src/views/{trend,talent,data}/**` 本任务改动（既有 2 文件为其他会话产物，见问题清单 5） |

### P5 走查清单（**待部署后执行**，本机仅静态自检）

- [ ] 门户 iframe 内打开：Cookie 登录态、get-permission-info 带 token、侧栏按权限过滤
- [ ] 独立手机 UA 打 `https://edu.itic-sci.com/tid/mobile/`：SSO 跳转 → 回调换票 → 落回原 path（无死循环）
- [ ] 桌面 UA 打 mobile 站：自动落 PC 站；门户 device.change 双向切站往返无闪烁
- [ ] `?subPath=` 深链刷新恢复；session_expired 上报后门户跳登录
- [ ] `/tid/mobile` 反代下 `/api` 401 响应形状与 PC 站一致（curl 对照）
- [ ] dev 环境 `captureDevSsoToken`：`#access_token=…` URL 自动清洗入 localStorage

> 走查依赖 K8s dev 发布（push 后 CI 自动 rollout）；按本机规约改动停在本地工作区，走查顺延至部署后。

## 遗留风险

1. **redirect_uri 登记**（问题清单 1）：上线前须在用户中心登记并实测独立 SSO 回调；未登记则手机独立访问不可用（嵌入态不受影响）。
2. **门户菜单树注册**：门户侧需为展示系统移动站配菜单（`/tid/mobile/...` URL）。perms 反查依赖门户 menus 树里出现移动站 URL 或 PC URL（`portalUrlCoversNav` 后缀匹配可命中 `/tid/...`，PC 与 mobile 菜单若在门户注册为同一棵树则天然共享授权）——若门户按站点分开注册，须保证移动站 URL 进树，否则嵌入态全量无权限。
3. P5 走查六项未执行（依赖部署），本次以五件自检脚本 + 双仓三绿代替静态验证；联调阶段如遇问题按九坑对策表（提示词 §4）排查。
4. `components.d.ts` 变更为 Vant unplugin 自动生成（NotAdaptedView 引入 van-empty/van-button 触发），非手写。

## CI/CD（必填）

- 分支：双仓 `dev`，已按用户 2026-11-13 逐字指令「commit、push」完成提交推送
- commit：`lumen-ui-science-mobile` `a9929e7..b3491b4`（feat(portal) 四套基础设施 36 文件 +2092/-39）；`lumen-ui-science-pc` `6849aea..6cd0fec`（fix(portal) device-switch 同域切站死链修复 5 文件 +125/-20）
- pipeline：已触发（双仓 push → CI → K8s dev rollout，随后续验证为准）
- K8s rollout：随 CI 自动进行
- dev 测试 URL：未发布；本地 `pnpm dev`（mobile :3100）可用

## 可观测性（建议）

- traceparent 头保持（request.ts 拦截器 `X-Trace-Id` + `traceparent`，未动既有 observability.ts）
- OTEL_SERVICE_NAME：N/A（前端仓）

## 架构合规自检（DoD 第 6 条）

| 铁律 | 结果 |
|------|------|
| D12 无 demo-* 引用 | ✅ `git diff` 双仓零 `demo-` 字样；调用链只经 `gkxlumen-platform-gateway`（`/api` 反代） |
| 调用链不越层 | ✅ 前端 → 网关 `/admin/*`（用户中心）/ 业务 `/api`，无直连 Python、无 nGQL |
| 可观测埋点 | ✅ traceparent/X-Trace-Id 全请求保留（移植前后一致） |
| 前端规约 R2 零新依赖 | ✅ portal 层纯 postMessage + fetch，未动 package.json |
| systemCode 口径 | ✅ `display`（用户中心区分子系统，对齐 PC 仓） |

## 涉及文件

**lumen-ui-science-mobile**（新增 12 / 修改 12）：
- 新增：`src/portal/`（10 文件）、`src/api/sso.ts`、`src/utils/{ssoCallback.mjs,ssoCallback.d.mts,ssoLogin.ts,authRedirect.ts,captureDevSsoToken.ts}`、`src/views/NotAdaptedView.vue`、`scripts/{portal-wiring,device-switch,nav-paths,sso-token-capture}.test.mjs`
- 修改：`src/main.ts`、`src/router/index.ts`、`src/utils/request.ts`、`src/utils/auth.ts`、`src/api/auth.ts`、`src/config/app.ts`、`src/shell/{nav.ts,navIcons.ts,MobileShell.vue}`、`src/assets/main.css`、`scripts/{breakpoints,router-base}.test.mjs`、`.env.development`、`.env.production`、`components.d.ts`（自动生成）

**lumen-ui-science-pc**（修改 5）：
- `src/portal/device-switch.ts`、`src/portal/index.ts`、`src/main.ts`、`.env.development`、`.env.production`
