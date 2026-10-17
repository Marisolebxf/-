# 智能服务集群-科技专题服务算法库测试用例（重点布局产业推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 重点布局产业推荐  
> **catalog**：`entry_id=chain.layout` · `catalog_page_id=chain.layout` · path `/chain/layout`  
> **A 线对照**：`fp-split-by-api-run/work/L26.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /innov/v1/industry/{chainId}/recommendation`（path 变量 `chainId`） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000394（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`chain.hotspot.recommendation`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 recommend_index、recommend_level 等数值或「优先布局」文案作为通过条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000394`～`000398`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000394 | 产业链分析 | 重点布局产业推荐 | 契约-不可用 | 重点布局产业推荐模型 | 重点布局产业推荐 | M13 布局推荐 | catalog 不可用态下布局推荐接口可识别非 live 成功 | 1、已确认 catalog `chain.hotspot.recommendation` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/recommendation，path 取组合 LAY-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 recommend_index 或 recommend_level 作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产布局推荐判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.13 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | | FULL | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000395 | 产业链分析 | 重点布局产业推荐 | 异常-鉴权 | 重点布局产业推荐模型 | 重点布局产业推荐 | M13 布局推荐 | 布局推荐接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/industry/{chainId}/recommendation，path 取组合 LAY-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 recommend_index 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.13 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | | FULL | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000396 | 产业链分析 | 重点布局产业推荐 | 异常-非法chainId | 重点布局产业推荐模型 | 重点布局产业推荐 | M13 布局推荐 | 非法 chainId 时布局推荐接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/recommendation，path 取组合 LAY-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无推荐空 recommend_level 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.13 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | | FULL | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000397 | 产业链分析 | 重点布局产业推荐 | 异常-缺path产业标识 | 重点布局产业推荐模型 | 重点布局产业推荐 | M13 布局推荐 | path 缺 chainId 时布局推荐接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//recommendation（组合 LAY-03） | 1、HTTP 为 4xx 或响应 code 非成功集合；2、响应体不是成功空对象冒充可用布局推荐结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.13 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | | FULL | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-03；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000398 | 产业链分析 | 重点布局产业推荐 | 契约-字段形态 | 重点布局产业推荐模型 | 重点布局产业推荐 | M13 布局推荐 | 成功信封下契约出参字段若存在是否符合类型 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000394 | 1.GET /innov/v1/industry/{chainId}/recommendation，path 取组合 LAY-01 | 1、若 code 属成功集合且 data 为对象，则 recommend_level 存在时为 string；2、recommend_index 存在时为 number；3、不得以 sample 中 84.2 或「优先布局」等样例值为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.13 | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/recommendation | | FULL | | | endpoint_id=chain.hotspot.recommendation catalog_page_id=chain.layout 组合=LAY-01；矩阵挂 recommend_index、recommend_level |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| LAY-01 | chain.hotspot.recommendation | path `chainId=INB170101`（catalog example，执行期可替换为试调有效 id） | 契约主路径（unavailable） |
| LAY-02 | chain.hotspot.recommendation | path `chainId=__invalid__` | 非法产业标识 |
| LAY-03 | chain.hotspot.recommendation | path 缺 `chainId`：`GET /innov/v1/industry//recommendation` | 缺失 path 变量 |
| LAY-04 | chain.hotspot.recommendation | path `chainId=INB1701`（catalog 描述「INB1701 无推荐」） | 文档空态参考；**本轮无稳定空态构造**，见矩阵 `_empty` |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.hotspot.recommendation | GET | /innov/v1/industry/{chainId}/recommendation | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.hotspot.recommendation | API-000394、API-000395、API-000396、API-000397、API-000398 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-000394），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000395）
- [x] 入参单缺陷 2 条（API-000396、API-000397）
- [x] responseFields 契约占位 1 条（API-000398）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000394）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000394～000398）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000394**～**API-000398** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
