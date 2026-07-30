# ENT V2 Lumen 子任务派单包

- 日期：2026-07-29
- 派单人：human:孔东（前端 Lead）
- 设计规格：`docs/superpowers/specs/2026-07-29-ent-v2-lumen-eval-risk-recruit-design.md`
- 父任务：ENT-MOD-RISK-V2-LUMEN、ENT-MOD-EVAL-V2-LUMEN、ENT-MOD-RECRUIT-V2-LUMEN
- 分工：孔东 75%（3 包）、曹丽影 25%（1 包）

## 子任务总表

| 序号 | 子任务 ID | 工作包 | 执行人 | 监管人 | 父任务 | 依赖 | effort | difficulty |
|------|-----------|--------|--------|--------|--------|------|--------|------------|
| 1 | ENT-MOD-SHARED-V2-LUMEN-S1 | 共享底座 + 三模块 API/Mock/类型/composable 全量（路由+对比篮上下文+dispatch 对齐+mock/register+评估/风险/引育 API 封装+类型+composable） | 孔东 | 孔东 | RISK+EVAL+RECRUIT | [] | 8 | XL |
| 2 | ENT-MOD-RISK-V2-LUMEN-S2 | 风险洞察全量（供应链图谱+痛难点+四态/历史/画像联动） | 孔东 | 孔东 | RISK | [S1] | 8 | L |
| 3 | ENT-MOD-EVAL-V2-LUMEN-S3 | 企业评估全量（配置页+过程/结果/历史页） | 孔东 | 孔东 | EVAL | [S1] | 8 | L |
| 4 | ENT-MOD-RECRUIT-V2-LUMEN-S4 | 引育推荐全量（页面组装+工作台+候选工作台+详情 Drawer） | 曹丽影 | 曹丽影 | RECRUIT | [S1] | 5 | L |

> 验收直接使用三个主任务（ENT-MOD-RISK-V2-LUMEN / ENT-MOD-EVAL-V2-LUMEN / ENT-MOD-RECRUIT-V2-LUMEN）的 DoD，不单设集成验收子任务。

## 串并行时序

```
S1（孔东，共享底座+全量 API/Mock/composable）
 │
 ├─→ S2（孔东，风险洞察全量）      ─→ 主任务验收
 ├─→ S3（孔东，企业评估全量）      ─→ 主任务验收
 └─→ S4（曹丽影，引育推荐全量）    ─→ 主任务验收
```

- S1 串行（孔东），完成后三支并行
- S2、S3 由孔东并行或串行（视本机会话调度）
- S4 由曹丽影独立执行，消费 S1 提供的 `useRecruit.ts`
- 各子任务完工后提交对应主任务 handoff + 会签单

---

## 孔东派单话术

### S1：共享底座 + 三模块 API/Mock/类型/composable

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Vite + Arco Design Vue + TypeScript + Vue Router + Pinia；组件化复用、只经网关调 Java、沿用 observability.ts 注入 traceId，不直连 Python/DB。
任务 ID：ENT-MOD-SHARED-V2-LUMEN-S1
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：dev（直推 origin/dev）
设计规格：${GKX_ROOT}/gkx-orchestration/docs/superpowers/specs/2026-07-29-ent-v2-lumen-eval-risk-recruit-design.md
必读：
  - agent-delivery/Design.md（D8 权威栈；token 不硬编码；主色 #165DFF；§14 14 条必查）
  - agent-delivery/architecture-baseline.md（方案 A、D8/D9）
  - agent-delivery/data-lineage-policy.md（D9 血缘 8 件套）
  - repos/lumen-ui-topic/ARCHITECTURE.md（仓内架构铁律）
  - repos/lumen-ui-topic/src/utils/http.ts（defineApi + registerApiMock 模式）
  - repos/lumen-ui-topic/src/mock/register.ts（mock 注册中心）
  - repos/lumen-ui-topic/src/config/compareBasketDispatch.ts（对比篮分发契约真源）
  - repos/lumen-ui-topic/src/router/menu.ts（菜单真源）
  - agent-handoffs/企业战略分析-ENT/API-ENT-full-catalog.md（#102~109、#113~121 接口真源）

范围（共享文件 + 三模块 API/Mock/类型/composable，不写页面组件）：

  A. 共享底座
  1. src/router/menu.ts：注册三个路由（enterprise/evaluation、enterprise/risk、enterprise/attraction），可先 showInMenu:false 仅打通对比篮分发
  2. src/composables/useCompareBasketDispatchContext.ts（新建）：解析 route.query（enterprise_org_ids[]、return_context_id、source、analysis_type）+ 返回对比篮逻辑
  3. src/mock/enterprise/searchBizApi.ts：对齐 DISPATCH_ROUTE 到 /enterprise/evaluation|risk|attraction
  4. src/config/enterpriseBreadcrumb.ts：增 eval/risk/attraction 来源
  5. src/mock/register.ts：合并注册三模块 mock 入口

  B. 企业评估 API/Mock/类型（#102~109、#113~121）
  6. src/api/enterprise/evaluation.ts（新建）：#102 创建任务、#103 列表、#104 详情、#105 结果指针、#107 取消、#108 运行中、#109 SSE
  7. src/api/enterprise/evaluation.ts 扩展：#113 行业、#114 指标树、#115 预检、#116 双企对比、#117~121 模板 CRUD
  8. src/api/enterprise/types/evaluation.ts（新建）：AnalysisTaskEntity、TemplateItem、EvalIndicatorsResponse、EvalPrecheckResponse 等
  9. src/mock/enterprise/evaluation.ts：按 catalog 字段 mock；#106 不 mock 数据，仅下载动态模拟

  C. 风险洞察 API/Mock
  10. src/api/enterprise/riskInsight.ts（新建或扩展）：风险洞察 API 封装（复用已有 risk.ts，按需扩展）
  11. src/mock/enterprise/riskInsight.ts：供应链 + 痛难点 mock（按 demo fixture 结构，不发明业务口径）

  D. 引育推荐 API/Mock/类型/composable
  12. src/api/enterprise/recommend.ts（扩展现有）：招引推荐、培育推荐、候选名单
  13. src/api/enterprise/types/recruit.ts（新建）：RecruitBaseRecommendation、AttractionExtension、CultivationExtension
  14. src/composables/useRecruit.ts（新建）：引育推荐状态机 composable，供曹丽影页面消费
      - 招引/培育切换、筛选/候选工作台切换
      - analysisState：initial/loading/success/empty/partial/error/permission
      - 三维权重校验（Σ=100%）
  15. src/mock/enterprise/recruitWorkbench.ts：引育 mock（按 demo fixture 结构，不发明业务口径）

Mock 铁律（评估接口）：
  - 同一 taskId 在 #102/103/104/105/109 间字段自洽
  - 状态仅 running/success/failed/cancelled（无 pending）
  - #113 is_preview、#115 data_source=mock 原样保留
  - 模板接口 snake_case；任务接口 camelCase
  - 不发明 dimension_diff/dimensions/enterprises[] 内部评分字段
  - 不发明预检阈值
  - #106 不 mock 数据；Mock 模式仅展示下载动态模拟（进度态→完成态）

DoD：
  - 三路由可访问（即使页面为占位）；对比篮分发不再提示「承接页待接入」
  - useCompareBasketDispatchContext 可解析 query 并提供返回对比篮方法
  - 所有 API 声明使用 defineApi({ id, real, mockDelay? }) 模式
  - 类型定义与 catalog 字段一致，不发明未定义字段
  - useRecruit.ts 提供稳定 ViewModel 接口，曹丽影只需消费
  - npm run build + type-check 通过
  - 不改 package.json / vite.config / tsconfig
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-SHARED-V2-LUMEN-S1.md
```

### S2：风险洞察全量

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Arco Design Vue + unocss + ECharts 力导向图 + TypeScript；组件化复用、只经网关调 Java。
任务 ID：ENT-MOD-RISK-V2-LUMEN-S2
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：dev
原型：页面布局、功能、交互、样式 复刻demo-ui-topic风险洞察页面
相关API及MOCK数据已经在任务ENT-MOD-SHARED-V2-LUMEN-S1完成；
硬约束：结果走 #105 → #106；演示数据进 fixtures + MockBadge，禁止再发明 riskInsight/* 结果 API
DoD：
  - 供应链图谱可渲染、节点可展开、关键/风险节点侧栏可筛选
  - 痛难点 Tab 可切换，四维诊断卡片可筛选，受影响企业 Drawer 可展开
  - 四视图闭环可演示；历史可恢复
  - 所有异常态有 UI 覆盖
  - 画像 risk tab 可访问
  - 对比篮 → /enterprise/risk?analysis_type=supply-chain|pain-points 可带入企业集合
  - 评审模式：评审模式相关内容要根据demo-ui-topic 中相关内容，根据当前项目的架构进行复刻
handoff 说明
  - npm run build + type-check 通过
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-RISK-V2-LUMEN-S2.md
```

### S3：企业评估全量

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Arco Design Vue + ECharts + TypeScript；组件化复用、只经网关调 Java。
任务 ID：ENT-MOD-EVAL-V2-LUMEN-S3
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：dev
原型：页面布局、功能、交互、样式 复刻demo-ui-topic企业评估页面
相关API及MOCK数据已经在任务ENT-MOD-SHARED-V2-LUMEN-S1完成；

DoD：
  - 三模式（technology/business/competitiveness）配置页可演示
  - 对比篮 → /enterprise/evaluation 可带入企业集合
  - 预检结果展示 ready/missing_codes/overall_confidence
  - 过程页六阶段进度可演示（Mock SSE）
  - 结果页排名/雷达/对比可渲染
  - #106 下载：Mock 模式展示进度态→完成态，不构造结果 JSON
  - 历史页可恢复任务
  - 评审模式：评审模式相关内容要根据demo-ui-topic 中相关内容，根据当前项目的架构进行复刻，MetricSpecCard + MockBadge 接入
  - **组件拆分自检**：demo 原型 `EnterpriseEvaluationPage.tsx` 1050 行 + `EnterpriseEvaluationResultWorkspace.tsx` 425 行为参照，lumen 落地须按职责拆为页面壳 + 配置面板 + 过程步骤 + 结果工作台 + 历史表 + composable；
  - npm run build + type-check 通过
  - 不改 register.ts / compareBasketDispatch.ts / API/Mock 层（已在 S1 完成）
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-EVAL-V2-LUMEN-S3.md
```

---

## 曹丽影派单话术

### S4：引育推荐全量

```markdown
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Arco Design Vue + TypeScript；组件化复用、只经网关调 Java。
任务 ID：ENT-MOD-RECRUIT-V2-LUMEN-S4
仓库：${GKX_ROOT}/repos/lumen-ui-topic
分支：dev
设计规格：${GKX_ROOT}/gkx-orchestration/docs/superpowers/specs/2026-07-29-ent-v2-lumen-eval-risk-recruit-design.md

原型：页面布局、功能、交互、样式 复刻 demo-ui-topic 引育推荐页面
相关API及MOCK数据已经在任务ENT-MOD-SHARED-V2-LUMEN-S1完成；

范围（仅改 src/views/enterprise/EnterpriseRecruit.vue + src/components/enterprise/recruit/**，不改 API/Mock/路由/注册）：

  1. EnterpriseRecruit.vue：路由壳 + 双层 Tab
     - 一级 Tab：招引推荐 / 培育推荐
     - 二级 Tab：条件筛选推荐 / 候选工作台
  2. RecruitWorkbench.vue：条件筛选推荐工作台
     - 筛选条件区：招引（企业标签/行业领域/地域来源）；培育（产业类别/政策导向/企业规模）
     - 三维权重滑块（合计 100% 校验）
     - 结果区：企业排名 Table + 区域分布视图（resultView=ranking/distribution 切换）
  3. CandidatePanel.vue：候选工作台
     - 候选企业 Table（指定对象复核，≤50 家）
     - 批量加入对比篮
  4. RecruitDetailDrawer.vue：企业详情 Drawer
     - 招引：三类综合维度、高潜挖掘依据、核心优势、关键指标、合作价值
     - 培育：三类综合维度、本地潜力识别依据、所需支持
     - 风险信用（state/recordCount/categories/records）
     - 政策方向
  5. 消费 useRecruit.ts（S1 孔东提供），不直接调 API/Mock
  6. 评审模式：评审模式相关内容要根据demo-ui-topic 中相关内容，根据当前项目的架构进行复刻
  7. 状态覆盖：initial/loading/success/empty/partial/error/permission

约束：
  - 不改 src/mock/register.ts、src/config/compareBasketDispatch.ts
  - 不改 src/composables/useRecruit.ts、src/api/enterprise/recommend.ts、src/api/enterprise/types/recruit.ts（S1 孔东提供）
  - 不改 package.json / vite.config / tsconfig
  - 只消费 useRecruit.ts 提供的 ViewModel，不自行封装 API

DoD：
  - 招引/培育双视图可切换
  - 筛选推荐工作台可演示；排名 Table + 区域分布可渲染
  - 权重校验 Σ=100%
  - 候选工作台可展示、可批量加入对比篮
  - 详情 Drawer 招引/培育字段完整
  - 评审模式血缘接入
  - 所有异常态有 UI 覆盖
  - **组件拆分自检**：demo 原型 `EnterpriseRecommendation.tsx` 1651 行为参照（典型上帝文件），lumen 落地须按职责拆为页面壳 + 工作台 + 候选面板 + 详情 Drawer + 各子展示块；业务逻辑全部走 `useRecruit.ts`；
  - npm run build + type-check 通过
Handoff：agent-handoffs/企业战略分析-ENT/ENT-MOD-RECRUIT-V2-LUMEN-S4.md
```

---

## 注意事项

1. 所有 commit message 必含 `[agent:frontend-agent]` 或 `[human:孔东]` / `[human:曹丽影]`
2. lumen-ui-topic 默认 push `origin/dev`，禁止 push `main`
3. 禁止改 `package.json` / `vite.config.ts` / `tsconfig.json`
4. 框架真源 = lumen-ui-topic（Vue + Arco Design Vue），demo-ui-topic 仅参考
5. 评审模式和 Mock 双轨必须保留
6. #106 不 mock 数据，Mock 模式仅展示下载动态模拟
7. 每个子任务完工后写 handoff + 回填 cost 四字段
8. 验收直接使用三个主任务 DoD，不单设集成验收子任务
9. **【组件拆分硬性要求 — 禁止上帝文件】**
   - demo-ui-topic 是原型参照，只复刻其交互、业务逻辑、样式、功能，**不复制其文件结构**
   - demo 原型存在大量上帝文件（如 `EnterpriseRecommendation.tsx` 1651 行、`EnterpriseEvaluationPage.tsx` 1050 行、`EnterpriseRiskInsightPage.tsx` 339 行），在 lumen-ui-topic 落地时**必须按职责合理拆分**
   - **单文件行数上限**：`.vue` / `.ts` 文件默认 ≤ 300 行；超过 300 行必须有充分理由并在 handoff 中说明；超过 500 行视为缺陷，必须拆分
   - **拆分原则**：
     - 页面壳（路由 + Tab + 视图切换）单独一个 `.vue`，不含业务逻辑
     - 每个面板/工作台/Drawer 独立组件，按 `src/components/enterprise/{module}/` 分子目录组织
     - 业务逻辑提到 composable（`src/composables/use*.ts`），组件只消费 ViewModel
     - 纯展示子块（卡片、表格、图表）再下沉一层，按 `components/enterprise/{module}/{Block}.vue` 组织
   - **验收检查**：每个子任务 DoD 须含「单文件 ≤300 行」自检，handoff 附 `wc -l src/views/enterprise/*.vue src/components/enterprise/**/*.vue src/composables/use*.ts` 输出
   - 这条与团队公约 §3.4「失败可逆」一致：拆分不合格 = 未完工，须 fix commit 拆分后再验收
