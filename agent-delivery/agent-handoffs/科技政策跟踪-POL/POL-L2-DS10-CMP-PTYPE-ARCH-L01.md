# POL-L2-DS10-CMP-PTYPE-ARCH-L01 · handoff

- 波次：CMP-PTYPE-FDE · B（架构定档与读法方案）
- 监管人：`human:淮政玮`（口径裁定见 QPOL-01 增补，2026-11-11）
- 强度：ponytail: full
- 上游：A 波次 `POL-L2-DS10-CMP-PTYPE-PROD-L01` 说明书 `#### 216`（已过 AV-1）

## 1. 范围与实现（功能点 → 架构落点）

| 216-PT | 架构决定 |
|---|---|
| PT-1 出数 | stats 同步读扩展 `policy_types` 块；`gkxlumen-element` 只读 DWD `policy_base_info`，`province × policy_type` GROUP BY 下推库端，`COUNT(DISTINCT policy_id)` 计件，Top 文种=件数多者（同数取字典序首个） |
| PT-2 🟡 角标 | 数据层不承载 UI 态；块内带 `caliber_note`（文种临时口径，QPOL-01），前端据此渲染角标，不自填就绪度 |
| PT-3 缺文种省 | 某省无文种行 → 条目缺席不造 0；`caliber_note` 不替代空态 |
| PT-4 218 交界 | 地区视角图以各省 Top 文种件数为量（同块数据，不进 `policy_intensity` Job）；政策视角无量保持空态 |

## 2. 读法定稿（二选一的裁定）

**选定 a) `stats` 同步读扩展块**，不选 b) `policy_intensity` Job 带出。理由：

1. 现行 216 力度就是 stats 同步读（ARCH §5.4 已签收口径）；政策类型同为对照展示列，同步读同一次请求带回，前端零新增任务触发点（I2-12）。
2. Job 链是力度分计算管道（`run()` 写 `ads.policy_intensity`），政策类型只是 GROUP BY 聚合，塞进 Job 徒增异步复杂度。
3. GROUP BY 下推库端，DWD 聚合量小，无性能顾虑（同 controller 既有 `INGEST_SQL` 直读 DWD 先例）。

链路不变：`前端 → display stats → element compare-stats → {dwd}.policy_base_info`。display 只透传 `policy_types` 块。

## 3. 边界（不做什么）

- 不建 gapfill 表、不写 ODS/ADS 新表、不加列（`policy_base_info.province/policy_type/policy_id` 均为既有列）。
- 不新造 `metric_id`：对照展示列 ≠ 新统计指标；`M_POLICY_TYPE_DIST`（全国文种分布，挂 QRY 统计）不被本列顶替、也不顶替本列。
- 不进 Job、不调用 Python、不在 Java 做内存聚合。
- 不改 `GDF-POLICY-MOCK-GATE-L01` 状态；D4 判定口径不变（读 DWD 真列非 mock 灌行）。
- QPOL-01 主口径（ODS 主题分类）不动，两者并行；甲方归一时切换只改该块 SELECT。

## 4. 定档

中档（数据源/读口变化）：读法方案 + API/DATA 分册修订 + 四角色会签。视觉零改动，不升高保真。

## 5. 架构合规自检（逐条）

| 铁律 | 结论 |
|---|---|
| D1 调用链 | ✅ 前端→display→element→DWD，不越层、不直连 Python、不进 Job |
| D5 可观测 | ✅ 沿 stats 既有 traceId 链，无新面 |
| D9 不伪闭合 | ✅ 缺文种省缺席不造 0；`caliber_note` 与 QPOL-01 同源；UI 🟡 不自填 |
| D12 demo/lumen 隔离 | ✅ 只读 lumen 侧 DWD，无 demo 资源 |
| D16 缺项边界 | ✅ 未建 `gapfill_` 表（DWD 有真列，不属缺项） |
| D18 可实现 | ✅ SQL GROUP BY 一条即可落地，现仓 `INGEST_SQL` 同表同读法先例 |
| 不新造 metric_id | ✅ 明确写进三份分册 |

## 6. 产物清单

- `sdd/l2/POL-L2-DS10-CMP-ARCH.md`：表头增补记录 + §2 表 216 行 + §5.4 增补段 + §5.6 交界段 + §8 表 216 行。
- `sdd/l2/POL-L2-DS10-CMP-API.md`：§1 表 216 行 + §2 委托表 stats 行 + 新增 §6.1 政策类型块 + §8 空态行 + §9 218 段。
- `sdd/l2/POL-L2-DS10-CMP-DATA.md`：§1 表 216 行 + §6 读法段。
- 本 handoff。

## 7. 偏离说明

无。A 波次已定第 3 条「走 stats 同步读扩展块」，本稿按此定稿。

## 8. 待下游

- C 波次会签：product（定义稿已过 AV-1）+ arch（本稿）双签，data/api 知会（DATA/API 分册修订已就绪随签生效）。
- D 波次：API-L01 按 §6.1 实现（element `policy_types` 块 + display 透传）→ FE-L01 接线 + 🟡 角标。

## 9. 验收证据

- 三份分册 diff（本 commit）；上游说明书 `#### 216`（commit `c732de1b`）。
- 现仓代码对照：`PolicyGapfillController.compareStats`（三块现状）、`INGEST_SQL`（DWD 直读先例）、`PolicyPanoramaService.statsBody`（透传位）。

## Cost 回填

- actual_tokens ≈ 30000；model_used: glm-5.3-flash；actual_cost: 0.15（估算）；cost_warn: green
