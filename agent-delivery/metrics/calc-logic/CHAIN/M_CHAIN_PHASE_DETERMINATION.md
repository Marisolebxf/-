# 产业链阶段判定（M_CHAIN_PHASE_DETERMINATION）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PHASE_DETERMINATION.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PHASE_DETERMINATION.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PHASE_DETERMINATION_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_PHASE_DETERMINATION |
| 指标名称 | 产业链阶段判定 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链概览阶段标签、链排序与筛选｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_PHASE_DETERMINATION.md` |

## 口径定义

12 条链都能被等频三分，但只有 8 条实测维度 ≥3；4 条链的阶段是空值机械落位，跨年 7 条翻转，只能判部分支持并把不可判定单列。

## 计算逻辑说明

```text
phase = 按 score 降序等频三分（前 1/3 成长、中 1/3 成熟、后 1/3 衰退）；n_dims_measured<3 → 不可判定
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PHASE_DETERMINATION.md` §二（M_CHAIN_PHASE_DETERMINATION.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_annual_financial_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 条链都有阶段分，等频三分可直接执行；但只有 8/12 条链实测维度 ≥3，低空经济/生物医药 4 维全空、分数恒 50，机械分段会把空值送进成熟期；跨年阶段翻转 7/12，其中人工智能 79.50→12.26、集成电路 71.38→32.85，阶段结论对统计年高度敏感；两套分段法（等频 vs 阈值）结果不一致。故判部分支持，并把不可判定链单独列出，不硬贴阶段。
- **基期声明**：主口径 2025、敏感性 2024。上游财务表虽覆盖 2013—2025，但 2025 年营收>0 仅 34 行、全表累计仅 2,191 行，更早年份样本更薄且企业集合逐年换人，故不把 2013—2023 当可比基期；这不是缺年补 0，而是明确不采用。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_PHASE_DETERMINATION.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PHASE_DETERMINATION.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_PHASE_DETERMINATION_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

