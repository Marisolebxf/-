# Handoff：ALGO-LIB-UI-NAV-L01 — 算法库联调台左右菜单改造

- **任务 ID**：ALGO-LIB-UI-NAV-L01
- **执行 Agent**：agent:frontend-agent
- **监管人**：human:淮政玮
- **仓**：`${GKX_ROOT}/repos/demo-ui-system-test`
- **状态**：待 review（registry MCP 不可用，需 coordinator 手动更新）
- **完成时间**：2026-08-04

---

## 1. 范围与实现

| 派单包要求 | 实现 | 状态 |
|-----------|------|------|
| layout 顶栏 + 左侧菜单 + 右侧 router-view | `src/layout/index.vue` + `menuConfig.ts` | ✅ |
| 一级菜单顺序 §2.2（含 2 项灰显占位） | 8 项固定顺序；产业服务/产业综合分析 disabled + Tooltip | ✅ |
| 登录后默认 `/home`（框架联调） | router redirect 不变 | ✅ |
| 首页移除大按钮堆入口 | `home/index.vue` 仅保留联调 Demo + 清空 | ✅ |
| Demo 文案改为「××分析算法库」 | chain / policy / entan 页头已更新 | ✅ |
| `/entan` Tab→嵌套子路由 | 13 个子路由；二级侧栏分「招标对齐」「工程增强」 | ✅ |
| 【灌数据】+ SeedHelpBadge 仅基础指标 | 逻辑迁至 `entan/pages/BasicPage.vue` | ✅ |
| 政策/产业链命名 + 左侧挂载 | 已挂载；**Tab 仍保留**（最小改动，见 as-built） | ✅ |

---

## 2. 企业分析子路由映射（as-built）

### 招标对齐组

| 子菜单 | 路由 | 组件 |
|--------|------|------|
| 基础指标 | `/entan/basic` | BasicPage（含灌数据） |
| 竞争力水平分析 | `/entan/competitiveness` | ScoreView + RankingView |
| 发展历程 | `/entan/history` | PlaceholderView |
| 痛难点识别 | `/entan/pain-points` | DiagnosisView |
| 供应链关系 | `/entan/supply-chain` | CentralityView |
| 技术力评估 | `/entan/tech` | TechPower |
| 商业力评估 | `/entan/biz` | BizPower |
| 招引推荐 | `/entan/attract` | PlaceholderView |
| 培育推荐 | `/entan/cultivate` | PlaceholderView |

### 工程增强组

| 子菜单 | 路由 | 组件 |
|--------|------|------|
| 风险评分 | `/entan/risk` | RiskView |
| 重点资讯 | `/entan/news` | NewsView |
| 企业图谱 | `/entan/graph` | GraphView |
| 企业评估（异步） | `/entan/eval-async` | EvalAsyncView |

---

## 3. 偏离说明

1. **产业链 / 政策**：本任务仅完成页头命名 + 一级左侧挂载；内部仍使用 `el-tabs`（派单包允许「最小改动」，后续可复用 entan 子路由范式）。
2. **registry 状态**：本机 Cursor 未加载 `task-registry` MCP，未能自动 `in_progress` / `review` / cost 回填，请 coordinator 补录。
3. **构建验证**：当前 shell 环境无 node/npm/pnpm，未执行 `pnpm build`；请在本地或 CI 补跑。

---

## 4. 产物清单

| 文件 | 变更 |
|------|------|
| `src/layout/index.vue` | 左右布局 + el-menu 一级导航 |
| `src/layout/menuConfig.ts` | 一级菜单配置 |
| `src/router/index.ts` | entan 嵌套子路由 + meta 标题 |
| `src/views/home/index.vue` | 移除算法库大按钮入口 |
| `src/views/chain/index.vue` | 标题 → 产业链分析算法库 |
| `src/views/policy/index.vue` | 标题 → 政策分析算法库 |
| `src/views/entan/index.vue` | 子路由布局壳 + 二级菜单 |
| `src/views/entan/entanMenuConfig.ts` | 企业子菜单配置 |
| `src/views/entan/pages/BasicPage.vue` | 基础指标 + 灌数据 |
| `src/views/entan/pages/CompetitivenessPage.vue` | 竞争力（综合评分+排名） |
| `src/views/entan/components/PlaceholderView.vue` | 占位 Empty |

---

## 5. 验收证据（待补截图）

- [ ] 左菜单全貌（含 2 项灰显 + Tooltip）
- [ ] 企业分析子页二级菜单（招标组 + 工程组）
- [ ] 基础指标页【灌数据】按钮
- [ ] 发展历程/招引/培育占位页
- [ ] `pnpm build` 绿

---

## 6. 架构合规自检

| 铁律 | 结果 |
|------|------|
| 前端只经网关调 Java | ✅ 未改 API 层 |
| 不直连 Python/DB | ✅ |
| Element Plus + Vue3 本仓栈 | ✅ |
| commit 含 `[agent:frontend-agent]` | 待用户确认后提交 |

---

## 7. Cost 回填（估算）

| 字段 | 值 |
|------|-----|
| actual_tokens | ~85k（估算） |
| model_used | composer |
| actual_cost | ~$0.15（估算） |
| cost_warn | false |

---

## 8. 建议验证步骤

```bash
cd ${GKX_ROOT}/repos/demo-ui-system-test
pnpm install
pnpm dev
# 登录 → 确认左侧 8 项菜单 → 进入企业分析算法库 → 切换子路由
pnpm build
```
