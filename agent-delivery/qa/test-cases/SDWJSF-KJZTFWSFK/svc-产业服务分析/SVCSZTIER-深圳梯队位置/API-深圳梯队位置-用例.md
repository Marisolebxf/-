# 智能服务集群-科技专题服务算法库测试用例（深圳梯队位置 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业服务分析 / 深圳梯队位置  
> **catalog**：`entry_id=svc.sz-tier` · `catalog_page_id=svc.sz-tier` · path `/industry-service/sz-tier`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/svc.json` 页 `svc.sz-tier` · endpoint `svc.sz-tier.main`  
> **A 线对照**：catalog 单 endpoint（`fp-split-by-api-run` 不扩六级，无独立 `Lxx.md`；覆盖矩阵见本目录 `coverage-fp.md`）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /entan/v1/svc/sz-tier`（查询参数 `industry`，可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00644（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`svc.sz-tier.main`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中梯队档位（如 T1、T2）、维度中文名或 `dim_key` 示例作为通过条件 |
| 样例与契约差 | `sampleResponse` 含 `dims` 数组元素（`dim`、`dim_key`、`tier` 等）；契约 `responseFields` **仅**声明 `dims`（array）。断言以 `responseFields` 为准；样例内 `tier` 枚举值不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00644`～`00648`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00644 | 产业服务分析 | 深圳梯队位置 | 契约-不可用 | 深圳梯队 | 深圳梯队位置 | 深圳梯队 | catalog 不可用态下深圳梯队接口可识别非 live 成功 | 1、已确认 catalog `svc.sz-tier.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SVCSZTIER-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中梯队档位或维度名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产深圳梯队判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A（catalog 页；不扩六级） | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | M_SVC_SZ_TIER | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SVCSZTIER-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00645 | 产业服务分析 | 深圳梯队位置 | 异常-鉴权 | 深圳梯队 | 深圳梯队位置 | 深圳梯队 | 深圳梯队接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SVCSZTIER-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 dims 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A（catalog 页；不扩六级） | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SVCSZTIER-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00646 | 产业服务分析 | 深圳梯队位置 | 异常-非法industry | 深圳梯队 | 深圳梯队位置 | 深圳梯队 | 明显非法 industry 取值时返回可识别失败而非伪梯队成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SVCSZTIER-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无梯队空 dims 成功态或 sample 形态 T1/T2 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A（catalog 页；不扩六级） | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SVCSZTIER-02；矩阵挂 industry、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00647 | 产业服务分析 | 深圳梯队位置 | 异常-空industry | 深圳梯队 | 深圳梯队位置 | 深圳梯队 | 空字符串 industry 时返回可识别失败而非静默默认产业梯队成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SVCSZTIER-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将空 industry 当作与合法产业等价的 dims 成功载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A（catalog 页；不扩六级） | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SVCSZTIER-03；矩阵挂 industry、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00648 | 产业服务分析 | 深圳梯队位置 | 契约-字段形态 | 深圳梯队 | 深圳梯队位置 | 深圳梯队 | 成功信封下契约出参 dims 若存在是否符合 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00644 | 1.GET /entan/v1/svc/sz-tier，查询参数取组合 SVCSZTIER-01 | 1、若 code 属成功集合且载荷含 dims（含 data 内或顶层），则 dims 为 array；2、不得以 sample 中梯队档位或维度条数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A（catalog 页；不扩六级） | N/A-技术项 | N/A | /entan/v1/svc/sz-tier | M_SVC_SZ_TIER | INTEG | | | endpoint_id=svc.sz-tier.main catalog_page_id=svc.sz-tier 组合=SVCSZTIER-01；矩阵挂 dims |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SVCSZTIER-01 | svc.sz-tier.main | `industry=人工智能`（对齐 catalog `sampleRequest`） | 契约主路径（unavailable） |
| SVCSZTIER-02 | svc.sz-tier.main | `industry=__invalid__` | 明显非法/不可解析产业名 |
| SVCSZTIER-03 | svc.sz-tier.main | `industry=`（空字符串） | 空产业筛选边界 |
| SVCSZTIER-04 | svc.sz-tier.main | 不传 `industry` | catalog 标可选；**本轮无独立用例**，与 01 语义待 endpoint available 后区分 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| svc.sz-tier.main | GET | /entan/v1/svc/sz-tier | unavailable | industry（可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.sz-tier.main | API-00644、API-00645、API-00646、API-00647、API-00648 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-00644），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-00645）
- [x] 入参单缺陷 2 条（API-00646 非法 industry、API-00647 空 industry）
- [x] responseFields 契约占位 1 条（API-00648 dims）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-00644）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-00644～00648；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-00644**～**API-00648** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
