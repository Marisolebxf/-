# 智能服务集群-科技专题服务算法库测试用例（M1 科创事件地图 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / M1 科创事件地图  
> **catalog**：`entry_id=innov.events` · `catalog_page_id=innov.events` · path `/innov/events`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.events`  
> **A 线对照**：`fp-split-by-api-run/work/` **未收录** `innov.events`（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵见同目录 `coverage-fp.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 业务 path | `GET /innov/v1/events`（列表 **与** 地图点位共用 path，以查询参数 `mode` 区分 `endpoint_id`）；`GET /innov/v1/events/heatmap`；`GET /innov/v1/events/{eventId}`；`GET /innov/v1/events/{eventId}/relations`；`GET /innov/v1/dict/event-types` |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00859（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00859」后，可只断言 `data` 载荷或失败态 |
| catalog 状态 | 本页 **6** 个 endpoint 均为 catalog `status=running`、`runtime=java_api`；**禁止**将 `sampleResponse` 中事件标题、importanceScore=92、total=3、坐标、weight=92、关联 score 或字典 color 等示例数值作为通过条件 |
| list / geo 同 path | `innov.events.list`：无 `mode` 或 `mode`≠`geo`；`innov.events.geo`：必填查询参数 `mode=geo`；验收以 **endpoint_id** 区分，不以 path 字符串 alone 区分 |
| 样例与契约差 | 列表样例 `list[]` 含 `title`/`importanceScore` 等；契约 `responseFields` 仅 `total`、`list`。详情样例含 `title`/`summary`；契约仅 `eventId`、`importanceDetail`。关联样例含 `relDesc`/`score`；契约仅 `relType`、`relName`。字典样例含 `color`；契约仅 `eventType`、`nameZh`。热力 `sampleResponse` 为顶层数组形态；联调台 observed 可能为 `data` 数组或 `data` 内嵌数组，断言以 **元素含 number 型 lng/lat/weight** 为准 |
| 依赖链 | 详情/关联合法 `eventId` 默认 `EVT-001`（catalog example）；执行期可先调 API-00859，若 `data.list` 非空则取首条 `eventId` 替换，须在执行记录注明 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 本页 endpoint 数 | **6** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00859`～`00888`。`路由route` = catalog path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.events`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00859 | 创新监测 | M1 科创事件地图 | 主流程-列表成功 | 事件列表 | M1 科创事件地图 | 事件列表 | 事件列表在有效鉴权下返回成功信封与 total、list 字段 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、断言对象为完整原始响应信封 | 1.GET /innov/v1/events，查询参数取组合 EVT-LST-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.total 存在且为 number；5、data.list 存在且为 array；6、禁止将 sample 中 total=3 或具体事件标题作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | M_INNOV_EVENT_COUNT | INTEG | | | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=EVT-LST-01 金样 §0未试调 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00860 | 创新监测 | M1 科创事件地图 | 异常-鉴权 | 事件列表 | M1 科创事件地图 | 事件列表 | 事件列表缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /innov/v1/events，查询参数取组合 EVT-LST-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功 total/list 业务载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=EVT-LST-01；全页其它 endpoint 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00861 | 创新监测 | M1 科创事件地图 | 异常-非法pageSize | 事件列表 | M1 科创事件地图 | 事件列表 | 事件列表 pageSize 非正整数时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events，查询参数取组合 EVT-LST-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 total/list 的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=EVT-LST-03；矩阵挂 pageSize、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00862 | 创新监测 | M1 科创事件地图 | 异常-非法pageNum | 事件列表 | M1 科创事件地图 | 事件列表 | 事件列表 pageNum 为负值时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events，查询参数取组合 EVT-LST-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功分页列表冒充 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=EVT-LST-04；矩阵挂 pageNum、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00863 | 创新监测 | M1 科创事件地图 | 异常-非法importanceLevels | 事件列表 | M1 科创事件地图 | 事件列表 | 事件列表 importanceLevels 含枚举外级别时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events，查询参数取组合 EVT-LST-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或成功态下 list 可解析且不得仅凭 sample 三条记录判定通过；2、禁止将明显非法级别静默当作全量列表成功 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.list catalog_page_id=innov.events 组合=EVT-LST-05；矩阵挂 importanceLevels、list、total、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00864 | 创新监测 | M1 科创事件地图 | 主流程-点位成功 | 地图点位 | M1 科创事件地图 | 地图点位 | 地图点位在 mode=geo 下返回 type 与 features 契约字段 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events，查询参数取组合 EVT-GEO-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.type 存在且为 string；5、data.features 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=EVT-GEO-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00865 | 创新监测 | M1 科创事件地图 | 异常-缺mode | 地图点位 | M1 科创事件地图 | 地图点位 | 地图点位契约要求 mode=geo 时缺 mode 不得构成 GeoJSON 成功载荷 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events，查询参数取组合 EVT-GEO-02 | 1、响应为失败态，或成功态下 data 不构成同时含 string 型 type 与 array 型 features 的 GeoJSON 契约载荷；2、不得将列表分页 total/list 形态当作 geo 点位成功 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=EVT-GEO-02；矩阵挂 mode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00866 | 创新监测 | M1 科创事件地图 | 异常-非法mode | 地图点位 | M1 科创事件地图 | 地图点位 | 地图点位 mode 非 geo 时返回可识别失败或非 GeoJSON 载荷 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events，查询参数取组合 EVT-GEO-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或 data 不满足 type+features 契约；2、不得将非法 mode 当作 FeatureCollection 成功 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=EVT-GEO-03；矩阵挂 mode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00867 | 创新监测 | M1 科创事件地图 | 契约-字段形态 | 地图点位 | M1 科创事件地图 | 地图点位 | 成功信封下 GeoJSON type、features 若存在是否符合契约形态 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events，查询参数取组合 EVT-GEO-01 | 1、若 code 属成功集合且含 type，则 type 为 string；2、若含 features 且非空，则首条元素为 object；3、禁止将 sample 坐标 113.94/22.54 作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=EVT-GEO-01；矩阵挂 type、features |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00868 | 创新监测 | M1 科创事件地图 | 异常-错误方法 | 地图点位 | M1 科创事件地图 | 地图点位 | 地图点位 path 使用非 GET 方法时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /innov/v1/events，查询参数取组合 EVT-GEO-01 | 1、HTTP 状态为 4xx 或 405，或响应 code 非成功集合；2、不得将错误方法当作 GeoJSON 成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events | | INTEG | | | endpoint_id=innov.events.geo catalog_page_id=innov.events 组合=EVT-GEO-01；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00869 | 创新监测 | M1 科创事件地图 | 主流程-热力成功 | 热力聚合 | M1 科创事件地图 | 热力聚合 | 热力聚合在有效鉴权下返回可解析热力点载荷 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/heatmap，查询参数取组合 EVT-HM-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为 array 或对象内可定位 array 载荷；4、若数组非空则首条元素含 number 型 lng、lat、weight | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/heatmap | | INTEG | | | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=EVT-HM-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00870 | 创新监测 | M1 科创事件地图 | 备选-重复请求 | 热力聚合 | M1 科创事件地图 | 热力聚合 | 连续两次无参请求热力接口响应均可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/heatmap，组合 EVT-HM-01；2.立即重复步骤 1 一次 | 1、两次响应均含可解析 code；2、若两次 code 均成功则热力载荷均为可解析 array 形态；3、禁止要求两次数组长度完全一致 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/heatmap | | INTEG | | | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=EVT-HM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00871 | 创新监测 | M1 科创事件地图 | 契约-字段形态 | 热力聚合 | M1 科创事件地图 | 热力聚合 | 成功信封下热力点 lng、lat、weight 元素类型可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/heatmap，查询参数取组合 EVT-HM-01 | 1、若 code 属成功集合且热力数组非空，则首条元素 lng、lat、weight 均为 number；2、禁止将 weight=92 等 sample 值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/heatmap | | INTEG | | | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=EVT-HM-01；矩阵挂 lng、lat、weight |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00872 | 创新监测 | M1 科创事件地图 | 异常-非法时间 | 热力聚合 | M1 科创事件地图 | 热力聚合 | 热力聚合 startTime、endTime 非法格式时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/heatmap，查询参数取组合 EVT-HM-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法时间当作含可信热力数组的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/heatmap | | INTEG | | | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=EVT-HM-02；矩阵挂 startTime、endTime、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00873 | 创新监测 | M1 科创事件地图 | 异常-错误path | 热力聚合 | M1 科创事件地图 | 热力聚合 | 热力 path 拼写错误时不得返回契约热力成功载荷 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/heatmap-invalid（组合 EVT-HM-03） | 1、HTTP 状态为 404 或 4xx，或响应 code 非成功集合；2、不得将错误 path 当作含 lng/lat/weight 数组的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/heatmap | | INTEG | | | endpoint_id=innov.events.heatmap catalog_page_id=innov.events 组合=EVT-HM-03；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00874 | 创新监测 | M1 科创事件地图 | 主流程-详情成功 | 事件详情 | M1 科创事件地图 | 事件详情 | 事件详情在合法 eventId 下返回 eventId 与 importanceDetail | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/EVT-001（path 取组合 EVT-DET-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.eventId 存在且为 string；5、data.importanceDetail 存在且为 array | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId} | | INTEG | | | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=EVT-DET-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00875 | 创新监测 | M1 科创事件地图 | 异常-非法eventId | 事件详情 | M1 科创事件地图 | 事件详情 | 事件详情 eventId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/__invalid__（组合 EVT-DET-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 eventId/importanceDetail 的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId} | | INTEG | | | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=EVT-DET-02；矩阵挂 eventId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00876 | 创新监测 | M1 科创事件地图 | 异常-空eventId | 事件详情 | M1 科创事件地图 | 事件详情 | 事件详情 path 段 eventId 为空占位时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/%20（组合 EVT-DET-03） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与合法 EVT-001 成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId} | | INTEG | | | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=EVT-DET-03；矩阵挂 eventId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00877 | 创新监测 | M1 科创事件地图 | 契约-字段形态 | 事件详情 | M1 科创事件地图 | 事件详情 | 成功信封下 importanceDetail 数组元素形态可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/EVT-001，组合 EVT-DET-01 | 1、若 code 属成功集合且 importanceDetail 非空，则首条元素为 object；2、禁止将 sample 分项 k/v 具体分值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId} | | INTEG | | | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=EVT-DET-01；矩阵挂 eventId、importanceDetail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00878 | 创新监测 | M1 科创事件地图 | 备选-依赖列表eventId | 事件详情 | M1 科创事件地图 | 事件详情 | 事件详情使用列表接口取得的 eventId 时契约字段可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、已调用 API-00859 且 data.list 非空并记录首条 eventId，或沿用 §0 默认 EVT-001 | 1.GET /innov/v1/events/{eventId}，path 取组合 EVT-DET-04 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 成功则 data.eventId 为 string 且 data.importanceDetail 为 array | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId} | | INTEG | | | endpoint_id=innov.events.detail catalog_page_id=innov.events 组合=EVT-DET-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00879 | 创新监测 | M1 科创事件地图 | 主流程-关联成功 | 关联分析 | M1 科创事件地图 | 关联分析 | 关联分析在合法 eventId 下返回可解析关联数组 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/EVT-001/relations（path 取组合 EVT-REL-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为 array；4、若数组非空则首条元素含 string 型 relType 与 relName | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations | | INTEG | | | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=EVT-REL-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00880 | 创新监测 | M1 科创事件地图 | 异常-非法eventId | 关联分析 | M1 科创事件地图 | 关联分析 | 关联分析 eventId 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/__invalid__/relations（组合 EVT-REL-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 relType/relName 的成功关联数组 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations | | INTEG | | | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=EVT-REL-02；矩阵挂 eventId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00881 | 创新监测 | M1 科创事件地图 | 异常-空eventId | 关联分析 | M1 科创事件地图 | 关联分析 | 关联分析 path 段 eventId 为空占位时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/%20/relations（组合 EVT-REL-03） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与合法 EVT-001 关联成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations | | INTEG | | | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=EVT-REL-03；矩阵挂 eventId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00882 | 创新监测 | M1 科创事件地图 | 契约-字段形态 | 关联分析 | M1 科创事件地图 | 关联分析 | 成功信封下关联元素 relType、relName 类型可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/events/EVT-001/relations，组合 EVT-REL-01 | 1、若 code 属成功集合且 data 非空，则首条元素 relType、relName 均为 string；2、禁止将 sample relDesc/score 作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations | | INTEG | | | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=EVT-REL-01；矩阵挂 relType、relName |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00883 | 创新监测 | M1 科创事件地图 | 异常-不存在eventId | 关联分析 | M1 科创事件地图 | 关联分析 | 关联分析 eventId 不存在时返回可识别失败或空数组成功 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/events/EVT-NOT-FOUND-999/relations（组合 EVT-REL-04） | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或 code 成功且 data 为空数组；2、不得将不存在 id 当作含 sample 关联对象的成功非空数组 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/events/{eventId}/relations | | INTEG | | | endpoint_id=innov.events.relations catalog_page_id=innov.events 组合=EVT-REL-04；矩阵挂 eventId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00884 | 创新监测 | M1 科创事件地图 | 主流程-字典成功 | 事件类型字典 | M1 科创事件地图 | 事件类型字典 | 事件类型字典在有效鉴权下返回可解析类型数组 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/dict/event-types（无查询参数，组合 EVT-TYP-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为 array；4、若数组非空则首条元素含 string 型 eventType 与 nameZh | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/dict/event-types | | INTEG | | | endpoint_id=innov.events.types catalog_page_id=innov.events 组合=EVT-TYP-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00885 | 创新监测 | M1 科创事件地图 | 异常-非法查询参数 | 事件类型字典 | M1 科创事件地图 | 事件类型字典 | 字典接口携带未登记查询参数时不得误判为契约失败以外的成功形态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/dict/event-types，查询参数取组合 EVT-TYP-02 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 非成功集合则为可识别失败；4、若 code 成功则 data 仍为 array 且元素含 eventType、nameZh 形态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/dict/event-types | | INTEG | | | endpoint_id=innov.events.types catalog_page_id=innov.events 组合=EVT-TYP-02；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00886 | 创新监测 | M1 科创事件地图 | 契约-字段形态 | 事件类型字典 | M1 科创事件地图 | 事件类型字典 | 成功信封下字典元素 eventType、nameZh 类型可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/dict/event-types，组合 EVT-TYP-01 | 1、若 code 属成功集合且 data 非空，则首条元素 eventType、nameZh 均为 string；2、禁止将 sample color 字段作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/dict/event-types | | INTEG | | | endpoint_id=innov.events.types catalog_page_id=innov.events 组合=EVT-TYP-01；矩阵挂 eventType、nameZh |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00887 | 创新监测 | M1 科创事件地图 | 异常-错误方法 | 事件类型字典 | M1 科创事件地图 | 事件类型字典 | 字典 path 使用非 GET 方法时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST /innov/v1/dict/event-types，组合 EVT-TYP-01 | 1、HTTP 状态为 4xx 或 405，或响应 code 非成功集合；2、不得将错误方法当作字典数组成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/dict/event-types | | INTEG | | | endpoint_id=innov.events.types catalog_page_id=innov.events 组合=EVT-TYP-01；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00888 | 创新监测 | M1 科创事件地图 | 备选-重复请求 | 事件类型字典 | M1 科创事件地图 | 事件类型字典 | 连续两次无参请求字典接口响应均可解析 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00859 | 1.GET /innov/v1/dict/event-types，组合 EVT-TYP-01；2.立即重复步骤 1 一次 | 1、两次响应均含可解析 code；2、若两次 code 均成功则 data 均为 array；3、禁止要求两次数组长度或内容完全一致 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M1 科创事件地图 | N/A-技术项 | N/A | /innov/v1/dict/event-types | | INTEG | | | endpoint_id=innov.events.types catalog_page_id=innov.events 组合=EVT-TYP-01 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| EVT-LST-01 | innov.events.list | `pageNum`: 1；`pageSize`: 20（对齐 catalog `sampleRequest`）；不传 `mode` | 列表主路径 |
| EVT-LST-02 | innov.events.list | `pageNum`: 1；`pageSize`: 20；`startTime`: `2024-01-01 00:00:00`；`endTime`: `2025-12-31 23:59:59` | 时间窗组合；**本轮无独立用例**，待试调后补 |
| EVT-LST-03 | innov.events.list | `pageNum`: 1；`pageSize`: 0 | pageSize 非正整数 |
| EVT-LST-04 | innov.events.list | `pageNum`: -1；`pageSize`: 20 | pageNum 负值越界 |
| EVT-LST-05 | innov.events.list | `importanceLevels`: `4,5`（枚举外 1/2/3） | 重要性 CSV 非法级别 |
| EVT-GEO-01 | innov.events.geo | `mode`: `geo`（catalog required） | 地图点位主路径 |
| EVT-GEO-02 | innov.events.geo | 不传 `mode`（同 path 列表语义） | 缺 geo 模式 |
| EVT-GEO-03 | innov.events.geo | `mode`: `__invalid__` | 非法 mode |
| EVT-HM-01 | innov.events.heatmap | 无查询参数 | 热力主路径 |
| EVT-HM-02 | innov.events.heatmap | `startTime`: `not-a-date`；`endTime`: `2025-12-31` | 非法时间格式 |
| EVT-HM-03 | innov.events.heatmap | path 误写为 `/innov/v1/events/heatmap-invalid` | 错误 path |
| EVT-HM-04 | innov.events.heatmap | `startTime`: `2024-01-01 00:00:00`；`endTime`: `2025-12-31 23:59:59` | 合法时间窗备选 |
| EVT-DET-01 | innov.events.detail | path `eventId`: `EVT-001`（catalog example） | 详情主路径 |
| EVT-DET-02 | innov.events.detail | path `eventId`: `__invalid__` | 非法 id |
| EVT-DET-03 | innov.events.detail | path `eventId`: 空白（URL 编码 `%20`） | 空占位 |
| EVT-DET-04 | innov.events.detail | path `eventId`: 取自 API-00859 首条 `eventId`，缺省 `EVT-001` | 列表→详情依赖 |
| EVT-REL-01 | innov.events.relations | path `eventId`: `EVT-001` | 关联主路径 |
| EVT-REL-02 | innov.events.relations | path `eventId`: `__invalid__` | 非法 id |
| EVT-REL-03 | innov.events.relations | path `eventId`: `%20` | 空占位 |
| EVT-REL-04 | innov.events.relations | path `eventId`: `EVT-NOT-FOUND-999` | 不存在 id |
| EVT-TYP-01 | innov.events.types | 无查询参数 | 字典主路径 |
| EVT-TYP-02 | innov.events.types | 未登记查询键 `debug`: `1` | 未知查询参数 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| innov.events.list | GET | /innov/v1/events | running | 无（与 geo 互斥语义见 §0） |
| innov.events.geo | GET | /innov/v1/events | running | `mode=geo` |
| innov.events.heatmap | GET | /innov/v1/events/heatmap | running | 无 |
| innov.events.detail | GET | /innov/v1/events/{eventId} | running | path `eventId` |
| innov.events.relations | GET | /innov/v1/events/{eventId}/relations | running | path `eventId` |
| innov.events.types | GET | /innov/v1/dict/event-types | running | 无 |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.events.list | API-00859、00860、00861、00862、00863 |
| innov.events.geo | API-00864、00865、00866、00867、00868 |
| innov.events.heatmap | API-00869、00870、00871、00872、00873 |
| innov.events.detail | API-00874、00875、00876、00877、00878 |
| innov.events.relations | API-00879、00880、00881、00882、00883 |
| innov.events.types | API-00884、00885、00886、00887、00888 |

---

## 3. 覆盖自检（§S1 / §I）

- [x] 6 个 `running` endpoint 各 5 条用例（共 **30** 条，API-00859～00888）
- [x] 金样 1 条且断言完整信封（**API-00859**）
- [x] 全页异常-鉴权 1 条（**API-00860**）；其余 endpoint 备注「鉴权同 API-00860」
- [x] list/geo 同 path 以 `endpoint_id` + 组合区分
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（6 处，无稳定必空试调证据）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 第 1～2 节、第 4 节与用例编号一致
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **30** |
| 编号闭区间 | **API-00859**～**API-00888** |
| endpoint 数 | **6** |
| 金样（完整信封） | **1**（API-00859） |
| 全页鉴权 | **1**（API-00860） |
| `_empty` 未覆盖 | **6**（见 coverage-fp.md） |
| FUNC | **0** |
| code-registry / run-log | **未改**（父控回写） |
| 烟测建议 | API-00859、00864、00869、00874、00879、00884 |
