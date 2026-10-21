# 智能服务集群-科技专题服务算法库测试用例（深圳产业链 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=chain.topic-panorama` · `catalog_page_id=chain.topic-panorama` · path `/chain/topic-panorama`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/chain.json` · 页 `chain.topic-panorama`  
> **A 线对照**：`fp-split-by-api-run/work/L15.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批6）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | A/B/C 按 op_id 写入 | chain.topic-panorama.ops | running |
| 2 | 专题全景图谱 | chain.topic-panorama.main | running |
| 3 | 深圳产业链模型 | chain.topic-panorama.m_chain_deep_118_1 | available |

**sampleRequest 取值**：写入类 `op_id=CHAIN_NER_INDUSTRY`，body `scope=one`、`id=INB13`、`mode=rule`、`dry_run=true`（不含 filter、relation_whitelist、dest_types）。专题全景图谱 `chainId=INB13`。深圳产业链模型 body 键 `chain_id=INB1701`（params.name 为 chainId，example 为 INB170101）。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00428**～**FUNC-00448**，共 **21** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=chain.topic-panorama`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00428 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查填写 sampleRequest 所示参数 后返回写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-01 场景=主流程 catalog_status=running 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00429 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查省略可选 id 时仍返回与主流程一致的写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同 OPS-01，body 不传 id，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-02 场景=备选-参数组合-省略 id catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00430 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查额外传入 filter 时仍返回与主流程一致的写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，另传filter={}，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-03 场景=备选-参数组合-传入 filter catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00431 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查省略可选 mode 时仍返回与主流程一致的写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同 OPS-01，body 不传 mode，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-04 场景=备选-参数组合-省略 mode catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00432 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查省略可选 dry_run 时仍返回与主流程一致的写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同 OPS-01，body 不传 dry_run，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-05 场景=备选-参数组合-省略 dry_run catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00433 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查传入 relation_whitelist 时仍返回与主流程一致的写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，另传relation_whitelist=[]，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-06 场景=备选-参数组合-传入 relation_whitelist catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00434 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查传入 dest_types 时仍返回与主流程一致的写入结果字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、写入类参数填写 path/op_id=CHAIN_NER_INDUSTRY、scope=one、id=INB13、mode=rule、dry_run=true，点击调用） | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，另传dest_types=[]，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：op_id（string，示例 CHAIN_NER_INDUSTRY）；written_nodes（array，responseFields 本次写入或 dry_run 计划写入的节点，示例为空数组）；written_edges（array，responseFields 本次写入或 dry_run 计划写入的边，示例为空数组）；skipped（array，responseFields empty_field/no_stable_id/not_in_wave/vid_too_long，示例为空数组）；source（string，responseFields，示例 demo_gkx_chain）；space（string，responseFields 恒为 demo_gkx_chain，示例 demo_gkx_chain）；mode_effective（string，示例 rule）；llm_fallback（boolean，示例 false）；calc_batch_id（string，示例空串） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} | M_CHAIN_GRAPH_102_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-07 场景=备选-参数组合-传入 dest_types catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00435 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查不传 op_id 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 path 与 body 均不传 op_id，其余同 OPS-01，点击调用 | 1、返回面板的 message 或 msg 指出 op_id 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-08 场景=异常-入参-缺op_id catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00436 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查不传 scope 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同 OPS-01，body 不传 scope，点击调用 | 1、返回面板的 message 或 msg 指出 scope 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-09 场景=异常-入参-缺scope catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00437 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查 id 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，id=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 id 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-10 场景=异常-入参-非法id catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00438 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查 filter 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，filter=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 filter 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-11 场景=异常-入参-非法filter catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00439 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查 mode 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，mode=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 mode 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-12 场景=异常-入参-非法mode catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00440 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查 dry_run 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，dry_run=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 dry_run 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-13 场景=异常-入参-非法dry_run catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00441 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查 relation_whitelist 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，relation_whitelist=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 relation_whitelist 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-14 场景=异常-入参-非法relation_whitelist catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00442 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | A/B/C 按 op_id 写入 | 验证 A/B/C 按 op_id 写入功能，检查 dest_types 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「A/B/C 按 op_id 写入」；4.填写 同OPS-01，dest_types=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 dest_types 缺失或非法；2、不返回含 written_nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/graph/ops/{op_id} |  | INTEG |  |  | endpoint_id=chain.topic-panorama.ops catalog_page_id=chain.topic-panorama 组合=OPS-15 场景=异常-入参-非法dest_types catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00443 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | 专题全景图谱 | 验证专题全景图谱功能，检查填写 chainId=INB1701=INB13 查询后返回 nodes、edges 等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、chainId=INB13 | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「专题全景图谱」；4.填写 chainId=INB13，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：nodes（array，responseFields 专题节点，示例为空数组）；edges（array，responseFields 结构边，示例为空数组）；source（string，示例 demo_gkx_chain）；space（string，示例 demo_gkx_chain） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama | M_CHAIN_NODE_COUNT | INTEG |  |  | endpoint_id=chain.topic-panorama.main catalog_page_id=chain.topic-panorama 组合=PAN-01 场景=主流程 catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00444 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | 专题全景图谱 | 验证专题全景图谱功能，检查不传 chainId 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「专题全景图谱」；4.不传 chainId，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出 chainId 缺失；2、不返回含 nodes 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /chain/v1/chain/{chainId}/panorama |  | INTEG |  |  | endpoint_id=chain.topic-panorama.main catalog_page_id=chain.topic-panorama 组合=PAN-02 场景=异常-入参-缺chainId catalog_status=running |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00445 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | 深圳产业链模型 | 验证深圳产业链模型功能，检查填写 sampleRequest 所示参数 传 chain_id=INB1701 后返回 metric_id 等字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「深圳产业链模型」；4.填写 bodychain_id=INB1701，点击调用 | 1、返回面板 body 为对象，与 sampleResponse 同层逐字段一致：metric_id（string，responseFields 指标 ID，示例 M_CHAIN_DEEP_118_1）；hint（string，示例 真实 compute 响应,以实际调用为准） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute | M_CHAIN_DEEP_118_1 | INTEG |  |  | endpoint_id=chain.topic-panorama.m_chain_deep_118_1 catalog_page_id=chain.topic-panorama 组合=DEEP-01 场景=主流程 catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00446 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | 深圳产业链模型 | 验证深圳产业链模型功能，检查不传 chainId/chain_id 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换至「算法测试」tab；3.接口下拉选择「深圳产业链模型」；4.填写 body 为空，不传 chainId/chain_id，点击调用（不传 chainId），点击调用 | 1、返回面板的 message 或 msg 指出 chainId 缺失；2、不返回含 metric_id 的成功业务 body | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute |  | INTEG |  |  | endpoint_id=chain.topic-panorama.m_chain_deep_118_1 catalog_page_id=chain.topic-panorama 组合=DEEP-02 场景=异常-入参-缺chainId catalog_status=available |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00447 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | 接口信息 | 验证深圳产业链的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.停留在「接口信息」tab；3.接口下拉切换到「专题全景图谱」 | 1、页头数量、下拉项数均为 3；2、下拉名称与 §0 各 title 一致；3、默认项概览 method、path 对应 A/B/C 按 op_id 写入 POST /chain/v1/chain/graph/ops/{{op_id}}；4、切换后概览对应专题全景图谱 GET /chain/v1/chain/{{chainId}}/panorama，参数表与示例区已刷新；1、确认页头接口数量为 3；2、查看默认选中接口的概览 title、method、path 与 §0 清单第一项一致 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.topic-panorama 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00448 | 算法工具库 | 科技专题服务算法库 | 深圳产业链模型构建 | 深圳产业链模型构建 | 深圳产业链 | 算法测试 | 验证深圳产业链的算法测试功能，检查下拉与 catalog 一致，且切换接口后调用区 method、path 正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「图谱」→「深圳产业链」；2.切换到「算法测试」tab；3.下拉切换到「深圳产业链模型」 | 1、算法测试 tab 下拉共 3 项，名称与接口信息 tab、catalog 一致；2、切换后下拉显示「深圳产业链模型」；3、调用区 method 为 POST、path 为 /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute；4、请求区已随所选接口刷新 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A |  |  | INTEG |  |  | catalog_page_id=chain.topic-panorama 场景=算法测试-清单 |
---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| OPS-01 | chain.topic-panorama.ops | path/body op_id=CHAIN_NER_INDUSTRY；scope=one；id=INB13；mode=rule；dry_run=true | 主路径（sampleRequest） |
| OPS-02 | chain.topic-panorama.ops | 同 OPS-01，body 不传 id | 省略可选 id |
| OPS-03 | chain.topic-panorama.ops | 同 OPS-01，另传 filter={} | 传入可选 filter |
| OPS-04 | chain.topic-panorama.ops | 同 OPS-01，body 不传 mode | 省略可选 mode |
| OPS-05 | chain.topic-panorama.ops | 同 OPS-01，body 不传 dry_run | 省略可选 dry_run |
| OPS-06 | chain.topic-panorama.ops | 同 OPS-01，另传 relation_whitelist=[] | 传入可选 relation_whitelist |
| OPS-07 | chain.topic-panorama.ops | 同 OPS-01，另传 dest_types=[] | 传入可选 dest_types |
| OPS-08 | chain.topic-panorama.ops | path 与 body 均不传 op_id，其余同 OPS-01 | 缺必填 op_id |
| OPS-09 | chain.topic-panorama.ops | 同 OPS-01，body 不传 scope | 缺必填 scope |
| OPS-10 | chain.topic-panorama.ops | 同 OPS-01，id=__invalid__ | 非法 id |
| OPS-11 | chain.topic-panorama.ops | 同 OPS-01，filter=__invalid__ | 非法 filter |
| OPS-12 | chain.topic-panorama.ops | 同 OPS-01，mode=__invalid__ | 非法 mode |
| OPS-13 | chain.topic-panorama.ops | 同 OPS-01，dry_run=__invalid__ | 非法 dry_run |
| OPS-14 | chain.topic-panorama.ops | 同 OPS-01，relation_whitelist=__invalid__ | 非法 relation_whitelist |
| OPS-15 | chain.topic-panorama.ops | 同 OPS-01，dest_types=__invalid__ | 非法 dest_types |
| PAN-01 | chain.topic-panorama.main | chainId=INB13 | 主路径（sampleRequest） |
| PAN-02 | chain.topic-panorama.main | 不传 chainId | 缺必填 chainId |
| DEEP-01 | chain.topic-panorama.m_chain_deep_118_1 | body chain_id=INB1701 | 主路径（sampleRequest） |
| DEEP-02 | chain.topic-panorama.m_chain_deep_118_1 | body 为空，不传 chainId/chain_id | 缺必填 chainId |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| A/B/C 按 op_id 写入 | chain.topic-panorama.ops | POST | /chain/v1/chain/graph/ops/{op_id} | op_id*；scope*；id?；filter?；mode?；dry_run?；relation_whitelist?；dest_types? | running |
| 专题全景图谱 | chain.topic-panorama.main | GET | /chain/v1/chain/{chainId}/panorama | chainId* | running |
| 深圳产业链模型 | chain.topic-panorama.m_chain_deep_118_1 | POST | /innov/v1/industry/chainan/metric/M_CHAIN_DEEP_118_1/compute | chainId* | available |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| chain.topic-panorama.ops | FUNC-00428～00442 |
| chain.topic-panorama.main | FUNC-00443、00444 |
| chain.topic-panorama.m_chain_deep_118_1 | FUNC-00445、00446 |
| （页面清单） | FUNC-00447、00448 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 3 个 title 均在功能点列出现且各有 1 条主流程（FUNC-00428、00443、00445）
- [x] 写入接口：sampleRequest 主流程 1 + 可选参数组合 6 + 每参数反向 8 = 15
- [x] 专题全景图谱、深圳产业链模型：各 1 条主流程 + 必填 chainId 缺省反向 1 条
- [x] 页面清单：接口信息、算法测试各 1 条（FUNC-00447、00448）
- [x] 步骤为联调台侧栏进页 + 算法测试调用，无 GET/POST 步骤
- [x] 五级/六级按 L15（深圳产业链模型构建）填写
- [x] `coverage-fp.md` 已同步 FUNC-00428～00448

**统计**：catalog endpoint **3**；FUNC 用例 **21** 条；主流程 **3**、备选 **6**、反向 **10**、清单 **2**；编号闭区间 **FUNC-00428**～**FUNC-00448**（R3-批6 chain.topic-panorama）。
