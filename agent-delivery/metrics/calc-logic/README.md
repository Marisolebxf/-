# calc-logic/ —— 口径计算逻辑 md（seed 的细稿）

seed yaml 只保留 8 件套摘要；完整口径（含子指标）在本目录 `{metric_id}.md`。

> **2026-10-23（E-METRIC-ALGOLIB-LAUNCH-L01 阶段1）**：20261021 王惠批 565 份全量入库后，
> 11 个域共 **566** 条（含存量 seed-only `M_CHAIN_STAGE_HEALTH_SCORE`），目录与条数如下。
> 支持度以 20261021 批实测为准；四维就绪度见 `registry/metric-readiness-matrix-{域}.yaml`。

| 域 | 本目录 | 条数 | 说明 |
|----|--------|------|------|
| CHAIN | [`CHAIN/`](./CHAIN/) | 100 | 产业链；20261021 批 99 + 存量 1（M_CHAIN_STAGE_HEALTH_SCORE） |
| COMMON | [`COMMON/`](./COMMON/) | 1 | 跨要素查询聚合；20261021 批 |
| ENT | [`ENT/`](./ENT/) | 96 | 企业维度；20261021 批 |
| INNOV | [`INNOV/`](./INNOV/) | 143 | 创新监测；20261021 批 |
| ORG | [`ORG/`](./ORG/) | 22 | 科研机构；20261021 批（20261023 新建域目录） |
| POLICY | [`POLICY/`](./POLICY/) | 35 | 政策分析；20261021 批 |
| SVC | [`SVC/`](./SVC/) | 51 | 产业服务；20261021 批 |
| SYNTH | [`SYNTH/`](./SYNTH/) | 46 | 综合智能分析；20261021 批 |
| TALENT | [`TALENT/`](./TALENT/) | 32 | 人才；20261021 批（20261023 新建域目录） |
| TECH | [`TECH/`](./TECH/) | 39 | 科技发展态势；20261021 批 |
| TNIE | [`TNIE/`](./TNIE/) | 1 | 科技新闻四要素抽取；20261021 批（20261023 新建域目录） |

入库过程件（指南 / 交接报告 / 批次 xlsx）在 [`../ingest/`](../ingest/)，不要和本目录混放。

新增域：建 `calc-logic/{域}/` + README 索引。Excel **活底稿**不进 git。
