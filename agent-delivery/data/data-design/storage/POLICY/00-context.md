# 政策维存储 · 上下文与铁律

```yaml
---
doc_id: POLICY-STORAGE-CONTEXT
element: POLICY
role: context
status: draft
version: "2026-08-21"
updated: 2026-08-21
signoff_owner: human:淮政玮
task_id: DATA-POLICY-STORAGE-S1-L01
---
```

> **本单不建表、不灌数、不 APPLY、不改 `polan`。** 贴源结构见 [`sources/ods-ddl.md`](./sources/ods-ddl.md)（文档化三方表，不是项目 CREATE）。

## 1. Data Product 边界

- **域**：政策维（POLICY）= **一份存储、两扇窗口**  
  - **展示**：DS-10/11/12 + 核增 PC · 原型 `demo-ui-science` `pages/policy-tracking` · SRS `bid-reference/srs/02-科技信息展示系统/科技政策跟踪/`  
  - **专题 / 算法库**：E7 · `polan` · `demo-ui-system-test` `/policy` · `demo-ui-topic` `/policy`  
- **内**：政策 ODS→DWD→ADS；点/边 hang 一张 G；ADS 图镜像  
- **外**：功能 USM/交互；CHAIN 底图权威  
- **对照窗口**：[`windows/display-ds10-12.md`](./windows/display-ds10-12.md)（draft）  
- **现网联调台（算法库）**：`demo-ui-system-test` `/policy` → 网关 `gkx-policy` → `gkx-entan-py`。**不是**展示产品链（D12）  
- **现网原型（展示）**：`policy-tracking` **fixture**（`policyData.js`）。目标态经 Java 读同一 ADS

## 2. 铁律

1. 图谱 = **NebulaGraph** 一张 G：Demo **`demo_gkx_chain`**。禁止 Neo4j。  
2. **禁止**目标态独立 space `gkx_policy`；禁止 `DROP SPACE demo_gkx_chain`；禁止写入 `gkx_chain`。  
3. 关系库 = **MySQL**；禁止 PostgreSQL / `dwd.` PG schema 叙述。  
4. Java **只读 ADS**；不直连 nGQL。算法 Python 写 ADS / 投影 Nebula。  
5. 跨域 hang：政策 `policy_id` 与产业链 `industry_link_code` / 企业 `org_id` 对齐后再上图；对不齐则不造假边。展示行业筛与专题同一 hang。  
6. 现网 as-built（2026-08-21 Tempo）：图谱 API **只读** `demo_gkxlumenx_ads.policy_graph_node/edge`。目标态：Nebula 优先，ADS 镜像兜底；`source` 必须诚实。  
7. 展示与专题 **分轨路由、同一 ADS**。`policyData.js` 禁止当 live 源。

## 3. 与 CHAIN / ENT / SVC

| 关系 | 约定 |
|------|------|
| CHAIN | 底图权威；政策 **挂接投影**，不复制 `chain`/`segment` 本体 |
| ENT | 企业节点 hang `org_id`；不平行第二套企业图 |
| SVC | 服务机构 hang `institution`；政策边不替代 SVC 圈定 |

## 4. 下一步

1. 流图已会签；S2–S4 **文档闭环**（细表 draft）  
2. B 叶投影编码（`POLICY-NEBULA-PROJECT-CHAIN-L01`）对照 `stores/nebula.md`  
3. 灌数另开 SEED；本树不 APPLY DDL  
4. 展示缺口 OPEN-POLICY-DISP-* 另单，不平行建库  
