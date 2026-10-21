# 智能服务集群-科技专题服务算法库测试用例（企业创新能力评估 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=entan.innovation` · `catalog_page_id=entan.innovation` · path `#/entan/innovation`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/entan.json` · 页 `entan.innovation`  
> **A 线对照**：无对应 Lxx（与 L31 相邻但不扩六级；`_l6-to-catalog-map.yaml` catalog_skip `entan.innovation`；不改 work）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批4；金样 CHAINBASIC）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 创新能力指数（企业集合） | entan.innovation.rank |

**enterprise_codes 试调取值**：文档 `sampleRequest` 四元组 `0218337e44ca794fee9850cf1627b03b`、`05dc8024336db695425572625773381b`、`0551ccfde6aa2b3c52e647e283204040`、`05ff69620c962ce3bbb852351f077299`（可替换为环境有效企业标识）。本接口仅此 1 个必填参数，无可选参数。catalog `status=unavailable`，仍按文档请求与返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00320**～**FUNC-00323**，共 **4** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=entan.innovation`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00320 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业创新能力评估模型 | 企业创新能力评估 | 创新能力指数（企业集合） | 验证创新能力指数（企业集合）功能，检查填写 chainId=INB1701 enterprise_codes 查询后返回创新能力指数明细等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、enterprise_codes=四元组 | 1.侧栏进入「企业分析」→「企业创新能力评估」；2.切换至「算法测试」tab；3.接口下拉选择「创新能力指数（企业集合）」；4.填写 enterprise_codes=[0218337e44ca794fee9850cf1627b03b,05dc8024336db695425572625773381b,0551ccfde6aa2b3c52e647e283204040,05ff69620c962ce3bbb852351f077299]，点击调用 | 1、返回面板含 metric_id（string，sampleResponse 示例 M_ENT_INNOVATION_INDEX）、metric_name_zh（string，示例企业创新能力指数）；2、value 为 object，value.enterprises 为 array（responseFields 企业创新能力指数明细），元素含 org_id（string）、enterprise_name（string）、innovation_index（number）；3、sampleResponse 示例两条：org_id=0218337e44ca794fee9850cf1627b03b、enterprise_name=云启智元科技股份有限公司、innovation_index=92.5，以及 org_id=05dc8024336db695425572625773381b、enterprise_name=星辰半导体香港有限公司、innovation_index=84.1；4、data_source（string，示例 real）、confidence（string，示例 high）；5、calc_process 为 object，含 definition（string，示例企业创新能力指数）、formula（string，示例创新投入/产出/可持续三维加权）、source_tables（string 数组，示例 ads.enterprise_score）、model_version（string，示例 entan-v1.0）。示例文案与数值说明 sampleResponse 形态，字段与结构须与文档一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | M_ENT_INNOVATION_INDEX | INTEG |  |  | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-01 catalog_status=unavailable 场景=主流程 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00321 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业创新能力评估模型 | 企业创新能力评估 | 创新能力指数（企业集合） | 验证创新能力指数（企业集合）功能，检查不传 enterprise_codes 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业创新能力评估」；2.切换至「算法测试」tab；3.接口下拉选择「创新能力指数（企业集合）」；4.不传 enterprise_codes，点击调用（不传 enterprise_codes），点击调用 | 1、返回面板的 message 或 msg 指出缺少 enterprise_codes；2、不返回含 innovation_index 的成功业务 enterprises 列表 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute |  | INTEG |  |  | endpoint_id=entan.innovation.rank catalog_page_id=entan.innovation 组合=INNO-02 catalog_status=unavailable 场景=异常-入参-缺enterprise_codes |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00322 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业创新能力评估模型 | 企业创新能力评估 | 接口信息 | 验证企业创新能力评估的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业创新能力评估」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=POST、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「创新能力指数（企业集合）」；3、核对概览区标题、method（POST）、path（/entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute |  | INTEG |  |  | catalog_page_id=entan.innovation 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00323 | 算法工具库 | 科技专题服务算法库 | 企业深度分析模型构建 | 企业创新能力评估模型 | 企业创新能力评估 | 算法测试 | 验证企业创新能力评估的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「企业分析」→「企业创新能力评估」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 POST、path 为 /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「创新能力指数（企业集合）」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 POST /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute |  | INTEG |  |  | catalog_page_id=entan.innovation 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| INNO-01 | entan.innovation.rank | enterprise_codes=[0218337e44ca794fee9850cf1627b03b, 05dc8024336db695425572625773381b, 0551ccfde6aa2b3c52e647e283204040, 05ff69620c962ce3bbb852351f077299] | 主路径全参（sampleRequest） |
| INNO-02 | entan.innovation.rank | 不传 enterprise_codes | 缺必填 enterprise_codes |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 创新能力指数（企业集合） | entan.innovation.rank | POST | /entan/v1/entan/metric/M_ENT_INNOVATION_INDEX/compute | enterprise_codes* | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| entan.innovation.rank | FUNC-00320、00321 |
| （页面清单） | FUNC-00322、00323 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「创新能力指数（企业集合）」在功能点列出现且有 ≥1 条 `场景=主流程`
- [x] 有参接口：文档示例全参 1 条主流程；必填 enterprise_codes 恰好 1 条反向；无可选参数，无备选组合
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 企业深度分析模型构建 / 企业创新能力评估模型
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00320～00323

**统计**：接口 **1**；主流程 **1**；反向 **1**；清单 **2**；合计 **4** 条；编号闭区间 **FUNC-00320**～**FUNC-00323**（父控 R3-批4 · entan.innovation 分配）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **4** |
| 编号闭区间 | **FUNC-00320**～**FUNC-00323** |
| 接口向（不含清单） | **2** |
| 清单 | **2** |
| 已删 API 册 | `API-企业创新能力评估-用例.md`（API-01141～01142 作废，不复用） |
| 鉴权用例 | **0** |
