# 智能服务集群-科技专题服务算法库测试用例（企业发展历程 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业发展历程  
> **catalog**：`entry_id=entan.history` · `catalog_page_id=entan.history` · path `/entan/history`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.history`  
> **A 线对照**：`fp-split-by-api-run/work/L28.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP（**本册不写鉴权步骤、不含 Token/401/424 用例**）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I · §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-18  
> **作废编号**：第一轮 `API-00085`～`00094` 整批作废，不复用  

---

## 0. 本页接口清单与约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（执行期等价 HTTP；鉴权由执行人自行持有，**不作为本册验收项**） |
| catalog 状态 | **企业搜索**、**发展历程** 两 endpoint 均为 `status=unavailable`；正向仍按各接口 `sampleResponse`/`responseFields` 写返回 body 预期，备注注明未交付 |
| org_id 样例 | `0218337e44ca794fee9850cf1627b03b`（`entan.history.timeline` params example，执行期可替换） |
| 试调 | **未试调**（S1 禁止 curl/浏览器） |

### 下拉框 title（与 catalog 一致）

1. **企业搜索**（`entan.history.enterprises` · GET `/entan/v1/enterprises`）  
2. **发展历程**（`entan.history.timeline` · GET `/entan/v1/history`）  

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.history`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00949 | 企业分析 | 企业发展历程 | 主流程 | 文档示例参 | 企业发展历程 | 企业搜索 | 企业搜索按 catalog sampleRequest（keyword 空、limit=1）返回文档企业列表字段 | 1、无额外业务前置 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-01 | 1、成功时返回 body 的业务载荷为数组（常见为 `data` 数组，与网关 envelope 一致）；2、元素含 org_id（string）、enterprise_name（string）；3、sampleResponse 示例 org_id=0218337e44ca794fee9850cf1627b03b、enterprise_name=云启智元科技股份有限公司，说明命中元素形态；4、允许空数组表示无匹配企业 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00950 | 企业分析 | 企业发展历程 | 备选-参数组合 | keyword与limit | 企业发展历程 | 企业搜索 | 企业搜索在 keyword=云启、limit=5 时返回文档列表字段 | 1、无额外业务前置 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-02 | 1、成功时业务载荷为数组；2、非空元素含 org_id（string）、enterprise_name（string）；3、sampleResponse 字段形态同 API-00949；4、空数组仍表示无匹配，不得与入参错误失败态混淆 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-02 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00951 | 企业分析 | 企业发展历程 | 异常-入参-非法limit | 企业搜索 | 企业发展历程 | 企业搜索 | 企业搜索 limit 非法时返回该参数错误说明 | 1、无额外业务前置 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-03 | 1、返回 body 的 message 或 msg 说明 limit 非法、越界或不可解析；2、不返回含可信 org_id/enterprise_name 命中列表的成功业务载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-03；矩阵挂 limit、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00952 | 企业分析 | 企业发展历程 | 异常-入参-非法keyword | 企业搜索 | 企业发展历程 | 企业搜索 | 企业搜索 keyword 明显非法时返回该参数错误说明 | 1、无额外业务前置 | 1.GET /entan/v1/enterprises，查询参数取组合 ENT-04 | 1、返回 body 的 message 或 msg 说明 keyword 非法或不可接受；2、不返回将失败冒充为含 org_id 的成功命中列表 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/enterprises | | INTEG | | | endpoint_id=entan.history.enterprises catalog_page_id=entan.history 组合=ENT-04；矩阵挂 keyword、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00953 | 企业分析 | 企业发展历程 | 主流程 | 文档示例org_id | 企业发展历程 | 发展历程 | 发展历程按 catalog sampleRequest org_id 返回文档时间线字段 | 1、org_id 使用 §0 样例或环境有效值 | 1.GET /entan/v1/history，查询参数取组合 HIS-01 | 1、成功时业务载荷为对象（常见为 `data` 对象）；2、含 enterprise_name（string），sampleResponse 示例「云启智元科技股份有限公司」说明形态；3、含 timeline（array）；4、timeline 元素含 year（number）、type（string）、title（string）、detail（object），sampleResponse 示例含 type=finance/patent/news 及 detail 内 revenue、patent_apply_count、finance_round 等键说明节点结构；5、timeline 可为空数组（无重大事件空态），与 API-00954 失败态区分 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-01 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00954 | 企业分析 | 企业发展历程 | 异常-入参-缺org_id | 发展历程 | 企业发展历程 | 发展历程 | 发展历程不传 org_id 时返回缺少该参数的错误说明 | 1、无额外业务前置 | 1.GET /entan/v1/history，查询参数取组合 HIS-02 | 1、返回 body 的 message 或 msg 指出 org_id 缺失或必填；2、不返回含 timeline 数组的成功业务载荷 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-02；矩阵挂 org_id、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00955 | 企业分析 | 企业发展历程 | 异常-入参-非法org_id | 发展历程 | 企业发展历程 | 发展历程 | 发展历程 org_id 非法时返回该参数错误说明 | 1、无额外业务前置 | 1.GET /entan/v1/history，查询参数取组合 HIS-03 | 1、返回 body 的 message 或 msg 说明 org_id 非法或企业不存在；2、不返回将失败冒充为合法 org_id 下空 timeline 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/history | | INTEG | | | endpoint_id=entan.history.timeline catalog_page_id=entan.history 组合=HIS-03；矩阵挂 org_id、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ENT-01 | entan.history.enterprises | keyword=（空字符串）；limit=1（catalog sampleRequest） | 主路径全参 |
| ENT-02 | entan.history.enterprises | keyword=云启；limit=5 | keyword+limit 合法组合 |
| ENT-03 | entan.history.enterprises | keyword=测试；limit=-1 | 只破坏 limit |
| ENT-04 | entan.history.enterprises | keyword=__invalid__；limit=10 | 只破坏 keyword |
| HIS-01 | entan.history.timeline | org_id=0218337e44ca794fee9850cf1627b03b（catalog params example，可替换） | 主路径全参 |
| HIS-02 | entan.history.timeline | 不传 org_id 查询参数 | 缺必填 org_id |
| HIS-03 | entan.history.timeline | org_id=__invalid__ | 非法 org_id |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 参数 |
|-------------|--------|------|--------|------|
| entan.history.enterprises | GET | /entan/v1/enterprises | unavailable | keyword、limit（均可选） |
| entan.history.timeline | GET | /entan/v1/history | unavailable | org_id（必填） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.history.enterprises | API-00949、API-00950、API-00951、API-00952 |
| entan.history.timeline | API-00953、API-00954、API-00955 |

---

## 3. 覆盖自检（§I）

- [x] 本页两个 title（企业搜索、发展历程）均在功能点列出现，且各至少 1 条主流程（API-00949、API-00953）
- [x] 鉴权用例 **0** 条；前置条件无 Token/登录验收
- [x] 正向预期按 sampleResponse/responseFields 写字段与类型（含 timeline 嵌套 detail）
- [x] 有参接口每参数 1 条反向：limit→00951、keyword→00952、org_id 缺/非法→00954/00955
- [x] unavailable 两接口均有按文档返回体写的主流程，非「契约占位不测」
- [x] `coverage-fp.md` 已更新至 API-00949～00955
- [ ] `code-registry.yaml` 由父控回写（本子任务不写 registry）

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **7** |
| 编号闭区间 | **API-00949**～**API-00955** |
| FUNC 条数 | **0** |
| 试调 | **未试调**（§0） |
