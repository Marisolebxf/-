# 智能服务集群-科技专题服务算法库测试用例（产业链基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 产业链基础指标  
> **catalog**：`entry_id=chain.basic` · `catalog_page_id=chain.basic` · path `/chain/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L01.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（50897 试调 2026-10-17）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView 默认 `admin` / `gkx@2026`，密码经 AES-CFB 加密提交）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message`（试调无 token：`HTTP 424`，`code=1`，`msg=token expired`） |
| 断言分工 | **API-00001（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 类型）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00001」后，可只断言 **data 载荷** 或失败态 |
| 试调 chainId | `INB1701`（`GET /innov/v1/industry/list` 试调首条 `chain_id`，可替换） |
| 试调 observed（仅记录，非预期） | `GET /innov/v1/industry/list` → `HTTP 200`，`code=0`，`msg=null`，`data` 为非空数组，元素含 `string` 型 `chain_id`、`chain_name`（样例另有 `industry_code` 等字段，本轮不设失败条件） |
| catalog 与现场 | live endpoint 以 catalog `status=available` 为准；`unavailable` 三类（机构规模/全球分布/动态资讯）仅契约占位，禁止将 sampleResponse 数值写入通过条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.basic`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00001 | 基础指标 | 产业链基础指标 | 主流程-列表成功 | 金样信封 | 产业链基础指标 | 产业链列表 | 产业链列表在有效鉴权下返回成功信封与产业标识字段 | 1、已按 §0 取得有效 token 与租户头；2、断言对象为完整原始响应信封 | 1.GET /innov/v1/industry/list（无查询参数） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 string 型 chain_id 与 chain_name | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/list | | INTEG | | | endpoint_id=chain.basic.list catalog_page_id=chain.basic 组合=— 金样 50897试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00002 | 基础指标 | 产业链基础指标 | 异常-鉴权 | 缺Token | 产业链基础指标 | 产业链列表 | 产业链列表缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/industry/list（无查询参数），skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务列表载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/list | | INTEG | | | endpoint_id=chain.basic.list catalog_page_id=chain.basic 组合=—；全页其它 endpoint 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00003 | 基础指标 | 产业链基础指标 | 主流程-市场规模 | 全参查询 | 产业链基础指标 | A1 产业市场规模 | 市场规模接口在合法 chainId 与 statYear 下返回 total_revenue 字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-00001 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 number 型 total_revenue | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | M_CHAIN_MARKET_SIZE | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00004 | 基础指标 | 产业链基础指标 | 异常-缺必填chainId | 市场规模 | 产业链基础指标 | A1 产业市场规模 | 市场规模接口缺少 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空数组冒充有规模数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00005 | 基础指标 | 产业链基础指标 | 异常-非法chainId | 市场规模 | 产业链基础指标 | A1 产业市场规模 | 市场规模接口 chainId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/market-stats，查询参数取组合 MKT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 非空；3、不得将失败当作含可信 total_revenue 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/market-stats | | INTEG | | | endpoint_id=chain.basic.market-stats catalog_page_id=chain.basic 组合=MKT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00006 | 基础指标 | 产业链基础指标 | 主流程-企业规模 | 全参查询 | 产业链基础指标 | A2 产业企业规模 | 企业规模接口在合法 chainId 下返回 enterprise_count 字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-00001 | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 number 型 enterprise_count | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | M_CHAIN_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00007 | 基础指标 | 产业链基础指标 | 异常-缺必填chainId | 企业规模 | 产业链基础指标 | A2 产业企业规模 | 企业规模接口缺少 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空数组冒充有企业规模 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00008 | 基础指标 | 产业链基础指标 | 异常-非法chainId | 企业规模 | 产业链基础指标 | A2 产业企业规模 | 企业规模接口 chainId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/enterprise-stats，查询参数取组合 ENT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 enterprise_count 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/enterprise-stats | | INTEG | | | endpoint_id=chain.basic.enterprise-stats catalog_page_id=chain.basic 组合=ENT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00009 | 基础指标 | 产业链基础指标 | 契约-不可用 | 机构规模 | 产业链基础指标 | A3 产业机构规模 | catalog 不可用态下机构规模接口不得按 live 成功数值验收 | 1、已确认 catalog `chain.basic.institution-stats` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/institution-stats，查询参数取组合 INS-01 | 1、不得将 unavailable 接口的 sampleResponse 机构数/增长率数值作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built 与 catalog 偏差 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/institution-stats | | INTEG | | | endpoint_id=chain.basic.institution-stats catalog_page_id=chain.basic 组合=INS-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00010 | 基础指标 | 产业链基础指标 | 主流程-投融资规模 | 全参查询 | 产业链基础指标 | A4 产业投融资规模 | 投融资规模接口在合法 chainId 下返回 total_amount 字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-00001 | 1.GET /innov/v1/industry/investment-stats，查询参数取组合 INV-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 number 型 total_amount | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats | | INTEG | | | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00011 | 基础指标 | 产业链基础指标 | 异常-缺必填chainId | 投融资规模 | 产业链基础指标 | A4 产业投融资规模 | 投融资规模接口缺少 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/investment-stats，查询参数取组合 INV-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空数组冒充有投融资数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats | | INTEG | | | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00012 | 基础指标 | 产业链基础指标 | 异常-非法chainId | 投融资规模 | 产业链基础指标 | A4 产业投融资规模 | 投融资规模接口 chainId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/investment-stats，查询参数取组合 INV-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 total_amount 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/investment-stats | | INTEG | | | endpoint_id=chain.basic.investment-stats catalog_page_id=chain.basic 组合=INV-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00013 | 基础指标 | 产业链基础指标 | 契约-不可用 | 全球分布 | 产业链基础指标 | A5 全球产业区域分布 | catalog 不可用态下全球分布接口不得按 live 成功数值验收 | 1、已确认 catalog `chain.basic.global-dist` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/global-dist，查询参数取组合 GLO-01 | 1、不得将 sampleResponse 国家/企业数等数值作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/global-dist | | INTEG | | | endpoint_id=chain.basic.global-dist catalog_page_id=chain.basic 组合=GLO-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00014 | 基础指标 | 产业链基础指标 | 主流程-全国分布 | 全参查询 | 产业链基础指标 | A6 全国产业分布 | 全国分布接口在合法 chainId 下返回 province 维度字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-00001 | 1.GET /innov/v1/industry/national-dist，查询参数取组合 NAT-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 string 型 province | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist | | INTEG | | | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00015 | 基础指标 | 产业链基础指标 | 异常-缺必填chainId | 全国分布 | 产业链基础指标 | A6 全国产业分布 | 全国分布接口缺少 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/national-dist，查询参数取组合 NAT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空数组冒充有省级分布 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist | | INTEG | | | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00016 | 基础指标 | 产业链基础指标 | 异常-非法chainId | 全国分布 | 产业链基础指标 | A6 全国产业分布 | 全国分布接口 chainId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/national-dist，查询参数取组合 NAT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 province 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/national-dist | | INTEG | | | endpoint_id=chain.basic.national-dist catalog_page_id=chain.basic 组合=NAT-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00017 | 基础指标 | 产业链基础指标 | 契约-不可用 | 动态资讯 | 产业链基础指标 | A7 产业动态资讯 | catalog 不可用态下资讯统计接口不得按 live 成功数值验收 | 1、已确认 catalog `chain.basic.news-stats` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/news-stats，查询参数取组合 NEW-01 | 1、不得将 sampleResponse 资讯数/热点数作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/news-stats | | INTEG | | | endpoint_id=chain.basic.news-stats catalog_page_id=chain.basic 组合=NEW-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00018 | 基础指标 | 产业链基础指标 | 主流程-深圳要素 | 全参查询 | 产业链基础指标 | A8 深圳产业要素 | 深圳要素接口在合法 chainId 下返回企业与机构计数字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-00001 | 1.GET /innov/v1/industry/sz-elements，查询参数取组合 SZE-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象或数组；4、载荷中含 number 型 enterprise_count 与 institution_count | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements | M_CHAIN_SZ_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00019 | 基础指标 | 产业链基础指标 | 异常-缺必填chainId | 深圳要素 | 产业链基础指标 | A8 深圳产业要素 | 深圳要素接口缺少 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/sz-elements，查询参数取组合 SZE-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空对象冒充有要素数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements | | INTEG | | | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00020 | 基础指标 | 产业链基础指标 | 异常-非法chainId | 深圳要素 | 产业链基础指标 | A8 深圳产业要素 | 深圳要素接口 chainId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/sz-elements，查询参数取组合 SZE-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 enterprise_count/institution_count 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-elements | | INTEG | | | endpoint_id=chain.basic.sz-elements catalog_page_id=chain.basic 组合=SZE-03 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00021 | 基础指标 | 产业链基础指标 | 主流程-深圳分布 | 全参查询 | 产业链基础指标 | A9 深圳产业分布 | 深圳分布接口在合法 chainId 下返回 district 维度字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-00001 | 1.GET /innov/v1/industry/sz-dist，查询参数取组合 SZD-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 string 型 district | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist | M_CHAIN_SZ_ENTERPRISE_COUNT | INTEG | | | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00022 | 基础指标 | 产业链基础指标 | 异常-缺必填chainId | 深圳分布 | 产业链基础指标 | A9 深圳产业分布 | 深圳分布接口缺少 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/sz-dist，查询参数取组合 SZD-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空数组冒充有区级分布 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist | | INTEG | | | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00023 | 基础指标 | 产业链基础指标 | 异常-非法chainId | 深圳分布 | 产业链基础指标 | A9 深圳产业分布 | 深圳分布接口 chainId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/industry/sz-dist，查询参数取组合 SZD-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 district 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/sz-dist | | INTEG | | | endpoint_id=chain.basic.sz-dist catalog_page_id=chain.basic 组合=SZD-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MKT-01 | chain.basic.market-stats | chainId=INB1701（§0 试调有效值，可替换）；statYear=2025 | 主路径全参 |
| MKT-02 | chain.basic.market-stats | 不传 chainId；statYear=2025 | 缺必填 chainId |
| MKT-03 | chain.basic.market-stats | chainId=__invalid__；不传 statYear | 非法 id + 省略可选 statYear |
| ENT-01 | chain.basic.enterprise-stats | chainId=INB1701；statYear=2025 | 主路径全参 |
| ENT-02 | chain.basic.enterprise-stats | 不传 chainId；statYear=2025 | 缺必填 chainId |
| ENT-03 | chain.basic.enterprise-stats | chainId=__invalid__ | 非法 chainId |
| INS-01 | chain.basic.institution-stats | chainId=INB1701 | unavailable 契约占位 |
| INV-01 | chain.basic.investment-stats | chainId=INB1701 | 主路径 |
| INV-02 | chain.basic.investment-stats | 不传 chainId | 缺必填 chainId |
| INV-03 | chain.basic.investment-stats | chainId=__invalid__ | 非法 chainId |
| GLO-01 | chain.basic.global-dist | chainId=INB1701 | unavailable 契约占位 |
| NAT-01 | chain.basic.national-dist | chainId=INB1701 | 主路径 |
| NAT-02 | chain.basic.national-dist | 不传 chainId | 缺必填 chainId |
| NAT-03 | chain.basic.national-dist | chainId=__invalid__ | 非法 chainId |
| NEW-01 | chain.basic.news-stats | chainId=INB1701 | unavailable 契约占位 |
| SZE-01 | chain.basic.sz-elements | chainId=INB1701 | 主路径 |
| SZE-02 | chain.basic.sz-elements | 不传 chainId | 缺必填 chainId |
| SZE-03 | chain.basic.sz-elements | chainId=__invalid__ | 非法 chainId |
| SZD-01 | chain.basic.sz-dist | chainId=INB1701 | 主路径 |
| SZD-02 | chain.basic.sz-dist | 不传 chainId | 缺必填 chainId |
| SZD-03 | chain.basic.sz-dist | chainId=__invalid__ | 非法 chainId |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.basic.list | GET | /innov/v1/industry/list | available | — |
| chain.basic.market-stats | GET | /innov/v1/industry/market-stats | available | chainId |
| chain.basic.enterprise-stats | GET | /innov/v1/industry/enterprise-stats | available | chainId |
| chain.basic.institution-stats | GET | /innov/v1/industry/institution-stats | unavailable | chainId |
| chain.basic.investment-stats | GET | /innov/v1/industry/investment-stats | available | chainId |
| chain.basic.global-dist | GET | /innov/v1/industry/global-dist | unavailable | chainId |
| chain.basic.national-dist | GET | /innov/v1/industry/national-dist | available | chainId |
| chain.basic.news-stats | GET | /innov/v1/industry/news-stats | unavailable | chainId |
| chain.basic.sz-elements | GET | /innov/v1/industry/sz-elements | available | chainId |
| chain.basic.sz-dist | GET | /innov/v1/industry/sz-dist | available | chainId |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.basic.list | API-00001、API-00002 |
| chain.basic.market-stats | API-00003、API-00004、API-00005 |
| chain.basic.enterprise-stats | API-00006、API-00007、API-00008 |
| chain.basic.institution-stats | API-00009 |
| chain.basic.investment-stats | API-00010、API-00011、API-00012 |
| chain.basic.global-dist | API-00013 |
| chain.basic.national-dist | API-00014、API-00015、API-00016 |
| chain.basic.news-stats | API-00017 |
| chain.basic.sz-elements | API-00018、API-00019、API-00020 |
| chain.basic.sz-dist | API-00021、API-00022、API-00023 |

---

## 3. 覆盖自检

- [x] 各 live endpoint 至少 1 条 P0 主路径
- [x] unavailable endpoint 已写契约占位（API-00009、00013、00017）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（无稳定空数据构造）
- [x] 金样 1 条且断言完整信封（API-00001）
- [x] 50897 试调 1 条主路径（产业链列表，§0）
- [x] `coverage-fp.md` 已更新
- [x] `code-registry.yaml` 已回写 API-00001～00023

**统计**：用例 **23** 条；编号 **API-00001**～**API-00023**（父控分配闭区间 00001～00050 内）。
