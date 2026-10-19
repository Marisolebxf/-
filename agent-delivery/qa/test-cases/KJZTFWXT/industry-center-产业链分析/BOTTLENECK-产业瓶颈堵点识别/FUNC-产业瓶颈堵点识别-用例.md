# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md`  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v3.0 · 2026-10-18（对照重写）  
> **模块**：产业瓶颈堵点识别（catalog `chain-bottleneck`）  
> **金样**：仅 `ZNFWJQ-KJZTFWXT-v1.0-FUNC-03188`（复制已完成配置 → 开始分析 → 查看分析结果 → 结果页）  
> **入口**：产业链分析 → 产业瓶颈堵点识别  
> **路由**：`/industry-center/diagnosis?workspace=bottleneck&tab=bottleneck`  
> **环境**：http://111.198.38.90:50892/ · 账号 `admin` / `123456`  
> **保留旧号**：00605。00607、00608、00622、00624 删除且不复用。其余 00601–00625 作废，由 03188–03227 重写。  
> **本段用到的最大号**：03228（号段 03228–03287，03229–03287 未使用）  
> **交付口径**：INTEG  
> **关联任务**：`QA-KJZTFWXT-BLINE-CASE-IND-L01`

## 关评审控件清单

| 格 | 结论 |
|----|------|
| 入口 A · 筛选条件到成功结果 | 03188 金样。默认条件下直接点「开始分析」到不了结果，见 03223 |
| 入口 B · 已选对象 | 无。本页没有对象名单，对比篮不在本页发起 |
| 任务列表 | 诊断记录。列与行操作见 03199、03208、03209、03213–03219、03225–03227 |
| 结果页 | 03188 到达后的检查见 03200–03207 |
| 摘要 · 标题 / 任务 / 对象 | 03200 |
| 摘要 · 瓶颈堵点数 | 03201 |
| 摘要 · 瓶颈严重度 | 03201 |
| 摘要 · 时间 / 权重 | 无。结果页没有这两项 |
| 筛选下拉 | 无。结果页没有筛选下拉 |
| 开始分析 · 当天 | 03220。现场未打开已有结果，预期仍按打开已有结果写，差异在备注 |
| 工具 · 重新分析 | 03228。复制已完成配置后点「重新分析」，进入生成过程并打开新结果 |
| 工具 · 回到配置 | 03207「按此配置新建分析」。没有名为「调整条件」的按钮 |
| 工具 · 结果搜索 | 无 |
| 表 · 列 / 翻页 / 勾选 / 行按钮 | 无。结果是环节图谱，不是表 |
| 详情 · 环节详情 | 03203、03204。区块标题为「环节详情」 |
| 二级 | 无 |
| 报告 · 查看 | 03205、03206、03221 |
| 报告 · 下载 | 03225。点已完成行的「下载报告」得到失败提示 |
| 报告 · 生成中 | 无。没有单独的生成中页面 |
| 入池 | 无 |
| 入口 B 各格 | 无 |
| 过程页阶段 | 03198 |
| 过程页 · 查看分析记录 | 03199 |
| 过程页 · 取消任务 | 未覆盖：任务完成后过程页只有「查看分析记录」「查看分析结果」，没有「取消任务」。本次任务在打开过程页时已经结束，造不出进行中的取消 |
| 配置 · 集群 / 产业 / 所属产业链 | 03191、03192、03193、03210 |
| 配置 · 维度名称 | 00605 |
| 配置 · 权重与合计 | 03194 |
| 配置 · 表头 / 来源 / 查看 | 03195、03196、03197 |
| 配置 · 选择列 | 03222 |
| 配置 · 重置参数 | 03211 |
| 配置 · 空产业链不能开始 | 03224 |
| 诊断记录 · 删除取消 / 确定 | 03218、03219 |
| 诊断记录 · 失败行 | 03226 |
| 诊断记录 · 分析中空列表 | 03227 |

---

## 1. 用例总表

> 排列：主流程 → 备选 → 异常。00605 保留原编号，插在主流程配置段。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03188 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-完成一次分析 | 复制配置后看到结果 | 产业瓶颈堵点识别 | 开始分析直到结果页 | 复制已完成任务的配置后开始分析，并打开成功结果页 | 1、已登录；2、诊断记录里至少有一条已完成任务 | 1.切到「诊断记录」；2.对一条已完成任务点「复制配置」；3.点「开始分析」；4.点「查看分析结果」 | 1、进入「产业瓶颈堵点识别生成中」过程页；2、过程页出现「分析结果已生成」；3、结果页标题为「产业瓶颈堵点识别结果」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈堵点识别｜完成分析看到结果 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 金样。默认条件下直接点「开始分析」到不了这一步，见 03223 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03189 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-入口 | 页标题与页签 | 产业瓶颈堵点识别 | 进入本页 | 进入产业瓶颈堵点识别后标题和两个页签正确 | 1、已登录 | 1.在左侧「产业链分析」中点「产业瓶颈堵点识别」 | 1、页标题为「产业瓶颈堵点识别」；2、页签为「产业瓶颈堵点识别」（选中）与「诊断记录」；3、地址含 workspace=bottleneck 与 tab=bottleneck | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜进入分析页 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03190 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 配置区构成 | 产业瓶颈堵点识别 | 分析配置区 | 分析配置区展示对象、维度表和两个操作按钮 | 1、已打开产业瓶颈堵点识别页 | 1.停留在「产业瓶颈堵点识别」页签 | 1、可见「分析配置」「分析对象」「所属产业链」「注册诊断维度」；2、可见「重置参数」与「开始分析」；3、维度表上方有「以下指标只读，确认后即可生成分析。」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜展示分析配置 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03191 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 集群下拉 | 产业瓶颈堵点识别 | 分析对象集群 | 分析对象左侧下拉给出 15 个产业集群 | 1、已打开默认分析配置 | 1.展开「分析对象」下左侧下拉 | 1、选项共 15 个，名称见附录A | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜选择集群 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 默认展示「新一代信息技术」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03192 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 产业下拉 | 产业瓶颈堵点识别 | 分析对象产业 | 当前集群下的产业下拉给出 7 个选项 | 1、已打开默认分析配置；2、左侧仍为「新一代信息技术」 | 1.展开「分析对象」下右侧下拉 | 1、选项共 7 个，名称见附录A | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜选择产业 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 默认展示「新一代信息技术」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03193 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 所属产业链下拉 | 产业瓶颈堵点识别 | 所属产业链 | 所属产业链下拉给出 6 个选项 | 1、已打开默认分析配置 | 1.展开「所属产业链」 | 1、选项共 6 个，名称见附录A | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜选择产业链 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 默认展示「半导体与集成电路」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00605 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置区 | 五维名称与资本口径 | 产业瓶颈堵点识别 | 五维度名称核对 | 五个维度名称与注册口径一致，第四维用「资本」且不拆第六维 | 1、已进入产业瓶颈堵点识别页 | 1.逐行读取维度名称 | 1、五个维度名称为技术、人才、市场需求、资本、政策；2、「资本」为独立维名，不出现「资金」拆出的第六维 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜提供技术成熟度指标 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-08 | 保留原号。现场五行名称与本预期一致 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03194 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 权重只读 | 产业瓶颈堵点识别 | 五维权重 | 五个维度权重只读且合计通过校验 | 1、已打开分析配置 | 1.看权重列；2.点某一权重的增减按钮 | 1、五行权重均为 20%；2、增减无效，数值仍为 20%；3、页脚为「权重合计：100% · 校验通过」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜展示权重 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03195 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 维度表表头 | 产业瓶颈堵点识别 | 注册诊断维度表 | 注册诊断维度表的列名完整 | 1、已打开分析配置 | 1.打开「注册诊断维度」表 | 1、表头为选择、指标名称、分组 / 维度、数据状态、权重、数据来源、指标说明 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜展示维度表 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03196 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 状态与数据来源 | 产业瓶颈堵点识别 | 维度行来源 | 五个维度的分组、状态和数据来源与表内原文一致 | 1、已打开分析配置 | 1.逐行看分组、数据状态和数据来源 | 1、分组 / 维度均为「五维诊断维度」；2、数据状态均为「可用」；3、数据来源依次为技术供给快照、人才供给快照、需求景气快照、融资与投入快照、政策覆盖快照 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜展示数据来源 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03197 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-分析配置 | 指标说明 | 产业瓶颈堵点识别 | 查看说明 | 「查看」打开该行指标说明并可关闭 | 1、已打开分析配置 | 1.点「技术」行的「查看」；2.关闭说明 | 1、抽屉标题为「技术 · 指标说明」；2、当前输入为 20%；3、关闭后不再显示该抽屉 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜查看维度说明 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 同屏还有指标来源「平台注册因子/维度（只读冻结）」、指标状态「固定演示配置」、阈值状态「正式口径待闭合」、版本「五维诊断配置 · 演示版」、支撑指标「技术成熟度、关键设备可得性、材料替代能力」。说明正文写识别核心技术、设备和材料约束 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03198 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-过程页 | 五个阶段 | 产业瓶颈堵点识别 | 分析过程 | 分析过程展示五个阶段且不自动进入结果页 | 1、已对一条已完成任务点过「复制配置」 | 1.点「开始分析」 | 1、五个阶段名称见附录B，结束时均为已完成；2、出现「分析结果已生成」；3、页面不自动改为结果页 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜展示计算过程 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 完成后按钮为「查看分析记录」「查看分析结果」。提示写明不会自动跳转 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03199 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-过程页 | 查看分析记录 | 产业瓶颈堵点识别 | 从过程页看记录 | 过程页「查看分析记录」进入诊断记录 | 1、过程页已出现「分析结果已生成」 | 1.点「查看分析记录」 | 1、页签切到「诊断记录」；2、列表含任务、类型、状态、创建时间、操作 | P0 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜从过程页进入 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03200 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-结果页 | 结果抬头 | 产业瓶颈堵点识别 | 结果摘要 | 结果页展示标题、任务、对象和降级说明 | 1、过程页已出现「查看分析结果」 | 1.点「查看分析结果」 | 1、区块标题为「产业瓶颈堵点识别结果」；2、可见「任务」与「任务 ID」；3、可见「分析对象」；4、可见「叙述能力不可用，已按规则结果诚实降级。」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈智能识别｜展示结果抬头 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 结构性检查 4 点。分析对象以「/」连接展示 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03201 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-结果页 | 两项摘要 | 产业瓶颈堵点识别 | 瓶颈摘要 | 结果页展示瓶颈堵点数和瓶颈严重度 | 1、已打开一条结果页 | 1.看结果页上的两张摘要卡 | 1、可见「瓶颈堵点数」；2、可见「瓶颈严重度」；3、两项均有文字，为数字或「暂无」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈智能识别｜展示堵点摘要 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 不同任务一个可为数字、一个可为「暂无」，两种都算有文字 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03202 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-结果页 | 健康图谱 | 产业瓶颈堵点识别 | 环节图谱 | 结果图谱给出健康分档图例和五个环节 | 1、已打开一条结果页 | 1.看「多维度瓶颈综合分析」 | 1、图例为「健康分档」，含稳健、关注、薄弱；2、环节为研发、设计、制造、销售、服务 | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜展示环节健康度 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 各环节旁有「健康度」。没有排序开关 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03203 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-结果页 | 环节详情 | 产业瓶颈堵点识别 | 点选环节 | 点选环节后详情标题改为该环节 | 1、已打开一条结果页 | 1.在图谱上点「设计」 | 1、「环节详情」中的名称变为「设计」；2、详情含「健康度」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜查看环节详情 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 区块标题为「环节详情」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03204 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-结果页 | 瓶颈标记 | 产业瓶颈堵点识别 | 已入选瓶颈 | 带瓶颈标记的环节在详情中标明已入选 | 1、有一条已完成任务，其图谱某环节带「瓶颈」 | 1.对该任务点「查看结果」；2.点带「瓶颈」的环节 | 1、「环节详情」出现「已入选瓶颈清单」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈智能识别｜展示已标记环节 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 现场曾在已完成任务的「研发」环节看到「瓶颈」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03205 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-报告 | 查看报告 | 产业瓶颈堵点识别 | 分析报告 | 「查看报告」打开本页报告并列出目录 | 1、已打开一条结果页 | 1.点「查看报告」 | 1、可见「产业瓶颈堵点识别报告」；2、目录 7 项名称见附录C | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈智能识别｜查看报告 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 页眉还有「产业链分析报告」和报告版本 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03206 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-报告 | 返回结果 | 产业瓶颈堵点识别 | 从报告返回 | 「返回分析结果」回到结果页 | 1、已打开报告页 | 1.点「返回分析结果」 | 1、回到标题为「产业瓶颈堵点识别结果」的页面 | P0 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈智能识别｜从报告返回 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03207 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-结果页 | 按此配置新建 | 产业瓶颈堵点识别 | 回到配置 | 「按此配置新建分析」回到分析配置 | 1、已打开一条结果页 | 1.点「按此配置新建分析」 | 1、回到「分析配置」；2、可见「开始分析」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜按结果回到配置 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 当天已有成功任务时，旁边还会出现「重新分析」。重新分析的终态见清单未覆盖 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03208 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-诊断记录 | 查看结果 | 产业瓶颈堵点识别 | 打开历史结果 | 诊断记录「查看结果」打开该条结果 | 1、诊断记录中有已完成任务 | 1.对一条已完成任务点「查看结果」 | 1、进入「产业瓶颈堵点识别结果」；2、任务 ID 与所点行一致 | P0 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜查看结果 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03209 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-诊断记录 | 复制配置 | 产业瓶颈堵点识别 | 复制历史配置 | 「复制配置」回到分析配置并提示已复制 | 1、诊断记录中有已完成任务 | 1.对一条已完成任务点「复制配置」 | 1、提示「已复制分析配置，可调整后重新分析」；2、页面回到「分析配置」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜复制配置 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 金样 03188 用这一步作为能发起分析的前置 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03228 | 产业链分析 | 产业瓶颈堵点识别 | 主流程-重新分析 | 到达新结果 | 产业瓶颈堵点识别 | 重新分析 | 点「重新分析」后进入新一轮分析并打开新结果页 | 1、已登录；2、已对一条已完成任务点「复制配置」；3、配置页可见「重新分析」 | 1.点「重新分析」；2.点「查看分析结果」 | 1、进入「产业瓶颈堵点识别生成中」；2、过程页出现「分析结果已生成」；3、结果页标题为「产业瓶颈堵点识别结果」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈堵点识别｜重新分析看到新结果 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 现场没有确认框。点击后提示「任务已创建，正在可视化展示分析过程」，诊断记录新增一条已完成任务。结果页任务与点击前不是同一条 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03210 | 产业链分析 | 产业瓶颈堵点识别 | 备选-分析配置 | 集群联动 | 产业瓶颈堵点识别 | 更换集群 | 更换集群后产业选项随之变化 | 1、已打开默认分析配置 | 1.把分析对象左侧下拉改为「生物产业」；2.展开右侧产业下拉 | 1、产业选项变为 3 个，名称见附录A；2、所属产业链已选文字被清空 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜集群联动产业 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 此时不点「开始分析」也不会新增任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03211 | 产业链分析 | 产业瓶颈堵点识别 | 备选-分析配置 | 重置参数 | 产业瓶颈堵点识别 | 重置 | 「重置参数」给出恢复提示且不发起分析 | 1、已把集群改为「生物产业」 | 1.点「重置参数」 | 1、提示「已恢复该分析类型的推荐配置」；2、仍停留在分析配置，不出现生成中页面 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜重置参数 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03212 | 产业链分析 | 产业瓶颈堵点识别 | 备选-页签 | 往返不发起 | 产业瓶颈堵点识别 | 页签往返 | 改过集群后往返页签不会发起分析 | 1、已打开分析配置 | 1.把左侧下拉改为「生物产业」；2.切到「诊断记录」；3.切回「产业瓶颈堵点识别」 | 1、切回后仍可见「分析配置」；2、不出现「产业瓶颈堵点识别生成中」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜页签往返 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03213 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 任务状态选项 | 产业瓶颈堵点识别 | 状态筛选 | 任务状态筛选列出四种状态 | 1、已打开「诊断记录」 | 1.展开「任务状态」 | 1、选项为全部状态、分析中、已完成、失败，共 4 个 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜状态选项 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 筛选项只有任务状态，没有对象或时间筛选 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03214 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 筛已完成 | 产业瓶颈堵点识别 | 已完成筛选 | 按已完成筛选后列表只剩已完成任务 | 1、已打开「诊断记录」 | 1.在任务状态中选「已完成」 | 1、列表中状态列均为「已完成」；2、类型列均为「产业瓶颈堵点识别」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜筛选已完成 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03215 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 重置筛选 | 产业瓶颈堵点识别 | 重置状态 | 「重置」把任务状态恢复为全部状态 | 1、已打开「诊断记录」 | 1.先选「失败」；2.点「重置」 | 1、任务状态显示「全部状态」；2、列表同时能看到已完成和失败 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜重置筛选 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03216 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 翻页 | 产业瓶颈堵点识别 | 第二页 | 诊断记录可以翻到第二页 | 1、每页为 10 条且总数大于 10 | 1.把每页条数设为「10 条/页」；2.点页码「2」 | 1、当前页为第 2 页；2、本页任务与第 1 页不是同一批 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜翻页 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 现场曾见共 15 条 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03217 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 每页条数 | 产业瓶颈堵点识别 | 页大小 | 每页条数可以改为 20 | 1、已打开「诊断记录」 | 1.展开每页条数；2.选「20 条/页」 | 1、选项含 10 条/页、20 条/页、50 条/页；2、选中后分页条显示「20 条/页」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜每页条数 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03218 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 删除取消 | 产业瓶颈堵点识别 | 取消删除 | 删除时点取消，该任务仍在列表 | 1、诊断记录中有任务 | 1.对一条任务点「删除」；2.在弹框点「取消」 | 1、弹框标题为「删除分析记录」；2、正文写明删除后列表不再显示；3、该任务行仍在 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜取消删除 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03219 | 产业链分析 | 产业瓶颈堵点识别 | 备选-诊断记录 | 删除确定 | 产业瓶颈堵点识别 | 确定删除 | 删除时点确定，该任务从列表消失 | 1、诊断记录中有一条失败任务 | 1.对一条失败任务点「删除」；2.在弹框点「确定」 | 1、提示「已删除」；2、该任务不再出现在当前列表 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜确定删除 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 用失败任务执行，避免删掉仅有的已完成样例 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03220 | 产业链分析 | 产业瓶颈堵点识别 | 备选-开始分析 | 当天再次开始 | 产业瓶颈堵点识别 | 当天复用结果 | 当天已成功后再点开始分析应打开已有结果 | 1、同一账号当天已有一条本页成功分析 | 1.回到分析配置；2.再点「开始分析」 | 1、打开已有结果页；2、诊断记录不新增任务 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜当天打开已有结果 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 现场点后提示「尚未选择分析对象」，未打开结果，也未新增任务。缺陷候选。预期仍按打开已有结果写 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03221 | 产业链分析 | 产业瓶颈堵点识别 | 备选-报告 | 导出不可用 | 产业瓶颈堵点识别 | 导出 | 报告页「导出」不可用 | 1、已打开报告页 | 1.看报告页右上角「导出」 | 1、「导出」为禁用，不能点出文件 | P1 |  |  |  |  |  | US-CHAIN-DIAG-06 | AC-US-CHAIN-DIAG-06-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜瓶颈智能识别｜导出报告 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 已完成任务的报告同样为禁用。按钮旁有「付费」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03222 | 产业链分析 | 产业瓶颈堵点识别 | 备选-分析配置 | 选择列禁用 | 产业瓶颈堵点识别 | 维度选择 | 维度表选择列不可改 | 1、已打开分析配置 | 1.点某一行的选择框 | 1、选择框保持禁用；2、五行选中状态不变 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜维度不可勾选 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03223 | 产业链分析 | 产业瓶颈堵点识别 | 异常-开始分析 | 未选对象 | 产业瓶颈堵点识别 | 默认不能发起 | 默认条件下点开始分析会提示未选对象 | 1、刚进入本页，未点「复制配置」 | 1.点「开始分析」 | 1、提示「尚未选择分析对象」；2、仍停在分析配置；3、诊断记录不新增任务 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜未选对象不可分析 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 下拉虽显示新一代信息技术 / 半导体与集成电路，仍出现该提示。改到「生物产业 / 生物医药与生命健康」后同样出现该提示 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03224 | 产业链分析 | 产业瓶颈堵点识别 | 异常-开始分析 | 产业链为空 | 产业瓶颈堵点识别 | 空产业链 | 所属产业链为空时不能开始分析 | 1、已打开分析配置 | 1.把集群改为「生物产业」 | 1、「开始分析」变为不可用 | P1 |  |  |  |  |  | US-CHAIN-DIAG-05 | AC-US-CHAIN-DIAG-05-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜多维度瓶颈综合分析｜无产业链不可分析 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 更换集群后所属产业链被清空 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03225 | 产业链分析 | 产业瓶颈堵点识别 | 异常-诊断记录 | 下载失败 | 产业瓶颈堵点识别 | 下载报告 | 下载报告在没有资产时给出失败提示 | 1、诊断记录中有已完成任务 | 1.对一条已完成任务点「下载报告」 | 1、提示「资产下载失败（HTTP 404）」；2、不打开新的报告页 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜下载报告 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03226 | 产业链分析 | 产业瓶颈堵点识别 | 异常-诊断记录 | 失败行不可看 | 产业瓶颈堵点识别 | 失败任务操作 | 失败任务不能查看结果、报告或下载 | 1、已打开「诊断记录」 | 1.把任务状态选为「失败」 | 1、「查看结果」为禁用；2、「查看报告」为禁用；3、「下载报告」为禁用 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜失败任务不可打开 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 「删除」仍可点，终态见 03218、03219 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03227 | 产业链分析 | 产业瓶颈堵点识别 | 异常-诊断记录 | 分析中空列表 | 产业瓶颈堵点识别 | 无进行中任务 | 筛选分析中且当前没有进行中任务时列表为空 | 1、当前没有进行中的本页任务 | 1.在任务状态中选「分析中」 | 1、列表显示「暂无数据」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.5 | T05｜诊断记录｜分析中空态 | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=bottleneck&tab=bottleneck |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 造不出长时间停留在分析中的任务，空列表即当前终态 |

---

## 2. 旧号处置

| 旧号 | 处置 | 新号 |
|------|------|------|
| 00601 | 作废。入口写成「产业运行诊断」，且不到结果页 | 03189 |
| 00602 | 作废。预期含现场没有的版本信息区 | 03190 |
| 00603 | 作废。对象写成产业 / INB1701 / 细分产业 | 03191、03192、03193 |
| 00604 | 作废。联动层级与现场下拉不符 | 03210、03212 |
| 00605 | 保留 | — |
| 00606 | 作废。把不可见标注写成了行上原文 | 03194、03222 |
| 00607 | 删除。用「没有某词」当验收 | — |
| 00608 | 删除。版本信息只在开关打开时出现 | — |
| 00609 | 作废。停在触发，没有成功结果 | 03188、03223 |
| 00610 | 作废。阶段原文与现场过程页不一致 | 03198 |
| 00611 | 作废。结果页没有「卡脖子环节数」 | 03200、03201 |
| 00612 | 作废。图谱结构按旧目标态写 | 03202 |
| 00613 | 作废。详情没有「是否瓶颈 / 是否卡脖子」两列 | 03204 |
| 00614 | 作废。结果页没有成因与改进建议 | 03203 |
| 00615 | 作废。结果页没有健康度排序 | 清单「表」为无 |
| 00616 | 作废。图例不是两行，且用禁词当验收 | 03202 |
| 00617 | 作废。只写打开说明，没有抽屉标题 | 03197 |
| 00618 | 作废。重置后的对象写回了 INB1701 | 03211 |
| 00619 | 作废。未按现场页签原文收口 | 03212 |
| 00620 | 作废。筛选项写成了对象、类型、时间 | 03213、03214、03215 |
| 00621 | 作废。恢复停在「不重建配置」 | 03208 |
| 00622 | 删除。版本快照只在开关打开时出现 | — |
| 00623 | 作废。本页没有周期 / 关键环节页签 | 清单不单列 |
| 00624 | 删除。整条都是开关与追溯 | — |
| 00625 | 作废。空对象终态与现场按钮禁用不符 | 03224 |

---

## 3. 覆盖自检

| 指标 | 数值 |
|------|------|
| 保留 | 1（00605） |
| 新号 | 03188–03228，共 41 |
| 删除不复用 | 00607、00608、00622、00624 |
| 作废 | 00601–00604、00606、00609–00621、00623、00625 |
| 主流程 | 24（03188–03209、03228 与 00605） |
| 备选 | 13（03210–03222） |
| 异常 | 5（03223–03227） |
| 主流程 ≥ 备选+异常 | 24 ≥ 18 |
| 金样 | 03188 |
| 预期 ≥6 点 | 0 |
| 预期 4 点 | 1（03200，结果抬头） |

红线 7：前置、步骤、预期、功能项中，开关名、人设入口、追溯挂件与泄漏字样命中 0。  
红线 2：未覆盖原因都是造不出终态或页面没有该控件。

---

### 附录A 下拉选项

**分析对象左侧（03191，15 个）**：新一代信息技术、生物产业、新能源、新材料、高端装备、智能网联新能源汽车、绿色环保、低空经济与空天、传统与创意产业、海洋产业、未来制造（智能机器人）、未来信息（光载信息、AI 底层生态）、未来能源、未来空间、未来健康（合成生物、细胞基因、脑机工程）。

**分析对象右侧，左侧为新一代信息技术时（03192，7 个）**：新一代信息技术、半导体与集成电路、人工智能与应用、智能终端、软件与信息服务、新型网络与通信、超高清视频与显示。

**所属产业链，默认条件下（03193，6 个）**：半导体与集成电路、人工智能与应用、新型网络与通信、超高清视频与显示、智能终端、软件与信息服务。

**左侧改为生物产业后的右侧（03210，3 个）**：生物、生物医药与生命健康、高端医疗器械。

### 附录B 过程阶段（03198）

1. 任务提交与产业链对象冻结  
2. 整合各环节技术/人才/资本/政策等时序数据  
3. 基于技术成熟度、人才供给量、融资事件、政策覆盖率计算环节健康度  
4. 瓶颈智能识别与卡脖子环节归因/改进建议生成  
5. 结果可信性校验与分析报告组装  

### 附录C 报告目录（03205）

01 报告身份、02 执行摘要、03 对象与范围、04 关键发现、05 证据与分析、06 数据来源与生成说明、07 局限性与使用边界。
