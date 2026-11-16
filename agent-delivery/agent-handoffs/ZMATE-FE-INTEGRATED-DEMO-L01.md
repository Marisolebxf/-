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
- V3 对抗审查降级为「溯源与结论」Tab 壳 + 静态问题清单。
- 首版曾 autoRun 跳过人闸 → **已返工**：三栏 HITL，确认需求前右侧「等待需求确认」。

## 修改内容

- 新增工作区 `src/app/pages/zmate-strategy/`：首页创作壳、**Graph Hub + 七站子页**、共享 `workspaceStore`、Mock、样式。
- **分站协作（禁止单页跑完全链）**：澄清 → Planner → 辩论∥切片 → Seeker → Writer → Judge；人闸解锁；旧 `/task/:id` 重定向 Hub。
- registry 子单：`ZMATE-FE-DEMO-L02`…`L08`（各站独立 DoD；本 L01 只交枢纽骨架，不一次签收全链）。
- **菜单只增不删**：`Layout.tsx` 追加「战略报告 Demo」；既有菜单未删。
- 路由见建设方案 §9.2。

### 与两份 HTML 原型能力映射

| 能力 | 德金 HTML | 之域 HTML | 本 Demo |
|---|---|---|---|
| 项目轨两级 | ✅ | 弱 | ✅ |
| Query / 报告类型 / 专家·安装≠本次使用 | ✅ | — | ✅ |
| 生成中不出正文 | ✅ | — | ✅ |
| 正反辩论 + 三层卷宗 | — | ✅ | ✅（人控轮次 + 读写/只读） |
| 需求澄清人闸 | V2 卡 | 澄清阶段 | ✅ 三步卡 + 确认前右侧等待 |
| 无胜负 Judge | — | ✅ | ✅ 文案 |
| 专题切片/研判卡 | 资产文案 | 无 | ✅ Mock 四态 |
| 基础溯源角标 | ✅ | — | ✅ |
| V3 对抗审查 | 偏壳 | — | 降级壳 |

### 建设方案 §9.4 验收对照

| 条款 | 结果 |
|---|---|
| 三轴合一 | ✅ Hub + 分站同工作区 |
| 人在回路 | ✅ 澄清人闸 / 分站解锁 / 禁单页跑完 |
| 术语铁律 | ✅ 「辩论知识卷宗」≠「专题切片/研判卡」 |
| Judge 分职 | ✅ |
| V1 不挡 | ✅ 可澄清后快速「结束辩论并生成」；不强制多轮 |
| 数据诚实 | ✅ 四态 + 🧪 Mock，无假 live |
| 菜单增量 | ✅ Layout 仅追加 |

## 测试结果

- `pnpm build`：✅（HITL 返工后再次本地 build）
- `pnpm design:check`：❌ 既有 theme.css 合同（非本单引入）
- 本地打开：`pnpm dev` → `/zmate-strategy-demo` → 创建任务或打开已有任务，验证右侧「等待需求确认」

## 遗留风险

- design:check 红可能影响依赖该脚本的 CI job（若有）；本单未改 theme。
- 辩论/生成仍为 Mock，不可当 V1 真后端验收。

## CI/CD（必填）

- 分支：`dev`
- commit：`37efe1a94b984a1ec6f9fc269f7127d3c96db6b4`（`demo-ui-topic` HITL 返工）
- pipeline：push 后由 GitLab CI 接管
- 部署 namespace / 镜像 tag：待 CI
- K8s rollout：待 CI
- 本地路径：`${GKX_ROOT}/repos/demo-ui-topic` · `/zmate-strategy-demo/task/:id`

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
