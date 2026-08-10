# 基本产业链查询与产业链全景图谱实现方案

| 属性 | 内容 |
|---|---|
| 版本 | v1.1 |
| 日期 | 2026-08-10 |
| 状态 | Draft |
| 范围 | 产业/产业链多维查询、产业链全景图谱 |
| 设计依据 | 需规、现有原型、DWD v5、ODS 2026-08-10 复检 |

---

## 1. 本方案解决什么

本方案只实现两个能力：

1. **基本产业链查询**：按产业、产业链、链方向、查询对象、所属领域、产业分类等条件查询 `industry` / `industry_chain` 对象，并进入全景图谱。
2. **产业链全景图谱查询**：按选中的产业或产业链查询节点、关系、链方向和关联对象，支持逐级展开与详情查看。

本期不纳入：

- 周期分析、瓶颈识别、区域评价、深圳优势等深度模型；
- 图谱动态演进、双快照对比；
- 市场规模、投融资等非结构数据；
- 产业介绍和发展历程正文维护。

---

## 2. 当前数据能否支撑

### 2.1 可用 ODS

| ODS 表 | 可提供的数据 |
|---|---|
| `dwd_industry_chain_info` | 12 条顶层产业链、1273 个层级节点、约 1261 条父子关系 |
| `dwd_org_industry_tags` | 企业与产业链/节点的标签关系，需拆 JSON 数组 |
| `dwd_org_industry_product_tags` | 企业、产品与产业链标签，本期可暂不使用 |
| `dwd_industry_chain_news_info` | 资讯，本方案不依赖 |

### 2.2 对应 DWD

| DWD 表 | 本方案用途 | 是否必须 |
|---|---|---|
| `industry_chain` | 产业链查询列表与基础信息 | 必须 |
| `industry_chain_node` | 全景图谱节点 | 必须 |
| `industry_chain_node_rel` | 图谱节点之间的关系边 | 必须 |
| `industry_chain_entity_rel` | 节点/产业链关联企业 | 必须 |

其余 10 张 DWD 表不阻塞本方案。

---

## 3. 总体实现方式

```text
ODS
  ├─ dwd_industry_chain_info
  └─ dwd_org_industry_tags
          │
          ▼
Python ETL
          │
          ▼
DWD
  ├─ industry_chain
  ├─ industry_chain_node
  ├─ industry_chain_node_rel
  └─ industry_chain_entity_rel
          │
          ▼
Python 查询服务
  ├─ 产业链查询
  ├─ 产业链详情
  ├─ 全景节点/边查询
  └─ 节点关联企业查询
          │
          ▼
Java REST 透传
          │
          ▼
前端查询页 + G6 全景图谱
```

调用链固定为：

```text
前端 → Java REST → Python → DWD/ADS
```

Java 不计算图谱、不执行 nGQL，只做鉴权、参数校验、统一包络和服务透传。

---

## 4. 基本产业链查询实现

### 4.1 页面目标

页面提供：

- 产业链名称/编码模糊查询；
- 产业链列表；
- 基础信息展示；
- 点击“查看全景图谱”进入所选产业链。

### 4.2 查询对象

查询结果只包含两类稳定对象：

| 查询对象 | 对象类型 | 主键 | 数据落点 |
|---|---|---|---|
| 产业（L0） | `industry` | `industry_id` | `industry_chain.chain_tier='L0'` |
| 产业链（L1） | `industry_chain` | `chain_id` | `industry_chain.chain_tier='L1'` |

主键统一使用 INB。示例：

```text
industry：INB1303 集成电路
industry_chain：INB130301 集成电路下某条 L1 子链
```

> 要支持“产业 + 产业链”同时查询，原先可选的 **41 条 L1 必须升格进入 `industry_chain`**。如果只灌 12 条 L0（方案 A），系统只能查产业，不能形成有稳定身份的产业链结果。

L2+ 默认作为全景图谱节点，不进入基础查询结果；后续确需检索时再按产品口径升格。

### 4.3 查询维度、来源与缺口

| 查询维度 | 查询含义 | 查询字段/关系 | 从哪里查 | 当前 ODS 支撑 |
|---|---|---|---|---|
| 产业 | 顶层产业对象 | `industry_id`、L0 名称 | `industry_chain` L0 | ✅ `chain_info.industry_code/name` |
| 产业链 | 产业下 L1 子链 | `chain_id`、`parent_chain_id` | `industry_chain` L1 | ✅ `industry_link_code/name` + `level=1` |
| 链方向 | 上游/中游/下游/终端等 | `industry_chain_node.stage_code` | 节点聚合或节点过滤 | ❌ ODS 无；不能用 `level` 冒充 |
| 查询对象类型 | 返回产业还是产业链 | `object_type` | 由 `chain_tier` 确定 | 🧮 系统生成 |
| 关联对象 | 企业/机构/技术/产品/政策/专利等 | `entity_type`、`entity_subtype` | `industry_chain_entity_rel` | 🔧 当前仅企业、产品有原料 |
| 所属领域 | 跨产业的领域标签 | `domain_code/domain_name` | 配置字典 + 对象领域映射 | ❌ 现 DWD/4 ODS 均无稳定字段 |
| 产业分类 | 未来产业/战略新兴/优势传统等 | `chain_category`、`future_industry_flag` | `industry_chain` + 配置字典 | ❌ ODS 无；需配置/人工确认 |
| 对象来源 | 供应方、平台配置、人工维护 | `source_system` | 公共治理字段 | ✅/🧮 |
| 可用状态 | 可用/不可用 | `status` | `industry_chain.status` | 🧮 ETL/发布状态 |

#### “对象”必须拆成两个概念

1. `object_type`：查询结果是什么，只允许 `industry` / `industry_chain`；
2. `entity_type`：这条产业链关联了什么，可为企业、机构、产品、技术等。

两者不得共用一个字段，否则“查产业链对象”和“筛选链上的企业对象”会混淆。

#### 三个不能从现有 ODS 硬推的字段

| 字段 | 禁止做法 | 正确来源 |
|---|---|---|
| 链方向 | 用 ODS `level` 推上/中/下游 | `stage_code` 配置、人工维护或有证据的关系抽取 |
| 所属领域 | 从名称关键词临时猜领域 | 领域字典 + 产业/产业链领域映射 |
| 产业分类 | 看到名称后前端写死“未来产业” | 配置库/甲方确认的分类映射 |

建议新增配置读模型（可落 `gkx_cfg`，不新增供应方 ODS）：

```text
cfg_industry_domain(domain_code, domain_name, status)
cfg_industry_category(category_code, category_name, status)
cfg_chain_direction(direction_code, direction_name, sort_no)
rel_industry_domain(object_type, object_id, domain_code)
```

`chain_category` / `future_industry_flag` 可同步回 DWD 当前快照；领域通常为多值，使用映射关系，不建议塞逗号字符串。

### 4.4 列表字段

| 字段 | 来源 | 说明 |
|---|---|---|
| `object_type` | 由 `chain_tier` 映射 | `industry` / `industry_chain` |
| `object_id` | `industry_id` / `chain_id` | INB 稳定主键 |
| `object_name` | `chain_name` | 产业/产业链名称 |
| `parent_industry_id` | `industry_id` | 产业链结果必填 |
| `chain_tier` | `industry_chain.chain_tier` | L0 / L1 |
| `chain_category` | 配置映射 | 可空；无确认不伪造 |
| `domains` | 领域映射 | 可多值 |
| `directions` | 节点 `stage_code` 聚合 | 可多值；无配置为空 |
| `related_entity_types` | `entity_rel` 聚合 | 企业/产品等 |
| `node_count` | 节点聚合 | 节点总数 |
| `enterprise_count` | 企业关系聚合 | 关联企业去重数 |
| `description` | CMS | 可空；不得拿 ODS 空字段伪造 |
| `updated_time` | DWD | 最近更新时间 |

`market_size`、`investment_amount` 等指标不进入一期基础查询，避免被当前缺失数据阻塞。

### 4.5 API

#### 产业/产业链查询

```http
POST /topic/v1/industry/search
```

请求：

```json
{
  "keyword": "集成电路",
  "object_types": ["industry", "industry_chain"],
  "industry_ids": ["INB1303"],
  "chain_ids": [],
  "direction_codes": ["upstream"],
  "related_entity_types": ["enterprise"],
  "domain_codes": ["D-ICT"],
  "category_codes": ["strategic_emerging"],
  "logic": "AND",
  "page": 1,
  "size": 20
}
```

简单关键词查询可保留：

```http
GET /topic/v1/industry/search?q=集成电路&objectType=industry,industry_chain&page=1&size=20
```

响应项：

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "total": 1,
    "items": [
      {
        "object_type": "industry",
        "object_id": "INB1303",
        "object_name": "集成电路",
        "parent_industry_id": null,
        "chain_tier": "L0",
        "chain_category": null,
        "domains": [],
        "directions": [],
        "related_entity_types": ["enterprise", "product"],
        "node_count": 120,
        "enterprise_count": 3500,
        "description": null,
        "updated_time": "2026-08-10 00:00:00"
      }
    ]
  }
}
```

#### 产业/产业链基础详情

```http
GET /topic/v1/industry/objects/{objectType}/{objectId}
```

### 4.6 查询从哪里查

不让查询接口在运行时临时拼 4 张 ODS。由 Python ETL 先形成 DWD 和查询投影：

```text
ODS chain_info
  → DWD industry_chain（L0 产业 + L1 产业链）
  → DWD industry_chain_node / node_rel

ODS org_industry_tags / product_tags
  → DWD industry_chain_entity_rel

配置库
  → 分类、领域、链方向

上述数据
  → ads_industry_chain_search（查询宽表/物化视图）
  → Java/Python 查询 API
```

建议查询投影 `ads_industry_chain_search`：

```text
object_type, object_id, object_name, parent_industry_id,
chain_tier, category_code, domain_codes,
direction_codes, related_entity_types,
node_count, enterprise_count, status,
source_system, updated_time
```

数据量当前很小，可使用 MySQL/PostgreSQL 查询表或物化视图，无需 Elasticsearch。

### 4.7 查询实现

Python 查询逻辑：

1. `object_types` 过滤 L0/L1；
2. 产业条件查 `industry_id`，产业链条件查 `chain_id`；
3. 链方向通过节点 `stage_code` 的存在性过滤；
4. 关联对象通过 `entity_rel.entity_type` 的存在性过滤；
5. 领域通过对象—领域映射过滤；
6. 产业分类通过 `chain_category` / 配置映射过滤；
7. 关键词匹配编码、名称、简称、别名；
8. 返回分页结果和可解释命中字段。

数据量很小，一期直接走 MySQL/PostgreSQL 索引查询即可，不需要 Elasticsearch。

建议索引：

```text
industry_chain(chain_tier, industry_id, chain_name)
industry_chain(chain_code)
industry_chain_node(chain_id, stage_code)
industry_chain_entity_rel(chain_id, entity_type, entity_id)
rel_industry_domain(object_type, object_id, domain_code)
```

---

## 5. 产业链全景图谱实现

### 5.1 页面目标

用户从基础查询选择一个对象后：

1. 选择 `industry`：查询该产业下全部已发布 L1 产业链及其节点；
2. 选择 `industry_chain`：直接查询该条 L1 产业链及其下级节点；
3. 图谱展示节点、父子结构、业务关系、链方向和关联对象；
4. 点击节点查看基础信息和关联企业/机构/技术/产品；
5. 支持按链方向、节点类型、关联对象类型做图内过滤。

### 5.2 图谱不是算法推断

必须区分两种图：

| 图谱层次 | 能展示什么 | 数据来源 | 当前状态 |
|---|---|---|---|
| 层级全景 | L0→L1→L2+ 父子树 | ODS `parent_code` → `node_rel(parent_child)` | ✅ 可实现 |
| 方向全景 | 上/中/下游、供需、依赖、替代等真实业务流 | `stage_code` + 非 `parent_child` 关系 | ❌ 当前 ODS 不支撑 |

因此当前 ODS 能先落“产业链层级全景”，不能把父子树包装成“上中下游关系全景”。真正的方向全景需补：

```text
节点 = industry_chain_node
阶段 = industry_chain_node.stage_code
边   = industry_chain_node_rel(relation_type, relation_direction)
对象 = industry_chain_entity_rel
```

该查询与展示不需要 NetworkX 在线计算；结构数据由 Python ETL 生产，图谱在线服务读取 DWD/ADS。需要跨链路径分析时再同步 NebulaGraph，前端仍只通过 Java REST 调用。

现原型按 `seq_no` 相邻造边只能用于 Mock，生产禁止使用。`parent_code` 只能生成父子边，不能生成供需或上下游边。

### 5.3 产业入口和产业链入口

以集成电路为例：

```text
object_type=industry&object_id=INB1303
  → 查询 INB1303 下全部 L1 产业链
  → 展开各 L1 下全部正式节点

object_type=industry_chain&object_id=INB130301
  → 直接查询 INB130301 这一条链
  → 展开该链下全部正式节点
```

图中可按条件过滤：

| 图内条件 | 查法 |
|---|---|
| 链方向 | `node.stage_code IN (...)`，同时保留必要的连接路径 |
| 节点类型 | `node.node_type IN (...)` |
| 关联对象类型 | `EXISTS entity_rel(entity_type=...)` |
| 某个产业链 | `chain_id=...` |

图谱默认加载当前对象的完整正式结构，不是一次加载全库 1273 节点；不得静默分页、折叠或只返回直接子节点。节点详情和大明细列表可按需加载。

### 5.4 图谱 API

#### 图谱结构

```http
GET /topic/v1/industry/panorama?objectType=industry&objectId=INB1303
GET /topic/v1/industry/panorama?objectType=industry_chain&objectId=INB130301
```

响应：

```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "object": {
      "object_type": "industry",
      "object_id": "INB1303",
      "object_name": "集成电路"
    },
    "effective_at": "2026-08-10T00:00:00+08:00",
    "graph_level": "hierarchy_only",
    "available_filters": {
      "directions": [],
      "entity_types": ["enterprise", "product"]
    },
    "nodes": [
      {
        "node_id": "INB130301",
        "name": "晶圆制造",
        "level": 1,
        "parent_node_id": "INB1303",
        "stage_code": null,
        "enterprise_count": 320,
        "has_children": true
      }
    ],
    "edges": [
      {
        "source": "INB1303",
        "target": "INB130301",
        "relation_type": "parent_child"
      }
    ]
  }
}
```

#### 节点关联企业

```http
GET /topic/v1/industry/panorama/nodes/{nodeId}/entities?entityType=enterprise&page=1&size=20
```

如果企业标签只能精确挂到链、暂时不能挂到节点：

- 返回链级企业列表；
- 响应增加 `relation_granularity="chain"`；
- 页面提示“当前为产业链级关联企业”；
- 禁止把链级企业伪装成节点级企业。

### 5.5 后端查询方式

1. 校验 `objectType/objectId` 和发布状态；
2. `industry` 先解析所属全部 L1 链，`industry_chain` 直接锁定单链；
3. 查询对象范围内全部正式节点与关系；
4. 聚合节点关联对象数量和可用筛选项；
5. 返回 `nodes/edges/effective_at/graph_level`；
6. 节点关联对象和大字段详情另行按需查询。

本期在线读取 DWD 即可。后续如加入快照演进，再由离线任务生成 ADS 图谱快照。

### 5.6 前端实现

| 项 | 方案 |
|---|---|
| 图组件 | AntV G6 |
| 布局 | 分层布局（上→下或左→右），不使用随机 force 作为默认 |
| 节点颜色 | 有 `stage_code` 时按链方向；无源时按层级并明确“层级图” |
| 点击节点 | 右侧 Drawer 显示基础信息、子节点数、企业数和企业列表 |
| 下钻 | 点击复合节点进入内部结构；返回时恢复原节点和视口 |
| 工具栏 | 放大、缩小、适配画布、回到根节点 |
| 状态 | Loading、空图、无子节点、接口失败、无企业数据 |

当前 `demo-ui-topic` 的 ForceGraph 可保留作参考，但正式原型应替换为 G6 分层图。

---

## 6. ETL 实现

### 6.1 产业链和节点

来源：

```text
dwd_industry_chain_info
```

映射：

| ODS | DWD |
|---|---|
| `industry_code/name` | L0 `industry_id` / `chain_id` / `chain_name` |
| `level=1` 的 `industry_link_code/name` | L1 `chain_id` / `chain_name`，并回填所属 `industry_id` |
| `industry_link_code` | `node_id`（L1 可同时保持图节点身份） |
| `industry_link_name` | `node_name` |
| `level` | `node_level` |
| `parent_code` | `parent_node_id` |

L1 升格规则是基本查询的强制前置，不再是可选方案；同一来源编码在目录对象与图节点中的身份映射必须可追溯。

### 6.2 节点关系

每条非空 `parent_code` 生成：

```text
relation_type = parent_child
src_node_id    = parent_code
dst_node_id    = industry_link_code
```

必须校验：

- 父节点存在；
- 节点属于同一 L0 产业链；
- 不形成自环；
- 关系防重。

### 6.3 企业关系

来源：

```text
dwd_org_industry_tags
```

处理：

1. 拆 `industry_code` / `industry_link_code` JSON 数组；
2. 企业主键优先 `credit_code`；
3. 能匹配具体节点则挂节点；
4. 只能匹配 L0 时挂链级；
5. 保存关系粒度。

---

## 7. 对现有原型和接口的改造

| 现状 | 改造 |
|---|---|
| 查询页使用 mock `chainCode` | 改为 `object_type + INB object_id` |
| 查询结果进入画像页 | 统一为“进入全景图谱” |
| `/v1/chain/list` 返回窄表 | 改为产业/产业链统一检索，支持本文查询维度 |
| `/panorama` 按 ADS mock 返回 | 改为读取 DWD 真实节点和 `node_rel` |
| 图谱用 force 布局 | 改为 G6 分层布局 |
| `seq_no` 相邻造边 | 删除，使用真实父子关系 |
| 全库 mock 图 | 改为只返回当前产业/产业链的完整正式结构 |

兼容期可保留：

```text
GET /v1/chain/list
GET /v1/chain/{chain_id}/panorama
```

但返回字段需对齐本方案。

---

## 8. 分期

### 第一期：基本查询

- 灌 `industry_chain` L0 + L1；
- 建查询投影，提供关键词与对象类型、产业、产业链筛选；
- 前端列表和进入图谱按钮。

### 第二期：结构全景

- 灌 `industry_chain_node`、`node_rel`；
- G6 展示当前对象完整层级结构；
- 节点基础信息。

### 第三期：对象挂载与配置维度

- 拆企业标签；
- 提供节点/链关联对象列表；
- 配置产业分类、领域、链方向；
- 查询页开放链方向、关联对象、领域、产业分类筛选；
- 明示链级或节点级粒度。

### 后续增强

- 上中下游语义关系；
- ADS 快照与动态演进；
- NebulaGraph 复杂遍历；
- 技术、机构、市场指标等多要素图谱。

---

## 9. 最终结论

### 基本产业链查询

```text
ODS + 配置 → DWD → ads_industry_chain_search
→ 按产业/产业链/链方向/对象/领域/产业分类查询
→ 选择 object_type + object_id
```

基础查询不依赖算法和 Nebula；但链方向、领域、产业分类必须先有配置来源，不能由前端或名称猜测。

### 产业链全景图谱

```text
industry 入口 → 查所属全部 L1 链及节点
industry_chain 入口 → 查该链节点
→ industry_chain_node + node_rel 返回完整结构
→ entity_rel 查询企业/机构/技术/产品等关联对象
```

当前 ODS 一期只能形成**真实父子层级图**；补齐 `stage_code` 和业务关系后才能称为真正的上中下游方向图。NebulaGraph、动态演进和模型分析在基础结构稳定后再增加。
