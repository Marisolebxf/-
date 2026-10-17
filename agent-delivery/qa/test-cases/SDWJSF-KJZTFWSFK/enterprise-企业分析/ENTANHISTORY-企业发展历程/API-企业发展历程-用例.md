# 智能服务集群-科技专题服务算法库测试用例（企业发展历程 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业发展历程  
> **catalog**：`entry_id=entan.history` · `catalog_page_id=entan.history` · path `/entan/history`  
> **A 线对照**：`fp-split-by-api-run/work/L28.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 成功 code 集合 | `0`、`"0"`、`200`、`"200"` |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 鉴权头 | `Authorization: Bearer <access_token>`（OAuth 密码模式，账号口径同 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 试调 | 本轮 **未试调**（父控宣布；本子任务禁止 curl）；执行期按金样步骤复核 |
| 断言分工 | **API-00085（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 可解析形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00085」后可只断言失败/不可用/入参错误态 |
| catalog 状态 | 本页 **2** 个 endpoint 均为 `status=unavailable`；**禁止**将 `sampleResponse` 中 `enterprise_name`、`org_id`、`timeline` 内 revenue/patent 等数值或文案作为通过条件 |
| 样例 org_id | `demo-org-sz-active-listed`（catalog `entan.history.timeline` example，执行期可替换） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.history`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00085 | 企业分析 | 企业发展历程 | 契约-不可用 | 金样信封 | 企业发展历程 | 企业搜索 | catalog 不可用态下企业搜索接口信封可解析且非 live 样例验收 | 1、已确认 catalog `entan.history.enterprises` 为 unavailable；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体含可解析的 code 与 message 或 msg；3、不得将 sampleResponse 中 org_id、enterprise_name 作为通过条件；4、若 code 属成功集合则 data 须为数组或约定载荷形态，且不得以固定样例企业名称判为已接通生产搜索 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00086 | 企业分析 | 企业发展历程 | 异常-鉴权 | 缺Token | 企业发展历程 | 企业搜索 | 企业搜索接口无 token 时网关拒绝访问 | 1、请求不携带 Authorization | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-01，无 Authorization 头 | 1、HTTP 状态为 401 或 424；2、响应体可辨认为鉴权失败（非成功业务企业列表载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-01；全页 timeline 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00087 | 企业分析 | 企业发展历程 | 备选-关键词检索 | 全可选参 | 企业发展历程 | 企业搜索 | 企业搜索在 keyword 与 limit 组合下返回可识别契约态 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00085 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-02 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 可解析；3、不得将样例配对 org_id/enterprise_name 数值化验收；4、失败态不得冒充空搜索成功列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-02；矩阵挂 keyword、limit |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00088 | 企业分析 | 企业发展历程 | 异常-非法limit | 企业搜索 | 企业发展历程 | 企业搜索 | 企业搜索 limit 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 非空或 HTTP 明示客户端错误；3、不得将失败当作含 org_id 的成功命中列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00089 | 企业分析 | 企业发展历程 | 异常-空关键词 | 企业搜索 | 企业发展历程 | 企业搜索 | 企业搜索不传 keyword 时契约可识别（拒绝或空结果其一） | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-04 | 1、响应可识别为拒绝、空结果集或不可用契约态之一；2、不得与网关鉴权失败混淆；3、若 code 成功且 data 为空数组，须与含 org_id 命中列表区分 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-04；矩阵挂 keyword、_empty |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00090 | 企业分析 | 企业发展历程 | 契约-不可用 | 发展历程 | 企业发展历程 | 发展历程 | catalog 不可用态下发展历程接口不得按 live 时间线数值验收 | 1、已确认 catalog `entan.history.timeline` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/history，查询参数取组合 HIS-01 | 1、不得将 sampleResponse 中 timeline 事件标题、revenue、patent 计数等作为通过条件；2、响应须为可识别未交付、占位或失败语义，或执行期记录 as-built；3、不得将失败当作空 timeline 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00091 | 企业分析 | 企业发展历程 | 异常-缺必填org_id | 发展历程 | 企业发展历程 | 发展历程 | 发展历程接口缺少 org_id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/history，查询参数取组合 HIS-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作合法 org_id 下空 timeline 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-02；矩阵挂 org_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00092 | 企业分析 | 企业发展历程 | 异常-非法org_id | 发展历程 | 企业发展历程 | 发展历程 | 发展历程接口 org_id 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/history，查询参数取组合 HIS-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 非空或 HTTP 明示错误；3、不得将失败当作空 timeline 冒充无事件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-03；矩阵挂 org_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00093 | 企业分析 | 企业发展历程 | 备选-全参占位 | 发展历程 | 企业发展历程 | 发展历程 | 发展历程在 catalog example org_id 下契约态可识别 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00085 | 1.GET /entan/v1/history，查询参数取组合 HIS-01 | 1、HTTP 与 code 可解析；2、若断言 data 为对象则须含 timeline 字段或约定空结构，类型与 catalog responseFields 一致（array）；3、禁止以样例事件条数或年份作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-01；矩阵挂 timeline |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00094 | 企业分析 | 企业发展历程 | 异常-越界limit | 企业搜索 | 企业发展历程 | 企业搜索 | 企业搜索 limit 越界时返回可识别失败或截断契约 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）或按契约可识别的截断语义；2、不得静默返回超上限条数且冒充全量成功 | P2 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ENT-01 | entan.history.enterprises | keyword=（空）；limit=1（catalog sampleRequest） | 契约占位主路径 |
| ENT-02 | entan.history.enterprises | keyword=云启；limit=5 | keyword+limit 联动 |
| ENT-03 | entan.history.enterprises | keyword=测试；limit=-1 | 非法 limit |
| ENT-04 | entan.history.enterprises | 不传 keyword；limit=10 | 空/缺 keyword 策略 |
| ENT-05 | entan.history.enterprises | keyword=科技；limit=100000 | limit 越界 |
| HIS-01 | entan.history.timeline | org_id=demo-org-sz-active-listed（§0 样例，可替换） | 契约占位全参 |
| HIS-02 | entan.history.timeline | 不传 org_id | 缺必填 org_id |
| HIS-03 | entan.history.timeline | org_id=__invalid__ | 非法 org_id |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.history.enterprises | GET | /entan/v1/enterprises | unavailable | —（keyword、limit 均为可选） |
| entan.history.timeline | GET | /entan/v1/history | unavailable | org_id |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.history.enterprises | API-00085、API-00086、API-00087、API-00088、API-00089、API-00094 |
| entan.history.timeline | API-00090、API-00091、API-00092、API-00093 |

---

## 3. 覆盖自检

- [x] 本页 0 条 FUNC
- [x] 两个 unavailable endpoint 均已写契约占位（API-00085、API-00090）
- [x] 异常-鉴权 1 条（API-00086）
- [x] timeline 缺必填与非法 org_id（API-00091、API-00092）
- [x] ≥1 条备注含 `金样` 且断言完整信封（API-00085）
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-00085～API-00094）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **10** |
| 编号闭区间 | **API-00085**～**API-00094** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
