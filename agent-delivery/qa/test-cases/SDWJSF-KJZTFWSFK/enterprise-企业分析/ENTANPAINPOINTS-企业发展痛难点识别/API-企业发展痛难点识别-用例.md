# 智能服务集群-科技专题服务算法库测试用例（企业发展痛难点识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业发展痛难点识别  
> **catalog**：`entry_id=entan.pain-points` · `catalog_page_id=entan.pain-points` · path `/entan/pain-points`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.pain-points`  
> **A 线对照**：`fp-split-by-api-run/work/L29.md`（覆盖矩阵用，禁止 field 一行一用例）  
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
| 断言分工 | **API-00095（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00095」后，可只断言失败/不可用态或单字段 |
| catalog 状态 | 本页 **2** 个 endpoint（`entan.pain-points.count` / `entan.pain-points.severity`）catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 count、severity、dimension_cards 内数值作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST JSON；必填 `enterprise_codes`（array）；组合定义见附录 A |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.pain-points`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00095 | 企业分析 | 企业发展痛难点识别 | 契约-不可用 | 痛难点反映企业数 | 企业发展痛难点识别 | 痛难点反映企业数（企业集合） | catalog 不可用态下反映企业数接口返回可识别非成功契约 | 1、已确认 catalog `entan.pain-points.count` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，请求体取组合 PPC-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 dimension_cards 的成功业务载荷；4、不得将 sampleResponse 示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | M_ENT_PAINPOINT_COUNT | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=PPC-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00096 | 企业分析 | 企业发展痛难点识别 | 异常-缺必填 | 痛难点反映企业数 | 企业发展痛难点识别 | 痛难点反映企业数（企业集合） | 反映企业数接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，请求体取组合 PPC-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法空 dimension_cards 或无反映企业成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=PPC-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00097 | 企业分析 | 企业发展痛难点识别 | 异常-空集合 | 痛难点反映企业数 | 企业发展痛难点识别 | 痛难点反映企业数（企业集合） | 反映企业数接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，请求体取组合 PPC-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无反映企业」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=PPC-03；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00098 | 企业分析 | 企业发展痛难点识别 | 异常-非法编码 | 痛难点反映企业数 | 企业发展痛难点识别 | 痛难点反映企业数（企业集合） | 反映企业数接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，请求体取组合 PPC-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将失败当作含可信 dimension_cards 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=PPC-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00099 | 企业分析 | 企业发展痛难点识别 | 契约-不可用 | 痛难点严重度 | 企业发展痛难点识别 | 痛难点严重度（企业集合） | catalog 不可用态下严重度接口返回可识别非成功契约 | 1、已确认 catalog `entan.pain-points.severity` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、信封规则见 API-00095 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，请求体取组合 PPS-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 dimension_cards 的成功严重度载荷；3、不得将 sampleResponse 严重度等级文案作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | M_ENT_PAINPOINT_SEVERITY | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=PPS-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00100 | 企业分析 | 企业发展痛难点识别 | 异常-缺必填 | 痛难点严重度 | 企业发展痛难点识别 | 痛难点严重度（企业集合） | 严重度接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，请求体取组合 PPS-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 dimension_cards 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=PPS-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00101 | 企业分析 | 企业发展痛难点识别 | 异常-空集合 | 痛难点严重度 | 企业发展痛难点识别 | 痛难点严重度（企业集合） | 严重度接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，请求体取组合 PPS-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下无严重度可算」空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=PPS-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00102 | 企业分析 | 企业发展痛难点识别 | 异常-非法编码 | 痛难点严重度 | 企业发展痛难点识别 | 痛难点严重度（企业集合） | 严重度接口 enterprise_codes 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，请求体取组合 PPS-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信严重度 dimension_cards 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=PPS-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00103 | 企业分析 | 企业发展痛难点识别 | 异常-鉴权 | 痛难点反映企业数 | 企业发展痛难点识别 | 痛难点反映企业数（企业集合） | 反映企业数接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute，请求体取组合 PPC-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 dimension_cards 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | | INTEG | | | endpoint_id=entan.pain-points.count catalog_page_id=entan.pain-points 组合=PPC-01；全页 severity 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00104 | 企业分析 | 企业发展痛难点识别 | 异常-类型错误 | 痛难点严重度 | 企业发展痛难点识别 | 痛难点严重度（企业集合） | 严重度接口 enterprise_codes 非数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute，请求体取组合 PPS-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功空 dimension_cards | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | | INTEG | | | endpoint_id=entan.pain-points.severity catalog_page_id=entan.pain-points 组合=PPS-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| PPC-01 | entan.pain-points.count | `enterprise_codes` = catalog example 四元组（`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`，执行期可替换） | unavailable 契约占位主路径 |
| PPC-02 | entan.pain-points.count | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| PPC-03 | entan.pain-points.count | `enterprise_codes`: `[]` | 空集合（失败哨兵，非空态） |
| PPC-04 | entan.pain-points.count | `enterprise_codes`: `["__invalid__"]` | 非法企业编码 |
| PPS-01 | entan.pain-points.severity | 同 PPC-01 企业集合 | unavailable 契约占位主路径 |
| PPS-02 | entan.pain-points.severity | 同 PPC-02 | 缺必填 |
| PPS-03 | entan.pain-points.severity | 同 PPC-03 | 空集合 |
| PPS-04 | entan.pain-points.severity | 同 PPC-04 | 非法编码 |
| PPS-05 | entan.pain-points.severity | `enterprise_codes`: `"demo-org-sz-active-listed"`（string，非 array） | 类型错误单缺陷 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.pain-points.count | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_COUNT/compute | unavailable | enterprise_codes |
| entan.pain-points.severity | POST | /entan/v1/entan/metric/M_ENT_PAINPOINT_SEVERITY/compute | unavailable | enterprise_codes |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.pain-points.count | API-00095、API-00096、API-00097、API-00098、API-00103 |
| entan.pain-points.severity | API-00099、API-00100、API-00101、API-00102、API-00104 |

---

## 3. 覆盖自检

- [x] 双 unavailable endpoint 已写契约占位（API-00095、API-00099）
- [x] 各 endpoint 必填 `enterprise_codes` 缺省、空集合、非法编码已覆盖（API-00096～00098、00100～00102）
- [x] 异常-鉴权 1 条（API-00103，全页复用）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定合法空结果构造）
- [x] 金样 1 条且断言完整信封（API-00095）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **10** 条；编号 **API-00095**～**API-00104**。
