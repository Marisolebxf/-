# QA 验收报告 · 企业要素全集（门户层 + 分析层 + 检索 + 统一画像 + 角色分级）

| 属性 | 内容 |
|------|------|
| 任务 | WP4 · 企业要素全集验收（qa-agent，验收角色，**未改任何 src 代码**） |
| 角色 / 作者 | `[agent:qa-agent]`（人评审：待 PM/UE/架构师） |
| 日期 | 2026-06-19 |
| 仓 / 分支 | `topic_demo`（原型仓）· `feat/ent-elements-build`（未 push） |
| 验收对象 | `src/app/pages/{development,enterprise}/*`、`components/{common,search}/*`、`routes.tsx`、`Layout.tsx`、`mock/enterprise/*` |
| 验收基准 | `acceptance-catalog/catalog-topic-enterprise.yaml`（E-01~E-37）/ `ENT-IA.md` / `ENT-gap-analysis.md` / `ENT-userflow.md` / `ENT-search-design.md` / `ENT-element-master-design.md` / `data-lineage-policy.md`（D9）/ `Design.md` §14（D8） |
| 验收方法 | 只读代码核验 + `npm run design:check` + `npm run build` + 浏览器烟测（dev server `:5173`，复用既有 server） |

---

## 0. 验收结论摘要

> **总结论：有条件通过（PASS WITH CONDITIONS）**

| 维度 | 结果 |
|------|------|
| 构建/契约门禁 | ✅ `design:check` 通过 + `build` exit 0 |
| 路由可达性（15 条核心路由 + 5 侧边栏菜单组） | ✅ 100% 可达，无白屏、无控制台报错 |
| E-20~E-35 前端可验收覆盖（16 项） | ✅ **通过 16 / 16（100%）**（E-36/E-37 为后台能力，非前端范围） |
| 检索体验 SE-01~06 | ✅ 通过 5 / 部分 1（SE-06 范式壳就位、仅企业 config 落地） |
| 角色分级 U1/U2/S1/S2 | ✅ 能力门非阻断 + ⚠️ 待甲方角标就位；⚠️ 1 处**角色标签口径与 userflow §0 不一致**（一般缺陷） |
| D8 §14 检查清单 + 验收标准 | ✅ 全部 ✅（原型沙箱兼容口径，技术栈 lumen 复刻另算） |
| D9 血缘 8 件套 / ⓘ / 🧪 / ⚠️ | ✅ 抽样 6 个 metric 8 件套齐全；ⓘ/🧪/⚠️ 三件套到位（4 段链路核验受 Wave 0 限制，延后 Wave 1） |
| 架构合规（公约 §2 前端相关项） | ✅ 全绿 |

**阻断级缺陷：0 项。**

**有条件项（上线 / 评审前需处理）**：
1. （一般）`RoleSwitch` 角色中文标签（S1=内部经办 / S2=内部管理 / U3=生态·企业）与 `ENT-userflow.md` §0 矩阵（S1=领导驾驶舱 / S2=业务分析师 / U3=内容管理员）口径不一致——能力门逻辑无误，仅展示文案需对齐统一。
2. （待甲方 🟡）Q010~Q018 业务口径（企业类型判定 / 区划精度 / 广度深度公式 / 评分权重 / 中心性 / 痛点维度等）均以「团队临时默认值 + ⚠️ 角标 + `pending_ref`」运行，上线前须甲方书面确认升 🟢。
3. （Wave 1）D9 四段链路核验（UI→API→ADS→DWD→ODS）受 Wave 0 无 `/metrics/v1/catalog` API、无真实 ODS 限制，本期仅核验 8 件套元数据完整性 + 声明级血缘链，链路实测延后 Wave 1。

---

## 1. design:check / build 结果

```text
> npm run design:check
> node scripts/check-design-contract.mjs
Design contract checks passed          ✅ (exit 0)

> npm run build
> vite build
✓ 3718 modules transformed
dist/assets/index-*.css  802.04 kB | gzip: 104.31 kB
dist/assets/index-*.js  3,621.15 kB | gzip: 956.83 kB
✓ built in 33.35s                      ✅ (exit 0)
```

- `design:check` 通过 = D8 契约硬断言（`.global-workbench-tabs`/`.analysis-tabs`、Arco Button/Select、无 `type="card"` Tab、无 `cursor-pointer` 假按钮、无原生 `<select>`/搜索 `<input>`、无 recharts、无 forbidden tailwind 模式等）全部满足。
- `build` exit 0；chunk > 500 kB 为既有告警（topic_demo 原型暂不拆包，非本期引入，非阻断）。
- 备注：PowerShell 捕获 npm 的 stderr 输出为 `NativeCommandError` 文本，**非构建失败**，vite 实际 `✓ built`，exit code = 0。

---

## 2. 路由可达性表（以 `routes.tsx` + `Layout.tsx` 实际为准）

| 层 | 路由 | 组件 | 侧边栏挂载 | 渲染 | 控制台 | 结论 |
|----|------|------|-----------|------|--------|------|
| 门户 | `/development/overview` | `DevelopmentOverview` | 门户-企业发展 ▸ 企业发展概况 | ✅ | 无 | 通过 |
| 门户 | `/development/search` | `SearchPage` | 门户-企业发展 ▸ 企业检索 | ✅ | 无 | 通过 |
| 门户 | `/development/enterprise/:enterpriseCode` | `EnterpriseProfilePage` | （分享直达页，不入菜单 ✅按约定） | ✅ | 无 | 通过 |
| 门户 | `/development/key-enterprises` | `KeyEnterprisesPanorama` | 门户-企业发展 ▸ 重点企业全景图 | ✅ | 无 | 通过 |
| 门户 | `/development/star-enterprises` | `StarEnterprises` | 门户-企业发展 ▸ 明星企业介绍 | ✅ | 无 | 通过 |
| 门户 | `/development/shenzhen` | `ShenzhenEnterprises` | 门户-企业发展 ▸ 深圳企业介绍 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/overview` (P0) | `EnterpriseOverview` | 企业分析 ▸ 企业概览 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/type-distribution` (P1) | `EnterpriseTypeDistribution` | 企业分析 ▸ 重点企业类型分析 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/domain-distribution` (P2) | `EnterpriseDomainDistribution` | 企业分析 ▸ 重点企业领域分布分析 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/capability` (P3) | `EnterpriseCapabilityEvaluation` | 企业分析 ▸ 企业能力评估 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/status-analysis` (P5) | `EnterpriseStatusAnalysis` | 企业分析 ▸ 深圳企业现状分析 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/recommendation` (P6) | `EnterpriseRecommendation` | 企业分析 ▸ 企业引育决策 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/supply-chain` (P8) | `SupplyChainAnalysis` | 企业分析 ▸ 供应链协同分析 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/pain-points` (P9) | `PainPointsAnalysis` | 企业分析 ▸ 企业发展支持 | ✅ | 无 | 通过 |
| 分析 | `/enterprise/competitiveness` (P10) | `CompetitivenessAnalysis` | 企业分析 ▸ 企业竞争力分析 | ✅ | 无 | 通过 |

> 另：`/enterprise/analysis`、`/enterprise/overview` 默认 index 重定向就位；门户 6 个快速入口（policy/park/talent/finance/report/appeal）保留 `PlaceholderPage` 占位，属门户外壳范围，非企业要素验收项。
> **路由可达性结论：15/15 通过（100%）。** 侧边栏「门户-企业发展」5 项 + 「企业分析」9 项菜单全部挂载且高亮正常。

---

## 3. E-20~E-35 覆盖矩阵（E-XX × 承载页 × scope 满足 × 结论 × 证据）

> 图例：✅ 通过 · 🟡 部分 · ❌ 不通过 · ⬛ 非前端范围

| E-XX | 名称 | 承载页 / 路由 | scope_summary 满足 | 结论 | 证据 |
|------|------|--------------|-------------------|------|------|
| E-20 | 企业分析概述 | P0 `/enterprise/overview` | 战略驾驶舱：JudgmentStrip + MetricCard×5（ⓘ+🧪）+ 历年趋势 + 全国分布 + TopN | ✅ | 烟测渲染正常；已移除 E-31~E-37 宣传内容（gap A2 闭环） |
| E-21 | 重点企业类型分析 | P1 `/enterprise/type-distribution`（**独立页**） | 国/省/市三级下钻 + 产业/类型筛选 + 类型结构 | ✅ | 烟测确认「国级/省级/市级」三级下钻控件 + Cascader 产业 + 类型多选；MapPanel Wave0 占位(🧪)。**WP3d 已修偏离为独立页+独立路由+菜单** |
| E-22 | 重点企业领域分布分析 | P2 `/enterprise/domain-distribution`（**独立页**） | 选企业→解析标签映射领域→广度/深度/多元化 | ✅ | 企业多选 + 覆盖广度/深度/多元化 MetricCard×3 + 领域饼/条形 + 映射表 + 抽屉画像 |
| E-23 | 企业技术力评估对比 | P3 `/enterprise/capability` 技术力 Tab | 指标库+自定义权重(Σ=100%)+雷达+排名+差距 | ✅ | 5 赋权滑块 + 雷达 + 排名表；权重校验门（≥2 家且 Σ=100%） |
| E-24 | 企业商业力评估对比 | P3 `/enterprise/capability` 商业力 Tab | 商业指标+对标+增长趋势+横向对比 | ✅ | 商业力 Tab 对标 + 趋势；市场份额无源灰显 |
| E-25 | 深圳企业现状分析 | P5 `/enterprise/status-analysis` | 产业链定位 + 多城市横向对标 | ✅ | 双 Tab（产业链定位/多城市对标）；**已去重「综合竞争力」Tab → 归并 P10** |
| E-26 | 招引企业推荐分析 | P6 `/enterprise/recommendation` 招引 Tab | 强链/补链/智能/存量 + 推荐名单 | ✅ | 三层 Tab（招引/培育→强链/补链/智能/存量）+ 推荐指数ⓘ 名单表 |
| E-27 | 培育企业推荐分析 | P6 `/enterprise/recommendation` 培育 Tab | 指标配置 + 梯度培育层 + 名单 | ✅ | 梯度层（专精特新/瞪羚/小巨人/独角兽）+ 培育名单 |
| E-28 | 企业供应链关系分析 | P8 `/enterprise/supply-chain` | 单链下钻/多链对比 + 图谱 + 关键节点 + 风险 | ✅ | ECharts 力导向图谱 + 中心性排名 + 断链风险 + 「仅看核心供应商」折叠；高风险→P9 |
| E-29 | 企业发展痛难点分析 | P9 `/enterprise/pain-points` | 诊断维度 + 分类统计 + 问题清单 + 方案 | ✅ | 诊断配置 + 柱/雷达 + 严重度 Tag 清单 + 方案 EvidenceList |
| E-30 | 企业竞争力分析 | P10 `/enterprise/competitiveness`（**唯一承载**） | 综合指标体系 + 评分排名 + 短板提示 | ✅ | 指标库赋权(Σ=100%)+雷达+综合排名+短板；对比篮非空自动带入。**两处重复已去重** |
| E-31 | 企业发展入口（父，含 4 子页） | 门户-企业发展菜单组 + `/development/overview` + `/development/search` | 入口 + 整体概况 + 重点/明星/深圳子页 | ✅ | 侧边栏 5 项齐全；检索工作台作入口核心 |
| E-32 | 企业整体概况 | `/development/overview` | 总数/趋势/全球全国分布/科研人数 | ✅ | MetricCard + 趋势 + 分布；快速入口已下沉 |
| E-33 | 重点企业全景图 | `/development/key-enterprises` | 产业链分类 + 规模统计 + 领域统计 | ✅ | 产业链上中下游全景 + 规模/领域分布 + Top 榜单 |
| E-34 | 明星企业介绍 | `/development/star-enterprises` | 产品全景/技术看板/团队/生态图谱 | ✅ | 明星单选 + 产品全景 + 团队表 + 产业生态力导图 |
| E-35 | 深圳企业介绍 | `/development/shenzhen` | 数量/领域/规模分布 + 重点企业 | ✅ | 概况 + 趋势 + 规模饼 + 区域柱 + 地图占位(🧪) + 重点企业表 |
| E-36 | 可视化展示内容管理 | （系统管理中心·后台） | 内容管理 | ⬛ | **非前端原型范围/后台能力**，仅预留前端消费字段口径 |
| E-37 | 门户内容管理维护 | （系统管理中心·后台） | 内容维护 | ⬛ | **非前端原型范围/后台能力**，标注待系统管理中心 |

**覆盖率统计（前端可验收 E-20~E-35，16 项）**：✅ 通过 16 / 🟡 0 / ❌ 0 = **100%**。
- 分析层 bid `.3.1~.3.10` 10 个三级叶子功能 1:1 全覆盖（.3.3+.3.4、.3.6+.3.7 Tab 承载；.3.1/.3.2 已独立成页；.3.10 去重），符合 ±10% 铁律。
- 跨层联动验证：P0 全国分布点击省→P1 带 `?region=`；门户「深度分析」→分析层带 `?enterprise_code=` 高亮；统一画像抽屉↔整页同源（DR-04）；对比篮跨页（P0/P3/P10）——均烟测/代码核验通过。

---

## 4. 检索体验 SE-01~06 判定表

| SE | 体验点 | 承载 | 结论 | 证据 |
|----|--------|------|------|------|
| SE-01 | 三模式检索（关键字/智能/高级筛选） | `SearchPage` ▸ `SearchHub`（`.global-workbench-tabs`） | ✅ 通过 | 烟测确认三模式 Tab 可切换；关键字检索出 12 条结果；智能搜索为 Wave0 本地 `smartParser` NL→DSL（Chips 回显），Wave1 切 Python |
| SE-02 | 抽屉画像 + 新窗口整页 | `ElementProfile`(`mode=drawer 720px` / `page`) | ✅ 通过 | 烟测：点公司名开右侧抽屉 → 抽屉头部「在新窗口完整打开」→ 新标签打开 `/development/enterprise/:code`；同源同数据（PR-01~PR-03） |
| SE-03 | 结果内再检索（排序/二次筛选/在结果中搜） | `ResultToolbar` | ✅ 通过 | 智能排序 + 视图切换（卡片/表格）+ 结果内再筛 + 在结果中搜；不重置主条件 |
| SE-04 | 高级筛选单/组合条件 + 存模板/模板库 | `FilterPanel` ▸ `ConditionBuilder`（Arco Drawer） | ✅ 通过 | 单条件+组合条件(AND/OR) + 字段库分类 + 存为模板/模板库；运算符随字段类型自适应（模板持久化 Wave0 本地） |
| SE-05 | 统计 ⓘ / Mock 🧪 / 待定 ⚠️ | `MetricCard`+`MetricSpecCard`+`MockBadge` | ✅ 通过 | 命中数 MetricCard 携 metric_id；ⓘ 弹 8 件套；🧪 Mock 角标；⚠️ pending_ref 待甲方提示（代码核验 + 烟测见 ⓘ） |
| SE-06 | 通用范式可复用（政策/科研机构/服务机构） | `SearchScaffold` + `ElementSearchConfig` | 🟡 部分 | 壳组件要素无关（RS-01~RS-05 就位），但仅 `enterpriseSearchConfig` 落地；其他要素 PoC 未做（设计 §9 列 P2/Wave2，符合分期，非阻断） |

**SE 结论：通过 5 / 部分 1（SE-06 按分期为 P2/Wave2，本期不阻断）。**

---

## 5. 角色分级 U1/U2/S1/S2 判定表（对照 userflow §0 矩阵）

| 能力门槛 | 设计要求 | 落地核验 | 结论 |
|---------|---------|---------|------|
| 级别识别（user_level） | 引入 user_level 上下文 + `RoleLevelGate` | `UserLevelProvider` + `useUserLevel` + `RoleSwitch`（嵌 ContextBar.extra）；门户默认 U2、分析层默认 S2；埋点统一携 `user_level` | ✅ |
| 能力收敛**非阻断** | 命中门槛弹「登录/升级」引导，不阻断浏览 | `RoleLevelGate` 越权 = 视觉弱化(opacity .55)+锁标(IconLock)+Tooltip 升级引导 + 记 `ent_upgrade_prompt`，**不禁用整页** | ✅ |
| U1 公众脱敏画像 | 敏感字段脱敏 + 登录引导 | 画像「联系方式（敏感信息）」经 `RoleLevelGate allow={['S1','S2']}` 脱敏（U1/U2 见锁标引导） | ✅ |
| U2 检索/对比/配额导出 | 全三模式 + 收藏/对比 + 配额导出 | 三模式开放；对比篮跨页；导出经 `RoleLevelGate`（分级）；去 SCRM 动作集（对比/收藏/导出/深度分析） | ✅ |
| S1 领导驾驶舱 | 看全局结论，隐藏明细配置 | 自定义指标/权重/生成 `allow={['S2']}`（S1 看结论）；导出/深度分析 `allow={['S1','S2']}` | ✅ |
| S2 业务分析师 | 完整分析工作台 | 全功能开放（筛选/评估/对比/诊断/导出）；`AnalysisShell` 默认 S2 | ✅ |
| ⚠️ 待甲方角标 | 未定口径加 ⚠️「待甲方确认」 | `MetricSpecCard` pending_ref → ⚠️ 提示；P1/P2/P5 页面级 ⚠️ 角标；登记 `客户决策清单跟踪表.md`（K-O30~K-O35 / Q010~Q018） | ✅ |
| 埋点携 user_level | 22 节点统一带 user_level | `observability.ts` `ENT_TRACK` 全事件 + `setUserLevel`；funnel 可分级 | ✅ |

**角色分级结论：通过。** RoleLevelGate 在 18+ 页面/组件广泛使用，能力门非阻断、矩阵落点与 userflow §0 一致。

> ⚠️ **一般缺陷（口径不一致）**：`RoleSwitch`/`RoleLevelGate` 中文标签为 `U1 公众访客 / U2 注册公众 / S1 内部经办 / S2 内部管理 / U3 生态·企业`，与 `ENT-userflow.md` §0 矩阵的 `U2 注册业务用户 / S1 领导驾驶舱用户 / S2 业务分析师 / U3 内容管理员` **展示文案不一致**（能力门 `allow` 逻辑与矩阵意图一致，仅文案需对齐）。建议由 ux/frontend 统一文案口径。
> 旁注：`Layout.tsx` 顶部另有一套全局 6 业务角色切换（驾/析/研/政/运/数），属既有专题级角色概念，与本期 ENT `user_level`（U1/U2/S1/S2/U3）为两套独立机制，非缺陷，但建议后续统一以免演示混淆。

---

## 6. D8 §14 检查清单 + 验收标准 逐条结果

> 真源：`Design.md` §14（「生成检查清单」8 条 + 「验收标准」10 条）。topic_demo 为原型沙箱，技术栈以 design-tokens + Arco + ECharts 落地，`design:check` 已机器校验 D8 契约。

### 6.1 生成检查清单（8 条）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 仍是浅蓝白科技工作台，非深色大屏 | ✅ | 页面底色浅色、克制风格；`design:check` 禁 forbidden 霓虹/深色模式 |
| 2 | 保留 Header / 左导航 / 主内容 / 主视图 / 右侧分析 | ✅ | `Layout`（app-sidebar + app-top-header + app-main）+ 各页右侧研判面板 |
| 3 | 选中态统一 `#165DFF` / `#E8F3FF` | ✅ | design-tokens `--sci-primary`；菜单 active、Tab 激活态统一 |
| 4 | 表单/按钮/分页/标签接近 Arco 节奏 | ✅ | 全 Arco（Button/Select/Cascader/Checkbox/Radio/Table/Tag/Drawer/Tooltip） |
| 5 | 地图工具栏/图例/筛选项尺寸克制 | ✅ | 控件 32px；地图为 Wave0 占位区块 |
| 6 | 有 loading/empty/disabled/error 状态 | ✅ | P2 未选企业 Empty 态、权重校验 disabled、Gate 锁态等 |
| 7 | 图表颜色遵循要素色/图表色序列 | ✅ | ECharts 统一 `EChart.tsx` 封装消费 design-tokens 色板 |
| 8 | 避免霓虹/紫蓝发光/营销 hero/emoji/无义占位 | ✅ | `design:check` 断言；🧪/⚠️ 用 Arco 图标（IconExperiment/IconExclamationCircle）非裸 emoji |

### 6.2 验收标准（10 条）

| # | 验收项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 首屏像「地图/图谱分析工作台」非卡片仪表盘 | ✅ | 工作台骨架（ContextBar + 主视图 + 右研判） |
| 2 | Header 高度接近 64px | ✅ | `app-top-header` 既有规格 |
| 3 | 左侧展开导航接近 200px | ✅ | `app-sidebar` 既有规格 |
| 4 | 表单/按钮/分页/工具栏高度接近 32px | ✅ | Arco size + tokens |
| 5 | 主色取样接近 `#165DFF` | ✅ | `--sci-primary` |
| 6 | 背景接近 `#D8E7FC`，无大面积深蓝/紫/黑 | ✅ | 浅色底；`design:check` 禁深色 |
| 7 | 普通卡片无强阴影、浮层阴影轻 | ✅ | `.sci-card` 白底 1px 边无阴影；Drawer 克制阴影 |
| 8 | 中央主视图面积 > 右侧分析面板 | ✅ | 各页主图区主导，右侧 SectionPanel 辅助 |
| 9 | 右侧分析面板存在 tabs/分组分析内容 | ✅ | SecondaryAnalysisTabs / SectionPanel |
| 10 | 依赖含 `@arco-design/web-react`，不只依赖 antd | ✅ | `package.json` 含 Arco；新页面零 antd 依赖 |

**D8 §14 结论：检查清单 8/8 ✅、验收标准 10/10 ✅。**（注：任务书所称「验收 6 条」对应 `Design.md` §14「验收标准」节，现行版本为 10 条，已逐条核验。）

---

## 7. D9 数据血缘自检

### 7.1 三件套到位

- **ⓘ MetricSpecCard**：`MetricCard` 内每个 metric_id 旁渲染 ⓘ（Arco Popover hover），展示 8 件套全字段（指标ID / 中文名 / 口径定义 / 计算公式 / 源表 / 源系统 / 更新频率 / 版本）+ 记 `metric_spec_view` 埋点。✅
- **🧪 MockBadge**：`is_mock=true` 时数字旁自动渲染 🧪（Arco Tooltip + IconExperiment），tooltip 含来源批次 + 替换计划（Wave 1）。当前 `metricSeed` 全部 `is_mock:true`，故所有 MetricCard 均带 🧪。✅
- **⚠️ 待甲方**：`pending_ref`（Q010~Q018）时 MetricSpecCard 内显示「口径待甲方确认（开放项 …），当前为团队临时默认值」；P1/P2/P5 另有页面级 ⚠️ 角标。✅

### 7.2 8 件套抽样核验（6 个 metric）

| metric_id | 中文名 | 8 件套齐全 | 命名规范 | is_mock | pending_ref | 承载页 |
|-----------|--------|:--------:|:-------:|:------:|:----------:|------|
| `M_ENT_SEARCH_RESULT_COUNT` | 检索命中企业数 | ✅ | ✅ | true | — | 检索工具条 |
| `M_ENT_COMPETITIVENESS_SCORE` | 综合竞争力得分 | ✅ | ✅ | true | Q014 | 卡片/画像/P10 |
| `M_ENT_TYPE_COUNT` | 各类型企业数 | ✅ | ✅ | true | Q010 | P1 |
| `M_ENT_DOMAIN_BREADTH` | 领域覆盖广度 | ✅ | ✅ | true | Q013 | P2 |
| `M_ENT_TOTAL_COUNT` | 企业总数 | ✅ | ✅ | true | — | 门户概况/全景 |
| `M_ENT_NODE_CENTRALITY` | 供应链中心性 | ✅ | ✅ | true | Q017 | P8 |

> `metricSeed.ts` 共收录 ~30 个 UI 实际引用 metric，全部含完整 8 件套（`metric_id`/`metric_name_zh`/`definition`/`formula`/`source_tables[]`/`source_systems[]`/`update_freq`/`version`），命名遵循 `M_ENT_*` 规则，源系统统一标 `Mock @ batch=mock_20260618`，并声明 ODS→DWD 血缘链（如 `dwd.enterprise.is_high_tech <- ods: dwd_org_tag_info`）。

### 7.3 四段链路核验（Wave 0 限制说明）

`data-lineage-policy.md` §7.6 要求 qa-agent 对 ≥5 个 metric 做「UI→API→ADS→DWD→ODS」四段链路核验。本期为 **Wave 0**：无 `/metrics/v1/catalog` / `/lineage` API、无真实 ADS/ODS 数据接入，metricSeed 为前端本地副本。故本期：
- ✅ 已核验：8 件套元数据完整性 + metric_id 命名 + 声明级血缘链（source_tables 引用真实 ODS/DWD 表名）+ ⓘ/🧪/⚠️ UI 表达。
- ⏭ 延后 Wave 1：真实四段链路实测（待 api-agent 上线 catalog/lineage + data-agent 接入真实源后执行，产出 `验收文档/数据血缘-链路核验-ENT.md`）。

**D9 结论：Wave 0 范围内通过；四段链路实测延后 Wave 1（非本期阻断）。**

---

## 8. 架构合规自检（公约 §2 十条·前端相关）

| # | 铁律 | 结论 | 说明 |
|---|------|------|------|
| 1 | 算法只在 Python | ✅ | 前端仅 Mock/展示；`smartParser`/`queryEngine` 标注 Wave1 迁 Python |
| 2 | 调用链不越层 | ✅ | Mock 阶段无直连；壳预留 Java→Python 替换点 |
| 3 | 图谱 NebulaGraph，禁 Neo4j | ✅ | 前端仅 ECharts graph 展示占位，未引 Neo4j；正式走 G6+NebulaGraph |
| 4 | 可观测性必加 | ✅ | `observability.ts` 全动作埋点 + user_level |
| 5 | CI/CD | ✅ | 原型仓，design:check/build 绿，无破坏 |
| 6 | demo2 只读 merge | ✅ | 仅 topic_demo 原型仓内变更，未涉 lumen |
| 7 | 前端只调 Java/共享聚合核心 | ✅ | 壳预留后端替换点，前端不写算法/不直连 nGQL |
| 8 | 标准表先行 + Mock | ✅ | metricSeed source_tables 引真实 ADS/DWD/ODS 表名，Wave1 零改动切真实 |
| 9 | 前端规范 D8 | ✅ | Arco + ECharts + design-tokens；`design:check` 通过 |
| 10 | 数据血缘 D9 | ✅ | ⓘ/🧪/⚠️ + 8 件套（§7） |

---

## 9. 缺陷 / 遗留清单（四档）

### 9.1 阻断（Blocker）
- **无。**

### 9.2 一般（Normal·建议本期或近期修）
| # | 缺陷 | 位置 | 建议 |
|---|------|------|------|
| N-1 | 角色中文标签口径与 userflow §0 不一致（S1/S2/U3） | `portalShared.tsx` `ROLE_OPTIONS` / `RoleLevelGate` `LEVEL_LABEL` | ux/frontend 统一为 userflow §0 文案（或反向更新 userflow，二选一对齐） |
| N-2 | 全局 6 业务角色切换 与 ENT user_level 两套机制并存 | `Layout.tsx` header | 评审前说明/统一，避免演示时角色概念混淆 |

### 9.3 Wave 1+ 延后（按分期，非本期阻断）
| # | 项 | 来源 handoff |
|---|----|-------------|
| W-1 | 地图三级下钻接 Leaflet GIS（当前 Wave0 占位区块 🧪） | FE-ENT-type-domain-pages §7 / FE-ENT-portal-pages §9 |
| W-2 | 关系/供应链图谱切 AntV G6 + NebulaGraph（当前 ECharts graph 占位） | FE-ENT-analysis-refactor §7 / FE-ENT-search-scaffold §2 |
| W-3 | 智能搜索 NL→DSL、评分/中心性等切 Python `/internal`；metric 改读 `/metrics/v1/catalog` | FE-ENT-search-scaffold §7 |
| W-4 | D9 四段链路实测（待 catalog/lineage API + 真实源） | 本报告 §7.3 |
| W-5 | SE-06 其他要素（政策/科研机构）检索范式 PoC 复用 | ENT-search-design §14（P2/Wave2） |
| W-6 | 孤儿文件 `ShenzhenEnterpriseIntroduction.tsx`（recharts/Tailwind，未路由，功能已由 `development/ShenzhenEnterprises.tsx` 承载）清理 | FE-ENT-analysis-refactor §7 |
| W-7 | chunk > 500kB 拆包优化（原型暂不处理） | FE-ENT-analysis-refactor §4 |

### 9.4 待甲方口径 🟡（上线前须升 🟢）
| # | 开放项 | 影响 | 现状处置 |
|---|--------|------|---------|
| Y-1 | Q010 企业类型 / 高企 / 专精特新判定阈值 | E-20/E-21 类型计数·占比 | 临时默认 + ⚠️ + pending_ref，登记决策表 |
| Y-2 | Q012 区划精度（国/省/市/区县下钻） | E-21 集聚指数 | 同上 |
| Y-3 | Q013 领域广度/深度/多元化公式 | E-22 | 同上 |
| Y-4 | Q014 技术力/商业力/竞争力评分权重 | E-23/E-24/E-30 | 同上 |
| Y-5 | Q015 招引/培育推荐指数阈值 | E-26/E-27 | 同上 |
| Y-6 | Q016 多城市对标城市集合 | E-25 | 同上 |
| Y-7 | Q017 供应链中心性/断链风险判定 | E-28 | 同上 |
| Y-8 | Q018 痛难点诊断维度集合 | E-29 | 同上 |
| Y-9 | K-O30~K-O35 用户级别划分/脱敏字段/导出配额/智能搜索词典 | 角色分级/检索 | 登记 userflow §5 + 客户决策清单 |

---

## 10. 截图证据

烟测截图由浏览器子代理生成，存放于：`C:\Users\hzw\AppData\Local\Temp\cursor\screenshots\`
- `search-drawer-enterprise-detail.png`（检索抽屉画像 + 在新窗口完整打开）
- `page-2026-06-19T09-53-22-163Z.png` / `…09-53-32-235Z.png`（P0 概览 ⓘ 指标卡）
- 其余各路由截图（overview / key-enterprises / star / shenzhen / type-distribution 三级下钻 / capability / 等）见同目录。

> 备注：临时目录截图非纳入仓库版本管理；如需归档，建议后续 coordinator 安排转存至 `agent-delivery/验收文档/截图/ENT/`。

---

## 11. 验收签署

- 验收角色：`qa-agent`（本报告仅为 AI 自动化验收证据，**最终验收以人评审 PM/UE/架构师签署为准**）。
- 验收范围声明：本报告**未修改任何 src 代码**，仅只读核验 + 跑 design:check/build + 浏览器烟测 + 文档产出。
- 阻断项：0；有条件通过，条件见 §0 / §9.2 / §9.4。
