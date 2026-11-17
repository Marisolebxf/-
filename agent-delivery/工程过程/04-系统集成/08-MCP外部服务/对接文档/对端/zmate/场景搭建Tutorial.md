<!-- feishu-doc {"doc": "Q0kWdvhy2obgsvxZBj2cPBhvnIf"} 只改标记下面的文字；不要删改 <!-- b:... --> 标记 -->
<!-- b:B4i3dk96xoSFrkxBRPJcrimpnpg text -->
本文档主要展示多个场景搭建的真实案例，为后续落地过程提供标准化SOP。后续项目可以通过该SOP完成zmate场景构建，实现快速落地。
<!-- b:MTlfdAapeowhRoxnftkcLJFynWh text -->
整个SOP的核心围绕 步骤进行：用户场景分析-员工方案选型-前端展示因素汇总-技术方案明确-数字员工开发
<!-- b:L8bcdJWHhoaD5axV5Ifc1LPdncf text -->
zmate提供的数字员工类型包括：助手型（独享沙箱），分身型（共享沙箱），无状态型（无状态沙箱池）
<!-- b:UVESdQFRcowGqVxqGrZcxwmTnVe text -->
zmate提供自由建设的技术组件包括：Persona，Skills，MCP，Extensions（tools），Plugin（hooks）
<!-- b:VfuGdxtUjoaSl2xCLWlcnDq8nPg heading1 -->
技术选型参考
<!-- b:T3lPdiZkZo9O1GxMq6zcWgSun0b ordered -->
数字员工选型参考：
<!-- b:Po0kd4hTBoHlpOxjfb9cuzpQnGf ordered -->
助手型：可以理解为云端虚拟机的满血版openclaw（正在拓展其他harness），覆盖个人7*24助手场景
<!-- b:LwLidqDD6ohEDrxYyMYcQDQfnYf ordered -->
分身型：多人共享openclaw沙箱，但是使用权限被限制（无法修改技能/人格文件等）。适合的使用场景为咨询/解决方案等场景（owner可以查看对应用户的聊天内容，接管会话以及管理建联人）
<!-- b:OxqldVt2MoISK3x4AjCceuE8n2e ordered -->
无状态型：通过无状态服务提供AaaS给到上层应用，支持ws或openresponses标准接口进行访问。
<!-- b:MV8vdO6hzoqsbVxhupwcnT07nwg ordered -->
技术组件参考：
<!-- b:S27LdNR5DozFlfxAXGEchvMGn7x ordered -->
Persona：同openclaw人格文件定义
<!-- b:I3zDdbBeEofElExaxSMcJBZInWd ordered -->
Skills：标准skills定义，但不定义请求接口（原因是防止PI-agent篡改API或Key），接口访问统一通过MCP控制
<!-- b:TNiadhPt0o3Xrmxs9UIcq6TSnmf ordered readonly -->
MCP：mcp server参考[mention_doc]进行用户鉴权和隔离。具体的实现
<!-- b:R0FHdqhi4o6kRKxweh7chrnznug ordered -->
Extensions：自定义工具，可以定义独立工具类型，可以扩展Agent基本工具能力，在工具中还可以定义独立的ws返回事件。基于该事件可以进行后续的应用拓展。
<!-- b:EZGhdW68NowB6yxOD3Bcnucinle ordered -->
Plugin：自定义钩子，可以对Agent行为进行约束（比如越界操作限制，工作目录初始化等）
<!-- b:U3gIdx6KGoK4Rcxw4wecW2zonHd text -->

<!-- b:Btqqd0FhzoZ6ofxEzjxcoInQnmg heading1 -->
国科信报告写作【无状态应用】
<!-- b:MG3adsAdMouEuExoeYfcNYrUnPe text -->
一句话描述项目目标：呈现形态为应用，进行深度报告撰写，输出类deep research 的多模态报告（markdown）
<!-- b:Sb4qdpgsGoXrVpxF4Z4cFd09ncd text readonly -->
项目文档：PRD[mention_doc]，技术方案[mention_doc][mention_doc]
<!-- b:JRf7d7PADoZnb0xLfnbcX7hTnIf text -->
建设思路：
<!-- b:CkEgdSp2oofZBjxXoK8c7vG5nKc ordered -->
由于呈现形态为应用，所以采用的员工方案是无状态数字员工，根据应用的需求，拆分为需求澄清员工和报告生成员工，分别用于生成需求澄清表单/大纲和端到端生成报告。
<!-- b:R8YNdsRngogVLFxnua8c1urun0b ordered -->
员工的人格文件/技能文件的构建逻辑需要契合单一任务场景的需要，删除无用的人格文件/技能内容。
<!-- b:B7kCd68JOogzKOxXpNscMyJunDf ordered -->
前端展示需要呈现可渲染表单/大纲和报告生成计划（该能力不在harness基础能力模式中），所以需要构建虚拟的extensions，完成ws中向前端的特殊事件传递。extensions可以在创建元虾处进行上传
<!-- b:R76VdEEHsoArcYxZNWscDxCanyg code -->
{"type":"event","event":"agent","payload":{"runId":"320db6e4-7837-4071-977d-4f27ce204ee5","stream":"report.strategy","data":{"object":"具身智能企业","strategic_objectives":["技术路线选择：明确具身智能核心技术方向（大模型驱动 vs 传统控制架构），确定研发优先级与资源分配策略","产品化与商业化路径：制定从技术验证到规模化落地的分阶段计划，明确首切场景与商业模式","产业链生态布局：构建上下游合作关系（传感器、执行器、芯片、云服务），建立技术与供应链护城河","融资与估值策略：规划融资节奏与估值管理，对标Figure AI、宇树科技等头部玩家，吸引战略投资与产业资本"],"expert_opinion":"具身智能是AI从数字世界走向物理世界的关键桥梁。当前行业处于\"技术验证→早期商业化\"的拐点，大模型赋能使机器人从专用工具走向通用智能体。建议采取\"大模型+垂直场景\"双轮驱动策略：短期以工业/服务机器人等高价值场景实现商业化闭环，中长期布局人形机器人通用平台。技术层面优先突破多模态感知融合与Sim-to-Real迁移，商业模式上避免过早追求通用性，先做深做透1-2个场景再横向扩展。融资窗口期约12-18个月，应加速完成B轮前技术验证与客户积累。"},"sessionKey":"agent:main:dashboard:2d63dcda-4c6b-4ea0-af99-6d1cc47c0e8b","seq":2,"ts":1788428427053},"seq":349}
<!-- b:H7d4dX7YPo6RgkxXsB8c9MrwnUe code -->
{"type":"event","event":"agent","payload":{"runId":"de57e623-e7b0-42ac-be48-eaa8e0adb350","stream":"report.task_plan","data":{"plan":[{"id":1,"status":"done","task":"调研头部厂商商业化数据与技术演进动态"},{"id":2,"status":"done","task":"调研市场规模、成本监管与Agent经济预测数据"},{"id":3,"status":"done","task":"进行引用整编与市场数据图表生成"},{"id":4,"status":"running","task":"进行战略咨询报告五章正文撰写"}]},"sessionKey":"agent:report:dashboard:d3deb01b-72e6-486e-b7e9-0fc91abd223d","seq":5,"ts":1788860208586},"seq":662}
<!-- b:X8c5d4osCo4MmZxeg3mcwPySn2g ordered -->
前端需要渲染对应的markdown和图像。定义了独立的extensions打通S3完成制品上传。
<!-- b:FRDydSuzMoMyvUxSJuBca0H8nzg ordered -->
无状态在完成agent runtime后，需要保证目录初始化，自动删除相关制品。实现逻辑为插入plugins，在runtime结束后自动化删除除skills和人格文件以外的所有工作区文件/目录。
<!-- b:IettdjuAdojmaXxNi05cJKTLnnh text -->
实现效果：两个AaaS服务数字员工，服务的前端交互通过ws的特殊事件传递，特殊事件由extensions定义。文件制品通过 s3 extensions传递到对象存储，随后通过特殊事件传递最终制品地址，runtime结束后自动清理初始化工作目录。整个业务逻辑通过数字员工能力分化，业务skills引导，特殊事件传递信息，extensions打通内网系统，完成了场景构建。
<!-- b:WyVldQZQEoJ2xyxaR4VcuzbUnBf text -->

<!-- b:ZWiSdceqXo9iGVx0yMbc1J1Tnzf text -->

<!-- b:UgKGdy4XyoJKWNxZoN9cLFL4nWd text -->

