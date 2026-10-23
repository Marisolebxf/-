# 区域技术壁垒（技术力叶子）（M_CHAIN_REG_TECH_BARRIER）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TECH_BARRIER.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_BARRIER.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_BARRIER_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_TECH_BARRIER |
| 指标名称 | 区域技术壁垒（技术力叶子） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链区域指数） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 产业链区域指数 → 技术力 → 区域技术壁垒 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_TECH_BARRIER.md` |

## 口径定义

公式的两个子项都能算出 48 个单元：空白子项 0.00—42.06（均值 22.02）、封锁子项 0.1705—0.5317（48 个不同值）、合成得分 0—100（42 个不同值）。但「统计年及前 3 年」的四年窗无法复现（缓存只有全期与 2024 单年两档），`kind='B'` 也无法单独切出（授权计数含实用新型与外观）→ 两处降级 → **部分支持**。本档位与 `code/M_CHAIN_REG_TECH_BARRIER_out.json` 的 `support_judgment.data_support_level` 一致。

## 计算逻辑说明

```text
Barrier=(minmax(BlankShare)+minmax(MeanEuclidDist))/2
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TECH_BARRIER.md` §二（M_CHAIN_REG_TECH_BARRIER.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_id`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：两个子项都算出了 48 个单元：空白占比 0.0%—42.063%，48/48 非空；封锁距离 0.1705—0.5317，48/48 有 IPC 样本；合成后 42 个不同取值。但口径有三个无法复原的缺口：①原稿的「统计年及前 3 年」窗口要求 2022—2025 逐年授权，缓存只有全期与 2024 单年两档；②原稿要求 `kind='B'`（发明授权），缓存只能给「granted_number 非空」，含实用新型与外观，导致空白占比被系统性低估；③封锁向量的 IPC 分布是全期而非 3 年窗。三项均为口径级降级，故判部分支持，不沿用旧版的完全转换支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 1.26 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TECH_BARRIER.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_BARRIER.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TECH_BARRIER_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

