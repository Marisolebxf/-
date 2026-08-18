# LUMEN-SVC-FE-PORTAL-FULL-L01 · SVC Gate-1：门户五 Tab + 产业级联 + 有数图表

> 日期：2026-08-18  
> Task：`LUMEN-SVC-FE-PORTAL-FULL-L01`  
> 总控：`DEMO-SVC-ABCD-长任务总控.md` / `DEMO-SVC-GATE1-全量派单.md`（已授权 · human:侯佳伟）  
> 上游：`DEMO-SVC-PY-PORTAL-AGG-L01`（integration · topic-py `858af1b`）· `LUMEN-SVC-JAVA-PORTAL-EXT-L01`（Map 透传已够，无 Java diff）

## 任务认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| lock | 24h |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最短 diff：壳级联 + 五页消费 overview 分段；未跳过 D8/D9/D12/调用链；不直连 demo-* / Python |

## 范围与实现

### 调用链（D12）

前端 → `POST /svc/topic/v1/service-portal/overview`（gateway `/api/svc/...`）→ Java `gkxlumen-topic-svc` Map 透传 → Python `/internal/gkx-svc/portal/overview`  
能力榜优先 `overview.capability_rank.items`；缺段才 fallback `POST .../ranking`。

### 五 Tab 对齐

| 路由 | 消费字段 | 有数表现 |
|------|----------|----------|
| `/service-portal/overview` | `trend` / `by_service_type` / `scale_dist` + stages 合计 | 趋势折线·类型环·规模四档；KPI 派生全球约数/新增/环节合计 |
| `/service-portal/industry-distribution` | `industry_distribution.stages` (+ nested type) | 六环节卡（0=暂无覆盖）+ 类型表；热力无矩阵则诚实空 |
| `/service-portal/region-map` | `region_map.{china,global}` | 全球⇄全国榜 + 地图壳 |
| `/service-portal/capability-rank` | `capability_rank.items` | Top 表 + 入篮/画像 |
| `/service-portal/shenzhen` | `shenzhen.{trend,type_dist,districts,key_orgs,sz_total}` | 趋势/类型/十区榜/重点机构；领域段诚实空 |

### 产业级联

- `ServicePortalShell`：`a-cascader` + `servicePortalIndustry.ts`（对齐 demo `industryChainCascadeOptions`）  
- URL `industry=`：`合成生物` 或 `合成生物.生物制造`；空则默认写入 `合成生物`

### D9

- 统计点旁 `ReviewMetricBadges`；`gap` 含 `Q-SVC-010` 时 pending-ref 诚实态  
- 不伪绿；缺段骨架 + 文案「不伪造」

## 偏离说明

- 领域×环节热力、深圳领域分布：门面无矩阵 → **诚实空**（不本地造数）  
- 区域 `global` 与 `china` 同城池（上游 ADS 无国别维）— FE 如实渲染

## 产物清单

| 产物 | 路径 |
|------|------|
| 产业级联 | `repos/lumen-ui-topic/src/views/service-portal/servicePortalIndustry.ts` |
| selfcheck | `.../servicePortalIndustry.selfcheck.mjs` |
| 壳 | `ServicePortalShell.vue` + `servicePortal.css` |
| 五页 | `ServicePortalOverview/IndustryDistribution/RegionMap/CapabilityRank/Shenzhen.vue` |
| 类型 | `src/api/svc/types.ts`（`trend`/`scale_dist`） |
| 本 handoff | `agent-handoffs/服务机构-SVC/LUMEN-SVC-FE-PORTAL-FULL-L01.md` |

## 验收证据

- [x] `node src/views/service-portal/servicePortalIndustry.selfcheck.mjs` → ok  
- [x] `vue-tsc`：本叶 portal 文件无新增错误（仓内既有 analysis 页 TS 债另计）  
- [x] commit `db7e5ac` push `origin/dev`  
- [x] 外网 SPA 路由 HTTP 200：`/service-portal/{overview,industry-distribution,region-map,capability-rank,shenzhen}`  
- [x] 外网 `POST .../api/svc/topic/v1/service-portal/overview` code=0：trend×8 · scale_dist×4 · types×3 · stages.rd=35 · region china×12 · capability items×35 · shenzhen 有  
- [x] GitLab pipeline `5199`（sha `db7e5ac`）：`frontend:build` / `frontend:image` / `deploy:k8s` **success**；`e2e:chain-gold` failed（CHAIN 诊断/深圳空跑用例，非本叶 SVC portal 范围）

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 2 | 前端→Java→`/internal/*` | ✅ 只调 `/svc/topic/v1/service-portal/**` |
| D8 | Design / Arco | ✅ 壳+图表 token 对齐 portal 兄弟页 |
| D9 | 角标 / Q-SVC-010 | ✅ ReviewMetricBadges + pending-ref |
| D10 | 交互 | ✅ 五 Tab + Cascader path-mode / change-on-select |
| D12 | 不调 demo-* | ✅ |
| 复刻五维 | 布局/交互/样式/评审/有数 | ✅ overview 有数；缺段诚实空 |

## Cost

| 字段 | 值 |
|------|-----|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~9 万 |
| actual_cost | 估 <$4 |
| cost_warn | false |

## CI/CD

- 分支：`dev`
- commit：`db7e5ac`
- pipeline：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines/5199
- jobs：`frontend:build` **success** · `frontend:image` **success** · `deploy:k8s` **success**（job 22748）· `trivy:frontend` success  
  - `e2e:chain-gold` **failed**（job 22749：`US-CHAIN-DIAG-03` / `US-CHAIN-SZ-03`；产业链金路径，非本叶门户改动）
- 外网基址：http://111.198.38.90:50892/
- 冒烟：五路由 200；overview sections 齐全（见上）

## 联调确认

联调通过：50892 overview 经 Java Map 透传返回门户扩展 sections；FE 五 Tab + 产业级联已绑 overview 字段并已 `deploy:k8s`；缺段诚实空。下一叶可并行 `LUMEN-SVC-FE-ANALYSIS-FULL-L01`（依赖 Job 白名单 + svcan）。
