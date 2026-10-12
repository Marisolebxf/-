# 综合竞争力排名（M_ENT_COMPETITIVENESS_RANK）

> 口径真源：同业按竞争力分降序 → 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：挂 `M_ENT_COMPETITIVENESS_SCORE`。按该评分降序排。  
> **口径可算完**：SCORE 一旦出数，本条就能排名。SCORE 本波没出是上游 MODEL，与本条口径无关。  
> **千万级不进公式**：生产用预计算，禁止请求路径全表窗口。见「分场景 / 千万级」。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_COMPETITIVENESS_SCORE`（MODEL，本波不算） | 用来排序的评分 |
| 2 | 本条 | 在可比集上给出名次 |

不改 SCORE 叶。Q014 仍 🟡（权重未闭合，随 SCORE）。

## 元数据

- **指标ID**：`M_ENT_COMPETITIVENESS_RANK`
- **指标名称**：综合竞争力排名
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：综合竞争力评估
- **更新频率**：随 SCORE 批次（年 / 模型版本）
- **对齐状态**：口径可算完（有分就能排）；SCORE 是否出数另算；生产预计算
- **是否在数据库**：ADS `enterprise_ranking` 720 行 demo，是杂烩名次表不是本条源；SCORE 正式落表 `ads_ent_competitiveness_score` **待建**
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014

## 口径定义

按综合竞争力评分在可比集内降序排名。

- **未选产业 = 全国有分都进榜**。选了产业 = 该产业有分窗口。选产业是 API 选窗口，不是不计算。

- **SCORE 出了就能排**。本条不重新算分，只排序。无分不进榜。
- 同分并列（`RANK()` 语义，下一名跳号）。
- 可比集 = 当前筛选（默认所选产业 + 同一统计期）。
- **禁止抄** `enterprise_ranking.rank_no`。**禁止** `enterprise_score.score_total` 顶替竞争力分。
- 只国内。国外无对等分表，不造表。

8 件套只保留 RANK 口径。实现（预计算）不得改口径。

## 两点分开（强制）

### ① 本条口径

有竞争力评分 → 可比集内按分排序 → 名次。公式完整，**可以算完**。

### ② SCORE 出不出数（另一回事）

`M_ENT_COMPETITIVENESS_SCORE` 是 MODEL，本波不算；落表未建；Q014 未闭合。  
这是**上游还没有分**，不是排名口径缺条件。现网 `enterprise_ranking` 720 行 demo 能读出名次，**不当接通、不能冒充 ① 已算完**。

生产怎么排（离线 peer_group、禁止全表窗口）是实现，见下节，不否定 ①。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 排序用的评分（源） | `ads_ent_competitiveness_score`（建议名，SCORE 落表） | **缺口：无此表**（SCORE 没出，不是排名公式缺列） |
| 名次（目标） | 按封闭可比集写入 `rank_no`（可复用 `enterprise_ranking` 的表形：`org_id + peer_group + rank_no + score`，或独立 `enterprise_competitiveness_rank`） | 现网 `enterprise_ranking` 是 demo 杂烩，**不能当源**；当目标须按 `peer_group` 重灌，本波不改 DDL |

源表 ≠ 目标表。GDF 暂缓。

## 分场景 / 千万级实现（不进 8 件套）

### 生产铁律

1. **请求路径禁止** `RANK() OVER()` / `COUNT(*)` 自比扫 SCORE 全表。千万行窗口在 MySQL 上基本跑不完，会拖死实例。
2. **名次只读预计算表**。查询必须带 `org_id`，以及 `peer_group`（全国 / 产业代码 / 统计年，封闭枚举）。索引 `(peer_group, org_id)` 或 `(org_id, peer_group)`。
3. **出榜在离线批次**（随 SCORE 年更/模型版本）：每个封闭可比集单独排序写入目标表。Worker 内对**该集**排序（集大小=该产业/该年全国有分企业，不是全库一次窗口）。不要用一条 SQL 对全库开窗。
4. 任意多条件交叉筛选（城市∩链∩标签…）**不出现全库口径名次**。列表只对已经收窄的候选 `org_id`（本页 / 明确上限）`ORDER BY score`，那是**展示序**，细稿与页面都不得标成「综合竞争力排名」。

### 场景 A · 单企画像

读目标表：`WHERE org_id=:id AND peer_group=:当前产业或全国` → `rank_no`。无行 = 无分不进榜。

### 场景 B · 列表

先走已有企业列表过滤得到本页 `org_id`，JOIN 目标表取名次。禁止为画一张榜对千万行现算 RANK。

### demo / 生产

| | demo（百～千行） | 生产（千万级企业 × 多 peer_group） |
|--|------------------|-------------------------------------|
| 算法 | 可 `RANK() OVER()` 便于对口径 | 只读预计算；离线按 peer_group 排序落表 |
| 现网 | `enterprise_ranking` 720 行 | 不算接通 |

**计算公式文件**：`M_ENT_COMPETITIVENESS_RANK.md`

## 源表字段

二次 STAT：

```
ads_ent_competitiveness_score <- metric: M_ENT_COMPETITIVENESS_SCORE
```

左端 SCORE 落表待建，不把 `enterprise_ranking` / `enterprise_score` 写进 8 件套。

来源系统：国内机构要素库（SCORE 原料侧）。

## 现网探针（2026-08-28；不进 8 件套）

- `gkxlumenx_ads.enterprise_ranking`：720 行。列 `rank_dim, rank_value, rank_no, total_in_group`。含 `overall` / `chain_*` / `city_*` / `innov` / `growth`。
- `gkxlumenx_ads.enterprise_score`：120 行，`score_innov/operate/growth/total`，禁止当竞争力分。
- `gkxlumenx_ads.tech_power`：技术力，不是本条。
- 无 `ads_ent_competitiveness_score`。

## 待建 / 缺口（不是口径算不全）

1. **上游**：SCORE 本波无出数、Q014 未闭合、SCORE 落表未建。分一出，本条就能排。
2. **实现**：生产出榜批次未建；现网 ranking 是 demo。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.10`；STAT。与 `M_ENT_TECH_RANK` 同类二次 RANK。商业力排名仍未开。

---
*2026-08-28 COVER-STAT-L01：口径有分就能排；SCORE 出数另算；生产预计算*
