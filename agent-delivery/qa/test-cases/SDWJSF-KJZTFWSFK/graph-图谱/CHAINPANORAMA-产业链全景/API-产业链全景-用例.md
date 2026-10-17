# 智能服务集群-科技专题服务算法库测试用例（产业链全景 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：图谱 / 产业链全景  
> **catalog**：`entry_id=chain.panorama` · `catalog_page_id=chain.panorama` · path `/chain/panorama`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.panorama`（2 endpoints）  
> **A 线对照**：`fp-split-by-api-run/work/L05.md`（ops）· `L14.md`（main）  
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
| 断言分工 | **API-00312（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 含 array 型 nodes/edges）；同册其余用例在前置写「信封规则见 §0，金样见 API-00312」后，可只断言 data 载荷或失败态 |
| catalog 状态 | 本页 **2** 个 endpoint 均为 catalog `status=running`（live）；**禁止**将 `sampleResponse` 中节点/边示例数量、vid、权重作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl / 浏览器；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST ops 为 JSON body + path 段 `op_id`；GET main 的 `chainId` 为 path 变量；组合见附录 A |
| 样例与契约差 | 样例顶层常含 `source`/`space` 等多于 `responseFields`；断言 **仅强制** catalog `responseFields`（main：nodes、edges；ops：written_nodes、written_edges、skipped、source、space） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.panorama`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00312 | 图谱 | 产业链全景 | 主流程-全景成功 | 全景图谱 | 产业链全景 | 全景图谱 | 全景图谱在合法 chainId 下返回成功信封与 nodes/edges | 1、已按 §0 携带有效 token 与租户头；2、断言对象为完整原始响应信封 | 1.GET /chain/v1/chain/INB13/panorama（path 取组合 MAIN-01） | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.nodes 存在且为 array；5、data.edges 存在且为 array；6、禁止将 sample 中空数组长度当作唯一通过条件 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama |  | INTEG |  |  | endpoint_id=chain.panorama.main catalog_page_id=chain.panorama 组合=MAIN-01 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00313 | 图谱 | 产业链全景 | 异常-鉴权 | 全景图谱 | 产业链全景 | 全景图谱 | 全景图谱缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /chain/v1/chain/INB13/panorama，组合 MAIN-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功全景 nodes/edges 载荷） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama |  | INTEG |  |  | endpoint_id=chain.panorama.main catalog_page_id=chain.panorama 组合=MAIN-01；全页其它 endpoint 鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00314 | 图谱 | 产业链全景 | 异常-非法chainId | 全景图谱 | 产业链全景 | 全景图谱 | 全景图谱在非法 chainId 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.GET /chain/v1/chain/__invalid__/panorama（组合 MAIN-02） | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将失败当作含可信 nodes/edges 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama |  | INTEG |  |  | endpoint_id=chain.panorama.main catalog_page_id=chain.panorama 组合=MAIN-02；矩阵挂 chainId、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00315 | 图谱 | 产业链全景 | 主流程-ops dry_run | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | A 产业识别 dry_run 在合法入参下返回图谱写入契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-01 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data 为对象；4、data.written_nodes 存在且为 array；5、data.written_edges 存在且为 array；6、data.skipped 存在且为 array；7、data.source 存在且为 string；8、data.space 存在且为 string | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00316 | 图谱 | 产业链全景 | 异常-缺必填scope | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | 写入接口缺少 scope 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作空 written_nodes 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-02；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00317 | 图谱 | 产业链全景 | 异常-非法scope | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | 写入接口 scope 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 scope 当作 batch 默认成功 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-03；矩阵挂 scope、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00318 | 图谱 | 产业链全景 | 主流程-B depends | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | B depends_on dry_run 在含 relation_whitelist 时返回契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.POST /chain/v1/chain/graph/ops/CHAIN_RE_DEPENDS_ON，请求体取组合 OPS-04 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data.written_edges 存在且为 array；4、data.skipped 存在且为 array | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-04；矩阵挂 relation_whitelist |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00319 | 图谱 | 产业链全景 | 异常-缺relation_whitelist | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | B 类写入缺少 relation_whitelist 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /chain/v1/chain/graph/ops/CHAIN_RE_DEPENDS_ON，请求体取组合 OPS-05 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-05；矩阵挂 relation_whitelist、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00320 | 图谱 | 产业链全景 | 主流程-C 产业企业 | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | C 产业-企业 dry_run 在含 dest_types 时返回契约字段 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.POST /chain/v1/chain/graph/ops/CHAIN_RE_INDUSTRY_ENTERPRISE，请求体取组合 OPS-06 | 1、HTTP 状态为 200；2、响应 code 属于成功集合；3、data.written_edges 存在且为 array；4、data.dest_types 若出现在 data 则类型为 array（非 responseFields 强制项，不设失败） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-06；矩阵挂 dest_types |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00321 | 图谱 | 产业链全景 | 异常-非法op_id | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | path 段 op_id 非法时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /chain/v1/chain/graph/ops/__INVALID_OP__，请求体取组合 OPS-01 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将未知 op_id 当作空 written_nodes 成功态 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-01；矩阵挂 op_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00322 | 图谱 | 产业链全景 | 异常-scope=one缺id | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | scope=one 且未提供 id 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-07 | 1、响应为失败态（code 非成功集合或 HTTP 4xx） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-07；矩阵挂 id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00323 | 图谱 | 产业链全景 | 备选-batch+filter | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | scope=batch 且带 filter 时接口可识别并返回契约形态 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-08 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data 含 written_nodes/written_edges/skipped 数组字段 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-08；矩阵挂 filter |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00324 | 图谱 | 产业链全景 | 备选-mode=llm | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | mode=llm 时接口返回可解析信封与契约字段形态 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-09 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、若 code 属成功集合则 data.source 存在且为 string | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-09；矩阵挂 mode |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00325 | 图谱 | 产业链全景 | 备选-dry_run=false | A/B/C 按 op_id 写入 | 产业链全景 | A/B/C 按 op_id 写入 | dry_run=false 时仍返回可解析契约信封（不写死写入条数） | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00312 | 1.POST /chain/v1/chain/graph/ops/CHAIN_NER_INDUSTRY，请求体取组合 OPS-10 | 1、HTTP 状态为 200 或 4xx；2、响应体含可解析 code；3、禁止将 sample 写入条数作为通过条件；4、若 code 属成功集合则 data.skipped 为 array | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.panorama.ops catalog_page_id=chain.panorama 组合=OPS-10；矩阵挂 dry_run；执行期注意真实写入风险 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| MAIN-01 | chain.panorama.main | path chainId=INB13（catalog example） | 主路径合法 chainId |
| MAIN-02 | chain.panorama.main | path chainId=__invalid__ | 非法 chainId |
| OPS-01 | chain.panorama.ops | path op_id=CHAIN_NER_INDUSTRY；body：scope=one；id=INB13；mode=rule；dry_run=true | A 类主路径 dry_run |
| OPS-02 | chain.panorama.ops | path CHAIN_NER_INDUSTRY；body 不含 scope；id=INB13；dry_run=true | 缺必填 scope |
| OPS-03 | chain.panorama.ops | path CHAIN_NER_INDUSTRY；scope=__invalid__；id=INB13 | 非法 scope |
| OPS-04 | chain.panorama.ops | path CHAIN_RE_DEPENDS_ON；scope=one；id=INB13；mode=rule；dry_run=true；relation_whitelist=["depends_on"] | B 类主路径 |
| OPS-05 | chain.panorama.ops | path CHAIN_RE_DEPENDS_ON；scope=one；id=INB13；dry_run=true；不含 relation_whitelist | 缺 relation_whitelist |
| OPS-06 | chain.panorama.ops | path CHAIN_RE_INDUSTRY_ENTERPRISE；scope=one；id=INB13；mode=rule；dry_run=true；dest_types=["enterprise"] | C 类主路径 |
| OPS-07 | chain.panorama.ops | path CHAIN_NER_INDUSTRY；scope=one；不含 id；dry_run=true | scope=one 缺 id |
| OPS-08 | chain.panorama.ops | path CHAIN_NER_INDUSTRY；scope=batch；filter={"all":true}；mode=rule；dry_run=true | batch+filter |
| OPS-09 | chain.panorama.ops | path CHAIN_NER_INDUSTRY；scope=one；id=INB13；mode=llm；dry_run=true | mode=llm |
| OPS-10 | chain.panorama.ops | path CHAIN_NER_INDUSTRY；scope=one；id=INB13；mode=rule；dry_run=false | dry_run 关闭 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| chain.panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | running | path op_id；body scope |
| chain.panorama.main | GET | /chain/v1/chain/{chainId}/panorama | running | path chainId |

---

## 3. 覆盖自检

- [x] 2 个 live endpoint 均已写主路径用例（API-00312、API-00315）
- [x] main 必填 chainId 非法哨兵（API-00314）
- [x] ops 必填 scope 缺省/非法、B 类 relation_whitelist、path op_id 非法、scope=one 缺 id 已覆盖
- [x] 异常-鉴权全页 1 条（API-00313，ops 备注「鉴权同 API-00313」）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（未试调，无稳定必空构造）
- [x] 金样 1 条且断言完整信封（API-00312）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新（L05+L14 grep 对齐）
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **14** 条；编号 **API-00312**～**API-00325**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **14**（00312～00325） |
| catalog endpoint 数 | **2** |
| 金样（完整信封） | **1**（API-00312） |
| 异常-鉴权 | **1**（API-00313） |
| live 主路径 | **2**（API-00312 main、API-00315 ops） |
| `_empty`（L05+L14） | **2** 行 **未覆盖** |
| code-registry 回写 | **父控**（本子任务未改） |
| A 线 grep（L05+L14 live field） | **20** 行中 **18** 行已挂用例；**2** 行 `_empty` 未覆盖；**3** 行 req_only 不纳入 API 矩阵 |
