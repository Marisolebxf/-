# 人才结构（区域）（M_CHAIN_REG_TALENT_STRUCTURE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-CHAIN-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TALENT_STRUCTURE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TALENT_STRUCTURE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TALENT_STRUCTURE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_CHAIN_REG_TALENT_STRUCTURE |
| 指标名称 | 人才结构（区域） |
| 所属域 | CHAIN（产业链分析） |
| 一级模块 | CHAIN（产业链区域指数） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 产业链区域指数 → 学术生态竞争力 → 人才结构 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: false |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/CHAIN/M_CHAIN_REG_TALENT_STRUCTURE.md` |

## 口径定义

表看起来是齐的，但四张附表与主表的 `scholar_id` 属于两个 ID 空间，学历表 15,851 个 ID 只有 1,753 个能在主表找到（8.22%），研究方向 8.69%、头衔 8.72%；主表 21,316 人中落 4 市仅 1,202 人，其中能对上学历的 119 人。学历结构的分母不足百人级，无法支撑 48 个链×城单元 → **完全不支持**。本档位与 `code/M_CHAIN_REG_TALENT_STRUCTURE_out.json` 的 `support_judgment.data_support_level` 一致。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TALENT_STRUCTURE.md` §二（M_CHAIN_REG_TALENT_STRUCTURE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_scholar`
- `dwd_scholar_education_background`
- `dwd_scholar_research_direction`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：人才结构的核心是「链上人才按学历/职称分层」，但两跳都断：其一，学历表 15,851 个 scholar_id 与主表 21,316 个只有 1,753 个（8.22%）能对上，研究方向与头衔同样只有 8.7%，四张附表实际是另一个学者宇宙；其二，能落 4 市的主表学者仅 1,202 人（5.64%），其中同时有学历记录的只有 119 人，不足以支撑任何市域学历分布；其三，学者机构以高校为主，与产业链标签无挂接，链维只能靠研究方向英文词代理，48 个单元里仅 14 个非零。结构与数据均不构成可算闭环，故维持完全不支持。
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.78 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_CHAIN_REG_TALENT_STRUCTURE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TALENT_STRUCTURE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_CHAIN_REG_TALENT_STRUCTURE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

