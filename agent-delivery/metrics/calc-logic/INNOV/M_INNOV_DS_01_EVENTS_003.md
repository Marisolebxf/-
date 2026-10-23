# 重要性等级（M_INNOV_DS_01_EVENTS_003）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_01_EVENTS_003.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_01_EVENTS_003.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_01_EVENTS_003_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_DS_01_EVENTS_003 |
| 指标名称 | 重要性等级 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技发展态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 科创事件 GIS 标记点颜色/大小、三档筛选｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_DS_01_EVENTS_003.md` |

## 口径定义

dwd_event 只有 20 行会议公告，缺事件 id、链、关注度、影响力、状态；没有事件流就不能合成等级，判完全不支持，只写需求。

## 计算逻辑说明

```text
0.5×关注度 + 0.5×影响力；P70/P30 三档；本件因输入不存在，不执行
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_01_EVENTS_003.md` §二（M_INNOV_DS_01_EVENTS_003.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_event`
- `dwd_id`
- `dwd_merger_acquisition_events_party_info`
- `dwd_policy_base`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：dwd_event 只有 20 行、15 列，日期仅 2026-05-13 至 2026-05-14，内容是医药论坛名录，不是科创事件流；10 个必需字段里原样存在的只有 0 个，chain_id/事件类型/关注度/影响力/事件状态/报道量/报道源全部缺失；全库没有事件簇表或事件结果面。没有输入就不能合成等级，用政策或新闻代理会伪造事件语义，故判完全不支持。
- **基期声明**：事件表只有 2026-05-13/14 两天，且不是年度序列；本指标没有可用的年度基期。used/missing 为空不是「缺年补 0」，而是事件流本身不存在。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_DS_01_EVENTS_003.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_01_EVENTS_003.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_DS_01_EVENTS_003_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

