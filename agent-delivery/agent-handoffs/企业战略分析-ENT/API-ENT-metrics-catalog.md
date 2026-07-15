# API handoff：API-ENT-metrics-catalog

- 时间：2026-06-18
- 角色：api-agent（Java 业务 API 层 / 只读 ADS / SQL 级统计）
- 仓库：`gkx_lumen_backend`
- 分支：`feature/ent-metrics-catalog`（基于本地 `main`）
- commit：`28a19149dd94c6cf29173b55fdb2b1611854dfa6`（**未 push**，走 PR 流程；lumen 禁直推 main/dev）
- 输入真源：`agent-delivery/metrics/cfg_metric-ENT-seed.yaml`（49 条 8 件套）
- 命名前提：Q009 方案 B（企业域一律 `M_ENT_*`，policy §3.2 v1.1.0）

---

## 1. 现状探明结论

| 探查项 | 结论 |
|--------|------|
| `gkx_lumen_backend` 是否有 `gkxlumen-metrics` 模块 | ❌ **不存在** |
| `gkx_lumen_backend` 是否有 `gkxlumen-topic` 模块 | ❌ **不存在** |
| lumen 现有模块 | register / gateway / auth / upms / common / flow / visual / app-server（Pigx 5.12.0，Spring Boot 3.5.11，包根 `com.topcomm.gkxlumen.*`，响应包装 `com.topcomm.gkxlumen.common.core.util.R`） |
| `gkx_service_demo` 是否有可参考 metrics/聚合实现 | ✅ **有** `gkx-innov`：`CityController`/`EventController` 等 6 controller + `InnovDao`（只读 `JdbcTemplate` + snake→camel + `R` 包装）。这是「只读 ADS、SQL 级统计、不写算法」的成熟范式 |
| `gkx_lumen_backend` 的 `gkx_lumen_backend` CI | repo-registry 标 `ci:false`（待 L02b 移植）；本次设计类无需触发 CI |

**决策**：模块不存在 → 按任务「产出 API 契约设计 + 最小骨架（不强造完整模块）」。复刻 `gkx-innov` 范式，新建 `gkxlumen-metrics` 骨架目录，**未注册进父 `pom.xml` 的 `<modules>`**（对现有 reactor 构建/CI 零影响），**不引入新依赖**，激活由人工 PR 完成。

---

## 2. catalog 契约要点（`/metrics/v1/catalog`，对齐 data-lineage-policy §2/§7.4）

- 端点：`GET /metrics/v1/catalog`
- 过滤：`?ids=`（逗号分隔精确匹配）、`?element=ENT`、`?idPrefix=M_ENT_`（支持 `M_ENT_*` 语义）、`?mappingStatus=✅`；可组合取交集。
- 数据源（Wave 0）：`cfg_metric-ENT-seed.yaml` 快照（骨架 bundle 为 classpath JSON）；**待接 DB** → 正式期读 `gkx_cfg.cfg_metric`。
- 响应：`R<{ total, element, seedVersion, batch, list[] }>`，`list[]` 每条含 **8 件套**（`metricId / metricNameZh / definition / formula / sourceTables / sourceSystems / updateFreq / version`）+ 推荐字段（`mappingStatus / isMock / bidRef / acceptanceUnitId / ownerAgent`）+ `aggEndpoint`（仅 14 条 ✅ 填充）。
- 血缘扩展：`GET /metrics/v1/lineage/{metricId}` 返回 8 件套 + `lineage{nodes,edges}`（Wave 0 由 `sourceTables` 文本解析 ADS↔ODS 两层）。
- 字段命名约定：`metric_id` **取值**保持 SCREAMING_SNAKE；JSON **字段**统一 camelCase（复刻 InnovDao 归一化）。
- 降级：catalog 失败时前端「数据说明加载中」，不阻塞主界面（policy §5.1）；Wave 0 全 `isMock=true` → UI 渲染 🧪 MockBadge。

---

## 3. 14 条 ✅ 直接聚合端点清单 + SQL 草稿（只读 ADS，SQL 级统计，非算法）

> 物理 ADS 表名以 `数据库设计.md`（data-agent）为准；下表 `ent_*` 为建议名，源自种子 `source_tables`。Wave 0 全部 Mock 返回。

| # | metric_id | 中文名 | 端点 | 聚合 SQL 草稿 |
|---|-----------|--------|------|---------------|
| 1 | M_ENT_TOTAL_COUNT | 企业总数 | `GET /metrics/v1/ent/total-count` | `SELECT COUNT(DISTINCT enterprise_id) FROM ent_enterprise` |
| 2 | M_ENT_NEW_COUNT_Y | 历年新增企业数 | `GET /metrics/v1/ent/new-count-by-year` | `SELECT YEAR(registration_date) y, COUNT(DISTINCT enterprise_id) v ... GROUP BY y` |
| 3 | M_ENT_AVG_RD_INVESTMENT | 平均研发投入 | `GET /metrics/v1/ent/avg-rd-investment` | `SELECT AVG(rd_investment) FROM ent_enterprise WHERE rd_investment IS NOT NULL` |
| 4 | M_ENT_PATENT_TOTAL | 专利总量 | `GET /metrics/v1/ent/patent-total` | `SELECT SUM(patent_grant_count) FROM ent_enterprise` |
| 5 | M_ENT_TYPE_MATCH_COUNT | 匹配企业总数 | `GET /metrics/v1/ent/type-match-count` | `COUNT(DISTINCT e.enterprise_id) ... WHERE i.industry_chain IN(:industry) AND e.ent_type IN(:type)` |
| 6 | M_ENT_TYPE_RATIO | 类型占比 | `GET /metrics/v1/ent/type-ratio` | `占比 = 各类型计数/总计 OVER()`（⚠️ 分子 ent_type 口径依赖 **Q010**） |
| 7 | M_ENT_DOMAIN_COVERAGE_COUNT | 覆盖领域数 | `GET /metrics/v1/ent/domain-coverage-count` | `SELECT COUNT(DISTINCT industry_chain) FROM ent_enterprise_industry` |
| 8 | M_ENT_PATENT_GRANT_COUNT | 专利授权数 | `GET /metrics/v1/ent/{enterpriseId}/patent-grant-count` | `SELECT patent_grant_count FROM ent_enterprise WHERE enterprise_id=:eid` |
| 9 | M_ENT_REVENUE_LATEST | 营收 | `GET /metrics/v1/ent/{enterpriseId}/revenue-latest` | `SELECT revenue_latest FROM ent_enterprise WHERE enterprise_id=:eid` |
| 10 | M_ENT_SZ_COUNT | 深圳企业数 | `GET /metrics/v1/ent/sz-count` | `COUNT(DISTINCT enterprise_id) WHERE headquarters_city='深圳' [AND chain]` |
| 11 | M_ENT_SZ_CHAIN_POSITION | 链中角色 | `GET /metrics/v1/ent/{enterpriseId}/chain-position` | `SELECT industry_chain, industry_chain_role FROM ent_enterprise_industry WHERE enterprise_id=:eid` |
| 12 | M_ENT_KEY_NODE_COUNT | 重点环节企业数 | `GET /metrics/v1/ent/key-node-count` | `COUNT(DISTINCT enterprise_id) GROUP BY industry_chain_node` |
| 13 | M_ENT_RECOMMEND_COUNT | 推荐企业数 | `GET /metrics/v1/ent/recommend-count` | `COUNT(DISTINCT enterprise_id) FROM ent_recommend_score WHERE scene=:scene AND score>=:threshold`（⚠️ score 依赖评分类 ADS + 阈值 **Q015**） |
| 14 | M_ENT_SUPPLIER_COUNT | 供应商数量 | `GET /metrics/v1/ent/{enterpriseId}/supplier-count` | `COUNT(DISTINCT related_enterprise_id) WHERE relation_type='上游'` |

- 标量响应：`R<{ metricId, value, unit, isMock }>`；序列/分组响应：`R<{ metricId, isMock, series/rows[] }>`，均带 `metricId` 供前端联动 catalog 取 ⓘ 数据说明卡。
- **依赖提醒**：#6（TYPE_RATIO 分子待 Q010）、#13（RECOMMEND_COUNT 依赖评分 ADS + Q015）聚合算子本身是 SQL，但需口径/上游就绪后才能「真聚合」；其余 12 条纯直接聚合，ADS 表就绪即可上线。

---

## 4. 评分类 / 算法依赖类 —— 待接清单（本任务不实现，铁律1）

> 标 `pending_algorithm`（🔧）/ `pending_data_lead`（⚠️）/ `no_source`（❌），共 35 条（49−14）。
> 必须由 `ent-analysis-demo`（Python，NebulaGraph 真源）等算法仓产出并**写入 ADS 标准表**后，api-agent 再以「只读 ADS」方式扩端点接入。

| 类别 | 代表 metric_id | 建议待接 ADS | 上游 |
|------|----------------|--------------|------|
| 技术/商业/竞争力评分 + 排名 | TECH_POWER_SCORE / BUSINESS_POWER_SCORE / COMPETITIVENESS_SCORE / *_RANK / TECH_RANK | `ent_score` | ent-analysis-demo |
| 区域/集聚/密度指数 | REGIONAL_DENSITY / AGGLOMERATION_INDEX / CITY_DENSITY / CITY_AVG_TECH_POWER | `ent_region_index` | ent-analysis-demo |
| 领域分布派生 | DOMAIN_COVERAGE_BREADTH / _DEPTH / DIVERSIFICATION_INDEX | `ent_domain_index` | ent-analysis-demo |
| 财务派生比率 | RD_INVESTMENT_RATIO / REVENUE_GROWTH_RATE / PROFIT_MARGIN | `ent_finance_ratio` | ent-analysis-demo |
| 招引/培育推荐 | ATTRACTION_INDEX / CULTIVATION_INDEX / GROWTH_POTENTIAL / INDUSTRY_MATCH_SCORE / POLICY_MATCH_SCORE | `ent_recommend_score`（供 #13 复用） | ent-analysis-demo |
| 供应链网络 | NODE_CENTRALITY / RELATION_STRENGTH / SUPPLY_CHAIN_RISK / CORE_SUPPLIER_COUNT | `ent_supply_graph_metric`（Nebula 中心性落表，**禁直连 nGQL**） | ent-analysis-demo |
| 痛难点诊断 | PAINPOINT_COUNT / _SEVERITY / _GAP | `ent_painpoint` | ent-analysis-demo |
| 口径待甲方计数 | INNOVATIVE_COUNT(Q011) / HIGH_TECH_COUNT(Q010) / TYPE_COUNT(Q010) / REGIONAL_COUNT(Q012) / CHAIN_COMPLETENESS | 口径定后转直接聚合 | PM 推动甲方 |
| 链/环节派生 | CHAIN_COMPLETENESS | `ent_chain_index` | ent-analysis-demo |
| 无来源 | MARKET_SHARE | ❌ 需采购市场调研数据 | 采购 |

---

## 5. 与 data / algorithm 的接力关系

```
data-agent（cfg_metric 落 DB + ADS 建表/字段血缘）
   → algorithm-agent（🔧 formula 实现，结果写 ADS 标准表；图谱中心性 Nebula→ADS 落表）
      → api-agent（只读 ADS 接入：catalog 改读 cfg_metric DB；§4 端点 Mock→真 SQL；扩 §5 评分类端点）
         → ui-agent（MetricSpecCard 从 /metrics/v1/catalog 动态读 8 件套，🧪 MockBadge / ⓘ 数据说明卡）
            → qa-agent（4 段抽样链路核验）
```
- **本任务交付边界**：契约 + 14 条 ✅ 的 Mock 端点 + catalog Mock 源。**不**实现算法、不接真实 ADS、不动父 pom、不接 DB。
- **api-agent 下一步（待上游就绪）**：① catalog 源切 `cfg_metric` DB；② 14 端点 Mock→真 ADS SQL；③ 按 §4 评分类 ADS 落表后扩端点。

---

## 6. 产物清单

- 分支：`feature/ent-metrics-catalog` @ `gkx_lumen_backend`，commit `28a1914`（未 push）
- 新增（11 文件，均在 `gkxlumen-metrics/`）：
  - `docs/ENT-metrics-catalog-contract.md`（**权威契约**：catalog + 14 端点 + SQL + 待接清单 + 合规自检）
  - `docs/openapi-metrics-v1.yaml`（OpenAPI 3 契约先行）
  - `pom.xml`（复刻 gkx-innov 依赖，**未入父 reactor**）
  - `src/main/java/.../GkxlumenMetricsApplication.java`
  - `src/main/java/.../support/MetricsDao.java`（只读 JdbcTemplate，snake→camel）
  - `src/main/java/.../support/MetricCatalogSource.java`（Mock 源加载 + 过滤）
  - `src/main/java/.../controller/MetricCatalogController.java`（catalog + lineage）
  - `src/main/java/.../controller/EntMetricAggController.java`（14 端点）
  - `src/main/resources/metrics/cfg_metric_ENT.mock.json`（14 ✅ 全量 + 5 代表性，共 19 条；JSON 校验通过）
  - `src/main/resources/bootstrap.yml`、`README.md`

---

## 7. 架构合规自检（公约 §2 + api.mdc 铁律）

| 铁律 | 自检 |
|------|------|
| 1 算法只在 Python，Java 不写 NLP/模型/图算法 | ✅ 仅 SQL 级聚合 + 读元数据；评分/中心性等均标「待算法落 ADS」 |
| 2 调用链不越层（前端→Java→Python /internal） | ✅ 本模块只对外 REST + 读 ADS，无越层 |
| 7 共享聚合核心 / 只读 ADS | ✅ `gkxlumen-metrics` 定位为聚合核心；全部 `ent_*` 只读，不直连 nGQL/Python/业务库 |
| OpenAPI 契约先行 | ✅ 契约 md + openapi yaml 先行 |
| 数据血缘（D9）8 件套 + ⓘ + 🧪 | ✅ catalog 返回 8 件套；`isMock` 驱动 🧪；端点带 metricId 供 ⓘ |
| 不引入新依赖 / 不动配置文件 | ✅ 骨架仅用 demo 已验证依赖；未改父 pom/gitignore；未注册进 reactor → CI 零影响 |
| lumen git 纪律 | ✅ feature 分支 + commit，**未 push**，待人工评审开 PR |

---

## 8. 成本回填（budget-estimate.md）

| 字段 | 值 |
|------|----|
| actual_tokens | ~110k（读种子/契约/探仓 + 产出 11 文件 handoff） |
| model_used | claude-opus（cursor agent） |
| actual_cost | ~$4.2（< $10 阈值，无需复盘） |
| cost_warn | false |

---

## 9. 给评审人 / 后续 PR 的提示

1. 激活模块：父 `pom.xml` `<modules>` 增加 `<module>gkxlumen-metrics</module>`；网关加 `/metrics/v1/**` 路由。
2. 校准依赖坐标：确认 lumen 内 `gkxlumen-common-security/-data/-log` 的实际 artifactId 与本骨架 pom 一致（已按 `com.topcomm:gkxlumen-common-*` 填写，与 common 模块结构吻合）。
3. catalog 源切换：`MetricCatalogSource` 留有「正式期改注入 cfg_metric Mapper」的接口位，契约不变。
4. 待 ADS 表名定稿（数据库设计.md），把 `EntMetricAggController` 各方法 `mock()` 换成 `dao` 真 SQL（草稿已在 javadoc）。
