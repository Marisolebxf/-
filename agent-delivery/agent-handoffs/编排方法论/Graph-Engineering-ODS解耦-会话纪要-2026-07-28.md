# 会话纪要：Graph Engineering 编排落地 + ODS/DWD 解耦策略

> **日期**：2026-07-28  
> **参与**：项目负责人 + AI agent  
> **范围**：多智能体协作方法论（Graph Engineering）在 GKX 编排体系中的落地；三方数据源风险下的血缘域定位；ODS/DWD 解耦决策固化  
> **状态**：规约与模板已落盘并 push（本纪要随同提交）

---

## 1. 议题脉络

1. **Graph Engineering 澄清**：非 Nebula 图工程，而是继 Loop Engineering 之后的**多智能体协作方法论**（拓扑编排：扇出/汇聚、层级委派等）。
2. **两种图模式如何在本项目加强**：Fan-out/Fan-in、Hierarchical Delegation。
3. **并发误解纠正**：本地并发 ≤4 = **人类监管人**同时盯的 agent 会话上限；**不是** coordinator 派单上限。
4. **子协调域扩展**：在原有平台/数据算法/交互/质量域基础上，新增**指标定义域**、**文档编写域**；并讨论是否新建**数据血缘域**。
5. **关键背景决策（项目负责人）**：甲方供应库 `dwd_*` 实质是本项目 **ODS**；项目自研 DWD 由架构师按需求设计、**不与 ODS 一一对应**；8/20 左右 ODS 稳定后再由 **GDF** 做映射。

---

## 2. 关键决策

### 2.1 监管并发 vs 派单并发

| 约束 | 本意 | 适用对象 |
|------|------|----------|
| 本地并发 ≤4 | 一名人类监管人同时监管的 agent ≤4 | 执行层 worker |
| coordinator 派单 | **无此上限** | coordinator（不写代码） |

派单时按 `team-roster.yaml` 的监管人容量分摊 `supervised_by`。

### 2.2 子协调域模型（修订稿）

```
coordinator
├── platform-subcoord      (平台基建：devops / api / integration)
├── data-algo-subcoord     (数据算法：data / algorithm) —— 产数据
├── lineage-subcoord       (数据血缘) —— 诊断/治理，前置闸门
├── metric-subcoord        (指标定义) —— 定口径；横切消费 lineage
├── ui-subcoord            (交互交付：ux / ui / frontend)
├── assurance-subcoord     (质量保障：qa)
└── doc-subcoord           (文档编写：doc) —— Epic 末尾 fan-in
```

### 2.3 lineage-subcoord：不归 data-algo，也不归 metric —— 独立成域

| 概念 | 粒度 | 说明 |
|------|------|------|
| A. 表级血缘 | ODS 字段 ↔ 项目 DWD | 结构性风险；先于指标定义 |
| B. 指标级血缘 | metric 8 件套 | D9 规约主战场；依赖 A |

独立成域的原因：时序前置、横切供水（data-algo / metric / ui / qa / PM）、风险升级直通甲方决策清单。

### 2.4 ODS/DWD 解耦（项目负责人拍板）

```
甲方供应层（不稳定，~8/20 定稿）
  MySQL gkx 库 dwd_* 表  =  本项目 ODS
        │  ← 现悬空；稳定后由 GDF 接
项目设计层（现在可全速推进）
  架构师自研 DWD → DWS → ADS
```

- Phase 1（现在 ~ 8/20）：治理**项目自研 DWD**；不做 ODS→DWD 映射；`mapping_status: ⏳ pending_ods`
- Phase 2（8/20 后）：GDF 映射 → lineage 验证 → 升级 `⏳→✅/❌`

连接真源：`data/third-party-source/gkx-mysql-raw/CONNECTION.md`（密码仅 `.env.local`）。

---

## 3. 本会话落盘产物

| 文件 | 内容 |
|------|------|
| `agent-delivery/data-lineage-policy.md` v1.2 | §2.2 状态机；Phase 1/2；§5.1.5 OdsPendingBadge；路线图按 Phase 改写 |
| `agent-delivery/Design.md` §7.4.1 | 四角标互斥：⏳ > ⚠️ > 🧪 > ⓘ |
| `agent-delivery/data/README.md` | 解耦说明 + Phase 对照表 |
| `agent-delivery/data/data-design/_templates/dwd-table-contract-template.md` | 单表契约模板（含 `ods_mapping_expectation`） |
| `agent-delivery/data/data-design/_templates/README.md` | 模板用法 |

**未纳入本次提交**（无关或临时文件）：`designs/houtai-arch-discussion.md`、`designs/tech-stack-*.md`、`scripts/_tmp_lease_check.mjs`。

---

## 4. 后续待办（未在本会话执行）

1. ~~将 7 域模型写入 `智能体编排与派单手册.md` + 修订 `coordinator.mdc` 派单铁律（澄清 ≤4 含义）~~ → **2026-07-28 B0 已落盘**（手册 §十三.1 + §十六；`coordinator.mdc`）
2. ~~`team-roster.yaml` 增加监管人容量可查询字段；可选 `find-supervisor-slot.ps1`~~ → **2026-07-28 B1 已落盘**（`capacity_policy` + `scripts/find-supervisor-slot.mjs` + `recover-expired-leases.mjs`）
3. ~~`task-registry` 增加 `subcoord` / `graph.role` / `ods_dependency_phase` 元数据~~ → **2026-07-28 B2 已落盘**（`graph_engineering_policy`；字段名 `graph_role`）
4. 架构师用契约模板先填 1～2 张样板表（企业主表 / 项目主表）
5. metric-subcoord 将现有指标 `mapping_status` 统一标 `⏳`（Phase 1）
6. ui-agent 实现 ⏳ OdsPendingBadge（Design.md 已定义）
7. 正式 registry task 认领与监管人留痕（本会话文档改动尚未挂 task-id）
8. （B 类后续）`touched_files` + Convoy 自动检测；coordinator 自治循环；Refinery 合并队列

---

## 5. 一句话结论

> Graph Engineering 在本项目的落地抓手是**显式拓扑（fan-out/fan-in + 层级子协调域）**；三方源风险下应独立 **lineage-subcoord**，并按负责人决策把**项目 DWD 设计与甲方 ODS 供应解耦**——8/20 前全速自研 DWD + `⏳`，之后 GDF 映射再升级血缘状态。
