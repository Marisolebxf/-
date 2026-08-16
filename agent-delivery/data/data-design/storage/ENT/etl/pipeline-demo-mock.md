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
s2_fill: complete   # 命名表 + LLM/离线 ODS 脚本已落仓（DEMO-ENT-LLM-ODS-L01）
---
```

## 1. 意图（拍板口径）

Demo 灌数基于 **ETL 工程调度模拟 GDF**。Mock 使用 **LLM**（及离线确定性样例）写入 `demo_*` 库 / MinIO `demo_**` 桶 / Nebula `demo_**`。ODS 结构以 **`third-party-source/doc/`** 为准（**优先读 `md-extract/`**，权威裁决看 xlsx），不以现网三方 as-built 为准。少量覆盖样例，先全链路闭环后性能。

（全文见会签口径；本文件 §1 不改拓扑。）

## 2. 主路径

```text
LLM Mock → demo ODS（约定表结构）→ ETL 模拟 GDF → demo DWD → ADS/ES/Nebula/MinIO
```

可选旁路：[`pipeline-mock-to-ads.md`](./pipeline-mock-to-ads.md)（不得冒充全链路验收）。

## 3. 结构 vs 实例

见规范 §5.1；结构真源 `stores/*`。

## 4. `demo_*` 命名表（OPEN-ENT-FLOW-06 · 命名已关）

> **决策（2026-08-13 · `human:淮政玮`）**：**开发阶段一律使用 `demo_*` 三件套**（ODS/DWD/ADS），与真实 ODS 接入后的开发/测试过程**隔离**。  
> 禁止 Demo/联调默认读写 `gkxlumenx_ods` / `gkxlumenx_dwd` / `gkxlumenx_ads`（对账探测除外，须显式开关）。  
> 落地任务：`DEMO-ENT-DEMO-DB-TRIPLE-L01`（监管 `human:徐滕强`；**2026-08-13 库已建齐 + 开发默认已切 demo_***）。建库 SQL 备份：`demo-algo-ent-analysis/scripts/mysql/create_demo_dbs.sql`。

| 角色 | **目标命名（规范 · 开发默认）** | **真实/正式（禁作 Demo 默认）** | 说明 |
|---|---|---|---|
| MySQL ODS | `demo_gkxlumenx_ods` | `gkxlumenx_ods` | LLM/Mock 写入面；表名/字段 = **md-extract**；**已建**（国内机构要素库 33 表结构） |
| MySQL DWD | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` | 结构同 stores；**已建**（enterprise_* 结构，无生产数据拷贝） |
| MySQL ADS | `demo_gkxlumenx_ads` | `gkxlumenx_ads` | 契约面结构同构；**已建** |
| MySQL DIM | `demo_gkxlumenx_dim` | `gkxlumenx_dim` | 码表；**已建**（16 表结构+字典拷贝，联调需要） |
| MySQL CFG | `gkxlumenx_cfg`（可共享） | 同左 | 模型注册等配置可共享；若污染风险再拆 `demo_gkxlumenx_cfg` |
| MinIO 桶 | `demo-gkx-analysis-results` | `gkx-analysis-results` | 平台正文见 `platform/minio.md` |
| Nebula space | `demo_entan` / `demo_gkx_enterprise` | `entan` / `gkx_enterprise` | 统一名待 Demo 会确认 |

**铁律**：结构共用 `stores/*`；**实例隔离**。ODS 字段口径对齐 `doc/`；指标 D4 标 mock；不得把真实库 as-built 回写成 stores 第二套 DDL。无建库权限时用 `--sql-out` / 交 DBA 执行 `create_demo_dbs.sql`。

## 5. LLM Mock / 调度入口（OPEN-ENT-FLOW-06 · **已关闭**）

| 项 | 值 |
|---|---|
| 三方 ODS | **权威** `doc/` xlsx；**优先读** `doc/md-extract/` |
| **LLM → 约定 ODS 脚本** | `${GKX_ROOT}/repos/demo-algo-ent-analysis/` · `entan/llm_ods/` · 入口 `scripts/run_llm_ods.py`（`--self-check` / `--offline` / `--llm` / `--sql-out`）· README：`entan/llm_ods/README.md` · 任务 `DEMO-ENT-LLM-ODS-L01` |
| **灌数接入 UI** | `DEMO-ENT-UI-SEED-ODS-L01` · system-test「灌数据」默认 **追加**（`mode=append`）；下拉可选 **重建**（`mode=replace`）。主路径 `llm_ods` → `demo_gkxlumenx_ods` → 模拟 GDF → `demo_gkxlumenx_dwd` → 算法全量重算 ADS。禁止默写正式库。 |
| 现有规则 Mock（非主路径） | `entan/mockgen/generate.py` · 仅 `ENTAN_SEED_LEGACY_MOCKGEN=1` 旁路；**不算**主路径验收 |
| ETL 模拟 GDF（同构管道） | 见本目录 `pipeline-ods-to-dwd.md` 等；GDF 工作包 `data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/` |
| 样本覆盖矩阵 | [`../seeds/README.md`](../seeds/README.md) |

## 6. 禁止

- 以现网三方 as-built、或未对齐 `doc/` 的 Wave A 草稿，当 Demo ODS 真源  
- 第二套表结构 / 直写 ADS 冒充全链路  
- 性能全量灌数优先于闭环  
- 大段粘贴 SQL / 约定全文  

## 7. 上链（Demo 补节 · `ENT-CHAIN-HANG-MOCK-L01`）

在模拟 GDF 灌出 `enterprise_base`、且 CHAIN 已有 `industry_chain_node`（INB）之后，把企业挂到链节点。过程与字段对照见 CHAIN [`../../CHAIN/etl/pipeline-ent-hang.md`](../../CHAIN/etl/pipeline-ent-hang.md)（此处不复制全文）。

```text
python scripts/run_ent_chain_hang.py --self-check
python scripts/run_ent_chain_hang.py --apply   # 仅 demo_gkxlumenx_dwd
```

写 ENT `enterprise_industry_chain` + CHAIN `industry_chain_entity_rel`。`credit` 对不上 `org_id` 则 drop。不造整棵链、不改 `yiji_sim/infer*`。