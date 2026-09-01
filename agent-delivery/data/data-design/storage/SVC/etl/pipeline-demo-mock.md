# SVC · Demo 模拟 GDF 全链路（指针）

```yaml
---
doc_id: SVC-ETL-DEMO-MOCK
element: SVC
role: etl
status: draft
version: "2026-08-19"
updated: 2026-08-19
engine: multi
task_id: DATA-SVC-STORAGE-S2-L02
---
```

> 流图已会签：[`../01-data-flow.md`](../01-data-flow.md) §7。  
> **本单只写指针，不按 50100 灌数据，不开 F-SEED。**  
> 细表名见 S3 [`../stores/mysql/`](../stores/mysql/README.md)（仍 **draft**；OPEN-SVC-FLOW-12 写作关闭，未 approved）。  
> **2026-09-01**：灌数**零图谱**真源 = [`pipeline-to-nebula.md`](./pipeline-to-nebula.md) §18（`DEMO-SVC-GRAPH-TRIPLE-UI-L01`）。下文 §1 仍画「→ hang Nebula」是 S2 指针债，**不是**步2 对照删除清单；对照删除只认 §18。

## 1. 主路径（与会签同构）

```text
md-extract 国内机构要素库（结构约定）
  → 共用 demo_gkxlumenx_ods（不新建 / 不 DROP 33 表）
  → svc_rule_demo_kw_v1 圈定（name_cn + industry_l*_name）
  → 模拟 GDF → demo_* SVC DWD（只 hang ENT org_id）
  → demo_* SVC ADS / hang Nebula demo_gkx_chain
```

灌数触发真源（**F-SEED 才按**）：50100「基础指标」按钮 `append`/`replace`。  
同源引擎：`demo-algo-ent-analysis` `/entan/internal/svc/*` 与 CLI/`svcseed`。本单不调用。

## 2. 谁写谁读（阶段 F）

| 步 | 写 | 读 |
|---|---|---|
| ODS 结构 | ENT 已建；本域只圈选 | SVC 圈定读 `dwd_org_base_info` |
| SVC DWD/ADS | `demo-algo-ent-analysis`（F-SEED / F-ALGO） | 50100 基础指标 / 图谱 / 十模型 |
| 图 hang | 同上 → `demo_gkx_chain` | 50100 图谱菜单 |
| Java / 50892 | **不写**（阶段 P 虚线） | 本总控不施工 |

## 3. 圈定

规则版 `svc_rule_demo_kw_v1`，词表 [`../seeds/svc_rule_demo_kw_v1.md`](../seeds/svc_rule_demo_kw_v1.md)。命中过少按规则诚实空态。一律待核验（Q-SVC-010）。  
禁止把临时词典写成已批准准入主路径。

## 4. 脚本入口（已有 / 待 F-SEED）

| 用途 | 路径 | 本单 |
|---|---|---|
| ENT ODS 结构灌入（共用 33 表） | `demo-algo-ent-analysis/scripts/run_llm_ods.py` | 只引用，不重跑当 SVC 退出门 |
| SVC 圈定 + DWD（F-SEED） | `entan` `/internal/svc/*` · `svcseed` | **禁止本单执行** |
| fixture 24 家 | `seed_svc_demo_mock.py` | **旁路**，不得当退出门 |

旧 `run_svc_ods_reconcile.py` 随范围 3 删除。本单不复活灌数脚本。核对/补列若 F-SEED 需要，另单 `ALTER ADD`，禁 DROP 重建。S3 已落 Demo DWD/ADS 空表 DDL，不在本文件执行。

## 5. 对象前缀

建议 `svc/{task_id}/`。写作指针：[`pipeline-to-minio.md`](./pipeline-to-minio.md)（OPEN-SVC-FLOW-03 写作关）。MinIO 现网参数仍跟平台 OPEN-ENT-FLOW-02 / OPEN-SVC-FLOW-02。

## 6. 禁止

- 前端/Java 造假；`svcModelCatalog` 充数  
- 写正式 `gkxlumenx_*`  
- 平行 `gkx_service` space  
- 改 `lumen-topic-py` / `lumen-algo-py` / `lumen-svc-platform` / `lumen-ui-topic`  
- 改 `storage/CHAIN` / `industry-center`
