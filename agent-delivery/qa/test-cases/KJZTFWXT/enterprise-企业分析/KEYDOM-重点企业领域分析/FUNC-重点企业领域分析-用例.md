# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md` **v1.2**（含 §5.4.1 用例级粒度铁律；编写红线见 `qa/as-built/prompts/_case.md`）  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v3.0 · 2026-10-18（对照重写；保留 00511 / 00515 / 00523 / 00528 / 00529，新号 01688～01731）  
> **模块**：重点企业领域分析（KEYDOM / catalog `ent-key-domain`）  
> **金样**：**01688 / 01689**（两条发起都走到结果页）；沿用 **00511 / 00515**  
> **环境**：http://10.50.69.111:30888/ · 账号 `admin` / `123456`  
> **入口**：侧栏「企业分析」→「重点企业领域分析」  
> **路由**：`/enterprise/key-enterprise-analysis`，query 含 `workspace=domain` 与 `view=domain`  
> **隔离**：与「重点企业类型分析」同壳。类型看板内容不写入本册  
> **功能点 / 功能点ID**：本步待 A 线回填；旧映射仍见同目录 `coverage-fp.md`（本步未改矩阵）  
> **自动化用例ID**：保留行沿用原脚本号；新行留空  
> **维护**：agent:qa-agent · 监管 human:黄敬洲

## 关评审控件清单

入口拓扑（关评审后的现场）：

| 区域 | 现场 | 用例 |
|------|------|------|
| 入口 A · 筛选条件发起 | 无。本页没有靠筛选条件开始分析的按钮 | 无 |
| 入口 B · 本页选择器 | 「打开对比篮」或「前往对比篮选择企业」→ 勾选 →「确定」回填后直接出结果 | 01688 金样 |
| 入口 B · 系统对比篮发起 | 勾选企业 →「发起分析」→「重点企业领域分布分析」→「下一步：前往配置」 | 01689 金样 |
| 任务列表 | 无。本页没有历史分析任务表 | 无 |
| 结果页 | 确定或发起之后出现四大区块 | 00515 |

结果页：

| 格 | 用例或原因 |
|----|------------|
| 摘要 · 对象与发起一致 | 01688 |
| 摘要 · 数据更新时点 | 01731 |
| 摘要 · 已覆盖领域 / 涉及企业 / 跨领域企业 / 识别依据 | 01691 |
| 摘要 · 四大区块 | 00515 |
| 结果页筛选下拉 | 无 |
| 开始分析 · 当天 | 无。本页没有「开始分析」，也不是异步任务 |
| 重新分析 | 无 |
| 调整对象 | 01711 |
| 取消回填 | 01712 |
| 返回对比篮 | 01713 |
| 报告打开与返回 | 00523 |
| 报告目录七节 | 01709 |
| 空态也能打开报告 | 01710 |
| 导出 | 01728 |
| 结果内搜索 | 无 |
| 分布表列 | 01694 |
| 分布表翻页 | 未覆盖：当前结果只有 1 条，分页没有第二页 |
| 分布表勾选 | 无 |
| 行按钮「查看识别依据」 | 01695 |
| 企业领域覆盖 | 01692 |
| 跨领域布局图例 | 01693 |
| 图节点下一级 | 无。点击图上企业节点没有打开下一级 |
| 企业详情及各页签 | 01696～01705 |
| 进入企业评估 | 01706 |
| 进入风险洞察 | 01707 |
| 查看画像 | 01708 |
| 画像「查看详情」 | 01725 |
| 入池 | 无。结果行没有加入名单；「加入招引候选」「加入培育候选」不在本页选择器上，不写入本册 |

选择分析企业：

| 格 | 用例或原因 |
|----|------------|
| 空态进入 | 01690 |
| 名称搜索无匹配 | 01716 |
| 无匹配后重置 | 01717 |
| 企业类型下拉 | 01718 |
| 选中某一类型 | 01719 |
| 全选当前筛选结果 | 01715 |
| 取消选择 / 未选不能确定 | 01714 |
| 勾选后确定到结果 | 01688（与主线同一条） |
| 移除 | 01720。该按钮没有取消弹出框 |
| 清空后取消 | 01721 |
| 清空后确定 | 01722 |
| 选择器翻页 | 未覆盖：篮内企业一次列完，没有第二页 |
| 新增弹层 | 01723 |
| 新增内搜索 | 01729 |
| 新增行详情 | 01730 |
| 加入对比篮 | 01724 |
| 新增列表翻页 | 未覆盖：弹层当前一页列完，没有出现下一页 |
| 同名不同主体 | 未覆盖：篮内企业名称各不相同，现场没有两家同名企业可比 |

系统对比篮（只写通向本页结果的差异）：

| 格 | 用例或原因 |
|----|------------|
| 选择分析任务六项 | 01727 |
| 发起后进入结果 | 01689 |
| 更多操作 · 恢复默认位置 | 01726 |
| 产业 / 服务机构 / 区域页签 | 无。不是本页分析对象 |
| 查看引育名单、加入招引候选、加入培育候选 | 无。不是本页能力 |
| 第二种账号 | 未覆盖：现场只有当前登录账号 |

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

> 排列：**主流程 → 备选 → 异常**。新号从 01688 连续用到 01731。  
> 00512、00513、00514、00516、00517、00520、00521、00522、00524、00525、00526、00527 作废，不复用。  
> 00518、00519、00530 删除，不复用。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00511 | 企业分析 | 重点企业领域分析 | 主流程-侧栏进入与路由 | 入口隔离 | 重点企业领域分析 | T10 \｜企业业务关联与领域覆盖计算 \｜展示企业业务与产业领域关联结果 | 侧栏进入领域分析页且路由携带领域参数与标题正确 | 1、系统正常；2、已登录 | 1.点击侧栏「企业分析」→「重点企业领域分析」 | 1、路由为领域分析页且地址携带领域参数；2、页面标题为「重点企业领域分析」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \｜企业业务关联与领域覆盖计算 \｜展示企业业务与产业领域关联结果 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-01 | 金样；接旧 00062 拆分（参数与标题收口本条）；参数具体取值（view=domain 与 workspace=domain 双参数并存）以现场为准（observed-执行时记录）；同壳层隔离的独立校验归 00528 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01688 | 企业分析 | 重点企业领域分析 | 主流程-选择器回填结果 | 确定回填 | 选择分析企业 | 待 A 线回填 | 勾选企业后点确定，进入领域分析结果 | 1、已打开重点企业领域分析；2、对比篮内至少有一家企业 | 1.点击「打开对比篮」；2.勾选一家篮内企业；3.点击「确定」 | 1、页面出现「领域布局概览」；2、分析对象显示来自对比篮及已选家数 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 金样；本页发起方式之一。选择器文案写明确定只回填、不另起分析任务，确定后直接出结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01689 | 企业分析 | 重点企业领域分析 | 主流程-发起分析进入结果 | 领域分布分析 | 系统对比篮 | 待 A 线回填 | 从系统对比篮发起领域分布分析后进入结果页 | 1、系统对比篮的企业页签内至少有一家企业 | 1.打开系统对比篮；2.勾选一家企业；3.点击「发起分析」；4.选择「重点企业领域分布分析」；5.点击「下一步：前往配置」 | 1、页面标题为「重点企业领域分析」；2、页面出现「领域布局概览」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 金样；本页第二种发起。弹窗选项个数归 01727 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01690 | 企业分析 | 重点企业领域分析 | 主流程-空态打开选择器 | 前往对比篮 | 待选择分析对象 | 待 A 线回填 | 未选对象时从空态进入选择分析企业 | 1、领域分析页尚未选择分析对象 | 1.点击「前往对比篮选择企业」 | 1、出现标题「选择分析企业」；2、文案说明确定后回填对象；3、文案说明不会发起分析任务 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 页头「打开对比篮」与本按钮打开同一选择器，回填成功归 01688 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00515 | 企业分析 | 重点企业领域分析 | 主流程-概览区构成 | 四大区块 | 领域布局概览 | T10 \｜企业业务关联与领域覆盖计算 \｜计算企业在各产业领域的参与深度 | 结果态按四大区块顺序构成完整 | 1、已选至少一家企业并进入结果态 | 1.自上而下浏览结果页 | 1、四大区块按序完整呈现；2、各区块内容区已渲染非骨架 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \｜企业业务关联与领域覆盖计算 \｜计算企业在各产业领域的参与深度 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-03 | 金样；新拆独立成条（旧 00065～00069 各写一区块、区块构成收口本条，结构性检查允许 3 点）；区块加载时序与骨架屏时长（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01691 | 企业分析 | 重点企业领域分析 | 主流程-概览四项指标 | 指标名称 | 领域布局概览 | 待 A 线回填 | 领域布局概览展示四项统计 | 1、已进入带对象的结果页 | 1.浏览「领域布局概览」 | 1、有已覆盖领域、涉及企业、跨领域企业、识别依据四项；2、每项都有数值 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01692 | 企业分析 | 重点企业领域分析 | 主流程-企业领域覆盖 | 覆盖矩阵 | 企业领域覆盖 | 待 A 线回填 | 企业领域覆盖按企业与领域展示，无依据格不可打开 | 1、结果页已出现「企业领域覆盖」 | 1.浏览「企业领域覆盖」；2.点击显示为「—」的覆盖格 | 1、行是企业、列是产业领域；2、「—」格不能打开下一级 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 勘察时识别依据为 0，覆盖格为「—」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01693 | 企业分析 | 重点企业领域分析 | 主流程-跨领域布局 | 图例 | 跨领域布局 | 待 A 线回填 | 跨领域布局用企业与产业领域两种图例 | 1、结果页已出现「跨领域布局」 | 1.浏览「跨领域布局」 | 1、图例含「企业」；2、图例含「产业领域」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 图上企业节点未打开下一级，不单列用例 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01694 | 企业分析 | 重点企业领域分析 | 主流程-重点领域分布列 | 表头 | 重点领域分布 | 待 A 线回填 | 重点领域分布表列出全部列名 | 1、结果页已出现「重点领域分布」 | 1.浏览「重点领域分布」表头 | 1、列名为产业领域、涉及企业、识别依据、代表企业、操作 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01695 | 企业分析 | 重点企业领域分析 | 主流程-查看识别依据 | 依据抽屉 | 重点领域分布 | 待 A 线回填 | 查看识别依据打开对应当前领域和当前企业的抽屉 | 1、分布表至少有一行 | 1.点击该行「查看识别依据」 | 1、抽屉标题含「为什么识别为」和该行领域；2、标题旁为该行企业；3、依据为 0 条时正文不列出依据条目 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 底部三个去向分别归 01696、01706、01707 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01696 | 企业分析 | 重点企业领域分析 | 主流程-企业详情工商概况 | 工商概况 | 企业详情 | 待 A 线回填 | 从识别依据打开企业详情的工商概况 | 1、已打开某行的识别依据抽屉 | 1.点击「企业详情」 | 1、抽屉标题为「企业详情」；2、「工商概况」含经营范围；3、「工商概况」含注册地址 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01697 | 企业分析 | 重点企业领域分析 | 主流程-企业详情主要团队 | 主要团队 | 企业详情 | 待 A 线回填 | 企业详情的主要团队页签给出姓名与职务 | 1、已打开「企业详情」 | 1.点击「主要团队」 | 1、表头含姓名、职务；2、没有记录时显示「暂无数据」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01698 | 企业分析 | 重点企业领域分析 | 主流程-企业详情资质荣誉 | 资质荣誉 | 企业详情 | 待 A 线回填 | 企业详情的资质荣誉页签给出认定信息 | 1、已打开「企业详情」 | 1.点击「资质荣誉」 | 1、表头含资质荣誉、类别、认定时间 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01699 | 企业分析 | 重点企业领域分析 | 主流程-企业详情知识产权 | 知识产权 | 企业详情 | 待 A 线回填 | 企业详情的知识产权页签给出专利字段 | 1、已打开「企业详情」 | 1.点击「知识产权」 | 1、表头含专利名称、类型、日期、状态 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01700 | 企业分析 | 重点企业领域分析 | 主流程-企业详情经营财务 | 经营财务 | 企业详情 | 待 A 线回填 | 企业详情的经营财务页签给出资产与利润字段 | 1、已打开「企业详情」 | 1.点击「经营财务」 | 1、展示总资产、净利润、研发投入 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01701 | 企业分析 | 重点企业领域分析 | 主流程-企业详情供应链关系 | 供应链关系 | 企业详情 | 待 A 线回填 | 企业详情的供应链关系页签给出关联方字段 | 1、已打开「企业详情」 | 1.点击「供应链关系」 | 1、表头含关联方、关系；2、没有记录时显示「暂无数据」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01702 | 企业分析 | 重点企业领域分析 | 主流程-企业详情关系图谱 | 关系图谱 | 企业详情 | 待 A 线回填 | 企业详情的关系图谱页签在无图谱时给出空态 | 1、已打开「企业详情」 | 1.点击「关系图谱」 | 1、显示「暂无关系图谱」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01703 | 企业分析 | 重点企业领域分析 | 主流程-企业详情舆情动态 | 舆情动态 | 企业详情 | 待 A 线回填 | 企业详情的舆情动态页签在无舆情时给出空态 | 1、已打开「企业详情」 | 1.点击「舆情动态」 | 1、显示「暂无舆情」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01704 | 企业分析 | 重点企业领域分析 | 主流程-企业详情风险信息 | 风险信息 | 企业详情 | 待 A 线回填 | 企业详情的风险信息页签给出两类计数 | 1、已打开「企业详情」 | 1.点击「风险信息」 | 1、展示司法案件计数；2、展示失信被执行人计数 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01705 | 企业分析 | 重点企业领域分析 | 主流程-企业详情招投标 | 招投标 | 企业详情 | 待 A 线回填 | 企业详情的招投标页签给出公告字段 | 1、已打开「企业详情」 | 1.点击「招投标」 | 1、表头含公告标题、角色、对手方、日期；2、没有记录时显示「暂无数据」 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01706 | 企业分析 | 重点企业领域分析 | 主流程-进入企业评估 | 企业评估 | 识别依据抽屉 | 待 A 线回填 | 从识别依据进入企业技术力评估，对象为当前企业 | 1、已打开某企业的识别依据抽屉 | 1.点击「进入企业评估」 | 1、页面标题为「企业技术力评估对比分析」；2、评估对象含该企业 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01707 | 企业分析 | 重点企业领域分析 | 主流程-进入风险洞察 | 痛难点 | 识别依据抽屉 | 待 A 线回填 | 从识别依据进入企业发展痛难点分析，对象为当前企业 | 1、已打开某企业的识别依据抽屉 | 1.点击「进入风险洞察」 | 1、页面标题为「企业发展痛难点分析」；2、分析对象含该企业 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01708 | 企业分析 | 重点企业领域分析 | 主流程-查看画像 | 画像快览 | 篮内企业 | 待 A 线回填 | 篮内企业的查看画像打开该企业快览 | 1、「选择分析企业」已打开 | 1.在一家企业卡片上点击「查看画像」 | 1、抽屉标题为「企业画像快览」；2、名称是所点企业；3、含基础摘要、竞争力摘要、风险摘要 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00523 | 企业分析 | 重点企业领域分析 | 主流程-HTML 报告入口 | 报告往返 | 页头 | T10 \｜企业业务关联与领域覆盖计算 \｜展示领域覆盖计算中状态 | 页头报告入口可打开报告并返回保留结果态 | 1、结果态 | 1.点击「查看 HTML 报告」；2.点击「返回分析结果」 | 1、报告以浮层或新页可读；2、返回后结果态保留 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-16 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \｜企业业务关联与领域覆盖计算 \｜展示领域覆盖计算中状态 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-12 | 接旧 00071；报告目录归 01709；报告正文为演示内容、真实性（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01709 | 企业分析 | 重点企业领域分析 | 主流程-报告目录 | 七节目录 | HTML 报告 | 待 A 线回填 | 结果页打开的报告目录与对象对应当前企业 | 1、已从带对象的结果页打开 HTML 报告 | 1.浏览报告目录 | 1、目录共 7 节（名称见附录A）；2、报告身份中的对象为当前分析企业 | P0 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-16 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 打开与返回归 00523 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01731 | 企业分析 | 重点企业领域分析 | 主流程-数据更新时点 | 页头时点 | 重点企业领域分析 | 待 A 线回填 | 页头展示数据更新时点 | 1、已进入重点企业领域分析 | 1.浏览页头 | 1、页头有「数据更新至」；2、没有时点时显示「暂无时点」 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01710 | 企业分析 | 重点企业领域分析 | 备选-空态打开报告 | 未选对象 | 页头 | 待 A 线回填 | 尚未选择企业时也能打开领域分析报告 | 1、领域分析页尚未选择分析对象 | 1.点击「查看 HTML 报告」 | 1、标题为「重点企业领域分析报告」；2、报告身份中的对象为「重点企业领域分析」 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-16 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 与带对象后的报告对象归 01709 分开 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01711 | 企业分析 | 重点企业领域分析 | 备选-调整分析对象 | 已选保留 | 结果页 | 待 A 线回填 | 调整对象时选择器带回当前已选家数 | 1、结果页已有分析对象 | 1.点击「打开对比篮调整对象」 | 1、打开「选择分析企业」；2、已选家数与当前分析对象家数一致 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01712 | 企业分析 | 重点企业领域分析 | 备选-取消回填 | 结果不变 | 选择分析企业 | 待 A 线回填 | 在选择器里改勾选后取消，结果页对象不变 | 1、结果页已有分析对象 | 1.点击「打开对比篮调整对象」；2.改动勾选；3.点击「取消」 | 1、选择器关闭；2、分析对象仍是打开前的企业 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01713 | 企业分析 | 重点企业领域分析 | 备选-返回对比篮 | 已选保留 | 结果页 | 待 A 线回填 | 返回对比篮后选择器仍保留已选 | 1、结果页已有分析对象 | 1.点击「返回对比篮」 | 1、打开「选择分析企业」；2、已选家数与当前结果一致 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01714 | 企业分析 | 重点企业领域分析 | 备选-取消选择 | 确定不可用 | 选择分析企业 | 待 A 线回填 | 取消选择后不能确定回填 | 1、「选择分析企业」已打开 | 1.点击「取消选择」 | 1、已选为 0 家；2、「确定」不可点击 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01715 | 企业分析 | 重点企业领域分析 | 备选-全选当前筛选 | 已选计数 | 选择分析企业 | 待 A 线回填 | 全选当前筛选结果只增加已选计数 | 1、「选择分析企业」已打开；2、当前列出至少一家企业 | 1.点击「全选当前筛选结果」 | 1、已选家数等于当前列出的企业家数；2、尚未出现「领域布局概览」 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01716 | 企业分析 | 重点企业领域分析 | 备选-名称搜索无匹配 | 只过滤名单 | 选择分析企业 | 待 A 线回填 | 按企业名称搜索无匹配时只缩小名单 | 1、「选择分析企业」已打开 | 1.在「按企业名称搜索」输入篮内不存在的名称 | 1、出现「当前篮内无匹配企业」；2、仍停留在选择器 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01717 | 企业分析 | 重点企业领域分析 | 备选-搜索重置 | 名单恢复 | 选择分析企业 | 待 A 线回填 | 无匹配后重置会恢复篮内企业 | 1、搜索已出现「当前篮内无匹配企业」 | 1.点击无匹配提示旁的「重置」 | 1、搜索框被清空；2、篮内企业卡片重新列出 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01718 | 企业分析 | 重点企业领域分析 | 备选-企业类型选项 | 下拉个数 | 选择分析企业 | 待 A 线回填 | 企业类型下拉给出全部类型 | 1、「选择分析企业」已打开 | 1.展开「全部企业类型」 | 1、选项共 7 个（名称见附录A） | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01719 | 企业分析 | 重点企业领域分析 | 备选-按企业类型过滤 | 外资企业 | 选择分析企业 | 待 A 线回填 | 选择外资企业后名单只留该类型 | 1、「选择分析企业」已打开 | 1.展开「全部企业类型」；2.选择「外资企业」 | 1、列出的企业带「外资企业」标识；2、不带该标识的企业不再列出 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01720 | 企业分析 | 重点企业领域分析 | 备选-移除篮内企业 | 立即移出 | 选择分析企业 | 待 A 线回填 | 移除篮内企业后该企业从列表消失 | 1、「选择分析企业」已列出企业 | 1.在一家企业卡片上点击「移除」 | 1、该企业不再出现在篮内列表；2、提示已移出对比篮 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 此按钮没有取消弹出框，点击即移出。清空的取消路径归 01721 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01721 | 企业分析 | 重点企业领域分析 | 备选-清空后取消 | 企业仍在 | 选择分析企业 | 待 A 线回填 | 清空对比篮后取消，篮内企业仍在 | 1、「选择分析企业」已列出企业 | 1.点击「清空对比篮」；2.在弹出框中点击「取消」 | 1、弹出框说明将清空篮内企业；2、弹出框说明不会删除企业数据；3、取消后这些企业仍在 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01722 | 企业分析 | 重点企业领域分析 | 备选-清空后确定 | 名单变空 | 选择分析企业 | 待 A 线回填 | 确定清空对比篮后篮内企业消失 | 1、「选择分析企业」已列出企业 | 1.点击「清空对比篮」；2.在弹出框中点击「确定」 | 1、篮内不再列出企业；2、提示对比篮已清空 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 会清掉当前账号的对比篮，执行后需重新加入企业 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01723 | 企业分析 | 重点企业领域分析 | 备选-新增企业弹层 | 行内操作 | 新增企业 | 待 A 线回填 | 新增打开可加入对比篮的企业列表 | 1、「选择分析企业」已打开 | 1.点击「新增」 | 1、弹层标题为「新增企业」；2、列有名称、操作；3、每行有「详情」和「加入对比篮」 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01724 | 企业分析 | 重点企业领域分析 | 备选-加入对比篮 | 新增行 | 新增企业 | 待 A 线回填 | 在新增列表把企业加入对比篮 | 1、「新增企业」已打开；2、某一行按钮为「加入对比篮」 | 1.点击该行「加入对比篮」 | 1、提示已加入该企业；2、该行按钮变为「移出对比篮」 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01725 | 企业分析 | 重点企业领域分析 | 备选-画像查看详情 | 完整画像 | 企业画像快览 | 待 A 线回填 | 从画像快览进入该企业的完整画像 | 1、已打开某企业的「企业画像快览」 | 1.点击「查看详情」 | 1、进入该企业的画像页；2、页内能对应所点企业 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 勘察时画像页出现请求失败，并有「返回企业检索」「重试」。通过标准仍是进入画像页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01726 | 企业分析 | 重点企业领域分析 | 备选-恢复默认位置 | 更多操作 | 系统对比篮 | 待 A 线回填 | 更多操作里恢复对比篮默认位置后篮仍打开 | 1、系统对比篮已打开 | 1.点击「更多操作」；2.点击「恢复默认位置」 | 1、菜单中有「恢复默认位置」；2、对比篮保持打开 | P2 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01727 | 企业分析 | 重点企业领域分析 | 备选-选择分析任务 | 六项 | 系统对比篮 | 待 A 线回填 | 发起分析弹出的任务里含领域分布分析 | 1、系统对比篮已勾选至少一家企业 | 1.点击「发起分析」 | 1、弹窗标题为「选择分析任务」；2、可选分析共 6 项（名称见附录A）；3、未选择时「下一步：前往配置」不可点击 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 选定领域分布并进入结果归 01689 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01729 | 企业分析 | 重点企业领域分析 | 备选-新增内搜索 | 企业名称 | 新增企业 | 待 A 线回填 | 新增企业里按名称搜索只过滤列表 | 1、「新增企业」已打开 | 1.在「输入企业名称」中输入一个企业名称片段 | 1、列表只保留名称匹配的企业；2、弹层不关闭 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01730 | 企业分析 | 重点企业领域分析 | 备选-新增行详情 | 画像快览 | 新增企业 | 待 A 线回填 | 新增列表的详情打开该企业画像快览 | 1、「新增企业」已打开 | 1.点击某一行「详情」 | 1、「新增企业」关闭；2、打开该企业的「企业画像快览」 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01728 | 企业分析 | 重点企业领域分析 | 异常-报告导出受限 | 未付费 | HTML 报告 | 待 A 线回填 | 未付费时导出报告只给出提示 | 1、已打开重点企业领域分析报告 | 1.点击「导出」 | 1、提示需付费才能导出；2、仍停留在报告页；3、没有下载文件 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-16 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | 待 A 线回填 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 按钮旁有「付费」标记。勘察提示原文：付费用户可导出报告 PDF |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00528 | 企业分析 | 重点企业领域分析 | 异常-同壳层隔离反向 | 同壳隔离 | 重点企业领域分析 | T10 \｜企业业务关联与领域覆盖计算 \｜展示企业业务与产业领域关联结果 | 领域参数下不落入类型看板且类型参数不串入领域态 | 1、已登录 | 1.从侧栏进入类型分析；2.返回侧栏进入领域分析 | 1、类型菜单进入后为类型看板且地址含类型参数；2、领域菜单进入后为领域页面且地址含领域参数 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \｜参数隔离 \｜同壳层 view 参数互斥 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-06 | 与类型册 00046 互为隔离反向；同一窗口先后往返（先类型后领域）覆盖参数残留场景；类型看板内容细核归类型册（隔离口径：本册不写类型看板内容） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00529 | 企业分析 | 重点企业领域分析 | 异常-结果态刷新恢复 | 刷新恢复 | 结果态 | T10 \｜企业业务关联与领域覆盖计算 \｜展示企业业务与产业领域关联结果 | 结果态刷新后分析对象与四大区块恢复 | 1、结果态已渲染完成 | 1.刷新页面 | 1、页面不回落至待选择空态；2、分析对象与四大区块恢复呈现 | P1 |  |  |  |  |  | US-KEYENT-01 | KEYENT-USM-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3 | T10 \｜企业业务关联与领域覆盖计算 \｜展示企业业务与产业领域关联结果 | TRACE-ENT-KEYENT.yaml | /enterprise/key-enterprise-analysis?workspace=domain&view=domain |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-07 | 新拆独立成条（刷新恢复旧册漏测，本条补）；指标数值刷新前后逐项一致性（observed-执行时记录） |

---

## 2. 附录 A · 枚举

**企业类型（7）**：外资企业、高新技术企业、小微企业、上市企业、专精特新、小巨人、链主龙头。

**报告目录（7）**：报告身份、执行摘要、对象与范围、关键发现、证据与分析、数据来源与生成说明、局限性与使用边界。

**选择分析任务（6）**：重点企业领域分布分析、技术力评估、商业力评估、综合竞争力评估、企业供应链关系分析、企业发展痛点分析。

---

## 3. 序号台账（本文件）

| 测试类型 | 已用序号 | 本段最大号 |
|----------|----------|------------|
| FUNC 保留 | 00511、00515、00523、00528、00529 | — |
| FUNC 新号 | 01688～01731 | 01731 |
| 作废不复用 | 00512～00514、00516～00522、00524～00527 | — |
| 删除不复用 | 00518、00519、00530 | — |
