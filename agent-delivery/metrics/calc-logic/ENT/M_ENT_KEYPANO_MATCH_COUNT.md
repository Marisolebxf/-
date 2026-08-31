# 匹配企业数（M_ENT_KEYPANO_MATCH_COUNT）

> 口径真源：全部产业链 × 链位上的重点企业去重 → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂重点名单 `M_ENT_KEY_TOTAL`（Q038）+ 上链 `enterprise_industry_chain`。  
> **口径可算完**：名单和上链边一出，本条就能 COUNT。Q038 / 上链 ODS / CMS 是另一回事。  
> **选链不进口径**：前端选链是展示过滤；后端 ETL 把所有链 × 链位都算完落表，API 按键查行。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点企业名单（先用专利数阈值；技术交易额搁置） |
| 2 | `enterprise_industry_chain` | 企业上了哪条链、链位是上/中/下游 |
| 3 | 本条 | 每个 `(chain_code, node_stage)` 一格 `COUNT(DISTINCT org_id)` |

不改 KEY_TOTAL 叶。Q038 仍 🟡。不把资质标签（高新/专精特新…）在本条重写成「重点企业」。

## 元数据

- 指标ID：`M_ENT_KEYPANO_MATCH_COUNT`
- 名称：匹配企业数
- 模块：企业分析 / 重点企业概览（E-33）
- 更新频率：周
- 关联Q：Q038（名单）；CMS 发布只在场景，不进 8 件套

## 口径定义

**按全部产业链 × 上中下游链位**，该格上的重点企业去重数。

```
COUNT(DISTINCT org_id)
WHERE 该企上了该链且 chain 的 node_stage 匹配
  AND org_id ∈ 重点企业名单
GROUP BY chain_code, node_stage
```

- 链位 = `enterprise_industry_chain.node_stage`（上 / 中 / 下游），不是目录叶子 `node_id`，也不是产业链 tags。
- 同一企业同一格多节点：去重后仍计 1。跨链各计各的。
- **链级合计**另 `GROUP BY chain_code` 再去重；禁止把各链位 `match_count` 相加（一企可能跨上中下游）。
- **禁止**把「当前所选产业链」写进口径。选链 / 选链位 = API 过滤预聚合行，不是计算条件。
- **禁止** `is_published` 进公式（CMS 发布是列表场景过滤）。
- **禁止**把不存在的 `enterprise_keypano_chain_node_summary` 当源（那是目标）。
- **禁止** ADS `key_enterprise` 87 行 demo 当接通。
- 只国内。无对等国外上链表则不 UNION。

8 件套只留这条 GROUP BY COUNT。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

名单 ∩ 上链边 → 按链 × 链位 COUNT。公式完整，**可以算完**。ETL 必须覆盖**所有**已有 `chain_code × node_stage`，不是「用户选了才算」。

### ② 上游出不出 / 上链 ODS（另一回事）

Q038 未闭合、KEY_TOTAL 仍 OPEN、上链 ODS 弱、demo 名单 87 行。不是本条 COUNT 缺条件。  
现网没有 keypano 汇总表可抄。demo 名单 **不当接通**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `key_enterprise`（KEY_TOTAL 出数）+ `enterprise_industry_chain` | 名单 demo 87 行；上链表在 |
| 目标 | `enterprise_keypano_chain_node_summary`（建议：`chain_code + node_stage + match_count`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

页面若要链级 KPI：同目标表加 `grain='chain'`（`node_stage` 空）或另表，按 `chain_code` 再去重 COUNT。禁止 `SUM(match_count)`。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 名单 ∩ 上链边，**所有** `chain_code × node_stage` 都 COUNT 写入目标表。没有企业的格可写 0 或不落行，API 无行当 0。 |
| API | 只读目标表。带 `chain_code` / `node_stage` 查对应行；不带条件可返回全量格子（下拉/地图）。**不算**「未选链无数」。禁止请求路径对全库 JOIN 现算。 |
| 前端 | 用户选链/链位 → 调 API 展示那一格。空态是页面行为。 |

demo 可现算对照口径，不算接通。生产只读预聚合。

**计算公式文件**：`M_ENT_KEYPANO_MATCH_COUNT.md`

## 源表字段

二次 STAT：

```
enterprise_industry_chain
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

左端上链表在；名单随 KEY_TOTAL 出数。不写 `gkx.dwd_*` 当 FROM。不写 CMS。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-30；不进 8 件套）

- 无 `enterprise_keypano_chain_node_summary`。
- ADS `key_enterprise` 87 行 demo（含 `patent_grant_count` / `key_score`），不当接通。
- `enterprise_industry_chain` 表在；ODS 上链仍弱（C 类）。

## 待建 / 缺口（不是口径算不全）

1. **上游**：KEY_TOTAL / Q038 名单未闭合；上链 ODS 弱。名单和上链边一出，本条就能数。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `E-33 重点企业概览`；STAT。不改 KEY_TOTAL / MODEL 叶。

---
*2026-08-30 COVER-STAT-L01：全量链×链位预聚合；选链是 API 过滤*
