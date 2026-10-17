# 智能服务集群-科技专题服务算法库测试用例（深圳企业竞争力水平分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 深圳企业竞争力水平分析  
> **catalog**：`entry_id=entan.competitiveness` · `catalog_page_id=entan.competitiveness` · path `/entan/competitiveness`  
> **A 线对照**：`fp-split-by-api-run/work/L27.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 信封成功码 | `code` ∈ {0, `"0"`, 200, `"200"`} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 鉴权头 | `Authorization: Bearer <access_token>`、`TENANT-ID: 1`（OAuth `POST /auth/oauth2/token`，密码经联调台 AES 加密；账号口径见 `lumen-ui-algo-apiview` LoginView） |
| 断言分工 | **API-00075（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00075」后，可只断言失败/不可用态或单点入参校验结果 |
| catalog 状态 | 本页 **2** 个 endpoint 均为 `status=unavailable`；**禁止**将 `sampleResponse` 中 `total_score`、`dimensions` 等数值作为通过条件 |
| 试调 | 父控宣布 **未试调**：本会话 **不** curl、**不** 登录取 token；以下仅约定网关与信封，无 observed JSON |
| 企业标识样例 | catalog `example`：`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`（执行期可替换为环境有效 org_id） |
| 载荷说明 | catalog `responseFields` 声明 `enterprises`（array）；样例 JSON 中明细位于 `value.enterprises`，断言 **仅强制** `responseFields`；endpoint 可用后 `data` 与 `enterprises` 嵌套关系以执行期 as-built 为准 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.competitiveness`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00075 | 企业分析 | 深圳企业竞争力水平分析 | 契约-不可用 | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | catalog 不可用态下得分接口返回可识别非成功契约信封 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、catalog `entan.competitiveness.score` 为 unavailable；3、断言对象为完整原始响应信封 | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应含可解析 `code` 与 `data` 或等价载荷字段；3、`code` 不属于成功集合，或 `data` 不构成含可信 `enterprises` 得分的成功业务载荷；4、不得将 sampleResponse 中 total_score 等数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | M_ENT_COMPETITIVENESS_SCORE | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00076 | 企业分析 | 深圳企业竞争力水平分析 | 异常-鉴权 | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 得分接口无有效 token 时网关拒绝访问 | 1、请求 deliberately 不携带 Authorization | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-01，无 Authorization 头 | 1、HTTP 状态为 401 或 424；2、响应体可辨认为鉴权失败（非成功业务 enterprises 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-01；本页 ranking 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00077 | 企业分析 | 深圳企业竞争力水平分析 | 异常-缺必填enterprise_codes | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 得分接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 enterprises 或无得分空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00078 | 企业分析 | 深圳企业竞争力水平分析 | 异常-空集合enterprise_codes | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 得分接口 enterprise_codes 为空集合时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 非空或 HTTP 为 4xx；3、不得将失败当作合法无数据空 enterprises 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00079 | 企业分析 | 深圳企业竞争力水平分析 | 异常-非法enterprise_codes | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 得分接口含明显非法企业编码时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 total_score 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00080 | 企业分析 | 深圳企业竞争力水平分析 | 异常-类型错误enterprise_codes | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 得分接口 enterprise_codes 非数组类型时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作成功 enterprises 数组载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00081 | 企业分析 | 深圳企业竞争力水平分析 | 契约-不可用 | 综合竞争力排名 | 深圳企业竞争力水平分析 | 综合竞争力排名（企业集合） | catalog 不可用态下排名接口返回可识别非成功契约 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、catalog `entan.competitiveness.ranking` 为 unavailable；3、信封规则见 API-00075 | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 RNK-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含可信排序 enterprises 的成功业务载荷；3、不得将 sampleResponse 排名示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | M_ENT_COMPETITIVENESS_SCORE | INTEG | | | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00082 | 企业分析 | 深圳企业竞争力水平分析 | 异常-缺必填enterprise_codes | 综合竞争力排名 | 深圳企业竞争力水平分析 | 综合竞争力排名（企业集合） | 排名接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 RNK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 enterprises 或无排名空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00083 | 企业分析 | 深圳企业竞争力水平分析 | 异常-空集合enterprise_codes | 综合竞争力排名 | 深圳企业竞争力水平分析 | 综合竞争力排名（企业集合） | 排名接口 enterprise_codes 为空集合时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 RNK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法无数据空 enterprises 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00084 | 企业分析 | 深圳企业竞争力水平分析 | 异常-非法enterprise_codes | 综合竞争力排名 | 深圳企业竞争力水平分析 | 综合竞争力排名（企业集合） | 排名接口含明显非法企业编码时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 RNK-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信排序 enterprises 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-04 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SCR-01 | entan.competitiveness.score | `enterprise_codes`=[`demo-org-sz-active-listed`,`demo-org-hk`,`demo-org-gz-00`,`demo-org-bj-01`]（catalog example，可替换） | unavailable 契约占位主路径 |
| SCR-02 | entan.competitiveness.score | 请求体不含 `enterprise_codes` 字段 | 缺必填 |
| SCR-03 | entan.competitiveness.score | `enterprise_codes`=[] | 空集合 |
| SCR-04 | entan.competitiveness.score | `enterprise_codes`=[`__invalid_org__`] | 非法编码 |
| SCR-05 | entan.competitiveness.score | `enterprise_codes`=`not-an-array`（字符串，非 array 类型） | 非法类型 |
| RNK-01 | entan.competitiveness.ranking | `enterprise_codes` 同 SCR-01 | unavailable 契约占位主路径 |
| RNK-02 | entan.competitiveness.ranking | 请求体不含 `enterprise_codes` | 缺必填 |
| RNK-03 | entan.competitiveness.ranking | `enterprise_codes`=[] | 空集合 |
| RNK-04 | entan.competitiveness.ranking | `enterprise_codes`=[`__invalid_org__`] | 非法编码 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.competitiveness.score | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | unavailable | enterprise_codes（body） |
| entan.competitiveness.ranking | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | unavailable | enterprise_codes（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.competitiveness.score | API-00075、API-00076、API-00077、API-00078、API-00079、API-00080 |
| entan.competitiveness.ranking | API-00081、API-00082、API-00083、API-00084 |

---

## 3. 覆盖自检

- [x] 两个 unavailable endpoint 均已写契约占位（API-00075、API-00081）
- [x] 每个 endpoint 的 required `enterprise_codes` 已覆盖缺省、空集合、非法编码（score 另含类型错误 API-00080）
- [x] 异常-鉴权 1 条（API-00076），ranking 备注引用
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（无试调证据的稳定空结果构造）
- [x] ≥1 条备注含 `金样` 且断言完整信封（API-00075）
- [x] 父控宣布未试调：§0 无 observed，未 curl/登录
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-00075～API-00084）

**统计**：用例 **10** 条；编号 **API-00075**～**API-00084**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **10**（00075～00084） |
| 金样（完整信封） | **1**（API-00075） |
| live 主路径 | **0**（两 endpoint 均 unavailable） |
| 每 endpoint 契约占位 | **2**（score 00075，ranking 00081） |
| 每 endpoint 缺必填 enterprise_codes | **2**（00077、00082） |
| 异常-鉴权 | **1**（00076） |
| `_empty` 矩阵 | **2** 行 **未覆盖** |
| `_fail` 矩阵 | **2** 行 **已覆盖**（缺必填用例挂接） |
| req_only（L27） | **11** 行 **未覆盖**（无 catalog endpoint） |
| 步骤以 POST+path 开头（抽检 3 条：00075、00077、00084） | **通过** |
| 预期无页面/图表表述（抽检 3 条） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
