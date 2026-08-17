# SVC · seeds 覆盖样例索引

```yaml
---
doc_id: SVC-SEEDS-INDEX
element: SVC
role: source
status: draft
version: "2026-08-14"
updated: 2026-08-14
task: DATA-SVC-STORAGE-S2-L01
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
| SEED-SVC-01 | 圈定命中 | 临时规则命中 ≥1 户；结果标 **待核验**（Q-SVC-010） | 本域圈定结果表（S3） | 待 S3 Python 圈定作业；规则草案可读 `business_scope` / `main_activities` **尽力而为** | 骨架 · 不伪闭合 |
| SEED-SVC-02 | 圈定未命中 | 同批对照未命中 ≥1 户；仍标待核验 | 同上 | 同上 | 骨架 |
| SEED-SVC-03 | 与 ENT 主体对齐 | 同一 `org_id` / `external_id` 可对上 ENT ODS | `dwd_org_base_info` + 圈定 | ENT `run_llm_ods.py --offline` 已有样例户 | 可验 ODS 键 |
| SEED-SVC-04 | industry* 可读 | base 行含文档 `industry*` 列（可空值）；不因 live 三方缺列删列 | `dwd_org_base_info` | `run_svc_ods_reconcile.py --check` | S2 结构已齐 |
| SEED-SVC-05 | 经营范围特征 | `dwd_org_org_product_info.main_activities` 非空 ≥1 | 产品表 → 临时圈定特征 | ENT offline 样例 | 待核验特征 |
| SEED-SVC-06 | 关系边 | 机构↔环节 / 机构↔机构 ≥1 | 本域关系 / Nebula demo | S3 stores + 灌边 | 骨架 |
| SEED-SVC-07 | 报告/对象 | 1 个导出对象（可选） | MinIO `demo_**` | 编排写桶（待） | 不替代业务表 |

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
