# 智能服务集群-科技专题服务算法库测试用例（企业创新能力评估 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：企业分析 / 企业创新能力评估  
> **catalog**：`entry_id=entan.innovation` · `catalog_page_id=entan.innovation` · path `/entan/innovation`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.innovation`  
> **A 线对照**：无独立 `work/Lxx.md`（`_l6-to-catalog-map.yaml` 注明与 L31 相邻不扩六级）；矩阵四行键形态对齐 `L33.md` 契约行 + catalog  
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
| 断言分工 | **API-00162（金样）** 断言 **完整原始信封**（HTTP + `code` + `data` 形态）；同册其余用例在前置写「信封规则见 §0，金样见 API-00162」后，可只断言失败/不可用态 |
| catalog 状态 | 本页 **1** 个 endpoint（`entan.innovation.rank`）catalog `status=unavailable`；**禁止**将 `sampleResponse` 中 `innovation_index`、`metric_id` 及 `value.enterprises` 成员示例数值作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST JSON；必填 `enterprise_codes`（array）；组合定义见附录 A |
| 样例与契约差 | `sampleResponse` 中明细位于 `value.enterprises`；契约 `responseFields` 仅声明顶层 `enterprises`（array）。断言以 `responseFields` 为准；样例嵌套路径不设失败条件 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-#####`。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.innovation`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00162 | 企业分析 | 企业创新能力评估 | 契约-不可用 | 创新能力指数（企业集合） | 企业创新能力评估 | 创新能力指数（企业集合） | catalog 不可用态下创新能力指数接口返回可识别非成功契约信封 | 1、已确认 catalog `entan.innovation.rank` 为 unavailable；2、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含 `code` 字段；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `enterprises` 的成功业务载荷；4、不得将 sampleResponse 创新能力指数示例数值作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | M_ENT_INNOVATION_INDEX | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00163 | 企业分析 | 企业创新能力评估 | 异常-鉴权 | 创新能力指数（企业集合） | 企业创新能力评估 | 创新能力指数（企业集合） | 创新能力指数接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 enterprises 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00164 | 企业分析 | 企业创新能力评估 | 异常-缺必填enterprise_codes | 创新能力指数（企业集合） | 企业创新能力评估 | 创新能力指数（企业集合） | 创新能力指数接口缺少 enterprise_codes 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 API-00162 | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作成功空 enterprises 或无指数空态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-02；矩阵挂 enterprise_codes、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00165 | 企业分析 | 企业创新能力评估 | 异常-空集合enterprise_codes | 创新能力指数（企业集合） | 企业创新能力评估 | 创新能力指数（企业集合） | 创新能力指数接口 enterprise_codes 为空数组时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得与「合法非空集合下 enterprises 为空」契约空态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-03；矩阵挂 _fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00166 | 企业分析 | 企业创新能力评估 | 异常-非法enterprise_codes | 创新能力指数（企业集合） | 企业创新能力评估 | 创新能力指数（企业集合） | 创新能力指数接口含明显非法企业编码时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求体取组合 INNO-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、message 或 msg 可非空；3、不得将失败当作含可信 innovation_index 的成功业务数据 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | | INTEG | | | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-04 |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INNO-01 | entan.innovation.rank | `enterprise_codes` = catalog example 四元组（`demo-org-sz-active-listed`、`demo-org-hk`、`demo-org-gz-00`、`demo-org-bj-01`，执行期可替换） | unavailable 契约占位主路径 |
| INNO-02 | entan.innovation.rank | 请求体不含 `enterprise_codes` 键 | 缺必填 |
| INNO-03 | entan.innovation.rank | `enterprise_codes`: `[]` | 空集合（失败哨兵，非空态） |
| INNO-04 | entan.innovation.rank | `enterprise_codes`: `["__invalid_org__"]` | 非法企业编码 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 必填参数 |
|-------------|--------|------|--------|----------|
| entan.innovation.rank | POST | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | unavailable | enterprise_codes（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.innovation.rank | API-00162、API-00163、API-00164、API-00165、API-00166 |

---

## 3. 覆盖自检

- [x] 唯一 unavailable endpoint 已写契约占位（API-00162）
- [x] 必填 `enterprise_codes` 缺省、空集合、非法编码已覆盖（API-00164～00166）
- [x] 异常-鉴权 1 条（API-00163）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定合法空 enterprises 构造）
- [x] 金样 1 条且断言完整信封（API-00162）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml`（父控回写）

**统计**：用例 **5** 条；编号 **API-00162**～**API-00166**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **5**（00162～00166） |
| 金样（完整信封） | **1**（API-00162） |
| live 主路径 | **0**（endpoint unavailable） |
| 每 endpoint 用例数 | **rank 5**（契约占位 1 + 鉴权 1 + 入参异常 3） |
| 每 endpoint 契约占位 | **1**（API-00162） |
| `_empty` 矩阵 | **1** 行 **未覆盖** |
| `_fail` 矩阵 | **1** 行 **已覆盖**（契约占位 + 入参失败哨兵） |
| A 线独立 Lxx work | **无**（catalog 四行键见 `coverage-fp.md`） |
| 步骤以 METHOD+path 开头（抽检 00162、00164、00166） | **通过** |
| 预期无页面/图表表述（抽检 00162、00163、00165） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| code-registry 回写 | **父控**（本子任务未改） |
