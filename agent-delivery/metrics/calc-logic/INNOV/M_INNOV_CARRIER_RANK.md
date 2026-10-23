# 创新载体排名（M_INNOV_CARRIER_RANK）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CARRIER_RANK.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_RANK.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_RANK_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_CARRIER_RANK |
| 指标名称 | 创新载体排名 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 创新监测 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | 科技信息展示系统·科技发展态势·全球创新监测 / 创新载体排行榜（多维度排名展示、排名筛选功能、创新载体详情查看）｜ **数据支持度**：**完全转换支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_CARRIER_RANK.md` |

## 口径定义

无现成「创新载体排名」结果表 → 非完全直接支持；深圳存活载体池 3,000 家当日现转完成总体宇宙排名（3,000 名、同分并列跳号）+ 领域宇宙演示（H02J 内 31 家可排）→ **完全转换支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CARRIER_RANK.md` §二（M_INNOV_CARRIER_RANK.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_zh_author`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：无现成「创新载体排名」结果表 → 非完全直接支持；深圳存活载体池 3,000 家当日现转完成总体宇宙排名（3,000 名、同分并列跳号）+ 领域宇宙演示（H02J 内 31 家可排）→ **完全转换支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_CARRIER_RANK.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_RANK.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_CARRIER_RANK_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

