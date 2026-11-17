# FE-TOPIC-SMALL-SVC-ORG-L01 — 专题小屏·产业服务链 C（机构三分析工作台）

- **状态**：已交付（commit `d49e23f`，已推 `origin/dev`）
- **执行**：agent:frontend-agent；**监管**：human:孔东
- **交付时间**：2026-11-17 23:20 (+08:00)
- **ponytail**: full（模型函数从 PC 同文移植；workspace 契约按 mobile 壳裁剪；自检脚本 1 个）

## 范围与实现（对照 PC ServiceOrgAnalysisWorkspace.vue）

| 交付物 | 说明 |
|---|---|
| `src/views/service/svcCoverageModel.ts` | 覆盖矩阵模型，PC 同文移植（矩阵形态探测 / narration 三态 / 广度深度结论 / 热力+象限 option） |
| `src/views/service/svcTrendModel.ts` | 趋势模型，PC 同文移植（年序列解析 / 窗口 3/5/8 / 对比 ≤2 / 热度诚实判定） |
| `src/views/service/svcCapabilityModel.ts` | 技术力模型，PC 同文移植（五维 + 自定义维度 / 三门槛 / 雷达 option / 禁前端重算） |
| `src/views/service/svcAnalysisWorkspace.ts` | mobile 裁剪版 workspace 契约（org_ids[] URL / svcFingerprint 4 段 / 8 叶回跳表；去 PC wait_view 壳逻辑） |
| `src/views/service/ServiceOrgAnalysisView.vue` | 三 workspace 分发主视图（field/trend/capability） |
| `src/router/index.ts` | `/service/institution-judgment` 挂真组件 |
| `scripts/svc-org-workspace.test.mjs` | 防漏自检（模型锚点/契约/三分发/路由/无前端重算） |

### 关键实现决策

1. **对象集首版 = URL `org_ids[]`**（E 单检索页「加入分析」跳入；页内 tag 可移除）。指纹 = 排序 id 串（`svcFingerprint` 4 段，与 PC 兼容历史快照解析）。mobile 无对比篮组件，`basket_empty` 门槛不适用。
2. **I2-12 闸门**：复用 `ChainAnalysisShell`；svc 扁平 create 带 org_ids/object_set/object_summary + capability 的 cap_on/cap_w + trend 的 trend_window/trend_compare（对齐 PC `useSvcAnalysisJob` #310–328）。
3. **ECharts option 复用 PC 模型原函数**：`buildCoverageHeatmapOption` / `buildCoverageMatrixOption` / `buildTrendLineOption` / `buildCapRadarOption`，触屏只需容器自适应（autoresize）。
4. **capability 门槛**：`getCapBlockers`（≥2 维 / 权重 100% / 机构 2~5 家）；权重改 stepper ±5。
5. **分数只认 GET result**：自检第 5 条正则锁死视图不得出现权重×得分求和。

## 产物清单

- 代码：commit `d49e23f`（7 文件，+2386 行）
- 自检：`node scripts/svc-org-workspace.test.mjs` ✅
- CI：commit 已推 `origin/dev`

## 验收证据

- `node scripts/svc-org-workspace.test.mjs` ✅
- `npm run type-check` ✅ 全绿（并行会话基线错误已由该会话自行修复）
- K8s dev URL：`/service/institution-judgment?workspace=field|trend|capability`

## 偏离说明

- PC 的对比篮 Pinia store + `compare-basket` API 消费未移植（mobile 首版 URL 方案，派单 note 已注明「对象集首版 URL org_ids 方案」）。API 端点已就位（任务 A），后续如需服务端篮可平滑接。
- 分析记录面板（PC `AnalysisRecordsPanel`）不在本单；mobile 由 shell 的闸门 + 「查看今日结果」覆盖核心闭环。

## 架构合规自检

- ✅ 调用链（前端 → Java REST → Python /internal，不可越层）：analysisTask* 只调 Java 门面
- ✅ D8 Design：图表配色沿用 PC token（TREND_SERIES_COLORS / SVC_CAP_RADAR_COLORS 蓝系）
- ✅ D9 数据血缘：分数/矩阵/序列只认 GET result payload；ⓘ 角标随 P2 批次统一补
- ✅ D10 交互规范：权重 stepper / 窗口 radio 键盘可达；空态文案诚实
- ✅ D12 demo/lumen 隔离：零 demo 依赖，模型为 PC 同文移植非 merge
- ✅ 可观测埋点：defineApi 走统一 http 封装
- ✅ CI/CD：commit 推 `origin/dev` → Pipeline → K8s dev rollout

## 开放项

- E 单（检索页「加入分析」跳转）是 org_ids[] 的上游来源，下一单交付。
- narration 的 ⓘ / ⚠️ 待甲方确认角标随 P2 批次统一补。

## cost

- actual_tokens ≈ 130k；model_used: glm-5.3；actual_cost ≈ $1.9；cost_warn: green
