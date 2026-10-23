# 湾区创新产值占比（M_INNOV_GBA_INNOV_RATIO）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_INNOV_RATIO.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INNOV_RATIO.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INNOV_RATIO_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_INNOV_RATIO |
| 指标名称 | 湾区创新产值占比 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新监测／湾区创新 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 湾区创新总览页「创新产出强度」条形图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| 缺失年份 | [2021, 2022, 2023, 2024, 2025] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_INNOV_RATIO.md` |

## 口径定义

比值类指标最怕的不是「两边都没有」，而是「一边有、一边没有」——因为后者会诱使人拿替代量硬除。本件正属后者：分母（地区生产总值）在 `dwd_macro_index_data` 里有表、有 1,136 行、覆盖 159 个地区码；分子（创新产值/高技术产业增加值）在城市×年份层面**一条序列都没有**。分母有、分子无，比值就无从定义——不是「精度低」，是**被除数为空**。故按 §0.1 判**完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_INNOV_RATIO.md` §二（M_INNOV_GBA_INNOV_RATIO.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_dim_admin_area`
- `dwd_dim_index_attribute`
- `dwd_high_tech_industry_bonds`
- `dwd_high_tech_output`
- `dwd_industry_added_value`
- `dwd_macro_index_data`
- `dwd_org_stock_finance_info`
- `dwd_output_value`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：分子（创新产值）在城市×年份层面没有任何可用序列：字典 867 条里 139 条创新类指标只有名字没有数据，25 条有数据的最大覆盖 1 个城市；分母（GDP）虽有表，但 9 城年度绝对值合计只有 25 个城年点、单年最多 2 城，2023 与 2025 两年为空。分子分母的年度交集只有 6 个点，全部是深圳 2021 年的「子行业新产品销售收入/R&D 经费」，不是增加值也不是产值，且多子行业不可加总——凑不出 11 城 × 5 年 = 55 个城年对里的任何一个正确口径点。唯一有城市广度的替代路径（规上工业增加值/GDP）只能凑出个位数城年对，其中一半比值 >100%（工业增加值大于 GDP），说明分母本身也存在口径冲突。结构与数据两端都不具备可算闭环，判完全不支持。
- **基期声明**：没有任何一年能形成同城同年的分子分母对，故 used 为空。缺的五年不是「按 0 摊入」，而是分子无源、分母单年最多 2 城——不补 0、不做插值、不外推。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_INNOV_RATIO.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INNOV_RATIO.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_INNOV_RATIO_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

