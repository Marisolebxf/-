# 企业技术力评分（M_ENT_TECH_POWER_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-ENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TECH_POWER_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_POWER_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_POWER_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_ENT_TECH_POWER_SCORE |
| 指标名称 | 企业技术力评分 |
| 所属域 | ENT（企业分析） |
| 一级模块 | 企业服务／企业评价／技术力 |
| 更新频率 | 建议半年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 企业画像「技术力」卡、技术型企业榜、招商技术尽调参考｜ **数据支持度**：**部分支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/ENT/M_ENT_TECH_POWER_SCORE.md` |

## 口径定义

专利三维（规模 0.5 / 广度 0.3 / 新鲜度 0.2）在 134,152 家有专利企业上出分，中位 0.0911、最高 0.7867，但人才与研发投入两维缺失，判部分支持。

## 计算逻辑说明

```text
score = 0.5*minmax(log1p(专利数)) + 0.3*minmax(IPC4广度) + 0.2*minmax(2024申请占比)
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TECH_POWER_SCORE.md` §二（M_ENT_TECH_POWER_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：两张结果面（tech_power、enterprise_score）都不存在，旧稿六维里只有专利侧三维能从 dwd_patent 逐企业算出，人才/转化/投入三维在 gkx 没有任何企业级表可挂。专利三维本身结构与量都够（134,152 家企业有专利），可产出完整分布与排名；缺三维意味着分值是「专利技术力」而不是「技术力」，故判部分支持而不是完全转换支持。
- **基期声明**：专利表只有 2021—2026（2017—2020 零行），D1 分母是全期申请，D3 用 2024 年申请占比；2025/2026 为残年不入分子。人才/转化维不涉及年份，因整维缺失而不存在基期。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_ENT_TECH_POWER_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_POWER_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_ENT_TECH_POWER_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

