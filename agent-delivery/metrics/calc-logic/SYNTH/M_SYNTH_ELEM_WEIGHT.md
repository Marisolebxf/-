# 类型/层次/领域权重分布（M_SYNTH_ELEM_WEIGHT）

> 口径真源：算法 2026-09 回填（各 1/3、展示=否）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：读类型/层次/领域三条 MODEL 指数，再乘本条权，刷出区域要素综合分。  
> 跟 `M_SYNTH_VIT_WEIGHT` 同规矩。Q-SYNTH-E-01 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-SYNTH-seed.yaml`。

## 依赖（强制，先于本条）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_SYNTH_ELEM_INDICATOR`（MODEL） | 三维下分项原值+得分 |
| 2 | `M_SYNTH_ELEM_TYPE_INDEX` | 类型维一条分 |
| 3 | `M_SYNTH_ELEM_LEVEL_INDEX` | 层次维一条分 |
| 4 | `M_SYNTH_ELEM_DOMAIN_INDEX` | 领域维一条分 |
| 5 | 本条权 | 各 1/3，合计 1 |
| 6 | 刷分 | `Σ index(维) × w(维)` |

不挂 `TYPE_SCORE` / `LEVEL_SCORE`（那是七要素各自分，不是三维合成输入）。  
上游设计：算法库 §10.6–10.8。本波不改那些 MODEL seed。

## 元数据

- 指标ID：`M_SYNTH_ELEM_WEIGHT`
- 名称：类型/层次/领域权重分布
- 模块：E8 区域创新要素
- 更新频率：随三维 INDEX 批次
- 关联Q：Q-SYNTH-E-01；综合公式另见 Q-SYNTH-02（INDEX 叶）

## 口径定义

区域一条要素综合分：

```
w_type = w_level = w_domain = 1/3
w 合计必须 = 1，否则该次无法计算

elem_score =
    (1/3) × type_index
  + (1/3) × level_index
  + (1/3) × domain_index

type_index   <- metric: M_SYNTH_ELEM_TYPE_INDEX
level_index  <- metric: M_SYNTH_ELEM_LEVEL_INDEX
domain_index <- metric: M_SYNTH_ELEM_DOMAIN_INDEX
```

- 缺任一维指数：该区域该次无法计算，不拿 0 顶。
- 无阈值、不再二次归一（归一在各维 INDEX 内）。
- 产品「计算方法」**不展示**权重表。
- 禁止按页面改权。禁止用七要素 SCORE 加总冒充三维分。
- 禁止读 demo 等权指数当已接通。

## 两点分开（强制）

### ① 本条口径

权已钉。三维 INDEX 有值就能刷 `elem_score`。

### ② 上游出不出

三条 INDEX / INDICATOR 仍 pending、专题库未建。这是 MODEL 叶缺口，**不改本条公式**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 三条 `*_INDEX` | MODEL 未出数 |
| 目标 | `ads.synth_elem_weight` 建议：`region_id + window`，列 `w_*` + `elem_score` | **缺口：无此表** |

源 ≠ 目标。本波不建 GDF DDL。

## 分场景 / 实现方案

### 场景 A · 跑批刷分

三维 INDEX 批次齐后点查乘权写入。禁止请求路径现算全库。

### 场景 B · 默认快照

读已刷 `elem_score`。缺维该行空。

### demo

演示等权 **不算接通**。

**计算公式文件**：`M_SYNTH_ELEM_WEIGHT.md`

## 源表字段

```
<- metric: M_SYNTH_ELEM_TYPE_INDEX
<- metric: M_SYNTH_ELEM_LEVEL_INDEX
<- metric: M_SYNTH_ELEM_DOMAIN_INDEX
```

无 ODS 右端。`source_systems` 不写 `Mock @ batch`。

## 待建 / 缺口

1. 三条维 INDEX 出数。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。Q-SYNTH-E-01 / Q-SYNTH-02 仍 🟡。

---
*2026-09-07 COVER-STAT-L01：权 1/3×3；formula 挂三维 INDEX 刷分*
