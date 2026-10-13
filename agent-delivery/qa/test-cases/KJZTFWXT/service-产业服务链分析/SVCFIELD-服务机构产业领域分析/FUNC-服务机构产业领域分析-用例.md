# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）  
> **规范**：`agent-delivery/qa-test-case-spec.md` **v1.2**（含 §5.4.1 用例级粒度铁律；编写红线见 `qa/as-built/prompts/_case.md` 红线 1~6）  
> **测试类型**：FUNC  
> **系统码**：KJZTFWXT  
> **版本**：v2.0 · 2026-10-13（全库粒度重写，自 00641 起编）  
> **模块**：服务机构产业领域分析（SVCFIELD / catalog `svc-org-field` / A 线 **T22 服务机构产业领域分析**，36 条功能点：服务机构产业领域覆盖分析 19 条 + 服务机构产业领域分析结果呈现 17 条）  
> **金样**：**00641 / 00643 / 00645 / 00646**（烟测子集 = 跑全部金样：入口路由、选择机构回显、开始分析门控与显式触发、热力图默认呈现）  
> **旧号段**：00273~00283 · **2026-10-13 全库粒度重写废弃，归档不删**（历史行存 git 版本；旧→新映射见同目录 `coverage-fp.md` 附录）  
> **环境**：http://111.198.38.90:50892/ · 账号 `admin` / `123456`（已在业务页且 URL 不含 `/login` 则不要登出）  
> **入口**：产业服务链分析 →「服务机构分析」→ 工作区 field  
> **路由**：`/service/institution-judgment?workspace=field&tab=coverage`（机构分析三兄弟 workspace 同路由，本册只认 `workspace=field`）  
> **as-built 实勘**：2026-10-12  
> **USM**：`agent-handoffs/产品整体定义/E7-产业服务链分析/SVCCHAIN-ORG-ANALYSIS-服务机构分析/USM-SVCCHAIN-ORG-ANALYSIS.md`（US-SVC-ORG-01 组装分析对象集 + US-SVC-ORG-02 领域覆盖分析与呈现；US-03 画像下钻在结果态承载）  
> **TRACE**：`TRACE-SVCCHAIN-ORG-ANALYSIS.yaml`（`acceptance_leaf`：REQ-SVC-ORG-COVERAGE / REQ-SVC-ORG-COVERAGE-VIS）  
> **原始需求**：`bid-reference/科技信息展示系统和科技专题服务系统.md` → `§1.1.1.2.4.2.7.1.1`（服务机构产业领域覆盖分析）/ `§1.1.1.2.4.2.7.1.2`（服务机构产业领域分析结果呈现）  
> **交付口径**：INTEG（前端 → Java → Python `/internal/*`）  
> **功能点 / 功能点ID**：见同目录 `coverage-fp.md`（v8 T22 全 36 条映射）  
> **禁止**：把兄弟工作区 trend（服务机构新增趋势分析）/ capability（服务机构技术力评估分析）写成用例（隔离统一归本册 00652）；对比篮浮层为系统级入口（现场共 8 项），专项归 COMPARE 用例集，本页只顺带 observed  
> **关联任务**：`QA-KJZTFWXT-BLINE-CASE-SRV-L01`  
> **维护**：agent:qa-agent · 监管 human:黄敬洲

**as_built 摘要（写期望用，不升 Fail，2026-10-12 实勘）**：路由 `/service/institution-judgment?workspace=field&tab=coverage`，页标题「服务机构产业领域分析」；顶部 Tab 为「服务机构产业领域分析（选中）/ 分析记录」双 Tab；分析配置区含领域筛选输入框（placeholder「筛选领域（不改分析指纹）」——口径：筛选只过滤领域展示范围，不改变分析指纹，不触发分析）、「选择机构」按钮、「开始分析」按钮；本页为异步分析工作区：切条件不自动起任务，须显式点「开始分析」；勘察时页面为配置空态（未选机构），结果态（领域覆盖热力图/矩阵图呈现）现场无结果，按 USM 口径写期望并标 observed（开放项 1）；评审增量：需求追溯按钮「服务机构分析工作区」「分析配置」，关闭评审模式后须零泄漏；系统级浮层对比篮共 8 项只 observed；机构分析三兄弟 workspace（field/trend/capability）同路由，隔离验证归 00652；「暂无覆盖数据」空行、计算中/失败态、ⓘ（`M_SVC_ORG_COVERAGE_DEPTH` D1 draft ⚠️ Q-SVCCHAIN-02）与 🧪 角标现场未见，不出预期硬判，归 coverage 部分覆盖/未覆盖与开放项。

---

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

> 排列顺序：**主流程（P0）→ 备选（P0/P1）→ 异常（P1）**；场景类见「功能项」列前缀。  
> 预期断言常态 1~3 点；本册无 4~5 点结构性例外。  
> observed 项一律入「备注」，不进预期。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00641 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-入口与路由 | 侧栏进入 field 工作区 | 服务机构产业领域分析 | 进入服务机构产业领域分析页 | 从直达路由进入服务机构产业领域分析工作区，路由与页头双 Tab 正确 | 1、系统正常；2、已登录 admin | 1.地址栏进入直达路由 `/service/institution-judgment?workspace=field&tab=coverage` | 1、路由为 field 工作区直达态（workspace=field、tab=coverage）；2、页标题为「服务机构产业领域分析」；3、顶部为「服务机构产业领域分析（选中）/ 分析记录」双 Tab | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 默认按全部产业领域计算服务覆盖 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 金样；接旧 00273；勘察为配置空态（observed-执行时记录）；兄弟工作区隔离归 00652 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00642 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-配置区构成 | 配置空态 | 服务机构产业领域分析 | 分析配置区 | 分析配置区三控件齐备且未选机构时为配置空态 | 1、已进入页面；2、未改动任何配置 | 1.从直达路由进入页面（不改动任何配置） | 1、分析配置区含领域筛选框、机构入口与「开始分析」按钮；2、领域筛选占位提示为「筛选领域（不改分析指纹）」；3、未选机构时无结果区渲染 | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 未选定重点服务机构时不可计算服务覆盖 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00273/00276 部分；机构入口按钮全名为「选择机构」；弹窗内部构成 observed-执行时记录（开放项 2） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00643 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-选择机构与回显 | 勾选确定回显 | 服务机构产业领域分析 | 机构选择与已选回显 | 勾选 1 家机构并确定后配置区回显该机构 | 1、已进入页面；2、配置区可见 | 1.点击「选择机构」按钮；2.勾选 1 家机构；3.点击弹窗确定按钮 | 1、机构挑选弹窗打开且机构可勾选；2、确定后配置区回显该已选机构 | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 选定单个重点服务机构 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage | M_SVC_ORG_SELECTED_COUNT | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 金样；接旧 00275 部分；弹窗构成（按类型分组/关键词搜索/单类全选/清空）与回显形态 observed-执行时记录（开放项 2） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00644 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-机构集合操作 | 加选/取消/移除 | 服务机构产业领域分析 | 机构集合变更 | 多机构加选、弹窗直接取消与单个移除行为正确 | 1、已回显至少 1 家已选机构 | 1.打开弹窗加选至多家机构并确定；2.再次打开弹窗后直接取消；3.点击已选机构条目的移除按钮 | 1、加选后回显集合与勾选一致且机构不重复；2、直接取消后已确认集合不变；3、已选机构可单个移除 | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 选定多个重点服务机构 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00275 部分；同时承载取消已选与互不相同口径；移除后门控联动见 00645 预期 1 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00645 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-开始分析门控与显式触发 | 未选不可发起 | 服务机构产业领域分析 | 开始分析门控与异步起任务 | 未选机构时不可发起；分析任务仅由显式点击触发且同条件单飞 | 1、已进入页面 | 1.未选机构时点击「开始分析」；2.经机构入口选定 1 家机构；3.点击「开始分析」并等待分析完成；4.任务在跑时以同条件再次点击「开始分析」 | 1、未选机构时「开始分析」不可用或给出先选机构引导；2、显式点击后发起分析任务并进入结果态；3、同条件重复点击不重复起任务 | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 未选定重点服务机构时不可计算服务覆盖 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 金样；接旧 00276；按钮禁用与提示形态 observed-执行时记录（开放项 2）；切条件不自动起任务归 00649；当天已成功直接打开结果归 00650 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00646 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-热力图默认呈现 | 行列与色阶 | 服务机构产业领域分析 | 热力图呈现覆盖结果 | 分析完成后结果态默认以热力图呈现机构×领域覆盖 | 1、已进入页面；2、已选定至少 1 家机构 | 1.选定 2 家机构；2.点击「开始分析」并等待完成 | 1、结果态默认以热力图呈现覆盖结果；2、热力图行为已选机构、列为产业领域全集；3、色阶分档与图例一致且含义为服务深度 | P0 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.2 | T22 \| 服务机构产业领域分析结果呈现 \| 以热力图呈现分析结果 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage | M_SVC_ORG_COVERAGE_DEPTH | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 金样；接旧 00277 部分；结果态勘察无结果，执行时构造后核验（本轮不判 Fail，开放项 1）；无覆盖数据机构行归 00654 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00647 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-热力图悬停明细与角标 | hover 与角标 | 服务机构产业领域分析 | 热力图悬停明细 | 热力图单元格悬停明细与统计数字角标正确 | 1、已进入结果态（热力图已呈现） | 1.悬停任一热力图单元格 | 1、悬停显示机构、领域与深度值且与单元格一致；2、服务深度与广度数字旁有 ⓘ 与演示角标 | P0 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.2 | T22 \| 服务机构产业领域分析结果呈现 \| 在可视化结果中展示服务深度 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage | M_SVC_ORG_COVERAGE_BREADTH | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00277 部分；ⓘ 角标评审态口径与治理引用 observed-执行时记录（Q-SVCCHAIN-02，开放项 6） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00648 | 产业服务链分析 | 服务机构产业领域分析 | 主流程-矩阵图与图型切换 | X/Y 轴与互斥 | 服务机构产业领域分析 | 矩阵图呈现与图型切换 | 矩阵图坐标口径正确且与热力图互斥同源切换 | 1、已进入结果态（热力图已呈现） | 1.将图型切换为矩阵图；2.切回热力图 | 1、矩阵图 X 轴为覆盖领域数、Y 轴为平均深度得分；2、两图型互斥呈现且出自同一次分析结果；3、往返切换后已选机构与领域上下文保持 | P0 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.2 | T22 \| 服务机构产业领域分析结果呈现 \| 以矩阵图呈现分析结果 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage | M_SVC_ORG_COVERAGE_BREADTH | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00278；四象限文本标注、气泡点按与刷新后图型保留 observed-执行时记录（开放项 1） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00649 | 产业服务链分析 | 服务机构产业领域分析 | 备选-领域筛选不改指纹 | 筛选仅过滤展示 | 服务机构产业领域分析 | 领域筛选输入框口径 | 领域筛选仅过滤展示范围，不触发分析、不改已选机构 | 1、已进入页面；2、已有已选机构 | 1.在领域筛选框键入关键词；2.清除关键词 | 1、键入后领域展示范围收窄至匹配项；2、清除后恢复全量；3、筛选动作不自动发起分析任务、不改变已选机构集合 | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.2 | T22 \| 服务机构产业领域分析结果呈现 \| 在可视化结果中展示不同产业 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00274；结果态下可视化面向筛选子集呈现 observed-执行时记录（开放项 1） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00650 | 产业服务链分析 | 服务机构产业领域分析 | 备选-分析记录与结果复用 | 列表/当天复用/重新分析 | 服务机构产业领域分析 | 分析记录 Tab | 分析记录呈现历史任务并可复用当天已成功结果 | 1、已产生至少一条已完成分析记录（无则先发起一次） | 1.点击顶部「分析记录」Tab；2.打开一条当天已成功记录；3.变更已选机构后再次点击「开始分析」 | 1、「分析记录」呈现历史分析任务列表；2、同条件当天已成功时直接打开既有结果不重跑；3、变更机构后须显式重新分析且可视化随之刷新 | P1 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 变更已选机构后重新计算服务覆盖情况 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00279；列表构成（条件摘要/状态/时间）observed-执行时记录（开放项 5）；单飞与当天复用口径=Q-ANALYSIS-01 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00651 | 产业服务链分析 | 服务机构产业领域分析 | 备选-URL 直达与刷新保留 | 参数恢复 | 服务机构产业领域分析 | URL 参数恢复与持久化 | URL 直达按参数恢复上下文，刷新后已选与 Tab 保留 | 1、已在 field 工作区选定机构 | 1.复制当前完整 URL 到新标签页打开；2.刷新页面 | 1、直达时按 workspace 与 tab 参数恢复上下文、不回落默认值；2、刷新后已选机构集合与激活 Tab 保留 | P1 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 默认按全部产业领域计算服务覆盖 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00281；清除本地存储后的默认态 observed-执行时记录（开放项 2） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00652 | 产业服务链分析 | 服务机构产业领域分析 | 备选-兄弟工作区隔离 | field/trend/capability | 服务机构产业领域分析 | 兄弟 workspace 隔离 | 机构分析三 workspace 往返互不污染且切回保留 | 1、已在 field 工作区选定机构 | 1.切到 workspace=trend；2.切到 workspace=capability；3.切回 workspace=field | 1、trend 与 capability 不显示 field 的分析结果或任务状态；2、切回 field 后已选机构与领域筛选保留；3、往返不自动触发任何工作区的分析任务 | P0 |  |  |  |  |  | US-SVC-ORG-01 | AC-US-SVC-ORG-01-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 输出各产业领域服务覆盖情况 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00280；三兄弟隔离统一在本册验证（trend/capability 册不重复出条）；隔离细节 observed-执行时记录（开放项 5） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00653 | 产业服务链分析 | 服务机构产业领域分析 | 备选-评审模式零泄漏 | 追溯显隐 | 服务机构产业领域分析 | 评审模式零泄漏 | 评审模式开启显示追溯按钮，关闭后零泄漏且业务态不变 | 1、可切换内部评审模式（人设面板内部评审开关） | 1.开启内部评审模式进入页面；2.点击两枚需求追溯按钮；3.关闭内部评审模式并刷新页面 | 1、开启后「服务机构分析工作区」「分析配置」追溯按钮可见可点；2、关闭后页面无追溯按钮与内部编号字样；3、开关不改变已选机构、领域筛选与分析状态 | P1 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-04 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1 | T22 \| 服务机构产业领域覆盖分析 \| 输出各产业领域服务覆盖情况 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00283；勘察时评审模式为开启态；结果态 ⚠️ 角标（Q-SVCCHAIN-02）observed-执行时记录（开放项 6） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00654 | 产业服务链分析 | 服务机构产业领域分析 | 异常-空态 | 配置空态与无覆盖数据行 | 服务机构产业领域分析 | 空态与局部空行 | 配置空态不渲染空图表，无覆盖数据机构行诚实呈现 | 1、已进入页面 | 1.进入未选机构的配置空态；2.选定一家无服务记录的机构并点击「开始分析」 | 1、配置空态不渲染空坐标轴或空图表；2、无覆盖数据机构行保留且显示「暂无覆盖数据」；3、空数据不以 0 填充且不参与排名 | P1 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 展示服务覆盖数据为空提示 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00282 部分；无服务记录机构需构造（observed-执行时记录，开放项 4） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00655 | 产业服务链分析 | 服务机构产业领域分析 | 异常-分析失败 | 局部错误与重试 | 服务机构产业领域分析 | 分析失败提示 | 分析失败呈局部错误提示且可重试、页面壳保留 | 1、已选定机构；2、可构造分析服务异常（断链） | 1.断开分析服务后点击「开始分析」；2.点击失败态的「重试」入口 | 1、失败时图表容器呈局部错误提示；2、失败态提供重试入口且页面壳与筛选保留 | P1 |  |  |  |  |  | US-SVC-ORG-02 | AC-US-SVC-ORG-02-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.7.1.1 | T22 \| 服务机构产业领域覆盖分析 \| 展示服务覆盖计算失败提示 | TRACE-SVCCHAIN-ORG-ANALYSIS.yaml | /service/institution-judgment?workspace=field&tab=coverage |  | INTEG | QA-KJZTFWXT-BLINE-CASE-SRV-L01 |  | 接旧 00282 部分；失败态需构造异常触发（本轮不判 Fail，开放项 3） |

---

## 2. 覆盖自检（2026-10-13 全库粒度重写）

**覆盖声明**：

- T22 范围（36 条功能点）覆盖结论见同目录 `coverage-fp.md`：已覆盖 13 / 部分覆盖 21 / 未覆盖 2（行为集与旧册一致，本次仅按新粒度拆分重排取号，未新增/删除现场能力判断）。
- US-SVC-ORG-01 / 02 在本页可见路径均有 P0/P1 用例；US-SVC-ORG-03 画像下钻由结果态明细表/行头承载（observed-执行时记录）。
- **金样清单**：00641（入口路由）、00643（选择机构回显）、00645（开始分析门控与显式触发）、00646（热力图默认呈现）——烟测 = 跑全部金样。
- 正向密度：每个可见区块默认态/典型值/边界值至少各 1 条正向用例——配置区（00642 默认空态 / 00643 典型单选 / 00644 多选边界）、热力图（00646 默认 / 00647 典型 hover / 00654 空数据边界）、矩阵图（00648）、分析记录（00650）、URL（00651）、隔离（00652）、评审层（00653）、失败态（00655）。

**断言分布统计**（spec §5.4.1）：

| 指标 | 数值 |
|------|------|
| 用例总数 | 15（00641~00655 连续无跳号） |
| 预期 1~3 点 | 15 条（100%，目标 ≥85% ✅） |
| 预期 4~5 点（结构性例外） | 0 条 ✅ |
| 预期 ≥6 点 | 0 条 ✅ |
| 场景分布 | 主流程 8（00641~00648）≥ 备选 5（00649~00653）+ 异常 2（00654~00655）= 7 ✅ |
| 优先级分布 | P0 ×10、P1 ×5 |

**红线自检结果**（内容红线 1~6 逐条，2026-10-13 执行）：

- [x] 红线 1 正文零内部引用：四列（测试内容/前置条件/测试步骤/预期结果）扫描 `US-|AC-|Q0\d|GAP-|开放项|coverage #|TRACE-|metric_id|\.yaml|\.md` = **0 命中**（追溯数据全部位于扩展列与备注）
- [x] 红线 2 observed 不进预期 / 废弃态不验不可见：勘察观测项（弹窗内部构成、按钮形态、列表构成、角标形态）全部入备注「observed-执行时记录」；无废弃能力「不可见」反向校验
- [x] 红线 3 步骤只写操作：步骤列扫描 `核对|确认|检查|校验|观察|比对|验证` = **0 命中**；预期列无操作动词
- [x] 红线 4 一句一事与长度：单条步骤/预期均 ≤60 字；步骤 ≤7 步（本册最大 4 步）；无贴上限写作
- [x] 红线 5 场景分层：主流程 → 备选 → 异常 顺序排列，「功能项」列前缀可辨（主流程-/备选-/异常-）
- [x] 红线 6 用例级粒度：每条「测试内容」一句话可概括（一测一问一答）；断言分布见上表；顺带点均满足三条件（零额外操作/同域/不跨状态）
- [x] 金样标记：4 条金样在元信息区与备注列双声明，均为正向、可独立执行、覆盖核心功能点

---

## 3. 序号台账（本文件）

| 测试类型 | 已用序号 | 下一号（系统 FUNC） |
|----------|----------|---------------------|
| FUNC | 00641–00655（旧 00273–00283 于 2026-10-13 全库粒度重写废弃归档） | 00656（C 组内顺延） |
| API / COMP / INT / PERF | 未用 | 见 `qa/code-registry.yaml` |

**code-registry 回写说明**：C 组 11 册完成后统一回写 `qa/code-registry.yaml`（next_seq 与 modules 的 SVCFIELD 条目），避免与并行组冲突。
