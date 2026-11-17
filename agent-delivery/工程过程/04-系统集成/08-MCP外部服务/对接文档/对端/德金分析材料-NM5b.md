<!-- feishu-doc {"doc": "NM5bdtntcogA8lxoNh3cirSgnif"} 只改标记下面的文字；不要删改 <!-- b:... --> 标记 -->
<!-- b:doxcnRym9M7CnjGlubLFyKpYt4e heading2 -->
一、目标与节奏
<!-- b:doxcnaD5P1AYdbztxNMXTHOKxgb text -->
以现有 Zmate 为基础改造报告创作流程，按“先跑通、再补强、后打磨”的顺序推进。三个版本连续交付，核心功能计划于 2026 年 12 月 22 日前完成；12 月 23—31 日用于发布稳定、试运行和问题收敛。
<!-- b:DnCfdGYaPonadbxmKudcNBD6nch text -->

<!-- b:EXP2dFvCNoZEyQxTOVacTui0nDf ordered -->
整体流程拆解，细化一点，从query、意图解析、query改写等等环节
<!-- b:BIHKdbSAlo0nZCxGrHNcDULHn5g ordered -->
技术底层框架确认，多Agent协同，协同模式、协同点、哪些Agent参与、辩论。其他系统的skill在哪个环节发挥作用。边辩论，边总结成指标和卷宗；
<!-- b:JqhPdACzqoDArUxXElQcT38TnQ1 ordered -->
数据层：知识库、指标层、卷宗层、
<!-- b:JT4qdHuxpoIN8bxOqZ3ckxqsnq9 ordered -->
产品形态：是不是要抄通用智能体的形式，或有什么更好的形式
<!-- b:ABr8dLYuhoFVzcxt2XnczucKny1 text -->

<!-- b:JzoWdCG4WoCwHdxmW71caZCDnCq text -->

<!-- b:doxcnmLlUGcLu8P80Hv3kysVRkf heading2 -->
二、V1：MVP全流程（11月16日—11月30日）
<!-- b:doxcnBWrwadteXj0ABU625J0U8d heading3 -->
建设目标
<!-- b:doxcn1wEavbeIsARUC7XA0WZgUc text -->
基于原有 Zmate 改造，首先让用户能够创建报告任务、看到智能体如何推进，并在任务完成后阅读一份可追溯的报告。优先保证真实流程可用，不将需求澄清卡片、复杂审阅和高级体验打包进 MVP。
<!-- b:doxcnKGEYqgM5Tl2ynKTbmUWdsg heading3 -->
核心需求（P0）
<!-- b:doxcnI5aIG4CELsiuD9b8VKhGSU ordered -->
Query 输入与任务创建
<!-- b:doxcnIrKkyfJkUtvA3vdbNKU7Nh bullet -->
支持输入报告需求、选择报告类型、召唤专家并添加已安装技能。
<!-- b:doxcn0kPlGKF2qm5kCwphPMZ28e bullet -->
支持选择或不选择项目文件夹；选择项目后，新任务自动归入该项目。
<!-- b:doxcnxa0ha5lBbXk3uBnpDEqQch bullet -->
支持回车或提交按钮创建报告任务，并进入任务工作区。
<!-- b:doxcnwIu39aDcK16PfTkIJET0Gb ordered -->
项目与报告任务管理
<!-- b:doxcnOG1u85Gn9VMxdKHz1xF6Cc bullet -->
左侧支持项目文件夹及报告任务的两级组织，文件夹可折叠。
<!-- b:doxcnEOqzushpv1qkecTauOrRxc bullet -->
报告任务显示标题、报告类型及状态：未读提示、生成中状态、完成/失败状态。
<!-- b:doxcnd9txf87ZWJr5vED04T56Hd bullet -->
点击既有任务可恢复对应上下文、任务进展和输出物。
<!-- b:doxcnQ7YAGbOQOPfjy7QkApudGf ordered -->
专家与技能调用
<!-- b:doxcn8inhlf6zNDfFafyCwkfRfc bullet -->
专家作为场景化能力入口；支持查看专家说明、安装技能、将技能加入当前任务。
<!-- b:doxcnm34TF5XpembWWe4zC3VHRf bullet -->
明确区分“安装技能”和“本次任务使用技能”，安装状态可持久保存。
<!-- b:doxcnJPUrWug4gISvviceGFSc7b bullet -->
MVP 先接入可用的专家/技能清单与基础调用链路；技能广场的推荐、版本更新推送后续迭代。
<!-- b:doxcnQoDPFuBFkTARsEfZ5G16Kc ordered -->
智能体执行过程与多轮交互
<!-- b:doxcnmQhA6xv563NzcP3A1S3EUb bullet -->
展示阶段性进展、面向用户的研判摘要、调用工具、调用状态、返回摘要和当前执行阶段。
<!-- b:doxcnQC0uTrVHObZdvBwzmNvhQT bullet -->
支持用户在执行过程中继续对话、补充要求；提供暂停/继续或中断入口（以 Zmate 现有执行能力为准）。
<!-- b:doxcn5JKfpopFp5d9Iukv149Dxd bullet -->
过程记录采用可审阅的阶段摘要，不展示模型内部逐字思维链。
<!-- b:doxcnhae7TZRw7Mo1YTDd4o23Gc ordered -->
报告输出与基础阅读
<!-- b:doxcnsDbcYLPnYawdAcnMEwLSf7 bullet -->
生成期间右侧不展示未完成的报告正文，只展示“生成中”状态与进度。
<!-- b:doxcneUMkiIybHfSr4shscbksbf bullet -->
任务完成后加载报告，支持基本目录、复制、下载和阅读。
<!-- b:doxcno7vbQPChCVx14KllT7sgkg bullet -->
迁移既有原型中已验证的基础溯源交互：报告关键结论显示角标，点击可查看引用来源或指标口径/计算逻辑。
<!-- b:doxcnCmupIp2DqgLJ5bIRzKUcng ordered -->
知识与指标来源的最小接入
<!-- b:doxcnXUesQAW79c3s1nCQahN0Vc bullet -->
写作链路预留并接通四类来源：官方知识库、个人知识库、官方指标库、个人指标库。
<!-- b:doxcnHkiY9nQMTCj6B6qEMjaXOd bullet -->
MVP 以现有可用数据和权限为边界，支持检索/调用并在报告中标记来源类型；暂不要求完整的知识治理后台、复杂入库审批和更新编排。
<!-- b:doxcnvkmUYBtOpFcHSkyXPWKaQc heading3 -->
MVP验收标准
<!-- b:doxcnc3kAp0Cumy8kkUYaKCmVgc bullet -->
从 Query 提交开始，能够完成任务创建、专家/技能选择、智能体执行、报告输出、报告阅读的端到端演示。
<!-- b:doxcnGAXAICglMd7WGBaI1XV2Sf bullet -->
项目文件夹可折叠；报告任务状态可区分；重新打开任务能恢复其上下文和状态。
<!-- b:doxcnyzLYKLTNci3W47jws490Hh bullet -->
生成期间报告正文不可见；完成后才开放阅读与下载。
<!-- b:doxcnZfXfEvqS8UOs7xaemq0Rxd bullet -->
至少有一条真实可执行的工具调用链路和一份可读的报告输出，不能只呈现静态进度动画。
<!-- b:doxcnHMiHE5nY9jcLRC8zTYqJyX bullet -->
报告中的代表性结论可打开溯源信息；来源类型、引用内容或指标计算口径与页面展示一致。
<!-- b:doxcnTJbFjw9FX6uerdGbMNERab bullet -->
11月25日提测；阻断问题关闭并通过验收后，于11月30日发布。
<!-- b:doxcnSKz5ZcofGD7VjCLNtSRRFg heading2 -->
三、V2：能力补强（12月1日—12月10日）
<!-- b:doxcnQqsg9CBqDpLZ1GxXZTxu1d heading3 -->
建设目标
<!-- b:doxcnWeoWEBGjHyEQzgzkJY5ePb text -->
在全流程可用的基础上，补上“把问题问清楚”和“把正确的数据、知识带进报告”的能力，让写作任务更可控、报告依据更完整。
<!-- b:doxcnmONxwYOwY0znqSbGCZpq7b heading3 -->
核心迭代
<!-- b:doxcnfv3JkPkYmqqLYDcgCP58fd ordered -->
需求澄清交互
<!-- b:doxcn3dsFjVkk7M8gcuiKntcqtg bullet -->
在第二环节以输入框上方的卡片逐项澄清研究对象、领域/行业、范围、时间边界、使用对象、报告深度和预期决策。
<!-- b:doxcnxmjMrvxJj6Kdga8KYt9n6g bullet -->
支持上一项/下一项、用户补充、跳过非必填项和回看已确认信息；确认后再进入正式生成。
<!-- b:doxcnyFJZJS6h90ETscM3MIF9rf ordered -->
知识库与指标库接入深化
<!-- b:doxcntQS3eiuWVWfnFJYh01u4bf bullet -->
明确数据类型与归属的二维结构：个人/官方 × 知识库/指标库。
<!-- b:doxcnDkj8XRu1v2YYnRkcj71q5g bullet -->
知识库承载非结构化文档；指标库承载结构化指标及其口径、来源、更新时间和计算关系。
<!-- b:doxcn54Uq4UuCGeRJcWEAfTxF7g bullet -->
支持按任务选择或排除来源，显示本次任务实际使用了哪些知识条目、指标和阶段性结论。
<!-- b:doxcnqviSWwaaQztg7hn7OllYKc bullet -->
补齐基础权限隔离、入库/更新状态和错误提示；官方与个人数据不得在检索或展示中混淆。
<!-- b:doxcnobjPEaDGtBSPxbx8nTpIjh ordered -->
溯源信息补全
<!-- b:doxcnls0iiYjj3velPo4yXlR4kO bullet -->
原文引用：展示文档名称、被引用段落、原文高亮及引用原因。
<!-- b:doxcnbaAqCqaX92PXlboi3sKVIg bullet -->
指标查询：展示指标库名称、指标定义、数据时间和血缘/计算逻辑。
<!-- b:doxcn8FPuqp52muklGCaaLOYHzb bullet -->
推断结论：展示推断步骤、使用的原始依据、假设与待核验提示；高级可信度评分在 V3 建设。
<!-- b:doxcnqNP5Lczd96RrydHlNyXEif ordered -->
任务连续性与稳定性
<!-- b:doxcnqCnZCXiGw58I2PJTzv1LGf bullet -->
需求澄清结果、来源选择、执行记录和报告版本与任务关联保存。
<!-- b:doxcnYLi4ctAESfidyPfbGYr5pc bullet -->
完善失败重试、继续执行、异常提示、空数据/权限不足提示和关键操作日志。
<!-- b:doxcnPf5kWxSSKyLTNZZ6E6OlYf heading3 -->
V2验收标准
<!-- b:doxcnI4Ktj1bqpSxKkTvUtYJsjb bullet -->
用户可在同一工作区完成结构化澄清并确认任务边界。
<!-- b:doxcnfjQsmkSNFccNKUjj5XvnZe bullet -->
四类知识/指标来源在产品和数据模型中可区分，按权限检索并记录实际调用结果。
<!-- b:doxcnUKeKrnGZIAQNiQSEbQdsnh bullet -->
报告中的原文引用、指标结论和推断结论能够进入相应的溯源展示。
<!-- b:doxcnbmgIDjqaIDsFiG8jJMLuVP bullet -->
任务中断或重新打开后，已确认需求、来源选择及已有执行记录不丢失。
<!-- b:doxcn0eYTwcO9vEVpwS15pRuNhg heading2 -->
四、V3：审阅与体验优化（12月11日—12月22日）
<!-- b:doxcnkzIgm4rzooyHl8vFE8Ypag heading3 -->
建设目标
<!-- b:doxcnukDtjlfomV8GohA0n56N4f text -->
让用户不仅能“生成并阅读报告”，还能够检查报告是否站得住、快速定位依据并完成定稿。审阅模式作为报告生成后的独立工作模式，不阻塞 MVP 的基本阅读。
<!-- b:doxcnAIXsXF0nYvfPCJn0RVKcad heading3 -->
核心迭代
<!-- b:doxcnigKKK012WRDYs0p3CUC7og ordered -->
审阅模式与对抗审查
<!-- b:doxcnFIhC3e8wimAzpdRI7weP6e bullet -->
在报告阅读顶部增加“审阅”入口，展开目录、溯源与审阅工具。
<!-- b:doxcnvwQp37XJGGvycsaOL8Dmqg bullet -->
对抗审查识别论据缺口、结论跳跃、证据不足、反方观点、关键假设和适用边界。
<!-- b:doxcnOvWhFb06EtvjASqwOpptDX bullet -->
输出可定位到章节/段落的问题清单，支持用户逐项采纳、忽略或要求 AI 修改。
<!-- b:doxcnw2GmvSGKkv0ggG2FN15q6g ordered -->
报告评测与质量体检
<!-- b:doxcnIKfncmvDFP2doDHS2qZmTd bullet -->
展示报告质量分项与总览，检查结构完整性、证据覆盖、引用规范、时效性、逻辑一致性及待人工核验项。
<!-- b:doxcnYHHVXYeqrCZwmgPOAp7d5b bullet -->
分数需可解释：展示评价维度、判定依据和改进建议；避免只给不可解释的单一分数。
<!-- b:doxcnv9YgpEpiQyEcVuYhgX8fGc ordered -->
三类溯源审阅体验完善
<!-- b:doxcnkQIwlQj9Ndghgg7xNTn2rd bullet -->
原文引用、指标血缘、基于事实的推断分别采用不同视图。
<!-- b:doxcngfTLC0DJ6hvlyCNKbzKRkh bullet -->
支持从报告角标直达依据，并从依据返回原结论；突出数据来源、更新时间、口径、计算逻辑、推断依据和可信度提示。
<!-- b:doxcnKHDsBj4SLMKE7nnc8bPrXg bullet -->
对低置信或存在冲突的证据保留显式风险提示，不以评分替代人工判断。
<!-- b:doxcn6haYscmWBzRSoPTj7bJyMf ordered -->
阅读与编辑体验
<!-- b:doxcnYXhS8eRffPlIfvKvt7UaFf bullet -->
优化目录定位、重点结论标记、笔记/批注、分段修改、全文修改入口和报告排版。
<!-- b:doxcn9xO0ylmh9NH6iaLHZeSlKd bullet -->
优化任务时间线的折叠、工具详情查看、进展反馈、暂停/继续和长任务恢复体验。
<!-- b:doxcnKhoISFRUOhEfT63FQBmaOg bullet -->
完成主流屏幕尺寸适配、性能和可访问性检查，以及试运行问题修复。
<!-- b:doxcnzbSSeq9nwm26Xj7TzfRnzg heading3 -->
V3验收标准
<!-- b:doxcnpSllV1WKKw06zZ1JihbhIe bullet -->
用户能从报告顶部进入审阅模式，查看目录、审查意见、质量评测和三类溯源。
<!-- b:doxcnG3Jaze6qIkwnezn6XQMy4g bullet -->
审查意见可定位到对应内容，并能触发针对性修改；修改前后版本可区分。
<!-- b:doxcnSZGVxTKT9CQWZ9ZYmXQBRg bullet -->
评测项有明确解释和可执行建议；低置信、冲突或缺失证据有风险提示。
<!-- b:doxcnxAEwmDOg7eTYzuUtAVq17d bullet -->
核心报告阅读、溯源、编辑和任务恢复流程通过回归测试，并完成试运行验收。
<!-- b:doxcndj9YZNkqbevVwgVR4d5rPe heading2 -->
五、知识库与指标库建设安排
<!-- b:doxcnGlMTUEFDavWZ6nGsdE6JYd text -->
数据资产
<!-- b:doxcnnimbpOvOlwBEXZLSbl5egb text -->
数据形态
<!-- b:doxcnZ6uC10mebGhWyzCH4qSxY5 text -->
归属
<!-- b:doxcnNwKSoAGBTeSzXuMvb2naEb text -->
在报告流程中的作用
<!-- b:doxcnrroQ7G6oqkQprysNp6kIGb text -->
版本安排
<!-- b:doxcnaoC4Swm9F1rl1W7JnU8Qbh text -->
官方知识库
<!-- b:doxcnuztsBnDaT3VILqU28cL7Tf text -->
非结构化文档、研究材料、政策/产业资料等
<!-- b:doxcnYDahorVvcogYHrhTeWBhDh text -->
官方公共
<!-- b:doxcnPaZxgU6xEJaKTXIk7jqQAB text -->
检索原文、提供引用证据和背景知识
<!-- b:doxcnHX07nAmoWI75gRVXHnBw2e text -->
V1接入可用来源；V2完善分类、权限、更新状态及来源选择
<!-- b:doxcn91FH6iQVmTTyldmTBoxQtb text -->
个人知识库
<!-- b:doxcnLr7atDyK7XyHt6KrDP8A2y text -->
用户上传或个人维护的非结构化资料
<!-- b:doxcnnTV2CIZeb2MWtSfes0Oxwf text -->
个人私有
<!-- b:doxcnxTd9lGhLLeYqi87bBISOGP text -->
将用户材料纳入任务上下文，支持原文引用
<!-- b:doxcnzyFs8YInayhFp6bIIueXZg text -->
V1支持基础调用；V2完善个人范围、权限隔离和任务选择
<!-- b:doxcnJmltHZRvcBvvvNG9M0TIrh text -->
官方指标库
<!-- b:doxcnVpZd2sHhgEaLhe0UzTANxc text -->
结构化指标、口径、来源、时间和计算关系
<!-- b:doxcn2wRnFR1JYyMKl93xDWLtYc text -->
官方公共
<!-- b:doxcnbcqeztmpM69sdqNDRx6mNf text -->
支撑分析结论、指标查询及数据血缘展示
<!-- b:doxcnC9ElNxDmxGprzPbfxBzlvf text -->
V1接入可用指标；V2完善血缘字段和调用记录；V3强化审阅呈现
<!-- b:doxcnwFIG0XOCC5rcDhg8CNpEuh text -->
个人指标库
<!-- b:doxcn06AHp43vNLZdmAggAeyKnd text -->
用户维护的结构化数据、指标或自定义口径
<!-- b:doxcnHuUNagnpkhZ7td1kp6v4Qf text -->
个人私有
<!-- b:doxcnkj7m5sQGlA6L77bhavkHuw text -->
支持用户专属数据和指标参与分析
<!-- b:doxcnTp9ZYoidmzmh2ykUSlFspf text -->
V1预留并在数据可用时接入；V2建设导入、权限和调用能力；V3完善核验提示
<!-- b:doxcnx9mxlYkPOlmvvVaWKwvh7b text -->
建设原则：四类数据在逻辑和权限上分层；报告结论记录实际来源；知识库与指标库分别治理；数据不足、过期、冲突或无权访问时明确提示，不静默替代或伪造依据。
<!-- b:doxcnAOMPMJ6MewSJ3AY1QzUSFg heading2 -->
六、版本边界与优先级
<!-- b:doxcnLTh00Y2JYObtpwZVG3cpMf text -->
优先级
<!-- b:doxcnxlbs4AWU4RRypoQCnn4jqd text -->
范围
<!-- b:doxcnHqxivDflnjzR4GLMF5wS8d text -->
主要内容
<!-- b:doxcnUZ8iIKfr45AYTl4m9ptCMw text -->
P0：首发必做
<!-- b:doxcnvBJweZutmwvI33sNayXdBd text -->
V1
<!-- b:doxcnbNbRwqmx0w19HTXr23vvxc text -->
Zmate改造；Query与任务创建；项目/报告任务列表和状态；专家/技能安装及调用；任务执行时间线和多轮对话；完成后报告阅读；基础溯源；四类数据源的最小接入；11月25日提测、11月30日发布
<!-- b:doxcn0gCrpncYm2iyaD5cE3M7gh text -->
P1：能力补强
<!-- b:doxcn9NiRCyzcO00n5bZwNgpbXe text -->
V2
<!-- b:doxcnVKsGZoApHULYPpMXuaMTse text -->
结构化需求澄清；知识库/指标库分类与权限深化；更完整的来源选择与溯源；任务连续性和异常处理
<!-- b:doxcnONwE3xWoEkN9KCxikoW6gg text -->
P2：审阅增值与体验
<!-- b:doxcnnHksGTuIIqctbzgRjoIdce text -->
V3
<!-- b:doxcnbsrUv4SPZix7QHNaYU9Dcc text -->
对抗审查；质量评分/体检；三类溯源审阅；全文/分段修改、笔记批注、排版与任务过程体验优化
<!-- b:doxcnU7hrmsoKfN5NRSwgOFF2rg heading3 -->
暂不作为首发前置条件
<!-- b:doxcnY8LnIDhwwSLxIRTUPUi4Hb bullet -->
自动发现并推荐开源技能、技能更新推送和复杂技能治理。
<!-- b:doxcnqV8JMmcyVjk1XZoaFh6s3g bullet -->
全自动知识采集、全量数据治理工作台及复杂审批流。
<!-- b:doxcnRWKx30zWgWrbcAFHRIsfVb bullet -->
完全自动化的专家评审或以模型评分替代专家/用户责任判断。
<!-- b:doxcngQJfF6Uv9czCGdInDARm2d bullet -->
12月22日之后的新需求扩展；进入稳定期后统一评估是否纳入后续版本。
<!-- b:doxcnSQDp7hxGPxKNRXCbFGUIpg heading2 -->
七、关键依赖与项目管理
<!-- b:doxcnFM40DwdgnRe1ZMCB0zzuWU ordered -->
Zmate改造边界：尽早确认可复用的任务、会话、工具调用、文件输出、权限和存储能力，避免在首发阶段重造底层平台。
<!-- b:doxcnh3iflX2EP7YP4Opv6Z0vnc ordered -->
数据与权限：明确个人/官方知识与指标的访问控制、可用数据清单、引用字段和测试账号；无数据或授权时使用清晰的空态，不用模拟内容冒充真实结果。
<!-- b:doxcnQitxgPeJW6hcbTxZ4mABjc ordered -->
跨团队联调：V1首周完成接口、数据结构和验收样例对齐；每个版本预留联调与回归时间，供应商按模块认领交付和缺陷责任。
<!-- b:doxcnwCzaStt1rKWLonk3NAFAOd ordered -->
版本门禁：V1以端到端闭环和阻断问题关闭为发布门槛；V2以来源分类、权限与溯源一致性为门槛；V3以审阅可用、评测可解释和回归通过为门槛。
<!-- b:doxcnibLqy86BnxnTiwQ3HyaoPg ordered -->
试运行反馈：12月23—31日邀请真实用户围绕科技企业、政府和科研院所场景试用，记录任务完成率、报告可用性、溯源点击/核验情况、失败原因及修改轮次，形成下一阶段需求池。
