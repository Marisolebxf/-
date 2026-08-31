# 企业领域分布（M_ENT_DOMAIN_DIST_TOPIC）

> 口径真源：专题 OPEN → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> 领域 = 15 集群 `cluster_id`（跟 `M_ENT_DOMAIN_COVERAGE_COUNT`）。不改挂 Q013。  
> 家数从 **`enterprise_industry_chain`** 去重，经 L0 → `industry_cluster_map`。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_DOMAIN_DIST_TOPIC`
- 名称：企业领域分布
- 模块：专题企业 / TOPIC-ENT-05
- 更新频率：年
- 关联Q：Q068（15 集群 🟡）；不挂 Q013

## 口径定义

自然年 × `cluster_id`：国内上链企业去重家数，以及该格同比。

```
COUNT(DISTINCT e.org_id)
FROM enterprise_industry_chain e
JOIN industry_chain c ON c.chain_id = e.chain_code
JOIN industry_cluster_map m
  ON m.industry_id = c.industry_id
 AND m.is_active = 1 AND m.map_status = 'mapped'
GROUP BY stat_year, m.cluster_id
```

同比（同一 `cluster_id`）：

```
(cnt_y - cnt_y-1) / cnt_y-1
```

上年 0 或空 → 同比空。

- 统计主体 = `enterprise_industry_chain`。禁止年报/专利/产品另抽 `field_id`。
- 领域键 = `industry_cluster_map.cluster_id`（15）。未映射不计。
- **选产业是 API**：ETL 全量年×集群（及需要的链键）；禁止把「当前所选产业」写进 GROUP BY。
- 统计年 = 批次自然年快照（该年末上链仍有效的边），不是专利公开年。
- 只国内。无国外上链，不 UNION。
- 禁止另造深度 / 多元化 ID。禁止改挂 Q013 加权。

8 件套只留这条 COUNT + 同比。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

上链边 + map 在就能 GROUP BY 年×集群 COUNT。公式完整。

### ② 灌数 / 目录（另一回事）

`chain_code` 须灌 INB；Q068 未甲方确认。demo 上链表 IC-* 对不上 INB，不当接通。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_industry_chain` | 表在；码未对齐 INB |
| 目标 | `enterprise_domain_year_dist`（建议：`stat_year + cluster_id + org_cnt + yoy`） | **缺口：无此表** |

源 ≠ 目标。维表 `industry_chain` / `industry_cluster_map` / `industry_cluster` 不进 `source_systems`。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 每年全量年×集群 COUNT 写入目标表；同比用上年同行。 |
| API | 按年 / `cluster_id` / 链键过滤；禁止请求路径全表现算。 |
| 前端 | 选产业 = 带链键查行。 |

**计算公式文件**：`M_ENT_DOMAIN_DIST_TOPIC.md`

## 源表字段

```
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端上链表。dim / `industry_chain` 写细稿。

来源系统：产业链要素库。

## 现网探针（2026-08-27 覆盖领域叶；不进 8 件套）

- dim 15 集群 + map 在。
- 上链表 `chain_code` 仍 IC-* 样例，对不上 INB。

## 待建 / 缺口（不是口径算不全）

1. 上链灌 INB；Q068 🟡。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `TOPIC-ENT-05`；STAT。不作废展示 `DOMAIN_COVERAGE_*`。

---
*2026-08-31 COVER-STAT-L01：年×集群 COUNT FROM 上链表；选产业是 API*
