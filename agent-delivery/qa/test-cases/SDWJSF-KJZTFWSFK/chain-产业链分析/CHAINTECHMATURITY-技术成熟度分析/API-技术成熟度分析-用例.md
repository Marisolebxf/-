# 智能服务集群-科技专题服务算法库测试用例（技术成熟度分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 技术成熟度分析  
> **catalog**：`entry_id=chain.tech-maturity` · `catalog_page_id=chain.tech-maturity` · path `/chain/tech-maturity`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/chain.json` 页 `chain.tech-maturity`  
> **A 线对照**：`fp-split-by-api-run/work/L*.md` 检索 `chain.tech-maturity` **无六级对应**（`_l6-to-catalog-map.yaml`：60 条无对应六级；覆盖矩阵见 `coverage-fp.md`，状态 **待 A 线合表核对**）  
> **环境**：`http://111.198.38.90:50897/`（联调台 hash `#/chain/tech-maturity`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（未试调）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | `GET /innov/v1/industry/{chainId}/tech-maturity`（path 变量 `chainId`） |
| 鉴权头 | `Authorization: Bearer <token>`（50897 登录页换取）；`TENANT-ID: 1`（与联调台默认租户一致，执行期以现场为准） |
| 信封成功码 | `code` ∈ {`0`, `"0"`, `200`, `"200"`} |
| 鉴权失败 | HTTP **401** 或 **424** |
| 断言分工 | **API-00399（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 类型）；同册其余用例在前置写「信封规则见 §0，金样见 API-00399」后，可只断言失败态或载荷形态 |
| catalog 口径 | `chain.tech-maturity.main` 的 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中成熟度评分 70、「趋于成熟」、`stage`、年度 `patent_count` 等示例数值作为通过条件 |
| 试调记录 | **未试调**（父控宣布；本会话禁止 curl / 浏览器 / 50897 无头 HTTP；有效鉴权主路径待 S3 执行期复核） |
| 本页 endpoint 数 | **1**（`chain.tech-maturity.main`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00399`～`00403`（父控闭区间）。`路由route` = path 模板；`备注` 含 `endpoint_id`、`catalog_page_id`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00399 | 产业链分析 | 技术成熟度分析 | 契约-不可用 | 技术成熟度模型 | 技术成熟度分析 | 技术成熟度 | catalog 不可用态下带鉴权请求是否可识别非 live 成功 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 变量取组合 TM-01 | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得仅凭 sample 形态将 unavailable 接口判为 live 成功（不得以固定成熟度分或阶段名为通过条件）；4、若 code 属成功集合则 data 形态须在执行期记录且不得当作已接通生产技术成熟度判定（须与 §0 unavailable 一致） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity |  | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TM-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00400 | 产业链分析 | 技术成熟度分析 | 异常-鉴权 | 技术成熟度模型 | 技术成熟度分析 | 技术成熟度 | 技术成熟度接口缺 Bearer 时是否返回鉴权失败 | 1、请求故意不携带 Authorization；2、可携带 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 变量取组合 TM-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、message 或 msg 非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity |  | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00401 | 产业链分析 | 技术成熟度分析 | 异常-非法chainId | 技术成熟度模型 | 技术成熟度分析 | 技术成熟度 | 非法 chainId 时是否返回可识别失败而非伪成熟度结果 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 变量取组合 TM-02 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得返回含可信 tech_maturity_score 或 trend 的成功业务体冒充合法成熟度分析 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity |  | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TM-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00402 | 产业链分析 | 技术成熟度分析 | 契约-字段形态 | 技术成熟度模型 | 技术成熟度分析 | 技术成熟度 | 成功信封下 tech_maturity_score 若存在是否仅为 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00399 | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 变量取组合 TM-01 | 1、若 code 属成功集合且 data 为对象，则 tech_maturity_score 存在时为 number；2、不得以 sample 中 70 等具体评分为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity |  | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TM-01；矩阵挂 tech_maturity_score |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00403 | 产业链分析 | 技术成熟度分析 | 契约-字段形态 | 技术成熟度模型 | 技术成熟度分析 | 技术成熟度 | 成功信封下 trend 若存在是否仅为 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00399 | 1.GET /innov/v1/industry/{chainId}/tech-maturity，path 变量取组合 TM-01 | 1、若 code 属成功集合且 data 为对象，则 trend 存在时为 array；2、不得以 sample 中年度专利量或条数为通过条件；3、空数组须与 _fail 区分（执行期记录） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/{chainId}/tech-maturity |  | INTEG |  |  | endpoint_id=chain.tech-maturity.main catalog_page_id=chain.tech-maturity 组合=TM-01；矩阵挂 trend |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TM-01 | chain.tech-maturity.main | path `chainId=INB170101`（catalog `params.example`，执行期可替换为试调有效 id） | 契约主路径（unavailable） |
| TM-02 | chain.tech-maturity.main | path `chainId=__invalid__` | 非法产业标识 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | catalog status | 必填参数 |
|-------------|--------|------|----------------|----------|
| chain.tech-maturity.main | GET | /innov/v1/industry/{chainId}/tech-maturity | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.tech-maturity.main | API-00399、API-00400、API-00401、API-00402、API-00403 |

---

## 3. 覆盖自检（§I）

- [x] 本页 **0** 条 FUNC
- [x] unavailable endpoint 契约占位 + 金样信封（API-00399）
- [x] 异常-鉴权 1 条（API-00400）
- [x] 入参单缺陷非法 chainId（API-00401，矩阵挂 `_fail`）
- [x] catalog `responseFields` 形态 2 条（API-00402、00403）
- [x] `_empty` 无稳定构造 → 矩阵 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [x] §0 标注 **未试调**；未 curl / 未改 code-registry（父控约束）

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **5**（00399～00403） |
| catalog endpoint 数 | **1** |
| 金样（完整信封） | **1**（API-00399） |
| 异常-鉴权 | **1**（API-00400） |
| `_empty`（契约行） | **1** 行 **未覆盖** |
| code-registry 回写 | **父控**（本子任务未改） |
| A 线六级 | **无对应**；矩阵键按 B 线 `endpoint_id` + catalog field，状态 **待 A 线合表核对** |
| 试调 | **未试调**（§0） |
