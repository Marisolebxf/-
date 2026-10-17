# 智能服务集群-科技专题服务算法库测试用例（产业周期分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业周期分析  
> **catalog**：`entry_id=chain.cycle` · `catalog_page_id=chain.cycle` · path `/chain/cycle`  
> **A 线对照**：`fp-split-by-api-run/work/L19.md`（覆盖矩阵见 `coverage-fp.md`）  
> **环境**：`http://111.198.38.90:50897/`（联调台 hash `#/chain/cycle`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §A～I  
> **维护人**：qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（试调后填写）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`/innov/v1/industry/{chainId}/cycle`（path 变量 `chainId`，非 query） |
| 鉴权头 | `Authorization: Bearer <token>`（50897 登录页换取）；`TENANT-ID: 1`（与联调台默认租户一致，执行期以现场为准） |
| 信封成功码 | `code` ∈ {`0`, `"0"`, `200`, `"200"`} |
| 断言分工 | **API-00055（金样）** 断言 **完整信封**（HTTP + `code` + `data` 类型）；同册其余用例在前置引用金样后，可只断言失败态或 HTTP |
| catalog 口径 | `chain.cycle.main` 的 catalog `status=unavailable`；**禁止**将 `sampleResponse` 中「成长期」、营收等数值作为通过条件 |
| 试调记录 | **2026-10-17** 主路径 1 次（无 Bearer）：`GET /api/innov/v1/industry/INB1701/cycle` + `TENANT-ID: 1` → **HTTP 424**，体 `code=1`，`msg` 含 `token expired`。**有效鉴权下主路径本轮未再试调**（按子任务约束不重试） |
| 本页 endpoint 数 | **1**（`chain.cycle.main`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00055`～`00058`。`路由route` = catalog path 模板；`备注` 含 `endpoint_id`、`catalog_page_id`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00055 | 产业链分析 | 产业周期分析 | 契约-不可用 | 产业周期分析模型 | 产业周期分析 | 产业周期分析 | catalog 不可用态下带鉴权请求是否可识别非 live 成功 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 CYCL-01 | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得仅凭 sample 形态将 unavailable 接口判为 live 成功（不得以固定「成长期」等样例数值为通过条件）；4、若 code 属成功集合则 data 不得被当作已接通生产周期判定（须与 §0 unavailable 一致，执行期记录形态） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.6 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.cycle.main catalog_page_id=chain.cycle 组合=CYCL-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00056 | 产业链分析 | 产业周期分析 | 异常-鉴权 | 产业周期分析模型 | 产业周期分析 | 产业周期分析 | 产业周期分析接口缺 Bearer 时是否返回鉴权失败 | 1、请求故意不携带 Authorization；2、可携带 TENANT-ID | 1.GET /innov/v1/industry/INB1701/cycle，path 变量取组合 CYCL-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、message 或 msg 非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.6 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.cycle.main catalog_page_id=chain.cycle 组合=CYCL-01；§0 无 token 试调 HTTP 424 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00057 | 产业链分析 | 产业周期分析 | 异常-非法chainId | 产业周期分析模型 | 产业周期分析 | 产业周期分析 | 非法 chainId 时是否返回可识别失败而非伪阶段 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/__invalid__/cycle，path 变量取组合 CYCL-02 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得返回含可信 cycle.cycle_stage 枚举的成功业务体冒充合法判定 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.6 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.cycle.main catalog_page_id=chain.cycle 组合=CYCL-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00058 | 产业链分析 | 产业周期分析 | 异常-path占位非法 | 产业周期分析模型 | 产业周期分析 | 产业周期分析 | path 中 chainId 为空占位时是否可识别入参错误 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//cycle（chainId 段为空），取组合 CYCL-03 | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得将路由错误当作空周期成功 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库 | 1.1.1.1.1.1.1.3.6 | N/A | N/A | /innov/v1/industry/{chainId}/cycle |  | INTEG |  |  | endpoint_id=chain.cycle.main catalog_page_id=chain.cycle 组合=CYCL-03；矩阵挂 chainId、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| CYCL-01 | chain.cycle.main | path `chainId=INB1701`（catalog example，执行期可替换为试调有效 id） | 契约主路径（unavailable） |
| CYCL-02 | chain.cycle.main | path `chainId=__invalid__` | 非法产业标识 |
| CYCL-03 | chain.cycle.main | path 段为空：`/innov/v1/industry//cycle` | 缺失 path 变量语义 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | catalog status | 必填参数 |
|-------------|--------|------|----------------|----------|
| chain.cycle.main | GET | /innov/v1/industry/{chainId}/cycle | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.cycle.main | API-00055、API-00056、API-00057、API-00058 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-00055），未写 sample 数值通过条件
- [x] 鉴权异常 1 条（API-00056）
- [x] 入参单缺陷 2 条（API-00057、API-00058）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [x] 金样 1 条且断言信封（API-00055）
- [x] 本页 0 条 FUNC

**统计**：用例 **4** 条；编号 **API-00055**～**API-00058**。
