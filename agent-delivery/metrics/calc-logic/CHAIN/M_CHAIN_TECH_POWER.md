# 技术能力（链技术力）（M_CHAIN_TECH_POWER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TECH_POWER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_POWER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_POWER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_TECH_POWER |
| 指标名称 | 技术能力（链技术力） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | 产业链分析／产业链总览／技术实力 |
| 更新频率 | 建议季度 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 链全景页「技术实力」评分卡、链条横向对比雷达｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_TECH_POWER.md` |

## 口径定义

专利规模与新鲜度两维可用（链内专利 973,769 件），壁垒维只有深圳 K 覆盖，12 链等权合成后人工智能 0.598 居首，但第三维语义已偏，判部分支持。

## 计算逻辑说明

```text
tech_power = (D1专利规模 + D2断链壁垒 + D3近一年申请占比) / 3，各维 min-max 归一
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TECH_POWER.md` §二（M_CHAIN_TECH_POWER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_industry_tags`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：tech_power 结果面不存在，但三维里有二维半可用：专利规模与近一年申请占比都能从 dwd_patent 的 2,939,895 行按申请人名聚合出来（12 链合计专利见 totals），断链壁垒可以用 K 节点未覆盖率算，但只有深圳口径。权重是等权默认值、甲方未裁定。结构与数据都够跑，缺的是全国 K 覆盖与官方权重，判部分支持。
- **基期声明**：专利表 apdt_year 只有 2021—2026，2017—2020 零行（DATA_FACTS 陷阱 3.13），所以「近一年占比」的分母是 2021—2024 全期申请，不是十年存量；2025/2026 为不完整年，不进分母。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_TECH_POWER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_POWER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_TECH_POWER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

