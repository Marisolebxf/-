# CHAIN · Mock 直写 ADS（可选旁路）

> draft · **非** Demo 全链路主路径  
> 主路径见 [`pipeline-demo-mock.md`](./pipeline-demo-mock.md)

```yaml
---
doc_id: CHAIN-ETL-MOCK-ADS
element: CHAIN
role: etl
status: draft
version: "2026-08-13"
updated: 2026-08-13
engine: mysql
---
```

## 何时用

只需验证 Java 只读 ADS / 前端指标，**暂不**跑 ODS→DWD 工厂时。不得与主路径形成两套 ADS 结构。

## 指针

| 项 | 说明 |
|---|---|
| ADS 表正文 | S3 → [`../stores/`](../stores/)（`mysql/ads.md`） |
| ENT 同构参考 | [`../../ENT/etl/pipeline-mock-to-ads.md`](../../ENT/etl/pipeline-mock-to-ads.md) |
| 本域开放 | 待 ADS 清单会签后补脚本路径 |
