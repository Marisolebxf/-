# 整链资质分布（M_ENT_KEYPANO_QUAL_DISTRIBUTION）

> 口径真源：整链重点名单，六类 × 区域键 COUNT → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂 KEY_TOTAL + 上链 + `enterprise_tag` + `region_id` + 复合成员。  
> **① DWD 能数**：标签关系和 `region_id` 在就能出格子。  
> **② ODS→DWD**：灌数另写，不进「无法执行」。  
> **选链/选区不进口径**：ETL 全量立方；API 按键查。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点名单 |
| 2 | `enterprise_industry_chain` | 上了哪条链 |
| 3 | `enterprise_tag` | 六类 `tag_code` |
| 4 | `enterprise_base.region_id` + `region_scope_member` | 区域键（含县区、复合区域） |
| 5 | 本条 | `(chain, tag_code, region_key)` 一格 COUNT |

不是覆盖数（`KEYPANO_REGIONAL_COUNT`），也不是只按类型的 `TYPE_STRUCTURE`。

## 元数据

- 指标ID：`M_ENT_KEYPANO_QUAL_DISTRIBUTION`
- 名称：整链资质分布
- 模块：企业分析 / 重点企业概览（E-33）
- 更新频率：周
- 关联Q：Q010；名单 Q038；复合区域 Q056🟢

## 口径定义

整链重点名单：每个 `(类型, 区域)` 一格 `COUNT(DISTINCT org_id)`。

**类型**（六类 `tag_code`）：`foreign` / `high_tech` / `sme` / `listed` / `little_giant` / `little_giant_pro`。禁止 honor / 主档 / `org_size`。

**区域键**（与覆盖数同一套，**含县区**）：

| 键 | 说明 |
|----|------|
| `nation:CN` | 该链该类型国内合计 |
| `admin:` + 省 2 位 | |
| `admin:` + 市 4 位 | 热门城市并入市，不另开键 |
| `admin:` + 县/区 6 位 | **合进交叉表** |
| `scope:gba` / `yrd` / `jjj` | 大湾区 / 长三角 / 京津冀 |

```
COUNT(DISTINCT org_id)
WHERE org_id ∈ 该链重点名单
  AND tag_code = :t
  AND 该企点亮 :region_key
GROUP BY chain_code, tag_code, region_key
```

嵌套格子不可加（南山 ⊂ 深圳 ⊂ 广东 ⊂ 全国）。大湾区与广东可重叠，也不可加。六类不可加总。

主粒度 = **整链**。选链 / 选区 / 选类型是 API 过滤。

## 两步分开（强制）

① `enterprise_tag` + `region_id` + 复合成员表在即可数。  
② ODS 标签灌数、`region_id` 绑码另写，不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 名单 + 上链 + tag + `region_id` + DIM 成员 | 表在；名单 demo |
| 目标 | `enterprise_keypano_chain_qual_matrix`（`chain_code + tag_code + region_key + ent_count`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。无行当 0。

## 分场景 / 千万级（不进 8 件套）

ETL：所有链 × 六类 × 全部区域键（只落有数格）。API 只读，按链/类型/区域查。禁止请求路径现算 JOIN。

**计算公式文件**：`M_ENT_KEYPANO_QUAL_DISTRIBUTION.md`

## 源表字段

```
enterprise_industry_chain
enterprise_tag
enterprise_base.region_id
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

维表 `region_scope` / `region_scope_member` 不进 `source_systems`。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-30；不进 8 件套）

- 无 `enterprise_keypano_chain_qual_matrix` / honor 表。
- Q047 旧「4×3 写死」废止。

## 待建 / 缺口（不是口径算不全）

无独立目标表。D3/D4 本波不升。`is_mock: true`。

## 备注

bid `E-33`；STAT。OPEN 旧四类 + 三档地域不再用。

---
*2026-08-30 COVER-STAT-L01：六类 × 全国/省/市/县/复合区域*
