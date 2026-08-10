# ENT-MOD-ENT-READINESS-UI-L01 — demo-ui-topic 四维就绪度刷新扩到企业维度全部菜单

> 状态：🔍 review（2026-08-01）· agent:frontend-agent · 监管 human:淮政玮
> 依赖：ENT-READINESS-MATRIX-ENT-L01（企业全域矩阵真源）
> 用户约束：**只动企业维度菜单**；技术链/产业链/科研/人才/政策/服务链等不受影响。

## 1. 实现方式（共享封装一次改对，企业页零散改动最小化）

| 层 | 文件 | 变更 |
|----|------|------|
| 数据 | `src/app/mock/enterprise/readinessSeed.ts` | 13 → **32 条**（EVAL 13 + SEARCH/RISK/RECRUIT/SHENZHEN 19）；`SchemaStatus` 增 `pending`；`METRIC_ID_ALIASES` 别名解析（M_ENT_DOMAIN_BREADTH→M_ENT_DOMAIN_COVERAGE_BREADTH）；真源指向 `metric-readiness-matrix-ENT.yaml` |
| 数据 | `src/app/mock/enterprise/entGapCatalog.ts`（新建） | SEARCH/RISK/RECRUIT/SHENZHEN 四模块缺口镜像 **18 条**；`getEntGap()` 模块优先 → EVAL 回落 → 别名解析 |
| 组件 | `MetricCard.tsx` / `ReviewMetricBadges.tsx` | 挂 `SchemaGapBadge` + `IngestingBadge`（自闸，无数据不渲染）；⚠️ 文案改读 `getEntGap`（catalog 真源，不硬编码）；排列改 D9 并存顺序 **数字→ⓘ→结构→⚠️→🧪/⟳** |
| 组件 | `MetricSpecCard.tsx` | 就绪度区块支持 D2 `pending` → 蓝色时钟「结构支撑待评估」 |
| 测试 | `tests/enterprise-eval-readiness.test.mjs` | 扩企业全域断言：32 条覆盖 / pending 诚实性 / 别名 / 聚合镜像与 4 份模块 catalog 弱一致 / 共享封装挂角标 / 矩阵真源改 ENT.yaml |

**页面覆盖机制**：企业各页（总览/明星/深圳介绍/风险结果页/引育/深圳现状等）已通过 `MetricCard` / `ReviewMetricBadges` / `MetricSpecCard` 消费 metricId，本次改封装后自动获得四维角标与 catalog 文案，页面文件零改动。

## 2. 验收证据

- `node --experimental-strip-types tests/enterprise-eval-readiness.test.mjs` → **PASS**（Enterprise readiness contract (ENT-wide) passed）
- 全量 tests 批跑：本任务相关（readiness / review-marker-self-gating / overview-e33-e35 / risk-definition / recruit-definition / mount 相关）全绿；其余 FAIL 均为存量问题（多为 *-pointer 系列 + `enterprise-review-mount-contract` 依赖编排仓缺失文件 `交付覆盖/ENT-RISK/implementation-coverage.yaml`），与本次变更无关
- 评审模式关闭时零泄漏：全部角标经 `ReviewOnly` 自闸（review-marker-self-gating PASS）

## 2.1 评审反馈修复（2026-08-01，监管人现场走查 · commit `9f184be`）

监管人走查发现两类问题，已修复并推 `origin/dev`：

| 反馈 | 根因 | 修复 |
|------|------|------|
| 评估页「技术人才/技术创新」等标题与 ⓘ 卡片对不上 | 技术力五维/商业力六维/竞争力三域是**评分维度**，无独立 metric_id，`enterpriseEvaluationModel.ts` 直接挂了父综合指标（或代理指标），卡片显示的是父指标 8 件套 | 指标定义增加 `metricRelation: { kind: 'dimension'\|'proxy', metricLabel }`；抽屉「内部指标元数据」块先显式声明「本条是『技术力综合评分』的评分维度，暂无独立 metric_id（维度级指标待 Q014 闭合）」再展示卡片，不再冒充本体 |
| Q018 等开放项编号对人不可读 | PendingBadge / 就绪度行 / 语义卡横幅只显示裸编号 | 新建 `openItemCatalog.ts`（Q010~Q058 + GAP-SZSTATUS 标题字典，镜像 `客户决策清单跟踪表.md`），统一渲染为「Q018 · 痛难点诊断维度与阈值（依赖专家知识库）」；长文案 Popover 加「开放项：…」行 |
| （附带）痛难点卡片未体现「融资」维诊断方法 | `metricSeed` 口径定义只写了维度集合，Wave0 判定规则在 gap catalog 里未上卡 | `M_ENT_PAINPOINT_COUNT` 口径定义补 Wave0 临时判定规则（研发投入下降→技术研发 / 营收下降→市场拓展 / **融资轮次停滞→融资**），并诚实标注人才/管理/政策维暂无规则待 Q018 |

契约测试新增：① 字典内全部 Q 编号必须存在于跟踪表真源（防 FE 自编语义）；② 共用综合 metricId 的评估行必须声明 `metricRelation=dimension`。测试 PASS。

## 3. 已知边界（存量问题，登记不掩盖）

| 边界 | 说明 | 收敛路径 |
|------|------|----------|
| KeyAnalysisV2 内联 meta | `EnterpriseKeyAnalysisV2Page` 用 `meta={...}` 绕过 metricSeed，就绪度角标不生效 | 改回 metricId 查 seed（另立小任务） |
| 风险主页硬编码 Q017/Q018 | `EnterpriseRiskInsightPage` 顶层 PendingBadge 未走 catalog（文案仍与 catalog 语义一致） | 换 `getEntGap` 驱动 |
| demo 本地 ID ≠ catalog ID | KEYPANO（M_ENT_KEYPANO_*）、STAR（demo 用 M_ENT_STAR_PATENT_COUNT/RD_RATIO，catalog 是 STAR_BY_INDUSTRY 等）无法对上 | 待王惠正式化统一 metric_id 后扩别名表或改页面 |
| 维护管理（OPS） | 产物为 capability 非统计指标，无矩阵条目 | 按 CMS 写侧能力另行管理 |

## 4. 架构合规自检（§2 十条）

1 算法只在 Python：不涉及 ✅ 2 调用链：纯 FE mock，无越层 ✅ 3 图谱：不涉及 ✅ 4 可观测：未动 observability.ts ✅ 5 CI/CD：demo 仓 push main 自动部署 ✅ 6 demo2 只读 merge：未 merge lumen ✅ 7 共享聚合核心：不涉及 ✅ 8 数据策略：Mock 先行 + 真源镜像 ✅ 9 D8 前端规范：Arco Icon、无 emoji 状态表达 ✅ 10 D9 血缘：本任务即其落地；每统计数字 ⓘ + 就绪度只读消费 + catalog 文案 ✅（D10 交互：角标键盘可达沿用既有组件 ✅）
