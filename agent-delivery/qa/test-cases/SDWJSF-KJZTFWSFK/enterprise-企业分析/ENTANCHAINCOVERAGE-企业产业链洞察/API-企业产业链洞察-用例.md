# 智能服务集群-科技专题服务算法库测试用例（企业产业链洞察 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业产业链洞察  
> **catalog**：`entry_id=entan.chain-coverage` · `catalog_page_id=entan.chain-coverage` · path `/entan/chain-coverage`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.chain-coverage`  
> **A 线对照**：`fp-split-by-api-run/_catalog-snapshot.md`（`chain-coverage` 三 endpoint；`_l6-to-catalog-map.yaml` 不扩六级，无独立 `work/Lxx.md`）  
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
| 断言分工 | **API-00231（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00231」后，可只断言失败/不可用态或单字段 |
| catalog 状态 | 本页 **3** 个 endpoint 均为 `status=unavailable`；**禁止**将 `sampleResponse` 中 `coverage_rate`、`value`、`node_count`、`max_level` 等数值或 `evidence_level` 文案作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | 三 endpoint 均为 POST JSON；必填 `enterprise_codes`（array）；组合定义见附录 A |
| 载荷说明 | 样例 JSON 指标值位于 `value` 对象内；断言 **仅强制** 各 endpoint `responseFields` 声明字段（`coverage_rate` / `value` / `value`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.chain-coverage`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00231 | 企业分析 | 企业产业链洞察 | 契约-不可用 | 重点企业全景图 | 企业产业链洞察 | 重点企业全景图（企业集合） | catalog 不可用态下全景图接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.chain-coverage.keypano` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute，请求体取组合 CCK-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 number 型 `coverage_rate` 的成功业务载荷；4、不得将 sampleResponse 全景覆盖率数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | M_ENT_KEYPANO_DOMAIN_SUMMARY | INTEG | | | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=CCK-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00232 | 企业分析 | 企业产业链洞察 | 异常-鉴权 | 重点企业全景图 | 企业产业链洞察 | 重点企业全景图（企业集合） | 全景图接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute，请求体取组合 CCK-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 coverage_rate 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | | INTEG | | | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=CCK-01；全页 diversification/coverage-depth 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00233 | 企业分析 | 企业产业链洞察 | 异常-缺必填 | 重点企业全景图 | 企业产业链洞察 | 重点企业全景图（企业集合） | 全景图接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00231 | 1.POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute，请求体取组合 CCK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法空 coverage_rate 或无全景成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | | INTEG | | | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=CCK-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00234 | 企业分析 | 企业产业链洞察 | 异常-空集合 | 重点企业全景图 | 企业产业链洞察 | 重点企业全景图（企业集合） | 全景图接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute，请求体取组合 CCK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无全景可算」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | | INTEG | | | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=CCK-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00235 | 企业分析 | 企业产业链洞察 | 异常-非法编码 | 重点企业全景图 | 企业产业链洞察 | 重点企业全景图（企业集合） | 全景图接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute，请求体取组合 CCK-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将失败当作含可信 coverage_rate 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | | INTEG | | | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=CCK-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00236 | 企业分析 | 企业产业链洞察 | 异常-类型错误 | 重点企业全景图 | 企业产业链洞察 | 重点企业全景图（企业集合） | 全景图接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute，请求体取组合 CCK-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功空 coverage_rate | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | | INTEG | | | endpoint_id=entan.chain-coverage.keypano catalog_page_id=entan.chain-coverage 组合=CCK-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00237 | 企业分析 | 企业产业链洞察 | 契约-不可用 | 多元化指数 | 企业产业链洞察 | 多元化指数（企业集合） | catalog 不可用态下多元化指数接口返回可识别非成功契约 | 1、已确认 catalog `entan.chain-coverage.diversification` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00231 | 1.POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，请求体取组合 CCD-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 number 型多元化 `value` 的成功载荷；3、不得将 sampleResponse 指数数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | M_ENT_DIVERSIFICATION_INDEX | INTEG | | | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=CCD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00238 | 企业分析 | 企业产业链洞察 | 异常-缺必填 | 多元化指数 | 企业产业链洞察 | 多元化指数（企业集合） | 多元化指数接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，请求体取组合 CCD-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空多元化指数成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | | INTEG | | | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=CCD-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00239 | 企业分析 | 企业产业链洞察 | 异常-空集合 | 多元化指数 | 企业产业链洞察 | 多元化指数（企业集合） | 多元化指数接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，请求体取组合 CCD-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下指数不可算」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | | INTEG | | | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=CCD-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00240 | 企业分析 | 企业产业链洞察 | 异常-非法编码 | 多元化指数 | 企业产业链洞察 | 多元化指数（企业集合） | 多元化指数接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，请求体取组合 CCD-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信多元化 value 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | | INTEG | | | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=CCD-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00241 | 企业分析 | 企业产业链洞察 | 异常-类型错误 | 多元化指数 | 企业产业链洞察 | 多元化指数（企业集合） | 多元化指数接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，请求体取组合 CCD-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功空 value | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | | INTEG | | | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=CCD-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00242 | 企业分析 | 企业产业链洞察 | 备选-单元素集合 | 多元化指数 | 企业产业链洞察 | 多元化指数（企业集合） | 单企业标识集合下多元化指数接口仍返回不可用契约 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute，请求体取组合 CCD-06 | 1、响应 code 不属于成功集合，或 data 不构成含 number 型 value 的成功载荷；2、不得将单元素集合当作必出成功指数 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | | INTEG | | | endpoint_id=entan.chain-coverage.diversification catalog_page_id=entan.chain-coverage 组合=CCD-06 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00243 | 企业分析 | 企业产业链洞察 | 契约-不可用 | 领域覆盖深度 | 企业产业链洞察 | 领域覆盖深度（企业集合） | catalog 不可用态下覆盖深度接口返回可识别非成功契约 | 1、已确认 catalog `entan.chain-coverage.coverage-depth` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00231 | 1.POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute，请求体取组合 CCV-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 number 型覆盖深度 value 的成功载荷；3、不得将 sampleResponse 深度数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | M_ENT_DOMAIN_COVERAGE_DEPTH | INTEG | | | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=CCV-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00244 | 企业分析 | 企业产业链洞察 | 异常-缺必填 | 领域覆盖深度 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 覆盖深度接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute，请求体取组合 CCV-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空深度成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | | INTEG | | | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=CCV-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00245 | 企业分析 | 企业产业链洞察 | 异常-空集合 | 领域覆盖深度 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 覆盖深度接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute，请求体取组合 CCV-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下深度不可算」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | | INTEG | | | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=CCV-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00246 | 企业分析 | 企业产业链洞察 | 异常-非法编码 | 领域覆盖深度 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 覆盖深度接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute，请求体取组合 CCV-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信覆盖深度 value 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | | INTEG | | | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=CCV-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00247 | 企业分析 | 企业产业链洞察 | 异常-类型错误 | 领域覆盖深度 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 覆盖深度接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute，请求体取组合 CCV-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功空 value | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | | INTEG | | | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=CCV-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00248 | 企业分析 | 企业产业链洞察 | 备选-双元素集合 | 领域覆盖深度 | 企业产业链洞察 | 领域覆盖深度（企业集合） | 双企业标识集合下覆盖深度接口仍返回不可用契约 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute，请求体取组合 CCV-06 | 1、响应 code 不属于成功集合，或 data 不构成含 number 型 value 的成功载荷；2、不得将双元素集合当作必出成功深度 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | | INTEG | | | endpoint_id=entan.chain-coverage.coverage-depth catalog_page_id=entan.chain-coverage 组合=CCV-06 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CCK-01 | entan.chain-coverage.keypano | `enterprise_codes` = catalog example 四元组（`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`，执行期可替换） | unavailable 契约占位主路径 |
| CCK-02 | entan.chain-coverage.keypano | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| CCK-03 | entan.chain-coverage.keypano | `enterprise_codes`: `[]` | 空集合（失败哨兵，非空态） |
| CCK-04 | entan.chain-coverage.keypano | `enterprise_codes`: `["__invalid__"]` | 非法企业编码 |
| CCK-05 | entan.chain-coverage.keypano | `enterprise_codes`: `"demo-org-sz-active-listed"`（string，非 array） | 类型错误单缺陷 |
| CCD-01 | entan.chain-coverage.diversification | 同 CCK-01 企业集合 | unavailable 契约占位主路径 |
| CCD-02 | entan.chain-coverage.diversification | 同 CCK-02 | 缺必填 |
| CCD-03 | entan.chain-coverage.diversification | 同 CCK-03 | 空集合 |
| CCD-04 | entan.chain-coverage.diversification | 同 CCK-04 | 非法编码 |
| CCD-05 | entan.chain-coverage.diversification | 同 CCK-05 | 类型错误 |
| CCD-06 | entan.chain-coverage.diversification | `enterprise_codes`: `["demo-org-sz-active-listed"]` | 单元素合法形态（仍 unavailable） |
| CCV-01 | entan.chain-coverage.coverage-depth | 同 CCK-01 企业集合 | unavailable 契约占位主路径 |
| CCV-02 | entan.chain-coverage.coverage-depth | 同 CCK-02 | 缺必填 |
| CCV-03 | entan.chain-coverage.coverage-depth | 同 CCK-03 | 空集合 |
| CCV-04 | entan.chain-coverage.coverage-depth | 同 CCK-04 | 非法编码 |
| CCV-05 | entan.chain-coverage.coverage-depth | 同 CCK-05 | 类型错误 |
| CCV-06 | entan.chain-coverage.coverage-depth | `enterprise_codes`: `["demo-org-sz-active-listed","demo-org-hk"]` | 双元素合法形态（仍 unavailable） |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.chain-coverage.keypano | POST | /entan/v1/entan/metric/M_ENT_KEYPANO_DOMAIN_SUMMARY/compute | unavailable | enterprise_codes |
| entan.chain-coverage.diversification | POST | /entan/v1/entan/metric/M_ENT_DIVERSIFICATION_INDEX/compute | unavailable | enterprise_codes |
| entan.chain-coverage.coverage-depth | POST | /entan/v1/entan/metric/M_ENT_DOMAIN_COVERAGE_DEPTH/compute | unavailable | enterprise_codes |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.chain-coverage.keypano | API-00231～00236 |
| entan.chain-coverage.diversification | API-00237～00242 |
| entan.chain-coverage.coverage-depth | API-00243～00248 |

---

## 3. 覆盖自检

- [x] 三 unavailable endpoint 均已写契约占位（API-00231、00237、00243）
- [x] 各 endpoint 必填 `enterprise_codes` 已覆盖缺省、空集合、非法编码、类型错误（keypano 00233～00236；diversification 00238～00241；coverage-depth 00244～00247）
- [x] 异常-鉴权 1 条（API-00232，全页复用）
- [x] 备选入参形态 2 条（API-00242 单元素、00248 双元素）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（三 endpoint unavailable，无稳定合法空结果构造）
- [x] 金样 1 条且断言完整信封（API-00231）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **18** 条；编号 **API-00231**～**API-00248**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **18**（00231～00248） |
| 金样（完整信封） | **1**（API-00231） |
| live 主路径 | **0**（三 endpoint 均 unavailable） |
| 每 endpoint 用例数 | **keypano 6**；**diversification 6**；**coverage-depth 6** |
| 每 endpoint 契约占位 | **3**（00231、00237、00243） |
| `_empty` 矩阵 | **3** 行 **未覆盖** |
| `_fail` 矩阵 | **3** 行 **已覆盖**（契约占位 + 入参失败哨兵） |
| responseFields 契约占位 | **3**（coverage_rate / value / value） |
| A 线独立 Lxx | **无**（snapshot 三 POST + map 不扩六级） |
| 步骤以 METHOD+path 开头（抽检 00231、00238、00245） | **通过** |
| 预期无页面/图表表述（抽检 00231、00243、00248） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
