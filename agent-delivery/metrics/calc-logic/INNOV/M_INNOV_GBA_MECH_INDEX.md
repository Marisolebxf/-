# 创新机制指数（湾区）（M_INNOV_GBA_MECH_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_MECH_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_MECH_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_MECH_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_MECH_INDEX |
| 指标名称 | 创新机制指数（湾区） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（湾区创新监测） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 湾区创新监测 → 粤港澳大湾区创新能力 → 创新机制指数 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_MECH_INDEX.md` |

## 口径定义

三个子项逐一落档：联合专利——主表**无 `applicants` 列**、关联表只有 20,000 个 pn（0.68%）；合作项目——`funded_institution` **整列为空**、参与机构是单值字段（可拆多机构的仅 0.05%）；成果转化——转移表同样只有 20,000 个 pn（0.68%）且名称对齐 2.07%。**三子项结构或数据均不闭合，0/3 可算**，故判**完全不支持**。本档位与 `code/M_INNOV_GBA_MECH_INDEX_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

```text
mech_index = (norm(joint) + norm(coop) + norm(transfer_rate)) / 3 × 100；缺测维不补 0，剩余权重归一
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_MECH_INDEX.md` §二（M_INNOV_GBA_MECH_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_base_info`
- `dwd_patent`
- `dwd_patent_applicants`
- `dwd_patent_transfer`
- `dwd_zh_author`
- `dwd_zh_project`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：三个子项全部无法按定义计算：联合专利缺 applicants 列且共申请人表仅 20,000 个 pn 的封闭抽样（0.68%，名称对齐 1.51%）；合作项目的 funded_institution 58,453 行整列为空、participating_institution 单值（可拆多机构仅 29 行）；成果转化表同为 20,000 pn 抽样（名称对齐 2.07%）。0/3 子项可算，指数无定义域 → 完全不支持
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_MECH_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_MECH_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_MECH_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

