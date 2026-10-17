# 智能服务集群-科技专题服务算法库测试用例（企业实体与关系 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 企业实体与关系  
> **catalog**：`entry_id=entan.graph` · `catalog_page_id=entan.graph` · path `/entan/graph`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.graph`（12 endpoints）  
> **A 线对照**：`fp-split-by-api-run/work/L09.md`（ner/main）· `L10.md`（intra/hang 关系类）  
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
| 断言分工 | **API-00167（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00167」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **12** 个 endpoint 均为 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 written_nodes/written_edges/nodes/edges 示例数值、vid、权重作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST 写入类为 JSON body；GET 浏览类为查询参数；组合见附录 A |
| 样例与契约差 | 样例顶层字段常多于 `responseFields`；断言 **仅强制** catalog `responseFields`（written_nodes、written_edges、skipped、space 或 nodes、edges、source） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.graph`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00167 | 图谱 | 企业实体与关系 | 契约-不可用 | A 实体识别 ENT_NER_ORG | 企业实体与关系 | A 实体识别 ENT_NER_ORG | catalog 不可用态下实体识别接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.graph.ner` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/ner，请求体取组合 NER-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 written_nodes/written_edges/skipped 与 string 型 space 的成功业务载荷；4、不得将 sampleResponse 写入点/边示例作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/ner |  | INTEG |  |  | endpoint_id=entan.graph.ner catalog_page_id=entan.graph 组合=NER-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00168 | 图谱 | 企业实体与关系 | 异常-鉴权 | A 实体识别 ENT_NER_ORG | 企业实体与关系 | A 实体识别 ENT_NER_ORG | 实体识别接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /entan/v1/entan/graph/ner，请求体取组合 NER-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务图谱写入载荷） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/ner |  | INTEG |  |  | endpoint_id=entan.graph.ner catalog_page_id=entan.graph 组合=NER-01；全页鉴权代表 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00169 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | A 实体识别 ENT_NER_ORG | 企业实体与关系 | A 实体识别 ENT_NER_ORG | 实体识别接口缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/ner，请求体取组合 NER-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 written_nodes 冒充 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/ner |  | INTEG |  |  | endpoint_id=entan.graph.ner catalog_page_id=entan.graph 组合=NER-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00170 | 图谱 | 企业实体与关系 | 异常-缺必填scope | A 实体识别 ENT_NER_ORG | 企业实体与关系 | A 实体识别 ENT_NER_ORG | 实体识别接口缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/ner，请求体取组合 NER-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/ner |  | INTEG |  |  | endpoint_id=entan.graph.ner catalog_page_id=entan.graph 组合=NER-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00171 | 图谱 | 企业实体与关系 | 契约-不可用 | B 合作 ENT_RE_COOP | 企业实体与关系 | B 合作 ENT_RE_COOP | catalog 不可用态下合作接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 COOP-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷；4、禁止 sampleResponse 边权示例作通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-coop catalog_page_id=entan.graph 组合=COOP-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00172 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | B 合作 ENT_RE_COOP | 企业实体与关系 | B 合作 ENT_RE_COOP | B 合作 ENT_RE_COOP缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 COOP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-coop catalog_page_id=entan.graph 组合=COOP-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00173 | 图谱 | 企业实体与关系 | 异常-缺必填scope | B 合作 ENT_RE_COOP | 企业实体与关系 | B 合作 ENT_RE_COOP | B 合作 ENT_RE_COOP缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 COOP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-coop catalog_page_id=entan.graph 组合=COOP-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00174 | 图谱 | 企业实体与关系 | 异常-缺必填relation_whitelist | B 合作 ENT_RE_COOP | 企业实体与关系 | B 合作 ENT_RE_COOP | B 合作 ENT_RE_COOP缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 COOP-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-coop catalog_page_id=entan.graph 组合=COOP-04；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00175 | 图谱 | 企业实体与关系 | 异常-非法scope | B 合作 ENT_RE_COOP | 企业实体与关系 | B 合作 ENT_RE_COOP | B 合作 ENT_RE_COOP scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 COOP-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-coop catalog_page_id=entan.graph 组合=COOP-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00176 | 图谱 | 企业实体与关系 | 契约-不可用 | B 投资 ENT_RE_INVEST | 企业实体与关系 | B 投资 ENT_RE_INVEST | catalog 不可用态下投资接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 INV-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷；4、禁止 sampleResponse 边权示例作通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-invest catalog_page_id=entan.graph 组合=INV-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00177 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | B 投资 ENT_RE_INVEST | 企业实体与关系 | B 投资 ENT_RE_INVEST | B 投资 ENT_RE_INVEST缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 INV-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-invest catalog_page_id=entan.graph 组合=INV-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00178 | 图谱 | 企业实体与关系 | 异常-缺必填scope | B 投资 ENT_RE_INVEST | 企业实体与关系 | B 投资 ENT_RE_INVEST | B 投资 ENT_RE_INVEST缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 INV-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-invest catalog_page_id=entan.graph 组合=INV-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00179 | 图谱 | 企业实体与关系 | 异常-缺必填relation_whitelist | B 投资 ENT_RE_INVEST | 企业实体与关系 | B 投资 ENT_RE_INVEST | B 投资 ENT_RE_INVEST缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 INV-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-invest catalog_page_id=entan.graph 组合=INV-04；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00180 | 图谱 | 企业实体与关系 | 异常-非法scope | B 投资 ENT_RE_INVEST | 企业实体与关系 | B 投资 ENT_RE_INVEST | B 投资 ENT_RE_INVEST scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 INV-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-invest catalog_page_id=entan.graph 组合=INV-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00181 | 图谱 | 企业实体与关系 | 契约-不可用 | B 归属 ENT_RE_BELONG | 企业实体与关系 | B 归属 ENT_RE_BELONG | catalog 不可用态下归属接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 BEL-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷；4、禁止 sampleResponse 边权示例作通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-belong catalog_page_id=entan.graph 组合=BEL-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00182 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | B 归属 ENT_RE_BELONG | 企业实体与关系 | B 归属 ENT_RE_BELONG | B 归属 ENT_RE_BELONG缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 BEL-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-belong catalog_page_id=entan.graph 组合=BEL-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00183 | 图谱 | 企业实体与关系 | 异常-缺必填scope | B 归属 ENT_RE_BELONG | 企业实体与关系 | B 归属 ENT_RE_BELONG | B 归属 ENT_RE_BELONG缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 BEL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-belong catalog_page_id=entan.graph 组合=BEL-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00184 | 图谱 | 企业实体与关系 | 异常-缺必填relation_whitelist | B 归属 ENT_RE_BELONG | 企业实体与关系 | B 归属 ENT_RE_BELONG | B 归属 ENT_RE_BELONG缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 BEL-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-belong catalog_page_id=entan.graph 组合=BEL-04；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00185 | 图谱 | 企业实体与关系 | 异常-非法scope | B 归属 ENT_RE_BELONG | 企业实体与关系 | B 归属 ENT_RE_BELONG | B 归属 ENT_RE_BELONG scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 BEL-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-belong catalog_page_id=entan.graph 组合=BEL-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00186 | 图谱 | 企业实体与关系 | 契约-不可用 | B′ 供应链 ENT_RE_SUPPLY | 企业实体与关系 | B′ 供应链 ENT_RE_SUPPLY | catalog 不可用态下供应链接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 SUP-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷；4、禁止 sampleResponse 边权示例作通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-supply catalog_page_id=entan.graph 组合=SUP-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00187 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | B′ 供应链 ENT_RE_SUPPLY | 企业实体与关系 | B′ 供应链 ENT_RE_SUPPLY | B′ 供应链 ENT_RE_SUPPLY缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 SUP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-supply catalog_page_id=entan.graph 组合=SUP-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00188 | 图谱 | 企业实体与关系 | 异常-缺必填scope | B′ 供应链 ENT_RE_SUPPLY | 企业实体与关系 | B′ 供应链 ENT_RE_SUPPLY | B′ 供应链 ENT_RE_SUPPLY缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 SUP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-supply catalog_page_id=entan.graph 组合=SUP-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00189 | 图谱 | 企业实体与关系 | 异常-缺必填relation_whitelist | B′ 供应链 ENT_RE_SUPPLY | 企业实体与关系 | B′ 供应链 ENT_RE_SUPPLY | B′ 供应链 ENT_RE_SUPPLY缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 SUP-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-supply catalog_page_id=entan.graph 组合=SUP-04；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00190 | 图谱 | 企业实体与关系 | 异常-非法scope | B′ 供应链 ENT_RE_SUPPLY | 企业实体与关系 | B′ 供应链 ENT_RE_SUPPLY | B′ 供应链 ENT_RE_SUPPLY scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/intra，请求体取组合 SUP-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/intra |  | INTEG |  |  | endpoint_id=entan.graph.intra-supply catalog_page_id=entan.graph 组合=SUP-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00191 | 图谱 | 企业实体与关系 | 契约-不可用 | C 产业 ENT_RE_INDUSTRY | 企业实体与关系 | C 产业 ENT_RE_INDUSTRY | catalog 不可用态下产业挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HIN-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-industry catalog_page_id=entan.graph 组合=HIN-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00192 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | C 产业 ENT_RE_INDUSTRY | 企业实体与关系 | C 产业 ENT_RE_INDUSTRY | C 产业 ENT_RE_INDUSTRY缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HIN-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-industry catalog_page_id=entan.graph 组合=HIN-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00193 | 图谱 | 企业实体与关系 | 异常-缺必填scope | C 产业 ENT_RE_INDUSTRY | 企业实体与关系 | C 产业 ENT_RE_INDUSTRY | C 产业 ENT_RE_INDUSTRY缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HIN-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-industry catalog_page_id=entan.graph 组合=HIN-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00194 | 图谱 | 企业实体与关系 | 契约-不可用 | C 技术 ENT_RE_TECH | 企业实体与关系 | C 技术 ENT_RE_TECH | catalog 不可用态下技术挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HTC-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-tech catalog_page_id=entan.graph 组合=HTC-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00195 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | C 技术 ENT_RE_TECH | 企业实体与关系 | C 技术 ENT_RE_TECH | C 技术 ENT_RE_TECH缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HTC-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-tech catalog_page_id=entan.graph 组合=HTC-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00196 | 图谱 | 企业实体与关系 | 异常-缺必填scope | C 技术 ENT_RE_TECH | 企业实体与关系 | C 技术 ENT_RE_TECH | C 技术 ENT_RE_TECH缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HTC-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-tech catalog_page_id=entan.graph 组合=HTC-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00197 | 图谱 | 企业实体与关系 | 契约-不可用 | C 人才 ENT_RE_TALENT | 企业实体与关系 | C 人才 ENT_RE_TALENT | catalog 不可用态下人才挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HTL-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-talent catalog_page_id=entan.graph 组合=HTL-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00198 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | C 人才 ENT_RE_TALENT | 企业实体与关系 | C 人才 ENT_RE_TALENT | C 人才 ENT_RE_TALENT缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HTL-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-talent catalog_page_id=entan.graph 组合=HTL-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00199 | 图谱 | 企业实体与关系 | 异常-缺必填scope | C 人才 ENT_RE_TALENT | 企业实体与关系 | C 人才 ENT_RE_TALENT | C 人才 ENT_RE_TALENT缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HTL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-talent catalog_page_id=entan.graph 组合=HTL-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00200 | 图谱 | 企业实体与关系 | 契约-不可用 | C 政策 ENT_RE_POLICY | 企业实体与关系 | C 政策 ENT_RE_POLICY | catalog 不可用态下政策挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HPO-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-policy catalog_page_id=entan.graph 组合=HPO-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00201 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | C 政策 ENT_RE_POLICY | 企业实体与关系 | C 政策 ENT_RE_POLICY | C 政策 ENT_RE_POLICY缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HPO-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-policy catalog_page_id=entan.graph 组合=HPO-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00202 | 图谱 | 企业实体与关系 | 异常-缺必填scope | C 政策 ENT_RE_POLICY | 企业实体与关系 | C 政策 ENT_RE_POLICY | C 政策 ENT_RE_POLICY缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HPO-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-policy catalog_page_id=entan.graph 组合=HPO-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00203 | 图谱 | 企业实体与关系 | 契约-不可用 | C 科研 ENT_RE_RESEARCH | 企业实体与关系 | C 科研 ENT_RE_RESEARCH | catalog 不可用态下科研挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HRS-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-research catalog_page_id=entan.graph 组合=HRS-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00204 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | C 科研 ENT_RE_RESEARCH | 企业实体与关系 | C 科研 ENT_RE_RESEARCH | C 科研 ENT_RE_RESEARCH缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HRS-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-research catalog_page_id=entan.graph 组合=HRS-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00205 | 图谱 | 企业实体与关系 | 异常-缺必填scope | C 科研 ENT_RE_RESEARCH | 企业实体与关系 | C 科研 ENT_RE_RESEARCH | C 科研 ENT_RE_RESEARCH缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HRS-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-research catalog_page_id=entan.graph 组合=HRS-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00206 | 图谱 | 企业实体与关系 | 契约-不可用 | C 服务 ENT_RE_SERVICE | 企业实体与关系 | C 服务 ENT_RE_SERVICE | catalog 不可用态下服务挂接接口返回可识别非成功契约信封 | 1、已确认 catalog 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HSV-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成契约 responseFields 成功载荷 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-service catalog_page_id=entan.graph 组合=HSV-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00207 | 图谱 | 企业实体与关系 | 异常-缺必填op_id | C 服务 ENT_RE_SERVICE | 企业实体与关系 | C 服务 ENT_RE_SERVICE | C 服务 ENT_RE_SERVICE缺少 op_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00167 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HSV-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-service catalog_page_id=entan.graph 组合=HSV-02；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00208 | 图谱 | 企业实体与关系 | 异常-缺必填scope | C 服务 ENT_RE_SERVICE | 企业实体与关系 | C 服务 ENT_RE_SERVICE | C 服务 ENT_RE_SERVICE缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/graph/hang，请求体取组合 HSV-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph/hang |  | INTEG |  |  | endpoint_id=entan.graph.hang-service catalog_page_id=entan.graph 组合=HSV-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00209 | 图谱 | 企业实体与关系 | 契约-不可用 | D 浏览 ENT_GRAPH_BROWSE | 企业实体与关系 | D 浏览 ENT_GRAPH_BROWSE | catalog 不可用态下企业图谱浏览接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.graph.main` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/entan/graph，查询参数取组合 MAIN-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 nodes/edges 与 string 型 source 的成功业务载荷；4、不得将 sampleResponse 节点权重示例作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph |  | INTEG |  |  | endpoint_id=entan.graph.main catalog_page_id=entan.graph 组合=MAIN-01 catalog_status=unavailable；鉴权同 API-00168 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00210 | 图谱 | 企业实体与关系 | 异常-非法hops类型 | D 浏览 ENT_GRAPH_BROWSE | 企业实体与关系 | D 浏览 ENT_GRAPH_BROWSE | 图谱浏览接口 hops 非整数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/entan/graph，查询参数取组合 MAIN-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作含可信 nodes 的成功数据 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph |  | INTEG |  |  | endpoint_id=entan.graph.main catalog_page_id=entan.graph 组合=MAIN-02；矩阵挂 hops、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00211 | 图谱 | 企业实体与关系 | 异常-limit越界 | D 浏览 ENT_GRAPH_BROWSE | 企业实体与关系 | D 浏览 ENT_GRAPH_BROWSE | 图谱浏览接口 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/entan/graph，查询参数取组合 MAIN-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/graph |  | INTEG |  |  | endpoint_id=entan.graph.main catalog_page_id=entan.graph 组合=MAIN-03；矩阵挂 limit、_fail |
---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| NER-01 | entan.graph.ner | op_id=ENT_NER_ORG；scope=one；id=ORG1；mode=rule；dry_run=true（catalog sampleRequest，执行期可替换） | unavailable 契约占位 |
| NER-02 | entan.graph.ner | 不含 op_id；scope=one；id=ORG1；dry_run=true | 缺必填 op_id |
| NER-03 | entan.graph.ner | op_id=ENT_NER_ORG；不含 scope；id=ORG1 | 缺必填 scope |
| COOP-01 | entan.graph.intra-coop | op_id=ENT_RE_COOP；scope=one；id=ORG1；mode=rule；dry_run=true；relation_whitelist=["cooperate"] | unavailable 契约占位 |
| COOP-02 | entan.graph.intra-coop | 不含 op_id；scope=one；relation_whitelist=["cooperate"] | 缺 op_id |
| COOP-03 | entan.graph.intra-coop | op_id=ENT_RE_COOP；不含 scope；relation_whitelist=["cooperate"] | 缺 scope |
| COOP-04 | entan.graph.intra-coop | op_id=ENT_RE_COOP；scope=one；不含 relation_whitelist | 缺 relation_whitelist |
| COOP-05 | entan.graph.intra-coop | op_id=ENT_RE_COOP；scope=__invalid__；relation_whitelist=["cooperate"] | 非法 scope |
| INV-01 | entan.graph.intra-invest | op_id=ENT_RE_INVEST；scope=one；id=ORG1；mode=rule；dry_run=true；relation_whitelist=["invest"] | unavailable 契约占位 |
| INV-02 | entan.graph.intra-invest | 不含 op_id；scope=one；relation_whitelist=["invest"] | 缺 op_id |
| INV-03 | entan.graph.intra-invest | op_id=ENT_RE_INVEST；不含 scope；relation_whitelist=["invest"] | 缺 scope |
| INV-04 | entan.graph.intra-invest | op_id=ENT_RE_INVEST；scope=one；不含 relation_whitelist | 缺 relation_whitelist |
| INV-05 | entan.graph.intra-invest | op_id=ENT_RE_INVEST；scope=__invalid__；relation_whitelist=["invest"] | 非法 scope |
| BEL-01 | entan.graph.intra-belong | op_id=ENT_RE_BELONG；scope=one；id=ORG1；mode=rule；dry_run=true；relation_whitelist=["parent_sub"] | unavailable 契约占位 |
| BEL-02 | entan.graph.intra-belong | 不含 op_id；scope=one；relation_whitelist=["parent_sub"] | 缺 op_id |
| BEL-03 | entan.graph.intra-belong | op_id=ENT_RE_BELONG；不含 scope；relation_whitelist=["parent_sub"] | 缺 scope |
| BEL-04 | entan.graph.intra-belong | op_id=ENT_RE_BELONG；scope=one；不含 relation_whitelist | 缺 relation_whitelist |
| BEL-05 | entan.graph.intra-belong | op_id=ENT_RE_BELONG；scope=__invalid__；relation_whitelist=["parent_sub"] | 非法 scope |
| SUP-01 | entan.graph.intra-supply | op_id=ENT_RE_SUPPLY；scope=one；id=ORG1；mode=rule；dry_run=true；relation_whitelist=["supply"] | unavailable 契约占位 |
| SUP-02 | entan.graph.intra-supply | 不含 op_id；scope=one；relation_whitelist=["supply"] | 缺 op_id |
| SUP-03 | entan.graph.intra-supply | op_id=ENT_RE_SUPPLY；不含 scope；relation_whitelist=["supply"] | 缺 scope |
| SUP-04 | entan.graph.intra-supply | op_id=ENT_RE_SUPPLY；scope=one；不含 relation_whitelist | 缺 relation_whitelist |
| SUP-05 | entan.graph.intra-supply | op_id=ENT_RE_SUPPLY；scope=__invalid__；relation_whitelist=["supply"] | 非法 scope |
| HIN-01 | entan.graph.hang-industry | op_id=ENT_RE_INDUSTRY；scope=one；id=ORG1；mode=rule；dry_run=true；dest_types=["industry"] | unavailable 契约占位 |
| HIN-02 | entan.graph.hang-industry | 不含 op_id；scope=one；dest_types=["industry"] | 缺 op_id |
| HIN-03 | entan.graph.hang-industry | op_id=ENT_RE_INDUSTRY；不含 scope；dest_types=["industry"] | 缺 scope |
| HTC-01 | entan.graph.hang-tech | op_id=ENT_RE_TECH；scope=one；id=ORG1；mode=rule；dry_run=true；dest_types=["technology"] | unavailable 契约占位 |
| HTC-02 | entan.graph.hang-tech | 不含 op_id；scope=one；dest_types=["technology"] | 缺 op_id |
| HTC-03 | entan.graph.hang-tech | op_id=ENT_RE_TECH；不含 scope；dest_types=["technology"] | 缺 scope |
| HTL-01 | entan.graph.hang-talent | op_id=ENT_RE_TALENT；scope=one；id=ORG1；mode=rule；dry_run=true；dest_types=["talent"] | unavailable 契约占位 |
| HTL-02 | entan.graph.hang-talent | 不含 op_id；scope=one；dest_types=["talent"] | 缺 op_id |
| HTL-03 | entan.graph.hang-talent | op_id=ENT_RE_TALENT；不含 scope；dest_types=["talent"] | 缺 scope |
| HPO-01 | entan.graph.hang-policy | op_id=ENT_RE_POLICY；scope=one；id=ORG1；mode=rule；dry_run=true；dest_types=["policy"] | unavailable 契约占位 |
| HPO-02 | entan.graph.hang-policy | 不含 op_id；scope=one；dest_types=["policy"] | 缺 op_id |
| HPO-03 | entan.graph.hang-policy | op_id=ENT_RE_POLICY；不含 scope；dest_types=["policy"] | 缺 scope |
| HRS-01 | entan.graph.hang-research | op_id=ENT_RE_RESEARCH；scope=one；id=ORG1；mode=rule；dry_run=true；dest_types=["research"] | unavailable 契约占位 |
| HRS-02 | entan.graph.hang-research | 不含 op_id；scope=one；dest_types=["research"] | 缺 op_id |
| HRS-03 | entan.graph.hang-research | op_id=ENT_RE_RESEARCH；不含 scope；dest_types=["research"] | 缺 scope |
| HSV-01 | entan.graph.hang-service | op_id=ENT_RE_SERVICE；scope=one；id=ORG1；mode=rule；dry_run=true；dest_types=["service"] | unavailable 契约占位 |
| HSV-02 | entan.graph.hang-service | 不含 op_id；scope=one；dest_types=["service"] | 缺 op_id |
| HSV-03 | entan.graph.hang-service | op_id=ENT_RE_SERVICE；不含 scope；dest_types=["service"] | 缺 scope |
| MAIN-01 | entan.graph.main | center=ent:ORG1；hops=1；limit=90（catalog example） | unavailable 契约占位 |
| MAIN-02 | entan.graph.main | center=ent:ORG1；hops=not_int；limit=90 | 非法 hops 类型 |
| MAIN-03 | entan.graph.main | center=ent:ORG1；hops=1；limit=-1 | limit 越界 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.graph.ner | POST | /entan/v1/entan/graph/ner | unavailable | op_id、scope（body） |
| entan.graph.intra-coop | POST | /entan/v1/entan/graph/intra | unavailable | op_id、scope、relation_whitelist |
| entan.graph.intra-invest | POST | /entan/v1/entan/graph/intra | unavailable | op_id、scope、relation_whitelist |
| entan.graph.intra-belong | POST | /entan/v1/entan/graph/intra | unavailable | op_id、scope、relation_whitelist |
| entan.graph.intra-supply | POST | /entan/v1/entan/graph/intra | unavailable | op_id、scope、relation_whitelist |
| entan.graph.hang-industry | POST | /entan/v1/entan/graph/hang | unavailable | op_id、scope |
| entan.graph.hang-tech | POST | /entan/v1/entan/graph/hang | unavailable | op_id、scope |
| entan.graph.hang-talent | POST | /entan/v1/entan/graph/hang | unavailable | op_id、scope |
| entan.graph.hang-policy | POST | /entan/v1/entan/graph/hang | unavailable | op_id、scope |
| entan.graph.hang-research | POST | /entan/v1/entan/graph/hang | unavailable | op_id、scope |
| entan.graph.hang-service | POST | /entan/v1/entan/graph/hang | unavailable | op_id、scope |
| entan.graph.main | GET | /entan/v1/entan/graph | unavailable | （无；center/hops/limit 均可选） |


---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.graph.ner | API-00167, API-00168, API-00169, API-00170 |
| entan.graph.intra-coop | API-00171, API-00172, API-00173, API-00174, API-00175 |
| entan.graph.intra-invest | API-00176, API-00177, API-00178, API-00179, API-00180 |
| entan.graph.intra-belong | API-00181, API-00182, API-00183, API-00184, API-00185 |
| entan.graph.intra-supply | API-00186, API-00187, API-00188, API-00189, API-00190 |
| entan.graph.hang-industry | API-00191, API-00192, API-00193 |
| entan.graph.hang-tech | API-00194, API-00195, API-00196 |
| entan.graph.hang-talent | API-00197, API-00198, API-00199 |
| entan.graph.hang-policy | API-00200, API-00201, API-00202 |
| entan.graph.hang-research | API-00203, API-00204, API-00205 |
| entan.graph.hang-service | API-00206, API-00207, API-00208 |
| entan.graph.main | API-00209, API-00210, API-00211 |

---

## 3. 覆盖自检

- [x] 12 个 unavailable endpoint 均已写契约占位
- [x] POST 类必填 op_id/scope（及 intra 的 relation_whitelist）缺省已覆盖
- [x] 异常-鉴权全页 1 条（API-00168，其余 endpoint 备注「鉴权同 API-00168」）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（未试调，无稳定必空构造）
- [x] 金样 1 条且断言完整信封（API-00167）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新（L09+L10）
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **45** 条；编号 **API-00167**～**API-00211**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **45**（00167～00211） |
| catalog endpoint 数 | **12** |
| 金样（完整信封） | **1**（API-00167） |
| 异常-鉴权 | **1**（API-00168） |
| live 主路径 | **0**（全页 unavailable） |
| `_empty`（L09+L10） | **12** 行 **未覆盖** |
| code-registry 回写 | **父控**（本子任务未改） |
