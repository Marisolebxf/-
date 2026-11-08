# POL-L2-PC1-STRUCT-DATA · 政策库结构化 · 后台数据架构设计

- 任务：`POL-L2-PC1-STRUCT-DATA` · 2026-11-08 · `agent:data-agent` · 监管：`human:淮政玮`
- SRS：**603** · 上游：STRUCT-ARCH

## 读表（零建表）

| 库 | 表 | 用途 |
|---|---|---|
| `gkxlumenx_ads` | `policy_text_parse` | 条款/标签；覆盖率分子；单政策摘要 |
| `gkxlumenx_ads` | `policy_industry_rel` | 产业关联概览 |
| `gkxlumenx_dwd` | `policy_base_info` | 覆盖率分母；政策选择候选 |
| `gkxlumenx_dwd` | `script_state` | job=c2 最新批次时间 |

不重开 GDF；不写 gapfill；跨项只消费第 6 项结果。`policyId` 拣 `policy_text_parse` 行。D4 不改绿。
