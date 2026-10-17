# 智能服务集群-科技专题服务算法库测试用例（湾区创新监测 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 湾区创新监测  
> **catalog**：`entry_id=innov.bay-area-monitoring` · `catalog_page_id=innov.bay-area-monitoring` · path `/innov/bay-area-monitoring`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.bay-area-monitoring`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `innov.bay-area-monitoring` 行（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
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
| 断言分工 | **API-00844（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00844」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **1** 个 endpoint（`innov.bay-area-monitoring.metrics`）catalog `status=unavailable`、`runtime=java_api`；指标清单接口未发布；**禁止**将 `sampleResponse` 中 `metrics[].metric_id`/`name`、`formula_status`、`total=16` 等示例作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 查询参数 | GET；`module` 为可选 string（slug，example `bay-area-monitoring`）；组合定义见附录 A |
| 样例与契约差 | `sampleResponse.metrics` 元素含 `algorithm_type`、`pending_ref` 等扩展字段；契约 `responseFields` **仅**声明 `metrics`（array）、`total`（number）。断言以 `responseFields` 为准；样例扩展字段不设失败条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00844`～`00848`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.bay-area-monitoring`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00844 | 创新监测 | 湾区创新监测 | 契约-不可用 | 湾区创新监测指标清单 | 湾区创新监测 | 湾区创新监测指标清单 | catalog 不可用态下指标清单接口返回可识别非成功契约信封 | 1、已确认 catalog `innov.bay-area-monitoring.metrics` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/innov/metrics，查询参数取组合 GBAY-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `metrics` 与 number 型 `total` 的成功业务载荷；4、不得将 sampleResponse 中 16 条指标或具体 metric_id 作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·湾区创新监测 | N/A-技术项 | N/A | /innov/v1/innov/metrics | M_INNOV_GBA_CAPACITY_INDEX | INTEG | | | endpoint_id=innov.bay-area-monitoring.metrics catalog_page_id=innov.bay-area-monitoring 组合=GBAY-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00845 | 创新监测 | 湾区创新监测 | 异常-鉴权 | 湾区创新监测指标清单 | 湾区创新监测 | 湾区创新监测指标清单 | 指标清单接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/innov/metrics，查询参数取组合 GBAY-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 metrics/total 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·湾区创新监测 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.bay-area-monitoring.metrics catalog_page_id=innov.bay-area-monitoring 组合=GBAY-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00846 | 创新监测 | 湾区创新监测 | 异常-非法module | 湾区创新监测指标清单 | 湾区创新监测 | 湾区创新监测指标清单 | module 为不可识别 slug 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00844 | 1.GET /innov/v1/innov/metrics，查询参数取组合 GBAY-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含 sample 形态 metrics 清单的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·湾区创新监测 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.bay-area-monitoring.metrics catalog_page_id=innov.bay-area-monitoring 组合=GBAY-02；矩阵挂 module、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00847 | 创新监测 | 湾区创新监测 | 异常-空module | 湾区创新监测指标清单 | 湾区创新监测 | 湾区创新监测指标清单 | module 为空字符串时返回可识别失败或与省略 module 可区分 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/innov/metrics，查询参数取组合 GBAY-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或可与 GBAY-04 省略 module 的语义明确区分；2、不得将空 module 静默当作 bay-area-monitoring 并成功返回 sample 形态 16 条指标 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·湾区创新监测 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.bay-area-monitoring.metrics catalog_page_id=innov.bay-area-monitoring 组合=GBAY-03；矩阵挂 module、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00848 | 创新监测 | 湾区创新监测 | 契约-字段形态 | 湾区创新监测指标清单 | 湾区创新监测 | 湾区创新监测指标清单 | 成功信封下契约出参 metrics、total 若存在是否符合 array/number 形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00844 | 1.GET /innov/v1/innov/metrics，查询参数取组合 GBAY-01 | 1、若 code 属成功集合且载荷含 metrics，则 metrics 为 array；2、若含 total，则 total 为 number；3、不得以 sample 中 total=16 或具体 metric_id 作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·湾区创新监测 | N/A-技术项 | N/A | /innov/v1/innov/metrics | M_INNOV_GBA_HOTSPOT | INTEG | | | endpoint_id=innov.bay-area-monitoring.metrics catalog_page_id=innov.bay-area-monitoring 组合=GBAY-01；矩阵挂 metrics、total |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GBAY-01 | innov.bay-area-monitoring.metrics | `module=bay-area-monitoring`（对齐 catalog `sampleRequest`） | unavailable 契约占位主路径 |
| GBAY-02 | innov.bay-area-monitoring.metrics | `module=__invalid_module__` | 不可识别模块 slug（单缺陷） |
| GBAY-03 | innov.bay-area-monitoring.metrics | `module`=`""`（空字符串） | 空 module 与省略参数边界 |
| GBAY-04 | innov.bay-area-monitoring.metrics | 不传 `module` | 可选 module 省略；**本轮无独立用例**，与 GBAY-01/00847 待试调后区分 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 必填参数 |
|-------------|--------|------|--------|---------|----------|
| innov.bay-area-monitoring.metrics | GET | /innov/v1/innov/metrics | unavailable | java_api | （无；`module` 可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.bay-area-monitoring.metrics | API-00844、00845、00846、00847、00848 |

---

## 3. 覆盖自检（§S1）

- [x] 唯一 unavailable endpoint 已写契约占位（API-00844）
- [x] 可选入参 `module` 非法值与空字符串已覆盖（API-00846、00847）
- [x] 异常-鉴权 1 条（API-00845）
- [x] 契约出参 `metrics`、`total` 形态占位 1 条（API-00848）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定「合法 module 下必空 metrics」试调证据）
- [x] 金样 1 条且断言完整信封（API-00844）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-00844**～**API-00848** |
| endpoint 数 | **1** |
| 金样（完整信封） | **1**（API-00844） |
| `_empty` 未覆盖 | **1**（见 coverage） |
| FUNC | **0** |
| code-registry / run-log | **未改**（父控回写） |
