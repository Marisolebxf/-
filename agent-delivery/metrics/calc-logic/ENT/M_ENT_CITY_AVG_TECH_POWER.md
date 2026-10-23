# 城市平均技术力（M_ENT_CITY_AVG_TECH_POWER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_AVG_TECH_POWER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_AVG_TECH_POWER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_AVG_TECH_POWER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_CITY_AVG_TECH_POWER |
| 指标名称 | 城市平均技术力 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 区域分析／城市对比／技术力 |
| 更新频率 | 随上游 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 城市对比页「平均技术力」卡、区域技术力地图｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_CITY_AVG_TECH_POWER.md` |

## 口径定义

四市有专利企业的专利三维分均值：惠州 0.1079、东莞 0.1064、广州 0.1、深圳 0.0987，但无专利企业不入分母，且样本 <100 的城市被剔除，判部分支持。

## 计算逻辑说明

```text
city_avg = AVG(0.5*专利规模 + 0.3*IPC4广度 + 0.2*新鲜度) OVER 该市有专利企业
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_AVG_TECH_POWER.md` §二（M_ENT_CITY_AVG_TECH_POWER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：tech_power 结果面不存在，但城市平均量可由企业级专利三维分聚合得到：专利计数、IPC4 广度、2024 申请量都在 dwd_patent 里，企业城市在 dwd_org_base_info 里，聚合链完整。缺的是技术力的另外三维（人才/转化/投入）与「全部企业」分母口径，故判部分支持。
- **基期声明**：专利表只有 2021—2026（2017—2020 零行），D1 分母为全期申请，D3 用 2024 年占比；2025/2026 残年不入分子。本件是截面均值，不做年度序列，故不列逐年基期。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_CITY_AVG_TECH_POWER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_AVG_TECH_POWER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_CITY_AVG_TECH_POWER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

