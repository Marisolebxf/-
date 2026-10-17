# 智能服务集群-科技专题服务算法库测试用例（风险洞察（异步） API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 风险洞察（异步）  
> **catalog**：`entry_id=innov.risk` · `catalog_page_id=innov.risk` · path `/innov/risk`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.risk`  
> **A 线对照**：`fp-split-by-api-run/_l6-to-catalog-map.yaml`（`innov.*` 不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
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
| 断言分工 | **API-00734、API-00739（金样）** 各断言 **完整原始信封**（HTTP + `code` + 可解析体，或网关不可路由时的 HTTP 失败态）；同 endpoint 其余用例在前置写「信封规则见 §0，金样见 API-00734 / API-00739」后，可只断言失败/不可用态或字段形态 |
| catalog 状态 | 本页 **2** 个 endpoint（`innov.risk.supply`、`innov.risk.pain`）均为 `status=unavailable`、`runtime=local_mock`；**`path` 登记为空**（Java REST 未发布）；**禁止**将 `sampleResponse` 中图谱节点、断链风险、痛难点列表等示例分值/文案作为通过条件 |
| 试调 | **未试调**（本子任务禁止 curl；执行期按金样步骤与 §0 鉴权复核） |
| 请求体 | POST JSON；各 endpoint 必填 `sub_type`（string，枚举见附录 A）；语义 `analysis_type=risk_insight` 为产品侧分析类型，catalog 未单列入参，本册以 `sub_type` 为契约入参 |
| 样例与契约差 | `sampleResponse` 含 `summary`、`nodes`/`edges`、`dimension_cards` 等扩展字段；契约 `responseFields` 对 supply 仅声明 `key_nodes`、`break_risks`（array），对 pain 仅声明 `issues`（array）。断言以 `responseFields` 为准 |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00734`～`00743`。`路由route` = catalog `path`（本页 endpoint 为空则填 `—`）；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.risk`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00734 | 创新监测 | 风险洞察（异步） | 契约-不可用 | 供应链风险图谱契约 | 风险洞察（异步） | 供应链风险图谱契约 | catalog 不可用态下供应链风险契约接口返回可识别非 live 成功 | 1、已确认 catalog `innov.risk.supply` 为 unavailable 且 path 为空；2、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-SUP-01 | 1、HTTP 状态为 404/405/4xx/5xx 或响应体为 JSON；2、若体为 JSON 则含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `key_nodes`/`break_risks` 的成功业务载荷；4、不得将 sampleResponse 节点影响力或断链等级示例作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=INNOVRISK-SUP-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00735 | 创新监测 | 风险洞察（异步） | 异常-鉴权 | 供应链风险图谱契约 | 风险洞察（异步） | 供应链风险图谱契约 | 供应链风险契约接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-SUP-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 key_nodes/break_risks 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=INNOVRISK-SUP-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00736 | 创新监测 | 风险洞察（异步） | 异常-缺必填sub_type | 供应链风险图谱契约 | 风险洞察（异步） | 供应链风险图谱契约 | 供应链风险契约缺少 sub_type 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00734 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-SUP-02 | 1、响应为失败态（HTTP 4xx/5xx 或 code 非成功集合）；2、不得将失败当作含可信 `key_nodes`/`break_risks` 的成功图谱结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=INNOVRISK-SUP-02；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00737 | 创新监测 | 风险洞察（异步） | 异常-非法sub_type | 供应链风险图谱契约 | 风险洞察（异步） | 供应链风险图谱契约 | 供应链风险契约 sub_type 非 supply_chain 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-SUP-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得将 pain_points 等其它子类型 sample 形态当作本 endpoint 供应链成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=INNOVRISK-SUP-03；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00738 | 创新监测 | 风险洞察（异步） | 异常-空sub_type | 供应链风险图谱契约 | 风险洞察（异步） | 供应链风险图谱契约 | 供应链风险契约 sub_type 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-SUP-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得与合法 `supply_chain` 主路径成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.supply catalog_page_id=innov.risk 组合=INNOVRISK-SUP-04；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00739 | 创新监测 | 风险洞察（异步） | 契约-不可用 | 发展痛难点契约 | 风险洞察（异步） | 发展痛难点契约 | catalog 不可用态下发展痛难点契约接口返回可识别非 live 成功 | 1、已确认 catalog `innov.risk.pain` 为 unavailable 且 path 为空；2、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-PAIN-01 | 1、HTTP 状态为 404/405/4xx/5xx 或响应体为 JSON；2、若体为 JSON 则含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `issues` 的成功业务载荷；4、不得将 sampleResponse 共性问题优先级或受影响企业数示例作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=INNOVRISK-PAIN-01 金样 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00740 | 创新监测 | 风险洞察（异步） | 异常-鉴权 | 发展痛难点契约 | 风险洞察（异步） | 发展痛难点契约 | 发展痛难点契约接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-PAIN-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 issues 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=INNOVRISK-PAIN-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00741 | 创新监测 | 风险洞察（异步） | 异常-缺必填sub_type | 发展痛难点契约 | 风险洞察（异步） | 发展痛难点契约 | 发展痛难点契约缺少 sub_type 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头；2、信封规则见 §0，金样见 API-00739 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-PAIN-02 | 1、响应为失败态（HTTP 4xx/5xx 或 code 非成功集合）；2、不得将失败当作含可信 `issues` 的成功痛难点结果 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=INNOVRISK-PAIN-02；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00742 | 创新监测 | 风险洞察（异步） | 异常-非法sub_type | 发展痛难点契约 | 风险洞察（异步） | 发展痛难点契约 | 发展痛难点契约 sub_type 非 pain_points 时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-PAIN-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得将 supply_chain 等其它子类型 sample 形态当作本 endpoint 痛难点成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=INNOVRISK-PAIN-03；矩阵挂 sub_type、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00743 | 创新监测 | 风险洞察（异步） | 异常-空sub_type | 发展痛难点契约 | 风险洞察（异步） | 发展痛难点契约 | 发展痛难点契约 sub_type 为空字符串时返回可识别失败 | 1、已按 §0 携带有效 token 与租户头 | 1.POST（catalog path 为空·local_mock）请求体取组合 INNOVRISK-PAIN-04 | 1、响应为失败态（code 非成功集合或 HTTP 4xx/5xx）；2、不得与合法 `pain_points` 主路径成功态混淆 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | — | | INTEG | | | endpoint_id=innov.risk.pain catalog_page_id=innov.risk 组合=INNOVRISK-PAIN-04；矩阵挂 sub_type、_fail |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INNOVRISK-SUP-01 | innov.risk.supply | `sub_type`: `supply_chain`（catalog example） | unavailable 供应链契约占位主路径 |
| INNOVRISK-SUP-02 | innov.risk.supply | 请求体 `{}`（不含 `sub_type`） | 缺必填 |
| INNOVRISK-SUP-03 | innov.risk.supply | `sub_type`: `pain_points`（同页另一 endpoint 合法值） | 非本 endpoint 子类型 |
| INNOVRISK-SUP-04 | innov.risk.supply | `sub_type`: `""` | 空字符串 |
| INNOVRISK-PAIN-01 | innov.risk.pain | `sub_type`: `pain_points`（catalog example） | unavailable 痛难点契约占位主路径 |
| INNOVRISK-PAIN-02 | innov.risk.pain | 请求体 `{}` | 缺必填 |
| INNOVRISK-PAIN-03 | innov.risk.pain | `sub_type`: `supply_chain` | 非本 endpoint 子类型 |
| INNOVRISK-PAIN-04 | innov.risk.pain | `sub_type`: `""` | 空字符串 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 必填参数 |
|-------------|--------|------|--------|---------|----------|
| innov.risk.supply | POST | （空） | unavailable | local_mock | sub_type（body） |
| innov.risk.pain | POST | （空） | unavailable | local_mock | sub_type（body） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.risk.supply | API-00734～API-00738 |
| innov.risk.pain | API-00739～API-00743 |

---

## 3. 覆盖自检

- [x] 2 个 unavailable endpoint 各 1 条契约占位金样（API-00734、API-00739）
- [x] 各 endpoint 异常-鉴权 1 条（API-00735、API-00740）
- [x] 各 endpoint 必填 `sub_type` 缺省、跨 endpoint 枚举、空字符串已覆盖（API-00736～00738、00741～00743）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定合法空结果构造）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [x] 本子任务 **不** 改 `code-registry.yaml` / `run-log.md`（父控回写）

**统计**：用例 **10** 条；编号 **API-00734**～**API-00743**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **10**（00734～00743） |
| 金样（完整信封或不可路由失败态） | **2**（00734、00739） |
| live 主路径 | **0**（双 endpoint unavailable + path 空） |
| 每 endpoint 契约占位 | **2**（supply 00734；pain 00739） |
| 异常-鉴权 | **2**（00735、00740） |
| `_empty` 矩阵 | **2** 行 **未覆盖** |
| `_fail` 矩阵 | **2** 行 **已覆盖**（各 endpoint 金样 + 入参失败用例） |
| 步骤以 POST+组合 开头（抽检 3 条：00734、00736、00742） | **通过** |
| 预期无页面/图表表述（抽检 3 条：00735、00739、00743） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| A 线 `work` 检索 `innov.risk` | **0 命中**（innov 域待 orphan 合表） |
