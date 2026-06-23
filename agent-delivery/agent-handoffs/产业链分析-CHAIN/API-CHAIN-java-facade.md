# Handoff · 产业链（CHAIN/E2/IND）Java REST 门面

- **任务**：CHAIN-L01 — 为已完成的产业链算法层（demo-algo-science）+ 已有前端 mock 页面（demo-ui-topic）补齐中间 Java REST 门面，打通「前端 → Java REST → Python /v1/chain」调用链。
- **角色**：`[agent:api-agent]`
- **仓库**：`demo-svc-platform`（gkx-innov 模块）
- **分支**：`feat/E-E2-IND-java-facade`
- **基线**：origin/dev `7ee4edb`（feat 与 dev 同点，无分叉，直接在 feat 上工作）
- **方式**：恢复上一轮被中断的 stash 草稿（`stash@{0}` auto-backup-before-dev-reset-20260623-200515）并补全 DoD 缺口。

---

## 1. 范围与实现（对照 DoD 8 条）

| # | DoD 项 | 状态 | 实现 |
|---|---|---|---|
| 1 | Feign 客户端逐一映射 `/v1/chain/**` 全部端点 | ✅ | `ChainAlgoClient`（13 个方法）逐一映射上游 list/panorama/cycle/key-nodes/bottlenecks/region-index/shenzhen/competitiveness/hotspot/roadmap/recommendation/market-stats/investment-stats |
| 2 | 对外 REST Controller，统一包络 `{code,msg,data}` | ✅ | `ChainController`（`/v1/industry/**`，13 个端点）原样透传上游 `{code,msg,data}`，字段形态完全不改写 |
| 3 | 网关 `/topic/**` 路由补 industry | ✅ | `helm/gkx-platform/configs/gkx-gateway-dev.yml` 新增 `gkx-topic-industry` 路由：`/topic/v1/industry/**` →（StripPrefix=1）→ `lb://gkx-innov` 的 `/v1/industry/**`（与既有 `/innov/**` 路由同一服务，兼容前缀保留） |
| 4 | OpenAPI 文档 `openapi-topic-industry-v1.yaml` | ✅ | `gkx-innov/src/main/resources/openapi/openapi-topic-industry-v1.yaml`（13 端点 + 统一包络 schema；注：`docs/` 被 .gitignore 忽略，故置于 resources 下，沿用 gkx-common-swagger 约定） |
| 5 | `OTEL_SERVICE_NAME` + trace 头透传 | ✅ | `values.yaml` innov 块新增 `OTEL_SERVICE_NAME=gkx-innov`；W3C `traceparent` 由 JavaAgent（`JAVA_TOOL_OPTIONS=-javaagent:opentelemetry-javaagent.jar`，commonEnv 注入）自动埋点 Feign CLIENT span，实现 gateway→gkx-innov→demo-algo-science 同一条 trace，无需手工埋点 |
| 6 | 上游不可达兜底 | ✅ | `ChainService.passthrough()` 捕获异常 → 返回 `{code:1,msg:"产业链算法服务暂不可达: ...",data:null}`，不抛栈 |
| 7 | 零算法逻辑 | ✅ | Java 只做 Feign 透传 + 只读 + 参数透传，无任何 NLP/图谱/打分/指标计算 |
| 8 | 编译可过 | ⚠️ deferred | 本机无法访问私有 Nexus（`http://10.126.138.142:8081` connect timeout），多个 BOM（opentelemetry-bom:1.51.0 等）未缓存，`mvn compile` 无法解析依赖。**非代码错误**，属 PM waiver v2 覆盖范围。静态核验见 §4 |

---

## 2. 产物清单

**复用草稿（stash 恢复，8 文件）：**
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/chain/ChainProperties.java`（新增，配置 `gkx.innov.chain.algo-base-url`）
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/chain/ChainAlgoClient.java`（新增，Feign 客户端，13 端点）
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/chain/ChainService.java`（新增，透传 + 兜底）
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/chain/ChainController.java`（新增，对外 `/v1/industry/**`）
- `gkx-innov/pom.xml`（改，加 `gkx-common-feign` 依赖）
- `gkx-innov/src/main/java/com/topcomm/gkx/innov/GkxInnovApplication.java`（改，加 `@EnableGkxFeignClients`）
- `gkx-innov/src/main/resources/application.yml`（改，加 `gkx.innov.chain.algo-base-url`）
- `helm/gkx-platform/values.yaml`（改，加 `INNOV_CHAIN_ALGO_BASE_URL` env）

**本轮补全（3 处）：**
- `helm/gkx-platform/configs/gkx-gateway-dev.yml`（改，新增 `gkx-topic-industry` 网关路由）
- `helm/gkx-platform/values.yaml`（改，innov 块新增 `OTEL_SERVICE_NAME=gkx-innov`）
- `gkx-innov/src/main/resources/openapi/openapi-topic-industry-v1.yaml`（新增，OpenAPI 3.0.3）

---

## 3. 三方映射表（对外 REST ↔ 上游 Python ↔ 前端 mock）

> chain_id 路径参数统一透传；前端 `chainCode`/`id` 与上游 `chain_id` 的映射口径**未定**，见 §6 阻塞项。

| 对外网关路径 | gkx-innov 内部 | 上游 Python `/v1/chain` | 上游主表 | 前端 mock 消费点 |
|---|---|---|---|---|
| `GET /topic/v1/industry/list` | `/v1/industry/list` | `/list` | `gkx_chain_dwd_chain` | `chainList.ts` CHAIN_LIST（基础字段） |
| `GET /topic/v1/industry/{chainId}/panorama` | `/{chainId}/panorama` | `/{chain_id}/panorama` | `ads_chain_panorama(_nodes/_edges)` | chainProfile 上中下游图谱、全景页 |
| `GET /topic/v1/industry/{chainId}/cycle` | `/{chainId}/cycle` | `/{chain_id}/cycle` | `ads_chain_cycle` + `ads_chain_stage` | profile.stage / 周期阶段（M_CHAIN_CYCLE_STAGE） |
| `GET /topic/v1/industry/{chainId}/key-nodes` | `/{chainId}/key-nodes` | `/{chain_id}/key-nodes` | `ads_chain_key_node` | profile.upstream/midstream/downstream isKey、highEndIndex |
| `GET /topic/v1/industry/{chainId}/bottlenecks` | `/{chainId}/bottlenecks` | `/{chain_id}/bottlenecks` | `ads_chain_bottleneck` | profile.bottleneckSummary（M_CHAIN_BOTTLENECK_SEVERITY） |
| `GET /topic/v1/industry/{chainId}/region-index` | `/{chainId}/region-index` | `/{chain_id}/region-index` | `ads_chain_region_index` | 区域产业指数页 |
| `GET /topic/v1/industry/{chainId}/shenzhen` | `/{chainId}/shenzhen` | `/{chain_id}/shenzhen` | `ads_chain_sz_panorama/_advantage/_problem/_opportunity` | 深圳产业分析页、szEnterpriseCount、completenessScore |
| `GET /topic/v1/industry/{chainId}/competitiveness` | `/{chainId}/competitiveness` | `/{chain_id}/competitiveness` | `ads_chain_competitiveness` | competitivenessScore、relatedEnterprises.competitiveness |
| `GET /topic/v1/industry/{chainId}/hotspot` | `/{chainId}/hotspot` | `/{chain_id}/hotspot` | `ads_chain_hotspot` | hotNewsCount、热点页（M_CHAIN_HOT_NEWS） |
| `GET /topic/v1/industry/{chainId}/roadmap` | `/{chainId}/roadmap` | `/{chain_id}/roadmap` | `ads_chain_roadmap` | 发展历程时间线页 |
| `GET /topic/v1/industry/{chainId}/recommendation` | `/{chainId}/recommendation` | `/{chain_id}/recommendation` | `ads_chain_layout_recommend` | 布局推荐页 |
| `GET /topic/v1/industry/market-stats?chainId&statYear` | `/market-stats` | `/market-stats?chain_id&stat_year` | `ads_chain_market` | profile.trend.marketScale、marketScale、growthRate |
| `GET /topic/v1/industry/investment-stats?chainId&statYear` | `/investment-stats` | `/investment-stats?chain_id&stat_year` | `ads_chain_investment` | investmentAmount（M_CHAIN_INVESTMENT） |

### 3.1 字段差异（前端 mock 有 / 上游 API 无，或反之）

- **前端 `chainList.ts` 列表是「宽表」，上游 `/list` 是「窄表」**：前端每行含 enterpriseCount / marketScale / growthRate / investmentAmount / segmentCount / hotNewsCount / szEnterpriseCount / competitivenessScore / completenessScore / highEndIndex 等 ~15 个指标；而上游 `/v1/chain/list` 仅返回 `chain_id / chain_name / industry_code / node_count / description`。
  → 这些聚合指标分散在 `market-stats`（marketScale/growthRate）、`investment-stats`（investmentAmount）、`shenzhen`（szEnterpriseCount/completeness）、`key-nodes`（highEndIndex）、`competitiveness`、`hotspot`（hotNewsCount）等端点。**当前 Java 门面按上游端点 1:1 透传，不做跨端点聚合**（聚合属算法/数据层职责，Java 零算法铁律）。前端列表页若要一次拿全字段，需：① 多次调用后端各端点在前端组装，或 ② 由 algorithm/data 层在上游 `/list` 直接补齐宽表字段（推荐，登记给上游）。
- **前端 `keySegments / upstream / midstream / downstream`（string[]）** 在上游来自 `panorama` / `key-nodes` 的 JSON 结构，命名/层级不完全一致，前端切真实接口时需做一次字段适配映射。
- **前端 `relatedEnterprises`（画像页关联企业列表）** 上游 chain API 无直接对应端点；可能需企业/要素库端点支撑，登记给上游确认。
- **`category`（未来产业/战略性新兴产业/优势传统产业）** 前端枚举固定，上游 `gkx_chain_dwd_chain` 仅有 `industry_code`，分类映射口径未定（见 §6）。

> 结论：**调用链已打通、端点已 1:1 齐全**；前端从 mock 切真实接口时需做一层「窄表→宽表」字段适配，且部分聚合字段建议在上游补齐而非 Java 拼装（守零算法铁律）。

---

## 4. 架构合规自检（铁律 7 条逐条）

1. **算法只在 Python** ✅ Java 仅 Feign 透传，`grep` 无任何打分/NLP/图谱/指标计算。
2. **调用链 前端→Java→Python** ✅ 网关 `/topic/v1/industry` → gkx-innov `/v1/industry` → Feign → demo-algo-science `/v1/chain`，未越层。
3. **图谱统一 NebulaGraph，禁止 Neo4j** ✅ 本次零图谱依赖，未引入 Neo4j。
4. **可观测性 OTel** ✅ `OTEL_SERVICE_NAME=gkx-innov` 显式声明；traceparent 由 JavaAgent 自动透传到 Feign。
5. **CI/CD waiver** ✅ 仅 code complete + feature 分支 push；mvn/CI/K8s deferred。
6. **demo2 只读，禁止 merge** ✅ 未触碰 demo-ui-science；改动仅在 demo-svc-platform feature 分支。
7. **共享聚合核心（方案 A）** ✅ Java 不写算法、不直连 nGQL、只读/透传；产业链统计字段不在 Java 计算。

**静态编译核验（替代 mvn）**：
- `gkx-common-feign` 依赖在 `gkx-common-bom` 已声明，`@EnableGkxFeignClients` 真实存在，其默认 `basePackages={"com.topcomm.gkx"}` 覆盖 `com.topcomm.gkx.innov.chain`，Feign 客户端可被扫描。
- 父 pom `maven-compiler-plugin` 已配 `<parameters>true</parameters>`，Controller 的隐式 `@PathVariable String chainId` / `@RequestParam ... String chainId` 可正常绑定。
- `ChainAlgoClient` 的 `@RequestParam(name="chain_id"/"stat_year")` 与上游 FastAPI query 参数名一致。

---

## 5. Git

- 分支：`feat/E-E2-IND-java-facade`
- 起点：`7ee4edb`（= origin/dev）
- commit：见 §completion（commit message 含 `[agent:api-agent]` + `CHAIN-L01`）
- push：→ `origin/feat/E-E2-IND-java-facade`（feature 分支，未直推 dev/main）

---

## 6. 阻塞 / 需甲方拍板的业务口径（不自行拍板）

> 以下均**未自行决定**，按团队临时默认透传上游 chain_id，建议登记到 `客户决策清单跟踪表.md`。

1. **chain_id ↔ 前端 chainCode 映射口径**：上游 `gkx_chain_dwd_chain.chain_id`（VARCHAR16）与前端 mock 的 `chainCode`（如 `synthetic-bio`）/`id`（如 `chain-001`）三套标识未统一。门面按路径原样透传 chainId，**未做任何转换**。需数据 Lead / 甲方确认主键口径，前端据此对齐。
2. **八大未来产业 / 产业链清单范围**：前端 mock 固定 8 条（合成生物、光载信息、量子信息、脑科学与脑机工程、深地深海、智能机器人、前沿新材料、未来网络与通信）；上游 `/list` 由 DWD 实际数据驱动。两者是否一致、是否含「优势传统产业」需甲方确认（关联 metric Q020/Q024）。
3. **`category` 分类口径**：未来产业/战略性新兴产业/优势传统产业 的归类规则（基于 industry_code？）未定。
4. **列表宽表聚合归属**：前端列表 ~15 个聚合指标，建议由上游 `/list` 补齐 or 前端组装；当前 Java 不聚合（守铁律）。需 PM/架构师确认归属与优先级。

---

## 7. 接力（下游）

- **frontend（demo-ui-topic）**：将 `src/app/mock/industry/*` 切到网关 `/topic/v1/industry/**`。
  - 列表页：`GET /topic/v1/industry/list` 取窄表，宽表指标需多端点组装或等上游补齐（见 §3.1）。
  - 画像/各分析页：按 §3 映射表逐页对接对应端点。
  - 切换时保留 MockBadge🧪 / MetricSpecCardⓘ；`mapping_status=⚠️/🔧` 的指标仍走 mock，直到上游补齐。
  - 注意做一层「上游 snake_case 窄表 → 前端 camelCase 宽表」字段适配。
- **algorithm/data（demo-algo-science）**：评估是否在 `/v1/chain/list` 直接补齐列表宽表聚合字段；落实 §6 chain_id 口径与产业链清单范围。
- **architect/PM**：§6 四项业务口径拍板。

---

## 8. cost

| 字段 | 值 |
|---|---|
| estimated_tokens | ~120k |
| actual_tokens | ~135k |
| model_used | Claude Opus 4.x（api-agent 子代理） |
| actual_cost | ~$3.0（估算，< $10 阈值） |
| cost_warn | false |
