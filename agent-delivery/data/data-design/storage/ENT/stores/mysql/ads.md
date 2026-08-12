# MySQL ADS · 企业维契约面

```yaml
---
doc_id: ENT-STORE-ADS
element: ENT
role: store-mysql
status: draft
version: "2026-08-12"
updated: "2026-08-12"
engine: mysql
s3_task: DATA-ENT-STORAGE-S3-L01
---
```

> **必须文档**。Java 业务 API **只读**本层（及经 Java→Python 的计算接口）；**禁止** Java 写 ADS / 扫 DWD。  
> **库名**：正式 `gkxlumenx_ads`；Demo 目标 `demo_gkxlumenx_ads`（或过渡同实例，见 pipeline-demo-mock）。  
> **status=draft**（契约表清单可随算法发布增补，改表须 CHANGELOG）。

## 1. 写读矩阵

| 写 | 读 |
|---|---|
| Python / 工厂写出；Demo：模拟 GDF 或旁路直写（[`../../etl/pipeline-mock-to-ads.md`](../../etl/pipeline-mock-to-ads.md)，不得冒充全链路） | **Java 只读**；前端不直连 |

## 2. 企业相关表清单（as-built / 算法仓）

真源指针（MySQL 实现以仓内 schema + 现网为准；旧 PG 草稿仅语义参考）：

| 表（`gkxlumenx_ads`） | 用途 | 生产者指针 |
|---|---|---|
| `enterprise_score` | A1 综合评分 | `demo-algo-ent-analysis` · `entan/depth` / realdata A1 |
| `enterprise_ranking` | A2 多维排名 | 同上 A2 |
| `enterprise_diagnosis` | A3 诊断短板 | 同上 A3 |
| `enterprise_centrality` | A4 链主中心性 | 同上 A4 + Nebula/图 |
| `realdata_key_enterprise` | 重点企业提取 | realdata demo-A1 |
| `realdata_enterprise_type_dist` | 类型分布 | realdata |
| `realdata_enterprise_news_stat` | 资讯统计 | realdata |
| `realdata_enterprise_risk` | 风险评分结果 | B1 |
| `realdata_policy_metrics` | 政策指标 | B3 |
| `realdata_chain_news_stat` | 链资讯统计 | D9 |
| `graph_node` / `graph_edge` | 图镜像兜底（1 跳） | Nebula 同步旁路 |

语义字段说明可对照：`${GKX_ROOT}/repos/demo-algo-ent-analysis/scripts/schema_ent_score.sql`（历史 PG 方言）与 `scripts/mysql/schema_mysql.sql`（MySQL 侧）。**以现网 MySQL 列名为准**；业务键已向 `org_id` 收敛处，文档与 API 映射以 Python Repository 为准。

## 3. 与 DWD 关系

- 工商/风险/预聚合原料在 DWD（[`dwd-entity`](./dwd-entity.md) / [`dwd-risk`](./dwd-risk.md) / [`dwd-aggregate`](./dwd-aggregate.md)）。  
- ADS **不**复制三方 ODS 字段进契约面（D7）。  
- 指标血缘 8 件套仍在 metrics 体系；本文件只列物理表。

## 4. 禁止

- 前端/Java 造假写 ADS  
- `demo_ads_*` 第二套契约表结构  
- 把 DWD 预聚合表伪装成 ADS 对外契约（除非已评审的只读例外并记入 API 契约）
