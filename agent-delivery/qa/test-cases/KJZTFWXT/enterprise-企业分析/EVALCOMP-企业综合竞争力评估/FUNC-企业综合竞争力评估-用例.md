# 智能服务集群-科技专题服务系统测试用例

> **文档类型**：测试用例（工作区 Markdown）
> **规范**：`agent-delivery/qa-test-case-spec.md`
> **测试类型**：FUNC
> **系统码**：KJZTFWXT
> **版本**：v2.2 · 2026-10-18（对照重写后返工四格；保留号仍在 00403–00437，新号 01988–02026）
> **模块**：企业综合竞争力评估（catalog `ent-eval-compete`）
> **金样**：01988（选定对象后开始分析，直到成功结果页）。旧金样标记已从 00403 / 00405 / 00409 / 00414 / 00419 备注移除
> **入口**：侧栏「企业分析」→「企业综合竞争力评估」
> **路由**：`/enterprise/evaluation?workspace=competitiveness`（同页带 `mode=competitiveness`）
> **环境**：https://edu.itic-sci.com/tts/svcz/ · 账号 admin / 123456
> **号段**：新号只用 01988–02087，本册用到 02026；未用号不写入用例
> **维护**：agent:qa-agent · 监管 human:黄敬洲

## 关评审控件清单

入口拓扑：只有一种发起。配置页选好对象并保持权重和为 100 后，点「开始分析」到成功结果。选择分析企业里的「确定」只回填，不发起。没有第二套对象工作台发起。入口 B：无。

| 格 | 用例或原因 |
| --- | --- |
| 入口 A · 开始分析到成功结果 | 01988（金样） |
| 入口 B · 已选对象另发起 | 无。确定只回填 |
| 开始分析 · 当天相同条件 | 01990 |
| 重新分析到新结果 | 01989 |
| 调整配置 | 00432 |
| 过程页 · 生成中 | 00413 |
| 过程页 · 取消任务 | 00434 |
| 过程页 · 稍后查看 | 02022 |
| 结果摘要 · 任务 ID / 对象 / 生成时间 | 01991 |
| 结果摘要 · 四张指标卡 | 01992 |
| 结果 · 单企诊断 | 00416 |
| 结果 · 双企对比 | 00417 |
| 结果 · 对比对象 A | 01993 |
| 结果 · 对象 B | 01994 |
| 结果 · 当前诊断企业 | 01995 |
| 结果 · 单企差距列 | 02000 |
| 结果 · 双企差距列 | 01996 |
| 结果 · 排名 | 00418 |
| 结果 · 短板提示 | 00419 |
| 结果 · 搜索 | 无 |
| 结果 · 翻页 | 无 |
| 结果 · 行按钮 | 无 |
| 报告 · 打开只读报告 | 00420 |
| 报告 · 七节目录 | 02020 |
| 报告 · 导出 | 02021 |
| 报告 · 失败任务 | 02009 |
| 报告 · 付费 | 02025 |
| 指标说明抽屉 | 02001 |
| 数据覆盖 | 02015 |
| 模板三组 | 00409 |
| 默认权重 | 00410 |
| 权重调节 | 00411 |
| 一键平均分配 | 00412 |
| 取消勾选维度 | 01999 |
| 权重和不为 100 | 00437 |
| 权重键入负数或小数 | 未覆盖：权重只靠调节钮，现场不能键入负数、大于 100 或小数 |
| 保存为个人模板 | 01998 |
| 重载系统模板 | 00428 |
| 未选对象时开始分析 | 00436 |
| 选择面板构成 | 00405 |
| 确定回填 | 00406 |
| 未勾选时确定不可用 | 00407 |
| 取消选择 | 00426 |
| 重置 | 02016 |
| 名称搜索与类型筛选 | 00424 |
| 企业类型选项个数 | 01997 |
| 全选当前筛选结果 | 02018 |
| 返回对比篮调整对象 | 02017 |
| 查看画像 | 02002 |
| 查看详情 | 02003 |
| 加入对比篮 | 02004 |
| 清空对比篮 · 取消 | 02005 |
| 清空对比篮 · 确定 | 02023 |
| 篮内移除 | 02026 |
| 回填后逐条移除 | 无。对象区没有逐条移除，只有返回选择面板 |
| 最近评估列 | 02006 |
| 恢复结果 | 02007 |
| 继续查看 · 已取消 | 02008 |
| 继续查看 · 失败 | 02009 |
| 按此配置新建评估 | 02010 |
| 查看 HTML 报告 · 历史行 | 02014 |
| 删除 · 取消 | 02011 |
| 删除 · 确定 | 02024 |
| 新建评估 | 02013 |
| 翻页 | 02012 |
| 侧栏隔离 | 02019 |
| 入口路由 | 00403 |
| 详情页下级 Tab | 未覆盖：查看详情进入企业详情后本次正文失败，没有可判定的下级 Tab |

## 1. 用例总表

> 顺序：主流程 → 备选 → 异常。

| 用例编号 | 功能模块 | 子功能模块 | 功能项 | 子功能项 | 页面 | 功能点 | 测试内容 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 是否通过 | 测试工程师 | 测试时间 | 审核员 | 测试截图 | 用户故事编号 | USM验收场景编号 | 原始需求文件 | 原始需求章节号 | 功能点ID | TRACE引用 | 路由route | metric_id | 交付口径tier | 关联任务ID | 自动化用例ID | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01988 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 分析发起 | 选定对象后开始分析，检查直到成功结果页 | 1、已进入综合竞争力评估；2、对比篮企业页至少有 1 家企业；3、权重和为 100 | 1.点击「前往对比篮选择企业」；2.勾选 1 家企业；3.点击「确定」；4.点击「开始分析」；5.等待出现综合竞争力评估结果 | 1、页面出现「综合竞争力评估结果」；2、结果含任务 ID；3、结果含纳入评价企业 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜展示企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-开始分析到结果 / 配置发起成功；金样；本页唯一发起方式；选择面板确定只回填，不单独发起 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00403 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 入口与路由 | 从侧栏进入综合竞争力评估页，检查路由与页标题正确 | 1、系统正常；2、已登录且可访问企业分析侧栏 | 1.点击侧栏「企业分析」→「企业综合竞争力评估」 | 1、路由为 `/enterprise/evaluation?workspace=competitiveness`；2、query 同显 `mode=competitiveness`；3、页标题为「企业综合竞争力评估 - 科技专题服务系统」 | P0 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-43 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | T18 \｜综合评估框架与指标库 \｜展示综合评估框架 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-01 | 主流程-入口路由 / 侧栏进入评估页；接旧 00097 部分；同壳层隔离归 02019；TRACE 目标态路由差异以现场 as-built 为准（开放项 8） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00405 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 评估对象选择 | 验证点击空态按钮打开「选择分析企业」浮层且构成正确 | 1、已进入综合竞争力页；2、评估对象区为空 | 1.点击「前往对比篮选择企业」 | 1、浮层打开且标题为「选择分析企业」；2、副标题含「从对比篮勾选」「确定回填；不会发起分析任务」语义；3、浮层含企业 Tab、名称搜索框、企业类型筛选；4、企业列表含勾选框、查看画像与移除动作 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | T18 \｜个性化竞争力评价与输出 \｜按用户设定计算企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-02 | 主流程-选择分析企业浮层 / 浮层构成；接旧 00099 部分；2026-10-13 实勘：浮层直回填路径（覆盖旧册「六类型弹窗」过时记载，映射见 coverage 附录）；结构性检查允许 4 点；企业 Tab 计数 5/50 与对比篮基数一致（observed-执行时记录）；重置见 02016；加入对比篮见 02004 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00406 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 评估对象回填 | 验证勾选 1 家企业点确定后对象区回填且可发起分析 | 1、「选择分析企业」浮层已打开 | 1.勾选 1 家企业；2.点击「确定」 | 1、对象区回填已选企业条目；2、URL 追加所选企业参数与对比篮来源标记；3、「开始分析」恢复可用 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | T18 \｜个性化竞争力评价与输出 \｜按用户设定计算企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-07 | 主流程-浮层确定回填 / 勾选确定回填对象；接旧 00099 部分；企业参数与来源标记现场形态（observed-执行时记录，勘察为 `enterprise_codes[]=xxx&source=compare-basket`）；回填后对象区含「返回对比篮调整对象」按钮与「按企业名称定位」搜索框（零额外操作顺带核对，同域同一到达态） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00409 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 模板分组 | 验证评估模板区呈现系统模板 / 我的模板 / 当次自定义配置三组 | 1、已进入综合竞争力页 | 1.浏览评估模板区 | 1、模板区分组为系统模板 / 我的模板 / 当次自定义配置三类；2、系统模板名为「综合竞争力标准模板」；3、我的模板数量随账号历史增减（初始账号为 0）；4、当次自定义配置初始为「当前未保存配置」 | P0 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18 \｜综合评估框架与指标库 \｜默认勾选预设评估指标 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-03 | 主流程-模板三态 / 模板区构成；接旧 00100 部分；系统模板名 2026-10-13 实勘为「综合竞争力标准模板」（非旧册「系统综合竞争力模板 v1.0」）；结构性检查允许 4 点；我的模板基数与 EVALTECH 现场不同（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00410 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 维度构成 | 验证指标与权重区展示 3 项综合维度且默认权重和为 100 | 1、已进入综合竞争力页；2、系统模板为默认加载态 | 1.浏览指标与权重区 | 1、维度为创新能力 / 经营能力 / 成长能力 3 项；2、默认权重为 40 / 40 / 20 且和为 100；3、每项带权重调节钮与查看明细入口 | P0 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18 \｜综合评估框架与指标库 \｜展示评估框架涵盖的多个维度 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness | M_ENT_COMPETITIVENESS_SCORE | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-09 | 主流程-指标与权重默认 / 默认维度与权重；接旧 00097 / 00101 部分；同时覆盖「展示评估指标库」「展示已选指标及权重」（coverage #2 / #7）；维度 vs 技术 / 市场 / 组织三类直接要求核对记 observed（开放项 7，组织能力缺口） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00411 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 权重设置 | 验证权重调节钮可增减数值且数值联动 | 1、已进入综合竞争力页；2、已带入至少 1 家企业 | 1.点击任一维度权重的上调钮一次；2.点击该权重的下调钮一次 | 1、上调后该维度权重数值加一档；2、下调后数值回落一档；3、权重输入框数值与按钮操作联动 | P0 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18 \｜综合评估框架与指标库 \｜为已选指标设置权重 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-10 | 主流程-权重调节 / 上下调节钮；接旧 00101 部分；调节步长与和值补偿规则（observed-执行时记录，勘察为 readonly 输入框 + 上下调节钮）；权重框不能键入非法值，见清单未覆盖 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00412 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 权重均分 | 验证一键平均分配将已选维度权重均分且和保持 100 | 1、已进入综合竞争力页；2、已带入至少 1 家企业 | 1.用调节钮将权重调成非均分态；2.点击「一键平均分配」 | 1、三项权重变为 34、33、33；2、权重和仍为 100 | P0 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18 \｜综合评估框架与指标库 \｜默认按已选指标均分权重 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-11 | 主流程-一键平均分配 / 均分权重；接旧 00101 部分；100 / 3 不整除时显示口径（observed-执行时记录，开放项 1）；静置无自动归一化（顺带核对，同域）；2 项维度均分各 50 场景（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00413 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 分析发起 | 验证点击开始分析后进入过程态且 URL 与任务标识正确 | 1、已带入至少 1 家企业；2、权重配置有效 | 1.点击「开始分析」；2.等待过程态页面呈现 | 1、页面进入过程态且标题为「综合竞争力评估生成中」；2、URL 含过程视图参数与分析类型参数；3、任务标识参数为「EVAL-年月日-三位序号」形态；4、页面含可视化分析过程区块与「取消任务」「稍后查看」按钮 | P0 |  |  |  |  |  | US-ENT-EVAL-COMP / US-ENT-EVAL-RESULT | ENT-EVAL-USM-05 / ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜展示综合竞争力计算中状态 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=processing |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-12 | 主流程-开始分析进过程态 / 分析发起与过程态；接旧 00105 部分；2026-10-13 实勘增量；任务标识现场形态 `EVAL-YYYYMMDD-NNN`（observed-执行时记录具体值）；过程态无伪造进度百分比（顺带核对）；稍后查看归 02022 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00414 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 结果态进入 | 验证分析完成后自动转入结果态且 URL 视图参数切换 | 1、过程态已发起（至少 1 家企业，配置有效） | 1.等待分析任务完成 | 1、URL 视图参数变为结果态；2、页面呈现综合竞争力评估结果区 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜展示企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result | M_ENT_COMPETITIVENESS_SCORE | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-04 | 主流程-分析完成转结果态 / 结果态进入；接旧 00105 部分；2026-10-13 实勘增量：结果态为本次重写最大增量；URL 其余参数保持（顺带核对）；分析耗时（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01991 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 结果摘要 | 验证成功结果页展示本次任务摘要 | 1、已处于成功结果页 | 1.阅读综合竞争力评估结果标题下的摘要 | 1、摘要含任务 ID；2、摘要含对象家数；3、摘要含生成时间 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜展示企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-结果任务摘要 / 任务信息；作废 00415 的指标说明入口；关评审后摘要无指标说明入口 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01992 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 结果指标卡 | 验证成功结果页展示四张竞争力指标卡 | 1、已处于成功结果页 | 1.阅读综合竞争力评估结果中的指标卡 | 1、有「综合竞争力最高得分」；2、有「纳入评价企业」；3、有「对象集平均得分」；4、有「高可信企业」 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜展示企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-结果四张指标卡 / 得分卡片；结构性 4 点；不钉死分值 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00416 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 雷达诊断 | 验证结果态雷达诊断区默认呈现单企诊断模式 | 1、已处于结果态 | 1.浏览「综合竞争力雷达诊断」区块 | 1、区块标题为「综合竞争力雷达诊断」；2、默认呈现单企诊断模式 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜以雷达图展示企业竞争力评价结果 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-14 | 主流程-雷达诊断单企模式 / 单企雷达诊断；接旧 00105 部分；单企对比口径 = 对象集均值与领先值（USM-05）；雷达维度随已选指标（顺带核对）；双企对比切换归 00417 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00418 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 竞争力排名 | 验证结果态展示综合竞争力排名且默认按得分降序 | 1、已处于结果态；2、评估对象含至少 2 家企业 | 1.浏览「综合竞争力排名」区块 | 1、排名区块列出各企业名次；2、默认按综合竞争力得分降序排列 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜展示企业竞争力排名 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result | M_ENT_COMPETITIVENESS_RANK | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-16 | 主流程-排名区块 / 排名呈现；接旧 00105 部分；排名数量字段呈现（observed-执行时记录）；排序方向切换入口以现场为准，无入口按 as-built 差异记（开放项 5） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00419 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 差距诊断 | 验证结果态展示竞争力与差距诊断且提示短板项 | 1、已处于结果态 | 1.浏览「综合竞争力与差距诊断」区块 | 1、区块存在且标题正确；2、诊断内容含竞争力短板项提示 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜展示短板提示 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result | M_ENT_SHORTBOARD_COUNT | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-05 | 主流程-差距诊断区块 / 短板与差距提示；接旧 00105 部分；同时覆盖「识别企业竞争力短板」（coverage #29）；诊断内容与短板清单（observed-执行时记录，不钉死）；「暂无短板」空态需构造特定对象，无法构造时按开放项 6 记 observed |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02000 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 差距诊断 | 验证单企诊断的差距表列出固定列 | 1、成功结果页处于单企诊断 | 1.阅读「综合竞争力与差距诊断」表头 | 1、列含维度、当前对象得分、对象集均值；2、列含对象集领先值、差距与优势短板 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜展示短板提示 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-单企诊断列 / 差距表列 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00420 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 评估报告 | 验证结果态提供查看评估报告入口且打开只读报告 | 1、已处于结果态 | 1.点击「查看 HTML 报告」 | 1、HTML 报告打开且页面标注只读；2、报告可返回评估结果 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | N/A-产品定义增量 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-17 | 主流程-评估报告入口 / HTML 报告；接旧 00105 部分；报告目录结构参照 KEYENT 同类七节形态（observed-执行时记录实际目录）；报告正文内容与得分一致性归算法库，本册不钉死 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02020 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 评估报告 | 验证只读报告按固定目录展示七节 | 1、已打开一条成功评估的 HTML 报告 | 1.阅读报告目录 | 1、目录含报告身份、执行摘要、对象与范围、关键发现；2、目录含证据与分析、数据来源与生成说明、局限性与使用边界 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=report |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-报告目录 / 只读报告章节；页眉为「企业评估 · 只读报告」。结构性 2 点概括七节，全名见附录 B |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02006 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 最近评估 | 验证最近评估表展示固定列 | 1、已进入综合竞争力评估 | 1.点击「最近评估」 | 1、表头含任务名称、任务 ID、模式、企业摘要、模板 / 版本；2、表头含创建时间、状态、可信度、报告、操作 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-最近评估列 / 任务表列；作废 00430 中的得分入口说法 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02007 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 恢复结果 | 验证已完成记录的恢复结果打开该次结果 | 1、最近评估中有状态为已完成的综合竞争力记录 | 1.在该行点击「恢复结果」 | 1、进入综合竞争力评估结果；2、结果任务 ID 与该行任务 ID 一致 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-恢复结果 / 已完成行；已取消、失败行没有恢复结果，见继续查看 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02001 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 指标说明 | 验证查看打开指标说明并给出业务字段 | 1、已进入综合竞争力评估配置 | 1.点击「创新能力」行的「查看」；2.关闭说明 | 1、标题为「创新能力 · 指标说明」；2、含衡量目的、所属维度、业务口径；3、含单位、指标方向、适用范围、数据状态、缺失影响 | P0 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-27 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18｜综合评估框架与指标库｜展示评估指标库 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-指标说明 / 查看抽屉；作废 00422；关评审后无技术/市场/组织映射段。结构性 3 点 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02015 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 数据覆盖与可信度 | 验证回填对象后数据覆盖区给出可见统计 | 1、已从选择分析企业确定至少 1 家企业 | 1.阅读「数据覆盖与可信度」 | 1、出现「全部可信度」；2、出现当前可见家数；3、无匹配时出现「未找到匹配企业」 | P0 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-07 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-数据覆盖 / 回填后覆盖区；作废 00408 的五档 Tab。预检失败时改为「预检未返回企业明细，请确认对象编码或稍后重试」，见备注不另写通过 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01997 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 对象筛选 | 验证选择分析企业里的企业类型下拉给出固定选项 | 1、「选择分析企业」已打开 | 1.展开「全部企业类型」 | 1、选项共 7 个；2、名称与附录 A 一致 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-企业类型下拉 / 类型选项个数；筛选结果见 00424 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02002 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 查看画像 | 验证篮内企业查看画像展示三段摘要 | 1、「选择分析企业」已打开 | 1.点击一家企业的「查看画像」 | 1、出现「企业画像快览」；2、含基础摘要、竞争力摘要、风险摘要 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-企业画像快览 / 画像区块；快览上另有「加入对比」「查看详情」，详情见 02003 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02003 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 查看详情 | 验证画像中的查看详情进入该企业详情页 | 1、企业画像快览已打开 | 1.点击「查看详情」 | 1、进入企业详情页；2、页标题为「企业详情 - 科技专题服务系统」 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-查看详情 / 画像进入详情；本次详情正文出现请求失败与重试，不把失败文案写成通过条件 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02004 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 加入对象 | 验证从新增企业把一家企业加入篮内列表 | 1、「选择分析企业」已打开 | 1.点击「新增」；2.在新增企业中对一家尚未在篮内的企业点击「加入对比篮」 | 1、新增企业窗口列出名称与操作；2、该企业出现在篮内企业列表 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-加入对比篮 / 新增企业；加入动作在本页新增窗口，不在结果表 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02010 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 按此配置新建评估 | 验证按此配置新建评估回到配置并带上该次对象 | 1、最近评估中有一条综合竞争力记录 | 1.在该行点击「按此配置新建评估」 | 1、进入当前分析配置；2、对象区出现该次企业；3、不立即产生新任务 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-按此配置新建评估 / 历史带入配置；旧任务可能因预检失败使开始分析不可用，不把不可用写成唯一通过条件 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02013 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 新建评估 | 验证最近评估的新建评估回到当前分析配置 | 1、已打开最近评估 | 1.点击「新建评估」 | 1、回到当前分析；2、页上出现评估对象与开始分析 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-新建评估 / 离开历史 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02014 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 查看 HTML 报告 | 验证已完成记录直接打开只读 HTML 报告 | 1、最近评估中有报告份数大于 0 的已完成记录 | 1.在该行点击「查看 HTML 报告」 | 1、进入只读报告；2、页上有「返回评估结果」与「导出」 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=report |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-历史查看报告 / 已完成行报告；结果页入口见 00420；目录见 02020 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02023 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 清空对比篮 | 验证清空对比篮并确定后篮变为空 | 1、「选择分析企业」已打开；2、篮内至少有 1 家企业 | 1.点击「清空对比篮」；2.在弹出框点击「确定」 | 1、出现「对比篮已清空」；2、企业计数变为「企业 0/50」；3、名单区出现「对比篮暂无企业」 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-清空对比篮确定 / 清空确定；取消路径见 02005。弹出框标题为清空对比篮 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02024 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 删除 | 验证删除分析记录并确定后该任务消失 | 1、最近评估至少有一条记录 | 1.在该行点击「删除」；2.在弹出框点击「确定」 | 1、出现「已删除」；2、该任务不再出现在最近评估；3、列表总条数减少 1 | P0 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-删除记录确定 / 删除确定；取消路径见 02011。弹出框标题为删除分析记录 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02025 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 付费 | 验证只读报告的付费标签点开后给出导出说明 | 1、已打开成功评估的只读 HTML 报告 | 1.点击「付费」 | 1、出现「付费用户可导出报告 PDF（演示：顶栏打开「付费权益」）」；2、页面仍停留在该只读报告 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=report |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-报告付费说明 / 付费；橙色标签，位于返回评估结果与导出之间。点击不离开报告 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02026 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 移除 | 验证篮内移除一家企业后该企业离开名单 | 1、「选择分析企业」已打开；2、篮内至少有 1 家企业 | 1.在该企业行点击「移除」 | 1、出现「已移出对比篮」；2、该企业离开篮内名单；3、企业计数减少 1 | P0 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 主流程-篮内移除 / 移除；无弹出框。行上按钮为查看画像与移除 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00407 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 对象选择门控 | 验证浮层内未勾选企业时确定与取消选择不可用 | 1、「选择分析企业」浮层已打开；2、未勾选任何企业 | 1.尝试点击「取消选择」按钮；2.尝试点击「确定」按钮 | 1、两按钮均为禁用态不可点击；2、浮层不关闭且不回填对象 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | T18 \｜个性化竞争力评价与输出 \｜未完成用户设定时不可计算综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-01 | 备选-浮层按钮门控 / 未勾选禁用；接旧 00099 部分；勾选后按钮恢复可用（顺带核对，同域同一到达态）；勾选态下取消选择路径归 00426 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00417 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 雷达对比模式 | 验证切换双企对比后雷达按两企业对比呈现 | 1、已处于结果态；2、评估对象含至少 2 家企业 | 1.在雷达诊断区切换为「双企对比」模式 | 1、雷达图切换为两企业对比形态；2、对比对象可指定 | P0 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜以雷达图展示企业竞争力评价结果 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-15 | 备选-雷达双企对比 / 双企对比模式；接旧 00105 部分；单企与双企往返不丢对象选择（observed-执行时记录）；对比对象指定交互形态（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00424 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 对象列表过滤 | 验证浮层内按名称搜索与按类型筛选均可过滤企业列表 | 1、「选择分析企业」浮层已打开；2、列表含多家企业 | 1.在搜索框输入任一企业名称关键词；2.清空搜索；3.展开企业类型筛选并选择任一类型 | 1、搜索后列表仅含名称匹配企业；2、清空后列表恢复；3、类型筛选后列表仅含该类型企业 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-03 | 备选-浮层搜索与类型筛选 / 名称搜索与类型筛选；接旧 00099 部分；命中条数不钉死（observed-执行时记录）；搜索与筛选组合行为（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00426 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 对象批量取消 | 验证浮层内取消选择可清空当前勾选 | 1、「选择分析企业」浮层已打开；2、已勾选企业 | 1.点击「取消选择」 | 1、勾选清空且确定按钮回到禁用 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-05 | 备选-取消选择清空 / 取消选择；接旧 00099 部分；确定按钮门控联动 00407（同册互指）；回填区无逐条移除，见清单 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00428 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 模板重载 | 验证重新选择系统模板后指标与权重恢复预设且对象不恢复 | 1、已带入至少 1 家企业；2、已用调节钮修改权重 | 1.重新选择系统模板「综合竞争力标准模板」 | 1、指标与权重恢复为模板预设 40 / 40 / 20；2、已带入的企业对象保持不恢复 | P1 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18 \｜综合评估框架与指标库 \｜默认勾选预设评估指标 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-07 | 备选-重载系统模板 / 模板恢复；接旧 00100 部分；「默认按已选指标均分权重」as-built 口径 = 默认为模板预设非均分，均分由一键平均承载（coverage #14）；加载我的模板恢复保存时组合（observed-执行时记录，保存框见 01998） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00432 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 调整配置 | 验证结果态调整配置可返回配置态 | 1、已处于结果态 | 1.点击「调整配置」按钮 | 1、页面返回配置态且对象区可见；2、URL 视图参数离开结果态 | P1 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18 \｜个性化竞争力评价与输出 \｜用户设定变更后重算企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-11 | 备选-调整配置返回 / 调整配置；接旧 00105 部分；2026-10-13 实勘按钮；返回后当次配置是否保留（observed-执行时记录）；再发起见 01988；重新分析见 01989；变更后重算一致性归算法库 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00434 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 取消任务 | 验证过程态取消任务后终止本次分析且配置保留 | 1、处于过程态（任务进行中） | 1.点击「取消任务」按钮 | 1、任务终止且页面离开过程态；2、已回填对象与配置不被清空 | P1 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=processing |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P1-13 | 备选-取消任务 / 过程态取消；接旧 00105 部分；2026-10-13 实勘按钮；取消后去向（回配置态或空态）以现场为准（observed-执行时记录）；计算失败提示形态不归本条（开放项 3） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01989 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 重新分析 | 验证结果页重新分析后出现新的成功结果 | 1、已打开一条成功的综合竞争力评估结果 | 1.点击「重新分析」；2.等待再次出现综合竞争力评估结果 | 1、新结果的任务 ID 与点击前不同；2、页面出现综合竞争力最高得分 | P1 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜用户设定变更后重算企业综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-重新分析到新结果 / 重新分析；作废 00433；无二次确认框；须等到新结果，不停在过程页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01990 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 开始分析 | 验证当天相同条件再次开始分析不新增任务 | 1、当天已用相同对象与权重成功完成一次评估；2、已从该结果回到配置且未改条件 | 1.点击「开始分析」 | 1、不产生新的任务 ID；2、打开该次已有评估结果 | P1 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-当天再次开始分析 / 相同条件复用；现场停在配置页并提示「已打开今天相同条件的评估结果」，地址附原任务号，结果区未自动展开。预期仍按打开已有结果写 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01993 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 雷达对象 | 验证双企结果左侧对象下拉的选项等于本次对象 | 1、成功结果的评估对象为 2 家 | 1.展开雷达区左侧对象下拉 | 1、该下拉对应对象 A；2、选项个数为 2 | P1 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜以雷达图展示企业竞争力评价结果 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-对象A下拉 / 对象下拉；全称随任务变化，不钉死企业名 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01994 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 雷达对象 | 验证双企结果的对象 B 下拉选项等于本次对象 | 1、成功结果的评估对象为 2 家 | 1.展开「对象 B」 | 1、选项个数为 2；2、选项与本次两家评估对象一致 | P1 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜以雷达图展示企业竞争力评价结果 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-对象B / 对象下拉；与对比对象 A 分开验收 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01995 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 差距诊断 | 验证切换当前诊断企业后诊断对象随之改变 | 1、成功结果的评估对象不少于 2 家 | 1.展开「当前诊断企业」；2.改选另一家企业 | 1、下拉选项个数等于本次对象家数；2、诊断区当前企业变为刚选的那一家 | P1 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜展示短板提示 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-当前诊断企业 / 诊断对象切换 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01996 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 差距诊断 | 验证双企对比下差距表改为两企业对照列 | 1、成功结果的评估对象为 2 家 | 1.点击「双企对比」 | 1、表头含企业 A 得分与企业 B 得分；2、表头含差值（A-B）与差异结论 | P1 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜以雷达图展示企业竞争力评价结果 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-双企差距表 / 双企对比列；单企列见 02000 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01998 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 个人模板 | 验证保存为个人模板打开名称框且字数上限为 30 | 1、已进入综合竞争力评估配置 | 1.点击「保存为个人模板」 | 1、出现模板名称输入框；2、字数计数以 /30 结尾 | P1 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-23 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18｜综合评估框架与指标库｜选取评估指标 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-保存为个人模板 / 名称计数；作废 00427 的保存成功断言；本次只见到打开后的计数，未另造一条保存成功 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-01999 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 指标选择 | 验证取消勾选一项维度后权重和离开 100 | 1、三项维度均已勾选且权重和为 100 | 1.取消勾选「成长能力」 | 1、权重合计变为 80%；2、合计行出现「需调整为 100%」 | P1 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18｜综合评估框架与指标库｜为已选指标设置权重 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-取消勾选指标 / 维度勾选；成长能力默认权重 20 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02005 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 清空对比篮 | 验证清空对比篮时取消则篮内企业仍在 | 1、「选择分析企业」已打开且篮内有企业 | 1.点击「清空对比篮」；2.在弹出框点击「取消」 | 1、弹出文案说明不会删除企业数据；2、取消后原企业仍在篮内列表 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-清空对比篮取消 / 清空取消；确认框标题为清空对比篮。确定后清空会删掉共享篮，本环境不写确定路径 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02011 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 删除 | 验证删除分析记录时取消则该记录仍在 | 1、最近评估至少有一条记录 | 1.在该行点击「删除」；2.在弹出框点击「取消」 | 1、弹出文案说明删除后列表不再显示；2、取消后该任务仍在列表中 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-删除分析记录取消 / 删除取消；确认框标题为删除分析记录。确定会删共享历史，本环境不写确定路径 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02012 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 翻页 | 验证最近评估翻到第二页后仍是评估任务 | 1、最近评估总数超过一页 | 1.点击页码 2 | 1、列表换成另一批任务；2、表头列与第一页相同 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-最近评估翻页 / 第二页；现场共 16 条，可翻到第 2 页 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02016 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 重置 | 已勾选后点重置，检查当前已选不被清掉 | 1、「选择分析企业」已打开；2、已勾选至少 1 家 | 1.点击「重置」 | 1、已选家数与点击前相同；2、「确定」仍可点击 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-重置已选 / 重置；作废 00423。重置并不清空勾选 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02017 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 调整对象 | 验证回填后可返回选择分析企业面板 | 1、对象区已回填至少 1 家企业 | 1.点击「返回对比篮调整对象」 | 1、再次打开「选择分析企业」；2、副标题仍说明确定只回填、不会发起分析 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-返回对比篮调整对象 / 回到选择面板；从历史按此配置进入时，对象区按钮文案为「返回对比篮」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02018 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 全选 | 验证列表已全选时再点全选会取消已选 | 1、「选择分析企业」已打开；2、当前列表中的企业都已勾选 | 1.点击「全选当前筛选结果」 | 1、已选家数变为 0；2、「确定」变为不可用 | P1 |  |  |  |  |  | US-ENT-EVAL-OBJ | ENT-EVAL-USM-01 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-全选当前筛选结果 / 全选切换；现场在仅 1 家且已选时点击后变为已选 0 家 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02019 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 工作台隔离 | 验证从侧栏进入技术力评估不会留在综合竞争力 | 1、已登录且能看到企业分析侧栏 | 1.点击侧栏「企业技术力评估对比分析」 | 1、地址进入技术力评估；2、页标题含企业技术力评估 | P1 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-43 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.3 | N/A-同壳层隔离 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-同壳层隔离 / 侧栏到技术力；作废 00404。技术力、商业力正向用例不在本册。商业力侧栏同理，不并进本条 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02021 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 导出 | 验证只读报告的导出给出可取得的文件或完成提示 | 1、已打开成功评估的只读 HTML 报告 | 1.点击「导出」 | 1、出现文件下载或导出完成提示 | P1 |  |  |  |  |  | US-ENT-EVAL-RESULT | ENT-EVAL-USM-26 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=report |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-导出报告 / 导出；页内说明为先阅读再导出 PDF。同页「付费」见 02025 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02022 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 稍后查看 | 验证生成中稍后查看转入最近评估且任务仍在 | 1、过程页处于综合竞争力评估生成中 | 1.点击「稍后查看」 | 1、进入最近评估列表；2、本次任务仍在列表中 | P1 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.2 | T18｜个性化竞争力评价与输出｜展示综合竞争力计算中状态 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 备选-稍后查看 / 离开过程页；作废 00435。现场没有「打开我的任务」 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00436 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 开始分析门控 | 验证未选评估对象时开始分析按钮禁用 | 1、已进入综合竞争力页；2、评估对象区为空 | 1.尝试点击「开始分析」按钮 | 1、「开始分析」为禁用状态且不可发起 | P0 |  |  |  |  |  | US-ENT-EVAL-COMP | ENT-EVAL-USM-05 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | T18 \｜个性化竞争力评价与输出 \｜未完成用户设定时不可计算综合竞争力得分 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-20 | 异常-开始分析门控 / 未选对象禁用；接旧 00105 / 00102 部分；带回对象后恢复可用由 00406 预期 3 承载（同册互指）；权重和校验拦截归 00437 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-00437 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 权重和校验 | 验证权重和不为 100 时开始分析被拦截且不自动归一化 | 1、已带入至少 1 家企业；2、权重和可偏离 100 | 1.用调节钮将权重和调至非 100；2.点击「开始分析」；3.点击「一键平均分配」；4.再次点击「开始分析」 | 1、权重和≠100 时「开始分析」被拦截且无任务发起；2、提示定位权重和问题且权重不被静默归一化；3、一键平均后「开始分析」恢复可用 | P0 |  |  |  |  |  | US-ENT-EVAL-QUALITY | ENT-EVAL-USM-06 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10.1 | T18 \｜综合评估框架与指标库 \｜校验指标权重之和为 100% | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 | P0-21 | 异常-权重和校验 / 权重和拦截；接旧 00102 部分；和值偏离手段（手动输入 vs 按钮补偿规则）以现场为准（observed-执行时记录）；拦截形态禁用或提示（observed-执行时记录，开放项 2）；「至少一指标」「均已赋权」校验：2026-10-13 实勘 3 维度为固定组合、未见取消勾选控件，若执行发现控件再按旧 00102 步骤补录（observed-执行时记录） |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02008 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 继续查看 | 验证已取消记录的继续查看进入失败说明 | 1、最近评估中有状态为已取消的记录 | 1.在该行点击「继续查看」 | 1、页面出现「评估失败」；2、出现「重试」与「按此配置新建」 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 异常-继续查看已取消 / 已取消行；已取消行的继续查看当前落到评估失败，不另写成恢复结果 |
| ZNFWJQ-KJZTFWXT-v1.0-FUNC-02009 | 科技专题战略分析 | 企业分析 | 企业竞争力分析 |  | 企业综合竞争力评估 | 继续查看 | 验证失败记录的继续查看给出失败原因 | 1、最近评估中有状态为失败的记录 | 1.在该行点击「继续查看」 | 1、页面出现「评估失败」；2、页面给出失败原因；3、出现「重试」与「按此配置新建」 | P1 |  |  |  |  |  | US-ENT-EVAL-HISTORY | ENT-EVAL-USM-44 | 科技信息展示系统和科技专题服务系统.md | 1.1.1.2.4.2.3.10 | N/A-现场增量 | TRACE-ENT-EVAL.yaml | /enterprise/evaluation?workspace=competitiveness&view=result |  | INTEG | QA-KJZTFWXT-BLINE-CASE-ENT-L01 |  | 异常-继续查看失败 / 失败行；与已取消行分开验收 |

## 附录 A · 企业类型

外资企业、高新技术企业、小微企业、上市企业、专精特新、小巨人、链主龙头。共 7 个。

## 附录 B · 报告目录

01 报告身份、02 执行摘要、03 对象与范围、04 关键发现、05 证据与分析、06 数据来源与生成说明、07 局限性与使用边界。

## 2. 旧号处置

| 旧号 | 处置 | 新号 |
| --- | --- | --- |
| 00403 | 保留。去掉备注中的金样和评审句 | |
| 00404 | 作废。步骤使用对比篮里的技术力、商业力发起，本页没有这两个按钮 | 02019 |
| 00405 | 保留。去掉金样 | |
| 00406 | 保留 | |
| 00407 | 保留。功能项改为备选 | |
| 00408 | 作废。现场不是高、中、低、不可生成五档 | 02015 |
| 00409 | 保留。去掉金样 | |
| 00410 | 保留 | |
| 00411 | 保留 | |
| 00412 | 保留。预期改为现场的 34 / 33 / 33 | |
| 00413 | 保留 | |
| 00414 | 保留。去掉金样。完整发起到结果见 01988 | |
| 00415 | 作废。关评审后没有指标说明入口，卡片名称与原文不符 | 01991、01992 |
| 00416 | 保留 | |
| 00417 | 保留。功能项改为备选 | |
| 00418 | 保留 | |
| 00419 | 保留。去掉金样 | |
| 00420 | 保留。步骤改为「查看 HTML 报告」 | |
| 00421 | 删除。结果页没有「打开我的任务」。旧号不复用 | |
| 00422 | 作废。预期写入了现场没有的技术、市场、组织映射 | 02001 |
| 00423 | 作废。重置并不清空已选 | 02016 |
| 00424 | 保留 | |
| 00425 | 作废。权重不能键入，旧步骤无法执行。旧号不复用 | |
| 00426 | 保留 | |
| 00427 | 作废。保存成功未在本次形成终态，只重写打开后的计数 | 01998 |
| 00428 | 保留 | |
| 00429 | 作废。回填后的对象区没有逐条移除。旧号不复用 | |
| 00430 | 作废。列说明写成了得分入口，与表现场列名不符 | 02006 |
| 00431 | 删除。评审专条。旧号不复用 | |
| 00432 | 保留 | |
| 00433 | 作废。停在过程态，没有到新结果 | 01989 |
| 00434 | 保留 | |
| 00435 | 作废。预期依赖不存在的「我的任务」 | 02022 |
| 00436 | 保留 | |
| 00437 | 保留 | |

## 3. 红线自检

- 金样只有 01988，步骤从选择对象走到成功结果页。
- 入口 B 写无。
- 新号 01988–02026。02027–02087 未使用。
- 返工四格：02023 清空确定、02024 删除确定、02025 付费、02026 篮内移除。01988、01989、01990 未改。02005、02011 仍为取消路径。
- 未改 code-registry.yaml。

## 4. 序号台账

| 测试类型 | 本册在用序号 | 本段用到的最大新号 |
| --- | --- | --- |
| FUNC | 保留 00403 等见上表；新号 01988–02026 | 02026 |
