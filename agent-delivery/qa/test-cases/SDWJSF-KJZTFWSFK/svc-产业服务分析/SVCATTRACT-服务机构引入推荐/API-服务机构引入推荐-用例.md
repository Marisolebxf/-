# 智能服务集群-科技专题服务算法库测试用例（服务机构引入推荐 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 服务机构引入推荐  
> **catalog**：`entry_id=svc.attract` · `catalog_page_id=svc.attract` · path `/industry-service/attract`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.attract` · endpoint `svc.attract.models`  
> **A 线对照**：`fp-split-by-api-run/work/L49.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /entan/v1/svc/models`（查询参数 `kind`，本页验收取值为 `attract`） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000629（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`svc.attract.models`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `attraction_index`、`priority_level`、`rank_no`、`recommend_reason`、`dimension_scores` 或机构名称示例作为通过条件 |
| 合 path 区分 | `GET /entan/v1/svc/models` 为多服务机构模型页共用；本页验收须 **`kind=attract`** + 页 title「服务机构引入推荐」；不得串其它 kind 模型结果 |
| 样例与契约差 | `sampleResponse.attract[]` 含 `org_id`、`ext.name`、`dimension_scores` 等；契约 `responseFields` 仅声明顶层 **`attract`（array）**。断言 **只强制 responseFields**；样例扩展字段不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000629`～`000633`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000629 | 产业服务分析 | 服务机构引入推荐 | 契约-不可用 | 服务机构引入推荐模型 | 服务机构引入推荐 | 引入推荐 | catalog 不可用态下引入推荐模型接口可识别非 live 成功 | 1、已确认 catalog `svc.attract.models` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/models，查询参数取组合 SVCATTRACT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中推荐指数、优先级级别或排序名次作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产引入推荐判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务机构引入推荐模型 | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_REC_ATTRACT_SCORE | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=SVCATTRACT-01 金样 §0未试调 catalog_status=unavailable kind=attract |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000630 | 产业服务分析 | 服务机构引入推荐 | 异常-鉴权 | 服务机构引入推荐模型 | 服务机构引入推荐 | 引入推荐 | 引入推荐模型接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /entan/v1/svc/models，查询参数取组合 SVCATTRACT-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 attract 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务机构引入推荐模型 | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=SVCATTRACT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000631 | 产业服务分析 | 服务机构引入推荐 | 异常-非法kind | 服务机构引入推荐模型 | 服务机构引入推荐 | 引入推荐 | 非法 kind 时返回可识别失败而非空 attract 成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/models，查询参数取组合 SVCATTRACT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无机构可引入空结果或伪 attract 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务机构引入推荐模型 | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=SVCATTRACT-02；矩阵挂 kind、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000632 | 产业服务分析 | 服务机构引入推荐 | 异常-非本页kind | 服务机构引入推荐模型 | 服务机构引入推荐 | 引入推荐 | 同 path 其它模型 kind 时不得当作本页 attract 引入推荐成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/models，查询参数取组合 SVCATTRACT-03 | 1、响应为失败态或可识别非 attract 契约态；2、不得将 gap 等其它 kind 的 sample 形态当作本页服务机构引入推荐通过 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务机构引入推荐模型 | N/A-技术项 | N/A | /entan/v1/svc/models | | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=SVCATTRACT-03；矩阵挂 kind、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000633 | 产业服务分析 | 服务机构引入推荐 | 契约-字段形态 | 服务机构引入推荐模型 | 服务机构引入推荐 | 引入推荐 | 成功信封下契约出参 attract 若存在是否符合 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000629 | 1.GET /entan/v1/svc/models，查询参数取组合 SVCATTRACT-01 | 1、若 code 属成功集合且载荷含 attract（含 data 内或顶层），则 attract 为 array；2、不得以 sample 中机构数、attraction_index 或 dimension_scores 数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·服务机构引入推荐模型 | N/A-技术项 | N/A | /entan/v1/svc/models | M_SVC_REC_ATTRACT_SCORE | INTEG | | | endpoint_id=svc.attract.models catalog_page_id=svc.attract 组合=SVCATTRACT-01；矩阵挂 attract；样例另含 M_SVC_DEEP_180_1 不设失败条件 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SVCATTRACT-01 | svc.attract.models | `kind=attract`（对齐 catalog `sampleRequest`） | 契约主路径（unavailable） |
| SVCATTRACT-02 | svc.attract.models | `kind=__invalid__` | 非法枚举/未知 kind |
| SVCATTRACT-03 | svc.attract.models | `kind=gap`（同 path 其它服务机构模型页典型 kind） | 非本页 kind，与 attract 空态区分 |
| SVCATTRACT-04 | svc.attract.models | 不传 `kind` | catalog 标可选；**本轮无独立用例**，语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| svc.attract.models | GET | /entan/v1/svc/models | unavailable | kind（可选；本页验收取值 attract） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.attract.models | API-000629、API-000630、API-000631、API-000632、API-000633 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-000629），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000630）
- [x] 入参单缺陷 2 条（API-000631 非法 kind、API-000632 非本页 kind）
- [x] responseFields 契约占位 1 条（API-000633 attract）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000629）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 API-000629～000633）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000629**～**API-000633** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
