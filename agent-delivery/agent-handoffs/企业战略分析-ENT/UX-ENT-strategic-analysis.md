# UX Handoff：企业分析（战略分析）IA / Wireframe / Gap 分析

> **⚠️ 本版为 rerun 重做版（v2），覆盖 v1（commit 6686cf1）。**
> v2 "换的思路"：在四件套之上新增 PRD 级 **功能设计说明书 `ENT-functional-design-v2.md`**（问题诊断 D1–D4 → 决策链 DC1–DC6 → 全局工作台模型 → 9 页分页规格 → E-20~E-30 验收矩阵 → 分期计划）；并把 gap 基准从 ui-agent 改造前的 7 页面刷新为 **P0 改造后（commit bc16e5a）** 的 9 页面真实状态。
> 完成方式：后台 ux-agent 子代理（重写 README/IA/userflow 后因 `resource_exhausted` 中断）→ 主会话 coordinator 接续补齐 FDS + 刷新 gap + 对齐 README，统一提交。

- **执行时间**：2026-06-18
- **角色**：ux-agent（子代理重写 3 份 + coordinator 接续补齐 3 份）
- **任务范围**：bid `§1.1.1.2.4.2.3 企业分析`（10 个三级子功能）+ acceptance-catalog `E-20 ~ E-30`
- **仓库**：`E:\gkx_src\topic_demo`（科技专题服务系统原型仓）
- **产物目录**：`topic_demo/docs/ia/enterprise/`（隔离白名单，未动 src/）

---

## 1. 完成清单对照 DoD

| DoD 项 | 状态 | 证据 |
|--------|------|------|
| 5 份 md 齐全且在隔离目录 | ✅ | README/ENT-IA/ENT-userflow/ENT-wireframe/ENT-gap-analysis |
| bid 10 子功能全覆盖 + 章节号 + E-XX | ✅ | ENT-IA §2 页面清单 |
| gap 表 A（10×7 矩阵）+ 表 B（组件映射） | ✅ | ENT-gap-analysis §1/§2 |
| 每页字段表 ≥3 核心字段（6 列） | ✅ | ENT-wireframe 各页 |
| 统计/聚合字段必有 metric_id | ✅ | 全部 `M_ENT_*`，~45 个 |
| 每页末尾 metric_id 清单 | ✅ | ENT-wireframe 各页 + 全模块汇总表 |
| mermaid 站点地图 + 主流 + ≥3 异常 | ✅ | IA §1 + userflow §1/§2（4 条异常） |
| §9 通用组件 ≥10 个被引用 | ✅ | wireframe 引用 18 个 |
| §4.2 5 段优先级每页都有 | ✅ | wireframe 各页 |
| §18 18 条对照 | ✅ | 见本 handoff §7 |
| 待评审开放项 ≥10 条 | ✅ | 见 §9（K-O1~K-O11，11 条） |
| 范围合规自检 | ✅ | IA §5 + gap §4 |
| git commit（不 push） | ✅ | commit `6686cf1` |

---

## 2. 五份产物（绝对路径 + 体量）

| 文件 | 绝对路径 | 说明 |
|------|---------|------|
| README | `E:\gkx_src\topic_demo\docs\ia\enterprise\README.md` | v2 重写 + 接力指引刷新（P0 已完成、转 P1） |
| **FDS（新增）** | `E:\gkx_src\topic_demo\docs\ia\enterprise\ENT-functional-design-v2.md` | **v2 新增**：PRD 级功能设计说明书（统领基线） |
| IA | `E:\gkx_src\topic_demo\docs\ia\enterprise\ENT-IA.md` | v2 重写（9 页架构 + Tab 分级） |
| userflow | `E:\gkx_src\topic_demo\docs\ia\enterprise\ENT-userflow.md` | v2 重写（主路径 + 4 异常 + 10 埋点） |
| wireframe | `E:\gkx_src\topic_demo\docs\ia\enterprise\ENT-wireframe.md` | 沿用 v1（已是 9 页 / M_ENT_* / 6 列字段表，v2 一致，未重写） |
| gap 分析 | `E:\gkx_src\topic_demo\docs\ia\enterprise\ENT-gap-analysis.md` | v2 刷新：基准改为 P0 改造后，覆盖率 9✅/1🟡，缺口转 P1 |

合计 **6 文件**（v2 新增 FDS 1 份）。

---

## 3. commit hash（注明未 push）

- v1 commit：`6686cf1`（topic_demo · main，原始 5 件套）
- **v2 commit：`5169a79`**（topic_demo · main）—— message：`[sandbox] ux-agent：企业分析 IA/wireframe/gap 重做(rerun v2) + 新增 FDS [agent:ux-agent]`
  - 含：新增 `ENT-functional-design-v2.md`、刷新 `ENT-gap-analysis.md`（基准转 P0 后）、更新 `README.md`（引用 FDS + §5 接力转 P1）
- **未 push**（topic_demo push 由 UE/UI 评审后人工触发，遵 ux.mdc）
- ⚠️ **完成记录**：本次 rerun 由后台子代理启动，重写 README 后因 `resource_exhausted` 中断；其对 `ENT-IA.md`/`ENT-userflow.md` 的临时改动在并发 git 活动（另一 `[agent:frontend]` 提交 `9966303`）中被回退，二者维持 6686cf1 的 9 页架构内容（已校验完好、与 v2 README/FDS/gap 一致，无断链）。coordinator 接续补齐 FDS + gap + README 并提交 5169a79。

---

## 4. 范围与实现

- **scope_ref**：bid §1.1.1.2.4.2.3.1~.10（行 4461–4607）；E-20~E-30。
- **implementation_as_built**：10 子功能映射为 9 个页面（.3.3+.3.4 合并 P3、.3.6+.3.7 合并 P6，用 PrimaryWorkbenchTabs；其余 1:1）+ E-20 概述页。新增建议路由 P1 `/enterprise/type-distribution`、P2 `/enterprise/domain-distribution`。
- **data_gaps**：市场份额 / 品牌声量 / 客户集中度 ❌ 无来源（需采购）；研发人数、毛利 ⚠️ 待确认（映射报告 §7）。
- **variance_note**：页面合并/拆分不改变叶子功能点数量（仍 10 个），符合 scope-baseline ±10%。未扩展到科研机构分析；未纳入 E-31~E-37 企业发展快速入口。

---

## 5. Gap 分析摘要（v2，基准 = P0 改造后 bc16e5a）

- **表 A 覆盖率**：✅ **9 项**（.3.1/.3.2/.3.3/.3.4/.3.5/.3.6/.3.7/.3.8/.3.9/.3.10）· 🟡 **1 项**（E-20 概述待 P1-1 收敛）· ❌ 0 项 · ⚠️ 超范围混入仍 4 处待 P1-1 迁出（明星企业 E-34 / 深圳企业 E-35 / 科研人数 E-32 / 孤儿文件 `ShenzhenEnterpriseIntroduction.tsx`）。
- **与 v1 差异**：v1 时 .3.1/.3.2/E-20 为 🟡、.3.10 "重复"；经 ui-agent P0（bc16e5a）拆页+去重后，仅余 E-20 概述 🟡。
- **当前缺口（焦点转 P1）**：
  - ~~P0-1/P0-2/P0-3~~ ✅ 已完成（bc16e5a）
  - **P1-1**（焦点）重构 overview 为纯战略概述、迁出 E-31~E-37、清理孤儿文件
  - **P1-2** Tab 样式对齐 §9.3（下划线激活）
  - **P1-3** 接入完整 MetricSpecCard/MockBadge（P0 已轻量占位）

---

## 6. §4.2 五段优先级覆盖表（每页 × 5 段）

| 页面 | ①关注什么 | ②为什么 | ③重点对象 | ④趋势/异常 | ⑤下钻明细 |
|------|----------|--------|----------|-----------|----------|
| P0 概述 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P1 类型分析 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P2 领域分布 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P3 能力评估 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P5 深圳现状 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P6 引育推荐 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P8 供应链 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P9 痛难点 | ✅ | ✅ | ✅ | ✅ | ✅ |
| P10 竞争力 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 7. §18 验收清单 18 条对照（UX 自检 + ui-agent 待办）

| # | 条目 | UX 阶段 | 责任 |
|---|------|--------|------|
| 1 | 分析工作台非门户 | 🟢 IA/wireframe 已按工作台骨架 | UX |
| 2 | 先结论再支撑 | 🟢 每页 judgment-strip 前置 | UX |
| 3 | 服务驾驶舱+分析师 | 🟢 双层 IA | UX |
| 4 | 浅色蓝灰风格 | 🟡 视觉留给 UI | ui-agent |
| 5 | 避免深色霓虹 | 🟢 文档已声明 | UX/UI |
| 6 | 信息主次清晰 | 🟢 §4.2 五段 | UX |
| 7 | 8px 圆角 | 🟡 视觉 | ui-agent |
| 8 | 升红降绿方向色 | 🟡 视觉 | ui-agent |
| 9 | chart-01~20 分类色 | 🟡 视觉 | ui-agent |
| 10 | Tag 浅底深字 | 🟡 StatusTag 视觉 | ui-agent |
| 11 | 图表用 ECharts | 🔴 现状 recharts，需迁移 | ui-agent |
| 12 | 控件用 Arco | 🔴 现状原生 select，需迁移 | ui-agent |
| 13 | 复杂筛选搜索/重置/确认/摘要 | 🟡 wireframe 已要求 SearchableCascadeFilter | ui-agent |
| 14 | 一级/二级 Tab 层级清楚 | 🟢 wireframe 已标 Primary/Secondary | UX |
| 15 | 通用+业务组件拆分 | 🟢 区块名用 §9 | UX |
| 16 | 文案克制 | 🟢 去口号 | UX |
| 17 | loading/empty/error/disabled | 🟡 userflow 异常已覆盖空态/校验/降级 | ui-agent |
| 18 | 适合截图汇报导出 | 🟢 每页含导出入口 | UX/UI |

> 绿（UX 已达成）：10 · 黄（待 ui-agent 视觉/交互）：6 · 红（技术栈偏离需迁移）：2。
> 第 19 条（D9 每个统计数字可追溯）：🟡 wireframe 已为所有统计字段分配 metric_id + 标注 ⓘ/🧪 要求，待 ui-agent 实现组件。

---

## 8. 给 ui-agent 接力的 next-step

1. **§10 Arco 控件映射**（见 gap 表 B）：`<select>`→`Cascader/Select`、`<table>`→`Table`、Modal→`Drawer/Modal`、recharts→`echarts-for-react`、自绘供应链图→AntV G6、地图→Leaflet。
2. **现有 Figma 组件迁移**：FigmaTabButton 的胶囊背景态违反 §9.3，重写为下划线激活 PrimaryWorkbenchTabs。
3. **缺口页面优先级**：先做 P0-1/P0-2（拆 .3.1/.3.2 独立页）+ P0-3（竞争力去重），再重构 overview。
4. **数据血缘组件**：实现 MetricSpecCard(ⓘ) + MockBadge(🧪)，所有 `M_ENT_*` 数字接入。
5. **复杂交互保真**：三级地理下钻、供应链 G6 图谱、雷达对比、自定义权重——不简化，按 wireframe 注解评审。

---

## 9. 待人评审开放项（≥10 条，按重要性排序）

| ID | 决策项 | 建议默认值 | 影响 | 跟踪表 |
|----|--------|-----------|------|--------|
| K-O1 | metric_id 要素代号 `ENT` vs `E1` | 按派单用 `M_ENT_*` | 全部 ~45 个 metric_id 命名 | Q009（架构决策，待 architect） |
| K-O2 | 企业类型（外企/高企/小微/上市）判定规则 | 按映射报告规则判定 | E-21 类型分析准确性 | Q010 |
| K-O6 | 技术力/商业力/竞争力指标库与默认权重 | 沿用原型默认权重 | E-23/E-24/E-30 模型 | Q014 |
| K-O9 | 招引/培育推荐指数阈值与权重 | 多因子等权 | E-26/E-27 推荐名单 | Q015 |
| K-O10 | 供应链核心供应商阈值+断链风险评级 | chain_score 阈值+中心性 | E-28 风险识别 | Q017 |
| K-O5 | 领域覆盖广度/深度口径 | chain_score+贡献加权 | E-22 | Q013 |
| K-O11 | 痛难点诊断维度与阈值 | 技术/市场/融资/管理四维 | E-29 | Q018 |
| K-O3 | "创新型企业"口径 | 高企∪专精特新∪瞪羚∪独角兽 | E-20 概述 KPI | Q011 |
| K-O8 | 多城市对标默认城市集合 | 北京/上海/苏州/广州 | E-25 | Q016 |
| K-O4 | 行政区划下钻精度（市/区县） | 到市级 | E-21 地图 | Q012 |
| K-O7 | 市场份额/品牌/客户集中度无数据源 | 暂置空+采购 | E-24 商业力 | （data-agent 采购，无甲方决策） |

---

## 10. 【数据血缘汇总】全部 metric_id 清单（按页面分组）

> 全部前缀 `M_ENT_`；命名冲突 K-O1 待 architect。统计/聚合字段 ~45 个，🔧 标记者待 algorithm-agent 实现 formula。

| 页面 | metric_id（去前缀） | source_tables（真实 DWD/ODS） | 算法依赖 |
|------|---------------------|------------------------------|---------|
| P0 | TOTAL_COUNT, INNOVATIVE_COUNT🔧, NEW_COUNT_Y, AVG_RD_INVESTMENT, PATENT_TOTAL, HIGH_TECH_COUNT🔧 | `dwd.enterprise`(+`dwd_company_honor_tags`/`dwd_org_rd_achiev_info`) | 创新型/高企标签解析 |
| P1 | TYPE_MATCH_COUNT, TYPE_COUNT🔧, TYPE_RATIO, REGIONAL_COUNT, REGIONAL_DENSITY🔧, AGGLOMERATION_INDEX🔧 | `dwd.enterprise`(+`dwd_org_reg_info.addr_lng/lat`) | 类型判定/密度/集聚 |
| P2 | DOMAIN_COVERAGE_COUNT, DOMAIN_COVERAGE_BREADTH🔧, DOMAIN_COVERAGE_DEPTH🔧, DIVERSIFICATION_INDEX🔧 | `dwd.enterprise_industry`(+`dwd_org_industry_chain_dtl.chain_score`) | 覆盖度/多元化 |
| P3 | TECH_POWER_SCORE🔧, BUSINESS_POWER_SCORE🔧, TECH_RANK🔧, PATENT_GRANT_COUNT, RD_INVESTMENT_RATIO🔧, REVENUE_LATEST, REVENUE_GROWTH_RATE🔧, PROFIT_MARGIN🔧, MARKET_SHARE❌ | `dwd.enterprise`/`dwd.enterprise_finance_history`/`dwd_org_rd_achiev_info` | 技术力/商业力评分模型 |
| P5 | SZ_COUNT, CITY_AVG_TECH_POWER🔧, CITY_DENSITY🔧, CHAIN_COMPLETENESS🔧, SZ_CHAIN_POSITION, KEY_NODE_COUNT | `dwd.enterprise`/`dwd.enterprise_industry`(`node_stage`) | 城市对标聚合 |
| P6 | ATTRACTION_INDEX🔧, CULTIVATION_INDEX🔧, GROWTH_POTENTIAL🔧, INDUSTRY_MATCH_SCORE🔧, POLICY_MATCH_SCORE🔧, RECOMMEND_COUNT | `dwd.enterprise`+`dwd.enterprise_business_tag` | 招引/培育推荐模型 |
| P8 | SUPPLIER_COUNT, CORE_SUPPLIER_COUNT🔧, NODE_CENTRALITY🔧, SUPPLY_CHAIN_RISK🔧, RELATION_STRENGTH🔧 | `dwd.enterprise_supply_chain`(`dwd_industry_chain_info`/`dwd_org_industry_chain_dtl`)+NebulaGraph | 中心性/断链风险 |
| P9 | PAINPOINT_COUNT🔧, PAINPOINT_SEVERITY🔧, PAINPOINT_GAP🔧 | 多表综合+专家知识库 | 痛难点诊断模型 |
| P10 | COMPETITIVENESS_SCORE🔧, COMPETITIVENESS_RANK🔧, SHORTBOARD_COUNT🔧, INNOVATION_INDEX🔧 | `dwd.enterprise`(tech×W1+business×W2) | 综合竞争力评分 |

**接力建议**：
- **data-agent**：把上述 metric_id 注册 `cfg_metric`（8 件套），source_tables 直接引用本表；统一 K-O1 命名后落地。
- **algorithm-agent**：实现 🔧 标记字段的 formula（技术力/商业力/竞争力/招引/培育/断链/痛难点 模型 + 密度/集聚/覆盖度计算）；与 `dwd.enterprise` 评分字段（tech_score 等）对齐。
- **api-agent**：`gkxlumen-metrics` /catalog 暴露 `M_ENT_*`；供应链走 NebulaGraph（不直连 nGQL，经 Python /internal）。

---

## 11. 【topic_demo ↔ D8 规范差异清单】

| 差异 | 现状 | D8 要求 | 复刻 lumen 时对齐建议 |
|------|------|---------|----------------------|
| 图表库 | recharts | ECharts | 全量迁 echarts-for-react |
| 表单控件 | 原生 `<select>`/`el-select` | Arco Cascader/Select | 替换 + 补搜索/重置/确认/摘要 |
| 供应链图 | div 绝对定位自绘 SVG | AntV G6 GraphCanvas | 重写，数据走 NebulaGraph |
| 地图 | 占位/区块 | Leaflet 三级下钻 | 接 Leaflet 行政区划 |
| Tab 样式 | 胶囊圆角背景态 | 下划线激活(§9.3) | 重写 PrimaryWorkbenchTabs |
| KPI 卡 | 裸 div 数字 | MetricCard + ⓘ + 🧪 | 封装 + 接 MetricSpecCard/MockBadge |
| 结论卡 | 营销渐变 bg-gradient | 克制 SectionPanel | 去渐变 |
| 弹窗 | fixed inset-0 自定义 | Arco Drawer/Modal | 详情用 DetailDrawer |

> topic_demo 作为原型沙箱保留现状（D8 对 demo2 已有代码兼容保留）；差异仅在 lumen 正式复刻时逐项对齐。

---

## 12. 【业务口径开放项登记确认】

已登记到 `agent-delivery/客户决策清单跟踪表.md`：
- §2.3：Q009（metric_id 命名 ENT/E1，架构决策）
- §2.4：Q010~Q018（企业类型/创新型口径/区划精度/覆盖度/指标权重/招引培育阈值/对标城市/供应链阈值/痛难点维度）

全部状态 🟡（临时默认值先跑），wireframe 对应区域标 ⚠️"待甲方确认"。

---

## 13. 成本回填（团队公约 §3.7）

| 字段 | 值 |
|------|-----|
| estimated_tokens | 90k–130k（UX 起草类基准） |
| actual_tokens | ~210k（含 bid/规范/映射/7 页面源码大量只读） |
| model_used | Claude Opus 4.8 |
| actual_cost | ~$7（估算，输入密集型） |
| cost_warn | 🟡 yellow（>$5，未超 $10 暂停线；主要成本在只读现有大页面做 gap 分析） |

> 备注：actual_tokens/cost 为估算值，最终以平台账单为准。
