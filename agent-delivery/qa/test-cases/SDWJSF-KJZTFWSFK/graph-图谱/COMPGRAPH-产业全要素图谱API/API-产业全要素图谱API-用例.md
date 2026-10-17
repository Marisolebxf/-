# 智能服务集群-科技专题服务算法库测试用例（产业全要素图谱 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 产业全要素图谱 API  
> **catalog**：`entry_id=comp.graph` · `catalog_page_id=comp.graph` · path `/industry-comp/graph`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.graph`（6 endpoints）  
> **A 线对照**：`fp-split-by-api-run/work/L13.md`（产业全要素图谱 API 服务开发）  
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
| 断言分工 | **API-000704（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-000704」后，可只断言 **data 载荷** 或失败态 |
| catalog 状态 | 本页 **6** 个 endpoint 均为 catalog `status=available`；**禁止**将 `sampleResponse` 中 nodes/edges/items/score/density/权重/vid 等示例数值作为通过条件（仅断言 `responseFields` 存在与类型） |
| 试调 | **未试调**（本子任务禁止 curl / 浏览器；`comp.graph.browse` 在 catalog 为 available 但本轮未现场复核，执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST 类为 JSON body；GET 类为查询参数；组合见附录 A |
| 样例与契约差 | 样例顶层常多于 `responseFields`（如 `op_id`、`written_nodes`、`total`、`tags`）；断言 **仅强制** catalog `responseFields` |
| 稳定 VID 占位 | catalog example `ent:ORG00000002`（执行期可替换，禁止用名称猜 VID） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.graph`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000704 | 图谱 | 产业全要素图谱 API | 主流程-浏览成功 | D 浏览 COMP_GRAPH_BROWSE | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | 图谱浏览在有效鉴权下返回成功信封与契约出参字段 | 1、已确认 catalog `comp.graph.browse` 为 available；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.nodes 存在且为 array；5、data.edges 存在且为 array；6、data.space 存在且为 string；7、不得将 sampleResponse 节点条数或权重作为通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph | M_COMP_GRAPH_116_1 | INTEG |  |  | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-01 金样 catalog_status=available §0未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000705 | 图谱 | 产业全要素图谱 API | 异常-鉴权 | D 浏览 COMP_GRAPH_BROWSE | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | 图谱浏览缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务图谱载荷） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph |  | INTEG |  |  | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-01；全页鉴权代表 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000706 | 图谱 | 产业全要素图谱 API | 异常-非法hops | D 浏览 COMP_GRAPH_BROWSE | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | 图谱浏览 hops 非整数时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-000704 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将类型错误当作含可信 nodes 的成功数据 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph |  | INTEG |  |  | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-02；矩阵挂 hops、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000707 | 图谱 | 产业全要素图谱 API | 异常-limit越界 | D 浏览 COMP_GRAPH_BROWSE | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | 图谱浏览 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph |  | INTEG |  |  | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000708 | 图谱 | 产业全要素图谱 API | 异常-非法center | D 浏览 COMP_GRAPH_BROWSE | 产业全要素图谱 API | D 浏览 COMP_GRAPH_BROWSE | 图谱浏览 center 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph，查询参数取组合 BRW-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 center 当作空图成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph |  | INTEG |  |  | endpoint_id=comp.graph.browse catalog_page_id=comp.graph 组合=BRW-04；矩阵挂 center、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000709 | 图谱 | 产业全要素图谱 API | 主流程-实体检索 | 实体检索 COMP_ENTITY_SEARCH | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索在合法 q 下返回 items 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.items 存在且为 array | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities | M_COMP_GRAPH_116_1 | INTEG |  |  | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000710 | 图谱 | 产业全要素图谱 API | 异常-缺必填q | 实体检索 COMP_ENTITY_SEARCH | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索缺少 q 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 items 冒充 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities |  | INTEG |  |  | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-02；矩阵挂 q、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000711 | 图谱 | 产业全要素图谱 API | 异常-空关键词 | 实体检索 COMP_ENTITY_SEARCH | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 q 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities |  | INTEG |  |  | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-03；矩阵挂 q、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000712 | 图谱 | 产业全要素图谱 API | 异常-非法sort | 实体检索 COMP_ENTITY_SEARCH | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索 sort 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 sort 当作默认排序成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities |  | INTEG |  |  | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-04；矩阵挂 sort、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000713 | 图谱 | 产业全要素图谱 API | 备选-分页排序 | 实体检索 COMP_ENTITY_SEARCH | 产业全要素图谱 API | 实体检索 COMP_ENTITY_SEARCH | 实体检索带 sort 与 size 组合时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/entities，查询参数取组合 ENT-05 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.items 为 array；4、禁止将 sample 条数作为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/entities |  | INTEG |  |  | endpoint_id=comp.graph.entities catalog_page_id=comp.graph 组合=ENT-05；矩阵挂 size |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000714 | 图谱 | 产业全要素图谱 API | 主流程-关系查询 | 关系查询 COMP_REL_QUERY | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询在合法 src 下返回 edges 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.edges 存在且为 array | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations | M_COMP_GRAPH_116_1 | INTEG |  |  | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000715 | 图谱 | 产业全要素图谱 API | 异常-缺必填src | 关系查询 COMP_REL_QUERY | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询缺少 src 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 edges 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations |  | INTEG |  |  | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-02；矩阵挂 src、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000716 | 图谱 | 产业全要素图谱 API | 异常-非法direction | 关系查询 COMP_REL_QUERY | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 direction 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 direction 当作 both 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations |  | INTEG |  |  | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-03；矩阵挂 direction、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000717 | 图谱 | 产业全要素图谱 API | 异常-非法src | 关系查询 COMP_REL_QUERY | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询 src 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 src 当作无关系成功空图 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations |  | INTEG |  |  | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-04；矩阵挂 src、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000718 | 图谱 | 产业全要素图谱 API | 备选-多参数 | 关系查询 COMP_REL_QUERY | 产业全要素图谱 API | 关系查询 COMP_REL_QUERY | 关系查询带 dst 与 rel 组合时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/relations，查询参数取组合 REL-05 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.edges 为 array；4、禁止将 sample 边类型作唯一通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/relations |  | INTEG |  |  | endpoint_id=comp.graph.relations catalog_page_id=comp.graph 组合=REL-05；矩阵挂 dst、rel |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000719 | 图谱 | 产业全要素图谱 API | 主流程-可视化 | 可视化 COMP_GRAPH_VIZ | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 图谱可视化在 layout=graph 下返回 nodes 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.nodes 存在且为 array | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz | M_COMP_GRAPH_116_1 | INTEG |  |  | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000720 | 图谱 | 产业全要素图谱 API | 异常-非法layout | 可视化 COMP_GRAPH_VIZ | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 图谱可视化 layout 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 layout 当作 graph 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz |  | INTEG |  |  | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-02；矩阵挂 layout、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000721 | 图谱 | 产业全要素图谱 API | 异常-limit越界 | 可视化 COMP_GRAPH_VIZ | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 图谱可视化 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz |  | INTEG |  |  | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000722 | 图谱 | 产业全要素图谱 API | 备选-wordcloud | 可视化 COMP_GRAPH_VIZ | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 图谱可视化 layout=wordcloud 时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-04 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.nodes 为 array；4、样例 tags 字段不设失败条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz |  | INTEG |  |  | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000723 | 图谱 | 产业全要素图谱 API | 备选-多参数 | 可视化 COMP_GRAPH_VIZ | 产业全要素图谱 API | 可视化 COMP_GRAPH_VIZ | 图谱可视化带 layout 与 limit 组合时响应可解析 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/viz，查询参数取组合 VIZ-05 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、禁止将 sample 节点条数作为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/viz |  | INTEG |  |  | endpoint_id=comp.graph.viz catalog_page_id=comp.graph 组合=VIZ-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000724 | 图谱 | 产业全要素图谱 API | 主流程-语义相似 | 语义相似 COMP_SEMANTIC_SIM | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似在合法 a、b 下返回 score 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.score 存在且为 number | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar | M_COMP_GRAPH_116_1 | INTEG |  |  | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000725 | 图谱 | 产业全要素图谱 API | 异常-缺必填a | 语义相似 COMP_SEMANTIC_SIM | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似缺少 a 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 score 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar |  | INTEG |  |  | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-02；矩阵挂 a、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000726 | 图谱 | 产业全要素图谱 API | 异常-缺必填b | 语义相似 COMP_SEMANTIC_SIM | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似缺少 b 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar |  | INTEG |  |  | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-03；矩阵挂 b、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000727 | 图谱 | 产业全要素图谱 API | 异常-非法mode | 语义相似 COMP_SEMANTIC_SIM | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似 mode 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 mode 当作 rule 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar |  | INTEG |  |  | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-04；矩阵挂 mode、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000728 | 图谱 | 产业全要素图谱 API | 备选-省略mode | 语义相似 COMP_SEMANTIC_SIM | 产业全要素图谱 API | 语义相似 COMP_SEMANTIC_SIM | 语义相似省略 mode 时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.POST /industry-comp/v1/comp/graph/similar，请求体取组合 SIM-05 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.score 为 number；4、禁止将 sample 0.5 作为通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/similar |  | INTEG |  |  | endpoint_id=comp.graph.similar catalog_page_id=comp.graph 组合=SIM-05 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000729 | 图谱 | 产业全要素图谱 API | 主流程-网络指标 | 网络指标 COMP_NETWORK_METRIC | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标在合法参数下返回 density 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.density 存在且为 number | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics | M_COMP_GRAPH_116_1 | INTEG |  |  | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000730 | 图谱 | 产业全要素图谱 API | 异常-limit越界 | 网络指标 COMP_NETWORK_METRIC | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics |  | INTEG |  |  | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-02；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000731 | 图谱 | 产业全要素图谱 API | 异常-非法center | 网络指标 COMP_NETWORK_METRIC | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标 center 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 center 当作 density=0 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics |  | INTEG |  |  | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-03；矩阵挂 center、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000732 | 图谱 | 产业全要素图谱 API | 备选-省略center | 网络指标 COMP_NETWORK_METRIC | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标省略 center 仅传 limit 时响应可解析 | 1、已按 §0 携带有效 token 与租户头；2、信封成功见 API-000704 | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-04 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.density 为 number；4、禁止将 sample density=0 作为唯一通过条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics |  | INTEG |  |  | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-04 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-000733 | 图谱 | 产业全要素图谱 API | 备选-多参数 | 网络指标 COMP_NETWORK_METRIC | 产业全要素图谱 API | 网络指标 COMP_NETWORK_METRIC | 网络指标带 center 与 limit 组合时响应可解析 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /industry-comp/v1/comp/graph/metrics，查询参数取组合 MET-05 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、样例 node_count/edge_count/centrality 不设失败条件 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /industry-comp/v1/comp/graph/metrics |  | INTEG |  |  | endpoint_id=comp.graph.metrics catalog_page_id=comp.graph 组合=MET-05 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| BRW-01 | comp.graph.browse | center=ent:ORG00000002；hops=1；limit=40（catalog sampleRequest，执行期可替换） | 主路径全参 |
| BRW-02 | comp.graph.browse | center=ent:ORG00000002；hops=not_int；limit=40 | 非法 hops 类型 |
| BRW-03 | comp.graph.browse | center=ent:ORG00000002；hops=1；limit=-1 | limit 越界 |
| BRW-04 | comp.graph.browse | center=__invalid__；hops=1；limit=40 | 非法 center |
| ENT-01 | comp.graph.entities | q=量子；sort=name；size=20（catalog sampleRequest） | 主路径 |
| ENT-02 | comp.graph.entities | 不传 q；sort=name | 缺必填 q |
| ENT-03 | comp.graph.entities | q=（空字符串）；sort=name | 空关键词 |
| ENT-04 | comp.graph.entities | q=量子；sort=__invalid__ | 非法 sort |
| ENT-05 | comp.graph.entities | q=量子；sort=-weight；size=10 | 分页排序组合 |
| REL-01 | comp.graph.relations | src=ent:ORG00000002；direction=both（catalog sampleRequest） | 主路径 |
| REL-02 | comp.graph.relations | 不传 src；direction=both | 缺必填 src |
| REL-03 | comp.graph.relations | src=ent:ORG00000002；direction=__invalid__ | 非法 direction |
| REL-04 | comp.graph.relations | src=__invalid__；direction=both | 非法 src |
| REL-05 | comp.graph.relations | src=ent:ORG00000002；dst=chain:IC；rel=industry_belong；direction=out | 多参数组合 |
| VIZ-01 | comp.graph.viz | layout=graph；limit=40（catalog sampleRequest） | 主路径关系图 |
| VIZ-02 | comp.graph.viz | layout=__invalid__；limit=40 | 非法 layout |
| VIZ-03 | comp.graph.viz | layout=graph；limit=-1 | limit 越界 |
| VIZ-04 | comp.graph.viz | layout=wordcloud；limit=40 | 词云布局 |
| VIZ-05 | comp.graph.viz | layout=graph；limit=20 | 多参数组合 |
| SIM-01 | comp.graph.similar | a=量子；b=量子计算；mode=rule（catalog sampleRequest） | 主路径 |
| SIM-02 | comp.graph.similar | 不含 a；b=量子计算；mode=rule | 缺必填 a |
| SIM-03 | comp.graph.similar | a=量子；不含 b；mode=rule | 缺必填 b |
| SIM-04 | comp.graph.similar | a=量子；b=量子计算；mode=__invalid__ | 非法 mode |
| SIM-05 | comp.graph.similar | a=量子；b=量子计算（省略 mode） | 省略可选 mode |
| MET-01 | comp.graph.metrics | limit=40（catalog sampleRequest，center 可选省略） | 主路径 |
| MET-02 | comp.graph.metrics | limit=-1 | limit 越界 |
| MET-03 | comp.graph.metrics | center=__invalid__；limit=40 | 非法 center |
| MET-04 | comp.graph.metrics | limit=40（不传 center） | 省略 center |
| MET-05 | comp.graph.metrics | center=ent:ORG00000002；limit=20 | 多参数组合 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| comp.graph.browse | GET | /industry-comp/v1/comp/graph | available | （无；center/hops/limit 均可选） |
| comp.graph.entities | GET | /industry-comp/v1/comp/graph/entities | available | q |
| comp.graph.relations | GET | /industry-comp/v1/comp/graph/relations | available | src |
| comp.graph.viz | GET | /industry-comp/v1/comp/graph/viz | available | （无；layout/limit 可选） |
| comp.graph.similar | POST | /industry-comp/v1/comp/graph/similar | available | a、b |
| comp.graph.metrics | GET | /industry-comp/v1/comp/graph/metrics | available | （无；center/limit 可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.graph.browse | API-000704, API-000705, API-000706, API-000707, API-000708 |
| comp.graph.entities | API-000709, API-000710, API-000711, API-000712, API-000713 |
| comp.graph.relations | API-000714, API-000715, API-000716, API-000717, API-000718 |
| comp.graph.viz | API-000719, API-000720, API-000721, API-000722, API-000723 |
| comp.graph.similar | API-000724, API-000725, API-000726, API-000727, API-000728 |
| comp.graph.metrics | API-000729, API-000730, API-000731, API-000732, API-000733 |

---

## 3. 覆盖自检

- [x] 6 个 available endpoint 均已写主路径（每 endpoint 首条 P0）
- [x] 必填入参 q / src / a / b 缺省已覆盖
- [x] 异常-鉴权全页 1 条（API-000705，其余 endpoint 备注「鉴权同 API-000705」）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（未试调，无稳定合法入参下必空证据）
- [x] 金样 1 条且断言完整信封（API-000704，`comp.graph.browse`）
- [x] §0 标明 **未试调**、禁止 curl；browse catalog=available 已注明
- [x] `coverage-fp.md` 已更新（L13）
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

**统计**：用例 **30** 条；编号 **API-000704**～**API-000733**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **30**（000704～000733） |
| catalog endpoint 数 | **6** |
| 金样（完整信封） | **1**（API-000704） |
| 异常-鉴权 | **1**（API-000705） |
| live 主路径 | **6**（browse/entities/relations/viz/similar/metrics 各 1） |
| `_empty`（L13） | **6** 行 **未覆盖** |
| req_only（L13） | **2** 行 **不纳入** |
| code-registry 回写 | **父控**（本子任务未改） |
