# 智能服务集群-科技专题服务算法库测试用例（政策实体与关系 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 政策实体与关系  
> **catalog**：`entry_id=policy.graph` · `catalog_page_id=policy.graph` · path `/policy/graph`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.graph`（6 endpoints）  
> **A 线对照**：`fp-split-by-api-run/work/L07.md`（ner/main）· `L08.md`（intra/hang 关系类）  
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
| 断言分工 | **API-000419（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-000419」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **6** 个 endpoint 均为 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 written_nodes/written_edges/nodes/edges 示例数值、vid、权重作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl / 浏览器；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST 写入类为 JSON body；GET 浏览类为查询参数；组合见附录 A |
| 样例与契约差 | 样例顶层字段常多于 `responseFields`；断言 **仅强制** catalog `responseFields` |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.graph`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000419 | 图谱 | 政策实体与关系 | 契约-不可用 | A 实体识别 POLICY_NER_POLICY | 政策实体与关系 | A 实体识别 POLICY_NER_POLICY | catalog 不可用态下实体识别接口返回可识别非成功契约信封 | 1、已确认 catalog `policy.graph.ner` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.POST /policy/v1/policy/graph/ner，请求体取组合 NER-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 written_nodes/skipped 与 string 型 space 的成功业务载荷；4、不得将 sampleResponse 写入点示例作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/ner |  | INTEG |  |  | endpoint_id=policy.graph.ner catalog_page_id=policy.graph 组合=NER-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000420 | 图谱 | 政策实体与关系 | 异常-鉴权 | A 实体识别 POLICY_NER_POLICY | 政策实体与关系 | A 实体识别 POLICY_NER_POLICY | 实体识别接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /policy/v1/policy/graph/ner，请求体取组合 NER-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务图谱写入载荷） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/ner |  | INTEG |  |  | endpoint_id=policy.graph.ner catalog_page_id=policy.graph 组合=NER-01；全页鉴权代表 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000421 | 图谱 | 政策实体与关系 | 异常-缺必填op_id | A 实体识别 POLICY_NER_POLICY | 政策实体与关系 | A 实体识别 POLICY_NER_POLICY | 实体识别接口缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000419 | 1.POST /policy/v1/policy/graph/ner，请求体取组合 NER-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 written_nodes 冒充 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/ner |  | INTEG |  |  | endpoint_id=policy.graph.ner catalog_page_id=policy.graph 组合=NER-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000422 | 图谱 | 政策实体与关系 | 异常-缺必填scope | A 实体识别 POLICY_NER_POLICY | 政策实体与关系 | A 实体识别 POLICY_NER_POLICY | 实体识别接口缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/ner，请求体取组合 NER-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/ner |  | INTEG |  |  | endpoint_id=policy.graph.ner catalog_page_id=policy.graph 组合=NER-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000423 | 图谱 | 政策实体与关系 | 异常-非法scope | A 实体识别 POLICY_NER_POLICY | 政策实体与关系 | A 实体识别 POLICY_NER_POLICY | 实体识别接口 scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/ner，请求体取组合 NER-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/ner |  | INTEG |  |  | endpoint_id=policy.graph.ner catalog_page_id=policy.graph 组合=NER-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000424 | 图谱 | 政策实体与关系 | 契约-不可用 | B 关系边上图 POLICY_RE_CITE | 政策实体与关系 | B 关系边上图 POLICY_RE_CITE | catalog 不可用态下引用关系接口返回可识别非成功契约信封 | 1、已确认 catalog `policy.graph.intra` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/intra，请求体取组合 CITE-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 written_edges/skipped 的成功业务载荷；4、禁止 sampleResponse 边示例作通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/intra |  | INTEG |  |  | endpoint_id=policy.graph.intra catalog_page_id=policy.graph 组合=CITE-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000425 | 图谱 | 政策实体与关系 | 异常-缺必填op_id | B 关系边上图 POLICY_RE_CITE | 政策实体与关系 | B 关系边上图 POLICY_RE_CITE | 引用关系接口缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000419 | 1.POST /policy/v1/policy/graph/intra，请求体取组合 CITE-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/intra |  | INTEG |  |  | endpoint_id=policy.graph.intra catalog_page_id=policy.graph 组合=CITE-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000426 | 图谱 | 政策实体与关系 | 异常-缺必填scope | B 关系边上图 POLICY_RE_CITE | 政策实体与关系 | B 关系边上图 POLICY_RE_CITE | 引用关系接口缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/intra，请求体取组合 CITE-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/intra |  | INTEG |  |  | endpoint_id=policy.graph.intra catalog_page_id=policy.graph 组合=CITE-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000427 | 图谱 | 政策实体与关系 | 异常-缺必填relation_whitelist | B 关系边上图 POLICY_RE_CITE | 政策实体与关系 | B 关系边上图 POLICY_RE_CITE | 引用关系接口缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/intra，请求体取组合 CITE-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/intra |  | INTEG |  |  | endpoint_id=policy.graph.intra catalog_page_id=policy.graph 组合=CITE-04；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000428 | 图谱 | 政策实体与关系 | 异常-非法scope | B 关系边上图 POLICY_RE_CITE | 政策实体与关系 | B 关系边上图 POLICY_RE_CITE | 引用关系接口 scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/intra，请求体取组合 CITE-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/intra |  | INTEG |  |  | endpoint_id=policy.graph.intra catalog_page_id=policy.graph 组合=CITE-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000429 | 图谱 | 政策实体与关系 | 契约-不可用 | C 扶持 POLICY_RE_SUPPORT | 政策实体与关系 | C 扶持 POLICY_RE_SUPPORT | catalog 不可用态下扶持挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 SUP-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-support catalog_page_id=policy.graph 组合=SUP-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000430 | 图谱 | 政策实体与关系 | 异常-缺必填op_id | C 扶持 POLICY_RE_SUPPORT | 政策实体与关系 | C 扶持 POLICY_RE_SUPPORT | C 扶持 POLICY_RE_SUPPORT缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000419 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 SUP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-support catalog_page_id=policy.graph 组合=SUP-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000431 | 图谱 | 政策实体与关系 | 异常-缺必填scope | C 扶持 POLICY_RE_SUPPORT | 政策实体与关系 | C 扶持 POLICY_RE_SUPPORT | C 扶持 POLICY_RE_SUPPORT缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 SUP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-support catalog_page_id=policy.graph 组合=SUP-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000432 | 图谱 | 政策实体与关系 | 异常-非法scope | C 扶持 POLICY_RE_SUPPORT | 政策实体与关系 | C 扶持 POLICY_RE_SUPPORT | C 扶持 POLICY_RE_SUPPORT scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 SUP-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-support catalog_page_id=policy.graph 组合=SUP-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000433 | 图谱 | 政策实体与关系 | 异常-scope=one缺id | C 扶持 POLICY_RE_SUPPORT | 政策实体与关系 | C 扶持 POLICY_RE_SUPPORT | C 扶持 POLICY_RE_SUPPORT scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 SUP-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-support catalog_page_id=policy.graph 组合=SUP-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000434 | 图谱 | 政策实体与关系 | 契约-不可用 | C 适用 POLICY_RE_APPLY_TO | 政策实体与关系 | C 适用 POLICY_RE_APPLY_TO | catalog 不可用态下适用挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 APL-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-apply catalog_page_id=policy.graph 组合=APL-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000435 | 图谱 | 政策实体与关系 | 异常-缺必填op_id | C 适用 POLICY_RE_APPLY_TO | 政策实体与关系 | C 适用 POLICY_RE_APPLY_TO | C 适用 POLICY_RE_APPLY_TO缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000419 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 APL-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-apply catalog_page_id=policy.graph 组合=APL-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000436 | 图谱 | 政策实体与关系 | 异常-缺必填scope | C 适用 POLICY_RE_APPLY_TO | 政策实体与关系 | C 适用 POLICY_RE_APPLY_TO | C 适用 POLICY_RE_APPLY_TO缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 APL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-apply catalog_page_id=policy.graph 组合=APL-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000437 | 图谱 | 政策实体与关系 | 异常-非法scope | C 适用 POLICY_RE_APPLY_TO | 政策实体与关系 | C 适用 POLICY_RE_APPLY_TO | C 适用 POLICY_RE_APPLY_TO scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 APL-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-apply catalog_page_id=policy.graph 组合=APL-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000438 | 图谱 | 政策实体与关系 | 异常-scope=one缺id | C 适用 POLICY_RE_APPLY_TO | 政策实体与关系 | C 适用 POLICY_RE_APPLY_TO | C 适用 POLICY_RE_APPLY_TO scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 APL-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-apply catalog_page_id=policy.graph 组合=APL-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000439 | 图谱 | 政策实体与关系 | 契约-不可用 | C 监管 POLICY_RE_REGULATE | 政策实体与关系 | C 监管 POLICY_RE_REGULATE | catalog 不可用态下监管挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 REG-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-regulate catalog_page_id=policy.graph 组合=REG-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000440 | 图谱 | 政策实体与关系 | 异常-缺必填op_id | C 监管 POLICY_RE_REGULATE | 政策实体与关系 | C 监管 POLICY_RE_REGULATE | C 监管 POLICY_RE_REGULATE缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000419 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 REG-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-regulate catalog_page_id=policy.graph 组合=REG-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000441 | 图谱 | 政策实体与关系 | 异常-缺必填scope | C 监管 POLICY_RE_REGULATE | 政策实体与关系 | C 监管 POLICY_RE_REGULATE | C 监管 POLICY_RE_REGULATE缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 REG-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-regulate catalog_page_id=policy.graph 组合=REG-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000442 | 图谱 | 政策实体与关系 | 异常-非法scope | C 监管 POLICY_RE_REGULATE | 政策实体与关系 | C 监管 POLICY_RE_REGULATE | C 监管 POLICY_RE_REGULATE scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 REG-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-regulate catalog_page_id=policy.graph 组合=REG-04；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000443 | 图谱 | 政策实体与关系 | 异常-scope=one缺id | C 监管 POLICY_RE_REGULATE | 政策实体与关系 | C 监管 POLICY_RE_REGULATE | C 监管 POLICY_RE_REGULATE scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /policy/v1/policy/graph/hang，请求体取组合 REG-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph/hang |  | INTEG |  |  | endpoint_id=policy.graph.hang-regulate catalog_page_id=policy.graph 组合=REG-05；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000444 | 图谱 | 政策实体与关系 | 契约-不可用 | D 浏览 POLICY_GRAPH_BROWSE | 政策实体与关系 | D 浏览 POLICY_GRAPH_BROWSE | catalog 不可用态下政策图谱浏览接口返回可识别非成功契约信封 | 1、已确认 catalog `policy.graph.main` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/graph，查询参数取组合 MAIN-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 nodes/edges 与 string 型 source 的成功业务载荷；4、不得将 sampleResponse 节点权重示例作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph |  | INTEG |  |  | endpoint_id=policy.graph.main catalog_page_id=policy.graph 组合=MAIN-01 catalog_status=unavailable；鉴权同 API-000420 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000445 | 图谱 | 政策实体与关系 | 异常-非法steps | D 浏览 POLICY_GRAPH_BROWSE | 政策实体与关系 | D 浏览 POLICY_GRAPH_BROWSE | 图谱浏览接口 steps 非整数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/graph，查询参数取组合 MAIN-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作含可信 nodes 的成功数据 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph |  | INTEG |  |  | endpoint_id=policy.graph.main catalog_page_id=policy.graph 组合=MAIN-02；矩阵挂 steps、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000446 | 图谱 | 政策实体与关系 | 异常-limit越界 | D 浏览 POLICY_GRAPH_BROWSE | 政策实体与关系 | D 浏览 POLICY_GRAPH_BROWSE | 图谱浏览接口 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/graph，查询参数取组合 MAIN-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph |  | INTEG |  |  | endpoint_id=policy.graph.main catalog_page_id=policy.graph 组合=MAIN-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000447 | 图谱 | 政策实体与关系 | 异常-非法center | D 浏览 POLICY_GRAPH_BROWSE | 政策实体与关系 | D 浏览 POLICY_GRAPH_BROWSE | 图谱浏览接口 center 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/graph，查询参数取组合 MAIN-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 center 当作空图成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph |  | INTEG |  |  | endpoint_id=policy.graph.main catalog_page_id=policy.graph 组合=MAIN-04；矩阵挂 center、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000448 | 图谱 | 政策实体与关系 | 备选-多参数 | D 浏览 POLICY_GRAPH_BROWSE | 政策实体与关系 | D 浏览 POLICY_GRAPH_BROWSE | 图谱浏览接口带 center/steps/limit 组合时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000419 | 1.GET /policy/v1/policy/graph，查询参数取组合 MAIN-05 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体含可解析 code；3、禁止将 sample 节点条数作为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/graph |  | INTEG |  |  | endpoint_id=policy.graph.main catalog_page_id=policy.graph 组合=MAIN-05 |
---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| NER-01 | policy.graph.ner | op_id=POLICY_NER_POLICY；scope=one；id=POLA；mode=rule；dry_run=true（catalog sampleRequest，执行期可替换） | unavailable 契约占位 |
| NER-02 | policy.graph.ner | 不含 op_id；scope=one；id=POLA；dry_run=true | 缺必填 op_id |
| NER-03 | policy.graph.ner | op_id=POLICY_NER_POLICY；不含 scope；id=POLA | 缺必填 scope |
| NER-04 | policy.graph.ner | op_id=POLICY_NER_POLICY；scope=__invalid__；id=POLA | 非法 scope |
| CITE-01 | policy.graph.intra | op_id=POLICY_RE_CITE；scope=batch；filter={"policy_ids":["POLA","POLB"]}；relation_whitelist=["cite"]；mode=rule；dry_run=true | unavailable 契约占位 |
| CITE-02 | policy.graph.intra | 不含 op_id；scope=one；relation_whitelist=["cite"] | 缺 op_id |
| CITE-03 | policy.graph.intra | op_id=POLICY_RE_CITE；不含 scope；relation_whitelist=["cite"] | 缺 scope |
| CITE-04 | policy.graph.intra | op_id=POLICY_RE_CITE；scope=one；不含 relation_whitelist | 缺 relation_whitelist |
| CITE-05 | policy.graph.intra | op_id=POLICY_RE_CITE；scope=__invalid__；relation_whitelist=["cite"] | 非法 scope |
| SUP-01 | policy.graph.hang-support | op_id=POLICY_RE_SUPPORT；scope=one；id=POLA；mode=rule；relation_whitelist=["support"]；dry_run=true | unavailable 契约占位 |
| SUP-02 | policy.graph.hang-support | 不含 op_id；scope=one；relation_whitelist=["support"] | 缺 op_id |
| SUP-03 | policy.graph.hang-support | op_id=POLICY_RE_SUPPORT；不含 scope；relation_whitelist=["support"] | 缺 scope |
| SUP-04 | policy.graph.hang-support | op_id=POLICY_RE_SUPPORT；scope=__invalid__；relation_whitelist=["support"] | 非法 scope |
| SUP-05 | policy.graph.hang-support | op_id=POLICY_RE_SUPPORT；scope=one；不含 id；dry_run=true；relation_whitelist=["support"] | scope=one 缺 id |
| APL-01 | policy.graph.hang-apply | op_id=POLICY_RE_APPLY_TO；scope=one；id=POLA；relation_whitelist=["apply_to"]；mode=rule；dry_run=true | unavailable 契约占位 |
| APL-02 | policy.graph.hang-apply | 不含 op_id；scope=one；relation_whitelist=["apply_to"] | 缺 op_id |
| APL-03 | policy.graph.hang-apply | op_id=POLICY_RE_APPLY_TO；不含 scope；relation_whitelist=["apply_to"] | 缺 scope |
| APL-04 | policy.graph.hang-apply | op_id=POLICY_RE_APPLY_TO；scope=__invalid__；relation_whitelist=["apply_to"] | 非法 scope |
| APL-05 | policy.graph.hang-apply | op_id=POLICY_RE_APPLY_TO；scope=one；不含 id；relation_whitelist=["apply_to"] | scope=one 缺 id |
| REG-01 | policy.graph.hang-regulate | op_id=POLICY_RE_REGULATE；scope=one；id=POLA；mode=rule；relation_whitelist=["regulate"]；dry_run=true | unavailable 契约占位 |
| REG-02 | policy.graph.hang-regulate | 不含 op_id；scope=one；relation_whitelist=["regulate"] | 缺 op_id |
| REG-03 | policy.graph.hang-regulate | op_id=POLICY_RE_REGULATE；不含 scope；relation_whitelist=["regulate"] | 缺 scope |
| REG-04 | policy.graph.hang-regulate | op_id=POLICY_RE_REGULATE；scope=__invalid__；relation_whitelist=["regulate"] | 非法 scope |
| REG-05 | policy.graph.hang-regulate | op_id=POLICY_RE_REGULATE；scope=one；不含 id；relation_whitelist=["regulate"] | scope=one 缺 id |
| MAIN-01 | policy.graph.main | center=pol:POLA；steps=1；limit=40（catalog sampleRequest，执行期可替换） | unavailable 契约占位 |
| MAIN-02 | policy.graph.main | center=pol:POLA；steps=not_int；limit=40 | 非法 steps 类型 |
| MAIN-03 | policy.graph.main | center=pol:POLA；steps=1；limit=-1 | limit 越界 |
| MAIN-04 | policy.graph.main | center=__invalid__；steps=1；limit=40 | 非法 center |
| MAIN-05 | policy.graph.main | center=pol:POLA；steps=2；limit=20 | 多参数组合 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| policy.graph.ner | POST | /policy/v1/policy/graph/ner | unavailable | op_id、scope（body） |
| policy.graph.intra | POST | /policy/v1/policy/graph/intra | unavailable | op_id、scope、relation_whitelist |
| policy.graph.hang-support | POST | /policy/v1/policy/graph/hang | unavailable | op_id、scope |
| policy.graph.hang-apply | POST | /policy/v1/policy/graph/hang | unavailable | op_id、scope |
| policy.graph.hang-regulate | POST | /policy/v1/policy/graph/hang | unavailable | op_id、scope |
| policy.graph.main | GET | /policy/v1/policy/graph | unavailable | （无；center/steps/limit 均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.graph.ner | API-000419, API-000420, API-000421, API-000422, API-000423 |
| policy.graph.intra | API-000424, API-000425, API-000426, API-000427, API-000428 |
| policy.graph.hang-support | API-000429, API-000430, API-000431, API-000432, API-000433 |
| policy.graph.hang-apply | API-000434, API-000435, API-000436, API-000437, API-000438 |
| policy.graph.hang-regulate | API-000439, API-000440, API-000441, API-000442, API-000443 |
| policy.graph.main | API-000444, API-000445, API-000446, API-000447, API-000448 |

---

## 3. 覆盖自检

- [x] 6 个 unavailable endpoint 均已写契约占位（每 endpoint 首条）
- [x] POST 类必填 op_id/scope（及 intra 的 relation_whitelist）缺省已覆盖
- [x] 异常-鉴权全页 1 条（API-000420，其余 endpoint 备注「鉴权同 API-000420」）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（未试调，无稳定必空构造）
- [x] 金样 1 条且断言完整信封（API-000419）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新（L07+L08）
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

**统计**：用例 **30** 条；编号 **API-000419**～**API-000448**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **30**（000419～000448） |
| catalog endpoint 数 | **6** |
| 金样（完整信封） | **1**（API-000419） |
| 异常-鉴权 | **1**（API-000420） |
| live 主路径 | **0**（全页 unavailable） |
| `_empty`（L07+L08） | **6** 行 **未覆盖** |
| code-registry 回写 | **父控**（本子任务未改） |
