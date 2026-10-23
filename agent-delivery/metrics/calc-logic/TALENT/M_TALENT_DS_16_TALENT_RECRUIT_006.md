# 文化融合风险评估（M_TALENT_DS_16_TALENT_RECRUIT_006）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-TALENT-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_006.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_006.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_006_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_TALENT_DS_16_TALENT_RECRUIT_006 |
| 指标名称 | 文化融合风险评估 |
| 所属域 | TALENT（科技人才态势） |
| 一级模块 | 科技信息展示系统 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 国际人才引进页「文化融合风险」（建议不上线自动评分，见 §5.4） |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/TALENT/M_TALENT_DS_16_TALENT_RECRUIT_006.md` |

## 口径定义

「文化融合风险」= 外籍/跨文化身份 × 文化距离 × 适应结果。身份侧 0 字段、距离侧 0 字段、结果侧 0 张表；唯一有数的是「海外经历」628/896 人，而经历越多通常适应越好，与风险方向相反。故判**完全不支持**。

## 计算逻辑说明

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_006.md` §二（M_TALENT_DS_16_TALENT_RECRUIT_006.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_forg_base_info`
- `dwd_scholar`
- `dwd_scholar_edu`
- `dwd_scholar_talent_flag`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：宗教/族群字段 0 列、文化/社区类表 0 张、国籍/签证字段 0 列；`dwd_forg_base_info` 是境外企业底册而非境外人才，country 列去重为 0；bio 提到华裔/外籍合计 3 条。既无「外籍身份」也無「融合结果」，无法构建风险评分。
- **基期声明**：纯截面判定，且不存在可用时间序列：身份、宗教、融合结果字段均无；履历表的 start_time/end_time 只记机构任期，不是适应过程。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_TALENT_DS_16_TALENT_RECRUIT_006.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_006.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_TALENT_DS_16_TALENT_RECRUIT_006_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-10-23: 新建（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

