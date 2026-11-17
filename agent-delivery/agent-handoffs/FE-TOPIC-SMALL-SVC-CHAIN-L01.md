# FE-TOPIC-SMALL-SVC-CHAIN-L01 — 专题小屏·产业服务链 B（服务链三分析工作台）

- **状态**：已交付（commit `587a81c`，已推 `origin/dev`）
- **执行**：agent:frontend-agent；**监管**：human:孔东
- **交付时间**：2026-11-17 23:00 (+08:00)
- **ponytail**: full（模型函数从 PC 同文移植不重写；UI 按 Vant 小屏重写；自检脚本 1 个）

## 范围与实现（对照 PC ServiceChainAnalysisWorkspace.vue）

| 交付物 | 说明 |
|---|---|
| `src/views/service/svcShortboardModel.ts` | 短板模型，PC 同文移植（判定阈值 55 / runtime_flag / 环节行解析） |
| `src/views/service/svcEcoGraphModel.ts` | 生态图谱模型，PC 同文移植（双密度 / relation_top 不当图 / 裁剪 / 度中心性 / 影响力） |
| `src/views/service/svcEcoAnalysisWorkspace.ts` | workspace 契约，PC 同文移植（三指纹 / eco_filter / clip 持久化 / segment 下钻） |
| `src/views/service/svcSzFrameworkModel.ts` | 深圳统一评价框架模型，PC 同文移植（四指标 + Q-SVCCHAIN-04 待核验） |
| `src/views/service/svcProfileModel.ts` | 补 `orgQueryPresent`（?org= 语义） |
| `src/views/service/ServiceChainAnalysisView.vue` | 三 workspace 分发主视图（chain/graph/shenzhen，route.query） |
| `src/components/visualization/SvcEcoRelationGraph.vue` | G6 force 触屏图（tap 选节点 / 缩放工具 / 聚焦态高亮） |
| `src/router/index.ts` | `/service/chain-analysis` 挂真组件（替 NotAdaptedView） |
| `scripts/svc-chain-workspace.test.mjs` | 防漏自检（模型锚点/三分发/路由/闸门唯一/无 fixture） |

### 关键实现决策

1. **I2-12 闸门**：复用 `ChainAnalysisShell`（切条件不自动 create、同条件在跑接续、当天成功直出+重新分析），视图零自建闸门逻辑（自检第 4 条锁死）。
2. **svc create 契约**：走 `createRequest` prop 扁平 params（对齐 PC `useSvcAnalysisJob` #310–328：analysis_fp/workspace/org_ids/object_summary/industry），非 chain object 契约。
3. **图谱触屏**：G6 force 布局 + zoom-canvas/drag-canvas；节点/边过滤 + 聚焦机构收进底部 sheet（PC 横排 checkbox → van-checkbox-group sheet）；点服务机构节点开 `SvcOrgProfileDrawer`（复用已有件）。
4. **空态诚实**：reason 分支（industry_no_org / industry_no_edges / unavailable）文案与 PC 同文；空图不补 fixture。

## 产物清单

- 代码：commit `587a81c`（9 文件，+2256 行）
- 自检：`node scripts/svc-chain-workspace.test.mjs` ✅
- CI：commit 已推 `origin/dev`，等 Pipeline 绿

## 验收证据

- `node scripts/svc-chain-workspace.test.mjs` ✅
- `npm run type-check`：本单新增代码零错（基线唯一报错 `chainBlockReportDocument.ts(735)` 属并行 INTEL-D 会话，任务 A handoff 已记录 stash 隔离验证）
- K8s dev URL：CI 绿后 `https://topic.itic-sci.com:3000/m/`（/service/chain-analysis?workspace=chain|graph|shenzhen）

## 偏离说明

- attract CSV 导出等不在本单（D 单范围）。
- 报告面板（PC `SvcAnalysisReportPanel` HTML 报告）不在本单；「查看报告」按钮暂空挂（shell 内置按钮条件触发），P2 批次收尾时接 svc 域块式报告（见批次 3 方案）。

## 架构合规自检

- ✅ 调用链（前端 → Java REST → Python /internal，不可越层）：eco-graph/analysisTask* 只调 Java 门面
- ✅ D8 Design：样式 token 对齐 PC（svcEcoKindChrome / SVC_ECO_EDGE_COLOR）；小屏按 Design-mobile 断点规则
- ✅ D9 数据血缘：分数/环节行/框架值只认 GET result payload；ⓘ 角标随 P2 批次统一补（见开放项）
- ✅ D10 交互规范：tap 选节点 / sheet 过滤均键盘可达（tabindex + enter）
- ✅ D12 demo/lumen 隔离：零 demo 依赖，模型为 PC 同文移植非 merge
- ✅ 可观测埋点：defineApi 走统一 http 封装
- ✅ CI/CD：commit 推 `origin/dev` → Pipeline → K8s dev rollout

## 开放项

- ⓘ MetricSpecCard / 角标（D9）随 P2 批次统一补齐（mobile 仓 review 层接线）。
- svc 域报告文档构建（P2）。
- 依赖本单的 D 单（推荐两工作台）已解锁。

## cost

- actual_tokens ≈ 110k；model_used: glm-5.3；actual_cost ≈ $1.6；cost_warn: green
