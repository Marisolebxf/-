# 智能服务集群-科技专题服务算法库测试用例（服务机构基础指标 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：基础指标 / 服务机构基础指标  
> **catalog**：`entry_id=svc.basic` · `catalog_page_id=svc.basic` · path `/industry-service/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L04.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定（50897 试调：**未试调**）

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 鉴权 | `POST /auth/oauth2/token`（`grant_type=password`，账号口径同 `lumen-ui-algo-apiview` LoginView 默认 `admin` / `gkx@2026`，密码经 AES-CFB 加密提交）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00529（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 与 catalog `responseFields` 形态）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00529」后，可只断言 HTTP/`code`、**data 载荷** 或契约占位语义 |
| 试调 observed | **本轮未试调**（父控宣布）；执行期以现场为准，样例 JSON 仅作形态参考，**禁止**写入预期数值 |
| catalog 与现场 | 本页 1 个 endpoint 为 `status=unavailable`；用例按 **契约占位 + 金样形态** 编写，不得将 `sampleResponse` 中机构数、金额、增长率等作为通过条件；若现场返回 mock 成功，记录 as-built 偏差 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00529`～`00533`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.basic`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00529 | 基础指标 | 服务机构基础指标 | 契约-不可用 | 金样信封 | 服务机构基础指标 | 基础指标 A1–A6 + STAT-21 T2 | catalog 不可用态下 kind=all 是否可识别非 live 成功 | 1、已按 §0 取得有效 token 与租户头；2、断言对象为完整原始响应信封 | 1.GET /entan/v1/svc/indicators，查询参数取组合 IND-01 | 1、HTTP 状态为 200 或 4xx/5xx 之一；2、响应体含可解析的 code 与 message 或 msg；3、不得将 sample 中 layout、global、org_count 等数值作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产全维指标判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_ORG_TOTAL | INTEG | | | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 组合=IND-01 金样 catalog_status=unavailable 未试调 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00530 | 基础指标 | 服务机构基础指标 | 异常-鉴权 | 缺Token | 服务机构基础指标 | 基础指标 A1–A6 + STAT-21 T2 | 指标接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /entan/v1/svc/indicators，查询参数取组合 IND-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务指标载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | | INTEG | | | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 组合=IND-01；全页鉴权同本用例 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00531 | 基础指标 | 服务机构基础指标 | 契约-字段形态 | A1A2块 | 服务机构基础指标 | 基础指标 A1–A6 + STAT-21 T2 | kind=all 时 layout、global 若存在是否为 array 形态 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-00529 | 1.GET /entan/v1/svc/indicators，查询参数取组合 IND-01 | 1、若 code 属成功集合且 data 含 layout 字段，则 layout 为 array；2、若 data 含 global 字段，则 global 为 array；3、不得以 sample 内 industry_field、org_count 数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INDUSTRY_LAYOUT | INTEG | | | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 组合=IND-01；矩阵挂 layout、global |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00532 | 基础指标 | 服务机构基础指标 | 备选-kind单维 | STAT-21 | 服务机构基础指标 | 基础指标 A1–A6 + STAT-21 T2 | kind=stat21 时是否关注 STAT-21 相关块形态 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-00529 | 1.GET /entan/v1/svc/indicators，查询参数取组合 IND-02 | 1、若 code 属成功集合且 data 含 org_total 字段，则 org_total 为 object；2、若 data 含 pt_type_dist 字段，则 pt_type_dist 为 array；3、不得以 sample 内 KPI 计数作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_PT_GLOBAL_TOTAL | INTEG | | | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 组合=IND-02；矩阵挂 kind、org_total、pt_type_dist |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00533 | 基础指标 | 服务机构基础指标 | 异常-非法kind | 指标查询 | 服务机构基础指标 | 基础指标 A1–A6 + STAT-21 T2 | kind 非法取值时是否返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /entan/v1/svc/indicators，查询参数取组合 IND-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含可信 layout/global 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | | INTEG | | | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 组合=IND-03；矩阵挂 kind、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| IND-01 | svc.basic.indicators | kind=all（catalog example） | unavailable 全维主组合 |
| IND-02 | svc.basic.indicators | kind=stat21（catalog option） | STAT-21 单维筛选 |
| IND-03 | svc.basic.indicators | kind=__invalid__ | 非法 kind（单缺陷） |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| svc.basic.indicators | GET | /entan/v1/svc/indicators | unavailable | —（kind 可选） |

catalog `responseFields`（形态参考，禁止 sample 数值验收）：layout、global、invest、new、sz_scale、sz_dist、org_total、pt_global_total、org_new_count、pt_type_dist、pt_region、pt_scale_dist、pt_sz_total、pt_sz_type_dist、pt_sz_region、sz_compare。

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.basic.indicators | API-00529、API-00530、API-00531、API-00532、API-00533 |

---

## 3. 覆盖自检（§S1）

- [x] 本页 **0** 条 FUNC
- [x] 1 个 endpoint **5** 条 API 用例（单 endpoint 套餐）
- [x] 金样 1 条（API-00529，备注含 `金样`）
- [x] 异常-鉴权 1 条（API-00530，全页复用）
- [x] 非法 kind 1 条（API-00533，矩阵挂 `_fail`）
- [x] `_empty` 无稳定构造 → 矩阵标 **未覆盖**（见 `coverage-fp.md`）
- [x] 50897 **未试调**（§0）
- [x] `coverage-fp.md` 已更新
- [x] 编号闭区间 **API-00529**～**API-00533**（父控分配；**未**改 `code-registry.yaml` / `run-log.md`）

**统计**：用例 **5** 条。

---

## 4. 红线自检（摘要）

| 检查 | 结果 |
|------|------|
| 正文四列内部引用扫描 | 0 命中 |
| 步骤含「核对/检查/验证」 | 0 命中 |
| 单条步骤/预期 ≤60 字、步骤 ≤7 | 通过 |
| 预期断言 1～4 点/条，无 ≥6 点 | 通过 |
| 用例按 主流程→备选→异常 排列 | 通过 |
| 金样备注 | API-00529 |
