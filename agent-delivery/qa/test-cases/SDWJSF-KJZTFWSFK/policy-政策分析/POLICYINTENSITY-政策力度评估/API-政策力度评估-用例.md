# 智能服务集群-科技专题服务算法库测试用例（政策力度评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 政策力度评估  
> **catalog**：`entry_id=policy.intensity` · `catalog_page_id=policy.intensity` · path `/policy/intensity`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.intensity` · endpoint `policy.intensity.main`  
> **A 线对照**：`fp-split-by-api-run/work/L36.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /policy/v1/policy/analysis/intensity`（查询参数 `scope_type`、`scope_code`、`limit`，均为可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000459（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`policy.intensity.main`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 intensity_index（如 91.2、88.6）、政策标题或产业覆盖等示例作为通过条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000459`～`000463`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000459 | 政策分析 | 政策力度评估 | 契约-不可用 | 政策力度评估模型 | 政策力度评估 | 力度评估 | catalog 不可用态下力度评估接口可识别非 live 成功 | 1、已确认 catalog `policy.intensity.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 intensity_index 或政策/省份名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产力度评估判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.2 | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000460 | 政策分析 | 政策力度评估 | 异常-鉴权 | 政策力度评估模型 | 政策力度评估 | 力度评估 | 力度评估接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 intensity_index 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.2 | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000461 | 政策分析 | 政策力度评估 | 异常-非法scope_code | 政策力度评估模型 | 政策力度评估 | 力度评估 | 不存在或非法 scope_code 时返回可识别失败而非空力度成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无力度空结果或伪 intensity_index 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.2 | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-02；矩阵挂 scope_code、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000462 | 政策分析 | 政策力度评估 | 异常-非法limit | 政策力度评估模型 | 政策力度评估 | 力度评估 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态排行榜 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.2 | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000463 | 政策分析 | 政策力度评估 | 契约-字段形态 | 政策力度评估模型 | 政策力度评估 | 力度评估 | 成功信封下契约出参 intensity_index 若存在是否符合 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000459 | 1.GET /policy/v1/policy/analysis/intensity，查询参数取组合 INT-01 | 1、若 code 属成功集合且载荷含 intensity_index（含列表元素内），则 intensity_index 为 number；2、不得以 sample 中 91.2 等具体指数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.8.2 | N/A-技术项 | N/A | /policy/v1/policy/analysis/intensity | | INTEG | | | endpoint_id=policy.intensity.main catalog_page_id=policy.intensity 组合=INT-01；矩阵挂 intensity_index |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INT-01 | policy.intensity.main | `scope_type=province`；`limit=20`（对齐 catalog sampleRequest；不传 scope_code） | 契约主路径（unavailable） |
| INT-02 | policy.intensity.main | `scope_type=policy`；`scope_code=__invalid__`；`limit=20` | 非法/不存在范围编码 |
| INT-03 | policy.intensity.main | `limit=0`（其余不传或仅 `scope_type=province`） | 非正整数条数上限 |
| INT-04 | policy.intensity.main | `scope_type=__invalid__`；`limit=20` | 非法 scope_type 枚举参考；**本轮无独立用例**，非法 scope_type 语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.intensity.main | GET | /policy/v1/policy/analysis/intensity | unavailable | scope_type、scope_code、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.intensity.main | API-000459、API-000460、API-000461、API-000462、API-000463 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-000459），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000460）
- [x] 入参单缺陷 2 条（API-000461 scope_code、API-000462 limit）
- [x] responseFields 契约占位 1 条（API-000463 intensity_index）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000459）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 API-000459～000463）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000459**～**API-000463** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
