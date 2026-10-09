# CROSS-VEC-DEMO-UI-L01 · 政策联调台语义抽槽 + 跑批≤100

> 总控 [`CROSS-VEC-长任务总控.md`](./CROSS-VEC-长任务总控.md)；上游 [`CROSS-VEC-DEMO-API-L01.md`](./CROSS-VEC-DEMO-API-L01.md)。联调台例外：demo UI → demo-platform-gateway → gkx-innov → lumen-algo-py，不是 D12 违规。不是 lumen 复刻单，不走 V1–V7 / fe-replica-visual-dod。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 接单时已 claimed + in_progress；lock 24h |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 挂在已有 BasicPage，复用 `request` / `runPipeline` 轮询 / `SeedHelpBadge` / livePlane。零新 npm。未用 YAGNI 跳过 limit≤100 前端拦、501/400/409 诚实提示、live 禁写、首选+`/innov` fallback。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 单仓单叶，本机未挂 Headroom |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `02-概要设计.md` §3.1（按钮）/ §3.2（Job A） |
| 图 diff | 落实联调台边：`demo-ui-system-test` BasicPage → `demo-platform-gateway` `/policy/v1/**`（404/405 回落 `/innov/v1/**`）→ `gkx-innov` → Feign `lumen-algo-py` `/internal/*`。禁止直连 19530 / TEI / Python。 |
| 会签态 | `v0.3-draft`（抄 02 frontmatter，未自填绿） |

## 范围与实现

**做**：政策「基础指标」页可点语义抽槽与跑批≤100，方便人机验证。不考虑性能。

### 挂载

- 页：政策分析 → **基础指标**（`src/views/policy/pages/BasicPage.vue`，路由 `/policy/basic`）
- 位置：原「灌数据 / 数据同步」头栏**下方**新区块「语义抽槽 · 跑批≤100」
- 按钮文案：**语义抽槽**、**开始跑批**、**续跑**

### API 路径（只打 demo-platform-gateway）

| 用途 | 首选 | fallback（HTTP 404/405 或无路由） |
|---|---|---|
| 按钮抽槽 | `POST /policy/v1/policy/industry/enrich` | `POST /innov/v1/policy/industry/enrich` |
| 跑批 | `POST /policy/v1/industry/jobs/enrich` | `POST /innov/v1/industry/jobs/enrich` |

- 按钮 body：单条 `{"policy_id"}`，多条 `{"policy_ids"}`。**不带** `cursor` / `mode`。
- 跑批 body：`{mode, force, cursor, limit}`；续跑加 `job_id` + `next_cursor`（同时写 `cursor`，对齐 Python）。
- `limit>100`：`enrichLimitBlockReason` 拦截，**不发 HTTP**。
- HTTP 封装：`src/api/policy/index.ts`；组件不写 axios。`skipGlobalError` + `request.ts` 回传 `__status`，以便 400/409/501 诚实 toast。

### 结果展示

- 有 `industry_link_code`（非数字/非 score）显示链码；无码只显示 `{name}`。
- 跑批进度行：`processed / skipped / coded / failed / status / index_version / job_id`。
- 501 / 400 / 409：`ElMessage.error`，空表，不 toast 成功、不填 fixture。
- live 面与灌数据一样禁用写槽。

**不做**：新路由、新 npm、Arco、直连 Python、lumen 网关、万级放开。

## 偏离

| # | 偏离 | 理由 / as-built |
|---|------|-----------------|
| 1 | 本机未对现网网关实打抽槽 | 联调台人机验证；自检 `node src/api/policy/enrich.check.mjs` 锁路径 / limit / 槽展示 |
| 2 | 跑批无独立 status 口，用同一 POST + `sleep` 续跑 | 上游契约即 `job_id`+`next_cursor`；复用本页灌数轮询范式 |

## 产物清单

- `demo-ui-system-test/src/api/policy/index.ts`（enrich 封装 + fallback + limit 闸）
- `demo-ui-system-test/src/api/policy/enrich.check.mjs`
- `demo-ui-system-test/src/views/policy/pages/BasicPage.vue`（联调区块）
- `demo-ui-system-test/src/utils/request.ts`（reject 带 `__status`）
- 本 handoff

## 验收证据

- 自检：`node src/api/policy/enrich.check.mjs` → `policy enrich console check ok`
- 超 100：`enrichLimitBlockReason(101)` 命中封顶文案
- 槽：`chain:INB1303` 显示链码；`score=0.503` 写成 link_code 时只显示 `{name}`
- 人点 3 步见下

### 人怎么点一遍（3 步）

1. 顶栏「政策」保持 **Demo**（live 按钮是灰的），打开 **政策分析 → 基础指标**。
2. 输入一条已在 DWD 的 `policy_id`，点 **语义抽槽**：看表里 coded / skipped / `{name}`；400/501 只报错空表。
3. limit 保持 ≤100，点 **开始跑批**：看 processed/skipped/coded/failed；`status=running` 会自动续跑，也可点 **续跑**。limit 改成 101 应立刻 400、网络面板无请求。

## 问题清单 / 开放项

| # | 事项 | 谁做 | 状态 |
|---|------|------|------|
| A | 现网 Nacos Path 未同步时走 `/innov/v1` fallback | devops / 网关 | UI 已兼容 |
| B | 现网人机实打 search 写槽 | 监管人在联调台点 | 本叶交按钮 |
| C | 万级放开 100 封顶 | 另叶 | 本波验证闸 |

## 修改内容

| 文件 | 行为 |
|------|------|
| `src/api/policy/index.ts` | 抽槽/跑批 POST、首选+innov fallback、limit 闸、槽格式化 |
| `src/views/policy/pages/BasicPage.vue` | 联调区块；live 禁写；400/409/501 诚实提示 |
| `src/utils/request.ts` | 错误对象带 `__status` |
| `src/api/policy/enrich.check.mjs` | 路径 / 闸 / 槽展示自检 |

## 测试结果

- `node src/api/policy/enrich.check.mjs` 绿
- 未直连 Milvus / TEI；零新依赖

## 遗留风险

- Nacos 未扩写且 entan-py catch-all 对未知路径返回 **200 错形**（不是 404）时，不会自动 fallback，须改网关或人改打 `/innov`
- Job A 单飞 409 只提示，不取消已有 running full

## CI/CD（必填）

- 分支：`demo-ui-system-test` `origin/dev`（先 `git pull --ff-only`）
- commit：`c13b81cad9b18028883b2102d45599a9af296508` `feat(policy): add industry enrich console on BasicPage` `[agent:frontend-agent]`
- pipeline：push 触发 GitLab CI `frontend:build`
- K8s rollout：demo-ui-system-test 静态/前端发布
- dev 测试：基础指标页点抽槽 / 跑批

## 可观测性（建议）

- 沿用 `src/utils/request.ts`：`X-Trace-Id` + `traceparent`
- 错误 toast 可带短 traceId（既有 `formatErrorMessage`；本页 4xx/501 走 skipGlobalError 自绘文案）

## 涉及文件

- `src/api/policy/index.ts`
- `src/api/policy/enrich.check.mjs`
- `src/views/policy/pages/BasicPage.vue`
- `src/utils/request.ts`

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 算法只在 Python `/internal/*` | ✅ 前端零 NLP / 零定码 |
| 调用链不可越层 | ✅ 前端 → demo Java 网关 → Python `/internal/*` |
| 图谱仅 Nebula | ✅ 未直连图 |
| 可观测 | ✅ 沿用 request trace 头 |
| CI/CD | ✅ push `origin/dev`，未 force；`[agent:frontend-agent]` |
| D12 | ✅ 本叶是 **demo 联调台**（任务书点名）；只打 `demo-platform-gateway`，禁止 `gkxlumen-platform-gateway` |
| 数据策略 | ✅ live 禁写；失败空表；不填 fixture |
| Java 不写算法 | N/A（本叶无 Java） |
| D8 / D9 / D10 | N/A（联调台 Element Plus，非 lumen 复刻 / 无指标卡） |
| 零新 npm 依赖 | ✅ |

## 成本回填

| 字段 | 值 |
|------|-----|
| actual_tokens | 82000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 0.44 |
| cost_warn | green |

口径：frontend 默认 80/20；B 档 `$3/$15` per 1M；`82000×0.80×3/1e6 + 82000×0.20×15/1e6 = 0.44`。
