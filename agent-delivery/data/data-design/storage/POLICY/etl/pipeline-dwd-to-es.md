# 管道 · DWD → ES（政策）

```yaml
---
doc_id: POLICY-ETL-DWD-TO-ES
element: POLICY
role: etl
status: not-built
version: "2026-08-31"
updated: 2026-08-31
engine: elasticsearch
task_id: DATA-POLICY-STORAGE-ETL-FILL-L01
---
```

## 结论：本域不施工

**政策域没有 DWD → ES 管道，`polan` 内零 ES 代码**（2026-08-31 全仓核查）。本文件存在的意义是占位说明，不是待办设计。

与 [`../stores/elasticsearch.md`](../stores/elasticsearch.md) 一致：本管线不建独立政策 ES 索引。

## 为什么不建

政策检索目前由 ADS 关系表直查满足（层级/类型/地区/时序都是结构化维度，量级也没到需要倒排的程度）。为一个模块单开索引会多一套同步链路和一致性责任，收益不匹配。

## 什么情况下才需要

出现下列任一条，再另开单评估，**不在本树预建**：

- 政策正文全文检索（`keypoints` / `factors` 长文本模糊匹配）成为产品硬需求；
- 展示侧 `OPEN-POLICY-DISP-03`（浏览量 / 智能排序权重）落地，排序因子超出 SQL 可承受；
- 政策与企业/产业跨域联合检索要求统一召回层。

届时优先**挂已有平台索引**，而不是新建 `demo_policy_*` 一套。

## 禁止

为凑齐 ETL 文档而预建空索引；把 ES 写进 `run_all_policy` 步序；在 `stores/elasticsearch.md` 之外另立索引口径。
