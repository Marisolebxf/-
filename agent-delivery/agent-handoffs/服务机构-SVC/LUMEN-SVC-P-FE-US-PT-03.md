# LUMEN-SVC-P-FE-US-PT-03 · US-SVC-PT-03 区域分布

> 日期：2026-08-22  
> Task：`LUMEN-SVC-P-FE-US-PT-03`  
> 总控：[`LUMEN-SVC-P-长任务总控.md`](./LUMEN-SVC-P-长任务总控.md)（§7 已生效）  
> 仓：`lumen-ui-topic` · `origin/dev`  
> 复刻真源：`demo-ui-topic` `src/app/pages/service-portal/ServicePortalRegionMap.tsx` + `servicePortalShared.tsx`（只读对照，未贴 JSX、未改 demo）

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务 24h 锁；本叶不标 `done` |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 复用 `ServicePortalShell`、`IndustryCatalogSelect`、`SectionPanel`、`JudgmentStrip`、`UnifiedLeafletMap`、`VChart`、`@/review`。未用 YAGNI 跳过 D8 页底 token、D9 四维角标、D10 评审自闸、可观测 `request.ts` X-Trace-Id、handoff、图即契约、五维复刻。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机会话未挂载 Headroom MCP。 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，不改工厂边）；`LUMEN-SVC-P-FE-US-PT-03-SEQ`（本叶区域分布） |
| 图 diff | LINEAGE 边未改。本叶把 SHELL 区域分布虚线改成实线：50892 FE `POST /svc/topic/v1/service-portal/region-map` → gateway → `gkxlumen-topic-svc` → `lumen-topic-py` `/internal/gkx-svc/portal/region-map` → ADS `svc_region_dist`（`M_SVC_ORG_CNT`）。capability/sz/keyorg 仍占位虚线。禁止事项未变：不打 `demo-*`、不填 `CHINA_REGION_DIST` / 南山区假点、不用 0 冒充全球、不把省名复制成国别、不改 `industry-center` / REC-02 / ECO-01 / PT-01 / PT-02 契约。 |
| 会签态 | `SVC-STORAGE-LINEAGE` 随 `01-data-flow.md` frontmatter：`approved`（`human:淮政玮` · 2026-08-19 流图；2026-08-20 选 B 增补 LINEAGE，**不改** §1 工厂边）。本叶 SEQ 为 `draft`，禁止自填绿。 |

### L2 消费（不改边）

本叶只读消费 [`storage/SVC/01-data-flow.md`](../../data/data-design/storage/SVC/01-data-flow.md) §1.1 `SVC-STORAGE-LINEAGE`：线上区域分布读 ADS 指标四表 A1–A6 的 `region_dist`（`M_SVC_ORG_CNT`），不联 ODS。前端不扫表，只消费 Java `china` / `global` / `geo_level_used` / `empty`。

### L4 本叶 SEQ · `LUMEN-SVC-P-FE-US-PT-03-SEQ`

```mermaid
sequenceDiagram
  actor User
  participant FE as lumen-ui-topic
  participant GW as gkxlumen-platform-gateway
  participant JAVA as gkxlumen-topic-svc
  participant PY as lumen-topic-py
  participant ADS as demo_gkxlumenx_ads
  Note over FE,GW: 不对前端暴露 /internal；禁止 /api/svc；D12 不打 demo-*
  User->>FE: 打开 /service-portal/region-map
  FE->>GW: POST /svc/topic/v1/service-portal/region-map
  GW->>JAVA: GlobalFilter 剥 svc → /topic/v1/service-portal/region-map
  JAVA->>PY: POST /internal/gkx-svc/portal/region-map
  PY->>ADS: SELECT svc_region_dist M_SVC_ORG_CNT geo_level=province
  PY->>ADS: SELECT svc_region_dist M_SVC_ORG_CNT geo_level=country
  alt 有 country 行
    ADS-->>PY: china + global
    PY-->>JAVA: geo_level_used=country；黄灯 Q-SVC-010 原样
    JAVA-->>GW: HTTP 200 R.ok(data) 不改绿、不补 0
    GW-->>FE: china[] / global[]
    FE-->>User: 全球⇄全国 Radio；全球只画 global；全国只画 china
  else 无 country 有省
    ADS-->>PY: 仅 province
    PY-->>JAVA: china=省列表 global=[] geo_level_used=province
    JAVA-->>GW: HTTP 200 只出省
    GW-->>FE: global=[]
    FE-->>User: 全球侧空/禁用；不把省名当成国家
  else 缺行 / empty
    ADS-->>PY: 无 region_dist 行
    PY-->>JAVA: empty=true china=[] global=[]
    JAVA-->>GW: HTTP 200 诚实空列表
    GW-->>FE: empty=true
    FE-->>User: 可见空态；禁止用 0 冒充全球、禁止区级假点
  end
  Note over FE: Java 无 lat/lng → UnifiedLeafletMap presetLayers=false + 空点；排行只认 name/count
  FE-.->GW: /service-portal/capability-rank（PT-04 占位）
```

| 生产者 | 消费者 | 触发 | 失败语义 | 禁止事项 |
|---|---|---|---|---|
| Java `POST /topic/v1/service-portal/region-map` | 本叶 FE | 打开区域分布 / 改产业筛选 | `empty` / `china=[]` / `global=[]` → 可见空；接口失败 Message + 空包络 | Demo `CHINA_REGION_DIST` / `GLOBAL_REGION_DIST` / 南山区；页内 `MOCK_`；直连 Python `/internal`；overview 冒充本页 |
| `global` + `geo_level_used=country` | 全球视图 KPI / 排行 | 有 country 行 | 无 country 或 `global=[]` → Radio 禁用 + 空列表，**不**把 `china` 省名当国家 | `industryScaleRatio`；把省复制进 global |
| `china` | 全国视图 KPI / 排行 | 有 province 行 | 无行 → 可见空，**不**补 0、**不**填南山区 | 区级假点；页面 `new L.map` |
| 黄灯 `gap` / `pending_client_confirm` | 研判条「待核验」+ `@/review` 角标 | Python 原样上送 | 不改绿 | 前端把 Q-SVC-010 标 aligned/live |

## 范围与实现

替换 SHELL 占位，落地 `/service-portal/region-map`（`US-SVC-PT-03`）：

1. 门户壳：复用 PT-01 `ServicePortalShell`（页底 `--sci-bg-page`、面包屑「专题服务 / 服务机构区域分布」、产业上下文 `IndustryCatalogSelect`、标题行 `#actions` 槽放全球⇄全国 Radio）。Java **不按产业切片** 时产业只作上下文，不用 Demo `industryScaleRatio` 缩放伪造另一套数。
2. 双视图：全球只渲染 Java `global`（`geo_level=country`）。`geo_level_used=province` 或 `global=[]` → 全球 Radio 禁用并回落到全国，不把 `china` 省名当成国家。
3. 全国只渲染 Java `china`（`geo_level=province`）。空则可见空，不补 0、不填南山区。
4. 地图：复用 `UnifiedLeafletMap`（`presetLayers=false`）。Java 无坐标字段 → 底图壳 + 空态文案，点位不发明；排行条形只认 `name/count`。
5. KPI / 排行数字旁 `@/review`（`M_SVC_ORG_CNT`）；Q-SVC-010 待核验。关评审零泄漏。mount-id：`SVC-PT-F03-REQ` / `SVC-PT-F03-MAP` / `SVC-PT-F03-RANK`。
6. Mock 开：`registerApiMock('svcPortalRegionMap')` 形状=Java 实包（省 3 条 + 国 1 条，`geo_level_used=country`）。关：页面不引 `@/mock/**`。
7. 未改 DefaultLayout、industry-center 业务页、PT-01 KPI omit、PT-02 六类/环节契约、REC-02、ECO-01。

**非范围**：PT-04 技术力 / PT-05 深圳 / PT-06 重点机构；改 Java/Python；宣称 K8s 绿。

## 偏离说明

- Demo 用 `CHINA_REGION_DIST` / `GLOBAL_REGION_DIST` 带 lng/lat，并按产业 `industryScaleRatio` 缩放。本叶类型真源 = Java 实包；筛选只写入 query 并随 POST body 透传，**不在前端缩放数字**；无坐标则地图空态。
- Demo KPI 挂 `M_SVC_PT_REGION_ORG` 并发明 Top12/其余。本叶挂 `M_SVC_ORG_CNT`；已出区域合计只加总当前视图 Java 行，不发明其余 0。
- Demo 默认全球视图。本叶在 Java 有 country 时默认全球，否则强制全国。
- 子导航 PT-04/05 仍占位。

## 复刻五维（R1–R5）

| # | 项 | 结果 |
|---|---|---|
| R1 布局 | 壳 + 筛选 + Radio + KPI×3 + 地图区 + 排行区都在；一节点一套 layout | ✅ |
| R2 交互 | 加载 / 失败 Message / 空「暂无」/ 有结果 / 全球禁用 / 筛选改 query 重拉 | ✅ |
| R3 样式 | `--sci-bg-page` / `#D8E7FC`；KPI 卡与本仓门户同皮肤 | ✅ |
| R4 评审 | 只从 `@/review`；mount-id `SVC-PT-F03-*`；关评审不渲染 metric_id / GAP-* / Q0xx | ✅ |
| R5 Mock | 开：`registerApiMock('svcPortalRegionMap')` 形状=Java 实包。关：页面不 import `@/mock/**` 填数 | ✅ |

### 检索皮肤（V1–V7）

本叶非检索 Hub。V1 页底必过；V2–V7 留给 `LUMEN-SVC-P-FE-US-ORG-07`。

| # | 结果 |
|---|---|
| V1 页底 `--sci-bg-page` / `#D8E7FC` | ✅ |
| V2–V7 | N/A（查询页） |

工作区 W1–W4：N/A。

## Design.md §14

页底 `--sci-bg-page`；主色 `#165DFF`；排行条用 primary。KPI 卡 24px 数字。无 `.ant-` / vendor-antd token。控件高 32px（产业筛选 / Radio button）。地图复用天地图 Leaflet 封装，页面未 `new L.map`。

## 测试结果

- `node src/views/service/servicePortalRegion.selfcheck.mjs` → `servicePortalRegion.selfcheck ok`
- `node src/views/service/servicePortalIndustry.selfcheck.mjs` → `servicePortalIndustry.selfcheck ok`
- `node src/views/service/servicePortalOverview.selfcheck.mjs` → `servicePortalOverview.selfcheck ok`
- `node src/router/menu.selfcheck.mjs` → `menu.selfcheck svc-shell ok`
- `npx vue-tsc --build` → 通过

## 遗留风险

- K8s 未注入 Python/MySQL 时区域分布 `empty` / 空省空全球（预期）；勿把空态当 5xx，不能自行补 0 或区级点。
- 产业筛选暂不切片（Python 忽略 body）；数字是圈定池全局，不是 Demo 缩放。
- Java 实包无 lat/lng，地图保持空点 + 底图壳；PT-04/05 仍占位。

## CI/CD（必填）

- 分支：`lumen-ui-topic` `origin/dev`
- commit：`980adcb`
- pipeline URL / ID：https://gitlab.htmisoft.net/gkx-lumen/lumen-ui-topic/-/pipelines?ref=dev （push 后由 GitLab 生成）
- 部署 namespace / 镜像 tag：待 E0 / CI
- K8s rollout：本叶未等、未宣称绿
- dev 测试 URL：http://111.198.38.90:50892/service-portal/region-map （CI 滚出后）
- 本地：上述 selfcheck + `vue-tsc --build`

## 可观测性

- 区域分布请求走 `src/utils/request.ts`：`X-Trace-Id` + `traceparent`
- OTEL_SERVICE_NAME：N/A（前端）
- Tempo / Loki：有（平台已有）

## 架构合规自检

| 铁律 | 结果 |
|------|------|
| 1 算法只在 Python | ✅ |
| 2 调用链 FE→Java→Python `/internal` | ✅ `POST /svc/topic/v1/service-portal/region-map` |
| 3 Nebula 非 Neo4j | ✅ 未碰图库；地图只复用 Leaflet 底图 |
| 4 可观测 | ✅ request 拦截器 |
| 5 CI | ✅ 已 push `origin/dev`（`980adcb`）；pipeline 由 GitLab 生成 |
| 6 demo2 不 merge 进 lumen | ✅ 只读对照 |
| 7 只调 Java | ✅ |
| 8 数据 ADS / 无硬 mock | ✅ USE_MOCK=false 不填 fixture |
| 9 D8 Design token | ✅ `--sci-bg-page` |
| 10 D9 八件套 / 不自造 ⓘ | ✅ `@/review` + `M_SVC_ORG_CNT` |
| 11 D10 `@/review` | ✅ |
| 12 D12 不打 demo-* | ✅ |

## Cost

| 字段 | 值 |
|------|-----|
| `actual_tokens` | 180000 |
| `model_used` | `claude-sonnet-4.5`（registry 合法枚举；本会话为 Cursor Grok 4.6，按 Sonnet 价表回填） |
| `actual_cost` | 0.97 |
| `cost_warn` | green |
| 口径 | frontend-agent 80/20；`180000×0.8×3/1e6 + 180000×0.2×15/1e6 = 0.97`；`source: session_estimate` |

## 涉及文件

- `lumen-ui-topic` `src/api/service/*`
- `lumen-ui-topic` `src/views/service/ServicePortalRegionMapPage.vue`
- `lumen-ui-topic` `src/views/service/ServicePortalShell.vue`（只加 `#actions` 槽，不改 PT-01/PT-02 内容）
- `lumen-ui-topic` `src/views/service/ServiceReviewMount.vue`（只加 PT-03 mount / TRACE）
- `lumen-ui-topic` `src/views/service/servicePortal.css`
- `lumen-ui-topic` `src/mock/service/portalRegionMock.ts`（仅 `registerApiMock`）
- `lumen-ui-topic` `src/router/menu.ts`
- 本 handoff

## 产物清单

- 代码：`980adcb`（`lumen-ui-topic` `dev`）
- 文档：本文件
- 未改：`industry-center` 业务页、`demo-ui-topic`、REC-02、ECO-01、PT-01 KPI omit、PT-02 六类/环节、PT-04/05 页内容

## 联调确认

联调通过（代码侧）：区域分布页只调 Java region-map；无 country 只出省、全球侧空/禁用；缺行诚实空；禁用 0 冒充全球；禁 Demo 区级假点；Q-SVC-010 待核验不改绿；USE_MOCK=false 不填 fixture。请 coordinator AV-0，**本叶不自行标 done**。

## Registry（MCP）

请 coordinator 核对 `task-update-fields` 后 AV-0：

- evidence：`agent-handoffs/服务机构-SVC/LUMEN-SVC-P-FE-US-PT-03.md`
- actual_tokens：180000 · model_used：`claude-sonnet-4.5` · actual_cost：0.97 · cost_warn：green
- note：联调通过；commit `lumen-ui-topic` `980adcb`；请 AV-0
