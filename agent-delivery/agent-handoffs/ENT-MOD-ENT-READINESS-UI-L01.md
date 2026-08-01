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

## 3. 已知边界（存量问题，登记不掩盖）

| 边界 | 说明 | 收敛路径 |
|------|------|----------|
| KeyAnalysisV2 内联 meta | `EnterpriseKeyAnalysisV2Page` 用 `meta={...}` 绕过 metricSeed，就绪度角标不生效 | 改回 metricId 查 seed（另立小任务） |
| 风险主页硬编码 Q017/Q018 | `EnterpriseRiskInsightPage` 顶层 PendingBadge 未走 catalog（文案仍与 catalog 语义一致） | 换 `getEntGap` 驱动 |
| demo 本地 ID ≠ catalog ID | KEYPANO（M_ENT_KEYPANO_*）、STAR（demo 用 M_ENT_STAR_PATENT_COUNT/RD_RATIO，catalog 是 STAR_BY_INDUSTRY 等）无法对上 | 待王惠正式化统一 metric_id 后扩别名表或改页面 |
| 维护管理（OPS） | 产物为 capability 非统计指标，无矩阵条目 | 按 CMS 写侧能力另行管理 |

## 4. 架构合规自检（§2 十条）

1 算法只在 Python：不涉及 ✅ 2 调用链：纯 FE mock，无越层 ✅ 3 图谱：不涉及 ✅ 4 可观测：未动 observability.ts ✅ 5 CI/CD：demo 仓 push main 自动部署 ✅ 6 demo2 只读 merge：未 merge lumen ✅ 7 共享聚合核心：不涉及 ✅ 8 数据策略：Mock 先行 + 真源镜像 ✅ 9 D8 前端规范：Arco Icon、无 emoji 状态表达 ✅ 10 D9 血缘：本任务即其落地；每统计数字 ⓘ + 就绪度只读消费 + catalog 文案 ✅（D10 交互：角标键盘可达沿用既有组件 ✅）
