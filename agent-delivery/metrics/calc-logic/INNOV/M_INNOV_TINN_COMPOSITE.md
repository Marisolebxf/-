# 技术创新力综合评估（M_INNOV_TINN_COMPOSITE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_COMPOSITE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_COMPOSITE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_COMPOSITE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_TINN_COMPOSITE |
| 指标名称 | 技术创新力综合评估 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 技术创新力指标展示页「技术创新力综合评估」卡片（雷达 + 排名 + 自定义权重面板） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | [2021, 2022, 2023, 2024] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_TINN_COMPOSITE.md` |

## 口径定义

三维 12 个子项里，只有「申请量」这半个子项全量可算：全量面板 2,939,895 行、IPC4 × 年 2,456 格、窗口标注率 82.87%，633 个领域四年合计 12.4 万件到 148,698 件不等。授权量只有全域 2,140,420（72.81%），质量维的 5 个子项与市场维的 5 个子项**全部无法按 IPC4 归属**（见同批 `M_INNOV_TINN_PATENT_QUALITY` 与 `M_INNOV_TINN_MARKET` 的「完全不支持」结论）。按 calc-logic 的「缺测维不补 0、剩余维权重重归一」，规模维权重落到 1.0，产物字段名为 `size_only_score`——**它是规模维的降级交付，不是综合分**。有维度可算、有维度不可算，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_COMPOSITE.md` §二（M_INNOV_TINN_COMPOSITE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_market`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_patent_claim`
- `dwd_patent_family`
- `dwd_patent_legal`
- `dwd_patent_transfer`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三维 12 个子项里，只有「申请量」这半个子项全量可算：全量面板 2,939,895 行、IPC4 × 年 2,456 格、窗口标注率 82.87%，633 个领域四年合计 12.4 万件到 148,698 件不等。授权量只有全域 2,140,420（72.81%），质量维的 5 个子项与市场维的 5 个子项**全部无法按 IPC4 归属**（见同批 `M_INNOV_TINN_PATENT_QUALITY` 与 `M_INNOV_TINN_MARKET` 的「完全不支持」结论）。按 calc-logic 的「缺测维不补 0、剩余维权重重归一」，规模维权重落到 1.0，产物字段名为 `size_only_score`——**它是规模维的降级交付，不是综合分**。有维度可算、有维度不可算，故判**部分支持**。
- **基期声明**：库内专利仅 2021—2026；2017—2020 零行，规模维的四年合计不是五年合计
- **复现实测耗时**：约 0.6 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_TINN_COMPOSITE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_COMPOSITE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_TINN_COMPOSITE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

