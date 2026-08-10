# ORPHAN-MD-P3 — 根目录 handoff 归集

> 日期：2026-08-10  
> 执行：`agent:coordinator`  
> 分支：`cursor/orphan-md-p0-p1-3405`  
> 用户确认：对根目录 md 分析后同意执行 P3 归集

## 1. 范围与实现

- `git mv` **82** 个根目录 handoff → 业务子目录
- 根目录现仅保留 `README.md`（符合 README §「只保留 README」）
- 新建目录：`科技新闻-TECH-NEWS/`、`高端智库-ZHIKU/`、`展示对齐-DISPLAY/`、`综合智能分析-SYNTH/`
- 更新 `agent-handoffs/README.md` 子目录索引与归集表

## 2. 未改

- **未改** `task-registry.yaml`（须 MCP）。旧简写 `agent-handoffs/<file>.md` 在迁入子目录后失效，需批量改 `handoff`/`evidence` 为完整子路径。
- 未再归档；本批均为有 registry 关联的正式 handoff。

## 3. 路径对照（from → to）

| from | to |
|---|---|
| `agent-handoffs/E-TECH-NEWS-ENTITY-M2-L01.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M2-L01.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M2-L02.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M2-L02.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M2-L03.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M2-L03.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M3-L01.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M3-L01.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M3-L02.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M3-L02.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M3-L03.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M3-L03.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M4-L01.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M4-L01.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M4-L02.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M4-L02.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-M4-L03.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-M4-L03.md` |
| `agent-handoffs/E-TECH-NEWS-ENTITY-PDR-L01.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-ENTITY-PDR-L01.md` |
| `agent-handoffs/E-TECH-NEWS-IE-M1-L01.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-IE-M1-L01.md` |
| `agent-handoffs/E-TECH-NEWS-IE-M1-L02.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-IE-M1-L02.md` |
| `agent-handoffs/E-TECH-NEWS-IE-M1-L03.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-IE-M1-L03.md` |
| `agent-handoffs/E-TECH-NEWS-IE-M1-L04.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-IE-M1-L04.md` |
| `agent-handoffs/E-TECH-NEWS-IE-M1-L05.md` | `agent-handoffs/科技新闻-TECH-NEWS/E-TECH-NEWS-IE-M1-L05.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-R1.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R1.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-R2.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R2.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-R3.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R3.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-R4.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R4.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-R5.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R5.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-R6.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-R6.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S0.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S0.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S1.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S1.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S2.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S2.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S3.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S3.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S4.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S4.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S5.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S5.md` |
| `agent-handoffs/E-ZHIKU-PROTOTYPE-110-S6.md` | `agent-handoffs/高端智库-ZHIKU/E-ZHIKU-PROTOTYPE-110-S6.md` |
| `agent-handoffs/FE-DISPLAY-ACHIEVE-ALIGN-L01.md` | `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-ACHIEVE-ALIGN-L01.md` |
| `agent-handoffs/FE-DISPLAY-GI-TOPBAR-OVERLAY-L01.md` | `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-GI-TOPBAR-OVERLAY-L01.md` |
| `agent-handoffs/FE-DISPLAY-KG-SERVICE-ALIGN-L01.md` | `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-KG-SERVICE-ALIGN-L01.md` |
| `agent-handoffs/FE-DISPLAY-SVC-ECO-ALIGN-L01.md` | `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-SVC-ECO-ALIGN-L01.md` |
| `agent-handoffs/FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01.md` | `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-TECHINDEX-MOCK-ALGO-L01.md` |
| `agent-handoffs/FE-DISPLAY-TECHINDEX-NEW-L01.md` | `agent-handoffs/展示对齐-DISPLAY/FE-DISPLAY-TECHINDEX-NEW-L01.md` |
| `agent-handoffs/ENT-MOD-ENT-READINESS-UI-L01.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-ENT-READINESS-UI-L01.md` |
| `agent-handoffs/ENT-MOD-ENT-READINESS-UI-L02.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-ENT-READINESS-UI-L02.md` |
| `agent-handoffs/ENT-MOD-EVAL-READINESS-UI-L01.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-EVAL-READINESS-UI-L01.md` |
| `agent-handoffs/ENT-MOD-EVAL-TEST-TRIAGE-L01.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-EVAL-TEST-TRIAGE-L01.md` |
| `agent-handoffs/ENT-MOD-OPS-PACK-L01.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-OPS-PACK-L01.md` |
| `agent-handoffs/ENT-MOD-OPS-UX-L01.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-OPS-UX-L01.md` |
| `agent-handoffs/ENT-MOD-OPS-V1-HIFI.md` | `agent-handoffs/企业战略分析-ENT/ENT-MOD-OPS-V1-HIFI.md` |
| `agent-handoffs/ENT-READINESS-MATRIX-ENT-L01.md` | `agent-handoffs/企业战略分析-ENT/ENT-READINESS-MATRIX-ENT-L01.md` |
| `agent-handoffs/ENT-READINESS-MATRIX-ENT-L02.md` | `agent-handoffs/企业战略分析-ENT/ENT-READINESS-MATRIX-ENT-L02.md` |
| `agent-handoffs/E-ENT-KEYENT-JAVA-L01.md` | `agent-handoffs/企业战略分析-ENT/E-ENT-KEYENT-JAVA-L01.md` |
| `agent-handoffs/E-ENT-KEYENT-PY-L01.md` | `agent-handoffs/企业战略分析-ENT/E-ENT-KEYENT-PY-L01.md` |
| `agent-handoffs/E-ENT-KEYENT-SZSTATUS-DISPATCH.md` | `agent-handoffs/企业战略分析-ENT/E-ENT-KEYENT-SZSTATUS-DISPATCH.md` |
| `agent-handoffs/E-ENT-SZSTATUS-PY-L01.md` | `agent-handoffs/企业战略分析-ENT/E-ENT-SZSTATUS-PY-L01.md` |
| `agent-handoffs/ARCH-ENT-PY-LUMEN-ALGO-ADAPT-L01.md` | `agent-handoffs/企业战略分析-ENT/ARCH-ENT-PY-LUMEN-ALGO-ADAPT-L01.md` |
| `agent-handoffs/CHAIN-OPS-PACK-DEMO-L01.md` | `agent-handoffs/产业链分析-CHAIN/CHAIN-OPS-PACK-DEMO-L01.md` |
| `agent-handoffs/TOPIC-SVCCHAIN-ALIGN-L01.md` | `agent-handoffs/产业链分析-CHAIN/TOPIC-SVCCHAIN-ALIGN-L01.md` |
| `agent-handoffs/TOPIC-SVCCHAIN-ALIGN-L02.md` | `agent-handoffs/产业链分析-CHAIN/TOPIC-SVCCHAIN-ALIGN-L02.md` |
| `agent-handoffs/TOPIC-SVCCHAIN-R1.md` | `agent-handoffs/产业链分析-CHAIN/TOPIC-SVCCHAIN-R1.md` |
| `agent-handoffs/TOPIC-SVCCHAIN-R2.md` | `agent-handoffs/产业链分析-CHAIN/TOPIC-SVCCHAIN-R2.md` |
| `agent-handoffs/TOPIC-SVCCHAIN-R2C.md` | `agent-handoffs/产业链分析-CHAIN/TOPIC-SVCCHAIN-R2C.md` |
| `agent-handoffs/TOPIC-SYNTH-R3.md` | `agent-handoffs/综合智能分析-SYNTH/TOPIC-SYNTH-R3.md` |
| `agent-handoffs/TOPIC-STRAT-R4.md` | `agent-handoffs/综合智能分析-SYNTH/TOPIC-STRAT-R4.md` |
| `agent-handoffs/SYNTH-MOD-COLLAB-PACK-L01.md` | `agent-handoffs/综合智能分析-SYNTH/SYNTH-MOD-COLLAB-PACK-L01.md` |
| `agent-handoffs/SYNTH-MOD-COLLAB-V1-HIFI.md` | `agent-handoffs/综合智能分析-SYNTH/SYNTH-MOD-COLLAB-V1-HIFI.md` |
| `agent-handoffs/SYNTH-MOD-ELEMENT-PACK-L01.md` | `agent-handoffs/综合智能分析-SYNTH/SYNTH-MOD-ELEMENT-PACK-L01.md` |
| `agent-handoffs/SYNTH-MOD-ELEMENT-V1-HIFI.md` | `agent-handoffs/综合智能分析-SYNTH/SYNTH-MOD-ELEMENT-V1-HIFI.md` |
| `agent-handoffs/SYNTH-MOD-VITALITY-PACK-L01.md` | `agent-handoffs/综合智能分析-SYNTH/SYNTH-MOD-VITALITY-PACK-L01.md` |
| `agent-handoffs/SYNTH-MOD-VITALITY-V1-HIFI.md` | `agent-handoffs/综合智能分析-SYNTH/SYNTH-MOD-VITALITY-V1-HIFI.md` |
| `agent-handoffs/POLICY-METRIC-OPEN-L01.md` | `agent-handoffs/政策模块-E7/POLICY-METRIC-OPEN-L01.md` |
| `agent-handoffs/POLICY-PACK-L01.md` | `agent-handoffs/政策模块-E7/POLICY-PACK-L01.md` |
| `agent-handoffs/POLICY-UX-L01.md` | `agent-handoffs/政策模块-E7/POLICY-UX-L01.md` |
| `agent-handoffs/DS10-12-PACK-L01.md` | `agent-handoffs/政策模块-E7/DS10-12-PACK-L01.md` |
| `agent-handoffs/DS10-12-V1-HIFI-L01.md` | `agent-handoffs/政策模块-E7/DS10-12-V1-HIFI-L01.md` |
| `agent-handoffs/DS10-SEARCH-REUSE-L01.md` | `agent-handoffs/政策模块-E7/DS10-SEARCH-REUSE-L01.md` |
| `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01.md` | `agent-handoffs/算法库联调-ALGO-LIB/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01.md` |
| `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01-audit.md` | `agent-handoffs/算法库联调-ALGO-LIB/FIX-TOPIC-SEARCH-PY-DWD-PREFIX-L01-audit.md` |
| `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-SCHEMA-REVIEW.md` | `agent-handoffs/算法库联调-ALGO-LIB/FIX-TOPIC-SEARCH-PY-DWD-SCHEMA-REVIEW.md` |
| `agent-handoffs/FIX-TOPIC-SEARCH-PY-DWD-TEST-L01.md` | `agent-handoffs/算法库联调-ALGO-LIB/FIX-TOPIC-SEARCH-PY-DWD-TEST-L01.md` |
| `agent-handoffs/algo-mysql-connection-info.md` | `agent-handoffs/算法库联调-ALGO-LIB/algo-mysql-connection-info.md` |
| `agent-handoffs/algo-pg-to-mysql-migration.md` | `agent-handoffs/算法库联调-ALGO-LIB/algo-pg-to-mysql-migration.md` |
| `agent-handoffs/innov-java-pg-cutover-checklist.md` | `agent-handoffs/算法库联调-ALGO-LIB/innov-java-pg-cutover-checklist.md` |
| `agent-handoffs/D9-READINESS-MODEL-L01.md` | `agent-handoffs/编排方法论/D9-READINESS-MODEL-L01.md` |
| `agent-handoffs/ORCH-DECISION-BOARD-L01.md` | `agent-handoffs/编排方法论/ORCH-DECISION-BOARD-L01.md` |
| `agent-handoffs/ORCH-GOLIVE-BOARD-L01.md` | `agent-handoffs/编排方法论/ORCH-GOLIVE-BOARD-L01.md` |
| `agent-handoffs/ORCH-METRIC-BOARD-L01.md` | `agent-handoffs/编排方法论/ORCH-METRIC-BOARD-L01.md` |
| `agent-handoffs/PM-DECISION-BACKFILL-L01.md` | `agent-handoffs/编排方法论/PM-DECISION-BACKFILL-L01.md` |
| `agent-handoffs/ORPHAN-MD-P0-P1-cleanup-20260810.md` | `agent-handoffs/编排方法论/ORPHAN-MD-P0-P1-cleanup-20260810.md` |
| `agent-handoffs/ORPHAN-MD-P2-archive-20260810.md` | `agent-handoffs/编排方法论/ORPHAN-MD-P2-archive-20260810.md` |

## 4. 架构合规

仅路径归集；D8/D9/D10/调用链 N/A。

## 5. cost

| 字段 | 值 |
|---|---|
| actual_tokens | n/a |
| model_used | cursor-grok-4.5-high-fast |
| actual_cost | n/a |
| cost_warn | false |

ponytail: off（coordinator 文档归集）
