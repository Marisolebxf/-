# 覆盖未来产业数（M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT）

> 口径真源：T0-X / E-32 / Q068 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> 与 `M_ENT_DOMAIN_COVERAGE_COUNT` **同一管道**，只数 5 个未来集群。  
> Q068 仍 🟡。不 reuse 覆盖领域数（那条是 15，只出一个数）。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT`
- 名称：覆盖未来产业数
- 模块：E-32 / ENT-E32-003
- 更新频率：日
- 关联Q：Q068（15 集群目录，其中未来 5 个）

## 口径定义

当前企业集合落到的 **未来产业集群 `cluster_id` 去重数**。值域 0～5。

5 个：`CL-FUT-01` 未来制造 / `02` 未来信息 / `03` 未来能源 / `04` 未来空间 / `05` 未来健康。  
判定：`industry_cluster.cluster_group='fut'`（不要手写 5 个名字当字典）。

```
COUNT(DISTINCT k.cluster_id)
FROM enterprise_industry_chain e
JOIN industry_chain c ON c.chain_id = e.chain_code
JOIN industry_cluster_map m
  ON m.industry_id = c.industry_id
 AND m.is_active = 1 AND m.map_status = 'mapped'
JOIN industry_cluster k
  ON k.cluster_id = m.cluster_id
 AND k.is_active = 1 AND k.cluster_group = 'fut'
WHERE e.org_id IN (:enterprise_set)
```

- 上链表不是领域表。`chain_code` 若为 L1，先收 L0 再进 map。
- 未映射 / 未激活：**不计**。
- 只国内。无国外上链，不 UNION、不造表。
- **选产业不进口径**。对象已是选定企业集合；再按一条链滤会把覆盖钉死成 0/1。
- 禁止 `chain_code` / 国标 NIC / 年报领域冒充。
- 禁止 reuse `DOMAIN_COVERAGE_COUNT` 的结果数（15 里滤不出这 5 个）。
- 不等于覆盖广度（/15）或深度加权。

8 件套只留这条 COUNT。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

上链边 + map + `fut` 行在就能数。公式完整。

### ② 灌数 / 目录（另一回事）

`chain_code` 须灌 INB。Q068 未甲方确认。demo 上链表 IC-* 对不上 INB。不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_industry_chain` | 表在；码未对齐 INB |
| 目标 | `enterprise_future_cluster_cover`（建议：`scope_key + cover_cnt`） | **缺口：无此表** |

源 ≠ 目标。维表 `industry_cluster` / `industry_cluster_map` / `industry_chain` 不进 `source_systems`。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 按企业集合键预聚合 DISTINCT `fut` 集群；或物化企业→集群后再 COUNT。 |
| API | 传入对比篮 / 页面企业集合，读预聚合。禁止请求路径全表扫。 |
| 前端 | 展示 0～5。选产业不改本核。 |

**计算公式文件**：`M_ENT_FUTURE_INDUSTRY_COVERAGE_COUNT.md`

## 源表字段

```
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端上链表。dim 写细稿。

来源系统：产业链要素库。

## 现网探针（2026-08-27 覆盖领域叶；不进 8 件套）

- dim 15 集群全开，其中 `fut` 5 行。
- map 有 `INB1801`～`1805` 对 `CL-FUT-*`。
- 上链表 `chain_code` 仍 IC-*，对不上 INB。

## 待建 / 缺口（不是口径算不全）

1. 上链灌 INB；Q068 🟡。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `ENT-E32-003`；STAT。不作废 `DOMAIN_COVERAGE_COUNT`。

---
*2026-08-31 COVER-STAT-L01：只数 5 个未来集群；管道同覆盖领域数*
