# LUMEN-CHAIN-JAVA-BIZ-UX-L01 · 产业链 Java — 对比篮/查询辅助/区域模板/分析维度权重补齐

> 格式参考 `templates/handoff-template.md`；内容按本单 as-built。  
> **不做**：前端 `lumen-ui-topic` 接线（collaborator 另单）、Job/async-service、造 Q016 对标城、改 `ent_*` 加 `biz_type`、**禁止 DROP 库/表**。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `pull` |
| 说明 | 2026-09-07 侯佳伟确认「认领并开工」；registry `in_progress`；lock 至 20:35 +08:00。本单完工转 **integration**，不标 done。 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单 `/goal` 一致。未用 YAGNI 跳过调用链（前端→Java REST→Python `/internal`）、D9（区域指标只挂 `metric_id` 占位，不手写就绪度改绿）、handoff。对比篮学服务机构：新 `chain_*` 表，不给 `ent_*` 加列。 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | MCP `task-registry` 本机未挂载，走 `scripts/lib/task-registry-lib.mjs`；任务与 ENT 对齐单 / FE localStorage 路径均精读。 |

## 范围与实现

写库落在 **`gkxlumenx_topic_enterprise`**（与企业篮同库、账号与 demo 相同：`192.168.88.43:3306` / `root` / `htrfadmin`）。topic-chain 本身连的是只读 `demo_gkxlumenx_ads`，故用户态写操作在 **topic-enterprise**，chain 门面 Feign 过去。路径优先 `/chain/topic/v1/industry/**`。

**DDL 安全**：只提交增量脚本 `db/9x_gkxlumenx_topic_enterprise_chain_ux_l01.sql`（`CREATE TABLE IF NOT EXISTS` + 幂等 INSERT）。**未改** `db/9x_gkxlumenx_topic_enterprise.sql`（该文件含 `DROP TABLE IF EXISTS`，**禁止再跑**）。本机 TCP 探 `192.168.88.43:3306` 超时，**未对线上执行任何 SQL**。内网执行时只跑增量文件。

### 新增表（同库，不 DROP）

| 表 | 用途 |
|---|---|
| `chain_compare_basket_item` | 对比篮；UK=`user_id+object_type+object_id`；类型仅 `industry` / `industry_chain` |
| `chain_search_example` | 示例词；`kind`=`smart` / `industry` |
| `chain_search_scene` | 热门场景（重点产业 / 未来产业） |
| `chain_search_history` | 最近检索；用户 + `search_type` 隔离 |
| `chain_filter_template` | 产业高筛「我的方案」；不与 `ent_filter_template` 混表 |
| `chain_regional_metric` | 区域指数可添加指标总表（index / competitiveness） |
| `chain_regional_template` | 官方/个人模板；官方 seed=`TPL-CHAIN-REGIONAL-OFFICIAL` |

### 对外路径（网关 `{GW}=http://192.168.88.50:30899`）

| 能力 | 方法 | 网关路径 | 服务内 | 写库 |
|---|---|---|---|---|
| 对比篮 | GET | `{GW}/chain/topic/v1/industry/compare-basket?user_id=` | topic-chain `/topic/v1/industry/compare-basket` | Feign → enterprise `/topic/v1/chain-ux/**` |
| 加入 | POST | `.../compare-basket/items` | 同左剥 `chain` | 同上 |
| 移除一项 | DELETE | `.../compare-basket/items/{object_type}/{object_id}` | 同上 | 同上 |
| 批量/清空 | DELETE | `.../compare-basket/items/batch` | 同上 | 同上 |
| 示例 | POST | `.../search-biz/examples/list` | 同上 | 同上 |
| 场景 | POST | `.../search-biz/scenes/list` | 同上 | 同上 |
| 最近检索 | POST | `.../search-biz/history/{list,save,clear}` | 同上 | 同上 |
| 高筛方案 | POST | `.../filter-template/{list,save,delete}` | 同上 | 同上 |
| 区域指标 | GET | `.../regional/metrics?eval_mode=index` | 同上 | 同上 |
| 官方模板 | GET | `.../regional/templates/official` | 同上 | 同上 |
| 我的模板 | POST | `.../regional/templates/mine/{list,save,delete}` | 同上 | 同上 |
| 分析维度 | GET | `{GW}/chain/topic/v1/industry/analysis-dims` | `IndustryFacadeController` 切 Python `meta()` | 不写库 |

`object_ids` / `object_type`，禁止 `enterprise_code`。`object_type=enterprise` 服务端拒绝。

分析维度：切片既有 `GET .../industry/meta` 的 `diagnosis` / `regional` / `shenzhen` / `year_windows` / `evaluation_cities`。`benchmark.items=[]`，`pending_ref=Q016`，**不发明对标城**。兼容继续用 `GET .../meta`。

接口总文档（格式对齐 `API-ENT-full-catalog.md` / GAP catalog）：  
`agent-delivery/agent-handoffs/产业链分析-CHAIN/API-CHAIN-BIZ-UX-CATALOG.md`（#U1–U18）。

### OpenAPI 示例

**加入对比篮** `POST /chain/topic/v1/industry/compare-basket/items`

```json
{
  "user_id": "u1",
  "object_type": "industry",
  "object_ids": ["INB1"],
  "object_names": ["人工智能"],
  "source": "search"
}
```

成功：`{"code":0,"data":{"added":1,"duplicated":0,"basket_count":1}}`

**查询示例** `POST .../search-biz/examples/list`

```json
{ "kind": "smart" }
```

**保存高筛方案** `POST .../filter-template/save`

```json
{
  "user_id": "u1",
  "template_name": "重点产业",
  "query_tree": { "logic": "AND", "conditions": [{ "field": "industry_attribute", "op": "in", "value": ["key"] }] }
}
```

**分析维度** `GET .../industry/analysis-dims` 关键字段：

```json
{
  "diagnosis": {},
  "regional": {},
  "shenzhen": {},
  "year_windows": [],
  "evaluation_cities": [],
  "benchmark": { "pending_ref": "Q016", "items": [] }
}
```

（`diagnosis`/`regional`/`shenzhen` 具体结构原样来自 Python `meta`，本叶不改算法。）

## 偏离说明（as-built）

| 项 | 派单 | As-built | 理由 |
|---|---|---|---|
| 高筛隔离 | `biz_type=industry` 落库 | **独立 `chain_filter_template`**，不给 `ent_*` 加 `biz_type` | 学服务机构篮；避免企业方案串数据；侯佳伟确认新表同库 |
| 写库位置 | 未强制 | topic-enterprise 写；topic-chain Feign | chain 数据源是只读 Demo ADS，不能写用户态 |
| 线上 DDL | 应落库 | 增量脚本已写；**本机未执行** | `192.168.88.43:3306` 本机超时；须内网只跑增量文件 |
| 对标城 | 诚实空 | `benchmark.items=[]` + `pending_ref=Q016` | 禁止发明清单 |

## 产物清单

| 产物 | 路径（相对 `lumen-svc-platform/`） |
|---|---|
| 增量 DDL（无 DROP） | `db/9x_gkxlumenx_topic_enterprise_chain_ux_l01.sql` |
| 门面 | `gkxlumen-topic-chain-biz/.../IndustryChainUxController.java` |
| Feign | `.../feign/RemoteChainUxClient.java` → `TOPIC_ENTERPRISE_SERVICE` |
| 分析维度 | `IndustryFacadeController#analysisDims` + `IndustryFacadeServiceImpl#analysisDims` |
| 内部写库 | `gkxlumen-topic-enterprise-biz/.../ChainUxInternalController.java` |
| DTO | `...-api/.../dto/chainux/ChainUxDTOs.java` |
| Entity/Mapper/Service | `chain_*` 七表对应 |
| 单测 | `IndustryChainUxControllerTest` / `IndustryFacadeAnalysisDimsTest` / `ChainCompareBasketServiceImplTest` |
| 本 handoff | `agent-delivery/agent-handoffs/产业链分析-CHAIN/LUMEN-CHAIN-JAVA-BIZ-UX-L01.md` |
| 接口总文档 | `agent-delivery/agent-handoffs/产业链分析-CHAIN/API-CHAIN-BIZ-UX-CATALOG.md` |

未改：`lumen-ui-topic`、`lumen-algo-py`、`db/9x_gkxlumenx_topic_enterprise.sql`（含 DROP，禁止再跑）。

## 验收证据

| 项 | 结果 |
|---|---|
| 对比篮 industry/industry_chain | ✅ 加入/移除/批量清空；拒绝 `enterprise`；上限 50 |
| 查询辅助 | ✅ 示例/场景/最近检索按 `kind`/`search_type` + `user_id` 隔离 |
| 高筛方案 | ✅ 独立 `chain_filter_template`，不读 `ent_filter_template` |
| 区域指数 | ✅ metrics（key/label/group/official/metric_id）+ 官方模板 + 我的模板 |
| 分析维度 | ✅ meta 切片；Q016 `items=[]` |
| 路径 | ✅ 网关 `/chain/topic/v1/industry/**`；Java 不写算法、不直连 nGQL |
| Maven 测试 | ✅ chain MockMvc：`IndustryChainUxControllerTest` + facade/analysis-dims **4 passed**；enterprise `ChainCompareBasketServiceImplTest` **3 passed**（`-am` + `-Dmaven.build.cache.enabled=false`） |
| DDL 安全 | ✅ 增量脚本无 `DROP DATABASE` / `DROP TABLE`；未执行旧 9x |
| 线上落表 | ⏳ 待内网执行增量 SQL |

## 架构合规自检（十条）

| # | 铁律 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 分析维度只切 Python `meta`；用户态无算法 |
| 2 | 前端 → Java REST → Python `/internal/*` | ✅ 写库走 Java；meta/dims 仍 Feign Python |
| 3 | 图谱 NebulaGraph；禁止 Neo4j | ✅ 未引入 |
| 4 | 可观测：Java Agent | ✅ 沿用 topic-chain / topic-enterprise Agent |
| 5 | CI/CD push → Pipeline | ⏳ 代码未 commit/push（等人点头） |
| 6 | demo2 不 merge lumen | ✅ 仅 lumen-svc-platform + 编排 handoff |
| 7 | Java 不写算法、不直连 nGQL、只读 ADS | ✅ 用户态写 `gkxlumenx_topic_enterprise`；ADS 仍只读 |
| 8 | 数据策略 | ✅ 示例/场景/官方模板幂等 seed；不 DROP 既有企业表 |
| 9 | D8 Design | N/A 无前端 |
| 10 | D9 血缘 | ✅ 区域指标带 `metric_id`；不改绿就绪度；Q016 诚实空 |

## CI/CD

- 分支：`lumen-svc-platform` `dev`（禁止 main、禁止 force）
- commit：尚未提交（等人确认后再 `[agent:api-agent]`）
- pipeline / K8s rollout：push 后走既有 `deploy:topic-chain` + `deploy:topic-enterprise`
- 部署后需 **重启 topic-enterprise**（新表 Mapper）+ **topic-chain**（新 Feign）
- 网关前缀已有 `Path=/chain/**`，本叶不改网关

## 可观测性

- `OTEL_SERVICE_NAME`：`gkxlumen-topic-chain-biz` / `gkxlumen-topic-enterprise-biz`
- Tempo / Loki：沿用平台 Collector

## 遗留风险 / 开放项

1. **增量 SQL 未上库**：请在能访问 `192.168.88.43` 的机器只执行  
   `lumen-svc-platform/db/9x_gkxlumenx_topic_enterprise_chain_ux_l01.sql`  
   **不要**执行 `db/9x_gkxlumenx_topic_enterprise.sql`（会 DROP 既有 `ent_*` 表）。
2. **前端接线另单**：`useFilterTemplates('industry')` 现仍打企业 `/filter-template`；`gkx-industry-search-recents:v1` 与区域模板仍 localStorage。collaborator=`frontend-agent`。
3. **Q016** 对标城继续空清单，等甲方书面确认。
4. 本 agent **不**把任务标 `done`。handoff + evidence 齐后由 coordinator AV-0 → `integration`。

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | 380000 |
| model_used | cursor-grok-4.6 |
| actual_cost | 2.05 |
| cost_warn | green |

口径：api-agent 默认 in/out=**80/20**，按 budget-estimate Sonnet 4.5 价表（$3 / $15 per 1M）折算（Grok 无独立价行）。`source: session_estimate`。公式：`380000×0.8×3/1e6 + 380000×0.2×15/1e6 = 2.052 ≈ 2.05`。单任务 <$5。

## 联调确认

**联调确认**：Java 契约层 MockMvc + basket 单测绿；对比篮拒绝 enterprise；分析维度 Q016 空 items。线上表与网关端到端 **待** 内网跑增量 SQL + 部署 topic-enterprise/topic-chain 后补 curl。本 agent **不**标 `done`（feature → 等人 commit/push 后 coordinator AV-0 → `integration`）。
