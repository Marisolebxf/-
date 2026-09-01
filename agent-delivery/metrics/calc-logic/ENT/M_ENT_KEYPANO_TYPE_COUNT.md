# 覆盖企业类型数（M_ENT_KEYPANO_TYPE_COUNT）

> 口径真源：每格重点名单里六类 DWD 标签有几类至少 1 家 → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂重点名单 `M_ENT_KEY_TOTAL` + 上链 + `enterprise_tag`。  
> **① DWD 能数**：六类都在 `enterprise_tag.tag_code`，关系在就能 COUNT。  
> **② ODS→DWD**：灌数另一步，不进「无法执行」。  
> **选链不进口径**：ETL 全量链×链位；API 按键查。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点企业名单 |
| 2 | `enterprise_industry_chain` | 企业上了哪条链、链位 |
| 3 | `enterprise_tag` | 六类标签关系 |
| 4 | 本条 | 每个 `(chain_code, node_stage)` 一格：有几类 ≥1 家 |

不改 KEY_TOTAL / TYPE_COUNT 叶的任务范围以外口径（TYPE_COUNT 已同步改挂标签）。

## 元数据

- 指标ID：`M_ENT_KEYPANO_TYPE_COUNT`
- 名称：覆盖企业类型数
- 模块：企业分析 / 重点企业概览（E-33）
- 更新频率：周
- 关联Q：Q010（判定边界）；名单侧 Q038

## 口径定义

每个 `(chain_code, node_stage)`：该格重点名单里，六类 DWD 标签有几类至少 1 家。结果 **0～6**。

六类一律 `enterprise_tag.tag_code`（`tag_dict`）：

| 类型 | `tag_code` | 禁止 |
|------|------------|------|
| 高新 | `high_tech` | — |
| 专精特新 | `little_giant` | — |
| 小巨人 | `little_giant_pro` | — |
| 小微 | `sme` | `org_size`；`sme_tech` |
| 外资 | `foreign` | `enterprise_type` 含外商 |
| 上市 | `listed` | `is_listed` / 主档 listing |

```
COUNT(DISTINCT tag_code)
WHERE tag_code ∈ {foreign, high_tech, sme, listed, little_giant, little_giant_pro}
  AND org_id ∈ 该格重点名单
GROUP BY chain_code, node_stage
```

- 一企可进多类。禁止把覆盖数理解成企业数（那是 MATCH）。按类家数是后面的 `TYPE_STRUCTURE`。
- 禁止 `honor_type` / 不存在的 honor 表。
- 禁止「当前结果集 / 所选产业链」进口径。
- 只国内。

## 两步分开（强制）

### ① DWD 能不能数

`enterprise_tag` 有这六类关系 + 名单 + 上链边 → COUNT。公式完整，**可以算完**。

### ② ODS → DWD（另一回事）

六类 ODS 有没有灌进左端 `enterprise_tag`，只记灌数 / D3。没灌 **不写「当前无法执行」**，不否定 ①。

名单 KEY_TOTAL / 上链 ODS 弱，也是依赖现状，不跟 ② 揉成一句。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `key_enterprise` + `enterprise_industry_chain` + `enterprise_tag` | 名单 demo；上链表在；标签表在 |
| 目标 | `enterprise_keypano_chain_node_summary.type_cover_count`（与 MATCH 同粒度） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 名单 ∩ 上链 ∩ 六类 tag，**所有** `chain_code × node_stage` 写 `type_cover_count`。 |
| API | 只读目标表，按键查行。不带条件可回全量格子。 |
| 前端 | 选链/链位是过滤。 |

禁止请求路径对全库 JOIN 现算。demo 可现算对口径，不算接通。

**计算公式文件**：`M_ENT_KEYPANO_TYPE_COUNT.md`

## 源表字段

```
enterprise_industry_chain
enterprise_tag
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

右端 ODS（`dwd_org_tech_tag` / 上链源）只作家谱，不证明 ① 已接通。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-30；不进 8 件套）

- 无 `enterprise_keypano_qual_summary` / honor 表。
- `tag_dict` 有 `sme` / `foreign` / `listed` / `high_tech` / `little_giant` / `little_giant_pro`。
- ADS `key_enterprise` 87 行 demo，不当接通。

## 待建 / 缺口（不是口径算不全）

1. 名单 / 上链依赖出数。
2. 无独立目标列。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `E-33 重点企业概览`；STAT。与 `M_ENT_TYPE_COUNT` 同一套六类码。

---
*2026-08-30 COVER-STAT-L01：六类 tag_code；DWD 能数 / ODS 灌数分开*
