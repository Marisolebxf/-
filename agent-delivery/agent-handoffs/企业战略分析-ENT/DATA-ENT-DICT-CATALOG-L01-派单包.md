# 派单包：DATA-ENT-DICT-CATALOG-L01

- **派单方**：coordinator-agent（调度者授权 · 2026-07-29）
- **监管人**：`human:淮政玮`
- **执行 Agent**：`data-agent`
- **Sprint**：2026-W30（stretch）
- **Epic**：E-ENT-SCRUM-PDR
- **性质**：设计类（`cicd: skip_design_only`）
- **仓**：`agent-delivery`（主）；只读参考 `demo-svc-topic-py` / `lumen-ui-topic`
- **上游**：`DATA-DIM-CODE-REGION-MIGRATE-2026-07-29.md`（code_region 已落 DIM，本单盘点其余字典）

---

## 0. 为何现在派

企业检索 UI 存在多套「字典/码表」来源，现状割裂：

1. **结果区地域级联**（全球 / 全国 / 区域 / 热门城市）— 前端写死  
   `lumen-ui-topic/src/components/search/regionOptions.ts`
2. **高级筛选省市区** — MySQL `gkxlumenx_dim.code_region`（仅 11 行样例，非全量国标）
3. **Python meta 固定枚举** — `company-types` / `enterprise-scales` / listing / operating 写死在  
   `demo-svc-topic-py/gkx_search_service/views/meta.py`
4. **标签字典** — 已有 `gkxlumenx_dwd.tag_dict`（需盘点是否够用）
5. **innov 同源** — `gkxlumenx_dim.admin_division` 与 `code_region` 并存，边界需写清

本单只做：**盘点 + 表设计 + 落库策略**；不写前端、不实现 Java、不强制全量灌数。

---

## 1. 铁律前置（违反必拒）

1. 码表优先落 **`gkxlumenx_dim.*`**；业务明细仍在 DWD；勿把枚举塞进 ADS
2. **算法/灌数只在 Python**；本单不出算法代码
3. 调用链仍前端 → Java → Python `/internal/*`（本单可只建议 meta 契约，不实现）
4. 业务口径歧义（如「区域」是否含大湾区法定边界）→ 登记 `客户决策清单跟踪表.md`，标 🟡，**不替甲方拍板**
5. 不得与 `code_region`（省市区国标树）和「全球/热门城市」运营字典混成一张物理表（可同 schema 多表）

---

## 2. 必读

| 文件 | 用途 |
|---|---|
| `agent-delivery/data-lineage-policy.md` | D9 血缘 / ODS·DWD 解耦 |
| `agent-delivery/agent-handoffs/algo-mysql-connection-info.md` | MySQL 连接真源 |
| `agent-delivery/agent-handoffs/企业战略分析-ENT/DATA-DIM-CODE-REGION-MIGRATE-2026-07-29.md` | code_region 已迁 DIM |
| `agent-delivery/data/ddl/gkxlumenx_dim_code_region.sql` | 已有 DDL 参考 |
| `repos/demo-svc-topic-py/gkx_search_service/views/meta.py` | 现有 meta 字典入口 |
| `repos/demo-svc-topic-py/docs/API-接口文档.md` §meta | 接口契约 |
| `repos/lumen-ui-topic/src/components/search/regionOptions.ts` | 前端写死地域级联 |
| `repos/lumen-ui-topic/src/components/search/RegionSelect.vue` | 消费方组件 |
| `agent-delivery/data/data-design/企业/DWD表结构设计-企业模块.md` v2.6 / v2.6.1 | 设计 changelog |

---

## 3. 范围与产出

### 必须产出

1. **字典/码表清单表**（建议列）：`dict_id` / 中文名 / 消费位置（UI 组件或 API） / 现状（前端写死|Python 枚举|已有表） / 建议落库（库.表） / 优先级 / 备注  
2. **缺表项 DDL**：落 `agent-delivery/data/ddl/`（至少覆盖结果区地域级联；其余按清单标 P0/P1）  
3. **边界说明**：`code_region` vs `admin_division` vs 新建运营地域字典 vs `tag_dict` vs 固定枚举  
4. **种子策略**：样例种子 / 全量国标 / 运营维护入口（本单可只写策略，灌数开 L02）  
5. **handoff**：`agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-CATALOG-L01.md`  
6. **follow-up 建议**：L02 灌数、L03 Python meta API、L04 前端接线（只列 ID 建议，不自行改 registry 状态机以外字段除非协调员同意）

### 明确不做

- 改 `lumen-ui-topic` / `demo-ui-topic` 代码  
- 改 Java Controller  
- 全量国标行政区划灌数  
- 替甲方确认「区域」业务口径  

---

## 4. DoD（验收）

见 `task-registry.yaml#DATA-ENT-DICT-CATALOG-L01.definition_of_done`。

---

## 5. 派单话术（粘贴到新会话）

```markdown
/goal data-agent
身份：你是经验丰富、遵循最佳实践的资深数据架构/数据工程师，精通数仓分层(ODS/DWD/DIM/ADS)、数据建模、数据质量与血缘；践行数据契约先行 + Mock 先行。
任务 ID：DATA-ENT-DICT-CATALOG-L01
性质：设计类（cicd: skip）
监管：human:淮政玮
认领：先按 gkx-task-claim-supervision 写入 claimed_by/supervised_by 后再动手
派单包：agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-CATALOG-L01-派单包.md
必读：派单包 §2；data-lineage-policy.md；DATA-DIM-CODE-REGION-MIGRATE-2026-07-29.md；meta.py；regionOptions.ts
目标：盘点企业检索/筛选相关字典与码表，设计缺表 DIM DDL，写清单 + 边界 + 种子策略 + handoff
不做：前端/Java 实现、全量灌数、替甲方拍板
DoD：见 task-registry DATA-ENT-DICT-CATALOG-L01
Handoff：agent-handoffs/企业战略分析-ENT/DATA-ENT-DICT-CATALOG-L01.md
架构铁律：算法只在 Python；调用链前端→Java→Python /internal/*；码表优先 gkxlumenx_dim；Nebula 不涉及本单
```

---

## 6. 状态机提示

1. registry 当前：`ready`，`claimed_by` 空，`supervised_by: human:淮政玮`  
2. 开工前：`update-task-status` → `claimed` → `in_progress`  
3. 交卷：`review` + handoff；coordinator 验收后 `done`
