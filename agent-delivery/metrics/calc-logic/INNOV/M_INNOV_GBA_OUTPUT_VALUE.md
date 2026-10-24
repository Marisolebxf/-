# 创新产值（M_INNOV_GBA_OUTPUT_VALUE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_OUTPUT_VALUE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_OUTPUT_VALUE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_OUTPUT_VALUE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_OUTPUT_VALUE |
| 指标名称 | 创新产值 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 粤港澳大湾区创新指标数据 GIS（指标勾选）｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_OUTPUT_VALUE.md` |

## 口径定义

「创新产值」要求的是**区域高技术产业增加值**，属于国民经济核算产出：gkx 280 表清单中，9 张产值/增加值/GDP/技术合同候选表全部缺席（实测 0/9 命中）；唯一沾边的企业财报是微观营业收入，只覆盖 3,302 家法人（底册 1.75%），且口径不可换算为增加值 → **完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_OUTPUT_VALUE.md` §二（M_INNOV_GBA_OUTPUT_VALUE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_project_output`
- `dwd_gdp`
- `dwd_high_tech_output`
- `dwd_industrial_output`
- `dwd_industry_added_value`
- `dwd_org_annual_financial_info`
- `dwd_org_base_info`
- `dwd_org_income_statement`
- `dwd_org_output_value`
- `dwd_output`
- `dwd_output_value`
- `dwd_region_economy`
- `dwd_region_output_value`
- `dwd_tech_contract`
- `dwd_zh_project_output`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：「创新产值」要求的是**区域高技术产业增加值**，属于国民经济核算产出：gkx 280 表清单中，9 张产值/增加值/GDP/技术合同候选表全部缺席（实测 0/9 命中）；唯一沾边的企业财报是微观营业收入，只覆盖 3,302 家法人（底册 1.75%），且口径不可换算为增加值 → **完全不支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 12.8 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_OUTPUT_VALUE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_OUTPUT_VALUE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_OUTPUT_VALUE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

