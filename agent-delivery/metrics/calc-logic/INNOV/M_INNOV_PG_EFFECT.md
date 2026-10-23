# 政策效果（M_INNOV_PG_EFFECT）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_EFFECT.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_EFFECT.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_EFFECT_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_EFFECT |
| 指标名称 | 政策效果 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 政策与条件保障力 → 政策效果评估 → 政策实施前后产出变化（专利 / 论文 / 项目） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024, 2025, 2026] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PG_EFFECT.md` |

## 口径定义

没有「政策效果」现成结果面，故非完全直接支持；论文（6,000 条/年）与项目（4,000 条/年）两个序列够长、可算前后窗增幅，故非完全不支持；但专利面板 `apdt_year` 只有 2021—2026、基线年 2016—2020 在库内**零行**，且政策表与产出表之间**没有任何企业级关联键**，因果识别所需的对照与 treatment 全部不可得，故判**部分支持**。

## 计算逻辑说明

```text
growth = (mean(T-2..T) − mean(T-7..T-3)) / max(base,1)；专利维不可算，论文/项目维按窗口敏感性披露
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_EFFECT.md` §二（M_INNOV_PG_EFFECT.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：没有「政策效果」现成结果面，故非完全直接支持；论文（6,000 条/年）与项目（4,000 条/年）两个序列够长、可算前后窗增幅，故非完全不支持；但专利面板 `apdt_year` 只有 2021—2026、基线年 2016—2020 在库内**零行**，且政策表与产出表之间**没有任何企业级关联键**，因果识别所需的对照与 treatment 全部不可得，故判**部分支持**。
- **基期声明**：由产物中实际出现的年度键反推：used=[2021, 2022, 2023, 2024, 2025, 2026]；未见其他年度，缺失年未按 0 摊入。此项为机械反推，需人工确认取数窗口。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_EFFECT.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_EFFECT.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_EFFECT_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

