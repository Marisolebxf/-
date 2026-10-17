# 智能服务集群-科技专题服务算法库测试用例（趋势预测 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 趋势预测  
> **catalog**：`entry_id=innov.forecast` · `catalog_page_id=innov.forecast` · path `/innov/forecast`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.forecast`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `innov.forecast` 行（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00784（金样）** 断言 **完整原始信封**（HTTP + `code` + 可解析 data）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00784」后，可只断言 data 载荷或失败态 |
| catalog 状态 | 本页 **3** 个 endpoint 均为 catalog `status=running`（`runtime=java_api`）；**禁止**将 `sampleResponse` 中历史年度数值、预测点 `predictValue`/`ciLower`/`ciUpper`、`contribution`、`burstScore`、事件标题或主题名称作为通过条件 |
| 样例与契约差 | `innov.forecast.domain` 样例含 `forecastMode` 等扩展字段；契约 `responseFields` 仅声明 `history`、`predictions`（array）。`innov.forecast.contributions` 样例含 `total` 与 `list` 元素内多字段；契约仅声明 `list`（array）。`innov.forecast.bursts` 样例为 **顶层数组** 形态；契约声明 `topicName`、`burstScore`（元素字段）。断言 **只强制 responseFields**；样例扩展字段不设失败条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 查询参数 | 三接口均为 GET；path 变量与查询参数组合见附录 A |
| 本页 endpoint 数 | **3** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00784`～`00798`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.forecast`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00784 | 创新监测 | 趋势预测 | 主流程-领域趋势 | 领域趋势预测 | 趋势预测 | 领域趋势预测 | 合法 domainId 下领域趋势接口返回成功信封与 history/predictions | 1、已按 §0 携带有效 token 与 TENANT-ID；2、断言对象为完整原始响应信封 | 1.GET /innov/v1/forecast/domain/D-AI（path 取组合 DOM-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.history 存在且为 array；5、data.predictions 存在且为 array；6、禁止将 sample 历史年度或预测点数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | M_INNOV_FORECAST_OUTPUT | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-01 金样 §0未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00785 | 创新监测 | 趋势预测 | 异常-鉴权 | 领域趋势预测 | 趋势预测 | 领域趋势预测 | 领域趋势接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/forecast/domain/D-AI，组合 DOM-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 history/predictions 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-01；全页其它 endpoint 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00786 | 创新监测 | 趋势预测 | 异常-非法domainId | 领域趋势预测 | 趋势预测 | 领域趋势预测 | 非法 domainId 时返回可识别失败而非伪趋势成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/forecast/domain/__invalid__（组合 DOM-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 history/predictions 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-02；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00787 | 创新监测 | 趋势预测 | 异常-空domainId | 领域趋势预测 | 趋势预测 | 领域趋势预测 | path 段 domainId 为空时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/forecast/domain/（path 段为空，组合 DOM-03） | 1、响应为失败态（HTTP 4xx 或 code 非成功集合）；2、不得将空 domainId 当作 D-AI 等价并成功返回 sample 形态预测序列 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-03；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00788 | 创新监测 | 趋势预测 | 契约-字段形态 | 领域趋势预测 | 趋势预测 | 领域趋势预测 | 成功信封下契约出参 history/predictions 若存在是否为 array | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00784 | 1.GET /innov/v1/forecast/domain/D-AI，组合 DOM-01 | 1、若 code 属成功集合且载荷含 history/predictions，则二者均为 array；2、不得以 sample 条数或 statYear/predictValue 具体数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/domain/{domainId} | M_INNOV_FORECAST_OUTPUT | INTEG | | | endpoint_id=innov.forecast.domain catalog_page_id=innov.forecast 组合=DOM-01；矩阵挂 history、predictions |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00789 | 创新监测 | 趋势预测 | 主流程-贡献度 | 创新点贡献度 | 趋势预测 | 创新点贡献度 | 合法 domainId 下贡献度接口返回成功信封与 list 数组 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00784 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CONTRIB-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.list 存在且为 array；5、禁止将 sample contribution 或事件标题作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CONTRIB-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00790 | 创新监测 | 趋势预测 | 异常-鉴权 | 创新点贡献度 | 趋势预测 | 创新点贡献度 | 贡献度接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CONTRIB-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 list 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CONTRIB-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00791 | 创新监测 | 趋势预测 | 异常-缺必填domainId | 创新点贡献度 | 趋势预测 | 创新点贡献度 | 贡献度接口缺少 domainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CONTRIB-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 list 的成功贡献度排行 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CONTRIB-02；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00792 | 创新监测 | 趋势预测 | 异常-非法pageSize | 创新点贡献度 | 趋势预测 | 创新点贡献度 | 非正整数 pageSize 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CONTRIB-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 pageSize 静默截断并成功返回 sample 形态 list | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CONTRIB-03；矩阵挂 pageSize、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00793 | 创新监测 | 趋势预测 | 契约-字段形态 | 创新点贡献度 | 趋势预测 | 创新点贡献度 | 成功信封下契约出参 list 若存在是否为 array | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00784 | 1.GET /innov/v1/forecast/contributions，查询参数取组合 CONTRIB-01 | 1、若 code 属成功集合且载荷含 list，则 list 为 array；2、不得以 sample 条数或 contribution 数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/contributions | | INTEG | | | endpoint_id=innov.forecast.contributions catalog_page_id=innov.forecast 组合=CONTRIB-01；矩阵挂 list |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00794 | 创新监测 | 趋势预测 | 主流程-主题突变 | 主题突变 | 趋势预测 | 主题突变 | 带 domainId 时主题突变接口返回成功信封与可解析载荷 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00784 | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BURST-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为 array 或含 array 型突变列表的可解析对象；4、禁止将 sample burstScore 或主题名称作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BURST-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00795 | 创新监测 | 趋势预测 | 异常-鉴权 | 主题突变 | 趋势预测 | 主题突变 | 主题突变接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BURST-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功突变列表载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BURST-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00796 | 创新监测 | 趋势预测 | 异常-非法domainId | 主题突变 | 趋势预测 | 主题突变 | 非法 domainId 查询时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BURST-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含 sample 形态突变列表的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BURST-03；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00797 | 创新监测 | 趋势预测 | 备选-不传domainId | 主题突变 | 趋势预测 | 主题突变 | catalog 可选 domainId 省略时接口仍返回可解析信封 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00784 | 1.GET /innov/v1/forecast/bursts（无查询参数，组合 BURST-02） | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则载荷为 array 或可解析列表对象；4、禁止将 sample 主题条数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BURST-02；矩阵挂 domainId |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00798 | 创新监测 | 趋势预测 | 契约-字段形态 | 主题突变 | 趋势预测 | 主题突变 | 成功载荷中契约字段 topicName/burstScore 若存在是否符合类型 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00784 | 1.GET /innov/v1/forecast/bursts，查询参数取组合 BURST-01 | 1、若 code 属成功集合且列表元素含 topicName，则 topicName 为 string；2、若含 burstScore，则 burstScore 为 number；3、不得以 sample 中 18.4 等强度值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·趋势预测 | N/A-技术项 | N/A | /innov/v1/forecast/bursts | | INTEG | | | endpoint_id=innov.forecast.bursts catalog_page_id=innov.forecast 组合=BURST-01；矩阵挂 topicName、burstScore |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| DOM-01 | innov.forecast.domain | path `domainId=D-AI`（对齐 catalog `sampleRequest`） | 领域趋势主路径 |
| DOM-02 | innov.forecast.domain | path `domainId=__invalid__` | 非法领域 ID |
| DOM-03 | innov.forecast.domain | path `domainId` 为空段（`/domain/` 后无值） | 空 path 变量边界 |
| CONTRIB-01 | innov.forecast.contributions | `domainId=D-AI`；`pageNum=1`；`pageSize=10`（对齐 catalog `sampleRequest`） | 贡献度主路径 |
| CONTRIB-02 | innov.forecast.contributions | 不传 `domainId`；`pageNum=1`；`pageSize=10` | 缺必填 domainId |
| CONTRIB-03 | innov.forecast.contributions | `domainId=D-AI`；`pageSize=0`；`pageNum=1` | 非正整数 pageSize |
| CONTRIB-04 | innov.forecast.contributions | `domainId=D-AI`；不传 `pageNum`/`pageSize` | 省略分页；**本轮无独立用例**，与 CONTRIB-01 待试调后区分 |
| BURST-01 | innov.forecast.bursts | `domainId=D-AI`（对齐 catalog `sampleRequest`） | 主题突变带领域筛选 |
| BURST-02 | innov.forecast.bursts | 不传 `domainId` | 可选 domainId 省略 |
| BURST-03 | innov.forecast.bursts | `domainId=__invalid__` | 非法领域 ID |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 参数 |
|-------------|--------|------|--------|------|
| innov.forecast.domain | GET | /innov/v1/forecast/domain/{domainId} | running | path domainId（必填） |
| innov.forecast.contributions | GET | /innov/v1/forecast/contributions | running | domainId（必填 query）；pageNum、pageSize（可选） |
| innov.forecast.bursts | GET | /innov/v1/forecast/bursts | running | domainId（可选 query） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.forecast.domain | API-00784、00785、00786、00787、00788 |
| innov.forecast.contributions | API-00789、00790、00791、00792、00793 |
| innov.forecast.bursts | API-00794、00795、00796、00797、00798 |

---

## 3. 覆盖自检（§S1）

- [x] 3 个 live endpoint 各 1 条主路径（API-00784、00789、00794），未写 sample 数值通过条件
- [x] 异常-鉴权 3 条（00785、00790、00795）；domain 备注全页鉴权代表
- [x] 入参单缺陷 6 条（domain 非法/空 path；contributions 缺 domainId、非法 pageSize；bursts 非法 domainId、省略 domainId）
- [x] responseFields 契约占位 4 条（history/predictions、list、topicName/burstScore）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条且断言完整信封（API-00784）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **15** |
| 编号闭区间 | **API-00784**～**API-00798** |
| endpoint 数 | **3**（各 5 条） |
| 金样（完整信封） | **1**（API-00784） |
| live 主路径 | **3**（00784、00789、00794） |
| `_empty` 未覆盖 | **3**（见 coverage） |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
