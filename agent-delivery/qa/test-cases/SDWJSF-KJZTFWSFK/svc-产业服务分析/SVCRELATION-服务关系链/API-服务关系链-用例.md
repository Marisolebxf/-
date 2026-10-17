# 智能服务集群-科技专题服务算法库测试用例（服务关系链 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 服务关系链  
> **catalog**：`entry_id=svc.relation` · `catalog_page_id=svc.relation` · path `/industry-service/relation`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.relation`  
> **A 线对照**：`fp-split-by-api-run/work/L42.md`（覆盖矩阵见本目录 `coverage-fp.md`）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | `GET /entan/v1/svc/models`（查询参数 `kind`，本页验收取值 **relation**）；`GET /entan/v1/svc/graph`（查询参数 `limit`） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000589（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页 **2** 个 endpoint 均为 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 density（如 0.042）、centrality、机构名称、nodes/edges 示例数量或边关系文案作为通过条件 |
| 合 path 区分 | `GET /entan/v1/svc/models` 为多服务机构模型页共用；本页验收须 **`kind=relation`** + 页 title「服务关系链」，不得串其它 kind 模型结果。`GET /entan/v1/svc/graph` 与服务机构图谱读接口 path 相同时，合表按 **`endpoint_id=svc.relation.graph`** 与本页 hang 区分验收 |
| 样例与契约差 | `sampleResponse` 含 `relation_summary.ext`、`relation_top[].org_id`/`centrality`、图上 `weight`/`mapped_from` 等；契约 `responseFields` 仅声明 `relation_summary.density`、`relation_top`、`nodes`、`edges`。断言 **只强制 responseFields**；样例扩展字段不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **2** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000589`～`000598`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000589 | 产业服务分析 | 服务关系链 | 契约-不可用 | 服务关系链模型 | 服务关系链 | 关系链模型 | catalog 不可用态下关系链模型接口可识别非 live 成功 | 1、已确认 catalog `svc.relation.models` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 density、centrality 或机构名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产关系链模型判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_RELATION_DENSITY | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-01 金样 §0未试调 catalog_status=unavailable kind=relation |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000590 | 产业服务分析 | 服务关系链 | 异常-鉴权 | 服务关系链模型 | 服务关系链 | 关系链模型 | 关系链模型接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 relation_summary/relation_top 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-01；graph 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000591 | 产业服务分析 | 服务关系链 | 异常-非法kind | 服务关系链模型 | 服务关系链 | 关系链模型 | kind 非法取值时返回可识别失败而非伪关系链成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 relation_summary/relation_top 成功态或 sample 形态密度成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-02；矩阵挂 kind、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000592 | 产业服务分析 | 服务关系链 | 异常-非本页kind | 服务关系链模型 | 服务关系链 | 关系链模型 | kind 为其它模型页取值时不得当作本页 relation 结果验收 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-03 | 1、响应为失败态或成功载荷语义不得被本页当作 kind=relation 关系链模型通过；2、不得将 tech 等其它 kind 的 sample 形态当作本页 relation_summary/relation_top 验收依据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-03；合 path 串 kind 防护 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000593 | 产业服务分析 | 服务关系链 | 契约-字段形态 | 服务关系链模型 | 服务关系链 | 关系链模型 | 成功信封下契约出参 density 与 relation_top 若存在是否符合形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000589 | 1.GET /entan/v1/svc/models，查询参数取组合 MOD-01 | 1、若 code 属成功集合且载荷含 relation_summary.density，则其为 number；2、若含 relation_top，则其为 array；3、不得以 sample 中 0.042 或中心度具体值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_RELATION_DENSITY | INTEG | | | endpoint_id=svc.relation.models catalog_page_id=svc.relation 组合=MOD-01；矩阵挂 relation_summary.density、relation_top |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000594 | 产业服务分析 | 服务关系链 | 契约-不可用 | 关系链图谱 | 服务关系链 | 关系链图谱 | catalog 不可用态下关系链图谱接口可识别非 live 成功 | 1、已确认 catalog `svc.relation.graph` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中节点/边数量或机构名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产关系网络判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000595 | 产业服务分析 | 服务关系链 | 异常-鉴权 | 关系链图谱 | 服务关系链 | 关系链图谱 | 关系链图谱接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 nodes/edges 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000596 | 产业服务分析 | 服务关系链 | 异常-非法limit | 关系链图谱 | 服务关系链 | 关系链图谱 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断并成功返回 sample 形态 nodes/edges | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-02；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000597 | 产业服务分析 | 服务关系链 | 异常-负limit | 关系链图谱 | 服务关系链 | 关系链图谱 | 负数 limit 时返回可识别入参失败而非空图成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将负数 limit 当作空 nodes/edges 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000598 | 产业服务分析 | 服务关系链 | 契约-字段形态 | 关系链图谱 | 服务关系链 | 关系链图谱 | 成功信封下契约出参 nodes 与 edges 若存在是否符合 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000594 | 1.GET /entan/v1/svc/graph，查询参数取组合 GRF-01 | 1、若 code 属成功集合且载荷含 nodes，则 nodes 为 array；2、若含 edges，则 edges 为 array；3、不得以 sample 中边类型或节点 id 具体值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务关系链模型 | N/A-技术项 | N/A | /entan/v1/svc/graph | | INTEG | | | endpoint_id=svc.relation.graph catalog_page_id=svc.relation 组合=GRF-01；矩阵挂 nodes、edges |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MOD-01 | svc.relation.models | `kind=relation`（对齐 catalog `sampleRequest`） | 本页关系链模型 unavailable 主路径 |
| MOD-02 | svc.relation.models | `kind=__invalid__` | 非法模型 kind |
| MOD-03 | svc.relation.models | `kind=tech`（其它服务机构模型页典型 kind） | 非本页 kind，防合 path 串验收 |
| GRF-01 | svc.relation.graph | `limit=40`（对齐 catalog `sampleRequest`） | 关系链图谱 unavailable 主路径 |
| GRF-02 | svc.relation.graph | `limit=0` | 非正整数节点上限 |
| GRF-03 | svc.relation.graph | `limit=-1` | 负数节点上限 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| svc.relation.models | GET | /entan/v1/svc/models | unavailable | kind（可选；本页验收取值 relation） |
| svc.relation.graph | GET | /entan/v1/svc/graph | unavailable | limit（可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.relation.models | API-000589、000590、000591、000592、000593 |
| svc.relation.graph | API-000594、000595、000596、000597、000598 |

---

## 3. 覆盖自检（§S1）

- [x] 2 个 unavailable endpoint 各 1 条契约占位（API-000589、000594），未写 sample 数值通过条件
- [x] 异常-鉴权 2 条（000590、000595；models 备注 graph 同口径）
- [x] models 入参单缺陷 2 条（000591 非法 kind、000592 非本页 kind）
- [x] graph 入参单缺陷 2 条（000596 limit=0、000597 limit=-1）
- [x] responseFields 契约占位 2 条（000593 models；000598 graph）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000589；graph 契约占位 000594）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000589～000598；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **10** |
| 编号闭区间 | **API-000589**～**API-000598** |
| endpoint 数 | **2**（各 5 条） |
| `_empty` 未覆盖 | **2**（models + graph） |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
