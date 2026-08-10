# 派单包：ENT-ES-ETL-L01

- **派单方**：coordinator-agent（用户指令：建任务给腾强）
- **时间**：2026-07-24
- **责任人 / 监管人**：`human:徐滕强`
- **建议执行 Agent**：`data-agent`（开会话时把 `claimed_by` 改为 `agent:data-agent`，`supervised_by` 保持本人）
- **Sprint**：2026-W30
- **Epic**：E-ENT-SCRUM-PDR
- **仓**：`demo-svc-topic-py`（主）；`demo-svc-platform`（Helm/CronJob / `GKX_ES_*` 注入）
- **上游依赖**：`ENT-ES-DESIGN-L01`（done）
- **设计真源**：`企业搜索-ES更新机制.md` v1.0 · `企业搜索-ES索引设计.md`

---

## 0. 为何现在派

查企业链路审计结论（2026-07-24）：

```
lumen-ui-topic → Java gkxlumen-topic-enterprise → Python /internal/gkx-search/*
```

已通，但：

1. K8s `GKX_MOCK_ENABLED=1`，列表/画像主体读内存 Mock
2. `demo-svc-topic-py` **无** SyncModule / 水位线 / 日批入口 / CronJob
3. Helm 仅占位 `GKX_ES_HOST=elasticsearch:9200`，未见真实外置 ES 配置

补充（同日）：**DWD 表中已有部分虚拟/Mock 数据，不影响 ETL**，可作 Extract 试点，勿当阻塞。

设计已在 `ENT-ES-DESIGN-L01` 完成；本任务做 **Phase 1 代码落地**。

---

## 1. 铁律前置（违反必拒）

1. **算法 / ETL 只在 Python**；Java / 前端不写灌 ES 逻辑
2. **调用链不越层**：检索仍走 `/internal/gkx-search/*`；本任务只补「写 ES」侧
3. **禁止全文档 PUT 互盖**：增量必须用 Painless script 局部更新（见更新机制 §0.2–0.3）
4. **司法明细不灌 ES**：只写 `risk_flags` 计数 + `risk_level`
5. **`_id = org_id`**；别名 `gkx_enterprise`
6. **范围 ±10%**：本期 Phase 1（骨架 + ≥3 核心模块 + 关 Mock 冒烟）；其余模块拆 L02
7. **无真实 ES / 表结构连不上 → blocked**：写清 `blocked_by`，禁止用假 ES 假装关 Mock
8. **DWD 已有虚拟/Mock 数据 ≠ 阻塞**：库内已灌入部分 Mock 企业行，**可直接作为 Phase 1 Extract 试点源**；勿因「源不是生产三方真数」停工或改 DoD。验收以「ETL 链路跑通 + 关 search Mock 后能命中灌入文档」为准

---

## 2. 必读

| 优先级 | 文件 | 用途 |
|---|---|---|
| P0 | `agent-delivery/data/data-design/企业/企业搜索-ES更新机制.md` | 17 模块、水位线、script 更新 |
| P0 | `agent-delivery/data/data-design/企业/企业搜索-ES索引设计.md` | mapping / 字段分层 |
| P0 | `agent-handoffs/企业战略分析-ENT/DATA-ENT-ES-design.md` | 设计 handoff |
| P0 | `agent-delivery/architecture-baseline.md` | D1–D8 / 数据工厂 |
| P1 | `repos/demo-svc-topic-py/gkx_common/es.py` | 现有只读 ES 客户端（扩展写路径时注意分层） |
| P1 | `repos/demo-svc-platform/helm/gkx-platform/values.yaml` → `searchPy.env` | 当前 ES/Mock 注入 |

---

## 3. Phase 1 范围（DoD 摘要）

| # | 交付物 |
|---|---|
| 1 | SyncModule 基类 + 水位线 + CLI/调度入口 + 同步日志 |
| 2 | ≥3 核心模块：建议 `reg_info` / `tag_info` / `product_info`（script 局部更新） |
| 3 | Helm：真实可达 `GKX_ES_*` + CronJob（或明确外部调度入口）+ 关 Mock 操作说明 |
| 4 | 冒烟：试点 org_id（可用 DWD 已有 Mock 行）灌入后，`GKX_MOCK_ENABLED=0` 下 search query 命中 |
| 5 | handoff + 架构合规自检 + cost 四字段；L02 剩余模块清单 |

**数据前提（2026-07-24 补充）**：DWD 表中已有部分虚拟/Mock 数据，**不影响、不阻塞 ETL**；Phase 1 应用这些行做端到端验证即可。

**明确不做（L02 / 他单）**：17 模块一次做完；ADS 总览预聚合全表；改 `lumen-ui-topic` 契约；实时 WAL→ES。

---

## 4. 派单话术（开 Cursor 会话可粘贴）

```text
/goal ENT-ES-ETL-L01
你是 data-agent，监管人 human:徐滕强。
在 demo-svc-topic-py 落地企业搜索 DWD/ODS→ES 日批 ETL Phase 1：
SyncModule 骨架 + 水位线 + ≥3 核心模块（reg_info/tag_info/product_info）+
Painless script 局部更新 + Helm GKX_ES_* / CronJob + 关 Mock 冒烟。
必读：企业搜索-ES更新机制.md、企业搜索-ES索引设计.md、本派单包。
禁止全文档 PUT 互盖；司法明细不灌 ES；无真实 ES/表连不上则 blocked。
DWD 已有 Mock 虚拟数据可直接作 Extract 试点，不阻塞。
完工写 agent-handoffs/企业战略分析-ENT/ENT-ES-ETL-L01-handoff.md 并转 review。
```

---

## 5. 验收关注点（coordinator）

- [ ] 代码在 `demo-svc-topic-py`，调度/配置在 `demo-svc-platform`（如有）
- [ ] 增量写路径为 script update，非全量 PUT
- [ ] 有可达 ES 地址与关 search Mock 证据（curl/日志）；试点源可为 DWD Mock 行
- [ ] handoff 含 L02 模块清单与 cost 四字段
- [ ] 未擅自扩到前端 / Java 检索契约
- [ ] 未因「DWD 是 Mock」误标 blocked
