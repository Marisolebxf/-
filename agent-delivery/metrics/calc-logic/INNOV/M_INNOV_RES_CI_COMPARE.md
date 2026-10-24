# 多企业竞争情报比对（M_INNOV_RES_CI_COMPARE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_CI_COMPARE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_COMPARE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_COMPARE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_RES_CI_COMPARE |
| 指标名称 | 多企业竞争情报比对 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 竞争情报比对页——12×12 重叠矩阵、企业重叠等级、规模×重叠四象限战略图 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_RES_CI_COMPARE.md` |

## 口径定义

矩阵、等级、四象限三件产物都已跑出：66 对重叠分 18.48—63.08，按 P30=39.66 / P70=48.43 切成「高 40 对 / 中 52 对 / 低 40 对」；12 家里 11 家落「中」、惠科落「低」。但重叠维实际只有 IPC 单维（学者维 0/66），论文规模有 3 家为 0，且派单措辞的「区域」口径未实现。故判**部分支持**：企业级竞争情报比对可用，区域竞争力对比需另立指标。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_CI_COMPARE.md` §二（M_INNOV_RES_CI_COMPARE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`
- `dwd_patent`
- `dwd_scholar`
- `dwd_zh_author`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：矩阵、等级、四象限三件产物都已跑出：66 对重叠分 18.48—63.08，按 P30=39.66 / P70=48.43 切成「高 40 对 / 中 52 对 / 低 40 对」；12 家里 11 家落「中」、惠科落「低」。但重叠维实际只有 IPC 单维（学者维 0/66），论文规模有 3 家为 0，且派单措辞的「区域」口径未实现。故判**部分支持**：企业级竞争情报比对可用，区域竞争力对比需另立指标。
- **基期声明**：竞争矩阵为截面比对，无年度分母；专利为全历史并集，论文为库内 100,900 篇切片

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_RES_CI_COMPARE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_COMPARE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_RES_CI_COMPARE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

