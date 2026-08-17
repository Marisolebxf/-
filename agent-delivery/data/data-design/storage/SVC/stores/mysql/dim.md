# MySQL DIM · 服务机构码表 / 对照（结构 draft）

```yaml
---
doc_id: SVC-STORE-DIM
element: SVC
role: store-mysql
status: draft
version: "2026-08-17"
updated: "2026-08-17"
engine: mysql
structure_task: DATA-SVC-STORAGE-DDL-L01
---
```

> **排除**：词典关键词内容、权重是否甲方批准。  
> **本文件只定**：枚举码、字典表落点、跨域唯一来源。

## 1. 六类 `service_type`（结构枚举 · Q-ALGO-006）

| 码 | 常量 | 中文（结构用名） |
|---|---|---|
| `FINANCE` | FINANCE | 金融服务 |
| `IP` | IP | 知识产权服务 |
| `HR` | HR | 人力资源服务 |
| `MKT` | MKT | 市场营销服务 |
| `CONSULT` | CONSULT | 咨询服务 |
| `INNOV` | INNOV | 科技创新服务 |

> 落库：建议 `gkxlumenx_dim.dim_svc_service_type`（code PK, name_cn, sort_no, is_active）。  
> **打标规则 / 关键词**另轨；本枚举仅约束列取值空间。

## 2. `verification_status`

| 码 | 含义 |
|---|---|
| `pending_client_confirm` | 待甲方确认（默认） |
| `accepted_temp` | 团队临时接受（仍非 live 契约） |
| `live` | 正式（**须 Q-SVC-010 关闭后**才允许写入） |
| `rejected` | 否决出池 |

## 3. 服务链环节字典

| 项 | 约定 |
|---|---|
| **唯一来源** | E7 生态叶子 `CHAIN_STAGES`（产品契约 CT-SVC-PT-01） |
| 本域用法 | `service_org_chain_rel.chain_stage_code` **只引用**，不在 SVC 另造第二套环节树 |
| 落库可选 | `dim_svc_chain_stage` 为只读镜像（同步自产品字典），禁止 SVC 私自改码 |

## 4. 其它

| 对象 | 库（常见） | 说明 |
|---|---|---|
| `cfg_metric` / lineage | `gkxlumenx_cfg` | `M_SVC_*` 八件套；口径另轨 |
| 行政区划 | 平台 DIM | 与 ENT 共用 |
| 圈定/打标 `rule_version` 注册 | cfg 可选表 | 只存版本元数据，不存规则正文 |

## 5. 禁止

业务 API 运行时改字典语义；六类码表外自由字符串写入 `service_type`。
