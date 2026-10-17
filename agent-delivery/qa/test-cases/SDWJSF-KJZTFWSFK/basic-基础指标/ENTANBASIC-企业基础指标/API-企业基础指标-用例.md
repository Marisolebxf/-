# 智能服务集群-科技专题服务算法库测试用例（企业基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 企业基础指标  
> **catalog**：`entry_id=entan.basic` · `catalog_page_id=entan.basic` · path `/entan/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L02.md`（覆盖矩阵用，禁止 field 一行一用例）  
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
| 断言分工 | **API-00063（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 类型与 catalog `responseFields` 形态）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00063」后，可只断言 HTTP/`code`、**data 载荷** 或契约占位语义 |
| 试调 observed | **本轮未试调**（父控宣布）；执行期以现场为准，样例 JSON 仅作形态参考，**禁止**写入预期数值 |
| catalog 与现场 | 本页 7 个 endpoint 在 catalog 均为 `status=unavailable`；用例按 **契约占位 + 金样形态** 编写，不得将 `sampleResponse` 中企业名、计数、金额等作为通过条件；若现场返回 mock 成功，记录 as-built 偏差 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.basic`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00063 | 基础指标 | 企业基础指标 | 主流程-筛选项形态 | 金样信封 | 企业基础指标 | 筛选项 | 筛选项在有效鉴权下返回成功信封与四维枚举字段形态 | 1、已按 §0 取得有效 token 与租户头；2、断言对象为完整原始响应信封 | 1.GET /entan/v1/meta/filters（无查询参数） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data 中 industries、cities、domains、years 存在且均为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/meta/filters | | INTEG | | | endpoint_id=entan.basic.filters catalog_page_id=entan.basic 组合=— 金样 catalog_status=unavailable 未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00064 | 基础指标 | 企业基础指标 | 异常-鉴权 | 缺Token | 企业基础指标 | 筛选项 | 筛选项缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /entan/v1/meta/filters（无查询参数），skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务筛选项载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/meta/filters | | INTEG | | | endpoint_id=entan.basic.filters catalog_page_id=entan.basic 组合=—；全页其它 endpoint 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00065 | 基础指标 | 企业基础指标 | 契约-不可用 | 重点企业 | 企业基础指标 | 重点企业 | catalog 不可用态下重点企业接口不得按 live 成功数值验收 | 1、已确认 catalog `entan.basic.key-enterprises` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-01 | 1、不得将 sampleResponse 中 enterprise_name、key_score 等数值作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | M_ENT_TOTAL_COUNT | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00066 | 基础指标 | 企业基础指标 | 契约-不可用 | 类型分布 | 企业基础指标 | 企业类型分布 | catalog 不可用态下类型分布接口不得按 live 成功数值验收 | 1、已确认 catalog `entan.basic.type-distribution` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/type-distribution，查询参数取组合 TYP-01 | 1、不得将 sampleResponse 中 rows 内 enterprise_count 等作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution | | INTEG | | | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00067 | 基础指标 | 企业基础指标 | 契约-不可用 | 领域分布 | 企业基础指标 | 领域分布 | catalog 不可用态下领域分布接口不得按 live 成功数值验收 | 1、已确认 catalog `entan.basic.domain-distribution` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/domain-distribution，查询参数取组合 DOM-01 | 1、不得将 sampleResponse 中 rows 企业数、增长率作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/domain-distribution | | INTEG | | | endpoint_id=entan.basic.domain-distribution catalog_page_id=entan.basic 组合=DOM-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00068 | 基础指标 | 企业基础指标 | 契约-不可用 | 历年新增 | 企业基础指标 | 历年新增企业 | catalog 不可用态下历年新增接口不得按 live 成功数值验收 | 1、已确认 catalog `entan.basic.new-enterprises` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/new-enterprises，查询参数取组合 NEW-01 | 1、不得将 sampleResponse 中 new_count、cumulative_count 作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/new-enterprises | M_ENT_NEW_COUNT_Y | INTEG | | | endpoint_id=entan.basic.new-enterprises catalog_page_id=entan.basic 组合=NEW-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00069 | 基础指标 | 企业基础指标 | 契约-不可用 | 资讯统计 | 企业基础指标 | 重点资讯统计 | catalog 不可用态下资讯统计接口不得按 live 成功数值验收 | 1、已确认 catalog `entan.news.stats` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/news/stats，查询参数取组合 NST-01 | 1、不得将 sampleResponse 中 news_count、total_amount、growth_rate 作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats | M_ENT_NEWS_STAT | INTEG | | | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00070 | 基础指标 | 企业基础指标 | 契约-不可用 | 资讯明细 | 企业基础指标 | 重点资讯明细 | catalog 不可用态下资讯明细接口不得按 live 成功数值验收 | 1、已确认 catalog `entan.news.list` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/news，查询参数取组合 NLST-01 | 1、不得将 sampleResponse 中 list 条目、total 作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00071 | 基础指标 | 企业基础指标 | 异常-非法limit | 重点企业 | 企业基础指标 | 重点企业 | 重点企业接口 limit 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、catalog 仍为 unavailable | 1.GET /entan/v1/key-enterprises，查询参数取组合 KEY-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或契约占位语义下不得冒充含可信 key_score 的成功列表；2、message 或 msg 非空（若返回业务失败信封） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/key-enterprises | | INTEG | | | endpoint_id=entan.basic.key-enterprises catalog_page_id=entan.basic 组合=KEY-02；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00072 | 基础指标 | 企业基础指标 | 异常-非法year | 类型分布 | 企业基础指标 | 企业类型分布 | 类型分布接口 year 非法类型时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/type-distribution，查询参数取组合 TYP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或不得将失败当作含可信 rows 的成功统计；2、不得用成功空 rows 冒充非法 year 已通过校验 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/type-distribution | | INTEG | | | endpoint_id=entan.basic.type-distribution catalog_page_id=entan.basic 组合=TYP-02；矩阵挂 year、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00073 | 基础指标 | 企业基础指标 | 异常-非法news_type | 资讯统计 | 企业基础指标 | 重点资讯统计 | 资讯统计接口 news_type 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/news/stats，查询参数取组合 NST-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或不得将失败当作含可信 news_count 的成功统计；2、message 或 msg 非空（若返回业务失败信封） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news/stats | | INTEG | | | endpoint_id=entan.news.stats catalog_page_id=entan.basic 组合=NST-02；矩阵挂 news_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00074 | 基础指标 | 企业基础指标 | 异常-非法page | 资讯明细 | 企业基础指标 | 重点资讯明细 | 资讯明细接口 page 非法类型时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/news，查询参数取组合 NLST-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或不得将失败当作含可信 list 的成功分页；2、不得用成功空 list 冒充非法 page 已通过校验 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/news | | INTEG | | | endpoint_id=entan.news.list catalog_page_id=entan.basic 组合=NLST-02；矩阵挂 page、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| KEY-01 | entan.basic.key-enterprises | industry=人工智能；city=深圳市；scale=大；limit=150（catalog example，可替换） | unavailable 契约占位主组合 |
| KEY-02 | entan.basic.key-enterprises | limit=-1；其余不传 | 非法 limit（单缺陷） |
| TYP-01 | entan.basic.type-distribution | year=2025 | unavailable 契约占位 |
| TYP-02 | entan.basic.type-distribution | year=__invalid__ | 非法 year 类型 |
| DOM-01 | entan.basic.domain-distribution | year=2025 | unavailable 契约占位 |
| NEW-01 | entan.basic.new-enterprises | domain=ALL（catalog example） | unavailable 契约占位 |
| NST-01 | entan.news.stats | 不传 news_type（全部） | unavailable 契约占位 |
| NST-02 | entan.news.stats | news_type=__invalid__ | 非法资讯类型 |
| NLST-01 | entan.news.list | news_type=financing；page=1；size=15；keyword 不传 | unavailable 契约占位 |
| NLST-02 | entan.news.list | page=abc；size=15 | 非法 page 类型 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.basic.filters | GET | /entan/v1/meta/filters | unavailable | — |
| entan.basic.key-enterprises | GET | /entan/v1/key-enterprises | unavailable | —（params 均为可选） |
| entan.basic.type-distribution | GET | /entan/v1/type-distribution | unavailable | — |
| entan.basic.domain-distribution | GET | /entan/v1/domain-distribution | unavailable | — |
| entan.basic.new-enterprises | GET | /entan/v1/new-enterprises | unavailable | — |
| entan.news.stats | GET | /entan/v1/news/stats | unavailable | — |
| entan.news.list | GET | /entan/v1/news | unavailable | — |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.basic.filters | API-00063、API-00064 |
| entan.basic.key-enterprises | API-00065、API-00071 |
| entan.basic.type-distribution | API-00066、API-00072 |
| entan.basic.domain-distribution | API-00067 |
| entan.basic.new-enterprises | API-00068 |
| entan.news.stats | API-00069、API-00073 |
| entan.news.list | API-00070、API-00074 |

---

## 3. 覆盖自检

- [x] 本页 0 条 FUNC
- [x] 7 个 endpoint 各有契约占位或金样/异常用例
- [x] 金样 1 条且断言完整信封（API-00063）
- [x] 异常-鉴权 1 条（API-00064，全页复用口径）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（unavailable + 未试调，无稳定空态构造）
- [x] 50897 **未试调**（§0）
- [x] `coverage-fp.md` 已更新

**统计**：用例 **12** 条；编号 **API-00063**～**API-00074**（父控分配闭区间）。
