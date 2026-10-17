# 智能服务集群-科技专题服务算法库测试用例（服务机构实体与关系 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 服务机构实体与关系  
> **catalog**：`entry_id=svc.graph` · `catalog_page_id=svc.graph` · path `/industry-service/graph`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/svc.json` · 页 `svc.graph`（10 endpoints）  
> **A 线对照**：`fp-split-by-api-run/work/L11.md`（ner/main）· `L12.md`（intra/hang 关系类）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000534（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-000534」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **10** 个 endpoint 均为 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 written_nodes/written_edges/nodes/edges 示例数值、vid、权重作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl / 浏览器；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST 写入类为 JSON body；GET 浏览类为查询参数；组合见附录 A |
| 样例与契约差 | 样例顶层字段常多于 `responseFields`；断言 **仅强制** catalog `responseFields` |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.graph`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000534 | 图谱 | 服务机构实体与关系 | 契约-不可用 | A 实体识别 SVC_NER_ORG | 服务机构实体与关系 | A 实体识别 SVC_NER_ORG | catalog 不可用态下实体识别接口返回可识别非成功契约信封 | 1、已确认 catalog `svc.graph.ner` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/ner，请求体取组合 NER-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 written_nodes/skipped 与 string 型 space 的成功业务载荷；4、不得将 sampleResponse 写入点示例作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/ner |  | INTEG |  |  | endpoint_id=svc.graph.ner catalog_page_id=svc.graph 组合=NER-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000535 | 图谱 | 服务机构实体与关系 | 异常-鉴权 | A 实体识别 SVC_NER_ORG | 服务机构实体与关系 | A 实体识别 SVC_NER_ORG | 实体识别接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /entan/v1/svc/graph/ner，请求体取组合 NER-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务图谱写入载荷） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/ner |  | INTEG |  |  | endpoint_id=svc.graph.ner catalog_page_id=svc.graph 组合=NER-01；全页鉴权代表 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000536 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | A 实体识别 SVC_NER_ORG | 服务机构实体与关系 | A 实体识别 SVC_NER_ORG | 实体识别接口缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/ner，请求体取组合 NER-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 written_nodes 冒充 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/ner |  | INTEG |  |  | endpoint_id=svc.graph.ner catalog_page_id=svc.graph 组合=NER-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000537 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | A 实体识别 SVC_NER_ORG | 服务机构实体与关系 | A 实体识别 SVC_NER_ORG | 实体识别接口缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/ner，请求体取组合 NER-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/ner |  | INTEG |  |  | endpoint_id=svc.graph.ner catalog_page_id=svc.graph 组合=NER-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000538 | 图谱 | 服务机构实体与关系 | 异常-非法scope | A 实体识别 SVC_NER_ORG | 服务机构实体与关系 | A 实体识别 SVC_NER_ORG | 实体识别接口 scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/ner，请求体取组合 NER-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/ner |  | INTEG |  |  | endpoint_id=svc.graph.ner catalog_page_id=svc.graph 组合=NER-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000539 | 图谱 | 服务机构实体与关系 | 契约-不可用 | B 关系边上图 SVC_RE_SVC_SVC | 服务机构实体与关系 | B 关系边上图 SVC_RE_SVC_SVC | catalog 不可用态下机构间关系接口返回可识别非成功契约信封 | 1、已确认 catalog `svc.graph.intra` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/intra，请求体取组合 PRT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 written_edges/skipped 的成功业务载荷；4、禁止 sampleResponse 边示例作通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/intra |  | INTEG |  |  | endpoint_id=svc.graph.intra catalog_page_id=svc.graph 组合=PRT-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000540 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | B 关系边上图 SVC_RE_SVC_SVC | 服务机构实体与关系 | B 关系边上图 SVC_RE_SVC_SVC | 机构间关系接口缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/intra，请求体取组合 PRT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/intra |  | INTEG |  |  | endpoint_id=svc.graph.intra catalog_page_id=svc.graph 组合=PRT-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000541 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | B 关系边上图 SVC_RE_SVC_SVC | 服务机构实体与关系 | B 关系边上图 SVC_RE_SVC_SVC | 机构间关系接口缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/intra，请求体取组合 PRT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/intra |  | INTEG |  |  | endpoint_id=svc.graph.intra catalog_page_id=svc.graph 组合=PRT-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000542 | 图谱 | 服务机构实体与关系 | 异常-缺必填relation_whitelist | B 关系边上图 SVC_RE_SVC_SVC | 服务机构实体与关系 | B 关系边上图 SVC_RE_SVC_SVC | 机构间关系接口缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/intra，请求体取组合 PRT-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/intra |  | INTEG |  |  | endpoint_id=svc.graph.intra catalog_page_id=svc.graph 组合=PRT-04；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000543 | 图谱 | 服务机构实体与关系 | 异常-非法scope | B 关系边上图 SVC_RE_SVC_SVC | 服务机构实体与关系 | B 关系边上图 SVC_RE_SVC_SVC | 机构间关系接口 scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/intra，请求体取组合 PRT-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/intra |  | INTEG |  |  | endpoint_id=svc.graph.intra catalog_page_id=svc.graph 组合=PRT-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000544 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 产业 SVC_RE_INDUSTRY | 服务机构实体与关系 | C 产业 SVC_RE_INDUSTRY | catalog 不可用态下C 产业 SVC_RE_INDUSTRY挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 IND-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-industry catalog_page_id=svc.graph 组合=IND-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000545 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 产业 SVC_RE_INDUSTRY | 服务机构实体与关系 | C 产业 SVC_RE_INDUSTRY | C 产业 SVC_RE_INDUSTRY缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 IND-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-industry catalog_page_id=svc.graph 组合=IND-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000546 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 产业 SVC_RE_INDUSTRY | 服务机构实体与关系 | C 产业 SVC_RE_INDUSTRY | C 产业 SVC_RE_INDUSTRY缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 IND-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-industry catalog_page_id=svc.graph 组合=IND-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000547 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 产业 SVC_RE_INDUSTRY | 服务机构实体与关系 | C 产业 SVC_RE_INDUSTRY | C 产业 SVC_RE_INDUSTRY scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 IND-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-industry catalog_page_id=svc.graph 组合=IND-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000548 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 产业 SVC_RE_INDUSTRY | 服务机构实体与关系 | C 产业 SVC_RE_INDUSTRY | C 产业 SVC_RE_INDUSTRY scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 IND-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-industry catalog_page_id=svc.graph 组合=IND-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000549 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 技术 SVC_RE_TECH | 服务机构实体与关系 | C 技术 SVC_RE_TECH | catalog 不可用态下C 技术 SVC_RE_TECH挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TEC-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-tech catalog_page_id=svc.graph 组合=TEC-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000550 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 技术 SVC_RE_TECH | 服务机构实体与关系 | C 技术 SVC_RE_TECH | C 技术 SVC_RE_TECH缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TEC-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-tech catalog_page_id=svc.graph 组合=TEC-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000551 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 技术 SVC_RE_TECH | 服务机构实体与关系 | C 技术 SVC_RE_TECH | C 技术 SVC_RE_TECH缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TEC-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-tech catalog_page_id=svc.graph 组合=TEC-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000552 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 技术 SVC_RE_TECH | 服务机构实体与关系 | C 技术 SVC_RE_TECH | C 技术 SVC_RE_TECH scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TEC-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-tech catalog_page_id=svc.graph 组合=TEC-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000553 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 技术 SVC_RE_TECH | 服务机构实体与关系 | C 技术 SVC_RE_TECH | C 技术 SVC_RE_TECH scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TEC-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-tech catalog_page_id=svc.graph 组合=TEC-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000554 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 企业 SVC_RE_ENTERPRISE | 服务机构实体与关系 | C 企业 SVC_RE_ENTERPRISE | catalog 不可用态下C 企业 SVC_RE_ENTERPRISE挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 ENT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-enterprise catalog_page_id=svc.graph 组合=ENT-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000555 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 企业 SVC_RE_ENTERPRISE | 服务机构实体与关系 | C 企业 SVC_RE_ENTERPRISE | C 企业 SVC_RE_ENTERPRISE缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 ENT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-enterprise catalog_page_id=svc.graph 组合=ENT-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000556 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 企业 SVC_RE_ENTERPRISE | 服务机构实体与关系 | C 企业 SVC_RE_ENTERPRISE | C 企业 SVC_RE_ENTERPRISE缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 ENT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-enterprise catalog_page_id=svc.graph 组合=ENT-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000557 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 企业 SVC_RE_ENTERPRISE | 服务机构实体与关系 | C 企业 SVC_RE_ENTERPRISE | C 企业 SVC_RE_ENTERPRISE scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 ENT-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-enterprise catalog_page_id=svc.graph 组合=ENT-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000558 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 企业 SVC_RE_ENTERPRISE | 服务机构实体与关系 | C 企业 SVC_RE_ENTERPRISE | C 企业 SVC_RE_ENTERPRISE scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 ENT-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-enterprise catalog_page_id=svc.graph 组合=ENT-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000559 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 政府 SVC_RE_GOV | 服务机构实体与关系 | C 政府 SVC_RE_GOV | catalog 不可用态下C 政府 SVC_RE_GOV挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 GOV-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-gov catalog_page_id=svc.graph 组合=GOV-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000560 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 政府 SVC_RE_GOV | 服务机构实体与关系 | C 政府 SVC_RE_GOV | C 政府 SVC_RE_GOV缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 GOV-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-gov catalog_page_id=svc.graph 组合=GOV-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000561 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 政府 SVC_RE_GOV | 服务机构实体与关系 | C 政府 SVC_RE_GOV | C 政府 SVC_RE_GOV缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 GOV-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-gov catalog_page_id=svc.graph 组合=GOV-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000562 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 政府 SVC_RE_GOV | 服务机构实体与关系 | C 政府 SVC_RE_GOV | C 政府 SVC_RE_GOV scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 GOV-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-gov catalog_page_id=svc.graph 组合=GOV-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000563 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 政府 SVC_RE_GOV | 服务机构实体与关系 | C 政府 SVC_RE_GOV | C 政府 SVC_RE_GOV scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 GOV-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-gov catalog_page_id=svc.graph 组合=GOV-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000564 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 人才 SVC_RE_TALENT | 服务机构实体与关系 | C 人才 SVC_RE_TALENT | catalog 不可用态下C 人才 SVC_RE_TALENT挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TAL-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-talent catalog_page_id=svc.graph 组合=TAL-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000565 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 人才 SVC_RE_TALENT | 服务机构实体与关系 | C 人才 SVC_RE_TALENT | C 人才 SVC_RE_TALENT缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TAL-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-talent catalog_page_id=svc.graph 组合=TAL-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000566 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 人才 SVC_RE_TALENT | 服务机构实体与关系 | C 人才 SVC_RE_TALENT | C 人才 SVC_RE_TALENT缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TAL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-talent catalog_page_id=svc.graph 组合=TAL-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000567 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 人才 SVC_RE_TALENT | 服务机构实体与关系 | C 人才 SVC_RE_TALENT | C 人才 SVC_RE_TALENT scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TAL-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-talent catalog_page_id=svc.graph 组合=TAL-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000568 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 人才 SVC_RE_TALENT | 服务机构实体与关系 | C 人才 SVC_RE_TALENT | C 人才 SVC_RE_TALENT scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 TAL-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-talent catalog_page_id=svc.graph 组合=TAL-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000569 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 政策 SVC_RE_POLICY | 服务机构实体与关系 | C 政策 SVC_RE_POLICY | catalog 不可用态下C 政策 SVC_RE_POLICY挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 POL-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-policy catalog_page_id=svc.graph 组合=POL-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000570 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 政策 SVC_RE_POLICY | 服务机构实体与关系 | C 政策 SVC_RE_POLICY | C 政策 SVC_RE_POLICY缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 POL-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-policy catalog_page_id=svc.graph 组合=POL-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000571 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 政策 SVC_RE_POLICY | 服务机构实体与关系 | C 政策 SVC_RE_POLICY | C 政策 SVC_RE_POLICY缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 POL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-policy catalog_page_id=svc.graph 组合=POL-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000572 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 政策 SVC_RE_POLICY | 服务机构实体与关系 | C 政策 SVC_RE_POLICY | C 政策 SVC_RE_POLICY scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 POL-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-policy catalog_page_id=svc.graph 组合=POL-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000573 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 政策 SVC_RE_POLICY | 服务机构实体与关系 | C 政策 SVC_RE_POLICY | C 政策 SVC_RE_POLICY scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 POL-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-policy catalog_page_id=svc.graph 组合=POL-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000574 | 图谱 | 服务机构实体与关系 | 契约-不可用 | C 科研 SVC_RE_RESEARCH | 服务机构实体与关系 | C 科研 SVC_RE_RESEARCH | catalog 不可用态下C 科研 SVC_RE_RESEARCH挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 RES-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-research catalog_page_id=svc.graph 组合=RES-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000575 | 图谱 | 服务机构实体与关系 | 异常-缺必填op_id | C 科研 SVC_RE_RESEARCH | 服务机构实体与关系 | C 科研 SVC_RE_RESEARCH | C 科研 SVC_RE_RESEARCH缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 RES-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-research catalog_page_id=svc.graph 组合=RES-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000576 | 图谱 | 服务机构实体与关系 | 异常-缺必填scope | C 科研 SVC_RE_RESEARCH | 服务机构实体与关系 | C 科研 SVC_RE_RESEARCH | C 科研 SVC_RE_RESEARCH缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 RES-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-research catalog_page_id=svc.graph 组合=RES-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000577 | 图谱 | 服务机构实体与关系 | 异常-非法scope | C 科研 SVC_RE_RESEARCH | 服务机构实体与关系 | C 科研 SVC_RE_RESEARCH | C 科研 SVC_RE_RESEARCH scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 RES-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-research catalog_page_id=svc.graph 组合=RES-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000578 | 图谱 | 服务机构实体与关系 | 异常-scope=one缺id | C 科研 SVC_RE_RESEARCH | 服务机构实体与关系 | C 科研 SVC_RE_RESEARCH | C 科研 SVC_RE_RESEARCH scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/svc/graph/hang，请求体取组合 RES-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph/hang |  | INTEG |  |  | endpoint_id=svc.graph.hang-research catalog_page_id=svc.graph 组合=RES-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000579 | 图谱 | 服务机构实体与关系 | 契约-不可用 | D 浏览 SVC_GRAPH_BROWSE | 服务机构实体与关系 | D 浏览 SVC_GRAPH_BROWSE | catalog 不可用态下产业服务图谱浏览接口返回可识别非成功契约信封 | 1、已确认 catalog `svc.graph.main` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/svc/graph，查询参数取组合 MAIN-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 nodes/edges 与 string 型 source 的成功业务载荷；4、不得将 sampleResponse 节点权重示例作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  |  | endpoint_id=svc.graph.main catalog_page_id=svc.graph 组合=MAIN-01 catalog_status=unavailable；鉴权同 API-000535 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000580 | 图谱 | 服务机构实体与关系 | 异常-非法hops | D 浏览 SVC_GRAPH_BROWSE | 服务机构实体与关系 | D 浏览 SVC_GRAPH_BROWSE | 图谱浏览接口 hops 非整数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/svc/graph，查询参数取组合 MAIN-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作含可信 nodes 的成功数据 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  |  | endpoint_id=svc.graph.main catalog_page_id=svc.graph 组合=MAIN-02；矩阵挂 hops、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000581 | 图谱 | 服务机构实体与关系 | 异常-limit越界 | D 浏览 SVC_GRAPH_BROWSE | 服务机构实体与关系 | D 浏览 SVC_GRAPH_BROWSE | 图谱浏览接口 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/svc/graph，查询参数取组合 MAIN-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  |  | endpoint_id=svc.graph.main catalog_page_id=svc.graph 组合=MAIN-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000582 | 图谱 | 服务机构实体与关系 | 异常-非法center | D 浏览 SVC_GRAPH_BROWSE | 服务机构实体与关系 | D 浏览 SVC_GRAPH_BROWSE | 图谱浏览接口 center 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/svc/graph，查询参数取组合 MAIN-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 center 当作空图成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  |  | endpoint_id=svc.graph.main catalog_page_id=svc.graph 组合=MAIN-04；矩阵挂 center、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000583 | 图谱 | 服务机构实体与关系 | 备选-多参数 | D 浏览 SVC_GRAPH_BROWSE | 服务机构实体与关系 | D 浏览 SVC_GRAPH_BROWSE | 图谱浏览接口带 center/hops/limit 组合时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000534 | 1.GET /entan/v1/svc/graph，查询参数取组合 MAIN-05 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体含可解析 code；3、禁止将 sample 节点条数作为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/graph |  | INTEG |  |  | endpoint_id=svc.graph.main catalog_page_id=svc.graph 组合=MAIN-05 |
---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| NER-01 | svc.graph.ner | op_id=SVC_NER_ORG；scope=batch；filter={"all":true}；mode=rule；dry_run=true（catalog sampleRequest，执行期可替换） | unavailable 契约占位 |
| NER-02 | svc.graph.ner | 不含 op_id；scope=batch；dry_run=true | 缺必填 op_id |
| NER-03 | svc.graph.ner | op_id=SVC_NER_ORG；不含 scope | 缺必填 scope |
| NER-04 | svc.graph.ner | op_id=SVC_NER_ORG；scope=__invalid__；dry_run=true | 非法 scope |
| PRT-01 | svc.graph.intra | op_id=SVC_RE_SVC_SVC；scope=batch；filter={"all":true}；relation_whitelist=["participates"]；mode=rule；dry_run=true | unavailable 契约占位 |
| PRT-02 | svc.graph.intra | 不含 op_id；scope=batch；relation_whitelist=["participates"] | 缺 op_id |
| PRT-03 | svc.graph.intra | op_id=SVC_RE_SVC_SVC；不含 scope；relation_whitelist=["participates"] | 缺 scope |
| PRT-04 | svc.graph.intra | op_id=SVC_RE_SVC_SVC；scope=one；不含 relation_whitelist | 缺 relation_whitelist |
| PRT-05 | svc.graph.intra | op_id=SVC_RE_SVC_SVC；scope=__invalid__；relation_whitelist=["participates"] | 非法 scope |
| IND-01 | svc.graph.hang-industry | op_id=SVC_RE_INDUSTRY；scope=one；id=ORG1；dest_types=["industry"]；mode=rule；dry_run=true | unavailable 契约占位 |
| IND-02 | svc.graph.hang-industry | 不含 op_id；scope=one；dest_types=["industry"] | 缺 op_id |
| IND-03 | svc.graph.hang-industry | op_id=SVC_RE_INDUSTRY；不含 scope；dest_types=["industry"] | 缺 scope |
| IND-04 | svc.graph.hang-industry | op_id=SVC_RE_INDUSTRY；scope=__invalid__；dest_types=["industry"] | 非法 scope |
| IND-05 | svc.graph.hang-industry | op_id=SVC_RE_INDUSTRY；scope=one；不含 id；dry_run=true；dest_types=["industry"] | scope=one 缺 id |
| TEC-01 | svc.graph.hang-tech | op_id=SVC_RE_TECH；scope=one；id=ORG1；dest_types=["tech"]；mode=rule；dry_run=true | unavailable 契约占位 |
| TEC-02 | svc.graph.hang-tech | 不含 op_id；scope=one；dest_types=["tech"] | 缺 op_id |
| TEC-03 | svc.graph.hang-tech | op_id=SVC_RE_TECH；不含 scope；dest_types=["tech"] | 缺 scope |
| TEC-04 | svc.graph.hang-tech | op_id=SVC_RE_TECH；scope=__invalid__；dest_types=["tech"] | 非法 scope |
| TEC-05 | svc.graph.hang-tech | op_id=SVC_RE_TECH；scope=one；不含 id；dry_run=true；dest_types=["tech"] | scope=one 缺 id |
| ENT-01 | svc.graph.hang-enterprise | op_id=SVC_RE_ENTERPRISE；scope=one；id=ORG1；dest_types=["enterprise"]；mode=rule；dry_run=true | unavailable 契约占位 |
| ENT-02 | svc.graph.hang-enterprise | 不含 op_id；scope=one；dest_types=["enterprise"] | 缺 op_id |
| ENT-03 | svc.graph.hang-enterprise | op_id=SVC_RE_ENTERPRISE；不含 scope；dest_types=["enterprise"] | 缺 scope |
| ENT-04 | svc.graph.hang-enterprise | op_id=SVC_RE_ENTERPRISE；scope=__invalid__；dest_types=["enterprise"] | 非法 scope |
| ENT-05 | svc.graph.hang-enterprise | op_id=SVC_RE_ENTERPRISE；scope=one；不含 id；dry_run=true；dest_types=["enterprise"] | scope=one 缺 id |
| GOV-01 | svc.graph.hang-gov | op_id=SVC_RE_GOV；scope=one；id=ORG1；dest_types=["gov"]；mode=rule；dry_run=true | unavailable 契约占位 |
| GOV-02 | svc.graph.hang-gov | 不含 op_id；scope=one；dest_types=["gov"] | 缺 op_id |
| GOV-03 | svc.graph.hang-gov | op_id=SVC_RE_GOV；不含 scope；dest_types=["gov"] | 缺 scope |
| GOV-04 | svc.graph.hang-gov | op_id=SVC_RE_GOV；scope=__invalid__；dest_types=["gov"] | 非法 scope |
| GOV-05 | svc.graph.hang-gov | op_id=SVC_RE_GOV；scope=one；不含 id；dry_run=true；dest_types=["gov"] | scope=one 缺 id |
| TAL-01 | svc.graph.hang-talent | op_id=SVC_RE_TALENT；scope=one；id=ORG1；dest_types=["talent"]；mode=rule；dry_run=true | unavailable 契约占位 |
| TAL-02 | svc.graph.hang-talent | 不含 op_id；scope=one；dest_types=["talent"] | 缺 op_id |
| TAL-03 | svc.graph.hang-talent | op_id=SVC_RE_TALENT；不含 scope；dest_types=["talent"] | 缺 scope |
| TAL-04 | svc.graph.hang-talent | op_id=SVC_RE_TALENT；scope=__invalid__；dest_types=["talent"] | 非法 scope |
| TAL-05 | svc.graph.hang-talent | op_id=SVC_RE_TALENT；scope=one；不含 id；dry_run=true；dest_types=["talent"] | scope=one 缺 id |
| POL-01 | svc.graph.hang-policy | op_id=SVC_RE_POLICY；scope=one；id=ORG1；dest_types=["policy"]；mode=rule；dry_run=true | unavailable 契约占位 |
| POL-02 | svc.graph.hang-policy | 不含 op_id；scope=one；dest_types=["policy"] | 缺 op_id |
| POL-03 | svc.graph.hang-policy | op_id=SVC_RE_POLICY；不含 scope；dest_types=["policy"] | 缺 scope |
| POL-04 | svc.graph.hang-policy | op_id=SVC_RE_POLICY；scope=__invalid__；dest_types=["policy"] | 非法 scope |
| POL-05 | svc.graph.hang-policy | op_id=SVC_RE_POLICY；scope=one；不含 id；dry_run=true；dest_types=["policy"] | scope=one 缺 id |
| RES-01 | svc.graph.hang-research | op_id=SVC_RE_RESEARCH；scope=one；id=ORG1；dest_types=["research"]；mode=rule；dry_run=true | unavailable 契约占位 |
| RES-02 | svc.graph.hang-research | 不含 op_id；scope=one；dest_types=["research"] | 缺 op_id |
| RES-03 | svc.graph.hang-research | op_id=SVC_RE_RESEARCH；不含 scope；dest_types=["research"] | 缺 scope |
| RES-04 | svc.graph.hang-research | op_id=SVC_RE_RESEARCH；scope=__invalid__；dest_types=["research"] | 非法 scope |
| RES-05 | svc.graph.hang-research | op_id=SVC_RE_RESEARCH；scope=one；不含 id；dry_run=true；dest_types=["research"] | scope=one 缺 id |
| MAIN-01 | svc.graph.main | q=；center=；hops=1；limit=200（catalog sampleRequest，执行期可替换） | unavailable 契约占位 |
| MAIN-02 | svc.graph.main | hops=not_int；limit=200 | 非法 hops 类型 |
| MAIN-03 | svc.graph.main | hops=1；limit=-1 | limit 越界 |
| MAIN-04 | svc.graph.main | center=__invalid__；hops=1；limit=200 | 非法 center |
| MAIN-05 | svc.graph.main | center=institution:ORG1；hops=2；limit=20 | 多参数组合 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| svc.graph.ner | POST | /entan/v1/svc/graph/ner | unavailable | op_id、scope（body） |
| svc.graph.intra | POST | /entan/v1/svc/graph/intra | unavailable | op_id、scope、relation_whitelist |
| svc.graph.hang-industry | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.hang-tech | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.hang-enterprise | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.hang-gov | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.hang-talent | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.hang-policy | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.hang-research | POST | /entan/v1/svc/graph/hang | unavailable | op_id、scope |
| svc.graph.main | GET | /entan/v1/svc/graph | unavailable | （无；q/center/hops/limit 均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.graph.ner | API-000534, API-000535, API-000536, API-000537, API-000538 |
| svc.graph.intra | API-000539, API-000540, API-000541, API-000542, API-000543 |
| svc.graph.hang-industry | API-000544, API-000545, API-000546, API-000547, API-000548 |
| svc.graph.hang-tech | API-000549, API-000550, API-000551, API-000552, API-000553 |
| svc.graph.hang-enterprise | API-000554, API-000555, API-000556, API-000557, API-000558 |
| svc.graph.hang-gov | API-000559, API-000560, API-000561, API-000562, API-000563 |
| svc.graph.hang-talent | API-000564, API-000565, API-000566, API-000567, API-000568 |
| svc.graph.hang-policy | API-000569, API-000570, API-000571, API-000572, API-000573 |
| svc.graph.hang-research | API-000574, API-000575, API-000576, API-000577, API-000578 |
| svc.graph.main | API-000579, API-000580, API-000581, API-000582, API-000583 |

---

## 3. 覆盖自检

- [x] 10 个 unavailable endpoint 均已写契约占位（每 endpoint 首条）
- [x] POST 类必填 op_id/scope（及 intra 的 relation_whitelist）缺省已覆盖
- [x] 异常-鉴权全页 1 条（API-000535，其余 endpoint 备注「鉴权同 API-000535」）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（未试调，无稳定必空构造）
- [x] 金样 1 条且断言完整信封（API-000534）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新（L11+L12）
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

**统计**：用例 **50** 条；编号 **API-000534**～**API-000583**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **50**（000534～000583） |
| catalog endpoint 数 | **10** |
| 金样（完整信封） | **1**（API-000534） |
| 异常-鉴权 | **1**（API-000535） |
| live 主路径 | **0**（全页 unavailable） |
| `_empty`（L11+L12） | **10** 行 **未覆盖** |
| code-registry 回写 | **父控**（本子任务未改） |
