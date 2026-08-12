# DEMO-ENT-DEMO-DB-TRIPLE-L01 · 派单说明

> **日期**：2026-08-13  
> **Task ID**：`DEMO-ENT-DEMO-DB-TRIPLE-L01`（registry · **ready**）  
> **派单人**：`human:淮政玮`  
> **监管 / 落地 Owner**：`human:徐滕强`  
> **执行 Agent**：`algorithm-agent` · 协作 `devops-agent` / `data-agent`（**建库需 root/DBA**）  
> **仓**：`demo-algo-ent-analysis` + 编排口径回写  
> **强度**：ponytail **full**  
> **关联**：建议作为 `DEMO-ENT-UI-SEED-ODS-L01` 的门禁/并行前置

---

## 1. 决策（已拍板）

**开发阶段一律使用 `demo_*` 三件套**，与真实 ODS 接入后的开发/测试**隔离**：

| 库 | 开发默认 | 禁止默认写入 |
|---|---|---|
| ODS | `demo_gkxlumenx_ods` | `gkxlumenx_ods` |
| DWD | `demo_gkxlumenx_dwd` | `gkxlumenx_dwd` |
| ADS | `demo_gkxlumenx_ads` | `gkxlumenx_ads` |

CFG（`gkxlumenx_cfg`）可暂共享。结构仍对齐 `stores/*`，**只隔离实例与数据**。

口径真源：`storage/ENT/etl/pipeline-demo-mock.md` §4（已回写本决策）。

---

## 2. 现状（2026-08-12 探测）

| 库 | 状态 |
|---|---|
| `demo_gkxlumenx_ods` | **已有**（P0 五表有少量样例） |
| `demo_gkxlumenx_dwd` | **无**；`gkxlumenx` 无 CREATE 权限 |
| `demo_gkxlumenx_ads` | **无**；同上 |
| 应用默认 | `settings.yaml` / K8s 仍指向真实 `gkxlumenx_dwd/ads` |

---

## 3. 交付步骤

1. **root/DBA** 执行：`scripts/mysql/create_demo_dbs.sql`（建库 + GRANT）  
2. **gkxlumenx** 执行：`scripts/mysql/demo_dwd_ads_schema_bootstrap.sql`（**仅结构**，48+7 表；**禁止**从真实库拷全量数据）  
3. 改默认：`conf/settings.yaml` · `deploy/k8s/*.yaml` · 清除/门控硬编码 `gkxlumenx_dwd`（如 `innov/analysis`）  
4. 冒烟：`run_llm_ods --offline` + mockgen/流水线写入 **仅** demo_*；确认真实三库行数不因 Demo 灌数暴增  
5. handoff + 探测摘录（`SHOW DATABASES` / 默认配置截图或日志）

---

## 4. 禁止

- 把 `gkxlumenx_ods` 全量当 Demo 数据源灌进 demo_*  
- 默写真实三库冒充 Demo  
- 密钥写入 git（建库用临时 root，会话结束废弃）  

---

## 5. 认领话术

```text
认领 DEMO-ENT-DEMO-DB-TRIPLE-L01
claimed_by=agent:algorithm-agent（或 human:徐滕强）
supervised_by=human:徐滕强
claim_type=pull
强度：ponytail full
目标：补齐 demo_ 三件套并切换开发默认，与真实 ODS 隔离
```

---

**建库若你（淮政玮）有 root**：可先本地执行 `create_demo_dbs.sql`，再让腾强改配置与灌数切换。
