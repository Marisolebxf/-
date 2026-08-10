# 产业链 ODS → DWD 字段映射复核报告（Step 2）

> 任务：`CHAIN-INST-DATA-ANALYSIS-L01`  
> 责任人：`[human:李伟]`（架构师）  
> 执行角色：`agent:architect-agent`  
> 实时核验：2026-08-06（首轮）；**2026-08-07 上午**按 v5 修订字段复检并收口仅 4 表；**2026-08-07 15:23 再次实时复检（数据补入后）**；**2026-08-10 13:13 ODS 重新灌数后复检**  
> 目标 DWD：`产业链-DWD表设计-业务需求驱动(v5).md`（14 张表；含 08-07 的 `industry_id`/`chain_tier`/`phase_*`/`severity_level`/`event_kind`）  
> 入站源：MySQL `183.240.141.251:3318/gkx`，只读账号 `gkx_reader_zp`  
> **本轮唯一参考 ODS（仅 4 张）**：  
> `dwd_industry_chain_info` / `dwd_org_industry_tags` / `dwd_org_industry_product_tags` / `dwd_industry_chain_news_info`  
> **铁律**：其他供应方表**默认不参与可灌判断**；旁路表仅作「库内补数观察」，未经监管扩大范围前不得写入正式灌数结论。  
> **Q053**：2026-08-07 已冻结为 **INB 升格平台主键**（`DEC-CHAIN-Q053-CODE-NORMALIZATION-20260807.md`），结构子集灌数不再因编码方案阻塞。

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
| `investment_*` | ❌ | ❌ | 旁路 `dwd_org_financing_info` 有效行仍 **0** |
| 模型/抽取/里程碑等 | 🧮/❌ | 🧮/❌ | 不变 |

### 0.4 旁路观察（仍不纳入 4 表灌数结论）

| 旁路表 | 08-10 有效行 | 备注 |
|---|---:|---|
| `dwd_org_important_news_info` | 19983 | 无链码；默认不灌 CHAIN 资讯事件 |
| `dwd_org_annual_financial_info` | 5352（均含 `operating_revenue`） | 市场规模 ADS 原料 |
| `dwd_org_financing_info` | **0** | Q054 维持 |

> **总判**：重新灌数后，**链/节点/企业标签底座结论不变**；**资讯从不可灌变为「可灌+编码映射」**；投融资仍无源。

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
| `dwd_org_financing_info` | **0** | 投融资不可灌 | 维持 Q054 |

---

## 1. 分析口径

```text
上述 4 张供应方表 → 本项目 DWD industry_chain_* → ADS → Java/API
```

本报告只判断这 4 张表能否支撑 v5 14 张 DWD：

- **字段结构匹配**：源字段能否映射到目标 DWD（含 2026-08-07 新增字段）；
- **当前实际可灌**：源表当前是否存在有效数据；
- **门户 L0/L1 对齐**：ODS `level` 与 v5 `industry_id`/`chain_tier` 如何落地。

| 状态 | 含义 |
|---|---|
| ✅ | 可直接映射 |
| 🔧 | 需拆行、关联、标准化或生成后映射 |
| 🟡 | 字段存在，但依赖跨域契约或其他开放项（非编码；**Q053 已于 2026-08-07 冻结为 INB**） |
| ❌ | 本轮 4 表无可用字段/数据 |
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

## 3. 对 v5 14 张目标表的总体可灌性（仅基于 4 表）

| 目标 DWD 表 | 4 表是否覆盖 | 当前可灌结论 | 说明 |
|---|---|---|---|
| `industry_chain` | ✅ `chain_info` | ✅ 可灌 **12 条 L0**（可选再灌 41 条 L1） | **Q053 已冻结**：`chain_id=INB`；`industry_id`/`chain_tier` 可规则派生 |
| `industry_chain_node` | ✅ `chain_info` | ✅ 可灌 **1273**（或 L2+ 子集） | **Q053 已冻结**：`node_id=INB`；缺 stage/type/description |
| `industry_chain_node_rel` | ✅ `parent_code` | ✅ 约 **1261** 条父子 | 仅 `parent_child`；键按 Q053=INB |
| `industry_chain_entity_rel` | ✅ tags + product_tags | 🔧 企业可灌；产品候选 | JSON 拆行；产品 UID 待冻结；键=INB |
| `industry_chain_market_observation` | ❌ 外部观测无源 | ❌ 直灌 | **产业市场规模 = 🧮 企业年报营收加总 → ADS**，非 4 表直灌 |
| `industry_chain_investment_event` | ❌ | ❌ | 4 表无投融资字段 |
| `industry_chain_investment_participant` | ❌ | ❌ | 同上 |
| `industry_chain_news_event` | 🔧 结构匹配 | **🔧** | **08-10：476 行正文可用**；源码为 `IC*`，需名称/对照挂 INB L0（见 §0.2） |
| `industry_chain_milestone_event` | ❌ ODS；✅ CMS 历程 | ❌ 直灌 | **产业发展历程 = CMS 录入**（门户真源）；DWD 表可选，4 表不灌 |
| `industry_chain_event_entity_rel` | ❌ | ❌ | 依赖有效事件 |
| `industry_chain_event_metric_observation` | ❌ | ❌ | 无互动量 |
| `industry_chain_extraction_result` | 🧮 | 🧮 Python | — |
| `industry_chain_model_run` | 🧮 | 🧮 系统 | — |
| `industry_chain_model_result_detail` | 🧮 | 🧮 Python | `severity_level` 等不由 ODS 灌 |

> **4 表可立即支撑：产业链（L0/可选 L1）、节点、节点父子关系、链/节点—企业关系，以及产品关系候选。其余 10 张目标表本轮不可由这 4 表灌入。**

---

## 4. 逐字段映射（仅 4 表）

表头约定：

| 列 | 含义 |
|---|---|
| 目标字段 | DWD 英文字段名 |
| 中文注释 | 与 v5 设计一致的字段中文名 |
| 来源表.字段 | 仅允许出自本轮 4 张 ODS；无则写「无」 |
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

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `event_id` 等业务字段 | 投融资事件全域主键及金额/轮次等 | 无 | ❌ | 4 表无投融资字段 |

**当前结论：❌ 不可灌。**

### 4.7 `industry_chain_investment_participant`（产业链投融资参与方表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `relation_id` 等 | 参与方扩展（金额份额等） | 无 | ❌ | 依赖投融资事件；4 表无 |

**当前结论：❌ 不可灌。**

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

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `relation_id` | 事件实体关系主键 | 无 | ❌ | 依赖有效事件 |
| `event_id` | 关联事件全域主键 | 无 | ❌ | — |
| `event_kind` | 事件域冗余分类 | 无 | ❌ | 有事件后由系统按前缀写入 |
| `entity_type` / `entity_id` / `relation_type` | 实体类型 / 键 / 关系类型 | 无 | ❌ | — |

**当前结论：❌ 不可灌。**

### 4.11 `industry_chain_event_metric_observation`（产业事件指标观测表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `observation_id` 等 | 浏览量/评论量/转发量等时序观测 | 无 | ❌ | 4 表无互动量字段 |

**当前结论：❌ 不可灌。**

### 4.12 `industry_chain_extraction_result`（产业链抽取结果表）

| 目标字段 | 中文注释 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `extraction_id` / `result_fingerprint` 等 | 实体/关系抽取可审计结果 | 无直接灌数字段 | 🧮 | 由 Python 产出；资讯修复后仅可作输入文档候选 |

**当前结论：🧮 不由 ODS 直接灌。**

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

08-10 起可灌 **476** 行：ETL 用 `id` 去重，用 **名称匹配 L0**（临时默认）或 **IC↔INB 对照表** 写 `chain_id=INB`；勿直写 `IC*`。覆盖目前仅「集成电路」「低空经济」两产业。

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

---

## 6. 最终判断（**2026-08-10 更新** · 仅 4 表）

> **仅依据上述 4 张表：v5 结构骨架与企业关系可部分落地；`industry_id`/`chain_tier` 可用 `level` 派生；`phase_*`/`severity_level` 无法从这 4 表灌入。投融资、互动量、抽取与模型结果仍不可由这 4 表灌入。资讯（08-10）可灌但须 IC/名称→INB 映射。产业介绍与发展历程为 CMS 录入。产业市场规模为跨域计算（Σ 链下企业年报营收 → ADS）。其他供应方表本轮不纳入判断。**

### 6.1 现在就能做的

1. **12** 条 L0 产业链（含派生 `industry_id`/`chain_tier`）；  
2. （可选会签）**41** 条 L1 子链；  
3. **1273** 节点；  
4. **约 1261** 父子关系；  
5. **最多 20000 家企业**的链/节点关系候选（拆行后行数放大）；  
6. 产品关系候选（主键冻结后生产化）；  
7. **资讯事件约 476 条**（挂 L0；需映射；覆盖 2 产业）。

### 6.2 核心缺口（相对 4 表）

| 优先级 | 缺口 | 影响 |
|---|---|---|
| P0 | 资讯源码 `IC*` ≠ INB；缺正式对照表 | `news_event.chain_id` 映射 |
| P0 | 4 表无投融资字段 | IC-06 / Q054 |
| P1 | 产业市场规模：ENT 年报字段与统计年口径 | QC06 / ADS |
| P1 | L0/L1 方案 A vs B 未会签 | 门户对象合同 |
| P1 | tags JSON 拆行 | ETL 正确性 |
| P1 | `product_uid` 未冻结 | 产品关系生产化 |
| P2 | 资讯仅覆盖 2 个产业名称 | 资讯面不全 |
| — | 产业介绍 / 发展历程 | **已定 CMS 录入** |
| P2 | 抽取/模型/severity | 算法链路 |
| ~~P0~~ | ~~Q053 编码归一~~ | **已关闭 🟢** |
| ~~P0~~ | ~~资讯 live 整表无效~~ | **08-10 已缓解 → 映射问题** |

### 6.3 建议下一步

1. 落地方案 A：`industry_chain` + `node` + `node_rel` + 企业 `entity_rel`（**按 INB 主键**）；  
2. 会签是否升级方案 B；  
3. **冻结资讯 IC↔INB（或名称）对照** 后灌 `news_event`；要求供应方后续直接给 INB；  
4. 投融资：另开任务与另定源表（4 表无字段）；  
5. 产业市场规模：对接 ENT 年报字段后做 ADS 计算（非 ODS 直灌）；  
6. 产业介绍 / 发展历程：走 CMS 运营录入（非本轮灌数）；  
7. 历史国标 Mock：迁移到 INB 或 `source_system=mock` 隔离，禁止与生产 INB 混关联。

---

## 7. 相对先前稿的收口说明

| 项 | 处理 |
|---|---|
| 融资 / bak 资讯 / 专利等其他表 | **默认不参与**可灌结论；旁路仅观察 |
| 2026-08-07 15:23 复检 | **4 表差分全 0**（当时） |
| **2026-08-10 复检** | **资讯 1→476**；链/标签不变；投融资仍 0 |
| 旁路 `dwd_org_important_news_info`（19983） | 企业要闻；无链码，默认不灌 CHAIN 资讯事件 |
| 旁路 `dwd_org_annual_financial_info`（5352） | 市场规模 ADS 原料 |
| Q054 | 投融资仍「4 表无字段 + 旁路融资表有效行 0」 |
| 可灌主结论 | 链/节点/父子/企业关系不变；**资讯改为 🔧 可映射灌** |
