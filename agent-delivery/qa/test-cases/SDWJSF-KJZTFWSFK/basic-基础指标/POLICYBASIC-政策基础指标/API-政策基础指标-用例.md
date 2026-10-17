# 智能服务集群-科技专题服务算法库测试用例（政策基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 政策基础指标  
> **catalog**：`entry_id=policy.basic` · `catalog_page_id=policy.basic` · path `/policy/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L03.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（50897 试调：**未试调**）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView 默认 `admin` / `gkx@2026`，密码经 AES-CFB 加密提交）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000409（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 与 catalog `responseFields` 形态）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-000409」后，可只断言 HTTP/`code`、**data 载荷** 或契约占位语义 |
| 试调 observed | **本轮未试调**（父控宣布）；执行期以现场为准，样例 JSON 仅作形态参考，**禁止**写入预期数值 |
| catalog 与现场 | 本页 2 个 endpoint 均为 `status=unavailable`；用例按 **契约占位 + 金样形态** 编写，不得将 `sampleResponse` 中政策数、时效、省份名等作为通过条件；若现场返回 mock 成功，记录 as-built 偏差 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000409`～`000418`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.basic`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000409 | 基础指标 | 政策基础指标 | 契约-不可用 | 金样信封 | 政策基础指标 | 指标总览 | catalog 不可用态下指标总览是否可识别非 live 成功 | 1、已按 §0 取得有效 token 与租户头；2、断言对象为完整原始响应信封 | 1.GET /policy/v1/policy/metrics（无查询参数） | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得将 sample 中政策总数、时效等数值作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产总览判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | M_POLICY_TOTAL_COUNT | INTEG | | | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 组合=— 金样 catalog_status=unavailable 未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000410 | 基础指标 | 政策基础指标 | 异常-鉴权 | 缺Token | 政策基础指标 | 指标总览 | 指标总览缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /policy/v1/policy/metrics（无查询参数），skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务总览载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | | INTEG | | | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 组合=—；全页其它 endpoint 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000411 | 基础指标 | 政策基础指标 | 契约-字段形态 | 指标总览 | 政策基础指标 | 指标总览 | 成功信封下 headline 若存在是否为 object 形态 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-000409 | 1.GET /policy/v1/policy/metrics（无查询参数） | 1、若 code 属成功集合且 data 含 headline 字段，则 headline 为 object；2、不得以 sample 内 KPI 键值数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | M_POLICY_VALIDITY_RATE | INTEG | | | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 组合=—；矩阵挂 headline |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000412 | 基础指标 | 政策基础指标 | 契约-空态占位 | 指标总览 | 政策基础指标 | 指标总览 | 总览无汇总数据时响应是否可与含 headline 结果区分 | 1、已确认 catalog `policy.basic.metrics` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/metrics（无查询参数） | 1、不得将失败态当作空总览成功；2、若 code 成功且 data 无 headline 或 headline 为空对象，执行期记录空态形态，不以 sample 数值验收 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | | INTEG | | | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 组合=—；矩阵挂 _empty |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000413 | 基础指标 | 政策基础指标 | 契约-失败占位 | 指标总览 | 政策基础指标 | 指标总览 | 上游或网关失败时总览是否可识别错误态 | 1、已按 §0 携带有效 token 与租户头；2、无稳定构造单点失败入参 | 1.GET /policy/v1/policy/metrics（无查询参数） | 1、若响应为失败态则 code 非成功集合或 HTTP 为 4xx/5xx；2、不得将失败当作空 headline 成功总览 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/metrics | | INTEG | | | endpoint_id=policy.basic.metrics catalog_page_id=policy.basic 组合=—；矩阵挂 _fail；无参接口待执行期复核 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000414 | 基础指标 | 政策基础指标 | 契约-不可用 | 五维金样 | 政策基础指标 | 基础指标 A1–A5 | catalog 不可用态下 kind=all 是否可识别非 live 成功 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-000409 | 1.GET /policy/v1/policy/indicators，查询参数取组合 IND-01 | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得将 sample 中级别、省份、政策数等作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产五维指标判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=IND-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000415 | 基础指标 | 政策基础指标 | 备选-kind单维 | A1级别 | 政策基础指标 | 基础指标 A1–A5 | kind=level 时是否仅关注级别分布块形态 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-000409 | 1.GET /policy/v1/policy/indicators，查询参数取组合 IND-02 | 1、若 code 属成功集合且 data 含 level 字段，则 level 为 array；2、不得以 sample 中 level_name、policy_count 数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_LEVEL_DIST | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=IND-02；矩阵挂 kind、level |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000416 | 基础指标 | 政策基础指标 | 备选-kind单维 | A3时序 | 政策基础指标 | 基础指标 A1–A5 | kind=timeseries 时是否仅关注时序块形态 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/indicators，查询参数取组合 IND-03 | 1、若 code 属成功集合且 data 含 timeseries 字段，则 timeseries 为 array；2、不得以 sample 中 period_key、publish_count 数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_TIMESERIES | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=IND-03；矩阵挂 timeseries |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000417 | 基础指标 | 政策基础指标 | 异常-非法kind | 五维指标 | 政策基础指标 | 基础指标 A1–A5 | kind 非法取值时是否返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/indicators，查询参数取组合 IND-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信五维数组的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=IND-04；矩阵挂 kind、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000418 | 基础指标 | 政策基础指标 | 契约-字段形态 | A4全国 | 政策基础指标 | 基础指标 A1–A5 | kind=national 时全国分布块是否为 array 形态 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /policy/v1/policy/indicators，查询参数取组合 IND-05 | 1、若 code 属成功集合且 data 含 national 字段，则 national 为 array；2、不得以 sample 中 province_name、policy_count 作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/indicators | M_POLICY_NATIONAL_DIST | INTEG | | | endpoint_id=policy.basic.indicators catalog_page_id=policy.basic 组合=IND-05；矩阵挂 national、type、sz 形态参考 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| IND-01 | policy.basic.indicators | kind=all（catalog example） | unavailable 五维主组合 |
| IND-02 | policy.basic.indicators | kind=level | A1 单维 |
| IND-03 | policy.basic.indicators | kind=timeseries | A3 单维 |
| IND-04 | policy.basic.indicators | kind=__invalid__ | 非法 kind（单缺陷） |
| IND-05 | policy.basic.indicators | kind=national | A4 单维 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| policy.basic.metrics | GET | /policy/v1/policy/metrics | unavailable | — |
| policy.basic.indicators | GET | /policy/v1/policy/indicators | unavailable | —（kind 可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.basic.metrics | API-000409、API-000410、API-000411、API-000412、API-000413 |
| policy.basic.indicators | API-000414、API-000415、API-000416、API-000417、API-000418 |

---

## 3. 覆盖自检

- [x] 本页 **0** 条 FUNC
- [x] 2 个 endpoint 各 **5** 条 API 用例（金样粒度）
- [x] 金样 2 条（API-000409、API-000414，备注含 `金样`）
- [x] 异常-鉴权 1 条（API-000410，全页复用）
- [x] 非法 kind 1 条（API-000417）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖/契约占位**（见 `coverage-fp.md`）
- [x] 50897 **未试调**（§0）
- [x] `coverage-fp.md` 已更新
- [x] 编号闭区间 **API-000409**～**API-000418**（父控分配；**未**改 `code-registry.yaml` / `run-log.md`）

**统计**：用例 **10** 条。

---

## 4. 红线自检（摘要）

| 检查 | 结果 |
|------|------|
| 正文四列内部引用扫描 | 0 命中 |
| 步骤含「核对/检查/验证」 | 0 命中 |
| 单条步骤/预期 ≤60 字、步骤 ≤7 | 通过 |
| 预期断言 1～4 点/条，无 ≥6 点 | 通过 |
| 用例按 主流程→备选→异常 排列 | 通过 |
| 金样备注 | API-000409、000414 |
