# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）
> **规范**：`agent-delivery/qa-test-case-spec.md` v1.3
> **测试类型**：FUNC
> **系统码**：KJZTFWXT
> **版本**：v3.1 · 2026-10-18（对照重写保留 01788–01825；返工只补 01826–01830，金样 01788 与重新分析 01790 未改）
> **模块**：企业技术力评估对比分析（catalog `ent-eval-tech`）
> **金样**：01788（对比篮勾选两家企业后开始分析，直到技术力评估结果）
> **环境**：http://10.50.69.111:30892/ · 账号 `admin` / `123456`
> **入口**：侧栏「企业分析」→「企业技术力评估对比分析」
> **路由**：`/enterprise/evaluation?workspace=technology`（同页可带 `mode=technology`）
> **实勘**：2026-10-18 在已发布页点到结果、报告、最近评估与选择分析企业
> **交付口径**：INTEG。算法分值是否算对不在本册，本册只验页面终态
> **自动化用例ID**：本步留空
> **维护**：agent:qa-agent · 监管 human:黄敬洲

旧号 00901、00906、00912、00913、00916、00917、00920、00922、00924、00925、00926、00928、00929 作废，不复用。00927 删除，不复用。保留号见下表。

---

## 关评审控件清单

### 入口拓扑

| 区域 | 现场 | 用例 |
| --- | --- | --- |
| 入口 A · 筛选条件发起 | 无。本页不能只靠筛选、不选企业就发起 | 无 |
| 入口 B · 已选对象发起 | 「前往对比篮选择企业」勾选后「确定」，再点「开始分析」 | 01788（金样） |
| 任务列表 | 「最近评估」 | 01802 起 |
| 结果页 | 「技术力评估结果」 | 01788 到达；摘要与表另条 |

### 结果页

| 格 | 用例或原因 |
| --- | --- |
| 摘要 · 对象家数与生成时间 | 01799 |
| 摘要 · 技术力最高得分 | 01788 |
| 摘要 · 纳入评价企业 | 01796 |
| 摘要 · 对象集平均得分 | 01797 |
| 摘要 · 高可信企业 | 01798 |
| 下拉 · 对比对象 A | 01792 |
| 下拉 · 对象 B | 01793 |
| 开始分析 · 当天 | 01789 |
| 重新分析 | 01790 |
| 调整配置 | 00923 |
| 结果搜索 | 无 |
| 排名条 | 01794 |
| 差距表列 | 01795 |
| 差距表翻页 | 未覆盖：本次结果只有 2 条，停在第 1 页 |
| 差距表勾选 | 无 |
| 差距表行按钮 | 无 |
| 差距详情抽屉 | 无。差距写在列「领先差距与优势短板」里 |
| 结果二级页 | 无 |
| 报告成功打开 | 01800 |
| 报告返回结果 | 01801 |
| 报告导出 | 01830 |
| 报告生成中 | 未覆盖：打开时报告已可阅读，没有生成中的反馈 |
| 报告失败 | 未覆盖：没有造出生成失败的报告 |
| 入池 | 无 |

### 选择分析企业（对象从对比篮来）

| 格 | 用例或原因 |
| --- | --- |
| 打开浮层 | 00903 |
| 名称搜索、类型筛选、重置 | 00921 |
| 企业类型选项个数 | 01821 |
| 全选与取消选择 | 01820 |
| 未勾选时确定不可用 | 00905 |
| 勾选后确定回填 | 00904 |
| 未选企业不能开始分析 | 00902 |
| 只选一家不能开始分析 | 01815 |
| 勾选后开始分析直到结果 | 01788 |
| 移除一家 | 01812 |
| 清空后取消 | 01811 |
| 清空后确定 | 01826 |
| 篮内翻页 | 未覆盖：篮内企业只有 2 家，没有第二页 |
| 新增并加入对比篮 | 01813 |
| 查看画像 | 01814 |
| 画像里的查看详情 | 01829 |
| 去掉已回填企业 | 01824 |
| 入口 A 的对象表 | 无 |

### 配置区

| 格 | 用例或原因 |
| --- | --- |
| 入口与标题 | 00900 |
| 与商业力菜单隔离 | 01818 |
| 模板三组 | 00907 |
| 加载模板恢复权重 | 00919 |
| 指标列 | 01823 |
| 默认五项与权重 | 00908 |
| 取消后再勾选 | 00909 |
| 权重上下调节 | 00910 |
| 合计偏离 100 | 01819 |
| 一键平均分配 | 00911 |
| 指标说明 | 01817 |
| 保存为个人模板后取消 | 01816 |
| 保存模板成功 | 01827 |
| 可信度五个选项 | 01791 |
| 覆盖卡片 | 01822 |
| 按企业名称定位 | 01828 |
| 当前分析与最近评估往返 | 00918 |

### 最近评估

| 格 | 用例或原因 |
| --- | --- |
| 列名 | 01802 |
| 翻页 | 01810 |
| 新建评估 | 01809 |
| 恢复结果 | 01803 |
| 按此配置新建评估 | 01804 |
| 查看 HTML 报告 | 01825 |
| 删除后取消 | 01805 |
| 删除后确定 | 01806 |
| 已取消行继续查看 | 01807 |
| 已取消行报告按钮 | 01808 |
| 另一种发起来源的行操作 | 无。历史任务都来自已选企业，没有第二套发起 |
| 取消任务、稍后查看、打开我的任务 | 未覆盖：再次开始分析会打开当天结果，重新分析会进入新结果，过程中没有稳定出现这些按钮 |

### 页面区块 → 用例

| 区块 | 用例 |
| --- | --- |
| 当前分析空态 | 00902 |
| 选择分析企业 | 00903、00904、00905、00921、01811–01814、01820、01821、01826、01829 |
| 评估对象条 | 01815、01824 |
| 评估模板 | 00907、00919 |
| 指标与权重 | 00908–00911、01817、01819、01823 |
| 保存为个人模板 | 01816、01827 |
| 数据覆盖与可信度 | 01791、01822、01828 |
| 开始分析 | 01788、01789 |
| 技术力评估结果 | 01788、01796–01799、00914 |
| 雷达与排名 | 00915、01792–01794 |
| 差距表与报告 | 01795、01800、01801、01825、01830 |
| 最近评估 | 01802–01810、00918 |
| 重新分析、调整配置 | 01790、00923 |

---

## 1. 用例总表

排列：主流程 → 备选 → 异常。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00900 | 企业分析 | 企业技术力评估对比分析 | 主流程-入口路由 | 入口隔离 | 企业技术力评估对比分析 | 进入技术力工作台 | 侧栏进入技术力评估页且路由携带技术力参数与标题正确 | 1、系统正常；2、已登录且可访问企业分析侧栏 | 1.点击侧栏「企业分析」→「企业技术力评估对比分析」 | 1、路由为企业评估页且携带 workspace=technology 参数；2、页标题为「企业技术力评估对比分析」 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-43 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜展示技术力指标库 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-01 | 接旧 00073 拆分（入口与标题收口本条）；mode=technology 同显形态（observed-执行时记录）；同壳层隔离归 01818；目标态路由差异以现场为准（coverage 开放项 7） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00902 | 企业分析 | 企业技术力评估对比分析 | 主流程-对象区空态 | 待选空态 | 企业技术力评估对比分析 | 对象空态与门控 | 未选评估对象时对象区显示空态引导且开始分析禁用 | 1、已进入技术力评估页；2、未选择任何评估对象 | 1.浏览评估对象区；2.浏览「开始分析」按钮 | 1、对象区显示前往对比篮选择企业的空态引导；2、「开始分析」为禁用态 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜多企业技术力对比分析 \｜未勾选两家企业时不可生成对比结果 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-07 | 接旧 00075 拆分（空态收口本条）；「开始分析」禁用为空态构成顺带点（零额外操作、同域同一到达态）；引导文案具体措辞（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00903 | 企业分析 | 企业技术力评估对比分析 | 主流程-选择分析企业浮层 | 浮层构成 | 企业技术力评估对比分析 | 评估对象选择 | 点击空态按钮打开选择分析企业浮层且构成正确 | 1、已进入技术力评估页；2、评估对象区为空 | 1.点击「前往对比篮选择企业」按钮 | 1、浮层打开且标题为「选择分析企业」、副标题含从对比篮勾选与确定回填不发起分析的语义；2、浮层含企业 Tab、名称搜索框与企业类型筛选；3、企业列表含勾选框、查看画像与移除动作 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜多企业技术力对比分析 \｜勾选两家对比企业 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-02 | 接旧 00075 拆分（浮层构成收口本条）；2026-10-13 同壳层实勘：浮层直回填取代旧册「六类型弹窗」过时记载（映射见 coverage 附录与开放项 8）；企业 Tab 计数与对比篮基数一致（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00904 | 企业分析 | 企业技术力评估对比分析 | 主流程-浮层确定回填 | 勾选确定回填 | 企业技术力评估对比分析 | 评估对象回填 | 勾选两家企业确定后对象区回填且可发起分析 | 1、「选择分析企业」浮层已打开；2、列表含至少 2 家企业 | 1.在浮层勾选 2 家企业；2.点击「确定」 | 1、对象区回填已选企业条目；2、地址追加所选企业参数与对比篮来源标记；3、「开始分析」恢复可用 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜多企业技术力对比分析 \｜勾选两家对比企业 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-08 | 接旧 00075 拆分（回填收口本条）；对象区含返回对比篮调整按钮与按企业名称定位搜索框（零额外操作顺带核对）；地址参数现场形态（observed-执行时记录，同壳层勘察为企业参数数组与来源标记）；同一企业不重复计入对象集（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00905 | 企业分析 | 企业技术力评估对比分析 | 主流程-浮层按钮门控 | 未勾选禁用 | 企业技术力评估对比分析 | 对象选择门控 | 浮层按钮随勾选状态正确门控 | 1、「选择分析企业」浮层已打开 | 1.未勾选任何企业时点击「取消选择」；2.点击「确定」；3.勾选 2 家企业；4.点击「取消选择」；5.点击「确定」 | 1、未勾选时「取消选择」与「确定」均为禁用态且浮层不关闭；2、「取消选择」可清空当前勾选；3、清空后「确定」回到禁用且对象区无回填 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-01 | 新拆独立成条（旧册按钮门控混在 00075 断言中，本条收口）；回填正向路径归 00904（同册互指）；「重置」归 00921，「新增」归 01813 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00907 | 企业分析 | 企业技术力评估对比分析 | 主流程-模板三态 | 三态分组 | 企业技术力评估对比分析 | 模板分组 | 评估模板区呈现系统模板、我的模板与当次自定义配置三组 | 1、已进入技术力评估页 | 1.浏览评估模板区 | 1、模板区分系统模板、我的模板、当次自定义配置三组；2、系统模板名为「技术力标准模板」；3、当次自定义配置初始为「当前未保存配置」 | P0 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜默认勾选预设技术力指标 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-03 | 接旧 00076 拆分（三态构成收口本条）；我的模板初始计数随账号历史变化（现场勘察为 1 条「技术力评估个人模板」，observed-执行时记录）；手动改动后进入当次自定义配置态的标识形态（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00908 | 企业分析 | 企业技术力评估对比分析 | 主流程-指标与权重默认 | 默认维度与权重 | 企业技术力评估对比分析 | 技术指标构成 | 指标与权重区展示 5 项技术指标且默认权重和为 100 | 1、已进入技术力评估页；2、系统模板为默认加载态 | 1.浏览指标与权重区 | 1、指标区含技术人才、技术创新、技术转化、技术合作、技术投入 5 项；2、默认权重依次为 20、25、20、15、20 且和为 100；3、每项带权重调节钮与「查看」明细入口 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜展示技术力指标库 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-04 | 接旧 00077 拆分（默认构成收口本条）；默认权重为模板预设非均分、均分由「一键平均分配」主动承载（coverage #17 as-built 口径）；权重和实时提示形态（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00909 | 企业分析 | 企业技术力评估对比分析 | 主流程-指标组合与移除 | 勾选与移除 | 企业技术力评估对比分析 | 指标组合与移除 | 技术指标可移出当次组合且恢复勾选后权重回显 | 1、已进入技术力评估页；2、指标区 5 项技术指标可见 | 1.取消勾选任一技术指标；2.重新勾选该指标 | 1、取消勾选后该指标移出当次组合；2、恢复勾选后该指标权重回显 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜组合已选技术力指标 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-10 | 接旧 00077 拆分（组合与移除收口本条）；移除后权重和提示联动（observed-执行时记录）；保存模板取消归 01816 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00910 | 企业分析 | 企业技术力评估对比分析 | 主流程-权重调节与输入 | 调节与输入 | 企业技术力评估对比分析 | 权重设置 | 权重调节钮可增减数值且非法输入不生效 | 1、已进入技术力评估页；2、已带入至少 2 家企业 | 1.点击任一指标权重的上调钮一次；2.点击同一指标权重的下调钮一次；3.在该指标权重输入框输入 -1；4.再输入 1.5 | 1、上调后该指标权重数值增加；2、下调后数值回落；3、负数与小数输入不生效 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-03 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜为已选指标设置权重 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-11 | 接旧 00077 拆分（调节与输入校验收口本条，同时覆盖单指标权重非负校验）；输入框可输入性以现场为准（旧勘为 spinbutton 可输入，同壳层新勘为只读加调节钮，observed-执行时记录）；0 与 100 边界合法值（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00911 | 企业分析 | 企业技术力评估对比分析 | 主流程-一键平均分配 | 均分权重 | 企业技术力评估对比分析 | 权重均分 | 一键平均分配将已选指标权重均分且和保持 100 | 1、已带入至少 2 家企业；2、5 项指标全选且权重为非均分状态 | 1.点击「一键平均分配」；2.取消勾选 1 项指标；3.再点击「一键平均分配」 | 1、5 项全选时均分后各项权重为 20；2、取消 1 项后均分各项为 25；3、两次均分后权重和均为 100 | P0 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜默认按已选指标均分权重 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-12 | 接旧 00078；合计偏离 100 的提示归 01819；静置期间权重无自动变化（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00914 | 企业分析 | 企业技术力评估对比分析 | 主流程-分析完成转结果态 | 结果态进入 | 企业技术力评估对比分析 | 结果态进入 | 分析完成后自动转入结果态且地址视图参数切换 | 1、过程态已发起且任务进行中 | 1.等待分析任务完成 | 1、地址视图参数变为结果态；2、页面呈现技术力评估结果区且含得分呈现 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜展示技术力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology&view=result | M_ENT_TECH_POWER_SCORE | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-13 | 接旧 00083 拆分（结果态进入收口本条）；细项归 00915、01794、01795、01800；分析耗时（observed-执行时记录）；得分数值与后端一致性归算法库，本册不钉死数值 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00915 | 企业分析 | 企业技术力评估对比分析 | 主流程-结果态雷达对比 | 雷达对比 | 企业技术力评估对比分析 | 雷达对比 | 结果态雷达图按已选技术指标维度展示企业对比 | 1、已处于结果态；2、评估对象含至少 2 家企业 | 1.浏览结果态雷达对比区块 | 1、雷达图维度与已选技术指标对应；2、雷达图呈现各对比企业的技术力对比形态 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜多企业技术力对比分析 \｜以雷达图展示两家企业技术力对比 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-14 | 接旧 00083 拆分（雷达收口本条）；雷达维度与勾选指标的对应细核、对比对象指定交互（observed-执行时记录）；对比数值正确性归算法库 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01788 | 企业分析 | 企业技术力评估对比分析 | 主流程-已选对象发起 | 到成功结果 | 企业技术力评估对比分析 | 技术力评估结果 | 勾选两家企业并开始分析后进入技术力评估结果 | 1、已进入技术力评估页；2、对比篮至少有 2 家企业 | 1.点击「前往对比篮选择企业」；2.勾选 2 家企业；3.点击「确定」；4.点击「开始分析」；5.等待结果页加载完成 | 1、页面出现「技术力评估结果」；2、「技术力最高得分」有分值 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 金样；本页只有这一种发起方式 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01790 | 企业分析 | 企业技术力评估对比分析 | 主流程-重新分析 | 新的结果 | 企业技术力评估对比分析 | 重新分析 | 在结果页重新分析后得到一条新的评估结果 | 1、已打开一条已完成的技术力评估结果 | 1.点击「重新分析」；2.等待结果页加载完成 | 1、页面为「技术力评估结果」；2、任务 ID 与点击前不同；3、「技术力最高得分」有分值 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 点击后无弹出框，直接进入新结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01791 | 企业分析 | 企业技术力评估对比分析 | 主流程-可信度下拉 | 五个选项 | 企业技术力评估对比分析 | 数据覆盖与可信度 | 数据覆盖区的可信度下拉给出五个固定选项 | 1、评估对象已回填 | 1.展开可信度下拉 | 1、选项共 5 个（名称见附录A） | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01792 | 企业分析 | 企业技术力评估对比分析 | 主流程-对比对象A | 选项个数 | 企业技术力评估对比分析 | 技术力多维雷达对比 | 雷达的对比对象 A 只列出本次结果中的企业 | 1、已打开至少两家企业的技术力评估结果 | 1.展开雷达图左侧企业下拉 | 1、选项个数等于本次结果的企业数 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01793 | 企业分析 | 企业技术力评估对比分析 | 主流程-对比对象B | 选项个数 | 企业技术力评估对比分析 | 技术力多维雷达对比 | 雷达的对象 B 只列出本次结果中的企业 | 1、已打开至少两家企业的技术力评估结果 | 1.展开「对象 B」 | 1、选项个数等于本次结果的企业数 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01794 | 企业分析 | 企业技术力评估对比分析 | 主流程-加权排名 | 得分条 | 企业技术力评估对比分析 | 技术力加权排名 | 技术力加权排名用条形展示各企业得分 | 1、已打开至少两家企业的结果 | 1.滚动到「技术力加权排名」 | 1、每家企业有一条得分条；2、得分更高的企业条更长 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01795 | 企业分析 | 企业技术力评估对比分析 | 主流程-差距诊断表 | 列全集 | 企业技术力评估对比分析 | 技术指标与差距诊断 | 技术指标与差距诊断表列出全部列 | 1、已打开技术力评估结果 | 1.滚动到「技术指标与差距诊断」 | 1、表头共 6 列（列名见附录B） | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01796 | 企业分析 | 企业技术力评估对比分析 | 主流程-纳入评价企业 | 家数 | 企业技术力评估对比分析 | 技术力评估结果 | 结果摘要给出纳入评价企业的家数 | 1、已打开技术力评估结果 | 1.滚动到「纳入评价企业」 | 1、「纳入评价企业」显示家数 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01797 | 企业分析 | 企业技术力评估对比分析 | 主流程-对象集平均得分 | 分值 | 企业技术力评估对比分析 | 技术力评估结果 | 结果摘要给出对象集平均得分 | 1、已打开技术力评估结果 | 1.滚动到「对象集平均得分」 | 1、「对象集平均得分」显示分值 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01798 | 企业分析 | 企业技术力评估对比分析 | 主流程-高可信企业 | 家数 | 企业技术力评估对比分析 | 技术力评估结果 | 结果摘要给出高可信企业的家数 | 1、已打开技术力评估结果 | 1.滚动到「高可信企业」 | 1、「高可信企业」显示家数 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01799 | 企业分析 | 企业技术力评估对比分析 | 主流程-结果抬头 | 对象与时间 | 企业技术力评估对比分析 | 技术力评估结果 | 结果抬头展示本次对象家数与生成时间 | 1、已打开技术力评估结果 | 1.滚动到结果抬头 | 1、抬头含对象家数；2、抬头含生成时间 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01800 | 企业分析 | 企业技术力评估对比分析 | 主流程-HTML报告 | 目录 | 企业技术力评估对比分析 | 评估报告 | 查看 HTML 报告后进入只读报告并列出目录 | 1、已打开技术力评估结果 | 1.点击「查看 HTML 报告」 | 1、页面出现「技术力评估报告」；2、报告目录共 7 节（名称见附录C） | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 从结果页进入 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01803 | 企业分析 | 企业技术力评估对比分析 | 主流程-恢复结果 | 打开该行结果 | 企业技术力评估对比分析 | 最近评估 | 恢复结果打开该行对应的评估结果 | 1、最近评估中有已完成记录 | 1.在一条已完成记录上点击「恢复结果」 | 1、进入「技术力评估结果」；2、任务 ID 与该行一致 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01804 | 企业分析 | 企业技术力评估对比分析 | 主流程-按此配置新建 | 带回企业 | 企业技术力评估对比分析 | 最近评估 | 按此配置新建评估带回该行企业并停在配置页 | 1、最近评估中有已完成记录 | 1.在一条已完成记录上点击「按此配置新建评估」 | 1、回到当前分析配置；2、评估对象含该行企业；3、不自动进入结果页 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01814 | 企业分析 | 企业技术力评估对比分析 | 主流程-查看画像 | 三块摘要 | 企业技术力评估对比分析 | 企业画像快览 | 查看画像打开企业画像快览并展示三块摘要 | 1、选择分析企业已打开 | 1.在一家企业上点击「查看画像」 | 1、标题为「企业画像快览」；2、可见基础摘要、竞争力摘要与风险摘要 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01817 | 企业分析 | 企业技术力评估对比分析 | 主流程-指标说明 | 字段 | 企业技术力评估对比分析 | 指标与权重 | 查看打开指标说明并展示业务字段 | 1、指标与权重表已显示 | 1.在「技术人才」行点击「查看」 | 1、标题为「技术人才 · 指标说明」；2、含衡量目的、所属维度、业务口径、单位与指标方向；3、含适用范围、数据状态与缺失影响 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-27 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01822 | 企业分析 | 企业技术力评估对比分析 | 主流程-数据覆盖卡片 | 可信度与覆盖 | 企业技术力评估对比分析 | 数据覆盖与可信度 | 回填企业后覆盖区列出每家企业的可信度与覆盖 | 1、已回填至少 1 家企业 | 1.等待数据覆盖区加载完成 | 1、每家企业显示可信度；2、显示可用数据覆盖 | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01823 | 企业分析 | 企业技术力评估对比分析 | 主流程-指标列 | 列全集 | 企业技术力评估对比分析 | 指标与权重 | 指标与权重表列出全部列 | 1、已进入当前分析 | 1.滚动到指标与权重表 | 1、表头共 7 列（列名见附录F） | P0 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01825 | 企业分析 | 企业技术力评估对比分析 | 主流程-历史打开报告 | 进入报告 | 企业技术力评估对比分析 | 最近评估 | 从最近评估打开该行的 HTML 报告 | 1、最近评估中有已完成且报告可打开的记录 | 1.在该行点击「查看 HTML 报告」 | 1、进入该任务的技术力评估报告 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00918 | 企业分析 | 企业技术力评估对比分析 | 备选-Tab 切换保留配置 | 当前往返 | 企业技术力评估对比分析 | 双 Tab 导航 | 两 Tab 可往返且返回当前分析后当次配置保留 | 1、已带入对象并调整过权重；2、至少存在 1 条历史评估任务 | 1.点击「最近评估」Tab；2.点击「当前分析」Tab | 1、「最近评估」以列表呈现历史评估任务；2、返回后对象与权重保持原值；3、往返切换不产生新任务 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | N/A-工作台交互 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-03 | 接旧 00074；目标态四 Tab 现场为两 Tab，按 as-built 验证；无历史任务时空列表形态、任务列表字段全集（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00919 | 企业分析 | 企业技术力评估对比分析 | 备选-模板加载恢复 | 系统与个人模板 | 企业技术力评估对比分析 | 模板恢复 | 加载系统模板与个人模板均恢复指标与权重且不恢复对象 | 1、已带入至少 2 家企业；2、我的模板已存在至少 1 条 | 1.用调节钮修改任一指标权重；2.重新点选系统模板「技术力标准模板」；3.点选我的模板中的「技术力评估个人模板」 | 1、重选系统模板后指标与权重恢复为预设 20、25、20、15、20；2、点选个人模板后恢复其保存的指标与权重；3、模板加载不恢复企业对象 | P1 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜默认勾选预设技术力指标 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-04 | 接旧 00076 拆分（模板恢复收口本条，系统与个人模板同问收口）；个人模板只存指标与权重不存对象（口径见 USM-23）；当次自定义配置态标识形态（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00921 | 企业分析 | 企业技术力评估对比分析 | 备选-浮层过滤与重置 | 搜索筛选重置 | 企业技术力评估对比分析 | 对象列表过滤 | 浮层内名称搜索、类型筛选与重置均正确作用 | 1、「选择分析企业」浮层已打开；2、列表含多家企业 | 1.在搜索框输入任一企业名称关键词；2.清空搜索；3.展开企业类型筛选并选择任一类型；4.点击「重置」 | 1、名称搜索后列表仅含匹配企业；2、类型筛选后列表仅含该类型企业；3、重置后勾选与筛选回到初始态 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-06 | 新拆独立成条（旧册过滤与重置漏测，本条补）；命中条数不钉死、搜索与筛选组合行为、重置是否影响已回填对象（observed-执行时记录）；「新增」按钮勘察仅见按钮（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00923 | 企业分析 | 企业技术力评估对比分析 | 备选-调整配置返回 | 返回配置态 | 企业技术力评估对比分析 | 调整配置 | 结果态调整配置可返回配置态 | 1、已处于结果态 | 1.点击「调整配置」按钮 | 1、页面返回配置态且评估对象区可见；2、地址视图参数离开结果态 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | T11 \｜技术力模型构建与参数自定义 \｜指标或权重变更后实时重算技术力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-08 | 新拆独立成条（2026-10-13 同壳层实勘按钮）；返回后当次配置保留性（observed-执行时记录）；再发起归 01788，重新分析归 01790；变更后重算一致性归算法库 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01789 | 企业分析 | 企业技术力评估对比分析 | 备选-当天再次开始 | 不新增任务 | 企业技术力评估对比分析 | 当天相同条件 | 当天相同条件再次开始分析时打开已有结果且不新增任务 | 1、当天已有相同企业与模板的成功结果；2、配置区已带回这组企业 | 1.点击「开始分析」 | 1、打开已有的技术力评估结果；2、出现「已打开今天相同条件的评估结果」；3、任务 ID 与当天已成功的那次相同 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 同一用户同一条件当天不新增任务 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01801 | 企业分析 | 企业技术力评估对比分析 | 备选-返回评估结果 | 回到结果 | 企业技术力评估对比分析 | 评估报告 | 从只读报告返回技术力评估结果 | 1、已打开技术力评估报告 | 1.点击「返回评估结果」 | 1、回到「技术力评估结果」 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01802 | 企业分析 | 企业技术力评估对比分析 | 备选-最近评估列 | 列全集 | 企业技术力评估对比分析 | 最近评估 | 最近评估表列出全部任务列 | 1、已进入技术力评估页 | 1.点击「最近评估」 | 1、表头共 10 列（列名见附录D） | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01805 | 企业分析 | 企业技术力评估对比分析 | 备选-删除取消 | 记录仍在 | 企业技术力评估对比分析 | 最近评估 | 删除分析记录时取消则该行仍在 | 1、最近评估中至少有一条记录 | 1.在某行点击「删除」；2.在弹出框中点击「取消」 | 1、弹出框说明删除后列表不再显示；2、该行仍留在列表中 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01806 | 企业分析 | 企业技术力评估对比分析 | 备选-删除确定 | 记录消失 | 企业技术力评估对比分析 | 最近评估 | 确定删除分析记录后该行从列表消失 | 1、最近评估中至少有一条可删除记录 | 1.在某行点击「删除」；2.在弹出框中点击「确定」 | 1、该任务不再出现在最近评估列表 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 勘察时已确定删除一条历史记录 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01809 | 企业分析 | 企业技术力评估对比分析 | 备选-新建评估 | 空配置 | 企业技术力评估对比分析 | 最近评估 | 新建评估回到未选企业的配置页 | 1、当前在最近评估 | 1.点击「新建评估」 | 1、进入当前分析；2、对象区提示先在对比篮选择企业 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01810 | 企业分析 | 企业技术力评估对比分析 | 备选-最近评估翻页 | 第二页 | 企业技术力评估对比分析 | 最近评估 | 最近评估翻到第 2 页后换成另一批任务 | 1、最近评估总数超过一页 | 1.点击分页「2」 | 1、第 2 页任务与第 1 页不同 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01811 | 企业分析 | 企业技术力评估对比分析 | 备选-清空对比篮 | 取消仍在 | 企业技术力评估对比分析 | 选择分析企业 | 清空对比篮时取消则篮内企业仍在 | 1、选择分析企业已打开；2、篮内至少有 1 家企业 | 1.点击「清空对比篮」；2.在弹出框中点击「取消」 | 1、弹出框询问是否清空篮内全部企业；2、取消后原企业仍在篮内 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 确定清空会抹掉账号对比篮，本条只收取消 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01812 | 企业分析 | 企业技术力评估对比分析 | 备选-移除篮内企业 | 立即消失 | 企业技术力评估对比分析 | 选择分析企业 | 从篮内移除企业后该企业立即消失 | 1、选择分析企业已打开；2、篮内至少有 1 家企业 | 1.对一家企业点击「移除」 | 1、该企业不再出现在篮内；2、篮内企业计数减少 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 移除没有弹出框 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01813 | 企业分析 | 企业技术力评估对比分析 | 备选-加入对比篮 | 篮内出现 | 企业技术力评估对比分析 | 新增企业 | 从新增企业加入对比篮后篮内出现该企业 | 1、选择分析企业已打开 | 1.点击「新增」；2.按名称搜索一家企业；3.点击「加入对比篮」 | 1、该企业出现在篮内企业中 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01816 | 企业分析 | 企业技术力评估对比分析 | 备选-保存个人模板 | 取消 | 企业技术力评估对比分析 | 保存为个人模板 | 保存为个人模板时取消则仍留在配置页 | 1、已进入当前分析 | 1.点击「保存为个人模板」；2.点击「取消」 | 1、对话框标题为「保存为个人模板」；2、名称旁显示 30 字上限；3、取消后对话框关闭且仍在配置页 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01818 | 企业分析 | 企业技术力评估对比分析 | 备选-菜单隔离 | 标题不同 | 企业技术力评估对比分析 | 同壳隔离 | 进入商业力评估后标题与技术力不同，返回后恢复 | 1、当前在企业技术力评估对比分析 | 1.点击侧栏「企业商业力评估对比分析」；2.再点击侧栏「企业技术力评估对比分析」 | 1、商业力页标题为「企业商业力评估对比分析」；2、返回后标题为「企业技术力评估对比分析」 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-43 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 只验菜单隔离，不在商业力页做分析 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01820 | 企业分析 | 企业技术力评估对比分析 | 备选-全选与取消 | 已选计数 | 企业技术力评估对比分析 | 选择分析企业 | 全选当前筛选结果后可以取消选择 | 1、选择分析企业已打开；2、当前列表至少有 1 家企业 | 1.点击「全选当前筛选结果」；2.点击「取消选择」 | 1、全选后已选家数等于当前列表企业数；2、取消选择后已选为 0；3、「确定」变为禁用 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01821 | 企业分析 | 企业技术力评估对比分析 | 备选-企业类型 | 七个选项 | 企业技术力评估对比分析 | 选择分析企业 | 企业类型下拉给出七个固定选项 | 1、选择分析企业已打开 | 1.展开「全部企业类型」 | 1、选项共 7 个（名称见附录E） | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01824 | 企业分析 | 企业技术力评估对比分析 | 备选-去掉已选企业 | 家数减少 | 企业技术力评估对比分析 | 评估对象 | 去掉已回填企业后对象家数减少 | 1、评估对象区至少有 1 家企业 | 1.点击该企业名称旁的关闭图标 | 1、该企业离开对象区；2、「来自对比篮」的家数减少 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01826 | 企业分析 | 企业技术力评估对比分析 | 备选-清空对比篮 | 确定后篮空 | 企业技术力评估对比分析 | 选择分析企业 | 确定清空对比篮后篮内企业清空且计数变为 0 | 1、选择分析企业已打开；2、篮内至少有 1 家企业 | 1.点击「清空对比篮」；2.在弹出框中点击「确定」 | 1、出现「对比篮已清空」；2、篮内不再列出企业；3、「企业」计数变为 0 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 弹出框文案为确认清空全部企业且不删除企业数据。2026-10-18 点确定后已出现「对比篮已清空」，但企业列表与「企业」计数未变（缺陷候选）；预期仍按篮空且计数变为 0 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01827 | 企业分析 | 企业技术力评估对比分析 | 备选-保存个人模板 | 出现在我的模板 | 企业技术力评估对比分析 | 保存为个人模板 | 保存个人模板后该名称出现在我的模板 | 1、已进入当前分析 | 1.点击「保存为个人模板」；2.填写一个未占用的模板名称；3.点击「保存模板」 | 1、出现「个人模板已保存」；2、「我的模板」中出现该名称 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 对话框按钮为「保存模板」。勘察时用未占用名称保存后，下拉「我的模板」出现该名称 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01828 | 企业分析 | 企业技术力评估对比分析 | 备选-按名称定位 | 可见家数 | 企业技术力评估对比分析 | 数据覆盖与可信度 | 按企业名称定位后覆盖区只留下匹配企业 | 1、已回填至少 2 家企业；2、数据覆盖区已显示这些企业 | 1.在「按企业名称定位」输入一家已加载企业的名称 | 1、「当前可见」变为 1 / 已加载家数；2、覆盖区只保留名称匹配的企业 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 输入框在数据覆盖区，占位为按企业名称定位。两家已加载时输入其中一家名称后为当前可见 1 / 2 家 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01829 | 企业分析 | 企业技术力评估对比分析 | 备选-画像查看详情 | 进入企业详情 | 企业技术力评估对比分析 | 企业画像快览 | 从企业画像快览查看详情后进入企业详情页 | 1、企业画像快览已打开 | 1.点击「查看详情」 | 1、页面标题为「企业详情」；2、面包屑为「企业分析 / 对比篮 / 企业画像」 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 离开评估配置。勘察时主区曾加载失败并出现「重试」，终态以标题与面包屑判定 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01830 | 企业分析 | 企业技术力评估对比分析 | 备选-报告导出 | 付费锁定 | 企业技术力评估对比分析 | 评估报告 | 未付费时报告上的导出不能下载 | 1、已打开技术力评估报告 | 1.点击「导出」 | 1、「导出」为禁用且旁有「付费」；2、页面仍为「技术力评估报告」；3、没有出现下载文件 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 按钮带锁且禁用，旁侧橙色标记为付费。点击后不离开报告页，也没有完成提示或文件 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01807 | 企业分析 | 企业技术力评估对比分析 | 异常-已取消记录 | 失败页 | 企业技术力评估对比分析 | 最近评估 | 已取消记录点继续查看后进入失败页 | 1、最近评估中有状态为已取消的记录 | 1.在该行点击「继续查看」 | 1、页面出现「评估失败」；2、出现「重试」与「按此配置新建」 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01808 | 企业分析 | 企业技术力评估对比分析 | 异常-已取消记录 | 报告不可用 | 企业技术力评估对比分析 | 最近评估 | 已取消记录不能打开 HTML 报告 | 1、最近评估中有状态为已取消的记录 | 1.点击「最近评估」 | 1、该行「查看 HTML 报告」为禁用 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01815 | 企业分析 | 企业技术力评估对比分析 | 异常-仅一家企业 | 不能开始 | 企业技术力评估对比分析 | 开始分析 | 只回填一家企业时不能开始分析 | 1、对比篮至少有 1 家企业 | 1.只勾选 1 家企业并点击「确定」 | 1、「开始分析」为禁用；2、页面仍停在当前分析 | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  |  |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01819 | 企业分析 | 企业技术力评估对比分析 | 异常-权重合计 | 需调整 | 企业技术力评估对比分析 | 指标与权重 | 上调权重后合计偏离 100 并提示需要调整 | 1、当前为技术力标准模板；2、权重合计为 100% | 1.点击「技术人才」权重的上调钮 | 1、该权重数值增加；2、权重合计提示需调整为 100% | P1 |  |  |  |  |  | US-ENT-EVAL-TECH | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | 待 A 线回填 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=technology |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 下调可回到原值，本条只收偏离提示 |

---

## 2. 附录

### 附录A · 可信度下拉（5）

全部可信度、高可信、中可信、低可信、不可生成

### 附录B · 技术指标与差距诊断列（6）

企业、技术力综合得分、创新点（项）、研发投入占比（%）、数据可信度、领先差距与优势短板

### 附录C · 报告目录（7）

01 报告身份、02 执行摘要、03 对象与范围、04 关键发现、05 证据与分析、06 数据来源与生成说明、07 局限性与使用边界

### 附录D · 最近评估列（10）

任务名称、任务 ID、模式、企业摘要、模板 / 版本、创建时间、状态、可信度、报告、操作

### 附录E · 企业类型（7）

外资企业、高新技术企业、小微企业、上市企业、专精特新、小巨人、链主龙头

### 附录F · 指标与权重列（7）

选择、指标名称、分组 / 维度、数据状态、权重、数据来源、指标说明

---

## 3. 红线自检

- 金样只有 01788，步骤从「前往对比篮选择企业」到「技术力评估结果」。
- 入口 A 写无。没有第二种发起方式。
- 新号 01788–01825。返工补号 01826–01830。作废旧号不复用。00927 已删除。
- 主流程 31 条，备选 24 条，异常 4 条。主流程不少于备选与异常合计。
- 金样 01788、重新分析 01790 本轮未改。
