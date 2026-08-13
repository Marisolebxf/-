# CHAIN · Demo / 约定 ODS 全链路（模拟 GDF）

> **口径**：对齐 ENT `pipeline-demo-mock.md`；CHAIN S1 锁定真源与库名。  
> **建表 Owner**：`human:李伟`（S2）  
> 流图：[`../01-data-flow.md`](../01-data-flow.md) §7

```yaml
---
doc_id: CHAIN-ETL-DEMO-MOCK
element: CHAIN
role: etl
status: draft
version: "2026-08-13"
updated: "2026-08-13"
engine: multi
---
```

## 1. 意图

Demo 灌数基于 **ETL 调度模拟 GDF**。ODS 结构以 **`third-party-source/doc/`** 为准（优先 `md-extract/`），不以现网 as-built 为准。落 `demo_*`。

## 2. 主路径

```text
约定文档(md-extract 产业链要素库)
  → CREATE / 灌入 demo_gkxlumenx_ods
  → ETL 模拟 GDF → demo_dwd / ads / ES / Nebula / MinIO
```

## 3. 命名表

| 角色 | 开发默认 | 禁止作 Demo 默认 |
|---|---|---|
| MySQL ODS | `demo_gkxlumenx_ods` | `gkxlumenx_ods` |
| MySQL DWD | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` |
| MySQL ADS | `demo_gkxlumenx_ads` | `gkxlumenx_ads` |

## 4. S2 待回填

- 建表脚本路径（可参考 `demo-algo-ent-analysis/entan/llm_ods`）
- `SHOW CREATE TABLE` / 表清单探测摘要
- seeds 入口

## 5. 旁路

直写 ADS 仅冒烟，不替代全链路验收；S2 补 `pipeline-mock-to-ads.md`。
