# SYSINT-SIT-02-L01 · 科技发展态势三要素供数 · 规格

> WBS-02-02｜registry id `SYSINT-SIT-02-L01`｜repo `lumen-ui-science-pc`（本叶范围）
> 监管人 `human:李伟`｜执行 `agent:frontend-agent`｜effort 8｜difficulty L
> 本文件为执行前规格，**待签字确认后**进入实施。人工验收闸门：改动停本地，不 commit/push。

## 1. 目标（DoD 原文）
1. 页面上的三要素（技术 / 技术链 / 科研机构）区块**经网关**「有数或空态」；前端**不直连**久新。
2. 不把 SCI-INT 的「待确认」写成「已接入」；空态**不用 fixture 填数**。
3. **本叶不拆**；页面计划里后端归徐滕强的页若要单独成叶，另开任务，不在本叶共管。
4. 菜单以**相对路径**进入统一用户中心；**企业不写成科研机构**。

## 2. 现状事实（已核实，2026-10-29）
| 页面(M) | 前端 API 文件 | 网关 BASE 现状 | 后端控制器 | 结论 |
|---|---|---|---|---|
| M1 科技全域态势 | `api/situation/index.ts` | `/display/v1/situation` | SituationController | 已接通；timeline/events 走空态 shim |
| M2 科学技术全景 | `api/situation/panorama.ts` | `/situation/v1/panorama` ❌ | 无 | **未接通** |
| M3 技术发展跟踪 | `api/situation/tracking.ts` | `/situation/v1/tracking` ❌ | 无 | **未接通** |
| M4 全球创新监测 | `api/situation/globalInnovation.ts` | `/display/v1/situation` | GlobalInnovationController | 已接通 |
| M5 湾区创新监测 | `api/situation/bayAreaInnovation.ts` | `/display/v1/situation` | BayInnovationController | 已接通 |
| M6 深圳创新监测 | `api/situation/shenzhenInnovation.ts` | `/display/v1/situation` | ShenzhenInnovationController | 已接通（allSettled 分区降级） |
| M7 科技创新评估 | `api/situation/innovationEvaluation.ts` | `/situation/v1/innovation-evaluation` ❌ | 无 | **未接通** |
| M8 科技指数 | `api/situation/techIndex.ts` | `/situation/v1/tech-index` ❌ | 无 | **未接通** |
| M9 科技发展规划 | `api/situation/techDevelopmentPlan.ts` | `/situation/v1/planning` ❌ | 无 | **未接通** |
| M10 维护管理 | `api/situation/maintain.ts` | `/situation/v1/maintain` ❌ | 无 | 非三要素页，**默认排除** |

共性缺陷：
- 裸 `fetch()` 绕过 `@/utils/request`（无鉴权头、无统一错误拦截、无 `R{code,data}` 解包）。
- 非 2xx 直接 `throw new Error`，不是「有数或空态」，且页面可能白屏。
- `tracking/index.vue` 用 `dataset ?? ({} as TrackingDataset)` 传组件，空对象下访问必填字段会崩。

## 3. 范围裁定（已确认 2026-10-29 · human:李伟）
- **A. 页面范围 = SRS 9 页（M1–M9，196 叶）**：registry 的「8 页」按文档勘误处理；**M10 维护管理排除**（非三要素页，不接线）。M1 已接通，纳入回归验证但不在本叶重做。
- **B. 后端缺口处置**：M2/M3/M7/M8/M9 后端无控制器。本叶**只做前端网关接线 + 诚实空态**，不新建后端控制器（后端归属徐滕强另开叶）。
- **C. 供数路径**：遵守 A3 过渡期许可——前端只经 `/display/**`，**不直连久新 Doris**；久新直连由 Java 侧（徐滕强范围）按架构基线执行，本叶不落任何 JDBC/HTTP 直连代码。

## 4. 变更设计（决策完成，逐文件）

### 4.1 新增公共件（第二处出现即封装）
新文件 `lumen-ui-science-pc/src/api/situation/honestEmpty.ts`：
- `NOT_IMPLEMENTED_STATUS = [404, 405, 501]`
- `optionalClient`（独立 axios 实例，baseURL = `BASE_URL`，无全局拦截器）
- `unwrap<T>(body)`
- `optionalPost<T>(fullPath: string, data: unknown, empty: T): Promise<T>`：命中 404/405/501 → `console.warn` + 返回 `empty`；其他错误照常 throw。
- `post<T>(fullPath: string, data?: unknown): Promise<T>`：正常网关 POST，走 `@/utils/request`。

`api/situation/index.ts` 改为从 `honestEmpty.ts` 导入 `optionalPost` / `unwrap` / `optionalClient`，删除本地重复实现（行为不变）。

### 4.2 逐文件接线
| 文件 | 改动 |
|---|---|
| `panorama.ts` | `BASE` → `/display/v1/situation/panorama`；`post` 改用公共 `post` |
| `tracking.ts` | 路径 → `/display/v1/situation/tracking/{meta,dataset}`；`fetch` → `optionalPost`；`real` 返回 `TrackingMetaResult \| null` / `TrackingDataset \| null`（404 时 null），新增 `EMPTY_TRACKING_DATASET`（`isEmpty:true`、全部数组 `[]`、对象 `{}`、数值 `0`） |
| `innovationEvaluation.ts` | 路径 → `/display/v1/situation/innovation-evaluation/{meta,snapshot}`；`fetch` → `optionalPost`；新增 `EMPTY_EVALUATION_META` / `EMPTY_EVALUATION_SNAPSHOT` |
| `techIndex.ts` | 路径 → `/display/v1/situation/tech-index/dataset`；`fetch` → `optionalPost`；新增 `EMPTY_TECH_INDEX_DATASET` |
| `techDevelopmentPlan.ts` | 路径 → `/display/v1/situation/planning/dataset`；`fetch` → `optionalPost`；新增 `EMPTY_PLAN_DATASET` |
| `maintain.ts` | **仅在确认纳入时**：路径 → `/display/v1/situation/maintain/meta`；否则不动 |

### 4.3 页面容错（防止空态白屏）
- `views/situation/tracking/index.vue`：`loadMeta()` 加 `try/catch`（null 时保留 null）；模板 `dataset ?? ({} as TrackingDataset)` 改为 `dataset ?? EMPTY_TRACKING_DATASET`；`meta?.timeline.years` 改 `meta?.timeline?.years`。
- 其余 4 页（panorama/evaluation/techIndex/plan）在空态时由既有 `?.`/`??` 兜底；逐页确认无必填字段解构崩溃，必要时补空态提示条（不造数）。

### 4.4 诚实性
- 404/405/501 = 「接口未上线」，控制台 warn + 页面空态；**不弹全局错误**、**不填 fixture**。
- 其它错误（500/网络/鉴权）照常抛出，不掩盖真故障。
- 不新增任何 `metric_id` 手写或就绪度「改绿」。

## 5. 验证（交付三绿）
1. `pnpm type-check`（`vue-tsc --noEmit`）零错误。
2. `pnpm build` 成功。
3. 自检扫描：
   - `src/api` 内 `/situation/v1` 零命中（maintain 如未纳入除外，需登记）。
   - `src/api` 内无久新 JDBC/HTTP 直连（`47.93.119.170` / `test2` / `29030` 零命中）。
   - `USE_MOCK=false` 下无 `@/mock` / demo fixture 填数路径。
   - `src/router/menu.ts` 菜单 `path` 全为相对路径（`${groupKey}/${itemKey}`）。
   - 文案扫描：三要素区块无把「企业」标成「科研机构」的标签。

## 6. 不做（明确边界）
- 不新建/修改后端控制器（徐滕强范围）。
- 不拆叶、不改任务 registry 归属。
- 不 commit / 不 push（等人工验收）。
- 不在本叶处理 M10 维护管理（除非签字纳入）。
