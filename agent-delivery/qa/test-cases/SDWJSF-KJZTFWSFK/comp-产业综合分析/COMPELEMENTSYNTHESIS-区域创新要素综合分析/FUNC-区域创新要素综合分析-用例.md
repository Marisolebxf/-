# 智能服务集群-科技专题服务算法库测试用例（区域创新要素综合分析 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=comp.element-synthesis` · `catalog_page_id=comp.element-synthesis` · path `/industry-comp/element-synthesis`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/comp.json` · 页 `comp.element-synthesis`  
> **A 线对照**：`fp-split-by-api-run/work/L59.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3 返工；双 endpoint 结构对齐 svc.sz-tier；金样主流程 ESYN-01）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | METHOD | status |
|---|------------------------|-------------|--------|--------|
| 1 | 要素综合 | comp.element-synthesis.main | GET | unavailable |
| 2 | 要素贡献度与影响路径 | comp.element-synthesis.m_synth_elem_contrib | POST | available |

两个接口均仅有可选 `region`（区域编码，example `440300`）。`sampleRequest` 均传 `region=440300`。主流程跟 sampleRequest。备选与 sample 相反：不传 `region`。反向各 1 条：`region=__invalid__`。不把省略写成反向。

`GET /comp/v1/comp/element-synthesis` 只挂 title「要素综合」，与同模块其它 `element-*` path 分开验收。`POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute` 只挂 title「要素贡献度与影响路径」。`要素综合` 的 catalog `status=unavailable`，仍按该接口 sampleResponse 编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-01070**～**FUNC-01077**，共 **8** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=comp.element-synthesis`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01070 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 要素综合 | 验证要素综合功能，检查填写 region=440300调用后返回要素综合指数与三维要素字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换至「算法测试」tab；3.接口下拉选择「要素综合」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：index（number，responseFields 要素综合指数，示例 71.5）、type（number，示例 73.5）、layer（number，示例 69.8）、domain（number，示例 71.2）；2、radar 为数组，元素含类型（number，示例 73.5）、层次（number，示例 69.8）、领域（number，示例 71.2）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 88、北京 86、上海 84、杭州 76、广州 73；4、pie_items 为数组，元素含 name（string）、value（number），示例类型 34、层次 33、领域 33；5、rows 为数组，元素含 name（string）、score（number）、rank（number）、tag（string）、note（string），示例类型维度 score 73.5 rank 1 tag 良好 note 企业/政策强、领域维度 score 71.2 rank 2 tag 良好 note 重点赛道密、层次维度 score 69.8 rank 3 tag 一般 note 应用层偏弱 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-synthesis | M_SYNTH_ELEM_INDEX | INTEG |  | FUNC-01070 | endpoint_id=comp.element-synthesis.main catalog_page_id=comp.element-synthesis 组合=ESYN-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01071 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 要素综合 | 验证要素综合功能，检查不传 region 后仍返回与 sampleResponse 同类字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换至「算法测试」tab；3.接口下拉选择「要素综合」；4.不传 region，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：index（number，responseFields 要素综合指数，示例 71.5）、type（number，示例 73.5）、layer（number，示例 69.8）、domain（number，示例 71.2）；2、radar 为数组，元素含类型（number，示例 73.5）、层次（number，示例 69.8）、领域（number，示例 71.2）；3、bar_items 为数组，元素含 name（string）、value（number），示例深圳 88、北京 86、上海 84、杭州 76、广州 73；4、pie_items 为数组，元素含 name（string）、value（number），示例类型 34、层次 33、领域 33；5、rows 为数组，元素含 name、score、rank、tag、note，三条示例与主流程相同 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-synthesis | M_SYNTH_ELEM_INDEX | INTEG |  | FUNC-01071 | endpoint_id=comp.element-synthesis.main catalog_page_id=comp.element-synthesis 组合=ESYN-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01072 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 要素综合 | 验证要素综合功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值 | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换至「算法测试」tab；3.接口下拉选择「要素综合」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 index 或 rows 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /comp/v1/comp/element-synthesis |  | INTEG |  | FUNC-01072 | endpoint_id=comp.element-synthesis.main catalog_page_id=comp.element-synthesis 组合=ESYN-03 场景=异常-入参-非法region catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01073 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 要素贡献度与影响路径 | 验证要素贡献度与影响路径功能，检查填写 region=440300调用后返回 metric_id、hint 与 index 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region=440300 | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换至「算法测试」tab；3.接口下拉选择「要素贡献度与影响路径」；4.填写 region=440300，点击调用 | 1、返回面板 body 与 sampleResponse 同层逐字段：metric_id（string，示例 M_SYNTH_ELEM_CONTRIB）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 另声明 index（number，要素综合指数），sampleResponse 未给出 index 示例值，返回中应含 index 且类型为 number | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | M_SYNTH_ELEM_CONTRIB | INTEG |  | FUNC-01073 | endpoint_id=comp.element-synthesis.m_synth_elem_contrib catalog_page_id=comp.element-synthesis 组合=ECON-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01074 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 要素贡献度与影响路径 | 验证要素贡献度与影响路径功能，检查不传 region 后仍返回计算结果结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 region | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换至「算法测试」tab；3.接口下拉选择「要素贡献度与影响路径」；4.不传 region，点击调用（不传 region），点击调用 | 1、返回面板 body 与 sampleResponse 逐字段同类：metric_id（string，示例 M_SYNTH_ELEM_CONTRIB）、hint（string，示例 真实 compute 响应,以实际调用为准）；2、responseFields 声明的 index（number，要素综合指数）仍应出现，类型与主流程一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | M_SYNTH_ELEM_CONTRIB | INTEG |  | FUNC-01074 | endpoint_id=comp.element-synthesis.m_synth_elem_contrib catalog_page_id=comp.element-synthesis 组合=ECON-02 场景=备选-参数组合 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01075 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 要素贡献度与影响路径 | 验证要素贡献度与影响路径功能，检查 region 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、region 取非法值 | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换至「算法测试」tab；3.接口下拉选择「要素贡献度与影响路径」；4.填写 region=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 region 非法；2、不返回含 metric_id 或 index 的成功业务结果 | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute |  | INTEG |  | FUNC-01075 | endpoint_id=comp.element-synthesis.m_synth_elem_contrib catalog_page_id=comp.element-synthesis 组合=ECON-03 场景=异常-入参-非法region catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01076 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 接口信息 | 验证区域创新要素综合分析的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.停留在「接口信息」tab | 1、页头数量、下拉项数均为 2；2、下拉名称与 §0 各 title 一致（要素综合、要素贡献度与影响路径）；3、默认项概览 method=GET、path=/comp/v1/comp/element-synthesis；4、切换后概览对应要素贡献度与影响路径 POST /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute，参数表与示例区已刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01076 | catalog_page_id=comp.element-synthesis 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-01077 | 算法工具库 | 科技专题服务算法库 | 产业综合分析模型构建 | 区域创新要素综合分析模型 | 区域创新要素综合分析 | 算法测试 | 验证区域创新要素综合分析的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「产业综合分析」→「区域创新要素综合分析」；2.切换到「算法测试」tab；3.下拉切换到「要素贡献度与影响路径」 | 1、算法测试 tab 下拉共 2 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「要素贡献度与影响路径」；3、调用区 method 为 POST、path 为 /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute；4、请求参数区已随所选接口刷新；5、未点击调用时不校验返回字段 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  | FUNC-01077 | catalog_page_id=comp.element-synthesis 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ESYN-01 | comp.element-synthesis.main | region=440300 | 主路径（sampleRequest） |
| ESYN-02 | comp.element-synthesis.main | 不传 region | 省略可选 region（与 sample 相反） |
| ESYN-03 | comp.element-synthesis.main | region=__invalid__ | 只破坏 region |
| ECON-01 | comp.element-synthesis.m_synth_elem_contrib | region=440300 | 主路径（sampleRequest，请求体） |
| ECON-02 | comp.element-synthesis.m_synth_elem_contrib | 不传 region | 省略可选 region（与 sample 相反） |
| ECON-03 | comp.element-synthesis.m_synth_elem_contrib | region=__invalid__ | 只破坏 region |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 要素综合 | comp.element-synthesis.main | GET | /comp/v1/comp/element-synthesis | region? | unavailable |
| 要素贡献度与影响路径 | comp.element-synthesis.m_synth_elem_contrib | POST | /entan/v1/synth-metric/metric/M_SYNTH_ELEM_CONTRIB/compute | region? | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| comp.element-synthesis.main | FUNC-01070、01071、01072 |
| comp.element-synthesis.m_synth_elem_contrib | FUNC-01073、01074、01075 |
| （页面清单） | FUNC-01076、01077 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 2 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`（FUNC-01070 要素综合、FUNC-01073 要素贡献度与影响路径）
- [x] 仅可选 region 的接口各 3 条（sampleRequest 主流程 + 省略 region 备选 + 非法 region 反向）
- [x] unavailable（要素综合）仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L59：`产业综合分析模型构建` / `区域创新要素综合分析模型`
- [x] 测试内容均含「验证」与「检查」；登录仅在前置条件
- [x] 双接口页清单用例 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`（含切换步骤）
- [x] `coverage-fp.md` 已同步 FUNC-01070～01077；A 线 `work/L59.md` 未改

**统计**：catalog endpoint **2**；title **2**；FUNC 用例 **8** 条；主流程 **2**、备选 **2**、反向 **2**、清单 **2**；编号闭区间 **FUNC-01070**～**FUNC-01077**（父控 R3 返工 · comp.element-synthesis）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **8** |
| 编号闭区间 | **FUNC-01070**～**FUNC-01077** |
| 接口向（不含清单） | **6** |
| 主流程 | **2**（FUNC-01070、FUNC-01073） |
| 备选-参数组合 | **2**（01071、01074） |
| 反向 | **2**（01072、01075） |
| 清单 | **2**（01076、01077） |
| catalog_page_id | `comp.element-synthesis` |
| endpoint 数 | **2** |
| 已删 API 册 | `API-区域创新要素综合分析-用例.md`（API-01814～01819 作废，不复用） |
| 鉴权用例 | **0** |
