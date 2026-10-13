# 城市对比指标值（M_SVC_SZ_COMPARE_METRIC）

## 基本信息

- 指标ID: M_SVC_SZ_COMPARE_METRIC
- 指标名称: 城市对比指标值
- 一级模块: 产业服务链分析
- 二级模块: 服务链分析
- 三级模块: 深圳对比
- 更新频率: 日（仅可 live 格随圈定；其余格不适用）
- 对齐状态判定: 部分闭合（0.2.0）
- 是否在数据库: 部分（仅深圳机构数可跟第 11 条同数；无外市/技术力/密度真灌）
- 关联Q编号: Q-SVCCHAIN-04（外市基准）+ Q-SVCCHAIN-01（技术力）+ Q-SVCCHAIN-03 / SVC-P1-1（网络密度边）

## 口径定义

生态页「深圳现状对比」的 **城市 × 小项** 多格取值面板，**不是**单一数字结果。

| 小项 | key | 真实情况 |
|---|---|---|
| 服务机构数量 | `orgCount` | **仅深圳可 live**；外市/全国平均不灌 |
| 平均技术力得分 | `avgTechScore` | **拿不到真数**（MODEL 未签） |
| 服务网络密度 | `networkDensity` | **拿不到真数**（无服务边） |

完整度另见 `M_SVC_SZ_CHAIN_COMPLETENESS`（已挂起，不在本三小项内）。

### 人口口径：服务机构，不是全量机构

对比柱上的「机构数」= **服务机构圈定池**（`svc_org_circle`），不是 `dwd_org_base_info` 全量工商。  
禁止：深圳用服务圈定、北上用全量工商横比（口径不一致）。

### 各格真实情况

#### 1) 深圳 × 服务机构数 —— 可闭合

与第 11 条 `M_SVC_PT_SZ_TOTAL` **同规则、同数**（圈定池 ∩ city=深圳）。  
数随圈定批次变，**不写死**历史快照 1355；前端旧 fixture 1240 **禁止**当 live。

#### 2) 外市 / 全国平均 × 机构数 —— 不灌

| 依据层 | 说明 |
|---|---|
| 样本事实 | Demo ODS / 圈定严重偏广东；同口径北上服务机构几乎为空（不是 SQL 不能 `GROUP BY city`） |
| 业务口径 | 城市基准数据源须甲方指定（`Q-SVCCHAIN-04`） |

「任意地区 COUNT」是查询能力，不是已闭合的城市对标口径。

#### 3) 平均技术力 —— 不进本 STAT 叶

归 MODEL `M_SVC_ORG_TECH_SCORE`；算法定义卡未签（`Q-SVCCHAIN-01` / 唐绍祖）。页面继续演示分 + 🧪⚠️。

#### 4) 网络密度 —— 不进本 STAT 叶（无边源）

归 GRAPH `M_SVC_GRAPH_DENSITY`。密度依赖「服务机构 A ——关系—— 服务机构 B」边。  
入站 **无** 服务机构↔服务机构合作/参与边（`SVC-P1-1`）；投资/股东边**不算**服务关系。没有边就没有服务关系网，密度算不出。口径另见 `Q-SVCCHAIN-03`。

## 计算公式

```text
可执行（仅一格）：
  深圳 orgCount = 与 M_SVC_PT_SZ_TOTAL 同一 COUNT（svc_org_circle + 主表 city=深圳）

禁止灌 ADS：
  北上广 / 全国平均 × orgCount
  任一城市 × avgTechScore
  任一城市 × networkDensity

禁止：
  用全量工商按城 COUNT 冒充服务机构对比
  把 CITY_METRIC_VALUES fixture 验收成 live
```

若 ADS 必须落本 ID：同一批最多允许 **深圳 × orgCount** 一行，且数值必须等于当期 `M_SVC_PT_SZ_TOTAL`。

## 源库表字段

```
svc_org_circle + dwd_org_base_info(city) — 仅深圳×机构数，同 M_SVC_PT_SZ_TOTAL
（缺口）外市服务机构可比池 / 城市基准源 <- Q-SVCCHAIN-04
（缺口）城市平均技术力 <- metric: M_SVC_ORG_TECH_SCORE（Q-SVCCHAIN-01 未签）
（缺口）服务机构↔服务机构边 <- ods: 待供方交付（SVC-P1-1）→ 网络密度
```

## 参考文献 / 依据

`SVC-ALGO-STAT-21-L01` 序号 21；`Q-SVCCHAIN-04` / `01` / `03`；`SVC-P1-1`；demo `CITY_METRIC_VALUES` / `ShenzhenCompareView.tsx`；2026-10-13 human:徐滕强 确认部分闭合与真实缺口。

## 更新记录

- 2026-08-21: 初版，模拟王惠调研产出
- 2026-08-28: 侯佳伟 1B2A3A（仅深圳机构数可跟第 11 条）
- 2026-10-13: 0.2.0 写入真实情况：多格面板、服务机构口径、外市样本+Q-04、技术力/无边源密度；不写死 1355
