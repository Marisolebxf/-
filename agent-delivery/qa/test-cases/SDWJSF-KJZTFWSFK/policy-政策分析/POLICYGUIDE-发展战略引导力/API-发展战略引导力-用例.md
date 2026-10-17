# 智能服务集群-科技专题服务算法库测试用例（发展战略引导力 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 发展战略引导力  
> **catalog**：`entry_id=policy.guide` · `catalog_page_id=policy.guide` · path `/policy/guide`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.guide` · endpoint `policy.guide.main`  
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
| 业务 path | Java REST：`GET /policy/v1/policy/analysis/guide`（查询参数 `scope_code`、`limit`，均为可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000514（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`policy.guide.main`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 effect_score（如 72.4）、layout_rec_cnt（如 3）、scope_name（如「广东省」）或示例 metric_id 作为通过条件 |
| 样例与契约差 | `sampleResponse` 含 `model_id`、`count`、`rows`（元素含 scope_name、effect_score、layout_rec_cnt、metric_id）；契约 `responseFields` **仅**声明 `rows`。断言 **只强制 responseFields**；样例内其他字段不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000514`～`000518`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000514 | 政策分析 | 发展战略引导力 | 契约-不可用 | C7组合读面模型 | 发展战略引导力 | 引导力 | catalog 不可用态下引导力接口可识别非 live 成功 | 1、已确认 catalog `policy.guide.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 effect_score、layout_rec_cnt 或区域名称作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产引导力判定 | P0 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.1 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | M_POLICY_DS_07_POLICY_GUARD_001 | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-01 金样 §0未试调 catalog_status=unavailable C7读C1+C6 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000515 | 政策分析 | 发展战略引导力 | 异常-鉴权 | C7组合读面模型 | 发展战略引导力 | 引导力 | 引导力接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 rows 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.1 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000516 | 政策分析 | 发展战略引导力 | 异常-非法scope_code | C7组合读面模型 | 发展战略引导力 | 引导力 | 不存在或非法 scope_code 时返回可识别失败而非空引导力成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无引导力空结果或伪 rows 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.1 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-02；矩阵挂 scope_code、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000517 | 政策分析 | 发展战略引导力 | 异常-非法limit | C7组合读面模型 | 发展战略引导力 | 引导力 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态列表 | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.1 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000518 | 政策分析 | 发展战略引导力 | 契约-字段形态 | C7组合读面模型 | 发展战略引导力 | 引导力 | 成功信封下契约出参 rows 若存在是否符合 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000514 | 1.GET /policy/v1/policy/analysis/guide，查询参数取组合 GUIDE-01 | 1、若 code 属成功集合且载荷含 rows，则 rows 为 array；2、不得以 sample 行内 effect_score 或 layout_rec_cnt 具体数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技信息展示系统和科技专题服务系统.md | 1.1.1.1.4.1.7.4.1 | N/A-技术项 | N/A | /policy/v1/policy/analysis/guide | M_POLICY_DS_07_POLICY_GUARD_001 | INTEG | | | endpoint_id=policy.guide.main catalog_page_id=policy.guide 组合=GUIDE-01；矩阵挂 rows |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GUIDE-01 | policy.guide.main | 不传 `scope_code`（全省/默认范围）；`limit=20`（对齐 catalog `sampleRequest`） | 契约主路径（unavailable） |
| GUIDE-02 | policy.guide.main | `scope_code=__invalid__`；`limit=20` | 非法/不存在范围编码 |
| GUIDE-03 | policy.guide.main | `limit=0`（scope_code 不传或空） | 非正整数条数上限 |
| GUIDE-04 | policy.guide.main | `scope_code=999999`；`limit=20` | 合法形态但可能不存在的省市区编码；**本轮无独立用例**，语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.guide.main | GET | /policy/v1/policy/analysis/guide | unavailable | scope_code、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.guide.main | API-000514、API-000515、API-000516、API-000517、API-000518 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-000514），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000515）
- [x] 入参单缺陷 2 条（API-000516 scope_code、API-000517 limit）
- [x] responseFields 契约占位 1 条（API-000518 rows）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000514）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000514～000518；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000514**～**API-000518** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
