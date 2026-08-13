# 产业链 ODS → DWD 字段映射复核报告（Step 2）

> **现行存储入口（S4）**：[`../storage/CHAIN/README.md`](../storage/CHAIN/README.md) · DWD [`../storage/CHAIN/stores/mysql/dwd-chain.md`](../storage/CHAIN/stores/mysql/dwd-chain.md)  
> 本稿为 **Step2 复核过程稿**；目标 DWD = v5；Demo ODS 见 S2。冲突以 `storage/CHAIN` 为准。

> 任务：`CHAIN-INST-DATA-ANALYSIS-L01`  
> 责任人：`[human:李伟]`（架构师）  
> 执行角色：`agent:architect-agent`  
> 实时核验：2026-08-06（首轮）；**2026-08-07 上午**按 v5 修订字段复检并收口仅 4 表；**2026-08-07 15:23 再次实时复检（数据补入后）**；**2026-08-10 13:13 ODS 重新灌数后复检**；**2026-08-11 补入 IC-06 投融资灌数逻辑 + `event_entity_rel` 分流（投融资←ODS / 资讯←大模型）**  
> 目标 DWD：`产业链-DWD表设计-业务需求驱动(v5).md`（14 张表；含 08-07 的 `industry_id`/`chain_tier`/`phase_*`/`severity_level`/`event_kind`）  
> 入站源：MySQL `183.240.141.251:3318/gkx`，只读账号 `gkx_reader_zp`  
> **结构/资讯参考 ODS（4 张）**：  
> `dwd_industry_chain_info` / `dwd_org_industry_tags` / `dwd_org_industry_product_tags` / `dwd_industry_chain_news_info`  
> **投融资参考 ODS（IC-06，§0.5 / §4.6–4.7 / §4.10）**：  
> **必选** `dwd_org_financing_info` + `dwd_org_industry_tags`；**可选** `dwd_org_invest_info` / `dwd_org_base_info`；**首期不纳入**并购/公募基金/年报财务  
> **`event_entity_rel`**：投融资 ← ODS ETL；资讯 ← 大模型（§4.10 / §5.6）；不纳入「ODS 可灌」混判  
> **铁律**：除上述指定表外，其他供应方表**默认不参与可灌判断**；旁路表仅作「库内补数观察」，未经监管扩大范围前不得写入正式灌数结论。  
> **Q053**：2026-08-07 已冻结为 **INB 升格平台主键**（`DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md`），结构子集灌数不再因编码方案阻塞。  
> **IC-06 范围**：只要**投融资**，不强制并购；`investment_participant` 可空表。

---

## 0. 2026-08-10 13:13 复检摘要（ODS 重新灌数后）

### 0.1 四主源相对 08-07 15:23 基线

| ODS 表 | 08-07 15:23 | **08-10 13:13** | 差分 | 可灌结论变化 |
|---|---:|---:|---:|---|
| `dwd_industry_chain_info` | 1273 | **1273** | 0 | 无；L0=12 / L1=41 / 节点=1273 / 父子边=1261 / 父悬挂=0 |
| `dwd_org_industry_tags` | 20000 | **20000** | 0 | 无；仍 100% JSON 数组（`industry_code`/`industry_link_code`），`credit_code` 全非空、去重企业=20000 |
| `dwd_org_industry_product_tags` | 20000 | **20000** | 0 | 无；产品名全非空；`industry_link_code` 仍为 JSON/空形态（需拆行，产品 UID 待冻） |
| `dwd_industry_chain_news_info` | 1（无效） | **476** | **+475** | **结构字段已可用**；见下节编码缺口 |

结构未变要点：`chain_info` 最大 `updated_time` 仍为 `2026-07-31`；L0 样例仍为 INB1204/1209/1236/1303… 等 12 链。

### 0.2 资讯表（本轮唯一实质变化）

| 检查项 | 结果 |
|---|---|
| 有效行 `is_deleted=0` | **476** |
| `id` / `title` / 合法 `publish_date` 非空 | **476 / 476 / 476**（相对旧 1 行脏数据已修复） |
| `industry_code` 前缀 | **全部 `IC*`**（`IC0007` 集成电路 331；`IC9901` 低空经济 145） |
| 按码直连 `chain_info.industry_code` / `industry_link_code`（INB） | **0** |
| 按 `industry_name` 对齐 L0 名称 | **476**（名称可挂） |
| ETL「码一致即可灌」计数 | **0** |

> **资讯可灌性修订**：由 ❌「无效不可灌」改为 **🔧 可灌但必须做 IC→INB（或名称→L0 `industry_id`）对照**，不得把 `IC*` 写入平台主键（Q053=INB）。建议登记开放项：**资讯源码与 INB 对照表**（团队临时默认：名称匹配 L0；上线前甲方/数据 Lead 确认）。

### 0.3 对 v5 14 表可灌结论（相对 08-07）

| 目标 DWD | 08-07 | **08-10** | 说明 |
|---|---|---|---|
| `industry_chain` / `node` / `node_rel` | ✅ | ✅ | 不变 |
| `entity_rel`（企业） | 🔧 | 🔧 | tags JSON 拆行；不变 |
| `entity_rel`（产品） | 候选 | 候选 | 不变 |
| `news_event` | ❌ | **🔧** | 476 行可用正文；挂链靠名称/对照，非 INB 直连 |
| `market_observation` | ❌ 直灌 | ❌ | 市场规模仍走 ADS←ENT 年报 |
| `investment_event` + 投融资向 `event_entity_rel` | ❌ | **🔧 字段可灌 / ❌ 数据 0 行** | 正式源见 §4.6；`financing_info` 仍 **0**（Q054） |
| `investment_participant` | ❌ | **❌ 业务字段无源** | 无逐方金额；允许空表（§4.7） |
| 资讯向 `event_entity_rel` | — | **🧮 大模型** | 非 ODS；见 §4.10.2 / §5.6 |
| `event_metric_observation` | — | **🧮 后期埋点** | 无真实 ODS；见 §4.11 / §5.7 |
| 模型/抽取/里程碑等 | 🧮/❌ | 🧮/❌ | 抽取可审计落 `extraction_result` |

> **总判**：重新灌数后，**链/节点/企业标签底座结论不变**；**资讯正文可灌+编码映射**；投融资**字段路径已定、数据仍空**；**`event_entity_rel` 投融资←ODS、资讯←大模型**；**事件互动量←后期埋点，非 ODS**。

### 0.5 IC-06 投融资灌数 ODS 清单（2026-08-11 定稿）

> 需规 IC-06：**只要投融资，不强制并购**。对照 [金融要素库](https://docs.qq.com/sheet/DWWJRb2pIYk5nZ1hM?tab=ywbtpe)。

| 优先级 | ODS 表 | 是什么 | 灌数作用 |
|---|---|---|---|
| **必选** | `dwd_org_financing_info` | 融资事件 | → `investment_event`；拆主体/投资方 → 投融资向 `event_entity_rel` |
| **必选** | `dwd_org_industry_tags` | 企业×产业链标签（**不是**投资事件表） | 用信用代码挂 `chain_id` / 可选 `node_id` |
| 可选 | `dwd_org_invest_info` | 对外投资事件 | 缺业务日期，不能单独撑事件；日期补齐后作辅源 |
| 可选 | `dwd_org_base_info` | 企业基础信息 | `org_id`→信用代码/名称补全（融资表已有 `external_id` 时可少用） |
| **不纳入** | `dwd_org_merger_acquisition_info` 等并购表 | 并购 | IC-06 不要求 |
| **不纳入** | 公募基金 / 年报财务 / 国外持股 | 非投融资事件 | 禁止冒充 |

```text
financing_info ──► investment_event（总额/轮次/日期）
               └──► event_entity_rel（financing_subject + 拆 investors_name）
               └──► investment_participant（暂空：无逐方金额；允许空表）
industry_tags  ──► 补 chain_id / node_id
```

**字段路径：🔧 可灌；当前数据：❌ `financing_info` 有效行=0（Q054）。** 详见 §4.6 / §4.7 / §4.10 / §5.5。

---

## 0′. 2026-08-07 15:23 复检摘要（历史保留）

### 0′.1 四主源相对上午基线

| ODS 表 | 上午 `is_deleted=0` | 15:23 复检 | 差分 |
|---|---:|---:|---:|
| `dwd_industry_chain_info` | 1273 | **1273** | **0** |
| `dwd_org_industry_tags` | 20000 | **20000** | **0** |
| `dwd_org_industry_product_tags` | 20000 | **20000** | **0** |
| `dwd_industry_chain_news_info` | 1（无效） | **1（仍无效）** | **0** |

结构指标亦未变：L0=**12**、节点=**1273**、L1=**41**、父子边≈**1261**、父悬挂=**0**；tags 仍 100% JSON 数组；product 空节点链仍 **4792**。

资讯 live 当时仅 1 行：`id`/`industry_code` 空，`publish_date=0000-00-00`（**已被 08-10 批次取代，见 §0**）。

> **当时结论：四表行数与可灌性无变化。**（已被 §0 覆盖处除外）

### 0′.2 库内旁路补数观察（默认不纳入本轮灌数）

| 旁路表 | 15:23 有效行数 | 与 CHAIN 灌数关系 | 建议 |
|---|---:|---|---|
| `dwd_org_important_news_info` | **19983** | 企业级要闻；无产业链编码 | 扩围需经 `credit_code`→`entity_rel` |
| `dwd_org_annual_financial_info` | **5352**（含 `operating_revenue`） | 市场规模 ADS | 与 ENT 对齐 |
| `dwd_org_financing_info` | **0** | 结构可作 IC-06 主源；当时无数 | 维持等待灌数（见 §0.5） |

---

## 1. 分析口径

```text
结构/资讯 4 表 + IC-06 投融资正式源（§0.5）
  → 本项目 DWD industry_chain_* → ADS → Java/API
```

本报告判断：

- **结构/资讯底座**：上述 4 张表能否支撑链/节点/企业关系/资讯；
- **IC-06 投融资**：`financing_info` + `industry_tags`（+ 可选 `invest_info`）能否支撑 `investment_event` / 投融资向 `event_entity_rel` / `investment_participant`；
- **字段结构匹配** vs **当前实际可灌**（有结构无数仍标 ❌ 数据）；
- **门户 L0/L1 对齐**：ODS `level` 与 v5 `industry_id`/`chain_tier`。

| 状态 | 含义 |
|---|---|
| ✅ | 可直接映射 |
| 🔧 | 需拆行、关联、标准化或生成后映射 |
| 🟡 | 字段存在，但依赖跨域契约或其他开放项（非编码；**Q053 已于 2026-08-07 冻结为 INB**） |
| ❌ | 指定正式源无可用字段/数据 |
| 🧮 | 应由本项目 Python/系统生成，不由 ODS 直接提供 |

---

## 2. 四张表实时核验（**以 §0 2026-08-10 为准**；下表保留 08-07 快照供对照）

| ODS 表 | 有效行数（`is_deleted=0`）08-07 | **08-10** | 粒度 | 当前可用性（08-10） |
|---|---:|---:|---|---|
| `dwd_industry_chain_info` | 1273 | **1273** | 产业链节点行（含根节点） | ✅ 可灌链/节点/节点关系 |
| `dwd_org_industry_tags` | 20000 | **20000** | 企业×产业链标签（JSON 多值） | 🔧 可灌链—企业关系（需拆行） |
| `dwd_org_industry_product_tags` | 20000 | **20000** | 企业×产品×产业链标签（JSON 多值） | 🔧 可灌链—产品关系（需拆行；产品 UID 待冻结） |
| `dwd_industry_chain_news_info` | 1（无效） | **476** | 产业资讯 | 🔧 正文可用；**IC\* 码无法直连 INB**，需名称/对照表挂 L0 |

相对 08-06 / 08-07：**链与标签无变化；资讯由无效 1 行变为 476 行可映射灌数（见 §0.2）**。

### 2.1 `dwd_industry_chain_info`

| 指标 | 结果 |
|---|---|
| 产业链条数（`level=0`） | **12** |
| 节点数（`DISTINCT industry_link_code`） | **1273** |
| 层级范围 | 0～7 |
| `level=1` 节点数 | **41**（每条 L0 下 3～6 个） |
| 有父节点 | 1261 |
| 无父节点（根） | 12 |
| 父节点悬挂 | **0** |

12 条产业链（INB 编码，= 门户 L0 候选）：

| industry_code | industry_name | 节点数 | L1 子节点数 |
|---|---|---:|---:|
| INB1303 | 集成电路 | 257 | 6 |
| INB2503 | 生物医药 | 185 | 3 |
| INB1323 | 传感器 | 128 | 4 |
| INB1309 | 人工智能 | 108 | 3 |
| INB1333 | 智能终端 | 98 | 3 |
| INB1236 | 低空经济 | 96 | 4 |
| INB1306 | 软件与信息服务 | 92 | 3 |
| INB1204 | 机器人 | 91 | 3 |
| INB1354 | 具身智能 | 79 | 3 |
| INB1209 | 智能网联汽车 | 62 | 3 |
| INB2505 | 合成生物 | 40 | 3 |
| INB1502 | 数字创意 | 37 | 3 |

集成电路 L1 样例：

```text
INB1303 集成电路（level=0 → chain_tier=L0）
 ├── INB130301 半导体材料（level=1 → 门户 L1 候选）
 ├── INB130302 EDA/IP核
 ├── INB130303 半导体设备
 ├── INB130304 晶圆制造
 ├── INB130305 Fabless设计
 └── INB130306 封测
```

源字段：`pk_id, industry_code, industry_name, industry_link_code, industry_link_name, level, parent_code, parent_name, node_company_count, created_time, updated_time, creater, updater, table_data_source, is_deleted`。

说明：`node_company_count` 为聚合统计，**不得**写入 DWD 节点主表；企业规模进 ADS。

### 2.2 `dwd_org_industry_tags`

| 指标 | 结果 |
|---|---|
| 有效行数 | 20000 |
| 不重复企业（`credit_code`） | 20000 |
| `industry_code` / `industry_link_code` 形态 | **JSON 数组**（100%） |

样例：`industry_code=['INB1306']`，`industry_link_code=['INB130601', ...]`。  
ETL 必须拆行 → 多行 `industry_chain_entity_rel`。

### 2.3 `dwd_org_industry_product_tags`

| 指标 | 结果 |
|---|---|
| 有效行数 | 20000 |
| `industry_link_code` 为空数组 `[]` | **4792** |
| `product_name` | 文本列表，非标准产品 UID |

产品关系仅候选；`product_uid` 未冻结前不得作生产跨域主键。

### 2.4 `dwd_industry_chain_news_info`

仅 1 行且关键字段无效：

| 字段 | 当前值 |
|---|---|
| `industry_code` | 空 |
| `id` | 空 |
| `title` | 有文本 |
| `publish_date` | `0000-00-00`（非法） |
| `abstract` | NULL |

**结论（历史 08-07）：资讯不可灌。** 已被 **08-10 §0 / §4.8** 取代（476 行可映射灌）。

---

## 3. 对 v5 14 张目标表的总体可灌性

> 结构/资讯仍以 4 表为准；**投融资三表按 §0.5 IC-06 正式源**判定（不再写「4 表无字段」）。

| 目标 DWD 表 | 正式源是否覆盖 | 当前可灌结论 | 说明 |
|---|---|---|---|
| `industry_chain` | ✅ `chain_info` | ✅ 可灌 **12 条 L0**（可选再灌 41 条 L1） | **Q053 已冻结**：`chain_id=INB`；`industry_id`/`chain_tier` 可规则派生 |
| `industry_chain_node` | ✅ `chain_info` | ✅ 可灌 **1273**（或 L2+ 子集） | **Q053 已冻结**：`node_id=INB`；缺 stage/type/description |
| `industry_chain_node_rel` | ✅ `parent_code` | ✅ 约 **1261** 条父子 | 仅 `parent_child`；键按 Q053=INB |
| `industry_chain_entity_rel` | ✅ tags + product_tags | 🔧 企业可灌；产品候选 | JSON 拆行；产品 UID 待冻结；键=INB |
| `industry_chain_market_observation` | ❌ 外部观测无源 | ❌ 直灌 | **产业市场规模 = 🧮 企业年报营收加总 → ADS**，非 4 表直灌 |
| `industry_chain_investment_event` | ✅ `financing_info` + tags | **🔧 字段可灌 / ❌ 数据 0 行** | 见 §4.6；Q054 |
| `industry_chain_investment_participant` | ❌ 无逐方金额源 | **❌ 业务字段无源**（允许空表） | 见 §4.7；IC-06 不依赖本表有行 |
| `industry_chain_news_event` | 🔧 结构匹配 | **🔧** | **08-10：476 行正文可用**；源码为 `IC*`，需名称/对照挂 INB L0（见 §0.2） |
| `industry_chain_milestone_event` | ❌ ODS；✅ CMS 历程 | ❌ 直灌 | **产业发展历程 = CMS 录入**（门户真源）；DWD 表可选，4 表不灌 |
| `industry_chain_event_entity_rel` | 投融资向：✅ ODS；资讯向：🧮 大模型 | **投融资：🔧/❌ 等融资有数**；**资讯：🧮** | 见 §4.10；两路不混用 |
| `industry_chain_event_metric_observation` | ❌ 无 ODS | **🧮 后期埋点统计** | 浏览/评论/转发等；非 ODS 灌（§4.11 / §5.7） |
| `industry_chain_extraction_result` | 🧮 | 🧮 Python/大模型 | 资讯抽取审计；可喂 §4.10.2 |
| `industry_chain_model_run` | 🧮 | 🧮 系统 | — |
| `industry_chain_model_result_detail` | 🧮 | 🧮 Python | `severity_level` 等不由 ODS 灌 |

> **立即可灌（有数）**：产业链（L0/可选 L1）、节点、节点父子、链/节点—企业、资讯正文（需映射）。  
> **字段已定、等数据**：投融资事件 + **投融资向** `event_entity_rel`（等 `financing_info`>0）。  
> **算法写入（非 ODS）**：**资讯向** `event_entity_rel`（大模型分析资讯产出）。  
> **埋点写入（非 ODS）**：`event_metric_observation`（后期前端/服务埋点统计）。  
> **允许空表**：`investment_participant`。

---

## 4. 逐字段映射

表头约定：

| 列 | 含义 |
|---|---|
| 目标字段 | DWD 英文字段名 |
| 中文注释 | 与 v5 设计一致的字段中文名 |
| 来源表.字段 | 结构/资讯限 4 表；**§4.6–4.7 / §4.10 投融资向允许 §0.5 正式源** |
| 状态 | ✅ / 🔧 / 🟡 / ❌ / 🧮 |
| 当前可灌说明 | 映射规则与阻塞点 |

### 4.1 `industry_chain`（产业链标准信息表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `chain_id` | 产业链归一主键 | `dwd_industry_chain_info.industry_code`（L0）；方案 B 下 L1 用 `industry_link_code` | ✅ | **Q053**：INB 原文升格为平台主键（= `chain_code`） |
| `industry_id` | L0 产业对象主键 | 同上根级 `industry_code` | ✅ | L0 行 `industry_id=chain_id`（INB） |
| `chain_code` | 产业链来源编码 | `dwd_industry_chain_info.industry_code` / L1 的 `industry_link_code` | ✅ | 与 `chain_id` 同值 |
| `chain_name` | 产业链标准名称 | `industry_name`（L0）/ `industry_link_name`（方案 B 的 L1） | ✅ | 当前可灌 |
| `chain_short_name` | 产业链简称 | 无 | ❌ | 4 表无简称 |
| `parent_chain_id` | 上级产业链主键 | 方案 B：L1 行写根 `industry_code` | 🔧 | 方案 A 下全部为空；勿把 `parent_code`（节点父级）当上级链 |
| `chain_tier` | 产业对象层级 | 由 `level` 映射：`0→L0`，`1→L1` | 🔧 | 规则派生；与权限 persona 无关 |
| `chain_level` | 来源/树形数值层级 | `level`；L0 可默认 0 | 🔧 | 与 `chain_tier` 并存 |
| `chain_category` | 产业链分类 | 无 | ❌ | 需配置库/人工 |
| `future_industry_flag` | 未来产业标记 | 无 | ❌ | 需配置库/人工 |
| `description` | 产业链说明 | 无（门户介绍走 CMS） | ❌ | **产业介绍 = CMS 录入**，不由 4 表灌；本字段非门户真源 |
| `status` | 产业链有效状态 | `is_deleted` 派生 | 🔧 | `is_deleted=0` → active |

**L0/L1 方案（产品/架构择一）：**

| 方案 | `industry_chain` | `node` | 说明 |
|---|---|---|---|
| **A. 保守（可先灌）** | 12×L0 | 全量 1273 | 门户 L1 用 `node_level=1` 视图 |
| **B. 对齐门户对象** | 12×L0 + 41×L1 | `level≥2` | 需会签后切换 |

**当前结论：可灌 12 条 L0 基础身份，并可派生 `industry_id`/`chain_tier`；缺简称、分类、未来产业标记、说明。**

### 4.2 `industry_chain_node`（产业链节点信息表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `node_id` | 产业链节点归一主键 | `dwd_industry_chain_info.industry_link_code` | ✅ | **Q053**：INB 原文 = `node_code` |
| `chain_id` | 所属产业链主键 | `industry_code`（方案 B 可挂 L1 码） | ✅ | INB |
| `node_code` | 节点来源编码 | `industry_link_code` | ✅ | 与 `node_id` 同值；1273 个编码 |
| `node_name` | 节点标准名称 | `industry_link_name` | ✅ | 当前可灌 |
| `parent_node_id` | 父节点主键 | `parent_code` | ✅ | 1261 条有父；12 条根为空 |
| `node_level` | 节点层级 | `level` | ✅ | 0～7 |
| `stage_code` | 上中下游阶段编码 | 无 | ❌ | 需规则或字典 |
| `node_type` | 节点业务类型 | 无 | ❌ | 需配置/规则；五环节不在 4 表 |
| `importance_level` | 来源明确的节点重要等级 | 无 | ❌ | 禁止用 `node_company_count` 冒充 |
| `sort_no` | 同级节点排序号 | 无 | ❌ | 系统生成或配置 |
| `node_path` | 节点层级路径 | `parent_code` 递归派生 | 🔧 | 父节点完整，可递归生成 |
| `description` | 节点说明 | 无 | ❌ | 门户节点简介暂无 ODS 正文 |
| `status` | 节点有效状态 | `is_deleted` 派生 | 🔧 | 可派生 |

**当前结论：可灌编码、名称、所属链、父节点、层级；缺阶段、类型、简介；路径可派生。**

### 4.3 `industry_chain_node_rel`（产业链节点关系表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `relation_id` | 节点关系主键 | 无 | 🧮 | 按链、父、子、有效期生成，建议 `node-rel:` 前缀 |
| `chain_id` | 所属产业链主键 | `industry_code` | ✅ | **Q053**：INB |
| `source_node_id` | 关系起点节点主键 | `parent_code` | ✅ | 父节点 |
| `target_node_id` | 关系终点节点主键 | `industry_link_code` | ✅ | 子节点 |
| `relation_type` | 节点关系类型编码 | 常量 `parent_child` | 🧮 | 仅能覆盖父子；无供需/替代/协同 |
| `relation_direction` | 关系方向 | 常量 `directed` | 🧮 | 系统默认 |
| `relation_weight` | 来源明确的关系权重 | 无 | ❌ | — |
| `confidence` | 关系识别置信度 | 无 | ❌ | — |
| `evidence_ref` | 关系证据引用 | `source_table` + `pk_id` | 🔧 | 可拼装追溯 |

**当前结论：可派生约 1261 条父子关系；仅 `parent_child`。**

### 4.4 `industry_chain_entity_rel`（产业链实体关系表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `relation_id` | 产业链实体关系主键 | 无 | 🧮 | 业务字段指纹生成，建议 `chain-entity-rel:` 前缀 |
| `chain_id` | 所属产业链主键 | tags/product_tags 拆行后的 `industry_code` | 🔧 | JSON 拆行；码值按 Q053 保持 INB 原文 |
| `node_id` | 所属节点主键 | 拆行后的 `industry_link_code` | 🔧 | 空数组时仅挂链级 |
| `node_scope_key` | 链级或节点级关系去重键 | `COALESCE(node_id,'__CHAIN__')` | 🧮 | 生成列 |
| `entity_type` | 关联实体类型 | 企业=`enterprise`；产品=`product` | 🧮 | 按源表区分 |
| `entity_id` | 关联实体权威业务键 | 企业：`credit_code`→`enterprise_code`；产品：待 `product_uid` | 🔧/🟡 | 产品未冻结前仅候选 |
| `entity_subtype` | 实体细分类别 | 无 | ❌ | — |
| `relation_type` | 关系类型编码 | 企业 `participates_in`；产品 `produces` | 🧮 | 配置库登记编码 |
| `role_type` | 业务角色 | 无 | ❌ | — |
| `importance_level` | 来源明确的关系重要等级 | 无 | ❌ | — |
| `confidence` | 关系识别置信度 | 无 | 🧮 | 可空或规则默认 |
| `is_primary` | 是否主要归属 | 无 | ❌ | — |
| `evidence_ref` | 关系证据引用 | `pk_id` / 来源记录 | 🔧 | 可拼装 |

关系覆盖小结：

| 关系语义 | 中文说明 | 来源 | 状态 |
|---|---|---|---|
| 链/节点—企业 | 企业参与产业链或节点 | `dwd_org_industry_tags` JSON 拆行 | 🔧 可灌 |
| 链/节点—产品 | 产品归属产业链或节点 | `dwd_org_industry_product_tags` | 🔧 候选 |
| 人才/技术/政策/机构/专利 | 其他七要素 | 4 表无 | ❌ |

**当前结论：企业关系可灌（需拆行 + 企业键归一）；产品关系仅候选；其余实体类型本轮无源。**

### 4.5 `industry_chain_market_observation`（产业链市场指标观测表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| （整表）外部市场观测 | 研报/市调类原子观测 | 本轮 4 表无 | ❌ | 非本轮灌数范围 |
| — | — | — | 🧮 | **产业市场规模不走本表直灌** |

**平台「产业市场规模」口径（非直灌，2026-08-07 确认）：**

```text
Σ 该产业链下全部关联企业的年报营收
— 只计企业（entity_type=enterprise）
— 不计机构/人才/其他主体
— 计算层：ADS / 指标引擎（M_CHAIN_MARKET_SIZE）
— 输入：industry_chain_entity_rel（可由 tags 灌）+ ENT 域年报营收
```

| 步骤 | 依赖 | 本轮 4 表角色 |
|---|---|---|
| 1. 链—企业关系 | `dwd_org_industry_tags` → `entity_rel` | 🔧 可灌（拆行） |
| 2. 企业年报营收 | ENT 域年报表（不在 4 表内） | 本轮不映射 |
| 3. 加总出市场规模 | Python/指标任务写 ADS | 🧮 计算，禁止当 ODS 观测灌 DWD |

**当前结论：4 表不直灌市场规模；结构关系可支撑「链下企业集合」，营收加总属跨域计算，不是 ODS→DWD 灌数项。**

### 4.6 `industry_chain_investment_event`（产业链投融资事件表）

> **正式源**：`dwd_org_financing_info`（主）+ `dwd_org_industry_tags`（挂链）。  
> **可选辅源**：`dwd_org_invest_info`（缺 `event_date`，不能单独撑事件）。  
> **不纳入**：并购表（IC-06 不要求）。参考 [金融要素库](https://docs.qq.com/sheet/DWWJRb2pIYk5nZ1hM?tab=ywbtpe)。

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `event_id` | 投融资事件全域主键 | 无 | 🧮 | 系统生成 `invest:` 前缀 |
| `source_investment_id` | 来源投融资业务 ID | `financing_info` 行键或指纹 | 🔧 | 建议 `org_id|completion_date|funding_round|funding_amount` 指纹；有独立行键则直用 |
| `chain_id` | 所属产业链主键 | **不在融资表**；`external_id`/`credit_code` → `industry_tags` 拆行 → INB | 🔧 | **跨表必做**；挂不上链则不进生产链表（或进待审）；多链时产品定「主链一行 / 拆多行」 |
| `node_id` | 所属节点主键 | tags 拆行后的 `industry_link_code` | 🔧 | 可选；空数组仅挂链级 |
| `investment_type` | 资本事件类型 | 常量 | 🧮 | 融资行 → `financing`；辅源投资 → `investment`；**首期不做 `merger`** |
| `financing_round` | 融资轮次 | `dwd_org_financing_info.funding_round` | ✅ | 字段齐；当前源行=0 |
| `amount` | 事件总金额 | `funding_amount` | ✅ | 同上 |
| `currency` | 币种 | `funding_currency_code` | ✅ | 有金额则必填 |
| `event_date` | 事件发生日期 | `completion_date` | ✅ | **融资表可满足必填**；`invest_info` 无此字段故不能单独撑 |
| `region_code` | 关联区域 | 无（可经 base_info 补） | ❌/🔧 | 非阻塞，可空 |
| `description` | 事件说明 | 无 | ❌ | 可空 |
| `evidence_ref` | 证据引用 | 无 URL/公告链 | ❌ | 可空；可拼装源表+行键 |

辅源字段缺口：

| 源表 | 能否单独撑 `investment_event` | 卡点 |
|---|---|---|
| `dwd_org_invest_info` | **否** | 无业务发生日 → 必填 `event_date` 挂空 |
| `dwd_org_merger_acquisition_info` | **首期不做** | IC-06 不要求；且缺业务日、挂链弱 |

**当前结论：🔧 字段可灌 / ❌ 数据不可灌。** 结构路径已定；`financing_info` 有效行仍 **0**（Q054）。IC-06 最低闭环 = 本表 + 投融资向 `event_entity_rel`，**不依赖** `investment_participant` 有行。

### 4.7 `industry_chain_investment_participant`（产业链投融资参与方表）

> v5：角色只落在 `event_entity_rel.relation_type`；本表仅扩展单方金额。禁止双写角色。

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `participant_record_id` | 参与方扩展主键 | 无 | 🧮 | 系统生成 |
| `relation_id` | 关联事件—实体关系 | FK → `event_entity_rel` | 🧮 | 先有关系行再挂扩展 |
| `participation_amount` | 单个参与方金额 | **无** | ❌ | 金融要素库仅有事件总金额 + `investors_name` 名单，**无逐方金额** |
| `currency` | 单方币种 | 可继承事件币种 | 🔧 | 无单方金额则无意义 |

**当前结论：❌ 业务字段无源；允许空表。**  
`investors_name` 只支撑拆名 → `event_entity_rel`（`investor` 等），**不**支撑本表。IC-06 验收**不依赖**本表有行；等供应方提供「事件×投资方×出资金额」后再灌。

### 4.8 `industry_chain_news_event`（产业链资讯事件表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明（**08-10**） |
|---|---|---|---|---|
| `event_id` | 资讯事件全域主键 | 无 | 🧮 | 系统生成 `news:` 前缀 |
| `source_news_id` | 来源资讯业务 ID | `dwd_industry_chain_news_info.id` | ✅ | **476** 行均有非空 `id` |
| `chain_id` | 所属产业链主键 | `industry_code` + 对照 | 🔧 | 源码为 **`IC*`**（非 INB）；**按码直连失败=0**；按 `industry_name`↔L0 名称可挂 **476**；平台主键仍写 INB（Q053） |
| `node_id` | 所属节点主键 | 无 | ❌ | 资讯仅挂到产业/链级 |
| `title` | 资讯标题 | `title` | ✅ | 476 非空 |
| `summary` | 资讯摘要 | `abstract` | ✅ | 样例有正文 |
| `news_type` | 资讯类型 | 无 | ❌ | — |
| `source_name` | 来源媒体名称 | `source` | ✅ | 有值 |
| `author_name` | 作者名称 | 无 | ❌ | — |
| `source_url` | 原文链接 | 无 | ❌ | — |
| `source_url_hash` / `news_dedup_key` | 链接哈希 / 去重键 | 系统生成 | 🧮 | 可用 `id` 作去重 |
| `publish_time` | 发布时间 | `publish_date` | ✅ | **476** 合法日期（样例多为 2026-05-14） |
| `region_code` | 关联区域编码 | 无 | ❌ | — |

**当前结论（08-10）：🔧 可灌。** 正文质量已修复；挂链必须做 **IC→INB 或名称→L0** 映射，禁止把 `IC*` 写入 `chain_id`。覆盖面仅 2 个产业名称（集成电路 / 低空经济），非 12 链全覆盖。

> 历史（08-07）：曾仅 1 行且 `id`/码/日期无效 → ❌；已被本轮取代。

### 4.9 `industry_chain_milestone_event`（产业链里程碑事件表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| （门户发展历程） | 阶段 / 历程条目 / 图文 | **CMS 录入** | 🧮 CMS | **真源在 CMS**，不在本轮 4 表 ODS |
| `event_id` 等 DWD 结构化字段 | 可选结构化里程碑 | 4 表无 | ❌ | 本轮不灌；非门户历程必选路径 |
| `phase_id` / `phase_name` / `phase_sort_no` | 发展阶段编码/名称/排序 | CMS（若结构化旁路） | ❌/CMS | 门户阶段文案以 CMS 为准 |

**当前结论：产业发展历程由 CMS 录入展示；4 表 ODS 不灌里程碑；DWD `milestone_event` 非本轮灌数项。**

### 4.10 `industry_chain_event_entity_rel`（产业事件实体关系表）

> 本表复用投融资 / 资讯 / 里程碑。**写入路径按事件域分流，不混用同源。**

| 事件域 | 写入路径 | 说明 |
|---|---|---|
| 投融资 `invest` | **ODS ETL**（§0.5 / §4.6） | 融资表拆主体/投资方 → 本表 |
| 资讯 `news` | **大模型分析资讯产出**（Python） | ODS 资讯只进 `news_event` 正文；实体关系不由 ODS 直灌 |
| 里程碑 `milestone` | CMS / 人工或后置抽取 | 本轮 ODS 不灌 |

#### 4.10.1 投融资向（ODS 可灌，正式源 = §0.5）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `relation_id` | 事件实体关系主键 | 无 | 🧮 | `event-entity-rel:` 前缀 |
| `event_id` | 关联事件全域主键 | ← 已生成的 `investment_event.event_id` | 🔧 | **先有事件行**；ETL 校验 `invest:` 存在 |
| `event_kind` | 事件域冗余分类 | 常量 `invest` | 🧮 | 必须与 `event_id` 前缀一致 |
| `entity_type` | 关联实体类型 | 规则 | 🧮 | 企业 `enterprise`；机构 `institution`（投资方归一后） |
| `entity_id` | 关联实体权威业务键 | 主体：`financing_info.external_id`（或经 `base_info`）；投资方：拆 `investors_name` 后归一 | 🔧 | 主体键优先信用代码；投资方名称归一另定规则 |
| `relation_type` | 事件—实体关系类型 | 规则 | 🧮 | `financing_subject` ← 融资企业；`investor` ← 拆名单（源无领投标记时勿臆造 `lead_investor`） |
| `confidence` / `evidence_ref` | 置信度 / 证据 | 可空或拼装源行 | 🔧 | — |

投融资角色灌数：

```text
financing_info.external_id     → relation_type=financing_subject
financing_info.investors_name  → 按分隔符拆分 → 多行 investor
（禁止把角色再写入 investment_participant）
```

**投融资向结论：🔧 ODS 字段可灌 / ❌ 当前无事件可挂（融资表 0 行）。**

#### 4.10.2 资讯向（大模型写入，非 ODS 直灌）

```text
news_event（可由 ODS 灌正文）
    → Python / 大模型分析标题+摘要(+正文)
    → （可选）落 extraction_result 审计
    → 归一实体权威键后写入 event_entity_rel
         event_kind=news
         relation_type 如 author / publisher / mentioned_enterprise / …
```

| 目标字段 | 状态 | 说明 |
|---|---|---|
| `event_id` | 🧮 | 必须已存在 `news:` 事件 |
| `event_kind` | 🧮 | 固定 `news` |
| `entity_type` / `entity_id` / `relation_type` | 🧮 模型 | **不从 ODS 资讯表直拷**；由模型抽取 + 实体归一 |
| `confidence` / `evidence_ref` | 🧮 模型 | 建议带置信度与句段/证据引用 |

| 方向 | 状态 | 说明 |
|---|---|---|
| 资讯事件—实体关系 | **🧮 算法写入** | ODS 无结构化「事件→权威实体键」；署名原文 ≠ 本表 |
| 里程碑相关主体 | ❌/CMS | 历程真源 CMS；本轮 ODS 不灌 |

**整表结论：**
- **投融资向**：ODS 路径已定，等 `financing_info` 有数；
- **资讯向**：明确走大模型产出写入，**不纳入 ODS→DWD 可灌判定**；
- 里程碑向：CMS，本轮不灌。

### 4.11 `industry_chain_event_metric_observation`（产业事件指标观测表）

> **无真实 ODS 数据源。** 已定：读取**后期埋点统计**（前端 `observability` / 服务端点击与互动埋点聚合），不从供应方表直灌。

| 目标字段 | 中文注释 | 来源 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `observation_id` | 事件指标观测主键 | 埋点聚合任务生成 | 🧮 | 系统 |
| `event_id` | 被观测事件全域主键 | 已存在的 `news:` / 其他事件 ID | 🔧 | 须先有事件主表行 |
| `metric_id` / `metric_version` | 互动指标编码与口径版本 | 指标配置库 | 🧮 | 浏览/评论/转发/点赞等 |
| `observed_time` | 指标采集时间 | 埋点聚合窗口时刻 | 🧮 | — |
| `metric_value` | 原子观测值 | 埋点计数聚合 | 🧮 | — |
| `unit` | 指标单位 | 配置 | 🧮 | 次、条等 |
| `metric_observation_scope_key` | 防重指纹 | 按 v5 规则计算 | 🧮 | — |

**当前结论：🧮 非 ODS 灌数。** 首期可空表；热点排序（IC-09/IC-19）待埋点上线后再写本表。禁止用 Mock 互动量冒充生产观测而不标来源。

### 4.12 `industry_chain_extraction_result`（产业链抽取结果表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `extraction_id` / `result_fingerprint` 等 | 实体/关系抽取可审计结果 | 无直接灌数字段 | 🧮 | 由 Python/大模型产出；**资讯→`event_entity_rel` 的推荐审计落点**（§4.10.2） |

**当前结论：🧮 不由 ODS 直接灌。** 资讯正文入 `news_event` 后，抽取结果可先落本表再归一写入资讯向 `event_entity_rel`。

### 4.13 `industry_chain_model_run`（产业链模型运行表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `run_id` / `model_id` / `model_version` 等 | 模型运行元数据 | 无 | 🧮 | 算法平台/系统生成 |

**当前结论：🧮 不由 ODS 灌。**

### 4.14 `industry_chain_model_result_detail`（产业链模型结果明细表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `result_id` / `result_value` / `result_label` 等 | 评分、标签、排名、预测、贡献等原子结果 | 无 | 🧮 | Python 产出 |
| `severity_level` | 严重度等级编码 | 无 | 🧮 | 诊断卡脖子用；不由 4 表提供 |
| `result_fingerprint` | 模型结果防重指纹 | 无 | 🧮 | 系统按 v5 规则计算 |

**当前结论：🧮 不由 ODS 灌。**

---

## 5. ETL 实施要点（可灌子集）

### 5.1 链与节点（建议先方案 A）

1. `level=0` → 12 条 `industry_chain`：`chain_tier='L0'`，`industry_id=chain_id←industry_code`；  
2. 全量 1273 → `industry_chain_node`；  
3. `parent_code` 非空 → `node_rel`（~1261，`parent_child`）；  
4. **Q053 已冻结**：`chain_id`/`node_id`/`industry_id` 直接写 INB 原文（与 code 同值）；生产批次校验 `^INB[0-9]+$`；  
5. 方案 B（41 条 L1）待会签后再切换。

### 5.2 企业 / 产品标签

JSON 拆行；企业 `credit_code` 归一；产品待 `product_uid`；4792 行空节点只挂链级。

### 5.3 资讯

08-10 起可灌 **476** 行正文进 `news_event`：ETL 用 `id` 去重，用 **名称匹配 L0**（临时默认）或 **IC↔INB 对照表** 写 `chain_id=INB`；勿直写 `IC*`。覆盖目前仅「集成电路」「低空经济」两产业。

**资讯向 `event_entity_rel` 不走本 ODS ETL**：见 §5.6。

### 5.4 本轮明确不灌的 v5 新字段

| 字段 | 中文注释 | 处理 |
|---|---|---|
| `phase_id` / `phase_name` / `phase_sort_no` | 发展阶段编码 / 名称 / 排序号 | 门户历程阶段在 **CMS**；DWD 可选旁路 |
| `severity_level` | 严重度等级编码 | 算法结果 |
| `event_kind` | 事件域冗余分类 | 有事件后系统生成 |
| `future_industry_flag` | 未来产业标记 | 配置库或规则 |
| `stage_code` / `node_type` | 上中下游阶段 / 节点业务类型 | 配置库或规则 |
| 产业介绍正文 | — | **CMS 录入**（按 industry_id/chain_id） |
| 产业发展历程 | — | **CMS 录入**（门户真源） |

### 5.5 IC-06 投融资（等 `financing_info` 有数后启用）

```text
1. 过滤 dwd_org_financing_info（is_deleted=0；completion_date 合法；尽量有金额或轮次）
2. external_id（或 org→credit）JOIN dwd_org_industry_tags
   → 拆 JSON 得 chain_id(=INB) / 可选 node_id
   → 挂不上链：不进生产 investment_event（或待审队列）
3. 写 investment_event：
     investment_type=financing
     financing_round/amount/currency/event_date ← 融资表字段
     event_id=invest:…
4. 写 event_entity_rel（event_kind=invest）：
     financing_subject ← 融资企业权威键
     investor ← 拆 investors_name（无领投标记勿写 lead_investor）
5. investment_participant：默认不建行（无逐方金额；IC-06 无单方金额业务硬需求）
6. 可选第二批：invest_info（补齐业务日期后）；禁止并购冒充 IC-06
```

供应方验收门槛（建议）：有效行>0；`completion_date`、`external_id`、(`funding_amount` 或 `funding_round`) 非空率可验收；`external_id` 能关联到带产业链标签的企业。

### 5.6 资讯向 `event_entity_rel`（大模型，非 ODS 灌数）

```text
1. 已存在 news_event（ODS 灌正文，§5.3）
2. Python / 大模型分析 title + summary（+ 正文若有）
3. （推荐）先写 extraction_result 留审计
4. 实体归一为权威键后写 event_entity_rel：
     event_kind=news
     relation_type：author / publisher / mentioned_enterprise / …（配置库登记）
5. 禁止用 ODS 资讯表字段「冒充」权威实体关系行
```

调用链仍遵守：算法只在 Python；前端不直连模型写 DWD。

### 5.7 事件互动指标观测（后期埋点，非 ODS）

```text
1. 前端 observability / 服务端埋点上报（浏览、评论、转发、点赞等）
2. 聚合任务按 event_id + metric_id + 时间窗汇总
3. 写入 event_metric_observation（含 metric_observation_scope_key 防重）
4. 无埋点上线前：本表允许空；禁止用供应方 ODS 或无来源 Mock 冒充生产观测
```

不纳入 ODS→DWD 可灌判定；热点排序（IC-09/IC-19）依赖本链路就绪。

---

## 6. 最终判断（**2026-08-11 更新**：结构/资讯 4 表 + IC-06 投融资源）

> **结构/资讯正文**：v5 骨架与企业关系可部分落地；资讯可灌但须 IC/名称→INB。  
> **投融资（IC-06）**：**正式源已定** = `dwd_org_financing_info` + `dwd_org_industry_tags`；字段路径可灌，融资行仍 0；`participant` 允许空表；不含并购。  
> **`event_entity_rel` 分流**：投融资 ← ODS；资讯 ← **大模型**（非 ODS 可灌项）。  
> **`event_metric_observation`**：无 ODS；**后期埋点统计**写入（§4.11 / §5.7）。  
> 产业介绍/历程 = CMS；市场规模 = Σ 链下企业年报 → ADS。

### 6.1 现在就能做的

1. **12** 条 L0 产业链（含派生 `industry_id`/`chain_tier`）；  
2. （可选会签）**41** 条 L1 子链；  
3. **1273** 节点；  
4. **约 1261** 父子关系；  
5. **最多 20000 家企业**的链/节点关系候选（拆行后行数放大）；  
6. 产品关系候选（主键冻结后生产化）；  
7. **资讯事件约 476 条**（挂 L0；需映射；覆盖 2 产业）。

### 6.2 核心缺口

| 优先级 | 缺口 | 影响 |
|---|---|---|
| P0 | 资讯源码 `IC*` ≠ INB；缺正式对照表 | `news_event.chain_id` 映射 |
| P0 | `dwd_org_financing_info` 有效行 **0** | IC-06 / Q054：字段齐、数据未到 |
| P1 | 产业市场规模：ENT 年报字段与统计年口径 | QC06 / ADS |
| P1 | L0/L1 方案 A vs B 未会签 | 门户对象合同 |
| P1 | tags JSON 拆行 | ETL 正确性 |
| P1 | `product_uid` 未冻结 | 产品关系生产化 |
| P2 | 资讯仅覆盖 2 个产业名称 | 资讯面不全 |
| P2 | 无逐方出资金额源 | `investment_participant` 长期空（已允许；业务无硬需求） |
| P2 | `invest_info` 缺业务日期 | 投资辅源暂不可单独撑事件 |
| P2 | 资讯向 `event_entity_rel` 算法链路未落地 | 大模型抽取 + 实体归一（非 ODS 缺口） |
| P2 | 事件互动埋点未上线 | `event_metric_observation` 暂空（§5.7；非 ODS） |
| — | 产业介绍 / 发展历程 | **已定 CMS 录入** |
| P2 | 抽取/模型/severity | 算法链路 |
| ~~P0~~ | ~~Q053 编码归一~~ | **已关闭 🟢** |
| ~~P0~~ | ~~资讯 live 整表无效~~ | **08-10 已缓解 → 映射问题** |
| ~~P0~~ | ~~「4 表无投融资字段」~~ | **08-11 已收口：正式源 = financing + tags** |

### 6.3 建议下一步

1. 落地方案 A：`industry_chain` + `node` + `node_rel` + 企业 `entity_rel`（**按 INB 主键**）；  
2. 会签是否升级方案 B；  
3. **冻结资讯 IC↔INB（或名称）对照** 后灌 `news_event`；要求供应方后续直接给 INB；  
4. **投融资**：催供应方灌 `dwd_org_financing_info`；有数后按 §5.5 灌 `investment_event` + 投融资向 `event_entity_rel`；`participant` 默认可空；  
5. **资讯实体关系**：按 §5.6 由大模型分析资讯写入 `event_entity_rel`（可经 `extraction_result`）；  
6. **事件互动观测**：埋点上线后按 §5.7 写 `event_metric_observation`（首期可空）；  
7. 产业市场规模：对接 ENT 年报字段后做 ADS 计算（非 ODS 直灌）；  
8. 产业介绍 / 发展历程：走 CMS 运营录入（非本轮灌数）；  
9. 历史国标 Mock：迁移到 INB 或 `source_system=mock` 隔离，禁止与生产 INB 混关联。

---

## 7. 相对先前稿的收口说明

| 项 | 处理 |
|---|---|
| 结构/资讯 4 表 | 仍为链/节点/标签/资讯底座 |
| **2026-08-11 IC-06** | 投融资正式源升级纳入 `financing_info`；`industry_tags` **双用**（企业关系 + 挂链）；不含并购 |
| **`event_entity_rel` 分流** | 投融资 ← ODS ETL；资讯 ← 大模型写入（§4.10 / §5.6）；禁止混用同源 |
| **`event_metric_observation`** | 无 ODS；后期埋点统计（§4.11 / §5.7）；首期可空 |
| 2026-08-07 15:23 复检 | **4 表差分全 0**（当时） |
| **2026-08-10 复检** | **资讯 1→476**；链/标签不变；融资旁路仍 0 |
| 旁路 `dwd_org_important_news_info`（19983） | 企业要闻；无链码，默认不灌 CHAIN 资讯事件 |
| 旁路 `dwd_org_annual_financial_info`（5352） | 市场规模 ADS 原料 |
| Q054 | 修订表述：**正式源已定，融资有效行仍 0**（不再写「4 表无字段」） |
| `investment_participant` | 范式保留；首期允许空表；非 IC-06 DoD |
| 可灌主结论 | 链/节点/父子/企业关系不变；资讯 🔧；投融资 **🔧 字段 / ❌ 数据** |
