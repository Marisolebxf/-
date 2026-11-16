# ZMATE-FE-INTEGRATED-DEMO-L01 · Zmate 战略报告纯前端综合 Demo

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | registry 已 in_progress；本叶完工交付 Demo |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 与派单一致；未用 YAGNI 跳过 D8/D10、可观测与建设方案 §9；D9 角标 Mock 示意、无假绿 live |

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机未对本单强制压缩 |

## 图即契约

| 字段 | 值 |
|------|-----|
| diagram_id | N/A |
| 说明 | 纯前端 Demo 页，未改存储/全局拓扑图 |

## 问题清单

- demo-ui-topic 无 `pnpm type-check` 脚本；以 `pnpm build` 为工程门禁。`pnpm design:check` 在既有 `theme.css` 缺 padding 断言处失败（与本单无关，未改 theme）。
- V3 对抗审查降级为抽屉壳 + 静态问题清单。
- 生成动画为假延迟 timeline，非真实 MCP。

## 修改内容

- 新增工作区 `src/app/pages/zmate-strategy/`：首页创作壳、任务工作区（澄清/辩论/切片/报告/审阅壳）、Mock fixture、样式。
- **菜单只增不删**：`Layout.tsx` `navGroups` 末尾追加分组「战略报告 Demo」→「战略报告创作工作台」；既有分组/项未删改。
- `routes.tsx` 增量路由：`/zmate-strategy-demo`、`/zmate-strategy-demo/task/:taskId`。
- 埋点：`zmate_strategy_home_view` / `task_create` / `task_view` / `generate_*` / `debate_round`。

### 与两份 HTML 原型能力映射

| 能力 | 德金 HTML | 之域 HTML | 本 Demo |
|---|---|---|---|
| 项目轨两级 | ✅ | 弱 | ✅ |
| Query / 报告类型 / 专家·安装≠本次使用 | ✅ | — | ✅ |
| 生成中不出正文 | ✅ | — | ✅ |
| 正反辩论 + 三层卷宗 | — | ✅ | ✅（读写/只读切换） |
| 无胜负 Judge | — | ✅ | ✅ 文案 |
| 专题切片/研判卡 | 资产文案 | 无 | ✅ Mock 四态 |
| 基础溯源角标 | ✅ | — | ✅ |
| V3 对抗审查 | 偏壳 | — | 降级壳 |

### 建设方案 §9.4 验收对照

| 条款 | 结果 |
|---|---|
| 三轴合一 | ✅ 同任务工作区阶段条切换 |
| 术语铁律 | ✅ 「辩论知识卷宗」≠「专题切片/研判卡」 |
| Judge 分职 | ✅ |
| V1 不挡 | ✅ 首页创建→自动生成可直达报告 |
| 数据诚实 | ✅ 四态 + 🧪 Mock，无假 live |
| 菜单增量 | ✅ Layout diff 仅 +8 行追加 |

## 测试结果

- `pnpm build`：✅（vite build ~38s，commit 前本地）
- `pnpm design:check`：❌ 既有 theme.css 合同（非本单引入）
- 本地打开：`pnpm dev` → 侧栏「战略报告 Demo」或直达 `/zmate-strategy-demo`

## 遗留风险

- design:check 红可能影响依赖该脚本的 CI job（若有）；本单未改 theme。
- 假进度与预置辩论数据仅供评审示意，不可当 V1 真后端验收。

## CI/CD（必填）

- 分支：`dev`
- commit：`4c0c4941634ad79df2389053cacebe9209306b65`（`demo-ui-topic`）
- pipeline：push 后由 GitLab CI 接管（本机未等流水线绿）
- 部署 namespace / 镜像 tag：待 CI
- K8s rollout：待 CI
- 本地路径：`${GKX_ROOT}/repos/demo-ui-topic` · 路由 `/zmate-strategy-demo`

## 可观测性（建议）

- 页面级 `track(...)` 已加；无 OTEL 服务名变更
- Wave 0 console/CustomEvent sink（仓内惯例）

## 涉及文件

- `repos/demo-ui-topic/src/app/pages/zmate-strategy/*`
- `repos/demo-ui-topic/src/app/components/Layout.tsx`（仅追加）
- `repos/demo-ui-topic/src/app/routes.tsx`（仅追加）

## 架构合规自检（摘要）

| 铁律 | 结果 |
|---|---|
| D8 Arco / Design token | ✅ |
| D12 未写 lumen-* | ✅ |
| 菜单只增不删 | ✅ |
| 不直连 metric-registry / 真 MCP | ✅ |
| 调用链不越层 | ✅（无后端） |
