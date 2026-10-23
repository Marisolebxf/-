# 区域政策覆盖率（M_CHAIN_REG_POLICY_COVERAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_POLICY_COVERAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_POLICY_COVERAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_POLICY_COVERAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_POLICY_COVERAGE |
| 指标名称 | 区域政策覆盖率 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链区域对比、政策覆盖热力图｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_POLICY_COVERAGE.md` |

## 口径定义

48 个链×城格子全部可算，均值 17.18%、最高 58.33%；但只命中标题、政策库 2021 年后仅 2,410 行、二值口径 20/48 已饱和，只能判部分支持。

## 计算逻辑说明

```text
Cov(c,r)=Σ_i hit_i/(hit_i+5)/|L1(c)|×100%；池=city=r ∪ 国家级(level=4)；hit=标题词命中
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_POLICY_COVERAGE.md` §二（M_CHAIN_REG_POLICY_COVERAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：12 链 × 4 市 = 48 个格子全部可算，政策底表 20,000 行、链树 1,273 节点齐备；但命中只基于标题（theme 非零行 2），不是正文语义覆盖；覆盖率最高仅 58.33%、均值 17.18%，但二值口径已有 20/48 个格子 100%（链路只要命中 1 条就算覆盖）、16 个格子 0%，说明连续值主要拉开「命中几条」，而非「覆盖/不覆盖」；政策库 2021 年后仅 2410 行，按年截断会把广州池从 2,499 砍到 157，故只能用存量、无法做年度政策增量；城市只认中文全称精确匹配，9,706 行 city=NULL 只能靠 level=4 区分国家级。故判部分支持。
- **基期声明**：政策覆盖是**存量截面**（全表 20,000 行，最早 1981-04-07、最晚 2024-02-18)，不做年度序列，因此没有年度基期。按 2021+ 截断不是「补 0」，而是把存量表误当增量表，本件明确拒绝该做法，并在 sensitivity 里量化其后果。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_POLICY_COVERAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_POLICY_COVERAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_POLICY_COVERAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

