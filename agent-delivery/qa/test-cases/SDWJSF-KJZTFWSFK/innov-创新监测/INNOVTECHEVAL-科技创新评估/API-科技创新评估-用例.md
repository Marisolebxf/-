# 智能服务集群-科技专题服务算法库测试用例（科技创新评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 科技创新评估  
> **catalog**：`entry_id=innov.tech-evaluation` · `catalog_page_id=innov.tech-evaluation` · path `/innov/tech-evaluation`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.tech-evaluation` · endpoint `innov.tech-evaluation.metrics`  
> **A 线对照**：`fp-split-by-api-run/work/` **无** `innov.tech-evaluation` 行（`_catalog-snapshot.md`：1 endpoint、0 running）；矩阵按 catalog + 本目录 `coverage-fp.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | Java REST：`GET /innov/v1/innov/metrics`（查询参数 `module` 可选，本页 slug 为 `tech-evaluation`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00819（金样）** 断言 **完整原始信封**（HTTP + `code` + 可解析体）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00819」后，可只断言失败态、鉴权态或 **data 载荷** 形态 |
| catalog 状态 | 本页 **1** 个 endpoint：`innov.tech-evaluation.metrics`，catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `total`（如 24）、`metric_id`、`formula_status` 或指标中文名作为通过条件 |
| 样例与契约差 | `sampleResponse` 的 `metrics` 元素含 `metric_id`、`name`、`algorithm_type`、`formula_status`、`pending_ref` 等；契约 `responseFields` **仅**声明 `metrics`（array）、`total`（number）。断言以 `responseFields` 为准；元素内扩展字段不设失败条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按 §0 鉴权与 catalog 复核） |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00819`～`00823`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.tech-evaluation`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00819 | 创新监测 | 科技创新评估 | 契约-不可用 | 科技创新评估指标清单 | 科技创新评估 | 指标元数据清单 | catalog 不可用态下指标清单接口可识别非 live 成功 | 1、已确认 catalog `innov.tech-evaluation.metrics` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID；3、断言对象为完整原始响应信封 | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 total=24 或指标条数作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产指标清单判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技创新评估 | N/A-技术项 | N/A | /innov/v1/innov/metrics | M_INNOV_PG_COMPOSITE | INTEG | | | endpoint_id=innov.tech-evaluation.metrics catalog_page_id=innov.tech-evaluation 组合=MET-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00820 | 创新监测 | 科技创新评估 | 异常-鉴权 | 科技创新评估指标清单 | 科技创新评估 | 指标元数据清单 | 指标清单接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 metrics/total 业务载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技创新评估 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.tech-evaluation.metrics catalog_page_id=innov.tech-evaluation 组合=MET-01；全页鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00821 | 创新监测 | 科技创新评估 | 契约-字段形态 | 科技创新评估指标清单 | 科技创新评估 | 指标元数据清单 | 成功信封下契约出参 metrics/total 若存在是否符合类型 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00819 | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-01 | 1、若 code 属成功集合且载荷含 metrics，则 metrics 为 array；2、若载荷含 total，则 total 为 number；3、不得以 sample 内 24 条或某 metric_id 作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技创新评估 | N/A-技术项 | N/A | /innov/v1/innov/metrics | M_INNOV_PG_COMPOSITE | INTEG | | | endpoint_id=innov.tech-evaluation.metrics catalog_page_id=innov.tech-evaluation 组合=MET-01；矩阵挂 metrics、total |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00822 | 创新监测 | 科技创新评估 | 备选-省略module | 科技创新评估指标清单 | 科技创新评估 | 指标元数据清单 | catalog 可选 module 省略时接口仍返回可解析信封 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00819 | 1.GET /innov/v1/innov/metrics（无查询参数，组合 MET-02） | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data 为对象且 metrics/total 形态同契约或为空；4、禁止将省略 module 与 MET-01 条数一致作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技创新评估 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.tech-evaluation.metrics catalog_page_id=innov.tech-evaluation 组合=MET-02；矩阵挂 module |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00823 | 创新监测 | 科技创新评估 | 异常-非法module | 科技创新评估指标清单 | 科技创新评估 | 指标元数据清单 | module 非法取值时返回可识别失败而非伪指标清单成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/innov/metrics，查询参数取组合 MET-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 metrics 数组的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技创新评估 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.tech-evaluation.metrics catalog_page_id=innov.tech-evaluation 组合=MET-03；矩阵挂 module、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MET-01 | innov.tech-evaluation.metrics | `module=tech-evaluation`（对齐 catalog `sampleRequest` / params example） | unavailable 主组合（本页 module slug） |
| MET-02 | innov.tech-evaluation.metrics | 不传 `module` | 可选 module 省略 |
| MET-03 | innov.tech-evaluation.metrics | `module=__invalid__` | 非法 module slug（单缺陷） |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| innov.tech-evaluation.metrics | GET | /innov/v1/innov/metrics | unavailable | module（可选，example `tech-evaluation`） |

catalog `responseFields`（形态参考，禁止 sample 数值验收）：`metrics`（array）、`total`（number）。

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.tech-evaluation.metrics | API-00819、00820、00821、00822、00823 |

---

## 3. 覆盖自检（§S1）

- [x] 本页 **0** 条 FUNC
- [x] 1 个 endpoint **5** 条 API 用例（单 endpoint 套餐）
- [x] unavailable endpoint 契约占位（API-00819），未写 sample 数值通过条件
- [x] 异常-鉴权 1 条（API-00820）
- [x] 可选 module：省略 1 条（00822）、非法 1 条（00823）
- [x] responseFields 契约占位 1 条（API-00821 metrics/total）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言信封（API-00819）
- [x] `coverage-fp.md` 已更新
- [x] 编号闭区间 **API-00819**～**API-00823**（**未**改 `code-registry.yaml` / `run-log.md`）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-00819**～**API-00823** |
| endpoint 数 | **1**（5 条/endpoint） |
| 金样（完整信封） | **1**（API-00819） |
| `_empty` 未覆盖 | **1**（见 coverage） |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
