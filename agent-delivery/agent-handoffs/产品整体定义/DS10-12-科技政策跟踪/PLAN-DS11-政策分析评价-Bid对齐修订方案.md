# 修订方案 · DS-11 政策分析评价（Bid §1.1.1.1.4.2.2 对齐）

> **致**：高颖（DS10-12 Owner）· 沈悦（体验 / 走查）  
> **抄送建议**：架构师（分轨 / 可视化栈）· frontend-agent（实施）  
> **状态**：**approved** · v1.0 · 2026-08-08（会话确认 §11 D1–D5）  
> **依据**：  
> - Bid 真源 `agent-delivery/bid-reference/科技信息展示系统和科技专题服务系统.md` **§1.1.1.1.4.2.2**（及叶子 `.1`～`.1.4`；本方案 Phase A–D 主攻可视化呈现；`.2` / `.3` 列入 Phase E）  
> - 定义包 `Wireframe-DS10-12` **F-DS-POL-11**（三类报告 + 维度条）  
> - 现状仓 `repos/demo-ui-science` → `PolicyAnalysis.jsx` + `policyData.js`  
> **前序**：会话缺口核对（2026-08-08）——地理分布 / 三类画像 / 落实 / 网民态度 / 真弦线 / 维度组合 / 模板深度与归档等未对齐  

---

## 0. 一句话结论

**把「政策分析评价」从「图表堆叠页」修订为「三类报告工作台」：顶栏固定时间·空间·类别·指标维度；「分析报告可视化」Tab 内按 Bid 叶子补齐趋势 / 分区对比 / 真弦线·传导 / 模板批量导出；父段要求的地理分布、话题热力、气泡、画像、落实与网民态度作为可视化手段挂入对应报告区，全部 Wave0 Mock（🧪），禁止直连 Nebula / Python。**

### 0.1 已批决策（2026-08-08 会话确认）· 实施铁律

| # | 决策点 | 锁定值 | 实施约束 |
| --- | --- | --- | --- |
| D1 | Tab 信息架构 | **收敛为 3 Tab**（分析报告可视化 / 结果解读 / 推荐方案） | 原「可视化分析 / 知识图谱 / 智能分析」能力下沉；禁止再增第 4 主 Tab |
| D2 | 地理分布图 | **ECharts + 现有 `geographicDistributionData` mock**（可用 `/data/china.json` registerMap） | 不引 Leaflet；不新增 npm 依赖 |
| D3 | 弦线图 | **Chord**（ECharts 6 无原生 chord → circular/ribbon 弦线形态；**禁止 sankey**） | force graph 仅作并列「关系网」，禁止标成弦线 |
| D4 | 三类画像 | Wave0：**三卡摘要 + Drawer** | 不做完整画像站；外链专题仅次要文案 |
| D5 | 导出归档 | **mock 批量队列 + 操作日志列表** | 真 PDF/Excel 生成标 🧪；禁止伪称已归档真实文件 |

```text
DEC-DS11-BID-ALIGN-20260808
  approved_by: 会话确认（产品）
  scheme: three_tabs_workbench + dimension_bar
  geo: echarts_geo_from_geographicDistributionData
  chord: chord_circular_ribbon (not sankey) + relation_graph_aside
  portrait: summary_cards_plus_drawer_wave0
  export: mock_batch_queue + op_log_list
```

---

## 1. 背景与动机

| 项 | 说明 |
| --- | --- |
| Bid | §1.1.1.1.4.2.2 **政策分析评价** → 三类报告；可视化手段含话题热力 / 地理分布 / 动态气泡 / 弦线；画像 + 话题 / 落实 / 网民态度 / 主体 |
| 叶子（本方案主攻） | `.1` 分析报告可视化 → `.1.1` 多维指标趋势 · `.1.2` 分区/群体对比 · `.1.3` 多维结构关联 · `.1.4` 模板定制与批量导出 |
| 现状痛点 | `PolicyAnalysis` 已有大量图表壳，但 **Tab 过碎（6）**、**无维度条**、**父段硬能力缺失**、叶子语义「有图≠原文」 |
| Wireframe | F-DS-POL-11 已写「维度条 + 三类报告」——实现未跟线框 |
| 目标 | V1 Demo 可走查 Bid 叶子句；覆盖矩阵可勾 `implemented`；不扩 ±10% 范围到推演/核增 |

---

## 2. 产品边界（必读）

| 允许 | 禁止 |
| --- | --- |
| 在 `demo-ui-science` 修订 `PolicyAnalysis` | 跳转专题 `/policy/*` 完成评价 |
| Mock 数据驱动图表 / 日志 | Java 写算法、前端直连 Nebula / Python |
| D9：KPI ⓘ + 🧪 MockBadge；待确认 ⚠️ | 伪闭合「已归档真实 PDF」 |
| 分轨文案可收纳到页脚/ⓘ，不抢首屏 | 新增对比篮或与 DS-10 检索混页 |

---

## 3. 缺口清单 → 修订动作映射

### 3.1 父段 §4.2.2（总述）

| ID | Bid 文案要点 | 现状 | 修订动作 | 优先级 |
| --- | --- | --- | --- | --- |
| G-P01 | 地理分布图 | 数据未挂载 | 挂 `GeographicMapPanel`（ECharts）到分析报告主画布 | P0 |
| G-P02 | 话题热力图 | 有，在独立 Tab | **迁入**分析报告或解读侧栏，去掉「可视化分析」散 Tab | P0 |
| G-P03 | 动态气泡图 | 有，散 Tab | 同上迁入 | P0 |
| G-P04 | 弦线图 | 伪 force | 真 chord/sankey + 保留关系网 | P0 |
| G-P05 | 政策/企业/人才画像 | 无 | `PortraitTrio` 三卡 + 抽屉详情 | P0 |
| G-P06 | 各地落实情况 | 无 | `ImplementationByRegion`（进度条/热力，字段落实率） | P0 |
| G-P07 | 网民态度 | 数据有 sentiment 未展示 | 热力 tooltip + 「态度分布」小图（正/中/负） | P0 |
| G-P08 | 相关主体 | 图谱弱覆盖 | 主体列表卡（与图谱联动高亮） | P1 |

### 3.2 叶子 §4.2.2.1.x

| ID | 叶子 | Bid 关键句 | 修订动作 | 优先级 |
| --- | --- | --- | --- | --- |
| G-L11 | `.1.1` 多维指标趋势 | 时间/区域/类别切换；组合指标；波动节点 | 顶栏维度条驱动 `TrendChart`；指标多选；`markPoint` 波动 | P0 |
| G-L12 | `.1.2` 分区/群体对比 | 柱状+热力；地区/行业/群体 | Tab 切换「地区 \| 行业 \| 群体」；柱状 + 效果热力 | P0 |
| G-L13 | `.1.3` 结构关联 | 因果路径、传导、弦线/关系网 | Chord + PathTrace（点击链路逐步高亮） | P0 |
| G-L14 | `.1.4` 模板与批量导出 | 周期/维度/图表类型；PDF/Excel；操作日志 | 模板表单扩展 + 批量任务列表 + `opLog[]` | P1 |

### 3.3 信息架构漂移（非功能句但阻塞验收）

| ID | 问题 | 修订 |
| --- | --- | --- |
| G-IA1 | 6 Tab ≠ Bid 三类报告 / Wireframe 3 Tab | **D1**：收敛为 3 Tab；能力下沉 |
| G-IA2 | 无维度条 | 页级 `DimensionBar`（时间·空间·类别·指标多选） |

---

## 4. 目标信息架构（修订后）

```text
┌─ 政策分析评价（DS-11）────────────────────────────────────────────┐
│ 标题区 · KPI 行（保留 D9）                                         │
│ DimensionBar：时间 ▾ · 空间 ▾ · 类别 ▾ · 指标多选 · [应用]          │
│ Tabs：                                                              │
│  [分析报告可视化]  [结果解读]  [推荐方案]                            │
│                                                                     │
│ 分析报告可视化：                                                    │
│  ┌ 左：评估指标雷达 + 画像三卡（政策/企业/人才）                    │
│  ├ 中上：多维指标趋势图（受维度条驱动）                              │
│  ├ 中下：分区/群体对比（柱状 | 热力切换）                            │
│  ├ 右/下：地理分布图 · 话题热力(+网民态度) · 气泡图                  │
│  └ 底：结构关联（弦线 | 关系网 | 传导路径）· 模板与批量导出           │
│                                                                     │
│ 结果解读 / 推荐方案：Phase E 细修（见 §7）                           │
└─────────────────────────────────────────────────────────────────────┘
```

与 Wireframe §4.1 对齐；Bid 父段可视化手段全部落在「分析报告可视化」可触达区域。

---

## 5. 文件与模块拆分（建议）

> 现状 `PolicyAnalysis.jsx` 过大；本修订**允许按区拆文件**，入口仍默认导出原页面。

| 路径（相对 `repos/demo-ui-science/src/pages/policy-tracking/`） | 职责 |
| --- | --- |
| `PolicyAnalysis.jsx` | 壳：KPI、DimensionBar、3 Tabs、导出 Modal |
| `analysis/DimensionBar.jsx` | 时间/空间/类别/指标多选 |
| `analysis/TrendMetricsChart.jsx` | `.1.1` 多维趋势 + 波动点 |
| `analysis/RegionGroupCompare.jsx` | `.1.2` 地区/行业/群体 · 柱+热力 |
| `analysis/GeographicMapPanel.jsx` | 地理分布（消费 `geographicDistributionData`） |
| `analysis/TopicHeatmapWithSentiment.jsx` | 热力 + 网民态度 |
| `analysis/BubbleChart.jsx` | 迁入现有气泡逻辑 |
| `analysis/StructureLinkPanel.jsx` | 弦线 / 关系网 / 传导路径 |
| `analysis/PortraitTrio.jsx` | 三类画像摘要+抽屉 |
| `analysis/ImplementationByRegion.jsx` | 各地落实 |
| `analysis/ReportTemplatePanel.jsx` | 模板定制 + 批量导出 + 操作日志 |
| `analysis/mock/*.js` 或扩 `policyData.js` | 落实率、态度分布、传导路径、opLog、画像 mock |
| `PolicyAnalysis.css` | 工作台栅格；维度条样式 |

编排侧同步（非阻断编码，收口时做）：

| 编排资产 | 动作 |
| --- | --- |
| `交付覆盖/.../implementation-coverage.yaml` | 增 DS-POL-11-* 叶子条目 |
| `Wireframe` F-DS-POL-11 | 补地理/画像/落实/态度控件行（若字段表缺） |
| 本 PLAN | 决策批后改 `approved` |

---

## 6. 分阶段实施计划

### Phase A · 信息架构收敛（0.5–1d）· P0 · ✅ 2026-08-08

- [x] 锁定 D1（3 Tab）  
- [x] `PolicyAnalysis` Tabs 收敛为：`report` / `interpretation` / `recommendation`  
- [x] 将现「可视化分析 / 知识图谱 / 智能分析」内容迁入 `report` / `interpretation`  
- [x] 新增页级 `DimensionBar`（默认：近 3 年 · 全国 · 全部类别 · 预选 3 指标）  
- [x] 验收：首屏仅 3 Tab；维度条应用驱动趋势图  

### Phase B · 父段硬缺口补齐（1–1.5d）· P0 · ✅ 2026-08-08

- [x] **G-P01** `GeographicMapPanel` 挂载已有 geo mock  
- [x] **G-P05** `PortraitTrio`（政策/企业/人才）+ 抽屉  
- [x] **G-P06** `ImplementationByRegion`  
- [x] **G-P07** 话题热力 + 网民态度饼图  
- [x] **G-P02/P03** 热力、气泡迁入分析报告画布  
- [x] 全部标 🧪；KPI 保持 MetricSpecTrigger  

### Phase C · 叶子 `.1.1`～`.1.3` 语义对齐（1–1.5d）· P0 · ✅ 2026-08-08

- [x] **G-L11** 趋势图：读 DimensionBar；指标多选；波动 `markPoint`  
- [x] **G-L12** 对比区：地区 / 行业 / 群体；柱状 + 热力  
- [x] **G-L13** `StructureLinkPanel`：**chord**（非 sankey）+ 关系网 + 传导路径  
- [x] 文案：force graph 仅标「关系网」  

### Phase D · 叶子 `.1.4` 模板与导出（0.5–1d）· P1 · ✅ 2026-08-08

- [x] 模板表单：汇报周期、图表类型多选  
- [x] 「批量导出」mock 队列 queued→done  
- [x] 「操作日志」列表  
- [x] UI 诚实标 🧪  

### Phase E · 结果解读 / 推荐方案收口（另开子方案）

| Bid | 状态 | 方案 |
| --- | --- | --- |
| `.2` 结果解读四叶子 | **已开子方案（draft）** | → `PLAN-DS11-结果解读多维展示-Bid对齐修订方案.md` |
| `.3` 推荐方案交互 | 未开 | 待解读方案批后另立 |

---

## 7. 验收用例（走查清单）

| ID | 步骤 | 通过标准 |
| --- | --- | --- |
| A1 | 打开「政策分析评价」 | 仅 3 主 Tab；有维度条 |
| A2 | 切换时间/空间/类别/指标 → 应用 | 趋势图 series/轴变化（Mock 即可） |
| A3 | 分析报告区可见 | 地理分布图 + 热力(含态度) + 气泡 + 画像三卡 + 落实表 |
| A4 | 结构关联 | 可见「弦线/流向」与「关系网」两种；可点选传导路径 |
| A5 | 分区对比 | 地区/行业/群体切换；柱+热力 |
| A6 | 模板导出 | 可选周期/维度/图类型；批量任务 + 操作日志有记录 |
| A7 | 全文搜 | 无「对比篮」；无跳转 `/policy/` 完成评价 |
| A8 | D9 | 效能相关 KPI 有 ⓘ；Mock 有 🧪 |

---

## 8. 不做清单

1. 不在本迭代做真实 PDF/Excel 服务端渲染。  
2. 不直连 Nebula / Python 做图谱推理。  
3. 不把 DS-12 推演、核增研报下载中心合并进本页。  
4. 不扩大到专题 E7 政策分析仓（展示分轨）。  
5. Phase E（解读多媒体、方案深度模拟）不阻塞 Phase A–D 签收。  

---

## 9. 派单建议（registry）

| 建议任务 ID | 内容 | 仓 | 依赖 |
| --- | --- | --- | --- |
| `DS11-BID-ALIGN-L00` | IA 收敛 3 Tab + DimensionBar | demo-ui-science | D1 批准 |
| `DS11-BID-ALIGN-L01` | 父段：地理/画像/落实/态度 + 图迁入 | demo-ui-science | L00 |
| `DS11-BID-ALIGN-L02` | 叶子 `.1.1`～`.1.3` 语义图 | demo-ui-science | L01 |
| `DS11-BID-ALIGN-L03` | 叶子 `.1.4` 模板批量+日志 + 覆盖回写 | demo-ui-science + orchestration | L02 |

> 建单走 task-registry MCP；本文件不直接改 registry。

---

## 10. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 单文件过大难改 | Phase A 先拆 `analysis/*` 再迁能力 |
| ECharts chord 兼容性 | 备选 sankey；验收文案写「弦线/流向图」 |
| 画像被做成专题跳转 | 抽屉内闭环；外链仅「前往专题」次要按钮且不默认 |
| 范围膨胀到 `.2`/`.3` | Phase E 单列；A–D DoD 不含 |

---

## 11. 决策记录（已确认 · 2026-08-08）

| # | 问题 | 确认 |
| --- | --- | --- |
| 1 | 批准 3 Tab 收敛（D1）？ | **是** |
| 2 | 地理图用 ECharts 消费现有 mock（D2）？ | **是** |
| 3 | 弦线用 chord 或 sankey（D3）？ | **chord**（不用 sankey） |
| 4 | 画像 Wave0 仅摘要抽屉（D4）？ | **是** |
| 5 | 导出归档用 mock 队列+日志（D5）？ | **是** |
| 6 | Phase E 是否另开方案？ | **是**（不阻塞 A–D） |

---

## 12. 修订后 DoD（A–D）

- [x] Bid §4.2.2 父段可视化手段与画像/落实/态度均可在页内指出  
- [x] §4.2.2.1.1～.1.4 叶子各有可演示主路径  
- [x] 与 F-DS-POL-11 线框一致（3 Tab + 维度条）  
- [x] `implementation-coverage` 增补 `DS-POL-11-VIZ-LEAVES`  
- [ ] handoff 含架构合规自检与 cost 回填（签收时补）  
- [x] `npm run build` 通过（2026-08-08）  

---

**维护**：决策批后升 `approved` 并回填 §11；实施以 Phase 勾选推进。  
**关联缺口会话**：2026-08-08 Bid 对齐核对（地理/画像/落实/态度/弦线/维度/归档）。
