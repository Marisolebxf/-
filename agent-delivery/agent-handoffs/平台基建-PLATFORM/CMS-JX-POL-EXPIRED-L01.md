# CMS-JX-POL-EXPIRED-L01 · 已失效政策列表（只读，集群内）

> **任务**：`CMS-JX-POL-EXPIRED-L01`（feature / P1 / CMS-JX-INT）
> **依据**：《CMS-JX接口规格书.md》v1.5 §2.1 只读回显注 + 老评估文档第二批接口 16 + 老设计单 CMS-JX-INT-DESIGN-L01 §5.2
> **代码**：lumen-svc-platform `gkxlumen-cms` commit `c18060c`

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强`（原单 human:淮政玮不空，2026-10-19 经监管人本人确认接管） |
| claim_type | pull |

## Ponytail

ponytail: `full`（复用 PolicyService/CmsEnvelope/信封分页惯例；无新依赖、无新表；DDL 未动）

## 交付

| 端点 | 行为 |
|------|------|
| `POST /api/open/cms/v1/policy/expired` | 已失效政策只读分页列表；body：`updated_after`(可选,增量) / `page` / `size`(≤200)；返回 `{total,page,size,records}`，record=`{id,title,expire_date,reason,update_time}` |

- **行集口径**：真源 `demo_gkxlumenx_dwd.policy_base_info` `status IN ('失效',2)`（双口径兼容，见 OPEN-1）∪ overlay 软删剔除（LEFT JOIN `cms_entity_overlay` POL）。虚拟政策（`cms:POL-%`）status 恒 NULL 不入列。
- **增量拉取**：`updated_after` 按真源 `update_time` 过滤——webhook（CMS-JX-POL-WEBHOOK-L01）失败时 CMS 次日 02:00 全量校对的兜底拉取口（老评估文档 §三 约定）。
- **reason 字段**：固定文案 `"失效"`（治理标记为唯一失效来源，真源无独立原因列；与 webhook body 契约 `reason:"失效"` 同文案）。
- **expire_date**：真源列直读，可空（19/48 失效行无到期日，治理标记失效但无日期场景返回 null）。
- **鉴权/前缀**：同模块 Api-Key filter（`/api/open/cms/v1/*`），集群内 ClusterIP，无 Ingress。

## 设计一致性（与既有 CMS-JX 实现对齐）

- 复用 `PolicyService` 的 StringBuilder where + args 分页模式（同 `list`/`auditLogs`）
- 标题 COALESCE overlay `$.title`（同 v_cms_pol 视角语义，真源∪覆盖）
- 真源表名硬编码 `demo_gkxlumenx_dwd`，同 `v_cms_pol` 视图与 auditLogs 标题回退链惯例；正式化随 `CMS_SOURCE_MYSQL_DB` 一处切
- 契约挂全量 OpenAPI `CMS-JX-OpenAPI-v1.0.json`（gen-openapi.py 已登记）；live 版此前因未实现被 PENDING 剔除——**本单合入后应移出 PENDING 集合并重生成 live 文档**（见 OPEN-2）

## 验证

- 编译：`mvn -pl gkxlumen-cms -am compile` 绿（本地离线）
- SQL 实测（10.50.11.76 真库，root 只读查询）：`status=2` 命中 48 行；TOP3 返回 id/title/expire_date 正常（POL202600577/POL202600571/POL202600552）
- utf8mb4 客户端验证中文标题无乱码
- CI/部署：push origin/dev `c18060c`，pipeline `backend:build` + `backend:image:cms` 由 CI 触发（见 GitLab pipeline）

## OPEN 项

1. **status 码值双口径**（登记待数据侧收口）：GDF 政策域 DDL 定稿 `status varchar(20)` 存「有效/失效」原文；当前 demo 库实际是 `bigint`（1=有效 552 行 / 2=失效 48 行，与 admin-ui M_POLICY_VALIDITY_RATE 公式 `status=1` 同口径）。代码 `IN ('失效',2)` 双兼容，正式库切 GDF DDL 后无需改代码；**需 data-agent/数据治理在正式化时统一**。同类隐患：`PolicyService.list` 的 `activeOnly` 只写 `status<>'失效'`，bigint 口径下过滤不生效（失效行仍出现在默认列表）——本单不扩范围，登记给 POL-CRUD 后续修。
2. **live OpenAPI 更新**：`gen-openapi.py` 的 PENDING 集合移除 `/policy/expired` 后重生成 live JSON + 久新 MD（下步动作，不阻塞本单验收）。

## 架构合规

✅ 纯 Java 读侧 / 真源只读 / Api-Key 集群内 / lumen 正式仓 origin/dev / 全 POST + body 无路径参数（动词铁律）

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~55000 |
| model_used | glm-5.3 (Cursor) |
| actual_cost | ~$0.6 |
| cost_warn | green |
