# 智能服务集群-科技专题服务算法库测试用例（产业战略重要性分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业战略重要性分析  
> **catalog**：`entry_id=chain.strategic-importance` · `catalog_page_id=chain.strategic-importance` · path `/chain/strategic-importance`  
> **A 线对照**：无六级 `work/Lxx.md`（`_l6-to-catalog-map.yaml` 待合表；覆盖矩阵见 `coverage-fp.md`）  
> **环境**：`http://111.198.38.90:50897/`（联调台 hash `#/chain/strategic-importance`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §方法论 / §细则 / §I / §S1  
> **维护人**：qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（未试调）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /innov/v1/industry/{chainId}/strategic-importance`（path 变量 `chainId`，非 query） |
| 鉴权头 | `Authorization: Bearer <token>`（50897 登录页换取）；`TENANT-ID: 1`（与联调台默认租户一致，执行期以现场为准） |
| 信封成功码 | `code` ∈ {`0`, `"0"`, `200`, `"200"`} |
| 断言分工 | **API-000404（金样）** 断言 **完整信封**（HTTP + `code` + `data` 形态）；同册其余用例可只断言失败态或 HTTP |
| catalog 口径 | `chain.strategic-importance.main` 的 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `importance_score`、`node_name`、`position` 等数值或文案作为通过条件 |
| 试调记录 | **未试调**（子任务约束：§0 不写 curl 观测；有效鉴权主路径待 S3 执行期复核） |
| 本页 endpoint 数 | **1**（`chain.strategic-importance.main`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000404`～`000408`（父控闭区间）。`路由route` = catalog path 模板；`备注` 含 `endpoint_id`、`catalog_page_id`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000404 | 产业链分析 | 产业战略重要性分析 | 契约-不可用 | 产业战略重要性分析模型 | 产业战略重要性分析 | 战略重要性 | catalog 不可用态下带鉴权请求是否可识别非 live 成功 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/INB170101/strategic-importance，path 变量取组合 STRAT-01 | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得仅凭 sample 形态将 unavailable 接口判为 live 成功（不得以固定 importance_score 等样例数值为通过条件）；4、若 code 属成功集合则 data 不得被当作已接通生产战略重要性判定（须与 §0 unavailable 一致，执行期记录形态） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | N/A | N/A | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  |  | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STRAT-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000405 | 产业链分析 | 产业战略重要性分析 | 异常-鉴权 | 产业战略重要性分析模型 | 产业战略重要性分析 | 战略重要性 | 战略重要性接口缺 Bearer 时是否返回鉴权失败 | 1、请求故意不携带 Authorization；2、可携带 TENANT-ID | 1.GET /innov/v1/industry/INB170101/strategic-importance，path 变量取组合 STRAT-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、message 或 msg 非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | N/A | N/A | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  |  | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STRAT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000406 | 产业链分析 | 产业战略重要性分析 | 异常-非法chainId | 产业战略重要性分析模型 | 产业战略重要性分析 | 战略重要性 | 非法 chainId 时是否返回可识别失败而非伪评分 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/__invalid__/strategic-importance，path 变量取组合 STRAT-02 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得返回含可信 rows 环节评分的成功业务体冒充合法判定 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | N/A | N/A | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  |  | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STRAT-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000407 | 产业链分析 | 产业战略重要性分析 | 异常-path占位非法 | 产业战略重要性分析模型 | 产业战略重要性分析 | 战略重要性 | path 中 chainId 为空占位时是否可识别入参错误 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//strategic-importance（chainId 段为空），取组合 STRAT-03 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得将路由错误当作空 rows 成功 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | N/A | N/A | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  |  | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STRAT-03；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000408 | 产业链分析 | 产业战略重要性分析 | 契约-字段形态 | 产业战略重要性分析模型 | 产业战略重要性分析 | 战略重要性 | 成功信封下 rows 若存在是否仅为 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000404 | 1.GET /innov/v1/industry/INB170101/strategic-importance，path 变量取组合 STRAT-01 | 1、若 code 属成功集合且 data 含 rows 字段，则 rows 为 array；2、不得以 sample 中具体环节名或评分数值为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | N/A | N/A | N/A | /innov/v1/industry/{chainId}/strategic-importance |  | INTEG |  |  | endpoint_id=chain.strategic-importance.main catalog_page_id=chain.strategic-importance 组合=STRAT-01；矩阵挂 rows；catalog responseFields |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| STRAT-01 | chain.strategic-importance.main | path `chainId=INB170101`（catalog example，执行期可替换为试调有效 id） | 契约主路径（unavailable） |
| STRAT-02 | chain.strategic-importance.main | path `chainId=__invalid__` | 非法产业标识 |
| STRAT-03 | chain.strategic-importance.main | path 段为空：`/innov/v1/industry//strategic-importance` | 缺失 path 变量语义 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | catalog status | 必填参数 |
|-------------|--------|------|----------------|----------|
| chain.strategic-importance.main | GET | /innov/v1/industry/{chainId}/strategic-importance | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.strategic-importance.main | API-000404、API-000405、API-000406、API-000407、API-000408 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-000404），未写 sample 数值通过条件
- [x] 鉴权异常 1 条（API-000405）
- [x] 入参单缺陷 2 条（API-000406、API-000407）
- [x] responseFields `rows` 形态 1 条（API-000408）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [x] 金样 1 条且断言信封（API-000404）
- [x] 本页 0 条 FUNC
- [x] §0 标注 **未试调**；未 curl / 未改 code-registry、run-log（子任务约束）

**统计**：用例 **5** 条；编号 **API-000404**～**API-000408**。
