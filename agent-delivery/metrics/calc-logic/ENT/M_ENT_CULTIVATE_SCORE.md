# 培育推荐评分（M_ENT_CULTIVATE_SCORE）

> 口径真源：seed「demo 快路径」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 COMPUTE**：挂上游分数等权，不从 ODS 现算。与招引评分对称。  
> **不强行结项**：口径留下，缺口摊开，当前无法执行。不与 `M_ENT_CULTIVATION_INDEX` 合并。Q015 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_CULTIVATE_SCORE`
- **指标名称**：培育推荐评分（demo路径）
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：培育推荐
- **更新频率**：周
- **对齐状态**：二次分口径已写；上游未出数；恢复项无合法挂接；无目标表
- **是否在数据库**：无 `cultivate_score` 列、无独立落分表；ADS `enterprise_score` / `enterprise_diagnosis` 是另一套 mock
- **是否在需求文档**：是（与 INDEX 并行，待 Q015）
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015（权重）；恢复项另受 Q018（痛点严重度不转得分）

## 口径定义

每个企业一条培育分，倒序可用于名单。

**目标**（团队临时默认 🟡，与招引条等权对齐；非甲方闭合）：

```
cultivate_score = (potential + growth + recovery) / 3
```

三项假定 0–100 同刻度。

| 分项 | 挂什么 | 现状 |
|------|--------|------|
| `potential` | `M_ENT_GROWTH_POTENTIAL` | MODEL，Q015，本波不算 |
| `growth` | `M_ENT_REVENUE_GROWTH_RATE` | STAT 已定口径；ODS 相邻年营收几乎没几家 |
| `recovery` | **无合法上游** | Q018：痛点严重度只作阅读优先级，**不转企业得分**。不能 `(100-penalty)`。ADS `enterprise_diagnosis` 无 `penalty` 列，120 行 mock |

与 `M_ENT_CULTIVATION_INDEX`（产业相关 / 政策匹配 / 企业潜力）**并行**，本波不合并。  
INDEX 的「企业潜力」≠ demo 的 `score_total`，也不等于本条 `potential` 在 GROWTH_POTENTIAL 出数之前的占位。

**禁止**：

- 读 `ads.enterprise_score.score_total` 当潜力
- 读 `enterprise_diagnosis.weaknesses` / `diag_level` 转恢复分
- 用 Q018 严重度档转 0–100
- 把 `ent_cultivate_candidate` 当本条落分表（那是名单）
- 本波升 D3/D4、升 Q015、与 INDEX 合并、结 COVER 叶

无三分齐全：**该企无法计算**。潜力整波无出数、恢复项无上游 → **整条当前无法执行**。

## 落表

| 目标 | 粒度 | 写什么 | 现网 |
|------|------|--------|------|
| `enterprise_cultivate_score`（建议名） | `org_id` 一条 | `cultivate_score` | **缺口：无此表** |

正式 / demo DWD、ADS 均无 `cultivate_score` 列。`gkxlumenx_topic_enterprise.ent_cultivate_candidate` 不是本条。  
GDF 暂缓，不建 DDL。**是否建表、用何表名：待后续讨论**。

## 分场景 / 实现方案

### 场景 A · 单企

上游三分都有值之后写入目标表。缺任一项该企空，不用 mock 凑。

### 场景 B · 培育名单

读目标表倒序。无表 / 无数：名单空。禁止扫 diagnosis mock。

### demo / 生产

两边都算不出。demo/正式 `enterprise_diagnosis` 120 行 mock 不是捷径。  
生产：先等 GROWTH_POTENTIAL 出数、增长率落表、恢复项另定指标（且不违反 Q018），再周任务写入目标表。

对应 seed `formula`：等权二次分 + **当前无法执行**。

**计算公式文件**：`M_ENT_CULTIVATE_SCORE.md`

## 源表字段

```
enterprise_finance_history <- metric: M_ENT_REVENUE_GROWTH_RATE
```

`M_ENT_GROWTH_POTENTIAL` 本波无落表，**不进** `source_tables` 左端（避免假接通）。恢复项无 ID，不进。  
`ads.enterprise_score` / `ads.enterprise_diagnosis` **不进** 8 件套。

产出（待建）：`enterprise_cultivate_score.cultivate_score`。

来源系统：国内机构要素库（只经上游间接）。

## 现网探针（2026-08-28；不进 8 件套）

- `gkxlumenx_ads.enterprise_diagnosis`：120 行；列 = advantages/weaknesses/suggestions/diag_level；无 penalty。
- 无 `cultivate_score` 列。`ent_cultivate_candidate` 在 topic 库，不是落分。
- `enterprise_score.score_total` 120 行 mock，禁止当本条。

## 待建 / 缺口（本波只暴露，不结项）

1. `M_ENT_GROWTH_POTENTIAL` MODEL 未出数。
2. `recovery` 无合法上游（Q018 挡转分）。
3. 无独立目标表 `enterprise_cultivate_score`。
4. Q015 未升 🟢。
5. `growth` 多数企业该项空。
6. D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.7`；COMPUTE。禁止 ADS mock 假接通。禁止本波与 INDEX 合并。禁止痛点转分。

---
*2026-08-28 COVER-STAT-L01 二次分口径 + 缺口暴露；不强行结项*
