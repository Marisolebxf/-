# 智能服务集群-科技专题服务算法库测试用例（深圳企业竞争力水平分析 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 深圳企业竞争力水平分析  
> **catalog**：`entry_id=entan.competitiveness` · `catalog_page_id=entan.competitiveness` · path `/entan/competitiveness`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.competitiveness`  
> **A 线对照**：`fp-split-by-api-run/work/L27.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP（`http://111.198.38.90:50897/`）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I · §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18（第二轮 R2-批1 · API-00943～00948）

---

## 0. 本页接口清单与执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（执行期由联调台或等价网关提供；**不**作为用例验收项） |
| 企业标识样例 | catalog `sampleRequest` / `params.example` 四元组：`0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（执行期可替换为环境有效 org_id） |
| 载荷嵌套 | `responseFields` 声明顶层 `enterprises`（array）；`sampleResponse` 明细位于 `value.enterprises`；正向预期同时覆盖契约字段与样例中出现的 `value` 嵌套结构 |
| catalog 状态 | `综合竞争力得分`、`综合竞争力排名` 为 `unavailable`（备注注明）；`M_ENT_CITY_COMPARE_TOPIC` 为 `available` |
| 数值断言 | 样例中的 `total_score`、`dimensions.*` 等具体数值仅说明字段形态，**不得**作为通过条件 |

**下拉框 title（与 catalog 一致）**

1. 综合竞争力得分（企业集合）  
2. 综合竞争力排名（企业集合）  
3. M_ENT_CITY_COMPARE_TOPIC  

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.competitiveness`、组合 id（如有）。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00943 | 企业分析 | 深圳企业竞争力水平分析 | 主流程 | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 综合竞争力得分在文档示例 enterprise_codes 下返回 sampleResponse 契约字段 | 1、enterprise_codes 使用 catalog 示例四元组（§0，可替换） | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-01 | 1、返回 body 含 string 型 metric_id、metric_name_zh；2、含 object 型 value，且 value.enterprises 为 array；3、若 enterprises 非空则元素含 string 型 org_id、enterprise_name，number 型 total_score，object 型 dimensions（含 innovation、operation、growth）；4、样例还含 data_source（string）、confidence（string）、calc_process（object）；5、契约 responseFields 要求的 enterprises（array）在载荷中可定位 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | M_ENT_COMPETITIVENESS_SCORE | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00944 | 企业分析 | 深圳企业竞争力水平分析 | 异常-入参-缺enterprise_codes | 综合竞争力得分 | 深圳企业竞争力水平分析 | 综合竞争力得分（企业集合） | 综合竞争力得分不传 enterprise_codes 时返回该参数错误说明 | 1、其余 body 字段保持合法（本接口仅 enterprise_codes） | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 SCR-02 | 1、返回 body 的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 sampleResponse 形态 total_score 与 dimensions 的成功得分结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.score catalog_page_id=entan.competitiveness 组合=SCR-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00945 | 企业分析 | 深圳企业竞争力水平分析 | 主流程 | 综合竞争力排名 | 深圳企业竞争力水平分析 | 综合竞争力排名（企业集合） | 综合竞争力排名在文档示例 enterprise_codes 下返回排名结果集契约字段 | 1、enterprise_codes 使用 catalog 示例四元组（§0，可替换） | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 RNK-01 | 1、返回 body 含 string 型 metric_id、metric_name_zh；2、含 object 型 value，且 value.enterprises 为 array；3、若 enterprises 非空则元素含 org_id、enterprise_name、total_score、dimensions（innovation、operation、growth）；4、样例还含 data_source、confidence、calc_process；5、enterprises 数组承载排名明细（排序语义以接口文档为准） | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | M_ENT_COMPETITIVENESS_SCORE | INTEG | | | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00946 | 企业分析 | 深圳企业竞争力水平分析 | 异常-入参-非法enterprise_codes | 综合竞争力排名 | 深圳企业竞争力水平分析 | 综合竞争力排名（企业集合） | 综合竞争力排名 enterprise_codes 含明显非法编码时返回该参数错误说明 | 1、仅破坏 enterprise_codes，其余保持合法 | 1.POST /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute，请求体取组合 RNK-02 | 1、返回 body 的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含可信排序 enterprises 与 total_score 的成功排名结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | | INTEG | | | endpoint_id=entan.competitiveness.ranking catalog_page_id=entan.competitiveness 组合=RNK-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00947 | 企业分析 | 深圳企业竞争力水平分析 | 主流程 | M_ENT_CITY_COMPARE_TOPIC | 深圳企业竞争力水平分析 | M_ENT_CITY_COMPARE_TOPIC | M_ENT_CITY_COMPARE_TOPIC 在文档示例 enterprise_codes 下返回 compute 契约字段 | 1、enterprise_codes 使用 catalog 示例四元组（§0，可替换） | 1.POST /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute，请求体取组合 CTY-01 | 1、返回 body 含 string 型 metric_id（样例为 M_ENT_CITY_COMPARE_TOPIC）；2、含 string 型 hint（样例为 compute 响应说明）；3、契约 responseFields 要求的 enterprises（array）在载荷中可定位；4、以实际调用为准时 hint 文案可变，但 metric_id 与 enterprises 字段形态须符合文档 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | M_ENT_CITY_COMPARE_TOPIC | INTEG | | | endpoint_id=entan.competitiveness.score.m_ent_city_compare_topic catalog_page_id=entan.competitiveness 组合=CTY-01 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00948 | 企业分析 | 深圳企业竞争力水平分析 | 异常-入参-缺enterprise_codes | M_ENT_CITY_COMPARE_TOPIC | 深圳企业竞争力水平分析 | M_ENT_CITY_COMPARE_TOPIC | M_ENT_CITY_COMPARE_TOPIC 不传 enterprise_codes 时返回该参数错误说明 | 1、其余 body 保持合法 | 1.POST /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute，请求体取组合 CTY-02 | 1、返回 body 的 message 或 msg 说明 enterprise_codes 缺失或非法；2、不返回含 metric_id 与 enterprises 的成功 compute 结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | | INTEG | | | endpoint_id=entan.competitiveness.score.m_ent_city_compare_topic catalog_page_id=entan.competitiveness 组合=CTY-02 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| SCR-01 | entan.competitiveness.score | `enterprise_codes`=[`0218337e44ca794fee9850cf1627b03b`,`05dc8024336db695425572625773381b`,`0551ccfde6aa2b3c52e647e283204040`,`05ff69620c962ce3bbb852351f077299`]（catalog sampleRequest，可替换） | 主路径全参 |
| SCR-02 | entan.competitiveness.score | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| RNK-01 | entan.competitiveness.ranking | `enterprise_codes` 同 SCR-01 | 主路径全参 |
| RNK-02 | entan.competitiveness.ranking | `enterprise_codes`=[`__invalid_org__`] | 只破坏 enterprise_codes |
| CTY-01 | entan.competitiveness.score.m_ent_city_compare_topic | `enterprise_codes` 同 SCR-01 | 主路径全参 |
| CTY-02 | entan.competitiveness.score.m_ent_city_compare_topic | 请求体不含 `enterprise_codes` 键 | 缺必填 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | title | METHOD | path | status | 必填参数 |
|-------------|-------|--------|------|--------|----------|
| entan.competitiveness.score | 综合竞争力得分（企业集合） | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | unavailable | enterprise_codes（body） |
| entan.competitiveness.ranking | 综合竞争力排名（企业集合） | POST | /entan/v1/entan/metric/M_ENT_COMPETITIVENESS_SCORE/compute | unavailable | enterprise_codes（body） |
| entan.competitiveness.score.m_ent_city_compare_topic | M_ENT_CITY_COMPARE_TOPIC | POST | /entan/v1/entan/metric/M_ENT_CITY_COMPARE_TOPIC/compute | available | enterprise_codes（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.competitiveness.score | API-00943、API-00944 |
| entan.competitiveness.ranking | API-00945、API-00946 |
| entan.competitiveness.score.m_ent_city_compare_topic | API-00947、API-00948 |

---

## 3. 覆盖自检

- [x] 本页 3 个 catalog title 均在功能点列出现，且各至少 1 条主流程（00943、00945、00947）
- [x] 有参接口每参数 1 条反向（enterprise_codes：00944、00946、00948）
- [x] 0 条鉴权 / Token / 401 / 424 / 契约占位功能项
- [x] 正向预期按各接口 sampleResponse / responseFields 写字段结构
- [x] `coverage-fp.md` 已更新至 API-00943～00948
- [ ] `code-registry.yaml` 由父控签收后回写（闭区间 00943～00948）

**统计**：用例 **6** 条；编号 **API-00943**～**API-00948**（第一轮 API-00075～00084 作废不复用）。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| 对象（3 title 各 ≥1 主流程） | **通过**（3/3） |
| 鉴权用例 | **0** |
| 正向（文档示例组合 + sampleResponse 字段） | **3**（00943、00945、00947） |
| 反向（每 endpoint 每参数 1 条） | **3**（00944、00946、00948） |
| unavailable 仍写主流程（非契约占位） | **2**（score、ranking；备注 catalog_status=unavailable） |
| 功能项禁契约占位 | **通过** |
| API 条数 | **6**（00943～00948） |
| 金样 | **1**（00943） |
