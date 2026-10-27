# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md` **v1.2**（含 §5.4.1 用例级粒度铁律；编写红线见 `qa/as-built/prompts/_case.md`）  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v3.0 · 2026-10-18（对照重写；保留号不动，新号 02088–02125）  
> **模块**：深圳企业现状分析（SZSTATUS / catalog `ent-sz-status`）  
> **金样**：**02088 / 00969**（选产业链到定位结果；已选链后进入多城市横向对标结果。烟测跑这两条）  
> **旧号段**：00960–00978 中保留 9 条；作废 9 条、删除 1 条，旧号不复用。新号只用 02088–02187 段，用到 **02125**  
> **环境**：https://edu.itic-sci.com/tts/svcz/ · 账号 `admin` / `123456`（已在业务页且 URL 不含 `/login` 则不要登出）  
> **入口**：侧栏「企业分析」→「深圳企业现状分析」  
> **路由**：`/enterprise/shenzhen-enterprise-status-analysis`  
> **发起方式**：只有一种。在「产业链」下拉点选一条产业链，定位结果即出现。没有对象名单发起，没有「开始分析」  
> **功能点 / 功能点ID**：新条填「待 A 线回填」；保留条沿用原扩展列  
> **自动化用例ID**：新条留空（第 2 步再回填）；保留条沿用原脚本号  
> **关联任务**：`QA-KJZTFWXT-BLINE-CASE-ENT-L01`  
> **维护**：agent:qa-agent · 监管 human:黄敬洲

---

## 关评审控件清单

入口拓扑（本页不是分析任务工作区，没有第二种发起）：

| 行 | 现场 | 用例 |
|----|------|------|
| 入口 A · 产业链下拉 | 点选一条产业链后进入「产业链定位」结果 | 02088 金样 |
| 入口 B · 已选对象发起 | 无。页上没有从名单发起本页分析的按钮 | 无 |
| 任务列表 | 无 | 无 |
| 结果 · 产业链定位 | 指标卡、两张分布图、企业清单 | 见下表 |
| 结果 · 多城市横向对标 | 同一条产业链下的另一结果页 | 00969 金样 |

| 格 | 用例或未覆盖 |
|----|----------------|
| 侧栏进入、默认 Tab「产业链定位」 | 00960 |
| 区域「全国热门科创城市 / 深圳 / 全部」锁定 | 00961 |
| 产业链下拉共 15 项 | 02093 |
| 未选链引导「请先选择产业链以加载深圳现状分析」 | 00963 |
| 未选链时切到「多城市横向对标」 | 02094 |
| 选「人工智能」到达定位结果 | 02088 金样 |
| 指标卡：深圳相关企业、覆盖产业链环节、重点环节企业、产业链完整度 | 02089 |
| 页头「数据更新至」 | 02090 |
| 「产业链环节分布」 | 02091 |
| 「链中角色分布」 | 02092 |
| 改选「生物医药」后回显并刷新 | 00975 |
| 双 Tab 往返后已选链仍在 | 00974 |
| 环节下拉 4 项并回显 | 02095 |
| 环节选择后清单收成该环节 | 未覆盖：点选后下拉会回显，清单条数与环节列没有收成该项 |
| 「搜索企业」无命中 | 02096 |
| 「搜索企业」命中「无线」 | 02097 |
| 清单表头 | 02098 |
| 翻到第 2 页 | 02099 |
| 翻页后勾选是否仍挂在原行 | 未覆盖：翻页能换行；同一次里勾选计数、条数和首行没有一起给出「原行仍勾着」的终态 |
| 勾选 1 行再取消 | 02100 |
| 「全选当前结果」再「取消全选」 | 02101 |
| 未勾选时「加入对比篮」 | 02102 |
| 勾选 1 家后「加入对比篮」 | 02103 |
| 「查看详情」抽屉首屏与「工商概况」 | 02104 |
| 详情页签「主要团队」 | 02105 |
| 详情页签「资质荣誉」 | 02106 |
| 详情页签「知识产权」 | 02107 |
| 详情页签「经营财务」 | 02108 |
| 详情页签「供应链关系」 | 02109 |
| 详情页签「关系图谱」 | 02110 |
| 详情页签「舆情动态」 | 02111 |
| 详情页签「风险信息」 | 02112 |
| 详情页签「招投标」 | 02113 |
| 详情再下一级 | 无 |
| 对标结果页出现，城市含北京、上海、苏州 | 00969 金样 |
| 平均技术力、平均商业力、企业密度 | 00970 |
| 对比表六列 | 02117 |
| 不可用指标不以 0 填上 | 00971 |
| 雷达图三个维度 | 02118 |
| 「对比对象 A」锁定深圳 | 02119 |
| 「对比对象 B」5 个选项 | 02120 |
| 「对比对象 B」改为北京市 | 02121 |
| 默认参照下的「相对优势」「相对短板」 | 02122 |
| 对标城市下拉 6 项 | 02123 |
| 关掉「苏州」标签 | 02124 |
| 选链或切对标时的过程页 | 未覆盖：点选和切 Tab 后直接出结果，没有可停留的过程页 |
| 提取失败、对标失败 | 未覆盖：页面没有失败入口，当前环境造不出失败终态 |
| 第二种账号 | 未覆盖：环境只有当前这一个账号 |
| 「查看 HTML 报告」打开后返回 | 00977 |
| 报告目录 7 节 | 02114 |
| 未选链时打开报告 | 02125 |
| 从对标 Tab 打开报告，对象为「深圳企业多城市横向对标」 | 02116 |
| 报告「导出」 | 02115 |
| 报告「付费」 | 未覆盖：没有点出一份独立的报告终态，不把顶栏权益开关写进用例 |
| 「开始分析」当天再点、重新分析、历史任务行 | 无 |
| 系统对比篮里的清空、移除、发起分析 | 无。本页只测清单上的「加入对比篮」 |

## 页面区块 → 用例编号

| 区块 | 用例 |
|------|------|
| 页头与双 Tab | 00960、00974、02094 |
| 区域与产业链 | 00961、02093、02088、00975 |
| 定位结果 | 02089、02090、02091、02092 |
| 企业清单 | 02095、02096、02097、02098、02099、02100、02101、02102、02103 |
| 企业详情 | 02104–02113 |
| 多城市横向对标 | 00969、00970、00971、02117–02124 |
| HTML 报告 | 00977、02114、02115、02116、02125 |

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

> 排列：**主流程 → 备选 → 异常**。保留条正文不改，只从 00960 备注去掉金样。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00960 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 进入深圳企业现状分析页 | 验证侧栏进入深圳企业现状分析页且路由标题与默认 Tab 正确 | 1、系统正常；2、已登录且可访问企业分析侧栏 | 1.点击侧栏「企业分析」→「深圳企业现状分析」 | 1、路由为 /enterprise/shenzhen-enterprise-status-analysis；2、页标题为「深圳企业现状分析」且副标题含产业链位置与竞争力语义；3、默认选中「产业链定位」Tab | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜深圳企业产业链定位 \｜选择目标产业链 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-01 | 主流程-入口路由 / 侧栏进入；接旧 00107 拆分（入口与页头文案收口本条）；筛选区构成归 00961~00963；TRACE 目标态路由差异以现场为准不判 Fail（coverage 开放项 7） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00961 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 区域锁定深圳 | 验证区域选择器锁定深圳且为只读不可切换 | 1、已进入深圳企业现状分析页 | 1.浏览筛选区区域控件；2.点击区域控件 | 1、区域控件为禁用只读态且有明确锁定呈现；2、无可改城市入口且区域锚点保持深圳 | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜深圳企业产业链定位 \｜校验所提取企业范围为深圳 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-06 | 主流程-区域锁定 / 区域只读；接旧 00109 拆分（锁定呈现收口本条；两 Tab 一致性归 00974）；区域控件文案形态（observed-执行时记录，原勘察：「全国热门科创城市/深圳/全部」相关呈现）；后台提取范围黑盒不核 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02093 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 产业链选项 | 验证产业链下拉展开后选项个数与附录一致 | 1、已进入页面；2、下拉尚未点开 | 1.展开产业链下拉 | 1、选项共 15 个，名称见附录A | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-产业链下拉 / 选项个数；页上没有快捷标签，选项只在这个下拉里 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00963 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 未选链空态 | 验证未选产业链时结果区为待选择引导态且无隐藏默认结果 | 1、已进入页面；2、未选定任何产业链 | 1.浏览结果区与页面壳呈现 | 1、结果区为待选择引导态且占位提示先选定产业链；2、页面壳与双 Tab 保留；3、无隐藏默认链结果（无数值与企业清单） | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜深圳企业产业链定位 \｜未选择产业链时不可提取深圳相关企业清单 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-08 | 主流程-未选链空态 / 结果区默认态；接旧 00111（「未完成企业提取时不可标注链中角色」同态合并验证，coverage #9）；空态不报错不白屏（顺带核对）；空态引导文案具体措辞（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02088 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 选链到达定位结果 | 验证从产业链下拉点选人工智能后到达定位结果 | 1、已进入页面；2、尚未选定产业链 | 1.展开产业链下拉；2.点选「人工智能」；3.等待「深圳相关企业清单」出现 | 1、产业链下拉回显「人工智能」；2、页面出现「深圳相关企业清单」；3、清单中有企业行 | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-选链出结果 / 人工智能；金样；本页唯一发起方式 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02089 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 定位指标卡 | 验证定位结果展示四张指标卡 | 1、已点选「人工智能」；2、定位结果已出现 | 1.阅读「产业链定位」下的指标卡 | 1、有「深圳相关企业」「覆盖产业链环节」两张卡；2、有「重点环节企业」「产业链完整度」两张卡；3、每张卡都有数字 | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-定位指标卡 / 四张卡；不把具体数字写成预期 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02090 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 数据更新时点 | 验证页头展示数据更新时点 | 1、已进入深圳企业现状分析页 | 1.阅读页头右侧时点 | 1、页头有「数据更新至」；2、时点文字可见 | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-数据时点 / 页头文案；时点可以是「暂无时点」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02091 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 产业链环节分布 | 验证环节分布图展示四个环节名 | 1、已点选「人工智能」；2、定位结果已出现 | 1.阅读「产业链环节分布」 | 1、区块标题为「产业链环节分布」；2、图中有行业应用、算力芯片、数据标注、算法框架 | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-环节分布 / 分布图；不写柱高 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02092 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 链中角色分布 | 验证角色分布图展示上游中游下游与暂未标注 | 1、已点选「人工智能」；2、定位结果已出现 | 1.阅读「链中角色分布」 | 1、区块标题为「链中角色分布」；2、图中有上游、中游、下游、暂未标注 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-角色分布 / 分布图；不写柱高 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02098 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 企业清单表头 | 验证深圳相关企业清单的表头与页面一致 | 1、已点选「人工智能」；2、清单已出现 | 1.阅读「深圳相关企业清单」表头 | 1、表头依次为选择、企业名称、所在区、产业链环节、链中角色、操作 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-清单表头 / 列名；行上按钮是「查看详情」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02104 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 查看详情首屏 | 验证查看详情打开企业详情并落在工商概况 | 1、清单中已有企业行 | 1.点击首行「查看详情」 | 1、抽屉标题为「企业详情」；2、首屏有法定代表人、成立时间、注册资本、所属产业、链位、统一社会信用代码；3、默认页签「工商概况」含经营范围、注册地址、官网、联系方式 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-企业详情 / 工商概况；无值可以是占位符，不写具体地址 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02105 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 主要团队 | 验证主要团队页签展示姓名与职务 | 1、企业详情抽屉已打开 | 1.点击「主要团队」 | 1、出现表头「姓名」「职务」；2、没有记录时文案为「暂无数据」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 主要团队 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02106 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 资质荣誉 | 验证资质荣誉页签展示类别与认定时间 | 1、企业详情抽屉已打开 | 1.点击「资质荣誉」 | 1、出现表头「类别」「认定时间」；2、没有记录时文案为「暂无数据」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 资质荣誉 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02107 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 知识产权 | 验证知识产权页签展示专利表 | 1、企业详情抽屉已打开 | 1.点击「知识产权」 | 1、表头含专利名称、类型、日期、状态；2、页签里有专利记录 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 知识产权；不写专利全名 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02108 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 经营财务 | 验证经营财务页签展示三项金额 | 1、企业详情抽屉已打开 | 1.点击「经营财务」 | 1、展示总资产、净利润、研发投入；2、没有数的项以占位呈现 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 经营财务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02109 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 供应链关系 | 验证供应链关系页签展示关联方与关系 | 1、企业详情抽屉已打开 | 1.点击「供应链关系」 | 1、出现表头「关联方」「关系」；2、没有记录时文案为「暂无数据」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 供应链关系 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02110 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 关系图谱 | 验证关系图谱页签给出图谱或空态原文 | 1、企业详情抽屉已打开 | 1.点击「关系图谱」 | 1、出现「企业关系图谱」；2、没有图谱时文案为「暂无关系图谱」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 关系图谱；无再下一级入口 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02111 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 舆情动态 | 验证舆情动态页签在无数据时给出原文 | 1、企业详情抽屉已打开 | 1.点击「舆情动态」 | 1、页签文案为「暂无舆情」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 舆情动态 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02112 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 风险信息 | 验证风险信息页签在无数据时给出原文 | 1、企业详情抽屉已打开 | 1.点击「风险信息」 | 1、页签文案为「暂无风险事件」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 风险信息 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02113 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 招投标 | 验证招投标页签展示四列表头 | 1、企业详情抽屉已打开 | 1.点击「招投标」 | 1、表头含公告标题、角色、对手方、日期；2、没有记录时文案为「暂无数据」 | P0 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-详情页签 / 招投标 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00969 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 多城市对标进入 | 验证切换对标 Tab 后视图加载且对标城市含北京上海苏州 | 1、已进入页面；2、已选定一条产业链 | 1.切换到「多城市横向对标」Tab；2.等待对标视图加载完成；3.浏览对标城市呈现 | 1、对标视图加载完成且不报错；2、对标城市含北京、上海、苏州；3、对比以深圳为主体锚点 | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜多城市横向对标分析 \｜纳入北京作为对标城市 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis | M_ENT_CITY_AVG_TECH_POWER | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-05 | 主流程-对标城市池 / Tab 进入与城市构成；金样；接旧 00116 拆分（城市池收口本条，同时覆盖纳入上海/苏州 coverage #20/#21）；本 Tab 现场未深勘，预期按 v8 需规写 observed（开放项 2）；未选链直接切对标 Tab 的形态（observed-执行时记录）；城市池临时默认集合（observed-执行时记录，开放项 1） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00970 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 对标指标构成 | 验证对标视图展示平均技术力平均商业力与企业密度指标 | 1、已切至「多城市横向对标」Tab 且视图加载完成 | 1.浏览对标视图指标区 | 1、指标含平均技术力、平均商业力与企业密度三项；2、对比呈现为深圳与对标城市同口径形态（城市表或雷达） | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜多城市横向对标分析 \｜计算平均技术力 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-11 | 主流程-对标指标构成 / 指标与对比形态；接旧 00116 拆分（指标构成收口本条，同时覆盖计算与展示三项 coverage #23~#28）；算法数值正确性归算法库（SDWJSF/KJZTFWSFK）；对比形态以现场为准（observed-执行时记录，口径=城市表或雷达） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02117 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 城市指标对比表 | 验证城市乘指标对比表的列名完整 | 1、已进入「多城市横向对标」且结果已出现 | 1.阅读「城市 × 指标对比表」表头 | 1、表头依次为对象、平均技术力、平均商业力、企业密度、产业链完整度、数据状态 | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-对标表头 / 城市指标表；不写单元格分数 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00971 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 缺口径指标呈现 | 验证缺口径指标呈现不可用态且空数据有提示不以 0 补齐 | 1、已切至「多城市横向对标」Tab 且视图加载完成 | 1.浏览对标视图各指标与数据呈现 | 1、缺口径指标呈现不可用态且不以 0 或替代指标补齐；2、对标数据为空时呈现空态提示 | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-09 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜多城市横向对标分析 \｜展示商业力 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-12 | 主流程-缺口径指标呈现 / 不可用态；接旧 00116 拆分（缺口径呈现收口本条，同时覆盖展示企业密度与对标空提示 coverage #28/#35）；缺口治理项与升级路径见 coverage 开放项 6（正文不出现）；不可用态形态（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02118 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 同口径雷达 | 验证雷达图按三个维度对比深圳与参照 | 1、已进入「多城市横向对标」且结果已出现 | 1.阅读「同口径多指标雷达对比」 | 1、雷达含平均技术力、企业密度、产业链完整度；2、图例含深圳市与当前参照 | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-对标雷达 / 三个维度 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02119 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 对比对象A | 验证对比对象A固定为深圳且不能改 | 1、已进入「多城市横向对标」 | 1.点击对象A下拉 | 1、控件标题为「对比对象 A」；2、控件为禁用态；3、当前值为「深圳」 | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-对比对象A / 锁定深圳 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02120 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 对比对象B选项 | 验证对比对象B下拉的选项个数与附录一致 | 1、已进入「多城市横向对标」 | 1.展开对象B下拉 | 1、控件标题为「对比对象 B」；2、选项共 5 个，名称见附录E | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-对比对象B / 选项个数 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02122 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 相对优势与短板 | 验证默认参照下给出相对优势和相对短板原文 | 1、已进入「多城市横向对标」；2、「对比对象 B」仍为 NATIONAL | 1.阅读相对优势与相对短板 | 1、所在区块标题为「当前产业链相对观察」；2、「相对优势」列出高于当前参照的指标；3、「相对短板」为「当前可比指标未发现低于参照对象的项」 | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-17 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-相对观察 / 默认参照；默认参照是 NATIONAL |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02123 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 对标城市选项 | 验证对标城市下拉的选项个数与附录一致 | 1、已进入「多城市横向对标」 | 1.展开对标城市下拉 | 1、选项共 6 个，名称见附录D | P0 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-对标城市下拉 / 选项个数；收起时多出来的城市写在「+1...」里 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02114 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 报告目录 | 验证报告页展示七节目录并能读到末节 | 1、已点选一条产业链；2、当前在分析结果页 | 1.点击「查看 HTML 报告」；2.滚动到报告末节 | 1、页内标题为「深圳企业现状分析报告」；2、目录共 7 节，名称见附录C；3、末节标题为「局限性与使用边界」 | P0 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-HTML报告 / 目录七节；不写报告版本时间 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00974 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 双 Tab 共享坐标系 | 验证双 Tab 可往返且返回后已选链与结果态保留 | 1、已选定产业链「人工智能」；2、定位结果已加载 | 1.切换到「多城市横向对标」Tab；2.切换回「产业链定位」Tab | 1、双 Tab 均可见可激活；2、返回「产业链定位」后已选产业链与定位结果保留；3、两 Tab 下区域锚点一致保持深圳 | P1 |  |  |  |  |  | US-SZSTATUS-04 | SZSTATUS-USM-11 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜多城市横向对标分析 \｜将深圳企业群与对标城市进行对比 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-01 | 备选-Tab 切换保留 / 往返状态保留；接旧 00108（共享深圳锚点与产业链坐标系为本条核心）；两 Tab 区域一致性自旧 00109 并入本条（切 Tab 为自然步骤）；对标 Tab 内容详验归 00969~00973 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00975 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 切链重新提取 | 验证下拉改选产业链后区块与清单按新链刷新 | 1、已在「人工智能」下加载结果 | 1.在产业链下拉改选「生物医药」；2.等待刷新完成 | 1、六区块与企业清单按新链刷新；2、产业链下拉回显更新为「生物医药」 | P1 |  |  |  |  |  | US-SZSTATUS-04 | SZSTATUS-USM-12 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜深圳企业产业链定位 \｜产业链变更后重新提取深圳相关企业清单 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-02 | 备选-切链重提取 / 下拉改选；接旧 00113 拆分（改选与刷新收口本条，同时覆盖「按所选产业链限定提取范围」联动证据 coverage #5）；旧链勾选清除与对比篮对象保留待有数据补验（开放项 4）；现场空数据下以区块联动复现记 observed |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02094 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 未选链的对标页 | 验证未选产业链时切到对标仍是同一句引导 | 1、已进入页面；2、尚未选定产业链 | 1.点击「多城市横向对标」 | 1、仍显示「请先选择产业链以加载深圳现状分析」；2、页面没有城市对比表 | P1 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-未选链切对标 / 引导仍在 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02095 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 产业链环节选项 | 验证环节下拉有四项并且能回显所选项 | 1、已点选「人工智能」；2、清单已出现 | 1.展开占位为「全部环节」的下拉；2.点选「行业应用」 | 1、选项共 4 个，名称见附录B；2、下拉回显「行业应用」 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-环节下拉 / 回显；回显之后清单条数没有收成该环节，不把收窄写成预期 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02097 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 按名称搜索 | 验证搜索无线后清单只留下名称含该词的行 | 1、已点选「人工智能」；2、清单已出现 | 1.在「搜索企业」输入「无线」；2.回车 | 1、当前结果家数小于搜索前；2、可见行的企业名称都含「无线」 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-搜索命中 / 搜索企业；不写命中条数，不写企业全名 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02099 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 清单翻页 | 验证翻到第2页后清单换成另一批企业 | 1、已点选「人工智能」；2、搜索框为空 | 1.点击分页里的「2」 | 1、清单首行与第 1 页不同；2、总条数文案仍在 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-清单翻页 / 第2页；不写总条数，不写企业全名 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02100 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 勾选与取消 | 验证勾选一行再取消时已选计数跟着变 | 1、清单已出现；2、当前没有勾选 | 1.勾选清单首行；2.再次点击该勾选框 | 1、首次勾选后已选计数为 1 家；2、再次点击后已选计数为 0 家 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-单行勾选 / 已选计数 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02101 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 全选当前结果 | 验证全选当前结果后可以取消并且已选回到零 | 1、清单已出现；2、当前没有勾选 | 1.点击「全选当前结果」；2.点击「取消全选」 | 1、按钮文案变为「取消全选」；2、已选家数等于当前页勾选行数；3、再点后已选计数为 0 家 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-全选当前结果 / 取消全选；再点后按钮写回「全选当前结果」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02102 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 未勾选不可加入 | 验证没有勾选时加入对比篮不可点击 | 1、清单已出现；2、没有任何勾选 | 1.保持清单行都未勾选 | 1、「加入对比篮」为不可点击状态 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-加入对比篮 / 未勾选 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02103 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 加入对比篮成功 | 验证勾选一家后加入对比篮出现成功提示 | 1、清单已勾选 1 家 | 1.点击「加入对比篮」 | 1、提示「已将 1 家企业加入对比篮」 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-加入对比篮 / 勾选一家；对比篮内部的清空和发起不在本页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00977 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 查看 HTML 报告 | 验证查看报告可打开且返回后页面筛选态保留 | 1、已进入页面；2、已选定一条产业链 | 1.点击「查看 HTML 报告」；2.关闭报告返回页面 | 1、报告以浮层或新页打开且内容可读不报错；2、返回后产业链、Tab 与筛选态保留 | P1 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | T13 \｜深圳企业产业链定位 \｜展示深圳相关企业清单 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-04 | 备选-HTML 报告 / 报告入口；接旧 00117；报告入口为页面级能力非 T13 独立功能点（按 as-built 现状验证不判 Fail）；报告正文结构与是否含定位结论（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02115 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 导出报告 | 验证点击导出后只出现付费说明且没有文件 | 1、已打开 HTML 报告 | 1.点击「导出」 | 1、提示「付费用户可导出报告 PDF」；2、没有文件被下载 | P1 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-报告导出 / 未付费提示；提示后半句指向顶栏权益开关，本条不打开该开关 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02116 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 对标页打开报告 | 验证从对标页打开的报告对象写的是多城市横向对标 | 1、已点选一条产业链；2、当前 Tab 为「多城市横向对标」 | 1.点击「查看 HTML 报告」 | 1、报告对象为「深圳企业多城市横向对标」；2、报告类型为「深圳企业现状分析」 | P1 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-报告对象 / 随当前 Tab；返回路径见 00977 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02125 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 未选链打开报告 | 验证未选产业链时仍能打开报告页 | 1、已进入页面；2、尚未选定产业链 | 1.点击「查看 HTML 报告」 | 1、页面变为报告页；2、页内标题为「深圳企业现状分析报告」 | P1 |  |  |  |  |  | US-SZSTATUS-01 | SZSTATUS-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-未选链报告 / 直接打开；引导句不再出现 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02121 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 对比对象改为北京 | 验证把对比对象B改成北京市后短板跟着变 | 1、已进入「多城市横向对标」；2、结果已出现 | 1.展开对象B下拉；2.点选「北京市」 | 1、「当前参照」变为北京市；2、「相对短板」出现低于该参照的说明 | P1 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-17 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-切换参照 / 北京市；不写哪一项低于参照 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02124 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 移除苏州 | 验证关掉苏州标签后对比里不再有苏州 | 1、对标城市标签里有「苏州」 | 1.点击「苏州」标签上的关闭 | 1、对标城市标签里不再有苏州；2、对比表里不再有苏州一行 | P1 |  |  |  |  |  | US-SZSTATUS-03 | SZSTATUS-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-移除对标城市 / 关掉苏州；没有取消框，点关闭即移除 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02096 | 科技专题战略分析 | 企业分析 | 深圳企业现状分析 |  | 深圳企业现状分析 | 搜索无企业 | 验证搜索不存在的名称后清单变为空态原文 | 1、已点选「人工智能」；2、清单已出现 | 1.在「搜索企业」输入「不存在的企业XYZ」；2.回车 | 1、清单文案为「当前条件下暂无企业」；2、已选计数与当前结果都是 0 家 | P1 |  |  |  |  |  | US-SZSTATUS-02 | SZSTATUS-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.5 | 待 A 线回填 | TRACE-ENT-SZSTATUS.yaml | /enterprise/shenzhen-enterprise-status-analysis |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 异常-搜索无命中 / 空清单 |

---

## 2. 附录

**附录A · 产业链下拉（15）**  
集成电路、生物医药、人工智能、新能源、低空经济、量子信息、海洋经济、智能机器人、外资企业、高新技术企业、小微企业、上市企业、专精特新、小巨人、链主龙头

**附录B · 产业链环节（4）**  
行业应用、算力芯片、数据标注、算法框架

**附录C · 报告目录（7）**  
报告身份、执行摘要、对象与范围、关键发现、证据与分析、数据来源与生成说明、局限性与使用边界

**附录D · 对标城市下拉（6）**  
北京、上海、苏州、广州、杭州、成都

**附录E · 对比对象 B（5）**  
北京市、上海市、苏州市、广州市、NATIONAL

---

## 3. 红线自检（2026-10-18 对照重写）

| 项 | 结果 |
|----|------|
| 在册条数 | 保留 9 + 新号 38 = 47（02088–02125） |
| 主流程 / 备选 / 异常 | 30 / 16 / 1，主流程不少于后两者之和 |
| 预期 6 点及以上 | 0 |
| 金样 | 02088、00969，都走到结果页 |
| 红线 7 | 前置、步骤、预期、功能项扫描内部评审、评审模式、评审开关、人设面板、需求追溯、零泄漏 = 0 |
| 用到的最大号 | 02125。02126–02187 不写入册 |

## 4. 序号台账

| 测试类型 | 在册 | 作废或删除（不复用） | 本段下一号 |
|----------|------|----------------------|------------|
| FUNC | 00960、00961、00963、00969、00970、00971、00974、00975、00977；02088–02125 | 00962、00964、00965、00966、00967、00968、00972、00973、00976 作废；00978 删除 | 02126（段内剩余，本册不占） |

`code-registry.yaml` 本步不改。

## 5. 旧号处置

| 旧号 | 处置 | 新号 |
|------|------|------|
| 00960 | 保留。去掉金样。入口本身不是结果主线 | — |
| 00961 | 保留 | — |
| 00962 | 作废。页上没有快捷标签，8 个名字只是下拉的一部分 | 02093 |
| 00963 | 保留 | — |
| 00964 | 作废。快捷标签不存在，选链改从下拉走到结果 | 02088 |
| 00965 | 作废。选链后直接出结果，没有可停留的过程页 | 清单未覆盖 |
| 00966 | 作废。步骤点的是不存在的快捷标签，区块名与现场四卡两图加清单不一致 | 02088、02089、02090、02091、02092 |
| 00967 | 作废。表头漏了「选择」「产业链环节」 | 02098 |
| 00968 | 作废。选链后清单有数据，空态要靠搜索打出来 | 02096 |
| 00969 | 保留，仍为金样 | — |
| 00970 | 保留 | — |
| 00971 | 保留 | — |
| 00972 | 作废。写了现场没有走到的「不足 3 项就降级」 | 02122、02121 |
| 00973 | 作废。切到对标后直接出表，没有可停留的计算过程 | 清单未覆盖 |
| 00974 | 保留 | — |
| 00975 | 保留。下拉改到「生物医药」后回显并刷新，已点到 | — |
| 00976 | 作废。预期按空数据写，现场有数据，全选会变成「取消全选」 | 02101、02100 |
| 00977 | 保留。补了目录、导出和未选链打开 | 02114、02115、02125 |
| 00978 | 删除。整条是评审开关，旧号不复用 | — |
