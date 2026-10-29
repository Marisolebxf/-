# Handoff：DATA-ENT-DICT-CATALOG-L01

- **task-id**：`DATA-ENT-DICT-CATALOG-L01`
- **执行**：`agent:data-agent`
- **监管**：`human:淮政玮`
- **认领**：`coordinator_dispatch` · `claimed_at=2026-07-29T17:20:00+08:00`
- **性质**：设计类（`cicd: skip_design_only`）
- **状态建议**：`review`（待 coordinator 验收 → `done`）
- **日期**：2026-07-29

---

## 1. 范围与实现（对照派单）

| DoD | 状态 | 产物 |
|-----|------|------|
| 字典/码表清单表 | ✅ | `agent-delivery/data/data-design/企业/ENT-DICT-CATALOG-L01.md` §2 |
| 缺表项 MySQL DDL | ✅ | `data/ddl/gkxlumenx_dim_region_scope.sql`；`data/ddl/gkxlumenx_dwd_tag_dict_align.sql` |
| 边界：code_region / admin_division / 运营地域 / tag_dict / 固定枚举 | ✅ | 清单 §3 |
| 种子策略 + 灌数 follow-up | ✅ | 清单 §4.2 / §6 |
| 业务口径登记客户决策清单 | ✅ | Q056–Q059 |
| 不做前端/Java/全量国标灌数 | ✅ | 本单无业务仓代码改动 |

**对照 bid / 架构**：企业检索筛选字典属数据契约先行；码表落 `gkxlumenx_dim.*`，标签明细字典留 `gkxlumenx_dwd.tag_dict`。

---

## 2. 关键结论（一句话）

结果区「全球/区域/热门城市」**必须新建运营维表**，不可塞进 `code_region`；省市区继续用 `code_region`（样例 11 行）；标签表需契约对齐；公司类型/规模/上市/经营状态 **Wave0 保持 Python 固定枚举**，口径歧义已登记 🟡。

### 2.1 实测现网（2026-07-29 · `10.50.11.76`）

| 对象 | 行数 / 备注 |
|------|-------------|
| `gkxlumenx_dim.code_region` | 11 |
| `gkxlumenx_dim.admin_division` | 11（同源样例） |
| `gkxlumenx_dim.city` | 14（含海外标杆） |
| `gkxlumenx_dwd.tag_dict` | 7；列缺 `tag_level`/`is_active`/`sort_order` |
| `gkxlumenx_dwd.risk_type_dict` | 0 |

---

## 3. 偏离说明

无范围外实现。`tag_dict` ALTER **仅交付 DDL**，本单未在生产库执行（避免未经监管的 schema 变更）。`region_scope` DDL **未建表执行**，待 L02/L03 或监管批准后落地。

深圳区县 `bind_admin_code` 中部分新区/编码标注「以国标灌数为准」——全量 `code_region` 到位后校正（L02）。

---

## 4. 产物清单

| 路径 | 说明 |
|------|------|
| `agent-delivery/data/data-design/企业/ENT-DICT-CATALOG-L01.md` | 清单 + 边界 + 种子策略 + follow-up |
| `agent-delivery/data/ddl/gkxlumenx_dim_region_scope.sql` | 新建运营地域表 + Wave0 种子 |
| `agent-delivery/data/ddl/gkxlumenx_dwd_tag_dict_align.sql` | tag_dict ALTER + 补种 |
| `agent-delivery/data/data-design/企业/DWD表结构设计-企业模块.md` | changelog v2.6.2 |
| `agent-delivery/客户决策清单跟踪表.md` | §2.z Q056–Q059 |
| 本 handoff | — |

---

## 5. 验收证据

- 清单覆盖：前端写死（`regionOptions.ts` / `filterFieldSchema.ts`）、Python 固定枚举（`meta.py`）、现网 DIM/DWD 表
- DDL 语法：InnoDB / utf8mb4；PK + parent/member 语义完整
- 决策项：Q056–Q059 已挂 🟡，未替甲方拍板
- 本仓为编排文档交付；`cicd: skip`

---

## 6. 架构合规自检

| # | 铁律 | 结果 |
|---|------|------|
| 1 | 算法只在 Python | ✅ 本单无算法代码 |
| 2 | 调用链 FE→Java→Python `/internal/*` | ✅ 仅建议 meta 契约，未越层实现 |
| 3 | NebulaGraph | ✅ 不涉及 |
| 4 | 可观测性 | ✅ N/A 设计类 |
| 5 | CI/CD | ✅ `skip_design_only` |
| 6 | demo2 只读 merge | ✅ 未改 lumen/demo UI 仓 |
| 7 | 共享聚合 / 前端只调 Java | ✅ 建议 Java 透传 follow-up |
| 8 | ADS 先行 / Mock | ✅ 种子为 Wave0 样例 |
| 9 | Design.md 前端规范 | ✅ N/A（未改 UI） |
| 10 | D9 血缘 | ✅ 字典与筛选指标边界写清；口径挂 Q 号 |
| 11 | D10 交互 | ✅ N/A |

---

## 7. 开放项 / Follow-up 建议

| 建议 task ID | 内容 |
|--------------|------|
| `DATA-ENT-DICT-REGION-SEED-L02` | `code_region` 全量国标；`region_scope_member` 法定边界种子；G20/热门 Mock；校正 `bind_admin_code` |
| `DATA-ENT-DICT-META-API-L03` | 建表执行 + `/meta/region-scopes`；修 `tag_dict`；规模四档+`is_above_scale`；listing=`上市/未上市/退市`；上市 ETL 派生 |
| `FE-ENT-DICT-WIRE-L04` | `RegionSelect` 接 meta；工商/资质双字段；规模与上市 UI 对齐 Q057–Q059 |
| `API-ENT-DICT-JAVA-L05` | Java 透传 region-scopes（若需） |

**决策闭合（2026-07-29）**：Q056 / Q057 / Q058 / Q059 均已 🟢（`human:淮政玮` 确认）。仍关联开放：Q010、Q049。

---

## 8. Cost 回填（供 registry）

| 字段 | 值 |
|------|----|
| `actual_tokens` | ~95000（估；含盘点读库与文档） |
| `model_used` | cursor-grok-4.5 |
| `actual_cost` | ~1.5（估，green） |
| `cost_warn` | green |

> coordinator 验收时可按会话用量微调。

### 补记 · 决策回写（2026-07-29 晚）

已回写：`客户决策清单跟踪表.md` §2.z、`ENT-DICT-CATALOG-L01.md` §2/§4.2/§5/§7、`gkxlumenx_dim_region_scope.sql` remark。本补记不改业务仓代码。
