# 覆盖区域数（M_ENT_KEYPANO_REGIONAL_COUNT）

> 口径真源：每条链重点名单点亮的区域去重 → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂 `M_ENT_KEY_TOTAL` + 上链 + `enterprise_base.region_id` + DIM 复合区域。  
> **① DWD 能数**：`region_id` 有值就能点亮省/市/县；再比 `region_scope_member` 点亮大湾区/长三角/京津冀。  
> **② ODS→DWD**：绑码灌数另一步，不进「无法执行」。  
> **选链不进口径**：ETL 算全部链；API 按键查。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点企业名单 |
| 2 | `enterprise_industry_chain` | 企业上了哪条链 |
| 3 | `enterprise_base.region_id` | 省 2 / 市 4 / 县 6 |
| 4 | `region_scope` / `region_scope_member`（DIM） | 复合区域成员（Q056🟢） |
| 5 | 本条 | 每条链一个 `cover_count` |

不改 `M_ENT_REGIONAL_COUNT`（那条是按区 COUNT 企业，不是覆盖数）。

## 元数据

- 指标ID：`M_ENT_KEYPANO_REGIONAL_COUNT`
- 名称：覆盖区域数
- 模块：企业分析 / 重点企业概览（E-33）
- 更新频率：周
- 关联Q：Q012（行政区精度）；复合区域 Q056 已 🟢；名单 Q038

## 口径定义

每条产业链上，重点名单点亮了多少个区域。**一个 COUNT DISTINCT**，集合如下。

| 进集合 | `region_key` | 怎么点亮 |
|--------|----------------|----------|
| 省 | `admin:` + `LEFT(region_id, 2)` | DWD `region_id` |
| 市（含热门城市） | `admin:` + `LEFT(region_id, 4)` | 同上。热门城市 `region_scope` 是导航别名，`bind_admin_code` 对到同一市，**不另加** `scope:shenzhen` |
| 县/区 | `admin:` + `region_id`（6 位） | 南山区 → `admin:440305` |
| 复合区域 | `scope:` + `scope_code` | `parent_code='regional'`：`gba` 大湾区 / `yrd` 长三角 / `jjj` 京津冀。`region_id` 前缀命中 `region_scope_member.admin_code` |

深圳南山一家：广东 + 深圳 + 南山区 + 大湾区 = **4**。

```
COUNT(DISTINCT region_key)
WHERE org_id ∈ 该链重点名单
  AND region_id 非空
  AND region_key ∈ {省} ∪ {市} ∪ {县} ∪ {已点亮的复合区域}
GROUP BY chain_code
```

**不进覆盖集合**：`national` / `global` / `china-all` 目录节点；国外 G20 城市（本条只国内）；热门城市叶子（已并入市）。

- 禁止城市中文名、经纬度当键。
- 禁止「当前所选产业链」进口径。
- 禁止把不存在的 `enterprise_keypano_chain_region_summary` 当源。
- 主粒度 = 整链。页面要链位切片，ETL 可加 `node_stage` 一行，不把「必须选链位」写进口径。
- 空 `region_id` 不点亮任何键。

## 两步分开（强制）

### ① DWD + 维表能不能数

`region_id` 在 → 省/市/县可点亮；复合成员表在 → 大湾区等可点亮。公式完整，**可以算完**。

### ② ODS → DWD（另一回事）

省市区有没有绑成 `region_id` 灌进主档，只记灌数 / D3。没绑 **不写「当前无法执行」**。  
复合区域成员是 DIM（Q056），不是 ODS 缺口。

名单 / 上链出不出是依赖，不跟 ② 混写。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 名单 + 上链 + `enterprise_base.region_id` + DIM 成员 | 上链表/主档在；名单 demo |
| 目标 | `enterprise_keypano_chain_region_summary`（`chain_code + cover_count`；可另存点亮 key 列表） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 名单 ∩ 上链，**所有** `chain_code` 展开省/市/县/复合区域后 COUNT DISTINCT 写入。 |
| API | 只读目标表，`WHERE chain_code=?`。不带条件可回全量链。 |
| 前端 | 选链 / 选大湾区是过滤或看该 scope 是否在点亮集。热门城市筛选走市键。 |

禁止请求路径对全库 JOIN 现算。demo 可现算对口径，不算接通。

**计算公式文件**：`M_ENT_KEYPANO_REGIONAL_COUNT.md`

## 源表字段

```
enterprise_industry_chain
enterprise_base.region_id
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

维表（不进 `source_systems`）：`gkxlumenx_dim.region_scope`、`region_scope_member`。  
右端 ODS 只作家谱。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-30；不进 8 件套）

- 无 `enterprise_keypano_chain_region_summary`。
- DIM 已有 `gba` / `yrd` / `jjj` 及成员（Q056）。
- `region_id` 绑码是 ②，不改 ①。

## 待建 / 缺口（不是口径算不全）

1. 名单 / 上链依赖。
2. 无独立目标表。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `E-33 重点企业概览`；STAT。不是 `M_ENT_REGIONAL_COUNT`，也不是后面的区域分布。

---
*2026-08-30 COVER-STAT-L01：省+市+县+复合区域；热门城市并入市*
