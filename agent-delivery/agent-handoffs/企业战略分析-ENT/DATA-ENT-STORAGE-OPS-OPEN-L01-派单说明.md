# DATA-ENT-STORAGE-OPS-OPEN-L01 · 派单说明

> **日期**：2026-08-12  
> **Task ID**：`DATA-ENT-STORAGE-OPS-OPEN-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 落地 Owner**：`human:徐滕强`（认领时 `supervised_by=human:徐滕强`）  
> **执行 Agent**：`data-agent`（主）· 协作 `architect-agent` / `devops-agent`；**OPEN-01 须 GDF 出数**  
> **仓**：`gkx-orchestration`（`agent-delivery/data/data-design/storage/**`）  
> **合包逻辑**：最粗① — 流图仍开 **OPEN-ENT-FLOW-01~04** 一次关清  
> **强度**：ponytail **off**（定义/登记类，不以缩文档为目标）

---

## 1. 目标（一句话）

把 `01-data-flow.md` §5 中仍开的四项开放项落到文档真源并标 **已关闭**（或登记不可关原因 + 新 OPEN），不阻塞 Demo 灌数 UI。

---

## 2. 覆盖范围

| OPEN | 交付物 | 谁填 / 谁签 |
|---|---|---|
| **01** | GDF ODS→DWD / DWD→ADS：**cron、DAG 名、门禁脚本路径** → `etl/pipeline-ods-to-dwd.md` 等 | **GDF 填** · 徐滕强会签 |
| **02** | MinIO Endpoint / 默认 bucket / TTL / 凭证落点（**密钥不入库**）→ `platform/minio.md` | 平台/运维填 · 徐会签 |
| **03** | ENT 对象前缀 ↔ 任务表字段 → `etl/pipeline-to-minio.md`（与 02 一致） | data 整理 · 徐会签 |
| **04** | ES / Nebula 同步失败告警 + 重试次数 SLA → `stores/elasticsearch/sync.md`（及 Nebula 对口处） | data+算法拟稿 · 徐会签 |

回写：`storage/ENT/01-data-flow.md` §5 四行状态；`CHANGELOG.md` 一行。

---

## 3. 必读

| 序 | 路径 |
|---:|---|
| 1 | `storage/ENT/01-data-flow.md` §5 |
| 2 | `storage/platform/minio.md` |
| 3 | `storage/ENT/etl/pipeline-to-minio.md` |
| 4 | `storage/ENT/etl/pipeline-ods-to-dwd.md` |
| 5 | `storage/ENT/stores/elasticsearch/sync.md` |
| 6 | GDF 工作包指针：`data/GDF/派单包/企业/GDF-ENT-WORKPACK-v1/`（若可访问） |

---

## 4. DoD

- [ ] OPEN-01~04 文档字段齐套或明确延期 OPEN（须理由）
- [ ] §5 状态回写；无密钥明文入仓
- [ ] handoff：`…/DATA-ENT-STORAGE-OPS-OPEN-L01.md`
- [ ] `supervised_by=human:徐滕强` 确认后再签收链

---

## 5. 禁止

- 为关 OPEN 伪造未确认的 DAG/Endpoint  
- 把生产密钥写入 git  
- 借本单改 Demo 灌数代码（那是 `DEMO-ENT-UI-SEED-ODS-L01`）

---

## 6. 认领话术

```text
认领 DATA-ENT-STORAGE-OPS-OPEN-L01
claimed_by=agent:data-agent（或 human:徐滕强）
supervised_by=human:徐滕强
claim_type=pull
强度：ponytail off
目标：关闭 OPEN-ENT-FLOW-01~04 并回写流图 §5
```

---

**合包汇总**：[`ENT-STORAGE-COARSE-DISPATCH-2026-08-12.md`](./ENT-STORAGE-COARSE-DISPATCH-2026-08-12.md)
