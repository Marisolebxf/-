# 智能服务集群-科技专题服务算法库测试用例（区域产业指数 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 区域产业指数  
> **catalog**：`entry_id=chain.region` · `catalog_page_id=chain.region` · path `/chain/region`  
> **A 线对照**：`fp-split-by-api-run/work/L23.md`（覆盖矩阵见 `coverage-fp.md`；矩阵键仅 grep L23，未读本六级 work 全文）  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.region`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 业务 path | `GET /innov/v1/industry/{chainId}/region-index`（`chain.region.main`）；`GET /innov/v1/industry/{chainId}/competitiveness`（`chain.region.competitiveness`）；path 变量 `chainId` |
| 鉴权 | `POST /auth/oauth2/token`（密码模式，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00360（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 类型）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00360」后，可只断言失败态或载荷形态 |
| catalog 状态 | `chain.region.main` 与 `chain.region.competitiveness` 均登记 **`status=unavailable`**；**禁止**将 `sampleResponse` 中 province、91/94 等指数分值或排名作为通过条件 |
| 试调 | **未试调**（本子任务禁 curl/浏览器；§0 鉴权与现场形态待执行期填写 observed） |
| 本页 endpoint 数 | **2** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00360 | 产业链分析 | 区域产业指数 | 契约-不可用 | 区域产业指数模型 | 区域产业指数 | 区域指数 | catalog 不可用态下区域指数接口可识别非 live 成功 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、catalog `status=unavailable` | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 REGM-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体含可解析 code 与 message 或 msg；3、不得将 sample 中 province 或 region_index 分值作为通过条件；4、若 code 属成功集合则 data 形态须在执行期记录且不得当作已接通生产区域指数 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-01 金样 §0未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00361 | 产业链分析 | 区域产业指数 | 异常-鉴权 | 区域产业指数模型 | 区域产业指数 | 区域指数 | 区域指数接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 REGM-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 region_index 业务载荷的成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-01；竞争力评价鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00362 | 产业链分析 | 区域产业指数 | 异常-非法chainId | 区域产业指数模型 | 区域产业指数 | 区域指数 | 非法 chainId 时区域指数接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 REGM-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无区域指数空结果成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00363 | 产业链分析 | 区域产业指数 | 异常-缺path产业标识 | 区域产业指数模型 | 区域产业指数 | 区域指数 | path 缺 chainId 时区域指数接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//region-index（组合 REGM-03） | 1、HTTP 为 4xx 或响应 code 非成功集合；2、响应体不是成功空数组冒充可用区域指数结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-03；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00364 | 产业链分析 | 区域产业指数 | 异常-缺租户头 | 区域产业指数模型 | 区域产业指数 | 区域指数 | 缺 TENANT-ID 时区域指数接口拒绝或返回可识别错误 | 1、已携带有效 Authorization；2、故意不携带 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 REGM-01 | 1、HTTP 为 401、424 或 4xx，或 code 非成功集合；2、不得返回含可信 region_index 业务载荷的成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00365 | 产业链分析 | 区域产业指数 | 契约-字段形态 | 区域产业指数模型 | 区域产业指数 | 区域指数 | 成功信封下 region_index 若存在是否仅为 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00360 | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 REGM-01 | 1、若 code 属成功集合且 data 为数组，则非空元素含 number 型 region_index；2、若 data 为对象则含 number 型 region_index（以 catalog responseFields 为准）；3、不得以 sample 中具体分值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-01；矩阵挂 region_index |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00366 | 产业链分析 | 区域产业指数 | 备选-合法chainId | 区域产业指数模型 | 区域产业指数 | 区域指数 | L0 产业 chainId 请求区域指数接口行为可识别 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00360 | 1.GET /innov/v1/industry/{chainId}/region-index，path 取组合 REGM-04 | 1、HTTP 与 code 可解析；2、不得将 catalog sample 数值作为通过条件；3、失败态与空结果态不得与 _fail 混淆（执行期记录形态） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/region-index | | FULL | | | endpoint_id=chain.region.main catalog_page_id=chain.region 组合=REGM-04；矩阵挂 chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00367 | 产业链分析 | 区域产业指数 | 契约-不可用 | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | catalog 不可用态下竞争力评价接口可识别非 live 成功 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、catalog `status=unavailable`；3、信封规则见 API-00360 | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 REGC-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含可信 competitiveness_index 的成功业务载荷；3、不得将 sample 中竞争力分值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00368 | 产业链分析 | 区域产业指数 | 异常-非法chainId | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | 非法 chainId 时竞争力评价接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 REGC-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 competitiveness_index 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00369 | 产业链分析 | 区域产业指数 | 异常-缺path产业标识 | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | path 缺 chainId 时竞争力评价接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//competitiveness（组合 REGC-03） | 1、HTTP 为 4xx 或响应 code 非成功集合；2、不得将路由错误当作空评价成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-03；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00370 | 产业链分析 | 区域产业指数 | 契约-字段形态 | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | 成功信封下 competitiveness_index 若存在是否仅为 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00360 | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 REGC-01 | 1、若 code 属成功集合且 data 为数组，则非空元素含 number 型 competitiveness_index；2、若 data 为对象则含 number 型 competitiveness_index；3、不得以 sample 分值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-01；矩阵挂 competitiveness_index |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00371 | 产业链分析 | 区域产业指数 | 备选-合法chainId | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | 另一合法格式 chainId 请求竞争力接口行为可识别 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00360 | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 REGC-04 | 1、HTTP 与 code 可解析；2、不得将 catalog sample 数值作为通过条件；3、失败态与空结果态须在执行期区分记录 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-04；矩阵挂 chainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00372 | 产业链分析 | 区域产业指数 | 异常-畸形chainId | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | 含非法字符的 chainId 时竞争力接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/competitiveness，path 取组合 REGC-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将畸形 id 当作合法产业返回 sample 形态数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-05；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00373 | 产业链分析 | 区域产业指数 | 异常-错误方法 | 区域产业指数模型 | 区域产业指数 | 竞争力评价 | 对竞争力 path 使用 POST 时是否返回可识别错误 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /innov/v1/industry/{chainId}/competitiveness（无 body 或空 JSON），path 取组合 REGC-01 | 1、HTTP 状态为 4xx 或 405；2、不得将错误方法当作 GET 成功竞争力评价 data | P2 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.9 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/competitiveness | | FULL | | | endpoint_id=chain.region.competitiveness catalog_page_id=chain.region 组合=REGC-01；矩阵挂 _fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| REGM-01 | chain.region.main | path `chainId=INB170101`（catalog `params.example`，执行期可替换） | 契约主路径（L1 示例） |
| REGM-02 | chain.region.main | path `chainId=__invalid__` | 非法产业标识 |
| REGM-03 | chain.region.main | path 缺 `chainId`：`GET /innov/v1/industry//region-index` | 缺失 path 变量 |
| REGM-04 | chain.region.main | path `chainId=INB1701`（产业链列表常见 L0 id） | 合法 id 另一层级 |
| REGC-01 | chain.region.competitiveness | path `chainId=INB170101`（catalog example） | 契约主路径 |
| REGC-02 | chain.region.competitiveness | path `chainId=__invalid__` | 非法产业标识 |
| REGC-03 | chain.region.competitiveness | path 缺 `chainId`：`GET /innov/v1/industry//competitiveness` | 缺失 path 变量 |
| REGC-04 | chain.region.competitiveness | path `chainId=INB1702`（列表样例备选产业） | 合法 id 备选 |
| REGC-05 | chain.region.competitiveness | path `chainId=INB%2F1701` 或含斜杠的畸形串（以网关实际编码为准） | 畸形 id |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.region.main | GET | /innov/v1/industry/{chainId}/region-index | unavailable | chainId（path） |
| chain.region.competitiveness | GET | /innov/v1/industry/{chainId}/competitiveness | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.region.main | API-00360～API-00366 |
| chain.region.competitiveness | API-00367～API-00373 |

---

## 3. 覆盖自检（§I）

- [x] 本页 **0** 条 FUNC
- [x] 两个 unavailable endpoint 均有契约占位（API-00360、00367）；金样信封 **API-00360**
- [x] 异常-鉴权 1 条（API-00361）；竞争力评价鉴权备注同本用例
- [x] 入参单缺陷：两 endpoint 各非法 id、缺 path；竞争力畸形 id（API-00362～00364、00368～00369、00372）
- [x] `region_index` / `competitiveness_index` 形态占位（API-00365、00370）
- [x] `_empty` 无稳定构造 → 矩阵 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 **API-00360～00373**）

---

## 4. 交卷计数（§I）

| 项 | 值 |
|----|-----|
| 用例条数 | **14** |
| 编号闭区间 | **API-00360**～**API-00373** |
| 金样 | **API-00360**（备注含 `金样`） |
| §0 试调 | **未试调** |
| FUNC 条数 | **0** |
| endpoint 数 | **2**（`chain.region.main`、`chain.region.competitiveness`） |
