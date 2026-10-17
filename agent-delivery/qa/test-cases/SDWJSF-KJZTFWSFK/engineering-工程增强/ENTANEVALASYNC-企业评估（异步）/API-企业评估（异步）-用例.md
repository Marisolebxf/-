# 智能服务集群-科技专题服务算法库测试用例（企业评估（异步） API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 企业评估（异步）  
> **catalog**：`entry_id=entan.eval-async` · `catalog_page_id=entan.eval-async` · path `/entan/eval-async`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.eval-async`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `entan.eval-async` 行（`_l6-to-catalog-map.yaml`：工程增强，非 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00157（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 可解析形态，或网关不可路由时的 HTTP 失败态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00157」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **1** 个 endpoint（`entan.eval-async.mock`）catalog `status=unavailable`、`runtime=local_mock`；**`path` 登记为空**（Java REST 未发布，联调台仅前端 Mock 契约）；**禁止**将 `sampleResponse` 各 `mode` 下 `task_id`、`max_score`、`avg_score`、`ranking`、`radar_series`、`diagnosis_rows` 等示例作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST JSON；必填 `mode`（string，枚举 `technology` / `business` / `competitiveness`）；组合定义见附录 A |
| 样例与契约差 | `sampleResponse` 按 `mode` 分三套嵌套对象（含 `result.ranking` 等）；契约 `responseFields` **仅**声明 `task_id`（string）。断言以 `responseFields` 为准；样例内雷达/表格扩展字段不设失败条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = catalog `path`（本 endpoint 为空则填 `—`）；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.eval-async`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00157 | 工程增强 | 企业评估（异步） | 契约-不可用 | 异步评估契约 | 企业评估（异步） | 异步评估契约 | catalog 不可用态下异步评估契约接口返回可识别非成功契约 | 1、已确认 catalog `entan.eval-async.mock` 为 unavailable 且 path 为空；2、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 EVAL-01 | 1、HTTP 状态为 404/405/4xx/5xx 或响应体为 JSON；2、若体为 JSON 则含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含 string 型 `task_id` 的成功业务载荷；4、不得将 sampleResponse 技术力/商业力/综合竞争力示例分值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00158 | 工程增强 | 企业评估（异步） | 异常-鉴权 | 异步评估契约 | 企业评估（异步） | 异步评估契约 | 异步评估契约接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST（catalog path 为空·local_mock）请求体取组合 EVAL-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 task_id 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00159 | 工程增强 | 企业评估（异步） | 异常-缺必填mode | 异步评估契约 | 企业评估（异步） | 异步评估契约 | 异步评估契约接口缺少 mode 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00157 | 1.POST（catalog path 为空·local_mock）请求体取组合 EVAL-02 | 1、响应为失败态（HTTP 4xx/5xx 或 code 非成功集合）；2、不得将失败当作含可信 `task_id` 的成功异步结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-02；矩阵挂 mode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00160 | 工程增强 | 企业评估（异步） | 异常-非法mode | 异步评估契约 | 企业评估（异步） | 异步评估契约 | 异步评估契约接口 mode 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 EVAL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、message 或 msg 可非空；3、不得将失败当作含可信 `task_id` 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-03；矩阵挂 mode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00161 | 工程增强 | 企业评估（异步） | 异常-空mode | 异步评估契约 | 企业评估（异步） | 异步评估契约 | 异步评估契约接口 mode 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 EVAL-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得与合法 `technology` 主路径成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-04；矩阵挂 _fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| EVAL-01 | entan.eval-async.mock | `mode`: `technology`（catalog example，执行期可替换为 `business` / `competitiveness`） | unavailable 契约占位主路径 |
| EVAL-02 | entan.eval-async.mock | 请求体 `{}`（不含 `mode` 键） | 缺必填 |
| EVAL-03 | entan.eval-async.mock | `mode`: `__invalid_mode__` | 枚举外取值 |
| EVAL-04 | entan.eval-async.mock | `mode`: `""` | 空字符串 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 必填参数 |
|-------------|--------|------|--------|---------|----------|
| entan.eval-async.mock | POST | （空） | unavailable | local_mock | mode（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.eval-async.mock | API-00157、API-00158、API-00159、API-00160、API-00161 |

---

## 3. 覆盖自检

- [x] 唯一 unavailable / local_mock endpoint 已写契约占位（API-00157）
- [x] 必填 `mode` 缺省、枚举外、空字符串已覆盖（API-00159～00161）
- [x] 异常-鉴权 1 条（API-00158）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定合法空 task 构造）
- [x] 金样 1 条且断言信封或网关不可路由失败态（API-00157）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **5** 条；编号 **API-00157**～**API-00161**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **5**（00157～00161） |
| 金样（完整信封或不可路由失败态） | **1**（API-00157） |
| live 主路径 | **0**（endpoint unavailable + path 空） |
| 每 endpoint 契约占位 | **1**（mock 00157） |
| 异常-鉴权 | **1**（00158） |
| `_empty` 矩阵 | **1** 行 **未覆盖** |
| `_fail` 矩阵 | **1** 行 **已覆盖**（00157、00159～00161） |
| 步骤以 POST+组合 开头（抽检 3 条：00157、00159、00161） | **通过** |
| 预期无页面/图表表述（抽检 3 条：00157、00158、00160） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| A 线 `work` 检索 `entan.eval-async` | **0 命中**（工程增强，待 A 线合表核对） |
