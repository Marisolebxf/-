# 监测异常点识别（M_INNOV_FACTOR_ANOMALY）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_ANOMALY.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_ANOMALY.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_ANOMALY_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_FACTOR_ANOMALY |
| 指标名称 | 监测异常点识别 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（科技信息展示系统） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 科技全域态势 → 异常监测 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_FACTOR_ANOMALY.md` |

## 口径定义

库内**没有任何监测异常检测结果面**，也没有「科技活动年度监测」宽表；但 `gkx` 有四张表能拼出长度 ≥8 的年序列（中文论文 46 期、学者-论文关系 38 期、机构新设 46 期、项目立项 38 期），MAD 算法可完整实现并跑通。**唯一被口径点名、却结构性做不到的是专利序列**：`gkx.dwd_patent.apdt_year` 只有 2021—2026 共 6 期，永远达不到 ≥8。六类声明输入（专利／中文论文／机构／学者／英文论文／项目）里，只有三类按原语义落地（中文论文、机构新设、项目）；专利 6 期、学者无按年存量、英文论文仅 1,387 行，三类未落地，故判**部分支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_ANOMALY.md` §二（M_INNOV_FACTOR_ANOMALY.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_paper`
- `dwd_org_base_info`
- `dwd_patent`
- `dwd_scholar`
- `dwd_scholar_paper_relation`
- `dwd_zh_paper`
- `dwd_zh_project`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：库内**没有任何监测异常检测结果面**，也没有「科技活动年度监测」宽表；但 `gkx` 有四张表能拼出长度 ≥8 的年序列（中文论文 46 期、学者-论文关系 38 期、机构新设 46 期、项目立项 38 期），MAD 算法可完整实现并跑通。**唯一被口径点名、却结构性做不到的是专利序列**：`gkx.dwd_patent.apdt_year` 只有 2021—2026 共 6 期，永远达不到 ≥8。六类声明输入（专利／中文论文／机构／学者／英文论文／项目）里，只有三类按原语义落地（中文论文、机构新设、项目）；专利 6 期、学者无按年存量、英文论文仅 1,387 行，三类未落地，故判**部分支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_FACTOR_ANOMALY.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_ANOMALY.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_FACTOR_ANOMALY_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

