# API · 产业集群（波次 B 契约）

> **任务**：`CHAIN-INDUSTRY-CLUSTER-SUPP-L01`  
> **日期**：2026-08-17  
> **状态**：demo-svc-platform `gkx-innov` 已落只读 + PUT；`demo_gkxlumenx_dim` 已灌 15/12。lumen 未复刻。  
> **存储真源**：`data/data-design/storage/CHAIN/stores/mysql/dim-industry-cluster.md`  
> **DDL / 种子**：`data/ddl/gkxlumenx_dim_industry_cluster.sql`  
> **Demo mock**：`data/data-design/storage/CHAIN/seeds/industry-cluster-sz-10+5-2026.yaml`  
> **口径**：Q068 🟡 · 政策版 `sz-10+5-2026`  
> **选择器 DEC**：`DEC-CHAIN-PORTAL-OVERVIEW-CLUSTER-SELECTOR-20260817.md`（高颖已补签）

---

## 0. 一句话

三个前端下拉读 **同一份 15 个集群**；出数前把 `cluster_id` 展开成 L0 `industry_id[]`，再打现有 ADS / 专题 / 企业接口。Java 只读写 dim，不算指标、不扫国标 NIC、不改 DWD。

---

## 1. 不要接错的三条字典

| 路径 | 是什么 | 本轮 |
|---|---|---|
| `POST .../search/meta/industries` | 国标行业 `code_nic` | **禁止**当集群下拉 |
| `POST .../search/meta/chains` | 旧产业链字典；`scope=future` 仍是八大 | **禁止**改成 15，也禁止门户继续用它当现行目录 |
| **本文** `.../meta/industry-clusters` | 深圳 3.0 10+5 | **现行**门户 / 展示 / 维护映射 |

Python 若仍有 `/internal/.../meta` 吐旧八大或旧 12 名：门户停用该列表，不必在算法里写 15 个名字。

---

## 2. 调用链

```text
前端 → Java REST（读/写 dim）→ 现有业务 API（入参仍是 industry_id[]）
```

| 规则 | 说明 |
|---|---|
| Java 读 | 只读 `industry_cluster` + `industry_cluster_map` |
| Java 写 | 仅维护页改 **map**；15 个集群名只读（换政策版除外） |
| Java 不算 | 禁止在这里聚合 ADS / 打分 / nGQL |
| 现有分析 API | 入参不变，仍吃 L0 `industry_id` 或 `industry_id[]` |
| 图谱 | 第一期不投影 Cluster 点 |
| CMS | 对象键仍是 L0 `industry_id` |
| Demo 未接 Java | mock **必须**与 yaml / SQL 同编码 |

网关前缀按仓拼接，**服务内路径相同**：

| 端 | 网关完整前缀（只读） |
|---|---|
| 专题 / 产业链 | `{gateway}/topic/v1/meta/industry-clusters` |
| 企业 | `{gateway}/enterprise/topic/v1/meta/industry-clusters` |
| 展示 | 经各自网关打到**同一契约**；禁止前端各写一份 15 个名字 |
| 维护写 | `{gateway}/ops/v1/industry-cluster-maps`（后台，C7） |

包络：`{ "code": 0, "msg": "ok", "data": ... }`。`code≠0` 时 `data` 为空，前端走空态，不造假 L0。

---

## 3. 只读

### 3.1 列表（下拉主接口）

`GET /topic/v1/meta/industry-clusters`

| Query | 说明 |
|---|---|
| `group` | 可选 `sei` \| `fut` |
| `include_l0` | 默认 `true` |
| `keyword` | 可选，匹配集群名 / `cluster_id` / L0 名 / `industry_id` |

```json
{
  "code": 0,
  "data": {
    "policy_version": "sz-10+5-2026",
    "q068": "pending_client",
    "items": [
      {
        "cluster_id": "CL-SEI-01",
        "group": "sei",
        "name": "新一代信息技术",
        "display_hint": null,
        "sort_order": 10,
        "map_status": "mapped",
        "l0": [
          { "industry_id": "INB1303", "name": "集成电路" }
        ]
      },
      {
        "cluster_id": "CL-SEI-03",
        "group": "sei",
        "name": "新能源",
        "display_hint": null,
        "sort_order": 30,
        "map_status": "pending_vendor",
        "l0": []
      }
    ]
  }
}
```

`map_status`：该集群有 ≥1 条有效 map → `mapped`，否则 `pending_vendor`。`l0=[]` 合法，前端空态「无相关产业数据」。

排序：`sort_order` 升序，与 storage §3 一致。

### 3.2 按集群展开 L0

`GET /topic/v1/meta/industry-clusters/{cluster_id}/l0`

```json
{
  "code": 0,
  "data": {
    "cluster_id": "CL-SEI-01",
    "industry_ids": ["INB1303", "INB1323", "INB1309", "INB1333", "INB1306"]
  }
}
```

未知 `cluster_id` → `code=404`。有集群无映射 → `industry_ids: []`（200，不是 404）。

前端拿到数组后再调现有分析接口。空数组**禁止**再请求 ADS 假装有数。

### 3.3 旧书签回填

`GET /topic/v1/meta/industry-clusters/resolve`

| Query（三选一） | 行为 |
|---|---|
| `cluster_id` | 回该集群 + 其 L0 |
| `industry_id` | 反查所属集群（本轮至多一个） |
| `future_industry_code` | **只读兼容**一版：能解析到集群或 L0 则回填；不能解析 → `code=404`，不猜。含企业旧 slug 与政策旧 `ind-*`（`ind-quantum` 对不上，不猜） |

新写入只用 `cluster_id` / `industry_id`。

### 3.4 目录覆盖（不是企业覆盖指标）

`GET /topic/v1/meta/industry-clusters/coverage`

```json
{
  "code": 0,
  "data": {
    "cluster_total": 15,
    "sei_total": 10,
    "fut_total": 5,
    "mapped_cluster_count": 7,
    "mapped_l0_count": 12,
    "future_coverage_denominator": 5
  }
}
```

只数 dim 行。**不是** `M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`（那是「有企业的未来产业数」，仍走 ADS / 指标 8 件套）。本接口只给选择器/空态用。

### 3.5 查询粒度展开（出数前门禁）

`POST /topic/v1/meta/industry-clusters/resolve-scope`

前端出数前必须先走本接口（或本地同语义 `resolveQueryScope`）。**禁止**把 `CL-*` 放进 `industry_id` 打 ADS。

```json
{
  "cluster_id": "CL-SEI-01",
  "industry_id": null,
  "industry_ids": [],
  "chain_node_id": null,
  "object_ids": []
}
```

| 入参 | 行为 |
|---|---|
| 只给 `cluster_id` 且有映射 | `grain=cluster`，`industry_ids[]` = 该集群全部有效 L0 |
| `cluster_id` + `industry_id=INB*` | `grain=industry`，数组长度 1 |
| `cluster_id` 无映射（如新能源 `CL-SEI-03`） | `grain=empty`，`empty_reason=unmapped_cluster`，`empty_message=无相关产业数据`；**不调 Python / ADS** |
| `industry_id` 或 `industry_ids[]` 出现 `CL-*` | **400** `industry_id must be INB*, not a cluster_id` |

```json
{
  "code": 0,
  "data": {
    "grain": "cluster",
    "cluster_id": "CL-SEI-01",
    "industry_ids": ["INB1303", "INB1323", "INB1309", "INB1333", "INB1306"],
    "node_ids": []
  }
}
```

空集群：

```json
{
  "code": 0,
  "data": {
    "grain": "empty",
    "cluster_id": "CL-SEI-03",
    "industry_ids": [],
    "node_ids": [],
    "empty_reason": "unmapped_cluster",
    "empty_message": "无相关产业数据"
  }
}
```

三层同一语义：前端 UX 禁生成 + 查询层 `canQueryAds=false` 本地空结果 + Java 硬闸不打 ADS。

---

## 4. 维护写（C7）

权限：后台维护角色。15 个 `cluster_id` **不可**增删改名（换 `policy_version` 另开任务）。

`PUT /ops/v1/industry-cluster-maps/{cluster_id}`

```json
{ "items": [ { "industry_id": "INB1303", "sort_order": 10 } ] }
```

| 校验 | 失败 |
|---|---|
| `cluster_id` 不存在 | 404 |
| `industry_id` 已被另一集群有效占用 | 409 |
| `industry_id` 不是 L0（若做存在性核对：读 `industry_chain.chain_tier='L0'`，只读） | 400 |
| 空 `items` | 200，该集群变 `pending_vendor` |

实现：替换该集群全部有效 map 行；重写 `industry_name` 快照。不写 DWD / ADS / cfg。

单条增删（可选，与 PUT 二选一即可）：

- `POST /ops/v1/industry-cluster-maps/{cluster_id}/items`
- `DELETE /ops/v1/industry-cluster-maps/{cluster_id}/items/{industry_id}`

---

## 5. 实现落点（波次 B 以后）

| 仓 | 做什么 |
|---|---|
| 编排仓（本文件） | 契约真源 |
| `demo-svc-platform` | 先落地只读 + 维护写；读 `demo_gkxlumenx_dim` |
| `lumen-svc-platform` | 复刻同一路径；只打 `gkxlumen-*`（D12） |
| Python | **不必**为列表新写算法；旧 `meta/chains?scope=future` 保持原义，门户不再用 |
| 三前端 | 波次 C 换源；未接 Java 前 mock = yaml |

可观测：Java 新接口按仓规加 trace；前端换源时走已有 `observability.ts`。

---

## 6. 自检

- [x] 实现不读 `meta/industries` / `meta/chains` 冒充集群（新包 `com.topcomm.gkx.innov.cluster`）  
- [x] 现有 `/topic/v1/industry/**` 入参未改成 `cluster_id` 主键  
- [x] 15 个 `cluster_id` 与 storage §3 逐字相同（`demo_gkxlumenx_dim` 已灌）  
- [x] 12 条 map 与 §4 相同；`uk_cluster_map_l0` 成立  
- [x] 8 个 pending 集群无 map 行（15−7 mapped）  
