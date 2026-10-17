# 智能服务集群-科技专题服务算法库测试用例（算法库后端模型 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 算法库后端模型  
> **catalog**：`entry_id=policy.deep` · `catalog_page_id=policy.deep` · path `/policy/deep`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/policy.json` 页 `policy.deep` · endpoint `policy.deep.models`  
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
| 业务 path | Java REST：`GET /policy/v1/policy/analysis/deep`（查询参数 `scope_code`、`limit`，均为可选） |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000524（金样）** 断言 **完整信封**（HTTP + `code` + 可解析体）；同册其余用例在前置引用金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`policy.deep.models`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中六大模型 `index`（如 82.6、78.4、3、9、6）、`model_name`、`metric_id` 等示例作为通过条件 |
| 样例与契约差 | `sampleResponse` 为对象，含 `rows` 数组；元素含 `model`、`model_name`、`metric_id`、`index`。契约 `responseFields` **仅**声明 `rows`（array）。断言 **只强制 responseFields**；`model` / `model_name` / `metric_id` / `index` 等样例字段不设失败条件（形态探测见 API-000528 对 `rows` 本身） |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000524`～`000528`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000524 | 政策分析 | 算法库后端模型 | 契约-不可用 | 六大模型综合索引 | 算法库后端模型 | 后端模型 | catalog 不可用态下后端模型索引接口可识别非 live 成功 | 1、已确认 catalog `policy.deep.models` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/deep，查询参数取组合 DEEP-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中六大模型 index 或 model_name 作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产六大模型索引判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A（catalog 聚合页；不扩六级） | N/A-技术项 | N/A | /policy/v1/policy/analysis/deep | | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=DEEP-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000525 | 政策分析 | 算法库后端模型 | 异常-鉴权 | 六大模型综合索引 | 算法库后端模型 | 后端模型 | 后端模型索引接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /policy/v1/policy/analysis/deep，查询参数取组合 DEEP-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 rows 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/deep | | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=DEEP-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000526 | 政策分析 | 算法库后端模型 | 异常-非法scope_code | 六大模型综合索引 | 算法库后端模型 | 后端模型 | 不存在或非法 scope_code 时返回可识别失败而非空索引成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/deep，查询参数取组合 DEEP-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无模型空结果或伪 rows 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/deep | | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=DEEP-02；矩阵挂 scope_code、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000527 | 政策分析 | 算法库后端模型 | 异常-非法limit | 六大模型综合索引 | 算法库后端模型 | 后端模型 | 非正整数 limit 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /policy/v1/policy/analysis/deep，查询参数取组合 DEEP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 limit 静默截断为默认条数并成功返回 sample 形态 rows | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/deep | | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=DEEP-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000528 | 政策分析 | 算法库后端模型 | 契约-字段形态 | 六大模型综合索引 | 算法库后端模型 | 后端模型 | 成功信封下契约出参 rows 若存在是否符合 array 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-000524 | 1.GET /policy/v1/policy/analysis/deep，查询参数取组合 DEEP-01 | 1、若 code 属成功集合且载荷含 rows（含 data 内或顶层），则 rows 为 array；2、不得以 sample 中六大模型 index 或条数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/deep | M_POLICY_DEEP_166_1 | INTEG | | | endpoint_id=policy.deep.models catalog_page_id=policy.deep 组合=DEEP-01；矩阵挂 rows；样例另含 M_POLICY_DEEP_167_1～171_1 不设失败条件 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| DEEP-01 | policy.deep.models | `scope_code=440300`；`limit=50`（对齐 catalog `sampleRequest`） | 契约主路径（unavailable） |
| DEEP-02 | policy.deep.models | `scope_code=__invalid__`；`limit=50` | 非法/不存在省市区编码 |
| DEEP-03 | policy.deep.models | `limit=0`（`scope_code` 不传或空） | 非正整数条数上限 |
| DEEP-04 | policy.deep.models | `scope_code=999999`；`limit=50` | 合法形态但可能不存在的编码；**本轮无独立用例**，语义待 endpoint available 后补 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| policy.deep.models | GET | /policy/v1/policy/analysis/deep | unavailable | scope_code、limit（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.deep.models | API-000524、API-000525、API-000526、API-000527、API-000528 |

---

## 3. 覆盖自检（§S1）

- [x] unavailable endpoint 已写契约占位（API-000524），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-000525）
- [x] 入参单缺陷 2 条（API-000526 scope_code、API-000527 limit）
- [x] responseFields 契约占位 1 条（API-000528 rows）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-000524）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-000524～000528；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000524**～**API-000528** |
| `_empty` 未覆盖 | **1** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
