# 事件影响力（M_INNOV_EVENT_INFLUENCE）

> 指标最终唯一解释口径（真源）。20261021 改源工程批（gkx 实测复算版）覆盖/迁入，对齐 `metrics/registry/cfg_metric-INNOV-seed.yaml`。
> 学术级调研正本（四判定 / 权威方法谱系 / 参考文献 / 附录）：`local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EVENT_INFLUENCE.md`；复现脚本 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_INFLUENCE.py` → `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_INFLUENCE_out.json`。

## 基础信息

| 项目 | 内容 |
|---|---|
| 指标ID | M_INNOV_EVENT_INFLUENCE |
| 指标名称 | 事件影响力 |
| 所属域 | INNOV（创新监测） |
| 一级模块 | 科技发展态势 |
| 更新频率 | 待确认（pending） |
| 数据支持度（四档） | **完全不支持** |
| UI 挂载 | 科创事件 GIS 标记点权重、重要性排序｜ **数据支持度**：**完全不支持** |
| 口径调研人 | 20261021 批指标文档写手（仿王惠方法论）；wanghui 标记: 未标注 |
| 基期（base_years_used） | []（截面件） |
| calc-logic 引用 | `metrics/calc-logic/INNOV/M_INNOV_EVENT_INFLUENCE.md` |

## 口径定义

事件表只有 20 行公告，资讯表 108,052 条但没有 event_id、簇 id、媒体层级；没有事件簇就不能算影响力，判完全不支持。

## 计算逻辑说明

```text
0.45×媒体层级 + 0.35×央媒报道量 + 0.20×周内报道跨度；本件因事件簇缺失不执行
```

完整计算过程（方法选择、分步推导、复现代码结果展示、逐链/逐项结果解读）见源件 `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EVENT_INFLUENCE.md` §二（M_INNOV_EVENT_INFLUENCE.py 零改语义复算）。

## 源表字段

gkx（183.240.141.251:3318，只读）源件点名表：

- `dwd_event`
- `dwd_industry_chain_news_info`

## 待建表字段

按 20261021 判档：关键依赖维在开发库+三方库均不可构建，暂无待建清单；补数据方向见源件 §四。

## 数据支持度与缺口

- **判档**：完全不支持
- **判档理由**：事件表只有 20 行会议公告，无报道明细；资讯表虽有 108,052 条、206 个源，但没有 event_id/簇 id/媒体层级，8 个必需字段里资讯表原样只有 0 个；要算影响力必须先聚类并建媒体层级表，两者都不存在或未验收。旧稿用新闻聚类 + 称谓规则硬分级，属于模型/人工假设，不是库内事件数据；本批规则禁止用新闻串伪事件，故判完全不支持。
- **基期声明**：事件表只有 2026-05-13/14 两天；资讯表覆盖 2025-02—2026-07，但没有事件簇，不能形成年度事件序列。used/missing 为空表示无年度基期，不是缺年补 0。

## 溯源与复现

| 项 | 值 |
|---|---|
| 入库批次 | 20261021_指标整体开发进度调研（第三方库 gkx 改源版） |
| 正本 MD | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/第三方库指标计算过程/M_INNOV_EVENT_INFLUENCE.md` |
| 复现脚本 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_INFLUENCE.py` |
| 复现产物 | `local-workspace/docs/tasks/investiage/20261021_指标整体开发进度调研/code/M_INNOV_EVENT_INFLUENCE_out.json` |
| 算法服务挂载 | 见 seed `algo_server_location`（阶段 2 上线时回填实测路径） |

## 更新记录

- 2026-08~2026-10: 历史版（王惠调研迁移 / 模拟王惠调研产出），本版覆盖前内容见 git 历史
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。
- 2026-10-23: 覆盖更新（20261021 gkx 改源版），由 `gen_phase1_calc_logic.py` 从源件结构化搬运生成（禁止手抄数字）。

