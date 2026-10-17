# 智能服务集群-科技专题服务算法库测试用例（引育推荐（异步） API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 引育推荐（异步）  
> **catalog**：`entry_id=innov.recommend` · `catalog_page_id=innov.recommend` · path `/innov/recommend`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` 页 `innov.recommend`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `innov.recommend` 行（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`，常见前缀 `/api`） |
| 业务 path | catalog 两 endpoint 登记 **`path` 为空**（`runtime=local_mock`，Java REST 未发布）；验收以联调台选中 endpoint 发送 **POST** 体，等价于对 `innov.recommend.attraction` / `innov.recommend.cultivation` 契约调用，**不得**臆造未登记 REST path |
| 鉴权头 | `Authorization: Bearer <access_token>`（50897 OAuth 密码模式，账号口径见 `lumen-ui-algo-apiview` LoginView）；`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00744（金样·招引）** 与 **API-00749（金样·培育）** 各断言 **完整可路由失败或不可用信封**（HTTP + 可解析体）；同 endpoint 其余用例在前置引用对应金样后，可只断言失败态、鉴权态或字段形态 |
| catalog 状态 | 本页 **2** 个 endpoint 均为 `status=unavailable`、`runtime=local_mock`；**禁止**将 `sampleResponse` 中 `task_id`、`candidate_count`、`weights`、`recommendation_score`、企业名称或 `rankings` 条数作为通过条件 |
| 页内区分 | 同页两契约仅 **`sub_type`** 与 endpoint 标题不同：招引 endpoint 验收取 `sub_type=attraction`；培育 endpoint 验收取 `sub_type=cultivation`；不得串用另一子类型 sample 形态当作本 endpoint 通过 |
| 样例与契约差 | 招引 sample 含 `weights`（待甲方确认 **Q015** 🟡）；培育 sample 含 `industry_category`、`enterprise_scale`、`development_bottleneck` 等；契约 `responseFields` 两 endpoint 均仅声明 **`rankings`（array）**。断言 **只强制 responseFields**；样例扩展字段不设失败条件 |
| 异步语义 | 页级 `autoRun=false`；本册只验 **契约 HTTP/入参/出参**，不验联调台任务池单飞、当天复用或重新分析（归专题异步工作区 FUNC/附录 E） |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **2** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00744`～`00753`。`路由route` = catalog `path`（本页为空则填 `—`）；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00744 | 创新监测 | 引育推荐（异步） | 契约-不可用 | 招引推荐契约 | 引育推荐（异步） | 招引推荐 | catalog 不可用态下招引推荐契约返回可识别非成功契约 | 1、已确认 catalog `innov.recommend.attraction` 为 unavailable 且 path 为空；2、已按 §0 携带有效 token 与 TENANT-ID | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-ATTR-01 | 1、HTTP 状态为 404/405/4xx/5xx 或响应体为 JSON；2、若体为 JSON 则含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `rankings` 的成功业务载荷；4、不得将 sample 招引榜示例分值或企业名作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=REC-ATTR-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00745 | 创新监测 | 引育推荐（异步） | 异常-鉴权 | 招引推荐契约 | 引育推荐（异步） | 招引推荐 | 招引推荐契约缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-ATTR-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 rankings 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=REC-ATTR-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00746 | 创新监测 | 引育推荐（异步） | 异常-缺必填sub_type | 招引推荐契约 | 引育推荐（异步） | 招引推荐 | 招引推荐契约缺少 sub_type 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 API-00744 | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-ATTR-02 | 1、响应为失败态（HTTP 4xx/5xx 或 code 非成功集合）；2、不得将失败当作含可信 `rankings` 的成功招引结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=REC-ATTR-02；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00747 | 创新监测 | 引育推荐（异步） | 异常-非法sub_type | 招引推荐契约 | 引育推荐（异步） | 招引推荐 | 招引推荐契约 sub_type 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-ATTR-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、message 或 msg 可非空；3、不得将失败当作含可信招引 rankings 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=REC-ATTR-03；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00748 | 创新监测 | 引育推荐（异步） | 异常-非本页sub_type | 招引推荐契约 | 引育推荐（异步） | 招引推荐 | 招引 endpoint 使用培育 sub_type 时不得当作本页招引成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-ATTR-05 | 1、响应为失败态或可识别非本页 attraction 契约态；2、不得将 `sub_type=cultivation` 的 sample 形态当作本页招引 rankings 通过 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.attraction catalog_page_id=innov.recommend 组合=REC-ATTR-05；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00749 | 创新监测 | 引育推荐（异步） | 契约-不可用 | 培育推荐契约 | 引育推荐（异步） | 培育推荐 | catalog 不可用态下培育推荐契约返回可识别非成功契约 | 1、已确认 catalog `innov.recommend.cultivation` 为 unavailable 且 path 为空；2、已按 §0 携带有效 token 与 TENANT-ID | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-CULT-01 | 1、HTTP 状态为 404/405/4xx/5xx 或响应体为 JSON；2、若体为 JSON 则含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `rankings` 的成功业务载荷；4、不得将 sample 培育榜示例分值或瓶颈文案作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=REC-CULT-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00750 | 创新监测 | 引育推荐（异步） | 异常-鉴权 | 培育推荐契约 | 引育推荐（异步） | 培育推荐 | 培育推荐契约缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-CULT-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 rankings 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=REC-CULT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00751 | 创新监测 | 引育推荐（异步） | 异常-缺必填sub_type | 培育推荐契约 | 引育推荐（异步） | 培育推荐 | 培育推荐契约缺少 sub_type 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 API-00749 | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-CULT-02 | 1、响应为失败态（HTTP 4xx/5xx 或 code 非成功集合）；2、不得将失败当作含可信 `rankings` 的成功培育结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=REC-CULT-02；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00752 | 创新监测 | 引育推荐（异步） | 异常-非法sub_type | 培育推荐契约 | 引育推荐（异步） | 培育推荐 | 培育推荐契约 sub_type 枚举外取值时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-CULT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得将失败当作含可信培育 rankings 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=REC-CULT-03；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00753 | 创新监测 | 引育推荐（异步） | 异常-非本页sub_type | 培育推荐契约 | 引育推荐（异步） | 培育推荐 | 培育 endpoint 使用招引 sub_type 时不得当作本页培育成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.POST（catalog path 为空·local_mock）请求体取组合 REC-CULT-04 | 1、响应为失败态或可识别非本页 cultivation 契约态；2、不得将 `sub_type=attraction` 的 sample 形态当作本页培育 rankings 通过 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·引育推荐（异步） | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.recommend.cultivation catalog_page_id=innov.recommend 组合=REC-CULT-04；矩阵挂 sub_type、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| REC-ATTR-01 | innov.recommend.attraction | `sub_type`: `attraction`（对齐 catalog `sampleRequest`） | 招引 unavailable 主路径 |
| REC-ATTR-02 | innov.recommend.attraction | 请求体 `{}`（不含 `sub_type` 键） | 缺必填 |
| REC-ATTR-03 | innov.recommend.attraction | `sub_type`: `__invalid__` | 枚举外取值 |
| REC-ATTR-04 | innov.recommend.attraction | `sub_type`: `""` | 空字符串；**本轮无独立用例**，语义待 path 发布且 available 后补 |
| REC-ATTR-05 | innov.recommend.attraction | `sub_type`: `cultivation` | 非本页子类型（培育值误挂招引 endpoint） |
| REC-CULT-01 | innov.recommend.cultivation | `sub_type`: `cultivation`（对齐 catalog `sampleRequest`） | 培育 unavailable 主路径 |
| REC-CULT-02 | innov.recommend.cultivation | 请求体 `{}`（不含 `sub_type` 键） | 缺必填 |
| REC-CULT-03 | innov.recommend.cultivation | `sub_type`: `__invalid__` | 枚举外取值 |
| REC-CULT-04 | innov.recommend.cultivation | `sub_type`: `attraction` | 非本页子类型（招引值误挂培育 endpoint） |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 请求体 |
|-------------|--------|------|--------|---------|--------|
| innov.recommend.attraction | POST | （空） | unavailable | local_mock | sub_type（必填；本页验收取值 attraction） |
| innov.recommend.cultivation | POST | （空） | unavailable | local_mock | sub_type（必填；本页验收取值 cultivation） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.recommend.attraction | API-00744、00745、00746、00747、00748 |
| innov.recommend.cultivation | API-00749、00750、00751、00752、00753 |

---

## 3. 覆盖自检（§S1）

- [x] 2 个 unavailable endpoint 各 1 条契约占位（API-00744、00749），未写 sample 数值通过条件
- [x] 异常-鉴权 2 条（00745、00750）
- [x] 各 endpoint 入参单缺陷 3 条（缺省 / 非法 / 跨子类型）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 金样 2 条（招引 00744、培育 00749）
- [x] 本页 **0** 条 FUNC
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务编号闭区间 API-00744～00753；**未改 registry**）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **10** |
| 编号闭区间 | **API-00744**～**API-00753** |
| endpoint 数 | **2**（各 5 条） |
| `_empty` 未覆盖 | **2** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
