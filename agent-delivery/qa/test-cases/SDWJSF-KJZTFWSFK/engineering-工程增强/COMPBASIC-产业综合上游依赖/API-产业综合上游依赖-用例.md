# 智能服务集群-科技专题服务算法库测试用例（产业综合上游依赖 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：工程增强 / 产业综合上游依赖  
> **catalog**：`entry_id=comp.basic` · `catalog_page_id=comp.basic` · path `/industry-comp/basic`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.basic`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `comp.basic` 行（`_l6-to-catalog-map.yaml`：上游依赖页，非 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1  
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
| 断言分工 | **API-00649（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00649」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **1** 个 endpoint（`comp.basic.upstream`）catalog `status=unavailable`、`runtime=local_mock`；Java `/comp/v1` 未发布，联调台不发真实业务请求；**禁止**将 `sampleResponse` 中 `kpis.vitality`/`element`/`synergy`、`upstream[].ready`、`bar_items`/`pie_items` 等示例数值作为通过条件 |
| 试调 | **未试调**（父控未试调；本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 查询参数 | GET 查询串；`region` 为可选 string；组合定义见附录 A |
| 样例与契约差 | `sampleResponse` 含 `bar_items`、`pie_items` 等图表演示字段；契约 `responseFields` **仅**声明 `upstream`（array）、`kpis`（object）。断言以 `responseFields` 为准；样例扩展字段不设失败条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00649`～`00653`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.basic`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00649 | 工程增强 | 产业综合上游依赖 | 契约-不可用 | 上游依赖与综合研判 | 产业综合上游依赖 | 上游依赖与综合研判 | catalog 不可用态下上游依赖接口返回可识别非成功契约信封 | 1、已确认 catalog `comp.basic.upstream` 为 unavailable 且 runtime=local_mock；2、已按 §0 携带有效 token 与租户头 | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 BASIC-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `upstream` 与 object 型 `kpis` 的成功业务载荷；4、不得将 sampleResponse 活力/要素/协同指数或七维就绪示例作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | M_COMP_UPSTREAM_READY | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=BASIC-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00650 | 工程增强 | 产业综合上游依赖 | 异常-鉴权 | 上游依赖与综合研判 | 产业综合上游依赖 | 上游依赖与综合研判 | 上游依赖接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 BASIC-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 upstream/kpis 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=BASIC-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00651 | 工程增强 | 产业综合上游依赖 | 异常-非法region | 上游依赖与综合研判 | 产业综合上游依赖 | 上游依赖与综合研判 | 上游依赖接口 region 为不可识别区域编码时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00649 | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 BASIC-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含 sample 形态 upstream 七维列表的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=BASIC-02；矩阵挂 region、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00652 | 工程增强 | 产业综合上游依赖 | 异常-空region | 上游依赖与综合研判 | 产业综合上游依赖 | 上游依赖与综合研判 | 上游依赖接口 region 为空字符串时返回可识别失败或与省略 region 可区分 | 1、已按 §0 携带有效 token 与租户头 | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 BASIC-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或可与 BASIC-01 省略 region 的成功语义明确区分；2、不得将空 region 静默当作默认区域并成功返回 sample kpis 数值 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=BASIC-03；矩阵挂 region、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00653 | 工程增强 | 产业综合上游依赖 | 契约-字段形态 | 上游依赖与综合研判 | 产业综合上游依赖 | 上游依赖与综合研判 | 成功信封下契约出参 upstream、kpis 若存在是否符合 array/object 形态 | 1、已按 §0 携带有效 token 与租户头；2、信封成功规则见 §0，金样见 API-00649 | 1.GET /comp/v1/comp/upstream-deps，查询参数取组合 BASIC-01 | 1、若 code 属成功集合且载荷含 upstream（含 data 内或顶层），则 upstream 为 array；2、若含 kpis，则 kpis 为 object；3、不得以 sample 中 vitality/element/synergy 具体数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/upstream-deps | M_SYNTH_VIT_INDEX | INTEG | | | endpoint_id=comp.basic.upstream catalog_page_id=comp.basic 组合=BASIC-01；矩阵挂 upstream、kpis；样例另含 M_SYNTH_ELEM_INDEX、M_SYNTH_COLLAB_INDEX 不设失败条件 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| BASIC-01 | comp.basic.upstream | `region`=440300（与 catalog example 一致，执行期可省略 region 作对照） | unavailable 契约占位主路径 |
| BASIC-02 | comp.basic.upstream | `region`=`__invalid_region__` | 不可识别区域编码（单缺陷） |
| BASIC-03 | comp.basic.upstream | `region`=`""`（空字符串） | 空 region 与省略参数边界 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 必填参数 |
|-------------|--------|------|--------|---------|----------|
| comp.basic.upstream | GET | /comp/v1/comp/upstream-deps | unavailable | local_mock | （无；`region` 可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.basic.upstream | API-00649、API-00650、API-00651、API-00652、API-00653 |

---

## 3. 覆盖自检（§S1）

- [x] 唯一 unavailable / local_mock endpoint 已写契约占位（API-00649）
- [x] 可选入参 `region` 非法值与空字符串已覆盖（API-00651、00652）
- [x] 异常-鉴权 1 条（API-00650）
- [x] 契约出参 `upstream`、`kpis` 形态占位 1 条（API-00653）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定「合法 region 下必空 upstream」试调证据）
- [x] 金样 1 条且断言完整信封（API-00649）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

**统计**：用例 **5** 条；编号 **API-00649**～**API-00653**。
