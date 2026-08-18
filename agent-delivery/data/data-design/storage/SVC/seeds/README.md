# SVC · seeds 覆盖样例索引

```yaml
---
doc_id: SVC-SEEDS-INDEX
element: SVC
role: source
status: draft
version: "2026-08-18"
updated: 2026-08-18
task: DEMO-SVC-A-RECLOSE-L01
---
```

> 少量样例，先闭环后性能。非第二套 DDL。ODS 口径见 [`../sources/inventory.md`](../sources/inventory.md)；主管道 [`../etl/pipeline-demo-mock.md`](../etl/pipeline-demo-mock.md)。

## 样本策略

| 原则 | 说明 |
|---|---|
| 机构主体 | **复用** ENT `run_llm_ods.py` / UI 灌数写入的 `demo_gkxlumenx_ods` 行；不另灌第二套主表 |
| 圈定 | Demo 临时规则允许，产出 **必须**标「待核验」；**不等于** Q-SVC-010 关闭 |
| 少而全 | 场景 × 数据特点最小集；具体 INSERT 可随 S3/灌数补 |

## 覆盖矩阵（骨架 · OPEN-SVC-FLOW-07）

| 场景 ID | 场景 | 数据特点（须覆盖） | 主要触达 | 脚本/入口 | 状态 |
|---|---|---|---|---|---|
| SEED-SVC-01 | 圈定命中 | 临时规则命中 ≥1 户；结果标 **待核验**（Q-SVC-010） | 本域圈定结果表 | `scripts/seed_svc_demo_mock.py` · batch `svc-mock-20260818` · 24 户 | **A-RECLOSE live** |
| SEED-SVC-02 | 圈定未命中 | 对照未入池（不写 SVC-MOCK 码） | 同上 | 脚本只灌命中池；未命中不插入 | 可验 |
| SEED-SVC-03 | 与 ENT 主体对齐 | ODS `dwd_org_base_info` 可对键 | `dwd_org_base_info` + 圈定 `org_id` | ENT `run_llm_ods` 样例 100 行 + MOCK `demo-proto-*` | ODS 100 行 live |
| SEED-SVC-04 | industry* 可读 | base 含文档 `industry*` 9 列 | `dwd_org_base_info` | `run_svc_ods_reconcile.py --check` | **aligned=true** |
| SEED-SVC-05 | 经营范围特征 | `main_activities` 非空 ≥1 | 产品表 → 临时圈定特征 | ENT offline 样例 | 待核验特征 |
| SEED-SVC-06 | 关系边 | 机构↔环节 / 机构↔机构 ≥1 | DWD rel 表 | `seed_svc_demo_mock.py` 写 `service_org_chain_rel` / `org_rel` | **A-RECLOSE live** |
| SEED-SVC-07 | 报告/对象 | 1 个导出对象（可选） | MinIO `demo_**` | 编排写桶（OPEN-SVC-FLOW-03） | 不替代业务表 |

### 待核验圈定样例（口径声明 · 非已批准）

```text
# 团队临时默认（Demo only · 待核验 · Q-SVC-010）
# 不得写入正式 ADS 契约为 live / approved
IF org 在 ENT 主体存在
  AND (
    industry* 命中服务类词典  OR  # 文档列；值质量不足时降级
    main_activities / business_scope 文本含服务类关键词  # 尽力而为
  )
THEN 纳入「服务机构候选池」并打标 pending_client_confirm
ELSE 未命中
```

**明确**：上框 = Demo 骨架说明，**不是**甲方+供方已批准的准入主路径。

## 禁止

- 用 seeds 伪闭合 Q-SVC-010（把临时圈定标成已批准准入）  
- 写正式 `gkxlumenx_*`  
- 为 SVC 另建机构主表样例冒充 ENT 主体  
