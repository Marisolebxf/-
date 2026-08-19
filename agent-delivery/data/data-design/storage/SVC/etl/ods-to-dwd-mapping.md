# SVC · ODS → 项目 DWD 字段映射（OPEN-SVC-FLOW-06）

> **任务**：`DATA-SVC-STORAGE-S3-L02`；A3 列名钉死补丁 `DATA-SVC-STORAGE-GAP-L02`  
> **关闭项**：OPEN-SVC-FLOW-06（本文件为写作关闭；细表仍 **draft**，不等于流图细表 approved）  
> **A1–A6 ADS 列对照**：[`ods-to-ads-mapping.md`](./ods-to-ads-mapping.md)（不拷 DWD 主体）  
> **ODS 列真源**：[`../sources/inventory.md`](../sources/inventory.md) · md-extract 国内机构要素库  
> **DWD 列真源**：[`../stores/mysql/dwd-svc.md`](../stores/mysql/dwd-svc.md)  
> **DDL**：[`../stores/mysql/ddl-demo-empty.sql`](../stores/mysql/ddl-demo-empty.sql)

```yaml
---
doc_id: SVC-ETL-ODS-DWD-MAPPING
element: SVC
role: etl
status: draft
version: "2026-08-19"
updated: "2026-08-19"
task_id: DATA-SVC-STORAGE-S3-L02
gap_task: DATA-SVC-STORAGE-GAP-L02
---
```

**源库是 ODS，不是 ENT 项目 DWD。** 供方把贴源表起名 `dwd_*`，物理位置仍是 `demo_gkxlumenx_ods`。

```text
demo_gkxlumenx_ods.dwd_org_base_info     ← ODS 贴源（圈定 / 抽取源）
        │  svc_rule_demo_kw_v1
        │  只 hang org_id + 圈定元数据
        ▼
demo_gkxlumenx_dwd.svc_org_circle        ← SVC 项目 DWD
        ▼
demo_gkxlumenx_ads.svc_*                 ← 契约 / 模型回写
```

禁止：`SELECT demo_gkxlumenx_dwd.enterprise_*` 当主路径；平行 `svc_org_base`；把 ODS 主表 **全列** 拷进 SVC。

图例：**hang** = 只落机构键；**派生** = 规则结果（须可追溯）；**n.a.** = 本 Demo 不落 SVC DWD（需要展示时 F-SEED 读 ODS 聚合进 ADS，或 JOIN 回 ODS，不造主体表）。

---

## 1. `demo_gkxlumenx_ods.dwd_org_base_info` → `svc_org_circle`

圈定规则 `svc_rule_demo_kw_v1`：**读** `name_cn` + `industry_l*_name`（有则加 `business_scope`）。Q-SVC-010：文档无 `business_scope`；`org_type` 不可作服务机构语义。

| ODS 列 | SVC DWD | 方式 |
|---|---|---|
| `org_id` | `svc_org_circle.org_id` | **hang**（UK；与 ENT 同一键） |
| `name_cn` | — | **n.a. 主体不复制**；仅圈定读 |
| `industry` / `industry_l1_name`…`industry_l4_name` / `industry_l*_code` | — | **n.a. 主体不复制**；仅圈定读 |
| `business_scope` | — | **n.a.**；文档无此列（Q-SVC-010）；有则圈定加读，仍不落主体 |
| （命中了哪些列） | `hit_fields` JSON | **派生** |
| — | `rule_version`=`svc_rule_demo_kw_v1` | **派生** |
| — | `service_type_candidate` | **派生** 六类候选；一律待核验 |
| — | `pending_client_confirm`=1 | **派生**（Q-SVC-010 不伪闭合 live） |
| `external_id` / `province` / `city` / `area` / `address` / `addr_*` / `postal_code` / `email` / `lerep` / `reg_status` / `registration_org` / `incorporation_*` / `start_date` / `end_date` / `org_type` / `listing_*` / `registered_capital_value` / `capital_currency` / `phone_num` / `org_size` / `data_source` / `created_time` / `updated_time` | — | **n.a. 主体不复制**。A2/A4/A5/A6 聚合时 F-SEED **读 ODS** 后写 ADS，不经本表拷列 |

`org_type` 只允许当工商组织形式旁路字段在 ODS 侧被读到，**禁止**写入圈定主路径。

---

## 2. 图 hang（不是十模型）

| 源 | SVC DWD | 方式 |
|---|---|---|
| `svc_org_circle.org_id` | `svc_org_graph_hang.org_id` | hang |
| — | `node_id` | 与决策 #7 对齐：`org_id`↔`node_id`；space 固定 `demo_gkx_chain` |
| — | `space_name`=`demo_gkx_chain` | 写死；禁 `gkx_service` |

Nebula 投影见 [`../stores/nebula/graph-svc.md`](../stores/nebula/graph-svc.md)。F-ALGO 才写图，本单只建空表。

---

## 3. 投融资 ODS → `svc_org_finance_event`（A3 / Q-SVC-006）

左表仍在 **ODS**（国内机构要素库已列；金融要素库归属见 Q-SVC-006，Demo 可 0 行）。无独立事件主键。

### 3.1 融资 `demo_gkxlumenx_ods.dwd_org_financing_info` → `event_type=FINANCING`

| ODS 列 | SVC DWD | 方式 |
|---|---|---|
| `org_id` | `org_id` | hang |
| `funding_amount` | `amount` | 直接 |
| `completion_date` | `event_date` | 直接；空则本行仍 hang，**不进** A3 时序 |
| `org_id` + `completion_date` + `funding_round` | `event_id` | **派生复合键**（无事件 pk） |
| `funding_round` / `funding_currency_code` / `investors_name` / `post_valuation` | `ext` JSON | 可选，不落主体 |

### 3.2 投资 `demo_gkxlumenx_ods.dwd_org_invest_info` → `event_type=INVEST`

文档**无**投资完成日。

| ODS 列 | SVC DWD | 方式 |
|---|---|---|
| `org_id` | `org_id` | hang（投资方） |
| `investment_amount` | `amount` | 直接 |
| — | `event_date` | **空**（禁止用 `created_time` 冒充业务日） |
| `org_id` + `inv_org_id` | `event_id` | **派生复合键**；同对多行再拼 `created_time` |
| `inv_org_id` / `inv_name` / `investment_ratio` | `ext` JSON | 可选 |

只 hang **圈定池内** `org_id`。**禁止**为此再建机构主体表。无行时诚实空态，不伪闭合 `M_SVC_INVEST_Y` live。

---

## 4. 不映射（写在这里以免下游误用）

| 对象 | 原因 |
|---|---|
| `demo_gkxlumenx_dwd.enterprise_base` 等 | 停机 / 总控：禁 `enterprise_*` 主路径 |
| `svc_org_base` / `gkx_dwd.service_org` 38 列稿 | 平行主体；旧 S3-L01 废作 |
| 产业链 `dwd_org_industry_tags` | `storage/CHAIN`，本轮不改 |

---

## 5. 禁止

- 映射左列不写库名、让 `dwd_org_base_info` 被读成项目 DWD  
- 把本映射当成正式 GDF 已上线  
- 本单执行 50100 灌数
