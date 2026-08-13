# CHAIN · 在线约定 vs 三方真实四表 — 差异

```yaml
---
doc_id: CHAIN-ODS-ONLINE-VS-LIVE-DIFF
element: CHAIN
role: source
status: draft
version: "2026-08-13"
updated: 2026-08-13
task: DATA-CHAIN-STORAGE-S2-L01
probed: "2026-08-13 live DESCRIBE @ 183.240.141.251:3318/gkx"
---
```

> **副产品（淮政玮口径）**：在线表 → md 与**三方数据源对应四表**的差异说明。  
> **不作** Demo ODS 建表真源；建表仍以 `doc/md-extract` 为准。  
> **真实侧**：`183.240.141.251:3318` / 库 `gkx` / 只读 `gkx_reader_zp`（见 CONNECTION.md）。

## 0. 对照双方

| 侧 | 真源 | 说明 |
|---|---|---|
| **在线约定** | `doc/md-extract/…__产业链要素库` | S2 Demo DDL 输入 |
| **真实数据源** | **`183.240.141.251:3318` / `gkx` 同名四表** | **本文件 §2 以 2026-08-13 当场 `DESCRIBE` 为准** |
| **勿用** | `gkx_schema_ddl.sql` 旧片段（`chain_code`/`node_id`/`news_id`…） | 沙箱 DDL **滞后**，与 live 不一致 |

### 四表 live 行数（`is_deleted=0` · 2026-08-13）

| # | 表名 | 行数 | 列数 |
|---|---|---:|---:|
| 1 | `dwd_industry_chain_info` | 1,273 | 15 |
| 2 | `dwd_org_industry_tags` | 20,000 | 13 |
| 3 | `dwd_org_industry_product_tags` | 20,000 | 16 |
| 4 | `dwd_industry_chain_news_info` | 476 | 14 |

证据 JSON（含 `SHOW CREATE`）：`third-party-source/gkx-mysql-raw/加工/_chain_four_tables_live_2026-08-13.json`

---

## 1. 共性差异

| 项 | 在线约定（md-extract） | 三方 live @3318 |
|---|---|---|
| 物理主键 | 业务列「是否为主键」 | 四表均为 `pk_id` BIGINT AI |
| 六技术字段 | **无** | 均有：`created_time` / `updated_time` / `creater` / `updater` / `table_data_source` / `is_deleted` |
| 取数 | — | 默认 `is_deleted=0` |

---

## 2. 分表字段差异（live DESCRIBE）

图例：✅ 同名可对齐 · 🔧 同名但类型/形态/键角色变 · ❌ 仅一侧有

### 2.1 `dwd_industry_chain_info`

| 在线英文字段 | 在线要点 | Live Type / Null / Key | 差异 |
|---|---|---|---|
| — | — | `pk_id` bigint NO **PRI** | ❌ 仅 live |
| `industry_code` | 字符 255 | varchar(255) NO MUL | ✅ |
| `industry_name` | 字符 255 | varchar(255) NO MUL | ✅ |
| `industry_link_code` | 字符 255 · **业务主键** | varchar(255) NO MUL | 🔧 非物理 PK |
| `industry_link_name` | 字符 255 | varchar(255) NO MUL | ✅ |
| `level` | 数值 | **int** NO MUL | 🔧 |
| `parent_code` | 字符 255 可空 | varchar(255) YES | ✅ |
| `parent_name` | 字符 255 可空 | varchar(255) YES | ✅ |
| `node_company_count` | 数值 可空 | **bigint** YES | 🔧 类型；聚合字段勿当 DWD 节点主属性 |
| — | — | 六技术字段 | ❌ 仅 live |

### 2.2 `dwd_org_industry_tags`

| 在线英文字段 | 在线要点 | Live Type / Null / Key | 差异 |
|---|---|---|---|
| — | — | `pk_id` + 六技术字段 | ❌ 仅 live |
| `industry_code` | 字符 **2500** · 样例单值 | varchar(**255**) NO · 样例为 **JSON 数组** | 🔧 长度/形态 |
| `industry_name` | 字符 **10000** | varchar(255) NO · JSON 数组 | 🔧 |
| `industry_link_code` | 字符 **10000** | varchar(**3000**) NO · JSON 数组 | 🔧 |
| `industry_link_name` | 字符 **10000** | varchar(**2000**) NO · JSON 数组 | 🔧 |
| `company_name` | 字符 500 | varchar(500) NO | ✅ |
| `credit_code` | 字符 255 · **业务主键** | varchar(255) NO MUL | 🔧 键角色 |

### 2.3 `dwd_org_industry_product_tags`

| 在线英文字段 | 在线要点 | Live Type / Null / Key | 差异 |
|---|---|---|---|
| — | — | `pk_id` + 六技术字段 | ❌ 仅 live |
| `industry_code` / `industry_name` | 长字符 · 样例单值 | varchar(255) · **JSON 数组** | 🔧 |
| `industry_link_code` / `_name` | 文本 | **text** · JSON/可空数组形态 | 🔧 |
| `id` | **数字** · 企业ID | **bigint YES**（可空） | 🔧 有列；类型/可空 |
| `company_name` | 字符 500 | varchar(500) NO | ✅ |
| `credit_code` | 字符 255 · 可空 · 标主键 | varchar(255) YES | 🔧 |
| `product_name` | 文本 | text NO | ✅ |
| `product_top5` | 文本 | **text YES MUL** | ✅ 列存在（先前文档曾存疑，**live 已确认有**） |

### 2.4 `dwd_industry_chain_news_info`

| 在线英文字段 | 在线要点 | Live Type / Null / Key | 差异 |
|---|---|---|---|
| — | — | `pk_id` + 六技术字段 | ❌ 仅 live |
| `industry_code` / `industry_name` | 长字符 | varchar(255) NO | 🔧 长度；编码系曾见 **`IC*`** vs 链表 **`INB*`**（挂链需对照/名称） |
| `id` | 字符 255 · 业务主键 | varchar(255) NO **UNI** | 🔧 物理键仍为 `pk_id` |
| `title` | 字符 255 | varchar(255) NO | ✅ |
| `publish_date` | 日期 | date NO | ✅ |
| `abstract` | 文本 | text YES | ✅ |
| `source` | 字符 500 可空 | varchar(500) YES | ✅ |

---

## 3. Demo ODS（`demo_gkxlumenx_ods`）相对两侧

| 项 | 说明 |
|---|---|
| 结构输入 | **只认在线 md-extract**（已 apply） |
| 相对在线 | `_demo_id`；超长→TEXT；业务键 KEY |
| 相对 live | 无六技术字段 / 无 `pk_id`；未按 JSON 形态约束 tags |
| 灌数 | 从三方抽数属后续；禁止用 live as-built 回写约定 DDL |

---

## 4. 开放项

| ID | 说明 | 状态 |
|---|---|---|
| OPEN-CHAIN-DIFF-01 | live `DESCRIBE` @ `183.240.141.251:3318` | **关闭**（2026-08-13） |
| OPEN-CHAIN-DIFF-02 | live 是否含 `product_top5` / `id` | **关闭**（均有；`id`=bigint 可空） |
| OPEN-CHAIN-DIFF-03 | 资讯 `IC*` ↔ 链表 `INB*` 对照 | 仍开放（业务挂链） |
| OPEN-CHAIN-DIFF-04 | 刷新/标注 `gkx_schema_ddl.sql` 产业链旧片段 | 仍开放 |

---

## 5. 指针

| 文档 | 路径 |
|---|---|
| 在线 MD | `doc/md-extract/市场研究（金融、宏观行业、行业分析、产业链）数据汇总表.md` §产业链要素库 |
| 三方连接 | `gkx-mysql-raw/CONNECTION.md`（密码仅 `.env.local`，不进 Git） |
| Live 快照 | `gkx-mysql-raw/加工/_chain_four_tables_live_2026-08-13.json` |
| Demo DDL | `storage/CHAIN/etl/demo_gkxlumenx_ods_chain_tables.sql` |
| 表清单 | [`inventory.md`](./inventory.md) |
