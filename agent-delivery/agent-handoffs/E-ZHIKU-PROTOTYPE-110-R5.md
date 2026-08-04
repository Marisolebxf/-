# Handoff｜E-ZHIKU-PROTOTYPE-110-R5：ZHIKU-STRATEGY-ROADMAP / ZHIKU-STRATEGY-REPORT / ZHIKU-SMART-QUERY 三叶子闭环重实现

> **批次**：R5（重跑，延续 R1 打样确认 + R2/R3/R4 同一标准）
> **执行**：frontend-agent（监管人/认领：human:淮政玮）
> **日期**：2026-08-05
> **业务仓 commit**：`6a94e93`（主实现）+ `e3abfa7` / `44e59df`（AC 补漏），demo-ui-gaoduanzhiku-view @ origin/dev

## 1. 范围与实现（对照 bid-reference）

范围真源：`agent-delivery/bid-reference/高端智库/新型高端智库需求拆解.md`。R5 覆盖序号 **46-58**（110 项中 R1-R4 之外的剩余段），三叶子切分：

- **ZHIKU-STRATEGY-ROADMAP 领域技术线路**：序号 46-49（德尔菲问卷/可视化路线图设计/宏观统计与项目列表/开发精度总览）
- **ZHIKU-STRATEGY-REPORT 战略咨询报告与成果**：序号 50-54（研究报告全生命周期/洞察月刊/三方向热点/战略报告生成/成果案例）
- **ZHIKU-SMART-QUERY 智能问数**：序号 55-58（数据接入/多轮 NL 问数/数据看板/一键数据报告）

| 序号段 | 需求 | 落地 |
| --- | --- | --- |
| 46 | 德尔菲问卷系统+路线图设计工具+最近项目 | F-RM-01/02/03：概览三统计卡、最近项目混排（问卷/路线双类型标签、更新时间倒序、点击真实定位）、里程碑时间轴设计器 |
| 47 | 问卷全流程管理 | F-RM-02：新建校验→草拟→发放（🧪 回收模拟推进）→催办（幂等+动态记录）→归档研判（1-5 评分分布图+共识度） |
| 48 | 宏观统计/搜索筛选/路线项目列表 | F-RM-03：关键词+领域+状态筛选持久化、里程碑增删改（越界"扩展周期/改日期"双选）、版本快照（保存/回看/恢复前自动另存）、`?project=` URL 分享恢复、**生成路线研判报告（CT-RM-01）** |
| 49 | 开发精度总览四模块卡片 | F-RM-04：环形完成度+子项清单，"数据在用"子项随问卷/路线真实数据量联动，🧪 预置口径诚实标注 |
| 50 | 研究报告全生命周期 | F-SP-01：上传（🧪 解析中→就绪，自动摘要/关键词）、元信息编辑、版本 +1 历史回看、归档/还原、删除引用拦截 |
| 51 | 洞察月刊多维度展示 | F-SP-02：期次卡+详情（产业/技术/热点/资本四维区块）、方向订阅（站内推送记录，退订即停）、PDF/图片导出（🧪 文本代演） |
| 52 | 三方向热点分析 | F-SP-03：产业/技术/资本切换持久化、排名+涨跌、下钻抽屉（四源构成+近 6 期走势）、回链洞察期次；**热度指数 D1 missing 红问号（GAP，不伪闭合）** |
| 53 | 战略报告生成 | F-SP-04：研报/月刊/专家意见三类底料勾选、大纲预览随勾选实时变化、脱敏 🧪 声明、**生成写作预填任务（CT-SP-01）**、生成历史底料失效追溯 |
| 54 | 战略咨询成果展示 | F-SP-05：四统计卡（总数/投资/ROI/满意度）、ROI 卡点击切换"ROI 突出"筛选、案例详情弹卡（背景/做法/成效/回报）、已发布报告成果区（承接 R1 发布链路）；与案例广场共享数据源、入口态独立持久化 |
| 55 | 数据源接入 | F-SQ-01：新建（类型/连接串）、连接测试（🧪 模拟，含失败可重试路径）、启停联动统计卡、语义映射/质量校验清单 🧪 预置、承建归属常驻声明 |
| 56 | 智能问数多轮会话 | F-SQ-02：会话新建/切换/删除持久化、三阶段问数反馈、每轮 SQL（🧪 预置样例匹配）+图表/表格双视图+图型切换记忆、**未命中/停用源诚实提示（禁止伪造数值）**、收藏/CSV 真实导出 |
| 57 | 数据看板 | F-SQ-03：看板集合 CRUD+搜索标签过滤、多页拖拽编辑器（收编 S3 DashboardCanvas，key `zhiku-dashboard-pages-v1` 保留）、手动刷新时间戳+定时刷新 🧪 说明、删最后一页拦截 |
| 58 | 一键数据报告 | F-SQ-04：收藏结果勾选为底料、来源校验（停用源警示+双选处置）、**生成写作预填任务（CT-SQ-01）**、生成历史+底料失效标注 |

**110 项序号覆盖归属核对结论**：R4=1-45（战略研究三叶子）、**R5=46-58（本批）**、R3=59-81（人才两叶子）、R2=82-87（基础研究）、R1=88-110（报告写作）。1-110 **全部闭合，无未覆盖序号**；三份 TRACE §反向核对逐条登记（46-49 / 50-54 / 55-58），跨叶子引用（如 100/104/105/107 与写作模块共用页面）在 TRACE 标注归属不重复计数。

## 2. 产物清单

**叶子五件套 ×3**（`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/`）：

- `ZHIKU-STRATEGY-ROADMAP-领域技术线路/`：USM（4 故事 US-ZHIKU-RM-01…04，22 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 46-49 反向核对闭合、`ZHIKU-S3-*` rename 登记）。
- `ZHIKU-STRATEGY-REPORT-战略咨询报告/`：USM（5 故事 US-ZHIKU-SP-01…05，26 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 50-54 闭合、`ZHIKU-S1-CASE/INSIGHT-*` rename 登记、`ZHIKU-SP-HOTSPOT-INDEX` D1 missing GAP 登记）。
- `ZHIKU-SMART-QUERY-智能问数/`：USM（4 故事 US-ZHIKU-SQ-01…04，22 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 55-58 闭合、智谱/智树承建归属声明）。

**业务仓代码**（3 commits，29 files，约 +5154/−879）：

- `src/mock/`：`techRoadmap.ts`（前缀 `zhiku-rm-`：问卷/路线/快照/筛选/回收模拟计时恢复）、`strategyReport.ts`（前缀 `zhiku-sp-`：研报生命周期/订阅推送/热点/生成历史）、`cases.ts` 重构为 store（`zhiku-sp-`：双入口独立 UI 态）、`smartQuery.ts`（前缀 `zhiku-sq-`：数据源/会话/收藏/看板元数据/生成历史）；旧 `reportLibrary.ts` 删除（数据并入 strategyReport）。
- `src/views/tech-roadmap/`：Home 重构 + Overview/Delphi/Roadmap/Precision 四 Panel（URL tab+project 契约）。
- `src/views/report-mgmt/`：StrategyReportHome 重构 + Research/Insight/Hotspot/Generate 四 Panel；MyReportTaskHome 指标正名。
- `src/views/case-show/`：StrategyAchievementHome（四统计卡+ROI 筛选）、CasePlazaHome 复用 `CaseGallery`（entry prop 双入口）。
- `src/views/smart-query/`：SmartQueryHome 重构 + Source/Query/Dashboard/Report 四 Panel（承建归属常驻横幅）。
- `src/mock/metricSeed.ts` / `readinessSeed.ts`：`ZHIKU-S1-TASK/MATERIAL-*` → `ZHIKU-WR-*`（R1 遗留补正名）、`ZHIKU-S1-CASE/INSIGHT-*` → `ZHIKU-SP-*`、`ZHIKU-S3-*` → `ZHIKU-RM-*` 正名 + SP/SQ 新指标 12 枚；`ZHIKU-SP-HOTSPOT-INDEX` D1 missing + GAP 引用；rg 校验旧 id 仅存注释 rename 记录、无双 id 活跃引用。

## 3. AC-US 自走查表（RM 22 + SP 26 + SQ 22 = 70 条）

### ZHIKU-STRATEGY-ROADMAP（22 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| RM-01-01 三统计卡 ⓘ+🧪 | ✅ | SURVEY-TOTAL / DELPHI-COMPLETION / PROJECT-INPROGRESS，8 件套+就绪度四行 |
| RM-01-02 最近项目混排+倒序 | ✅ | 问卷/路线类型标签 |
| RM-01-03 点击真实定位条目 | ✅ | 问卷 focusId 展开 / 路线 `?project=` 打开设计器 |
| RM-01-04 动作后统计即时反映 | ✅ | store getter 实时联动 |
| RM-01-05 Empty+双入口 | ✅ | 新建问卷/新建路线按钮 |
| RM-02-01 新建校验入列置顶 | ✅ | 空标题/专家数<1/过期截止日拦截 |
| RM-02-02 四阶段单向流转 | ✅ | 按钮随阶段变化，归档只留查看 |
| RM-02-03 回收模拟推进+完成率联动 | ✅ | 🧪 标注，`resumeSurveyTimers` 刷新恢复 |
| RM-02-04 催办幂等+动态记录 | ✅ | 5 分钟重复拦截，站内演示声明 |
| RM-02-05 归档评分分布+共识度 | ✅ | 1-5 分布图（ECharts） |
| RM-02-06 刷新全保持 | ✅ | `zhiku-rm-` 前缀 |
| RM-03-01 三条件筛选+Empty | ✅ | 关键词/领域/状态叠加持久化 |
| RM-03-02 新建校验+默认里程碑 | ✅ | 起止倒挂拦截，默认"启动"里程碑 |
| RM-03-03 里程碑增删改+时间轴重排+进度重算 | ✅ | 状态着色，进度=已完成占比 |
| RM-03-04 仅剩一个拦截+越界双选 | ✅ | "确认扩展项目周期/返回修改日期" Modal |
| RM-03-05 快照保存/回看/恢复前自动另存 | ✅ | 历史倒序持久化 |
| RM-03-06 `?project=` 分享恢复+非法回落 | ✅ | 提示后回列表 |
| RM-03-07 生成路线研判报告（CT-RM-01） | ✅ | createTask 预填里程碑统计+快照说明，跳大纲 |
| RM-03-08 宏观统计卡 ⓘ+🧪 | ✅ | ROADMAP-PROJECT-TOTAL / PROJECT-INPROGRESS |
| RM-04-01 四模块卡+环形完成度 | ✅ | `e3abfa7` 补漏改环形进度 |
| RM-04-02 🧪 预置口径诚实标注 | ✅ | 顶部 Alert 声明非 CI 真实统计 |
| RM-04-03 子项明细+数据在用联动 | ⚠️ 偏离 | 子项明细**内联直出**（信息等价、免二次点击），未做抽屉；"数据在用"随问卷/路线数据量联动 ✅ |

### ZHIKU-STRATEGY-REPORT（26 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| SP-01-01 上传→解析中→就绪+🧪 摘要 | ✅ | `resumeParsing` 刷新恢复 |
| SP-01-02 关键词+行业筛选+Empty | ✅ | 持久化+清空按钮 |
| SP-01-03 元信息编辑+版本 +1 回看 | ✅ | 版本历史各版摘要 |
| SP-01-04 归档区回看+还原 | ✅ | 主列表隐藏 |
| SP-01-05 删除确认+引用拦截 | ✅ | 被生成记录引用的报告删除受阻并说明 |
| SP-01-06 研报总数卡 ⓘ+🧪 | ✅ | `ZHIKU-SP-RESEARCH-TOTAL` |
| SP-01-07 刷新全保持 | ✅ | `zhiku-sp-` 前缀 |
| SP-02-01 期次详情四维区块 | ✅ | 产业/技术/热点/资本 |
| SP-02-02 内容 🧪 自动生成标注 | ✅ | 演示态声明 |
| SP-02-03 订阅开关+站内推送+退订停止 | ✅ | pushRecords 持久化 |
| SP-02-04 导出 PDF/图片双选项 | ✅ | 🧪 文本代演说明 |
| SP-02-05 月刊总数卡 ⓘ+🧪 | ✅ | `ZHIKU-SP-INSIGHT-TOTAL` |
| SP-03-01 三方向切换持久化 | ✅ | hotspotDirection |
| SP-03-02 热度指数 D1 missing 红问号 | ✅ | 点开只显 GAP 治理引用，不显伪 8 件套、不伪装正式算法 |
| SP-03-03 下钻抽屉四源构成+走势 | ✅ | 🧪 标注，近 6 期折线 |
| SP-03-04 回链洞察期次 | ✅ | open-issue 跨 Panel 跳转 |
| SP-04-01 三类底料勾选+大纲实时预览 | ✅ | 每要点标注来源 |
| SP-04-02 未勾选禁用+tooltip | ✅ | 按钮 disabled |
| SP-04-03 生成写作预填任务（CT-SP-01） | ✅ | createTask+跳大纲确认 |
| SP-04-04 生成历史+底料失效追溯 | ✅ | 归档/删除态标注 |
| SP-04-05 脱敏/智能推荐 🧪 | ✅ | 演示态标注 |
| SP-05-01 四统计卡 ⓘ+🧪 | ✅ | CASE-TOTAL / INVEST-TOTAL / ROI-AVG / SATISFACTION |
| SP-05-02 ROI 卡点击筛选+视觉反馈 | ✅ | 高于均值过滤+激活态样式 |
| SP-05-03 案例详情弹卡完整 | ✅ | 背景/做法/成效/投资回报 |
| SP-05-04 已发布报告成果区回归 | ✅ | 承接 R1 发布链路（published） |
| SP-05-05 双入口共享数据+独立筛选态 | ✅ | CaseGallery entry prop（case-show/plaza） |

### ZHIKU-SMART-QUERY（22 条）

| AC | 结论 | 说明 |
| --- | --- | --- |
| SQ-01-01 新建数据源+校验 | ✅ | 名称/类型/连接串 |
| SQ-01-02 连接测试失败可重试 | ✅ | 🧪 模拟，失败显示原因 |
| SQ-01-03 启停联动统计卡 | ✅ | `ZHIKU-SQ-SOURCE-CONNECTED` ⓘ |
| SQ-01-04 语义映射/质量校验清单 🧪 | ✅ | 详情预置标注 |
| SQ-01-05 承建归属常驻声明 | ✅ | Home 级横幅（智谱/智树边界） |
| SQ-01-06 刷新保持 | ✅ | `zhiku-sq-` 前缀 |
| SQ-02-01 会话建/切/删+确认 | ✅ | 上下文持久化 |
| SQ-02-02 SQL+双视图+图型记忆 | ✅ | 🧪 预置样例标注，柱/线/饼切换 |
| SQ-02-03 未命中诚实提示+可问清单 | ✅ | 不伪造数值，一键填入重试 |
| SQ-02-04 收藏幂等+CSV 真实导出 | ✅ | 含真实数据行 |
| SQ-02-05 停用源提示+US-01 联动 | ✅ | missReason 引导去接入页启用 |
| SQ-02-06 会话数卡 ⓘ+🧪+承建声明 | ✅ | `ZHIKU-SQ-SESSION-TOTAL` |
| SQ-03-01 看板 CRUD+搜索标签过滤 | ✅ | 持久化 |
| SQ-03-02 多页拖拽编辑器复验 | ✅ | 收编 S3 DashboardCanvas，key 保留 |
| SQ-03-03 手动刷新+定时刷新 🧪 | ✅ | `44e59df` 补漏：时间戳更新+反馈+tooltip 说明 |
| SQ-03-04 删最后一页拦截+删看板确认 | ✅ | Modal 确认 |
| SQ-03-05 看板数卡 ⓘ+🧪+智树声明 | ✅ | `ZHIKU-SQ-DASHBOARD-TOTAL` |
| SQ-04-01 收藏勾选+预览实时更新 | ✅ | 🧪 标注 |
| SQ-04-02 来源校验+停用警示双选 | ✅ | 继续生成/去处理 |
| SQ-04-03 生成写作预填任务（CT-SQ-01） | ✅ | 底料摘要注入大纲，跳大纲确认 |
| SQ-04-04 生成历史+无收藏 Empty 引导 | ✅ | go-query 跳问数页 |
| SQ-04-05 一键报告承建声明 | ✅ | Home 级横幅覆盖 |

## 4. 验收证据

- `vue-tsc --build`：**0 错**（exit 0，三轮验证，末轮含两处 AC 补漏后全量）。
- `vite build`：**通过**（exit 0，仅 chunk 体积告警，与 R1-R4 一致）。
- 业务仓 push：`13bf8ee..6a94e93..e3abfa7..44e59df dev -> dev`，GitLab CI 自动触发（K8s dev rollout）。
- 走查路径：W1 概览→问卷发放/催办/归档研判→回概览统计联动 → W2 路线筛选→设计器里程碑编辑（越界双选）→快照保存/恢复→生成路线研判报告跨叶子 → W3 研报上传/版本/归档/引用拦截→月刊订阅推送→热点下钻回链→底料生成战略报告跨叶子 → W4 成果四卡+ROI 筛选→案例详情→已发布成果区↔案例广场双入口独立态 → W5 数据源启停→多轮问数（命中/未命中/停用源三态）→收藏 CSV→看板拖拽/手动刷新→一键报告跨叶子（对应三份 USM §5）。

## 5. 架构合规自检（公约 §2 十条）

1. 算法只在 Python：✅ NL2SQL/热度指数/自动摘要/解析全部 🧪 演示态并登记 GAP，无前端真实算法冒充。
2. 调用链：✅ demo 全 mock；正式态服务面已在三份 IA §7 声明（Java REST → Python internal / 智谱 / 智树集成边界）。
3. 图谱：✅ 本批不涉图谱组件，未引入 Neo4j。
4. 可观测性：✅ 沿用仓内 `observability.ts` 接线，未破坏。
5. CI/CD：✅ push dev 触发 Pipeline。
6. demo2 只读 merge：✅ 不涉及。
7. 共享聚合核心：✅ 前端只消费 mock/未来 Java REST。
8. 数据策略：✅ 指标 8 件套 source_tables 写 ADS 目标口径，Mock 填充。
9. 前端规范（D8）：✅ Arco Design Vue + ECharts 栈内；主色/token 未改。
10. 数据血缘（D9）：✅ 全部统计卡 ⓘ+metric_id+就绪度角标；`ZHIKU-SP-HOTSPOT-INDEX` D1 missing 红问号 GAP 引用；🧪 MockBadge 全量；S1/S3 rename + R1 遗留 WR 正名，rg 校验无双 id 活跃引用。

## 6. 偏离说明

- **RM-04-03**：开发精度子项明细为卡片内联直出而非下钻抽屉（信息等价、交互更直接），登记为实现偏离，如体验评审要求抽屉再补。
- **热点热度指数（序号 52）**：四源加权指标体系算法定义卡未落地，保持 D1 missing 诚实态（GAP-ZHIKU-SP-HOTSPOT-INDEX，挂 Q-ZHIKU-04），演示数值禁止对外决策展示。
- **NL2SQL（序号 56）**：为预置样例关键词匹配（🧪），真实语义解析归智谱问数服务；未命中一律诚实提示不伪造。
- **连接测试/分发催办/月刊导出/脱敏**：均为站内模拟演示（🧪 标注），无真实外部触达/文件渲染。
- **投资额/ROI/满意度口径（序号 54）**：财务与调查口径为演示值，正式口径待甲方确认（metricSeed mock_until 登记）。
- **看板定时刷新（序号 57）**：调度为智树侧能力，demo 仅手动刷新+🧪 说明。

## 7. cost 回填（budget-estimate 口径）

- `actual_tokens`：≈ 400,000（本批次会话累计，含三套五件套撰写与 12 Panel 实现及两轮 AC 补漏）
- `model_used`：claude-fable-5
- `actual_cost`：≈ $6.2（估算）
- `cost_warn`：false（< $10）

## 8. 遗留风险

- CI 流水线结果需在 GitLab 确认绿（`44e59df` push 后自动触发，本 handoff 提交时处于运行中）。
- 热度指数/NL2SQL/自动摘要三类算法能力依赖算法定义卡（Q-ZHIKU-04），上线前必须补齐或业务态置灰。
- 智谱问数/智树看板为三方承建集成边界，正式态接口契约（IA §7）需与承建方对齐后替换 mock。
- 案例投资/ROI/满意度业务口径待甲方确认（🟡，客户决策清单跟踪表待登记项）。
- localStorage 状态与 R1-R4 各域独立；演示前如需干净环境，清除 `zhiku-rm-` / `zhiku-sp-` / `zhiku-sq-` 前缀 key（S3 看板 `zhiku-dashboard-pages-v1` 保留兼容）。
