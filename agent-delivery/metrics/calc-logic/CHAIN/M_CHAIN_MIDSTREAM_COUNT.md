# 中游环节数（M_CHAIN_MIDSTREAM_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_MIDSTREAM_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MIDSTREAM_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MIDSTREAM_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_MIDSTREAM_COUNT |
| 指标名称 | 中游环节数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链全景／链条结构 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链图谱「中游」段着色计数、链详情页结构卡片 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_MIDSTREAM_COUNT.md` |

## 口径定义

每条产业链的 9 位 L1 分支中，去掉编码最小（首段）与编码最大（末段）两支后剩余的 L1 子树；统计其全部节点（含 L1 自身，容器与叶子各计 1），12 条链求和。编码序位是代理，不等于官方 chain_stage='midstream'。

> 一句话口径（源件 §0.3）：中游是「三段里最难定义的一段」：上游可靠首段界定、下游可靠末段界定，中游只能取「剩下的」。源表无 `chain_stage`、`level` 恒 0，本件用「中间 L1 分支」代理，得到 493；这个值在结构上完全可复算，但 17 个中间分支里有 4 个的语义与编码位置不一致，其中 3 个是明确反例，故判 **部分支持**。

## 计算逻辑说明

```text
Mid = Σ_k |∪_{c∈M_k} subtree(c)|，M_k = L1_k − {min L1_k, max L1_k}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_MIDSTREAM_COUNT.md` §二（M_CHAIN_MIDSTREAM_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：中游是「三段里最难定义的一段」：上游可靠首段界定、下游可靠末段界定，中游只能取「剩下的」。源表无 `chain_stage`、`level` 恒 0，本件用「中间 L1 分支」代理，得到 493；这个值在结构上完全可复算，但 17 个中间分支里有 4 个的语义与编码位置不一致，其中 3 个是明确反例，故判 **部分支持**。
- **基期声明**：截面指标：链树为静态维表，无版本列、无年度分区，不涉及年份分母，故 used/missing 均为空。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_MIDSTREAM_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MIDSTREAM_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_MIDSTREAM_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

