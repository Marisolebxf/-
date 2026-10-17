# 智能服务集群-科技专题服务算法库测试用例（区域产业创新人才综合评价 API）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：API  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **模块**：产业综合分析 / 区域产业创新人才综合评价  
> **catalog**：`entry_id=comp.talent-outcome` · `catalog_page_id=comp.talent-outcome` · path `/industry-comp/talent-outcome`  
> **契约真源**：`repos/lumen-ui-algo-apiview/src/catalog/comp.json` 页 `comp.talent-outcome` · endpoint `comp.talent-outcome.main`  
> **A 线对照**：`fp-split-by-api-run/work/L53.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **环境**：50897 联调台或等价 HTTP；鉴权见本册 §0（不另建 FUNC 册）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §编写细则 A～I  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-17  

---

## 0. 执行约定

| 项 | 内容 |
|----|------|
| 网关 base | `http://111.198.38.90:50897/api`（联调台 `VITE_APP_BASE_API`） |
| 业务 path | `GET /comp/v1/comp/region-talent-outcome`（查询参数 `region`、`year`，catalog 均为可选；与同模块其它 `region-*-outcome` path **互斥**，验收以 `endpoint_id=comp.talent-outcome.main` + `catalog_page_id=comp.talent-outcome` 区分） |
| 鉴权 | `POST /auth/oauth2/token`（密码模式，账号口径同 `lumen-ui-algo-apiview` LoginView）；请求头 `Authorization: Bearer <access_token>`、`TENANT-ID: 1` |
| 信封成功码 | `code` ∈ {0, "0", 200, "200"} |
| 鉴权失败 | HTTP **401** 或 **424**；体含可识别 `msg`/`message` |
| 断言分工 | **API-00664（金样）** 断言 **完整原始信封**（HTTP + `code` + 可解析体）；同册其余用例在前置写「信封成功规则见 §0，金样见 API-00664」后，可只断言失败/不可用态或字段形态 |
| catalog 状态 | `comp.talent-outcome.main` 登记 **`status=unavailable`**；**禁止**将 `sampleResponse` 中 index（如 66.3）、rank、radar/bar/pie 示例或 rows 内 score/rank 作为通过条件 |
| 样例与契约差 | `sampleResponse` 含 `rank`、`yoy`、`adv`、`radar`、`bar_items`、`pie_items`、`rows` 等；契约 `responseFields` 仅声明顶层 `index`。断言 **只强制 responseFields**；样例扩展字段不设失败条件 |
| 试调 | **本会话未试调**（子任务约束禁止 curl）；执行期按 §0 鉴权与 catalog 复核，observed 仅记入执行记录 |
| 本页 endpoint 数 | **1**（`comp.talent-outcome.main`；**非** `kind` 套餐 path） |

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00664`～`00668`。`路由route` = path 模板；`备注` 含 `endpoint_id=`、`catalog_page_id=`、组合 id。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00664 | 产业综合分析 | 区域产业创新人才综合评价 | 契约-不可用 | 人才成果评价 | 区域产业创新人才综合评价 | 人才成果评价 | catalog 不可用态下区域产业创新人才成果接口可识别非 live 成功 | 1、已确认 catalog `comp.talent-outcome.main` 为 unavailable；2、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 COMPTALENT-01 | 1、HTTP 状态为 200 或 4xx/5xx；2、响应体为对象且含可解析 code；3、不得将 sample 中 index、雷达/柱状示例或 rows 明细作为通过条件；4、若 code 属成功集合则 data 不得被当作已接通生产人才创新成果评价判定 | P0 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业综合分析模型构建·区域产业创新人才综合评价模型 | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=COMPTALENT-01 金样 §0未试调 catalog_status=unavailable |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00665 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-鉴权 | 人才成果评价 | 区域产业创新人才综合评价 | 人才成果评价 | 人才成果评价接口缺 Bearer 时网关拒绝访问 | 1、请求不携带 Authorization（可带 TENANT-ID） | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 COMPTALENT-01 | 1、HTTP 状态为 401 或 424；2、响应 code 不属于成功集合；3、不得返回含可信 index 业务载荷的成功 data | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业综合分析模型构建·区域产业创新人才综合评价模型 | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=COMPTALENT-01 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00666 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-非法region | 人才成果评价 | 区域产业创新人才综合评价 | 人才成果评价 | 不存在或非法 region 时返回可识别失败而非空成果成功态 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 COMPTALENT-02 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将失败当作无人才成果空 index 成功态 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业综合分析模型构建·区域产业创新人才综合评价模型 | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=COMPTALENT-02；矩阵挂 region、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00667 | 产业综合分析 | 区域产业创新人才综合评价 | 异常-非法year | 人才成果评价 | 区域产业创新人才综合评价 | 人才成果评价 | 非法或超出可用年份的 year 时返回可识别入参失败 | 1、已按 §0 携带有效 token 与 TENANT-ID | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 COMPTALENT-03 | 1、响应为失败态（code 非成功集合或 HTTP 4xx）；2、不得将非法 year 静默忽略后返回 sample 形态 index | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业综合分析模型构建·区域产业创新人才综合评价模型 | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=COMPTALENT-03；矩阵挂 year、_fail |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-API-00668 | 产业综合分析 | 区域产业创新人才综合评价 | 契约-字段形态 | 人才成果评价 | 区域产业创新人才综合评价 | 人才成果评价 | 成功信封下契约出参 index 若存在是否符合声明类型 | 1、已按 §0 携带有效 token 与 TENANT-ID；2、信封成功规则见 §0，金样见 API-00664 | 1.GET /comp/v1/comp/region-talent-outcome，查询参数取组合 COMPTALENT-01 | 1、若 code 属成功集合且载荷含 index，则 index 为 number；2、不得以 sample 中 66.3 或 rank 等扩展字段数值作为通过条件 | P1 | | | | | | N/A-技术项 | N/A | 科技专题服务算法库.md | 产业综合分析模型构建·区域产业创新人才综合评价模型 | N/A-技术项 | N/A | /comp/v1/comp/region-talent-outcome | M_SYNTH_184_1 | INTEG | | | endpoint_id=comp.talent-outcome.main catalog_page_id=comp.talent-outcome 组合=COMPTALENT-01；矩阵挂 index |

---

## 附录 A · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| COMPTALENT-01 | comp.talent-outcome.main | `region=440300`；`year=2025`（对齐 catalog `sampleRequest`） | unavailable 契约占位主路径 |
| COMPTALENT-02 | comp.talent-outcome.main | `region=__invalid__`；`year=2025` | 非法/不存在区域编码 |
| COMPTALENT-03 | comp.talent-outcome.main | `region=440300`；`year=0` | 非正整数/非法统计年份 |
| COMPTALENT-04 | comp.talent-outcome.main | 不传 `region`、不传 `year` | 双参缺失参考；**本轮无独立用例**，缺失语义与 unavailable 占位合并由金样执行期 observed |

---

## 附录 B · 本页 endpoint 清单

| endpoint_id | METHOD | path | status | 查询参数 |
|-------------|--------|------|--------|----------|
| comp.talent-outcome.main | GET | /comp/v1/comp/region-talent-outcome | unavailable | region、year（均可选） |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.talent-outcome.main | API-00664～API-00668 |

---

## 3. 覆盖自检（§I）

- [x] 本页 **0** 条 FUNC
- [x] unavailable endpoint 契约占位 + 金样信封（API-00664）
- [x] 异常-鉴权 1 条（API-00665）
- [x] 入参单缺陷：非法 region、非法 year（API-00666、00667）
- [x] responseFields 契约占位 1 条（API-00668 index）
- [x] `_empty` 无稳定构造 → 矩阵 **未覆盖**（见 `coverage-fp.md`）
- [x] `coverage-fp.md` 已更新
- [ ] `code-registry.yaml` 由父控回写（本子任务禁改 registry；闭区间 **API-00664～00668**）

---

## 4. 交卷计数（§I）

| 项 | 值 |
|----|-----|
| 用例条数 | **5** |
| 编号闭区间 | **API-00664**～**API-00668** |
| 金样 | **API-00664**（备注含 `金样`） |
| §0 试调 | **未试调** |
| FUNC 条数 | **0** |
