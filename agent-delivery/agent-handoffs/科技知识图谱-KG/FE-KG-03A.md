# FE-KG-03A · 算法展示 — 整页复刻（三算法切换 15 叶）

> demo 真源：`repos/demo-ui-science/src/pages/tech-knowledge-graph/AlgorithmDisplay.jsx`(165) + `PathSearchPanel.jsx`(17KB) + `CentralityPanel.jsx`(23KB) + `CommunityPanel.jsx`(21KB) + `pathSearch.js`/`centrality.js`/`community.js` + 3 selfcheck

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:frontend-agent` |
| supervised_by | `human:孔东` |
| claim_type | `pull`（4h 锁，2026-11-05 11:37 起） |
| 说明 | 认领时依赖 FE-KG-S01 为 `integration`（基座三绿+浏览器验证过）；开工前核对 01A/02A handoff 踩坑记录（5 轮走查沉淀） |

## Ponytail（coding 任务必填）

| 字段 | 值 |
|------|-----|
| ponytail | `full` |
| 说明 | 未用 YAGNI 跳过 D8 token / D9 ⓘ🧪 / 可观测埋点 / 架构铁律。算法层按规划 D1「照 demo 前端演示 + 🧪」，三算法模型层纯函数移植（禁随机/时间，见修改内容 1） |

## 01A/02A 踩坑对照（本单开工依据）

开工前通读 01A（4 轮走查）+ 02A（2 轮走查）handoff 记录，本单预先规避：

1. **Tab/卡头标题纯文字**（02A 第 2 轮升级口径）：本单开工即按「Tab 标题 + 卡头标题一律不挂图标」实现，自检断言 `<a-card` #title 块与 PageTabFrame tabs 无 `<Icon` —— **免走查返工**（用户本轮明确要求）
2. **a-table 列插槽必须声明 slotName**（02A 第 1 轮）：本单全部自定义渲染列（Tag/着色文本/路径卡片）均 `slotName` 声明 + 模板插槽名一致，自检静态断言全表校验
3. **a-progress 0-1**：percent 全部换算 0–1 域
4. **图标显式 import + 正确图标名**：先查 `@arco-design/web-vue/es/icon/index.js` 实际导出再写
5. **禁 Math.random/Date.now/new Date**：demo 三算法模型含随机（社群 LPA 传播序、PageRank 扰动等）→ 移植为确定性实现（hashSeed / 冻结种子），自检断言 models 与组件零字面量
6. **图表容器显式高度**：ECharts 容器均定高防 init 0 高死锁

## Headroom（可选）

| 字段 | 值 |
|------|-----|
| headroom | `skip`（本机未挂载） |

## 问题清单

- 无阻塞。metric 正名沿用 S01/01A/02A 盘点口径（见 D9 节）

## 修改内容

**仓：`repos/lumen-ui-science-pc`（dev，完工停本地工作区等孔东人工验收，未 commit/push）**

1. **算法层移植**（`src/views/knowledge-graph/models/`，纯函数 TS 化）：
   - `pathSearchAlgo.ts`：BFS/DFS/Dijkstra/Bellman-Ford/A* 五算法 + 4 场景子图（coop/spread/partner/nav，节点边冻结）+ 多路径枚举（DFS 限深）+ `runPathSearch` 组装（optimal/alternatives/error）；ECharts 着色映射 `PATH_NODE_TYPE_COLORS`
   - `centralityAlgo.ts`：度/紧密/中介（Brandes）/PageRank（含迭代历史）+ 相关矩阵（Pearson）+ 紧密聚类 + 移除影响分析 + 报告生成；演示图 15 节点/25 边冻结
   - `communityAlgo.ts`：Louvain 单层模块度贪心 + LPA（确定性 hashSeed 传播序）+ CNM 模块度贪心 + Infomap 近似 + 谱聚类近似 + K-means + 社群间链路矩阵 + 生命周期演化序列
2. **路径搜索面板**（`components/KgPathSearchPanel.vue`，§423–427）：场景选择（a-radio-group type="button"）→ 起/终点选择（a-select allow-search）→ 算法选择（5 算法 desc）→ 5 步进度动画 → 路径卡（optimal/alternatives，Tag 最优/可行）→ ECharts 力导图（路径节点放大红描边、路上边加深）→ 节点详情抽屉
3. **中心性分析面板**（`components/KgCentralityPanel.vue`，§428–432）：视图切换（degree/closeness/betweenness/pagerank/compare）+ 节点类型/领域/子集筛选 + slider 参数 → 度分布热力图 + 类型条形图 + 度趋势表 | 紧密雷达 + 散点 + 聚类卡 | 中介 ECharts 图（桥节点追踪 + 路径追踪 + 移除影响）| PageRank 表 + 收敛曲线 + 分布条形 + 相关热力图 | 多指标对比表 + 快照版本对比 + 雷达图 + Markdown 报告导出
4. **社群发现面板**（`components/KgCommunityPanel.vue`，§433–437）：算法选择（Louvain/LPA/CNM/Infomap/谱聚类/K-means）+ resolution/K slider → 视图切换（overview/structure/lifecycle/viz）→ 概览卡 + 色分 ECharts 图 | 结构构成饼图 + 特征卡 + 社群间热力图 | 生命周期 Timeline + 规模曲线 | 可视化指标表 + 社群详情抽屉
5. **整页**（`algorithms/index.vue`，重写 S01 占位页壳）：
   - PageTabFrame 真 3 Tab（demo 三 key：path/centrality/community，**纯文字标题无图标**）
   - #header：KgPageHeader title="算法展示" + 双轨 fetchKgAlgorithms（mock 种子 → contractPending 网关占位）
   - v-if 渲染三面板（互斥 display 不叠加）
6. **自检**（`algorithms/FE-KG-03A.test.mjs`）：demo 三份 selfcheck 断言语义摘选移植 + 03A 接线组（三面板挂接/PageTabFrame 保留判定/纯文字 Tab/Card 断言/表格 slotName 全表校验/图标显式 import 逐文件校验/禁随机时间——含注释剥离防误报）

## 测试结果（三绿）

- `pnpm type-check`（vue-tsc --build）：**0 错**（修复 4 处模型类型收窄：stepState 返回类型笔误、SCENARIO_GRAPHS possibly-undefined、reconstruct prev 索引签名、CentEdge map 元组解构）
- `node src/views/knowledge-graph/algorithms/FE-KG-03A.test.mjs`：**4 组全绿**
- `node src/views/knowledge-graph/kg.selfcheck.mjs`（S01 基座防回归）：**全绿（9 组）**
- `node src/views/knowledge-graph/analysis/FE-KG-01A.test.mjs`（01A 防回归）：**全绿**
- `node src/views/knowledge-graph/indicators/FE-KG-02A.test.mjs`（02A 防回归）：**全绿（5 组）**
- `pnpm build`：**绿**（44.4s，无本页相关告警；KnowledgeGraphCanvas 大 chunk 为 echarts 全量注册存量）

## D9 数据血缘（按 data-lineage-policy §2.3 执行契约）

- 算法层为前端演示模型（规划 D1 拍板「演示 + 🧪」）：三算法输出均 mock 语义，🧪 MockBadge 挂面板头（评审层门控，默认关闭零泄漏）
- KPI/统计卡 ⓘ：本页无独立 KPI 行（demo 源该页无头部 KPI），统计数字（社群数/模块度等）随卡片展示；metric 正名待 data-agent 统一入 registry（与 S01 `M_KG_SVC_*`、01A `M_KG_ANALY_*`、02A `M_KG_IND_*` 同批）
- 不伪闭合：报告导出/参数调整均为会话级演示态，Message 明示演示语义

## 架构合规自检（公约 §2 逐条）

- ✅ 调用链：前端不直连图谱服务/不感知 nGQL；数据经 api/knowledgeGraph.ts 双轨（mock/网关占位 contractPending）
- ✅ D8：Arco 全替换（Tabs/RadioGroup/Select/Slider/Drawer/Table/Tag/Timeline/Alert/Progress 0-1/Message）；token 走 CHART_BASE + 主色 #165dff；**Tab 与卡头标题纯文字无装饰图标**（用户本轮要求 + 01A/02A 走查口径合并）
- ✅ D12：零 demo 仓依赖；mock 种子冻结自 demo（禁 Math.random、USE_MOCK=false 零 fixture）
- ✅ 图谱铁律：demo G6 图 → ECharts graph 力导布局替换（架构铁律 3 禁 Neo4j/G6 直用），着色语义与 demo 逐 token 对齐
- ✅ 可观测：trackKgInteraction 埋点（page-mounted/path-card-pick 等）
- ✅ 互斥 display 不叠同一节点（三 Tab 面板 v-if 切换）

## 遗留风险

- metric_id 正名待 data-agent（本页统计数字随卡片，无独立 KPI 行，同批处理）
- 确定性算法与 demo 随机函数数值不同源——demo 侧 selfcheck 只断言语义（可达性/排序/模块度非降），本单自检同语义全绿；真算接入后由 BE-KG-CONTRACT-01 换数据源
- 报告导出文件名时间戳用冻结演示日期（2026-05-20 语境）；真机联调时若走 BE 时间轴需对齐（契约单登记）

## CI/CD

- 分支：`dev`（lumen-ui-science-pc）——**未 commit/push**（孔东监管限定 2026-11-04：supervised_by human:孔东 的任务完工停本地工作区等人工确认，AGENTS.md 仓级裁定优先于「完工即推」）
- 待孔东验收放行后：commit（`[agent:frontend-agent]` 标注）+ push `origin/dev` 触发 CI

## 2026-11-05 孔东走查调整（第 1 轮，任务仍处 integration 停本地）

- **抽屉加宽**：走查指认详情抽屉偏窄。本单三处 a-drawer 统一加宽——`KgPathSearchPanel.vue` 节点信息 360→**560**、`KgCentralityPanel.vue` 节点详情 400→**560**、`KgCommunityPanel.vue` 社群详情 400→**560**（三面板一致口径）
- 验证：三绿复跑全过（03A 自检 4 组 / type-check 0 错 / build 35.4s 绿）

## 签收与推送（2026-11-05）

- **人工走查放行**：human:孔东 2026-11-05 12:11 走查通过，明示「任务状态联调中，代码可 commit、push dev」
- 前端仓提交：`lumen-ui-science-pc@dev` `a78506a`（8 文件，+4043/-23；只含 FE-KG-03A 产物，policy/* 与 .env.development 本地改动非本任务产物未纳入）
- CI 将按公约触发 K8s dev rollout
- 状态保持 `integration`——UI 复刻已走查放行，但**接口尚未接入**，待 BE 接口联调完成后才转 `pending_test`（当前页面为冻结 mock 演示态，与 02A 同口径）

## 涉及文件

- `src/views/knowledge-graph/algorithms/index.vue`（重写，S01 占位页壳 → 整页）
- `src/views/knowledge-graph/algorithms/FE-KG-03A.test.mjs`（新增）
- `src/views/knowledge-graph/components/KgPathSearchPanel.vue`（新增）
- `src/views/knowledge-graph/components/KgCentralityPanel.vue`（新增）
- `src/views/knowledge-graph/components/KgCommunityPanel.vue`（新增）
- `src/views/knowledge-graph/models/pathSearchAlgo.ts`（新增）
- `src/views/knowledge-graph/models/centralityAlgo.ts`（新增）
- `src/views/knowledge-graph/models/communityAlgo.ts`（新增）

---

- actual_tokens ≈ 160k（读 demo 真源 7 件 + 01A/02A 踩坑 handoff + 实现 + 三绿 + 自检迭代）
- model_used：glm-5.3（Cursor agent 会话）
- actual_cost ≈ $2.3；cost_warn：否
