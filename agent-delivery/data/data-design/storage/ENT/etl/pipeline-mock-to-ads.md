# ENT · Mock 直写 ADS（可选旁路）

> draft · **非** Demo 全链路主路径  
> 主路径见 [`pipeline-demo-mock.md`](./pipeline-demo-mock.md)（LLM → 约定 ODS → ETL 模拟 GDF）  
> 本文件仅覆盖：不跑工厂时，Python 按 D7 **直写同一套 ADS** 做 UI/契约冒烟

```yaml
---
doc_id: ENT-ETL-MOCK-ADS
element: ENT
role: etl
status: draft
version: "2026-08-12"
updated: 2026-08-12
engine: mysql
---
```

## 1. 何时用

- 只需验证 Java 只读 ADS / 前端指标，**暂不**跑 ODS→DWD 工厂。
- 与 `pipeline-demo-mock.md` **不得**混成两套 ADS 结构；表仍回链 [`../stores/mysql/ads.md`](../stores/mysql/ads.md)。

## 2. 待填（S2）

| 项 | 值 |
|---|---|
| 脚本仓 / 路径 | （待填） |
| 目标 ADS 表 | 回链 `stores/mysql/ads.md` |
| 与 Demo 主路径的切换说明 | （待填） |

## 3. 禁止

- 用本旁路替代 Demo「约定 ODS + 模拟 GDF」闭环验收  
- 另起 `demo_ads_*` 契约面  
