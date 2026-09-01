# 产业链完整度（M_ENT_CHAIN_COMPLETENESS）

> 口径真源：王惠底稿「覆盖节点数 / 标准节点总数」→ 2026-08-31 方案1：`formula` 只写 k/K；灌数对不上是另一回事。  
> **粒度**：某地区全部企业 vs 固定全量环节目录（不是「必须选一条链」）。  
> **分母**：叶子节点（2026-08-28 徐滕强确认）。不算链根、不算中间文件夹。QC01 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CHAIN_COMPLETENESS`
- **指标名称**：产业链完整度
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：产业链定位 / 多城市对标
- **更新频率**：周
- **对齐状态**：分母钉叶子；默认全目录；formula 与有数分开
- **是否在数据库**：结果列有 mock %；ODS 标准环节有数；项目 DWD 上链表无节点
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：QC01（节点覆盖口径）；Q016（对标城市，细稿记载）

## 口径定义

某地区：该地区**全部企业**覆盖的叶子环节数 / 固定目录中**全部叶子**数 × 100。

- **目录**：ODS `dwd_industry_chain_info` 12 条 `INB*` 链（智能终端、传感器、人工智能、机器人、集成电路、具身智能、生物医药、智能网联汽车、软件与信息服务、合成生物、低空经济、数字创意）。有限闭集。
- **叶子**：`industry_link_code` 不再作为任何节点的 `parent_code`。现网 **K=954**。
- **不算** level=0 链根（码等于产业链本身）。**不算**中间层（如「零部件」下面还有「核心零部件」时，零部件不是叶子）。
- **k**：该地区企业挂到的环节码，拆开后与叶子集合求交、去重。至少 1 家企业算覆盖。不加权。
- 只打到祖先文件夹、没打到叶子：**不**把子孙叶子算作已覆盖（不上卷冒充）。
- **默认用全目录**（12 链全部叶子）。不对 12 条链各自算完再平均。
- 页面若选了某链：只当过滤，k/K 收窄到该链叶子。未选 = 全目录。
- K=0：**无法计算**。k=0 且 K>0：完整度 = 0。
- 只国内。国外无对等上链表，不并。
- 地区 = `LEFT(enterprise_base.region_id, 4)`。禁止中文城市名。
- 对标哪些市：Q016 🟡；未闭合前只更新 `sz_city_benchmark` 已有 6 位 `city_code` 行。`NATIONAL` = 不按市过滤的全国叶子覆盖率。
- **禁止读** `sz_city_benchmark.chain_completeness`（深圳 75.0 等 mock）。
- **禁止**用 demo `chain_node`（`CH001` 等）当 K。
- 不挂 `M_CHAIN_SZ_COMPLETENESS` / `M_CHAIN_COMPLETENESS_SCORE`。

## 两点分开（强制）

### ① formula

上链表有环节码、叶子目录有 K，就能写 `k/K*100`。K=0 该次无法计算（除零）。k=0 且 K>0：完整度 = 0。

### ② 有没有数

`node_id` 全空、`chain_code` 仍是 `IC-*`：只记灌数 / 映射。**不写「当前无法执行」**。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `sz_city_benchmark.chain_completeness` | `city_code` 一条 | 该市 k/K×100（默认全目录叶子） |

## 分场景 / 实现方案

### 场景 A · 对标表（默认）

1. 叶子集合 L = 12 链中无子节点的 `industry_link_code`。
2. 该市企业 ∩ 上链：`enterprise_base.region_id` 市前缀 JOIN `enterprise_industry_chain`。
3. 将 `node_id` / tags 数组拆成码，与 L 求交得 k。
4. UPDATE `chain_completeness = k / |L| * 100`。

### 场景 B · 页面选了某链

L、k 都限制在该 `industry_code`。同一除法。

### 场景 C · 单市 KPI（深圳）

`region_id LIKE '4403%'`，写入 `city_code=440300`。

### demo（`demo_gkxlumenx_*`）

- 对标表行少，可全表算。
- `node_id` 全空、`chain_code` 为 `IC-*`：② 灌数缺口。不要用 `chain_node` / mock 75 顶。
- ODS tags 的 `industry_link_code` 是 **JSON 数组**（祖先+叶子混在一格），ETL 要拆开再对叶子目录。

### 生产（`gkxlumenx_*`）

- 只更新对标已有市。叶子目录从 ODS 灌项目维表后点查。
- 禁止无过滤当常规方案扫全表 tags。

对应 seed `formula`：k/K×100（全目录叶子）+ ①能写 + ②有数另写。

**计算公式文件**：`M_ENT_CHAIN_COMPLETENESS.md`

## 源表字段

```
enterprise_industry_chain <- ods: dwd_org_industry_tags
enterprise_base.region_id <- ods: dwd_org_base_info
```

计算 FROM 只用左端 DWD。分母：`dwd_industry_chain_info` 叶子；项目维表待灌，**不进** 8 件套 `source_tables`。禁止 mock `chain_node`。

产出（不进 `source_tables`）：`sz_city_benchmark.chain_completeness`。

来源系统：产业链要素库、国内机构要素库。

## 现网探针（2026-08-28；不进 8 件套）

- ODS `dwd_industry_chain_info`：12 条链；level=1=41；非根=1261；**叶子=954**。
- ODS `dwd_org_industry_tags`：20011 行；`industry_link_code` 为 JSON 数组（如 `['INB120401','INB12040101',…]`），不是单码。
- DWD `enterprise_industry_chain`：143 行；`chain_code` 全是 `IC-*`，**0 条** `INB*`；`node_id` **全空**。
- DWD `chain_node`：`CH001`… 8 链 41 节点，**不当 K**。
- `sz_city_benchmark.chain_completeness`：8 行有值（深圳 75.0），mock。

## 待建 / 缺口

- ETL：拆 tags 数组 → 叶子 `node_id`；`INB*` → `chain_code`（②，不改公式）。
- 项目叶子维表（从 ODS 灌），替换 mock `chain_node`。
- QC01 甲方未签；本波团队默认叶子（不是 level=1、不是全部非根）。
- Q016 对标集合 🟡。
- `region_id` 缺列：市过滤缺口留在 COUNT 叶，本条不重复整条挡。
- D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.5`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止多链平均。禁止用父节点覆盖冒充叶子覆盖。禁止 `node_company_count` 顶 k。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 分母改叶子；2026-08-31 方案1 formula 与有数分开*
