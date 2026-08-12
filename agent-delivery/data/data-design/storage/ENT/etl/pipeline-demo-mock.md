# ENT · Demo / LLM Mock 全链路（模拟 GDF）

> **口径 Owner**：`human:淮政玮`（2026-08-12 确认）  
> **地位**：Demo 灌数 **主路径**（全链路开发/测试闭环）  
> **S2 回填**：`DATA-ENT-STORAGE-S2-L01` · 2026-08-12  
> 规范：[`../../README.md`](../../README.md) §5.1 · 流图：[`../01-data-flow.md`](../01-data-flow.md) §7

```yaml
---
doc_id: ENT-ETL-DEMO-MOCK
element: ENT
role: etl
status: approved
version: "2026-08-12"
updated: "2026-08-12"
engine: multi
signoff_by: human:淮政玮
signoff_at: 2026-08-12
s2_fill: partial   # 命名表已填；LLM 脚本入口仍 OPEN-06 残余
---
```

## 1. 意图（拍板口径）

Demo 灌数基于 **ETL 工程调度模拟 GDF**。Mock 使用 **LLM** 写入 `demo_*` 库 / MinIO `demo_**` 桶 / Nebula `demo_**`。ODS 结构以 **三方在线约定文档**为准，不以现网三方 as-built 为准。少量覆盖样例，先全链路闭环后性能。

（全文见会签口径；本文件 §1 不改拓扑。）

## 2. 主路径

```text
LLM Mock → demo ODS（约定表结构）→ ETL 模拟 GDF → demo DWD → ADS/ES/Nebula/MinIO
```

可选旁路：[`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md)（不得冒充全链路验收）。

## 3. 结构 vs 实例

见规范 §5.1；结构真源 `stores/*`。

## 4. `demo_*` 命名表（OPEN-ENT-FLOW-06 · 命名部分关闭）

| 角色 | **目标命名（规范）** | **现网/过渡常见值** | 说明 |
|---|---|---|---|
| MySQL ODS | `demo_gkxlumenx_ods` | （多数环境尚未建） | LLM/Mock 写入面；表名=承诺名 |
| MySQL DWD | `demo_gkxlumenx_dwd` | 过渡：`gkxlumenx_dwd`（mockgen 直写） | 结构同 stores；正式非 demo 库另部署 |
| MySQL ADS | `demo_gkxlumenx_ads`（或同仓 ADS schema） | 算法 demo 常写 ADS 同实例 | 契约面结构不拆 |
| MinIO 桶 | `demo-gkx-analysis-results` | 过渡：`gkx-analysis-results` | 平台正文见 `platform/minio.md` |
| Nebula space | `demo_entan` / `demo_gkx_enterprise` | 过渡：`entan`（demo-algo-ent-analysis）/ `gkx_enterprise`（registry） | 结构见 stores/nebula；统一名待 Demo 会确认 |

**过渡期铁律**：在 `demo_*` 实例未建齐前，允许用过渡实例做联调，但 **ODS 字段口径仍必须对齐在线约定文档**；指标 D4 标 mock；不得把过渡实例结构回写成 stores 第二套 DDL。

## 5. LLM Mock / 调度入口（OPEN-ENT-FLOW-06 · 脚本部分仍开放）

| 项 | 值 |
|---|---|
| 三方 ODS 在线约定文档 | `agent-delivery/data/third-party-source/doc/` + `md-extract/`（**已关 OPEN-05**） |
| **LLM → 约定 ODS 脚本** | **尚未落仓**（OPEN-ENT-FLOW-06 残余）· 待 Demo 工程新建 |
| 现有规则 Mock（非 LLM·非 ODS 主路径） | `${GKX_ROOT}/repos/demo-algo-ent-analysis/entan/mockgen/generate.py` · 入口 `scripts/run_all.py` → 写 `gkxlumenx_dwd` |
| ETL 模拟 GDF（同构管道） | 见本目录 `pipeline-ods-to-dwd.md` 等；GDF 工作包 `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/` |
| 样本覆盖矩阵 | [`../seeds/README.md`](../seeds/README.md) |

## 6. 禁止

- 以现网三方 as-built 当 Demo ODS 真源  
- 第二套表结构 / 直写 ADS 冒充全链路  
- 性能全量灌数优先于闭环  
- 大段粘贴 SQL / 约定全文  
