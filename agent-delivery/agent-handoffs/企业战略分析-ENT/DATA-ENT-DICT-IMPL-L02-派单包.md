# 派单包：DATA-ENT-DICT-IMPL-L02

- **派单方**：coordinator-agent（调度者 / `human:淮政玮` 授权 · 2026-07-29）
- **监管人**：`human:淮政玮`
- **执行 Agent**：`data-agent`
- **Sprint**：2026-W30
- **Epic**：E-ENT-SCRUM-PDR
- **性质**：实现类（`cicd: required` · `demo-svc-topic-py`）
- **仓**：`demo-svc-topic-py`（主代码）；`agent-delivery`（DDL 执行记录 / handoff）
- **上游**：`DATA-ENT-DICT-CATALOG-L01`（已 `done`；Q056–Q059 🟢）

---

## 0. 为何现在派

L01 已完成字典盘点与 DDL 设计，口径已闭合。本单把设计**落到 MySQL + Python meta**，让前端/Java 后续接线有真源可读。

---

## 1. 铁律前置（违反必拒）

1. 码表落 **`gkxlumenx_dim.*`**；标签对齐 **`gkxlumenx_dwd.tag_dict`**；勿混表
2. **算法/灌数只在 Python**；本单可改 `demo-svc-topic-py`
3. 调用链仍前端 → Java → Python `/internal/*`（本单实现 Python `/internal/.../meta/*`；**不改 Java / 不改前端**）
4. 严格按 **Q056–Q059** 已确认口径，不得回退到旧五档互斥规模或「已上市/拟上市」混用
5. **不做** `code_region` 全量国标灌数（另开 SEED 任务）

---

## 2. 必读

| 文件 | 用途 |
|---|---|
| `agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-CATALOG-L01.md` | 上游 handoff |
| `data/data-design/企业/ENT-DICT-CATALOG-L01.md` | 清单 + §5 口径 + §5.1 上市派生 |
| `data/ddl/gkxlumenx_dim_region_scope.sql` | 建表+种子 |
| `data/ddl/gkxlumenx_dwd_tag_dict_align.sql` | tag_dict ALTER |
| `客户决策清单跟踪表.md` §2.z | Q056–Q059 |
| `agent-handoffs/algo-mysql-connection-info.md` | MySQL 连接 |
| `repos/demo-svc-topic-py/gkx_search_service/views/meta.py` | 改码目标 |
| `repos/demo-svc-topic-py/docs/API-接口文档.md` | 契约同步 |

---

## 3. 范围与产出

### 必须做

1. **执行 DDL**（MySQL `192.168.88.43`）：`region_scope` / `region_scope_member`；`tag_dict` ALIGN  
2. **种子**：Q056 — 区域成员按法定边界初始化（可运营改）；热门城市 Mock；全球 = G20 主要科创城市 Mock（可扩 `dim.city`）  
3. **Python meta**  
   - 新增 `/meta/region-scopes`（或等价）读 `region_scope`  
   - 修 `/meta/tags`：库表 `gkxlumenx_dwd.tag_dict` + 新列  
   - `/meta/enterprise-scales`：大型/中型/小型/微型；规上独立（Q058）  
   - `/meta/filters` listing：`上市`/`未上市`/`退市`（Q059；文案不加「已」）  
4. **文档 + 单测** + **handoff**

### 明确不做

- 全量国标 `code_region`  
- `lumen-ui-topic` / 前端接线（建议 follow-up `FE-ENT-DICT-WIRE-L04`）  
- Java Facade（建议 `API-ENT-DICT-JAVA-L05`）  
- 上市 ODS 全量 ETL 明细表（可在 handoff 留开放项；本单至少 meta 枚举与 Mock 对齐）

---

## 4. DoD

见 `task-registry.yaml#DATA-ENT-DICT-IMPL-L02.definition_of_done`。

---

## 5. 派单话术（粘贴到新会话）

```markdown
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师，精通数仓分层与数据契约；能在 demo-svc-topic-py 落地 meta 只读接口。
任务 ID：DATA-ENT-DICT-IMPL-L02
性质：实现类（cicd: required）
监管：human:淮政玮
认领：先按 gkx-task-claim-supervision 写入 claimed 后再动手
派单包：agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-IMPL-L02-派单包.md
上游：DATA-ENT-DICT-CATALOG-L01（done）+ Q056–Q059 🟢
目标：执行 region_scope/tag_dict DDL 与 Q056 种子；改 meta.py（region-scopes、tags、规模四档+规上独立、listing=上市/未上市/退市）；文档+单测+handoff
不做：全量国标 code_region、前端、Java
DoD：见 task-registry DATA-ENT-DICT-IMPL-L02
Handoff：agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-IMPL-L02.md
架构铁律：算法只在 Python；调用链前端→Java→Python /internal/*；码表优先 gkxlumenx_dim
仓 git：demo-svc-topic-py 默认 push origin/main（demo 策略）；编排文档在 gkx-orchestration
```

---

## 6. 状态机提示

1. registry：`ready`，`supervised_by: human:淮政玮`，`claimed_by` 空  
2. 开工：`claimed` → `in_progress`  
3. 交卷：`review` + handoff；coordinator 验收后 `done`
