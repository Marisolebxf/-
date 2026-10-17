# 智能服务集群-科技专题服务算法库测试用例（风险评分 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 风险评分  
> **catalog**：`entry_id=entan.risk` · `catalog_page_id=entan.risk` · path `/entan/risk`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.risk`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `entan.risk` 行（工程增强非 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
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
| 断言分工 | **API-00152（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00152」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **1** 个 endpoint（`entan.risk.list`）catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `risk_score`、`risk_level`、各 `*_count` 及企业名称示例作为通过条件 |
| 试调 | **未试调**（父控未试调；本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 查询参数 | GET 查询串；`level`、`limit` 均为可选；组合定义见附录 A |
| 样例与契约差 | `sampleResponse` 顶层为 `rows` 数组；契约 `responseFields` 仅声明 `rows`（array）。断言以 `responseFields` 为准；样例行内扩展字段（如 `enterprise_name`）不设失败条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.risk`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00152 | 工程增强 | 风险评分 | 契约-不可用 | 风险评分 | 风险评分 | 风险评分 | catalog 不可用态下风险列表接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.risk.list` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/risk，查询参数取组合 RISK-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `rows` 的成功业务载荷；4、不得将 sampleResponse 风险分示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00153 | 工程增强 | 风险评分 | 异常-鉴权 | 风险评分 | 风险评分 | 风险评分 | 风险列表接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /entan/v1/risk，查询参数取组合 RISK-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 rows 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00154 | 工程增强 | 风险评分 | 异常-非法level | 风险评分 | 风险评分 | 风险评分 | 风险列表接口 level 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00152 | 1.GET /entan/v1/risk，查询参数取组合 RISK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 rows 或无风险空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-02；矩阵挂 level、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00155 | 工程增强 | 风险评分 | 异常-非法limit类型 | 风险评分 | 风险评分 | 风险评分 | 风险列表接口 limit 非整数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/risk，查询参数取组合 RISK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将类型错误当作含可信 rows 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00156 | 工程增强 | 风险评分 | 异常-limit越界 | 风险评分 | 风险评分 | 风险评分 | 风险列表接口 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/risk，查询参数取组合 RISK-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将越界参数当作成功 rows 截断结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/risk | | INTEG | | | endpoint_id=entan.risk.list catalog_page_id=entan.risk 组合=RISK-04；矩阵挂 limit、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| RISK-01 | entan.risk.list | 不传 `level`；`limit`=200（与 catalog example 一致，执行期可替换） | unavailable 契约占位主路径 |
| RISK-02 | entan.risk.list | `level`=`__invalid_level__`；不传 `limit` | 枚举外等级（单缺陷） |
| RISK-03 | entan.risk.list | `limit`=`not_a_number`；不传 `level` | 非法类型 |
| RISK-04 | entan.risk.list | `limit`=-1；不传 `level` | 越界数量 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.risk.list | GET | /entan/v1/risk | unavailable | （无；`level`、`limit` 均为可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.risk.list | API-00152、API-00153、API-00154、API-00155、API-00156 |

---

## 3. 覆盖自检

- [x] 唯一 unavailable endpoint 已写契约占位（API-00152）
- [x] 可选入参 `level`、`limit` 单缺陷异常已覆盖（API-00154～00156）
- [x] 异常-鉴权 1 条（API-00153）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定「合法筛选下 rows 必空」试调证据）
- [x] 金样 1 条且断言完整信封（API-00152）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **5** 条；编号 **API-00152**～**API-00156**。
