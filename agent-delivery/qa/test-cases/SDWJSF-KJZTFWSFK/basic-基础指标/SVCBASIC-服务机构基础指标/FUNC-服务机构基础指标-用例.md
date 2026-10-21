# 智能服务集群-科技专题服务算法库测试用例（服务机构基础指标 FUNC）

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：SDWJSF/KJZTFWSFK  
> **版本**：v1.0  
> **catalog**：`entry_id=svc.basic` · `catalog_page_id=svc.basic` · path `#/industry-service/basic`  
> **A 线对照**：`fp-split-by-api-run/work/L04.md`（覆盖矩阵用，禁止 field 一行一用例）  
> **编排**：`agent-delivery/qa/algo-lib-api-case-playbook.md` 第三轮 R3-批1  
> **联调台**：https://edu.itic-sci.com/dma/algovwz/  
> **维护人**：agent:qa-agent  
> **更新日期**：2026-10-19  

---

## 0. 本页接口清单（与调试台下拉框 title 一致）

| # | title（功能点列原文） | endpoint_id |
|---|------------------------|-------------|
| 1 | 服务机构基础指标（全维度） | svc.basic.indicators |
| 2 | 全球服务机构产业布局 | svc.basic.indicators-layout |
| 3 | 全球服务机构分布 | svc.basic.indicators-global |
| 4 | 投融资动态资讯 | svc.basic.indicators-invest |
| 5 | 新增服务机构动态 | svc.basic.indicators-new |
| 6 | 深圳服务机构规模及分布 | svc.basic.indicators-sz |

**kind 文档取值**：全维度 `all`；产业布局 `layout`；全球分布 `global`；投融资 `invest`；新增 `new`；深圳 `sz`。六个接口共用 `GET /entan/v1/svc/indicators`，`kind` 均为可选；省略属于备选，非法值作反向。同 path 多 endpoint 时步骤靠下拉 title 区分，备注写 `endpoint_id`。

---

## 1. 用例总表

> 取号：`ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-#####`（本轮 **FUNC-00080**～**FUNC-00099**）。`路由route` = path；`备注` 含 `endpoint_id=`、`catalog_page_id=svc.basic`、`场景=`、组合 id。本页 6 个接口 `status=unavailable`，仍按 catalog 返回体编写。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00080 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 服务机构基础指标（全维度） | 验证服务机构基础指标（全维度）功能，检查填写 kind=all调用后返回全维度 layout、global、invest 等指标字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=all | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构基础指标（全维度）」；4.填写 kind=all，点击调用 | 1、返回面板的 data 为对象；2、含 layout、global、invest、invest_events、new、sz_scale、sz_dist（均为 array；layout/global/invest/new/sz_scale/sz_dist 见 responseFields，invest_events 仅见 sampleResponse）；3、layout 元素含 service_type（string）、industry_field（string）、org_count（number）、growth_rate（number）；4、global 元素含 country（string）、org_count（number）；5、invest 元素含 stat_year（number）、amount（number）；6、invest_events 元素含 org_name（string）、investee（string）、domain（string）、amount（number）、event_time（string）；7、new 元素含 stat_year（number）、org_count（number）、growth_rate（number）；8、sz_scale 元素含 org_count（number）、capability（number）、growth_rate（number）；9、sz_dist 元素含 district（string）、org_count（number）；10、responseFields 另有 sampleResponse 未给示例的 org_total（object）、pt_global_total（object）、org_new_count（array）、pt_type_dist（array）、pt_region（array）、pt_scale_dist（array）、pt_sz_total（object）、pt_sz_type_dist（array）、pt_sz_region（array）、sz_compare（object），非空载荷中应出现这些键；11、结构与 sampleResponse 一致（示例 layout：service_type FINANCE/IP/HR/MKT/CONSULT/INNOV，industry_field 金融服务/知识产权服务/人力资源服务/市场营销服务/咨询服务/科技创新服务，org_count 48/41/36/33/27/22，growth_rate 8.2/6.1/4.5/9.0/3.2/5.4；global：country 广东/北京/上海/浙江，org_count 86/52/41/28；invest：stat_year 2022/2023/2024，amount 9100/10500/12800；invest_events：南山科技金融站/芯联微电子/集成电路/3200/2024-03-12，知产服务中心/蓝海生物/生物医药/1800/2024-05-08；new：stat_year 2022/2023/2024，org_count 24/31/36，growth_rate 33.3/29.2/16.1；sz_scale：org_count 84、capability 73.2、growth_rate 6.8；sz_dist：district 南山/福田/宝安/龙岗，org_count 28/18/14/12） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INDUSTRY_LAYOUT | INTEG |  |  | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 场景=主流程 组合=ALL-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00081 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 服务机构基础指标（全维度） | 验证服务机构基础指标（全维度）功能，检查不传 kind 后仍返回全维度指标结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构基础指标（全维度）」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板的 data 为对象；2、仍含 layout、global、invest、invest_events、new、sz_scale、sz_dist（array）；3、layout 元素仍含 service_type（string）、industry_field（string）、org_count（number）、growth_rate（number）；4、global 元素仍含 country（string）、org_count（number）；5、invest 元素仍含 stat_year（number）、amount（number）；6、invest_events 元素仍含 org_name（string）、investee（string）、domain（string）、amount（number）、event_time（string）；7、new 元素仍含 stat_year（number）、org_count（number）、growth_rate（number）；8、sz_scale 元素仍含 org_count（number）、capability（number）、growth_rate（number）；9、sz_dist 元素仍含 district（string）、org_count（number）；10、responseFields 另列的 org_total、pt_global_total、org_new_count、pt_type_dist、pt_region、pt_scale_dist、pt_sz_total、pt_sz_type_dist、pt_sz_region、sz_compare 在非空载荷中仍应出现；11、结构与 sampleResponse 同类（示例取值同全维度 sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INDUSTRY_LAYOUT | INTEG |  |  | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 场景=备选-参数组合 组合=ALL-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00082 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 服务机构基础指标（全维度） | 验证服务机构基础指标（全维度）功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「服务机构基础指标（全维度）」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 layout、global、invest、invest_events、new、sz_scale、sz_dist 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | endpoint_id=svc.basic.indicators catalog_page_id=svc.basic 场景=异常-入参-非法kind 组合=ALL-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00083 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 全球服务机构产业布局 | 验证全球服务机构产业布局功能，检查填写 kind=layout调用后返回 layout 产业布局字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=layout | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「全球服务机构产业布局」；4.填写 kind=layout，点击调用 | 1、返回面板的 data 为对象；2、含 layout（array，responseFields A1 产业布局）；3、元素含 service_type（string）、industry_field（string）、org_count（number）、growth_rate（number）；4、结构与 sampleResponse 一致（示例 service_type FINANCE/IP/HR/MKT/CONSULT/INNOV，industry_field 金融服务/知识产权服务/人力资源服务/市场营销服务/咨询服务/科技创新服务，org_count 48/41/36/33/27/22，growth_rate 8.2/6.1/4.5/9.0/3.2/5.4） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INDUSTRY_LAYOUT | INTEG |  |  | endpoint_id=svc.basic.indicators-layout catalog_page_id=svc.basic 场景=主流程 组合=LAY-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00084 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 全球服务机构产业布局 | 验证全球服务机构产业布局功能，检查不传 kind 后仍返回 layout 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「全球服务机构产业布局」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板的 data 为对象；2、仍含 layout（array）；3、元素仍含 service_type（string）、industry_field（string）、org_count（number）、growth_rate（number）；4、结构与 sampleResponse 同类（示例取值同 layout sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INDUSTRY_LAYOUT | INTEG |  |  | endpoint_id=svc.basic.indicators-layout catalog_page_id=svc.basic 场景=备选-参数组合 组合=LAY-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00085 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 全球服务机构产业布局 | 验证全球服务机构产业布局功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「全球服务机构产业布局」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 service_type、industry_field、org_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | endpoint_id=svc.basic.indicators-layout catalog_page_id=svc.basic 场景=异常-入参-非法kind 组合=LAY-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00086 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 全球服务机构分布 | 验证全球服务机构分布功能，检查填写 kind=global调用后返回 global 分布字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=global | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「全球服务机构分布」；4.填写 kind=global，点击调用 | 1、返回面板的 data 为对象；2、含 global（array，responseFields A2 全球/地区分布）；3、元素含 country（string）、org_count（number）；4、结构与 sampleResponse 一致（示例 country 广东/北京/上海/浙江，org_count 86/52/41/28） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_ORG_CNT | INTEG |  |  | endpoint_id=svc.basic.indicators-global catalog_page_id=svc.basic 场景=主流程 组合=GLO-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00087 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 全球服务机构分布 | 验证全球服务机构分布功能，检查不传 kind 后仍返回 global 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「全球服务机构分布」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板的 data 为对象；2、仍含 global（array）；3、元素仍含 country（string）、org_count（number）；4、结构与 sampleResponse 同类（示例取值同 global sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_ORG_CNT | INTEG |  |  | endpoint_id=svc.basic.indicators-global catalog_page_id=svc.basic 场景=备选-参数组合 组合=GLO-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00088 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 全球服务机构分布 | 验证全球服务机构分布功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「全球服务机构分布」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 country、org_count 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | endpoint_id=svc.basic.indicators-global catalog_page_id=svc.basic 场景=异常-入参-非法kind 组合=GLO-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00089 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 投融资动态资讯 | 验证投融资动态资讯功能，检查填写 kind=invest调用后返回 invest 与 invest_events 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=invest | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「投融资动态资讯」；4.填写 kind=invest，点击调用 | 1、返回面板的 data 为对象；2、含 invest（array，responseFields A3 投融资）、invest_events（array，出现在 sampleResponse）；3、invest 元素含 stat_year（number）、amount（number）；4、invest_events 元素含 org_name（string）、investee（string）、domain（string）、amount（number）、event_time（string）；5、结构与 sampleResponse 一致（示例 invest：stat_year 2022/2023/2024，amount 9100/10500/12800；invest_events：南山科技金融站/芯联微电子/集成电路/3200/2024-03-12，知产服务中心/蓝海生物/生物医药/1800/2024-05-08） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INVEST_Y | INTEG |  |  | endpoint_id=svc.basic.indicators-invest catalog_page_id=svc.basic 场景=主流程 组合=INV-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00090 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 投融资动态资讯 | 验证投融资动态资讯功能，检查不传 kind 后仍返回投融资结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「投融资动态资讯」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板的 data 为对象；2、仍含 invest、invest_events（array）；3、invest 元素仍含 stat_year（number）、amount（number）；4、invest_events 元素仍含 org_name（string）、investee（string）、domain（string）、amount（number）、event_time（string）；5、结构与 sampleResponse 同类（示例取值同 invest sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_INVEST_Y | INTEG |  |  | endpoint_id=svc.basic.indicators-invest catalog_page_id=svc.basic 场景=备选-参数组合 组合=INV-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00091 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 投融资动态资讯 | 验证投融资动态资讯功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「投融资动态资讯」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 stat_year、amount、invest_events 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | endpoint_id=svc.basic.indicators-invest catalog_page_id=svc.basic 场景=异常-入参-非法kind 组合=INV-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00092 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 新增服务机构动态 | 验证新增服务机构动态功能，检查填写 kind=new调用后返回 new 新增动态字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=new | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「新增服务机构动态」；4.填写 kind=new，点击调用 | 1、返回面板的 data 为对象；2、含 new（array，responseFields A4 新增机构）；3、元素含 stat_year（number）、org_count（number）、growth_rate（number）；4、结构与 sampleResponse 一致（示例 stat_year 2022/2023/2024，org_count 24/31/36，growth_rate 33.3/29.2/16.1） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_NEW_CNT | INTEG |  |  | endpoint_id=svc.basic.indicators-new catalog_page_id=svc.basic 场景=主流程 组合=NEW-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00093 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 新增服务机构动态 | 验证新增服务机构动态功能，检查不传 kind 后仍返回 new 结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「新增服务机构动态」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板的 data 为对象；2、仍含 new（array）；3、元素仍含 stat_year（number）、org_count（number）、growth_rate（number）；4、结构与 sampleResponse 同类（示例取值同 new sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_NEW_CNT | INTEG |  |  | endpoint_id=svc.basic.indicators-new catalog_page_id=svc.basic 场景=备选-参数组合 组合=NEW-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00094 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 新增服务机构动态 | 验证新增服务机构动态功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「新增服务机构动态」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 stat_year、org_count、growth_rate 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | endpoint_id=svc.basic.indicators-new catalog_page_id=svc.basic 场景=异常-入参-非法kind 组合=NEW-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00095 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 深圳服务机构规模及分布 | 验证深圳服务机构规模及分布功能，检查填写 kind=sz调用后返回 sz_scale、sz_dist 字段 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind=sz | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「深圳服务机构规模及分布」；4.填写 kind=sz，点击调用 | 1、返回面板的 data 为对象；2、含 sz_scale（array，responseFields A5 深圳规模）、sz_dist（array，responseFields A6 深圳分布）；3、sz_scale 元素含 org_count（number）、capability（number）、growth_rate（number）；4、sz_dist 元素含 district（string）、org_count（number）；5、结构与 sampleResponse 一致（示例 sz_scale：org_count 84、capability 73.2、growth_rate 6.8；sz_dist：district 南山/福田/宝安/龙岗，org_count 28/18/14/12） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_SZ_SCALE | INTEG |  |  | endpoint_id=svc.basic.indicators-sz catalog_page_id=svc.basic 场景=主流程 组合=SZ-01 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00096 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 深圳服务机构规模及分布 | 验证深圳服务机构规模及分布功能，检查不传 kind 后仍返回深圳规模与分布结构 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、不传 kind | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「深圳服务机构规模及分布」；4.不传 kind，点击调用（不传 kind），点击调用 | 1、返回面板的 data 为对象；2、仍含 sz_scale、sz_dist（array）；3、sz_scale 元素仍含 org_count（number）、capability（number）、growth_rate（number）；4、sz_dist 元素仍含 district（string）、org_count（number）；5、结构与 sampleResponse 同类（示例取值同 sz sampleResponse） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators | M_SVC_SZ_SCALE | INTEG |  |  | endpoint_id=svc.basic.indicators-sz catalog_page_id=svc.basic 场景=备选-参数组合 组合=SZ-02 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00097 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 深圳服务机构规模及分布 | 验证深圳服务机构规模及分布功能，检查 kind 非法时返回指出该参数的错误说明 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/；2、kind 取文档枚举外的值 | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.接口下拉选择「深圳服务机构规模及分布」；4.填写 kind=__invalid__，点击调用 | 1、返回面板的 message 或 msg 指出 kind 非法；2、不返回含 sz_scale、sz_dist 的成功业务 data | P1 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | endpoint_id=svc.basic.indicators-sz catalog_page_id=svc.basic 场景=异常-入参-非法kind 组合=SZ-03 catalog_status=unavailable 文档标记未交付 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00098 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 接口信息 | 验证服务机构基础指标的接口信息功能，检查接口数量、名称和 URL 与文档一致，且切换接口后信息正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.下拉切换至「全球服务机构产业布局」 | 1、页头「N 个接口」的 N 与下拉项数均为 6；2、下拉名称依次为附录 B 六个 title；3、切换前后概览区的 method、path 与所选接口 catalog 一致；4、切换后参数表与示例区正常刷新（不逐字段核对 params、responseFields、sampleResponse）；1、确认处于「接口信息」tab；2、核对页头接口数量为 6、下拉项数为 6 且名称与附录 B 各 title 一致；3、核对默认选中项的概览标题、method（GET）、path（/entan/v1/svc/indicators）对应当前接口 | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | catalog_page_id=svc.basic 场景=接口信息-清单 |
| ZNFWJQ-SDWJSF/KJZTFWSFK-v1.0-FUNC-00099 | 算法工具库 | 科技专题服务算法库 | 基础指标分析模型 | 服务机构基础指标模型构建 | 服务机构基础指标 | 算法测试 | 验证服务机构基础指标的算法测试功能，检查下拉与调用区 method、path 随接口切换正常刷新 | 1、已登录联调台 https://edu.itic-sci.com/dma/algovwz/ | 1.侧栏进入「基础指标」→「服务机构基础指标」；2.切换至「算法测试」tab；3.下拉切换至「投融资动态资讯」 | 1、算法测试 tab 下拉数量与名称与接口信息 tab、catalog 一致（6 项）；2、切换接口后调用区 method、path 变为所选接口；3、请求参数区正常刷新；4、未点击调用时不校验返回字段；1、核对下拉项数与名称同「接口信息」tab 及附录 B；2、核对当前选中接口在调用区展示的 method（GET）、path（/entan/v1/svc/indicators） | P0 |  |  |  |  |  | N/A-技术项 | N/A | 科技专题服务算法库.md | N/A | N/A-技术项 | N/A | /entan/v1/svc/indicators |  | INTEG |  |  | catalog_page_id=svc.basic 场景=算法测试-清单 |
---

## 附录 A

> 参数赋值已展开至步骤/前置；本表仅作编写对照。
 · 入参组合

| 组合 id | endpoint_id | 参数赋值 | 意图 |
|---------|-------------|----------|------|
| ALL-01 | svc.basic.indicators | kind=all | 主路径（sampleRequest） |
| ALL-02 | svc.basic.indicators | 不传 kind | 省略可选 kind（与 sample 相反） |
| ALL-03 | svc.basic.indicators | kind=__invalid__ | 非法 kind |
| LAY-01 | svc.basic.indicators-layout | kind=layout | 主路径（sampleRequest） |
| LAY-02 | svc.basic.indicators-layout | 不传 kind | 省略可选 kind（与 sample 相反） |
| LAY-03 | svc.basic.indicators-layout | kind=__invalid__ | 非法 kind |
| GLO-01 | svc.basic.indicators-global | kind=global | 主路径（sampleRequest） |
| GLO-02 | svc.basic.indicators-global | 不传 kind | 省略可选 kind（与 sample 相反） |
| GLO-03 | svc.basic.indicators-global | kind=__invalid__ | 非法 kind |
| INV-01 | svc.basic.indicators-invest | kind=invest | 主路径（sampleRequest） |
| INV-02 | svc.basic.indicators-invest | 不传 kind | 省略可选 kind（与 sample 相反） |
| INV-03 | svc.basic.indicators-invest | kind=__invalid__ | 非法 kind |
| NEW-01 | svc.basic.indicators-new | kind=new | 主路径（sampleRequest） |
| NEW-02 | svc.basic.indicators-new | 不传 kind | 省略可选 kind（与 sample 相反） |
| NEW-03 | svc.basic.indicators-new | kind=__invalid__ | 非法 kind |
| SZ-01 | svc.basic.indicators-sz | kind=sz | 主路径（sampleRequest） |
| SZ-02 | svc.basic.indicators-sz | 不传 kind | 省略可选 kind（与 sample 相反） |
| SZ-03 | svc.basic.indicators-sz | kind=__invalid__ | 非法 kind |

---

## 附录 B · 本页 endpoint 清单

| title | endpoint_id | METHOD | path | 参数 | status |
|-------|-------------|--------|------|------|--------|
| 服务机构基础指标（全维度） | svc.basic.indicators | GET | /entan/v1/svc/indicators | kind? | unavailable |
| 全球服务机构产业布局 | svc.basic.indicators-layout | GET | /entan/v1/svc/indicators | kind? | unavailable |
| 全球服务机构分布 | svc.basic.indicators-global | GET | /entan/v1/svc/indicators | kind? | unavailable |
| 投融资动态资讯 | svc.basic.indicators-invest | GET | /entan/v1/svc/indicators | kind? | unavailable |
| 新增服务机构动态 | svc.basic.indicators-new | GET | /entan/v1/svc/indicators | kind? | unavailable |
| 深圳服务机构规模及分布 | svc.basic.indicators-sz | GET | /entan/v1/svc/indicators | kind? | unavailable |

---

## 2. endpoint → 用例简表

| endpoint_id | 用例编号 |
|-------------|----------|
| svc.basic.indicators | FUNC-00080、00081、00082 |
| svc.basic.indicators-layout | FUNC-00083、00084、00085 |
| svc.basic.indicators-global | FUNC-00086、00087、00088 |
| svc.basic.indicators-invest | FUNC-00089、00090、00091 |
| svc.basic.indicators-new | FUNC-00092、00093、00094 |
| svc.basic.indicators-sz | FUNC-00095、00096、00097 |
| （页面清单） | FUNC-00098、00099 |

---

## 3. 覆盖自检（第三轮口径）

- [x] 6 个 title 均在功能点列出现且各有 ≥1 条 `场景=主流程`
- [x] 仅可选 kind 的接口各 3 条（sampleRequest 主流程 + 省略 kind 备选 + 非法 kind 反向）
- [x] 步骤均为联调台侧栏/下拉/填参/点击调用；0 条 GET/POST 步骤
- [x] 模块列：算法工具库 / 科技专题服务算法库 / 基础指标分析模型 / 服务机构基础指标模型构建
- [x] 测试内容均含「验证」与「检查」
- [x] 清单 2 条：`场景=接口信息-清单`、`场景=算法测试-清单`
- [x] unavailable 仍按 catalog sampleResponse 写主流程与备选，备注注明未交付
- [x] 无鉴权 / Token / 401 / 424 / 契约占位 / 纯 HTTP 4xx 预期
- [x] `coverage-fp.md` 已同步 FUNC-00080～00099

**统计**：用例 **20** 条（主流程 **6**、备选 **6**、反向 **6**、清单 **2**）；编号闭区间 **FUNC-00080**～**FUNC-00099**（父控 R3-批1 分配）。
