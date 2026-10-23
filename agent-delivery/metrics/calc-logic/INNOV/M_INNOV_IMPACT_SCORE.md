# 创新影响分数（M_INNOV_IMPACT_SCORE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_IMPACT_SCORE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_SCORE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_SCORE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_IMPACT_SCORE |
| 指标名称 | 创新影响分数 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统／科技发展态势／全球创新监测 |
| 更新频率 | 待确认 |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 机构影响榜、领域影响榜 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | [2021, 2022, 2023] |
| 缺失年份 | [2017, 2018, 2019, 2020] |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_IMPACT_SCORE.md` |

## 口径定义

在 4,039 家「既发论文又申专利」的机构里，综合影响分第一是**广州中医药大学第一附属医院 68.76**（论文 751 篇、共著邻居 194 个，两项都是盘内最大），第二是**华南理工大学 56.05**（专利 28,053 件），而专利件数占全盘 **8.6573%** 的**华为技术有限公司只有 39.47**（第 6）——它 81,376 件专利在 $\log$ 压缩后被论文与共著两维彻底稀释，授权率 16.4176% 又拉了后腿。换成熵权，华为反而以 59.63 登顶。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_IMPACT_SCORE.md` §二（M_INNOV_IMPACT_SCORE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_cited`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：在 4,039 家「既发论文又申专利」的机构里，综合影响分第一是**广州中医药大学第一附属医院 68.76**（论文 751 篇、共著邻居 194 个，两项都是盘内最大），第二是**华南理工大学 56.05**（专利 28,053 件），而专利件数占全盘 **8.6573%** 的**华为技术有限公司只有 39.47**（第 6）——它 81,376 件专利在 $\log$ 压缩后被论文与共著两维彻底稀释，授权率 16.4176% 又拉了后腿。换成熵权，华为反而以 59.63 登顶。
- **基期声明**：专利 apdt_year 在 2017—2020 零行（DATA_FACTS §3.13），故 missing 记这四年；2024 论文是回填孤峰（32,379 篇 = 32.09%，§3.74），不按 0 摊入、也不计入 used；2025—2026 专利只有 440,401 / 74,810 件，明显是尚未公开完全的残年，同样不进窗口。本件为截面计件，窗口只用于解释「件数覆盖哪个年代」，不参与归一。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_IMPACT_SCORE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_SCORE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_IMPACT_SCORE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

