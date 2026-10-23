# 发展方向预警（M_INNOV_PLAN_DIRECTION_ALERT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_DIRECTION_ALERT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_DIRECTION_ALERT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_DIRECTION_ALERT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PLAN_DIRECTION_ALERT |
| 指标名称 | 发展方向预警 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技发展规划页「全球热点技术捕捉」——潜在科技发展方向预警列表 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2019, 2020, 2021, 2022] |
| 缺失年份 | [2016, 2017, 2018] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PLAN_DIRECTION_ALERT.md` |

## 口径定义

无「预警结果」现成表 → 非完全直接支持；六源中专利/论文/产业三源可算，项目与政策因停录只能前移窗口，人才源因两套 ID 宇宙不互通而不可得 → 预警只能覆盖部分源，判**部分支持**。

## 计算逻辑说明

```text
{'wanghui': 'F=mean(g_s)；g_s=(近窗年均值-基期年均值)/max(基期年均值,1)；level=2 if F>=1 且两源g>0, 1 if F>=0.5, else 0', 'windows': {'patent': {'base': [2021, 2022], 'recent': [2023, 2024]}, 'paper': {'base': [2021, 2022], 'recent': [2023, 2024]}, 'project': {'base': [2019, 2020], 'recent': [2022, 2023]}, 'industry': {'base': [2021, 2022], 'recent': [2023, 2024]}, 'policy': {'base': [2019, 2020], 'recent': [2021, 2022]}}, 'weights_assumed': 'A 套五源等权（王惠未给权重）；B 套两源等权'}
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_DIRECTION_ALERT.md` §二（M_INNOV_PLAN_DIRECTION_ALERT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`
- `dwd_scholar_`
- `dwd_scholar_paper_relation`
- `dwd_scholar_research_direction`
- `dwd_talent_base`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：六源中仅专利与产业可用且同出 dwd_patent（不独立）；论文单日回填、项目与政策 2022 起停录、人才无映射。A 套字面执行可跑但 F 的方差被论文维垄断，B 套收缩为两源后仍只能算「原型」
- **基期声明**：各源窗口不同，基线年按源显式列出；专利/论文/产业基线为 2021—2022（2016—2020 在 dwd_patent 无行），项目/政策因停录前移至 2019—2020。缺失年不得按 0 摊入分母。
- **复现实测耗时**：约 21.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PLAN_DIRECTION_ALERT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_DIRECTION_ALERT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PLAN_DIRECTION_ALERT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

