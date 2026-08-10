# Handoff — E-ZHIKU-PROTOTYPE-110-R1（R1 打样：ZHIKU-WRITING 写作链路闭环）

- **任务**：高端智库重跑-R1-打样-ZHIKU-WRITING 写作链路闭环（报告创作 + 素材库 + 报告任务 + 成果区）
- **执行**：agent:frontend-agent（监管人待签）
- **日期**：2026-08-05
- **仓库**：`${GKX_ROOT}/repos/demo-ui-gaoduanzhiku-view`（branch `dev`）
- **commit**：`988bfcb` feat(writing): R1 重跑——ZHIKU-WRITING 写作链路闭环重实现 [agent:frontend-agent]

## 1. 范围与实现（对照 TRACE-ZHIKU-WRITING，序号 88-110）

### 1.1 五件套（产品定义，已于本任务前半段落盘）

`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/ZHIKU-WRITING-报告智能写作/`

| 产物 | 文件 |
|---|---|
| USM（8 故事 / WR-01~WR-08，E2 粒度） | `USM-ZHIKU-WRITING.md` |
| IA（7 Frame + 对象定义 + 边界） | `IA-ZHIKU-WRITING.md` |
| Wireframe（F-WR-01~07 字段表含 metric_id） | `Wireframe-ZHIKU-WRITING.md` |
| UX-SPEC（旅程/状态/异常/键盘可达） | `UX-SPEC-ZHIKU-WRITING.md` |
| TRACE（88-110 → 故事 → Frame → 页面矩阵） | `TRACE-ZHIKU-WRITING.yaml` |

### 1.2 代码实现（12 文件，+1864/-374）

**领域层（`src/mock/writing/`）**

| 文件 | 内容 |
|---|---|
| `types.ts` | 领域模型重构：`ReportSection/ReportParagraph(citationIds,fromIdea)/ReportChartBlock(style 持久化)/ReportCitation(derivation 提炼过程 + sourceDoc 原文 + materialId 素材回链)/NlIntent` |
| `taskStore.ts` | Pinia store reducer 化：create/updateOutline/confirmOutlineAndWrite/updateParagraph/previewRewrite/setChartStyle/saveVersion/submit/approve/**reject（驳回意见）**/remove/resetToSeed；**localStorage 持久化**（key `zhiku-wr:`）；后台写作进度定时器**刷新可恢复**（resumeWritingTimers） |
| `generator.ts` | 规则式内容生成（🧪）：按大纲+分析思路生成段落；脚注编号连续、保底 ≥3 角标；素材引用与系统来源**同格式**；数据类章节自动挂图表卡（含来源脚注） |
| `nl.ts` | NL 意图解析（🧪 规则式）：主题/类型/时间范围抽取 + 歧义追问 + 推荐章节；信息量不足返回 null 触发拦截提示 |
| `exporter.ts` | 真实文件导出：Word（HTML 内容流 .doc 下载）/ PDF（打印视图另存 PDF）；图表导出为数据表 + 来源注记 |
| `persist.ts` | localStorage 助手（异常静默，不阻断 demo） |

**视图层**

| 页面 | 覆盖序号 | 闭环要点 |
|---|---|---|
| `WritingCreateHome.vue`（F-WR-01/02/03/04/05） | 88-90,94-99,101,103-106,108-110 | 三态入口 + **NL 双入口**（解析→追问→确认发起）；配置页模板大纲实时预览 + 素材关联（仅已解析）；大纲确认：章节增删改**上下移** + 每章**分析思路** + 常用章节面板；编辑器：脚注角标 popover（来源+**提炼过程**+**查看原文抽屉**+素材回链 tag）、思路转写段标记、图表卡三样式切换持久化、段落 inline 编辑、**AI 改写对照稿确认**、保存版本、提交审核、导出；阶段经 URL query（step/task）持久化，刷新不丢 |
| `MyReportTaskHome.vue`（F-WR-06） | 91-93,102 | 列表进度列（writing 实时推进）+ 工作台 + 发布四步流；**审核驳回**（意见回显到编辑器）；Word/PDF 导出接真实 exporter；恢复演示数据入口 |
| `WritingMaterialsHome.vue`（F-WR-07） | 108-110 | 上传（自定义文件名/类型 🧪）→ 解析 → 摘要；**报告引用回链列**（citation.materialId 反查，点击直达对应报告编辑器）；被引用素材删除防呆 |
| `StrategyAchievementHome.vue` / `CasePlazaHome.vue` | 54 | **发布闭环**：审核通过的报告自动进入两页「已发布报告」区，可回跳编辑器 |
| `templates.ts` | 94-97 | 新增 `updateTemplate`（重命名 + 章节编辑），配套模板编辑抽屉 |

## 2. AC 自走查（对照 USM-ZHIKU-WRITING 验收标准，抽核心项）

| AC | 结果 |
|---|---|
| WR-01 三态入口各自可发起，任务配置校验（标题/模板必填拦截） | ✅ |
| WR-02 大纲可增删改排序、空标题拦截、常用章节一键加入、分析思路逐章录入 | ✅ |
| WR-03 确认后后台写作可离开页面，进度刷新可恢复（persist + resumeWritingTimers） | ✅ |
| WR-04 NL 输入不足时拦截并给示例；意图卡展示主题/类型/时间范围+追问；确认后生成任务+大纲 | ✅ |
| WR-05 正文脚注 ≥3、编号连续；弹层含来源/提炼过程/原文；无原文时置灰说明 | ✅（generator 保底逻辑） |
| WR-05 图表卡带 Mock 标 + 来源脚注；样式切换后持久化（刷新/导出一致） | ✅ |
| WR-06 AI 改写走「要求→对照稿→采用/放弃」，采用自动记版本 | ✅ |
| WR-06 版本历史时间线展示；手动保存版本可用 | ✅ |
| WR-07 素材引用与系统来源同格式（同 popover/同列表），带素材 id 回链 | ✅ |
| WR-08 提交→审核（通过/驳回）→发布；驳回意见回任务与编辑器；发布进成果区 | ✅ |
| 导出：Word 得到可打开的 .doc 文件；PDF 经打印视图另存；未生成正文时拦截 | ✅ |
| D9：统计卡走 MetricCard（ⓘ + metric_id + 🧪），页面不手写口径 | ✅（沿用 ZHIKU-S1-* 已注册指标） |

## 3. 偏离说明

1. **导出 PDF 用浏览器打印视图**而非内置 PDF 库：仓库无 jsPDF 依赖且公约禁止随意改 `package.json`；demo 闭环可拿到真实 PDF（另存为 PDF），正式态由服务端导出替换。
2. **NL 解析 / 内容生成 / 审核流转均为规则式演示（🧪）**：UI 已按诚实性约束标注「演示 🧪」，正式态分别对接 Python `/internal/*` NLU、生成服务与审批后端。
3. 指标沿用已注册的 `ZHIKU-S1-*` metric_id（口径不变），未新增指标；待 R6 收口批次统一评估是否更名 R 批次。

## 4. 产物清单

- 代码：demo-ui-gaoduanzhiku-view `dev@988bfcb`（push 成功，CI 由 GitLab Pipeline 触发）
- 五件套：见 §1.1（前置提交于编排仓）
- 本 handoff：`agent-delivery/agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R1.md`

## 5. 验收证据

- `npm run type-check`（vue-tsc --build）：**通过，0 错误**
- `npm run build`（type-check + vite build）：**通过**（3320 modules，25.9s；chunk 体积告警为存量问题）
- push：`764726f..988bfcb dev -> dev`（gitlab.htmisoft.net/gkx-lumen/demo-ui-gaoduanzhiku-view）
- 走查路径（本地/dev 环境）：
  1. 报告创作 → NL 输入示例 → 解析 → 确认发起 → 大纲（加思路）→ 确认 → 进度 → 编辑器脚注/图表/改写
  2. 我的报告任务 → 提交审核 → 驳回（看意见回显）→ 再提交 → 通过 → 战略咨询成果「已发布报告」
  3. 素材库 → 上传 → 创作时关联 → 生成后查看引用回链

## 6. 架构合规自检（公约 §2 十条)

| # | 条款 | 结果 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 前端纯 mock 演示，无算法实现（规则式转写均标 🧪） |
| 2 | 调用链不越层 | ✅ 无后端调用（demo mock 阶段） |
| 3 | 图谱 NebulaGraph | N/A 本模块无图谱 |
| 4 | 可观测性 | ✅ 沿用仓内 `observability.ts` 全局接入，未破坏 |
| 5 | CI/CD push→Pipeline | ✅ 已 push dev 触发 |
| 6 | demo2 只读 merge | ✅ 未涉及 |
| 7 | 共享聚合核心 | N/A demo 阶段无 Java 依赖 |
| 8 | 标准表先行 Mock 填充 | ✅ 全 mock，源表口径在 metricSeed 注册 |
| 9 | 前端规范 D8 | ✅ Arco Design Vue + ECharts + design tokens（本仓 Vue 技术线沿用既定基线） |
| 10 | 数据血缘 D9 | ✅ 统计数字走 MetricCard（ⓘ/🧪），图表卡带来源注记 |

## 7. cost 回填

- `actual_tokens`：≈ 1,900,000（本会话累计，含五件套撰写）
- `model_used`：claude-fable-5
- `actual_cost`：≈ $8.5（估算）
- `cost_warn`：false（< $10）

## 8. 下一步（待用户打样确认）

R1 为**打样批次**：请用户按 §5 走查路径确认交互深度与视觉是否达标；确认后按同一标准执行 R2（ZHIKU-BASIC-RESEARCH）→ R6 收口。
