# Handoff｜E-ZHIKU-PROTOTYPE-110-R3：ZHIKU-TALENT-POOL / ZHIKU-TALENT-MAP 科技人才智慧服务闭环重实现

> **批次**：R3（重跑，延续 R1 打样确认 + R2 同一标准）
> **执行**：frontend-agent（监管人/认领：human:淮政玮）
> **日期**：2026-08-05
> **业务仓 commit**：`03e0d42`（主实现）+ `1fc778b` / `5783d06`（AC 补漏），demo-ui-gaoduanzhiku-view @ origin/dev

## 1. 范围与实现（对照 bid-reference）

范围真源：`agent-delivery/bid-reference/高端智库/新型高端智库需求拆解.md` §四 模块二"科技人才智慧服务"。两叶子切分：

- **ZHIKU-TALENT-POOL 科技人才库**：序号 59-74 + 80-81（画像四维、领域分类、TOP100 人才池、多维检索清单、收藏、人才资讯、推送）
- **ZHIKU-TALENT-MAP 科技人才地图**：序号 75-79（分布地图、人才指数、精准检索、驾驶舱、高端订阅）

| 序号段 | 需求 | 落地 |
| --- | --- | --- |
| 59-62 | 人才全景画像（基础/关联/行为/心理四维） | F-TP-01/02：URL `scholar+tab` 可分享恢复、活跃学者持久化、搜索未命中 Empty 不清词、相似学者/合作网络节点切换画像、心理 Tab 常驻 ⚠️ Q-ZHIKU-05 边界声明 |
| 63-65 | 领域分类与新兴方向 | F-TP-03：九大类树选中持久化、图谱节点跳画像、推荐已阅持久化、真实 CSV 导出 |
| 66-70 | TOP100 与人才池 | F-TP-04：筛选持久化、命名池建/改/删（撤销）、共享复制摘要、真实 CSV、**生成人才池分析报告 → writing createTask 预填并跳大纲（CT-TP-01）** |
| 71-74 | 多维检索个性化清单 | F-TP-05：四维筛选+双视图持久化、统计图随筛联动、空态导出禁用、收藏三处同步（F-TP-06 FavoritesDrawer 跨页沉淀） |
| 80-81 | 人才资讯与推送 | F-TP-07/08：资讯类别/关键词过滤持久化、关联学者回链画像、订阅关键词入偏好（CT-TP-02）、偏好增删幂等、新增偏好真实生成推送条目、未读卡 `ZHIKU-TP-PUSH-UNREAD` |
| 75 | 人才分布地图 | F-TM-01：类别/热力/流向持久化、地图↔列表双向联动、选中点持久化+被过滤自动清除 |
| 76 | 人才指数 | F-TM-02：权重滑杆持久化、多区域对比选择、权重和为 0 显示"—"、`ZHIKU-TM-INDEX-SCORE` **D1 missing 红问号 + GAP（Q-ZHIKU-04）** |
| 77 | 人才精准检索 | F-TM-03：语义/关键词双模式、状态机 loading/empty、历史 5 条持久化、空词拦截、结果下钻画像 |
| 78 | 人才驾驶舱 | F-TM-04：统计卡显隐定制（至少留一张）+ 产业联动选中持久化、预测虚线演示态声明、`ZHIKU-TM-COCKPIT-ALERT` D1 missing |
| 79 | 高端人才订阅 | F-TM-05：规则增删幂等持久化、命中预览实时联动、**新增规则真实推送至人才动态（CT-TM-02）**；F-TM-06：**生成人才地图分析报告 → writing 预填任务（CT-TM-01）** |

## 2. 产物清单

**叶子五件套 ×2**（`agent-delivery/agent-handoffs/产品整体定义/E-ZHIKU-新型高端智库/`）：

- `ZHIKU-TALENT-POOL-科技人才库/`：USM（8 故事 US-ZHIKU-TP-01…08，42 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 59-74+80-81 反向核对闭合、指标 rename 登记）。
- `ZHIKU-TALENT-MAP-科技人才地图/`：USM（6 故事 US-ZHIKU-TM-01…06，27 AC）/ IA / Wireframe / UX-SPEC / TRACE.yaml（序号 75-79 闭合、`ZHIKU-S4-TALENT-FLOW-NET` 错挂修正登记）。

**业务仓代码**（3 commits，25+6+2 files，约 +1824/−328）：

- `src/mock/talentPool.ts` / `talentNews.ts`（前缀 `zhiku-tp-`）、`talentMap.ts`（前缀 `zhiku-tm-`）：reducer 化 action + localStorage 持久化（筛选/收藏/人才池/偏好/推送流/订阅规则/权重/选中点/驾驶舱定制等 20+ key）。
- `src/views/talent/`：4 Home + 12 Panel 全部重实现或重构（URL tab/scholar 契约、EmptyState 全覆盖）；新增 `components/FavoritesDrawer.vue`。
- `src/utils/csv.ts`：真实 CSV 下载工具（BOM + 转义）。
- `src/mock/metricSeed.ts` / `readinessSeed.ts`：`ZHIKU-S4-TALENT-*` → `ZHIKU-TP-*`（7 枚）/ `ZHIKU-TM-*`（5 枚）正名，S4 期未注册即上屏的 5 枚指标补登记；全仓 rg 校验 0 命中 `ZHIKU-S4-TALENT`。

## 3. AC-US 自走查表（TP 42 + TM 27 = 69 条）

### ZHIKU-TALENT-POOL

| AC | 结论 | 说明 |
| --- | --- | --- |
| TP-01-01 URL scholar+tab 恢复 | ✅ | route.query 双向同步 + `zhiku-tp-active-scholar` |
| TP-01-02 基础信息结构化字段+双时间轴 | ✅ | ProfileBasicPanel（S4 资产收编） |
| TP-01-03 关联信息四块+贡献度 ⓘ | ✅ | `ZHIKU-TP-INFLUENCE-SCORE` 演示态标注 |
| TP-01-04 行为信息三块 | ✅ | `ZHIKU-TP-GROWTH-INDEX` ⓘ |
| TP-01-05 相似学者切换+URL 同步；未命中 Empty 不清词 | ✅ | switchScholar → URL watch；missKeyword 保留 |
| TP-01-06 指数演示态诚实标注 | ✅ | 两处"演示态简化公式"标注 |
| TP-02-01 心理 Tab 常驻 ⚠️ 声明 | ✅ | 顶部 a-alert 不可折叠 |
| TP-02-02 三块全 mock 种子 | ✅ | talentProfile.ts 种子，无硬编码结论 |
| TP-02-03 打分演示态标注 | ✅ | 全数值带标注 |
| TP-02-04 tab=psych URL 直达 | ✅ | tab 同步契约 |
| TP-02-05 无结论性文案 | ✅ | 无"风险判定/不建议引进"类表述 |
| TP-03-01 树选中联动+持久化 | ✅ | `zhiku-tp-domain-selected` |
| TP-03-02 节点总数卡 ⓘ+🧪 | ✅ | `ZHIKU-TP-DOMAIN-NODE-TOTAL` |
| TP-03-03 图谱节点跳画像 | ✅ | scholar 参数契约 |
| TP-03-04 推荐已阅持久化+演示标注 | ✅ | `zhiku-tp-rec-read` |
| TP-03-05 导出真实 CSV | ✅ | downloadCsv 节点分布 |
| TP-04-01 筛选叠加+刷新保留+空态清空 | ✅ | `zhiku-tp-top100-filters` |
| TP-04-02 命名池保存+持久化 | ✅ | `zhiku-tp-pools`（名称去重校验） |
| TP-04-03 池重命名/更新成员/删除确认 | ✅ | removePool 带撤销 Modal |
| TP-04-04 共享复制摘要+导出真实 CSV | ✅ | sharePool clipboard + exportPool |
| TP-04-05 池成员下钻画像 | ✅ | scholar 参数契约 |
| TP-04-06 两统计卡 ⓘ+🧪 | ✅ | `ZHIKU-TP-TOP100-TOTAL` / `ZHIKU-TP-POOL-TOTAL` |
| TP-04-07 生成报告真实建任务+跳大纲 | ✅ | CT-TP-01 createTask 预填 5 章 |
| TP-05-01 四类筛选+总数卡联动 | ✅ | `ZHIKU-TP-LIST-TOTAL` |
| TP-05-02 双视图+筛选持久化 | ✅ | `zhiku-tp-list-view` / `list-filters` |
| TP-05-03 统计图随筛联动+空态 | ✅ | distOption 计算属性 |
| TP-05-04 导出真实 CSV+空结果禁用 | ✅ | 按钮 :disabled + 守卫 |
| TP-05-05 条目下钻+收藏点亮 | ✅ | toggleFavorite 即时同步 |
| TP-06-01 三处收藏入口同步 | ✅ | 同一 store.favorites getter |
| TP-06-02 抽屉跳画像/取消+徽标一致 | ✅ | FavoritesDrawer + a-badge |
| TP-06-03 收藏持久化 | ✅ | `zhiku-tp-favorites` |
| TP-06-04 空收藏引导 Empty | ✅ | EmptyState 引导文案 |
| TP-07-01 类别+关键词过滤持久化 | ✅ | `zhiku-tp-news-filters` |
| TP-07-02 关联学者徽标跳画像 | ✅ | 无关联不显徽标 |
| TP-07-03 订阅关键词入偏好 | ✅ | CT-TP-02 → preferences + 推送生成 |
| TP-07-04 空态+清空筛选 | ✅ | EmptyState + 按钮 |
| TP-07-05 预置资讯池演示标注 | ✅ | 卡片标注 |
| TP-08-01 未读卡与推送流一致 | ✅ | `ZHIKU-TP-PUSH-UNREAD` = unreadCount |
| TP-08-02 偏好三类增删幂等+持久化 | ✅ | `zhiku-tp-push-prefs` |
| TP-08-03 新增偏好真实生成推送 | ✅ | generatePushForPreference 带匹配原因+🧪 |
| TP-08-04 单条/全部已读+持久化 | ✅ | markAllRead / markRead |
| TP-08-05 模板推送演示标注 | ✅ | 推送区标注 |

### ZHIKU-TALENT-MAP

| AC | 结论 | 说明 |
| --- | --- | --- |
| TM-01-01 地图↔列表双向联动 | ✅ | selectedId prop（R2 增量）+ select-point |
| TM-01-02 类别/热力切换持久化 | ✅ | `zhiku-tm-categories` / `heat` |
| TM-01-03 分布总数卡 ⓘ+🧪 联动 | ✅ | `ZHIKU-TM-DIST-TOTAL` 随筛联动 |
| TM-01-04 流向完整；被过滤自动清除选中 | ✅ | clearStalePointSelection watch |
| TM-01-05 选中点刷新恢复 | ✅ | `zhiku-tm-selected-point` |
| TM-02-01 权重滑杆实时反算+持久化 | ✅ | `zhiku-tm-index-weights` |
| TM-02-02 指数 D1 missing 红问号+GAP | ✅ | GAP-ZHIKU-TM-INDEX 治理引用 |
| TM-02-03 区域切换联动+视图切换 | ✅ | 柱/雷达 + 对比区域选择 |
| TM-02-04 权重和 0 显示"—" | ✅ | weightedScoreDisplay，不伪造 |
| TM-02-05 Q-ZHIKU-04 常驻声明 | ✅ | a-alert 常驻 |
| TM-03-01 双模式切换+🧪 说明条 | ✅ | 语义模式意图解析说明 |
| TM-03-02 结果/专家下钻画像 | ✅ | scholar 参数跨叶子契约 |
| TM-03-03 历史 5 条持久化复搜 | ✅ | `zhiku-tm-search-history` |
| TM-03-04 无命中 Empty 不清词；空词拦截 | ✅ | Message.warning 拦截 |
| TM-03-05 匹配度演示态标注 | ✅ | "演示态相似度"标注 |
| TM-04-01 统计卡显隐定制+全隐拦截 | ✅ | toggleCockpitCard 至少留一张 |
| TM-04-02 产业联动+选中持久化 | ✅ | `zhiku-tm-cockpit-industry` |
| TM-04-03 预测分段+D1 missing | ✅ | `ZHIKU-TM-COCKPIT-ALERT` 红问号 |
| TM-04-04 统计口径一致 | ✅ | 与种子数据同源 |
| TM-05-01 规则增删幂等+持久化 | ✅ | `zhiku-tm-sub-rules` |
| TM-05-02 订阅总数卡 ⓘ+🧪 联动 | ✅ | `ZHIKU-TM-SUBSCRIPTION-TOTAL` |
| TM-05-03 新增规则真实推送人才动态 | ✅ | CT-TM-02 appendGeneratedPush |
| TM-05-04 命中预览联动+Empty 引导 | ✅ | rulePreview 计算属性 |
| TM-05-05 预置资源池演示标注 | ✅ | 订阅区标注 |
| TM-06-01 真实创建写作任务+统计要点 | ✅ | CT-TM-01 createTask 大纲注入分布数据 |
| TM-06-02 跳大纲+任务入列表 | ✅ | `/writing/create?step=outline&task=` |
| TM-06-03 Modal 说明跨模块+🧪 | ✅ | 确认制，取消无副作用 |

## 4. 验收证据

- `vue-tsc --build`：**0 错**（exit 0，三轮验证）。
- `vite build`：**通过**（exit 0，仅 chunk 体积告警，与 R1/R2 一致）。
- 业务仓 push：`2d6dd9c..03e0d42..1fc778b..5783d06 dev -> dev`，GitLab CI 自动触发（K8s dev rollout）。
- 走查路径：W1 画像 URL 分享+收藏三处同步 → W2 人才池建池/共享/导出/生成报告跨叶子 → W3 地图双向联动+选中持久化 → W4 指数权重+对比+D1 missing → W5 订阅规则→人才动态推送闭环（对应两份 USM §5）。

## 5. 架构合规自检（公约 §2 十条）

1. 算法只在 Python：✅ 影响力/成长/指数/预测/语义检索全部 🧪 演示态并登记 GAP，无前端真实算法冒充。
2. 调用链：✅ demo 全 mock；正式态服务面已在两份 IA §7 声明（Java REST → Python internal）。
3. 图谱：✅ 合作网络为前端 GraphView 演示，未引入 Neo4j。
4. 可观测性：✅ 沿用仓内 `observability.ts` 接线，未破坏。
5. CI/CD：✅ push dev 触发 Pipeline。
6. demo2 只读 merge：✅ 不涉及。
7. 共享聚合核心：✅ 前端只消费 mock/未来 Java REST。
8. 数据策略：✅ 指标 8 件套 source_tables 写 ADS 目标口径，Mock 填充。
9. 前端规范（D8）：✅ Arco Design Vue + ECharts + Leaflet 栈内；主色/token 未改。
10. 数据血缘（D9）：✅ 12 枚指标 ⓘ+metric_id+就绪度角标；`ZHIKU-TM-INDEX-SCORE` / `ZHIKU-TM-COCKPIT-ALERT` D1 missing 红问号 GAP 引用；🧪 MockBadge 全量；rename 无双 id 残留。

## 6. 偏离说明

- 心理信息（序号 62）：仅 mock 结构演示 + 常驻边界声明，采集/展示边界待合规 Owner 书面确认（Q-ZHIKU-05，TRACE deviations 已登记）。
- 人才指数（序号 76）：权重加权为前端本地演示计算，算法定义卡未落地（Q-ZHIKU-04），指标 D1 missing 诚实态，上线前须补算法卡或业务态置灰。
- 驾驶舱趋势预测（序号 78）：预测段为演示态虚线，非模型产出，同挂 Q-ZHIKU-04。
- 主页/荣誉等学者外链（序号 59）：demo 以占位文本呈现，不做真实外站跳转。

## 7. cost 回填（budget-estimate 口径）

- `actual_tokens`：≈ 360,000（本批次会话累计，含两套五件套撰写与实现）
- `model_used`：claude-fable-5
- `actual_cost`：≈ $5.5（估算）
- `cost_warn`：false（< $10）

## 8. 遗留风险

- CI 流水线结果需在 GitLab 确认绿（`5783d06` push 后自动触发，本 handoff 提交时处于运行中）。
- 两枚 D1 missing 指标（人才指数/驾驶舱预警预测）依赖算法定义卡（Q-ZHIKU-04），上线前必须补齐。
- 人才画像心理信息边界（Q-ZHIKU-05）未获甲方书面确认前，该 Tab 只能以演示态出现，禁止对外展示。
- localStorage 状态与 R1（`zhiku-wr:`）/R2（`zhiku-br-`）域相互独立；演示前如需干净环境，清除 `zhiku-tp-` / `zhiku-tm-` 前缀 key。
