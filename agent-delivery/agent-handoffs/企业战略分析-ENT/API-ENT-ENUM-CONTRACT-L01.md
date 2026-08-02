# API-ENT-ENUM-CONTRACT-L01 · 检索/高筛枚举契约对齐

> 格式对齐 `templates/handoff-template.md` + 公约 §5 DoD；内容按本单实测实写。  
> **给验收人**：先看 **§2 新增**，再看 **§1 纠错**；勿与 `ENT-ES-ETL-L01` 混验。

---

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| task-id | `API-ENT-ENUM-CONTRACT-L01` |
| claimed_by | `agent:data-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| claimed_at | `2026-08-02T12:20:00+08:00` |
| lock_until | `2026-08-02T16:20:00+08:00` |
| in_progress_at | `2026-08-02T12:22:00+08:00` |
| status（registry） | `review` |
| 仓 | `demo-svc-topic-py`（`dev`）+ `gkx-orchestration`（registry/handoff） |
| 性质 | 实现 + 契约文档（`cicd: required`） |
| 派单包 | `agent-handoffs/企业战略分析-ENT/API-ENT-ENUM-CONTRACT-L01-派单包.md` |
| evidence | 本文件（registry `evidence` 已指向） |

---

## 0. 范围与实现（对照 bid / DoD）

| DoD 条目 | 状态 | 证据 |
|----------|------|------|
| §3.1.1 listing / scale / `is_above_scale` 与 meta Q058/Q059 一致 | ✅ | `docs/API-接口文档.md` §3.1.1；`meta.py` 常量 |
| §3.1.2 ops 含 `not_in`/`all`/`exist`；字段对齐 `_FIELD_STRATEGY`；`enterprise_region` 仅 eq/in | ✅ | §3.1.2；catalog 51/51 |
| 新增 `POST /meta/query-tree-schema` | ✅ 已 push `ec1ff14` | `meta.py`；§3.6b |
| `/meta/filters` 返回 stock/supply/core_tech | ✅ 已 push `ec1ff14` | `meta.py`；§3.6 |
| API §25 Java Agent 枚举专章；Feign `region_type`/`node_key` | ✅ | §25；§14.1 |
| pytest meta filters + query-tree-schema；catalog==strategy | ✅ 本地 + CI `py:smoke` | §5；Pipeline 4621 |
| handoff 纠错 vs 新增分表；cost 可回填 | ✅ | §1 / §2 / §9 |
| 明确不做 Java/前端/ETL-L01 | ✅ | §6；下游 L02 |

**上游**：`DATA-ENT-DICT-IMPL-L02`（done）— 已有 filters/regions/company-types/enterprise-scales/tags/region-scopes。

---

## 1. 纠错项（文档/示例 ↔ 代码真值）

| # | 位置 | 错误/旧口径 | 正确口径 | 状态 |
|---|------|-------------|---------|------|
| C1 | §3.1.1 `listing_status` | `已上市`/`拟上市` | `上市`/`未上市`/`退市`（Q059） | ✅ |
| C2 | §3.1.1 `enterprise_scale` | 含「规上」一档 | 四档；规上=`is_above_scale`（Q058） | ✅ |
| C3 | §3.1.1 | 缺 `is_above_scale` | boolean，可与四档叠加 | ✅ |
| C4 | §3.1.2 ops | 缺 `not_in`/`all`/`exist` | 12 ops | ✅ |
| C5 | §3.1.2 字段表 | ~23 字段 | 对齐 `_FIELD_STRATEGY`（51） | ✅ |
| C6 | `enterprise_region` | `containsAny` | 仅 `eq`/`in` | ✅ |
| C7 | Feign `region_type` | 行政区层级误写 | `standard`/`city_cluster` | ✅ |
| C8 | Feign graph expand | `target_key` | `node_key` | ✅ |
| C9 | 全景 `enterprise_scale` | 含规上 | 四档 + `is_above_scale` 说明 | ✅ |
| C10 | `listed_status` | 易与 listing 混淆 | 注明证券详情字段 | ✅ |
| C11 | 三检索接口 `sort_field` | 非法值原样进入 ES | 四项白名单；非法字段回退 `competitiveness_score`，非法方向回退 `desc` | ✅ |
| C12 | 其它枚举入口（region_type / meta mode / category / dimension / base_tag / node_stage） | 文档有枚举但运行时原样透传 | 统一 `enum_guards.py` 白名单归一化；非法值不进 SQL/ES 标识符位 | ✅ |

真源：`meta.py`（`_LISTING_STATUSES` 等）；`enterprise_search.py`（`_FIELD_STRATEGY` / `_QIKE_OP_MAP`）。

---

## 2. 新增项（本单新产物，必须单独验收）

| # | 产物 | 说明 | 状态 |
|---|------|------|------|
| N1 | `POST /internal/gkx-search/meta/query-tree-schema` | `operators` / `fields`(51) / `enums` / `value_source_apis` | ✅ 已 push `ec1ff14` |
| N2 | `/meta/filters` 扩展 | `stock_types` / `supply_chain_roles` / `core_tech_tags` | ✅ 已 push `ec1ff14` |
| N3 | API **§3.6b** | schema 接口说明 | ✅ 已 push |
| N4 | API **§25** | 【Java Agent】枚举契约修复手册（变更记录为 §26） | ✅ 已 push |
| N5 | 文档版本 **v16.4** | 变更记录（含 §25.7 枚举入口铁律） | ✅ |
| N6 | 单测 | `test_meta_filters_enhanced` + `test_meta_query_tree_schema` + enum_guards | ✅ 本地 263 + CI smoke |

### 2.1 新增接口契约摘要

```http
POST /internal/gkx-search/meta/query-tree-schema
Content-Type: application/json
{}
```

| `data` 键 | 含义 |
|-----------|------|
| `operators` | 全部 query_tree 操作符 |
| `fields` | 叶子字段目录（strategy / ops / value_source） |
| `enums` | 固定枚举块 |
| `value_source_apis` | 动态码表应对应的 meta 路径 |

### 2.2 与旧有 meta 的关系

**本单不是从零发明码表体系。** v10/v10.2 已有：`/filters` `/regions` `/company-types` `/enterprise-scales` `/tags` `/region-scopes`。  
本单在其上：**新增**总目录、**扩展**三项固定下拉、**补齐** §25 专章。

---

## 3. 修改内容 / 涉及文件

### `demo-svc-topic-py`（分支 `dev`，已 push `ec1ff14`）

| 文件 | 变更 |
|------|------|
| `gkx_search_service/enum_guards.py` | **新增**：请求契约枚举统一白名单（铁律入口） |
| `gkx_search_service/views/meta.py` | `_QUERY_TREE_FIELD_CATALOG`；`/query-tree-schema`；filters 扩展；`mode`/`category` 白名单 |
| `gkx_search_service/views/enterprise_search.py` | Format B `contains`；排序白名单与默认回退（企业查询/高级筛选/Mock） |
| `gkx_search_service/views/enterprise_compare.py` | 智能搜索复用统一排序白名单 |
| `gkx_search_service/views/enterprise_distribution.py` | `region_type` 白名单 |
| `gkx_search_service/views/key_analysis.py` | `dimension`/`base_tag`/`region_level` 白名单 |
| `gkx_search_service/views/sz_status.py` | `node_stage` 白名单 |
| `gkx_search_service/views/enterprise_key_enterprise.py` | `node_stage`/`region_level` 白名单 |
| `gkx_search_service/main.py` | endpoints 列表增加 schema 路径 |
| `docs/API-接口文档.md` | v16.4：§25.7 枚举入口铁律；变更记录 |
| `tests/test_enterprise_search.py` | meta/schema、Format B、排序白名单回归 |
| `tests/test_enum_guards.py` | 枚举守卫单元测试 |

### `gkx-orchestration`

| 文件 | 变更 |
|------|------|
| `agent-delivery/task-registry.yaml` | 登记 `API-ENT-ENUM-CONTRACT-L01` |
| `agent-handoffs/.../API-ENT-ENUM-CONTRACT-L01-派单包.md` | 派单包 |
| `agent-handoffs/.../API-ENT-ENUM-CONTRACT-L01.md` | 本 handoff |

---

## 4. 问题清单（开工前）

1. 文档枚举与代码不一致 → Java/AI 无法安全对接  
2. 无「只读本章」的 Java Agent 枚举入口 → 被迫扫全仓  
3. 高筛缺字段总目录；缺 stock/supply/core_tech 固定下拉  

---

## 5. 测试结果

```text
环境：本地 Mock（GKX_MOCK_ENABLED=1），.venv pytest
catalog keys == _FIELD_STRATEGY → 51/51

pytest:
  tests/test_enterprise_search.py::test_meta_filters
  tests/test_enterprise_search.py::test_meta_filters_enhanced
  tests/test_enterprise_search.py::test_meta_query_tree_schema
  tests/test_enterprise_search.py::test_meta_company_types
  tests/test_enterprise_search.py::test_meta_enterprise_scales
  tests/test_enterprise_search.py::test_meta_tags
  tests/test_enterprise_search.py::test_meta_regions
→ 7 passed（2026-08-02）

排序白名单专项：
  test_search_sort_whitelist_falls_back_before_es
  test_search_sort_whitelist_applies_to_all_three_endpoints
  test_smart_search_sort_params
  + catalog strategy / Format B contains 回归
→ 5 passed（2026-08-02）

完整回归：
  GKX_MOCK_ENABLED=1 pytest tests/test_enum_guards.py tests/test_enterprise_search.py tests/test_key_analysis_sz_status.py -q
→ 263 passed，1 warning（pandas/bottleneck 版本提示，与本单无关）

冒烟：
  POST /meta/filters → 含 stock_types / supply_chain_roles / core_tech_tags
  POST /meta/query-tree-schema → fields=51
  POST /enterprises/advanced（正确枚举）→ HTTP 200 code=0
```

---

## 6. 偏离说明 / 遗留风险

| 项 | 说明 |
|----|------|
| 未 commit / push | ✅ Python `ec1ff14` / 编排已 push；Pipeline 4621 smoke/image 绿；deploy ⏳ |
| 未改 Java 生产代码 | **刻意留给下游** `ENT-JAVA-ENUM-CONTRACT-L02`；契约真源见 API §25；派单包见同目录 `ENT-JAVA-ENUM-CONTRACT-L02-派单包.md` |
| `core_tech_tags` | Wave0 固定六项（对齐 Mock）；正式 DIM 可再跟进 |
| `_FIELD_STRATEGY` 与 catalog 双份 | 已加 pytest 断言 field+strategy 一致；彻底单源化留 follow-up |
| `listed_status` vs `listing_status` | 详情证券字段 vs 筛选字段，文档已区分；存量数据可能仍含「已上市」兼容值 |
| `sort_field` 服务端白名单 | 已实现统一归一化；非法字段/方向不进入 ES，并记录 warning |
| 枚举入口铁律 | 凡文档声明的枚举/标识符入参，**禁止**原样透传 ES field/sort/agg 或 SQL 枚举谓词；统一走 `enum_guards`（或局部同等白名单）。已有护栏：aggregations `field`、distribution `dimension`、type-scale `region_level`、三检索 sort、以及 C12 补齐项 |

### 6.1 Review 排查修复（2026-08-02，对照 review-agent）

| 优先级 | 问题 | 处理 |
|--------|------|------|
| P1 | `industry_class` 误绑 `filters.industries`（中文名） | catalog + §3.1.2 改为 `free_text`；`industry_class_name` 仍绑 industries |
| P1 | Format B 不认 `contains`，条件静默丢失 | `_QIKE_OP_MAP` 增加 `contains`；单测 Format A/B 等价 |
| P2 | catalog 与 `_FIELD_STRATEGY` 双份漂移 | 新增 `test_meta_query_tree_schema_matches_field_strategy` |
| P3 | §26 写在 §25 变更记录前、编号颠倒 | 专章改为 **§25**，变更记录 **§26** |

---

## 7. CI/CD（必填）

| 项 | 值 |
|----|-----|
| 分支 | `demo-svc-topic-py`：`dev` |
| commit | `ec1ff14`（已 push `origin/dev`） |
| pipeline URL / ID | [#4621](https://gitlab.htmisoft.net/gkx-lumen/demo-svc-topic-py/-/pipelines/4621)（`py:smoke`/`py:image:*` 绿；`deploy:search-py` 待手动） |
| 部署 namespace / 镜像 tag | ⏳ 点跑 `deploy:search-py` 后回填；或登记 deploy waiver |
| K8s rollout | ⏳ 同上 |
| dev 测试 URL / 命令 | 本地：§5；外网 search：`http://111.198.38.90:50105`（部署后验 `/meta/query-tree-schema`） |
| 架构验收 | `API-ENT-ENUM-CONTRACT-L01-ARCH-ACCEPT.md`（**条件通过**，2026-08-02） |

> **现状**：代码与编排已 push；CI 测试/镜像绿；deploy 待手动。架构条件通过，关 `done` 见 ARCH-ACCEPT 关单条件。编排最新：`233775e`+本 commit。

---

## 8. 可观测性（建议）

| 项 | 值 |
|----|-----|
| OTEL_SERVICE_NAME | `gkx-search-service`（既有；本单未改 instrument） |
| traceId（dev 抽样） | N/A（未改入口中间件） |
| Tempo / Loki | 无新增要求 |

---

## 9. 架构合规自检（公约 §2）

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ meta 只读；无 Java 算法 |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ 仅扩展 Python `/internal/gkx-search/meta/*`；未改 FE/Java 实现 |
| 3 | 图谱 NebulaGraph，禁 Neo4j | ✅ 不涉及 |
| 4 | 可观测性 | ✅ 既有服务；本单未改中间件 |
| 5 | CI/CD push→Pipeline→K8s | ✅ push+smoke/image 绿；⏳ deploy manual（见 ARCH-ACCEPT） |
| 6 | demo 不 merge lumen | ✅ 改 `demo-svc-topic-py` |
| 7 | 共享聚合 / Java 不写算法、不直连 nGQL | ✅ |
| 8 | 数据策略 ADS/码表 | ✅ 固定枚举+既有 DIM/DWD meta；无 ODS 乱接 |
| 9 | Design.md 前端规范 | ✅ 本单无前端 |
| 10 | 数据血缘 D9 | ✅ 无新统计指标；契约/枚举 |
| 11 | 交互规范 D10 | ✅ 本单无 UI |

---

## 10. Cost 四字段（回填 registry）

| 字段 | 值 |
|------|-----|
| `actual_tokens` | ~150_000 |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~2.5（估 USD） |
| `cost_warn` | green（&lt; $10） |

> 已写入 `task-registry.yaml`。

---

## 11. 下游 Java 交接（给 api-agent / 派单用）

> **本单（L01）只交付 Python 契约真源。Java 必须另开单，禁止把 Java 改码塞进本 handoff 验收。**

| 项 | 值 |
|----|-----|
| 建议 task-id | `ENT-JAVA-ENUM-CONTRACT-L02` |
| 执行 Agent | `agent:api-agent` |
| 建议监管 | `human:徐滕强` |
| 认领人 | `human:侯佳伟`（Java 实现认领） |
| 仓 | `lumen-svc-platform`（`origin/dev`） |
| 依赖 | `API-ENT-ENUM-CONTRACT-L01` = `done`（至少 Python 已 push + 文档 v16.4 §25 可读） |
| 契约真源 | `repos/demo-svc-topic-py/docs/API-接口文档.md` **§25 + §3.1.0 + §3.1.2 + §3.6b**（不要扫 Python） |
| 上游 handoff | 本文件 |
| 派单包 | `agent-handoffs/企业战略分析-ENT/ENT-JAVA-ENUM-CONTRACT-L02-派单包.md` |

### 11.1 Java 必须做（摘要）

1. **请求契约 enum** 按 §25.2 落地（至少：`SearchSortField`/`SearchSortOrder`/`ListingStatus`/`EnterpriseScale`/`OperatingStatus`/`QueryTreeOp`/`DistributionRegionType`/`NodeStage`/`KeyAnalysisBaseTag` 等）
2. **Feign 纠错**：`node_key`（非 `target_key`）；`region_type` 仅 `standard`/`city_cluster`；listing/scale 对齐 Q058/Q059；`is_above_scale`；query_tree 支持 `not_in`/`all`/`exist`
3. **新透传**：`POST /topic/.../meta/query-tree-schema` → Python `/internal/gkx-search/meta/query-tree-schema`
4. **扩展透传**：`/meta/filters` 响应含 `stock_types` / `supply_chain_roles` / `core_tech_tags`（typed DTO，勿丢字段）
5. **禁止**：在 Java 硬编码地区/标签等动态码表；禁止写算法；非法枚举在 Java 侧也应拒绝或落到文档默认（与 Python 白名单一致）

### 11.2 其它 follow-up

| 建议 ID | 内容 | Agent |
|---------|------|-------|
| `FE-ENT-ADV-FILTER-WIRE`（建议） | 高筛面板改调 schema + filters 新字段 | frontend-agent |
| （可选）`DATA-ENT-CORE-TECH-DIM` | `core_tech_tags` 从固定六项迁 DIM | data-agent |
| （可选）共享模块 | `_FIELD_STRATEGY` 与 catalog 单源 | data-agent |
| — | **不要**把本单并入 `ENT-ES-ETL-L01` | — |

---

## 12. 监管人下一步

1. 审阅本 handoff §2 新增项（尤其 N1）是否接受  
2. ~~授权 commit/push~~ → **已完成**：Python `ec1ff14` / 编排已 push  
3. ~~架构验收~~ → **条件通过**（`API-ENT-ENUM-CONTRACT-L01-ARCH-ACCEPT.md`）  
4. 点跑 `deploy:search-py`（Pipeline 4621）或书面 deploy waiver → coordinator 转 L01 `done`  
5. 侯佳伟按 `ENT-JAVA-ENUM-CONTRACT-L02-派单包.md` 开工（契约真源 API §25 v16.4；L01 `done` 前勿关 L02）  
