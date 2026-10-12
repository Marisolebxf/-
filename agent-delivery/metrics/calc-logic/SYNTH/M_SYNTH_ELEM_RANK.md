# 对比范围要素综合排名（M_SYNTH_ELEM_RANK）

> 口径真源：Q-SYNTH-02 → 2026-08-31 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：只排 `M_SYNTH_ELEM_INDEX`，不算类型/层次/领域。跟 `M_SYNTH_VIT_RANK` / 企业 `TECH_RANK` 同规矩。  
> 指数未出数前禁止对外决策展示。Q-SYNTH-02 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-SYNTH-seed.yaml`。

## 依赖（强制）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_SYNTH_ELEM_INDEX` | 要素综合指数（MODEL，本波不算） |
| 2 | 本条 | 当前对比范围内按指数降序 RANK |

## 元数据

- 指标ID：`M_SYNTH_ELEM_RANK`
- 名称：对比范围要素综合排名
- 模块：E8 区域创新要素
- 更新频率：随指数批次
- 关联Q：Q-SYNTH-02

## 口径定义

目标区域在所选对比范围内，按要素综合指数降序的名次。

默认对比范围与 `VIT_RANK` 同一份：北京、上海、广州、深圳、杭州、南京、武汉、重庆、宁波、成都、合肥（宁=宁波，可追加）。

```
RANK() OVER (ORDER BY elem_index DESC)
  于当前对比范围 ∩ 已出指数的区域
无指数 → 不进榜
同分并列（RANK，下一名跳号）
```

- 选对比范围 / 时间窗是 API。筛选变了必须对当前可比集重算，禁止抄全库总榜。
- 本条不算三维权重、不写贡献路径。
- **禁止**用类型指数 / 层次指数 / 领域指数单独冒充综合指数来排。
- **禁止**对外决策使用，直到 Q-SYNTH-02 闭合。

8 件套只留这条 RANK。

## 两点分开（强制）

### ① 本条口径

RANK 公式完整。依赖已钉 `ELEM_INDEX`。

### ② 当前无法执行

指数 MODEL 未出数。演示等权指数不当接通。不进「口径未定」。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | 指数结果（`<- metric: M_SYNTH_ELEM_INDEX`） | 无正式指数表 |
| 目标 | `ads.synth_elem_rank`（建议：对比范围键 + `region_id` + `elem_rank`） | **缺口：无此表** |

源 ≠ 目标。生产禁止请求路径全表窗口现算。

## 分场景 / 千万级（不进 8 件套）

- 默认快照：深圳 × 全国重点城市 × 近 3 年，读跑批排名。
- 改条件：跟指数批次重算后再 RANK。
- demo 有演示指数：**不算接通**。

**计算公式文件**：`M_SYNTH_ELEM_RANK.md`

## 源表字段

```
<- metric: M_SYNTH_ELEM_INDEX
```

无 ODS 右端。`source_systems` 不写 `Mock @ batch`。

## 待建 / 缺口

1. `M_SYNTH_ELEM_INDEX` 出数（MODEL 波）。
2. **无独立目标表**。
3. D3 / D4 本波不升。`is_mock: true`。Q-SYNTH-02 🟡。

---
*2026-08-31 COVER-STAT-L01：RANK 挂 ELEM_INDEX；当前无法执行*
