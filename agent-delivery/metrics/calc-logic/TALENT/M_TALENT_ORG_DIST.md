# M_TALENT_ORG_DIST（M_TALENT_ORG_DIST）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ORG_DIST.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ORG_DIST.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ORG_DIST_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_ORG_DIST |
| 指标名称 | M_TALENT_ORG_DIST |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技人才态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全转换支持** |
| UI 挂载 | — |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_ORG_DIST.md` |

## 口径定义

| 证据 | 实测值 | 落盘位置 | 对判档的作用 | |---|---|---|---| | 机构名填充 | 20,829 / 21,316 = 97.72% | `coverage.org_filled` / `org_share` | 分母足够大，不存在「整列空」 | | 机构串去重 | 2,108 个 | `coverage.distinct_org` | 足以做 CR/HHI，不需要外部机构库 | | 机构主键 | `scholar_org_id` 非空 0 行 | `coverage.org_id_filled` | 不能直接 group by 主键，必须走名称转换 |

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ORG_DIST.md` §二（M_TALENT_ORG_DIST.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_org_heis_info`
- `dwd_org_recruit_info`
- `dwd_scholar`
- `dwd_scholar_talent_flag`
- `dwd_scholar_work_experience`

## 待建表字段

20261021 实测后无新待建物理表挂账；缺口以「数据/字段缺失」形式登记（见下节与源件 §四）。

## 数据支持度与缺口

- **判档**：完全转换支持
- **判档理由**：| 证据 | 实测值 | 落盘位置 | 对判档的作用 | |---|---|---|---| | 机构名填充 | 20,829 / 21,316 = 97.72% | `coverage.org_filled` / `org_share` | 分母足够大，不存在「整列空」 | | 机构串去重 | 2,108 个 | `coverage.distinct_org` | 足以做 CR/HHI，不需要外部机构库 | | 机构主键 | `scholar_org_id` 非空 0 行 | `coverage.org_id_filled` | 不能直接 group by 主键，必须走名称转换 |
- **基期声明**：截面指标：dwd_scholar 为当前主档快照，无年度序列；需求提到的「环比增长率」需第二期快照，本件不产出（见 §四 4.1）

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_ORG_DIST.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ORG_DIST.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_ORG_DIST_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

