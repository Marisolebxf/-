# 链中角色（M_ENT_SZ_CHAIN_POSITION）

> 口径真源：王惠底稿「上/中/下游、链主」→ 2026-08-31 方案1：`formula` 只写怎么算；**缺列 / 缺目录 / 未灌都标缺口，不写无法执行**。  
> **团队临时默认**：角色 = **上 / 中 / 下游**（徐滕强）。游列锁 **`chain_node.position`**。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_SZ_CHAIN_POSITION`
- **指标名称**：链中角色
- **一级模块**：企业分析
- **二级模块**：深圳企业现状分析
- **三级模块**：产业链定位 / 多城市对标
- **更新频率**：日
- **对齐状态**：游列已锁 `position`；缺口见下表，不进无法执行
- **是否在数据库**：`chain_node.position` 41 行全有上游/中游/下游；对标 JSON 有 mock
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：无现成 Q（INB 叶子灌入并带 position 待 GDF）；对标城市见 Q016（细稿）

## 口径定义

某地区企业按 **上游 / 中游 / 下游** 去重计数。

- 游 = 项目节点表 **`chain_node.position`**（值：上游 / 中游 / 下游）。目录节点名不是游。
- 企业叶子码 JOIN 节点表得 `position`。对不上的进 `unlabeled`。
- 默认：该地区全部上链企业。页面选链：只计该链。
- 一企多个叶子、跨游：各游都计。
- **链主**不进本 JSON。
- 只国内。地区 = `LEFT(enterprise_base.region_id, 4)`。禁止中文城市名。
- Q016 未闭合前只更新已有 6 位 `city_code`。`NATIONAL` = 不按市过滤。
- **禁止读** `sz_city_benchmark.chain_position` mock JSON。
- **禁止**用 `enterprise_industry_chain.node_stage`（链主/核心配套/一般参与）顶游。
- **禁止**按树序三等分硬编游。
- **禁止**把现网 CH001 中文节点名去对 INB 码。

## 两点分开（强制）

### ① formula

上链表有叶子码、节点表有 `position`，就能 `JOIN` 后按游 COUNT。对不上进 `unlabeled`（口径，不是整条算不了）。

### ② 有没有数

CH 目录、空 `node_id`、缺 `region_id`：只标缺口。**不写「当前无法执行」**。

## 落表

| 目标 | 粒度 | 写什么 |
|------|------|--------|
| `sz_city_benchmark.chain_position` | `city_code` 一条 JSON | `{upstream, midstream, downstream, unlabeled}` = 各游 `COUNT(DISTINCT org_id)` |

## 分场景 / 实现方案

### 场景 A · 对标表（默认）

叶子码能 JOIN 到带 `position` 的节点表之后：该市企业 → 叶子 → `position` → `GROUP BY` 计数 → 写 JSON。

### 场景 B · 页面选了某链

只保留该链叶子再分组。

### 场景 C · 单企画像（不进 8 件套公式）

该企叶子对应的游集合（可多值）。

### demo / 生产

- 现网 `chain_node`：8 链 `CH001`–`CH008`，41 节点，`position` 全满（上游 10 / 中游 15 / 下游 16），`node_id` 自增整数。
- 企业上链 / 完整度目录是 **INB\*** 叶子（954）。JOIN 键对不上 = **缺口：目录未灌 INB**，不要用 CH 中文名或 mock JSON 凑。
- tags 数组拆开后只对叶子再查 `position`。
- 生产：GDF 按同结构把 INB 叶子灌进节点表并带 `position` 后，按市码过滤计算。禁止无过滤全表当常规方案。

对应 seed `formula`：JOIN `position` 按游 COUNT + ①能写 + ②缺口另列。

**计算公式文件**：`M_ENT_SZ_CHAIN_POSITION.md`

## 源表字段

```
enterprise_industry_chain <- ods: dwd_org_industry_tags
enterprise_base.region_id <- ods: dwd_org_base_info
```

计算 FROM 只用左端 DWD。游列在 `chain_node.position`（项目 DWD 节点表，不是三方 ODS 现成列），**不进** 8 件套 `source_tables`（与 `code_region.area` 同类）。禁止把 `node_stage` 当源。

产出（不进 `source_tables`）：`sz_city_benchmark.chain_position`。

来源系统：产业链要素库、国内机构要素库。

## 现网探针（2026-08-28；不进 8 件套）

- `gkxlumenx_dwd.chain_node.position`：**有标记**，41/41 = 上游/中游/下游。链码 `CH001`…，节点名如「基因编辑工具」。
- ODS `dwd_industry_chain_info`：12 条 `INB*`，无 `position` 列；名称含上中下游 = 0。
- DWD `enterprise_industry_chain`：`IC-*` + `node_id` 空，接不上 `CH*` 也接不上 `INB*`。
- `node_stage`：链主/核心配套/一般参与，不是游。
- `sz_city_benchmark.chain_position`：mock JSON。

## 待建 / 缺口（必须标；不是无法执行）

| 类型 | 缺什么 | 现网 |
|------|--------|------|
| 缺目录 | `chain_node` 应是 INB 叶子 + `position` | 现为 CH001–8、41 节点、`node_id` 自增 |
| 缺灌数 | `enterprise_industry_chain.node_id` / `chain_code` 对上 INB | `node_id` 全空；`chain_code` 全 `IC-*` |
| 缺列 | `enterprise_base.region_id`（市过滤） | 主档无此列；跟 `SZ_COUNT` 同一缺口 |
| 缺列 | ODS `dwd_industry_chain_info.position` | 无游列；游只锁项目 `chain_node.position` |
| 无独立结果含义 | 对标 JSON 可写，但是 mock | `sz_city_benchmark.chain_position` 不当接通 |
| 口径未闭合 | Q016 对标城市集合 | 仍 🟡 |

D3 / D4 本波不升。`is_mock: true`。本波不改 GDF DDL。

## 备注

bid `§1.1.1.2.4.2.3.5`；STAT。禁止把 `gkx.dwd_*` 写入 `source_tables` 主体。禁止三分树硬编游。禁止用 CH 目录假接通 INB 上链。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-28 游锁 position；2026-08-31 方案1 缺口标出、不写无法执行*
