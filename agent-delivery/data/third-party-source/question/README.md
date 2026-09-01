# question — 给三方供应方的问题清单

> **方法真源**：`agent-delivery/agent-handoffs/算法库联调-ALGO-LIB/DATA-SUPPLIER-Q-FROM-METRICS-DISPATCH.md`（2026-09-01 锁定）。  
> 只问供应方 `dwd_*` 字段与主键，不问项目派生列（如 `related_entities`）。

## 范围

- 本波算法类型：`STAT` / `COMPUTE` / `MODEL` / `third_party` / `GRAPH` / `UNKNOWN`
- **`MIXED` 后拆**，本波不进对外清单
- D1 `draft` 照样出题，标「随口径修订」；文档按**分析日**追加日志
- 进度表「源缺口」：sidecar [`source-gap-index.yaml`](source-gap-index.yaml) **优先于**矩阵 `d3_gap`

## 目录（注册表域）

| 维度目录 | 域码 | 清单 |
|----------|------|------|
| [产业链维度/](产业链维度/) | CHAIN | 待补 |
| [企业维度/](企业维度/) | ENT | 待补 |
| [政策维度/](政策维度/) | POLICY | [POLICY-SUPPLIER-QUESTIONS.md](政策维度/POLICY-SUPPLIER-QUESTIONS.md) |
| [服务机构维度/](服务机构维度/) | SVC（中文域名：产业服务） | 待补 |
| [综合维度/](综合维度/) | **SYNTH** | 待补 |
| [创新维度/](创新维度/) | INNOV | 待补 |
| [机构维度/](机构维度/) | ORG | 待补 |
| [人才维度/](人才维度/) | TALENT | 待补 |
| [技术维度/](技术维度/) | TECH | 待补 |
| [通用维度/](通用维度/) | COMMON | 待补（命中本波类型再写） |
| [科技动态维度/](科技动态维度/) | TNIE | 待补（命中本波类型再写） |

约定：文件名**不加日期**；日期只写在「分析日志」章节。发给对方看「现行待回复」；日志可一并转发以便对日期。
