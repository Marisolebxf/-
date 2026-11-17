# FE-TOPIC-SMALL-SVC-REC-L01 — 专题小屏·产业服务链 D（推荐两分析工作台）

- **状态**：已交付（commit `52e3cf5`，已推 `origin/dev`）
- **执行**：agent:frontend-agent；**监管**：human:孔东
- **交付时间**：2026-11-17 23:35 (+08:00)
- **ponytail**: full（模型从 PC 同文移植；视图 Vant 小屏重写；自检脚本 1 个）

## 范围与实现（对照 PC ServiceRecommendAttractWorkspace.vue + ServiceRecommendCultivateWorkspace.vue）

| 交付物 | 说明 |
|---|---|
| `src/views/service/svcRecommendAttractModel.ts` | 招引名单模型，PC 同文移植（固定权重 35/30/20/15 / 禁 Σ(指标×权重) / 保持 Java 顺序） |
| `src/views/service/svcRecommendAttractWorkspace.ts` | 推荐 workspace 契约，PC 同文移植（两指纹 / 集群→L0 链码并集 / 指纹还原产业） |
| `src/views/service/ServiceRecommendView.vue` | 两 workspace 分发主视图（attract/cultivate） |
| `src/router/index.ts` | `/service/institution-decision` 挂真组件 |
| `scripts/svc-rec-workspace.test.mjs` | 防漏自检（固定权重/两指纹/rec-list 只认 Java/路由/无本地 CSV） |

### 关键实现决策

1. **attract 固定权重**：Tag 展示 35/30/20/15（Q-SVCCHAIN-05 等权待甲方确认标注保留）；名单行读四指标 `indicators/dimension_scores`。
2. **名单只认 Java**：任务成功后拉 `svcRecList`（kind=attract|cultivate，chain_codes 产业切片）；分数/名次禁前端重算、保持 Java 顺序。
3. **narration 三态**：复用 `parseSvcCoverageNarration` + `userFacingSvcNarration`（ok 才渲染 AI 研判）。
4. **导出**：不做本地 CSV（`buildAttractCsv` 未消费）；首版走分析任务产物下载（shell「查看报告」按钮位）。
5. **I2-12 闸门**：复用 `ChainAnalysisShell`；指纹产业进段（同产业复用当天结果，切产业开新分析）。

## 产物清单

- 代码：commit `52e3cf5`（5 文件，+728 行）
- 自检：`node scripts/svc-rec-workspace.test.mjs` ✅
- CI：commit 已推 `origin/dev`

## 验收证据

- `node scripts/svc-rec-workspace.test.mjs` ✅
- `npm run type-check` ✅ 全绿
- K8s dev URL：`/service/institution-decision?workspace=attract|cultivate`

## 偏离说明

- attract CSV 导出、分析记录面板不在本单（mobile 首版闭环 = 配置 → 分析 → 名单 + AI 研判；导出走任务产物）。
- PC 的 300+ 行筛选面板（城市/环节/优先级 facets）未移植；mobile 首版按产业切片过滤（chain_codes），后续按需补。

## 架构合规自检

- ✅ 调用链（前端 → Java REST → Python /internal，不可越层）：rec-list 只调 Java 门面
- ✅ D8 Design：卡片式名单对齐 PC token（rank badge / 指标行）
- ✅ D9 数据血缘：名单分数/名次只认 Java items；Q-SVCCHAIN-05 待确认文案保留
- ✅ D10 交互规范：名单行 tap 开画像抽屉；空态诚实
- ✅ D12 demo/lumen 隔离：零 demo 依赖
- ✅ 可观测埋点：defineApi 走统一 http 封装
- ✅ CI/CD：commit 推 `origin/dev` → Pipeline → K8s dev rollout

## 开放项

- ⓘ 角标 / 分析记录面板随 P2 批次统一。

## cost

- actual_tokens ≈ 100k；model_used: glm-5.3；actual_cost ≈ $1.4；cost_warn: green
