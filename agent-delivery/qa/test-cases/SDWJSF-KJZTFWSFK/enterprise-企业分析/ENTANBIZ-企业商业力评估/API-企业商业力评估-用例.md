# 智能服务集群-科技专题服务算法库测试用例（企业商业力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业商业力评估  
> **catalog**：`entry_id=entan.biz` · `catalog_page_id=entan.biz` · path `/entan/biz`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.biz`  
> **A 线对照**：`fp-split-by-api-run/work/L32.md`（覆盖矩阵用，禁止 field 一行一用例）  
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
| 断言分工 | **API-00126（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00126」后，可只断言失败/不可用态或单点入参校验结果 |
| catalog 状态 | 本页 **4** 个 endpoint 均为 `status=unavailable`；**禁止**将 `sampleResponse` 中 `biz_power_index`、`market_score`、`weight`、`markdown` 等数值或文案作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 企业标识样例 | catalog `example`：`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`（执行期可替换） |
| 载荷说明 | `entan.biz.rank` 的 `responseFields` 声明 `enterprises`（array）；样例 JSON 明细位于 `value.enterprises`，断言 **仅强制** `responseFields`；`entan.biz.weights` 样例为数组、契约字段为 `weight`，嵌套关系以 endpoint available 后 as-built 为准 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.biz`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00126 | 企业分析 | 企业商业力评估 | 契约-不可用 | 商业力得分 | 企业商业力评估 | 商业力得分（企业集合） | catalog 不可用态下得分接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.biz.rank` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，请求体取组合 BRK-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `enterprises` 的成功业务载荷；4、不得将 sampleResponse 商业力指数数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=BRK-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00127 | 企业分析 | 企业商业力评估 | 异常-缺必填 | 商业力得分 | 企业商业力评估 | 商业力得分（企业集合） | 得分接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，请求体取组合 BRK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法空 enterprises 或无得分成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=BRK-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00128 | 企业分析 | 企业商业力评估 | 异常-空集合 | 商业力得分 | 企业商业力评估 | 商业力得分（企业集合） | 得分接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，请求体取组合 BRK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无商业力得分」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=BRK-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00129 | 企业分析 | 企业商业力评估 | 异常-非法编码 | 商业力得分 | 企业商业力评估 | 商业力得分（企业集合） | 得分接口 enterprise_codes 含明显非法编码时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，请求体取组合 BRK-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 enterprises 得分的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=BRK-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00130 | 企业分析 | 企业商业力评估 | 契约-不可用 | 商业力详情 | 企业商业力评估 | 商业力详情 | catalog 不可用态下详情接口返回可识别非成功契约 | 1、已确认 catalog `entan.biz.detail` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00126 | 1.GET /entan/v1/biz-power/{orgId}，路径 orgId 取组合 BDT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 number 型 market_score 的成功详情载荷；3、不得将 sampleResponse 市场得分数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=BDT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00131 | 企业分析 | 企业商业力评估 | 异常-非法orgId | 商业力详情 | 企业商业力评估 | 商业力详情 | 详情接口路径 orgId 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/biz-power/{orgId}，路径 orgId 取组合 BDT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 market_score 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | | INTEG | | | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=BDT-02；矩阵挂 orgId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00132 | 企业分析 | 企业商业力评估 | 异常-占位orgId | 商业力详情 | 企业商业力评估 | 商业力详情 | 详情接口路径 orgId 为占位非法段时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/biz-power/{orgId}，路径 orgId 取组合 BDT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/404）；2、不得与「企业存在但无 market_score」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | | INTEG | | | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=BDT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00133 | 企业分析 | 企业商业力评估 | 异常-鉴权 | 商业力详情 | 企业商业力评估 | 商业力详情 | 详情接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /entan/v1/biz-power/{orgId}，路径 orgId 取组合 BDT-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 market_score 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/biz-power/{orgId} | | INTEG | | | endpoint_id=entan.biz.detail catalog_page_id=entan.biz 组合=BDT-01；全页 rank/weights/report 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00134 | 企业分析 | 企业商业力评估 | 契约-不可用 | 模型权重 | 企业商业力评估 | 模型权重 | catalog 不可用态下权重接口返回可识别非成功契约 | 1、已确认 catalog `entan.biz.weights` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00126 | 1.GET /entan/v1/eval/weights，查询参数取组合 BWT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 number 型 weight 的成功权重载荷；3、不得将 sampleResponse 权重数组数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=BWT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00135 | 企业分析 | 企业商业力评估 | 异常-缺必填 | 模型权重 | 企业商业力评估 | 模型权重 | 权重接口缺少 model 查询参数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 BWT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 weight 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=BWT-02；矩阵挂 model、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00136 | 企业分析 | 企业商业力评估 | 异常-非法model | 模型权重 | 企业商业力评估 | 模型权重 | 权重接口 model 为不支持标识时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 BWT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 weight 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=BWT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00137 | 企业分析 | 企业商业力评估 | 异常-空model | 模型权重 | 企业商业力评估 | 模型权重 | 权重接口 model 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/eval/weights，查询参数取组合 BWT-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「模型存在但 weight 为空配置」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/eval/weights | | INTEG | | | endpoint_id=entan.biz.weights catalog_page_id=entan.biz 组合=BWT-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00138 | 企业分析 | 企业商业力评估 | 契约-不可用 | 评估报告 | 企业商业力评估 | 评估报告 | catalog 不可用态下报告接口返回可识别非成功契约 | 1、已确认 catalog `entan.biz.report` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00126 | 1.GET /entan/v1/enterprises/{orgId}/report，路径 orgId 取组合 BRPT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 string 型 markdown 的成功报告载荷；3、不得将 sampleResponse 报告标题文案作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | M_ENT_BUSINESS_POWER_SCORE | INTEG | | | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=BRPT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00139 | 企业分析 | 企业商业力评估 | 异常-非法orgId | 评估报告 | 企业商业力评估 | 评估报告 | 报告接口路径 orgId 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises/{orgId}/report，路径 orgId 取组合 BRPT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 markdown 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | | INTEG | | | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=BRPT-02；矩阵挂 orgId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00140 | 企业分析 | 企业商业力评估 | 异常-占位orgId | 评估报告 | 企业商业力评估 | 评估报告 | 报告接口路径 orgId 为占位非法段时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises/{orgId}/report，路径 orgId 取组合 BRPT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/404）；2、不得与「企业存在但报告为空」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises/{orgId}/report | | INTEG | | | endpoint_id=entan.biz.report catalog_page_id=entan.biz 组合=BRPT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00141 | 企业分析 | 企业商业力评估 | 异常-类型错误 | 商业力得分 | 企业商业力评估 | 商业力得分（企业集合） | 得分接口 enterprise_codes 非数组类型时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute，请求体取组合 BRK-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功空 enterprises | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | | INTEG | | | endpoint_id=entan.biz.rank catalog_page_id=entan.biz 组合=BRK-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| BRK-01 | entan.biz.rank | `enterprise_codes` = catalog example 四元组（`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`，执行期可替换） | unavailable 契约占位主路径 |
| BRK-02 | entan.biz.rank | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| BRK-03 | entan.biz.rank | `enterprise_codes`: `[]` | 空集合（失败哨兵，非空态） |
| BRK-04 | entan.biz.rank | `enterprise_codes`: `["__invalid__"]` | 非法企业编码 |
| BRK-05 | entan.biz.rank | `enterprise_codes`: `"demo-org-sz-active-listed"`（string，非 array） | 类型错误单缺陷 |
| BDT-01 | entan.biz.detail | 路径 `orgId` = `demo-org-sz-active-listed`（catalog example） | unavailable 契约占位主路径 |
| BDT-02 | entan.biz.detail | 路径 `orgId` = `__invalid__` | 非法企业标识 |
| BDT-03 | entan.biz.detail | 路径 `orgId` = `%20`（空白占位段，执行期 URL 编码） | 占位/不可解析 orgId |
| BWT-01 | entan.biz.weights | 查询 `model` = `biz_power`（catalog example） | unavailable 契约占位主路径 |
| BWT-02 | entan.biz.weights | 不传 `model` 查询参数 | 缺必填 |
| BWT-03 | entan.biz.weights | 查询 `model` = `__unsupported_model__` | 非法或不支持模型标识 |
| BWT-04 | entan.biz.weights | 查询 `model` = ``（空字符串） | 空 model 单缺陷 |
| BRPT-01 | entan.biz.report | 路径 `orgId` = `demo-org-sz-active-listed`（catalog example） | unavailable 契约占位主路径 |
| BRPT-02 | entan.biz.report | 路径 `orgId` = `__invalid__` | 非法企业标识 |
| BRPT-03 | entan.biz.report | 路径 `orgId` = `%20`（空白占位段，执行期 URL 编码） | 占位/不可解析 orgId |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.biz.rank | POST | /entan/v1/entan/metric/M_ENT_BUSINESS_POWER_SCORE/compute | unavailable | enterprise_codes（body） |
| entan.biz.detail | GET | /entan/v1/biz-power/{orgId} | unavailable | orgId（path） |
| entan.biz.weights | GET | /entan/v1/eval/weights | unavailable | model（query） |
| entan.biz.report | GET | /entan/v1/enterprises/{orgId}/report | unavailable | orgId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.biz.rank | API-00126、API-00127、API-00128、API-00129、API-00141 |
| entan.biz.detail | API-00130、API-00131、API-00132、API-00133 |
| entan.biz.weights | API-00134、API-00135、API-00136、API-00137 |
| entan.biz.report | API-00138、API-00139、API-00140 |

---

## 3. 覆盖自检

- [x] 四 unavailable endpoint 均已写契约占位（API-00126、00130、00134、00138）
- [x] `entan.biz.rank` 必填 `enterprise_codes` 已覆盖缺省、空集合、非法编码、类型错误（API-00127～00129、00141）
- [x] `entan.biz.detail` / `entan.biz.report` 路径 orgId 已覆盖合法占位、非法、空白占位（各 3 条入参类 + 详情鉴权）
- [x] `entan.biz.weights` 必填 `model` 已覆盖缺省、非法、空字符串（API-00135～00137）
- [x] 异常-鉴权 1 条（API-00133，全页复用）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（四 endpoint unavailable，无稳定合法空结果构造）
- [x] 金样 1 条且断言完整信封（API-00126）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **16** 条；编号 **API-00126**～**API-00141**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **16**（00126～00141） |
| 金样（完整信封） | **1**（API-00126） |
| live 主路径 | **0**（四 endpoint 均 unavailable） |
| 每 endpoint 用例数 | **rank 5**；**detail/weights/report 各 4**（含全页鉴权 1 条挂 detail） |
| 每 endpoint 契约占位 | **4**（00126、00130、00134、00138） |
| `_empty` 矩阵 | **4** 行 **未覆盖** |
| `_fail` 矩阵 | **4** 行 **已覆盖**（契约占位 + 入参失败哨兵） |
| req_only（L32） | **13** 行 **未覆盖**（无 catalog endpoint） |
| 步骤以 METHOD+path 开头（抽检 00126、00131、00135） | **通过** |
| 预期无页面/图表表述（抽检 00126、00138、00141） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
