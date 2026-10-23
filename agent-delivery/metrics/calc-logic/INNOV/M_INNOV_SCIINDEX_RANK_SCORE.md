# 科技成果综合得分与名次（M_INNOV_SCIINDEX_RANK_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCIINDEX_RANK_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_RANK_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_RANK_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_SCIINDEX_RANK_SCORE |
| 指标名称 | 科技成果综合得分与名次 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统／科技发展态势／科技创新评估 |
| 更新频率 | 年 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 成果综合榜、机构对比卡 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_SCIINDEX_RANK_SCORE.md` |

## 口径定义

gkx 能排出一张**机构级**综合榜：2023 年池内 **649 家**，中国科学院以 **92.90** 分居首、领先第二名中山大学 **9.68** 分；但正本要排的是「科技成果条目」，且分值应由智库后台按待签权重合成——本件这两条都不满足，只能算替代读数。

## 计算逻辑说明

```text
score = 100·(0.5·log1p(papers)/log1p(max_papers) + 0.5·log1p(patents)/log1p(max_patents))
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCIINDEX_RANK_SCORE.md` §二（M_INNOV_SCIINDEX_RANK_SCORE.py 零改语义复算）。

## 源表字段

源件未点名任何 dwd_/ads_/ods_ 物理表（纯派生/合成件，输入为兄弟件产物或快照）；依赖清单见源件 §〇/§三。

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：gkx 能排出一张**机构级**综合榜：2023 年池内 **649 家**，中国科学院以 **92.90** 分居首、领先第二名中山大学 **9.68** 分；但正本要排的是「科技成果条目」，且分值应由智库后台按待签权重合成——本件这两条都不满足，只能算替代读数。
- **基期声明**：专利表 2017—2020 零行；2024 论文断点、2025—2026 申请人分年缺失，均不按 0 摊入。入池要求两源同年都有量，故池子天然限制在 2021—2023。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_SCIINDEX_RANK_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_RANK_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_SCIINDEX_RANK_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

