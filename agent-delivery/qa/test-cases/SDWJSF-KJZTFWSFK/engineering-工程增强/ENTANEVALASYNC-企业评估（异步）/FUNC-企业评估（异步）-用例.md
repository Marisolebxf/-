# 智能服务集群-科技专题服务算法库测试用例（企业评估（异步） FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.eval-async` · `catalog_page_id=entan.eval-async` · path `#/entan/eval-async`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.eval-async`  
> **A 线对照**：无对应 Lxx（工程增强，非 60 六级；`_l6-to-catalog-map.yaml` catalog_skip `entan.eval-async`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批4；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 异步评估契约 | entan.eval-async.mock |

必填参数仅 `mode`（string，枚举 technology / business / competitiveness）。主路径取 `sampleRequest`：`mode=technology`。catalog `path` 为空字符串，`status=unavailable`（文档标记未交付）。runtime 为 `local_mock`，仍按文档请求与返回体编写用例。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00316**～**FUNC-00319**，共 **4** 条）。`路由route` = catalog `path`（本 endpoint 为空则填（空））；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.eval-async`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00316 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业评估（异步） | 异步评估契约 | 验证异步评估契约功能，检查填写 chainId=INB1701 mode=technology 后返回契约示例字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、mode=technology | 1.侧栏进入「工程增强」→「企业评估（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「异步评估契约」；4.填写 mode=technology，点击调用 | 1、返回面板 body 为对象，含 technology、business、competitiveness 三个对象（与 sampleResponse 一致）；responseFields 的 task_id（string，任务标识）出现在三个对象内；2、technology 含 task_id（string，示例 EVAL-20260730-001）、sub_type（string，technology）、report_status（string，not_created）；enterprises 为数组，元素含 enterprise_code（string）、enterprise_name（string），示例 ORG00000050/智芯科技（深圳）有限公司、ORG00000054/绿能装备制造有限公司；3、technology.summary 含 max_score（number，88.6）、enterprise_count（number，5）、avg_score（number，72.3）、high_risk_count（number，1）；4、technology.result.radar_dimensions 为 string 数组（技术创新、技术人才、技术投入、技术合作、技术转化）；radar_series 为数组，元素含 enterprise_name（string）、values（number 数组），示例智芯 92/88/85/78/90、绿能 55/48/42/50/38；5、technology.result.ranking 为数组，元素含 enterprise_name（string）、score（number）、rank（number），示例智芯 score=88.6 rank=1、绿能 score=46.6 rank=5；6、technology.result.diagnosis_rows 为数组，元素含 enterprise_name（string）、total_score（number）、confidence（string）、gap_text（string），示例智芯 total_score=88.6 confidence=high gap_text=建议加强产业链协同、绿能 total_score=46.6 confidence=low gap_text=研发投入强度偏低；7、business 含 task_id（string，EVAL-20260730-002）、sub_type（string，business）、report_status（string，not_created）；enterprises 元素含 enterprise_code（ORG00000050）、enterprise_name（智芯科技（深圳）有限公司）；summary 含 max_score（number，85.2）、enterprise_count（number，5）、benchmark_avg_score（number，68.5）；8、business.result.operating_indicators 为数组，元素含 enterprise_name（string）与 indicators 对象（市场 88、产品 90、品牌 82、技术合作 78、产业链覆盖 85、关键环节参与 80，均为 number）；ranking 含 enterprise_name、score（number，85.2）、rank（number，1）；diagnosis_rows 含 enterprise_name、total_score（number，85.2）、confidence（string，high）、gap_text（string，市场与产品表现突出）；9、competitiveness 含 task_id（string，EVAL-20260730-003）、sub_type（string，competitiveness）、report_status（string，not_created）；enterprises 元素含 enterprise_code（ORG00000050）、enterprise_name（智芯科技（深圳）有限公司）；summary 含 max_score（number，85.9）、enterprise_count（number，5）、avg_score（number，66.8）；10、competitiveness.result.radar_dimensions 为 string 数组（创新能力、经营能力、成长能力）；radar_series 元素含 enterprise_name（string）、values（number 数组，智芯 92/88/86，集合均值 75.6/67.0/66.4）；ranking 含 enterprise_name、score（number，88.7）、rank（number，1）；diagnosis_rows 含 enterprise_name、total_score（number，88.7）、confidence（string，high）、gap_text（string，集合龙头） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | （空） |  | INTEG |  |  | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00317 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业评估（异步） | 异步评估契约 | 验证异步评估契约功能，检查不传 mode 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「企业评估（异步）」；2.切换至「算法测试」tab；3.接口下拉选择「异步评估契约」；4.填写 请求体不含 mode，点击调用（不传 mode），点击调用 | 1、返回面板的 message 或 msg 指出缺少 mode；2、不返回含 task_id 的成功契约对象（technology、business、competitiveness） | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | （空） |  | INTEG |  |  | endpoint_id=entan.eval-async.mock catalog_page_id=entan.eval-async 组合=EVAL-02 catalog_status=unavailable 场景=异常-入参-缺mode |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00318 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业评估（异步） | 接口信息 | 验证企业评估（异步）的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「企业评估（异步）」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=POST、path 与附录 B 一致（catalog 原文为空）；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「异步评估契约」；3、核对概览区标题、method（POST）、path（（空））与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | （空） |  | INTEG |  |  | catalog_page_id=entan.eval-async 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00319 | 算法工具库 | 科技专题服务算法库 | 待挂需规 | 待挂需规 | 企业评估（异步） | 算法测试 | 验证企业评估（异步）的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「工程增强」→「企业评估（异步）」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 POST、path 为 catalog 原文（空）；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「异步评估契约」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 POST 与 path（（空）），请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | （空） |  | INTEG |  |  | catalog_page_id=entan.eval-async 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| EVAL-01 | entan.eval-async.mock | mode=technology（sampleRequest） | 主路径全参 |
| EVAL-02 | entan.eval-async.mock | 请求体不含 mode | 缺必填 mode |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 异步评估契约 | entan.eval-async.mock | POST | （空） | mode* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.eval-async.mock | FUNC-00316、00317 |
| （页面清单） | FUNC-00318、00319 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「异步评估契约」在功能点列出现且有 ≥1 条 `场景=主流程`
- [x] 有参接口：sampleRequest 主流程 1 条；必填 mode 恰好 1 条反向
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 待挂需规 / 待挂需规
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00316～00319

**统计**：接口 **1**；主流程 **1**；反向 **1**；清单 **2**；合计 **4** 条；编号闭区间 **FUNC-00316**～**FUNC-00319**（父控 R3-批4 · entan.eval-async 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **4** |
| 编号闭区间 | **FUNC-00316**～**FUNC-00319** |
| 接口向（不含清单） | **2** |
| 清单 | **2** |
| 主流程 | **1**（FUNC-00316） |
| 反向 | **1**（FUNC-00317） |
| catalog_page_id | `entan.eval-async` |
| endpoint 数 | **1**（`entan.eval-async.mock`） |
| 已删 API 册 | `API-企业评估（异步）-用例.md`（API-01139～01140 作废，不复用） |
| 鉴权用例 | **0** |
