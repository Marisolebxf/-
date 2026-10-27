# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）
> **规范**：`agent-delivery/qa-test-case-spec.md`（编号与主表列）
> **测试类型**：FUNC
> **系统码**：KJZTFWXT
> **版本**：v3.0 · 2026-10-18（对照重写）
> **模块**：产业关键环节识别（catalog `chain-key-link`）
> **金样**：03088（只此一条：选齐对象后开始分析，直到成功结果页）
> **号段**：本册新号 03088–03135（父控段 03088–03187，用到的最大号 **03135**）
> **旧号**：00578–00600 全部退出本册正文。处置见文末「旧号处置」。00593 删除且不复用。
> **环境**：https://edu.itic-sci.com/tts/svcz/ · 已登录后从左侧「产业链分析」进入「产业关键环节识别」
> **路由**：`/industry-center/diagnosis?workspace=key_link&tab=key-link`
> **交付口径**：INTEG
> **自动化用例ID**：本步留空
> **维护**：agent:qa-agent

## 关评审控件清单

入口拓扑：

| 区域 | 现场 | 用例 |
| --- | --- | --- |
| 入口 A | 「分析配置」：分析对象两个下拉、所属产业链、注册识别因子；按钮「开始分析」 | 03088 |
| 入口 B | 无。本页没有对象名单，也不从名单发起 | 无 |
| 任务列表 | 页签「诊断记录」 | 03112 起 |
| 结果页 | 「产业关键环节识别结果」 | 03088 到达后的摘要与图谱各条 |

核心主线：

| 主线 | 用例 |
| --- | --- |
| 入口 A · 筛选条件 | 03088（金样）。步骤选齐三个下拉 →「开始分析」→「查看分析结果」→「产业关键环节识别结果」 |
| 入口 B · 已选对象 | 无 |

结果页（只写入口 A）：

| 格 | 用例或原因 |
| --- | --- |
| 摘要·任务号与任务 ID | 03088 |
| 摘要·分析对象与发起条件一致 | 03098 |
| 摘要·关键环节数 | 03099 |
| 摘要·市场规模 | 03100 |
| 摘要·投融资总额 | 03101 |
| 摘要·降级说明 | 03102 |
| 筛选下拉 | 无。结果页没有筛选下拉 |
| 开始分析·当天 | 03117 |
| 工具·重新分析 | 无。页上没有「重新分析」 |
| 工具·调整条件 | 03119「按此配置新建分析」：回到分析配置且对象仍在 |
| 工具·结果搜索 | 无 |
| 表·列 / 翻页 / 勾选 / 行按钮 | 无。结果不是表，是全链路图 |
| 详情·环节详情 | 03106。区块标题「环节详情」，文案「该环节暂无详情说明」 |
| 详情·代表企业 | 03107。标题「代表企业」 |
| 详情·企业画像 | 03108。标题「企业画像」 |
| 图例 | 03105「关键环节」「皇冠明珠」 |
| 高亮节点 | 未覆盖：成功结果的关键环节数为 0，图上没有被标成关键环节或皇冠明珠的节点，造不出高亮终态 |
| 排序 | 无。没有升序或降序控件 |
| 二级 | 无。代表企业为空，没有下一级入口 |
| 报告·查看 | 03109（结果页）、03128（诊断记录） |
| 报告·目录 | 03109，七节见附录D |
| 报告·返回 | 03120 |
| 报告·生成中 | 未覆盖：已完成任务打开报告时已是成稿，造不出报告生成中 |
| 报告·导出 | 03135。按钮不可点击 |
| 报告·下载 | 03134。提示失败，文件未落地 |
| 入池 | 无 |

入口 B 各格：无。

任务列表 × 入口 A（入口 B 无，不单列）：

| 格 | 用例 |
| --- | --- |
| 列：任务、类型、状态、创建时间、操作 | 03112 |
| 查看结果 | 03113 |
| 复制配置 | 03118；失败行 03123 |
| 查看报告 | 03128 |
| 下载报告 | 03134 |
| 删除·取消 | 03132 |
| 删除·确定 | 03133 |
| 任务状态 4 项 | 03121 |
| 筛选失败 | 03122 |
| 失败行不可打开结果和报告 | 03131 |
| 筛选重置 | 03124 |
| 翻页 | 03125 |
| 每页条数 | 03126 |
| 筛选分析中 | 03127 |
| 生成页五阶段 | 03110 |
| 查看分析记录 | 03111 |

配置区：

| 格 | 用例 |
| --- | --- |
| 第一个下拉 15 项 | 03090，附录A |
| 第二个下拉初始 7 项 | 03091，附录B |
| 所属产业链初始 6 项 | 03092，附录C |
| 选新能源后的下级个数 | 03114 |
| 改选生物产业后清空下级 | 03115 |
| 注册识别因子三行 | 03093 |
| 权重只读与合计 | 03094 |
| 指标说明·附加值率 / 技术壁垒 / 市场集中度 | 03095 / 03096 / 03097 |
| 重置参数 | 03116 |
| 未点选就开始分析 | 03129 |
| 产业链为空不能开始 | 03130 |
| 清空按钮 | 无。下拉没有清空控件 |
| 配置页版本四项 | 无。版本语句在指标说明抽屉内，不单列 |

## 页面区块 → 用例

| 区块 | 用例 |
| --- | --- |
| 菜单进入与双页签 | 03089 |
| 分析对象与所属产业链 | 03090、03091、03092、03114、03115、03129、03130 |
| 注册识别因子 | 03093、03094、03095、03096、03097、03116 |
| 开始分析 / 生成页 / 当天 | 03088、03110、03111、03117 |
| 结果摘要与全链路 | 03098–03108 |
| 报告 | 03109、03120、03128、03134、03135 |
| 诊断记录 | 03112、03113、03118、03121–03128、03131–03133 |

## 1. 用例总表

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03088 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 开始分析得到结果 | 选齐分析对象后开始分析，检查并进入成功结果页 | 1、已登录；2、已进入产业关键环节识别；3、当天尚未用「新能源 / 新能源 / 新能源」成功分析过 | 1.在「分析对象」第一个下拉选择「新能源」；2.在第二个下拉选择「新能源」；3.在「所属产业链」选择「新能源」；4.点击「开始分析」；5.点击「查看分析结果」 | 1、页面出现「产业关键环节识别结果」；2、任务号与任务 ID 为同一编号 | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-发起分析 / 开始分析到结果；金样；入口 A 主线 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03089 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 进入本页 | 验证从菜单进入后页标题、页签和地址正确 | 1、已登录 | 1.点击左侧「产业链分析」；2.点击「产业关键环节识别」 | 1、页标题为「产业关键环节识别」；2、页签「产业关键环节识别」为选中；3、地址路径为 /industry-center/diagnosis；4、地址参数含 workspace=key_link 与 tab=key-link | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-入口 / 页签与地址；4 点为入口结构例外 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03090 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 分析对象选项 | 验证分析对象第一个下拉的选项个数 | 1、已进入产业关键环节识别 | 1.展开「分析对象」第一个下拉 | 1、选项共 15 个（名称见附录A） | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析对象 / 第一个下拉选项 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03091 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 分析对象选项 | 验证初始展示下第二个下拉的选项个数 | 1、已进入本页；2、第一个下拉仍显示「新一代信息技术」 | 1.展开「分析对象」第二个下拉 | 1、选项共 7 个（名称见附录B） | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析对象 / 第二个下拉选项 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03092 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 所属产业链选项 | 验证初始展示下所属产业链的选项个数 | 1、已进入本页；2、第二个下拉仍显示「新一代信息技术」 | 1.展开「所属产业链」 | 1、选项共 6 个（名称见附录C） | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-所属产业链 / 产业链选项 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03093 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 注册识别因子 | 验证注册识别因子表的三行名称、分组和数据状态 | 1、已进入本页 | 1.定位「注册识别因子」表 | 1、指标为附加值率、技术壁垒、市场集中度；2、分组均为「关键环节识别因子」；3、数据状态均为「可用」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-注册识别因子 / 三行指标 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03094 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 权重只读 | 权重与行首选择不可改，检查且合计通过 | 1、已进入本页 | 1.点击权重加减钮；2.点击行首选择框 | 1、权重依次为 34%、33%、33%；2、权重与行首选择均不能改；3、显示「权重合计：100% · 校验通过」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-注册识别因子 / 权重只读；行首选择为选中态 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03095 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 指标说明 | 验证附加值率的指标说明抽屉对应当前行 | 1、已进入本页 | 1.点击「附加值率」行的「查看」 | 1、抽屉标题为「附加值率 · 指标说明」；2、可见「说明」和「支撑指标」；3、支撑指标含环节产值、利润贡献、单位产出 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-指标说明 / 附加值率 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03096 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 指标说明 | 验证技术壁垒的指标说明抽屉对应当前行 | 1、已进入本页 | 1.点击「技术壁垒」行的「查看」 | 1、抽屉标题为「技术壁垒 · 指标说明」；2、可见「说明」和「支撑指标」；3、支撑指标含专利壁垒、工艺复杂度、替代难度 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-指标说明 / 技术壁垒 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03097 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 指标说明 | 验证市场集中度的指标说明抽屉对应当前行 | 1、已进入本页 | 1.点击「市场集中度」行的「查看」 | 1、抽屉标题为「市场集中度 · 指标说明」；2、可见「说明」和「支撑指标」；3、支撑指标含头部企业份额、主体数量、竞争强度 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-指标说明 / 市场集中度 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03098 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 结果分析对象 | 验证结果页分析对象与本次发起条件一致 | 1、已用「新能源 / 新能源 / 新能源」跑完并打开结果 | 1.打开该次「产业关键环节识别结果」 | 1、分析对象显示「新能源 / 新能源」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果摘要 / 分析对象 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03099 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 关键环节数 | 验证结果页展示关键环节数 | 1、已打开 03098 同一条成功结果 | 1.定位「关键环节数」 | 1、「关键环节数」显示为 0 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果摘要 / 关键环节数；同册互指 03098 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03100 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 市场规模 | 验证结果页对市场规模给出诚实空态 | 1、已打开 03098 同一条成功结果 | 1.定位「市场规模」 | 1、「市场规模」为「暂无正式数据源」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果摘要 / 市场规模；同册互指 03098 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03101 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 投融资总额 | 验证结果页对投融资总额给出诚实空态 | 1、已打开 03098 同一条成功结果 | 1.定位「投融资总额」 | 1、「投融资总额」为「数据筹备中」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果摘要 / 投融资总额；同册互指 03098 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03102 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 结果降级说明 | 验证结果页展示叙述降级说明 | 1、已打开 03098 同一条成功结果 | 1.定位结果页顶部说明 | 1、出现「叙述能力不可用，已按规则结果诚实降级。」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果摘要 / 降级说明；同册互指 03098 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03103 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 全链路环节 | 验证结果页按顺序展示五个环节和衔接 | 1、已打开一条成功结果 | 1.定位「全链路环节结构化展示」 | 1、从左到右为研发、设计、制造、销售、服务；2、相邻环节之间标有「衔接」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.1 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-全链路 / 五环节 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03104 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 环节高端化 | 验证五个环节都显示高端化占位 | 1、已打开一条成功结果 | 1.定位五个环节圆点 | 1、五个环节均显示「高端化 —」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-全链路 / 高端化；步骤「看」改为定位 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03105 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 环节图例 | 验证全链路图例包含两类标记 | 1、已打开一条成功结果 | 1.定位「全链路环节结构化展示」图例 | 1、图例含「关键环节」；2、图例含「皇冠明珠」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-全链路 / 图例；本结果关键环节数为 0，无被点亮节点，高亮终态见清单未覆盖 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03106 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 环节详情 | 验证点击环节后详情区给出暂无说明 | 1、已打开一条成功结果 | 1.点击环节「设计」 | 1、「环节详情」为「该环节暂无详情说明」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.1 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-环节详情 / 暂无详情；研发、制造、销售、服务点击后同文案 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03107 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 代表企业 | 验证结果页代表企业为空态文案 | 1、已打开一条成功结果 | 1.定位「代表企业」 | 1、文案为「暂无代表企业」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-代表企业 / 空态 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03108 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 企业画像 | 验证结果页企业画像为空态文案 | 1、已打开一条成功结果 | 1.定位「企业画像」 | 1、文案为「暂无画像」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4.2 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-企业画像 / 空态 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03109 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 分析报告 | 验证从结果页打开分析报告 | 1、已打开一条成功结果 | 1.点击「查看报告」 | 1、进入「产业关键环节识别报告」；2、可见「报告目录」共 7 节（附录D） | P0 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-报告 / 查看报告 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03110 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 分析生成过程 | 开始分析后停在生成页，检查五阶段完成且不自动进结果 | 1、已进入本页；2、当天尚未成功分析过即将选择的这组对象 | 1.选齐分析对象的两个下拉和所属产业链；2.点击「开始分析」 | 1、当前页为「产业关键环节识别生成中」；2、五个阶段均显示「已完成」（附录E）；3、可见「查看分析结果」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-生成页 / 五阶段；生成结束不自动进入结果页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03111 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 回到诊断记录 | 验证生成页可以回到诊断记录并看到本次任务 | 1、已停在「产业关键环节识别生成中」 | 1.点击「查看分析记录」 | 1、进入「诊断记录」；2、列表中能看到本次任务号 | P0 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-生成页 / 查看分析记录 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03112 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 诊断记录列表 | 验证诊断记录表列出本页任务的字段 | 1、已进入本页 | 1.点击「诊断记录」 | 1、表头为任务、类型、状态、创建时间、操作；2、已完成行的类型为「产业关键环节识别」 | P0 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-诊断记录 / 表头 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03113 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 打开历史结果 | 验证已完成任务可以打开对应结果 | 1、诊断记录中有一条已完成任务 | 1.点击该行「查看结果」 | 1、进入「产业关键环节识别结果」；2、结果页任务号与该行相同 | P0 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-诊断记录 / 查看结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03114 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 新能源选项个数 | 选中新能源后，检查下级下拉的选项个数 | 1、已进入本页 | 1.在「分析对象」第一个下拉选择「新能源」；2.展开第二个下拉；3.选择「新能源」；4.展开「所属产业链」 | 1、第二个下拉为「新能源」和「新能源(L1)」，共 2 个；2、「所属产业链」只有「新能源」，共 1 个 | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析对象 / 新能源选项；与 03088 同一组对象，本条只数选项 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03115 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 下级联动 | 验证改选集群后清空下级并更换产业选项 | 1、已进入本页 | 1.在「分析对象」第一个下拉改选「生物产业」；2.展开第二个下拉 | 1、第二个下拉和「所属产业链」被清空；2、第二个下拉为生物、生物医药与生命健康、高端医疗器械，共 3 个 | P1 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-分析对象 / 切换集群 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03116 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 重置参数 | 重置参数只提示恢复推荐配置，检查不改已选对象 | 1、已进入本页；2、已把第一个下拉改为「生物产业」 | 1.点击「重置参数」 | 1、提示「已恢复该分析类型的推荐配置」；2、第一个下拉仍为「生物产业」；3、仍停留在「分析配置」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-重置参数 / 恢复推荐配置；权重仍为 34%、33%、33% |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03117 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 当天打开已有结果 | 验证同一天同一组对象再次开始分析时打开已有结果 | 1、当天已用「新能源 / 新能源 / 新能源」成功分析过 | 1.再次选中这一组对象；2.点击「开始分析」 | 1、提示「今日已分析过相同条件，已打开结果」；2、打开的任务号与当天已成功的那次相同 | P0 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-当天复用 / 再次开始分析 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03118 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 复制配置 | 验证已完成任务的复制配置回到分析配置且不自动开始 | 1、诊断记录中有一条已完成任务 | 1.点击该行「复制配置」 | 1、回到「分析配置」；2、下拉回显该任务保存的分析对象；3、未进入结果页 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 复制配置 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03119 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 按此配置新建分析 | 验证按此配置新建分析回到配置且对象仍在 | 1、已打开一条成功结果 | 1.点击「按此配置新建分析」 | 1、回到「分析配置」；2、下拉回显该结果的分析对象；3、可见「开始分析」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-结果工具 / 按此配置新建分析；不自动创建新任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03120 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 返回结果 | 验证报告页可以返回对应分析结果 | 1、已打开一条成功任务的报告 | 1.点击「返回分析结果」 | 1、回到「产业关键环节识别结果」；2、任务号与该报告所属任务相同 | P1 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-报告 / 返回分析结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03121 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 任务状态 | 验证任务状态下拉的选项个数 | 1、已打开「诊断记录」 | 1.展开「任务状态」 | 1、选项为全部状态、分析中、已完成、失败，共 4 个 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 任务状态选项 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03122 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 失败任务 | 验证按失败筛选后只留下失败任务 | 1、已打开「诊断记录」 | 1.将「任务状态」选为「失败」 | 1、列表中每条任务的状态都是「失败」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 筛选失败 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03123 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 失败任务复制配置 | 验证失败任务仍可复制配置回到分析配置 | 1、「任务状态」已选「失败」；2、列表中有失败任务 | 1.点击该行「复制配置」 | 1、回到「分析配置」；2、下拉回显该任务保存的对象；3、未进入结果页 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 失败行复制配置 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03124 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 重置任务状态 | 验证重置把任务状态恢复为全部状态 | 1、已把「任务状态」选为「失败」 | 1.点击「重置」 | 1、「任务状态」恢复为「全部状态」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 重置筛选 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03125 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 列表翻页 | 验证诊断记录翻到第 2 页后换成另一批任务 | 1、诊断记录总数超过 10 条 | 1.点击页码「2」 | 1、首行任务号与第 1 页不同；2、表头仍为任务、类型、状态、创建时间、操作 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 翻页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03126 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 每页条数 | 验证每页条数可以改为 20 条 | 1、已打开「诊断记录」；2、任务总数不少于 20 条 | 1.展开每页条数；2.选择「20 条/页」 | 1、选项为 10 条/页、20 条/页、50 条/页，共 3 个；2、当前页显示 20 行 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 每页条数 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03127 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 分析中任务 | 验证筛选分析中时不混入已结束任务 | 1、已打开「诊断记录」；2、当前没有进行中的任务 | 1.将「任务状态」选为「分析中」 | 1、列表没有任务行 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 筛选分析中；勘察时没有进行中任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03128 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 从记录打开报告 | 验证已完成任务可以从记录打开报告 | 1、诊断记录中有一条已完成任务 | 1.点击该行「查看报告」 | 1、进入「产业关键环节识别报告」；2、报告中的任务号与该行相同 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-诊断记录 / 查看报告 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03129 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 未选对象 | 验证不改下拉直接开始分析时提示尚未选择 | 1、刚进入本页，尚未在下拉里点选过 | 1.点击「开始分析」 | 1、提示「尚未选择分析对象」；2、仍停留在「分析配置」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-未选对象 / 开始分析；下拉初始文字是占位，点选后才算选定 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03130 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 未选产业链 | 验证只选到产业、产业链为空时不能开始分析 | 1、已进入本页 | 1.第一个下拉选「生物产业」；2.第二个下拉选「生物医药与生命健康」 | 1、「所属产业链」为空；2、「开始分析」不可点击 | P1 |  |  |  |  |  | US-CHAIN-DIAG-03 | AC-US-CHAIN-DIAG-03-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-未选产业链 / 开始分析不可用 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03131 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 失败任务不可看结果 | 验证失败任务不能打开结果和报告 | 1、「任务状态」已选「失败」；2、列表中有失败任务 | 1.点击该行「查看结果」；2.点击该行「查看报告」；3.点击该行「下载报告」 | 1、「查看结果」不可点击；2、「查看报告」不可点击；3、「下载报告」不可点击 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-失败任务 / 行上按钮；「复制配置」和「删除」仍可点击，见 03123、03132 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03132 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 取消后记录仍在 | 删除时取消，检查任务仍留在列表 | 1、诊断记录中有一条任务 | 1.点击该行「删除」；2.点击「取消」 | 1、弹出标题为「删除分析记录」的对话框；2、取消后该任务仍在列表中 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-删除 / 取消删除；对话框写明删除后列表不再显示该任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03133 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 确定后记录消失 | 验证确定删除后该任务从列表消失 | 1、诊断记录中有一条可删任务 | 1.点击该行「删除」；2.点击「确定」 | 1、提示「已删除」；2、该任务不再出现在当前列表 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-删除 / 确定删除；勘察时删除了一条失败记录后列表不再显示它 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03134 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 下载报告 | 验证已完成任务下载报告时给出失败提示 | 1、诊断记录中有一条已完成任务 | 1.点击该行「下载报告」 | 1、提示「资产下载失败（HTTP 404）」；2、仍停留在「诊断记录」 | P1 |  |  |  |  |  | US-CHAIN-DIAG-07 | AC-US-CHAIN-DIAG-07-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-下载报告 / 下载失败；文件未落地 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03135 | 科技专题战略分析 | 产业链分析 | 产业关键环节识别 |  | 产业关键环节识别 | 报告导出 | 验证报告页的导出当前不可点击 | 1、已打开一条已完成任务的报告 | 1.定位报告页的「导出」 | 1、「导出」不可点击 | P1 |  |  |  |  |  | US-CHAIN-DIAG-04 | AC-US-CHAIN-DIAG-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.4 |  | TRACE-CHAIN-TOPIC-DIAGNOSIS.yaml | /industry-center/diagnosis?workspace=key_link&tab=key-link |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-导出 / 导出不可用；当前账号页眉为未付费，没有已开通导出的另一种账号，不测文件落地 |

## 2. 旧号处置

| 旧号 | 处置 | 新号或原因 |
| --- | --- | --- |
| 00578 | 作废 | 03089。旧步骤写「产业运行诊断」，菜单现场是「产业链分析 / 产业关键环节识别」。旧金样取消 |
| 00579 | 作废 | 03090–03092。现场不是「产业 / INB1701 / 细分产业」三级 |
| 00580 | 作废 | 03115。联动对象是两个分析对象下拉加所属产业链 |
| 00581 | 作废 | 03093、03094。指标名为附加值率、技术壁垒、市场集中度 |
| 00582 | 作废 | 配置页没有版本四项，不写「不可见」 |
| 00583 | 作废 | 03088。旧条停在创建任务，未到成功结果页 |
| 00584 | 作废 | 03110。阶段名以生成页现场五句为准 |
| 00585 | 作废 | 03103。结果标题是「产业关键环节识别结果」 |
| 00586 | 作废 | 03103 只保留现场「衔接」。没有单独的功能边界说明，该格为无 |
| 00587 | 作废 | 03104。现场是「高端化 —」，没有降序排列 |
| 00588 | 作废 | 03105 只写图例。高亮终态未覆盖，原因见清单 |
| 00589 | 作废 | 无排序控件 |
| 00590 | 作废 | 03116。重置不把对象改回初始展示 |
| 00591 | 作废 | 本次未复测跨页对象共享，不沿用旧断言 |
| 00592 | 作废 | 03112、03121。列和筛选项以诊断记录现场为准 |
| 00593 | 删除 | 评审专条。旧号不复用，不新写 |
| 00594 | 作废 | 03113。行按钮是「查看结果」 |
| 00595 | 作废 | 本次未复测同路由隔离，不沿用旧控件名 |
| 00596 | 作废 | 配置页没有版本快照区 |
| 00597 | 作废 | 03107、03108。没有竞争格局、技术趋势和加入名单 |
| 00598 | 作废 | 无「重新分析」。当天再次开始为 03117 |
| 00599 | 作废 | 无清空控件。未点选见 03129 |
| 00600 | 作废 | 03100–03102。空态用现场原句 |

## 3. 红线自检

- 主流程 27 条（03088–03114）≥ 备选 14 条（03115–03128）+ 异常 7 条（03129–03135）。
- 金样只有 03088。入口 B、重新分析、结果搜索、结果表、二级、入池、排序均为无。
- 用到的最大号：03135。03136–03187 未写入。
- 前置、步骤、预期、功能项四列对评审层字样的扫描为 0。

### 附录A 分析对象第一个下拉（03090，15）

新一代信息技术；生物产业；新能源；新材料；高端装备；智能网联新能源汽车；绿色环保；低空经济与空天；传统与创意产业；海洋产业；未来制造（智能机器人）；未来信息（光载信息、AI 底层生态）；未来能源；未来空间；未来健康（合成生物、细胞基因、脑机工程）。

### 附录B 分析对象第二个下拉（03091，初始 7）

新一代信息技术；半导体与集成电路；人工智能与应用；智能终端；软件与信息服务；新型网络与通信；超高清视频与显示。

### 附录C 所属产业链（03092，初始 6）

半导体与集成电路；人工智能与应用；新型网络与通信；超高清视频与显示；智能终端；软件与信息服务。

### 附录D 报告目录（03109，7）

报告身份；执行摘要；对象与范围；关键发现；证据与分析；数据来源与生成说明；局限性与使用边界。

### 附录E 生成页阶段（03110，5）

任务提交与产业链对象冻结；全链路环节结构化拆解（研发/设计/制造/销售/服务）；基于附加值率、技术壁垒、市场集中度计算高端化指数；关键环节智能标注与竞争格局/代表企业/技术趋势归纳；结果可信性校验与分析报告组装。
