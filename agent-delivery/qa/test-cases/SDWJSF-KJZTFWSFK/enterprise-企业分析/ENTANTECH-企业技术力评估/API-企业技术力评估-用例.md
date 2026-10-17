# 智能服务集群-科技专题服务算法库测试用例（企业技术力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业技术力评估  
> **catalog**：`entry_id=entan.tech` · `catalog_page_id=entan.tech` · path `/entan/tech`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.tech`  
> **A 线对照**：`fp-split-by-api-run/work/L31.md`（覆盖矩阵用，禁止 field 一行一用例）  
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
| 断言分工 | **API-00110（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 可解析形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00110」后，可只断言失败/不可用态或单点入参校验 |
| catalog 状态 | 本页 **4** 个 endpoint 均为 `status=unavailable`；**禁止**将 `sampleResponse` 中 `tech_power_index`、`talent_score`、`trend` 点值、`weight`、`markdown` 正文等作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 载荷说明 | `entan.tech.rank` 的 `responseFields` 声明 `enterprises`（array）；样例 JSON 明细位于 `value.enterprises`，断言 **仅强制** `responseFields`；`entan.tech.weights` 样例为数组，契约字段为 `weight`（number），endpoint 可用后 `data` 嵌套关系以执行期 as-built 为准 |
| 企业标识样例 | catalog example：`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`；路径 `orgId` 默认 `demo-org-sz-active-listed`；权重 `model=tech_power` |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.tech`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00110 | 企业分析 | 企业技术力评估 | 契约-不可用 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | catalog 不可用态下得分接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.tech.rank` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含可信 `enterprises` 的成功业务载荷；4、不得将 sampleResponse 中 tech_power_index 等数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00111 | 企业分析 | 企业技术力评估 | 异常-缺必填 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | 得分接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法空 enterprises 或无得分空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00112 | 企业分析 | 企业技术力评估 | 异常-空集合 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | 得分接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无技术力得分」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00113 | 企业分析 | 企业技术力评估 | 异常-非法编码 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | 得分接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 enterprises 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00114 | 企业分析 | 企业技术力评估 | 异常-类型错误 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | 得分接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功 enterprises 载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00115 | 企业分析 | 企业技术力评估 | 契约-不可用 | 技术力详情 | 企业技术力评估 | 技术力详情 | catalog 不可用态下详情接口不得按 live 得分与趋势验收 | 1、已确认 catalog `entan.tech.detail` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00110 | 1.GET /entan/v1/tech-power/demo-org-sz-active-listed（路径 orgId 取组合 TKD-01） | 1、不得将 sampleResponse 中 talent_score、trend 年份与 value 作为通过条件；2、响应须为可识别未交付、占位或失败语义；3、不得将失败当作空 talent_score/trend 成功态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=TKD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00116 | 企业分析 | 企业技术力评估 | 异常-非法orgId | 技术力详情 | 企业技术力评估 | 技术力详情 | 详情接口 orgId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/tech-power/__invalid__（路径 orgId 取组合 TKD-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作企业存在但无详情空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} | | INTEG | | | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=TKD-02；矩阵挂 orgId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00117 | 企业分析 | 企业技术力评估 | 契约-不可用 | 模型权重 | 企业技术力评估 | 模型权重 | catalog 不可用态下权重接口返回可识别非成功契约 | 1、已确认 catalog `entan.tech.weights` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 TKW-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含可信 weight 配置的成功业务载荷；3、不得将 sampleResponse 权重数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=TKW-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00118 | 企业分析 | 企业技术力评估 | 异常-缺必填model | 模型权重 | 企业技术力评估 | 模型权重 | 权重接口缺少 model 查询参数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 TKW-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 weight 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=TKW-02；矩阵挂 model、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00119 | 企业分析 | 企业技术力评估 | 异常-非法model | 模型权重 | 企业技术力评估 | 模型权重 | 权重接口 model 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 TKW-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 weight 的成功配置 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=TKW-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00120 | 企业分析 | 企业技术力评估 | 契约-不可用 | 评估报告 | 企业技术力评估 | 评估报告 | catalog 不可用态下报告接口不得按 live markdown 验收 | 1、已确认 catalog `entan.tech.report` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises/demo-org-sz-active-listed/report（路径 orgId 取组合 TKRPT-01） | 1、不得将 sampleResponse 中 markdown 标题文案作为通过条件；2、响应须为可识别未交付、占位或失败语义；3、不得将失败当作空 markdown 成功态 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | | INTEG | | | endpoint_id=entan.tech.report catalog_page_id=entan.tech 组合=TKRPT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00121 | 企业分析 | 企业技术力评估 | 异常-非法orgId | 评估报告 | 企业技术力评估 | 评估报告 | 报告接口 orgId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises/__invalid__/report（路径 orgId 取组合 TKRPT-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无法生成报告的空 markdown 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | | INTEG | | | endpoint_id=entan.tech.report catalog_page_id=entan.tech 组合=TKRPT-02；矩阵挂 orgId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00122 | 企业分析 | 企业技术力评估 | 异常-鉴权 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | 得分接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-01，无 Authorization 头 | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 enterprises 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-01；全页 detail/weights/report 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00123 | 企业分析 | 企业技术力评估 | 异常-非法格式orgId | 技术力详情 | 企业技术力评估 | 技术力详情 | 详情接口 orgId 含不允许字符时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/tech-power/org%2F..%2Finject（路径 orgId 取组合 TKD-03） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将路径注入尝试当作有效详情成功载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/tech-power/{orgId} | | INTEG | | | endpoint_id=entan.tech.detail catalog_page_id=entan.tech 组合=TKD-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00124 | 企业分析 | 企业技术力评估 | 异常-未知model | 模型权重 | 企业技术力评估 | 模型权重 | 权重接口 model 未知标识时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 TKW-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「模型存在但未配置权重」空态混淆为成功空 weight | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.tech.weights catalog_page_id=entan.tech 组合=TKW-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00125 | 企业分析 | 企业技术力评估 | 备选-最小集合 | 技术力得分 | 企业技术力评估 | 技术力得分（企业集合） | 得分接口单元素 enterprise_codes 下契约态可识别 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00110 | 1.POST /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute，请求体取组合 TKR-06 | 1、HTTP 与 code 可解析；2、不得将单企业样例 tech_power_index 作为通过条件；3、失败态不得冒充单企业空 enterprises 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | M_ENT_TECH_POWER_SCORE | INTEG | | | endpoint_id=entan.tech.rank catalog_page_id=entan.tech 组合=TKR-06；矩阵挂 enterprises 契约占位 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TKR-01 | entan.tech.rank | `enterprise_codes` = catalog example 四元组（`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`，可替换） | unavailable 契约占位主路径 |
| TKR-02 | entan.tech.rank | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| TKR-03 | entan.tech.rank | `enterprise_codes`: `[]` | 空集合 |
| TKR-04 | entan.tech.rank | `enterprise_codes`: `["__invalid__"]` | 非法企业编码 |
| TKR-05 | entan.tech.rank | `enterprise_codes`: `"demo-org-sz-active-listed"`（string，非 array） | 类型错误 |
| TKR-06 | entan.tech.rank | `enterprise_codes`: `["demo-org-sz-active-listed"]` | 最小合法集合形态 |
| TKD-01 | entan.tech.detail | 路径 `orgId=demo-org-sz-active-listed`（§0 样例） | 契约占位 |
| TKD-02 | entan.tech.detail | 路径 `orgId=__invalid__` | 非法 orgId |
| TKD-03 | entan.tech.detail | 路径 `orgId=org/..inject`（URL 编码后请求） | 非法格式 orgId |
| TKW-01 | entan.tech.weights | `model=tech_power`（catalog example） | 契约占位 |
| TKW-02 | entan.tech.weights | 不传 `model` 查询参数 | 缺必填 |
| TKW-03 | entan.tech.weights | `model=__invalid__` | 非法 model |
| TKW-04 | entan.tech.weights | `model=unknown_model_xyz` | 未知 model |
| TKRPT-01 | entan.tech.report | 路径 `orgId=demo-org-sz-active-listed` | 契约占位 |
| TKRPT-02 | entan.tech.report | 路径 `orgId=__invalid__` | 非法 orgId |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.tech.rank | POST | /entan/v1/entan/metric/M_ENT_TECH_POWER_SCORE/compute | unavailable | enterprise_codes（body） |
| entan.tech.detail | GET | /entan/v1/tech-power/{orgId} | unavailable | orgId（path） |
| entan.tech.weights | GET | /entan/v1/eval/weights | unavailable | model（query） |
| entan.tech.report | GET | /entan/v1/enterprises/{orgId}/report | unavailable | orgId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.tech.rank | API-00110、API-00111、API-00112、API-00113、API-00114、API-00122、API-00125 |
| entan.tech.detail | API-00115、API-00116、API-00123 |
| entan.tech.weights | API-00117、API-00118、API-00119、API-00124 |
| entan.tech.report | API-00120、API-00121 |

---

## 3. 覆盖自检

- [x] 四 unavailable endpoint 均已写契约占位（API-00110、00115、00117、00120）
- [x] `entan.tech.rank` 必填 `enterprise_codes` 已覆盖缺省、空集合、非法、类型错误（API-00111～00114）
- [x] `entan.tech.detail` / `entan.tech.report` 路径 orgId 非法已覆盖（API-00116、00121、00123）
- [x] `entan.tech.weights` 必填 `model` 已覆盖缺省与非法/未知（API-00118～00119、00124）
- [x] 异常-鉴权 1 条（API-00122，全页复用）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（四 endpoint unavailable，无稳定合法空结果试调证据）
- [x] 金样 1 条且断言完整信封（API-00110）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-00110～API-00125）

**统计**：用例 **16** 条；编号 **API-00110**～**API-00125**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **16**（00110～00125） |
| 金样（完整信封） | **1**（API-00110） |
| live 主路径 | **0**（四 endpoint 均 unavailable） |
| 每 endpoint 契约占位 | **4**（rank 00110，detail 00115，weights 00117，report 00120） |
| 异常-鉴权 | **1**（00122） |
| `_empty` 矩阵 | **4** 行 **未覆盖** |
| `_fail` 矩阵 | **4** 行 **已覆盖**（含缺必填/非法入参用例挂接） |
| req_only（L31） | **11** 行 **未覆盖** |
| 步骤以 METHOD+path 开头（抽检 3 条：00110、00116、00118） | **通过** |
| 预期无页面/图表表述（抽检 3 条：00110、00117、00120） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
