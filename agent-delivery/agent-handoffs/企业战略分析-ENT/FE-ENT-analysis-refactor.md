# Handoff · WP3c 企业「分析层」FDS v2 重构 + 跨层带参打通

| 属性 | 内容 |
|------|------|
| 任务 | WP3c · 企业分析层（E-20~E-30）按 FDS v2 重构 + 与门户层跨层带参联通 |
| 角色 | frontend-agent |
| 仓库 / 分支 | `topic_demo`（原型仓） · `feat/ent-elements-build` |
| 真源 | `docs/ia/enterprise/ENT-functional-design-v2.md`（FDS v2）/ `ENT-gap-analysis.md` / `ENT-userflow.md` §0 / `scripts/check-design-contract.mjs` |
| 状态 | ✅ 完成（design:check 绿 / build exit 0 / lints 0） |

---

## 1. 按 FDS v2 重构了哪些页（对照 gap-analysis）

复用 WP3a 基础层（`components/common/*`：ContextBar / MetricCard / MetricSpecCard ⓘ / MockBadge 🧪 / StatusTag / RoleLevelGate / CompareBasket / EChart）与 WP3b 门户层（`pages/development/portalShared.tsx`：`useEnterpriseProfileDrawer` / `buildEnterpriseProfileUrl` / `findEnterprise` / `JudgmentStrip` / `SectionPanel` / `RoleSwitch` / ContextBar 选项）。**统一企业画像复用 `ElementProfile`（DR-04 抽屉/整页同源），未另起实现。**

新增分析层公共骨架 `src/app/pages/enterprise/analysisShared.tsx`：`AnalysisShell`（角色上下文 S1/S2 + 标题 + JudgmentStrip 结论先行 + 全局 ContextBar + 角色切换）、`useEnterpriseCodeParam`（读跨层 `enterprise_code`）、`SearchEntryButton`（跳检索工作台）、`DeepAnalysisEntryBanner`（带参回跳定位/高亮 + 一键开画像）。

| 验收点 | 页面 | 现状(gap) → FDS v2 重构后 | 决策链阶段 |
|--------|------|---------------------------|-----------|
| E-20 | `EnterpriseOverview.tsx`（P0） | 🟡 混入 E-31~E-37 宣传/科研人数 → **纯战略驾驶舱**：结论先行 JudgmentStrip + MetricCard×5（企业总数/创新型/平均研发投入/专利总量/高企数，均带 ⓘ+🧪）+ 历年新增趋势(ECharts) + 全国分布(点击省→P1) + 重点企业 TopN(加入对比篮/开画像) + 决策链下钻入口。**已移除明星/深圳企业介绍/科研人数大盘**（迁门户层，§6.4） | 入口 |
| E-21 / E-22 | 并入 `EnterpriseOverview` 结构洞察(analysis-tabs) | 🟡 P1/P2 独立路由当前分支未建 → 按 FDS §4.2 **并入承载**：`setPanoramaSubTab` 切「企业全景 / 企业类型分布分析 / 领域分布分析」，类型/领域 ECharts + 指标卡 + Q010/Q012/Q013 ⚠️ 角标 | A 结构洞察 |
| E-23 / E-24 | `EnterpriseCapabilityEvaluation.tsx`（P3） | ✅→ 强化：global-workbench-tabs(技术力/商业力)；指标库勾选 + 权重滑块(Σ=100% 且 ≥2 家才可生成，NF-08)；雷达 + 加权排名 + 差距结论；商业力对标 + 增长趋势；市场份额无源**灰显**(R-02) | B 能力评估 |
| E-25 | `EnterpriseStatusAnalysis.tsx`（P5） | ✅→ 重构：global-workbench-tabs(产业链定位/多城市横向对标)；链位清单+链中角色 StatusTag；城市对标雷达/环节柱/完整度/趋势；**已移除「综合竞争力」Tab（.3.10 去重，仅 P10 承载）**；Q016 ⚠️ | A 结构洞察 |
| E-26 / E-27 | `EnterpriseRecommendation.tsx`（P6） | ✅→ 重构：global-workbench-tabs(招引/培育) + 招引二级 analysis-tabs(强链/补链/智能/存量)；读 `strategy=补链` 默认补链；名单列含 推荐指数ⓘ/核心优势/关键指标/合作价值·所需支持/操作；培育梯度层(专精特新/瞪羚/小巨人/独角兽) | D 行动推荐 |
| E-28 | `SupplyChainAnalysis.tsx`（P8） | ✅→ 重构：global-workbench-tabs(单链下钻/多链对比)；**ECharts graph 力导向图谱**(lumen 复刻走 G6+NebulaGraph，NF-02)；中心性排名+StatusTag；断链风险等级+处置建议；「仅看核心供应商」折叠；高风险→跳 P9 | C 风险诊断 |
| E-29 | `PainPointsAnalysis.tsx`（P9） | ✅→ 重构：诊断维度勾选(技术/市场/融资/人才/管理/政策)+生成；分类统计(ECharts)+行业最佳对标雷达；问题清单(严重度 Tag+成因)；解决方案+最佳实践 EvidenceList；导出；加入培育候选 | C 风险诊断 |
| E-30 | `CompetitivenessAnalysis.tsx`（P10） | ✅(原两处重复)→ 唯一入口：综合指标库+赋权(Σ=100%,NF-08)+生成；雷达+综合排名+短板维度提示；一键导入 P3 技术力/商业力子维度；对比篮非空自动带入 | B 能力评估 |

**技术栈对齐 D8**：全部页 recharts → **ECharts**（复用 `EChart.tsx`）；交互控件统一 Arco（Button/Select/Checkbox/Slider/Tag/Message）；主切换 `.global-workbench-tabs`、次级 `.analysis-tabs`；样式消费 `design-tokens`；规避 check 脚本全部 forbidden 模式。

---

## 2. 跨层带参 + 统一画像联通实现点

- **统一画像抽屉（DR-04）**：每页 `useEnterpriseProfileDrawer()`（来自 portalShared，内部即 `ElementProfile` + `enterpriseSearchConfig`）。所有企业名/卡片点击 → `openProfile(record)`（Arco `Button type="text"`，**非 cursor-pointer 假按钮**）。
- **新窗口整页画像**：抽屉「在新窗口完整打开」→ `buildEnterpriseProfileUrl(code)` → `/development/enterprise/:enterpriseCode`（portalShared 内置，同源同数据）。
- **门户「深度分析」回跳**：`useEnterpriseCodeParam()` 读 `?enterprise_code=<统一社会信用代码>`，`DeepAnalysisEntryBanner` 定位/高亮命中企业 + 一键开画像；P6/P0 列表对命中行 `--sci-primary-soft` 高亮。
- **检索入口**：P0 及各页 `SearchEntryButton` → `/development/search?mode=keyword`。
- **页内跳转带参（FDS §7.3）**：P0 省份点击→P1（region/industry）；P0/P5 下钻→P5/P6；P5 链位缺口→P6（chain_gap, strategy=补链）；P8 高风险→P9（enterprise_code, dimension=供应链）。当前为 Mock Message + 埋点占位（路由跳转用 `useNavigate`，带参跳转记 `ENT_DEEPANALYSIS_JUMP` / `GEO_DRILLDOWN`）。
- **对比篮跨页**：P0 TopN/ P3·P10 复用 `useCompareBasket('enterprise')`（单例+localStorage，跨页保留）；P3/P10 篮非空时自动带入对比企业（FDS §7.2）。
- **埋点（observability，含 user_level）**：`ENT_DEEPANALYSIS_JUMP / GEO_DRILLDOWN / EVALUATE_RUN / INDICATOR_CONFIG / REPORT_EXPORT / ENT_ADD_COMPARE / ENT_ADD_LIST / ENT_SEARCH_MODE_SWITCH / ENT_FILTER_APPLY` 等，统一携带当前角色级别。

---

## 3. S1/S2 角色分级落点（ENT-userflow §0）

`AnalysisShell` 默认 `initialLevel='S2'`（功能全开），ContextBar 内置 RoleSwitch 可切 S1 演示分级；`RoleLevelGate` 命中门槛**非阻断**（弱化+锁标+升级引导，记 `ent_upgrade_prompt`）。

| 能力 | 门槛 | 落点页 |
|------|------|--------|
| 自定义指标/权重 + 生成评估/诊断 | `allow={['S2']}` | P3 / P9 / P10（业务分析师专属，S1 看结论） |
| 导出报告/名单 | `allow={['S1','S2']}` | 全部分析页 |
| 深度分析跨层跳转 / 补链名单 / 风险诊断跳转 / 综合竞争力下钻 | `allow={['S1','S2']}` | P0 / P5 / P8 |
| 加入对比篮 | `allow={['U2','S1','S2']}` | P0 TopN |

> S1 领导驾驶舱：看全局结论 + 趋势 + 重点对象（隐藏自定义指标/生成等明细操作）；S2 业务分析师：完整分析工作台（筛选/评估/对比/诊断/导出）。

---

## 4. design:check / build 结果

```
> npm run design:check
Design contract checks passed

> npm run build
dist/assets/index-*.js  3,604.29 kB | gzip: 952.81 kB
✓ built in 33.08s   (exit 0)
```

- `scripts/check-design-contract.mjs` 对 `pages/enterprise/*` 的全部硬断言通过（global-workbench-tabs / analysis-tabs / setPanoramaSubTab / Arco Button·Select / 无私有·card Tab / 无 type="card" / 无 cursor-pointer / 无原生 button(P9·P10) / 无 `<select>`·`<input 搜索>`·forbidden tailwind 等）。
- ReadLints：改动文件 0 错误。
- chunk >500kB 为既有告警（非本任务引入，topic_demo 原型暂不拆包）。

---

## 5. 改动文件树（仅本 WP 改动；未 add dist/ node_modules/）

```
topic_demo/
├─ src/app/pages/enterprise/
│  ├─ analysisShared.tsx           （新增｜分析层公共骨架 + 跨层带参 hook）
│  ├─ EnterpriseOverview.tsx       （重写｜P0 驾驶舱，2929→约 360 行，移除门户内容）
│  ├─ EnterpriseCapabilityEvaluation.tsx （重写｜P3）
│  ├─ EnterpriseStatusAnalysis.tsx （重写｜P5，去重竞争力 Tab）
│  ├─ EnterpriseRecommendation.tsx （重写｜P6）
│  ├─ SupplyChainAnalysis.tsx      （重写｜P8，ECharts graph）
│  ├─ PainPointsAnalysis.tsx       （重写｜P9）
│  └─ CompetitivenessAnalysis.tsx  （重写｜P10）
└─ src/app/mock/enterprise/
   └─ metricSeed.ts                （扩展｜补 13 个分析层 metric 8 件套：M_ENT_INNOVATIVE_COUNT /
                                      RD_INVEST_AVG / PATENT_TOTAL / TECH_POWER_SCORE / BUSINESS_POWER_SCORE /
                                      CHAIN_COMPLETENESS / CITY_RANK / ATTRACTION_INDEX / CULTIVATION_INDEX /
                                      NODE_CENTRALITY / SUPPLY_CHAIN_RISK / PAINPOINT_COUNT / PAINPOINT_SEVERITY）
```

handoff：`agent-delivery/agent-handoffs/企业战略分析-ENT/FE-ENT-analysis-refactor.md`（本文件）。

---

## 6. 与 wireframe / FDS v2 对照（核对项）

- ✅ 每页 JudgmentStrip 非空（结论+原因+建议动作 deep link）。
- ✅ 每个统计数字旁 ⓘ MetricSpecCard（metric_id 8 件套）+ Wave0 🧪 MockBadge。
- ✅ 全局 ContextBar（产业/时间窗/区域）+ 角色切换跨页骨架；对比篮跨页（P0/P3/P10）。
- ✅ E-20~E-30 10 叶子功能 1:1 覆盖（P1/P2 并入 P0 结构洞察；.3.10 去重仅 P10）。
- ✅ 业务口径未定项（Q010~Q018）UI 加 ⚠️「待甲方确认」提示 + MetricSpecCard pending_ref。

---

## 7. 遗留 / 需 coordinator 处理项

1. **P1/P2 独立路由缺失**（`/enterprise/type-distribution`、`/enterprise/domain-distribution`）：本 WP 严格不改 `routes.tsx` / `Layout.tsx`（WP3b 范围）。当前类型/领域分布**已并入 P0「结构洞察」analysis-tabs 承载**，叶子功能不缺。若 FDS v2 §6.2 要求独立页与侧边栏入口，**需 coordinator 安排在 routes.tsx 增 2 条路由 + Layout 侧边栏 2 菜单**（届时可将 P0 结构洞察子视图抽为独立页复用同 mock）。
2. **孤儿文件 `ShenzhenEnterpriseIntroduction.tsx`**：未路由、属门户层 E-35（已由 `development/ShenzhenEnterprises.tsx` 承载）。本 WP 未改（避免越界 + 非分析层 FDS 范围），仍为 recharts/Tailwind。建议后续 coordinator 安排清理或正式归并门户层。
3. **跨层页内带参跳转**目前为 Mock（Message + 埋点），真实 query 跳转/落参（region_code、chain_gap、bottleneck_tags[] 等）待 Wave 1 各目标页接收侧实现。
4. **地图三级下钻 / G6 图谱 / 权重校验后端**：Wave 1（Leaflet/AntV G6/Python 模型）替换，当前 ECharts graph + 省份柱状为占位（NF-06/NF-09 降级不阻塞）。
5. **新增 metric 口径**：`metricSeed.ts` 补的 13 条为前端 Mock 占位（多为 pending_algorithm / pending_data_lead Q011/Q014/Q015/Q016/Q017/Q018），需 data-agent 在 `cfg_metric-ENT-seed.yaml` 会签正式口径后对齐。
