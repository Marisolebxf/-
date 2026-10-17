# 智能服务集群-科技专题服务算法库测试用例（市场热度评级 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 市场热度评级  
> **catalog**：`entry_id=svc.market-heat` · `catalog_page_id=svc.market-heat` · path `/industry-service/market-heat`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.market-heat` · endpoint `svc.market-heat.main`  
> **A 线对照**：catalog 单 endpoint（`fp-split-by-api-run` 不扩六级，无独立 `Lxx.md`；覆盖矩阵见本目录 `coverage-fp.md`）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /entan/v1/svc/market-heat`（查询参数 `industry`，可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000639（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`svc.market-heat.main`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `market_heat_level`（如「高」）、`trend_slope`、`volatility` 或 `series` 内 `new_org_count` 等示例数值作为通过条件 |
| 样例与契约差 | `sampleResponse` 含 `trend_slope`、`volatility`；契约 `responseFields` **仅**声明 `market_heat_level`（string）、`series`（array）。断言以 `responseFields` 为准；样例 KPI 与折线图扩展字段不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000639`～`000643`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000639 | 产业服务分析 | 市场热度评级 | 契约-不可用 | 市场热度 | 市场热度评级 | 市场热度 | catalog 不可用态下市场热度接口可识别非 live 成功 | 1、已确认 catalog `svc.market-heat.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中热度等级或序列点数作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产市场热度判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·市场热度评级 | N/A-技术项 | N/A | /entan/v1/svc/market-heat | M_SVC_ORG_MARKET_HEAT | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000640 | 产业服务分析 | 市场热度评级 | 异常-鉴权 | 市场热度 | 市场热度评级 | 市场热度 | 市场热度接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 market_heat_level 或 series 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·市场热度评级 | N/A-技术项 | N/A | /entan/v1/svc/market-heat | | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000641 | 产业服务分析 | 市场热度评级 | 异常-非法industry | 市场热度 | 市场热度评级 | 市场热度 | 不存在或非法 industry 时返回可识别失败而非伪热度成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无序列空态或伪 market_heat_level 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·市场热度评级 | N/A-技术项 | N/A | /entan/v1/svc/market-heat | | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-02；矩阵挂 industry、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000642 | 产业服务分析 | 市场热度评级 | 异常-错误path | 市场热度 | 市场热度评级 | 市场热度 | 错误业务 path 时网关或应用返回可识别非本接口成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.按组合 MH-03 发起 GET（path 为 `/entan/v1/svc/market-heats`，查询参数同 MH-01） | 1、HTTP 状态为 404 或响应为失败态（code 非成功集合）；2、不得将错误 path 响应当作含可信 market_heat_level 的本页成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·市场热度评级 | N/A-技术项 | N/A | /entan/v1/svc/market-heats | | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-03；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000643 | 产业服务分析 | 市场热度评级 | 契约-字段形态 | 市场热度 | 市场热度评级 | 市场热度 | 成功信封下契约出参 market_heat_level 与 series 若存在是否符合声明类型 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000639 | 1.GET /entan/v1/svc/market-heat，查询参数取组合 MH-01 | 1、若 code 属成功集合且载荷含 market_heat_level，则其为 string；2、若载荷含 series，则 series 为 array；3、不得以 sample 中热度文案或 new_org_count 数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业服务深度分析模型构建·市场热度评级 | N/A-技术项 | N/A | /entan/v1/svc/market-heat | M_SVC_ORG_MARKET_HEAT | INTEG | | | endpoint_id=svc.market-heat.main catalog_page_id=svc.market-heat 组合=MH-01；矩阵挂 market_heat_level、series |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MH-01 | svc.market-heat.main | `industry=人工智能`（对齐 catalog `sampleRequest`） | 契约主路径（unavailable） |
| MH-02 | svc.market-heat.main | `industry=__invalid__` | 非法/不存在产业或技术领域 |
| MH-03 | svc.market-heat.main | path=`/entan/v1/svc/market-heats`；查询参数同 MH-01 | 错误 path（拼写偏差） |
| MH-04 | svc.market-heat.main | 不传 `industry` | catalog 标可选；**本轮无独立用例**，全领域默认语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| svc.market-heat.main | GET | /entan/v1/svc/market-heat | unavailable | industry（可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.market-heat.main | API-000639、API-000640、API-000641、API-000642、API-000643 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-000639），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000640）
- [x] 入参单缺陷 1 条（API-000641 industry）
- [x] 路径异常 1 条（API-000642）
- [x] responseFields 契约占位 1 条（API-000643 market_heat_level + series）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000639）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 API-000639～000643）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000639**～**API-000643** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
