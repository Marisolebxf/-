# 企业要素全集落地 topic_demo · 交付总册（as-built）

> 角色：doc-agent（WP5 收尾，因子代理 resource_exhausted 由 coordinator 手工接管完成）
> 范围：企业要素 **E-20~E-37** 两层模型落地 topic_demo（门户层 + 分析层 + 检索工作台 + 统一企业画像 + 角色分级）
> 分支：`topic_demo @ feat/ent-elements-build`（**未 push**）；外层文档仓 `E:/gkx_src @ main`
> 验收结论：**有条件通过（PASS WITH CONDITIONS）· 阻断项 0**（详见 `QA-ENT-acceptance-report.md`）

---

## 1. 范围与实现（对照 catalog-topic-enterprise.yaml / bid-reference）

| 分层 | 验收点 | 前端落地 | 说明 |
|------|--------|---------|------|
| 分析层 | E-20~E-30（11 项 / 10 个三级子功能） | ✅ 全部 | P0 概述 + P1 类型 + P2 领域 + P3 能力(E-23/24) + P5 现状 + P6 引育(E-26/27) + P8 供应链 + P9 痛难点 + P10 竞争力 |
| 门户层 | E-31~E-35（5 项） | ✅ 全部 | 企业发展概况 + 检索工作台 + 重点企业全景图 + 明星企业 + 深圳企业 + 统一企业画像 |
| 后台能力 | E-36/E-37 + E-01~E-19 多数 | ⏸ 预留 | 内容管理 / 指标模型 / 数据采集等属后台能力或模型层，非前端原型范围，catalog route 保持 null 并标注 |

- bid 的 10 个三级子功能 **1:1 全覆盖，不增不减**；`.3.3+.3.4`、`.3.6+.3.7` 为"页面合并 Tab 承载"（叶子功能点数量不变），符合 ±10% 铁律。
- 检索工作台与统一企业画像是 E-31/E-32/E-33 的**载体与交互范式**，不新增叶子功能点；体验维度以 `SE-01~06` 跟踪。

---

## 2. as-built 路由表（路由 ↔ 页面 ↔ E-XX ↔ 角色可见性）

### 2.1 门户层 `/development/*`（集群服务·企业发展）

| 路由 | 页面组件 | E-XX | 角色可见性 |
|------|---------|------|-----------|
| `/development/overview` | DevelopmentOverview | E-31/E-32 | U1/U2/S1/S2 |
| `/development/search` | SearchPage（SearchScaffold+enterpriseSearchConfig） | E-31 入口核心 / SE-01~06 | U1🔸 / U2/S1/S2 |
| `/development/enterprise/:enterpriseCode` | EnterpriseProfilePage（统一画像整页） | DR-04 / E-33 触点 | U1 脱敏 / U2/S1/S2 |
| `/development/key-enterprises` | KeyEnterprisesPanorama | E-33 | U1 看 / U2/S1/S2 |
| `/development/star-enterprises` | StarEnterprises | E-34 | U1 看 / U2/S1/S2 |
| `/development/shenzhen` | ShenzhenEnterprises | E-35 | U1 看 / U2/S1/S2 |

### 2.2 分析层 `/enterprise/*`（战略分析·企业分析）

| 路由 | 页面组件 | E-XX | bid 章节 |
|------|---------|------|---------|
| `/enterprise/overview` | EnterpriseOverview（P0 战略驾驶舱） | E-20 | §1.1.1.2.4.2.3 |
| `/enterprise/type-distribution` | EnterpriseTypeDistribution（P1） | E-21 | .3.1 |
| `/enterprise/domain-distribution` | EnterpriseDomainDistribution（P2） | E-22 | .3.2 |
| `/enterprise/capability` | EnterpriseCapabilityEvaluation（P3） | E-23/E-24 | .3.3/.3.4 |
| `/enterprise/status-analysis` | EnterpriseStatusAnalysis（P5） | E-25 | .3.5 |
| `/enterprise/recommendation` | EnterpriseRecommendation（P6） | E-26/E-27 | .3.6/.3.7 |
| `/enterprise/supply-chain` | SupplyChainAnalysis（P8） | E-28 | .3.8 |
| `/enterprise/pain-points` | PainPointsAnalysis（P9） | E-29 | .3.9 |
| `/enterprise/competitiveness` | CompetitivenessAnalysis（P10） | E-30 | .3.10 |

> 统一画像（DR-04）抽屉态/整页态同源（`ElementProfile` 的 `mode`），两层共享同画像同数据；跨层带参：概况下钻 P1/P2、门户"深度分析"带 `enterprise_code` 高亮、检索带 `?mode=&q=`。

---

## 3. 技术栈 as-built（重要澄清）

- **权威栈 = Arco Design + ECharts + design-tokens（Tailwind v4 任意值消费 CSS 变量）**。
- ⚠️ **栈口径澄清**：派单初期曾把"维持现栈"误判为 Tailwind+recharts 并下达"禁止 Arco"。经核实 `topic_demo` 实际**已内置 `@arco-design/web-react` + `echarts`**，`App.tsx` 用 Arco `ConfigProvider`，且 `scripts/check-design-contract.mjs`（`npm run design:check`）**强制 Arco**，与团队公约 D8 一致。故"维持现栈"真实指向即 Arco，**非新决策**；已在 WP3a 阶段纠正，全部前端按 Arco+ECharts 落地。
- 全程**未改** `package.json`/`vite.config.ts`/`.gitignore`/tailwind 配置；无新增依赖。

---

## 4. 各 WP 产物清单与提交基线（均未 push）

### 4.1 topic_demo `feat/ent-elements-build`

| commit | WP | 内容 |
|--------|----|------|
| `23be412` | WP2 ui | design-tokens.css + README-tokens.md + ENT-ui-spec.md + index.css(@import) |
| `47a0a67` | WP1 ux | ENT-IA / userflow / wireframe / gap + 主设计 / 检索设计 8 份文档收口 |
| `fd4d419` | WP3a fe | 通用检索范式 SearchScaffold 基础层（common 件 + search 壳 + mock + observability，Arco+ECharts） |
| `d539829` | WP3b fe | 门户层 5 页 + 路由 + 侧边栏 + 整页/抽屉同源画像 |
| `088781e` | WP3c fe | 分析层 8 页按 FDS v2 重构（recharts→ECharts）+ 跨层带参 + S1/S2 分级 |
| `7aa5c88` | WP3d fe | 修偏离：E-21/E-22 改回独立页 + 2 路由 + 2 侧边栏入口 |

### 4.2 外层仓 `E:/gkx_src @ main`

| commit | 内容 |
|--------|------|
| `2a36bf9` | FE-ENT-search-scaffold handoff（WP3a） |
| `8663cdb` | UX/UI handoff 收口（UX-ENT-ia-wireframe-gap + UI-ENT-tokens-spec） |
| `7a2b256` | FE-ENT-analysis-refactor handoff（WP3c） |
| `bc25dc2` | QA-ENT-acceptance-report（WP4） |
| 本次 doc | FE-ENT-portal-pages + FE-ENT-type-domain-pages handoff 归集 + 本总册 + catalog route 回填 |

---

## 5. 验收证据（摘自 QA-ENT-acceptance-report.md）

- 门禁：`design:check` 通过 + `build` exit 0（每个前端 WP 完工均复跑通过）。
- 路由可达：核心路由 15/15（100%），无白屏/控制台报错，侧边栏菜单齐全。
- E-20~E-35 前端可验收 **16/16 全通过**；E-21/E-22 已确认独立页；E-30 去重完成；E-36/E-37 标注后台能力。
- 检索体验 SE-01~06：通过 5 + 部分 1（SE-06 通用范式仅企业 config 落地，属 Wave2）。
- 角色分级 U1/U2/S1/S2：RoleLevelGate 非阻断、能力矩阵落点正确、⚠️ 待甲方角标就位。
- D8 §14 检查清单 8/8 + 验收标准 10/10 全绿。
- D9 血缘：抽样 6 个 metric 8 件套齐全、ⓘ/🧪/⚠️ 到位（四段链路实测受 Wave 0 限制延后 Wave 1）。

---

## 6. 架构合规自检（公约 §2 十条 · 前端相关项）

| 铁律 | 结论 |
|------|------|
| ① 算法只在 Python | ✅ 前端无算法，NL→DSL 解析为前端 mock 占位（Wave1 接后端） |
| ② 调用链不越层 | ✅ 前端只消费 mock/约定接口，未直连 nGQL/Python |
| ③ 图谱 NebulaGraph | ✅ 前端仅 ECharts 力导向渲染，不涉图库选型 |
| ④ 可观测性 | ✅ `lib/observability.ts` 埋点（22 节点 + user_level） |
| ⑤ CI/CD | ⏸ 设计/原型阶段，分支未 push（见 §7 待人类决策） |
| ⑥ demo2 只读 merge | ✅ 不涉及 |
| ⑦ 共享聚合核心 | ✅ 前端只调既定层 |
| ⑧ 数据策略 ADS+Mock | ✅ Wave 0 全 Mock + 🧪 MockBadge |
| ⑨ 前端规范唯一来源 D8 | ✅ Arco+ECharts+design-tokens，design:check 通过 |
| ⑩ 数据血缘 D9 | ✅ metric 8 件套 + ⓘ/🧪/⚠️ |

---

## 7. 偏离与修正记录

1. **栈口径**：误判 Tailwind+recharts → 核实并纠正为 Arco+ECharts（仓库现状 + D8 + design:check 三方一致）。WP3a 即时纠偏，无遗留。
2. **E-21/E-22 归位**：WP3c 一度并入 P0「结构洞察」Tab（未授权合并）→ WP3d 按权威 IA §2.2/§3.2 改回**独立页 + 独立路由 + 侧边栏入口**，并对 EnterpriseOverview 做减法去重。

---

## 8. 遗留与后续（非阻断）

- **Wave1+**：真实数据接入（替换 Mock）、地图三级下钻接 Leaflet、供应链 G6/权重后端、检索 NL→DSL 真实解析、跨层带参真实落参。
- **SE-06**：通用要素检索范式壳已就位，仅企业 config 落地；政策/科研/服务要素 config 属 Wave2 复用扩展。
- **清理项**：孤儿文件 `topic_demo/src/app/pages/development/ShenzhenEnterpriseIntroduction.tsx`（E-35 已由 `ShenzhenEnterprises` 承载）建议后续移除。
- **截图归档**：QA 烟测截图存于临时目录未持久化到仓库；如需归档需重跑烟测留证（已建空目录 `agent-delivery/验收文档/截图/ENT/`）。

---

## 9. 待人类决策清单（PM / 架构师）

1. **分支 push / PR**：`feat/ent-elements-build` 6 个提交均未 push；是否推送 + 走 PR 评审由人类按公约 §4.2 决策。
2. **RoleSwitch 文案口径对齐**（QA 一般缺陷）：分析层 `RoleSwitch` 标签（S1=内部经办 / S2=内部管理 / U3=生态·企业）与 `ENT-userflow.md` §0（领导驾驶舱 / 业务分析师 / 内容管理员）文案不一致——涉及"分析层级别命名"与"全局外壳角色命名"的口径取舍，需 UX/PM 统一后由 frontend-agent 改文案（逻辑无误）。
3. **待甲方业务口径 🟡**：`客户决策清单跟踪表.md` §2.4 已登记 **Q010~Q019**（企业类型判定 / 创新型口径 / 区划精度 / 覆盖广度深度 / 各力指标权重 / 招引培育阈值 / 多城市集合 / 供应链风险规则 / 痛难点维度 / 市场份额无源），均以临时默认值 + ⚠️ 运行，上线前须甲方书面确认升 🟢。无需新增登记项。
