# 智能服务集群-科技专题服务算法库测试用例（焦点识别(单个政策) API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：政策分析 / 焦点识别(单个政策)  
> **catalog**：`entry_id=policy.focus-one` · `catalog_page_id=policy.focus-one` · path `/policy/focus-one`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.focus-one`  
> **A 线对照**：`fp-split-by-api-run-v0-202609/work/L35.md`（POST 段）；`policy.focus-one` 为 **L35 单政策变体**（`_l6-to-catalog-map.yaml` catalog_skip「挂 L35 时按 path 去重」）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 业务 path | `POST /policy/v1/policy/analysis/focus-one`（JSON body） |
| 鉴权 | `POST /auth/oauth2/token`（密码模式，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-000454（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 可解析形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-000454」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **1** 个 endpoint：`policy.focus-one.main`，catalog **`status=unavailable`**；**禁止**将 `sampleResponse` 中 `focus_list`/`bottleneck_list`/`suggestions` 内 term、score、item 等示例作为通过条件 |
| 样例与契约差 | `sampleResponse` 含 `mode`、`persisted` 等扩展字段；契约 `responseFields` **仅**声明顶层 `focus_list`、`bottleneck_list`、`suggestions`（array）。断言以 `responseFields` 为准 |
| 试调 | **未试调**（本子任务禁止 curl/浏览器；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST JSON；必填 `text`（string）；可选 `mode`（`rule` \| `llm`）、`title`、`execution`、`aux`；组合见附录 A |
| 本页 endpoint 数 | **1**（`policy.focus-one.main`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.focus-one`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000454 | 政策分析 | 焦点识别(单个政策) | 契约-不可用 | 政策焦点识别模型 | 焦点识别(单个政策) | 单条焦点识别 | catalog 不可用态下单条焦点识别接口返回可识别非 live 成功 | 1、已确认 catalog `policy.focus-one.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FOC-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 `code`；3、不得将 sample 中焦点词/堵点/建议示例条目作为通过条件；4、若 code 属成功集合则 data 不得构成含可信 `focus_list`/`bottleneck_list`/`suggestions` 业务清单的成功载荷（契约未交付态） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.5 | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | FULL | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FOC-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000455 | 政策分析 | 焦点识别(单个政策) | 异常-鉴权 | 政策焦点识别模型 | 焦点识别(单个政策) | 单条焦点识别 | 单条焦点识别接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FOC-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信焦点/堵点业务 data 的成功载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.5 | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | FULL | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FOC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000456 | 政策分析 | 焦点识别(单个政策) | 异常-缺必填text | 政策焦点识别模型 | 焦点识别(单个政策) | 单条焦点识别 | 缺少必填政策文本 text 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 API-000454 | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FOC-02 | 1、响应为失败态（HTTP 4xx/5xx 或 code 非成功集合）；2、不得将失败当作空 `focus_list`/`bottleneck_list`/`suggestions` 成功空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.5 | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | FULL | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FOC-02；矩阵挂 text、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000457 | 政策分析 | 焦点识别(单个政策) | 异常-非法mode | 政策焦点识别模型 | 焦点识别(单个政策) | 单条焦点识别 | mode 非 catalog 点名 rule/llm 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FOC-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、message 或 msg 可非空；3、不得将失败当作含 sample 形态焦点清单的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.5 | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | FULL | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FOC-03；矩阵挂 mode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000458 | 政策分析 | 焦点识别(单个政策) | 异常-空text | 政策焦点识别模型 | 焦点识别(单个政策) | 单条焦点识别 | 政策文本 text 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /policy/v1/policy/analysis/focus-one，请求体取组合 FOC-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得与合法非空 text 主路径成功态混淆；3、不得将失败当作「无法识别焦点」的空清单成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 1.1.1.1.1.1.1.3.5 | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | | FULL | | | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FOC-04；矩阵挂 text、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| FOC-01 | policy.focus-one.main | `mode`: `rule`，`title`/`text`/`execution`/`aux` 取 catalog `sampleRequest` 同值（text 非空） | unavailable 契约占位主路径 |
| FOC-02 | policy.focus-one.main | 请求体 `{"mode":"rule","title":"占位标题"}`（不含 `text` 键） | 缺必填 text |
| FOC-03 | policy.focus-one.main | `mode`: `__invalid__`，`text`: `推进先进封装产业化。` | 非法 mode |
| FOC-04 | policy.focus-one.main | `mode`: `rule`，`text`: `""` | 空字符串 text |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| policy.focus-one.main | POST | /policy/v1/policy/analysis/focus-one | unavailable | text（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.focus-one.main | API-000454～API-000458 |

---

## 3. 覆盖自检（§I）

- [x] 本页 **0** 条 FUNC
- [x] unavailable endpoint 契约占位 + 金样信封（API-000454）
- [x] 异常-鉴权 1 条（API-000455）
- [x] 必填 `text` 缺省与空字符串（API-000456、API-000458）
- [x] 非法 `mode`（API-000457）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定「合法 text 必空清单」构造）
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 **API-000454～000458**）

---

## 4. 交卷计数（§I）

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-000454**～**API-000458** |
| 金样 | **API-000454**（备注含 `金样`） |
| §0 试调 | **未试调** |
| FUNC 条数 | **0** |
