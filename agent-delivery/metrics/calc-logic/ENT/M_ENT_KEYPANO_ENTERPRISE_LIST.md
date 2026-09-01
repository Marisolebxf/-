# 企业清单（M_ENT_KEYPANO_ENTERPRISE_LIST）

> 口径真源：重点名单 ∩ 链×链位的成员集 → 2026-08-30 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：不是 COUNT，是成员行。展示字段查询 JOIN。  
> **① DWD 能列**：名单 + 上链边在就能出成员。  
> **② ODS→DWD**：灌数另写。  
> **选链/链位/类型/区域/分页不进口径**：ETL 全量成员表；API 过滤分页。  
> CMS 发布不进 8 件套。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点名单 |
| 2 | `enterprise_industry_chain` | 链 + 链位 |
| 3 | `enterprise_base` / `enterprise_tag` | 查询时名称、`region_id`、六类标签 |
| 4 | 本条 | 成员表 `(org_id, chain_code, node_stage)` |

不改 KEY_TOTAL。Q039 是文案，不进口径。

## 元数据

- 指标ID：`M_ENT_KEYPANO_ENTERPRISE_LIST`
- 名称：企业清单（当前链位）
- 模块：E-33
- 更新频率：周
- 关联Q：Q038

## 口径定义

```
成员 = (org_id, chain_code, node_stage)
WHERE org_id ∈ 重点名单
  AND 上了该链且 node_stage 匹配
```

查询 JOIN（不进成员表主键）：

- `enterprise_base`：名称、`region_id`
- `enterprise_tag`：六类 `tag_code`

禁止 honor 表、禁止 `honor_type_list`、禁止把不存在的 list ADS 当源。  
禁止 `is_published` 进公式（CMS 是列表场景再滤）。  
只国内。选链/链位/类型/区域/分页是 API。

## 两步分开

① 名单 + 上链在即可列出。  
② ODS 灌数另写，不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 名单 + 上链 + 主档/标签（查询） | 表在；名单 demo |
| 目标 | `enterprise_keypano_node_enterprise_list`（`org_id + chain_code + node_stage`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。不要把 `enterprise_base` 整表复制进目标。

## 分场景 / 千万级

ETL 写全部链×链位成员。API：`WHERE chain_code=? AND node_stage=?`，再按 `tag_code` / `region_key` 过滤，分页。禁止请求路径全库扫 JOIN。

**计算公式文件**：`M_ENT_KEYPANO_ENTERPRISE_LIST.md`

## 源表字段

```
enterprise_industry_chain
enterprise_base
enterprise_tag
key_enterprise <- metric: M_ENT_KEY_TOTAL
```

来源系统：国内机构要素库、产业链要素库。

## 待建 / 缺口

无独立目标表。D3/D4 本波不升。`is_mock: true`。

---
*2026-08-30 COVER-STAT-L01：成员表；CMS/honor 不进口径*
