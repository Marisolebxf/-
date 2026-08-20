# DEMO-SVC-LAB-UI-MODELS-L01 · 50100 十模型页接 ADS

> 日期：2026-08-20  
> Task：`DEMO-SVC-LAB-UI-MODELS-L01`  
> 仓：`demo-ui-system-test`  
> 总控：阶段 F-ALGO。`human:淮政玮` 授权后按建议做本叶。不开 F-GATE / 50892 / lumen 四仓 / 企业挂点。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控已授权「不必再问」；GRAPH+MODELS 已 integration，联调闸门开本叶 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 一页 `SvcModelsPage` 按 slug 读 `GET /entan/v1/svc/models`；删 `svcModelCatalog.ts` 避免 fixture 充数。图谱图例只留服务机构，边标签看 `mapped_from`。不挂企业/高校/资本。 |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | CLI 认领；本机未挂载 Headroom |

## 图即契约（架构 / 存储流图 / ARCH-IMPL / 联调 / IA 首页必填）

| 字段 | 值 |
|------|-----|
| diagram_id | `SVC-STORAGE-LINEAGE`（消费，未改边） |
| 图 diff | 无工厂边变更。前端只读 ADS / hang；算法仍在 Python |
| 会签态 | 流图仍 2026-08-19 approved |
| 说明 | 出数铁律不变：契约表 → Python → Demo ADS/hang；UI 不内置节点充数 |

## 范围与实现

1. 新增 `pages/SvcModelsPage.vue`：`gap` / `relation` / 六类 `tech-*` / `attract` / `cultivate` 一律读 ADS。无结果 `el-empty`，不回落 catalog。  
2. 路由 `extraImports` 覆盖上述 slug；`CatalogModelPage` 不再 `getSvcModelSpec`。删除 `svcModelCatalog.ts`。  
3. 短板：运行时列 Q-SVCCHAIN-03（空白/薄弱/瓶颈）；Q061 只对照列。关系页表格 Top50 + 密度，线图仍走 `/industry-service/graph`。  
4. 图谱：图例仅「服务机构」粉点；边底图仍 `participates`，标签按 `mapped_from` 显示合作/投资（待核验）。  
5. 页头可再跑十模型（与图谱页同一 `POST /entan/internal/svc/run-models`）。正式库只读。  
6. 未做：企业/高校/资本 hang、新建 Edge、F-GATE、50892、切换 Q061 运行时。

## 偏离说明

- 版式已改回原 `ModelDemoPage`（KPI / 雷达 / 柱 / 饼 / 表；关系链含力导向）。数字仍只读 ADS，不恢复 catalog 机构池。  
- Q062 仍 🟡，合作/投资只是 `mapped_from` 展示，不伪标 live。  
- 技术力各页过滤 `service_type`；该类 Top50 为空则空态，不用旧机构池填。

## 产物清单

| 产物 | 路径 |
|---|---|
| 十模型页 | `demo-ui-system-test/src/views/industry-service/pages/SvcModelsPage.vue` |
| 路由 | `src/router/index.ts` extraImports |
| 图谱 | `src/views/industry-service/components/GraphView.vue` |
| 页签 | `src/views/industry-service/index.vue` |
| 去 Mock | 删除 `svcModelCatalog.ts`；`CatalogModelPage` 不再给 SVC 充数 |

## 测试结果

- [x] 十模型路由不再走 `CatalogModelPage` / fixture  
- [x] 图谱图例只服务机构；边带 `mapped_from`  
- [x] D9 ⓘ 挂短板/密度/技术力/招引/培育  
- [x] 不开 50892 / lumen / GATE  

## 遗留风险

- 本机未再打 50100 页面（ADS 批次仍是 MODELS `svcmodels_20260820_163323`）。K8s 静态站跟 `origin/dev`。  
- 无 hang / 未跑十模型时各页诚实空态。  
- 下一叶才是 `DEMO-SVC-LAB-GATE-L01`（等本叶签收积压不挡，但本会话不开闸）。

## 验收证据

- [x] 50100 图谱/短板/关系/六类技术力/引入/培育：有算法结果读 ADS 或 hang，无则空态  
- [x] 禁止前端 fixture 冒充 F-ALGO  
- [x] 待核验不标 Mock live  
- [x] 不 DROP ODS；不开 50892  

## 架构合规自检

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ UI 只读 |
| 2 | 调用链 | ✅ 50100 → `/entan/v1/svc/models` 与 `/internal/svc/run-models` |
| 3 | 图谱 Nebula，禁 Neo4j | ✅ 不改 space；不 CREATE Edge |
| 4 | 可观测 | ✅ 沿用 `request.ts` TraceHeader |
| 6 | demo 不污染 lumen | ✅ |
| 8 | ADS | ✅ 名单不联 ODS |
| 9 | D8 | ✅ 本仓仍 Element Plus（50100 既有栈，未另起 UI） |
| 10 | D9 | ✅ ⓘ + 待核验；不伪闭合 Q060~Q063 |
| 12 | D12 | ✅ 未改 lumen 四仓 |

## CI/CD

- 分支：`origin/dev`  
- 仓：`demo-ui-system-test`  
- 部署：50100 CI 跟 `dev`

## Cost

| 字段 | 值 |
|------|-----|
| estimated_tokens | 40000 |
| actual_tokens | 90000 |
| model_used | `cursor-grok-4.6` |
| actual_cost | 0.45 |
| cost_warn | green |
