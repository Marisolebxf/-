# 智能服务集群-科技专题服务系统测试用例

> **模块**：企业查询（SEARCH）· **完整版**  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v1.2 · 2026-08-09（预期结果加字段/页签勾选粒度；详情分 SEARCH 容器 vs ENT-PROFILE 冒烟）  
> **规范**：`agent-delivery/qa-test-case-spec.md` v1.0  
> **任务**：`ENT-MOD-SEARCH-QA-ACCEPT-L01`  
> **执行仓 / 环境**：`lumen-ui-topic` · `http://192.168.88.50:30892`（`VITE_APP_USE_MOCK=false` 联调）  
> **备用 DEMO 仓**：`demo-ui-topic`（仅交互走查；结论须标注 DEMO）  
> **USM / TRACE**：`产品整体定义/E1-企业查询/USM-…` · `TRACE-E1-ENT-SEARCH-企业查询.yaml`  
> **原始需求**：`bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.2.3`  
> **入口**：登录 → 侧栏「企业分析」→「企业查询」· `/enterprise/enterprise-search`  
> **交付口径**：INTEG（前端 → Java `/topic/v1` → 检索服务）；断链须记 Blocked/降级说明  
> **监管**：`human:黄敬洲`  
> **维护**：`agent:qa-agent`

### 测试分层（对齐派单包）

| 层级 | 范围 | 用例号 |
|------|------|--------|
| **必测 Goal** | S-T2 初始引导 + S-T1 筛选可用 | 见覆盖矩阵「Goal」列 |
| **Stretch** | S-T3 查企业/结果硬化 | Goal=Stretch |
| **完整库（本文件）** | US-E1-SCH-01～08 全验收点原子化；字段/页签见 §0.1 | 00001～00014 + 00030～00045 |
| **暂缓不测 Fail** | SCH-06 跨模块完整接力、SCH-07 导出完整链路 | 已登记但标 `暂缓`；出现问题记开放项，不单独判 Theme Fail |

裁剪勿判 Fail：Q033（无 LLM）、Q034（仅长卡片）、Q036（无复杂 AND/OR）。

---

## 0. 覆盖矩阵（故事 → 用例）

| 故事 | 验收要点（摘要） | 用例编号 | Goal |
|------|------------------|----------|------|
| US-E1-SCH-01 | 查企业名称关键词；长卡片；进画像 | 00001, 00041 | Stretch / 完整 |
| US-E1-SCH-02 | 智能搜索多字段；无 LLM 承诺 | 00002 | 完整 |
| US-E1-SCH-03 | 四层主视觉；示例回填；热门待应用；最近检索；普通查询无方案 | 00003, 00004, 00005, 00030, 00031, 00032 | **Goal S-T2** |
| US-E1-SCH-03 | 评审模式标题溯源 | 00033 | 完整 |
| US-E1-SCH-04 | 条件叠加；无嵌套；Footer；方案模板；清空 | 00007, 00008, 00034, 00035, 00036 | **Goal S-T1** |
| US-E1-SCH-05 | 长卡片排序；全选本页；画像抽屉；再筛；双空态；区县级联 | 00009, 00010, 00011, 00037, 00038, 00039 | Goal 触点 / Stretch |
| US-E1-SCH-05 | 业务/评审全选一致 | 00040 | 完整 |
| US-E1-SCH-06 | 加篮去重角标；批量契约（跨模块完整链路暂缓） | 00013, 00042 | 暂缓/完整登记 |
| US-E1-SCH-07 | 导出入口与上限提示（完整异步链路暂缓） | 00014, 00043 | 暂缓 |
| US-E1-SCH-08 | 推荐动作受限；0 命中无推荐；理由/机制分层 | 00006, 00012, 00044 | **Goal S-T2** |
| 联调 | 地区/字典经 Java；Mock 标识；断链可读 | 00045 | **Goal S-T1** |

---

## 0.1 字段 / 页签勾选附录（与人工勾选版一致）

**分层**：A=SEARCH 可判 Fail · B=页签冒烟（缺页签可 Fail）· C=页内指标深度→开放项 Q010/ENT-PROFILE。

| 清单 | 用于 | 要点 |
|------|------|------|
| R 推荐卡 | 00006 / 00044 | 名称·状态·资质·产业·区域·单企理由；仅查看画像/加入对比；无以此查询/无 Logo；业务态无机制文案 |
| L 结果长卡 | 00001 / 00009 | 无 Logo；状态/资质/产业；有效专利数·最新营收·成立时间·综合竞争力(ⓘ)；查看画像/加入对比；无双视图 |
| D-A 抽屉容器 | 00006 / 00011 | 不跳路由；企业头部+内容区；业务态无溯源/Mock 版本常驻；关后保留查询态；企业名与查看画像同一抽屉 |
| D-B 页签冒烟 | 00006 / 00011 | 默认工商概况；十页签：工商概况、主要团队、资质荣誉、知识产权、经营财务、供应链关系、关系图谱、舆情动态、风险信息、招投标（对齐 E-25 / ENT-PROFILE） |

人工执行清单全文：`agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01-人工测试用例.md`。

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00001 | 企业分析 | 企业查询 | 查企业 | 名称关键词 | 企业查询 | 查企业召回 | 按企业名称关键词模糊查询并得到长卡片结果 | 1、系统正常；2、已登录可访问企业查询 | 1.切「查企业」确认提示文案；2.输入已知企业名称关键词并搜索；3.按清单 L 核对长卡片字段；4.点企业名打开详情并按清单 D 核对 | 1、提示为「输入企业名称关键词」；2、无 Logo 横向长卡片；3、卡片可见：名称、状态/资质/产业标签、有效专利数、最新营收、成立时间、综合竞争力(ⓘ)、查看画像/加入对比；4、抽屉：当前页不跳路由、有企业头部与内容区、关闭后保留查询态；5、页签冒烟见备注 | P0 | | | | | | US-E1-SCH-01 | E1-SCH-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=company | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | Stretch；详情页签清单 D-B / Q010 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00002 | 企业分析 | 企业查询 | 智能搜索 | 多字段关键词 | 企业查询 | 智能搜索召回 | 多字段关键词匹配且不承诺 LLM | 1、系统正常；2、默认智能搜索可用 | 1.停在「智能搜索」；2.输入产业/技术/区域等线索词并搜索；3.观察结果与文案 | 1、返回横向长卡片结果或明确空态；2、界面无「大模型/意图识别/自然语言理解」能力承诺 | P0 | | | | | | US-E1-SCH-02 | E1-SCH-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.2 | E-22 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=smart | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | Q033 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00003 | 企业分析 | 企业查询 | 初始引导 | 蓝色主视觉层级 | 企业查询 | 搜索主视觉 | 普通查询顶部四层顺序与分行 | 1、进入企业查询默认智能搜索 | 1.观察顶部区域自上而下结构；2.确认示例查询与热门场景是否分行 | 1、固定为：检索模式 → 搜索框 → 示例查询 → 热门场景；2、示例与热门各占独立一行；3、蓝色搜索主视觉可见 | P0 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2** · DEC-HERO |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00004 | 企业分析 | 企业查询 | 初始引导 | 示例查询 | 企业查询 | 示例回填 | 点击示例只回填不自动提交 | 1、初始态可见示例查询 | 1.点击任一「示例查询」；2.观察搜索框与结果区；3.再手动点搜索 | 1、搜索框回填示例词；2、**不**自动进入结果检索态；3、手动搜索后进入有结果或空态 | P0 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00005 | 企业分析 | 企业查询 | 初始引导 | 热门场景 | 企业查询 | 热门进高筛 | 热门场景进入高级筛选且条件待应用 | 1、初始态可见热门场景 | 1.点击任一「热门场景」；2.观察是否进入高级筛选及条件状态；3.点击「应用筛选」 | 1、进入高级筛选字段库并带入预置条件；2、条件为待应用，**不**直接出结果；3、应用后进入结果态；4、高筛页不继承蓝色主视觉 | P0 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=advanced | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00006 | 企业分析 | 企业查询 | 初始引导 | 推荐企业 | 企业查询 | 初始推荐 | 初始空态展示推荐企业且动作受限 | 1、未执行主查询的初始态 | 1.核对推荐区标题与卡片字段（名称/状态/资质/产业标签/区域/单企推荐理由）；2.确认动作仅查看画像、加入对比且无「以此查询」、无 Logo；3.业务态无机制说明；4.点查看画像按清单 D 核对抽屉 | 1、有「推荐企业」分区；2、卡片字段与理由可见（空值须有结构占位）；3、仅两动作、无「以此查询」、无 Logo；4、无 Top30/倒排/非个性化/Mock 机制文案；5、抽屉：不跳路由、有头部与内容、业务态无溯源/Mock 版本常驻；6、页签冒烟见备注 | P1 | | | | | | US-E1-SCH-08 | E1-SCH-USM-08 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-33/E-34 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2**；D-B→ENT-PROFILE/Q010 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00007 | 企业分析 | 企业查询 | 高级筛选 | 条件叠加 | 企业查询 | 简化条件构造 | 逐项添加条件并应用，无复杂嵌套 UI | 1、进入高级筛选 | 1.添加地区等条件；2.再叠加规模/资质等；3.点击应用筛选；4.确认无任意 AND/OR 组嵌套编辑器 | 1、条件可简单叠加并出结果；2、无任意条件组嵌套；3、条件摘要可读 | P0 | | | | | | US-E1-SCH-04 | E1-SCH-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=advanced | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** · Q036 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00008 | 企业分析 | 企业查询 | 高级筛选 | Footer | 企业查询 | 固定 Footer | 展开/结果态共用底边 Footer 且主按钮原位切换 | 1、高级筛选可展开 | 1.展开字段库观察 Footer；2.应用进入结果态再观察 Footer；3.看主按钮文案变化 | 1、Footer 吸附画框底边，保存/使用方案/清空不换位；2、应用后主按钮由「应用筛选」原位变为「编辑高级筛选」；3、导出不在该 Footer | P1 | | | | | | US-E1-SCH-04 | E1-SCH-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=advanced | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** · DEC-FOOTER |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00009 | 企业分析 | 企业查询 | 结果列表 | 形态与排序 | 企业查询 | 长卡片结果 | 仅长卡片形态且四类排序可用 | 1、已有非空结果列表 | 1.确认无卡片/表格双视图；2.按清单 L 核对字段常驻；3.分别按综合竞争力、有效专利数、最新营收、成立时间排序；4.打开综合竞争力 ⓘ | 1、始终横向长卡片无 Logo；2、卡上同时可见有效专利数/最新营收/成立时间/综合竞争力(ⓘ)；3、四类排序均可执行；4、ⓘ 可打开指标说明 | P0 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | E-30 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | M_ENT_COMPETITIVENESS_SCORE | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | Stretch · Q034 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00010 | 企业分析 | 企业查询 | 结果列表 | 全选本页 | 企业查询 | 三态选择 | 全选本页三态与翻页/再筛清选择 | 1、结果≥2 条且可分页或可再筛 | 1.观察全选三态；2.全选本页后翻页或改排序；3.结果内再筛；4.空结果页观察全选 | 1、未选/半选/全选可辨；2、翻页/再筛/排序/重查后选择被清除；3、空结果时全选禁用；4、不跨页全选 | P0 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | E-23 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | Stretch · DEC-SELECT-ALL |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00011 | 企业分析 | 企业查询 | 结果列表 | 画像抽屉 | 企业查询 | 详情不跳转 | 打开企业详情大抽屉：容器必验 + 页签冒烟 | 1、有结果列表 | 1.点企业名称打开抽屉；2.核对企业头部与内容区、业务态无溯源/Mock 版本常驻；3.确认默认「工商概况」且十页签名称存在（工商概况/主要团队/资质荣誉/知识产权/经营财务/供应链关系/关系图谱/舆情动态/风险信息/招投标）；4.（可选）从查看画像再开；5.关闭后核对查询态 | 1、当前页同一套抽屉且不跳路由；2、有企业头部与业务内容区；3、十页签名称齐且默认工商概况；4、关闭后条件/列表/分页或滚动/已选保留；5、页签内字段深度不归本用例 Fail（Q010/ENT-PROFILE） | P0 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | Stretch；页签对齐 E-25/ENT-PROFILE |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00012 | 企业分析 | 企业查询 | 空态 | 主查询0命中 | 企业查询 | 纠错空态 | 0 命中展示纠错且不推推荐 | 1、可构造无结果关键词 | 1.输入必无命中词搜索；2.观察空态动作与是否出现推荐 | 1、提供改词/清空/切模式/进高筛等纠错；2、**不**展示推荐企业 | P1 | | | | | | US-E1-SCH-08 | E1-SCH-USM-08 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2**/Stretch |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00013 | 企业分析 | 企业查询 | 对比篮接力 | 加入对比 | 企业查询 | 加入对比篮 | 结果加入系统对比篮且无页内聚合角标 | 1、有结果；2、系统对比篮入口可见 | 1.确认结果工具栏无页内「对比篮」聚合按钮/数量角标；2.对单企执行加入对比篮；3.查看 Shell 角标；4.点短暂「查看对比篮」（若有） | 1、无页内常驻对比篮聚合入口；2、加入成功且 Shell 红色角标同步；3、查看反馈只展开系统浮层 | P1 | | | | | | US-E1-SCH-06 | E1-SCH-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.6 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **暂缓**完整跨模块 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00014 | 企业分析 | 企业查询 | 导出 | 当前结果 | 企业查询 | 异步导出 | 导出入口与上限/权限提示 | 1、有结果；2、账号导出策略已知 | 1.在结果工具区找到导出；2.尝试导出或观察禁用；3.核对 ≤1000 及水印/资产中心口径 | 1、导出在结果工具区不在高筛 Footer；2、超限或无权限有明确说明；3、完整异步链路本轮可记开放项 | P2 | | | | | | US-E1-SCH-07 | E1-SCH-USM-07 | 科技信息展示系统和科技专题服务系统.md | Q035 | Q035 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **暂缓** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00030 | 企业分析 | 企业查询 | 初始引导 | 最近检索 | 企业查询 | 最近检索恢复 | 最近检索可恢复查询上下文 | 1、已执行过至少一次普通查询产生历史 | 1.回到初始/普通查询态；2.点击「最近检索」一条；3.必要时点搜索/应用 | 1、恢复对应关键词或条件上下文；2、可进入可解释结果态；3、普通查询区**不**出现「查询方案」入口 | P0 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00031 | 企业分析 | 企业查询 | 初始引导 | 访客最近检索 | 企业查询 | 访客不落库 | 访客不记录个人最近检索 | 1、可切换至访客/未登录或无个人历史角色（按环境能力） | 1.以访客或等价低权限进入；2.执行查询；3.刷新或重进观察最近检索 | 1、不出现可归因个人的最近检索写入；或明确不可用；2、与登录用户行为可区分 | P2 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | 环境无访客则 Blocked |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00032 | 企业分析 | 企业查询 | 智能搜索+查企业 | 热门场景双模式 | 企业查询 | 热门双入口 | 智能搜索与查企业页热门均进字段库 | 1、两种模式均可切换 | 1.在智能搜索点热门场景；2.返回后切查企业再点热门（若查企业也展示热门） | 1、均进入高级筛选并带入待应用条件；2、不直接出结果 | P1 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2** 补强 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00033 | 企业分析 | 企业查询 | 评审模式 | 标题溯源 | 企业查询 | 内部评审挂载 | 评审模式显示章节溯源，关闭后隐藏 | 1、可开启全局内部评审模式 | 1.关闭评审模式观察标题；2.开启后观察页面标题/推荐标题；3.再关闭 | 1、开启后可见源需求章节溯源挂载；2、关闭后完整隐藏；3、不改变查询结果与选择集合 | P1 | | | | | | US-E1-SCH-03 | E1-SCH-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | review_trace_contract |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00034 | 企业分析 | 企业查询 | 高级筛选 | 查询方案保存 | 企业查询 | 方案模板 | 保存方案仅含高筛条件不含关键词/结果 | 1、高筛已构造若干条件 | 1.点击「保存为查询方案」并命名；2.清空条件；3.「使用查询方案」恢复 | 1、可保存；2、恢复后回到编辑态条件一致；3、不恢复智能搜索/查企业关键词；4、不恢复企业结果名单；5、需用户再点应用才出结果 | P0 | | | | | | US-E1-SCH-04 | E1-SCH-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=advanced | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** · DEC-PLAN |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00035 | 企业分析 | 企业查询 | 高级筛选 | 清空条件 | 企业查询 | 清空 | Footer「清空条件」可用且不换位 | 1、高筛已有条件 | 1.确认清空按钮在 Footer 固定位；2.点击清空；3.再应用或观察编辑态 | 1、条件被清空；2、按钮位置相对保存/使用方案不变；3、页面不崩溃 | P1 | | | | | | US-E1-SCH-04 | E1-SCH-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=advanced | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00036 | 企业分析 | 企业查询 | 高级筛选 | 地区字段 | 企业查询 | 全国地区树 | 企业所属地区为全国级联非死写深圳 | 1、进入高筛字段库 | 1.打开「企业所属地区」或等价字段；2.浏览省市区选项 | 1、全国省市区树/级联可选；2、非仅深圳区县死写 | P0 | | | | | | US-E1-SCH-04 | E1-SCH-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=advanced | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00037 | 企业分析 | 企业查询 | 结果列表 | 结果内再筛 | 企业查询 | 再筛 | 结果内再筛可解释且可清除 | 1、已有非空高筛或搜索结果 | 1.在结果工具条改一项再筛；2.观察列表变化；3.清除/放宽该再筛 | 1、条数或内容变化可解释；2、清除后放宽/恢复；3、不卡死 | P0 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | E-23 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** 触点 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00038 | 企业分析 | 企业查询 | 结果列表 | 再筛空态 | 企业查询 | 局部空态 | 结果内再筛 0 命中保留原方案 | 1、有结果且可构造再筛无命中 | 1.施加极窄结果内再筛至 0 命中；2.观察空态与工具区 | 1、保留原查询方案与结果操作区；2、仅列表区局部空态；3、与主查询 0 命中（无推荐+纠错）表现可区分 | P1 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00039 | 企业分析 | 企业查询 | 结果列表 | 注册区县再筛 | 企业查询 | 四级地域 | 注册区县复用四级地域级联 | 1、结果态可见注册区县/地域再筛 | 1.打开注册区县筛选；2.按省→市→区县逐级选择 | 1、四级（或产品定义的级联）可选；2、结果按最终选中行政地域收窄；3、对齐 Q037 | P1 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | Q037 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | Q037 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00040 | 企业分析 | 企业查询 | 结果列表 | 全选与评审 | 企业查询 | 模式不变选择 | 业务/评审模式共用选择集合 | 1、结果页有可选企业 | 1.业务模式勾选若干；2.开启评审模式观察选择；3.关闭评审模式 | 1、选择集合不变；2、全选无评审说明挂载（review_mounts 空）；3、不因模式切换清空 | P1 | | | | | | US-E1-SCH-05 | E1-SCH-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-23 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00041 | 企业分析 | 企业查询 | 查企业 | 非名称字段 | 企业查询 | 召回边界 | 查企业不按信用代码等非名称命中 | 1、已知某企业信用代码但名称不同 | 1.查企业模式下仅输入信用代码或曾用名片段（非现用名）；2.搜索 | 1、不因信用代码/曾用名单独命中（或明确无结果）；2、与「仅企业名称」口径一致 | P1 | | | | | | US-E1-SCH-01 | E1-SCH-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-20 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search?mode=company | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | 数据不足则 Blocked |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00042 | 企业分析 | 企业查询 | 对比篮 | 批量与重复 | 企业查询 | 批量加篮 | 全选本页与逐项加篮同一契约 | 1、结果多条；2、对比篮可用 | 1.逐项加 1 家；2.全选本页批量加入；3.对已加入项再加入 | 1、批量与逐项权限/反馈一致；2、重复有已存在反馈；3、跨模块带参完整链路仍标暂缓 | P2 | | | | | | US-E1-SCH-06 | E1-SCH-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.6 | E-26 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **暂缓**深度 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00043 | 企业分析 | 企业查询 | 导出 | 范围选项 | 企业查询 | 导出范围 | 支持单企/已选/当前结果口径可见 | 1、有结果且可多选 | 1.打开导出菜单/对话框；2.核对手选范围选项 | 1、可见单企业/已选/当前结果等范围；2、有数量上限提示；3、完整 PDF 水印链路暂缓 | P2 | | | | | | US-E1-SCH-07 | E1-SCH-USM-07 | 科技信息展示系统和科技专题服务系统.md | Q035 | Q035 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search#results | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **暂缓** |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00044 | 企业分析 | 企业查询 | 推荐 | 理由与机制 | 企业查询 | 推荐分层 | 业务态显示理由；机制说明仅评审模式 | 1、初始推荐可见；2、可切换评审模式 | 1.业务态查看推荐卡是否有单企理由；2.开启评审模式看机制/Mock/策略说明；3.关闭后机制说明消失 | 1、业务态可有单企推荐理由；2、Top30/竞争力倒排/非个性化/Mock 等机制说明仅评审模式；3、关闭后隐藏 | P1 | | | | | | US-E1-SCH-08 | E1-SCH-USM-08 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | E-33/E-34 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T2** 补强 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00045 | 企业分析 | 企业查询 | 联调 | 数据路径 | 企业查询 | Java 门面 | 地区/字典经网关 Java；断链可读 | 1、浏览器 Network 可观察；2、INTEG 环境 | 1.打开高筛触发地区/字典请求；2.确认经 `/topic` 或网关而非直连 Python；3.可选断网一次 | 1、请求走前端→Java 网关；2、有 Mock 则角标可辨；3、断链有用户可读提示不白屏 | P0 | | | | | | US-E1-SCH-04 | E1-SCH-USM-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.1.1 | E-25 | TRACE-E1-ENT-SEARCH-企业查询.yaml | /enterprise/enterprise-search | | INTEG | ENT-MOD-SEARCH-QA-ACCEPT-L01 | | **Goal S-T1** 联调 |

---

## 2. Goal 必测清单（人工优先）

| 顺序 | 用例编号 | Theme | 一句话 |
|------|----------|-------|--------|
| 1 | 00003 | S-T2 | 四层蓝色主视觉 |
| 2 | 00004 | S-T2 | 示例只回填 |
| 3 | 00005 | S-T2 | 热门待应用 |
| 4 | 00030 | S-T2 | 最近检索恢复 |
| 5 | 00006 | S-T2 | 推荐可点画像 |
| 6 | 00044 | S-T2 | 推荐理由/机制分层 |
| 7 | 00012 | S-T2/T3 | 0 命中无推荐 |
| 8 | 00036 | S-T1 | 全国地区树 |
| 9 | 00007 | S-T1 | 条件叠加应用 |
| 10 | 00008 | S-T1 | Footer 切换 |
| 11 | 00034 | S-T1 | 查询方案模板 |
| 12 | 00035 | S-T1 | 清空条件 |
| 13 | 00037 | S-T1 | 结果内再筛 |
| 14 | 00045 | S-T1 | 联调路径 |

Stretch 建议：00001、00009、00010、00011。

---

## 3. 覆盖自检

- [x] US-E1-SCH-01～08 均有对应用例
- [x] Sprint Goal S-T1/S-T2 要点全覆盖
- [x] SCH-06/07 已登记并标暂缓
- [x] Q033/Q034/Q036 裁剪写入备注
- [x] 编号：`00001`～`00014` + `00030`～`00045`（`00015`～`00029` 留给 COMPARE）
- [x] 人工执行记录空表：`qa/test-records/KJZTFWXT/SEARCH/FUNC-企业查询-记录-待填.md`

## 4. 序号台账（本文件）

| 测试类型 | 本模块已用 | 全局下一号（KJZTFWXT-FUNC） |
|----------|------------|-----------------------------|
| FUNC | 00001–00014, 00030–00045 | 见 `qa/code-registry.yaml` → **46** |

## 5. 关联产物

| 产物 | 路径 |
|------|------|
| 人工勾选执行版 | `agent-handoffs/企业战略分析-ENT/ENT-MOD-SEARCH-QA-ACCEPT-L01-人工测试用例.md` |
| 派单包 | `…/ENT-MOD-SEARCH-QA-ACCEPT-L01-派单包.md` |
| 执行记录空表 | `qa/test-records/KJZTFWXT/SEARCH/FUNC-企业查询-记录-待填.md` |
