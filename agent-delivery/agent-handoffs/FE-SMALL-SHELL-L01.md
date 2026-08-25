# FE-SMALL-SHELL-L01 · 小屏壳 + 宽度断点约定（展示+专题共用）

> 目标仓：`lumen-ui-science-mobile`。专题移动端日后复制 `src/shell/`，不另起断点。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `human:孔东` |
| supervised_by | `human:高颖` |
| claim_type | `pull` |
| Owner | `human:孔东` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 与 DoD 一致。未用 YAGNI 跳过 D8 token、D9 评审层保留、`observability.ts` 请求头、D12 网关指向。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未挂载 Headroom MCP；壳任务无需大日志。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 图 diff | 不改 Java/Python 调用链；前端仍 `/api` → 网关 |
| 会签态 | N/A |
| 说明 | 日常壳，不改拓扑。K8s nginx 从 `demo-platform-gateway` 改为 `gkxlumen-platform-gateway`（D12）。 |

## 范围与实现

- 手机 `≤767px` 用本仓 `MobileShell`（顶栏 + 滑入侧栏 + 列表卡片）。
- 平板走 PC 站收缩（`TABLET_USES_PC_SITE`），本仓宽屏只提示、不叠 PC 侧栏。
- 双系统空路由：`#/display`、`#/topic` 及白名单占位页可进。
- 从 `lumen-ui-algo-apiview` 拷来的算法页/G6/原地图 mock/联调页已删；天地图 Leaflet 作为通用组件重新接入（`src/components/map/`）。
- 组件预览：`#/display/preview`、`#/topic/preview`（侧栏「组件预览」）。样例数据标「预览样例」，不走 `USE_MOCK` fixture。

对照招标：小屏 = 中屏核心裁剪，不是独立 App IA。

## 偏离说明

- 注册表曾写「展示+专题共用仓」；按监管人决定，**壳真源在 science-mobile**，专题复制目录而不是同仓自适应。
- NodePort 定为 `30898`（避开 pc 30891 / topic 30892 / admin 30893 / feishu 30894 / zhiku 30895 / 已占用 30896 / algo 30897）。
- 空壳首页不造统计数字，故无 ⓘ 挂点；`src/review` 保留给后续 BATCH。

## 产物清单

- 断点+裁剪规则：`repos/lumen-ui-science-mobile/docs/小屏断点与裁剪规则.md`
- 可复制壳：`src/shell/`（`MobileShell.vue` / `nav.ts`）
- 通用组件：`src/components/`（`ListCard` / `StatCard` / `QuickFilter` / `ProfileDrawer` / `map/UnifiedLeafletMap`）
- 预览页：`src/views/ComponentPreviewView.vue`
- 本地：`pnpm test` `pnpm type-check` `pnpm build` 绿；`pnpm dev` http://localhost:3101/（3100 占用）

## 验收证据（DoD）

| 条 | 结果 |
|---|---|
| 断点档 + 1 页裁剪规则 | ✅ `PHONE_MAX_PX=767` + 上列文档 |
| 展示与专题导航/抽屉/列表卡片 | ✅ 顶栏切换 + 滑入侧栏 + 首页 ListCard |
| 双系统空壳路由可跑；禁止互斥 display 叠层 | ✅ 仅 MobileShell；无 `display:none` 双树 |
| ponytail lite | ✅ |
| Owner=孔东 | ✅ |

复刻五维：本叶是空壳不是 Demo 复刻。R3 token `#D8E7FC`/`#165DFF`；R5 `USE_MOCK` 默认 false、已删 `@/mock`。V1–V7 / W1–W4 N/A。

## 测试结果

- `pnpm test`：5 passed（断点、无叠层、展示/专题菜单、预览路由）
- `pnpm lint` / `pnpm type-check` / `pnpm build`：通过
- 浏览器：`human:孔东` 已点测登录、展示/专题切换、滑入侧栏、空壳页、组件预览（筛选 / 地图点选 / 底栏抽屉 / ⓘ）

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 150000（in+out 估算；含壳 + 预览组件，会话模型 Cursor Grok 4.6） |
| model_used | `claude-sonnet-4.5`（registry 枚举按 B 档口径） |
| actual_cost | 0.81（frontend 默认 80/20 × B 档 $3/$15 per M） |
| cost_warn | green |

## 遗留风险

- K8s NodePort `30898`；push 后看 GitLab CI / rollout
- 登录默认要 `VITE_ENABLE_MOCK_AUTH=true` 才不打网关（见 `.env.example`）
- `Design.md` §11 仍写「专题不做小屏」，与本 Epic 冲突，待文档回写

## CI/CD（必填）

- 分支：`origin/dev`（`lumen-ui-science-mobile` + `gkx-orchestration`）
- commit：`lumen-ui-science-mobile` `725d7879dabf1eab4829f0bc53b8539950737268`（`origin/dev`）；orchestration 为本 handoff 提交
- pipeline URL / ID：push 后 GitLab `lumen-ui-science-mobile` pipelines
- 部署 namespace / 镜像 tag：CI 触发后填写
- K8s rollout：push 后由 CI 执行；清单 `k8s/lumen-science-mobile.yaml`，网关 `gkxlumen-platform-gateway`
- dev 测试 URL / 命令与结果：本地 `pnpm dev` http://localhost:3101/ ；构建成功；浏览器点测通过

## 可观测性

- 请求拦截器仍写 `X-Trace-Id` + `traceparent`（`src/utils/request.ts`）
- Tempo / Loki：无本叶新配置

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 1 算法只在 Python | ✅ 本仓无算法 |
| 2 调用链 前端→Java→Python | ✅ 仅 `/api` |
| 3 Nebula | ✅ 未引入 |
| 4 可观测 | ✅ trace 头保留 |
| 5 CI/CD | 🟡 已 push `origin/dev`；集群 rollout 以 GitLab CI 为准 |
| 6 demo 不污染 lumen | ✅ |
| 7 方案 A / D12 | ✅ 网关改为 `gkxlumen-platform-gateway`，不再打 demo gateway |
| 8 ADS | ✅ 空壳不读数 |
| 9 D8 | ✅ token / Arco Vue / 触控 44px；排版 lite |
| 10 D9 | ✅ 评审层保留；预览页样例数字挂 MetricMarker +「预览样例」角标，不走业务 fixture |
| 11 D10 | ✅ 抽屉+键盘焦点环；空态 Empty |
| 12 D12 | ✅ 见上 |

## 涉及文件

- `repos/lumen-ui-science-mobile/src/shell/*`
- `repos/lumen-ui-science-mobile/src/config/breakpoints.ts`
- `repos/lumen-ui-science-mobile/docs/小屏断点与裁剪规则.md`
- `repos/lumen-ui-science-mobile/k8s/lumen-science-mobile.yaml`
- `src/components/{ListCard,StatCard,QuickFilter,ProfileDrawer,map/UnifiedLeafletMap}.vue`
- `src/views/ComponentPreviewView.vue`
- 删除算法库组件 / mock / G6；Leaflet 仅作通用地图组件重新加入

## 问题清单

- NodePort 已改为 30898，避开 admin 30893 与已被占用的 30896
- 专题复制壳时改 `nav.ts` 与 `APP_TITLE`
