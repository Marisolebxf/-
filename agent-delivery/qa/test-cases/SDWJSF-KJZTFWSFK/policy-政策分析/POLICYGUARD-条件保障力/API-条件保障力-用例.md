# 智能服务集群-科技专题服务算法库测试用例（条件保障力 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 条件保障力  
> **catalog**：`entry_id=policy.guard` · `catalog_page_id=policy.guard` · path `/policy/guard`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guard` · endpoint `policy.guard.main`  
> **A 线对照**：catalog 单 endpoint（`fp-split-by-api-run` 不扩六级，无独立 `Lxx.md`；覆盖矩阵见本目录 `coverage-fp.md`）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /policy/v1/policy/analysis/guard`（查询参数 `scope_code`、`limit`，均为可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000519（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`policy.guard.main`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 effect_score（如 68.1）、scope_name、metric_id 等示例作为通过条件 |
| 样例与契约差 | `sampleResponse` 含 `model_id`、`count`、`rows`（元素含 `scope_name`、`effect_score`、`metric_id`）；契约 `responseFields` **仅**声明 `rows`（array）。断言以 `responseFields` 为准；样例内 `effect_score` 等不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000519`～`000523`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000519 | 政策分析 | 条件保障力 | 契约-不可用 | 政策与条件保障力综合评估模型 | 条件保障力 | 保障力评估 | catalog 不可用态下条件保障力接口可识别非 live 成功 | 1、已确认 catalog `policy.guard.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GUARD-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 effect_score 或区域名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产条件保障力判定 | P0 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.6 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GUARD-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000520 | 政策分析 | 条件保障力 | 异常-鉴权 | 政策与条件保障力综合评估模型 | 条件保障力 | 保障力评估 | 条件保障力接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GUARD-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 rows 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.6 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GUARD-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000521 | 政策分析 | 条件保障力 | 异常-非法scope_code | 政策与条件保障力综合评估模型 | 条件保障力 | 保障力评估 | 不存在或非法 scope_code 时返回可识别失败而非空保障力成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GUARD-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无评估结果空态或伪 effect_score 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.6 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GUARD-02；矩阵挂 scope_code、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000522 | 政策分析 | 条件保障力 | 异常-非法limit | 政策与条件保障力综合评估模型 | 条件保障力 | 保障力评估 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GUARD-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态 rows | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.6 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GUARD-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000523 | 政策分析 | 条件保障力 | 契约-字段形态 | 政策与条件保障力综合评估模型 | 条件保障力 | 保障力评估 | 成功信封下契约出参 rows 若存在是否符合 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000519 | 1.GET /policy/v1/policy/analysis/guard，查询参数取组合 GUARD-01 | 1、若 code 属成功集合且载荷含 rows，则 rows 为 array；2、不得以 sample 中行数或 effect_score 具体值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.6 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guard | M_POLICY_DS_07_POLICY_GUARD_008 | INTEG | | | endpoint_id=policy.guard.main catalog_page_id=policy.guard 组合=GUARD-01；矩阵挂 rows |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GUARD-01 | policy.guard.main | `scope_code=440000`；`limit=20`（对齐 catalog `sampleRequest` 的 limit 与 params 中省编码示例） | 契约主路径（unavailable） |
| GUARD-02 | policy.guard.main | `scope_code=__invalid__`；`limit=20` | 非法/不存在范围编码 |
| GUARD-03 | policy.guard.main | `limit=0`（`scope_code` 不传或空） | 非正整数条数上限 |
| GUARD-04 | policy.guard.main | 仅 `limit=20`（不传 scope_code，对齐 catalog sampleRequest） | 无 scope 列表模式参考；**本轮无独立用例**，全量 scope 语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.guard.main | GET | /policy/v1/policy/analysis/guard | unavailable | scope_code、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.guard.main | API-000519、API-000520、API-000521、API-000522、API-000523 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-000519），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000520）
- [x] 入参单缺陷 2 条（API-000521 scope_code、API-000522 limit）
- [x] responseFields 契约占位 1 条（API-000523 rows）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000519）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000519～000523；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000519**～**API-000523** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
