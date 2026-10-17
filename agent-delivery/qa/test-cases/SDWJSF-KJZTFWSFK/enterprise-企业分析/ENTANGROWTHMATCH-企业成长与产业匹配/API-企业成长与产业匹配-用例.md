# 智能服务集群-科技专题服务算法库测试用例（企业成长与产业匹配 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业成长与产业匹配  
> **catalog**：`entry_id=entan.growth-match` · `catalog_page_id=entan.growth-match` · path `/entan/growth-match`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.growth-match`  
> **A 线对照**：无独立 `work/Lxx.md`（`_l6-to-catalog-map.yaml` 注明 `entan.growth-match` 不扩六级）；矩阵四行键由 `entan.json` + `_catalog-snapshot.md` 对齐  
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
| 断言分工 | **API-00249（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00249」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **2** 个 endpoint（`entan.growth-match.potential` / `entan.growth-match.match`）catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `value` 数值及 `value.dimensions`、`upstream_degree` 等样例嵌套字段作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST JSON；必填 `enterprise_codes`（array）；组合定义见附录 A |
| 样例与契约差 | `sampleResponse` 中得分常位于 `value` 对象内（如 `value.value`）；契约 `responseFields` 仅声明顶层 **number** 型 `value`。断言以 `responseFields` 为准；样例多出的 dimensions / upstream_degree / hint 不设失败条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.growth-match`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00249 | 企业分析 | 企业成长与产业匹配 | 契约-不可用 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | catalog 不可用态下成长潜力接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.growth-match.potential` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 number 型 `value` 的成功业务载荷；4、不得将 sampleResponse 成长潜力示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | M_ENT_GROWTH_POTENTIAL | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00250 | 企业分析 | 企业成长与产业匹配 | 异常-缺必填 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00249 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法空 value 或无得分成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00251 | 企业分析 | 企业成长与产业匹配 | 异常-空集合 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无成长潜力可算」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-03；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00252 | 企业分析 | 企业成长与产业匹配 | 异常-非法编码 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将失败当作含可信 number 型 value 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00253 | 企业分析 | 企业成长与产业匹配 | 异常-类型错误 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功 value 载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00254 | 企业分析 | 企业成长与产业匹配 | 契约-不可用 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | catalog 不可用态下产业匹配度接口返回可识别非成功契约 | 1、已确认 catalog `entan.growth-match.match` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00249 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 number 型 `value` 的成功产业匹配度载荷；3、不得将 sampleResponse 匹配度示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | M_ENT_INDUSTRY_MATCH_SCORE | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00255 | 企业分析 | 企业成长与产业匹配 | 异常-缺必填 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 value 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00256 | 企业分析 | 企业成长与产业匹配 | 异常-空集合 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无匹配度可算」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00257 | 企业分析 | 企业成长与产业匹配 | 异常-非法编码 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信产业匹配度 value 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00258 | 企业分析 | 企业成长与产业匹配 | 异常-类型错误 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功 value 载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00259 | 企业分析 | 企业成长与产业匹配 | 异常-鉴权 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 value 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-01；全页 match 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00260 | 企业分析 | 企业成长与产业匹配 | 备选-最小集合 | 成长潜力（企业集合） | 企业成长与产业匹配 | 成长潜力（企业集合） | 成长潜力接口单元素 enterprise_codes 下契约态可识别 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00249 | 1.POST /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute，请求体取组合 GMP-06 | 1、HTTP 与 code 可解析；2、不得将单企业样例得分作为通过条件；3、失败态不得冒充单企业空 value 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | M_ENT_GROWTH_POTENTIAL | INTEG | | | endpoint_id=entan.growth-match.potential catalog_page_id=entan.growth-match 组合=GMP-06；矩阵挂 value 契约占位 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00261 | 企业分析 | 企业成长与产业匹配 | 备选-最小集合 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度接口单元素 enterprise_codes 下契约态可识别 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-06 | 1、HTTP 与 code 可解析；2、不得将单企业样例匹配度作为通过条件；3、失败态不得冒充单企业空 value 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | M_ENT_INDUSTRY_MATCH_SCORE | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-06；矩阵挂 value 契约占位 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00262 | 企业分析 | 企业成长与产业匹配 | 异常-null值 | 产业匹配度（企业集合） | 企业成长与产业匹配 | 产业匹配度（企业集合） | 产业匹配度接口 enterprise_codes 为 null 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute，请求体取组合 GMM-07 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将 null 当作空数组或省略键的成功空 value 态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | | INTEG | | | endpoint_id=entan.growth-match.match catalog_page_id=entan.growth-match 组合=GMM-07；矩阵挂 _fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GMP-01 | entan.growth-match.potential | `enterprise_codes` = catalog example 四元组（`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`，执行期可替换） | unavailable 契约占位主路径 |
| GMP-02 | entan.growth-match.potential | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| GMP-03 | entan.growth-match.potential | `enterprise_codes`: `[]` | 空集合（失败哨兵，非空态） |
| GMP-04 | entan.growth-match.potential | `enterprise_codes`: `["__invalid_org__"]` | 非法企业编码 |
| GMP-05 | entan.growth-match.potential | `enterprise_codes`: `"demo-org-sz-active-listed"`（string，非 array） | 类型错误单缺陷 |
| GMP-06 | entan.growth-match.potential | `enterprise_codes`: `["demo-org-sz-active-listed"]` | 单元素集合契约占位 |
| GMM-01 | entan.growth-match.match | 同 GMP-01 企业集合 | unavailable 契约占位主路径 |
| GMM-02 | entan.growth-match.match | 同 GMP-02 | 缺必填 |
| GMM-03 | entan.growth-match.match | 同 GMP-03 | 空集合 |
| GMM-04 | entan.growth-match.match | 同 GMP-04 | 非法编码 |
| GMM-05 | entan.growth-match.match | 同 GMP-05 | 类型错误 |
| GMM-06 | entan.growth-match.match | 同 GMP-06 | 单元素集合 |
| GMM-07 | entan.growth-match.match | `enterprise_codes`: `null` | null 值单缺陷 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.growth-match.potential | POST | /entan/v1/entan/metric/M_ENT_GROWTH_POTENTIAL/compute | unavailable | enterprise_codes（body） |
| entan.growth-match.match | POST | /entan/v1/entan/metric/M_ENT_INDUSTRY_MATCH_SCORE/compute | unavailable | enterprise_codes（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.growth-match.potential | API-00249～00253、00259、00260 |
| entan.growth-match.match | API-00254～00258、00261、00262 |

---

## 3. 覆盖自检

- [x] 双 unavailable endpoint 已写契约占位（API-00249、API-00254）
- [x] 各 endpoint 必填 `enterprise_codes` 已覆盖缺省、空集合、非法编码、类型错误（API-00250～00253、00255～00258）；match 另含 null（API-00262）
- [x] 异常-鉴权 1 条（API-00259，全页复用）
- [x] 单元素集合契约占位各 1 条（API-00260、00261）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定合法空 value 构造）
- [x] 金样 1 条且断言完整信封（API-00249）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **14** 条；编号 **API-00249**～**API-00262**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **14**（00249～00262） |
| 金样（完整信封） | **1**（API-00249） |
| live 主路径 | **0**（双 endpoint 均 unavailable） |
| 每 endpoint 用例数 | **potential 7**；**match 7**（含全页鉴权 1 条挂 potential） |
| 每 endpoint 契约占位 | **2**（potential 00249+00260；match 00254+00261） |
| `_empty` 矩阵 | **2** 行 **未覆盖** |
| `_fail` 矩阵 | **2** 行 **已覆盖**（含 catalog 不可用与入参失败哨兵） |
| A 线独立 Lxx work | **无**（catalog 四行键见 `coverage-fp.md`） |
| 步骤以 METHOD+path 开头（抽检 00249、00255、00262） | **通过** |
| 预期无页面/图表表述（抽检 00249、00259、00261） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| code-registry 回写 | **父控**（本子任务未改） |
