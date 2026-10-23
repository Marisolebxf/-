# 区域覆盖数（M_ENT_REGION_COVERAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REGION_COVERAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGION_COVERAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGION_COVERAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_REGION_COVERAGE |
| 指标名称 | 区域覆盖数 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／企业总览／区域分布 |
| 更新频率 | 日 |
| 数据支持度（四档） | **完全直接支持** |
| UI 挂载 | 区域分布卡（省/市/县三级下钻）｜ **数据支持度**：**完全直接支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_REGION_COVERAGE.md` |

## 口径定义

去重计数直接可算：29 个省级、65 个市级、146 个县级覆盖格，`province`/`city` 填充率 99.9995%，判完全直接支持；唯一限定是底册偏粤（广东 99.82%），读数只能表述为「名录触达面」。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REGION_COVERAGE.md` §二（M_ENT_REGION_COVERAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_org_base_info`

## 待建表字段

无（直接支持：现有结果面直读）。

## 数据支持度与缺口

- **判档**：完全直接支持
- **判档理由**：calc-logic 的源表字段就是 gkx.dwd_org_base_info(org_id, province, city)，去重计数即定义本身，无需换算、无需补维：实测 189,116 行底册可得 29 个省级、65 个市级、146 个县级覆盖格，province/city 非空率 99.9995%。
- **基期声明**：截面件：口径是「当前底册覆盖多少个行政区域」，不含年度序列，故无基期年份。若要做跨年覆盖变化，需按底册快照日期留档（民政部每年调整区划代码，跨期比须先对齐版本）。
- **复现实测耗时**：约 134.72 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REGION_COVERAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGION_COVERAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGION_COVERAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

