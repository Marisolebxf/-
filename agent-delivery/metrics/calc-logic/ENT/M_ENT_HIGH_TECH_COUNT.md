# 高企数量（M_ENT_HIGH_TECH_COUNT）

> 口径真源：王惠底稿 → 2026-08-27 COVER-STAT-L01；**2026-08-31 改挂 `enterprise_tag.tag_code='high_tech'`**（不再 `tag_name` 模糊含）。  
> **① DWD 能数**：`enterprise_tag` 有 `high_tech` 关系就能 COUNT。  
> **② ODS→DWD**：灌数另一步，不进「无法执行」。  
> Q010 仍 🟡。无认定起止日，码在就算。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_HIGH_TECH_COUNT`
- **指标名称**：高企数量
- **一级模块**：企业分析
- **二级模块**：企业总览
- **三级模块**：企业整体概况
- **更新频率**：日
- **对齐状态**：未对齐（Q010）；判定改 `tag_code=high_tech`
- **是否在数据库**：ODS 标签有样例行；项目 DWD 待 GDF 灌数（D4 仍 mock）
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q010

## 口径定义

高新技术企业去重家数。团队临时默认：`enterprise_tag.tag_code = 'high_tech'`，按 `org_id` 去重。

```
COUNT(DISTINCT org_id)
FROM enterprise_tag
JOIN enterprise_base
WHERE tag_code = 'high_tech'
```

- 只国内。无 `enterprise_forg_tag` / `dwd_forg_*tag*`，不造表。
- **不按产业过滤**。选产业是别的页（`TYPE_COUNT` / KEYPANO），不进本条 8 件套。
- 与 `TYPE_COUNT` 的高新格子同一判定码；本条是总览一个数，不是六类分布。
- 无认定起止日：**码在就算**。曾获是否挂 `high_tech` 由 ODS→DWD 灌数决定，禁止再用 `tag_name` 含「高新技术企业」把「曾获国家级…」模糊扫进来。
- 计算键 `org_id`，JOIN `enterprise_base`，对不上 drop。
- **禁止** `tag_name` 模糊含。
- **禁止** `enterprise_type`。
- **禁止** `M_ENT_KEY_TOTAL` / 专利≥50 当高企。
- **禁止** 把六类 SUM 当本条。

## 两点分开（强制）

### ① DWD 能不能数

`enterprise_tag` 有 `tag_code='high_tech'` 就能 COUNT。公式完整，**可以算完**。

### ② ODS → DWD（另一回事）

ODS `dwd_org_tech_tag` 有没有灌进左端、曾获行挂不挂 `high_tech`，只记灌数 / D3。没灌 **不写「当前无法执行」**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `enterprise_tag` + `enterprise_base` | 表在 |
| 目标 | 建议 `ads.ent_high_tech_count`（全国一格 `high_tech_cnt`） | **缺口：无独立目标表** |

源 ≠ 目标。GDF 暂缓。生产预聚合一格即可；查询带键。禁止请求路径全表扫标签。

**计算公式文件**：`M_ENT_HIGH_TECH_COUNT.md`

## 源表字段

```
enterprise_tag <- ods: dwd_org_tech_tag
enterprise_base <- ods: dwd_org_base_info
```

计算 FROM 只用左端 DWD。右端只作家谱。不写 `tag_name` / `national_tag`。

来源系统（`source_systems`）：国内机构要素库。

## 分场景 / 千万级（不进 8 件套）

- 场景 A · 企业总览「高企数量」：全国一格 COUNT。
- 场景 B · 与类型分析高新格子对照：同一 `tag_code`，本条无产业维。
- demo：标签量小可 JOIN 现算。生产：按 `tag_code` 预聚合；禁止全表 `tag_name LIKE`。

## 现网探针（live `gkx`，2026-08-27；不进 8 件套）

- `dwd_org_tech_tag` 20000 行；含「高新技术企业」2807、「国家级高新技术企业」2054、「曾获国家级高新技术企业」1381。
- 无国外标签表。
- 这些行怎么映射到 `tag_code=high_tech` 属 ②，不改 ①。

## 待建 / 缺口

- **缺口：无独立目标表**。
- D1 仍 draft（Q010）。D3 维持 pending_ods；D4 维持 mock。本波不升。
- 认定起止日补上后才能按「有效认定期」剔曾获；当前码在就算。

## 备注

bid `§1.1.1.2.4.2.3`；STAT。与 TYPE_COUNT / KEYPANO 高新码同一套。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 只国内、暂含曾获；2026-08-31 改 `tag_code=high_tech`*
