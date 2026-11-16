# ZMATE-RPT · 合规演示用例

> **模块**：ZMATE 战略报告创作（Demo 纯前端样机）  
> **对照**：`USM-ZMATE-战略报告创作.md` 验收句 ZMATE-USM-01…13  
> **实现**：`repos/demo-ui-topic` @ `3c088cf` · 路由 `/zmate-strategy-demo`  
> **阶段**：无 Java/Python 真链；接口列写 `N/A（localStorage Mock）`；§6.5 后端 LOOP **本阶段 N/A**（见 E-QA 简报）  
> **作者**：`agent:qa-agent` · 监管人 `human:淮政玮` · 2026-11-16

本页回答「当前 Demo 数据下怎么演」。循环不另编预期。`可演` 以手工/脚本走查为准。

## 覆盖表

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| ZMATE-USM-01 创作壳发起 | `/zmate-strategy-demo` | Query=`集团固态电池业务东南亚扩张战略（2027–2029）`；报告类型=`战略咨询报告`；文件夹=`低空经济战略研究` | 点「创建报告任务」 | N/A（localStorage `zmate-strategy-workspace-v2`） | `createRun({title, reportType, folderName, skillsUsed})` → `runId=run-*` | 左侧项目轨可见；菜单「战略报告 Demo」保留；进入 `/zmate-strategy-demo/run/:runId` Hub；仅澄清 `ready`，其后站 `locked` | 可演 |
| ZMATE-USM-02 安装≠本次使用 | 创作壳「已安装 Skill」标签 vs「本次使用」勾选 | 已安装含战略/辩论/写作等；本次使用默认勾 `sk-strategy`/`sk-debate`/`sk-write`；取消「产业链扫描」勾选 | 创建任务 | N/A | `skillsUsed` 仅含勾选 skillId，不含未勾选 | 安装态芯片与「本次使用」文案分离；run 上 `skillsUsed` 与勾选一致；取消项不进入 `skillsUsed`（Demo 无后续 Skill 调用时间线，静默调用以该字段核对） | 可演（局限：无时间线条） |
| ZMATE-USM-03 人闸澄清禁 autoRun | `/run/:runId/clarify` + 右侧报告区 | 未点「确认需求」 | 进入澄清 / 观察右侧 | N/A | stages.clarify=`ready`；无 brief.confirmedAt | 右侧固定「等待需求确认」；无正文；Hub **无**「一键跑完」；Planner…Judge 锁定 | 可演 |
| ZMATE-USM-04 研判卡 + slice_id | 澄清末步候选研判卡 | 选 `slice-ssb-sea-2026`（或另一候选卡）并完成澄清卡必填项 | 「确认需求」 | N/A | `brief.boundSliceId=slice-ssb-sea-2026`；clarify→done；planner→ready | 至少一张研判卡；界面暴露 `slice_id=…`；Planner 解锁 | 可演 |
| ZMATE-USM-05 Hub 阶段序与人闸 | Hub `/run/:runId` | 按序：澄清确认 → Planner 完成 → 辩论∥切片 ready | 各站「进入本站」；锁定站不可点 | N/A | 解锁合同：clarify→planner；planner→debate+slice；slice→seeker；seeker+辩论结束/跳过→writer；writer→judge | Hub 展示澄清→Planner→辩论∥切片→Seeker→Writer→Judge；锁定钮 disabled + Tooltip 解锁条件；无静默全链 | 可演 |
| ZMATE-USM-06 辩论卷宗人控 | `/run/:runId/debate` | Planner 完成后进辩论；「新一轮」→「结束辩论」 | 新一轮 / 引导轮 / 结束辩论 | N/A | dossier.claims 三层（title/reasoning/sources）；`locked=true` | 人控轮次；结束后只读；站顶文案「无战略胜负裁判」；对象名=辩论知识卷宗 | 可演 |
| ZMATE-USM-07 术语不混用 | 辩论站顶 banner + 切片站顶 banner；评审术语卡 | 对照两站文案 | 目视 | N/A | — | 「辩论知识卷宗」≠「专题切片/研判卡」；禁止用「卷宗」指切片 | 可演 |
| ZMATE-USM-08 指标四态诚实 | `/run/:runId/slice` 指标表 | DEMO_SLICE 四条需求 | 打开切片站 | N/A | 四态文案：可用/待建/待真接/待外网补数；无「live 已对齐」 | 四态可见；缺口进 known_gaps；无假绿 live | 可演 |
| ZMATE-USM-09 装配与溯源 | Writer → 报告宿主 | 辩论结束或 Hub「标记跳过辩论」+ Seeker 完成 | 「装配结构草稿」 | N/A | report.generating 时 paragraphs=[]；完成后有 citationLabels | 生成中右侧骨架、**不出未完成正文**；完成后组件大纲 + 溯源角标（推断/metric/缺口） | 可演 |
| ZMATE-USM-10 Judge Default-FAIL | `/run/:runId/judge` | Demo 默认含待真接/待建/待外网补数 | 「跑合规检查（Default-FAIL）」或「尝试 PASS」 | N/A | findings 含缺口/人闸类；有违规时 prefer PASS 仍 FAIL | 结果 `compliance_fail`；文案「≠ 战略胜负裁判」；known_gaps 回写；职责≠辩论裁判 | 可演 |
| ZMATE-USM-11 项目轨恢复 | 创作壳左侧「本机已存 run」/ 新建任务轨条目 | 用新建任务的 `runId` 点「恢复」 | 点击恢复 | N/A | `getRun(runId)` 恢复 stages/brief | 回到正确阶段，不跳过人闸 | 可演（见红项：fixture 示例任务） |
| ZMATE-USM-12 内部评审模式 | 右上角用户/角色「内部评审模式」 | 开→关 | 切换开关 | N/A | `ZmateReviewMount` reviewMode 自闸 | 开：页特有挂载（条款/术语/四态/Judge）；关：无 metric_id/GAP/条款字样泄漏；业务 Query/任务保留 | 可演 |
| ZMATE-USM-13 Demo 边界声明 | 创作壳副标题 + FE handoff + 本用例头 | — | 读文档 | N/A | — | 声明 `demo-ui-topic` 纯前端；不挡 V1 真后端；非目标清单可读 | 可演 |

### 人闸 / Judge FAIL 专项行（主路径异常）

| 需规位置 | 界面 | 输入或选择 | 触发 | 接口地址 | 按界面值填好的请求 | 期望输出 | 数据情况 |
|---|---|---|---|---|---|---|---|
| 人闸·未确认出报告 | 右侧报告宿主 | clarify 未 done | 任意后续站尝试 | N/A | stages.planner…=`locked` | 右侧仍「等待需求确认」；无 autoRun | 可演 |
| 人闸·Writer 未满足条件 | Writer | 辩论未结束且未跳过，或 Seeker 未完成 | 「装配结构草稿」 | N/A | writer=`locked` | 准入条列出未满足项；按钮 disabled / Message 警告 | 可演 |
| Judge·缺 id / 假 live / 绕过人闸 | Judge | Demo 缺口 demands；或 report 空；或辩论未锁且未跳过 | 跑合规检查 | N/A | `collectFindings()` 非空 → verdict=FAIL | Default-FAIL；带回 findings / known_gaps | 可演 |
| Judge·≠胜负裁判 | Judge / 辩论 banner | — | 目视 | N/A | — | 无「胜负/采信方」战略裁判文案 | 可演 |

## 一条主路径（V1 最短 · 可跳过辩论）

固定输入：Query / 报告类型 / 文件夹同上表 USM-01；本次使用勾 `sk-strategy`、`sk-debate`、`sk-write`。

1. 打开 `/zmate-strategy-demo`。核对项目轨、Query、报告类型、专家入口、安装 Skill ≠ 本次使用。  
2. 「创建报告任务」→ Hub。确认仅澄清可进；右侧「等待需求确认」。  
3. 澄清站走完 7 步，绑定 `slice-ssb-sea-2026`，「确认需求」→ Planner 解锁。  
4. Planner 完成（确认组件/任务树摘要）→ 辩论与切片并行 ready。  
5. Hub「标记跳过辩论 · 记缺口」（或完整走辩论后结束）。  
6. 切片站批准至少一项可用指标 → Seeker 解锁；Seeker 取数摘要写入证据包。  
7. Writer「装配结构草稿」：生成中右侧无正文 → 结构草稿 + 溯源角标 → Judge 解锁。  
8. Judge「跑合规检查（Default-FAIL）」：因 Demo 含非 ready 指标 → **FAIL** + known_gaps；文案标明 ≠ 战略裁判。带着缺口仍可开终稿只读入口（产品约定）。  
9. 回创作壳，点「本机已存 run」恢复，确认停在已完成阶段、不跳过人闸。  
10. 开/关内部评审模式：开见页特有挂载；关零泄漏。

## 走查证据（本轮）

| 证据 | 结果 |
|---|---|
| `pnpm build`（demo-ui-topic @ 3c088cf） | 绿 · vite build ~36s |
| 浏览器 preview `http://127.0.0.1:4173/zmate-strategy-demo` | 创作壳可见；创建任务进 Hub；澄清人闸文案可见；后续站锁定 |
| `sdd/简报/qa-gate-check.mjs` | OK · 解锁合同 + Judge Default-FAIL |

## 红项 / 黄项

| ID | 级别 | 说明 |
|---|---|---|
| R-ZMATE-QA-01 | 黄 | 项目轨 fixture `task-demo-*` 点入可能 fallback 到 `runs[0]`/`ensureDemoRun`，不保证示例任务自身阶段；**新建任务 runId** 恢复路径绿（FE handoff 已记） |
| R-ZMATE-QA-02 | 黄 | USM-02「取消后不得静默调用」无 Skill 调用时间线 UI，仅 `skillsUsed` 可核对 |
| R-ZMATE-QA-03 | 信息 | §6.5 后端 LOOP（token/库/接口）对本 Demo **N/A**；验收以本表手工/脚本为准 |
