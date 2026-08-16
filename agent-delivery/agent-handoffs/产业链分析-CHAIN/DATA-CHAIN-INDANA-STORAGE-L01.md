# DATA-CHAIN-INDANA-STORAGE-L01 · 行业分析要素库六表 — CHAIN storage 入站/店面补全

> **日期**：2026-08-16  
> **监管**：`human:淮政玮`  
> **仓**：仅 `gkx-orchestration` 编排资产（`storage/CHAIN/**` + 本 handoff）  
> **禁止**：commit / push；改 `task-registry.yaml`；改 `demo-algo-ent-analysis` 推理；对 `gkxlumenx_dwd` APPLY

## 任务认领（必填）

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:data-agent` |
| supervised_by | `human:淮政玮` |
| claim_type | `coordinator_dispatch` |
| 说明 | 长任务总控派单；task 开工时已 `in_progress` |

## Ponytail

| 字段 | 值 |
|------|-----|
| ponytail | `N/A` |
| 说明 | 定义/文档类；未用 YAGNI 裁必交付文档；本叶不写 Python 推理 / 前端 |

## Headroom

| 字段 | 值 |
|------|-----|
| headroom | `skip` |
| 说明 | 本叶未挂 Headroom；MySQL 抽检走本机 pymysql |

## 范围与实现

- 对照：`storage/CHAIN` 同构；产业链四表清单 [`inventory.md`](../../data/data-design/storage/CHAIN/sources/inventory.md) **保留**；行业分析另开切片。  
- **六表全收**（Demo 现表名 → 项目 DWD 仅去 `dwd_`）：

| Demo / 入站现表 | 项目 DWD |
|---|---|
| `dwd_industry_analysis_documents` | `industry_analysis_documents` |
| `dwd_industry_analysis_companies` | `industry_analysis_companies` |
| `dwd_industry_analysis_industries` | `industry_analysis_industries` |
| `dwd_industry_analysis_topics` | `industry_analysis_topics` |
| `dwd_industry_analysis_content_types` | `industry_analysis_content_types` |
| `dwd_industry_analysis_countries` | `industry_analysis_countries` |

- 列结构复制现表（`pk_id` / 类型 / UK / 技术字段一并收录）。CSV 英表 `documents` 等只作要素库对照。  
- `01-data-flow.md`：**未**改 `signoff_status=approved`；只加「增量切片 · 未会签」附录 + OPEN-CHAIN-INDANA-*。  
- 细表 frontmatter 保持 **draft**。

## 偏离说明

- 监管称六表已在 `demo_gkxlumenx_dwd`。2026-08-16 对 `192.168.88.43:3306` / `demo_gkxlumenx_dwd` 抽检：**六表均不存在**。同日三方 `gkx` @ `183.240.141.251:3318` **六表均在**。结构复制暂以三方 live `SHOW CREATE` 为真源（**不是** `gkx-mysql-raw` 沙箱旧稿压列名）。待 Demo 建表后以 Demo `SHOW CREATE` 覆盖（OPEN-CHAIN-INDANA-01）。  
- CSV 标 `document_id` 为主键；现表 PRI=`pk_id`。按铁律 **现表 DDL 赢**，不改列（OPEN-CHAIN-INDANA-02）。  
- GDF 派单包现行仅「企业」域，**无**行业分析 Mapping 作业名，不编造（OPEN-CHAIN-INDANA-03）。

## 产物清单

| 路径 | 说明 |
|---|---|
| `data/data-design/storage/CHAIN/sources/inventory-industry-analysis.md` | 三层命名 + 六表字段摘要 |
| `data/data-design/storage/CHAIN/sources/README.md` | 入口加本切片 |
| `data/data-design/storage/CHAIN/sources/inventory.md` | 仅加指针，四表正文未毁 |
| `data/data-design/storage/CHAIN/stores/mysql/dwd-industry-analysis.md` | 项目 DWD 六表店面 |
| `data/data-design/storage/CHAIN/stores/mysql/README.md` · `ads.md` | 索引 + ADS 不并入指针 |
| `data/data-design/storage/CHAIN/stores/README.md` | 索引提及本切片 |
| `data/data-design/storage/CHAIN/etl/pipeline-demo-mock.md` · `pipeline-ods-to-dwd.md` · `README.md` | 主路径一句 + DDL 指针 |
| `data/data-design/storage/CHAIN/etl/gkx_industry_analysis_show_create.sql` | 三方 live SHOW CREATE |
| `data/data-design/storage/CHAIN/etl/demo_gkxlumenx_dwd_industry_analysis_show_create.sql` | 去 `dwd_` 设计快照（未 APPLY） |
| `data/data-design/storage/CHAIN/README.md` · `CHANGELOG.md` · `01-data-flow.md` | 读序 / 一行变更 / 未会签附录 |
| 本 handoff | — |

## DoD 自检

| DoD | 结果 |
|---|---|
| 六表全收，去 `dwd_` 得 `industry_analysis_*` | ✅ |
| 列结构从现表复制，禁止空想改字段 | ✅（暂 gkx live；Demo 待补） |
| 不塞 ENT / 不用产业链资讯表冒充 | ✅ |
| CSV 英表只对照、不是项目 DWD 名 | ✅ |
| pipeline 主路径 + GDF 缺席 OPEN | ✅ |
| README / CHANGELOG / 流图不翻签 | ✅ |
| 细表 draft | ✅ |
| handoff + MCP evidence | ✅（本文件） |

## 开放项

| ID | 内容 | Owner | 挡会签增量？ |
|---|---|---|---|
| OPEN-CHAIN-INDANA-01 | Demo `demo_gkxlumenx_dwd` 六表未建；待补 Demo `SHOW CREATE` | data / 李伟 | 否（店面已按六表名落地） |
| OPEN-CHAIN-INDANA-02 | CSV 主键 vs 现表 `pk_id`；技术列 CSV 无。现表赢 | 数据 Lead | 否 |
| OPEN-CHAIN-INDANA-03 | GDF 无行业分析 Mapping 作业名，禁止编造 | GDF / 胡森泉 | 否 |
| OPEN-CHAIN-INDANA-04 | 正文不进 CHAIN ADS v2；抽边读 DWD 六表 | 算法后续叶 | 否 |
| OPEN-CHAIN-INDANA-05 | `01-data-flow` 增量切片待 `human:李伟` 会签（主图未翻签） | `human:李伟` | **本叶不自行关闭** |

## 下游

- 会签增量：`human:李伟`（主图 approved 不动）。  
- Demo 建入站六表 / 项目 DWD 去前缀表：另叶；**禁止**本叶 APPLY 正式库。  
- 图谱抽边：`ENT-YIJI-INFER-LLM` 读 `industry_analysis_documents` 等，本叶不改推理。

## 架构合规自检

| 铁律 | 结果 |
|---|---|
| 算法只在 Python；本叶不写算法 | ✅ |
| 调用链前端→Java→Python；Java 只读 ADS、不扫 DWD | ✅ |
| 图谱 NebulaGraph，禁止 Neo4j | ✅ |
| 关系库仅 MySQL | ✅ |
| D12 不碰 lumen 调 demo | ✅ 只改编排仓文档 |
| 禁止第二套 schema / CHAIN-demo | ✅ |
| 供应方 `dwd_*` ≠ 项目 DWD `industry_analysis_*` | ✅ |
| 细表 draft；流图不翻签 | ✅ |

## CI/CD

- 分支：`gkx-orchestration` 工作区改动（**本叶不 commit / 不 push**）  
- pipeline / K8s：N/A（纯文档）

## Cost（估 · 定义叶）

| 字段 | 值 |
|---|---|
| model_used | Cursor Grok 4.6 |
| actual_tokens | 估 ~9.5 万（含 MySQL 抽检与文档） |
| actual_cost | 估 <$5 |
| cost_warn | green |
