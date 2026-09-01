# 招引推荐评分（M_ENT_ATTRACT_SCORE）

> 口径真源：seed「demo 快路径」→ 2026-08-28 `ENT-SYNTH-METRIC-COVER-STAT-L01`。  
> **二次 COMPUTE**：挂上游分数加权，不从 ODS 现算。  
> **不强行结项**：口径留下，缺口摊开，当前无法执行。不与 `M_ENT_ATTRACTION_INDEX` 合并。Q015 仍 🟡。  
> 维护：data-agent · 8 件套摘要见 `cfg_metric-ENT-seed.yaml`。

## 元数据

- **指标ID**：`M_ENT_ATTRACT_SCORE`
- **指标名称**：招引推荐评分（demo路径）
- **一级模块**：企业分析
- **二级模块**：引育推荐
- **三级模块**：招引推荐
- **更新频率**：周
- **对齐状态**：二次分口径已写；上游未出数；无目标表
- **是否在数据库**：无 `attract_score` 列、无独立目标表；ADS `enterprise_score` 是另一套 mock，不是本条
- **是否在需求文档**：是（与 INDEX 并行，待 Q015）
- **是否在原型页面**：是
- **是否在原型代码**：是
- **关联Q编号**：Q015（权重/阈值待甲方；本条只用团队临时等权，不升 🟢）

## 口径定义

每个企业一条招引分，倒序可用于名单。

**目标**（团队临时默认 🟡，徐滕强；非甲方闭合）：

```
attract_score = (tech_proxy + growth + regional) / 3 − 0.2 × risk_score
```

三项假定 0–100 同刻度；扣完下限 0。

| 分项 | 挂什么 | 现状 |
|------|--------|------|
| `tech_proxy` | `M_ENT_TECH_POWER_SCORE` | MODEL，本波不算。DWD 算不出技术力。ADS `tech_power.tech_power_index` 是模型 mock，禁止当已接通 |
| `growth` | `M_ENT_REVENUE_GROWTH_RATE` | STAT 已定口径；ODS 相邻年营收几乎没几家。无值该企该项空 |
| `regional` | **无对应企业级指标** | 不能拿 INDEX 的「深圳连接度」、不能拿 `CITY_DENSITY`（市层）冒充 |
| 风险 | **无本波已过风险 STAT** | ADS `realdata_enterprise_risk.risk_score` 39 行 mock，禁止当已接通 |

与 `M_ENT_ATTRACTION_INDEX`（产业相关 / 政策匹配 / 深圳连接）**并行**，本波不合并。

**禁止**：

- 读 `ads.enterprise_score.score_total` / `score_innov` / `score_growth` 当本条分项（另一套 mock 综合分）
- 读 `tech_power.rank_overall`
- 硬编与 INDEX 混用的权重
- 把缺目标表说成唯一缺口
- 本波升 D3/D4、升 Q015、结 COVER 叶

无三类齐全输入：**该企无法计算**。技术代理整波算不出、区域项无上游 → **整条当前无法执行**。

## 落表

| 目标 | 粒度 | 写什么 | 现网 |
|------|------|--------|------|
| `enterprise_attract_score`（建议名） | `org_id` 一条 | `attract_score` | **缺口：无此表** |

正式 / demo DWD、ADS 均无此表，也无任何 `attract*` 列。  
**禁止**把 `enterprise_score` 当目标表。GDF 暂缓，本波不建 DDL。**是否建表、用何表名：待后续讨论**，此处只暴露缺口。

当前：结果无处可落，且算式也跑不完。

## 分场景 / 实现方案

### 场景 A · 单企

上游三分 + 风险都有值之后：按公式写目标表该 `org_id`。缺任一项：该企不写分（空），不是用 mock 凑。

### 场景 B · 招引名单

读目标表 `ORDER BY attract_score DESC`。无表 / 无数：名单空。禁止扫 ADS mock 排序冒充。

### demo / 生产

两边都算不出。demo `enterprise_score` 100 行、正式 120 行，全是 mock，**不是**实现捷径。  
生产：先等技术力 MODEL 出数、增长率落表、区域项定指标、风险 STAT 过线，再周任务写入目标表。禁止请求路径现算 MODEL。

对应 seed `formula`：等权二次分 + **当前无法执行**（上游 + 区域/风险缺口 + 无目标表）。

**计算公式文件**：`M_ENT_ATTRACT_SCORE.md`

## 源表字段

8 件套 `source_tables`（二次，右端 `metric:`，不写 ODS）：

```
tech_power <- metric: M_ENT_TECH_POWER_SCORE
enterprise_finance_history <- metric: M_ENT_REVENUE_GROWTH_RATE
```

区域项、风险项 **无上游 ID**，不进 `source_tables`，缺口见上表。  
`ads.enterprise_score` / `ads.realdata_enterprise_risk` **不进** 8 件套。

产出（不进 `source_tables`）：`enterprise_attract_score.attract_score`（待建）。

来源系统：国内机构要素库（只经上游指标间接；本条无直接 ODS）。

## 现网探针（2026-08-28；不进 8 件套）

- `gkxlumenx_ads.enterprise_score`：120 行，`score_innov/operate/growth/total` 全满；无 `tech_proxy` / `regional` / `attract_score`。
- demo 同表 100 行。
- `realdata_enterprise_risk`：39 行，`risk_score` 全满 mock。
- 无 `enterprise_attract_score` / `attract*` 列。
- 技术力：项目 DWD 无分；ADS `tech_power` 有 `tech_power_index` mock（本波不读当源）。

## 待建 / 缺口（本波只暴露，不结项）

1. `M_ENT_TECH_POWER_SCORE` MODEL 未出数。
2. `regional` 无企业级指标。
3. 风险无本波已过 STAT。
4. 无独立目标表 `enterprise_attract_score`。
5. Q015 权重/阈值待甲方；此处仅团队临时 1/3 与 `0.2×risk`。
6. `growth` 多数企业无相邻年 → 该项空（即使整条将来能跑，这些企仍算不出）。
7. D3 / D4 本波不升。

## 备注

bid `§1.1.1.2.4.2.3.6`；COMPUTE。禁止 `gkx.dwd_*` 进 `source_tables`。禁止 ADS mock 假接通。禁止本波与 INDEX 合并。

---
*2026-08-28 COVER-STAT-L01 二次分口径 + 缺口暴露；不强行结项*
