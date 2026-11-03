# POL-L2-DS10-SENT-SSO-L01 · 舆情 jobs 401 重登引导 + systemCode 头补齐

- 任务：`POL-L2-DS10-SENT-SSO-L01`（前端修复，lumen-ui-science-pc）
- 日期：2026-11-04（01:40–02:20）
- 监管：`human:淮政玮`
- 执行：`agent:frontend-agent`
- 强度：ponytail full
- commit：lumen-ui-science-pc dev `1e9e0c9`（已推 origin/dev）；编排仓本文 + 截图
- 后续基线修复（同任务会话产出，已推 origin/dev）：`66e37cb`（补提交遗漏的 `shared/reportExport.ts`，修复 CI job #23696）、`9ee8d51`（tracking 类型空值安全加固 + meta 口径字段对齐，清除 23 项基线 type 错误）

## 1. 根因链（已查实，父会话提供 + 本会话复核确认）

线上 trace `67a60eb3`（2026-11-04 00:42:40）：浏览器 → display `POST /display/v1/policy/panorama/jobs`（sub_type=policy_effect）→ async-service 拒收「未获取到当前用户」。

display 日志原文（两条）：

1. `sso check-token non-zero: code=401 msg=访问令牌已过期` —— UC 令牌过期，`SecurityUtils.getUser()=null`，`currentUserId()=null`，body 无 user_id。
2. `sso introspect: unknown systemCode=null` ×6 —— 部分请求未带 systemCode 头。

前端侧根因：`panoramaGet/panoramaPost`（src/api/policy.ts）用 `optional:true + headers:{skipErrorToast:true}`，401 被 optional 静默吞掉——用户只见任务失败红条，没有「请重新登录」引导。

## 2. 修复点（commit 1e9e0c9，4 文件 +90/-6）

### 2.1 jobs 两入口改走 Authed 辅助（不再 optional 静默）

`src/api/policy.ts` 新增 `panoramaGetAuthed` / `panoramaPostAuthed`（无 `optional`，保留 `skipErrorToast: true`——任务卡已有红条文案，避免双重弹窗）：

- `panoramaJobs`（POST /jobs，J1「开始分析」/ J10「重新分析」）→ `panoramaPostAuthed`
- `panoramaJobDetail`（GET /jobs/{taskId}，轮询与当天复用查询）→ `panoramaGetAuthed`

401/过期文案由 `@/utils/request` 响应拦截器既有分支统一引导（复用既有链路，不自造第二套登录逻辑）：

- 嵌入态：`notifyPortalSessionExpired()` 上报门户 SESSION_EXPIRED，由门户统一跳登录；
- 独立态：`removeToken()` + `triggerAuthRedirect()` → `redirectToStandaloneSso()` 整页跳 UC SSO。

其余 GET/PUT/DELETE（反馈、报告、收藏、订阅等增强信息）保持 `optional` 静默降级不变——「不能整页其它功能被拖死」要求落实：非 jobs 请求 401 依旧降级空态。

### 2.2 过期文案识别补全

`src/portal/sessionExpired.ts` `isPortalAuthHttpError` 正则补充两条文案：

- `访问令牌已过期`（原正则只认「不存在」，漏判 trace 67a60eb3 场景）
- `sso check-token failed`（display 侧日志原文透传识别）

### 2.3 systemCode=display 头补齐

- `@/utils/request` 请求拦截器**已有**全局 `config.headers.systemCode = 'display'`（2026-10-23 用户裁定已有落点），走 `request` 的全部 `/display/v1/policy/**` 天然带齐——无需改动。
- 唯一绕过全局拦截器的真实网关客户端 `optionalClient`（`src/api/situation/honestEmpty.ts`，裸 axios.create）**缺失**该头 → 已补 `systemCode: 'display'` 默认头。这正是 `unknown systemCode=null` 6 条日志的来源。

### 2.4 自检断言（FE-POL-SENT-LIVE.test.mjs 2b 组）

新增 9 条断言：panoramaJobs/panoramaJobDetail 必须走 Authed 辅助；Authed 辅助不得带 optional、保留 skipErrorToast；isPortalAuthHttpError 须含「访问令牌已过期/sso check-token failed」且落在判定正则内；request 拦截器与 optionalClient 须带 systemCode=display。

## 3. 三绿结果

| 项 | 结果 | 说明 |
|---|---|---|
| node 自检 | ✅ 全绿 | `FE-POL-SENT-LIVE.test.mjs`（含 2b 组 9 断言）+ `portal.selfcheck.mjs`；基线修复后复跑仍全绿 |
| pnpm type-check | ✅ 全绿（终态） | `1e9e0c9` 时点本任务文件 0 错误（仓级 23 项基线遗留见下）；`9ee8d51` 清除全部基线 type 错误后终态 `vue-tsc --build` exit 0 |
| pnpm build | ✅ 全绿（终态） | `66e37cb` 补齐 `reportExport.ts` + `9ee8d51` 类型修复后，`pnpm build`（run-p type-check + vite build）于 2026-11-04 02:0x 本地验证 exit 0（4109 modules，dist 产出完整） |

基线断裂说明（历史时序）：`1e9e0c9` 提交时仓级 type-check/build 失败 23 项，**全部**位于 `src/mock/modules/tracking.ts` / `src/views/situation/tracking/**` / `src/views/situation/global-innovation/index.vue`——基线 `a56ec07`（前序任务提交）引用了**未提交**的 `src/views/situation/shared/reportExport.ts` 且 tracking 类型扩 `number|null` 后未同步调用方。该两处已由本会话以 `66e37cb` + `9ee8d51` 补齐修复（CI job #23696 应随之转绿），与本任务核心改动（policy 401 / systemCode）正交。

## 4. 复验结果

### 4.1 已完成（dev 线上，浏览器 CDP）

- **未登录态访问 `/tid/` → 整页跳 UC SSO 登录页**（`https://edu.itic-sci.com/uc/sso/login?...`，state 带回跳路径）：路由守卫 requiresAuth → redirectToStandaloneSso 链路完整工作。截图 `SSO-01-未登录访问跳UC登录页.png`。
- **已登录态（门户 Cookie 会话）舆情页签操作**：`?tab=sentiment` 打开正常渲染四卡（受众反馈/评估报告/实施效果/匹配推送），点「开始分析」按钮正确进入 submitting→polling 态（按钮 disabled/loading）。截图 `SSO-01-舆情页签初始态.png`、`SSO-02-开始分析提交后.png`。
- 复验时点线上入口 chunk 仍是旧版（鉴权正则无「访问令牌已过期」）——`1e9e0c9` 尚未部署（pipeline #3670 build 红，job #23696）；且后续浏览器会话中断（"No browser tab available" 重试 6+ 次无法恢复），J1 终态渲染未能继续观察。

### 4.2 部署阻塞与处置（如实记录）

- CI `frontend:build` 跑 `npm run build`，被基线 `a56ec07` 的断裂挡住（引用未提交文件 reportExport + tracking 23 个 type 错误），`1e9e0c9` 无法部署。
- **基线已由本会话修复**：`66e37cb`（补提交 `reportExport.ts`）+ `9ee8d51`（tracking 类型加固）均已推 origin/dev，本地三绿验证通过。CI 应随之转绿，`1e9e0c9` 随最近一次成功 pipeline 一同部署。
- 需要人工复验的动作（部署完成后）：登录态过期时在舆情评估页签点「开始分析」应弹重新登录引导（不再静默红条）；正常登录后 J1 开始分析→终态区域表+时序；J10 刷新当天复用直出结果；「重新分析」POST body 带 force:true。

## 5. 截图清单

`agent-handoffs/科技政策跟踪-POL/qa-shots/SENT-QA-L01/`：

- `SSO-01-未登录访问跳UC登录页.png`（未登录访问展示系统被正确引导至 UC SSO 登录页）
- `SSO-01-舆情页签初始态.png`（门户登录态下舆情评估页签四卡正常渲染，实施效果卡 idle 态 +「开始分析」按钮在场）
- `SSO-02-开始分析提交后.png`（J1 点击「开始分析」后按钮正确进入 loading/disabled 提交态；时点为旧版线上构建，修复未部署）

## 6. 未复验项（如实记录，不伪造）

1. **J1 成功终态渲染**（区域表+时序）、**J10 当天复用直出**、**force:true 重新分析**——复验时点线上版本未部署 `1e9e0c9`（基线断裂挡 CI，现已由 `66e37cb`+`9ee8d51` 修复），且浏览器会话在轮询观察期间中断（"No browser tab available"，重试无法恢复）、UC 登录需人工凭证无法自动完成。留给部署后人工走查（监管人已确认自行手动测试）。
2. **401 触发重登引导的端到端截图**（本地 token 过期场景）——线上未部署新构建无法复现；修复链路的路由守卫跳转部分（SSO-01-未登录）已验，拦截器 401 分支逻辑由 2b 组断言覆盖。

## 7. 架构合规自检

- ✅ 未改 Java、未动 D4、未动检索页签逻辑；改动仅在公共头与 jobs 两入口
- ✅ 复用全局 401 引导链路，未自造第二套登录逻辑
- ✅ 非 401 行为（optional 静默空）保持不变
- ✅ 造任务数据零、伪造截图零、未写「联调通过」、未标 done
- ⚠️ CI 红为基线遗留（他人提交断裂），非本提交引入；已在 §4.2 说明处置路径

ponytail: full —— 核心修复 4 文件 +90/-6（`1e9e0c9`）；修复点收敛在 jobs 两入口 + 一条正则 + 一处默认头，其余全部复用既有拦截器链路。基线抢救另耗 `66e37cb`（1 文件补提交）+ `9ee8d51`（3 文件类型加固），均为让 CI/部署通道恢复所必需的最小集。
