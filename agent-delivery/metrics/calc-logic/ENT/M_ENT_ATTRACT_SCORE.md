# 招引推荐评分（M_ENT_ATTRACT_SCORE）

> 口径真源：算法 2026-09（都留 ID；公式=INDEX 三维）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 COMPUTE / 别名**：`attract_score = M_ENT_ATTRACTION_INDEX`。不另算第二套三维。  
> 能算。只缺独立目标表（查询读 INDEX 落表）。INDEX 未出数是上游。Q015 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_ATTRACTION_INDEX`（MODEL，本波不算） | 三维加权：产业相关 / 政策匹配 / 深圳连接。本条直接取该综合分 |
| 2 | 本条 | 同一数值，保留独立 `metric_id` |

不改 INDEX 叶。权重 / 归一化 / 深圳连接度贴源仍在 INDEX。Q015 仍 🟡。

## 元数据

- **指标ID**：`M_ENT_ATTRACT_SCORE`
- **指标名称**：招引推荐评分
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：招引推荐
- **更新频率**：周（读 INDEX 最新批次）
- **对齐状态**：D1 aligned；别名 INDEX；能算；只缺独立目标表
- **是否在数据库**：无独立 SCORE 表；读 INDEX 落表
- **是否在需求文档**：是（与 INDEX 同验收单元 E-26）
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015

## 口径定义

每个企业一条招引分：

```
attract_score(org_id) = M_ENT_ATTRACTION_INDEX(org_id)
```

三维（只在 INDEX 叶算，本条不重写）：产业相关度、政策匹配度、深圳连接度。

**丢掉** 2026-08-28 demo 快路径：`(tech_proxy+growth+regional)/3 − 0.2×risk`。

**禁止**：

- 另算一套三维（两套数）
- 读 `ads.enterprise_score.score_total` / `score_innov` / `score_growth`
- 挂 `M_ENT_TECH_POWER_SCORE` / `M_ENT_REVENUE_GROWTH_RATE` / 风险 STAT
- 把 INDEX 的深圳连接度换成风险扣分
- 本波升 D3/D4、升 Q015

INDEX 无值：**该企本条空**（不是 0）。整波 INDEX 未出数：名单空。不进「无法执行」。

## 两点分开（强制）

### ① 本条口径

INDEX 出分 → 原样读。能算。

### ② 上游出不出（另一回事）

INDEX MODEL 本波不算；深圳连接度贴源、政策词典在 INDEX 叶。  
`ads.enterprise_score` **不当接通**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | INDEX 落表（随 `M_ENT_ATTRACTION_INDEX`） | **上游未建 / 未出数** |
| 目标 | **无独立目标表**。查询直接读 INDEX 落表，不另建 `enterprise_attract_score` | 不建 |

源 ≠ 另落一份。GDF 不为本条建 DDL。

## 分场景 / 实现方案

### 场景 A · 单企

`org_id` 查 INDEX 综合分，当作本条分。无 INDEX 行：空。

### 场景 B · 招引名单

`ORDER BY attraction_index DESC`。无数：名单空。禁止扫 `enterprise_score` mock。

### demo / 生产

demo 可对小表对口径，不算接通。生产：INDEX 批次出数后读；禁止请求路径现算三维。`RECOMMEND_COUNT` 招引侧仍只挂 INDEX，不挂本条。

**计算公式文件**：`M_ENT_ATTRACT_SCORE.md`

## 源表字段

二次 COMPUTE：

```
metric: M_ENT_ATTRACTION_INDEX
```

不写 `gkx.dwd_*` 当 FROM。不进技术力 / 增长率 / 风险。

来源系统：国内机构要素库、产业链要素库（经 INDEX 间接）。

## 现网探针（2026-08-28；不进 8 件套）

- 无独立 `enterprise_attract_score` / `attract*` 列。
- `gkxlumenx_ads.enterprise_score` 120 行 mock，禁止当本条。
- INDEX 正式落表未建。

## 待建 / 缺口

1. **无独立目标表**（公式只标这一条；读 INDEX 落表）。
2. INDEX 未出数：上游，不进无法执行。
3. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.6`；COMPUTE。ID 保留。不与 INDEX 废掉其中一个。禁止 ADS mock 假接通。

---
*2026-09-07 COVER-STAT-L01：0.3.2 别名 INDEX；能算；只缺独立目标表；D1 aligned*
