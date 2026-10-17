# 智能服务集群-科技专题服务算法库测试用例（文本解析 · 匹配 · 推演 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 文本解析 · 匹配 · 推演  
> **catalog**：`entry_id=policy.text` · `catalog_page_id=policy.text` · path `/policy/text`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.text`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `policy.text` 行（`_l6-to-catalog-map.yaml`：parse/match/simulate 合页，非 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000484（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页 **3** 个 endpoint 均为 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中政策标题、`elements`、`match_score`、企业名称、`baseline_value`/`simulated_value`、`curve` 等示例作为通过条件 |
| 样例与契约差 | `policy.text.parse` / `policy.text.match` 的 `sampleResponse` 为 **顶层数组**；契约 `responseFields` 分别仅声明 `title`、`match_score`。`policy.text.simulate` 样例同为数组，契约仅声明 `simulated_value`。断言 **只强制 responseFields**；样例扩展字段不设失败条件 |
| 试调 | **未试调**（父控未试调；本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 查询参数 | 三接口均为 GET；组合定义见附录 A |
| 本页 endpoint 数 | **3** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000484`～`000498`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.text`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000484 | 工程增强 | 文本解析 · 匹配 · 推演 | 契约-不可用 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | catalog 不可用态下文本解析接口可识别非 live 成功 | 1、已确认 catalog `policy.text.parse` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中政策标题或 elements 作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产文本解析判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_TEXT_PARSE | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000485 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-鉴权 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 文本解析接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信解析列表业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000486 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-非法policy_id | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 不存在或非法 policy_id 时返回可识别失败而非伪解析成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含 sample 形态标题列表的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-02；矩阵挂 policy_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000487 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-非法limit | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000488 | 工程增强 | 文本解析 · 匹配 · 推演 | 契约-字段形态 | 文本解析 | 文本解析 · 匹配 · 推演 | 文本解析 | 成功信封下契约出参 title 若存在是否符合 string 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000484 | 1.GET /policy/v1/policy/text/parse，查询参数取组合 PARSE-01 | 1、若 code 属成功集合且载荷含 title（含列表元素内），则 title 为 string；2、不得以 sample 中具体政策标题文案作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/text/parse | M_POLICY_TEXT_PARSE | INTEG | | | endpoint_id=policy.text.parse catalog_page_id=policy.text 组合=PARSE-01；矩阵挂 title |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000489 | 工程增强 | 文本解析 · 匹配 · 推演 | 契约-不可用 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | catalog 不可用态下政策匹配接口可识别非 live 成功 | 1、已确认 catalog `policy.text.match` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 match_score 或主体/政策名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产匹配判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000490 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-鉴权 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 政策匹配接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信匹配排行业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000491 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-非法subject_type | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | subject_type 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无匹配空结果或伪 match_score 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-02；矩阵挂 subject_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000492 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-非法limit | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断并成功返回 sample 形态列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000493 | 工程增强 | 文本解析 · 匹配 · 推演 | 契约-字段形态 | 政策匹配 | 文本解析 · 匹配 · 推演 | 政策匹配 | 成功信封下契约出参 match_score 若存在是否符合 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000489 | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01 | 1、若 code 属成功集合且载荷含 match_score（含列表元素内），则 match_score 为 number；2、不得以 sample 中 0.86 等具体匹配度作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.text.match catalog_page_id=policy.text 组合=MATCH-01；矩阵挂 match_score |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000494 | 工程增强 | 文本解析 · 匹配 · 推演 | 契约-不可用 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | catalog 不可用态下效果推演接口可识别非 live 成功 | 1、已确认 catalog `policy.text.simulate` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 baseline_value、simulated_value 或 curve 作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产推演判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_SIMULATE | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000495 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-鉴权 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 效果推演接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信推演曲线业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000496 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-非法scenario_id | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | scenario_id 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含 sample 推演值的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-02；矩阵挂 scenario_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000497 | 工程增强 | 文本解析 · 匹配 · 推演 | 异常-非法limit | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断并成功返回 sample 形态列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000498 | 工程增强 | 文本解析 · 匹配 · 推演 | 契约-字段形态 | 效果推演 | 文本解析 · 匹配 · 推演 | 效果推演 | 成功信封下契约出参 simulated_value 若存在是否符合 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000494 | 1.GET /policy/v1/policy/simulate，查询参数取组合 SIM-01 | 1、若 code 属成功集合且载荷含 simulated_value（含列表元素内），则 simulated_value 为 number；2、不得以 sample 中 81.4 等具体推演值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/simulate | M_POLICY_SIMULATE | INTEG | | | endpoint_id=policy.text.simulate catalog_page_id=policy.text 组合=SIM-01；矩阵挂 simulated_value |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| PARSE-01 | policy.text.parse | 不传 `policy_id`；`limit=20`（对齐 catalog `sampleRequest`） | 文本解析 unavailable 主路径 |
| PARSE-02 | policy.text.parse | `policy_id=__invalid_policy__`；`limit=20` | 非法政策 ID |
| PARSE-03 | policy.text.parse | `limit=0`（不传 policy_id） | 非正整数条数 |
| MATCH-01 | policy.text.match | `subject_type=enterprise`；`limit=20`（对齐 catalog `sampleRequest`） | 政策匹配 unavailable 主路径 |
| MATCH-02 | policy.text.match | `subject_type=__invalid_type__`；`limit=20` | 枚举外主体类型 |
| MATCH-03 | policy.text.match | `limit=0`（不传 subject_id / subject_type 或留空） | 非正整数条数 |
| SIM-01 | policy.text.simulate | `scope_code=440300`；`limit=20`（对齐 catalog `sampleRequest`） | 效果推演 unavailable 主路径 |
| SIM-02 | policy.text.simulate | `scenario_id=__invalid_scenario__`；`scope_code=440300`；`limit=20` | 枚举外推演情景 |
| SIM-03 | policy.text.simulate | `limit=0`（不传 scope_code / scenario_id 或留空） | 非正整数条数 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.text.parse | GET | /policy/v1/policy/text/parse | unavailable | policy_id、limit（均可选） |
| policy.text.match | GET | /policy/v1/policy/match | unavailable | subject_id、subject_type、limit（均可选） |
| policy.text.simulate | GET | /policy/v1/policy/simulate | unavailable | scope_code、scenario_id、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.text.parse | API-000484、000485、000486、000487、000488 |
| policy.text.match | API-000489、000490、000491、000492、000493 |
| policy.text.simulate | API-000494、000495、000496、000497、000498 |

---

## 3. 覆盖自检（§S1）

- [x] 3 个 unavailable endpoint 各 1 条契约占位（API-000484、000489、000494），未写 sample 数值通过条件
- [x] 异常-鉴权 3 条（000485、000490、000495）
- [x] 入参单缺陷 6 条（parse policy_id/limit；match subject_type/limit；simulate scenario_id/limit）
- [x] responseFields 契约占位 3 条（title、match_score、simulated_value）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000484；match/simulate 金样同 unavailable 语义）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000484～000498；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **15** |
| 编号闭区间 | **API-000484**～**API-000498** |
| endpoint 数 | **3**（各 5 条） |
| 金样（完整信封） | **1**（API-000484；全册信封规则见 §0） |
| `_empty` 未覆盖 | **3**（每 endpoint 1，见 coverage） |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
