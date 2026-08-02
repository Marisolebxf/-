# DG-ENT-SEARCH-拍板纪要

> **模块**：E1-企业 · 企业查询（SEARCH）  
> **日期**：2026-08-03  
> **汇报**：郭万迎（编排补登）  
> **决策人**：淮政玮  
> **触发**：故事驱动实现 leaf（如 `ENT-MOD-SEARCH-DATA-PATH-L01`）依赖 `ENT-MOD-SEARCH-DG-G3`，registry 缺门 3 锚点；用户指令「补齐完成门3」  
> **结论**：⚠️ **批准附条件**（编排补登 · 工程已超前；附条件须在 Sprint 内闭合）

---

## 1. 决策摘要（淮政玮 30 秒项）

| # | 决策事项 | 决定 | 类型 |
|---|----------|------|------|
| D1 | SEARCH 是否解锁实现轨依赖（ARCH/API/DATA/FE/QA 故事拆单 leaf） | **批准**补登 `ENT-MOD-SEARCH-DG-G3=done`，允许 `depends_on` 满足 | 范围取舍 |
| D2 | 门 2 / V1-FINAL / V2 会签单尚未全部 `done` | **附条件**：不阻塞本批 backlog→confirm；须补签收（见 §4） | 临时默认 |
| D3 | 未单列 `ENT-MOD-SEARCH-G2-SIGNOFF` | **视同**：以 V2 会签 + PDR 体验结论暂代；正式 G2 签字单可后补 | 体验偏离/流程补登 |
| D4 | 数据路径与 `ENT-DATA-IMPL-PATH`（进行中）关系 | **不合并 ID**；SEARCH DATA-PATH 验收须引用企业维 Mapping 进展，避免双开冲突 | 范围取舍 |

---

## 2. 输入与现状盘点

| 门禁 | leaf / 证据 | 状态 |
|------|-------------|------|
| 门 1 PDR | `ENT-MOD-SEARCH-PDR-G1` + `PM-PDR-ENT-SEARCH-评审纪要.md` | ✅ done（legacy 附条件通过） |
| 门 1 完整闭合 | `ENT-MOD-SEARCH-PDR-G1-RECLOSE` | ⬜ ready（待闭合） |
| V1 首轮 | `ENT-MOD-SEARCH-V1-HIFI` | ✅ done |
| V1 联合冻结 | `ENT-MOD-SEARCH-V1-FINAL` | ⬜ ready |
| V2 准生产 | `ENT-MOD-SEARCH-V2-S0/S1/S2A/S4/S5` | ✅ done；父 leaf `V2-DEMO` = ready_to_sign |
| 门 2 | `ENT-MOD-SEARCH-G2-SIGNOFF` | ❌ 未建 leaf |
| METRIC-OPEN | `ENT-MOD-SEARCH-METRIC-OPEN-L01` | ⬜ ready_to_sign |
| 工程超前 | `ENT-JAVA-SEARCH-*` / 地区筛选等 | 已 integration（与 DECIDE-FE-V2-LUMEN-DIRECT 一致） |

---

## 3. 开放项（不因本 DG 关闭）

| Q / 项 | 处置 | Deadline |
|--------|------|----------|
| Q033~Q037（SEARCH PDR Δ） | 保持 🟡；实现 leaf DoD 须对齐 | 下一切 SEARCH Sprint Review |
| METRIC-OPEN 签收 | 淮政玮/语义侧关 `ready_to_sign→done` | 尽快 |
| V1-FINAL / PDR-RECLOSE | product 闭合后改 done | W32/W33 Planning |
| V2-DEMO 会签单签字 | 孔东补 `FE-LUMEN-V2-ALIGN-ENT-SEARCH` | V2 ready_to_sign→done 前 |
| G2 正式签字单 | 可选后补 leaf 或并入 V2 会签证据 | 门 I3 前 |

---

## 4. 附条件（⚠️）

- [ ] `ENT-MOD-SEARCH-V1-FINAL` → done（联合修订冻结证据落盘）
- [ ] `ENT-MOD-SEARCH-V2-DEMO` → done（会签单 + commit/URL）
- [ ] `ENT-MOD-SEARCH-METRIC-OPEN-L01` → done 或书面 N/A
- [ ] `ENT-MOD-SEARCH-PDR-G1-RECLOSE` → done 或 note 标明被本 DG 附条件覆盖
- [ ] 实现 leaf unlock 仍走 **派单门控「待确认」→「已确认」**（本 DG **不**自动 ready）

---

## 5. task-registry 解锁

| task-id | 原状态 | 新状态 | 备注 |
|---------|--------|--------|------|
| `ENT-MOD-SEARCH-DG-G3` | （无） | **done** | 本纪要；用户指令 2026-08-03 |
| `ENT-MOD-SEARCH-*-L01`（故事拆单） | backlog | 仍 backlog | 依赖已满足；**须 confirm** 后 ready |

---

## 6. 签字

| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 决策 Owner | 淮政玮 | ⚠️ 编排代登（用户指令「补齐完成门3」；须书面/看板追认） | 2026-08-03 |
| 合规 Owner | 郭万迎 | 汇报补登 | 2026-08-03 |

> **公约对齐**：业务口径仍以 `客户决策清单跟踪表` 🟡 为准，本 DG 不替甲方拍板。
