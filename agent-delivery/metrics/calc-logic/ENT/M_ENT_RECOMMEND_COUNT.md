# 推荐企业数（M_ENT_RECOMMEND_COUNT）

> 口径真源：算法/监管 2026-09-07（招引/培育同一阈值 **70**）→ `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 STAT**：只挂两条 INDEX，不挂 SCORE。  
> 能算。只缺独立目标表。INDEX 未出数是上游。Q015 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 依赖（标明，不改上游叶）

| 顺序 | 指标 | 本条用它做什么 |
|------|------|----------------|
| 1 | `M_ENT_ATTRACTION_INDEX`（MODEL，本波不算） | 招引过阈：`attraction_index ≥ 70` |
| 2 | `M_ENT_CULTIVATION_INDEX`（MODEL，本波不算） | 培育过阈：`cultivation_index ≥ 70` |
| 3 | 本条 | 两个场景各 `COUNT(DISTINCT org_id)` |

**不挂** `M_ENT_ATTRACT_SCORE` / `M_ENT_CULTIVATE_SCORE`（已是 INDEX 别名；COUNT 仍只认 INDEX 叶）。

## 元数据

- **指标ID**：`M_ENT_RECOMMEND_COUNT`
- **指标名称**：推荐企业数
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：招引 / 培育名单规模
- **更新频率**：周（随指数批次）
- **对齐状态**：D1 aligned；阈值=70 团队临时；能算；只缺独立目标表
- **是否在数据库**：无本条计数表；INDEX 正式落表未建
- **是否在需求文档**：是
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015（权重/正式阈值待甲方；本条只用团队临时 70，不升 🟢）

## 口径定义

刻度跟 INDEX：0–100。招引 / 培育**同一阈值**。

```
招引推荐企业数 = COUNT(DISTINCT org_id) WHERE attraction_index >= 70
培育推荐企业数 = COUNT(DISTINCT org_id) WHERE cultivation_index >= 70
```

页面按招引 / 培育各读一个数。**不**把两名单 UNION 成合计（本波不拍，不进 8 件套）。

- 无指数值：**不进**该场景分子（不是 0 分过线）。
- 只国内（指数叶未并国外）。
- 选产业：先随指数过滤后再 COUNT，本条不自己 JOIN 链。
- **禁止**百分位 / TOP N 冒充 70。
- **禁止** `COUNT(*)` demo `svc_attraction_recommend` / `svc_cultivation_recommend`。
- **禁止**读 `ent_cultivate_candidate` 行数。
- **禁止**用 SCORE 冒充 INDEX。

## 两点分开（强制）

### ① 本条口径

INDEX 分在就能 `≥70` COUNT。能算。

### ② 上游出不出（另一回事）

INDEX MODEL 本波不算、无正式落表。demo `svc_*` **不当接通**。

## 落表

| 角色 | 表 | 现网 |
|------|-----|------|
| 源 | INDEX 落表 | **上游未建 / 未出数** |
| 目标 | `enterprise_recommend_summary`（建议名）：招引 / 培育各一条或一行两列 | **缺口：无此表** |

源 ≠ 目标。GDF 暂缓，不建 DDL。

## 分场景 / 实现方案

### 场景 A · 招引名单规模

INDEX 批次后：`COUNT DISTINCT org_id WHERE attraction_index >= 70` → 写招引列。

### 场景 B · 培育名单规模

同理 `cultivation_index >= 70`。

### demo / 生产

demo mock 指数表不算接通。生产：周任务等指数批次后再 COUNT；禁止请求路径现算 MODEL。

**计算公式文件**：`M_ENT_RECOMMEND_COUNT.md`

## 源表字段

二次 STAT：

```
metric: M_ENT_ATTRACTION_INDEX
metric: M_ENT_CULTIVATION_INDEX
```

不写 `gkx.dwd_*` 当 FROM。不写 demo `svc_*`。

来源系统：国内机构要素库、产业链要素库（经 INDEX 间接）。

## 现网探针（2026-08-28；不进 8 件套）

- 正式 ADS：无招引/培育指数表；无 `enterprise_recommend_summary`。
- demo：`svc_attraction_recommend` / `svc_cultivation_recommend`，禁止当源。
- `ent_cultivate_candidate` 是名单，不是本条。

## 待建 / 缺口

1. **无独立目标表**（公式只标这一条）。
2. INDEX 未出数：上游，不进无法执行。
3. Q015 正式阈值未升 🟢。
4. D3 / D4 本波不升。`is_mock: true`。

## 备注

bid `§1.1.1.2.4.2.3.7`；STAT。70 = 团队临时，对齐 demo 高档 0.7，不是甲方。禁止挂 SCORE。

---
*2026-09-07 COVER-STAT-L01：0.3.2 阈值=70；能算；只缺目标表；D1 aligned；补矩阵行*
