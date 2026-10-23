# 产业链环节覆盖（M_ENT_CHAIN_STAGE_COVERAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CHAIN_STAGE_COVERAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_STAGE_COVERAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_STAGE_COVERAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CHAIN_STAGE_COVERAGE |
| 指标名称 | 产业链环节覆盖 |
| 所属域 | ENT（企业分析） |
| 一级模块 | ENT（企业分析） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业分析 → 产业链定位 / 产业链分析 → 环节覆盖 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CHAIN_STAGE_COVERAGE.md` |

## 口径定义

{'unit': '% / 个环节', 'formula_catalog': 'k_K = |被企业驻扎的目录叶子 ∩ 链目录叶子| / |链目录叶子|', 'formula_breadth': 'breadth = Σ叶子关联数 / 企业数', 'stage_grouping': '原式按 level 上/中/下游；当前不可执行，仅给码深代理'}

> 一句话口径（源件 §0.3）：企业侧数据充足：`gkx.dwd_org_industry_tags` 2,283,762 行、标签体系 6,628 个环节码；目录侧 `gkx.dwd_industry_chain_info` 1,273 节点、954 叶子。但王惠原式要求的「按 `level` 分组（上游/中游/下游）」**不可执行**——`level` 全库 1,273/1,273 行为 0，无任何命名段位行；且 24.93% 的标签行 `industry_link_code` 为空、5,674 个环节码不在目录内。段位维整块缺失，故判**部分支持**。本档位与 `code/M_ENT_CHAIN_STAGE_COVERAGE_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CHAIN_STAGE_COVERAGE.md` §二（M_ENT_CHAIN_STAGE_COVERAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_industry_chain_info`
- `dwd_org_base_info`
- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：目录侧 954 个叶子节点、1273 个节点可用于覆盖率，企业侧 2,283,762 行标签中 569,303 行（24.93%）`industry_link_code` 为空、无法定位环节，可算行 201,604（四城）。但王惠原式要求的『上游/中游/下游』段位字段 `level` 全为 0、命名行 0 条，段位维整块缺失；另发现标签体系使用 5,674 个目录外环节码，目录（1,273 节点）只是企业实际使用分类的一小部分，k/K 只能读作『目录口径覆盖率』，不能读作『真实产业链覆盖率』。故判部分支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.1 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CHAIN_STAGE_COVERAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_STAGE_COVERAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CHAIN_STAGE_COVERAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

