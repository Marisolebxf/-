# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）
> **规范**：`agent-delivery/qa-test-case-spec.md` **v1.2**
> **测试类型**：FUNC
> **系统码**：KJZTFWXT
> **版本**：v3.1 · 2026-10-18（补丁 03424；金样改为从已完成记录进入）
> **模块**：深圳产业发展分析（catalog `chain-sz-dev`）
> **金样**：**03388**（只此一条：在已完成记录上点「查看结果」，打开「深圳产业发展分析结果」）
> **环境**：https://edu.itic-sci.com/tts/svcz/ · 账号 `admin` / `123456`
> **入口**：产业链分析 →「深圳产业发展分析」
> **路由**：`/industry-center/shenzhen?workspace=development&tab=development`
> **交付口径**：INTEG（前端 → Java → Python `/internal/*`）
> **维护**：agent:qa-agent · 监管 human:黄敬洲
> **本步**：只写人读用例。自动化用例 ID 仅保留对照重写前已回填的旧号。

## 关评审控件清单

入口拓扑：只有一种发起。对象名单发起没有。

| 区域 | 现场 | 用例 |
| --- | --- | --- |
| 入口 A | 分析对象 + 有效对比来源 + 发展目标，按钮「开始分析」 | 03424。点「开始分析」后仍停在配置页 |
| 入口 B | 无 | 无 |
| 任务列表 | 「分析记录」 | 03404 起 |
| 结果页 | 成功结果；生成失败停在失败页 | 03388 金样 / 03395 |

| 格 | 用例或原因 |
| --- | --- |
| 摘要·条件回显 | 03398 |
| 摘要·时间 | 无。结果页对象行没有单独的分析时间 |
| 摘要·权重 | 无 |
| 摘要·来源依据 | 00763 |
| 摘要·三类建议 | 00765 |
| 摘要·发展路径 | 00766 |
| 摘要·叙述降级 | 03419 |
| 摘要·全球案例匹配（配置区） | 03420 |
| 摘要·全球案例匹配（结果页） | 03421 |
| 筛选下拉·分析对象 | 03390（15 个）；占位 00756；搜索 03391 |
| 筛选下拉·对比来源 | 00760；随产业变化 03392 |
| 筛选下拉·任务状态 | 03405 |
| 开始分析·当天 | 未覆盖：造不出终态 |
| 重新分析 | 无。结果页、失败页、记录行都没有这个按钮 |
| 调整条件 | 03410「复制配置」回到配置且条件还在。03417 预期同样要求带回条件 |
| 结果搜索 | 无 |
| 表·路径列 | 03418 |
| 表·翻页 | 无。结果表没有分页器 |
| 表·勾选 | 无 |
| 表·行按钮 | 无 |
| 详情·抽屉 | 00764 关闭后仍在结果页；03399 写出区块标题 |
| 二级 | 无 |
| 报告·查看 | 03400 / 03411 |
| 报告·返回 | 03401 |
| 报告·导出 | 03402。按钮不可点击，没有文件 |
| 报告·下载 | 03413。失败记录见 03412 |
| 报告·付费 | 03403 |
| 入池 | 无 |
| 入口 B 整段 | 无 |
| 记录·列 | 03404 |
| 记录·每页条数 | 03416 |
| 记录·翻页 | 未覆盖：记录不到一页，下一页不可用 |
| 记录·查看结果 × 已完成 | 03408 |
| 记录·查看结果 × 失败 | 03409 |
| 记录·复制配置 | 03410 |
| 记录·查看报告 × 已完成 | 03411 |
| 记录·查看报告 × 失败 | 03412 |
| 记录·下载报告 × 已完成 | 03413 |
| 记录·下载报告 × 失败 | 03412 |
| 记录·删除取消 | 03414 |
| 记录·删除执行 | 03415 |
| 记录·分析中空态 | 03406 |
| 记录·重置筛选 | 03407 |
| 记录 × 入口 B | 无 |
| 单飞 | 未覆盖：失败任务大约一秒结束，造不出第二条仍在跑的任务 |
| 生成失败 | 03395 |
| 失败页返回配置 | 03396 |
| 失败页查看记录 | 03397 |
| 门控 | 00761 / 00778 |
| 重置 | 03394 |
| 主体区域 | 00758 |
| 发展目标 | 00767 / 03393 |
| 不自动开始 | 03389 |
| 不自动带入最近对比 | 00777 |
| Tab 往返 | 00772 |
| 对比菜单隔离 | 03422 |

## 1. 用例总表（总集列 + 右侧 GKX 扩展）

> 排列：**主流程 → 备选 → 异常**。金样只有 03388。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03423 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 进入发展分析页 | 从菜单进入深圳产业发展分析，检查路由与标题正确 | 1、系统正常；2、已登录 | 1.在左侧「产业链分析」中点击「深圳产业发展分析」 | 1、地址含 /industry-center/shenzhen，且工作区与页签均为 development；2、页标题为「深圳产业发展分析」 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜进入页面 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-入口与路由 / 页头与路由；作废 00754 后重写；菜单原文为「深圳产业发展分析」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00755 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 双 Tab 结构 | 验证顶部双 Tab 构成与默认选中态正确 | 1、已进入深圳产业发展分析页 | 1.读取顶部 Tab 构成；2.读取默认选中态 | 1、顶部含「深圳产业发展分析」与「分析记录」两枚 Tab，顺序一致；2、默认选中「深圳产业发展分析」，「分析记录」未选中 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜展示多套发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-07 | 主流程-入口与路由 / 双 Tab 构成；保留；Tab 往返见 00772；记录表见 03404 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03388 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 打开成功结果页 | 从已完成记录点「查看结果」，检查打开结果页 | 1、已进入深圳产业发展分析页；2、分析记录里有一条状态为「已完成」的记录 | 1.点击「分析记录」；2.在已完成记录上点击「查看结果」 | 1、页内出现标题「深圳产业发展分析结果」 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜查看结果 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果页 / 已完成记录打开结果；金样。从已完成记录的「查看结果」进入 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00756 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 选择目标产业 | 验证分析对象产业下拉未选态占位提示与选项加载正确 | 1、已进入页面；2、分析对象为初始未选态（已选时先重置） | 1.展开分析对象产业下拉；2.浏览下拉选项 | 1、未选产业时下拉呈引导占位提示「请选择产业」；2、下拉选项正常加载，含可选产业集群 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-02 | 主流程-分析配置区 / 产业下拉占位与选项；保留占位；选项个数见 03390 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03390 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 分析对象选项 | 验证分析对象下拉给出全部可选产业 | 1、已进入页面 | 1.展开分析对象下拉 | 1、可选产业共 15 个，名称见附录A | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜分析对象 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析配置区 / 产业下拉选项个数；补 00756 未写个数 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00757 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 选择目标产业 | 验证切换分析对象产业后已选值回显正确且主体保持锁定 | 1、已进入页面；2、产业已选任一值（如「新一代信息技术」） | 1.展开产业下拉并切换为另一产业；2.回读已选值；3.切回原产业；4.回读已选值；5.回读主体区域 | 1、切换后已选值回显为新选产业；2、切回后已选值回显为原产业；3、主体区域保持「深圳」只读锁定 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-08 | 主流程-分析配置区 / 产业切换回显与主体保持；保留 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00758 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 主体区域深圳固定只读 | 验证主体区域「深圳」只读锁定不可更改 | 1、已进入页面 | 1.点击主体区域「深圳」；2.尝试输入其他区域名；3.尝试清空「深圳」值；4.回读主体区域 | 1、主体区域固定显示「深圳」，呈只读锁定态；2、输入与清空均无法更改该值 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-03 | 主流程-分析配置区 / 主体深圳锁定；保留 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00759 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 有效对比结果显式绑定 | 验证对比结果绑定选择器未绑定态占位与只读形态正确 | 1、已进入页面；2、绑定选择器为未绑定态 | 1.定位「有效的深圳产业情况分析对比结果」选择器；2.读取未绑定态占位提示；3.在选择器内尝试直接键入文本 | 1、未绑定时呈占位提示「请显式选择有效结构化结果」（原文见附录A）；2、选择器为只读显式选择形态，不可自由键入 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-04 | 主流程-分析配置区 / 绑定选择器构成与占位；保留；无效项见 00760；门控见 00761 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00760 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 无效对比结果条目不可选 | 验证绑定下拉条目构成正确且无效条目不可选 | 1、已进入页面；2、绑定下拉中同时存在有效与无效条目 | 1.展开绑定下拉；2.浏览条目构成；3.点击一条置灰的无效条目；4.回读绑定值 | 1、下拉同时含有效条目与置灰无效条目；2、无效条目带不可作为输入的标注（原文样例见附录A）；3、点击无效条目后绑定值不变 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-09 | 主流程-分析配置区 / 绑定下拉条目构成与无效项过滤；保留；置灰原文见附录A |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00761 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 开始分析按钮门控 | 验证「开始分析」按钮随门禁满足状态联动门控 | 1、已进入页面；2、配置为初始空态 | 1.读取初始态「开始分析」按钮状态；2.仅选择一个产业；3.回读按钮状态；4.绑定一条有效对比结果；5.回读按钮状态 | 1、初始态「开始分析」置灰禁用；2、仅配置产业时按钮仍为禁用态；3、产业与有效对比结果齐备后按钮恢复可用 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-05 | 主流程-操作区 / 门控状态机；保留；走到成功结果见 03388 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03420 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 配置区提示 | 验证分析配置区展示全球案例匹配未纳入交付的提示 | 1、已进入分析配置 | 1.阅读配置区提示 | 1、配置区有「全球案例匹配本轮未纳入交付宣称。」 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜配置提示 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析配置区 / 全球案例匹配提示；结果页另句见 03421 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00763 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 展示建议所依据的短板与优势 | 验证成功结果页顶部来源依据快照构成完整 | 1、已有一条成功的深圳产业发展分析结果 | 1.经「分析记录」打开一条成功结果；2.浏览顶部来源依据区 | 1、顶部呈现来源依据快照，含独特优势、差距、劣势三类摘要 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜展示多套发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-10 | 主流程-结果态 / 来源依据快照；保留；对象行见 03398；抽屉见 03399 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03398 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 结果页对象行 | 验证成功结果页回显分析对象与任务编号 | 1、已有一条成功结果 | 1.打开该条成功结果 | 1、对象行同时给出分析对象与任务编号 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜结果摘要 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果态 / 对象与任务回显；历史结果对象行曾显示未选产业，预期仍要求回显发起时的产业 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00764 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 展示建议所依据的对比结果 | 验证成功结果页完整对比以只读抽屉展开且关闭后不离开 | 1、已有一条成功的发展分析结果 | 1.经「分析记录」打开一条成功结果；2.点击「展开完整对比结果」；3.关闭抽屉；4.回读当前页面 | 1、完整对比以只读抽屉呈现，不可编辑；2、关闭抽屉后仍停留在发展结果页 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜展示多套发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-11 | 主流程-结果态 / 完整对比只读抽屉；保留并改步骤为按钮原文；区块标题见 03399 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03399 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 完整对比区块标题 | 验证完整对比抽屉写出可见区块标题 | 1、已打开一条成功结果 | 1.点击「展开完整对比结果」 | 1、抽屉标题为「来源对比结果（只读）」；2、可见对比结果、对标研判、产业化潜力与发展阶段综合判断 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜完整对比 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果态 / 对比抽屉区块；对比结果表含维度与深圳，行有企业、专利、政策、人才 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00765 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 展示三类维度发展建议 | 验证成功结果页三类建议齐备且条目带「针对」标签 | 1、已有一条成功的发展分析结果 | 1.经「分析记录」打开一条成功结果；2.浏览建议区构成；3.浏览建议条目标签 | 1、政策、技术、人才三类建议齐备；2、建议条目带「针对」标签与适用条件 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜展示多套发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-12 | 主流程-结果态 / 三类建议与「针对」标签；保留 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00766 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 提供多套发展路径 | 验证成功结果页发展路径至少两套且不足时诚实标注 | 1、已有一条成功的发展分析结果 | 1.经「分析记录」打开一条成功结果；2.浏览发展路径区构成 | 1、发展路径至少两套，条目带「针对」标签与适用条件；2、可靠路径不足两套时标注不完整、不伪造路径 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜展示多套发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-13 | 主流程-结果态 / 多套路径与诚实标注；保留；表列见 03418；现场成功结果为两套，并有「不少于 2 套」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03418 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 路径表字段 | 验证发展路径表列出路径、适用条件、局限性与针对 | 1、已打开一条成功结果 | 1.阅读发展路径表头 | 1、表头为路径、适用条件、局限性、针对 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果态 / 发展路径表列；表上无分页、无勾选、无行按钮 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03419 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 结果页说明 | 验证成功结果页展示叙述降级说明 | 1、已打开一条成功结果 | 1.阅读结果页说明 | 1、页内有「叙述能力不可用，已按规则结果诚实降级。」 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜结果说明 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果态 / 叙述降级说明 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03421 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 结果页提示 | 验证成功结果页标明全球案例匹配未宣称交付 | 1、已打开一条成功结果 | 1.阅读结果页底部提示 | 1、页底有全球案例匹配本轮未宣称交付 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜结果提示 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-结果态 / 全球案例匹配提示；与配置区 03420 不是同一句 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03408 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 打开成功结果 | 验证从已完成记录打开该次成功结果 | 1、分析记录中有一条已完成的发展分析 | 1.打开「分析记录」；2.在该条上点击「查看结果」 | 1、打开该任务的成功结果页；2、页内有来源依据与发展路径 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜查看结果 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析记录 / 查看结果；失败记录的同名按钮见 03409 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03411 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 从记录打开报告 | 验证从已完成记录打开分析报告 | 1、分析记录中有一条已完成的发展分析 | 1.在该条上点击「查看报告」 | 1、打开该任务的分析报告 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜查看报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析记录 / 查看报告；报告章节见 03400 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03400 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 查看报告目录 | 验证结果页查看报告后能看到报告目录 | 1、已打开一条成功结果 | 1.点击「查看报告」 | 1、标题为「深圳产业发展分析报告」；2、目录共 7 节，名称见附录A | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜分析报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-报告 / 报告章节 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03401 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 从报告返回 | 验证从报告返回对应的分析结果 | 1、已打开一条发展分析报告 | 1.点击「返回分析结果」 | 1、回到「深圳产业发展分析结果」页 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜返回结果 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-报告 / 返回分析结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03404 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 分析记录字段 | 验证分析记录表展示任务、类型、状态、创建时间与操作 | 1、已进入深圳产业发展分析页 | 1.点击「分析记录」 | 1、表头为任务、类型、状态、创建时间、操作 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜分析记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析记录 / 记录表列；作废 00773；行上按钮为查看结果、复制配置、查看报告、下载报告、删除 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03405 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 状态筛选选项 | 验证任务状态下拉给出四个状态 | 1、已打开「分析记录」 | 1.展开「任务状态」 | 1、选项共 4 个：全部状态、分析中、已完成、失败 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜记录筛选 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析记录 / 任务状态选项 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03410 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 带回分析条件 | 验证复制配置带回该条的产业与对比来源 | 1、分析记录中至少有一条发展分析 | 1.在该条上点击「复制配置」 | 1、回到分析配置并回显该条产业与对比来源；2、不自动开始分析 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜复制配置 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析记录 / 复制配置；已完成与失败记录均可复制；结果页「按此配置新建分析」见 03417 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03416 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 分页条数选项 | 验证记录表每页条数下拉给出三个档 | 1、已打开「分析记录」 | 1.展开每页条数下拉 | 1、选项为 10 条/页、20 条/页、50 条/页，共 3 个 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜记录分页 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 主流程-分析记录 / 每页条数；翻页见清单未覆盖 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00767 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 政策/技术/人才三维目标勾选 | 验证发展目标三项勾选状态机回显正确 | 1、已进入页面 | 1.逐项勾选政策、技术、人才三项；2.取消其中一项；3.重新勾选该项；4.取消全部三项；5.重新勾选全部三项 | 1、勾选区由政策、技术、人才三项构成；2、勾选与取消后选中态即时正确回显；3、全取消后重新勾选，三项均恢复选中 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜校验建议覆盖政策、技术、人才三维 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P1-01 | 备选-分析配置区 / 发展目标三项勾选；保留；取消一项后按钮见 03393 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03389 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 不自动创建任务 | 验证只改产业与对比来源时不创建分析任务 | 1、已进入分析配置 | 1.选择一个产业；2.选择一条未置灰的对比来源；3.停留在配置页 | 1、页面仍是分析配置；2、不出现「深圳产业发展分析生成中」 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜不自动开始 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-操作区 / 改条件不自动开始；作废 00762 的后半；点「开始分析」才创建，见 03388 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03391 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 过滤产业选项 | 验证在分析对象中输入关键字后选项被收窄 | 1、已进入页面 | 1.展开分析对象下拉；2.输入「生物」 | 1、下拉只留下名称含「生物」的选项 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜分析对象搜索 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-分析配置区 / 产业搜索 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03392 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 对比来源联动 | 验证更换分析对象后对比来源列表按产业刷新 | 1、已进入页面 | 1.选择「新一代信息技术」并展开对比来源；2.改选「生物」并再次展开对比来源 | 1、第二次列表按「生物」刷新；2、仍含一条置灰的 PDF 项 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜来源联动 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-分析配置区 / 来源随产业变化 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03393 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 目标不全时的开始按钮 | 验证取消一项发展目标后仍可以开始分析 | 1、已选产业并绑定一条有效对比来源；2、「开始分析」可点 | 1.取消「技术」 | 1、「技术」变为未选；2、「开始分析」仍可点击 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜发展目标 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-分析配置区 / 取消一项发展目标 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03394 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 重置后来源与按钮 | 验证重置参数后对比来源清空且开始分析不可用 | 1、已选产业并绑定一条有效对比来源 | 1.点击「重置参数」 | 1、对比来源恢复为未选占位；2、「开始分析」不可点击 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜重置参数 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-操作区 / 重置参数；作废 00768。现场重置后分析对象上的产业名称仍留着 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00772 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 分析记录 Tab 切换 | 验证「分析记录」Tab 与发展分析 Tab 互斥切换且切回后条件保持 | 1、已进入页面；2、已选中产业并勾选目标 | 1.切到「分析记录」Tab；2.切回「深圳产业发展分析」Tab；3.回读已选产业与目标勾选 | 1、记录区与配置区互斥呈现，不叠加；2、切回后已选产业等配置条件保持 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜展示多套发展路径 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P1-06 | 备选-分析记录 / Tab 互切与条件保持；保留；曾用「海洋」切走再切回，产业仍在 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03422 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 不落到对比工作区 | 验证深圳产业情况分析对比页不出现发展分析的目标与来源绑定 | 1、已能看到产业链分析菜单 | 1.点击「深圳产业情况分析对比」 | 1、该页是对比配置并含标杆区域；2、不出现「发展目标」；3、不出现「有效的深圳产业情况分析对比结果」 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜工作区隔离 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-菜单隔离 / 对比页不承载发展配置；作废 00774。切回发展分析后，离开前选的产业不会留下来 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03407 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 恢复全部记录 | 验证重置筛选后任务状态回到全部并重新列出记录 | 1、已打开「分析记录」 | 1.把任务状态改为「失败」；2.点击「重置筛选」 | 1、任务状态回到「全部状态」；2、列表重新出现各状态的记录 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜重置筛选 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-分析记录 / 重置筛选 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03417 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 从结果回到配置 | 验证按此配置新建分析回到配置且不自动开始 | 1、已打开一条成功结果 | 1.点击「按此配置新建分析」 | 1、回到分析配置并带回该次产业与对比来源；2、不自动开始分析 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜按此配置新建分析 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-结果态 / 按此配置新建分析；现场曾回到空配置。预期仍要求带回该次条件 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03396 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 从失败页回配置 | 验证失败页返回配置重试后回到分析配置 | 1、当前停在生成失败页 | 1.点击「返回配置重试」 | 1、打开分析配置；2、不自动开始新的分析 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜返回配置重试 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-生成失败 / 返回配置重试；现场落地时产业与来源为空 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03397 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 从失败页看记录 | 验证失败页查看分析记录后打开记录表 | 1、当前停在生成失败页 | 1.点击「查看分析记录」 | 1、打开「分析记录」；2、能看到任务状态与记录表 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜查看分析记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-生成失败 / 查看分析记录 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03403 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 报告上的付费 | 验证点击报告上的付费不离开当前报告 | 1、已打开一条发展分析报告 | 1.点击「付费」 | 1、仍停留在当前报告页 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜报告付费 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 备选-报告 / 付费；点击后没有新页面 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00777 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 不自动继承最近结果 | 验证刷新页面不自动带入最近一次对比结果 | 1、已进入页面；2、账号下存在历史对比结果记录；3、当前未绑定任何对比结果 | 1.刷新页面；2.回读绑定选择器 | 1、刷新后绑定选择器保持未绑定占位态，不自动带入最近一次对比结果 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P1-11 | 异常-分析配置区 / 刷新不自动继承；保留 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00778 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 门禁未满足禁用触发 | 验证门禁未满足时「开始分析」任何触发方式均不发起任务 | 1、已进入页面；2、门禁未满足（如仅选产业未绑定结果） | 1.点击「开始分析」；2.聚焦按钮后按回车；3.回读页面与「分析记录」列表 | 1、禁用态下点击与回车均不创建任务、不跳转结果态；2、页面不静默代选产业或对比结果发起任务 | P0 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜智能建议推荐与发展路径规划｜未识别短板与优势时不可生成建议 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 | P0-14 | 异常-操作区 / 禁用态触发无效；保留 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03424 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 点开始后不进入生成 | 选定「新一代信息技术」与同产业来源后点「开始分析」，检查仍停在配置页 | 1、已进入深圳产业发展分析页 | 1.选择分析对象「新一代信息技术」；2.选择对比来源「CHAIN-20260821-016 · CHAIN-20260821-016」；3.点击「开始分析」 | 1、提示「尚未选择分析对象」；2、仍停在「分析配置」；3、不进入「深圳产业发展分析生成中」 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜开始分析 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-开始分析 / 同产业来源仍停配置；该来源与「新一代信息技术」同产业 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03395 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 分析以失败结束 | 验证对比来源与产业不一致时分析失败且不打开成功结果 | 1、已进入分析配置；2、对比来源里有可点、但与当前产业不一致的条目 | 1.选择「生物」；2.点选一条与「生物」不同产业的可点来源；3.点击「开始分析」；4.等待过程结束 | 1、过程以失败结束并给出失败说明；2、不打开成功结果页 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-03 | AC-US-CHAIN-SZ-03-02 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜生成失败 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-生成失败 / 来源不匹配；失败页有「返回配置重试」与「查看分析记录」。过程五段里第二段为来源校验失败 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03406 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 无在跑任务 | 没有进行中的任务时，检查按分析中筛选得到空列表 | 1、当前没有状态为分析中的发展分析 | 1.打开「分析记录」；2.把任务状态选为「分析中」 | 1、列表显示「暂无数据」 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜空记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-分析记录 / 分析中空态 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03409 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 失败不可打开结果 | 验证失败记录的查看结果不可用 | 1、分析记录中有一条失败的发展分析 | 1.在该条上点击「查看结果」 | 1、「查看结果」不可点击；2、不打开成功结果页 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜失败记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-分析记录 / 失败记录查看结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03412 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 失败不可打开报告 | 验证失败记录不能查看或下载报告 | 1、分析记录中有一条失败的发展分析 | 1.在该条上点击「查看报告」 | 1、「查看报告」与「下载报告」均不可点击；2、不打开报告页 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜失败报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-分析记录 / 失败记录的报告 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03413 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 已完成记录下载 | 验证已完成记录下载报告时得到文件或失败提示 | 1、分析记录中有一条已完成的发展分析 | 1.在该条上点击「下载报告」 | 1、得到报告文件，或出现失败提示；2、该记录状态仍为已完成 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜下载报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-分析记录 / 下载报告；现场点击后没有文件，也没有失败提示 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03402 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 报告导出 | 验证报告页导出不可用时不产生文件 | 1、已打开一条发展分析报告 | 1.点击「导出」 | 1、「导出」不可点击；2、不产生报告文件 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-04 | AC-US-CHAIN-SZ-04-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜导出报告 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-报告 / 导出不可用 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03414 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 删除后仍保留 | 验证取消删除后该条分析记录仍在 | 1、分析记录中至少有一条记录 | 1.在该条上点击「删除」；2.在对话框中点击「取消」 | 1、对话框说明删除后列表不再显示该条；2、该条仍留在列表中 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜取消删除 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-分析记录 / 取消删除 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-03415 | 科技专题战略分析 | 产业链分析 | 深圳产业发展分析 |  | 深圳产业发展分析 | 删除后记录消失 | 验证确认删除后该条分析记录从列表消失 | 1、分析记录中有一条可以删除的失败记录 | 1.在该条上点击「删除」；2.点对话框右下角执行删除的按钮 | 1、该条记录从列表消失 | P1 |  |  |  |  |  |  | US-CHAIN-SZ-05 | AC-US-CHAIN-SZ-05-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.2.7 | T07｜深圳产业发展分析｜删除记录 | TRACE-CHAIN-TOPIC-SHENZHEN.yaml | /industry-center/shenzhen?workspace=development&tab=development |  | INTEG | QA-KJZTFWXT-BLINE-CASE-IND-L01 |  | 异常-分析记录 / 执行删除；执行按钮原文是「确定」 |

## 2. 旧号处置

| 旧号 | 处置 | 新号 |
| --- | --- | --- |
| 00754 | 作废。步骤写成「深圳产业决策」，菜单上没有这个名字 | 03423 |
| 00755 | 保留 | — |
| 00756 | 保留。占位已闭合；个数另条补上 | 03390 |
| 00757 | 保留 | — |
| 00758 | 保留 | — |
| 00759 | 保留 | — |
| 00760 | 保留 | — |
| 00761 | 保留 | — |
| 00762 | 作废。停在创建任务，没有成功结果页 | 03388、03389 |
| 00763 | 保留。前置改为已有成功结果 | — |
| 00764 | 保留。打开步骤改为按钮原文「展开完整对比结果」 | 03399 补区块标题 |
| 00765 | 保留 | — |
| 00766 | 保留 | 03418 补表列 |
| 00767 | 保留 | — |
| 00768 | 作废。预期写成全部回到空态，现场只清空了对比来源 | 03394 |
| 00769 | 作废。不另写。清单标未覆盖 | — |
| 00770 | 作废。不另写。清单标未覆盖 | — |
| 00771 | 删除。页上没有「重新分析」，旧号不复用 | — |
| 00772 | 保留 | — |
| 00773 | 作废。列和按钮不是本页原文（写了关联报告、完成时间） | 03404 及记录行各条 |
| 00774 | 作废。后半句「切回后条件恢复」现场不成立 | 03422 |
| 00775 | 删除。评审专条，旧号不复用 | — |
| 00776 | 删除。评审专条，旧号不复用 | — |
| 00777 | 保留 | — |
| 00778 | 保留 | — |

新号用到 **03424**。03425～03487 未使用。

## 3. 覆盖自检

| 指标 | 数值 |
| --- | --- |
| 用例总数 | 52 |
| 主流程 | 28 |
| 备选 | 13 |
| 异常 | 11 |
| 主流程不少于备选加异常 | 是 |
| 金样 | 03388 |

## 4. 序号台账

| 测试类型 | 已用序号 | 说明 |
| --- | --- | --- |
| FUNC | 保留 00755～00761、00763～00767、00772、00777、00778；新号 03388～03424 | 本册不改 code-registry.yaml。本次补丁只用 03424 |

### 附录A 长枚举

**分析对象（03390）共 15 个**：新一代信息技术、生物、新能源、新材料、高端装备、智能网联新能源汽车、绿色环保、低空经济与空天、传统与创意、海洋、未来制造、未来信息、未来能源、未来空间、未来健康。

**对比来源置灰项（00760）**：（无效）导出 PDF 报告 · 不可作为输入。

**报告目录（03400）共 7 节**：报告身份、执行摘要、对象与范围、关键发现、证据与分析、数据来源与生成说明、局限性与使用边界。

**完整对比抽屉（03399）**：标题「来源对比结果（只读）」。区块为对比结果、对标研判、产业化潜力与发展阶段综合判断。对比结果表的行是企业、专利、政策、人才。
