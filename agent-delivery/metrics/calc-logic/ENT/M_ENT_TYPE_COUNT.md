# 各类型企业数（M_ENT_TYPE_COUNT）

> 口径真源：王惠底稿 → 2026-08-27 COVER-STAT-L01；**2026-08-30 六类一律改挂 `enterprise_tag.tag_code`**（外资/上市/小微不再走主档或「无法计算」）。  
> **① DWD 能数**：`enterprise_tag` 有六类关系就能 COUNT。  
> **② ODS→DWD**：灌数另一步，不进「无法执行」。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TYPE_COUNT`
- **指标名称**：各类型企业数
- **一级模块**：企业分析
- **二级模块**：重点企业类型分析
- **三级模块**：类型与区域分析
- **更新频率**：月度/年度
- **对齐状态**：六类全部走 DWD 标签关系；小微=`sme`
- **关联Q编号**：Q010（判定边界，不否定 ①）

## 口径定义

按六类分别 `COUNT(DISTINCT org_id)`：外资 / 高新 / 小微 / 上市 / 专精特新 / 小巨人。

- 六类不是互斥维，**一企可进多类**。禁止把六类 SUM 当企业总数。
- **一律** `enterprise_tag.tag_code`（`tag_dict`），不再分类走主档。

| 类型 | `tag_code` | 禁止 |
|------|------------|------|
| 高新 | `high_tech` | 仅用 `tag_name` 含（本条改码） |
| 专精特新 | `little_giant` | — |
| 小巨人 | `little_giant_pro` | — |
| 小微 | `sme` | `org_size`；`sme_tech` |
| 外资 | `foreign` | `enterprise_type` 含外商 |
| 上市 | `listed` | `is_listed` |

- 只国内。无 `enterprise_forg_tag`，不造表。选产业后国外无上链，不并入。
- 计算键 `org_id`，JOIN `enterprise_base`，对不上 drop。

## 计算逻辑说明

```
对每一类 t ∈ 上表六个 tag_code:
  COUNT(DISTINCT org_id)
  FROM enterprise_tag
  JOIN enterprise_base
  WHERE tag_code = t
```

选产业：再 JOIN `enterprise_industry_chain`。

曾获/过期：无起止日则码在就算，与 HIGH_TECH 临时默认一致。

## 两步分开（强制）

### ① DWD 能不能数

`enterprise_tag` 有该 `tag_code` 关系就能 COUNT。六类公式完整，**可以算完**（含小微/外资/上市）。

### ② ODS → DWD（另一回事）

ODS 有没有灌进左端标签表，只记灌数 / D3。没灌 **不写「当前无法执行」**。

现网 ODS `dwd_org_tech_tag` 可能没有「小微/外资/上市」字样，**不能据此说本条算不了**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_tag` + `enterprise_base`（+ 选产业时上链表） | 表在 |
| 目标 | 建议 `enterprise_type_count`（`tag_code + chain_code? + type_count`） | **缺口：无独立目标表** |

源 ≠ 目标。GDF 暂缓。生产按六类（×可选链）预聚合；查询带条件键。

**计算公式文件**：`M_ENT_TYPE_COUNT.md`

## 源表字段

```
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_base <- ods: dwd_org_base_info
enterprise_industry_chain <- ods: dwd_org_industry_tags
```

计算 FROM 只用左端 DWD。右端只作家谱。不写 `is_listed` / `enterprise_type` / `org_size`。

来源系统：国内机构要素库、产业链要素库。

## 现网探针（不进 8 件套）

- DWD `tag_dict` 已有六类码（2026-08-30 对照 `gkxlumenx_dwd_tag_dict_align.sql`）。
- ODS 标签样例原先多是高新/专精特新/小巨人：记在 ②，不改 ①。
- 无国外标签表。

## 待建 / 缺口

- 无独立目标表。
- D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。与 KEYPANO_TYPE_COUNT / TYPE_RATIO 同一套码。

---
*2026-08-27 六类分类 COUNT；2026-08-30 外资/上市/小微改挂 tag_code*
