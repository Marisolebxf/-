# DATA-SVC-STORAGE-S3-L01 · 服务机构存储 S3 — stores 清单

> **日期**：2026-08-14  
> **确认**：`human:侯佳伟` · **2026-08-17** · **会签通过 · 放行 S4**（随「进行本地 S4」）  
> **本地签**：仅本地 handoff / 状态文案；**不 commit / 不 push**  
> **前置**：`ARCH-SVC-STORAGE-FLOW-SIGNOFF-L01` · S2 本地签收

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:侯佳伟` |
| claim_type | `coordinator_dispatch` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `lite` |
| 说明 | 清单级 stores；未粘贴全 DDL；未用 YAGNI 跳过 ADS / 待核验标注 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本机 MCP 面板未挂载；用 `scripts/task-mcp-cli.mjs` |

## 问题清单

- Demo `demo_gkxlumenx_dwd` / `_ads` **物理建表**未在本单执行（文档清单先行；联调缺表时另补）
- Q-SVC-010 / 六类仍阻断 live；圈定表已标待核验
- 招引/技术力口径（Q-SVCCHAIN-*）另轨 METRIC-OPEN，ADS 表仅占位

## 修改内容

### stores（`storage/SVC/stores`）

| 路径 | 内容 |
|---|---|
| `mysql/dwd-svc.md` | `service_org*` 5 表；ENT 共用键 vs 本域独有 |
| `mysql/ads.md` | **ADS 必含** · `svc_*` 10 表对齐 E7 四叶子 |
| `mysql/dim.md` | cfg_metric / 六类枚举 / 区划 |
| `elasticsearch/index-svc.md` + `sync.md` | `gkx_svc_org` 等 |
| `nebula/graph-svc.md` | `gkx_svc` space；禁复制 CHAIN |
| `stores/README.md` | 索引回填 |

### etl 指针

`pipeline-ods-to-dwd` / `dwd-to-ads` / `dwd-to-es` / `to-nebula` / `to-minio` / `mock-to-ads` + `etl/README.md`

## 测试结果

| 检查 | 结果 |
|---|---|
| ADS 文档存在 | ✅ `stores/mysql/ads.md` |
| 细表 status | 全部 `draft`（无 approved） |
| 圈定待核验 | ✅ `service_org` / `service_org_type_tag` |
| 未复制 ENT 主表 | ✅ |
| git push | ⏸ 本轮不推 |

## 遗留风险 / 开放项

| ID | 说明 | 是否挡 S4 |
|---|---|---|
| Q-SVC-010 | 圈定 live | 挡 live；不挡 S4 stub |
| Demo 物理 DDL | dwd/ads 本域表未建 | 否（联调另单） |
| Tag/Edge 对齐 E7 | OPEN | 否 |

**放行 S4**：`DATA-SVC-STORAGE-S4-L01` — **已放行**（2026-08-17 · 本地）。

## CI/CD

- 分支：本地工作区  
- commit / push：**跳过**（Owner 指示）  
- K8s：N/A  

## 可观测性

- N/A（存储定义文档）

## 架构合规自检

| # | 铁律 | |
|---|---|---|
| 1 | 算法只在 Python | ✅ 写路径声明 Python |
| 2 | 调用链 | ✅ Java 只读 ADS |
| 3 | Nebula | ✅ 禁 Neo4j；禁复制 CHAIN |
| 4–5 | 可观测 / CI | N/A 本轮不 push |
| 6 | demo→lumen | ✅ Demo 命名隔离 |
| 8 | ADS 先行 | ✅ ads.md 必含 |
| D12 | 不写正式 ODS 当真源 | ✅ |

## 涉及文件

- `agent-delivery/data/data-design/storage/SVC/stores/**`
- `agent-delivery/data/data-design/storage/SVC/etl/pipeline-*.md`
- `agent-delivery/data/data-design/storage/SVC/{README,CHANGELOG}.md`
- 本 handoff

## Cost（估）

| 字段 | 值 |
|---|---|
| model_used | Cursor Grok 4.5 |
| actual_tokens | 估 ~4–6 万 |
| actual_cost | 估 <$3 |
| cost_warn | false |
