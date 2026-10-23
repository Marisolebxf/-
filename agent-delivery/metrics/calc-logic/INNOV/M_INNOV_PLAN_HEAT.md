# 热度指数（M_INNOV_PLAN_HEAT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_HEAT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_HEAT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_HEAT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_HEAT |
| 指标名称 | 热度指数 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技发展规划页「全球热点技术捕捉」——热点技术列表及热度分级 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2023, 2024] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PLAN_HEAT.md` |

## 口径定义

无「热度指数」现成结果表 → 非完全直接支持；专利维结构完整、2024 年数据足量，论文/项目维可算但方向归属依赖 Top-1 22.14% 的术语桥，且论文为单日回填、项目 2022 起停录 → 三维可算但第三维不可独立验证，判**部分支持**。

## 计算逻辑说明

```text
{'heat': 'Heat_i = mean_{s∈可得维} pct_s(x_{i,s})，pct=100*(rank-1)/(n-1)，n=258', 'reference_years': {'patent': 2024, 'paper': 2023, 'project': 2021}, 'normalization': '源内百分位（抗三源量纲差三个数量级）'}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_HEAT.md` §二（M_INNOV_PLAN_HEAT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维结构齐全、258 个方向均出分，但三源无法取同一年（专利 2024 / 论文 2023 / 项目 2021），论文维单日批量入库、项目维 2022 起停录，且论文/项目方向归属依赖 Top-1 22.14% 的术语桥；「全球监测」所需国际语料不具备
- **基期声明**：热度是横截面指标，分母为「258 个面板方向内的排名」，不涉及时序分母；三个参考年各自取该源最后一个完整年，异年拼接已在正文披露。
- **复现实测耗时**：约 20.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_HEAT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_HEAT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_HEAT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

