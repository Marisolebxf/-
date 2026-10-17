# 智能服务集群-科技专题服务算法库测试用例（科技发展规划 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：创新监测 / 科技发展规划  
> **catalog**：`entry_id=innov.tech-planning` · `catalog_page_id=innov.tech-planning` · path `/innov/tech-planning`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/innov.json` · 页 `innov.tech-planning`  
> **A 线对照**：`fp-split-by-api-run/work/` 内 **无** `innov.tech-planning` 行（`_l6-to-catalog-map.yaml`：创新监测不在本轮 60 六级）；矩阵按 catalog + `_catalog-snapshot.md`  
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
| 断言分工 | **API-00824（金样）** 断言 **完整原始信封**（HTTP + `code` + 可解析体）；同册其余用例在前置写「信封规则见 §0，金样见 API-00824」后，可只断言失败/不可用态或字段形态 |
| catalog 状态 | 本页 **1** 个 endpoint（`innov.tech-planning.metrics`）catalog `status=unavailable`、`runtime=java_api`；path `GET /innov/v1/innov/metrics`；**禁止**将 `sampleResponse` 中 13 条指标 `metric_id`、`formula_status` 或 `total=13` 作为通过条件 |
| 模块入参 | 可选 query `module`；本页 catalog example 为 `tech-planning`；与其它 innov 指标页共用 path，以 `module` 区分页语义 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 样例与契约差 | `sampleResponse.metrics[]` 含 `pending_ref` 等扩展字段；契约 `responseFields` 仅声明 `metrics`（array）、`total`（number）。断言以 `responseFields` 为准 |
| 本页 endpoint 数 | **1** |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00824`～`00828`。`路由route` = catalog path；`备注` 含 `endpoint_id=`、`catalog_page_id=innov.tech-planning`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00824 | 创新监测 | 科技发展规划 | 契约-不可用 | 科技发展规划指标清单 | 科技发展规划 | 科技发展规划指标清单 | catalog 不可用态下本页指标清单接口返回可识别非 live 成功 | 1、已确认 catalog `innov.tech-planning.metrics` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/innov/metrics，查询参数取组合 TECHPLAN-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 `code`；3、`code` 不属于成功集合，或 `data` 不构成含 array 型 `metrics` 与 number 型 `total` 的成功业务载荷；4、不得将 sample 中 M_INNOV_PLAN_DIRECTION_ALERT 等具体指标条目或 total=13 作为通过条件 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技发展规划 | N/A-技术项 | N/A | /innov/v1/innov/metrics | M_INNOV_PLAN_DIRECTION_ALERT | INTEG | | | endpoint_id=innov.tech-planning.metrics catalog_page_id=innov.tech-planning 组合=TECHPLAN-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00825 | 创新监测 | 科技发展规划 | 异常-鉴权 | 科技发展规划指标清单 | 科技发展规划 | 科技发展规划指标清单 | 指标清单接口缺有效 token 时网关拒绝访问 | 1、请求不携带 Authorization（可不携带 TENANT-ID） | 1.GET /innov/v1/innov/metrics，查询参数取组合 TECHPLAN-01，skipAuth | 1、HTTP 状态为 401 或 424；2、响应体可识别鉴权失败（非成功业务 metrics/total 载荷） | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技发展规划 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.tech-planning.metrics catalog_page_id=innov.tech-planning 组合=TECHPLAN-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00826 | 创新监测 | 科技发展规划 | 异常-非法module | 科技发展规划指标清单 | 科技发展规划 | 科技发展规划指标清单 | 指标清单 module 为不可识别 slug 时返回可识别失败 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00824 | 1.GET /innov/v1/innov/metrics，查询参数取组合 TECHPLAN-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作含 sample 形态 metrics 清单的成功业务 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技发展规划 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.tech-planning.metrics catalog_page_id=innov.tech-planning 组合=TECHPLAN-02；矩阵挂 module、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00827 | 创新监测 | 科技发展规划 | 异常-空module | 科技发展规划指标清单 | 科技发展规划 | 科技发展规划指标清单 | 指标清单 module 为空字符串时返回可识别失败或与省略 module 可区分 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /innov/v1/innov/metrics，查询参数取组合 TECHPLAN-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx），或可与 TECHPLAN-04 省略 module 的语义明确区分；2、不得将空 module 静默当作 tech-planning 并成功返回 sample 指标清单 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技发展规划 | N/A-技术项 | N/A | /innov/v1/innov/metrics | | INTEG | | | endpoint_id=innov.tech-planning.metrics catalog_page_id=innov.tech-planning 组合=TECHPLAN-03；矩阵挂 module、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00828 | 创新监测 | 科技发展规划 | 备选-省略module | 科技发展规划指标清单 | 科技发展规划 | 科技发展规划指标清单 | 指标清单省略 module 查询参数时响应可解析且不与非法 slug 成功态混淆 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封规则见 §0，金样见 API-00824 | 1.GET /innov/v1/innov/metrics，查询参数取组合 TECHPLAN-04 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体含可解析 `code`；3、若 code 属成功集合则 data.metrics 为 array 且 data.total 为 number；4、禁止将 sample 指标条数或具体 metric_id 作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 创新监测·科技发展规划 | N/A-技术项 | N/A | /innov/v1/innov/metrics | M_INNOV_PLAN_LOCAL_ADV | INTEG | | | endpoint_id=innov.tech-planning.metrics catalog_page_id=innov.tech-planning 组合=TECHPLAN-04；矩阵挂 metrics、total |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| TECHPLAN-01 | innov.tech-planning.metrics | `module`=`tech-planning`（catalog example） | unavailable 本页指标清单契约占位主路径 |
| TECHPLAN-02 | innov.tech-planning.metrics | `module`=`__invalid_module_slug__` | 不可识别模块 slug（单缺陷） |
| TECHPLAN-03 | innov.tech-planning.metrics | `module`=`""`（空字符串） | 空 module 与省略参数边界 |
| TECHPLAN-04 | innov.tech-planning.metrics | （无查询参数，省略 module） | 可选入参省略 |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | runtime | 必填参数 |
|-------------|--------|------|--------|---------|----------|
| innov.tech-planning.metrics | GET | /innov/v1/innov/metrics | unavailable | java_api | （无；`module` 可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| innov.tech-planning.metrics | API-00824、00825、00826、00827、00828 |

---

## 3. 覆盖自检（§S1）

- [x] 唯一 unavailable endpoint 已写契约占位（API-00824）
- [x] 可选入参 `module` 合法 example、非法 slug、空字符串与省略已覆盖（00824、00826、00827、00828）
- [x] 异常-鉴权 1 条（API-00825）
- [x] 契约出参 `metrics`、`total` 形态占位 1 条（API-00828）
- [x] `_empty` 在 `coverage-fp.md` 标 **未覆盖**（endpoint unavailable，无稳定必空 metrics 试调证据）
- [x] 金样 1 条且断言完整信封（API-00824）
- [x] §0 标明 **未试调**、禁止 curl
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` / `run-log.md` 由父控回写（本子任务 **未改** registry / run-log）

**统计**：用例 **5** 条；编号 **API-00824**～**API-00828**。

---

## 4. §I 交卷自检计数

| 检查项 | 结果 |
|--------|------|
| FUNC 条数 | **0** |
| API 条数 | **5**（00824～00828） |
| 金样（完整信封） | **1**（00824） |
| unavailable 契约占位 | **1**（00824） |
| 异常-鉴权 | **1**（00825） |
| `_empty` 矩阵 | **1** 行 **未覆盖** |
| `_fail` 矩阵 | **1** 行 **已覆盖**（入参/鉴权/不可用哨兵） |
| 步骤以 GET+path 开头（抽检 00824、00826） | **通过** |
| 预期无页面/图表表述（抽检 00825、00828） | **通过** |
| 无一条同时覆盖成功+失败 | **通过** |
| A 线 `work` 检索 `innov.tech-planning` | **0 命中** |
