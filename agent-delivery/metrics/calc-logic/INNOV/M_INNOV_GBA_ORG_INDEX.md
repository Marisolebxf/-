# 创新机构指数（湾区）（M_INNOV_GBA_ORG_INDEX）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_ORG_INDEX.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_ORG_INDEX.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_ORG_INDEX_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_GBA_ORG_INDEX |
| 指标名称 | 创新机构指数（湾区） |
| 所属域 | INNOV（创新监测） |
| 一级模块 | INNOV（湾区创新监测） |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **部分支持** |
| UI 挂载 | 科技信息展示系统 → 科技发展态势 → 湾区创新监测 → 粤港澳大湾区创新能力 → 创新机构指数 |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: true |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_GBA_ORG_INDEX.md` |

## 口径定义

无现成「机构指数」结果面 → 非完全直接支持；三个子项中**载体数量**（底册 189,116 行 + 科研院所 2,074 行，`org_id` 无交集）与**科技型机构**（高企标签 202,424 行、去重 27,634 家 + 科研院所）完整可算，**载体产出**只剩专利（2,126,758 件），论文维因作者单位与底册精确对齐率仅 **1.01%** 而整维缺测；11 城仅 4 城有机构底册、港澳为 0 → **部分支持**。本档位与 `code/M_INNOV_GBA_ORG_INDEX_out.json` 的 `support_judgment` 一致。

## 计算逻辑说明

```text
org_index = (norm(载体数量) + norm(载体产出) + norm(科技型机构)) / 3 × 100
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_ORG_INDEX.md` §二（M_INNOV_GBA_ORG_INDEX.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_en_author`
- `dwd_en_paper`
- `dwd_forg_base_info`
- `dwd_org_base_info`
- `dwd_org_tech_tag`
- `dwd_patent`
- `dwd_research_institute_base_info`
- `dwd_zh_author`
- `dwd_zh_journal`
- `dwd_zh_paper`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：部分支持
- **判档理由**：三子项中载体数量与科技型机构完整可算（底册 189,116 行、高企标签 202,424 行、科研院所 2,074 行），载体产出只剩专利单口径（论文作者单位与底册对齐率 1.01%，整维缺测）；11 城仅 4 城有机构底册，港澳在 dwd_forg_base_info 中为 0 —— 故判部分支持
- **基期声明**：本指标为截面计算，产物与参数中均无年度键、无年份窗口，不存在时序分母，故 used/missing 均为空；不是「缺年按 0 摊入」的情形。
- **复现实测耗时**：约 0.4 秒（源件落盘记录）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_GBA_ORG_INDEX.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_ORG_INDEX.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_GBA_ORG_INDEX_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

