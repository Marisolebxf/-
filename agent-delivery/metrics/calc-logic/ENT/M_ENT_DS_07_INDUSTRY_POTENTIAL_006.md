# 产业发展潜力综合评估（M_ENT_DS_07_INDUSTRY_POTENTIAL_006）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_07_INDUSTRY_POTENTIAL_006.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_006.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_006_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_DS_07_INDUSTRY_POTENTIAL_006 |
| 指标名称 | 产业发展潜力综合评估 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 产业服务／产业评价／发展潜力 |
| 更新频率 | 建议年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链详情页「发展潜力」雷达图 + 12 链排名表｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2014] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_DS_07_INDUSTRY_POTENTIAL_006.md` |

## 口径定义

五维中四维有链级代理，等权合成后 12 条链排名可出（人工智能 0.8562 居首），但科学影响力无载体、权重非甲方值，判部分支持。

## 计算逻辑说明

```text
potential = mean(minmax(D1 专利密度), D2 K覆盖率, D3 营收样本, D5 专利总量)；D4 科学影响力缺失
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_07_INDUSTRY_POTENTIAL_006.md` §二（M_ENT_DS_07_INDUSTRY_POTENTIAL_006.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_org_shareholder_info`
- `dwd_org_stock_finance_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：eval_weight（用户权重表）不存在，但五维里有四维能找到链级代理且都是真数：专利密度、K 覆盖率、样本营收、专利总量，12 链齐全。等权替代权重后综合分与排名可直接产出，故不判完全不支持；科学影响力维无载体、产值只有样本、权重非甲方值，故判部分支持。
- **基期声明**：营收基准取 2014（有效企业最多的一年，752 家）；2015 年后样本逐年塌陷至 34 家，用末年会让 D3 变成小样本噪声，故不用末年、也不按 0 补齐中间年。专利窗口 2021—2024。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_DS_07_INDUSTRY_POTENTIAL_006.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_006.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_DS_07_INDUSTRY_POTENTIAL_006_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

