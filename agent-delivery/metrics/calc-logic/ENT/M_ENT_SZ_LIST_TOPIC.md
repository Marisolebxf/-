# 深圳企业清单与链中角色（M_ENT_SZ_LIST_TOPIC）

> 口径真源：专题 OPEN seq 47 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **Q076 / Q-MO-ENT-05 团队暂定 D**（human:徐滕强）：深圳跟 `M_ENT_SZ_COUNT`，`region_id LIKE '4403%'`。禁止 `headquarters_city`。Q076 仍 🟡。  
> 角色 = `node_stage`（上中下游）。不 reuse `M_ENT_SZ_CHAIN_POSITION`（那是地区游分布 COUNT）。不走 ENT-D14 抽取。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_SZ_LIST_TOPIC`
- 名称：深圳企业清单与链中角色
- 模块：专题企业 / TOPIC-ENT-05
- 更新频率：年
- 关联Q：Q076 / Q-MO-ENT-05（暂定 D，仍 🟡）；深圳键同 `SZ_COUNT`

## 口径定义

自然年：国内行政落在深圳、且上链的企业成员行，并标注链中角色。

```
成员 = (org_id, chain_code, node_stage)
FROM enterprise_base b
JOIN enterprise_industry_chain e ON e.org_id = b.org_id
WHERE b.region_id LIKE '4403%'
```

查询 JOIN（不进成员表主键）：

- `enterprise_base`：名称

- 深圳 = `region_id LIKE '4403%'`（市码 4403，含各区）。跟 `SZ_COUNT`。禁止 `headquarters_city` / `city` 中文名。
- 角色 = `node_stage`（上 / 中 / 下游）。禁止 `chain_node.position` 顶本条；禁止节点名顶游。
- **选链是 API**：ETL 全量链成员；禁止把「当前所选链」写进主键口径。
- 只国内。不 UNION。
- 不另造 CNT ID。清单规模 = 同核成员去重，不 reuse `SZ_COUNT` 结果表。
- 禁止 reuse `SZ_CHAIN_POSITION`。禁止 ENT-D14 关系抽取进本核。禁止 `M_CHAIN_SZ_ENTERPRISE*` 顶替。

8 件套只留这条成员行。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

主档 `region_id` + 上链边在就能列出。公式完整。

### ② 灌数 / 绑码（另一回事）

现网 `enterprise_base` 无 `region_id` 列（跟 `SZ_COUNT` 探针）。待 ETL 绑码。不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_base` / `enterprise_industry_chain` | 表在；主档无 `region_id` 列 |
| 目标 | `enterprise_sz_chain_list`（建议：`org_id + chain_code + node_stage`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。不要把 `enterprise_base` 整表复制进目标。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 全量深圳上链成员写入目标表。 |
| API | `WHERE chain_code=?`，分页。禁止请求路径全库扫。 |
| 前端 | 选链 = 带链键查行。 |

**计算公式文件**：`M_ENT_SZ_LIST_TOPIC.md`

## 源表字段

```
enterprise_base.region_id <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端。维表不进 `source_systems`。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-28 覆盖 SZ_COUNT 叶；不进 8 件套）

- 正式 / demo `enterprise_base` 无 `region_id` 列。
- ODS `city='深圳市'` 有样例行，不当计算键。

## 待建 / 缺口（不是口径算不全）

1. `region_id` 绑码；Q076 🟡。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `TOPIC-ENT-05`；STAT。Q076 A/B/C 不作本条口径。

---
*2026-08-31 COVER-STAT-L01：深圳=4403%；角色=node_stage；选链是 API*
