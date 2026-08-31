# 企业类型分布（M_ENT_KEYPANO_TYPE_STRUCTURE）

> 口径真源：链×链位上六类各 COUNT → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂 KEY_TOTAL + 上链 + `enterprise_tag`。无区域维。  
> **① DWD 能数**：六类标签关系在就能 COUNT。  
> **② ODS→DWD**：灌数另写，不进「无法执行」。  
> **选链/链位不进口径**：ETL 全量；API 按键查。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点名单 |
| 2 | `enterprise_industry_chain` | 链 + 链位（上中下游） |
| 3 | `enterprise_tag` | 六类 `tag_code` |
| 4 | 本条 | `(chain_code, node_stage, tag_code)` 一格 COUNT |

不是覆盖类型数（那是有几类 ≥1）。不是整链资质分布（那是类型×区域）。要看「大湾区里各类型多少家」查 `M_ENT_KEYPANO_QUAL_DISTRIBUTION`。

## 元数据

- 指标ID：`M_ENT_KEYPANO_TYPE_STRUCTURE`
- 名称：企业类型分布（当前链位）
- 模块：企业分析 / 重点企业概览（E-33）
- 更新频率：周
- 关联Q：Q010；名单 Q038

## 口径定义

每个 `(chain_code, node_stage)` 格子里，六类各有多少家重点企业。

```
COUNT(DISTINCT org_id)
WHERE org_id ∈ 该格重点名单
  AND tag_code = :t
GROUP BY chain_code, node_stage, tag_code
```

六类码：`foreign` / `high_tech` / `sme` / `listed` / `little_giant` / `little_giant_pro`。  
禁止 honor / `enterprise_type` / `is_listed` / `org_size` / `sme_tech`。

一企多类，六类不可加总。不带区域维。只国内。

选链 / 选链位是 API 过滤。ETL 写全部链×链位×六类（无行当 0）。

## 两步分开（强制）

① `enterprise_tag` + 名单 + 上链边在即可数。  
② ODS 标签灌数另写，不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 名单 + 上链 + `enterprise_tag` | 表在；名单 demo |
| 目标 | `enterprise_keypano_node_type`（`chain_code + node_stage + tag_code + ent_count`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

ETL 全量预聚合。API 只读，按 `chain_code` + `node_stage`（+ `tag_code`）查。禁止请求路径现算 JOIN。

**计算公式文件**：`M_ENT_KEYPANO_TYPE_STRUCTURE.md`

## 源表字段

```
enterprise_industry_chain
enterprise_tag
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-30；不进 8 件套）

无 `enterprise_keypano_node_type` / honor 表。`key_enterprise` 87 行 demo 不当接通。

## 待建 / 缺口（不是口径算不全）

无独立目标表。D3/D4 本波不升。`is_mock: true`。

## 备注

bid `E-33`；STAT。与 TYPE_COUNT / QUAL 同一套六类码。

---
*2026-08-30 COVER-STAT-L01：链×链位×六类 COUNT；无区域维*
