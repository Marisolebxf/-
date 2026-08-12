# 管道 · DWD → ADS

> S2 回填 · Java **只读** ADS；写入者 = Python / 工厂 / Demo 模拟 GDF

## 意图

从 DWD（及算法产物）发布企业维 **ADS 契约面**，供 `gkxlumen-topic` 等聚合读取。

## 指针

| 项 | 路径 |
|---|---|
| 契约面文档 | [`../stores/mysql/ads.md`](../stores/mysql/ads.md)（S3 灌表） |
| 基线 | `architecture-baseline.md` D3/D7 |
| Demo | 经模拟 GDF 写出 `demo_*` ADS；旁路见 [`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md) |
| 现有算法写 ADS 参考 | `repos/demo-algo-ent-analysis`（过渡实例；非 LLM→ODS 主路径） |

## 禁止

Java/前端写 ADS；三方字段泄漏进契约面。
