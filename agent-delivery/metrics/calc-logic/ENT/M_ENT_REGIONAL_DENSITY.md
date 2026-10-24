# 区域企业密度（M_ENT_REGIONAL_DENSITY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REGIONAL_DENSITY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGIONAL_DENSITY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGIONAL_DENSITY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_REGIONAL_DENSITY |
| 指标名称 | 区域企业密度 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业分析／区域分布／集聚效应 |
| 更新频率 | 日 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 区域密度图层（省/市/县）｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_REGIONAL_DENSITY.md` |

## 口径定义

分子齐（189,116 家、240 个格子）、分母无（0 个数值型面积列 / 0 张面积表 / 0 行宏观面积口径），按口径「area 空该区空」交付 0 行，判部分支持；另给一条「家/行政区」的降级读数，明确标注非交付值。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REGIONAL_DENSITY.md` §二（M_ENT_REGIONAL_DENSITY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_heis_info`
- `dwd_macro_index_data`
- `dwd_org_base_info`
- `dwd_substance`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：分子侧完全就绪（189,116 家企业可按省/市/县三级聚合），但分母「行政区土地面积」在 gkx 内不存在：information_schema 全库 15 个 area/面积 相关列全部是编码或名称，无数值型面积列；区划维表 dwd_dim_admin_area（20,000 行）也不含面积字段。按口径「area 空该区空」，交付 0 行；有分子、有层级、无分母，故判部分支持而非完全不支持。
- **基期声明**：截面件：分子取当前底册快照，分母（面积）不存在，故无年度序列与基期年份。面积一旦灌入，本件可直接按区划键出数，不需要改口径。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_REGIONAL_DENSITY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGIONAL_DENSITY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_REGIONAL_DENSITY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

