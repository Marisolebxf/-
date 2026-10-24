# 全国分布区域数（M_CHAIN_NATIONAL_REGION_COUNT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NATIONAL_REGION_COUNT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NATIONAL_REGION_COUNT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NATIONAL_REGION_COUNT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_NATIONAL_REGION_COUNT |
| 指标名称 | 全国分布区域数 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链概览「覆盖 N 个省级行政区」、区域分布地图的省域着色数、全国—深圳对比页的分母｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_NATIONAL_REGION_COUNT.md` |

## 口径定义

省级区域轴（`dwd_org_base_info.province`）与链—企桥结构都齐备，公式可执行、数字可复算；但链上 2,283,762 家企业里只有 **35,046 家（1.53%）** 能落到属地，其中 **35,022 家在广东（99.93%）**，省外仅 **24 家**，且海外主体与产业链编码挂接 **0 行**——「全国分布」这一关键依赖维在本库**没有样本**，故判**部分支持**。

## 计算逻辑说明

```text
COUNT(DISTINCT province) over chain members with non-empty province
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NATIONAL_REGION_COUNT.md` §二（M_CHAIN_NATIONAL_REGION_COUNT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_`
- `dwd_org_base_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：省级行政区轴与链—企桥结构齐全，公式可执行、数值可复算；但链上主体 97.7% 无属地、可落属地的 99.93% 在广东，省外仅 24 家，「全国分布」这一关键依赖维在本库无样本 → 按 §〇 判部分支持。不得把 24 家（或底册省外 339 家）冒充全国覆盖。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_NATIONAL_REGION_COUNT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NATIONAL_REGION_COUNT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_NATIONAL_REGION_COUNT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08-21: 初版（模拟王惠调研；省市粒度混写 + scope 伪条件 + 老表漂移）
- 2026-10-14: 0.2.0 口径钉死（省级默认、市级下钻不另开 ID；空值不计数；简称 ETL 归一；province 值域实核入 D2 注记）；补矩阵行 aligned/D3=none。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

