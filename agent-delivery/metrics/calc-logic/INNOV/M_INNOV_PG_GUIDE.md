# 政策导向（M_INNOV_PG_GUIDE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_GUIDE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_GUIDE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_GUIDE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_PG_GUIDE |
| 指标名称 | 政策导向 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 政策与条件保障力 → 发展战略引导力 → 政策导向分析（前瞻性 / 系统性 / 针对性三视图） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_PG_GUIDE.md` |

## 口径定义

没有「政策导向」现成结果面，故非完全直接支持；`dwd_policy_base.title` 与 `content` 两列 96% 有值，可支撑「前瞻性」这一维的文本判定，故非完全不支持；但「系统性」依赖的 `quote_policy` 全表只有 2 条非空且不是 JSON 数组、「针对性」依赖的 `policy_support` 全表 20,000 条均为字符串 `null`，两维的输入字段是空壳，故判**部分支持**。

## 计算逻辑说明

```text
三性等权；本库仅前瞻性可算（title 单字段 + 两级清洗），系统性/针对性不可算，故不输出综合分
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_GUIDE.md` §二（M_INNOV_PG_GUIDE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_patent`
- `dwd_policy_base`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：没有「政策导向」现成结果面，故非完全直接支持；`dwd_policy_base.title` 与 `content` 两列 96% 有值，可支撑「前瞻性」这一维的文本判定，故非完全不支持；但「系统性」依赖的 `quote_policy` 全表只有 2 条非空且不是 JSON 数组、「针对性」依赖的 `policy_support` 全表 20,000 条均为字符串 `null`，两维的输入字段是空壳，故判**部分支持**。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_PG_GUIDE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_GUIDE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_PG_GUIDE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

