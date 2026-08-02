# 派单包：API-ENT-ENUM-CONTRACT-L01

- **派单方**：监管人确认 pull 认领（`human:徐滕强` · 2026-08-02）
- **监管人**：`human:徐滕强`
- **执行 Agent**：`agent:data-agent`
- **认领**：`pull` · `claimed_at=2026-08-02T12:20:00+08:00` · `lock_until=2026-08-02T16:20:00+08:00`
- **Sprint**：2026-W31
- **Epic**：`E-ENT-SCRUM-PDR`
- **性质**：实现 + 契约文档（`cicd: required` · `demo-svc-topic-py`）
- **仓**：`demo-svc-topic-py`（主代码，默认 push `origin/dev`）；`gkx-orchestration` / `agent-delivery`（registry + handoff）
- **上游**：`DATA-ENT-DICT-IMPL-L02`（已 `done`；Q056–Q059 🟢；meta 码表体系已落地）
- **优先级**：P1

---

## 0. 为何现在派

Java 对接检索三接口 / 高级筛选时，**文档枚举与 Python 真值不一致**（listing / scale / ops / Feign 字段名等），且缺少「只给 java-agent 看」的枚举专章，导致 AI/人需扫全仓猜值。  
高筛下拉码表 **v10 起已有 meta 接口**，但缺 **query_tree 字段总目录**，以及板块 / 供应链角色 / 核心技术等固定下拉。

本单独立收口，**禁止并入** `ENT-ES-ETL-L01`（ETL / 关 Mock 范围）。

---

## 1. 铁律前置（违反必拒）

1. **算法只在 Python**：本单仅 meta 只读契约 + 文档；禁止在 Java 写枚举派生算法  
2. **调用链**：前端 → Java REST → Python `/internal/*`；本单实现/扩展 Python `/internal/gkx-search/meta/*`；**不改 Java 生产 Controller、不改前端**  
3. **口径**：严格按 **Q058 / Q059**（四档规模 + `is_above_scale`；`上市`/`未上市`/`退市`）；禁止回退「已上市/拟上市」或「规上作第五档」  
4. **码表边界**：动态码表继续走既有 meta；固定枚举与 `_FIELD_STRATEGY` 对齐；勿混表、勿 invent Neo4j  
5. **范围隔离**：不改 `ENT-ES-ETL-L01` DoD；不做全量国标灌数；不扩 ADS 预聚合  

---

## 2. 必读

| 文件 | 用途 |
|------|------|
| `agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-IMPL-L02.md` | 上游 meta 落地 handoff |
| `agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-CATALOG-L01.md` | 字典盘点 / Q056–Q059 口径 |
| `客户决策清单跟踪表.md` | Q058 / Q059 |
| `repos/demo-svc-topic-py/gkx_search_service/views/meta.py` | 固定枚举 + meta 端点真源 |
| `repos/demo-svc-topic-py/gkx_search_service/views/enterprise_search.py` | `_FIELD_STRATEGY` / `_QIKE_OP_MAP` |
| `repos/demo-svc-topic-py/docs/API-接口文档.md` | 契约文档（目标升 v16.3） |
| `agent-delivery/architecture-baseline.md` | 架构铁律 D1–D8 |
| `00-team-constitution` / `task-claiming-guide.md` | 认领与 handoff DoD |

---

## 3. 范围与产出

### 3.1 必须做 — 纠错（文档/示例 ↔ 代码）

| 项 | 正确口径 |
|----|----------|
| `listing_status` | `上市` / `未上市` / `退市`（Q059） |
| `enterprise_scale` | `大型`/`中型`/`小型`/`微型`；规上 = `is_above_scale`（Q058） |
| query_tree ops | 含 `not_in` / `all` / `exist`（及既有 eq/in/range/…） |
| query_tree 字段表 | 与 `_FIELD_STRATEGY` 对齐 |
| `enterprise_region` | 仅 `eq` / `in`（删除错误的 `containsAny`） |
| Feign 示例 | `region_type`=`standard`\|`city_cluster`；graph expand=`node_key` |
| 搜索排序运行时保护 | `sort_field` 非四项白名单 → `competitiveness_score`；非法 `sort_order` → `desc`；均不得进入 ES |

### 3.2 必须做 — 新增（handoff 必须单列）

| 产物 | 说明 |
|------|------|
| `POST /meta/query-tree-schema` | `operators` + `fields` + `enums` + `value_source_apis` |
| `/meta/filters` 扩展 | `stock_types` / `supply_chain_roles` / `core_tech_tags` |
| API 文档 **§3.6b** | schema 接口说明 |
| API 文档 **§25** | 【Java Agent】枚举契约修复手册 |
| API 文档 **§26** | 变更记录 |
| 单测 | filters 增强断言 + `test_meta_query_tree_schema` |
| handoff | 纠错表 vs 新增表分列；架构合规 + cost |

### 3.3 明确不做

- Java Controller / 生产 Feign 改码（契约文档与 §25 指引除外；**实现另开** `ENT-JAVA-ENUM-CONTRACT-L02`，派单包已起草）  
- `lumen-ui-topic` / 前端改码  
- 改 `ENT-ES-ETL-L01` 范围或关 Mock 部署  
- 全量国标 `code_region` 灌数  
- 抽 `_FIELD_STRATEGY` 与 catalog 为共享模块（可留 follow-up）  

### 3.5 下游 Java（本单不实现，须单独派单）

| 项 | 值 |
|----|-----|
| task-id | `ENT-JAVA-ENUM-CONTRACT-L02` |
| agent | `api-agent` |
| 监管建议 | `human:徐滕强` |
| 认领人 | `human:侯佳伟` |
| 派单包 | `ENT-JAVA-ENUM-CONTRACT-L02-派单包.md` |
| 依赖 | 本单 `review`/`done`（Python 已 push） |
### 3.4 背景：已有 meta（非本单发明）

| 接口 | 用途 |
|------|------|
| `/meta/filters` | 筛选项 + 固定枚举 |
| `/meta/regions` | 企业所属地区树 |
| `/meta/company-types` | 工商类型 |
| `/meta/enterprise-scales` | 四档 + 规上 |
| `/meta/tags` | 资质标签 |
| `/meta/region-scopes` | 运营地域 |

本单在其上：**补 schema + 三项固定枚举 + 文档专章**。

---

## 4. DoD

见 `task-registry.yaml#API-ENT-ENUM-CONTRACT-L01.definition_of_done`。

关键证据（最低）：

1. `query-tree-schema.fields` 字段集合 == `_FIELD_STRATEGY` keys  
2. pytest：`test_meta_filters_enhanced` + `test_meta_query_tree_schema`（及相关 meta）绿  
3. handoff 分表：**纠错** vs **新增**；架构合规 10 条；cost 四字段  
4. commit 含 `[agent:data-agent]`；push 后 CI 证据写入 handoff（或注明待监管授权 push）
5. 企业查询 / 智能搜索 / 高级筛选传非法排序字段时，统一按综合竞争力降序，DSL 中不得出现非法字段

---

## 5. 派单话术（粘贴到新会话）

```markdown
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据/API 契约工程师，精通检索 meta 与 OpenAPI 对齐。
任务 ID：API-ENT-ENUM-CONTRACT-L01
性质：实现 + 契约文档（cicd: required）
监管：human:徐滕强
认领：先按 gkx-task-claim-supervision 写入 claimed 后再动手（本会话已确认）
派单包：agent-handoffs/企业战略分析-ENT/API-ENT-ENUM-CONTRACT-L01-派单包.md
上游：DATA-ENT-DICT-IMPL-L02（done）+ Q058/Q059 🟢
目标：
  1) 纠错 API 文档枚举与 meta/_FIELD_STRATEGY 一致（listing/scale/ops/enterprise_region/Feign）
  2) 新增 POST /meta/query-tree-schema；扩展 /meta/filters（stock/supply/core_tech）
  3) API 文档 §3.6b + §25 Java Agent 枚举专章；单测 + handoff（纠错/新增分表）
不做：Java/前端实现、ENT-ES-ETL-L01 范围、全量国标灌数
DoD：见 task-registry API-ENT-ENUM-CONTRACT-L01
Handoff：agent-handoffs/企业战略分析-ENT/API-ENT-ENUM-CONTRACT-L01.md
架构铁律：算法只在 Python；调用链前端→Java→Python /internal/*；码表不混表
仓 git：demo-svc-topic-py push origin/dev；编排资产在 gkx-orchestration
```

---

## 6. 状态机提示

1. registry：本单已由监管确认 → `claimed`（`2026-08-02T12:20`）→ `in_progress`（`12:22`）  
2. 本地实现/文档就绪后：监管授权 **commit + push**  
3. 交卷：`review` + 本 handoff；coordinator / 监管验收后 `done`  
4. 阻塞：立即 `blocked` + `blocked_by`，停止改仓  

---

## 7. 验收人关注点

1. §3.2 **新增**是否接受（尤其 N1 新接口）  
2. 纠错是否与 Q058/Q059、代码常量一致  
3. 未把本单工作误记入 `ENT-ES-ETL-L01`  
