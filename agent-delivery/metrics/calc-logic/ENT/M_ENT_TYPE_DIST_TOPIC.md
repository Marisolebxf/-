# 重点企业类型分布（M_ENT_TYPE_DIST_TOPIC）

> 口径真源：专题 OPEN seq 40 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：先 `M_ENT_KEY_TOTAL`（专利总量 ≥ 50），再按招标四类 `tag_code` 分组。  
> OPEN 原文「对象=产业名录、不改挂 Q038」已由 2026-08-31 human:徐滕强 覆盖：对象暂定专利名单。Q038 / Q072 仍 🟡。  
> 不 reuse `M_ENT_TYPE_COUNT`（六类、无名单核）。不 reuse `KEYPANO_TYPE_STRUCTURE`（六类 × 链位）。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 依赖 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_KEY_TOTAL` / Q038 | 重点名单（专利 ≥ 50） |
| 2 | `enterprise_tag` | 四类 `tag_code` |
| 3 | `enterprise_industry_chain` | 选产业过滤（API） |
| 4 | 本条 | 年 × 四类 COUNT + 占比 + 环比 |

禁止用四类 / 六类并集重写重点。门槛只在 `KEY_TOTAL`。

## 元数据

- 指标ID：`M_ENT_TYPE_DIST_TOPIC`
- 名称：重点企业类型分布
- 模块：专题企业 / TOPIC-ENT-05
- 更新频率：年
- 关联Q：Q072 / Q-MO-ENT-01（A 四类，仍 🟡）；Q038（N=50，仍 🟡）

## 口径定义

自然年：重点名单内，招标四类各去重家数、占当期名单占比、相对上年环比。

```
COUNT(DISTINCT t.org_id)
FROM enterprise_tag t
WHERE t.org_id ∈ key_enterprise
  AND t.tag_code = :t
GROUP BY stat_year, t.tag_code
```

四类：`foreign` / `high_tech` / `sme` / `listed`。  
禁止 `little_giant` / `little_giant_pro`。  
禁止 `enterprise_type` / `is_listed` / `org_size` / `sme_tech`。

占比：

```
type_cnt / list_cnt
```

`list_cnt` = 同一自然年、同一产业过滤后的名单去重家数。分母 0 → 占比空。  
一企可进多类，四类 SUM 禁止当总数，合计可 >100%。

环比（同一 `tag_code`）：

```
(cnt_y - cnt_y-1) / cnt_y-1
```

上年 0 或空 → 环比空。

- **选产业是 API**：ETL 全量年×四类（及需要的链键）。禁止把「当前所选产业」写进 GROUP BY。
- 只国内。无国外标签，不 UNION。
- 筛选壳不是本核。不另造重点门槛 ID。

8 件套只留这条 COUNT + 占比 + 环比。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

名单 + 四类标签关系在就能 GROUP BY。公式完整。依赖标明 `KEY_TOTAL`。

### ② 灌数 / 阈值（另一回事）

专利灌数、标签灌数、N=50 未甲方确认。不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `key_enterprise` / `enterprise_tag` / 上链表 | 名单无生产结果表；标签表在 |
| 目标 | `enterprise_type_year_dist`（建议：`stat_year + tag_code + org_cnt + share + wow`） | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 每年全量年×四类写入目标表；`share` / 环比用上年同行。 |
| API | 按年 / `tag_code` / 链键过滤；禁止请求路径现算。 |
| 前端 | 选产业 = 带链键查行。 |

**计算公式文件**：`M_ENT_TYPE_DIST_TOPIC.md`

## 源表字段

```
key_enterprise <- metric: M_ENT_KEY_TOTAL
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

二次 STAT：名单右端写 `metric:`，不把专利 ODS 再写一遍。

来源系统：国内机构要素库、产业链要素库。

## 待建 / 缺口（不是口径算不全）

1. `KEY_TOTAL` 生产名单表；Q038 / Q072 🟡。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `TOPIC-ENT-05`；STAT。与 `KEYPANO_TYPE_STRUCTURE` 并列：本条年×四类+占比+环比，那条链×链位×六类。

---
*2026-08-31 COVER-STAT-L01：对象=KEY_TOTAL；四类 tag_code；选产业是 API*
