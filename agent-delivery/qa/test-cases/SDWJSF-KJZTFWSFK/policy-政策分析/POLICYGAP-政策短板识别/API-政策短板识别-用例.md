# 智能服务集群-科技专题服务算法库测试用例（政策短板识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策短板识别  
> **catalog**：`entry_id=policy.gap` · `catalog_page_id=policy.gap` · path `/policy/gap`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.gap` · endpoint `policy.gap.shortboard`  
> **A 线对照**：`fp-split-by-api-run/work/L38.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /policy/v1/policy/analysis/gap`（查询参数 `scope_code`、`limit`，均为可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000469（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`policy.gap.shortboard`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 shortboard_cnt（如 9、7、6）、scope_name（如「汕尾市」）等示例作为通过条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000469`～`000473`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000469 | 政策分析 | 政策短板识别 | 契约-不可用 | 政策短板识别模型 | 政策短板识别 | 短板分析 | catalog 不可用态下短板分析接口可识别非 live 成功 | 1、已确认 catalog `policy.gap.shortboard` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 shortboard_cnt 或区域名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产短板分析判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.4 | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | M_POLICY_SHORTBOARD_COUNT | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000470 | 政策分析 | 政策短板识别 | 异常-鉴权 | 政策短板识别模型 | 政策短板识别 | 短板分析 | 短板分析接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 shortboard_cnt 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.4 | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000471 | 政策分析 | 政策短板识别 | 异常-非法scope_code | 政策短板识别模型 | 政策短板识别 | 短板分析 | 不存在或非法 scope_code 时返回可识别失败而非空短板成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无短板空结果或伪 shortboard_cnt 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.4 | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-02；矩阵挂 scope_code、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000472 | 政策分析 | 政策短板识别 | 异常-非法limit | 政策短板识别模型 | 政策短板识别 | 短板分析 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.4 | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000473 | 政策分析 | 政策短板识别 | 契约-字段形态 | 政策短板识别模型 | 政策短板识别 | 短板分析 | 成功信封下契约出参 shortboard_cnt 若存在是否符合 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000469 | 1.GET /policy/v1/policy/analysis/gap，查询参数取组合 GAP-01 | 1、若 code 属成功集合且载荷含 shortboard_cnt（含列表元素内或 rows 内），则 shortboard_cnt 为 number；2、不得以 sample 中 9/7/6 等具体计数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.4 | N/A-技术项 | N/A | /policy/v1/policy/analysis/gap | M_POLICY_SHORTBOARD_COUNT | INTEG | | | endpoint_id=policy.gap.shortboard catalog_page_id=policy.gap 组合=GAP-01；矩阵挂 shortboard_cnt |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GAP-01 | policy.gap.shortboard | 不传 `scope_code`（全省/默认范围）；`limit=20`（对齐 catalog sampleRequest） | 契约主路径（unavailable） |
| GAP-02 | policy.gap.shortboard | `scope_code=__invalid__`；`limit=20` | 非法/不存在范围编码 |
| GAP-03 | policy.gap.shortboard | `limit=0`（scope_code 不传或空） | 非正整数条数上限 |
| GAP-04 | policy.gap.shortboard | `scope_code=999999`；`limit=20` | 合法形态但可能不存在的省市区编码；**本轮无独立用例**，语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.gap.shortboard | GET | /policy/v1/policy/analysis/gap | unavailable | scope_code、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.gap.shortboard | API-000469、API-000470、API-000471、API-000472、API-000473 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-000469），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000470）
- [x] 入参单缺陷 2 条（API-000471 scope_code、API-000472 limit）
- [x] responseFields 契约占位 1 条（API-000473 shortboard_cnt）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000469）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 API-000469～000473）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000469**～**API-000473** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
