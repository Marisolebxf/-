# 智能服务集群-科技专题服务算法库测试用例（产业瓶颈堵点识别 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业链分析 / 产业瓶颈堵点识别  
> **catalog**：`entry_id=chain.bottleneck` · `catalog_page_id=chain.bottleneck` · path `/chain/bottleneck`  
> **A 线对照**：`fp-split-by-api-run/work/L22.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 成功 code 集合 | `0`、`"0"`、`200`、`"200"` |
| 鉴权失败 | HTTP **401** 或 **424**；业务体可含 `code` 非成功集合及 `message`/`msg` |
| 鉴权头 | `Authorization: Bearer <access_token>`（联调台 LoginView：OAuth 密码模式，默认账号口径见 `lumen-ui-algo-apiview`）；`TENANT-ID: 1`（与 apiview 默认租户一致） |
| 断言对象分工 | **API-00051（金样）** 断言 **完整信封**（HTTP + `code` + `data` 形态）；同册其余用例断言 HTTP 与失败/不可用态，不将 catalog `sampleResponse` 中 severity、overall_score 等数值作为通过条件 |
| catalog 状态 | 本页仅 **1** 个 endpoint：`chain.bottleneck.main`，catalog `status=unavailable`；**不写** live 成功业务数值预期 |
| 试调（2026-10-17） | 50897 **可达**。无鉴权主路径试调 **1 次**：`GET /api/innov/v1/industry/INB170101/bottlenecks` → HTTP **424**，响应体 `code=1`（非成功集合）、`msg` 非空。**带有效 token 的契约不可用主路径未试调**（登录需联调台密码加密，本轮未完成 OAuth 取 token）；执行期按金样步骤复核信封 |
| 本页 endpoint 数 | **1**（`chain.bottleneck.main`） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.bottleneck`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00051 | 产业链分析 | 产业瓶颈堵点识别 | 契约-不可用 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别 | 瓶颈堵点 | catalog 不可用态下瓶颈堵点接口返回可识别非成功契约 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、catalog 登记 status 为 unavailable | 1.GET /innov/v1/industry/{chainId}/bottlenecks，path 取组合 BOT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应 code 不属于成功集合，或 data 不构成含 severity/overall_score 的成功业务载荷；3、不得将 sampleResponse 示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | | | | | /innov/v1/industry/{chainId}/bottlenecks | | | | | endpoint_id=chain.bottleneck.main catalog_page_id=chain.bottleneck 组合=BOT-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00052 | 产业链分析 | 产业瓶颈堵点识别 | 异常-鉴权 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别 | 瓶颈堵点 | 瓶颈堵点接口无 token 时网关拒绝访问 | 1、请求 deliberately 不携带 Authorization | 1.GET /innov/v1/industry/{chainId}/bottlenecks，path 取组合 BOT-01，无 Authorization 头 | 1、HTTP 状态为 401 或 424；2、响应体可辨认为鉴权失败（非成功业务 data） | P1 | | | | | | N/A-技术项 | | | | | /innov/v1/industry/{chainId}/bottlenecks | | | | | endpoint_id=chain.bottleneck.main catalog_page_id=chain.bottleneck 组合=BOT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00053 | 产业链分析 | 产业瓶颈堵点识别 | 异常-非法chainId | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别 | 瓶颈堵点 | 非法 chainId 时瓶颈堵点接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry/{chainId}/bottlenecks，path 取组合 BOT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无堵点空 severity/overall_score 成功态 | P1 | | | | | | N/A-技术项 | | | | | /innov/v1/industry/{chainId}/bottlenecks | | | | | endpoint_id=chain.bottleneck.main catalog_page_id=chain.bottleneck 组合=BOT-02；矩阵覆盖 chainId 与 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00054 | 产业链分析 | 产业瓶颈堵点识别 | 异常-缺path产业标识 | 产业瓶颈堵点识别模型 | 产业瓶颈堵点识别 | 瓶颈堵点 | path 缺 chainId 时瓶颈堵点接口返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/industry//bottlenecks（path 无产业标识段，组合 BOT-03） | 1、HTTP 为 4xx 或响应 code 非成功集合；2、响应体不是成功空对象冒充可用瓶颈结果 | P1 | | | | | | N/A-技术项 | | | | | /innov/v1/industry/{chainId}/bottlenecks | | | | | endpoint_id=chain.bottleneck.main catalog_page_id=chain.bottleneck 组合=BOT-03 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| BOT-01 | chain.bottleneck.main | path `chainId=INB170101`（catalog example，执行期可替换为试调有效 id） | 契约占位主路径 |
| BOT-02 | chain.bottleneck.main | path `chainId=__invalid__` | 非法产业标识 |
| BOT-03 | chain.bottleneck.main | path 缺 `chainId`：`GET /innov/v1/industry//bottlenecks` | 缺必填 path 参数 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.bottleneck.main | GET | /innov/v1/industry/{chainId}/bottlenecks | unavailable | chainId（path） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.bottleneck.main | API-00051、API-00052、API-00053、API-00054 |

---

## 3. 覆盖自检

- [x] unavailable endpoint 已写契约占位（API-00051）
- [x] 异常-鉴权 1 条（API-00052）
- [x] 非法 chainId / 缺 path 入参（API-00053、API-00054）
- [x] ≥1 条备注含 `金样` 且断言信封（API-00051）
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-00051～API-00054）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **4** |
| 编号闭区间 | **API-00051**～**API-00054** |
| `_empty` 未覆盖 | **1**（无稳定空数据构造条件，见矩阵） |
| FUNC 条数 | **0** |
