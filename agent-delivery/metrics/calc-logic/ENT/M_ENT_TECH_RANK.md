# 技术力排名（M_ENT_TECH_RANK）

> 口径真源：王惠《企业分析模型指标字段清单》20260816 底稿 → 2026-08-27 `ENT-SYNTH-METRIC-COVER-STAT-L01`。二次 STAT：排的是 SCORE 产物，不是 DWD 原料。Q014 挂 SCORE。
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_TECH_RANK`
- **指标名称**：技术力排名
- **一级模块**：企业分析
- **二级模块**：企业评估
- **三级模块**：技术力评估
- **更新频率**：周（随 SCORE 批次）
- **对齐状态**：FROM 已锁 ADS `tech_power`；排序键未等同招标五维闭合（随 SCORE）
- **是否在数据库**：ADS `tech_power` 有分与 `rank_overall`（demo 批次）；DWD 无 `tech_score`
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q014（随 `M_ENT_TECH_POWER_SCORE`）

## 口径定义

按技术力分在可比集内降序排名。

- **未选产业 = 全国有分都进榜**（查询不滤 = 底层默认窗口是全国）。不是「不计算」。
- **选了产业 = 只在该产业有分企业里 RANK**。选产业是 API 选窗口。
- COUNT 类指标的「未选」只是不滤预聚合；RANK 的窗口会改名次，所以默认窗口要写死为全国。

- 排序键：`tech_power.tech_power_index`（ADS）。
- 无分不进榜。
- 同分并列（`RANK()`，下一名跳号）。
- **依赖** `M_ENT_TECH_POWER_SCORE` 先出分；本条只做 RANK，不算五维。
- 禁止抄 `rank_overall`：那是全库总榜，筛选变了必须对当前可比集重算。
- 禁止用 `enterprise_score`（创新/经营/成长）、`brand_score`、`core_tech_coverage`、专利量顶替。
- 只国内。国外无对等 ADS 表，暂不并。
- 产业：用当前筛选限定可比集，不是分组维另出一张榜。

## 计算逻辑说明

```
RANK() OVER (ORDER BY tech_power_index DESC)
  于当前筛选企业 ∩ tech_power.org_id
无 tech_power_index → 不进榜
```

对应 seed `formula`：RANK 于当前可比集；禁止 `rank_overall`。

**计算公式文件**：`M_ENT_TECH_RANK.md`

## 源表字段

本波例外：二次 STAT 左端允许 ADS 结果表，右端写指标依赖，不写 ODS。

```
tech_power <- metric: M_ENT_TECH_POWER_SCORE
```

完整链（细稿，不进 8 件套左端）：ADS `tech_power` ← SCORE/MODEL ← DWD 原料 ← ODS。GDF：DWD **勿建** `enterprise_score`。

来源系统（`source_systems`）：国内机构要素库（SCORE 原料侧）。不写 ADS 库名、行数、`Mock @ batch`。

## 现网探针

- `gkxlumenx_ads.tech_power`：120 行；字段 `tech_power_index` + 五维 + `rank_overall`；`model_version=ahp_weighted_v0.1-demo`。
- `demo_gkxlumenx_ads.tech_power`：100 行。
- `demo_gkxlumenx_ads.svc_tech_power_score`：283 行（Q060 注释）；正式 ADS **无**此表，不作为 FROM。
- DWD `enterprise_base`：无 `tech_score`。
- `enterprise_score`（ADS）：`score_innov/operate/growth`，不是技术力。

## 待建 / 缺口

- SCORE 五维是否 = 招标 Q014：MODEL 叶，本波不改 `M_ENT_TECH_POWER_SCORE`。
- 现网分是 demo 批次，本波 `is_mock=true`。
- 国外无对等分表。
- D3 维持 pending_ods；D4 维持 mock。本波不升。

## 备注

bid `§1.1.1.2.4.2.3.3`；STAT。COVER-STAT-L01 仅本条开 ADS FROM 例外。同类商业力/竞争力排名未点头不准套。

---
*王惠 20260816 底稿正式化 2026-08-18；2026-08-27 COVER-STAT-L01 RANK 挂 tech_power_index*
