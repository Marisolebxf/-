# DATA-INDUSTRY-NODE-DICT-L02 · 产业节点字典端点 + 高筛候选切字典（收窄版 + 走查修正轮）

> 执行会话收窄裁定（覆盖原交付 2 部分）：不新增 `industry_node_code` 字段、不做四段值 / OR 组出站；
> 节点查询维持既有 `industry_node`（industry_node_names_flat）名称 in 语义，不扩张查询语句语义。
>
> **走查修正轮（2026-10-27 晚，用户裁定，纯代码修正·禁动表·禁重灌）**：
> ① 后端桥接主路径改查 `industry_chain.industry_id`（v5 §5.1 语义），新增 `/industry-chains` 链行集端点；
> ② 前端第三级改「链树」：按 chain_tier/parent_chain_id 逐层展开 L2+ 子链（live 库 L1~L8 共 1261 链行），
>    叶子链再懒加载节点——替代写死两层 + 节点直挂的旧形态。

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
  - 新增 `_resolve_chain_id` 桥接（走查修正后降级为旧契约兼容，主路径让位 industry_id）；
  - **走查修正**：新增 `POST /internal/gkx-search/meta/industry-chains`（`meta_industry_chains`）：
    body `{industry_code}`（Q068 产业码或任意链码，子链码经 industry_id 归属定位）→
    `WHERE industry_id=%s` 返回该产业全部链行 `{chain_id, chain_name, chain_tier, parent_chain_id}`，
    ORDER BY chain_tier, chain_id；空参/无归属行回 hint；v10.7 变更头；
  - 模块头 v10.6 / v10.7 变更记录。
- `gkx_search_service/views/enterprise_search.py`：聚合白名单 `allowed` 加 `industry_node_names_flat`（修第三级聚合 buckets=null）。
- `tests/test_industry_node_dict.py`（新增）：9 用例（节点字典 5 + 链行集 4：industry_id 过滤/空参拒绝/子链码归属定位/未知码 hint）。

### lumen-svc-platform（Java，改动停本地待验收）
- `gkxlumen-topic-enterprise-api`：新增 `IndustryNodesDTOs`（Request{chain_code} / Item{nodeCode,nodeName,chainId} / Response{items,hint}）；
  **走查修正**：新增 `IndustryChainsDTOs`（Request{industry_code} / Item{chainId,chainName,chainTier,parentChainId} / Response{items,hint}）。
- `gkxlumen-topic-enterprise-biz`：`RemoteEnterprisePythonClient.industryNodes` + `industryChains`（Feign 两方法）；
  `EnterpriseMetaDictService` + Impl（null 兜底透传两方法）；
  `EnterpriseMetaDictController` `POST /topic/v1/search/meta/industry-nodes` + `POST /topic/v1/search/meta/industry-chains`；
  `EnterpriseMetaDictServiceImplTest` 4 用例（nodes 转发/nodes null 兜底/chains 转发/政策导向存量）。
- 网关对外完整路径：`/enterprise/topic/v1/search/meta/industry-nodes`、`/enterprise/topic/v1/search/meta/industry-chains`。

### lumen-ui-topic（Vue，改动停本地待验收）
- `src/api/enterprise/paths.ts`：`searchMetaIndustryNodes` + `searchMetaIndustryChains` 路径。
- `src/api/enterprise/types/search.ts`：`EntIndustryNodesRequest/Response`、`EntIndustryNodeItem`；
  **走查修正**：`EntIndustryChainsRequest/Response`、`EntIndustryChainRow`（chain_tier/parent_chain_id；命名避撞 common 旧同名）。
- `src/api/enterprise/search.ts` + `index.ts`：`entSearchMetaIndustryNodes` + `entSearchMetaIndustryChains` API 及聚合出口。
- `src/utils/industryLinkOutbound.ts`：
  - `fetchIndustryNodeOptions(chainCode)`（按链 Map 缓存，失败回退聚合镜像 + console.warn，`setNodeOptionsFetcher` 注入缝）；
  - **走查修正**：`fetchIndustryChainRows`（链行集按产业缓存）+ `reparentByPrefix`（live 库 77 行 parent 塌陷按码前缀归位）
    + `buildChainChildIndex`（父码 → 子链行 O(1) 桶）+ `fetchIndustryChildren(industryCode, chainCode)`；
  - `expandIndustryLinkLeaf` 语义收口：**末段=勾选对象**——INB 码（首层产业或深层子链）→ industry_chain_code prefix；
    节点名（任意深度）→ industry_node in 名称；旧码（IC001 系）映射 Q068 后走 prefix；中间段仅导航不参与匹配。
- `src/types/industryLink.ts`：值模型支持任意深度——中间段严格 INB/旧码校验，末段码或节点名不限（`isIndustryLinkLeaf` 不再限 3 段）。
- `src/components/filter/IndustryThreeLevelCascader.vue`：load-more 重写——先查子链（有 → 子链 children，isLeaf=false 继续懒加载），
  无子链再拉节点（叶子）；产业行带 industryCode 供深层取链行集；⚠️ 角标维持 fixture schema 层。
- `src/components/search/QueryConditionSummary.vue`：`formatIndustryLink` 按段解析显示完整勾选路径（深层链码回退原码，集群名/产业名查目录）。
- `scripts/industry-link-outbound.test.mts`：19 用例（出站形态 10 + 节点字典 3 + 链树导航 6：逐层展开/塌陷归位/失败重试/勾链出站/深层勾节点出站/四段值识别）。

## 测试结果

- **py**：`pytest tests/test_industry_node_dict.py` → **9 passed**；全仓回归 288 passed / 7 failed 全部为存量（干净区复跑同样失败，见问题清单与上轮记录）。
- **py 真库端到端（demo 库）**：`{industry_code:"INB1701"}` → 8 链行（L0 新一代信息技术 + 7×L1）；子链码 `INB130901` 经 industry_id 归属定位返回整产业链行集；`INB170101` 节点 8 个（首节点 集成电路设计）。live 库结构对照：L1 12 / L2 41 / L3 165 / L4 420 / L5 388 / L6 142 / L7 80 / L8 25。
- **Java**：`mvn api install + biz compile + test-compile` → 全部 BUILD SUCCESS（JDK21）；`EnterpriseMetaDictServiceImplTest` 经 JUnit Console Launcher → **4/4 绿**。
- **UI**：`pnpm type-check` 0 错；`pnpm build` 成功；`node --test`（alias-loader）4 套件 **42/42 绿**。
- **端到端出站语义**：
  - 勾深层子链：`CL-SEI-01|INB1309|INB130901|INB13090101` → `{field:'industry_chain_code', operator:'in', value:['INB13090101']}`（码前缀自含子树，中间层级仅导航）；
  - 深层勾节点：`CL-SEI-01|INB1309|INB130901|机器学习框架` → `{field:'industry_node', operator:'in', value:['机器学习框架']}`；
  - 旧三段历史值与首层勾选形态回归通过（42 用例内回归锚）。

## 遗留风险

- demo 库与 live 库 `industry_chain` 层级差异（demo 仅 L0/L1 共 49 行 vs live L1~L8 共 1261 行）：demo 环境链树暂只比 live 少展示深度，逻辑一致；live 灌齐后端到端自动补全深度，无需改码。
- live 库 77 行 parent_chain_id 塌陷指 L1（码前缀完好）：前端 `reparentByPrefix` 已按前缀归位兜底；若后续数据修正 parent_chain_id，归位逻辑自动退化为直通（取最长前缀父即真父），无需改码。
- UI 聚合镜像回退路径仅在浏览器可用（依赖 import.meta.env 链），node --test 无法覆盖该分支（已测失败→空→可重试语义）。
- QueryConditionSummary 深层子链中文名暂回退显示原码（目录仅含集群/l0 两级）；待链行集进入目录层后可回填链名。
- 勾中间层链与勾其子链会产出两条 prefix 叶（如 INB130901 与 INB13090101）——prefix 语义下两者交集=子集，结果集不受污染，与既「集群+产业混选」聚合行为一致。

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
