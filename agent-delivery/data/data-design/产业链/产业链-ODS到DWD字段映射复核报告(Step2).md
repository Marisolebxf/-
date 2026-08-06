# 产业链 ODS → DWD 字段映射复核报告（Step 2）

> 任务：`CHAIN-INST-DATA-ANALYSIS-L01`  
> 责任人：`[human:李伟]`（架构师）  
> 执行角色：`agent:architect-agent`  
> 实时核验：2026-08-06  
> 目标 DWD：`产业链-DWD表设计-业务需求驱动(v5).md`（14 张表）  
> 入站源：MySQL `183.240.141.251:3318/gkx`，只读账号 `gkx_reader_zp`  
> **本轮主数据源（4 张）**：`dwd_industry_chain_info` / `dwd_org_industry_tags` / `dwd_org_industry_product_tags` / `dwd_industry_chain_news_info`

---

## 1. 分析口径

```text
供应方 gkx.dwd_*（本轮聚焦 4 张） → 本项目 DWD industry_chain_* → ADS → Java/API
```

本报告同时判断：

- **字段结构匹配**：源字段能否映射到目标 DWD；
- **当前实际可灌**：源表当前是否存在有效数据。

| 状态 | 含义 |
|---|---|
| ✅ | 可直接映射 |
| 🔧 | 需拆行、关联、标准化或生成后映射 |
| 🟡 | 字段存在，但依赖编码/业务键/跨域契约（含 Q053） |
| ❌ | 当前 4 张主源无可用字段 |
| 🧮 | 应由本项目 Python/系统生成，不由 ODS 直接提供 |

---

## 2. 四张主源实时核验

| ODS 表 | 有效行数（`is_deleted=0`） | 粒度 | 当前可用性 |
|---|---:|---|---|
| `dwd_industry_chain_info` | **1273** | 产业链节点行（含根节点） | ✅ 可灌链/节点/节点关系 |
| `dwd_org_industry_tags` | **20000** | 企业×产业链标签（JSON 多值） | 🔧 可灌链—企业关系（需拆行） |
| `dwd_org_industry_product_tags` | **20000** | 企业×产品×产业链标签（JSON 多值） | 🔧 可灌链—产品关系（需拆行；产品 UID 待冻结） |
| `dwd_industry_chain_news_info` | **1** | 产业资讯 | ❌ 当前无效，不可灌 |

### 2.1 `dwd_industry_chain_info` 覆盖

| 指标 | 结果 |
|---|---|
| 产业链条数（`level=0`） | **12** |
| 节点数（`DISTINCT industry_link_code`） | **1273** |
| 链—节点对 | 1273 |
| 层级范围 | 0～7 |
| 有父节点 | 1261 |
| 无父节点（根） | 12 |
| 父节点悬挂 | **0** |

12 条产业链（INB 编码）：

| industry_code | industry_name | 节点数 |
|---|---|---:|
| INB1303 | 集成电路 | 257 |
| INB2503 | 生物医药 | 185 |
| INB1323 | 传感器 | 128 |
| INB1309 | 人工智能 | 108 |
| INB1333 | 智能终端 | 98 |
| INB1236 | 低空经济 | 96 |
| INB1306 | 软件与信息服务 | 92 |
| INB1204 | 机器人 | 91 |
| INB1354 | 具身智能 | 79 |
| INB1209 | 智能网联汽车 | 62 |
| INB2505 | 合成生物 | 40 |
| INB1502 | 数字创意 | 37 |

结构样例（机器人链）：

```text
INB1204 机器人（level=0）
 ├── INB120401 零部件（level=1）
 │    ├── INB12040101 核心零部件（level=2）
 │    └── ...
 ├── INB120402 本体制造（level=1）
 └── INB120403 整机集成（level=1）
```

### 2.2 `dwd_org_industry_tags` 覆盖

| 指标 | 结果 |
|---|---|
| 有效行数 | 20000 |
| 不重复企业（`credit_code`） | 20000 |
| 缺信用代码 | 0 |
| `industry_code` / `industry_link_code` 形态 | **JSON 数组**（100% 为 `['...']`） |

样例：

```text
credit_code=91440300MA5FFEXXXW
industry_code=['INB1306']
industry_link_code=['INB130601','INB13060101','INB1306010103','INB130601010303']
```

ETL 必须拆行（unpivot）：一行企业标签 → 多行 `industry_chain_entity_rel`。

### 2.3 `dwd_org_industry_product_tags` 覆盖

| 指标 | 结果 |
|---|---|
| 有效行数 | 20000 |
| 不重复企业 | 20000 |
| `industry_link_code` 为空数组 `[]` | **4792** |
| `product_name` | 文本列表，非标准产品 UID |

样例：

```text
credit_code=91420100565570094Q
industry_code=['INB2505','INB1303']
industry_link_code=['INB250503','INB25050305','INB2505030501']
product_name=['6840 临床检验分析仪器', '流式点阵仪']
```

产品关系可形成候选，但 `product_uid` 未冻结前不得作为生产跨域主键。

### 2.4 `dwd_industry_chain_news_info` 覆盖

当前仅 1 行，且关键字段为空或非法：

| 字段 | 当前值 |
|---|---|
| `industry_code` | 空 |
| `id` | 空 |
| `title` | 有标题文本 |
| `publish_date` | `0000-00-00`（非法日期） |
| `abstract` | NULL |

**结论：资讯主源当前不可灌。**

---

## 3. 对 v5 14 张目标表的总体可灌性

| 目标 DWD 表 | 主源是否覆盖 | 当前可灌结论 | 说明 |
|---|---|---|---|
| `industry_chain` | ✅ `dwd_industry_chain_info` | 🟡 可灌 12 条 | 依赖 Q053 编码归一 |
| `industry_chain_node` | ✅ `dwd_industry_chain_info` | 🟡 可灌 1273 个节点 | 依赖 Q053；缺 stage/type 等 |
| `industry_chain_node_rel` | ✅ `dwd_industry_chain_info.parent_code` | 🟡 可派生约 1261 条父子关系 | 仅 parent_child |
| `industry_chain_entity_rel` | ✅ tags + product_tags | 🟡 企业关系可灌；产品关系候选 | JSON 拆行；产品 UID 待冻结 |
| `industry_chain_market_observation` | ❌ | ❌ | 4 源无市场观测 |
| `industry_chain_investment_event` | ❌ | ❌ | 4 源无投融资 |
| `industry_chain_investment_participant` | ❌ | ❌ | 同上 |
| `industry_chain_news_event` | 🔧 表结构匹配，数据无效 | ❌ | 1 行无效 |
| `industry_chain_milestone_event` | ❌ | ❌ | 无可直接里程碑源 |
| `industry_chain_event_entity_rel` | ❌ | ❌ | 依赖有效事件 |
| `industry_chain_event_metric_observation` | ❌ | ❌ | 无互动量字段 |
| `industry_chain_extraction_result` | 🧮 | 🧮 Python | 4 源仅可作未来输入文档候选 |
| `industry_chain_model_run` | 🧮 | 🧮 系统 | 不由 ODS 灌 |
| `industry_chain_model_result_detail` | 🧮 | 🧮 Python | 不由 ODS 灌 |

> **本轮 4 张主源可立即支撑的，只有：产业链、节点、节点父子关系、链/节点—企业关系，以及产品关系候选。**

---

## 4. 14 张目标 DWD 表逐字段映射（基于 4 张主源）

### 4.1 `industry_chain`（产业链标准信息表）

| 目标字段 | 字段注解 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `chain_id` | 平台归一产业链主键 | `dwd_industry_chain_info.industry_code`（取 `level=0`） | 🟡 | 需按 Q053 将 INB 编码归一为平台 `chain_id`；当前 12 条 |
| `chain_code` | 产业链来源编码 | `dwd_industry_chain_info.industry_code` | ✅ | 当前 12 个 INB 编码 |
| `chain_name` | 产业链标准名称 | `dwd_industry_chain_info.industry_name` | ✅ | 当前可灌 |
| `chain_short_name` | 产业链简称 | 无 | ❌ | 4 源无简称 |
| `parent_chain_id` | 上级产业链主键 | 无可靠字段 | ❌ | `parent_code` 是节点父级，不是上级产业链 |
| `chain_level` | 产业链层级 | 根节点可默认 `0`/`1` | 🔧 | 主源只有节点 `level`；链级可按根默认 |
| `chain_category` | 产业链分类 | 无稳定分类 | ❌ | 需配置库/人工 |
| `future_industry_flag` | 未来产业标记 | 无 | ❌ | 需配置库/人工标注 |
| `description` | 产业链说明 | 无 | ❌ | 4 源无定义字段 |
| `status` | 有效状态 | `is_deleted` 派生 | 🔧 | `is_deleted=0` → active |

**当前结论：可灌 12 条产业链基础身份；缺简称、上级链、分类、未来产业标记、说明。**

### 4.2 `industry_chain_node`（产业链节点信息表）

| 目标字段 | 字段注解 | 来源表.字段 | 状态 | 当前可灌说明 |
|---|---|---|---|---|
| `node_id` | 节点归一主键 | `dwd_industry_chain_info.industry_link_code` | 🟡 | 建议平台归一；当前可先保留 INB 节点码 |
| `chain_id` | 所属产业链主键 | `dwd_industry_chain_info.industry_code` | 🟡 | 依赖 Q053 |
| `node_code` | 节点来源编码 | `dwd_industry_chain_info.industry_link_code` | ✅ | 1273 个编码 |
| `node_name` | 节点标准名称 | `dwd_industry_chain_info.industry_link_name` | ✅ | 当前可灌 |
| `parent_node_id` | 父节点主键 | `dwd_industry_chain_info.parent_code` | ✅ | 1261 条有父；12 条根为空 |
| `node_level` | 节点层级 | `dwd_industry_chain_info.level` | ✅ | 0～7 |
| `stage_code` | 上中下游阶段 | 无 | ❌ | 需规则或字典 |
| `node_type` | 节点业务类型 | 无 | ❌ | 需配置/规则 |
| `importance_level` | 来源明确重要等级 | 无可用来源字段 | ❌ | 不可把算法得分回写；`node_company_count` 不是重要等级 |
| `sort_no` | 同级排序 | 无 | ❌ | 系统生成或配置 |
| `node_path` | 节点层级路径 | `parent_code` 递归派生 | 🔧 | 父节点完整，可递归生成 |
| `description` | 节点说明 | 无 | ❌ | — |
| `status` | 节点有效状态 | `is_deleted` 派生 | 🔧 | 可派生 |

说明：`node_company_count` 是聚合统计，不应写入节点主表；企业规模统计应进 ADS。

**当前结论：可灌 1273 个节点的编码、名称、所属链、父节点、层级；缺阶段、类型、路径可派生。**

### 4.3 `industry_chain_node_rel`（产业链节点关系表）

| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `relation_id` | 节点关系主键 | 无 | 🧮 按链、父、子、有效期生成 |
| `chain_id` | 所属产业链主键 | `dwd_industry_chain_info.industry_code` | 🟡 |
| `source_node_id` | 关系起点（父） | `parent_code` | ✅ |
| `target_node_id` | 关系终点（子） | `industry_link_code` | ✅ |
| `relation_type` | 关系类型 | 常量 `parent_child` | 🧮 |
| `relation_direction` | 关系方向 | 常量 `directed` | 🧮 |
| `relation_weight` | 来源明确权重 | 无 | ❌ |
| `confidence` | 置信度 | 无 | ❌ |
| `evidence_ref` | 证据引用 | `source_table + pk_id` | 🔧 |

**当前结论：可派生约 1261 条父子关系；仅覆盖 parent_child，不覆盖供需/替代/协同。**

### 4.4 `industry_chain_entity_rel`（产业链实体关系表）

| 关系类型 | 注解 | 来源表.字段 | 目标字段映射 | 当前状态 |
|---|---|---|---|---|
| 链/节点—企业 | 企业参与产业链或节点 | `dwd_org_industry_tags.industry_code/industry_link_code/credit_code` | `entity_type='enterprise'`，`entity_id←credit_code→enterprise_code` | 🔧 **20000 行可拆** |
| 链/节点—产品 | 产品归属产业链或节点 | `dwd_org_industry_product_tags.industry_code/industry_link_code/product_name` | `entity_type='product'` | 🔧 候选；`product_uid` 待冻结；4792 行节点空 |
| 链—人才/技术/政策/机构/专利 | 其他七要素 | 无（本轮 4 源不含） | — | ❌ |

其他字段：

| 目标字段 | 字段注解 | 来源/规则 | 状态 |
|---|---|---|---|
| `relation_id` | 实体关系主键 | 业务字段指纹生成 | 🧮 |
| `node_scope_key` | 链级/节点级去重键 | `COALESCE(node_id,'__CHAIN__')` | 🧮 |
| `entity_subtype` | 实体细分类别 | 无稳定来源 | ❌ |
| `relation_type` | 关系类型编码 | 企业 `participates_in`；产品 `produces` | 🧮 |
| `role_type` | 业务角色 | 无 | ❌ |
| `importance_level` | 关系重要等级 | 无 | ❌ |
| `confidence` | 置信度 | 规则默认或空 | 🧮 |
| `is_primary` | 是否主要归属 | 无 | ❌ |
| `evidence_ref` | 证据引用 | `pk_id` / 来源记录 | 🔧 |

**当前结论：企业关系可灌（需 JSON 拆行 + 企业键归一）；产品关系仅候选；其余实体类型本轮无源。**

### 4.5 `industry_chain_market_observation`

本轮 4 源无市场规模、销量、价格、产值等观测字段。

**当前结论：❌ 不可灌。**

### 4.6 `industry_chain_investment_event` / 4.7 `industry_chain_investment_participant`

本轮 4 源无投融资、并购字段。

**当前结论：❌ 不可灌。**

### 4.8 `industry_chain_news_event`（产业链资讯事件表）

| 目标字段 | 字段注解 | 来源表.字段 | 状态 |
|---|---|---|---|
| `event_id` | 资讯事件主键 | 无 | 🧮 `news:*` |
| `source_news_id` | 来源资讯 ID | `dwd_industry_chain_news_info.id` | ✅/❌ 结构有，当前值空 |
| `chain_id` | 所属产业链 | `industry_code` | ✅/❌ 结构有，当前值空 |
| `node_id` | 所属节点 | 无 | ❌ |
| `title` | 标题 | `title` | ✅ 结构匹配 |
| `summary` | 摘要 | `abstract` | ✅ 结构匹配 |
| `news_type` | 资讯类型 | 无 | ❌ |
| `source_name` | 来源媒体 | `source` | ✅ 结构匹配 |
| `author_name` | 作者 | 无 | ❌ |
| `source_url` | 原文链接 | 无 | ❌ |
| `source_url_hash/news_dedup_key` | 防重指纹 | 系统生成 | 🧮 |
| `publish_time` | 发布时间 | `publish_date` | ✅/❌ 结构有，当前非法日期 |
| `region_code` | 区域 | 无 | ❌ |

**当前结论：字段结构部分匹配，但当前 1 行数据无效，❌ 不可灌。**

### 4.9～4.11 里程碑 / 事件实体关系 / 事件指标观测

本轮 4 源均无直接可用数据。

**当前结论：❌ 不可灌。**

### 4.12～4.14 抽取结果 / 模型运行 / 模型结果

应由本项目 Python/算法平台生成；4 张主源不负责直接灌入。

资讯表未来若补齐，可作为抽取输入文档候选，但仍需 Python 产出。

**当前结论：🧮 系统/Python。**

---

## 5. ETL 实施要点（针对可灌部分）

### 5.1 产业链与节点

1. 从 `dwd_industry_chain_info` 取 `level=0` 生成 `industry_chain`（12 条）；
2. 全量行生成 `industry_chain_node`（1273 条）；
3. `parent_code` 非空时生成 `industry_chain_node_rel`（约 1261 条，`relation_type=parent_child`）；
4. `chain_id/node_id` 在 Q053 确认前，可临时保留 INB 码并登记 `source_system`，但不得承诺为最终生产主键。

### 5.2 企业标签拆行

`dwd_org_industry_tags` 的 `industry_code` / `industry_link_code` 为 JSON 数组，ETL 必须：

1. 解析 JSON；
2. 按节点编码拆成多行；
3. `entity_type='enterprise'`；
4. `entity_id` 通过 `credit_code` 归一到 ENT 域 `enterprise_code`；
5. 若仅有链码无节点，则写链级关系（`node_id` 空，`node_scope_key='__CHAIN__'`）。

### 5.3 产品标签

1. 同样 JSON 拆行；
2. `product_name` 为文本列表，需再拆产品；
3. `product_uid` 未冻结前仅可进沙箱/候选，不得进生产跨域关联；
4. `industry_link_code='[]'` 的 4792 行只能挂链级，不能挂节点。

### 5.4 资讯

在供应方补齐 `id/industry_code/publish_date` 有效值前，跳过资讯灌数。

---

## 6. 最终判断

> **以当前 4 张主源为准，v5 14 张目标表中：结构骨架和实体关系可部分落地；市场、投融资、资讯、里程碑、互动量、抽取与模型结果仍不可由这 4 张表灌入。**

### 6.1 现在就能做的

1. **12 条**产业链基础记录；
2. **1273 个**产业链节点；
3. **约 1261 条**节点父子关系；
4. **最多 20000 家企业**的链/节点关系候选（JSON 拆行后行数会放大）；
5. **产品关系候选**（需产品主键冻结后才可生产化）。

### 6.2 核心缺口

| 优先级 | 缺口 | 影响 |
|---|---|---|
| P0 | Q053 编码归一（INB vs 平台主键） | 所有 `chain_id/node_id` 生产关联 |
| P0 | 资讯源无效（1 行空字段） | `industry_chain_news_event` 无法灌 |
| P0 | 无投融资/市场观测主源 | IC-03/IC-06 无法由本轮 4 源落地 |
| P1 | tags/product_tags 为 JSON 多值 | ETL 必须拆行，否则关系表灌错 |
| P1 | `product_uid` 未冻结 | 产品关系不能进生产跨域键 |
| P1 | 缺 stage_code / node_type / future_industry_flag | 全景展示与筛选能力不完整 |
| P2 | 无互动量、无抽取结果、无模型结果 | 热点、NLP、十三类模型需其他链路 |

### 6.3 建议下一步

1. 先落地可灌子集：`industry_chain` + `industry_chain_node` + `industry_chain_node_rel` + 企业版 `industry_chain_entity_rel`；
2. 同步推动 Q053 编码方案拍板；
3. 要求供应方修复/补齐 `dwd_industry_chain_news_info`；
4. 投融资与市场观测另找 ODS 表或采购源，不硬塞进这 4 张主源；
5. 产品关系等 `product_uid` 冻结后再生产化。
