# 智能服务集群-科技专题服务算法库测试用例（产业发展路线历程 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业发展路线历程  
> **catalog**：`entry_id=chain.roadmap` · `catalog_page_id=chain.roadmap` · path `/chain/roadmap`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.roadmap`  
> **A 线对照**：`fp-split-by-api-run/work/L16.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 业务 path | `GET /innov/v1/industry/{chainId}/roadmap`（path 变量 `chainId`） |
| 鉴权 | `POST /auth/oauth2/token`（密码模式，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00389（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 类型）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00389」后，可只断言失败/不可用态 |
| catalog 状态 | `chain.hotspot.roadmap` 登记 **`status=unavailable`**；**禁止**将 `sampleResponse` 中 timeline、key_events、事件标题或企业名等示例数值作为通过条件 |
| 样例与契约差 | `sampleResponse` 含按年 `key_events` 明细与 `viz` 配置；契约 `responseFields` 仅声明顶层 `timeline`（array）。断言 **只强制 responseFields**；样例内事件类型/年份不设失败条件 |
| 试调 | **未试调**（本子任务禁 curl/浏览器；§0 鉴权与现场形态待执行期填写 observed） |
| 本页 endpoint 数 | **1**（`chain.hotspot.roadmap`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00389 | 产业链分析 | 产业发展路线历程 | 契约-不可用 | 产业发展路线历程模型 | 产业发展路线历程 | M3 发展历程 | catalog 不可用态下发展历程接口可识别非 live 成功 | 1、已确认 catalog `chain.hotspot.roadmap` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/roadmap，path 取组合 RDM-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 `code`；3、不得将 sample 中 timeline 事件清单或企业名示例值作为通过条件；4、若 code 属成功集合则 data 形态须在执行期记录且不得当作已接通生产历程时间线 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.3 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap | | FULL | | | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDM-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00390 | 产业链分析 | 产业发展路线历程 | 异常-鉴权 | 产业发展路线历程模型 | 产业发展路线历程 | M3 发展历程 | 发展历程接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/industry/{chainId}/roadmap，path 取组合 RDM-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信历程业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.3 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap | | FULL | | | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00391 | 产业链分析 | 产业发展路线历程 | 异常-非法chainId | 产业发展路线历程模型 | 产业发展路线历程 | M3 发展历程 | 非法 chainId 时发展历程接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/roadmap，path 取组合 RDM-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将失败当作无事件空 timeline 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.3 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap | | FULL | | | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDM-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00392 | 产业链分析 | 产业发展路线历程 | 异常-缺path产业标识 | 产业发展路线历程模型 | 产业发展路线历程 | M3 发展历程 | path 缺 chainId 时发展历程接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//roadmap（组合 RDM-03） | 1、HTTP 为 4xx 或响应 code 非成功集合；2、响应体不是成功空对象冒充可用历程结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.3 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap | | FULL | | | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDM-03；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00393 | 产业链分析 | 产业发展路线历程 | 异常-畸形chainId | 产业发展路线历程模型 | 产业发展路线历程 | M3 发展历程 | 含非法字符的 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/roadmap，path 取组合 RDM-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将畸形 id 当作合法产业返回 sample 形态 timeline 数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.3 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/roadmap | | FULL | | | endpoint_id=chain.hotspot.roadmap catalog_page_id=chain.roadmap 组合=RDM-04；矩阵挂 _fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RDM-01 | chain.hotspot.roadmap | path `chainId=INB1701`（catalog `params.example`，执行期可替换） | unavailable 契约占位主路径 |
| RDM-02 | chain.hotspot.roadmap | path `chainId=__invalid__` | 非法产业标识 |
| RDM-03 | chain.hotspot.roadmap | path 缺 `chainId`：`GET /innov/v1/industry//roadmap` | 缺失 path 变量 |
| RDM-04 | chain.hotspot.roadmap | path `chainId=INB%2F1701` 或含空格/斜杠的畸形串（以网关实际编码为准） | 畸形 id |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.hotspot.roadmap | GET | /innov/v1/industry/{chainId}/roadmap | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.hotspot.roadmap | API-00389～API-00393 |

---

## 3. 覆盖自检（§I）

- [x] 本页 **0** 条 FUNC
- [x] unavailable endpoint 契约占位 + 金样信封（API-00389）
- [x] 异常-鉴权 1 条（API-00390）
- [x] 入参单缺陷：非法 id、缺 path、畸形 id（API-00391、00392、00393）
- [x] `timeline` 升 live 后须补主路径/字段形态用例（本批金样仅 5 条，形态占位见矩阵）
- [x] `_empty` 无稳定构造 → 矩阵 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 **API-00389～00393**）

---

## 4. 交卷计数（§I）

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-00389**～**API-00393** |
| 金样 | **API-00389**（备注含 `金样`） |
| §0 试调 | **未试调** |
| FUNC 条数 | **0** |
