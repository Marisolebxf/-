# 创新型企业数（M_ENT_INNOVATIVE_COUNT）

> 口径真源：算法 2026-09（四类并集，曾获算）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> 判定只走 `enterprise_tag.tag_code`。源中文 `org_tag` 由项目映射到码，属洗数。Q011 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 四码（项目编，源给中文即可）

| 中文（源 `org_tag`） | `tag_code` |
|----------------------|------------|
| 专精特新 | `little_giant` |
| 小巨人 | `little_giant_pro` |
| 制造业单项冠军 | `manufacturing_champion`（本波新编） |
| 创新型中小企业 | `innovative_sme`（本波新编；**不是** `sme_tech`） |

含「曾获 / 过期」落到同一码，**算**。不含高企 / 瞪羚 / 独角兽。禁止 `tag_name` 模糊含。

## 元数据

- 指标ID：`M_ENT_INNOVATIVE_COUNT`
- 名称：创新型企业数
- 更新频率：日
- 关联Q：Q011
- 对齐：D1 aligned（算法 2026-09）

## 口径定义

```
COUNT(DISTINCT org_id)
FROM enterprise_tag JOIN enterprise_base
WHERE tag_code IN (
  'little_giant',
  'little_giant_pro',
  'manufacturing_champion',
  'innovative_sme'
)
```

- 只国内。无 `enterprise_forg_tag`，不造表。
- 选产业：国内经 `enterprise_industry_chain` 半连接；未选不按产业滤。国外无上链不并。
- 计算键 `org_id`。

## 两点分开

### ① 口径

DWD 有 `enterprise_tag.tag_code` 就能 COUNT。四码已定，**能算**。

### ② 有没有数

中文未洗进两新码 = 灌数，不进「无法执行」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_tag` + `enterprise_base` | 有表 |
| 目标 | 建议 `ads.ent_innovative_count` | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。

## 分场景 / 实现方案

### 场景 A · 未选产业

标签 ∩ 主档，四码并集去重 COUNT。

### 场景 B · 选了产业

上一步结果半连接上链表。生产禁止请求路径扫全库标签。

### demo

行少可直查。禁止用 `tag_name` LIKE 顶码。

## 源表字段

```
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端。`dwd_org_tech_tag.org_tag` → `tag_code`。来源系统：国内机构要素库、产业链要素库。

## 现网探针（2026-08-27；不进 8 件套）

- `dwd_org_tech_tag`：中文四类有样例（含省级/国家级、曾获/过期变体）。
- 无国外标签表。
- `tag_dict` 原无后两码，本波公式已编，灌字典是实现。

## 待建 / 缺口

1. **无独立目标表**。
2. 后两码进 `tag_dict` + 中文对照（洗数，不挡口径）。
3. D3/D4 本波不升。`is_mock: true`。

---
*2026-09-07 COVER-STAT-L01：0.3.1 四码可算；只缺目标表；D1 aligned*
