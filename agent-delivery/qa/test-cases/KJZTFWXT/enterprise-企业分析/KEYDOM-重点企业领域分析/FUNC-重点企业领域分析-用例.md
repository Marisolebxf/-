# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md` v1.0  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v1.0 · 2026-10-12  
> **模块**：重点企业领域分析（KEYDOM / catalog `ent-key-domain` / A 线 **T10 重点企业领域分布分析**，20 条功能点）  
> **环境**：http://111.198.38.90:50892/ · 账号 `admin` / `123456`（已在业务页且 URL 不含 `/login` 则不要登出）  
> **入口**：侧栏「企业分析」→「重点企业领域分析」  
> **路由**：`/enterprise/key-enterprise-analysis`，query 须含 `view=domain` 或 `workspace=domain`  
> **禁止**：把「重点企业类型分析」（T09 / `view=type`）写成用例；隔离归 00046  
> **USM / Wireframe**：`agent-handoffs/产品整体定义/E-20_E-22-重点企业分析/USM-ENT-KEYENT.md`（领域节）  
> **TRACE**：`TRACE-ENT-KEYENT.yaml`  
> **原始需求**：`bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.2.3`（E-21）  
> **交付口径**：INTEG（前端 → Java → Python `/internal/*`）  
> **功能点 / 功能点ID**：见同目录 `coverage-fp.md`（v8 T10 全 20 条映射）  
> **关联任务**：`QA-KJZTFWXT-BLINE-CASE-ENT-L01`  
> **维护**：agent:qa-agent · 监管 human:黄敬洲

**as_built 摘要（写期望用，不升 Fail）**：入口为侧栏二级（与类型分析同壳层）；空态主区「领域分析对象 / 待选择分析对象」+ 引导文案「可从企业查询、重点企业分析、总览或企业画像中加入企业」；分析对象从**系统对比篮**发起（勾选企业 →「发起分析」→ 六类型单选弹窗 → 选「重点企业领域分布分析」→「下一步：前往配置」，URL 带 `source=compare-basket&analysis_type=key-enterprise-domain&return_context_id=cmp-*`）；结果态四大区块：领域布局概览 / 企业领域覆盖 / 跨领域布局 / 重点领域分布；KPI 有 ⓘ 指标说明与「口径待甲方确认（Q013）」角标；页头有「查看 HTML 报告」与需求追溯（评审态）。

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00062 | 企业分析 | 重点企业领域分析 | 入口与路由 | 侧栏进领域 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 展示企业业务与产业领域关联结果 | 从领域菜单进入领域分析页，URL 含 domain，不落到类型看板 | 1、系统正常；2、已登录 | 1.点侧栏「企业分析」→「重点企业领域分析」；2.读地址栏与 H1；3.确认主区空态 | 1、进入 `/enterprise/key-enterprise-analysis` 且 query 含 `view=domain` 或 `workspace=domain`；2、H1 为「重点企业领域分析」；3、空态显示「领域分析对象 / 待选择分析对象」而非类型看板内容 | P0 | | | | | | US-KEYENT-01 | KEYENT-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 展示企业业务与产业领域关联结果 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | 与 T09（00046）互为隔离反向 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00063 | 企业分析 | 重点企业领域分析 | 分析对象 | 对比篮发起 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 自动映射企业业务至预设产业领域 | 空态引导从对比篮收集企业并六类型弹窗可选领域分析 | 1、已进入领域页；2、对比篮有 ≥1 家企业 | 1.点「打开对比篮」；2.勾选 1 家企业；3.点「发起分析」；4.观察六类型单选；5.选「重点企业领域分布分析」点「下一步：前往配置」 | 1、弹窗含 6 个分析类型 radio（领域/技术力/商业力/综合竞争力/供应链/痛点）；2、未选类型时「下一步」disabled；3、选领域分析后进入配置态且 URL 带 `analysis_type=key-enterprise-domain`；4、领域分析对象区显示「已选择 N 家企业」 | P0 | | | | | | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 自动映射企业业务至预设产业领域 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | 六类型弹窗横跨 T10/T11/T12/T18/T16/T17 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00064 | 企业分析 | 重点企业领域分析 | 分析对象 | URL 上下文 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 识别企业已覆盖的产业领域 | 对比篮发起后 URL 携带 source/return_context_id 且可返回 | 1、已按 00063 发起 | 1.读地址栏参数；2.点「返回对比篮」；3.观察对比篮状态 | 1、URL 含 `source=compare-basket` 与 `return_context_id=cmp-*`；2、返回后对比篮选择态保留；3、页面不白屏不丢上下文 | P1 | | | | | | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 识别企业已覆盖的产业领域 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00065 | 企业分析 | 重点企业领域分析 | 领域布局概览 | KPI 指标 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 计算企业在各产业领域的参与深度 | 概览区展示覆盖领域数/深度/广度 KPI 且数值与对象数一致可读 | 1、已选 ≥1 家企业进入结果态 | 1.看「领域布局概览」区块；2.核对 KPI 项名称；3.切换企业数（增删篮内企业再发起）观察 KPI 变化 | 1、可见覆盖领域数、领域覆盖深度、领域覆盖广度等 KPI；2、数值为 0 或暂无时按 as-built 口径显示（记 observed 不钉死）；3、对象变化后 KPI 随之更新或显示空态 | P0 | | | | | | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 计算企业在各产业领域的参与深度 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | KPI 项以现场为准 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00066 | 企业分析 | 重点企业领域分析 | 领域布局概览 | 指标说明 ⓘ | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 以预设产业领域作为映射目标 | 每个 KPI 有 ⓘ 指标说明且标注 Q013 待甲方确认 | 1、结果态可见 KPI | 1.点开「指标说明：覆盖领域数」ⓘ；2.点开深度/广度 ⓘ；3.观察角标 | 1、ⓘ 弹卡含指标口径说明；2、带「口径待甲方确认（开放项 Q013），当前为团队临时默认值」角标；3、说明文案不自相矛盾 | P0 | | | | | | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 以预设产业领域作为映射目标 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | D9 铁律：ⓘ 必有 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00067 | 企业分析 | 重点企业领域分析 | 企业领域覆盖 | 明细展示 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 按产业领域分别展示参与深度 | 企业领域覆盖区按领域展示各企业参与深度 | 1、结果态 | 1.看「企业领域覆盖」区块；2.逐企业核对领域标签与深度值；3.核对参与深度呈现形式 | 1、按企业×领域矩阵或等价形式展示；2、参与深度有数值或等级呈现；3、无数据格有空态占位不显示 NaN | P0 | | | | | | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 按产业领域分别展示参与深度 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00068 | 企业分析 | 重点企业领域分析 | 跨领域布局 | 多元化评估 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 依据各领域参与深度评估企业多元化程度 | 跨领域布局区呈现企业多元化程度评估 | 1、结果态 | 1.看「跨领域布局」区块；2.核对多元化程度展示；3.与概览 KPI 交叉对照 | 1、区块存在且与企业维度关联；2、多元化评估可读（覆盖领域数/分布形态）；3、与 KPI 口径一致 | P1 | | | | | | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 依据各领域参与深度评估企业多元化程度 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00069 | 企业分析 | 重点企业领域分析 | 重点领域分布 | 分布展示 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 展示企业业务与产业领域关联结果 | 重点领域分布区展示领域聚合分布 | 1、结果态 | 1.看「重点领域分布」区块；2.核对聚合口径（按领域汇总企业数/深度）；3.切换对象数观察刷新 | 1、区块渲染分布图/列表；2、聚合值与明细可对上（抽样核）；3、对象变化后刷新 | P1 | | | | | | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 展示企业业务与产业领域关联结果 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00070 | 企业分析 | 重点企业领域分析 | 数据源 | 年报/专利/产品映射 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 将年报、专利与产品信息共同用于领域映射 | 领域映射基于年报+专利+产品多源数据（口径可见） | 1、结果态 | 1.打开 ⓘ 指标说明；2.看映射口径描述；3.与 §1.1.1 需规描述对照 | 1、口径说明提及年报/专利/产品标签等映射来源；2、说明与实际 KPI 命名一致；3、（黑盒不核后台数据） | P1 | | | | | | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 将年报、专利与产品信息共同用于领域映射 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | 算法侧验证归算法库 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00071 | 企业分析 | 重点企业领域分析 | HTML 报告 | 报告入口 | 重点企业领域分析 | / | 页头「查看 HTML 报告」可打开只读报告 | 1、结果态 | 1.点「查看 HTML 报告」；2.浏览报告结构；3.返回分析结果 | 1、报告 overlay/新页可读；2、含领域分析结论结构；3、返回后结果态保留 | P1 | | | | | | US-KEYENT-01 | KEYENT-USM-16 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 展示领域覆盖计算中状态 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | 报告正文 Wave 0 Mock 可记 observed |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00072 | 企业分析 | 重点企业领域分析 | 评审模式 | 需求追溯 | 重点企业领域分析 | T10 \| 企业业务关联与领域覆盖计算 \| 展示各领域参与深度为空提示 | 评审模式显示需求追溯按钮且关闭后零泄漏 | 1、可切内部评审模式 | 1.开评审模式看「分析类型输入归属需求追溯」「分析对象需求追溯」等按钮；2.关闭评审模式；3.全页检索追溯字样 | 1、开启后追溯按钮可见可点；2、关闭后 DOM 无「需求追溯 / metric_id / Q0xx」字样泄漏；3、不改变分析结果 | P1 | | | | | | US-KEYENT-01 | KEYENT-USM-16 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \| 企业业务关联与领域覆盖计算 \| 展示各领域参与深度为空提示 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?view=domain | | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | | review 零泄漏铁律 |

---

## 2. 覆盖自检

- [x] 20 条 v8 功能点已全部映射（见 `coverage-fp.md`；校验/空态/异常维度合并入对应 UI 用例，算法维度标「算法库侧」）
- [x] 六类型弹窗、URL 上下文、Q013 角标均入用例
- [x] 编号：`00062`～`00072`（11 条）
