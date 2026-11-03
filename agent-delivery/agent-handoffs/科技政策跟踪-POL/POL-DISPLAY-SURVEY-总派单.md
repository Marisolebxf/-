# POL-DISPLAY 调研段 · 总派单

总控：`POL-DISPLAY-长任务总控.md`。监管 `human:淮政玮`。执行 `agent:arch-agent`。强度：ponytail off（定义任务，不缩文档）。

四叶可同时写。每叶只写自己的两个文件。

共同判定：

| 档 | 含义 |
|---|---|
| 可接统计读面 | 指标 `algorithm_type` 为 STAT 或 COMPUTE，页面能挂 `metric_id`。D4=mock 必须写明，数值仍是 mock |
| 501 | MODEL 或未注册的推演 / 解析 / 研报。契约冻结前真路径不得用 fixture 填 |
| 跨项索引 | 专题 E7、门户扶持、GDF、第 7 项读图。只写已有任务号，不设成展示新任务 |

`/goal` 头（四叶通用，替换叶名与路径）：

```text
/goal arch-agent
身份：架构师。只写本叶文档。
强度：ponytail off
监管人：human:淮政玮
总控：agent-handoffs/科技政策跟踪-POL/POL-DISPLAY-长任务总控.md
仓：gkx-orchestration。不 commit，不 push，不改注册表，不改 WBS，不改 lumen/demo。
```

## DS-10

任务 `POL-DISPLAY-SURVEY-DS10-L01`。页：科创政策全景。对照 `FE-POL-01A`、`FE-POL-01B`。用户故事 US-DS-POL-01～04 里属于全景的部分。SRS：`bid-reference/srs/02-科技信息展示系统/科技政策跟踪/科创政策全景.md`。产物 `survey/DS-10.md`。

## DS-11

任务 `POL-DISPLAY-SURVEY-DS11-L01`。页：政策分析评价。对照 `FE-POL-02A`。US-DS-POL-05。SRS：`政策分析评价.md`。推演模型不要写进本叶。产物 `survey/DS-11.md`。

## DS-12

任务 `POL-DISPLAY-SURVEY-DS12-L01`。页：政策效果推演。对照 `FE-POL-03A`。US-DS-POL-06。SRS：`政策效果推演.md`。必须写明推演与专题「政策布局推荐」分键。产物 `survey/DS-12.md`。

## PC

任务 `POL-DISPLAY-SURVEY-PC-L01`。四页合为一叶：政策数据治理、智能政策拆解、多维政策对比、智能研报。对照 `FE-POL-04A`～`07A`。US-DS-POL-07～10。SRS 在 `政策对比功能升级（核增需求）/`。产物 `survey/PC.md`。不要拆成四份文件。
