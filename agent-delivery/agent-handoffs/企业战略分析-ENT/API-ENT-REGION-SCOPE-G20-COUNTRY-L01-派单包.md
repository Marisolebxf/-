# 派单包：API-ENT-REGION-SCOPE-G20-COUNTRY-L01

> 当前状态：`backlog`（待本派单包人工审阅；未认领、未开工）  
> 执行角色：`api-agent`  
> 建议监管：`human:侯佳伟`，派发时由后端团队确认  
> 仓库：`lumen-svc-platform`（正式派发后目标分支 `dev`）  
> 强度：`ponytail full`  
> 性质：实现类 `feature`，`cicd: required`

## 1. 任务目标

补齐 G20 地区树变更在 Java 聚合层的契约，不在 Java 重复实现 Python 逻辑：

1. `region-scopes` 响应保留 Python 的 `bind_country_code`；
2. key-analysis 公共请求透传 `region_ids[]`、`country_codes[]`、`city_codes[]`；
3. recommendation 异步任务继续递归透传嵌套区位参数，并用测试锁定 snake_case wire；
4. Java 只做 DTO、参数校验和 Feign 转发，不查 ES、不拆码、不写 OR/推荐算法。

本单是 `API-ENT-DICT-JAVA-L04` 的增量，不重建 meta Controller/Service/Feign 链路。

## 2. 范围与依据

- 范围基线：`bid-reference/科技信息展示系统和科技专题服务系统.md`
  - §1.1.1.2.4.2.3 企业分析；
  - §1.1.1.2.4.2.3.1 重点企业类型分析；
  - §1.1.1.2.4.2.3.6 招引企业推荐分析；
  - §1.1.1.2.4.2.3.7 培育企业推荐分析。
- 已确认业务口径：`客户决策清单跟踪表.md#Q056`。
- 地区树契约：`PY-ENT-REGION-SCOPE-G20-COUNTRY-L01.md`。
- Python 查询契约：`PY-ENT-KEYANALYSIS-RECOMMEND-COUNTRY-派单包.md`。
- 城市码真源：`agent-delivery/data/ddl/CITY-CODE-G20.md`。
- 架构真源：`architecture-baseline.md` D1–D7。

本单只扩展同一功能链的接口字段，不新增功能点，不触发范围 ±10% 变更。

## 3. 开工门禁与依赖

| 前置任务 | 原因 |
|---|---|
| `API-ENT-DICT-JAVA-L04` | 已有 meta Facade；同目录同文件，必须先 `done` |
| `E-ENT-KEYENT-JAVA-L01` | 已有 key-analysis DTO/Feign；与本单共享 `KeyAnalysisCommonRequest`，必须先 `done` |
| `DATA-ENT-CODE-COUNTRY-APPLY-L01` | `bind_country_code` 与 G20 城市树数据已落库 |
| `PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01` | Java DTO 必须对齐已实现的三分 OR 入参 |
| `PY-ENT-RECOMMEND-GEO-COUNTRY-L01` | recommendation 下游契约已实现 |

全部依赖 `done`、本单转 `ready`、真人确认监管人并完成认领后才能开工。当前 MCP 的 `task-update-fields` 不能补写 `depends_on`；registry 已在 note 记录 `E-ENT-KEYENT-JAVA-L01` 硬 Convoy，coordinator 转 `ready` 前必须人工核验。

## 4. 当前代码基线与缺口

| 位置 | 当前行为 | 本单缺口 |
|---|---|---|
| `EnterpriseResponseDTOs.RegionScopeItem` | 有 `bindAdminCode`、`bindCityCode`，使用 `SnakeCaseStrategy` | 缺 `bindCountryCode`，Python 返回字段会被忽略 |
| `KeyAnalysisCommonRequest` | 有单值 `regionId`/`regionLevel` | 缺三数组 |
| `GkxSearchKeyAnalysisFeignClient` | 各端点复用公共 DTO | DTO 补齐后应自然透传，禁止各端点重复加字段 |
| `TalentRecommendAnalysisAdapterImpl` | `Map` 入参经 `AnalysisRequestBodySupport` 递归 camel→snake | 生产代码原则上无需改；缺区位嵌套回归测试 |

## 5. 冻结契约

### 5.1 `region-scopes` 响应

网关：

```text
POST /enterprise/topic/v1/search/meta/region-scopes
```

服务内：

```text
POST /topic/v1/search/meta/region-scopes
```

Python：

```text
POST /internal/gkx-search/meta/region-scopes
```

节点字段：

```json
{
  "scope_code": "g20-c-jpn",
  "scope_name": "日本",
  "node_kind": "country",
  "bind_admin_code": null,
  "bind_country_code": "JPN",
  "bind_city_code": null,
  "children": []
}
```

Java DTO 使用 `bindCountryCode`，通过 `@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)` 与 wire 字段 `bind_country_code` 对齐。

### 5.2 key-analysis 请求

`KeyAnalysisCommonRequest` 增量字段：

```text
List<String> regionIds    ↔ region_ids
List<String> countryCodes ↔ country_codes
List<String> cityCodes    ↔ city_codes
```

保留现有 `regionId`、`regionLevel`，避免破坏旧前端和国内单选路径；新前端优先发送三数组。Java 不合并、不展开、不判定 alpha-3/UN/LOCODE，只原样透传。

请求样例：

```json
{
  "region_ids": ["440300"],
  "country_codes": ["JPN"],
  "city_codes": ["USNYC"],
  "chain_codes": [],
  "tag_codes": [],
  "base_tag": "key_enterprise"
}
```

### 5.3 recommendation 异步任务

当前正式链路：

```text
POST /topic/v1/analysis/tasks
  → TalentRecommendAnalysisAdapterImpl
  → AnalysisRequestBodySupport.build(...)
  → /internal/gkx-ai/recommend/tasks
```

前端 camelCase 样例：

```json
{
  "analysisType": "talent_recommend",
  "params": {
    "subType": "attraction",
    "selectionMode": "filter",
    "filters": {
      "geographicSources": ["440300", "JPN", "USNYC"]
    }
  }
}
```

下游必须得到：

```json
{
  "analysis_type": "talent_recommend",
  "sub_type": "attraction",
  "selection_mode": "filter",
  "filters": {
    "geographic_sources": ["440300", "JPN", "USNYC"]
  }
}
```

若现有 `AnalysisRequestBodySupport` 已正确处理，只补测试，不改生产实现。不得为 recommendation 新建重复的强类型 DTO 或 Java 区位解析器。

## 6. 实现要求

1. `RegionScopeItem` 增加 `bindCountryCode` 及完整中文 Javadoc；
2. `KeyAnalysisCommonRequest` 增加三数组及完整中文 Javadoc；
3. 所有 key-analysis Controller/Service/Feign 继续复用公共 DTO，不在各端点复制字段；
4. 现有 `regionId`/`regionLevel` 保持兼容；空数组原样传递或按现有 Jackson 规则处理，不自动填默认地域；
5. recommendation 先以回归测试验证现状；测试通过则不改 `TalentRecommendAnalysisAdapterImpl`；
6. Java 禁止访问 ES、编写区位三分 OR、正则拆码、候选企业解析或算法筛选；
7. OpenAPI/接口文档补充国家码、城市码和三数组样例；
8. 使用现有 OTel Java Agent 和 trace 传播，不关闭、不另造埋点框架。

## 7. 建议触达文件

- `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/src/main/java/com/topcomm/gkxlumen/topic/enterprise/api/dto/EnterpriseResponseDTOs.java`
- `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/src/main/java/com/topcomm/gkxlumen/topic/enterprise/api/dto/keyanalysis/KeyAnalysisCommonRequest.java`
- `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/src/test/java/**/RegionScopeItemSerializationTest.java`（或仓内等价 Jackson 契约测试位置）
- `gkxlumen-topic-enterprise/gkxlumen-topic-enterprise-api/src/test/java/**/KeyAnalysisCommonRequestSerializationTest.java`（或等价位置）
- `gkxlumen-topic-async-service/gkxlumen-topic-async-service-biz/src/test/java/com/topcomm/gkxlumen/topic/async/service/adapter/analysis/AnalysisAdapterValidationTest.java`
- `agent-delivery/data/data-design/企业/E-ENT-KEYENT-JAVA-L01-实施方案.md`（公共 Body 字段说明，若实际文件名一致）
- `agent-delivery/agent-handoffs/企业战略分析-ENT/API-ENT-full-catalog.md`（若作为当前契约目录）
- 对应 OpenAPI/契约文档

若现有序列化测试位置不同，沿用仓内测试组织，不为两项字段新增测试框架。

## 8. 验收用例

| 场景 | 期望 |
|---|---|
| Python 返回 `bind_country_code=JPN` | Java response 保留为 `bind_country_code: "JPN"` |
| Python 返回未知扩展字段 | 既有 `ignoreUnknown` 行为不回归 |
| key-analysis 仅国内 | `region_ids` 原样到 Python |
| key-analysis 仅国家 | `country_codes` 原样到 Python |
| key-analysis 仅海外城市 | `city_codes` 原样到 Python |
| key-analysis 混选 | 三数组同时保留；Java 不改变 OR 语义 |
| 旧请求只含 `region_id` | 继续可用 |
| recommend `geographicSources` | 下游为 `geographic_sources`，值与顺序不变 |
| recommend 结构化数组 | 若前端发送，递归转为对应 snake_case，值不丢失 |
| 空数组/空 filters | 保持现有 validation 规则，不私自补深圳或全国 |

## 9. DoD

1. Registry 中的 7 条 `definition_of_done` 全部满足；
2. 单元/契约测试覆盖 §8；
3. 公开类、字段、方法中文 Javadoc 完整；
4. `spring-javaformat`、目标模块测试和构建通过；
5. CI 绿，K8s dev rollout 成功；
6. 联调证据包含 region-scopes 响应、key-analysis 混选请求、recommend 下游请求；
7. handoff：`agent-handoffs/企业战略分析-ENT/API-ENT-REGION-SCOPE-G20-COUNTRY-L01.md`；
8. handoff 含 commit/pipeline/dev URL、Swagger、traceId、架构 D1–D10 自检、`ponytail` 与 cost 四字段。

## 10. 不做

- 不在 Java 查询 Elasticsearch、MySQL ODS/DWD 或 Nebula；
- 不在 Java 实现区位拆码、三分 OR、候选企业解析或推荐算法；
- 不改前端 Cascader；
- 不改 Python 算法/适配层；
- 不改 DIM/ES mapping/灌数；
- 不删除旧 `region_id` 兼容字段；
- 不新建 recommendation 重复 DTO，除非现有 Map 契约经测试证明无法安全透传且经架构师确认。

## 11. 待审派单话术

```text
/goal API-ENT-REGION-SCOPE-G20-COUNTRY-L01
强度：ponytail full
仓：lumen-svc-platform；目标分支 dev
监管：待后端团队确认（建议 human:侯佳伟）
前置：API-ENT-DICT-JAVA-L04、E-ENT-KEYENT-JAVA-L01、DATA-ENT-CODE-COUNTRY-APPLY-L01、PY-ENT-KEYANALYSIS-COUNTRY-SCOPE-L01、PY-ENT-RECOMMEND-GEO-COUNTRY-L01 均 done
目标：补 bind_country_code、key-analysis 三数组 DTO，并用测试锁定 recommendation 嵌套 filters 递归 snake_case 透传
硬边界：Java 仅 DTO/校验/Feign；不查 ES、不拆码、不写 OR/算法；旧 region_id 保持兼容
必读：本派单包、architecture-baseline.md、PY 两份地区契约、CITY-CODE-G20.md、api.mdc
Handoff：agent-handoffs/企业战略分析-ENT/API-ENT-REGION-SCOPE-G20-COUNTRY-L01.md
```

> 本文件经用户审阅后才能正式派发；审阅前不得认领、编码或推送。
