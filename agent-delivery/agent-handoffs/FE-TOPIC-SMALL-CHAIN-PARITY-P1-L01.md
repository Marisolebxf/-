# Handoff · FE-TOPIC-SMALL-CHAIN-PARITY-P1-L01

- **任务**：专题小屏·产业分析差单 P1（区域地图图表 / 深圳看板 / 指标说明 / 过程条 / 全景补全 / 节点下钻）
- **仓库**：`repos/lumen-ui-topic-mobile`（origin/dev）
- **监管**：human:孔东 · **执行**：agent:frontend-agent
- **状态**：implementation 完成，自检三绿
- **ponytail:** full —— 复用 PC 已有实现模式（RegionalCompareMap / peerDisplayName / stepDescription / nodeTechnologyRoutes 全部从 lumen-ui-topic 对齐移植），零新依赖（leaflet/echarts/vant 仓内已装），geo 表为仓内数据资产复制（非代码，D12 允许）

## 范围与实现（对照 DoD 七项）

### ① 区域页地图与图表
- `src/utils/regionalCompareMapPoints.ts`（新）：自 PC 对齐移植，adcode→坐标索引 + gisItems/rows 双源构建圆点；含「禁止 codes[index] 配对」注释
- `src/assets/geo/region-geo-table.json`（新）：DataV GeoAtlas 中心点表（PC 同源资产复制）
- `src/components/visualization/RegionalCompareMap.vue`（新）：Leaflet + 天地图 vec/cva，circleMarker 尺寸/色阶映射；工具条（放大/缩小/复位）z-index 500 低于侧栏 Menu；小屏关 scrollWheelZoom，触摸手势由 Leaflet 默认行为支持
- `IndustryRegionalView.vue`：结果区补**地理分布**（index/competitiveness 双模式，multi_industry 不出图）、**综合指数条形图**（第 1 名 #165DFF 高亮）、**领先主体雷达图**（四力维度 max 100）
- `parseRegionalBoard` 补 `heatmap_gis` 解析 → `gisItems` / `gisEnabled` 字段（对齐 PC）

### ② 深圳页
- 发展结果 KPI 补**投融资总额**（`M_CHAIN_INVEST_TOTAL`）
- 补**来源依据**板块（sourceEvidence 三卡：独特优势/差距/劣势）+ **完整对比快照只读展开**（PC a-drawer → 小屏 van-popup bottom，快照内 peer 名走 peerDisplayName 规范化）
- 移植 `peerDisplayName`（约 20 行纯函数）：meta.benchmark.items 按 region_code/code/leaf 解析中文，修历史 payload 拼音列头；对比结果表头/快照/标杆 KPI 三处统一走 `peerColumns`

### ③ 指标说明入口
- `src/components/visualization/IndustryMetricSpecSheet.vue`（新）：小屏版指标说明 Sheet，字段与 PC IndustryMetricSpecDrawer 同源（来源/状态/权重/阈值/范围/版本/适用范围/当前输入/说明/支撑指标）；reviewMode 下显示 metricId + MetricMarker
- `IndustryRegionalView.vue`：指数权重行 + 竞争力三维行各加「说明」按钮 → `openMetricSpec`（对齐 PC openRegionalMetricSpec 契约）

### ④ 过程阶段条
- `ChainAnalysisShell.vue` running 态加 **van-steps direction="vertical"**：`chainTaskStages`（stagesForAnalysisType 真源）+ `currentStageIndex`（新工具函数，对齐 PC）驱动；三态描述（已完成/进行中/等待中）；failed 步 ✕ 红标

### ⑤ 全景页节点详情补全
- `src/api/industry/paths.ts` + `index.ts`：注册 `nodeTechnologyRoutes` 端点（`/topic/v1/meta/industry-clusters/node-routes`）+ `NodeTechnologyRoute` 类型
- 节点详情改三页签（van-tabs）：**关联企业**（去 6 截断，全量展示）/ **主流技术路线**（懒加载带竞态守卫，空态「暂无已发布主流技术路线」、失败态「技术路线读取失败」）/ **市场规模**（`dataset.marketSize` 有则展示数值+同比，无则 Q056 空态诚实文案「没有正式数据时保留空值，不使用估算值替代」）

### ⑥ 全景页节点下钻
- `canDrillSelected`（对齐 PC）：`node.drilldown || chains.some(id === node.id)`
- 详情抽屉「进入子链」按钮 → `drillToNode`：重设 draftChainId、关抽屉、重拉快照

### ⑦ 工程自检
- `pnpm type-check` ✅ · `pnpm test` 72/72 ✅ · `pnpm build` ✅（14.14s）

## 防漏扫描摘要（附录 D）

- **D.1 页面差集**：本单 6 子项全部落在 DoD 列表；对比篮/高筛 DSL/筛选模板/智能 chips 维持裁剪（Design-mobile §10 红线，未顺手补齐）
- **D.2 本地 KPI 接线**：新增统计位 2 个（投融资总额 M_CHAIN_INVEST_TOTAL、市场规模 tab——空态走诚实文案无伪数值）；既有 M_CHAIN_REGION_INDEX / M_CHAIN_SZ_ENTERPRISE_COUNT 保持
- **D.3 镜像 vs 矩阵**：本单未新增 metric 镜像；readiness 消费走既有 MetricMarker
- **D.4 错挂/正名**：peer 列头统一走 peerDisplayName（region_code 真源），修历史拼音列头错挂
- **D.5 契约防漏**：nodeTechnologyRoutes 入参 `node_id`、create extra 不变（as_of）；全景下钻复用 loadSnapshot 不另起任务

## 裁剪声明

- 无热力图降级：本单地图为 circleMarker 分布图（对齐 PC RegionalCompareMap 语义），未引入 heatmap 图层；DoD 中「热力图降级」条款不适用（PC 同名组件亦无热力层）
- 来源快照展开为 van-popup（小屏无 drawer 空间），语义与 PC a-drawer 只读一致

## 产物

- commit：`[agent:frontend-agent] FE-TOPIC-SMALL-CHAIN-PARITY-P1-L01 …`（lumen-ui-topic-mobile origin/dev）
- CI：push 后 GitLab pipeline 自动触发 → K8s dev rollout

## 架构合规自检

| 铁律 | 状态 |
|---|---|
| D8 Design/Design-mobile token | ✅ 主色 #165DFF、--sci-* 变量 |
| D9 指标 8 件套入口 | ✅ StatCard metric-id + 说明 Sheet + MetricMarker |
| D12 不 merge demo | ✅ 只读对照 PC 重写 |
| I2-12 异步闸门 | ✅ Shell 复用，未动闸门逻辑 |
| 调用链 前端→Java REST | ✅ 新端点走既有 request 封装 |
