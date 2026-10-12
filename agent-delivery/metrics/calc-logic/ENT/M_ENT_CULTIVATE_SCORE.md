# 培育推荐评分（M_ENT_CULTIVATE_SCORE）

> 口径真源：算法 2026-09（都留 ID；公式=INDEX 三维，第三维=企业潜力）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 COMPUTE / 别名**：`cultivate_score = M_ENT_CULTIVATION_INDEX`。不另算第二套三维。  
> 能算。只缺独立目标表（查询读 INDEX 落表）。INDEX 未出数是上游。Q015 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_CULTIVATION_INDEX`（MODEL，本波不算） | 三维加权：产业相关 / 政策匹配 / **企业潜力**。本条直接取该综合分 |
| 2 | 本条 | 同一数值，保留独立 `metric_id` |

不改 INDEX 叶。企业潜力算法在 INDEX。Q015 仍 🟡。

## 元数据

- **指标ID**：`M_ENT_CULTIVATE_SCORE`
- **指标名称**：培育推荐评分
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：培育推荐
- **更新频率**：周（读 INDEX 最新批次）
- **对齐状态**：D1 aligned；别名 INDEX；能算；只缺独立目标表
- **是否在数据库**：无独立 SCORE 表；读 INDEX 落表
- **是否在需求文档**：是（与 INDEX 同验收单元 E-27）
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015；Q018（痛点不转分，本条已不碰）

## 口径定义

每个企业一条培育分：

```
cultivate_score(org_id) = M_ENT_CULTIVATION_INDEX(org_id)
```

三维（只在 INDEX 叶算，本条不重写）：产业相关度、政策匹配度、企业潜力。

**丢掉** 2026-08-28 demo 快路径：`(potential+growth+recovery)/3`。  
恢复项已改成企业潜力，**不再碰** diagnosis / 痛点。

**禁止**：

- 另算一套三维
- 读 `ads.enterprise_score.score_total`
- 挂 `M_ENT_GROWTH_POTENTIAL` / `M_ENT_REVENUE_GROWTH_RATE` 当本条三维
- Q018：痛点严重度 / `enterprise_diagnosis` **不转**企业得分（`(100-penalty)` 禁止）
- 把 `ent_cultivate_candidate` 当落分表
- 本波升 D3/D4、升 Q015

INDEX 无值：**该企本条空**。整波未出数：名单空。不进「无法执行」。

## 两点分开（强制）

### ① 本条口径

INDEX 出分 → 原样读。能算。

### ② 上游出不出（另一回事）

INDEX MODEL 本波不算。企业潜力归属语义（GAP-RECRUIT-METRIC-02）记在 INDEX 叶。  
diagnosis mock **不当接通**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | INDEX 落表（随 `M_ENT_CULTIVATION_INDEX`） | **上游未建 / 未出数** |
| 目标 | **无独立目标表**。查询直接读 INDEX 落表，不另建 `enterprise_cultivate_score` | 不建 |

GDF 不为本条建 DDL。

## 分场景 / 实现方案

### 场景 A · 单企

`org_id` 查 INDEX 综合分。无行：空。

### 场景 B · 培育名单

`ORDER BY cultivation_index DESC`。禁止扫 diagnosis mock。

### demo / 生产

demo 可对小表对口径，不算接通。生产：INDEX 批次出数后读；禁止请求路径现算三维。`RECOMMEND_COUNT` 培育侧仍只挂 INDEX，不挂本条。

**计算公式文件**：`M_ENT_CULTIVATE_SCORE.md`

## 源表字段

二次 COMPUTE：

```
metric: M_ENT_CULTIVATION_INDEX
```

不写 `gkx.dwd_*` 当 FROM。不进增长率 / GROWTH_POTENTIAL / diagnosis。

来源系统：国内机构要素库、产业链要素库（经 INDEX 间接）。

## 现网探针（2026-08-28；不进 8 件套）

- 无独立 `cultivate_score` 列。`ent_cultivate_candidate` 不是本条。
- `enterprise_diagnosis` 120 行 mock，无 penalty，禁止转分。
- INDEX 正式落表未建。

## 待建 / 缺口

1. **无独立目标表**（公式只标这一条；读 INDEX 落表）。
2. INDEX 未出数：上游，不进无法执行。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.7`；COMPUTE。ID 保留。禁止痛点转分。禁止 ADS mock 假接通。

---
*2026-09-07 COVER-STAT-L01：0.3.2 别名 INDEX；能算；只缺独立目标表；D1 aligned*
