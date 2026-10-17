# 智能服务集群-科技专题服务算法库测试用例（技术图谱 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 技术图谱  
> **catalog**：`entry_id=innov.graph` · `catalog_page_id=innov.graph` · path `/innov/graph`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.graph`（3 endpoints）  
> **A 线对照**：`fp-split-by-api-run/_l6-to-catalog-map.yaml`（`innov.*` 不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1 · §编写细则 A～I  
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
| 断言分工 | **API-00754（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00754」后，可只断言 **data 载荷** 或失败态 |
| catalog 状态 | 本页 **3** 个 endpoint 均为 catalog `status=running`、`runtime=java_api`（按 **live** 主路径验收，等价 playbook 之 `available`）；**禁止**将 `sampleResponse` 中领域名、影响分、rank、nodes/edges 条数或示例实体名作为通过条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 请求体 | 本页均为 **GET** 查询参数；组合见附录 A |
| 样例与契约差 | `domains` 样例为数组元素含 `parentId`/`level`/`domainSource` 等；`subgraph` 样例含 `period`；`rank` 样例含 `total`/`period` 及 `list` 元素内 `rankInDomain` 等。断言 **仅强制** catalog `responseFields`（`domains`：domainId、name；`subgraph`：nodes、edges；`rank`：list） |
| 稳定领域占位 | catalog example `domainId=D-AI`（执行期可替换，禁止用领域中文名猜 id） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00754`～`00768`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.graph`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00754 | 创新监测 | 技术图谱 | 主流程-列表成功 | 领域树 | M2 创新点落图与赋分 | 领域树 | 领域树在有效鉴权下返回成功信封与契约出参字段 | 1、已确认 catalog `innov.graph.domains` 为 running；2、已按 §0 携带有效 token 与租户头；3、断言对象为完整原始响应信封 | 1.GET /innov/v1/graph/domains（无查询参数，组合 GRA-DOM-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为数组；4、若数组非空则元素含 string 型 domainId 与 name；5、不得将 sampleResponse 领域条数或 level 示例作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/domains | | INTEG | | | endpoint_id=innov.graph.domains catalog_page_id=innov.graph 组合=GRA-DOM-01 金样 catalog_status=running §0未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00755 | 创新监测 | 技术图谱 | 异常-鉴权 | 领域树 | M2 创新点落图与赋分 | 领域树 | 领域树缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/graph/domains，组合 GRA-DOM-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务领域树载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/domains | | INTEG | | | endpoint_id=innov.graph.domains catalog_page_id=innov.graph 组合=GRA-DOM-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00756 | 创新监测 | 技术图谱 | 契约-字段形态 | 领域树 | M2 创新点落图与赋分 | 领域树 | 成功信封下领域树契约字段 domainId/name 形态符合 catalog | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00754 | 1.GET /innov/v1/graph/domains，组合 GRA-DOM-01 | 1、若 code 属成功集合且 data 为非空数组，则每条元素 domainId、name 存在且为 string；2、不得以样例「人工智能」等名称或 parentId 层级作通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/domains | | INTEG | | | endpoint_id=innov.graph.domains catalog_page_id=innov.graph 组合=GRA-DOM-01；矩阵挂 domainId、name |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00757 | 创新监测 | 技术图谱 | 异常-错误方法 | 领域树 | M2 创新点落图与赋分 | 领域树 | 领域树使用 POST 时返回可识别非 GET 成功态 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /innov/v1/graph/domains（无请求体） | 1、HTTP 状态为 405 或 4xx/5xx，或响应 code 不属于成功集合；2、不得将错误方法响应当作含可信领域数组的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/domains | | INTEG | | | endpoint_id=innov.graph.domains catalog_page_id=innov.graph；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00758 | 创新监测 | 技术图谱 | 异常-路径不存在 | 领域树 | M2 创新点落图与赋分 | 领域树 | 错误 path 后缀时不得返回领域树成功载荷 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/domains/__not_found__ | 1、HTTP 状态为 404 或 4xx/5xx，或响应 code 不属于成功集合；2、不得将 404 响应当作与 GRA-DOM-01 等价的领域树成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/domains | | INTEG | | | endpoint_id=innov.graph.domains catalog_page_id=innov.graph；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00759 | 创新监测 | 技术图谱 | 主流程-子图成功 | 领域子图 | M2 创新点落图与赋分 | 领域子图 | 领域子图在合法 domainId 下返回成功信封与 nodes/edges 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-00754 | 1.GET /innov/v1/graph/subgraph，查询参数取组合 GRA-SUB-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.nodes 存在且为 array；5、data.edges 存在且为 array；6、不得将 sample 节点影响力或边 weight 作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=GRA-SUB-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00760 | 创新监测 | 技术图谱 | 异常-鉴权 | 领域子图 | M2 创新点落图与赋分 | 领域子图 | 领域子图缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization | 1.GET /innov/v1/graph/subgraph，查询参数取组合 GRA-SUB-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务子图载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=GRA-SUB-01；鉴权同 API-00755 语义 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00761 | 创新监测 | 技术图谱 | 异常-缺必填domainId | 领域子图 | M2 创新点落图与赋分 | 领域子图 | 领域子图缺少 domainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/subgraph，查询参数取组合 GRA-SUB-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 nodes/edges 的成功子图 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=GRA-SUB-02；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00762 | 创新监测 | 技术图谱 | 异常-非法domainId | 领域子图 | M2 创新点落图与赋分 | 领域子图 | 领域子图 domainId 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/subgraph，查询参数取组合 GRA-SUB-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 domainId 当作空图成功态冒充 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=GRA-SUB-03；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00763 | 创新监测 | 技术图谱 | 异常-limit越界 | 领域子图 | M2 创新点落图与赋分 | 领域子图 | 领域子图 limit 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/subgraph，查询参数取组合 GRA-SUB-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/subgraph | | INTEG | | | endpoint_id=innov.graph.subgraph catalog_page_id=innov.graph 组合=GRA-SUB-04；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00764 | 创新监测 | 技术图谱 | 主流程-排行成功 | 影响分排行 | M2 创新点落图与赋分 | 影响分排行 | 影响分排行在典型分页参数下返回成功信封与 list 契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-00754 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 GRA-RNK-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.list 存在且为 array；5、不得将 sample 中 influenceScore 或 rankInDomain 示例值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=GRA-RNK-01 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00765 | 创新监测 | 技术图谱 | 异常-鉴权 | 影响分排行 | M2 创新点落图与赋分 | 影响分排行 | 影响分排行缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 GRA-RNK-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 list 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=GRA-RNK-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00766 | 创新监测 | 技术图谱 | 异常-非法domainId | 影响分排行 | M2 创新点落图与赋分 | 影响分排行 | 影响分排行 domainId 明显非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 GRA-RNK-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 list 的成功排行 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=GRA-RNK-02；矩阵挂 domainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00767 | 创新监测 | 技术图谱 | 异常-非法nodeType | 影响分排行 | M2 创新点落图与赋分 | 影响分排行 | 影响分排行 nodeType 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 GRA-RNK-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 nodeType 当作「全部」成功排行 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=GRA-RNK-03；矩阵挂 nodeType、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00768 | 创新监测 | 技术图谱 | 异常-pageSize越界 | 影响分排行 | M2 创新点落图与赋分 | 影响分排行 | 影响分排行 pageSize 为负时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /innov/v1/graph/influence/rank，查询参数取组合 GRA-RNK-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·M2 创新点落图与赋分 | N/A-技术项 | N/A | /innov/v1/graph/influence/rank | | INTEG | | | endpoint_id=innov.graph.rank catalog_page_id=innov.graph 组合=GRA-RNK-04；矩阵挂 pageSize、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| GRA-DOM-01 | innov.graph.domains | 无查询参数 | 领域树主路径 |
| GRA-SUB-01 | innov.graph.subgraph | `domainId=D-AI`；`limit=60`（对齐 catalog `sampleRequest`） | 子图主路径 |
| GRA-SUB-02 | innov.graph.subgraph | 不传 `domainId`；`limit=60` | 缺必填 domainId |
| GRA-SUB-03 | innov.graph.subgraph | `domainId=__invalid__`；`limit=60` | 非法领域 id |
| GRA-SUB-04 | innov.graph.subgraph | `domainId=D-AI`；`limit=-1` | limit 越界 |
| GRA-SUB-05 | innov.graph.subgraph | `domainId=`（空字符串）；`limit=60` | 空 domainId；**本轮无独立用例**，与缺必填语义执行期 observed 合并 |
| GRA-RNK-01 | innov.graph.rank | `domainId=D-AI`；`pageNum=1`；`pageSize=20`（对齐 catalog `sampleRequest`） | 排行主路径 |
| GRA-RNK-02 | innov.graph.rank | `domainId=__invalid__`；`pageNum=1`；`pageSize=20` | 非法领域 |
| GRA-RNK-03 | innov.graph.rank | `domainId=D-AI`；`nodeType=__invalid__`；`pageNum=1`；`pageSize=20` | 非法 nodeType |
| GRA-RNK-04 | innov.graph.rank | `domainId=D-AI`；`pageNum=1`；`pageSize=-1` | pageSize 越界 |
| GRA-RNK-05 | innov.graph.rank | 不传 `domainId`；`pageNum=1`；`pageSize=20` | 默认 ALL 领域；**本轮无独立用例**，与主路径差异待试调后补备选 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 必填参数 |
|-------------|--------|------|--------|---------|----------|
| innov.graph.domains | GET | /innov/v1/graph/domains | running | java_api | （无） |
| innov.graph.subgraph | GET | /innov/v1/graph/subgraph | running | java_api | domainId |
| innov.graph.rank | GET | /innov/v1/graph/influence/rank | running | java_api | （无；domainId/nodeType/pageNum/pageSize 均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.graph.domains | API-00754～00758 |
| innov.graph.subgraph | API-00759～00763 |
| innov.graph.rank | API-00764～00768 |

---

## 3. 覆盖自检（§S1 / §I）

- [x] 3 个 live endpoint 各 1 条主路径（00754、00759、00764）
- [x] 异常-鉴权 3 条（00755、00760、00765）
- [x] `domains` 无参 L 类补契约形态 + 错误方法 + 错误 path（00756～00758）
- [x] `subgraph` 必填 domainId 缺省/非法 + limit 越界（00761～00763）
- [x] `rank` 非法 domainId/nodeType + pageSize 越界（00766～00768）
- [x] `_empty` 无稳定构造 → 矩阵 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 1 条（API-00754）断言完整信封
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务 **未改** registry / run-log；闭区间 **API-00754～00768**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **15** |
| 编号闭区间 | **API-00754**～**API-00768** |
| endpoint 数 | **3**（各 5 条） |
| `_empty` 未覆盖 | **3**（每 endpoint 1，无试调空结果证据） |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
