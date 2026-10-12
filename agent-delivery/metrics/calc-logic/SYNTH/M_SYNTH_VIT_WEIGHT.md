# 维度权重分布（M_SYNTH_VIT_WEIGHT）

> 口径真源：算法 2026-09 回填（各 0.25、展示=否）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：读 `M_SYNTH_VIT_DIM_SCORE` 四维 MODEL 分，再乘本条权，刷出区域活力分。  
> 权是参数；分来自上游 MODEL。Q-SYNTH-V-01 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-SYNTH-seed.yaml`。

## 依赖（强制，先于本条）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_SYNTH_VIT_INDICATOR`（MODEL） | 四维下分项原值+得分；正式清单 Q-SYNTH-01 |
| 2 | `M_SYNTH_VIT_DIM_SCORE`（MODEL） | 科技/产业/人才/政策各一条单维分 |
| 3 | 本条权 | 各 0.25，合计 1 |
| 4 | 刷分 | `Σ dim_score(维) × w(维)` → 写入目标列（供 INDEX / 后续批次读） |

DIM 上游设计：算法库 §10.1–10.4（科技/产业/人才/政策专题综合评价）。本波不改那四叶 MODEL seed。

## 元数据

- 指标ID：`M_SYNTH_VIT_WEIGHT`
- 名称：维度权重分布
- 模块：E8 区域创新活力
- 更新频率：随 DIM 批次
- 关联Q：Q-SYNTH-V-01（权）；Q-SYNTH-01（分项池，在 INDICATOR 叶）

## 口径定义

区域一条活力分：

```
w_tech = w_industry = w_talent = w_policy = 0.25
w 合计必须 = 1，否则该次无法计算

vit_score =
    0.25 × dim_score_tech
  + 0.25 × dim_score_industry
  + 0.25 × dim_score_talent
  + 0.25 × dim_score_policy

dim_score_* <- metric: M_SYNTH_VIT_DIM_SCORE
```

- 缺任一维分：该区域该次无法计算，不拿 0 顶。
- 无阈值、不再二次归一（归一在 DIM_SCORE 内）。
- 产品「计算方法」**不展示**权重表（算法：展示=否）。
- 禁止按页面改权。禁止用 ENT STAT（高企/专利家数）冒充维分。
- 禁止读 demo 等权指数当已接通。

8 件套只留上面这条刷分公式。分项怎么合成维分，在 DIM_SCORE / INDICATOR 叶。

## 两点分开（强制）

### ① 本条口径

权已钉。公式完整：DIM 四条有值就能刷 `vit_score`。

### ② 上游出不出（另一回事）

`M_SYNTH_VIT_DIM_SCORE` / `INDICATOR` 公式仍 pending、专题库未建、D4=mock。这是 MODEL 叶缺口，**不改本条公式**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | `M_SYNTH_VIT_DIM_SCORE` 四维分 | MODEL 未出数 |
| 目标 | `ads.synth_vit_weight` 建议：`region_id + window` 一行，列 `w_*` + `vit_score` | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。

## 分场景 / 实现方案

### 场景 A · 跑批刷分（生产）

DIM 批次齐后，按区域+时间窗点查四维分，乘权写入目标表。禁止请求路径现算全库。

### 场景 B · 默认快照

深圳 × 近 3 年：读已刷 `vit_score`。DIM 缺维则该行空。

### demo

演示等权指数 **不算接通**。不要用 mock 分顶公式。

**计算公式文件**：`M_SYNTH_VIT_WEIGHT.md`

## 源表字段

```
<- metric: M_SYNTH_VIT_DIM_SCORE
```

无 ODS 右端。`source_systems` 不写 `Mock @ batch`。INDICATOR / §10.1–10.4 写在依赖表，不进 8 件套 `source_tables`。

## 待建 / 缺口

1. `M_SYNTH_VIT_DIM_SCORE` 出数（再上游 `INDICATOR` + 四专题库）。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。Q-SYNTH-V-01 / Q-SYNTH-01 仍 🟡。

---
*2026-09-07 COVER-STAT-L01：权 0.25×4；formula 挂 DIM_SCORE 刷分*
