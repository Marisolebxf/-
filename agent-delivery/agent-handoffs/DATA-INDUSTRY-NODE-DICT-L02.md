# DATA-INDUSTRY-NODE-DICT-L02 · 产业节点字典端点 + 高筛候选切字典（收窄版）

> 执行会话收窄裁定（覆盖原交付 2 部分）：不新增 `industry_node_code` 字段、不做四段值 / OR 组出站；
> 节点查询维持既有 `industry_node`（industry_node_names_flat）名称 in 语义，不扩张查询语句语义。

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent`（frontend-agent 接线） |
| supervised_by | `human:徐滕强` |
| claim_type | `pull` |
| 说明 | 收窄指令来自用户裁定（2026-10-27），registry note 已同步 |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 最小 diff：py 端点 1 函数 + 桥接 1 函数 + 白名单 1 行；Java 纯透传五处仿 chains 先例；UI 复用既有注入先例（setClusterScopeResolver → setNodeOptionsFetcher）。未用 YAGNI 跳过可观测/契约对齐 |

## 问题清单

- 数据形态双库差异（实测）：live `gkxlumenx_dwd.industry_chain_node` 1273 行 / 12 链（INB1204…INB2505，无 INB17xx）；demo `demo_gkxlumenx_dwd` 222 行、含 INB17xx 链、node_code 为 `INB1309-01` 破折号形态。端点逻辑对两库一致（精确 → 前缀桥接 → 空+hint），无需按库分支。
- `industry_chain` 表两库均混入全层级码（非纯链根），前缀桥接若查该表按 LENGTH 排序会误选深层叶码——已改查 `industry_chain_node` 自身 DISTINCT chain_id 取**最短**命中（= 树根），并有单测钉住。
- Q068 产业码（INB170101 等）在 live 库与 12 棵节点树前缀零交集：诚实返回 `items:[] + hint`，不伪造全量；demo 库因字典含 17xx 链则精确命中。
- Java 本机默认 JDK 为 1.8（无效目标发行版 17），验证需 `JAVA_HOME=jdk-21`；biz 模块老 surefire 不认 JUnit5（Tests run: 0），单测经 junit-platform-console-standalone 直跑验证（3/3 绿）。CI 侧 pipeline 用 JDK17 + 自有 surefire 配置，不受本机影响。

## 修改内容

### lumen-topic-py（Python，改动停本地待验收）
- `gkx_search_service/views/meta.py`：
  - 新增 `POST /internal/gkx-search/meta/industry-nodes`（`meta_industry_nodes`）：body `{chain_code?}` → `{items:[{node_code,node_name,chain_id}], hint?}`，`ORDER BY sort_no, node_code`，空 chain_code 返回全量；
  - 新增 `_resolve_chain_id` 桥接：精确匹配 chain_id → 码长>7 时前缀匹配树根集合（最短命中）→ 空 + hint；
  - 模块头 v10.6 变更记录。
- `gkx_search_service/views/enterprise_search.py`：聚合白名单 `allowed` 加 `industry_node_names_flat`（修第三级聚合 buckets=null）。
- `tests/test_industry_node_dict.py`（新增）：5 用例（按链过滤+SQL 形态 / 空码全量 / 子码桥接树根 / Q068 空+hint / 聚合白名单功能断言）。

### lumen-svc-platform（Java，改动停本地待验收）
- `gkxlumen-topic-enterprise-api`：新增 `IndustryNodesDTOs`（Request{chain_code} / Item{nodeCode,nodeName,chainId} / Response{items,hint}）。
- `gkxlumen-topic-enterprise-biz`：`RemoteEnterprisePythonClient.industryNodes`（Feign → `/internal/gkx-search/meta/industry-nodes`）；`EnterpriseMetaDictService` + Impl（null 兜底透传）；`EnterpriseMetaDictController` `POST /topic/v1/search/meta/industry-nodes`；`EnterpriseMetaDictServiceImplTest` +2 用例。
- 网关对外完整路径：`/enterprise/topic/v1/search/meta/industry-nodes`。

### lumen-ui-topic（Vue，改动停本地待验收）
- `src/api/enterprise/paths.ts`：`searchMetaIndustryNodes` 路径。
- `src/api/enterprise/types/search.ts`：`EntIndustryNodesRequest/Response`、`EntIndustryNodeItem`；聚合注释补 industry_node_names_flat。
- `src/api/enterprise/search.ts` + `index.ts`：`entSearchMetaIndustryNodes` API 及聚合出口。
- `src/utils/industryLinkOutbound.ts`：`fetchIndustryNodeOptions(chainCode)` 重写——默认走字典端点（按链 Map 缓存，仅成功写缓存），失败回退聚合镜像 + console.warn；新增 `setNodeOptionsFetcher` 测试注入缝（同 setClusterScopeResolver 先例）；`resetIndustryLinkCaches` 清 Map。
- `src/components/filter/IndustryThreeLevelCascader.vue`：load-more 传当前产业 INB 码（option.value）给新 API；头注释更新。值序列化维持「集群ID|INB码|节点名」三段不变；⚠️ 角标维持 fixture schema 层（Q068 仍 pending_client）。
- `scripts/industry-link-outbound.test.mts`：+3 用例（按链过滤+缓存 / 失败不缓存可重试 / 出站节点叶维持 industry_node 名称 in 回归锚）。

## 测试结果

- **py**：`pytest tests/test_industry_node_dict.py` → 5 passed；相关回归（meta_dimension / query_tree_dsl / gkx_svc_meta / enterprise_search / gkx_svc_search）41+ passed，7 failed 全部为存量（stash 干净区复跑同样失败：chains fallback ×2、schema 对齐、qa_passthrough ×4，即工单已知 finance 口径存量）。
- **py 真库端到端（demo 库）**：全量 222 items；`INB1309` → 4 items（首条 算力芯片）；`INB130901` 桥接 → 树根 INB1309 同 4 items 无 hint；`INB170101`（Q068）→ demo 精确命中，live 库同入参返回空+hint（语义一致）。
- **Java**：`mvn -pl gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz -am compile` → BUILD SUCCESS（JDK21）；`EnterpriseMetaDictServiceImplTest` 经 JUnit Console Launcher → 3/3 绿（老 surefire 跑 0 个测试为工程存量现象）。
- **UI**：`pnpm type-check` 0 错；`pnpm build` 成功；`node --test`（alias-loader）4 套件 36/36 绿。
- **端到端出站语义**：选「新一代信息技术→半导体与集成电路→某节点」出站仍为 `{field:'industry_node', operator:'in', value:[节点名]}`（收窄裁定形态，有回归锚测试钉住）。

## 遗留风险

- demo 库与 live 库 `industry_chain_node` 行数/码形态不一致（222 vs 1273），后续以 live 库为准收口时桥接/hint 行为自动随数据切换，无需改码。
- UI 聚合镜像回退路径仅在浏览器可用（依赖 import.meta.env 链），node --test 无法覆盖该分支（已测失败→空→可重试语义）。
- 聚合白名单放开 `industry_node_names_flat` 后，其它调用方也可聚合该字段——语义与 catalog `industry_node` 一致，无额外暴露。

## CI/CD（必填）

- 分支：三仓均 `dev`（改动停本地，**未 commit/push**，待人工验收）
- commit：无（见上）
- pipeline URL / ID：N/A（本单禁止推送）
- 部署 namespace / 镜像 tag：N/A
- K8s rollout：未触发
- dev 测试 URL / 命令与结果：见「测试结果」（本机 pytest / JUnit Console / pnpm 三绿）

## 可观测性（建议）

- OTEL_SERVICE_NAME：不适用（纯透传端点，走既有 search 服务埋点）
- traceId（dev 抽样）：无（未部署）
- Tempo / Loki：无

## 涉及文件

- `repos/lumen-topic-py/gkx_search_service/views/meta.py`
- `repos/lumen-topic-py/gkx_search_service/views/enterprise_search.py`
- `repos/lumen-topic-py/tests/test_industry_node_dict.py`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/.../api/dto/meta/IndustryNodesDTOs.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/.../feign/RemoteEnterprisePythonClient.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/.../service/meta/EnterpriseMetaDictService.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/.../service/meta/impl/EnterpriseMetaDictServiceImpl.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/.../controller/meta/EnterpriseMetaDictController.java`
- `repos/lumen-svc-platform/gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-biz/src/test/.../EnterpriseMetaDictServiceImplTest.java`
- `repos/lumen-ui-topic/src/api/enterprise/paths.ts`
- `repos/lumen-ui-topic/src/api/enterprise/types/search.ts`
- `repos/lumen-ui-topic/src/api/enterprise/search.ts`
- `repos/lumen-ui-topic/src/api/enterprise/index.ts`
- `repos/lumen-ui-topic/src/utils/industryLinkOutbound.ts`
- `repos/lumen-ui-topic/src/components/filter/IndustryThreeLevelCascader.vue`
- `repos/lumen-ui-topic/scripts/industry-link-outbound.test.mts`
