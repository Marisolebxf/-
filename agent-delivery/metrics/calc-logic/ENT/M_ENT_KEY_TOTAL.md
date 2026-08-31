# 重点企业总数（M_ENT_KEY_TOTAL）

> 口径真源：国内企业专利总量 ≥ 阈值 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **名单核**：重点概览清单 / 匹配数都挂本条。Q038 先用专利数，技术交易额搁置。  
> **禁止**王惠旧稿「高企∪专精特新∪上市」当重点（那是类型，不是本核）。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- 指标ID：`M_ENT_KEY_TOTAL`
- 名称：重点企业总数
- 模块：企业分析 / 企业总览
- 更新频率：周
- 关联Q：Q038（阈值 N 团队临时 = 50，仍 🟡）

## 口径定义

**国内企业**去重数：该企专利总量（跟 `M_ENT_PATENT_TOTAL`：`COUNT(DISTINCT patent_id)`，不过滤法律状态）≥ 50。

```
名单 = { org_id ∈ enterprise_base
         | COUNT(DISTINCT patent_id) ≥ 50 }
本条 = COUNT(名单)
```

- 件数只来自 `enterprise_patent_detail`，受让人已映射到 `org_id`。
- **只国内**。不 UNION `enterprise_forg_base`。港澳台 ≠ 国外。
- **禁止**技术交易额进口径（Q038 搁置）。
- **禁止**六类 / 四类 `tag_code`、上市、高新并集当「重点」。
- **禁止**选产业进本核。选链 / 选产业是 API 拿名单再过滤，不改名单本身。
- 阈值 **N = 50**（2026-08-31 徐滕强：跟 demo A1 `patent_grant_min`；件数用总量不是授权。Q038 不升 🟢）。

8 件套只留这条 COUNT。下面实现不得改口径。

## 两点分开（强制）

### ① 本条口径

专利明细在就能出名单和家数。公式完整。N 已有团队临时值。

### ② 灌数（另一回事）

项目 DWD 专利待 GDF 灌。demo `key_enterprise` 87 行 **不当接通**。N=50 不升 Q038 绿。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_patent_detail` + `enterprise_base` | 表结构在；灌数待 GDF |
| 目标 | `key_enterprise`（建议：`org_id + patent_cnt`；本条家数可另汇总一行或查询 COUNT） | **缺口：无独立生产结果表**；ADS 87 行 demo 不算 |

源 ≠ 目标。GDF 暂缓。

## 分场景 / 千万级（不进 8 件套）

| 层 | 做什么 |
|----|--------|
| ETL | 按 `org_id` 聚合专利件数，`>= 50` 写入 `key_enterprise`。查询家数 = `COUNT(*)` 该表。 |
| API | 读名单表或读家数；禁止请求路径对全专利表明算阈值。 |
| 下游 | KEYPANO 等二次 STAT 只读本条出数，不重算阈值。 |

demo 可扫小表对口径，不算接通。生产只读预聚合名单。

**计算公式文件**：`M_ENT_KEY_TOTAL.md`

## 源表字段

```
enterprise_patent_detail <- ods: dwd_patent
enterprise_patent_detail.assignee_name <- ods: dwd_patent_assignees
enterprise_base
```

计算 FROM 只用左端。不写 `gkx.dwd_*`。不写标签表 / 技术交易表。

来源系统：国内机构要素库。

## 现网探针（2026-08-27 专利叶；不进 8 件套）

- `dwd_patent` 有样例；项目 DWD 灌数未齐。
- ADS `key_enterprise` 87 行 demo（含 `patent_grant_count` / `key_score`），禁止当本条接通。
- 无生产 `key_enterprise` 结果表。

## 待建 / 缺口（不是口径算不全）

1. **Q038**：N=50 仅团队临时，不升 🟢。
2. **无独立生产目标表**。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

acceptance `Q038`；STAT。作废王惠 20260816「标签并集 COUNT」。

---
*王惠底稿 2026-08-18 入仓；2026-08-31 COVER-STAT-L01：专利阈值名单核，技术交易额/标签不进*
