# ALGO-LIB-METRIC-DEPS-L01 handoff

- task: ALGO-LIB-METRIC-DEPS-L01
- status: done
- task_type: spike
- supervised_by: human:唐绍祖
- claimed_by: algorithm-agent
- ponytail: N/A
- reviewed_by: human:唐绍祖
- reviewed_at: 2026-08-24
- signoff: approved
- signoff_note: 按验收教程 §9「通过」分支会签；pending_ods 为待核验，非已确认缺口
- signed_by: human:淮政玮
- signed_at: 2026-08-24
- process_handoff: agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/ALGO-LIB-METRIC-DEPS-L01.md

## 交付

- `ALGO-LIB-METRIC-DEPS-L01-requirements.yaml`：表1，97 叶需规对应
- `ALGO-LIB-METRIC-DEPS-L01-metrics.yaml`：表2，指标/算法/公式/输入依赖
- `ALGO-LIB-METRIC-DEPS-L01-ods-gaps.yaml`：表3 机器投影
- `ALGO-LIB-METRIC-DEPS-L01-ods-gaps.md`：给人缺口清单
- `ALGO-LIB-METRIC-DEPS-L01-ods-status.xlsx`：8/25 四 sheet 主表
- `ALGO-LIB-METRIC-DEPS-L01-summary.md`：八维计数

## 架构自检

- 未改 seed / registry / 就绪度矩阵。
- 未写业务代码，未交 `*-deps.yaml` 混表。
- 未核 ODS 输入全部落在待核验 sheet，未标 full。
- pending_ods 未写入不满足。
- 第三方维度公式写“不展开”，但仍列 inputs。
- ODS 五档：full=1，partial=3，none=37，pending_ods=334，n/a=94。

## 开放项

- 三方 ODS 字段级核验完成后，pending_ods 条目需升格为 full/partial/none。
- 本表为 spike 底稿；正式 metric_id 由 B 轨 / data-agent 回填，不在本叶改 seed。
