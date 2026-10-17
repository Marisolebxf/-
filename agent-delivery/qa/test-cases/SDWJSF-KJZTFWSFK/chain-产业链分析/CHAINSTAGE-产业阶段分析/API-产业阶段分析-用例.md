# 智能服务集群-科技专题服务算法库测试用例（产业阶段分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业阶段分析  
> **catalog**：`entry_id=chain.stage` · `catalog_page_id=chain.stage` · path `/chain/stage`  
> **A 线对照**：`fp-split-by-api-run/work/L20.md`（覆盖矩阵见 `coverage-fp.md`；矩阵键仅 grep L20，未读本六级 work 全文）  
> **环境**：`http://111.198.38.90:50897/`（联调台 hash `#/chain/stage`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（未试调）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /innov/v1/industry/{chainId}/cycle`（path 变量 `chainId`；与 `chain.cycle` 页 **同 path**，以 `endpoint_id=chain.stage.main` 区分验收语义） |
| 鉴权头 | `Authorization: Bearer <token>`（50897 登录页换取）；`TENANT-ID: 1`（与联调台默认租户一致，执行期以现场为准） |
| 信封成功码 | `code` ∈ {`0`, `"0"`, `200`, `"200"`} |
| 断言分工 | **API-00340（金样）** 断言 **完整信封**（HTTP + `code` + `data` 类型）；同册其余用例在前置引用金样后，可只断言失败态或 HTTP |
| catalog 口径 | `chain.stage.main` 的 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中「成长期」「加速扩张」、营收等数值作为通过条件 |
| 试调记录 | **未试调**（父控宣布；本会话禁止 curl / 50897 无头 HTTP；有效鉴权主路径待 S3 执行期复核） |
| 本页 endpoint 数 | **1**（`chain.stage.main`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00340`～`00349`（父控闭区间）。`路由route` = path 模板；`备注` 含 `endpoint_id`、`catalog_page_id`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00340 | 产业链分析 | 产业阶段分析 | 契约-不可用 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | catalog 不可用态下带鉴权请求是否可识别非 live 成功 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 STG-01 | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得仅凭 sample 形态将 unavailable 接口判为 live 成功（不得以固定「成长期」等样例数值为通过条件）；4、若 code 属成功集合则 data 不得被当作已接通生产阶段判定（须与 §0 unavailable 一致，执行期记录形态） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00341 | 产业链分析 | 产业阶段分析 | 异常-鉴权 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 产业阶段分析接口缺 Bearer 时是否返回鉴权失败 | 1、请求故意不携带 Authorization；2、可携带 TENANT-ID | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 STG-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、message 或 msg 非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00342 | 产业链分析 | 产业阶段分析 | 异常-鉴权 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 产业阶段分析接口缺 TENANT-ID 时是否拒绝或返回可识别失败 | 1、已携带 Authorization Bearer；2、故意不携带 TENANT-ID | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 STG-01 | 1、HTTP 状态为 4xx 或响应 code 不属于成功集合；2、不得将缺租户当作含可信 cycle_stage 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00343 | 产业链分析 | 产业阶段分析 | 异常-鉴权 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 无效 Bearer 时产业阶段接口是否返回鉴权失败 | 1、Authorization 为明显无效 token；2、可携带 TENANT-ID: 1 | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 STG-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 stage.sub_stage 的成功业务载荷 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00344 | 产业链分析 | 产业阶段分析 | 异常-非法chainId | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 非法 chainId 时是否返回可识别失败而非伪阶段 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/__invalid__/cycle，path 变量取组合 STG-02 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得返回含可信 cycle.cycle_stage 或 stage.sub_stage 枚举的成功业务体冒充合法判定 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00345 | 产业链分析 | 产业阶段分析 | 异常-path占位非法 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | path 中 chainId 为空占位时是否可识别入参错误 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//cycle（chainId 段为空），取组合 STG-03 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得将路由错误当作空阶段成功 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-03；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00346 | 产业链分析 | 产业阶段分析 | 异常-非法chainId | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | chainId 仅空白字符时是否可识别入参错误 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/%20/cycle（path 变量为单空格，取组合 STG-04） | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得返回含 stage 判定语义的成功业务体 | P2 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00347 | 产业链分析 | 产业阶段分析 | 契约-字段形态 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 成功信封下 cycle.cycle_stage 若存在是否仅为 string 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00340 | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 STG-01 | 1、若 code 属成功集合且 data 为对象并含 cycle 体，则 cycle.cycle_stage 存在时为 string；2、不得以 sample 中具体中文阶段名为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01；矩阵挂 cycle.cycle_stage；catalog responseFields |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00348 | 产业链分析 | 产业阶段分析 | 契约-字段形态 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 成功信封下 stage.sub_stage 若存在是否仅为 string 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00340 | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 STG-01 | 1、若 code 属成功集合且 data 为对象并含 stage 体，则 stage.sub_stage 存在时为 string；2、不得以 sample 中「加速扩张」等具体子阶段名为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01；矩阵挂 stage.sub_stage |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00349 | 产业链分析 | 产业阶段分析 | 异常-错误方法 | 产业阶段分析模型 | 产业阶段分析 | 产业阶段分析 | 对阶段查询 path 使用 POST 时是否返回可识别错误 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /innov/v1/industry/INB1701/cycle（无 body 或空 JSON），取组合 STG-01 | 1、HTTP 状态为 4xx 或 405；2、不得将错误方法当作 GET 成功阶段判定 data | P2 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.7 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.stage.main catalog_page_id=chain.stage 组合=STG-01；矩阵挂 _fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| STG-01 | chain.stage.main | path `chainId=INB1701`（catalog example，执行期可替换为试调有效 id） | 契约主路径（unavailable） |
| STG-02 | chain.stage.main | path `chainId=__invalid__` | 非法产业标识 |
| STG-03 | chain.stage.main | path 段为空：`/innov/v1/industry//cycle` | 缺失 path 变量语义 |
| STG-04 | chain.stage.main | path `chainId=` 单空格（URL 编码 `%20`） | 空白 chainId 单缺陷 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | catalog status | 必填参数 |
|-------------|--------|------|----------------|----------|
| chain.stage.main | GET | /innov/v1/industry/{chainId}/cycle | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.stage.main | API-00340、API-00341、API-00342、API-00343、API-00344、API-00345、API-00346、API-00347、API-00348、API-00349 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-00340），未写 sample 数值通过条件
- [x] 鉴权异常 3 条（API-00341～00343）
- [x] 入参单缺陷 3 条（API-00344～00346）
- [x] responseFields 形态 2 条（API-00347、00348）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [x] 金样 1 条且断言信封（API-00340）
- [x] 本页 0 条 FUNC
- [x] §0 标注 **未试调**；未 curl / 未改 code-registry（父控约束）
