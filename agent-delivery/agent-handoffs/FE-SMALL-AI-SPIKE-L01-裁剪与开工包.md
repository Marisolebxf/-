# FE-SMALL-AI-SPIKE-L01 · 裁剪清单与开工包

> 状态：只整理、不开工。等 `FE-SMALL-SHELL-L01` = `done` 且本叶 `ready` 后再认领。  
> 人已拍板（2026-08-25 `human:孔东`）：`claimed_by` = `supervised_by` = `human:孔东`；展示=科技全域态势；专题=企业总览；任务不拆；view 按系统分目录。

## 0. 执行约定

| 项 | 值 |
|---|---|
| 任务 | `FE-SMALL-AI-SPIKE-L01`（`spike`，不拆叶） |
| 仓 | `lumen-ui-science-mobile` |
| 执行 / 监管 | `human:孔东` / `human:孔东`（自监管，人已拍板） |
| 强度 | `ponytail lite`（排版门槛低；AI→人改） |
| 后续 | 文件拆开后，`human:曹丽影` 可只改 `src/views/topic/**` |

本叶目标是 **可演示的小屏裁剪样板 + 提示词备忘**，不是把 demo `App.jsx` / 企业驾驶舱整页搬过来。后面 BATCH-A / TOPIC-ENT 再加量。

---

## 1. 目标文件（按系统拆，方便专题仓搬走）

```text
src/views/display/trend/TechOverallSituationView.vue   # 展示 · 科技全域态势
src/views/topic/enterprise/EnterpriseOverviewView.vue  # 专题 · 企业总览
```

路由（壳里已有空壳，开工时从 `PlaceholderView` 换成上列文件）：

| 系统 | 菜单 | hash |
|---|---|---|
| 展示 | 科技发展态势 → 科技全域态势 | `#/display/trend/tech-overall-situation` |
| 专题 | 企业分析 → 企业发展 | `#/topic/enterprise-center/overview` |

`src/router/index.ts`：对上述两个 path **单独 import**，其余导航项仍走 `PlaceholderView`。不要把两页写进同一个 vue。

共用仍走 `src/components/`（`StatCard` / `ListCard` / `QuickFilter` / `ProfileDrawer` / `map/UnifiedLeafletMap`）和 `src/review/`。专题仓日后复制：`src/shell/` + `src/views/topic/` + 上述组件（按需）。

禁止本叶：新开 topic-mobile 仓、往 `lumen-ui-topic` 塞小屏、加 echarts/G6 新依赖。

---

## 2. 展示 · 科技全域态势（裁剪）

**真源**

- 招标：`bid-reference/科技信息展示系统和科技专题服务系统.md` §1.1.1.1.4.1.1（地图操作 / 图层配置 / 科创要素 / 科创事件）
- Demo 中屏：`demo-ui-science/src/App.jsx`（万行工作台：图谱、路径比较、卡片编辑、级联筛选等）
- lumen PC：`lumen-ui-science-pc` 仅有菜单名，**无对等正式页**。本叶按招标四块做 **手机总览裁剪**，不宣称 DS-01 算法闭合。

### 2.1 招标四块 → 小屏去留

| 招标块 | PC/Demo 现状（摘要） | 本叶小屏 | 说明 |
|---|---|---|---|
| 地图操作：放大缩小 / 平移 / 复位 | GIS 工具条、滚轮、搜索定位、快捷键、双指复位 | **迁入（瘦）** | Leaflet 捏合缩放 + 拖动；提供「复位」按钮调 `UnifiedLeafletMap.reset`。不做搜索历史、智能匹配后端、ESC/Ctrl+R |
| 图层配置：多对象图层 / 分组改名上色 / 数据源 | 要素开关 + 热力 + 图例 | **迁入（瘦）** | 3～4 类要素开关（论文 / 专利 / 机构 / 专家）控制点或热力。不做图层重命名、颜色编辑、数据源配置、实时监控 |
| 科创要素：详情 / 统计 / 分析 / 趋势 / 地图 | 概览卡片可拖拽隐藏、列表表、图谱、比较、导出 | **迁入（瘦）** | 见下表「要」 |
| 科创事件：时间筛选 / 重要性 / 详情 | 工作台 events tab | **迁入（极瘦）** | 3 条事件 `ListCard` → 底栏抽屉。不做时间轴滑条、重要性算法、关联分析、导出分享 |

### 2.2 迁移功能清单（展示）

**要（本叶必须可点）**

1. 页头一句态势结论（预览样例）
2. `StatCard` ×4：论文 / 专利 / 机构 / 专家（或招标主体里任选四类）。数字旁 MetricMarker；镜像没有该 `metric_id` 就走红问号，**禁止手写伪 8 件套**
3. `QuickFilter`：关键词 + 要素类型（或地区）一档。重置 / 筛选只滤本页样例
4. `UnifiedLeafletMap`：湾区/深圳若干点 + 可选热力；点选打开 `ProfileDrawer`
5. 要素 `ListCard` 5 条以内，点选同一套抽屉
6. 事件 `ListCard` 3 条，抽屉里看标题/时间/地点
7. 全部样例打「预览样例」；`USE_MOCK=false` 不走 `@/mock` / Demo fixture

**缓（BATCH-A 或 PC 复刻）**

- 卡片模板库、拖拽排序、隐藏/恢复
- 知识图谱、路径比较、路径播放
- 要素横向对比、聚类、影响力模型
- 趋势预测、异常监测、CSV 导出、关注收藏
- 地域×时间×领域级联全套
- 地图/列表双视图表格多列排序（列表用卡片即可）
- 搜索要素定位 + 历史缓存

**不要（本叶禁止）**

- 把 `App.jsx` 贴进 Vue
- 互斥 `display` 叠 PC 工作台
- 直连 Python / demo 网关
- 新增 npm 包（含 echarts、G6）

---

## 3. 专题 · 企业总览（裁剪）

**真源**

- Demo：`demo-ui-topic/src/app/pages/enterprise/EnterpriseOverview.tsx`（结论条 + MetricCard×5 + 历年新增图 + 省分布下钻 + TopN 对比篮 + 决策链按钮 + 双 Tab）
- lumen PC：`lumen-ui-topic` 侧栏 **尚未挂「企业发展」总览页**。小屏样板以 demo 总览结构为准。

### 3.1 Demo 块 → 小屏去留

| Demo 块 | 本叶小屏 | 说明 |
|---|---|---|
| JudgmentStrip 结论 | **迁入** | 一行结论 + 预览样例 |
| MetricCard ×5 | **迁入 4 张** | 企业总数 `M_ENT_TOTAL_COUNT`、近一年新增 `M_ENT_NEW_COUNT_Y`；另两张用已登记指标（技术力/商业力/竞争力三选二）。demo 的创新型/研发投入/专利/高企若镜像没有 id，不要伪造 8 件套 |
| 历年新增 EChart | **迁入（无图）** | 本仓无 echarts。用 5 行 `ListCard`（年 + 新增数）或一句趋势文案 |
| 全国分布 + 点省下钻 P1 | **迁入（瘦）** | 地图点或 3～5 条地区 `ListCard`；点击 **只开抽屉**，不跳 PC 类型分析（目标页仍是空壳） |
| 重点企业 TopN + 对比篮 | **迁入列表，丢掉篮** | `ListCard` 5 条 → `ProfileDrawer`。无对比篮、无 PermGate |
| 决策链下钻 6 按钮 | **迁入 2 条占位** | 「类型分析」「深圳现状」`ListCard` → 已有专题空壳路由（证明能跳，不要求页内有数） |
| 总览看板 / 企业总览入口双 Tab | **不要** | 只保留看板语义 |
| 全景子 Tab 重点/类型/领域 | **不要** | |
| 导出 / DeepAnalysisBanner / 权限锁 | **不要** | |
| Q031 待确认角标 | **评审层自闸** | 不要页面硬编码长文案 |

### 3.2 迁移功能清单（专题）

**要**

1. 结论条
2. `StatCard` ×4 + MetricMarker（优先已登记 id）
3. 新增趋势：列表或文案，不接 echarts
4. 地区分布：地图或列表 → 抽屉
5. TopN 企业列表 → 底栏抽屉（名称、行业、竞争力分数）
6. 两条下钻占位到现有 `nav.ts` 路由
7. 样例标「预览样例」

**缓（`FE-TOPIC-SMALL-ENT-L01`）**

- 对比篮、导出、PermGate、L1/L2/L3
- 点省进类型/领域分析真页
- 竞争力推演/权重
- 与 lumen PC 企业查询/评估工作区对齐

**不要**

- 复制 `EnterpriseOverview.tsx` 的 Tab/栅格/对比篮
- 业务 fixture 当 live
- 改 `src/views/display/**`（专题页独立文件）

---

## 4. 两页共用实现约束

- 壳、断点、token：已有 `MobileShell` / `docs/小屏断点与裁剪规则.md` / `#165DFF` / `#D8E7FC` / 触控 44px
- 趋势色：升红降绿
- 可观测：不删 `observability.ts` 请求头；本叶可不加新埋点事件
- 数据：页内常量即可，注释写「预览样例，非 USE_MOCK fixture」
- 人改：AI 出一版后孔东改间距/文案/卡片顺序，不重写壳

---

## 5. 建议开工顺序（仍是一叶）

1. 路由接线 + 两个空 vue 骨架（能进页）
2. 展示全域态势（样板，先写备忘草稿）
3. 专题企业总览（套同一套组件）
4. 定稿 `docs/小屏AI出效果备忘.md`（提示词 + 改哪些/不改哪些）
5. handoff + cost；`spike`：`in_progress` → `ready_to_sign`

丽影介入时：只 PR `src/views/topic/enterprise/EnterpriseOverviewView.vue`（及该页样式），不要动展示目录。

---

## 6. 开工话术（放行后贴新会话）

闸门：`task-get FE-SMALL-SHELL-L01` 为 `done`，`FE-SMALL-AI-SPIKE-L01` 为 `ready` 后，先 MCP `task-claim`。

```text
/goal frontend-agent
身份：你是经验丰富、遵循最佳实践的资深前端工程师，精通 Vue 3 + Vite + Arco Design Vue / TypeScript；只经网关调 Java，沿用 observability.ts，不直连 Python/DB。
强度：ponytail lite。禁止用 YAGNI 跳过 D8/D9/D10、可观测与架构铁律。本叶是小屏裁剪样板，不追求与 demo 中屏 1:1。
复刻：本叶不是整页 Demo 复刻。对照裁剪清单做「布局+交互+样式+评审+预览样例」。禁止 USE_MOCK=false 时 fixture 填数。范围=下面两页，不是一模块全菜单。
任务 ID：FE-SMALL-AI-SPIKE-L01
claimed_by：human:孔东
supervised_by：human:孔东
仓库：${GKX_ROOT}/repos/lumen-ui-science-mobile
必读：
  - agent-delivery/agent-handoffs/FE-SMALL-AI-SPIKE-L01-裁剪与开工包.md（本包，去留真源）
  - repos/lumen-ui-science-mobile/docs/小屏断点与裁剪规则.md
  - repos/lumen-ui-science-mobile/src/views/ComponentPreviewView.vue（组件用法）
  - agent-delivery/Design.md（token / 主色 #165DFF / 页底 #D8E7FC）
范围清单：
  1. 展示 科技全域态势 → src/views/display/trend/TechOverallSituationView.vue
     路由 #/display/trend/tech-overall-situation
  2. 专题 企业总览 → src/views/topic/enterprise/EnterpriseOverviewView.vue
     路由 #/topic/enterprise-center/overview
  3. router 只把这两条从 PlaceholderView 换成真页；其它菜单仍空壳
  4. 只复用已有 StatCard / ListCard / QuickFilter / ProfileDrawer / UnifiedLeafletMap
  5. 写 docs/小屏AI出效果备忘.md（提示词 + 改哪些/不改哪些）
禁止：
  - 拆成两个 registry 任务
  - 新增 echarts/G6/npm 包
  - 搬 demo App.jsx / 对比篮 / 卡片编辑 / 图谱
  - 两页写在同一个 vue；展示代码放进 views/topic 或相反
DoD：registry 四条 + 本包「要」清单可点 + 备忘落地 + handoff（ponytail: lite）
Handoff：agent-delivery/agent-handoffs/FE-SMALL-AI-SPIKE-L01.md
```

未放行时不要 `task-claim`、不要改业务 vue。
