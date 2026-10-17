# 智能服务集群-科技专题服务算法库测试用例（政策匹配推送 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 匹配推送  
> **catalog**：`entry_id=policy.match` · `catalog_page_id=policy.match` · path `/policy/match`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.match` · endpoint `policy.match.main`  
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
| 业务 path | Java REST：`GET /policy/v1/policy/match`（查询参数 `subject_id`、`subject_type`、`limit`，均为可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000504（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`policy.match.main`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 match_score（如 75）、rank_no、主体/政策示例名称等作为通过条件 |
| 样例与契约差 | `sampleResponse` 为数组，元素含 `rank_no`、`subject_name`、`policy_title`、`match_score`、`metric_id`；契约 `responseFields` **仅**声明 `match_score`。断言 **只强制 responseFields**；其余样例字段不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000504`～`000508`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000504 | 政策分析 | 匹配推送 | 契约-不可用 | 政策匹配推送模型 | 匹配推送 | 政策匹配 | catalog 不可用态下匹配推送接口可识别非 live 成功 | 1、已确认 catalog `policy.match.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 match_score 或示例主体/政策名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产匹配推送判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.2.6 | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MATCH-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000505 | 政策分析 | 匹配推送 | 异常-鉴权 | 政策匹配推送模型 | 匹配推送 | 政策匹配 | 匹配推送接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 match_score 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.2.6 | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MATCH-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000506 | 政策分析 | 匹配推送 | 异常-非法subject_type | 政策匹配推送模型 | 匹配推送 | 政策匹配 | 枚举外 subject_type 时返回可识别失败而非空匹配成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无匹配空结果或伪 match_score 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.2.6 | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MATCH-02；矩阵挂 subject_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000507 | 政策分析 | 匹配推送 | 异常-非法limit | 政策匹配推送模型 | 匹配推送 | 政策匹配 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.2.6 | N/A-技术项 | N/A | /policy/v1/policy/match | | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MATCH-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000508 | 政策分析 | 匹配推送 | 契约-字段形态 | 政策匹配推送模型 | 匹配推送 | 政策匹配 | 成功信封下契约出参 match_score 若存在是否符合 number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000504 | 1.GET /policy/v1/policy/match，查询参数取组合 MATCH-01 | 1、若 code 属成功集合且载荷含 match_score（含列表元素内），则 match_score 为 number；2、不得以 sample 中 75 等具体分值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.2.6 | N/A-技术项 | N/A | /policy/v1/policy/match | M_POLICY_MATCH | INTEG | | | endpoint_id=policy.match.main catalog_page_id=policy.match 组合=MATCH-01；矩阵挂 match_score |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MATCH-01 | policy.match.main | `subject_type=enterprise`；`limit=20`（对齐 catalog `sampleRequest`；`subject_id` 不传） | 契约主路径（unavailable） |
| MATCH-02 | policy.match.main | `subject_type=__invalid__`；`limit=20` | 枚举外主体类型 |
| MATCH-03 | policy.match.main | `limit=0`（`subject_type` 不传或留空） | 非正整数条数上限 |
| MATCH-04 | policy.match.main | `subject_id=__not_exist__`；`subject_type=enterprise`；`limit=20` | 合法形态但可能不存在的主体 ID；**本轮无独立用例**，语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.match.main | GET | /policy/v1/policy/match | unavailable | subject_id、subject_type、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.match.main | API-000504、API-000505、API-000506、API-000507、API-000508 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-000504），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000505）
- [x] 入参单缺陷 2 条（API-000506 subject_type、API-000507 limit）
- [x] responseFields 契约占位 1 条（API-000508 match_score）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000504）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000504～000508；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000504**～**API-000508** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
