# 产业周期阶段（M_CHAIN_CYCLE_STAGE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_CYCLE_STAGE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CYCLE_STAGE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CYCLE_STAGE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_CYCLE_STAGE |
| 指标名称 | 产业周期阶段 |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链总览／周期研判 |
| 更新频率 | 建议季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「周期阶段」标签、产业链目录的阶段徽标、周期对比看板｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2018, 2019, 2020, 2022, 2023, 2024] |
| 缺失年份 | [2021] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_CYCLE_STAGE.md` |

## 口径定义

融资热度三年窗口对比 + 成立年份结构两条腿，12 条链全部出阶段（成长期 2、成熟期 2、衰退期 8），但「衰退」只等于资本退潮，产出侧无口径可用，故判部分支持。

## 计算逻辑说明

```text
融资热度腿：post(2022-2024)/pre(2018-2020)-1 >=+10% 成长、-10%~+10% 成熟、<=-10% 衰退；new_share>=25% 且热度>=0 覆盖为孕育
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_CYCLE_STAGE.md` §二（M_CHAIN_CYCLE_STAGE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_org_financing_info`
- `dwd_org_industry_tags`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：chain_stage 结果面不存在，三条候选腿里营收腿被数据证据否决（样本从 198 家塌到 11 家），但融资腿与年龄结构腿成立：25,654 条融资事件中 14,626 条可挂链，12 链各有 175—5,024 条事件，跨窗口样本均 >=50 的有 11 链。阶段标签可由「资本热度方向 + 年龄结构」规则映射得到，不需要外部参数表与结果面，故判部分支持；但热度≠产出，且 8 链落在衰退期的结论主要由 2022—2024 融资退潮驱动，只能作方向性判断。
- **基期声明**：主判腿用两个三年窗口（2018—2020 与 2022—2024）对比，2021 为疫情异常年，主动留空不入窗口，不是缺年补 0；年龄腿用截至 2024 的成立年份分布。融资事件在 2025—2026 大幅减少（919/618→238），为未完整年度，不入窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_CYCLE_STAGE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CYCLE_STAGE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_CYCLE_STAGE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

