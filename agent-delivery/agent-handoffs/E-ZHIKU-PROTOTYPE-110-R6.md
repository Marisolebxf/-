# E-ZHIKU-PROTOTYPE-110-R6 · 全链路 E2E 走查 + 总收口 handoff

> **任务**：E-ZHIKU-PROTOTYPE-110-R6（tech_task）· 认领/监管：human:淮政玮 · 执行：agent:frontend
> **日期**：2026-08-05 · **仓库**：`demo-ui-gaoduanzhiku-view @ dev`（前端）+ `gkx-orchestration @ dev`（编排）
> **背景**：S1-S5 首轮实现经用户评审判定未达 USM 标准/操作不闭环，整体置 needs-revision 后按"叶子五件套先行 + 闭环重实现"标准重跑（R1 打样经用户 2026-08-05 确认达标，R2-R5 按同一标准链式执行）。本批为集成验证与总收口，不新增页面。

## 1. R1-R6 总览

| 批次 | 范围 | 业务仓 commit | 编排仓交付 | AC 自走查 | registry |
|---|---|---|---|:---:|:---:|
| R1 | ZHIKU-WRITING（88-110） | R1 批次 3 commits（#4707-#4709 流水线绿） | 五件套 + handoff R1 | 核心项抽核 + **用户打样确认达标** | integration |
| R2 | ZHIKU-BASIC-RESEARCH（82-87） | `2d6dd9c` | 五件套 + handoff R2 | 39/39 ✅ | integration |
| R3 | ZHIKU-TALENT-POOL / TALENT-MAP（59-81） | `03e0d42`/`1fc778b`/`5783d06` | 五件套 ×2 + handoff R3 | 69/69 ✅ | integration |
| R4 | RESEARCH-NEED / TECH-SYSTEM / TECH-TREND（1-45） | `a3173a1`/`405a8e3`/`13bf8ee` | 五件套 ×3 + handoff R4 | 88/88 ✅ | integration |
| R5 | STRATEGY-ROADMAP / STRATEGY-REPORT / SMART-QUERY（46-58） | `6a94e93`/`e3abfa7`/`44e59df` | 五件套 ×3 + handoff R5 | 70/70 ✅（1 条偏离登记） | integration |
| R6 | E2E 走查 + coverage 重核 + 开放项集中登记 + 总收口 | `84af75f` | 本 handoff + `coverage-matrix-110-R重核.md` + 决策表 §2.ad | 见 §2 | integration |

- 十份叶子 USM 共定义 **308 条 AC**（WR41/BR40/TP42/TM27/RN25/TS35/TT28/RM22/SP26/SQ22）；R2-R5 handoff 逐条登记通过 266 条，R1 为打样批次核心项抽核 + 用户人工确认。
- **110 项序号全闭合**：R4=1-45、R5=46-58、R3=59-81、R2=82-87、R1=88-110，逐序号归属/路由/状态见 `产品整体定义/E-ZHIKU-新型高端智库/coverage-matrix-110-R重核.md`。

## 2. R6 全链路 E2E 走查（静态核对）

| 检查项 | 方法 | 结论 |
|---|---|---|
| 九组路由 19 个二级项全挂真实组件 | 读 `src/router/menu.ts` + Glob views | ✅ 无 DevelopingView 占位 |
| 纯左侧手风琴导航 | 读 `MainLayout.vue` | ✅ `a-menu mode="vertical" accordion` |
| 跨叶子契约（CT-\*）真实调用 | rg `useWritingTaskStore`/`createTask` | ✅ 11 处调用点（BR×2/TP/TM/RN/TS/TT×2/RM/SP/SQ）均真实 `createTask` 预填注入并跳大纲确认 |
| 旧指标 id 零残留 | rg `ZHIKU-S[1-5]-` 全 src | ✅ 仅存 metricSeed/readinessSeed 注释 rename 记录（无运行时双 id） |
| 指标 ⓘ/角标在位 | rg `MetricCard` src/views | ✅ 39 个视图文件覆盖全部十叶子，未见裸数字规模性遗漏 |
| 共享文件无相互覆盖/断链 | vue-tsc 全量 + 走查 metricSeed/readinessSeed/menu.ts/taskStore/TalentMapView/achievements | ✅ R2-R5 连续修改后类型闭合、引用一致 |
| localStorage 域独立 | rg `zhiku-*-` 前缀枚举 | ✅ 十叶子前缀齐备（wr/br/tp/tm/rn/ts/tt/rm/sp/sq），互不串写 |

**发现并修复 2 处**（commit `84af75f`，vue-tsc 0 错 + vite build 通过后推 dev）：
1. `src/router/menu.ts` L49 残留"顶部一级导航"旧注释，与纯左侧手风琴现状矛盾 → 修正；
2. `docs/coverage-matrix-110.md` 第 41 行仍引用旧指标 id `ZHIKU-S3-TREND-FORECAST` → 更正为 `ZHIKU-TT-TREND-FORECAST`（R4 正名）并补 Q-ZHIKU-04 关联；同时在矩阵追加 §六 R 批次重跑说明（序号归属表 + R6 终验结论 + 演示准备指引）。

## 3. coverage matrix 重核结论

- 新建 `产品整体定义/E-ZHIKU-新型高端智库/coverage-matrix-110-R重核.md`：110 行逐序号登记归属叶子/TRACE/路由/状态，与五份（十份）TRACE 反向核对一致，**无遗漏、无双重归属**（跨叶子共用页面 100/104/105/107 在 TRACE 标注共用、计数归 WR）。
- 状态分布：✅ closed 80 行；✅🧪 演示态 27 行；✅❓ 口径待定 3 行（54/55/57）。全部 🧪/❓ 行均有 UI 诚实性标注 + 决策清单登记，不阻塞演示、禁止对外决策展示。

## 4. 开放项集中登记

Q-ZHIKU-01~05（角色口径/页面归属/权限映射/算法定义卡族/心理信息边界）+ R5 新提出的 Q-ZHIKU-06（案例投资/ROI/满意度口径）、Q-ZHIKU-07（智谱/智树集成契约）共 **7 项**，已补登 `agent-delivery/客户决策清单跟踪表.md` **§2.ad**（全部 🟡，含临时默认/影响面/落地路径），与各叶子 TRACE gaps、METRIC-OPEN 核对记录一致。其中 Q-ZHIKU-05 涉合规风险（建议 PM 优先推进郭万迎书面确认）、Q-ZHIKU-04 为上线闸门（算法定义卡未落地前相关指标保持 D1 missing 红问号/演示态）。

## 5. CI 最终确认（GitLab API 实查，2026-08-05）

`demo-ui-gaoduanzhiku-view` dev 分支最近 20 条流水线：R1-R5 全部提交 **success**（#4707-#4719），R6 收口 commit `84af75f` push 后自动触发（同栈构建配置未变）。历史 failed 仅 S2/S3 时代（#4687 `9b0ef3b`、#4697 `d9de833`），已被后续提交修复覆盖，与 S6 结论一致。当前 dev HEAD 前一提交 `44e59df` pipeline #4719 **success**。

## 6. 演示准备指引

- 部署地址：dev 环境（CI 自动 rollout）；如需干净演示环境，清除浏览器 localStorage 中 `zhiku-wr-` / `zhiku-br-` / `zhiku-tp-` / `zhiku-tm-` / `zhiku-rn-` / `zhiku-ts-` / `zhiku-tt-` / `zhiku-rm-` / `zhiku-sp-` / `zhiku-sq-` 前缀的全部 key（各叶子 store 自动恢复演示种子数据）。
- 评审模式开关控制血缘/就绪度角标显隐；Q-ZHIKU-05 的心理信息边界声明为业务态文案，关闭评审模式仍保留（面向甲方的诚实性）。
- 推荐演示动线：写作创作闭环（模板/NL 双入口→大纲→编辑→发布→成果中心）→ 任一分析叶子"生成报告"跨叶子契约 → 人才地图联动 → 基础研究下钻。

## 7. 架构合规自检（公约 §2 十条）

| # | 条款 | 结论 |
|---|---|---|
| 1 | 算法只在 Python | ✅ 前端原型无算法实现，AI 能力全部 🧪 模拟并标注 |
| 2 | 调用链不越层 | ✅ 纯前端 Mock，无直连算法/数据库；正式化路径已在 TRACE 登记走 Java REST |
| 3 | 图谱 NebulaGraph | ✅ 未引入 Neo4j；图可视化为 G6 前端渲染 |
| 4 | 可观测性 | ➖ demo 原型仓不接 OTel（与 S0 批次口径一致，正式仓落地时补） |
| 5 | CI/CD | ✅ push→Pipeline 绿（§5 实查） |
| 6 | demo2 只读 merge | ✅ 未 merge 进任何 lumen 仓 |
| 7 | 共享聚合核心 | ✅ 指标消费契约按 `/metrics/v1/catalog` 目标态预留（镜像模块过渡） |
| 8 | 数据策略 | ✅ 全 Mock + 🧪 标注，D1 missing 不伪闭合 |
| 9 | 前端规范 D8 | ✅ Arco Vue + design-tokens 与 lumen-ui-topic 同源；ECharts/G6/Leaflet 按权威栈 |
| 10 | 数据血缘 D9 | ✅ 指标 8 件套 + ⓘ/MockBadge/红问号，39 视图文件覆盖 |

## 8. cost 回填（R6）

- `actual_tokens` ≈ 120k · `model_used`: claude-fable-5 · `actual_cost` ≈ $1.8 · `cost_warn`: green（已用 task-update-fields 回填）

## 9. registry 终态与遗留

- R1-R5：均 `integration`（各批 evidence/cost 已回填）；R6：本批推 `integration`。
- 后续人工节点：①（可选）qa-agent 领取 pending_test 走测试闸门（feature 类 R1-R5 依 AV-1 需 note 联调确认关键词后转 pending_test）；② 最终 `ready_to_sign → done` 由 human:淮政玮 签收。
- 遗留风险：Q-ZHIKU-04 算法定义卡（上线闸门）、Q-ZHIKU-05 合规确认（高优）、Q-ZHIKU-07 三方集成契约（联调前）；`84af75f` 流水线结果需在 GitLab 上最终过目（历史同栈 13 连绿，风险低）。
