# 智能服务集群-科技专题服务算法库测试用例（焦点识别(单个政策) FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=policy.focus-one` · `catalog_page_id=policy.focus-one` · path `#/policy/focus-one`  
> **联调台**：`https://edu.itic-sci.com/dma/algovwz/`  
> **契约真源**：`lumen-ui-algo-apiview/src/catalog/policy.json` · 页 `policy.focus-one`  
> **A 线对照**：`fp-split-by-api-run/work/L35.md`（挂接表 `catalog_skip`：本页为 L35 单政策变体，按 path 去重；不把 `policy.focus` 的 field 灌成新用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` §S1（第三轮 R3-批10）  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id | status |
|---|------------------------|-------------|--------|
| 1 | 单条焦点识别 | policy.focus-one.main | unavailable |

参数：`mode?` `title?` `text!` `execution?` `aux?`。`sampleRequest` 五字段都传。正向只写 1 条全参主流程，再对 4 个可选参数各写 1 条「不传」（与 sample 相反），不做全组合。反向 5 条：`text` 缺省，`mode` / `title` / `execution` / `aux` 各 1 条非法。catalog `status=unavailable`，仍按文档返回体编写，备注注明未交付。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00611**～**FUNC-00622**，共 **12** 条）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=policy.focus-one`、组合 id（如有）、`场景=`。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00611 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查填写 sampleRequest 所示参数 提交 mode、title、text、execution、aux 后返回焦点、堵点与建议字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、请求体使用文档 sampleRequest（mode=rule，title、text、execution、aux 取示例原文） | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.填写 mode=rule、title=深圳市加快集成电路产业发展若干措施、text=推进先进封装产业化，支持科技型中小企业流片补贴。、execution=流片补贴兑付率低，仅完成计划40%。、aux=行业解读认为先进封装是下一阶段焦点。，点击调用 | 1、返回面板 body 的 data 为对象，与 sampleResponse 同层逐字段一致：mode（string，sampleResponse 多出字段，示例 rule）；focus_list（array，responseFields 焦点词 Tag；第1条 term=集成电路（string）、score=1（number）、evidence=rule（string））；bottleneck_list（array，responseFields 堵点清单；第1条 item=流片补贴兑付率低（string）、evidence=文本/执行措辞（string））；suggestions（array，responseFields 优化建议；第1条 item=补充实施进度（string）、reason=缺执行数据（string））；persisted（boolean，sampleResponse 多出字段，示例 false） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00611 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-01 场景=主流程 catalog_status=unavailable 文档标记未交付 金样 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00612 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查省略可选 mode、其余保持 sampleRequest 时仍返回焦点、堵点与建议字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 mode，title、text、execution、aux 保持文档示例 | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.不传 mode，填写 title、text、execution、aux 同 FO1-01，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 mode（string）、focus_list（array）、bottleneck_list（array）、suggestions（array）、persisted（boolean）；3、focus_list 元素仍含 term（string）、score（number）、evidence（string）；4、bottleneck_list 元素仍含 item（string）、evidence（string）；5、suggestions 元素仍含 item（string）、reason（string）；6、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00612 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-02 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00613 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查省略可选 title、其余保持 sampleRequest 时仍返回焦点、堵点与建议字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 title，mode、text、execution、aux 保持文档示例 | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.不传 title，填写 mode、text、execution、aux 同 FO1-01，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 mode（string）、focus_list（array）、bottleneck_list（array）、suggestions（array）、persisted（boolean）；3、focus_list 元素仍含 term（string）、score（number）、evidence（string）；4、bottleneck_list 元素仍含 item（string）、evidence（string）；5、suggestions 元素仍含 item（string）、reason（string）；6、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00613 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-03 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00614 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查省略可选 execution、其余保持 sampleRequest 时仍返回焦点、堵点与建议字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 execution，mode、title、text、aux 保持文档示例 | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.不传 execution，填写 mode、title、text、aux 同 FO1-01，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 mode（string）、focus_list（array）、bottleneck_list（array）、suggestions（array）、persisted（boolean）；3、focus_list 元素仍含 term（string）、score（number）、evidence（string）；4、bottleneck_list 元素仍含 item（string）、evidence（string）；5、suggestions 元素仍含 item（string）、reason（string）；6、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00614 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-04 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00615 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查省略可选 aux、其余保持 sampleRequest 时仍返回焦点、堵点与建议字段结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 aux，mode、title、text、execution 保持文档示例 | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.不传 aux，填写 mode、title、text、execution 同 FO1-01，点击调用 | 1、返回面板 body 的 data 为对象；2、仍含 mode（string）、focus_list（array）、bottleneck_list（array）、suggestions（array）、persisted（boolean）；3、focus_list 元素仍含 term（string）、score（number）、evidence（string）；4、bottleneck_list 元素仍含 item（string）、evidence（string）；5、suggestions 元素仍含 item（string）、reason（string）；6、结构与 sampleResponse 同类 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one | M_POLICY_DEEP_166_1 | INTEG |  | FUNC-00615 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-05 场景=备选-参数组合 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00616 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查不传必填 text 时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 text，mode、title、execution、aux 保持文档示例 | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.不传 text，填写 mode、title、execution、aux 同 FO1-01，点击调用 | 1、返回面板的 message 或 msg 指出缺少 text；2、不返回含 focus_list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00616 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-06 场景=异常-入参-缺text catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00617 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查 mode 取非法值时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、仅 mode 取非法值，其余保持 sampleRequest | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.填写 mode=__invalid__（不在rule、llm）、title、text、execution、aux 同 FO1-01，点击调用 | 1、返回面板的 message 或 msg 指出 mode 非法；2、不返回含 focus_list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00617 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-07 场景=异常-入参-非法mode catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00618 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查 title 取非法类型时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、仅 title 取非 string，其余保持 sampleRequest | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.填写 title=0（number，非string）、mode、text、execution、aux 同 FO1-01，点击调用 | 1、返回面板的 message 或 msg 指出 title 非法；2、不返回含 focus_list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00618 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-08 场景=异常-入参-非法title catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00619 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查 execution 取非法类型时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、仅 execution 取非 string，其余保持 sampleRequest | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.填写 execution=0（number，非string）、mode、title、text、aux 同 FO1-01，点击调用 | 1、返回面板的 message 或 msg 指出 execution 非法；2、不返回含 focus_list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00619 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-09 场景=异常-入参-非法execution catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00620 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 单条焦点识别 | 验证单条焦点识别功能，检查 aux 取非法类型时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、仅 aux 取非 string，其余保持 sampleRequest | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab；3.接口下拉选择「单条焦点识别」；4.填写 aux=0（number，非string）、mode、title、text、execution 同 FO1-01，点击调用 | 1、返回面板的 message 或 msg 指出 aux 非法；2、不返回含 focus_list 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00620 | endpoint_id=policy.focus-one.main catalog_page_id=policy.focus-one 组合=FO1-10 场景=异常-入参-非法aux catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00621 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 接口信息 | 验证焦点识别(单个政策)的接口信息功能，检查接口数量、名称和 URL 与文档一致 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.停留在「接口信息」tab | 1、页头接口数量与下拉项数均为 1；2、下拉名称与 §0 唯一 title 一致；3、概览 method=POST、path 与附录 B 一致；4、参数表与示例区已展示（不逐字段核对 params、responseFields、sampleResponse）；1、核对页头显示「1 个接口」；2、核对「当前接口」下拉仅此 1 项，名称为「单条焦点识别」；3、核对概览区标题、method（POST）、path（/policy/v1/policy/analysis/focus-one）与该接口一致，参数表与示例区有内容 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00621 | catalog_page_id=policy.focus-one 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00622 | 算法工具库 | 科技专题服务算法库 | 政策焦点识别模型 | 焦点识别 | 焦点识别(单个政策) | 算法测试 | 验证焦点识别(单个政策)的算法测试功能，检查下拉与 catalog 一致，且调用区 method、path 正常展示 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「政策分析」→「焦点识别(单个政策)」；2.切换至「算法测试」tab | 1、算法测试 tab 下拉共 1 项，名称与接口信息 tab、catalog 一致；2、调用区 method 为 POST、path 为 /policy/v1/policy/analysis/focus-one；3、请求参数区已随所选接口刷新；4、未点击调用时不校验返回字段；1、核对调用区下拉仅此 1 项，名称为「单条焦点识别」；2、核对接口下拉与「接口信息」tab 名称一致；3、确认调用区展示 POST /policy/v1/policy/analysis/focus-one，请求参数区正常刷新（不点击调用） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /policy/v1/policy/analysis/focus-one |  | INTEG |  | FUNC-00622 | catalog_page_id=policy.focus-one 场景=算法测试-清单 |

---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| FO1-01 | policy.focus-one.main | mode=rule；title=深圳市加快集成电路产业发展若干措施；text=推进先进封装产业化，支持科技型中小企业流片补贴。；execution=流片补贴兑付率低，仅完成计划40%。；aux=行业解读认为先进封装是下一阶段焦点。 | 主路径全参（sampleRequest） |
| FO1-02 | policy.focus-one.main | 不传 mode；title、text、execution、aux 同 FO1-01 | 省略可选 mode（sample 含 mode） |
| FO1-03 | policy.focus-one.main | 不传 title；mode、text、execution、aux 同 FO1-01 | 省略可选 title（sample 含 title） |
| FO1-04 | policy.focus-one.main | 不传 execution；mode、title、text、aux 同 FO1-01 | 省略可选 execution（sample 含 execution） |
| FO1-05 | policy.focus-one.main | 不传 aux；mode、title、text、execution 同 FO1-01 | 省略可选 aux（sample 含 aux） |
| FO1-06 | policy.focus-one.main | 不传 text；mode、title、execution、aux 同 FO1-01 | 缺必填 text |
| FO1-07 | policy.focus-one.main | mode=__invalid__（不在 rule、llm）；title、text、execution、aux 同 FO1-01 | 只破坏 mode |
| FO1-08 | policy.focus-one.main | title=0（number，非 string）；mode、text、execution、aux 同 FO1-01 | 只破坏 title |
| FO1-09 | policy.focus-one.main | execution=0（number，非 string）；mode、title、text、aux 同 FO1-01 | 只破坏 execution |
| FO1-10 | policy.focus-one.main | aux=0（number，非 string）；mode、title、text、execution 同 FO1-01 | 只破坏 aux |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 单条焦点识别 | policy.focus-one.main | POST | /policy/v1/policy/analysis/focus-one | mode?；title?；text*；execution?；aux? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| policy.focus-one.main | FUNC-00611、00612、00613、00614、00615、00616、00617、00618、00619、00620 |
| （页面清单） | FUNC-00621、00622 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 1 个 title「单条焦点识别」在功能点列出现且有 ≥1 条 `场景=主流程`（FUNC-00611）
- [x] 有参接口：sample 全参 1 条主流程；每个可选参数单独省略 1 条备选（00612～00615）；反向缺 text + 非法 mode / title / execution / aux（00616～00620）
- [x] unavailable 仍按 catalog sampleResponse 写主流程，备注注明未交付
- [x] 步骤均为 algovwz 页面操作；0 条裸 GET/POST 步骤
- [x] 五级/六级按 L35（政策焦点识别模型 / 焦点识别）填写
- [x] 测试内容均含「验证」「检查」；登录仅在前置条件
- [x] 单接口页清单用例 2 条：预期写明下拉仅此 1 项；`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] `coverage-fp.md` 已同步 FUNC-00611～00622

**统计**：catalog endpoint **1**；title **1**；FUNC 用例 **12** 条；主流程 **1**、备选 **4**、反向 **5**、清单 **2**；编号闭区间 **FUNC-00611**～**FUNC-00622**（R3-批10 policy.focus-one）。

---

## 4. 交卷计数

| 项 | 值 |
|----|-----|
| 用例条数 | **12** |
| 编号闭区间 | **FUNC-00611**～**FUNC-00622** |
| 接口向（不含清单） | **10** |
| 主流程 | **1** |
| 备选-参数组合 | **4** |
| 反向 | **5** |
| 清单 | **2** |
| 已删 API 册 | `API-焦点识别(单个政策)-用例.md`（API-01409～01418 作废，不复用；B 线只保留本 FUNC 册） |
| 鉴权用例 | **0** |
