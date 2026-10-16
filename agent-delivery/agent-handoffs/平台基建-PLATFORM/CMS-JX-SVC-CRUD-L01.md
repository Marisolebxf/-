# CMS-JX-SVC-CRUD-L01 · 服务机构实体写侧

> **任务**：`CMS-JX-SVC-CRUD-L01`（feature / P1）
> **依据**：《CMS-JX接口规格书.md》§3.1
> **代码**：lumen-svc-platform `gkxlumen-cms` commits `09c2b0b` + `0ad4cc2`（bugbot high 修复）

## 认领

| 字段 | 值 |
|------|-----|
| claimed_by | `agent:api-agent` |
| supervised_by | `human:徐滕强` |
| claim_type | pull |

## Ponytail

ponytail: `full`（复用 overlay 机制与 CmsErrors；圈定池只读不扩；无新依赖）

## 交付

| 端点 | 行为 |
|------|------|
| `POST /cms/v1/service-org/list` | 视图 `v_cms_svc`（圈定池∪虚拟，软删剔除）；keyword(name)/type/flag/priority + 分页钳制 |
| `POST /cms/v1/service-org/detail` | 详情（含回显 industry/province/city/area/org_size） |
| `POST /cms/v1/service-org/create` | 虚拟机构 `cms:SVC-{uuid8}`，name 必填；**圈定池 svc_org_circle 只读不扩** |
| `POST /cms/v1/service-org/update` | 9 字段白名单合并；requireVisible 防幽灵；软删行 404 |
| `POST /cms/v1/service-org/delete` | reason 必填 → 四路引用检查（svc_news.org_ids / svc_sz.org_id / kg_relation / expert_knowledge）40901 → 软删+审计 |

**bugbot high 修复**：`v_cms_svc` 补 `contact`/`ability` 投影（原写侧存 overlay、读侧无列=写后黑洞）；真源段补 `card.org_size`；`founded`/`phone_num` 真源无对应列（规格假设的 ODS 列名 demo 库不存在），NULL 占位保接口契约，**正式化切正式库时需对列**（偏差已记录）。

## 验证

- CI：pipelines 6545（09c2b0b）build+image:cms 绿；0ad4cc2 仅 DDL（无 Java 改动，live 已重建视图 18 列）
- 部署：Pod `gkxlumen-cms:09c2b0bc`
- 冒烟：list(total=43296)→create 虚拟→detail→update(虚拟 P0+真源 cert)→ghost 404→无 reason 40001→软删后 404；**回读专项**：contact/ability 写入后 detail+list 双回显 `ROUNDTRIP_OK`
- bugbot 复审：no bugs

## 架构合规

✅ 纯 Java CRUD / 圈定池与真源只读 / Api-Key / lumen 正式仓

## Cost

| 字段 | 值 |
|------|-----|
| actual_tokens | ~35000 |
| model_used | composer |
| actual_cost | ~$0.4 |
| cost_warn | green |
