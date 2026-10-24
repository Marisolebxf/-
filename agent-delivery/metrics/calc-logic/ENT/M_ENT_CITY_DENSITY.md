# 城市企业密度（M_ENT_CITY_DENSITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_DENSITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_DENSITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_DENSITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CITY_DENSITY |
| 指标名称 | 城市企业密度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析 |
| 更新频率 | 年度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CITY_DENSITY.md` |

## 口径定义

分子齐全（66 城 / 189,115 行，深圳 95,600 家），分母在 gkx 完全不存在（面积类数值列 0 命中、区划字典 29 列无面积列），密度值一律不出，判部分支持。

## 计算逻辑说明

```text
density_c = N_c / A_c * 100，单位 家/百km²；A_c 为城市行政区划土地面积（km²）
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_DENSITY.md` §二（M_ENT_CITY_DENSITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_dim_index_attribute`
- `dwd_macro_index_data`
- `dwd_org_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：分子侧完全可得（66 个城市、189,115 行可绑定城市码，深圳 95,600 家），分母侧在 gkx 无任何 km² 数值载体：面积类数值列扫描 0 命中，`area` 5 列全是 varchar 行政区名，区划字典 29 列无面积列；人口密度指标 a77361 仅 30 行 / 14 个国家代码 / 止于 2021 年，不能反解城市面积。密度 = 分子/分母，分母恒缺即指标不可完整构建，故判部分支持（分子可交付、密度不可交付）。
- **基期声明**：截面指标：分子为当前主档全量计数；分母缺，无年度序列可谈。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_DENSITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_DENSITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_DENSITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

