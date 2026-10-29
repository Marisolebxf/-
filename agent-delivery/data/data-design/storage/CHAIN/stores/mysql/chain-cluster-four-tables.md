# 产业链四表速览：industry_cluster / industry_cluster_map / industry_chain / industry_chain_node

> **定位**：面向同事的表定义与关系速查（非规范真源）。字段级 DDL / 种子口径只认：
> `dim-industry-cluster.md`（同目录，Q068 存储真源）与 `dwd-chain.md`。
> 数据口径截至 2026-10-29（demo_gkxlumenx_* 线上实测）。

## 一、这四张表分两层，别混

| 层 | 表 | 库 | 作用 |
|---|---|---|---|
| **DIM 展示目录层** | `industry_cluster`、`industry_cluster_map` | `demo_gkxlumenx_dim` | 给领导/外部看的**固定 15 个产业集群**目录，以及集群→产业的挂接关系。是"翻译层"：界面选集群，查数时翻译成产业码 |
| **DWD 产业树层** | `industry_chain`、`industry_chain_node` | `demo_gkxlumenx_dwd` | 从三方供应库贴源映射出的**真实产业树**（产业链 + 链上环节），是所有产业数据的挂接骨架 |

两层的关系靠 `industry_cluster_map.industry_id = industry_chain.chain_id`（仅 level=0 的链）连接。

## 二、逐表说明

### 1. `industry_cluster` —— 集群目录（15 行，固定）

- **内容**：深圳 3.0「10 战新 + 5 未来」产业集群目录，编码 `CL-SEI-01~10`（战新）、`CL-FUT-01~05`（未来），政策版 `sz-10+5-2026`
- **关键列**：`cluster_id`（PK）、`cluster_group`（sei/fut）、`cluster_name`、`display_hint`（括号说明）、`sort_order`
- **口径**：目录本身固定 15 个不随灌数变；变化要走甲方决策（Q068，当前 🟡 团队默认）
- **当前数据**：15 行全启用

### 2. `industry_cluster_map` —— 集群↔产业映射（当前 15 行）

- **内容**：集群挂接哪些 L0 产业。`cluster_id` + `industry_id` 联合主键，`industry_name` 是展示名快照
- **基数**：集群→L0 为 **1:N，允许 0**；同时**一个 L0 可挂多个集群**（如"人工智能"同时挂"新一代信息技术"和"未来信息"，"低空经济"同时挂"低空经济与空天"和"未来空间"——2026-09-02 监管人确认的共享）
- **`map_status`**：`mapped`=已挂接；`pending_vendor`=供应方产业未到、**不占行**（当前新能源/新材料/高端装备/绿色环保/海洋/未来能源 6 个集群无对应 L0）
- **维护方式**：**随灌数自动重建**（灌数流程读 DWD L0 + 按定稿种子挂接表重新生成，带行数/孤儿码双校验，见 `demo-algo-science` `chainan/llm_ods/cluster_map.py`）；日常微调走 ops 运营页
- **口径备注**：建表注释"同一 L0 只挂一个集群"是早期注释，现行以 Q068 共享口径为准（允许跨集群共享）

### 3. `industry_chain` —— 产业链（L0 链）表（当前 53 行）

- **内容**：产业链标准信息。**只放产业树的"链"层**：当前 = 12 个 L0 主链 + 41 个 L1 子链
- **关键列**：`chain_id`（业务主键，即 INB 产业码，唯一键）、`chain_name`、`parent_chain_id`（上级链）、`chain_tier`（L0/L1）、`chain_level`（数值层级 0/1）、`industry_id`、`future_industry_flag`
- **数据来源**：三方库 `gkx.dwd_industry_chain_info`（贴源同步）→ 灌数时映射（`chain_id`=源 `industry_link_code`，level 0/1 的行进本表）
- 注意：源表列曾有错位（link 列装父码、parent_name 装 level 数字），数据同步功能已内置自动修正（`ods_sync.normalize_chain_info_rows`），2026-10-29 后同步的数据即为正确结构

### 4. `industry_chain_node` —— 产业链环节（节点）表（当前 1220 行）

- **内容**：每条链下面的**环节**（level≥2 的产业节点），如"机器人→核心零部件→伺服系统→伺服驱动器"
- **关键列**：`node_id`/`node_code`（业务键=INB 码）、`chain_id`（所属链 FK）、`node_name`、`parent_node_id`、`node_level`（≥2）、`stage_code`（上/中/下游）、`sort_no`（同级排序）
- **唯一键**：`(chain_id, node_id)`
- **数据来源**：与 industry_chain 同源同流程（源 level≥2 的行进本表，链归属=编码去末段对应的上级）
- **诚实备注**：`stage_code`（上/中/下游）目前按编码末两位数字段规则推断（1-4 上游 / 5-8 中游 / 9+ 下游），源数据没有真实工序字段，归类可能不完全贴合业务实际——已挂起待供应方确认

## 三、关系图（文字版）

```
DIM 展示目录层                                DWD 产业树层
industry_cluster (15 集群)                  industry_chain (53 链: 12 L0 + 41 L1)
      │ 1:N                                        │ 1:N
      ▼                                            ▼
industry_cluster_map (15 行)   ──industry_id──▶ (仅 level=0 的 chain_id)
   集群↔L0 挂接；L0 可跨集群共享                industry_chain_node (1220 环节)
                                                  │ chain_id + node_level≥2
                                                  ▼
                                               挂企业/新闻/投资等明细（entity_rel 等）
```

- **界面选集群** → 经 `industry_cluster_map` 展开成一组 `industry_id`（L0 码）→ 拿码去 ADS 查数
- **改映射 ≠ 改目录**：领导调整关注点只动 `_map`，15 个集群编码永不变
- **数据刷新链路**：三方库同步（贴源，含自动纠错）→ 灌数（映射出链/节点 + 自动重建集群映射 + 重算 ADS）

## 四、几个容易踩的口径点

1. 集群目录（15）≠ 产业树（12 L0 + 41 L1 + 1220 节点），两套编码体系，靠映射表连接
2. 真源码族是 `INB12xx/13xx/15xx/25xx`；旧 mock 的 `INB17xx/18xx` 已废弃（相关映射备份在 `industry_cluster_map_20261029`）
3. `pending_vendor` 的 6 个集群不是丢数据，是供应方产业还没到，到货后在映射表补挂
4. 共享挂接（一个产业多个集群）是确认过的合法形态，去重统计时注意按 `industry_id` 去重

## 五、当前映射快照（2026-10-29 重建后）

| cluster_id | 集群 | 挂接 L0 |
|---|---|---|
| CL-SEI-01 | 新一代信息技术 | INB1303 集成电路；INB1323 传感器；INB1309 人工智能；INB1333 智能终端；INB1306 软件与信息服务 |
| CL-SEI-02 | 生物产业 | INB2503 生物医药 |
| CL-SEI-03 | 新能源 | pending_vendor |
| CL-SEI-04 | 新材料 | pending_vendor |
| CL-SEI-05 | 高端装备 | pending_vendor |
| CL-SEI-06 | 智能网联新能源汽车 | INB1209 智能网联汽车 |
| CL-SEI-07 | 绿色环保 | pending_vendor |
| CL-SEI-08 | 低空经济与空天 | INB1236 低空经济 |
| CL-SEI-09 | 传统与创意产业 | INB1502 数字创意 |
| CL-SEI-10 | 海洋产业 | pending_vendor |
| CL-FUT-01 | 未来制造 | INB1204 机器人；INB1354 具身智能 |
| CL-FUT-02 | 未来信息 | INB1306 软件与信息服务；INB1309 人工智能（共享 SEI-01） |
| CL-FUT-03 | 未来能源 | pending_vendor |
| CL-FUT-04 | 未来空间 | INB1236 低空经济（共享 SEI-08） |
| CL-FUT-05 | 未来健康 | INB2505 合成生物 |
